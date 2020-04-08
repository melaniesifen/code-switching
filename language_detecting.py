from text_class import Text, Database
from googletrans import Translator
import time
import goslate

with open("common_english.txt", "r") as eng:
    eng = eng.read().split()
    
with open("common_spanish.txt", "r") as span:
    span = span.read().split()
    
def run_file(my_file, title):
    text = Text(my_file, title)
    detect_language(text.content)
    createdb = Database(text)
    #write_analysis(text_to_analyze, w)
        
def detect_language(content):
    for key in content:
        sentence = content[key][0]
        language = detect_by_cache(sentence)
        if language != None:
            content[key][1] = language
            if language == "both":
                categorize(sentence)
            continue
        language = detect_by_google(sentence)
        content[key][1] = language
        categorize(sentence)
        
def detect_by_cache(sentence):
    if all(word in eng for word in sentence.split()):
        return "en"
    elif all(word in span for word in sentence.split()):
        return "es"
    elif all((word in eng) or (word in span) for word in sentence.split()):
        return "both"
    return None
        
def detect_by_google(sentence):
    translator = Translator()
    language, confidence = translator.detect(sentence)
    if confidence < .98:
        return "both"
    return language

def detect_by_api(sentence):
    gs = goslate.Goslate()
    language = gs.detect(sentence)

def categorize(sentence):
    # emphasis or clarification, lexical need, quoting, style
    # if 2 or fewer words in one lang, lexical need
    # if quotes, quoting
    # if words are self-translating, emphasis or clafification
    if is_self_translating(sentence):
        return "emphasis"
    # style
    pass
def is_self_translating(sentence):
    translator = Translator()
    is_self_translating = False
    sentence_en = translator.translate(sentence, "en", "en")
    for word in sentence_en.split():
        pass
        
        
    
def main():
    #my_file = input("name of file: ")
    #title = input("Title: ")
    my_file = "Wao1.pdf"
    title = "Wao"
    run_file(my_file, title)
    


start_time = time.time()  
main()
print("--- %s seconds ---" % (time.time() - start_time))
