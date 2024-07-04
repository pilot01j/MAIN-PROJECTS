import requests
import pandas as pd
import pyodbc
import warnings
import os
from datetime import datetime
from shutil import copyfile
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ssl
from system_proxy import get_system_proxy


# ----------------------CONSTANTELE-------------------------------------------------------------
server = 'tar2.sql.maib.local'
database = 'InsightDataTemp'
driver = '{ODBC Driver 17 for SQL Server}'
file_path = r'C:\Users\Marin.M.Mucuta\My_Python\Companii_GovMD\company.xlsx'
url = "https://dataset.gov.md/dataset/a1f38191-f35c-4180-8d80-297851a08f60/" \
      "resource/68f16467-5974-47c7-bb51-62ef4d321ed5/download/company.xlsx"

# --------------------Suprimarea cerintelor HTTPS-----------------------------------------------
warnings.simplefilter('ignore', InsecureRequestWarning)

# --------------------Configurarea conexiunii proxy----------------------------------------------
proxies = get_system_proxy()

# --------------------Contectarea la Baza de Date-----------------------------------------------
conn = pyodbc.connect(f'Driver={driver};'
                      f'Server={server};'
                      f'Database={database};'
                      f'Trusted_Connection=yes;')

cursor = conn.cursor()


# --------------------Inlocuirea caracterelor-------------------------------------------------------
def replace_special_chars(text):
    if isinstance(text, str):
        replace_dict = {
            'ș': 's', 'ț': 't', 'ă': 'a', 'î': 'i', 'â': 'i',
            'Ș': 'S', 'Ț': 'T', 'Ă': 'A', 'Î': 'I', 'Â': 'I'
        }
        for char, repl in replace_dict.items():
            text = text.replace(char, repl)
    return text


# --------------------Curatarea denumirea coloanelor-----------------------------------------------
def clean_column_name(name):
    name = replace_special_chars(name)
    name = name.strip()
    name = name.replace(' ', '_')
    name = name.replace('./', '_')
    name = name.replace('/', '_')
    name = ''.join(c for c in name if c.isalnum() or c == '_')
    if name[0].isdigit():
        name = '_' + name
    return name


# --------------------Determinarea nr de caractere p.u fiecare coloana---------------------------
def get_max_length(column):
    max_len = column.astype(str).str.len().max()
    # Adăugăm o marjă de siguranță și rotunjim la cel mai apropiat multiplu de 10
    return min(max(int(max_len * 1.2 // 10 + 1) * 10, 50), 4000)


# --------------------Descarcarea a fisierului xlsx----------------------------------------------
def download_and_verify_file(url_, file_path_, proxies_=None):
    # stergem fisierul vechi daca exista
    if os.path.exists(file_path_):
        os.remove(file_path_)
        print(f"Fisierul {file_path_} a fost sters cu succes!")

    session = requests.Session()
    session.ssl_version = ssl.PROTOCOL_TLSv1_2
    response = session.get(url_, verify=False, proxies=proxies_)
    with open(file_path_, 'wb') as file:
        file.write(response.content)
    pd.read_excel(file_path_, sheet_name='Company', header=None, engine='openpyxl')  # check if is Excel
    print(f"Fisierul {file_path_} a fost descarcat si verificat cu succes!")
    return True


if not download_and_verify_file(url, file_path, proxies):
    print("Nu s-a putut procesa fișierul. Programul se oprește.")
    exit()

# --------------------Perfectarea datelor din fisierul descarcat----------------------------------
# Citește fisierul XLSX și extrage prima foaie
df = pd.read_excel(file_path, sheet_name='Company', header=None, engine='openpyxl')

# Extragem data din textul specificat în rindul 0, coloana 3
date_text = df.iloc[0, 3]
date_str = date_text.split("starea la ")[-1].strip(")").strip()
Data_Stare = datetime.strptime(date_str, "%d.%m.%Y").date()

# Extragem denumirile coloanelor din rindul 2 și datele de la rindul 3
columns = [clean_column_name(col) for col in df.iloc[1].tolist()]
df = df.iloc[2:].reset_index(drop=True)
df.columns = columns

# Aplică funcția de inlocuire pe fiecare valoare din fiecare coloană
for col in df.columns:
    df[col] = df[col].apply(replace_special_chars)

# Modificam toate coloanele la tip object la string
df = df.astype(object)

# Adaugam doua coloane suplimentare dacă nu există deja
if 'Data_Stare' not in df.columns:
    df['Data_Stare'] = Data_Stare
if 'Data_Import ' not in df.columns:
    df['Data_Import '] = datetime.now().date()

# Converteste datele din coloanele la formatul date (YYYY-MM-DD)
if len(df.columns) > 11:
    col_10_name = df.columns[10]
    if col_10_name in df.columns:
        df[col_10_name] = pd.to_datetime(df[col_10_name]).dt.date

    col_1_name = df.columns[1]
    if col_1_name in df.columns:
        df[col_1_name] = pd.to_datetime(df[col_1_name]).dt.date

# Înlocuiește NaN cu None
df = df.where(pd.notnull(df), None)


# --------------------Copiazam fișierul descarcat în noua locație si-l redenumim--------------------
new_file_name = f"Company_{date_str.replace('.', '_')}.xlsx"
new_file_path = os.path.join(r'V:\$Flux\Watch_List\GovMD_Company', new_file_name)
copyfile(file_path, new_file_path)
print(f"Fisierul a fost copiat în {new_file_path}")


# --------------------Crearea si inserarea daelor in Baza de Date----------------------------------
# Creem un dictionar cu lungimile maxime pentru fiecare coloana
column_lengths = {col: get_max_length(df[col]) for col in df.columns}

# Creem un tabelul în SQL Server folosind denumirile coloanelor curatate și lungimile determinate
create_table_sql = '''
IF OBJECT_ID('[InsightDataTemp].[DASRC].GovMD_Company', 'U') IS NOT NULL
    DROP TABLE [InsightDataTemp].[DASRC].GovMD_Company;
CREATE TABLE [InsightDataTemp].[DASRC].GovMD_Company (
    {}
);
'''.format(', '.join([f'[{col}] NVARCHAR({column_lengths[col]})' for col in df.columns]))

cursor.execute(create_table_sql)
conn.commit()

# Inserem datele în tabelul creat
for index, row in df.iterrows():
    # Convertește toate valorile la string, cu excepția None și aplicăm limitarea la 4000 de caractere
    values = [val[:4000] if isinstance(val, str) and len(val) > 4000 else val for val in row]

    placeholders = ', '.join(['?' for _ in values])
    columns = ', '.join([f'[{col}]' for col in df.columns])

    query = f'''
    INSERT INTO [InsightDataTemp].[DASRC].GovMD_Company ({columns})
    VALUES ({placeholders});
    '''

    cursor.execute(query, values)

    if index % 1000 == 0:
        conn.commit()
        print(f"Inserate {index} rânduri...")

conn.commit()
cursor.close()
conn.close()

print("Datele au fost importate cu succes!")
