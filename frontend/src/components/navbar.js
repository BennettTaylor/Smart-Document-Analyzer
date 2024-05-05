// Navbar.js
import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";
import "./navbar.css"; // Import the CSS file

export const Navbar = () => {
    const { store, actions } = useContext(Context);

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
			<div className="container">
					<ul>
						<li className="nav-item">
							<Link to="/" className="nav-link">Smart Document Analyzer</Link>
						</li>
						{!store.token ?
							<li className="nav-item">
								<Link to="/register" className="nav-link">Register</Link>
							</li>
							:
							<li className="nav-item">
								<Link to="/dashboard" className="nav-link">Dashboard</Link>
							</li>
						}
						{!store.token ?
							<li className="nav-item">
								<Link to="/login" className="nav-link">Login</Link>
							</li>
							:
							<li className="nav-item">
								<Link to="/" onClick={() => actions.logout()} className="nav-link">Logout</Link>
							</li>
						}
					</ul>
			</div>
        </nav>
    );
};