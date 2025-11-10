import { useState } from "react";

function Login() {
    async function login(email, password) {
        const res = await fetch("http://localhost:5000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        const data = await res.json();

        if (data.token) {
            localStorage.setItem("token", data.token);
            window.location.href = "/";
        } else {
            alert("Неверный логин или пароль");
        }
    }

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    return (
        <form className="auth-form" onSubmit={(e) => {
            e.preventDefault();
            login(email, password);
        }}>
            <input
                className="form-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Введите ваш email"
                type="email"
                required
            />
            <input
                className="form-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                placeholder="Введите ваш пароль"
                required
            />
            <button className="main-button" type="submit">
                Войти
            </button>
        </form>
    );
}

export default Login;