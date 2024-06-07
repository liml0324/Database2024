from flask import Flask, render_template, request, jsonify
import os

# Init app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/paper', methods=['GET'])
def paper():
    return render_template('paper.html')

@app.route('/project', methods=['GET'])
def project():
    return render_template('project.html')

@app.route('/course', methods=['GET'])
def course():
    return render_template('course.html')

@app.route('/query', methods=['GET'])
def query():
    return render_template('query.html')