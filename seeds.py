from datetime import date, timedelta
from random import randint, sample

import faker

from sqlalchemy import insert

from connect_db import Session
from models.models import Group, Teacher, Student, Subject, Grade

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 30
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20
SUBJECTS = ['Математика', 'Історія', 'Фізика', 'Англійська мова', 'Географія']

def generate_fake_data(number_groups, number_teachers, number_students) -> tuple:

    fake_groups = []
    fake_teachers = []
    fake_students = []
    
    fake_data = faker.Faker('uk_UA')

    for i in range(number_groups):
        fake_groups.append(100 + i + 1)
    
    for _ in range(number_teachers):
        fake_teachers.append(fake_data.unique.name())

    for _ in range(number_students):
        name = fake_data.unique.name()
        email = fake_data.unique.email()
        fake_students.append((name, email))
    
    return fake_groups, fake_teachers, fake_students

def prepare_data(groups, teachers, students, subjects) -> tuple:

    for_groups = [{'number': number} for number in groups]

    for_teachers = [{'name': name} for name in teachers]

    teachers_id = sample(range(1, len(teachers) + 1), len(subjects))

    for_subjects = [
        {'name': subject, 'teacher_id': teacher_id}
        for subject, teacher_id in zip(subjects, teachers_id)
    ]

    for_students = [
        {'name': name, 'email': email, 'group_id': randint(1, len(groups))}
        for name, email in students
    ]

    for_grades = []
    start_date = date(2025, 9, 1)
    end_date = date(2026, 6, 25)
    delta_days = (end_date - start_date).days

    for student_id in range(1, len(students) + 1):
        number_of_grades = randint(1, NUMBER_GRADES)

        for _ in range(number_of_grades):
            subject_id = randint(1, len(subjects))
            grade = randint(1, 100)
            grade_date = start_date + timedelta(days=randint(0, delta_days))
            for_grades.append({
                'student_id': student_id,
                'subject_id': subject_id,
                'grade': grade,
                'date': grade_date,
            })
    
    return for_groups, for_teachers, for_subjects, for_students, for_grades

def insert_data_to_db(groups, teachers, subjects, students, grades):

    with Session() as session:
        session.add_all([Group(**g) for g in groups])
        session.flush()

        session.add_all([Teacher(**t) for t in teachers])
        session.flush()

        session.add_all([Subject(**s) for s in subjects])
        session.flush()

        session.add_all([Student(**s) for s in students])
        session.flush()

        session.add_all([Grade(**g) for g in grades])

        session.commit()


if __name__ == '__main__':

    groups, teachers, students = generate_fake_data(NUMBER_GROUPS, NUMBER_TEACHERS, NUMBER_STUDENTS)

    groups, teachers, subjects, students, grades = prepare_data(groups, teachers, students, SUBJECTS)

    insert_data_to_db(groups, teachers, subjects, students, grades)

