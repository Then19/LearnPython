from flask import request, jsonify, send_from_directory
from app import app
from tools.cors import response
from tools import sql


@app.route('/journal/users', methods=['GET'])
def get_all_users():
    users = sql.get_users()
    return response({'data': users})


@app.route('/journal/jr', methods=['GET'])
def get_journal_by_name():
    name = request.args.get('name', 'None None')
    journal = sql.get_journal(name)
    return response({'data': journal})


@app.route('/journal/grade', methods=["GET"])
def get_grade_answers():
    name = request.args.get('name', 'None None')
    task_id = request.args.get('id', 0)
    lst = sql.get_user_answers(name, task_id)
    return response({'data': lst})
