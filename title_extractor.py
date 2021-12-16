import re
import Levenshtein as lev
import string
import nltk
import re
from nltk.corpus import stopwords
#nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def exclude_stopWord(word):
    stop_words.remove(word)

def add_stopWord(word):
    stop_words.extend(word)


def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


def clean_title(title):
    
    # remove emoji's
    title = deEmojify(title)

    # lowercasing the text 
    title = title.lower()
    
    # encoding the text to ASCII format
    title_encode = title.encode(encoding="ascii", errors="ignore")
    # decoding the text
    title_decode = title_encode.decode()
    # cleaning the text to remove extra whitespace 
    title = " ".join([word for word in title_decode.split()])
    
    title = re.sub('[^a-zA-Z0-9 \n\.]', " ", title)
    title = re.sub('  ', " ", title)
    
    word_list = title.split()
    if len(word_list) > 1:
        title = " ".join([word for word in title.split() if word not in stop_words])
    
    return title

def distance(s1, s2):
    Distance = lev.distance(s1.lower(),s2.lower())
    Ratio = lev.ratio(s1.lower(),s2.lower()) * 100
    return Distance, Ratio


def extract_title(s, keyword_list):
    possible_title_matches = {}
    title_matches = {}
    s_list =  clean_title(str(s)).split()

        
    for keyword_ in keyword_list:
        
        possible_title_matches[keyword_] = {}
        keyword = clean_title(keyword_)
        word_combinations = []
        
        for i in range(0, len(s_list) - len(keyword.split()) + 1):
            word_combinations.append(s_list[i:len(keyword.split())+i])
        
        for combinations in word_combinations:
            
            sub_string = ' '.join(combinations)
            Distance, Ratio = distance(sub_string, keyword)
            possible_title_matches[keyword_].update({sub_string:Ratio})
            
            if len(keyword.split()) > 1: #multiple word title comparison

                ratio = 100 - ((2/len(keyword)) *100) ##best possible case

                if Ratio >= ratio or Ratio == 100:
 
                    title_matches[keyword_] = Ratio
                    for elem in sub_string.split():
                        s_list.remove(elem)
                    break

            else:
                
                if Distance <= int(len(keyword)*0.15) or sub_string == keyword: ## single word title comparison
                    title_matches[keyword_] = Ratio
                    
                    for elem in sub_string.split():
                        s_list.remove(elem)  
                    break
    
    for key, val in possible_title_matches.items():
        try:
            if max(val.values()) > 65:
                if key not in title_matches.keys():
                    title_matches[key] = max(val.values())
        except:
            pass
    
                
    #print(title_matches)
    return(title_matches)