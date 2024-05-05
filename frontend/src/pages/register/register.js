import React, { useContext, useState } from "react";
import { Context } from "../../store/appContext";
import "./register.css";

export const Register = () => {
	const { store, actions } = useContext(Context);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");

    const handleClick= () => {
        const opts = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(
                {
                    name:  name,
                    email: email,
                    password: password
                }
            )
        }
        fetch('http://localhost:5000/register', opts)
            .then(resp => {
                if(resp.status === 200) return resp.json();
                else alert("Registration failed");
            })
            .then(data => {
                sessionStorage.setItem("token", data.access_token)
            })
            .catch(error => {
                console.error("Error at registration", error);
            })
    }

	return (
		<div className="registration-container">
            <div className="registration-form">
                <h1 className="registration-header">Register</h1>
                <form>
                    <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)}/>
                    <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>    
                    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>   
                    <button type="button" onClick={handleClick}>Register</button>  
                </form>
            </div>
        </div>
	);
};