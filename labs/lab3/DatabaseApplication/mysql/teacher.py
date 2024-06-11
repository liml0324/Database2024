import pymysql as mysql

def get_all_teachers():
    conn = mysql.connect(
        host='localhost',
        user='root',
        password='MySQL030324',
        database='Faculty'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM 教师')
    teachers_data = cursor.fetchall()
    teachers = []
    for teacher_data in teachers_data:
        teacher = {}
        teacher['id'], teacher['name'], teacher['gender'], teacher['title'] = teacher_data
        teacher['gender'] = '男' if teacher['gender'] == 1 else '女'
        teacher['title'] = ['','博士后' , '助教', '讲师', '副教授', '特任教授', '教授', '助理研究员', '特任副研究员', '副研究员', '特任研究员', '研究员'][teacher['title']]
        teachers.append(teacher)
    cursor.close()
    conn.close()
    return teachers