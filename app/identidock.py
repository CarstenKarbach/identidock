from flask import Flask, Response, send_file, request
import requests
import os
import hashlib
import redis

app = Flask(__name__)
salt = "UNIQUE_SALT"
default_name = 'Joe Bloggs'
cache = redis.StrictRedis(host='idredis', port=6379, db=0)

callcount = 0

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    name = default_name
    global callcount
    callcount += 1
    
    if request.method == 'POST':
        name = request.form['name']
    
    salted_name = salt+name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()
    
    dirname = os.path.dirname(__file__)
    html = open(dirname+'/resources/identicon.html').read()
    html = html.replace('@@name@@', name)
    html = html.replace('@@name_hash@@', name_hash)
    html = html.replace('@@callcount@@', str(callcount))
    return html

@app.route('/monster/<name>')
def get_identicon(name):
    
    image = cache.get(name)
    
    if image is None:
        r = requests.get('http://dnmonster:8080/monster/'+name+'?size=80')
        image = r.content
        cache.set(name, image)
        app.logger.info('No hit for '+name)
    else:
        app.logger.info('Cache hit for '+name)
    return Response(image,mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
