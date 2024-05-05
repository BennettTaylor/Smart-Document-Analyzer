import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { Login } from './pages/login/login.js'
import { Home } from './pages/home/home.js'
import { Register } from './pages/register/register.js'
import { Dashboard } from './pages/dashboard/dashboard.js'

import { Navbar } from "./components/navbar.js";
import injectContext from "./store/appContext";


function App() {
  return (
    <div>
      <BrowserRouter>
        <Navbar />
        <Routes>
            <Route element={<Home />} path="/" />
            <Route element={<Login />} path="/login" />
            <Route element={<Register />} path="/register" />
            <Route element={<Dashboard />} path="/dashboard" />
            <Route element={<h1>Not found!</h1>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default injectContext(App);
