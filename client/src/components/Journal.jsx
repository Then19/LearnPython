import React, {useEffect, useState} from 'react';
import '../styles/tasks.css'
import '../styles/journal.css'
import axios from "axios";
import cfg from '../config.json'

const Journal = () => {
    const [users, setUsers] = useState([])
    const [journal, setJournal] = useState([])
    const [selectUser, setSelectUser] = useState('')
    const [ansData, setAnsData] = useState({answers: [], grade: {}})
    const [showAns, setShowAns] = useState({})

    async function getUsersApi() {
        const response = await axios.get(cfg.apiUrl + "/journal/users")
        setUsers(response.data.data)
    }

    async function getJournalApi(userName) {
        console.log(userName.split(' ').length)
        if (userName.split(' ').length === 2){
            const response = await axios.get(cfg.apiUrl + "/journal/jr?name=" + userName)
            setJournal(response.data.data)
        } else {
            const response = await axios.get(cfg.apiUrl + "/journal/jr")
            setJournal(response.data.data)
        }
    }

    async function getAnsDataApi(task_id) {
        const response = await axios.get(cfg.apiUrl + "/journal/grade?name=" + selectUser + '&id=' + task_id)
        setAnsData(response.data.data)
    }

    useEffect(() => {
        getUsersApi()
    }, [])

    function getJournal(userName){
        getJournalApi(userName)
        setSelectUser(userName)
        setAnsData({answers: [], grade: {}})
        setShowAns({})
    }

    function getColorTask(select) {
        if (select === 1) {
            return "jr-one-task"
        } else if (select === 2) {
            return "jr-two-task"
        } else if (select === 3) {
            return "jr-three-task"
        }else {
            return "jr-zero-task"
        }
    }

    function render_task(task_id){
        getAnsDataApi(task_id)
        setShowAns({})
    }

    function showAnswer(answer){
        setShowAns(answer)
    }

    function renderAnswer(){
        if (showAns.id === undefined){
            return
        }
        return (
            <div className="Task-open">
                <p className="jr-answer">{showAns.answer}</p>
            </div>
        )
    }

    function renderGrade(){
        if (ansData.grade.grade === undefined){
            return
        }
        let color = "jr-grade-color-green"
        if (ansData.grade.grade < 6){
            color = "jr-grade-color-red"
        }
        return (
            <div className={"jr-open-grade " + color}>
                <p className="jr-answer">Оценка: {ansData.grade.grade}/12</p>
                <p className="jr-answer">Комментарий: {ansData.grade.comment}</p>
            </div>
        )
    }

    return (
        <div className="Tasks-main">
            <div className={"jr-selector"}>
                <select className={"jr-selector-select"} name="" id="" onChange={event => getJournal(event.target.value)}>
                    <option className={"jr-selector-options"} defaultChecked value="">Выберите</option>
                    {users.map(user =>
                        <option key={user} value={user}>{user}</option>
                    )}
                </select>
            </div>
            {renderGrade()}
            <div>
                {ansData.answers.map(item =>
                    <div className="Tasks-task" key={item.id}>
                        <button className={"Tasks-btn"} onClick={() => showAnswer(item)}>
                            <div className="Task-div">
                                <div className={"Tasks-title"}>
                                    <div className={"Task-id"}>Задание #{item.task_id}</div>
                                    <div>Номер ответа: {item.id}</div>
                                </div>
                                <div><span>{item.date}</span></div>
                            </div>
                        </button>
                    </div>
                )}
            </div>
            {renderAnswer()}
            <div className="jr-block">
                {journal.map(jr =>
                    <div key={jr[0]} className={getColorTask(jr[1]) + ' jr-task'} onClick={() => render_task(jr[0])}>{jr[0]}</div>
                )}
            </div>
            <div className={"jr-desc"}>
                <p>Серый - Зададание не выполнено.</p>
                <p>Синий - Зададание выполнено, но не проверено.</p>
                <p>Зеленый - Зададание выполнено и проверено.</p>
            </div>
        </div>
    );
};

export default Journal;