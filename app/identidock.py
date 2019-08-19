from flask import Flask, Response, send_file, request
import requests
import os
import hashlib
import redis
import html

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
        name = html.escape(request.form['name'], quote=True)
    
    salted_name = salt+name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()
    
    dirname = os.path.dirname(__file__)
    fh = open(dirname+'/resources/identicon.html')
    result = fh.read()
    fh.close()
    result = result.replace('@@name@@', name)
    result = result.replace('@@name_hash@@', name_hash)
    result = result.replace('@@callcount@@', str(callcount))
    return result

@app.route('/monster/<name>')
def get_identicon(name):
    
    name = html.escape(name, quote=True)
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
