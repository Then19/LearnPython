from sqlalchemy import Integer, Column, VARCHAR, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    date = Column(VARCHAR(40), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    answer_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    start = Column(Text, nullable=False)

    def __init__(self, title: str, description: str, start: str):
        self.date = datetime.today().strftime("%d.%m.%Y")
        self.answer_id = 0
        self.status = 1
        self.title = title
        self.description = description
        self.start = start

    def __repr__(self):
        return '<Tasks(id: %s, title: %s, description: %s)>' % (self.id, self.title, self.description)

    def get_json(self) -> dict:
        """Возвращает все данные в виде словаря"""
        return {'id': self.id, 'date': self.date, 'title': self.title,
                'description': self.description, 'answer_id': self.answer_id, 'status': self.status}


class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    first_name = Column(VARCHAR(20), nullable=False)
    last_name = Column(VARCHAR(20), nullable=False)
    answer = Column(Text, nullable=False)

    def __init__(self, first_name: str, last_name: str, answer: str, task_id: int):
        self.first_name = first_name
        self.last_name = last_name
        self.answer = answer
        self.task_id = task_id

    def __repr__(self):
        return '<Answers(id: %s, first_name: %s, task_id: %s)>' % (self.id, self.first_name, self.task_id)

    def get_json(self) -> dict:
        """Возвращает все данные в виде словаря"""
        return {'id': self.id, 'task_id': self.task_id, 'first_name': self.first_name,
                'last_name': self.last_name, 'answer': self.answer}


class TaskRequest(Base):
    __tablename__ = "task_request"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    start = Column(Text, nullable=False)
    comment = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)

    def __init__(self, title: str, description: str, start: str, comment: str):
        self.status = 1
        self.title = title
        self.description = description
        self.start = start
        self.comment = comment

    def __repr__(self):
        return '<RequestTask(id: %s, title: %s, description: %s)>' % (self.id, self.title, self.description)


class Journal(Base):
    __tablename__ = "journal"

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(20), nullable=False)
    last_name = Column(VARCHAR(20), nullable=False)
    task_id = Column(Integer, nullable=False)
    answer_id = Column(Integer, nullable=False)
    grade = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)

    def __init__(self, answer: Answers, grade: int, comment: str):
        self.first_name = answer.first_name
        self.last_name = answer.last_name
        self.task_id = answer.task_id
        self.answer_id = answer.id
        self.grade = grade
        self.comment = comment

    def __repr__(self):
        return '<Journal(id: %s, last_name: %s, gradle: %s)>' % (self.id, self.last_name, self.grade)

    def get_json(self) -> dict:
        """Возвращает все данные в виде словаря"""
        return {'id': self.id, 'task_id': self.task_id, 'first_name': self.first_name,
                'last_name': self.last_name, 'answer_id': self.answer_id, 'grade': self.grade,
                'comment': self.comment}
