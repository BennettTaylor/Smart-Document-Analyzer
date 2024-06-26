import React, { useContext } from "react";
import { Context } from "../../store/appContext";
import "./home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
			<h1>{store.message || "Loading message from the backend (make sure your python backend is running)..."}</h1>
		</div>
	);
};