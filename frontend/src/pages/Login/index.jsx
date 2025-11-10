import { useState } from "react";
import Registration from "../../components/Registration"
import Login from "../../components/Login"
import "./style.css"
function LoginPage(){
    const [activeTab, setActiveTab] = useState('register');

    return (
        <div className="login-page">
            <img 
                src="/src/assets/cinema.jpg" 
                alt="Movie background" 
                className="background-image"
            />
            <div className="background-overlay"></div>
            
            <div className="login-container">
                <h1 className="welcome-title">Кинотеатр</h1>
                <p className="welcome-subtitle">Добро пожаловать в мир кино</p>
                
                <div className="auth-buttons">
                    <button 
                        className={`auth-tab ${activeTab === 'register' ? 'active' : ''}`}
                        onClick={() => setActiveTab('register')}
                    >
                        Регистрация
                    </button>
                    <button 
                        className={`auth-tab ${activeTab === 'login' ? 'active' : ''}`}
                        onClick={() => setActiveTab('login')}
                    >
                        Вход
                    </button>
                </div>

                <div className="form-container">
                    {activeTab === 'register' ? (
                        <>
                            <h2 className="form-title">Создать аккаунт</h2>
                            <Registration />
                        </>
                    ) : (
                        <>
                            <h2 className="form-title">Войти в аккаунт</h2>
                            <Login />
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

export default LoginPage