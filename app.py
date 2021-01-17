#main app file

from flask import Flask, render_template, request, jsonify, make_response
from database import create_connection, select_all_items, update_item, reset_items
from flask_cors import CORS, cross_origin
from pusher import Pusher
import simplejson
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# configure pusher object
pusher = Pusher(
app_id='1139320',
key='4ac52c799ded4e369788',
secret='SECRET_KEY',
cluster='us2',
ssl=True)

database = "./pythonsqlite.db"
conn = create_connection(database)
cur = conn.cursor()
hour = 3600
question = 'Hello World'

def main():
    global conn, cur

@app.route('/')
def index():
    return render_template('index.html', var=question)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if (request.method == 'POST'):
        reset_items(conn)
    global question
    question = request.form.get('textbox')
    return render_template('admin.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = simplejson.loads(request.data)
    v = request.cookies.get('vote', '0')
    print(v)
    if (v != data['member']):
        if (v != ''):
            update_item(cur, -1, v)
        update_item(cur, 1, data['member'])
    output = select_all_items(cur, data['member'])
    pusher.trigger(u'poll', u'vote', output)
    responce = make_response("")
    responce.set_cookie('vote', data['member'], 3600)
    return responce
    

if __name__ == '__main__':
    main()
    app.run(debug=True)
