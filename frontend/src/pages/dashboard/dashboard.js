import React, { useContext } from "react";
import { Context } from "../../store/appContext";
import "./dashboard.css";

export const Dashboard = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
			<h1>Hello Bennett!!</h1>
			<div className="alert alert-info">
				{store.message || "Loading message from the backend (make sure your python backend is running)..."}
			</div>
		</div>
	);
};