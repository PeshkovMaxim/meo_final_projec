from nltk import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string

nltk.download('punkt')
nltk.download('stopwords')
russian_stopwords = stopwords.words("russian")

real = [1]

def most_query(most_count=10):
    f = open('resources/request_log.txt', "r")
    text = f.read().lower()
    print(text)
    f.close()
    text = "".join([ch for ch in text if ch not in string.punctuation])
    text_tokens = word_tokenize(text)
    text = nltk.Text(text_tokens, russian_stopwords)

    fdist = FreqDist(text)
    return fdist.most_common(most_count)


def metrics(real, pred, mod=None):
    # длина последовательности
    row_len = len(real)
    # сумма элементов последовательности
    sum = 0
    if mod == 'mse':
        for r in real:
            for p in pred:
                sum += (r - p) ** 2

        return 1 / row_len * sum

    if mod == 'mae':
        for r in real:
            for p in pred:
                sum += abs(r - p)

        return 1 / row_len * sum

    if mod == 'mape':
        for r in real:
            print('this is r: ',r)
            if r == 0.0:
                continue
            else:
                for p in pred:
                    sum += abs(r - p) / abs(r)
            return 1 / row_len * sum

    if mod == 'mpe':
        for r in real:
            if r == 0.0:
                continue
            else:
                for p in pred:
                    sum += (r - p) / r
            return 1 / row_len * sum


def get_metrics():
    data = []
    analize = []
    analize_result = {}
    metrics_result = []
    with open('resources/request_stats.txt', 'r') as file:
        for el in file:
            data.append(el.replace('\n', '').strip().split(':'))
            analize.append(float(el.replace('\n', '').strip().split(':')[1]))
    for el in data:
        metrics_result.append({'mae': metrics(real, [float(el[1])],  mod='mae')})
        metrics_result.append({'mse':metrics(real,[float(el[1])],  mod='mse')})
        metrics_result.append({'mpe':metrics(real,[float(el[1])],  mod='mpe')})
        metrics_result.append({'mape':metrics(real,[float(el[1])],  mod='mape')})


    analize_result['MAE']= metrics(real,analize,  mod='mae')
    analize_result['MSE']= metrics(real,analize,  mod='mse')
    analize_result['MPE']= metrics(real,analize,  mod='mpe')
    analize_result['MAPE']= metrics(real,analize,  mod='mape')
    # возвращаем два результата: анализ и запросы с оценкой совпадения
    return analize_result, data


