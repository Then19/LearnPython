from app import db
from tools.modeles import Answers, Tasks, TaskRequest, Journal
from .validation import validate_fname_lname as valid


def get_main_tasks() -> list[dict]:
    """Получить актуальные задания"""
    tasks = Tasks.query.filter_by(status=1).all()
    return [i.get_json() for i in tasks]


def get_archive_tasks() -> list[dict]:
    """Получить задания из архива"""
    tasks = Tasks.query.filter_by(status=2).all()
    return [i.get_json() for i in tasks]


def add_new_answer(first_name: str, last_name: str, answer: str, task_id: int) -> Answers:
    """Добавить новый ответ"""
    answer = Answers(first_name, last_name, answer, task_id)
    db.session.add(answer)
    db.session.commit()
    return answer


def add_new_task_request(title: str, description: str, start_code: str, comment: str) -> TaskRequest:
    """Новый запрос на задание"""
    task = TaskRequest(title, description, start_code, comment)
    db.session.add(task)
    db.session.commit()
    return task


def get_answer_by_id(answer_id: int) -> dict:
    """Получить ответ по id"""
    answer: Answers = Answers.query.filter_by(id=answer_id).first()
    return answer.get_json() if answer else {'id': 0, 'task_id': 0, 'first_name': "Имя",
                'last_name': "Фамилия", 'answer': "Лучшего ответа пока нет"}


def get_users():
    """Список пользователей кто давал ответ"""
    ans: list[Answers] = Answers.query.all()
    users_list = [f'{i.last_name} {i.first_name}'.title().strip() for i in ans]
    users = set([i for i in users_list if valid(i)])
    return sorted(list(users))


def get_journal(name: str):
    """возвращает словарь с журналом 0 - не выполнено, 1 - не проверено, 2 - есть оценка"""
    first_name = name.split()[-1]
    last_name = name.split()[0]

    journal = {}
    tasks: list[Tasks] = Tasks.query.all()
    for i in tasks:
        journal[i.id] = 0

    ans: list[Answers] = Answers.query.filter_by(first_name=first_name, last_name=last_name).all()
    for i in ans:
        journal[i.task_id] = 1

    jr: list[Journal] = Journal.query.filter_by(first_name=first_name, last_name=last_name).all()
    for i in jr:
        journal[i.task_id] = 2 if i.grade > 5 else 3

    return list(journal.items())


def get_user_answers(name: str, task_id: str):
    """Возвращает словарь с ответами пользователя, оценкой и комментарием"""
    first_name = name.split()[-1]
    last_name = name.split()[0]

    answers = Answers.query.filter_by(first_name=first_name, last_name=last_name, task_id=task_id).all()
    grade = Journal.query.filter_by(first_name=first_name, last_name=last_name, task_id=task_id).all()

    last_grade = grade[-1].get_json() if grade else {}

    return {'answers': [i.get_json() for i in answers], 'grade': last_grade}


if __name__ == "__main__":
    db.create_all()

