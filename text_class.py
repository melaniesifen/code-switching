import pdftotext
import re
import mysql.connector
from fuck import ret

#with open("nameset.txt", "r") as names:
    #names = names.readlines


# analyze text from txt or pdf file
class Text(object):
    def __init__(self, file, title):
        self.file = file
        self.title = title
        self.pages = []
        if ".pdf" in self.file:
            with open(self.file, "rb") as self.pages:
                self.pages = pdftotext.PDF(self.pages)
        elif ".txt" in self.file:
            with open(self.file, "r") as self.pages:
                self.pages = [word for word in self.pages]
                    
        self.content = ""
        # define content by sentences using reg expression and punctuation as deliminators
        punctuation = [".", "!", "?"]
        punctuation = '|'.join(map(re.escape, punctuation))
        self.content = "".join(self.pages)
        self.content = "".join(item for item in self.content if item != "\n")
        self.content = self.content.lower()
        self.content = re.split(punctuation, self.content)
        # remove whitespace
        self.content = [item.strip() for item in self.content]
        
        # clean content
        remove_word = []
        acceptable_words = ["a", "i", "y", "o", "e"] # one letter words en and es
        content = []
        for sentence in self.content:
            for word in sentence.split():
                if len(word) <= 1 and word not in acceptable_words:
                    remove_word.append(word)
                if not word.isalpha():
                    remove_word.append(word)
                if len(word) != len(set(letter for letter in word)):
                    remove_word.append(word)
            sentence = " ".join(item for item in sentence.split() if item not in remove_word)
            # remove blank sentences
            if len(sentence) < 1:
                continue
            content.append(sentence)
        self.content = content 
        
        # creat dict
        keys = [i for i in range(1, len(self.content) + 1)]
        list_sentences = [sent for sent in self.content]
        list_lang = [None for i in range(len(self.content) + 1)]
        list_cs_reason = [None for i in range(len(self.content) + 1)]
        vals = [list(item) for item in zip(list_sentences, list_lang, list_cs_reason)]
        content_dict = dict(zip(keys, vals))
        self.content = content_dict
    
        
    # string representation
    def __str__(self):
        return self.title
    
    # number of pages in content
    def get_num_pages(self):
        if ".pdf" in self.file:
            return len(self.pages)
        return 1
        
    # number of sentences in content
    def get_num_sentences(self):
        return len(self.content)


        
class Database(object):
    def __init__(self, text):
        self.content = text.content
        self.table_name = text.title
        p = ret()
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = p,
            database='textdatabase' 
        )
        
        mycursor = mydb.cursor()
        table_name = self.table_name
        
        # remove table if already exists
        mycursor.execute("DROP TABLE IF EXISTS " + table_name)
        
        # create table for text
        mycursor.execute("CREATE TABLE " + table_name + " (sentence_number INT PRIMARY KEY, sentence TEXT, lang VARCHAR(7), cs_reason VARCHAR(10))")
        
        for key in self.content:
            sql = "INSERT INTO " + table_name + " (sentence_number, sentence, lang, cs_reason) VALUES (%s, %s, %s, %s)"
            sentence_number = key
            sentence = self.content[key][0]
            lang = self.content[key][1]
            cs_reason = self.content[key][2]
            val = (sentence_number, sentence, lang, cs_reason)
            mycursor.execute(sql, val)
            mydb.commit()

    
    
  
        


        
    
    
    
    
    