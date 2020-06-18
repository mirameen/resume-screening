import spacy
import sys
import json
nlp = spacy.load("en_core_web_sm")

from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

#Phrase matcher
phrase_matcher = PhraseMatcher(nlp.vocab)

phrases = json.loads(sys.argv[2])
patterns = [nlp(text) for text in phrases]
phrase_matcher.add('AI', None, *patterns)

def get_matchphrase(text):
    result = nlp(text.lower())
    matched_phrases = phrase_matcher(result)
    skills = []

    for match_id, start, end in matched_phrases:
        string_id = nlp.vocab.strings[match_id]  
        span = result[start:end]
        skills.append(span.text)                   
        #print(match_id, string_id, start, end, span.text)
    return skills 
   
mp = set(get_matchphrase(sys.argv[1]))
if(len(mp)==len(phrases)):
    print("True")
else:
    print("False")
