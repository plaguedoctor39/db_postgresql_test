import psycopg2 as pg


def create_db():  # создает таблицы
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS student (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                gpa NUMERIC(10, 2),
                birth TIMESTAMP WITH TIME ZONE
            );''')
        cur.execute('''CREATE TABLE IF NOT EXISTS course (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );''')
        cur.execute('''CREATE TABLE IF NOT EXISTS student_course (
                    student_id INT REFERENCES student(id),
                    course_id INT REFERENCES course(id),
                    CONSTRAINT student_course_pk PRIMARY KEY(student_id, course_id)
                );''')


def get_students(course_id):  # возвращает студентов определенного курса
    # students_list = []
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        # cur.execute(f'''SELECT student_id FROM student_course WHERE course_id = {course_id};''', (course_id,))
        # students_ids = cur.fetchall()
        cur.execute(f'''SELECT student.id, student.name, course.name, course_id 
                        FROM student_course 
                        LEFT JOIN student 
                        ON student_id = student.id 
                        LEFT JOIN course 
                        ON course.id = course_id;''', (course_id,))
        # for student_id in students_ids:
        #     students_list.append(get_student(student_id[0]))
        students_list = cur.fetchall()
        return students_list


def add_students(course_id, students):  # создает студентов и
    # записывает их на курс
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        for student in students:
            add_student(student)
            cur.execute('''INSERT INTO student_course(student_id, course_id) VALUES (%s, %s)''',
                        (student['id'], course_id))
        cur.execute('''SELECT * FROM student_course''')
        print(cur.fetchall())


def add_course(course_name):
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        cur.execute('''INSERT INTO course(name) VALUES (%s);''', (course_name,))


def add_student(student):  # просто создает студента
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO student(name, gpa, birth) VALUES (%s, %s, %s);',
                    (student['name'], student['gpa'], student['birth'],))
        cur.execute('''SELECT * FROM student;''')
        print(cur.fetchall())


def get_student(student_id):
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM student WHERE id = {student_id}''', (student_id,))
        cur_student = cur.fetchall()
    return cur_student


if __name__ == '__main__':
    # create_db()
    # student = {'name': 'Михаил',
    #            'gpa': 5,
    #            'birth': '1/8/1999'}
    # add_student(student)
    # add_course('Python-разработчик')
    # print(get_student(1))
    students = []
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        # cur.execute('''DROP TABLE student, course, student_course;''')
        # conn.commit()
        cur.execute('''SElECT * FROM student;''')
        students_list = cur.fetchall()
        for student in students_list:
            curr_student = {'id': student[0],
                            'name': student[1],
                            'gpa': student[2],
                            'birth': student[3]}
            students.append(curr_student)
        # print(students)
        print(get_students(1))
        # cur.execute('''SELECT * FROM student_course;''')
        # print(cur.fetchall())
        # add_students(1, students)
