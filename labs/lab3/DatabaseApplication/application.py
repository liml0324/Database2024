from flask import Flask, render_template, request, jsonify
import os
import mysql
import mysql.paper

# Init app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/paper', methods=['GET', 'POST'])
def paper():
    if request.method == 'POST':
        print(request.form)
        id = request.form.get('id')
        title = request.form.get('title')
        source = request.form.get('source')
        year = request.form.get('year')
        type = request.form.get('type')
        level = request.form.get('level')
        authorid = request.form.get('authorid')
        papers = mysql.paper.get_paper(id, title, source, year, type, level, authorid)
        print(papers)
        return render_template('paper.html', papers=papers)
    if request.method == 'GET':
        return render_template('paper.html', papers=None)

@app.route('/paper/register', methods=['GET', 'POST'])
def paper_register():
    if request.method == 'POST':
        print(request.form)
        return jsonify({'message': '提交成功！'})
    if request.method == 'GET':
        return render_template('paper/register.html')

@app.route('/project', methods=['GET'])
def project():
    return render_template('project.html')

@app.route('/course', methods=['GET'])
def course():
    return render_template('course.html')

@app.route('/query', methods=['GET'])
def query():
    return render_template('query.html')