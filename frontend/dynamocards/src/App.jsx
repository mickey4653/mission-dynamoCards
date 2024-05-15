import {useState} from 'react';
import axios from 'axios';
import Flashcard from './Flashcard';
import './Flashcard.css';
import './App.css';

function App(){
    const [youtubeLink, setYoutubeLink ] = useState("");
    const [keyConcepts, setKeyConcepts] = useState([]);
    const [error, setError] = useState(null);

    const handleLinkChange = (event) =>{
        setYoutubeLink(event.target.value);
    };

    const sendLink = async () =>{
        try{
            const response = await axios.post("http://localhost:8000/analyze_video", {
                youtube_link: youtubeLink,
            });
            console.log("Response data:", response.data);
            // setKeyConcepts(response.data);
            
            
            // console.log(data);
            // Check if the response contains key concepts
            if(response.data && response.data.key_concepts && response.data.key_concepts.length > 0){
                 // Combine terms and definitions into pairs
                 const combinedConcepts = response.data.key_concepts.map(concept => ({
                    term: Object.keys(concept)[0],
                    definition: Object.values(concept)[0]
                }));
                setKeyConcepts(combinedConcepts)
                setError(null); // Clear any Previous errors
            }
            else{
                setKeyConcepts([]);
                // console.error("Data does not contain key concepts: ", data);
                setError("No key concepts found for this video.");
            }
            
    }catch (error){
        console.log("Error:", error);
        setError("An error occurred. Please try again later."); // Set Error message
        setKeyConcepts([]); // Clear Key Concepts
    }
};

const discardFlashcard = (index) =>{
    setKeyConcepts(currentConcepts => currentConcepts.filter((_, i) => i !== index));
};
    return(
        <div className='App'>
            <h1>Youtube Link to Flashcards Generator</h1>
            <div className="input-container">
            <input 
            type="text"
            placeholder='Paste Youtube Link Here'
            value={youtubeLink}
            onChange={handleLinkChange}
            />
            <button className='generate-button' onClick={sendLink}>
                Generate Flashcards
            </button>
            </div>
            {error &&  
            <div className='error'>
                {error}
            </div>} {/* Display Error message if error is not null */}
            {keyConcepts.length > 0 && (
                <div className='response-container'>
                    <h2>Response Data: </h2>
                    {/* <p>{JSON.stringify(keyConcepts, null, 2)}</p> */}
                    <div className='flashcards-container'>
                        {keyConcepts.map((concept, index) => (
                            <Flashcard 
                                key ={index}
                                term={concept.term}
                                definition={concept.definition}
                                onDiscard ={()=> discardFlashcard(index)}
                            />    
                        ))}
                    </div>                
                </div>
            )}
        </div>
    );
}

export default App;