import re
from datetime import datetime, timedelta

def change_date(text):
    text = text.replace('/', '.')
    text = text.lower()

    # check the format of publication_date ant transform it from text to number
    patern_minut = r"acum 1 minut"
    pattern_minute = r"acum (\d+) minute"
    pattern_de_minute = r"acum (\d+) de minute"
    patern_ora = r"acum 1 oră"
    pattern_o_ora = r"acum o oră"
    pattern_ore = r"acum (\d+) ore"
    pattern_de_ore = r"acum (\d+) de ore"
    patern_zi = r"acum 1 zi"
    patern_o_zi = r"acum o zi"
    pattern_zile = r"acum (\d+) zile"
    pattern_saptamana = r"acum o săptămână"
    pattern_saptamani = r"acum (\d+) săptămâni"
    pattern_o_luna = r"acum o lună"

    match_minut = re.search(patern_minut, text)
    match_minute = re.search(pattern_minute, text)
    match_de_minute = re.search(pattern_de_minute, text)
    match_o_ora = re.search(pattern_o_ora, text)
    match_ora = re.search(patern_ora, text)
    match_ore = re.search(pattern_ore, text)
    match_de_ore = re.search(pattern_de_ore, text)
    match_zi = re.search(patern_zi, text)
    match_o_zi = re.search(patern_o_zi, text)
    matches_zile = re.findall(pattern_zile, text)
    match_saptamana = re.search(pattern_saptamana, text)
    matches_saptamani = re.findall(pattern_saptamani, text)
    match_o_luna = re.search(pattern_o_luna, text)

    if matches_zile:
        numar_zile = int(matches_zile[0])
        data_modificata = datetime.now() - timedelta(days=numar_zile)
        return data_modificata.strftime("%d.%m.%Y")
    elif match_zi:
        data_modificata = datetime.now() - timedelta(days=1)
        return data_modificata.strftime("%d.%m.%Y")
    elif match_o_zi:
        data_modificata = datetime.now() - timedelta(days=1)
        return data_modificata.strftime("%d.%m.%Y")
    elif match_o_luna:
        data_modificata = datetime.now() - timedelta(days=30)
        return data_modificata.strftime("%d.%m.%Y")
    elif match_saptamana:
        data_modificata = datetime.now() - timedelta(days=7)
        return data_modificata.strftime("%d.%m.%Y")
    elif matches_saptamani:
        numar_saptamani = int(matches_saptamani[0])
        data_modificata = datetime.now() - timedelta(weeks=numar_saptamani)
        return data_modificata.strftime("%d.%m.%Y")
    elif match_minut:
        # For "Acum [număr] minute", return current date
        return datetime.now().strftime("%d.%m.%Y")
    elif match_minute:
        # For "Acum [număr] minute", return current date
        return datetime.now().strftime("%d.%m.%Y")
    elif match_de_minute:
        # For "Acum [număr] de minute", return current date
        return datetime.now().strftime("%d.%m.%Y")
    elif match_ora:
        # For "Acum o oră", return current date
        return datetime.now().strftime("%d.%m.%Y")
    elif match_o_ora:
        # For "Acum o oră", return current date
        return datetime.now().strftime("%d.%m.%Y")
    elif match_ore:
        # For "Acum [număr] ore", return current date
        return datetime.now().strftime("%d.%m.%Y")
    elif match_de_ore:
        # For "Acum [număr] ore", return current date
        return datetime.now().strftime("%d.%m.%Y")
    else:
        # convert month from text to int
        month_dict = {
            'ian.': '01',
            'feb.': '02',
            'mart.': '03',
            'mar.': '03',
            'apr.': '04',
            'mai': '05',
            'iun.': '06',
            'iul.': '07',
            'aug.': '08',
            'sept.': '09',
            'oct.': '10',
            'nov.': '11',
            'dec.': '12',
            'ianuarie': '01',
            'februarie': '02',
            'martie.': '03',
            'martie': '03',
            'aprilie': '04',
            'mai.': '05',
            'iunie': '06',
            'iulie': '07',
            'august': '08',
            'septembrie': '09',
            'octombrie': '10',
            'noiembrie': '11',
            'decembrie': '12',
        }

        current_year = datetime.now().year

        def replace_month(match):
            day, month, year = match.groups()
            if len(day) == 1:
                day = '0' + day
            if year is None:
                return f'{day}.{month_dict[month]}.{current_year}'
            return f'{day}.{month_dict[month]}.{year}'

        date_regex = r'(\d{1,2}) (\w+\.?) (\d{4})'
        return re.sub(date_regex, replace_month, text)

# Test
# text1 = "acum 5 ore"
# text2 = "02 mart. 2023"
#
# data_modificata1 = change_date(text1)
# data_modificata2 = change_date(text2)
#
# print(data_modificata1)
# print(data_modificata2)
