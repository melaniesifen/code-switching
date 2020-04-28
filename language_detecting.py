print("Allow 15 seconds for imports...")
from text_class import Text, Database
from googletrans import Translator
from wn import WordNet
from wn.info import WordNetInformationContent
from wn.constants import wordnet_30_dir
from itertools import chain

wordnet = WordNet(wordnet_30_dir)
translator = Translator()

with open("dictionaries/common_english.txt", "r") as eng:
    eng = eng.read().split()
    
with open("dictionaries/common_spanish.txt", "r") as span:
    span = span.read().split()
    
with open("dictionaries/say.txt", "r") as say:
    say = say.read().split()
    
with open("dictionaries/exceptions.txt", "r") as exceptions:
    exceptions = exceptions.read().split()
    
# read input file and title and create text object and database    
def run_file(my_file, title):
    # create text object
    print("cleaning data")
    text = Text(my_file, title)
    #detect language of each sentence
    print("analyzing sentences")
    num_sentences = text.get_num_sentences()
    if ".pdf" in my_file:
        print("this may take up to ", int(num_sentences*0.05), " seconds...")
    detect_language(text.content)
    print("done")
    categorize(text.content)
    #create table in textdatabase
    print("creating database")
    createdb = Database(text)
    #write_analysis(text_to_analyze, w)

# detect language of each sentence
def detect_language(content):
    # iterate through sentences in text and determine language
    for key in content:
        sentence = content[key][0]
        language = detect_by_cache(sentence)
        if language != None:
            content[key][1] = language
            continue
        language = detect_by_google(sentence)
        content[key][1] = language
        
# detect language of sentence via cache 
def detect_by_cache(sentence):
    if all(word in eng for word in sentence.split()):
        return "en"
    elif all(word in span for word in sentence.split()):
        return "es"
    elif all((word in eng) or (word in span) for word in sentence.split()):
        return "both"
    return None

def categorize_by_cache(word):
    if word in eng and word not in span:
        return "en"
    elif word in span and word not in eng:
        return "span"
    elif word in eng: # both
        return "both"
    else:
        return "not in cache"
        

# detect language of sentence via API    
def detect_by_google(sentence):
    language, confidence = translator.detect(sentence)
    if confidence < .99:
        return "both"
    return language

# categorize code-switching
def categorize(content):
    for key in content:
        sentence = content[key][0]
        if content[key][1] != "both":
            continue
        print("categorizing code-switch in sentence ", key)
        if is_quote(sentence):
            content[key][2] = "quote"
        elif is_self_translating(sentence):
            content[key][2] = "emphasis"
        elif is_lexical(sentence):
            content[key][2] = "lexical need"
        else:
            content[key][2] = "style"
    
# code-swithcing for lexical need
def is_lexical(sentence):
    # if number of code-switches <= 20% of sentence then it is lexical
    count_en = 0
    count_es = 0
    l = len(sentence.split())
    check = []
    if l <= 2:
        return False
    for word in sentence.split():
        language = categorize_by_cache(word)
        if language == "en" or language == "es":
            if language == "en":
                count_en += 1
            else:
                count_es += 1
            if l < 12 and count_en >= 2 and count_es >= 2:
                    return False
            else:
                if count_en >= 3 and count_es >= 3:
                    return False
        elif language == "both":
            check.append(word)
    if check:      
        i = len(check)
        if l < 12 and ((count_en + i) >= 2 and count_es >= 2):
            return False
        elif l < 12 and (count_en >= 2 and (count_es + i) >= 2):
            return False
        elif l >= 12 and ((count_en + i) >= 3 and count_es >= 3):
            return False
        elif l >= 12 and (count_en >= 3 and (count_es + i) >= 3):
            return False
    if l < 12:
        if count_en >= 2 and count_es > 1:
            return False
        elif count_en > 1 and count_es >= 2:
            return False
    else:
        if count_en >= 2 and count_es > 2:
            return False
        elif count_en > 2 and count_es >= 2:
            return False
            
    return True

# code-switching for quote
def is_quote(sentence):
    for word in sentence.split():
        if word in say:
            return True
    return False

# code-switching for emphasis/clarification
def is_self_translating(sentence):
    sentence_en = []
    check = []
    # remove words in exceptions
    # create new sentence without duplicate english words and duplicate spanish words
    sentence = set(word for word in sentence.split() if word not in exceptions)
    sentence = " ".join(word for word in sentence)
    try:
        sentence_en = translate_short(sentence)
    except:
        sentence = "".join(ch for ch in sentence if ord(ch) < 128)
        try:
            sentence_en = translate_short(sentence)
        except:
            return False
    sentence_en = str(sentence_en)
    for word in sentence_en.split():
        if sentence_en.count(word) > 1:
            return True
        word_list = wordnet.synsets(word)
        syn = []
        for item in word_list:
            item = str(item)
            item = item[8:-2]
            syns = wordnet.synset(item).lemma_names()
            syn.append(syns)
        syn = list(chain.from_iterable(syn))
        syn = set(syn)
        count = 0
        for item in sentence_en:
            if item in syn:
                count += 1
            if count > 1:
                return True
    return False

# translate word in sentence using API               
def translate_short(item):
    item_en = translator.translate(item, "en", "es")
    return item_en
