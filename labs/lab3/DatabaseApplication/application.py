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
        id = request.form.get('id')
        title = request.form.get('title')
        source = request.form.get('source')
        year = request.form.get('year')
        type = request.form.getlist('type')
        level = request.form.getlist('level')
        authorid = request.form.get('authorid')
        papers = mysql.paper.get_paper(id, title, source, year, type, level, authorid)
        return render_template('paper.html', papers=papers)
    if request.method == 'GET':
        return render_template('paper.html', papers=None)

@app.route('/paper/register', methods=['GET', 'POST'])
def paper_register():
    if request.method == 'POST':
        authorids = []
        i = 1
        while i < 100:
            authorid = request.form.get('authorId'+str(i))
            if not authorid:
                break
            authorids.append(authorid)
            i += 1
        id = request.form.get('id')
        title = request.form.get('title')
        source = request.form.get('source')
        year = request.form.get('year')
        type = request.form.get('type')
        level = request.form.get('level')
        authors = [authorids, request.form.get("isCorrespondingAuthor")]
        json = mysql.paper.register_paper(id, title, source, year, type, level, authors)
        return jsonify(json)
    if request.method == 'GET':
        return render_template('paper/register.html')

@app.route('/paper/<id>/delete', methods=['GET'])
def paper_delete(id):
    message = mysql.paper.delete_paper(id)
    return render_template('paper/delete.html', message=message)

@app.route('/paper/<id>/view', methods=['GET'])
def paper_view(id):
    result = mysql.paper.get_paper_details(id)
    if not result:
        return render_template('paper/view_warning.html', message='序号不合法或论文不存在！')
    paper, authors = result
    return render_template('paper/view.html', paper=paper, authors=authors)

@app.route('/paper/<id>/edit', methods=['GET', 'POST'])
def paper_edit(id):
    result = mysql.paper.get_paper_details(id, False)
    if not result:
        return render_template('paper/edit_warning.html', message='序号不合法或论文不存在！')
    paper, authors = result
    if request.method == 'POST':
        authorids = []
        i = 1
        while i < 100:
            authorid = request.form.get('authorId'+str(i))
            if not authorid:
                break
            authorids.append(authorid)
            i += 1
        old_id = id
        print(old_id)
        id = request.form.get('id')
        title = request.form.get('title')
        source = request.form.get('source')
        year = request.form.get('year')
        type = request.form.get('type')
        level = request.form.get('level')
        authors = [authorids, request.form.get("isCorrespondingAuthor")]
        json = mysql.paper.edit_paper(old_id, id, title, source, year, type, level, authors)
        return jsonify(json)
    if request.method == 'GET':
        return render_template('paper/edit.html', paper=paper, authors=authors)

@app.route('/project', methods=['GET'])
def project():
    return render_template('project.html')

@app.route('/course', methods=['GET'])
def course():
    return render_template('course.html')

@app.route('/query', methods=['GET'])
def query():
    return render_template('query.html')