# -------
# imports
# -------
from io import StringIO
from unittest import main, TestCase

# UnitTests


class TestAnalysis (TestCase):
    
    # Test removing punctuation
    def test_remove_punctuation1(self):
        # no change expected
        word = "hello"
        word = remove_punctuation(word)
        self.assertEqual(word, "hello")
    
    def test_remove_punctuation2(self):
        # remove ! and '
        word = "g'day!"
        word = remove_punctuation(word)
        self.assertEqual(word, "gday")
        
    def test_remove_punctuation3(self):
        # remove special characters and numbers
        word = chr(8217)+chr(8220)+"8"+"yester-day."
        word = remove_punctuation(word)
        self.assertEqual(word, "yesterday")
        
    # test reading script
    
    def test_read1(self):
        text = "dictionaries/spanish_words.txt"
        text = read(text)
        self.assertEqual(type(text), list)
        
        
    def test_edit2(self):
        text = "Wao1.pdf"
        text = read(text)
        self.assertEqual(type(text), list)
        
    # test analyzing
    """
    def test_analyze1(self):
        r = StringIO("dictionaries/spanish_words.txt", "dictionaries/english_words.txt", "Wao1.pdf")
        w = StringIO()
        analyze_text(r, w)
        self.assertEqual(w.getvalue(),
                         
                         )
    """
        

    


if __name__ == "__main__":
    main()
