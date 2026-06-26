from sqlalchemy import select, func, desc, and_

from connect_db import session

from models.models import Group, Teacher, Subject, Student, Grade

#Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1(session):

    return (
        session.query(
            Student.name.label('student'),
            func.round(func.avg(Grade.grade), 1).label('avg_grade')
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc('avg_grade'))
        .limit(5)
        .all()
    )

#Знайти студента із найвищим середнім балом з певного предмета
def select_2(session, subject_id):

    return (
        session.query(
            Student.name.label('name'),
            func.round(func.avg(Grade.grade), 1).label('average_grade'),
            Subject.name.label('subject')
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id, Subject.name)
        .order_by(desc('average_grade'))
        .limit(1)
        .all()
    )

#Знайти середній бал у групах з певного предмета
def select_3(session, subject_id):

    return (
        session.query(
            Group.number.label('group_number'),
            func.round(func.avg(Grade.grade), 1).label('average_grade'),
            Subject.name.label('subject')
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id, Group.number, Subject.name)
        .order_by(desc('average_grade'))
        .all()
    )

#Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4(session):

    return (
        session.query(
            func.round(func.avg(Grade.grade), 1).label('average_grade')
        )
        .select_from(Grade)
        .all()
    )

#Знайти які курси читає певний викладач
def select_5(session, teacher_id):

    return (
        session.query(
            Teacher.name.label('teacher'),
            Subject.name.label('subject')
        )
        .select_from(Subject)
        .join(Teacher)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )

#Знайти список студентів у певній групі
def select_6(session, group_id):

    return (
        session.query(
            Student.name.label('student'),
            Group.number.label('group_number')
        )
        .select_from(Student)
        .join(Group)
        .filter(Student.group_id == group_id)
        .all()
    )

#Знайти оцінки студентів у окремій групі з певного предмета
def select_7(session, group_id, subject_id):

    return (
        session.query(
            Group.number.label('group_number'),
            Student.name.label('student'),
            Grade.grade,
            Subject.name.label('subject')
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(Subject.id == subject_id, Group.id == group_id)
        .all()
    )

#Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(session, teacher_id):

    return (
        session.query(
            Teacher.name.label('teacher'),
            Subject.name.label('subject'),
            func.round(func.avg(Grade.grade)).label('average_grade')
        )
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .filter(Subject.teacher_id == teacher_id)
        .group_by(Teacher.name, Subject.name)
        .all()
    )

#Знайти список курсів, які відвідує певний студент
def select_9(session, student_id):

    return (
        session.query(
            Student.name.label('student'),
            func.string_agg(Subject.name.distinct(), ',').label('subjects')
        )
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .filter(Grade.student_id == student_id)
        .group_by(Student.id, Student.name)
        .all()
    )

#Список курсів, які певному студенту читає певний викладач
def select_10(session, student_id, teacher_id):

    return (
        session.query(
            Teacher.name.label('teacher'),
            Subject.name.label('subject'),
            Student.name.label('student')
        )
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .join(Student)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )

#Середній бал, який певний викладач ставить певному студентові
def select_11(session, student_id, teacher_id):
    
    return (
        session.query(
            Teacher.name.label('teacher'),
            Student.name.label('student'),
            func.round(func.avg(Grade.grade), 1).label('average_grade')          
        )
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .join(Student)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .group_by(Teacher.name, Student.name)
        .all()
    )

#Оцінки студентів у певній групі з певного предмета на останньому занятті
def select_12(session, group_id, subject_id):

    subquery = (
        select(func.max(Grade.date))
        .join(Student)
        .filter(Grade.subject_id == subject_id, Student.group_id == group_id)
        .scalar_subquery()
    )

    return (
        session.query(
            Group.number.label('group_number'),
            Student.name.label('student'),
            Subject.name.label('subject'),
            Grade.grade,
            Grade.date.label('lesson_date')
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(
            Group.id == group_id,
            Subject.id == subject_id,
            Grade.date == subquery
        )
        .all()
    )