import { useState } from "react";

function Registration(){
    async function register(email, password) {
        const res = await fetch("http://localhost:5000/api/register",{
            headers: {
                'Content-Type': 'application/json',
            },
            method: "POST",
            body: JSON.stringify({email,password})
        })
        const data = await res.json();
        console.log(data);
    }
    const [email,setEmail] = useState("")
    const [password,setPassword] = useState("")
    return (
        <form onSubmit={e => { e.preventDefault(); register(email, password); }}>
        <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email"/>
        <input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="Пароль"/>
        <button type="submit">Зарегистрироваться</button>
        </form>
    );
}

export default Registration