import React, {useEffect, useState} from 'react';
import '../styles/tasks.css'
import '../styles/journal.css'
import axios from "axios";

const Journal = () => {
    const [users, setUsers] = useState([])
    const [journal, setJournal] = useState([])

    async function getUsersApi() {
        const response = await axios.get("https://api.imsr.su/journal/users")
        setUsers(response.data.data)
    }

    async function getJournalApi(userName) {
        console.log(userName.split(' ').length)
        if (userName.split(' ').length === 2){
            const response = await axios.get("https://api.imsr.su/journal/jr?name=" + userName)
            setJournal(response.data.data)
        } else {
            const response = await axios.get("https://api.imsr.su/journal/jr")
            setJournal(response.data.data)
        }
        console.log(journal)
    }

    useEffect(() => {
        getUsersApi()
    }, [])

    function getJournal(userName){
        getJournalApi(userName)

    }

    function getColorTask(select) {
        if (select === 1) {
            return "jr-one-task"
        } else if (select === 2) {
            return "jr-two-task"
        }else {
            return "jr-zero-task"
        }
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
            <div className="jr-block">
                {journal.map(jr =>
                    <div key={jr[0]} className={getColorTask(jr[1]) + ' jr-task'}>{jr[0]}</div>
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