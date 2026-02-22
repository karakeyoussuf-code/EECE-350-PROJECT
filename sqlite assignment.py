import sqlite3


db = sqlite3.connect("students.conn")
cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS registered_courses (
    student_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    student_id INTEGER,
    course_id INTEGER,
    grade REAL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")


cursor.execute("INSERT INTO student VALUES (1, 'Ali', 20)")
cursor.execute("INSERT INTO student VALUES (2, 'Sara', 22)")

cursor.execute("INSERT INTO grades VALUES (1, 101, 85)")
cursor.execute("INSERT INTO grades VALUES (1, 102, 92)")
cursor.execute("INSERT INTO grades VALUES (2, 101, 78)")
cursor.execute("INSERT INTO grades VALUES (2, 103, 88)")

db.commit()


print("Maximum grades:")
cursor.execute("""
SELECT g.student_id, g.course_id, g.grade
FROM grades g
JOIN (
    SELECT student_id, MAX(grade) AS max_grade
    FROM grades
    GROUP BY student_id
) m
ON g.student_id = m.student_id AND g.grade = m.max_grade
""")

for row in cursor.fetchall():
    print(row)


print("\nAverage grades:")
cursor.execute("""
SELECT student_id, AVG(grade)
FROM grades
GROUP BY student_id
""")

for row in cursor.fetchall():
    print(row)


db.close()