from flask import Flask, render_template, request, jsonify, send_file
from spire.doc import Document, FileFormat
import tempfile
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
        query = {'id': id, 'title': title, 'source': source, 'year': year, 'authorid': authorid}
        for t in type:
            query['type'+t] = 1
        for l in level:
            query['level'+l] = 1
        return render_template('paper.html', papers=papers, query=query)
    if request.method == 'GET':
        return render_template('paper.html', papers=None, query=None)

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

@app.route('/paper/<id>/delete', methods=['DELETE'])
def paper_delete(id):
    message = mysql.paper.delete_paper(id)
    return jsonify({'message': message})

@app.route('/paper/<id>/view', methods=['GET'])
def paper_view(id):
    result = mysql.paper.get_paper_details(id)
    if not result:
        return render_template('warning.html', message='序号不合法或论文不存在！')
    paper, authors = result
    return render_template('paper/view.html', paper=paper, authors=authors)

@app.route('/paper/<id>/edit', methods=['GET', 'POST'])
def paper_edit(id):
    result = mysql.paper.get_paper_details(id, False)
    if not result:
        return render_template('warning.html', message='序号不合法或论文不存在！')
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

@app.route('/project', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        source = request.form.get('source')
        type = request.form.getlist('type')
        funds = request.form.get('funds')
        begin_year = request.form.get('begin_year')
        end_year = request.form.get('end_year')
        leader_id = request.form.get('leader_id')
        projects = mysql.project.get_projects(id, name, source, type, funds, begin_year, end_year, leader_id)
        query = {'id': id, 'name': name, 'source': source, 'funds': funds, 'begin_year': begin_year, 'end_year': end_year, 'leader_id': leader_id, 'type': type}
        print(type)
        return render_template('project.html', projects=projects, query=query)
    if request.method == 'GET':
        return render_template('project.html', projects=None, query=None)
    return render_template('project.html')

@app.route('/project/<id>/delete', methods=['DELETE'])
def project_delete(id):
    message=mysql.project.delete_project(id)
    return jsonify({'message': message})

@app.route('/project/<id>/view', methods=['GET'])
def project_view(id):
    result = mysql.project.get_project_details(id)
    if not result:
        return render_template('warning.html', message='项目号不合法或项目不存在！')
    project, leaders = result
    return render_template('project/view.html', project=project, leaders=leaders)

@app.route('/project/<id>/edit', methods=['GET', 'POST'])
def project_edit(id):
    result = mysql.project.get_project_details(id, False)
    if not result:
        return render_template('warning.html', message='项目号不合法或项目不存在！')
    project, leaders = result
    if request.method == 'POST':
        leaders = []
        for i in range(1, 100):
            leaderId = request.form.get('leaderId'+str(i))
            if not leaderId:
                break
            leaderFunds = request.form.get('leaderFunds'+str(i))
            leaders.append([leaderId, leaderFunds])
        old_id = id
        id = request.form.get('id')
        name = request.form.get('name')
        source = request.form.get('source')
        type = request.form.get('type')
        funds = request.form.get('funds')
        begin_year = request.form.get('begin_year')
        end_year = request.form.get('end_year')
        json = mysql.project.edit_project(old_id, id, name, source, type, funds, begin_year, end_year, leaders)
        return jsonify(json)
    if request.method == 'GET':
        return render_template('project/edit.html', project=project, leaders=leaders)

@app.route('/project/register', methods=['GET', 'POST'])
def project_register():
    if request.method == 'POST':
        leaders = []
        for i in range(1, 100):
            leaderId = request.form.get('leaderId'+str(i))
            if not leaderId:
                break
            leaderFunds = request.form.get('leaderFunds'+str(i))
            leaders.append([leaderId, leaderFunds])
        id = request.form.get('id')
        name = request.form.get('name')
        source = request.form.get('source')
        type = request.form.get('type')
        funds = request.form.get('funds')
        begin_year = request.form.get('begin_year')
        end_year = request.form.get('end_year')
        json = mysql.project.register_project(id, name, source, type, funds, begin_year, end_year, leaders)
        return jsonify(json)
    if request.method == 'GET':
        return render_template('project/register.html')

@app.route('/course', methods=['GET', 'POST'])
def course():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        hours = request.form.get('hours')
        type = request.form.getlist('type')
        year = request.form.get('year')
        term = request.form.getlist('term')
        teacherid = request.form.get('teacherid')
        courses = mysql.course.get_course(id, name, hours, type, year, term, teacherid)
        query = {'id': id, 'name': name, 'hours': hours, 'type': type, 'year': year, 'term': term, 'teacherid': teacherid}
        return render_template('course.html', courses=courses, query=query)
    if request.method == 'GET':
        return render_template('course.html', query=None, courses=None)

@app.route('/query', methods=['GET'])
def query():
    return render_template('query.html')

@app.route('/course/register', methods=['GET', 'POST'])
def course_register():
    teachers = []
    if request.method == 'POST':
        for i in range(1, 100):
            teacherid = request.form.get('teacherId'+str(i))
            if not teacherid:
                break
            teacherHours = request.form.get('teacherHours'+str(i))
            teachers.append([teacherid, teacherHours])
        id = request.form.get('id')
        year = request.form.get('year')
        term = request.form.get('term')
        json = mysql.course.register_course(id, year, term, teachers)
        return jsonify(json)
    if request.method == 'GET':
        return render_template('course/register.html')
    
@app.route('/course/<id>/<year>/<term>/delete', methods=['DELETE'])
def course_delete(id, year, term):
    message = mysql.course.delete_course(id, year, term)
    return jsonify({'message': message})

@app.route('/course/<id>/<year>/<term>/view', methods=['GET'])
def course_view(id, year, term):
    result = mysql.course.get_course_details(id, year, term)
    if not result:
        return render_template('warning.html', message='课程不存在或课程信息有误！')
    course, teachers = result
    return render_template('course/view.html', course=course, teachers=teachers)

@app.route('/course/<id>/<year>/<term>/edit', methods=['GET', 'POST'])
def course_edit(id, year, term):
    result = mysql.course.get_course_details(id, year, term, False)
    if not result:
        return render_template('warning.html', message='课程不存在或课程信息有误！')
    course, teachers = result
    if request.method == 'POST':
        teachers = []
        for i in range(1, 100):
            teacherId = request.form.get('teacherId'+str(i))
            if not teacherId:
                break
            teacherHours = request.form.get('teacherHours'+str(i))
            teachers.append([teacherId, teacherHours])
        old_year = course['year']
        old_term = course['term']
        year = request.form.get('year')
        term = request.form.get('term')
        json = mysql.course.edit_course(id, old_year, old_term, year, term, teachers)
        return jsonify(json)
    if request.method == 'GET':
        print(type(course['term']))
        return render_template('course/edit.html', course=course, teachers=teachers)
    
@app.route('/info/course', methods=['GET'])
def course_info():
    courses = mysql.course.get_all_courses()
    return render_template('info/course.html', courses=courses)

@app.route('/info/teacher', methods=['GET'])
def teacher_info():
    teachers = mysql.teacher.get_all_teachers()
    return render_template('info/teacher.html', teachers=teachers)

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    if request.method == 'POST':
        id = request.form.get('id')
        begin_year = request.form.get('begin_year')
        end_year = request.form.get('end_year')
        query = {'id': id, 'begin_year': begin_year, 'end_year': end_year}
        result = mysql.statistics.get_statistics(id, begin_year, end_year)
        if type(result) == str:
            return jsonify({'message': result})
        teacher, courses, papers, projects = result
        return render_template('statistics.html', query=query, teacher=teacher, courses=courses, papers=papers, projects=projects, show_button=True, begin_year=begin_year, end_year=end_year)

    if request.method == 'GET':
        return render_template('statistics.html', query=None, teacher=None, courses=None, papers=None, projects=None, show_button=False)
    
@app.route('/statistics/<id>/<begin_year>/<end_year>', methods=['GET'])
def get_pdf(id, begin_year, end_year):
    result = mysql.statistics.get_statistics(id, begin_year, end_year)
    if type(result) == str:
        return render_template('warning.html', message=result)
    teacher, courses, papers, projects = result
    query = {'id': id, 'begin_year': begin_year, 'end_year': end_year}
    html_text = render_template('pdf.html', query=query, teacher=teacher, courses=courses, papers=papers, projects=projects)
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_file.close()
    doc = Document()
    sec = doc.AddSection()
    par = sec.AddParagraph()
    par.AppendHTML(html_text)
    doc.SaveToFile(pdf_file.name, FileFormat.PDF)
    return send_file(pdf_file.name, mimetype='application/pdf', as_attachment=True)