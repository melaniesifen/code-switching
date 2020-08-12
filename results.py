from text_class import Database
from secrets import secret
import mysql.connector

def get_results():
        p = secret()
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = p,
            database='textdatabase' 
        )
        
        mycursor = mydb.cursor()
        mycursor.execute("DROP TABLE IF EXISTS cs_results;")
        mycursor.execute("CREATE TABLE cs_results (title varchar(80), lexical DECIMAL(5, 2), emphasis DECIMAL(5, 2), style DECIMAL(5, 2), quote DECIMAL(5, 2));")
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
            if both_lang_count == 0:
                percentages[table_name] = [0, 0, 0, 0]
                continue
                
            lexical = "select count(cs_reason) from " + table_name + " where cs_reason = 'lexical need';"
            emphasis = "select count(cs_reason) from " + table_name + " where cs_reason = 'emphasis';"
            style = "select count(cs_reason) from " + table_name + " where cs_reason = 'style';"
            quote = "select count(cs_reason) from " + table_name + " where cs_reason = 'quote';"
            cs_reason_list = [lexical, emphasis, style, quote]
            count_list = []
            for reason in cs_reason_list:
                mycursor.execute(reason)
                count = mycursor.fetchall()
                try:
                        count = count[0][0]
                except IndexError:
                        count = 0
                count = round(count/both_lang_count, 2)*100
                count_list.append(count)
         
            percentages[table_name] = count_list
            
        for table_name in percentages:
            sql = "INSERT INTO cs_results (title, lexical, emphasis, style, quote) VALUES (%s, %s, %s, %s, %s)"
            title = table_name
            lexical = percentages[table_name][0]
            emphasis = percentages[table_name][1]
            style = percentages[table_name][2]
            quote = percentages[table_name][3]
            val = (title, lexical, emphasis, style, quote)
            mycursor.execute(sql, val)
            mydb.commit()
get_results()
