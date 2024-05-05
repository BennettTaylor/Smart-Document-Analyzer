import React, { useContext, useState } from "react";
import { Context } from "../../store/appContext";
import { useNavigate } from 'react-router-dom';
import "./login.css";

export const Login = () => {
	const { store, actions } = useContext(Context);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleClick= () => {
        actions.login(email, password)
    }
    if (store.token && store.token !== "" && store.token !== undefined) navigate("/");
	return (
		<div className="login-container">
            <div className="login-form">
                <h1 className="login-header">Login</h1>
                {store.token && store.token !== "" && store.token !== undefined ? (
                    <p>You are logged in with this token: {store.token}</p>
                ) : (
                    <form>
                        <input type="text" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>    
                        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>  
                        <button type="button" onClick={handleClick}>Login</button>  
                    </form>
                )}
            </div>
        </div>
	);
};