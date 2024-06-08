import pymysql as mysql
from datetime import datetime

def get_paper(id, title, source, year, type, level, authorid):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    level_list = ['', 'CCF-A', 'CCF-B', 'CCF-C', '中文 CCF-A', '中文 CCF-B', '无等级']
    type_list = ['', 'full paper', 'short paper', 'poster paper', 'demo paper']
    cursor = conn.cursor()
    params = []
    if authorid:
        sql = "SELECT Distinct 论文.序号 FROM 论文, 发表论文, 教师 WHERE 论文.序号=发表论文.序号 AND 发表论文.工号=教师.工号 "
    else:
        sql = "SELECT Distinct 论文.序号 FROM 论文 WHERE 1=1 "
    flag=True
    if id:
        try:
            id = int(id)
        except:
            cursor.close()
            conn.close()
            return None 
        if id < 1:
            cursor.close()
            conn.close()
            return None 
        if flag:
            sql += "AND 论文.序号=%s "
            params.append(int(id))
    flag=True
    if title:
        sql += "AND 论文.论文名称 LIKE %s "
        params.append("%"+title+"%")
    if source:
        sql += "AND 论文.发表源 LIKE %s "
        params.append("%"+source+"%")
    if year:
        try:
            year = int(year)
        except:
            cursor.close()
            conn.close()
            return None 
        if year < 1500 or year > datetime.now().year:
            cursor.close()
            conn.close()
            return None 
        if flag:
            sql += "AND 论文.发表年份=%s "
            params.append(str(year)+'-01-01')
    flag=True
    if type:
        
        sql += "AND ("
        for t in type:
            try:
                t = int(t)
            except:
                cursor.close()
                conn.close()
                return None
            if t < 1 or t > 4:
                cursor.close()
                conn.close()
                return None
            
            sql += "论文.类型='%s' OR "
            params.append(int(t))
        sql = sql[:-4] + ') '
    if level:
        sql += "AND ("
        for l in level:
            try:
                l = int(l)
            except:
                cursor.close()
                conn.close()
                return None
            if l < 1 or l > 6:
                cursor.close()
                conn.close()
                return None
            sql += "论文.级别='%s' OR "
            params.append(int(l))
        sql = sql[:-4] + ') '
    if authorid:
        sql += "AND (教师.工号=%s OR 教师.姓名 LIKE %s)"
        params.append(authorid)
        params.append("%"+authorid+"%")
    
    cursor.execute(sql, params)
    paper_ids = cursor.fetchall()
    papers = []
    for paper_id in paper_ids:
        author_names = []
        cursor.execute("SELECT 教师.姓名 FROM 教师, 发表论文 WHERE 发表论文.工号=教师.工号 AND 序号=%s", paper_id)
        author_names.append(cursor.fetchall())
        cursor.execute("SELECT * FROM 论文 WHERE 序号=%s", paper_id)
        paper = {}
        paper['id'], paper['title'], paper['source'], paper['year'], paper['type'], paper['level'] = cursor.fetchone()
        paper['type'] = type_list[paper['type']]
        paper['level'] = level_list[paper['level']]
        paper['year'] = str(paper['year']).split('-')[0]
        author_name_str = ''
        if author_names and author_names[0]:
            for author_name in author_names[0]:
                author_name_str += author_name[0] + ', '
        paper['authors'] = author_name_str[:-2]
        papers.append(paper)
    cursor.close()
    conn.close()
    if papers:
        return papers
    else:
        return None
    
def get_paper_details(id, transaction=True):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not id:
        return None
    try:
        id = int(id)
    except:
        return None
    if id < 1:
        return None
    cursor.execute("SELECT * FROM 论文 WHERE 序号=%s", id)
    paper = cursor.fetchone()
    if not paper:
        return None
    temp = paper
    paper = {}
    paper['id'], paper['title'], paper['source'], paper['year'], paper['type'], paper['level'] = temp
    paper['year'] = str(paper['year']).split('-')[0]
    if transaction:
        paper['type'] = ['', 'full paper', 'short paper', 'poster paper', 'demo paper'][paper['type']]
        paper['level'] = ['', 'CCF-A', 'CCF-B', 'CCF-C', '中文 CCF-A', '中文 CCF-B', '无等级'][paper['level']]

    corresponding = cursor.execute("SELECT 工号 FROM 发表论文 WHERE 序号=%s AND 是否通讯作者=true", id)
    if corresponding:
        corresponding = cursor.fetchone()[0]
        corresponding_name = cursor.execute("SELECT 姓名 FROM 教师 WHERE 工号=%s", corresponding)
        if corresponding_name:
            corresponding_name = cursor.fetchone()[0]
        else:
            corresponding_name = None
    else:
        corresponding = None
    paper['corresponding'] = corresponding_name
    authors = []
    cursor.execute("SELECT 工号, 排名 FROM 发表论文 WHERE 序号=%s", id)
    author_data = cursor.fetchall()
    for authorid, rank in author_data:
        cursor.execute("SELECT * FROM 教师 WHERE 工号=%s", authorid)
        author = {}
        author['id'], author['name'], author['gender'], author['title'] = cursor.fetchone()
        if transaction:
            if author['gender'] == 1:
                author['gender'] = '男'
            else:
                author['gender'] = '女'
        if transaction:
            author['title'] = ['','博士后' , '助教', '讲师', '副教授', '特任教授', '教授', '助理研究员', '特任副研究员', '副研究员', '特任研究员', '研究员'][author['title']]
        author['no'] = rank
        if authorid == corresponding:
            if transaction:
                author['corresponding'] = '是'
            else:
                author['corresponding'] = 1
        else:
            if transaction:
                author['corresponding'] = '否'
            else:
                author['corresponding'] = 0
        authors.append(author)
    cursor.close()
    conn.close()
    return paper, authors

    
def register_paper(id, title, source, year, type, level, authors):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if id == '':
        cursor.execute("SELECT MAX(序号) FROM 论文")
        id = cursor.fetchone()
        if id[0]:
            id = id[0] + 1
        else:
            id = 1
    else:   # 检查id是否为正整数
        try:
            id = int(id)
        except:
            return {'message': '序号必须为正整数！'}
        if id < 1:
            return {'message': '序号必须为正整数！'}
        
    cursor.execute("SELECT * FROM 论文 WHERE 序号=%s", id)
    if cursor.fetchall():
        return {'message': '该编号已被使用！'}
    
    if not title:
        return {'message': '论文名称不能为空！'}
    if not source:
        return {'message': '发表源不能为空！'}
    if not year:
        return {'message': '发表年份不能为空！'}
    if not type:
        return {'message': '论文类型不能为空！'}
    if not level:
        return {'message': '论文级别不能为空！'}
    if not authors:
        return {'message': '作者不能为空！'}
    
    try:
        year = int(year)
    except:
        return {'message': '年份必须为整数！'}
    if year < 1500 or year > datetime.now().year:
        return {'message': '年份不合法！'}
    
    try:
        type = int(type)
    except:
        return {'message': '类型不合法！'}
    if type < 1 or type > 4:
        return {'message': '类型不合法！'}
    
    try:
        level = int(level)
    except:
        return {'message': '级别不合法！'}
    if level < 1 or level > 6:
        return {'message': '级别不合法！'}
    
    if len(authors) < 2:
        return {'message': '通讯作者不能为空！'}

    authorids = authors[0]
    corresponding = authors[1]

    # 检查作者是否存在
    for authorid in authorids:
        cursor.execute("SELECT * FROM 教师 WHERE 工号=%s", authorid)
        if not cursor.fetchall():
            return {'message': '作者工号不存在！'}
        
    # 检查是否有重复作者
    if len(authorids) != len(set(authorids)):
        return {'message': '不能有重复作者！'}
    
    # 检查通讯作者是否合法
    if not corresponding:
        return {'message': '通讯作者不能为空！'}
    
    try:
        corresponding = int(corresponding)
    except:
        return {'message': '通讯作者不合法！'}
    
    if corresponding > len(authorids) or corresponding < 1:
        return {'message': '通讯作者不合法！'}
    
    cursor.execute("INSERT INTO 论文 VALUES (%s, %s, %s, %s, %s, %s)", (id, title, source, str(year)+'-01-01', type, level))
    i = 1
    for authorid in authorids:
        cursor.execute("INSERT INTO 发表论文 VALUES (%s, %s, %s, %s)", (authorid, id, i, i==corresponding))
        i += 1
    conn.commit()
    cursor.close()
    conn.close()
    return {'message': '提交成功！'}

def delete_paper(id):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    # 检查id是否为正整数
    try:
        id = int(id)
    except:
        return "序号不合法！"
    if id < 1:
        return "序号不合法！"
    
    cursor.execute("SELECT * FROM 论文 WHERE 序号=%s", id)
    if not cursor.fetchall():
        return "该编号不存在！"
    
    # 先删除所有关联的发表论文
    cursor.execute("DELETE FROM 发表论文 WHERE 序号=%s", id)
    cursor.execute("DELETE FROM 论文 WHERE 序号=%s", id)
    conn.commit()
    cursor.close()
    conn.close()
    return "删除成功！"

def edit_paper(old_id, id, title, source, year, type, level, authors):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not old_id:
        return {'message': '原序号不能为空！'}
    try:
        old_id = int(old_id)
    except:
        return {'message': '原序号必须为正整数！'}
    if old_id < 1:
        return {'message': '原序号必须为正整数！'}

    
    
    if not title:
        return {'message': '论文名称不能为空！'}
    
    if not source:
        return {'message': '发表源不能为空！'}
    
    if not year:
        return {'message': '发表年份不能为空！'}
    
    if not type:
        return {'message': '论文类型不能为空！'}
    
    if not level:
        return {'message': '论文级别不能为空！'}
    
    try:
        year = int(year)
    except:
        return {'message': '年份必须为整数！'}
    if year < 1500 or year > datetime.now().year:
        return {'message': '年份不合法！'}
    
    try:
        type = int(type)
    except:
        return {'message': '类型不合法！'}
    if type < 1 or type > 4:
        return {'message': '类型不合法！'}
    
    try:
        level = int(level)
    except:
        return {'message': '级别不合法！'}
    if level < 1 or level > 6:
        return {'message': '级别不合法！'}

    if len(authors) < 2:
        return {'message': '通讯作者不能为空！'}
    
    authorids = authors[0]
    corresponding = authors[1]

    # 检查作者是否存在
    for authorid in authorids:
        cursor.execute("SELECT * FROM 教师 WHERE 工号=%s", authorid)
        if not cursor.fetchall():
            return {'message': '作者工号不存在！'}
        
    # 检查是否有重复作者
    if len(authorids) != len(set(authorids)):
        return {'message': '不能有重复作者！'}
    
    # 检查通讯作者是否合法
    if not corresponding:
        return {'message': '通讯作者不能为空！'}
    
    try:
        corresponding = int(corresponding)
    except:
        return {'message': '通讯作者不合法！'}
    
    if corresponding > len(authorids) or corresponding < 1:
        return {'message': '通讯作者不合法！'}
    
    cursor.execute("DELETE FROM 发表论文 WHERE 序号=%s", old_id)
    cursor.execute("DELETE FROM 论文 WHERE 序号=%s", old_id)
    if id == '':
        cursor.execute("SELECT MAX(序号) FROM 论文")
        id = cursor.fetchone()
        if id[0]:
            id = id[0] + 1
        else:
            id = 1
    else:   # 检查id是否为正整数
        try:
            id = int(id)
        except:
            return {'message': '序号必须为正整数！'}
        if id < 1:
            return {'message': '序号必须为正整数！'}
        
    cursor.execute("INSERT INTO 论文 VALUES (%s, %s, %s, %s, %s, %s)", (id, title, source, str(year)+'-01-01', type, level))
    i = 1
    for authorid in authorids:
        cursor.execute("INSERT INTO 发表论文 VALUES (%s, %s, %s, %s)", (authorid, id, i, i==corresponding))
        i += 1
    conn.commit()
    cursor.close()
    conn.close()
    return {'message': '修改成功！点击确定关闭页面。'}


