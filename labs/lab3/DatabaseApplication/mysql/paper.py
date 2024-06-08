import pymysql as mysql

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
    if id:
        sql += "AND 论文.序号=%s "
        params.append(int(id))
    if title:
        sql += "AND 论文.题目 LIKE '%%%s%%' "
        params.append(title)
    if source:
        sql += "AND 论文.来源 LIKE '%%%s%%' "
        params.append(source)
    if year:
        sql += "AND 论文.年份=%s "
        params.append(year+'-01-01')
    if type:
        sql += "AND 论文.类型='%s' "
        params.append(int(type))
    if level:
        sql += "AND 论文.级别='%s' "
        params.append(int(level))
    if authorid:
        sql += "AND 教师.工号=%s "
        params.append(authorid)
    
    print(cursor.execute(sql, params))
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