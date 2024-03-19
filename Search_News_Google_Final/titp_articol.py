import time
import g4f
from g4f.errors import RetryProviderError


def ask_gpt_4(promt: str) -> str:
    check_status = True
    while check_status:
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": promt}],
                max_tokens=1
            )
            check_status = False
            return response.lower()
        except RetryProviderError:
            print("RetryProviderError occurred in ask_gpt_4. Retrying...")
            time.sleep(3)


# Verificăm dacă șirul conține cuvântul "negativ"
def check_word(text):
    text = text.lower()

    if 'negativ' in text:
        return 'negativ'
    elif 'pozitiv' in text:
        return 'pozitiv'
    else:
        return 'neutru'


def add_tip_articol(title, company_name):
    check_status = True
    while check_status:
        try:
            gpt_result = ask_gpt_4(
                    f"răspunde doar cu cuvintele 'negativ' sau 'pozitiv' , dacă următorul articol : '{title}' "
                    f"este pozitiv sau negativ despre compania {company_name}, "
                    f"nu scrie ca ai analizat articolul, nu scrie cum a fost analizat articolul, "
                    f"nu scrie motivul alegeri, nu scrie despre rezultatele comaniei , "
                    f"nu scrie nimic inafara de cuvintele pozitiv sau negativ.")
            time.sleep(3)
            article_type = check_word(str(gpt_result).lower())
            check_status = False
            return article_type

        except RetryProviderError:
            print("RetryProviderError occurred in add_tip_articol. Retrying...")
            time.sleep(3)


