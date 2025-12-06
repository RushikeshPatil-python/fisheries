from translate import Translator

translator = Translator(from_lang="en", to_lang="mr-IN")

def to_marathi(text):
    try:
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text
