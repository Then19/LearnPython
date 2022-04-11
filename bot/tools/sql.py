from sqlalchemy import create_engine, Integer, Column, VARCHAR, Table, select, update
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from tools.modeles import Answers, Tasks, Base, TaskRequest, Journal
from config import sql_login


engine = create_engine(sql_login)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def reconnect(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            try:
                session.rollback()
                return func(*args, **kwargs)
            except Exception as ex:
                print(ex)
    return wrapper


@reconnect
def add_new_task(title, task, start=''):
    """Добавляем новый таск"""
    session.add(Tasks(title, task, start))
    session.commit()
    return True


@reconnect
def update_visibility(task_id, vis):
    """Изменяем видимость"""
    u = update(Tasks).where(Tasks.id == task_id).values(status=vis). \
        execution_options(synchronize_session="fetch")
    session.execute(u)
    session.commit()


@reconnect
def get_tasks_by_id(task_id) -> list[Answers]:
    """Получаем массив ответов"""
    session.commit()
    return session.query(Answers).filter_by(task_id=task_id).all()


@reconnect
def get_tasks_by_last_name(last_name, number: int = 0) -> list[Answers]:
    """Получаем массив ответов по фамилии"""
    session.commit()
    return session.query(Answers).filter_by(last_name=last_name).filter(Answers.task_id > number).all()


@reconnect
def get_request_tasks() -> list[TaskRequest]:
    """Получения заданий на проверку"""
    session.commit()
    return session.query(TaskRequest).filter(TaskRequest.status == 1).all()


@reconnect
def update_best_answer(answer_id):
    """Изменяем видимость"""
    task_id = session.query(Answers).filter_by(id=answer_id).first().task_id
    u = update(Tasks).where(Tasks.id == task_id).values(answer_id=answer_id). \
        execution_options(synchronize_session="fetch")
    session.execute(u)
    session.commit()


@reconnect
def set_vis_request(request_id: int, vis: int):
    """vis 0 - отклонить
    vis 1 - принять"""
    u = update(TaskRequest).where(TaskRequest.id == request_id).values(status=vis). \
        execution_options(synchronize_session="fetch")
    session.execute(u)
    session.commit()
    if vis:
        t: TaskRequest = session.query(TaskRequest).filter_by(id=request_id).first()
        add_new_task(t.title, t.description, t.start)


def set_grade(answer_id, grade, comment):
    session.commit()
    ans = session.query(Answers).filter_by(id=answer_id).first()
    session.add(Journal(ans, grade, comment))
    session.commit()
