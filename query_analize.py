
from nltk import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string

nltk.download('punkt')
nltk.download('stopwords')
russian_stopwords = stopwords.words("russian")

def most_query(most_count=10):
    f = open('resources/request_log.txt', "r")
    text = f.read().lower()
    f.close()
    text = "".join([ch for ch in text if ch not in string.punctuation])
    text_tokens = word_tokenize(text)
    text = nltk.Text(text_tokens, russian_stopwords)

    fdist = FreqDist(text)
    return fdist.most_common(most_count)
