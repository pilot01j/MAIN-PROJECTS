import re
from datetime import datetime, timedelta


def change_date(text):
    text = text.replace('/', '.')

    # check the format of publication_date ant transform it from text to number

    pattern_minute = r"Acum (\d+) de minute" or r"acum (\d+) ore" or r"Acum o oră" or r"Acum (\d+) ore"
    patern_o_zi = r"Acum o zi"
    pattern_zile = r"Acum (\d+) zile"
    pattern_saptamana = r"Acum o săptămână"
    pattern_saptamani = r"Acum (\d+) săptămâni"
    pattern_o_luna = r"Acum o lună"

    match_minute = re.search(pattern_minute, text)
    match_zi = re.search(patern_o_zi, text)
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
    elif match_minute:
        # For "Acum [număr] de minute", return current date
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
# text1 = "acum 5 zile"
# text2 = "02 mart. 2023"
#
# data_modificata1 = modificare_data(text1)
# data_modificata2 = modificare_data(text2)
#
# print(data_modificata1)
# print(data_modificata2)
