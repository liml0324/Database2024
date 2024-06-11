import pymysql as mysql
from datetime import datetime

def get_course(id, name, hours, type, year, term, teacherid):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    type_list = ['', '本科生课程', '研究生课程']
    term_list = ['', '春季学期', '夏季学期', '秋季学期']
    cursor = conn.cursor()
    params = []
    sql = "SELECT Distinct 课程.课程号, 主讲课程.学期, 主讲课程.年份 FROM 课程, 主讲课程, 教师 WHERE 课程.课程号 = 主讲课程.课程号 AND 主讲课程.工号 = 教师.工号 "
    
    if id:
        sql += "AND 课程.课程号 = %s "
        params.append("%" + id + "%")
        
    if name:
        sql += "AND 课程.课程名称 = %s "
        params.append("%" + name + "%")
    
    if hours:
        try:
            hours = int(hours)
        except:
            return None
        if hours <= 0:
            return None
        sql += "AND 课程.学时数 = %s "
        params.append(hours)
    
    if type:
        sql += "AND ("
        for t in type:
            try:
                t = int(t)
            except:
                return None
            if t < 1 or t > 2:
                return None
            sql += "课程.课程类型 = %s OR "
            params.append(t)
        sql = sql[:-4] + ") "
        
    if year:
        try:
            year = int(year)
        except:
            return None
        if year < 1958:
            return None
        sql += "AND 主讲课程.年份 = %s "
        params.append(year)
        
    if term:
        sql += "AND ("
        for t in term:
            try:
                t = int(t)
            except:
                return None
            if t < 1 or t > 3:
                return None
            sql += "主讲课程.学期 = %s OR "
            params.append(t)
        sql = sql[:-4] + ") "
    
    if teacherid:
        sql += "AND (教师.工号=%s OR 教师.姓名 LIKE %s)"
        params.append(teacherid)
        params.append('%'+teacherid+'%')
        
    cursor.execute(sql, params)
    courses = []
    result = cursor.fetchall()
    
    for id, term, year in result:
        teacher_names_str = ''
        cursor.execute("SELECT 教师.姓名 FROM 教师, 主讲课程 WHERE 主讲课程.工号 = 教师.工号 AND 主讲课程.课程号 = %s AND 主讲课程.学期 = %s AND 主讲课程.年份 = %s", (id, term, year))
        teachers = cursor.fetchall()
        for teacher in teachers:
            teacher_names_str += teacher[0] + ', '
        teacher_names_str = teacher_names_str[:-2]
        
        cursor.execute("SELECT * FROM 课程 WHERE 课程.课程号 = %s", (id))
        course = {}
        course['id'], course['name'], course['hours'], course['type'] = cursor.fetchone()
        course['teachers'] = teacher_names_str
        course['term_id'] = term
        course['term'] = term_list[term]
        course['year'] = year
        course['type'] = type_list[course['type']]
        courses.append(course)
        
    cursor.close()
    conn.close()
    if courses:
        return courses
    else:
        return None
    
def get_course_details(id, year, term, transform=True):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not id:
        return None
    if not year:
        return None
    if not term:
        return None
    cursor.execute("SELECT * FROM 课程 WHERE 课程.课程号 = %s", (id))
    course_data = cursor.fetchone()
    if not course_data:
        return None
    course = {}
    course['id'], course['name'], course['hours'], course['type'] = course_data
    if transform:
        course['type'] = '本科生课程' if course['type'] == 1 else '研究生课程'
    
    try:
        term = int(term)
    except:
        return None
    if term < 1 or term > 3:
        return None
    try:
        year = int(year)
    except:
        return None
    if year < 1958:
        return None
    course['year'] = year
    course['term'] = term
    if transform:
        course['term'] = ['','春季学期', '夏季学期', '秋季学期'][term]
    teachers = []
    cursor.execute("SELECT 工号, 承担学时 FROM 主讲课程 WHERE 主讲课程.课程号 = %s AND 主讲课程.学期 = %s AND 主讲课程.年份 = %s", (id, term, year))
    if cursor.rowcount == 0:
        return None
    for teacher_id, teacher_hours in cursor.fetchall():
        cursor.execute("SELECT * FROM 教师 WHERE 工号 = %s", (teacher_id))
        teacher_data = cursor.fetchone()
        if not teacher_data:
            return None
        teacher = {}
        teacher['id'], teacher['name'], teacher['gender'], teacher['title'] = teacher_data
        if transform:
            if teacher['gender'] == 1:
                teacher['gender'] = '男'
            else:
                teacher['gender'] = '女'
            teacher['title'] = ['','博士后' , '助教', '讲师', '副教授', '特任教授', '教授', '助理研究员', '特任副研究员', '副研究员', '特任研究员', '研究员'][teacher['title']]
        teacher['hours'] = teacher_hours
        teachers.append(teacher)
        
    cursor.close()
    conn.close()
    return course, teachers
        

def register_course(id, year, term, teachers):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not id:
        return {'message': '课程号不能为空！'}
    if not year:
        return {'message': '年份不能为空！'}
    if not term:
        return {'message': '学期不能为空！'}
    if not teachers:
        return {'message': '教师不能为空！'}
    try:
        year = int(year)
    except:
        return {'message': '年份不合法！'}
    if year < 1958:
        return {'message': '年份不合法！'}
    try:
        term = int(term)
    except:
        return {'message': '学期不合法！'}
    if term < 1 or term > 3:
        return {'message': '学期不合法！'}
    cursor.execute("SELECT 学时数 FROM 课程 WHERE 课程号 = %s", (id))
    hours = cursor.fetchone()
    if not hours:
        return {'message': '课程号不存在！'}
    cursor.execute("SELECT * FROM 主讲课程 WHERE 课程号 = %s AND 学期 = %s AND 年份 = %s", (id, term, year))
    if cursor.fetchone():
        return {'message': '该时间段已有教师承担该课程教学！'}
    totol_hours = 0
    teacherids = []
    for teacher_id, teacher_hours in teachers:
        cursor.execute("SELECT * FROM 教师 WHERE 工号 = %s", (teacher_id))
        if not cursor.fetchone():
            return {'message': '工号为'+teacher_id+'的教师不存在！'}
        try:
            teacher_hours = int(teacher_hours)
        except:
            return {'message': '工号为'+teacher_id+'的教师的承担学时数不合法！'}
        if teacher_hours <= 0:
            return {'message': '工号为'+teacher_id+'的教师的承担学时必须为正整数！'}
        totol_hours += teacher_hours
        teacherids.append(teacher_id)
        
    if len(teacherids) != len(set(teacherids)):
        return {'message': '不能有重复教师！'}
    
    if totol_hours != hours[0]:
        return {'message': '教师承担学时数之和必须等于课程学时数！'}
    
    for teacher_id, teacher_hours in teachers:
        cursor.execute("INSERT INTO 主讲课程(课程号, 学期, 年份, 工号, 承担学时) VALUES (%s, %s, %s, %s, %s)", (id, term, year, teacher_id, teacher_hours))
        
    conn.commit()
    cursor.close()
    conn.close()
    return {'message': '提交成功！'}    

def delete_course(id, year, term):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not id:
        return '课程号不能为空！'
    if not year:
        return '年份不能为空！'
    if not term:
        return '学期不能为空！'
    cursor.execute("SELECT * FROM 主讲课程 WHERE 课程号 = %s AND 学期 = %s AND 年份 = %s", (id, term, year))
    if not cursor.fetchone():
        return '该时间段没有教师承担该课程教学！'
    print(cursor.execute("DELETE FROM 主讲课程 WHERE 课程号 = %s AND 学期 = %s AND 年份 = %s", (id, term, year)))
    conn.commit()
    cursor.close()
    conn.close()
    return '删除成功！'

def edit_course(id, old_year, old_term, year, term, teachers):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not id:
        return {'message': '课程号不能为空！'}
    if not year:
        return {'message': '年份不能为空！'}
    if not term:
        return {'message': '学期不能为空！'}
    if not teachers:
        return {'message': '教师不能为空！'}
    try:
        old_year = int(old_year)
    except:
        return {'message': '原年份不合法！'}
    if old_year < 1958:
        return {'message': '原年份不合法！'}
    
    try:
        year = int(year)
    except:
        return {'message': '新年份不合法！'}
    if year < 1958:
        return {'message': '新年份不合法！'}
    try:
        old_term = int(old_term)
    except:
        return {'message': '原学期不合法！'}
    if old_term < 1 or old_term > 3:
        return {'message': '原学期不合法！'}
    
    try:
        term = int(term)
    except:
        return {'message': '新学期不合法！'}
    if term < 1 or term > 3:
        return {'message': '新学期不合法！'}
    cursor.execute("SELECT 学时数 FROM 课程 WHERE 课程号 = %s", (id))
    hours = cursor.fetchone()
    if not hours:
        return {'message': '课程号不存在！'}
    cursor.execute("SELECT * FROM 主讲课程 WHERE 课程号 = %s AND 学期 = %s AND 年份 = %s", (id, old_term, old_year))
    if not cursor.fetchone():
        return {'message': '原时间段没有教师承担该课程教学！'}
    cursor.execute("SELECT * FROM 主讲课程 WHERE 课程号 = %s AND 学期 = %s AND 年份 = %s", (id, term, year))
    if (old_term != term or old_year != year) and cursor.fetchone():
        return {'message': '新时间段已有教师承担该课程教学！'}
    totol_hours = 0
    teacherids = []
    for teacher_id, teacher_hours in teachers:
        cursor.execute("SELECT * FROM 教师 WHERE 工号 = %s", (teacher_id))
        if not cursor.fetchone():
            return {'message': '工号为'+teacher_id+'的教师不存在！'}
        try:
            teacher_hours = int(teacher_hours)
        except:
            return {'message': '工号为'+teacher_id+'的教师的承担学时数不合法！'}
        if teacher_hours <= 0:
            return {'message': '工号为'+teacher_id+'的教师的承担学时必须为正整数！'}
        totol_hours += teacher_hours
        teacherids.append(teacher_id)
        
    if len(teacherids) != len(set(teacherids)):
        return {'message': '不能有重复教师！'}
    
    if totol_hours != hours[0]:
        return {'message': '教师承担学时数之和必须等于课程学时数！'}
    
    cursor.execute("DELETE FROM 主讲课程 WHERE 课程号 = %s AND 学期 = %s AND 年份 = %s", (id, old_term, old_year))
    for teacher_id, teacher_hours in teachers:
        cursor.execute("INSERT INTO 主讲课程(课程号, 学期, 年份, 工号, 承担学时) VALUES (%s, %s, %s, %s, %s)", (id, term, year, teacher_id, teacher_hours))
        
    conn.commit()
    cursor.close()
    conn.close()
    return {'message': '修改成功！点击确定关闭页面。'}