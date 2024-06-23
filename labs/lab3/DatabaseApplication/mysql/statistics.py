import pymysql as mysql

def get_statistics(id, begin_year, end_year):
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    if not id:
        return "请输入工号"
    if not begin_year:
        return "请输入起始年份"
    if not end_year:
        return "请输入结束年份"
    cursor.execute('SELECT * FROM 教师 WHERE 工号 = %s', (id,))
    teacher_data = cursor.fetchone()
    if not teacher_data:
        return "工号不存在！"
    try :
        begin_year = int(begin_year)
        end_year = int(end_year)
    except:
        return "年份必须为整数！"
    if begin_year > end_year:
        return "起始年份不能大于结束年份！"
    teacher = {}
    teacher['id'], teacher['name'], teacher['gender'], teacher['title'] = teacher_data
    teacher['title'] = ['','博士后' , '助教', '讲师', '副教授', '特任教授', '教授', '助理研究员', '特任副研究员', '副研究员', '特任研究员', '研究员'][teacher['title']]
    teacher['gender'] = '男' if teacher['gender'] == 1 else '女'
    cursor.execute('SELECT * FROM 主讲课程 WHERE 工号 = %s AND 年份 >= %s AND 年份 <= %s', (id, begin_year, end_year))
    courses_data = cursor.fetchall()
    courses = []
    for _, course_id, year, term, hours in courses_data:
        course = {}
        course['id'] = course_id
        course['year'] = year
        course['term'] = ['', '春季学期', '夏季学期', '秋季学期'][term]
        course['hours'] = hours
        cursor.execute('SELECT * FROM 课程 WHERE 课程号 = %s', (course_id,))
        course_data = cursor.fetchone()
        _, course['name'], _, course['type'] = course_data
        course['type'] = ['', '本科生课程', '研究生课程'][course['type']]
        courses.append(course)

    if not courses:
        courses = None

    cursor.execute('SELECT 项目.项目号, 项目.项目名称, 项目.项目来源, 项目.项目类型, 项目.总经费, 承担项目.承担经费, 项目.开始年份, 项目.结束年份 FROM 项目, 承担项目 WHERE 项目.项目号=承担项目.项目号 AND 承担项目.工号 = %s AND 项目.结束年份 >= %s AND 项目.开始年份 <= %s', (id, begin_year, end_year))
    projects_data = cursor.fetchall()
    projects = []
    for project_id, name, source, type, funds, leader_funds, project_begin_year, project_end_year in projects_data:
        project = {}
        project['id'] = project_id
        project['name'] = name
        project['source'] = source
        project['type'] = ['', '国家级', '省部级', '市厅级', '企业合作', '其他类型'][type]
        project['funds'] = funds
        project['leader_funds'] = leader_funds
        project['begin_year'] = project_begin_year
        project['end_year'] = project_end_year
        projects.append(project)

    if not projects:
        projects = None

    cursor.execute('SELECT 论文.序号, 论文.论文名称, 论文.发表源, 论文.发表年份, 论文.类型, 论文.级别, 发表论文.排名, 发表论文.是否通讯作者 FROM 论文, 发表论文 WHERE 论文.序号=发表论文.序号 AND 发表论文.工号 = %s AND 论文.发表年份 >= %s AND 论文.发表年份 <= %s', (id, begin_year+'-1-1', end_year+'-1-1'))
    papers_data = cursor.fetchall()
    papers = []
    for paper_id, title, source, year, type, level, rank, is_corresponding_author in papers_data:
        paper = {}
        paper['id'] = paper_id
        paper['title'] = title
        paper['source'] = source
        paper['year'] = str(year).split('-')[0]
        paper['type'] = ['', 'full paper', 'short paper', 'poster paper', 'demo paper'][type]
        paper['level'] = ['', 'CCF-A', 'CCF-B', 'CCF-C', '中文 CCF-A', '中文 CCF-B', '无等级'][level]
        paper['rank'] = rank
        paper['corresponding'] = '是' if is_corresponding_author else '否'
        papers.append(paper)

    if not papers:
        papers = None

    cursor.close()
    conn.close()
    return teacher, courses, papers, projects