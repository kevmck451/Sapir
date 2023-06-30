from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process_file')
def process_file():
    return render_template('process_file.html')

@app.route('/process_directory')
def process_directory():
    return render_template('process_directory.html')

@app.route('/data_collection')
def data_collection():
    return render_template('data_collection.html')

@app.route('/data_processing')
def data_processing():
    return render_template('data_processing.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
