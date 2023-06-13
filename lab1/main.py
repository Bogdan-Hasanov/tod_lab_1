import mysql.connector

# Підключення до бази даних
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql_pwd",
    database="LAB1"
)

# Створення таблиці students
cursor = cnx.cursor()
create_table_query = """
    CREATE TABLE IF NOT EXISTS students (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        age INT,
        email VARCHAR(255)
    )
"""
cursor.execute(create_table_query)

# Додавання 5 студентів
students = [
    ("John Doe", 20, "john.doe@example.com"),
    ("Jane Smith", 22, "jane.smith@example.com"),
    ("Michael Johnson", 19, "michael.johnson@example.com"),
    ("Emily Davis", 21, "emily.davis@example.com"),
    ("Daniel Wilson", 23, "daniel.wilson@example.com")
]
insert_query = "INSERT INTO students (name, age, email) VALUES (%s, %s, %s)"
cursor.executemany(insert_query, students)
cnx.commit()

# Вибірка всіх студентів
select_all_query = "SELECT * FROM students"
cursor.execute(select_all_query)
students = cursor.fetchall()
for student in students:
    print(student)

# Вибірка студента за ім'ям
select_by_name_query = "SELECT * FROM students WHERE name = %s"
cursor.execute(select_by_name_query, ("John Doe",))
student = cursor.fetchone()
print(student)

# Оновлення віку одного зі студентів
update_age_query = "UPDATE students SET age = %s WHERE id = %s"
cursor.execute(update_age_query, (21, 1))
cnx.commit()

# Видалення студента за ідентифікатором
delete_query = "DELETE FROM students WHERE id = %s"
cursor.execute(delete_query, (5,))
cnx.commit()

# Використання транзакцій для додавання студентів
try:
    cursor.execute("START TRANSACTION")

    insert_query = "INSERT INTO students (name, age, email) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, ("Alice Brown", 20, "alice.brown@example.com"))
    cursor.execute(insert_query, ("Bob Johnson", 22, "bob.johnson@example.com"))

    cursor.execute("COMMIT")
except mysql.connector.Error as error:
    print("Transaction failed. Rolling back changes.")
    cursor.execute("ROLLBACK")

# Створення таблиці courses
create_table_query = """
    CREATE TABLE IF NOT EXISTS courses (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        description VARCHAR(255),
        credits INT
    )
"""
cursor.execute(create_table_query)

# Додавання 3 курсів
courses = [
    ("Mathematics", "Advanced calculus", 3),
    ("Physics", "Quantum mechanics", 4),
    ("Computer Science", "Introduction to programming", 3)
]
insert_query = "INSERT INTO courses (name, description, credits) VALUES (%s, %s, %s)"
cursor.executemany(insert_query, courses)
cnx.commit()

# Створення таблиці student_courses
create_table_query = """
    CREATE TABLE IF NOT EXISTS student_courses (
        student_id INT,
        course_id INT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
"""
cursor.execute(create_table_query)

# Заповнення таблиці student_courses даними
insert_query = "INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)"
cursor.execute(insert_query, (1, 1))
cursor.execute(insert_query, (1, 2))
cursor.execute(insert_query, (2, 1))
cnx.commit()

# Вибірка студентів, які вибрали певний курс
select_students_by_course_query = """
    SELECT students.name
    FROM students
    INNER JOIN student_courses ON students.id = student_courses.student_id
    WHERE student_courses.course_id = %s
"""
cursor.execute(select_students_by_course_query, (1,))
students = cursor.fetchall()
for student in students:
    print(student)

# Вибірка курсів, які вибрали студенти за певним ім'ям
select_courses_by_student_query = """
    SELECT courses.name
    FROM courses
    INNER JOIN student_courses ON courses.id = student_courses.course_id
    INNER JOIN students ON students.id = student_courses.student_id
    WHERE students.name = %s
"""
cursor.execute(select_courses_by_student_query, ("John Doe",))
courses = cursor.fetchall()
for course in courses:
    print(course)

# Вибірка студентів та їх курсів за допомогою JOIN
select_students_courses_query = """
    SELECT students.name, courses.name
    FROM students
    INNER JOIN student_courses ON students.id = student_courses.student_id
    INNER JOIN courses ON courses.id = student_courses.course_id
"""
cursor.execute(select_students_courses_query)
results = cursor.fetchall()
for row in results:
    print(row)

# Закриття курсора та з'єднання
cursor.close()
cnx.close()