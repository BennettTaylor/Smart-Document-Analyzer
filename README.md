# EC 530 Smart-Document-Analyzer

## Description

My smart document analyzer application consists of a website frontend built using react.js and a backend api built using react. In the applications users can securely register an account and log in. Once logged in a user can go to their dashboard where they can upload a file, which will add it to a list of files that have already been uploaded. The list of files will be displayed and can be clicked on to bring the user to a page that analyzes the file selected. It will have information including a document summary, sentiment analysis, keywords and the text itself. It will also have the text split into paragraphs, with each paragraph recieving its own sentiment score and keywords.

## Features

- Secure login with jwt
- Storing users and files using SQLAlchemy
- Password encryption
- Natural language processing using vaderSentiment
- Summary generation using facebook's BART large CNN

## Issues

There seems to be an issue with dockerization because of a bug either in python 3.9 or tensorflow which results in the docker image not being able to be generated
