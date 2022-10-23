# -*- coding: utf-8 -*-
import query_analize
import os
import flask
import requests
from flask import render_template, request
import DAO

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = r"путь к полученному файлу json после авторизации"
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
success_text = 'успех!'
error_text = 'что-то пошло не так :( обратитесь к разработчикам'
# человечные индексы для наполнения словаря
row_id = 0
message = 1
chat_id = 2
dt = 3
status = 4

# telegram
api_telegram = 'https://api.telegram.org/bot'
token = 'token'
method = 'sendMessage'

# flask
app = flask.Flask(__name__)
app.secret_key = 'REPLACE ME - this value is here as a placeholder.'


@app.route('/')
def index():
    return render_template('success.html', request_status='Страница приветствия. Собственно - Привет!')


# обработчик статуса сообщений
@app.route('/<state>/')
def view_messages(state):
    if state == 'not-learned':
        data = DAO.get_not_learned()
        page_data = []
        for el in data:
            page_data.append(
                {'row_id': el[row_id], 'message': el[message], 'chat_id': el[chat_id], 'status': el[status],
                 'date': el[dt]})
        return render_template('index.html', messages=page_data)

    if state == 'added':
        data = DAO.get_added()
        page_data = []
        for el in data:
            page_data.append(
                {'row_id': el[row_id], 'message': el[message], 'chat_id': el[chat_id], 'status': el[status],
                 'date': el[dt]})
        return render_template('added.html', messages=page_data)

    if state == 'statistics':
        stat = query_analize.most_query(50)
        return render_template('statistics.html', most_popular=stat)
    if state == 'metrics':
        analize_result, data = query_analize.get_metrics()
        return render_template('metrics.html', analize_result=analize_result, query=data)
    
    return '404'


# обработчик страницы с ответами пользователю
@app.route('/answer/', methods=['POST', 'GET'])
def answer():
    if request.method == 'GET':
        req_chat_id = request.args.get('chat_id')
        return render_template('answer.html', chat_id=req_chat_id)

    if request.method == 'POST':
        answer = request.form.get('message')
        id_chat = request.form.get('chat_id')
        print(message)
        print(f"{api_telegram}{token}/{method}?chat_id={id_chat}&text={answer}")
        response = requests.get(f'{api_telegram}{token}/{method}?chat_id={id_chat}&text={answer}')
        print(response.status_code)
        if response.status_code == 200:
            return render_template('success.html', request_status=success_text)
        else:
            return render_template('success.html', request_status=error_text)


@app.route('/revert', methods=['POST'])
def change_state():
    text = request.form.get('text')
    # DAO.save_data(message.text, message.chat.id, status=mode)
    DAO.revert_status(text)
    return flask.redirect('/not-learned', code=302, Response=None)


if __name__ == '__main__':
    app.run('0.0.0.0', 8090, debug=False)
