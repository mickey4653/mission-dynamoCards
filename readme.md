# Dynamo Flash Cards App

Transform educational YouTube content into interactive flashcards with ease!

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Introduction
The Dynamo Flash Cards App is a web application that allows users to extract key concepts from educational YouTube videos and convert them into flashcards. It simplifies the learning process by condensing lengthy video content into digestible flashcards, making it easier for learners to review and retain information.

## Features
- **YouTube Video Analysis**: Extracts text content from YouTube videos using AI-powered text processing.
- **Flashcard Generation**: Converts extracted key concepts into interactive flashcards.
- **Customizable**: Users can discard flashcards, customize display settings, and more.
- **Error Handling**: Provides informative error messages in case of invalid YouTube links or processing errors.
- **Scalable Backend**: Utilizes FastAPI and Google VertexAI for efficient backend processing.

## Installation
1. Clone the repository: `git clone https://github.com/your-username/dynamo-flash-cards.git`
2. Navigate to the project directory: `cd dynamo-flash-cards`
3. Install dependencies: `npm install` (for frontend) and `pip install -r requirements.txt` (for backend)

## Usage
1. Start the frontend server: `npm start` or `npm run dev`
2. Start the backend server: `uvicorn main:app --reload`
3. Open your browser and visit `http://localhost:3000`
4. Paste a YouTube link into the input field and click "Generate Flashcards"
5. Explore the generated flashcards and discard as needed

## Contributing
Contributions are welcome! If you'd like to contribute to the Dynamo Flash Cards App, please follow these steps:
1. Fork the repository
2. Create your feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License
This project is licensed under the [MIT License](LICENSE).
