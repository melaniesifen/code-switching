import pdftotext
import re
import mysql.connector
from fuck import ret

with open("dictionaries/nameset.txt", "r") as names:
    names = names.read().split()

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
        asc = []
        for sentence in self.content:
            sentence = sentence.split()
            for word in sentence:
                if len(word) <= 1 and word not in acceptable_words:
                    remove_word.append(word)
                if not word.isalpha():
                    remove_word.append(word)
                if word in names:
                    remove_word.append(word)
                if word == None or word.isspace():
                    remove_word.append(word)
                if len(word) != len(set(letter for letter in word)):
                    remove_word.append(word)
            sentence = " ".join(item for item in sentence if item not in remove_word)
            # remove blank sentences
            if len(sentence) < 1 or sentence == None or sentence.isspace():
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
        print("done")
    
        
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
    
    def get_content(self):
        for key in self.content:
            print(self.content[key][0])
        
        
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
        mycursor.execute("CREATE TABLE " + table_name + " (sentence_number INT PRIMARY KEY, sentence TEXT, lang VARCHAR(7), cs_reason VARCHAR(15))")
        
        for key in self.content:
            sql = "INSERT INTO " + table_name + " (sentence_number, sentence, lang, cs_reason) VALUES (%s, %s, %s, %s)"
            sentence_number = key
            sentence = self.content[key][0]
            lang = self.content[key][1]
            cs_reason = self.content[key][2]
            val = (sentence_number, sentence, lang, cs_reason)
            mycursor.execute(sql, val)
            mydb.commit()
            
    def get_results(self):
        p = ret()
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = p,
            database='textdatabase' 
        )
        
        mycursor = mydb.cursor()
        
        mycursor.execute("CREATE TABLE cs_results (title varchar(80), lexical DECIMAL(5, 2), emphasis DECIMAL(5, 2), style DECIMAL(5, 2), quote DECIMAL(5, 2);")
        
        sql = "select table_name from information_schema.tables where table_schema = 'textdatabase' and table_name != 'cs_results';"
        mycursor.execute(sql)
        all_tables = mycursor.fetchall()
        all_tables_list = []
        percentages = dict()
        
        for name in all_tables:
            name = "".join(ch for ch in name)
            all_tables_list.append(name)
            
        for table_name in all_tables_list:
            both_lang = "select count(lang) from " + table_name + " where lang = 'both';"
            mycursor.execute(both_lang)
            both_lang_count = mycursor.fetchall()
            both_lang_count = both_lang_count[0][0]
            lexical = "select count(cs_reason) from " + table_name + " where cs_reason = 'lexical need';"
            mycursor.execute(lexical)
            lexical_count = mycursor.fetchall()
            lexical_count = lexical_count[0][0]
            emphasis = "select count(cs_reason) from " + table_name + " where cs_reason = 'emphasis';"
            mycursor.execute(emphasis)
            emphasis_count = mycursor.fetchall()
            emphasis_count = emphasis_count[0][0]
            style = "select count(cs_reason) from " + table_name + " where cs_reason = 'style';"
            mycursor.execute(style)
            style_count = mycursor.fetchall()
            style_count = style_count[0][0]
            quote = "select count(cs_reason) from " + table_name + " where cs_reason = 'quote';"
            mycursor.execute(lexical)
            quote_count = mycursor.fetchall()
            quote_count = quote_count[0][0]
            percentages[table_name] = [round(lexical_count/both_lang_count, 2)*100, 
                                       round(emphasis_count/both_lang_count, 2)*100, 
                                       round(style_count/both_lang_count, 2)*100,
                                       round(quote_count/both_lang_count, 2)*100]
            
        for table_name in percentages:
            sql = "INSERT INTO cs_results (title, lexical, emphasis, style, quote) VALUES (%s, %s, %s, %s, %s)"
            title = table_name
            lexical = percentages[table_name][1]
            emphasis = percentages[table_name][2]
            style = percentages[table_name][3]
            quote = percentages[table_name][4]
            val = (title, lexical, emphasis, style, quote)
            mycursor.execute(sql, val)
            mydb.commit()
        
        
        

    
    
  
        


        
    
    
    
    
    