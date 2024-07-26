from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Initialize english grammar model
# donwload this model: https://huggingface.co/jasonlau/en-grammar-correction/tree/main in this maps
model_directory_grammar_en = r"./MODELS/grammar-en--jasonlau--en-grammar-correction"
tokenizer_grammar_en = AutoTokenizer.from_pretrained(model_directory_grammar_en)
model_grammar_en = AutoModelForSeq2SeqLM.from_pretrained(model_directory_grammar_en, local_files_only=True)

# Initialize rumanian grammar model
# donwload model: https://huggingface.co/BlackKakapo/t5-small-grammar-ro-root/tree/main in this map
model_directory_grammar_ro = r"./MODELS/grammar-ro--BlackKakapo--t5-small-grammar-ro-root"
tokenizer_grammar_ro = AutoTokenizer.from_pretrained(model_directory_grammar_ro)
model_grammar_ro = AutoModelForSeq2SeqLM.from_pretrained(model_directory_grammar_ro, local_files_only=True)


# EN
def grammar_text_en(text):
    input_text = f"grammar: {text}"
    input_ids = tokenizer_grammar_en(input_text, return_tensors='pt').input_ids
    outputs = model_grammar_en.generate(input_ids, max_new_tokens=150)
    final_text = tokenizer_grammar_en.decode(outputs[0], skip_special_tokens=True)

    return final_text


# RO
def grammar_text_ro(text):
    input_text = f"grammar: {text}"
    input_ids = tokenizer_grammar_ro(input_text, return_tensors='pt').input_ids
    outputs = model_grammar_ro.generate(input_ids, max_new_tokens=150)
    corrected_text = tokenizer_grammar_ro.decode(outputs[0], skip_special_tokens=True)

    def preserve_casing(original_text, corr_text):
        original_words = original_text.split()
        corrected_words = corr_text.split()
        final_words = []

        for original_word, corrected_word in zip(original_words, corrected_words):
            if original_word.isupper():
                final_words.append(corrected_word.upper())
            else:
                final_words.append(corrected_word)
        return ' '.join(final_words)
    final_text = preserve_casing(text, corrected_text)

    return final_text
