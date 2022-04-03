from langdetect import detect
from googletrans import Translator

#simple function to detect and translate text 
def detect_and_translate(text, target_lang):
    
    result_lang = detect(text)
    # print(result_lang)
    
    if result_lang == target_lang:
        return "" 
    
    else:
        translator= Translator()
        translation = translator.translate(text, src=result_lang, dest=target_lang)
        return translation.text