// Dashboard.js
import React, { useState, useEffect, useContext } from 'react';
import { Context } from "../../store/appContext";
import { useNavigate } from 'react-router-dom';
import "./dashboard.css";

export const Dashboard = () => {
    const { store } = useContext(Context);;
    const [fileNames, setFileNames] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetchFileNames();
    }, []);

    const fetchFileNames = async () => {
        try {
            const response = await fetch('http://localhost:5000/get_filenames', {
                headers: {
                    Authorization: `Bearer ${store.token}`
                }
            });
            if (!response.ok) {
                throw new Error('Failed to fetch file names');
            }
            const data = await response.json();
            setFileNames(data.file_names);
        } catch (error) {
            console.error(error.message);
        }
    };

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        try {
            const formData = new FormData();
            formData.append('file', selectedFile);

            const response = await fetch('http://localhost:5000/upload_file', {
                method: 'POST',
                body: formData,
                headers: {
                    Authorization: `Bearer ${store.token}`
                }
            });
            if (!response.ok) {
                throw new Error('Failed to upload file');
            }
            fetchFileNames();
        } catch (error) {
            console.error(error.message);
        }
    };

    return (
        <div>
            <h2>Dashboard</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
            <div>
            <h2>File List</h2>
            <ul>
                {fileNames.map((fileName, index) => (
                    <li key={index}>
                        <Link to={`/file/${fileName.id}`}>{fileName.name}</Link>
                    </li>
                ))}
            </ul>
        </div>
        </div>
    );
};