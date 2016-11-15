## bag of words 
import string
import re
from bs4 import BeautifulSoup

__western_emoticons__ = open("westernascii.txt", 'r').read().splitlines()
__sideways_emoticons__ = open("sidewayslatin.txt", 'r').read().splitlines()
__upright_emoticons__ = open("uprightlatin.txt", 'r').read().splitlines()

class BoW():

    def __init__(self):
        self.workflow = []


    ## Transformers

    def toLowerCase(self):
         self.workflow.append(Transformer('to lower case', 
                                          lambda x : x.lower()))

    def removePunct(self):        
         self.workflow.append(Transformer('remove punctuation', 
                                          lambda x : x.translate(None, string.punctuation)))
        

   
    def removeNumerics(self):
         self.workflow.append(Transformer('remove numerics', 
                                          lambda x : x.translate(None, string.digits)))

    def removeTags(self):
        
        self.workflow.append(Transformer('remove tags',
                                         lambda x : BeautifulSoup(x).get_text()))
                                         
    def __removeStopWords__(self, tokens, filepath):
        
        ## load stopword list from file with lowercase words one per line
        rawWords = open(filepath, 'r').read().splitlines()
        stops = set(rawWords)
        return [word for word in tokens if word not in stops]
        
                                          

    def removeStopWords(self, filepath, sep = None):
        
        self.workflow.append(Transformer('remove stop words',
                                         lambda x : self.__removeStopWords__(x.split(sep), filepath)))


    def countNumerics(self):
         
         self.workflow.append(Extractor('numerics_count', 
                                        lambda x : len([char for char in x if char in string.digits])))

    def countChars(self):
         
         self.workflow.append(Extractor('character_count', 
                                        lambda x : len(x)))

    def countPunct(self):
         
         self.workflow.append(Extractor('punctuation_count', 
                                        lambda x : len([char for char in x if char in string.punctuation])))

    def countWords(self, sep = None):
         
         self.workflow.append(Extractor('word_count', 
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
         
         self.workflow.append(Extractor('word_lengths_count', 
                                        lambda x :  self.__countWordLengths__(x.split(sep))))
                                        
                                       
    def __countEmojis__(self, tokens):
        
        
        labels = ['ascii','misc','emoticons']
        counts = [0] * 3
        ## These are the magic numbers that define bounds for certain unicode 
        ## classes - http://www.unicode.org/charts/
        misc_lower = 0x2600
        misc_upper = 0x26ff
        emoji_lower = 0x1f500
        emoji_upper = 0x1f64f
       
        ## tokens are words or rather sequences of chars separated by ws
        ## first we treat tokens as entities and check against reference files
        ascii = len([token for token in tokens if token in __western_emoticons__])
        ascii = ascii + len([token for token in tokens if token in __sideways_emoticons__])
        ascii  = ascii + len([token for token in tokens if token in __upright_emoticons__])
        counts[0] = ascii
        ## now we look at indivisual chars in the tokens for single emoticons
        ## according to unicode ranges
        for token in tokens:  
        
            counts[1] = len([char for char in token if misc_lower <= ord(char) <= misc_upper])
            counts[2] = len([char for char in token if emoji_lower <= ord(char) <= emoji_upper])
        
        return dict(zip(labels,counts))
        
    def countEmojis(self, sep = None):
         
         self.workflow.append(Extractor('emoticons_count', 
                                        lambda x :  self.__countEmojis__(x.split(sep))))                                       
                                  

    def calculateDiversity(self, sep = None):
        
        self.workflow.append(Extractor('lexical_diversity',
                                       lambda x : len(set(x.split(sep)))/len(x.split(sep))))
                                       
    def calculateVocabulary(self, sep=None):
    
        self.workflow.append(Extractor('vocabulary_count',
                                       lambda x : len(set(x.split(sep)))))                                   

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
    
    