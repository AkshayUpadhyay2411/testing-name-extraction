import nltk
from tika import parser
import os
import re
import spacy
from spacy.matcher import Matcher
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

punc = '''[](-)*!,'-"/’<•>#$;'''

def clean_text(text):
    try:
        text = text.lower()
        translator = str.maketrans('', '', punc)
        text = text.translate(translator)
        text = " ".join(text.split('\n'))
        text = " ".join([word for word in str(text).split() if word not in stop_words])
        text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
        # remove extra space
        text = re.sub(' +', ' ', text)
        return text
    except Exception as e:
        print("Error in clean_text:", e)
        return None

def extract_name(resume_text):
    try:
        nlp = spacy.load('en_core_web_sm')
        matcher = Matcher(nlp.vocab)

        patterns = [
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
        ]

        for pattern in patterns:
            matcher.add('NAME', patterns=[pattern])

        doc = nlp(resume_text)
        matches = matcher(doc)

        
        for match_id, start, end in matches:
            span = doc[start:end]
            print(span.text)

        for match_id, start, end in matches:
            span = doc[start:end]
            return span.text

        return None
    except Exception as e:
        print("Error in extract_name:", e)
        return None


cnt = 0
for file in os.listdir('resumes'):
    if file.endswith('.pdf'):
        cnt+=1
        
        print(cnt, " File Name : ", file)

        try:
            raw = parser.from_file(os.path.join('resumes', file))
            text = raw.get('content')
        except Exception as e:
            print("Error reading file:", e)
            continue

        try:
            text = clean_text(text)
        except Exception as e:
            print("Error cleaning text:", e)
            continue

        try:
            name = extract_name(text)
        except Exception as e:
            print("Error extracting name:", e)
            continue

        if name :
            print(cnt, " Name : ", name)

        print()
        print()

