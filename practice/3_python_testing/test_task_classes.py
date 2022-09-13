"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

from datetime import datetime
import sys, os
import pytest
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/2_python_part_2")

# print(sys.path)
from task_classes import Teacher, Homework, Student


@pytest.fixture
def teacher(scope = "session"):
    yield Teacher('TLast', 'TFirst')

@pytest.fixture
def student(scope = "session"):
    yield Student('SFirst', 'SLast')

@pytest.fixture
def homework_day(scope = "session"):
    yield Homework("Homework", 1)

def test_teacher_init(teacher):
    t = teacher
    assert t.last_name == 'TLast'
    assert t.first_name == 'TFirst'

def test_student_init(student):
    s = student
    assert s.last_name == 'SLast'
    assert s.first_name == 'SFirst'

def test_create_homework(teacher):
    h = teacher.create_homework('Simple homework 1', 1)
    assert h.text == 'Simple homework 1'
    assert h.deadline == datetime.timedelta(days = 1)

def test_do_homework(student, homework_day):
    s = student
    h = homework_day
    result = s.do_homework(h)
    assert result.is_active() == False
    assert result is not None

def test_do_late_homework(student, homework_day):
    h = homework_day
    h.deadline = datetime.timedelta(days = -1)

    result = student.do_homework(h)
    assert result is None