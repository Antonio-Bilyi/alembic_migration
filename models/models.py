from sqlalchemy import Column, Date, String, Integer, CheckConstraint
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Group(Base):

    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)

class Teacher(Base):

    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)

class Student(Base):

    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    email = Column(String(32), nullable=False, unique=True)
    group_id = Column(Integer, ForeignKey(Group.id, ondelete='CASCADE'))

class Subject(Base):

    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    teacher_id = Column(Integer, ForeignKey(Teacher.id, ondelete='SET NULL'), nullable=False)

class Grade(Base):

    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(Student.id, ondelete='CASCADE'))
    subject_id = Column(Integer, ForeignKey(Subject.id, ondelete='CASCADE'))
    grade = Column(Integer, CheckConstraint('grade BETWEEN 1 AND 100'), nullable=False)
    date = Column(Date, nullable=False)