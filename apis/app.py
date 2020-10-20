import time
from flask import Flask
from flask import jsonify
from flask import send_file
from flask import make_response
import glob
import io
from functools import wraps, update_wrapper
from datetime import datetime
from PIL import Image, ImageDraw
import os


app = Flask(__name__)

@app.route('/')

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)

def index():
    return 'Hello World'

@app.route('/time')
def get_current_time():
    return jsonify({'time': time.time()})

@app.route('/debug')
def get_debug():
    return jsonify([])

@app.route('/last24h')
def get_latest_gif():
    list_of_files = glob.glob('/home/pi/greenhouse-react/captures/*')
    last_24_files = sorted(list_of_files, key=lambda t: -os.stat(t).st_mtime)

    images = []
    for f in last_24_files[0:24]:
        images.append(Image.open(f))
    images[0].save('./timelapse/24h.gif', save_all=True, append_images=images[1:], optimize=True, duration=400, loop=0)
    return send_file('../timelapse/24h.gif', mimetype='image/gif', cache_timeout=0)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
