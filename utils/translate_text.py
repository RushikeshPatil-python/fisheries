import requests
from translate import Translator

translator = Translator(from_lang="en", to_lang="mr-IN")

def to_marathi(text):
    try:
        print("Text: ", text)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def translate_to_marathi(text):
    endpoint = f"https://api.mymemory.translated.net/get?langpair=en|mr-IN&q={text}&de=shubhamchougale1@gmail.com"
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            translated_text = data['responseData']['translatedText']
            if translated_text:
                return translated_text
            matches = data['matches']
            if matches:
                next_best_match = next(match for match in matches)
                return next_best_match['translation']
        else:
            print(f"Translation API error: {response.status_code}")
            return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def update_translation(text, trans):
    endpoint = f"https://api.mymemory.translated.net/set?seg={text}&tra={trans}&langpair=en|mr-IN&de=shubhamchougale1@gmail.com"
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Translation API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Translation error: {e}")
        return None
