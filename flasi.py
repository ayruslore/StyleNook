from flask import Flask, render_template, request
from werkzeug import secure_filename
import requests
import os

app = Flask(__name__)
global link
link = 'http://0.0.0.0:4000'

''' api calls to be made to the main server
/matchsylist/<num>
/makereturncountsepe
/cleanuserprofile
/makevariablesagain
'''

@app.route('/upload/wpusers', methods=['POST'])
def wpuser_files():
    global link
    f = request.files['wpusers']
    f.save(secure_filename(f.filename))
    r1 = requests.get(link + '/makestylistdata')
    if r1.status_code == 200 :
        r2 = requests.get(link + '/makevariablesagain')
        if r2.status_code == 200 :
            return 'File uploaded successfully'
        else:
            return 'Please try again.'
    else:
        return 'Please try again.'

@app.route('/upload/orders', methods=['POST'])
def order_files():
    global link
    f = request.files['orders']
    f.save(secure_filename(f.filename))
    r1 = requests.get(link + '/makereturncountsepe')
    if r1.status_code == 200 :
        r2 = requests.get(link + '/makestylistdata')
        if r2.status_code == 200 :
            r3 = requests.get(link + '/makevariablesagain')
            if r3.status_code == 200 :
                return 'File uploaded successfully'
            else:
                return 'Please try again.'
        else:
            return 'Please try again.'
    else:
        return 'Please try again.'

@app.route('/upload/returns', methods=['POST'])
def return_files():
    global link
    f = request.files['returns']
    f.save(secure_filename(f.filename))
    r1 = requests.get(link + '/makereturncountsepe')
    if r1.status_code == 200 :
        r2 = requests.get(link + '/makestylistdata')
        if r2.status_code == 200 :
            r3 = requests.get(link + '/makevariablesagain')
            if r3.status_code == 200 :
                return 'File uploaded successfully'
            else:
                return 'Please try again.'
        else:
            return 'Please try again.'
    else:
        return 'Please try again.'

@app.route('/upload/stylist', methods=['POST'])
def stylist_files():
    global link
    f = request.files['stylist']
    f.save(secure_filename(f.filename))
    r1 = requests.get(link + '/makereturncountsepe')
    if r1.status_code == 200 :
        r2 = requests.get(link + '/makestylistdata')
        if r2.status_code == 200 :
            r3 = requests.get(link + '/makevariablesagain')
            if r3.status_code == 200 :
                return 'File uploaded successfully'
            else:
                return 'Please try again.'
        else:
            return 'Please try again.'
    else:
        return 'Please try again.'

@app.route('/upload/users', methods=['POST'])
def user_files():
    global link
    f = request.files['users']
    f.save(secure_filename(f.filename))
    r1 = requests.get(link + '/cleanuserprofile')
    if r1.status_code == 200 :
        r2 = requests.get(link + '/makestylistdata')
        if r2.status_code == 200 :
            r3 = requests.get(link + '/makevariablesagain')
            if r3.status_code == 200 :
                return 'File uploaded successfully'
            else:
                return 'Please try again.'
        else:
            return 'Please try again.'
    else:
        return 'Please try again.'

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug = True)
