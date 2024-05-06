// FileDetails.js
import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { Context } from '../../store/appContext';
import "./filedetails.css";

export const FileDetails = () => {
    const { id } = useParams(); // Get the file ID from URL params
    const { store } = useContext(Context);
    const [fileDetails, setFileDetails] = useState(null);

    useEffect(() => {
        fetchFileDetails();
    }, []);

    const fetchFileDetails = async () => {
        try {
            const response = await fetch(`http://localhost:5000/get_file_details/${id}`, {
                headers: {
                    Authorization: `Bearer ${store.token}`
                }
            });
            if (!response.ok) {
                throw new Error('Failed to fetch file details');
            }
            const data = await response.json();
            setFileDetails(data.fileDetails);
        } catch (error) {
            console.error(error.message);
        }
    };

    return (
        <div>
            <h2>File Details</h2>
            {fileDetails && (
                <div>
                    <h3>File Analysis:</h3>
                    <p>File Name:{fileDetails.filename}</p>
                    <p>Text: {fileDetails.text}</p>
                    <p>Summary: {fileDetails.document_summary}</p>
                    <p>Sentiment Score: {fileDetails.sentiment_score}</p>
                    <p>Keyword: {fileDetails.keywords}</p>
                    {/* Add more details as needed */}
                    <h2>List of Paragraphs</h2>
                        {fileDetails.paragraphs.map((paragraph, index) => (
                            <div key={index}>
                            <p><strong>Paragraph {index + 1}</strong></p>
                            <p>Text: {paragraph.text}</p>
                            <p>Sentiment Score: {paragraph.sentiment_score}</p>
                            <p>Keyword: {paragraph.keywords}</p>
                        </div>
                        ))}
                </div>
            )}
        </div>
    );
};