import pymysql as mysql
from datetime import datetime

def get_projects(id, name, source, type, funds, begin_year, end_year, leader_id):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    type_list = ['', '国家级', '省部级', '市厅级', '企业合作', '其他类型']
    params = []
    if leader_id:
        sql = 'SELECT Distinct 项目.项目号 FROM 项目, 承担项目, 教师 WHERE 项目.项目号 = 承担项目.项目号 AND 承担项目.工号 = 教师.工号 '
    else:
        sql = 'SELECT Distinct 项目.项目号 FROM 项目 WHERE 1=1 '

    if id:
        sql += ' AND 项目.项目号 = %s '
        params.append(id)
    if name:
        sql += ' AND 项目.项目名称 LIKE %s '
        params.append("%" + name + "%")

    if source:
        sql += ' AND 项目.项目来源 LIKE %s '
        params.append("%" + source + "%")

    if type:
        sql += 'AND ('
        for t in type:
            try:
                t = int(t)
            except:
                cursor.close()
                conn.close()
                return None
            if t < 1 or t > 5:
                cursor.close()
                conn.close()
                return None
            
            sql += '项目.项目类型 = %s OR '
            params.append(type_list[int(t)])
        sql = sql[:-4] + ')'

    if funds:
        try:
            funds = float(funds)
        except:
            cursor.close()
            conn.close()
            return None
        if funds < 0:
            cursor.close()
            conn.close()
            return None
        
        sql += ' AND 项目.总经费 = %s '
        params.append(funds)
    
    if begin_year:
        try:
            begin_year = int(begin_year)
        except:
            cursor.close()
            conn.close()
            return None
        if begin_year < 1958 or begin_year > datetime.now().year:
            cursor.close()
            conn.close()
            return None
        sql += ' AND 项目.开始年份 = %s '
        params.append(begin_year)

    if end_year:
        try:
            end_year = int(end_year)
        except:
            cursor.close()
            conn.close()
            return None
        if end_year < begin_year:
            cursor.close()
            conn.close()
            return None
        sql += ' AND 项目.结束年份 = %s '
        params.append(end_year)

    if leader_id:
        sql += "AND (教师.工号=%s OR 教师.姓名 LIKE %s) "
        params.append(leader_id)
        params.append("%"+leader_id+"%")

    cursor.execute(sql, params)
    project_ids = cursor.fetchall()
    projects = []
    for project_id in project_ids:
        leader_names = []
        cursor.execute('SELECT 教师.姓名, 承担项目.排名 FROM 教师, 承担项目 WHERE 教师.工号 = 承担项目.工号 AND 承担项目.项目号 = %s', project_id)
        leader_data = cursor.fetchall()
        leader_data = list(leader_data)
        leader_names = []
        leader_data.sort(key=lambda x: x[1])
        for leader in leader_data:
            leader_names.append(leader[0])
        cursor.execute('SELECT * FROM 项目 WHERE 项目号 = %s', project_id)
        project = {}
        project['id'], project['name'], project['source'], project['type'], project['funds'], project['begin_year'], project['end_year'] = cursor.fetchall()[0]
        project['type'] = type_list[project['type']]
        leader_name_str = ''
        if leader_names:
            for leader_name in leader_names:
                leader_name_str += leader_name + ', '
        project['leaders'] = leader_name_str[:-2]
        projects.append(project)
    cursor.close()
    conn.close()
    if projects:
        return projects
    return None

def register_project(id, name, source, type, funds, begin_year, end_year, leaders) :
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not id:
        return {'message': '项目号不能为空！'}
    if not name:
        return {'message': '项目名称不能为空！'}
    if not source:
        return {'message': '项目来源不能为空！'}
    if not type:
        return {'message': '项目类型不能为空！'}
    if not funds:
        return {'message': '总经费不能为空！'}
    if not begin_year:
        return {'message': '开始年份不能为空！'}
    if not end_year:
        return {'message': '结束年份不能为空！'}
    if not leaders:
        return {'message': '负责人不能为空！'}
    try:
        funds = float(funds)
    except:
        return {'message': '总经费必须为数字！'}
    if funds < 0:
        return {'message': '总经费不能为负数！'}
    try:
        begin_year = int(begin_year)
    except:
        return {'message': '开始年份必须为数字！'}
    if begin_year < 1958 or begin_year > datetime.now().year:
        return {'message': '开始年份不合法！'}
    try:
        end_year = int(end_year)
    except:
        return {'message': '结束年份必须为数字！'}
    if end_year < begin_year:
        return {'message': '结束年份不合法！'}
    try:
        type = int(type)
    except:
        return {'message': '项目类型不合法！'}
    if type < 1 or type > 5:
        return {'message': '项目类型不合法！'}
    cursor.execute('SELECT * FROM 项目 WHERE 项目号 = %s', id)
    if cursor.fetchall():
        return {'message': '项目号已存在！'}
    
    totol_funds = 0
    leaderids = []
    for leader_id, leader_funds in leaders:
        cursor.execute('SELECT * FROM 教师 WHERE 工号 = %s', leader_id)
        if not cursor.fetchall():
            return {'message': '负责人工号不存在！'}
        try:
            leader_funds = float(leader_funds)
        except:
            return {'message': '负责人经费必须为数字！'}
        if leader_funds < 0:
            return {'message': '负责人经费不能为负数！'}
        totol_funds += leader_funds
        leaderids.append(leader_id)
    if len(leaderids) != len(set(leaderids)):
        return {'message': '不能有重复负责人！'}
    if totol_funds - funds > 0.0001 or totol_funds - funds < -0.0001:
        return {'message': '负责人经费之和必须等于总经费！'}
    
    cursor.execute('INSERT INTO 项目 VALUES (%s, %s, %s, %s, %s, %s, %s)', (id, name, source, type, funds, begin_year, end_year))
    i = 1
    for leader_id, leader_funds in leaders:
        leader_funds = float(leader_funds)
        cursor.execute('INSERT INTO 承担项目 VALUES (%s, %s, %s, %s)', (leader_id, id, i, leader_funds))
        i += 1
    conn.commit()
    cursor.close()
    conn.close()
    return {'message': '提交成功！'}

def get_project_details(id, transform=True):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not id:
        return None
    cursor.execute("SELECT * FROM 项目 WHERE 项目号=%s", id)
    project = cursor.fetchone()
    if not project:
        return None
    temp = project
    project = {}
    project['id'], project['name'], project['source'], project['type'], project['funds'], project['begin_year'], project['end_year'] = temp
    if transform:
        project['type'] = ['', '国家级', '省部级', '市厅级', '企业合作', '其他类型'][project['type']]
    leaders = []
    cursor.execute("SELECT 工号, 排名, 承担经费 FROM 承担项目 WHERE 项目号=%s", id)
    leader_data = cursor.fetchall()
    for leaderid, rank, funds in leader_data:
        cursor.execute("SELECT * FROM 教师 WHERE 工号=%s", leaderid)
        leader = {}
        leader['id'], leader['name'], leader['gender'], leader['title'] = cursor.fetchone()
        if transform:
            if leader['gender'] == 1:
                leader['gender'] = '男'
            else:
                leader['gender'] = '女'
        if transform:
            leader['title'] = ['','博士后' , '助教', '讲师', '副教授', '特任教授', '教授', '助理研究员', '特任副研究员', '副研究员', '特任研究员', '研究员'][leader['title']]
        leader['no'] = rank
        leader['funds'] = funds
        leaders.append(leader)
    leaders.sort(key=lambda x: x['no'])
    cursor.close()
    conn.close()
    return project, leaders



def delete_project(id):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM 项目 WHERE 项目号 = %s', id)
    if not cursor.fetchall():
        return '项目号不存在！'
    # 先删除所有的承担项目
    cursor.execute('DELETE FROM 承担项目 WHERE 项目号 = %s', id)
    # 删除项目
    cursor.execute('DELETE FROM 项目 WHERE 项目号 = %s', id)
    conn.commit()
    cursor.close()
    conn.close()
    return '删除成功！'

def edit_project(old_id, id, name, source, type, funds, begin_year, end_year, leaders):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not id:
        return {'message': '项目号不能为空！'}
    if not name:
        return {'message': '项目名称不能为空！'}
    if not source:
        return {'message': '项目来源不能为空！'}
    if not type:
        return {'message': '项目类型不能为空！'}
    if not funds:
        return {'message': '总经费不能为空！'}
    if not begin_year:
        return {'message': '开始年份不能为空！'}
    if not end_year:
        return {'message': '结束年份不能为空！'}
    if not leaders:
        return {'message': '负责人不能为空！'}
    try:
        funds = float(funds)
    except:
        return {'message': '总经费必须为数字！'}
    if funds < 0:
        return {'message': '总经费不能为负数！'}
    try:
        begin_year = int(begin_year)
    except:
        return {'message': '开始年份必须为数字！'}
    if begin_year < 1958 or begin_year > datetime.now().year:
        return {'message': '开始年份不合法！'}
    try:
        end_year = int(end_year)
    except:
        return {'message': '结束年份必须为数字！'}
    if end_year < begin_year:
        return {'message': '结束年份不合法！'}
    try:
        type = int(type)
    except:
        return {'message': '项目类型不合法！'}
    if type < 1 or type > 5:
        return {'message': '项目类型不合法！'}
    cursor.execute('SELECT * FROM 项目 WHERE 项目号 = %s', old_id)
    if not cursor.fetchall():
        return {'message': '原项目号不存在！'}
    cursor.execute('SELECT * FROM 项目 WHERE 项目号 = %s', id)
    if cursor.fetchall() and old_id != id:
        return {'message': '新项目号已存在！'}
    totol_funds = 0
    leaderids = []
    for leader_id, leader_funds in leaders:
        cursor.execute('SELECT * FROM 教师 WHERE 工号 = %s', leader_id)
        if not cursor.fetchall():
            return {'message': '负责人工号不存在！'}
        try:
            leader_funds = float(leader_funds)
        except:
            return {'message': '负责人经费必须为数字！'}
        if leader_funds < 0:
            return {'message': '负责人经费不能为负数！'}
        totol_funds += leader_funds
        leaderids.append(leader_id)
    if len(leaderids) != len(set(leaderids)):
        return {'message': '不能有重复负责人！'}
    if totol_funds - funds > 0.0001 or totol_funds - funds < -0.0001:
        return {'message': '负责人经费之和必须等于总经费！'}
    cursor.execute('DELETE FROM 承担项目 WHERE 项目号 = %s', old_id)
    cursor.execute('UPDATE 项目 SET 项目号=%s, 项目名称=%s, 项目来源=%s, 项目类型=%s, 总经费=%s, 开始年份=%s, 结束年份=%s WHERE 项目号=%s', (id, name, source, type, funds, begin_year, end_year, old_id))
    i = 1
    for leader_id, leader_funds in leaders:
        leader_funds = float(leader_funds)
        cursor.execute('INSERT INTO 承担项目 VALUES (%s, %s, %s, %s)', (leader_id, id, i, leader_funds))
        i += 1
    conn.commit()
    cursor.close()
    conn.close()
    return {'message': '修改成功！点击确定关闭页面。'}
