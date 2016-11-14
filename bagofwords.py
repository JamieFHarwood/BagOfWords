## bag of words 
import string
import re
from bs4 import BeautifulSoup
import unicodedata

__western_emoticons__ = open("westernascii.txt", 'r').read().splitlines()
__sideways_emoticons__ = open("sidewayslatin.txt", 'r').read().splitlines()
__upright_emoticons__ = open("uprightlatin.txt", 'r').read().splitlines()

class BoW():

    def __init__(self):
        self.workflow = []


    ## Transformers

    def removePunct(self):        
         self.workflow.append(Transformer('remove punctuation', 
                                          lambda x : x.translate(None, string.punctuation)))
        

   
    def removeNumerics(self):
         self.workflow.append(Transformer('remove numerics', 
                                          lambda x : x.translate(None, string.digits)))

    def removeTags(self):
        
        self.workflow.append(Transformer('remove tags',
                                         lambda x : BeautifulSoup(x).get_text()))




    def countNumerics(self):
         
         self.workflow.append(Extractor('count numerics', 
                                        lambda x : len([char for char in x if char in string.digits])))

    def countChars(self):
         
         self.workflow.append(Extractor('count characters', 
                                        lambda x : len(x)))

    def countPunct(self):
         
         self.workflow.append(Extractor('count punctuation', 
                                        lambda x : len([char for char in x if char in string.punctuation])))

    def countWords(self, sep = None):
         
         self.workflow.append(Extractor('count words', 
                                        lambda x : len(x.split(sep))))

    def countThisChar(self, thisChar):
        
        self.workflow.append(Extractor(thisChar + '_count', 
                                        lambda x : x.count(thisChar)))
                                        
    def countThisPattern(self, pattern):
        
        self.workflow.append(Extractor('pattern_' + re.escape(pattern) + '_count', 
                                        lambda x : re.findall(pattern, x)))
                                        
    def countUrls(self):
        
        self.workflow.append(Extractor('url_count', 
                                        lambda x : re.findall('https?://', x)))
                                        
    def countParagraphs(self):
        
        self.workflow.append(Extractor('paragraph_count', 
                                        lambda x : x.count('\n')))
                                        
    def countSentences(self, sentenceEnders = None):
        
        sentenceEnders = '[.?!](\s\s?)|($)' if sentenceEnders == None else '[' + sentenceEnders + '](\s\s?)|($)'
        self.workflow.append(Extractor('sentence_count', 
                                        lambda x : len(re.findall(sentenceEnders, x))))                                       

    def __countWordLengths__(self, tokens):
        
        counts = [0] * 20
        labels = range(1,21)
        counts_dict = dict(zip(labels, counts))
        for token in tokens:
            tl = len(token)
            if tl <= 20:
             
                counts_dict[len(token)] = counts_dict[len(token)] + 1
        return counts_dict
        
        
        
    def countWordLengths(self, sep = None):
         
         self.workflow.append(Extractor('count word lengths', 
                                        lambda x :  self.__countWordLengths__(x.split(sep))))
                                        
    ## This is broken - we need ot iterate by words for ascii but but "char" 
    ## for misc and emoji                                    
    def __countEmojis__(self, chars):
        
        for char in chars :
            print(string.decode('utf-8'))
        labels = ['ascii','misc','emoticons']
        counts = [0] * 3
        ascii = len([char for char in chars if char in __western_emoticons__])
        ascii = ascii + len([char for char in chars if char in __sideways_emoticons__])
        ascii  = ascii + len([char for char in chars if char in __upright_emoticons__])
        counts[0] = ascii
        counts[1] = len([char for char in chars if '\u2600' <= char.decode('utf-8') <= '\u26FF'])
        counts[2] = len([char for char in chars if '\u1F600' <= char.decode('utf-8') <= '\u1F64F'])
        
        return dict(zip(labels,counts))
        
    def countEmojis(self):
         
         self.workflow.append(Extractor('count emoticons', 
                                        lambda x :  self.__countEmojis__(x)))                                       
                                  

"""
    

         
 
     
         
    def countEmojis




    def removeStopWords():







"""

class ProcessStep():
    
    def __init__(self, name, processor):
        self.name = name;
        self.processor = processor
        
    def processor(self):
        return self.processor
        
class Transformer(ProcessStep):
    pass

class Extractor(ProcessStep):
    pass
    
    