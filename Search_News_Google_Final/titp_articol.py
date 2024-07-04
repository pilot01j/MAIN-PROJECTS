import time
import g4f
from g4f.errors import RetryProviderError
import asyncio
import ollama
from openai import OpenAI




def ask_gpt_4(promt: str) -> str:
    time.sleep(6)
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
            time.sleep(6)

def ask_ollama(question):
    response = ollama.generate(model='llama3', prompt=f"{question}")
    return response.lower()


# Example: reuse your existing OpenAI setup

def ask_lm_studio(question):
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": "Always answer in rhymes."},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
    )

    response_content = completion.choices[0].message.content  # Access the content attribute correctly
    return response_content.lower()


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
            gpt_result = ask_lm_studio(f'raspunde scurt daca stirea "{title}" este pozitiva, negativa sau neutru.')

            article_type = check_word(str(gpt_result).lower())
            check_status = False
            return article_type

        except RetryProviderError:
            print("RetryProviderError occurred in add_tip_articol. Retrying...")
            time.sleep(6)


