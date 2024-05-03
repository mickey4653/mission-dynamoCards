import {useState} from 'react';
import axios from 'axios';

function App(){
    const [youtubeLink, setYoutubeLink ] = useState("");
    const [responseData, setResponseData] = useState(null);
    const [error, setError] = useState(null);

    const handleLinkChange = (event) =>{
        setYoutubeLink(event.target.value);
    };

    const sendLink = async () =>{
        try{
            const response = await axios.post("http://localhost:8000/analyze_video", {
                youtube_link: youtubeLink,
            });
            setResponseData(response.data);
            setError(null); // Clear any Previous errors
    }catch (error){
        console.log(error);
        setError("An error occurred. Please try again later."); // Set Error message
    }
};

    return(
        <div className='App'>
            <h1>Youtube Link to Flashcards Generator</h1>
            <input 
            type="text"
            placeholder='Paste Youtube Link Here'
            value={youtubeLink}
            onChange={handleLinkChange}
            />
            <button onClick={sendLink}>
                Generate Flashcards
            </button>
            {error &&  
            <div className='error'>
                {error}
            </div>} {/* Display Error message if error is not null */}
            {responseData && (
                <div>
                    <h2>Response Data: </h2>
                    <p>{JSON.stringify(responseData, null, 2)}</p>
                </div>
                )}
        </div>
    )
}

export default App;