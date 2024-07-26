from transformers import AutoTokenizer, FSMTForConditionalGeneration, AutoModelForSeq2SeqLM


# Initialize ro-en translator model
#  donwload model: https://huggingface.co/inseq/wmt20-mlqe-ro-en/tree/main in this map
model_dir_ro_en = r"./MODELS/translate-ro-en--wmt20-mlqe"

tokenizer_ro_en = AutoTokenizer.from_pretrained(model_dir_ro_en)
model_ro_en = FSMTForConditionalGeneration.from_pretrained(model_dir_ro_en)

# Initialize en-ro translator model
# donwload model: https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-ro in this map
model_dir_en_ro = r"./MODELS/translate-en-ro--Helsinki-NLP--opus-mt-tc-big-en-ro"
tokenizer_en_ro = AutoTokenizer.from_pretrained(model_dir_en_ro)
model_en_ro = AutoModelForSeq2SeqLM.from_pretrained(model_dir_en_ro)


# RO - EN
def translate_text_ro_en(text, num_beams=5, max_length=60, length_penalty=1.0, early_stopping=True):
    # Dicționar de traduceri personalizate
    custom_translations = {
        "MOMENTE CHEIE - RISC OPERAȚIONAL": "KEY MOMENTS - OPERATIONAL RISK",
        "RETAIL: INDICATORI - POLITICA DE CREDITARE": "RETAIL: CREDIT POLICY TRIGGERS",
        "BUSINESS BANKING: DINAMICA DE MIGRARE PORTOFOLIULUI DE CREDITE ÎN FUNCȚIE DE GRUPUL DPD": "BUSINESS BANKING: LOAN PORTFOLIO MIGRATION BY DPD BUCKET ",
        "CORPORATE : INDICATORI - POLITICA DE CREDITARE": "CORPORATE: CREDIT POLICY TRIGGERS",
        "CORPORATE: DINAMICA DE MIGRARE PORTOFOLIULUI DE CREDITE ÎN FUNCȚIE DE GRUPUL DPD": "CORPORATE: LOAN PORTFOLIO MIGRATION BY DPD BUCKET",
        "INDICATORI DE RISC DE LICHIDITATE": "LQ RISK INDICATORS",
        "RISC DE RISC DE LICHIDITATE, EWS": "LQ RISK INDICATORS, EWS",
        "RISC FINANCIAR: RISCUL DE PIAȚĂ": "FINANCIAL RISKS: FX RISK",
        "RISCURI FINANCIARE: RISCUL DE ȚARĂ ȘI CONTRAPARTE – BĂNCI CORESPONDENTE, LIMITE": "FINANCIAL RISKS: COUNTRY AND COUNTERPARTY RISK- Correspondent banks, limits",
        "RISCURI OPERAȚIONALE: KRI - SUMAR": "OPERATIONAL RISK: KRI - SUMARY",
        "PRIN CANALE DIGITALE": "THROUGH DIGITAL CHANNELS "
        # ....
    }

    def custom_translation_fixes(text):
        return custom_translations.get(text, text)

    # Aplicarea regulilor personalizate înainte de traducere
    fixed_text = custom_translation_fixes(text)
    if fixed_text != text:
        return fixed_text

    # AI Translate to English
    inputs = tokenizer_ro_en(text, return_tensors="pt", truncation=True)
    translated_text = model_ro_en.generate(
        **inputs,
        num_beams=num_beams,
        max_length=max_length,
        length_penalty=length_penalty,
        early_stopping=early_stopping
    )
    final_text = tokenizer_ro_en.decode(translated_text[0], skip_special_tokens=True)
    #print(f"Translated text (before correction): {text_en[:40]}")  # Added for debugging

    return final_text


# EN - RO
def translate_text_en_ro(text):
    inputs = tokenizer_en_ro(text, return_tensors="pt", truncation=True)
    translated_text = model_en_ro.generate(**inputs)
    final_text = tokenizer_en_ro.decode(translated_text[0], skip_special_tokens=True)
    return final_text
