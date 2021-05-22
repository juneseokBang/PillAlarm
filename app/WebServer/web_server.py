# -*- encoding:utf-8 -*-

import sys
from importlib import reload

reload(sys)
from jinja2 import evalcontextfilter
from markupsafe import Markup
import re
import socket
import json
import pprint
import MedicineSearch

from flask import Flask
from flask import request
from flask import render_template
import threading

app = Flask(__name__, static_url_path="/image", static_folder="image")

UPLOAD_FOLDER = './image'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    _paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace(u'\r\n', u'<br/>') for p in _paragraph_re.split(value))
    #print(result)
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.route('/')
def hello_world():
    result = {}
    if "userID" in request.cookies:
        result["login"] = {"bool": "true"}
    else:
        print(2)
        result["login"] = {"bool": "false"}
        result["memos1"] = []
        result["memos2"] = []
    #print(result)
    return render_template('home.html', result=result)


@app.route('/search/medicine/<medicine_link>')
def specific_medicine(medicine_link):
    return render_template('Medicine_info.html', result=MedicineSearch.search_item_by_id(medicine_link)[0])


@app.route('/search/medicine', methods=['POST'])
def search_medicine():
    medicine_name = request.form['medicine_name']
    result = {}
    result["medicines"] = MedicineSearch.crawler(medicine_name)
    result["login"] = {"bool": "None"}
    pprint.pprint(result)
    #print(result)
    return render_template('Medicine_list.html', result=result)


def smartphone_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 5000))
    sock.listen(5)
    try:
        while True:
            client, addr = sock.accept()
            req = client.recv(1024)
            #print(req)
            req = json.loads(req)
            if req['Type'] == 'Search_Medicine':
                client.send(MedicineSearch.crawler(req["Name"]))
            client.close()
    except Exception as e:
        print(e)
        sock.close()


if __name__ == '__main__':
    threading.Thread(target=smartphone_connection).start()
    app.run(host="")
    # unittest.main()
