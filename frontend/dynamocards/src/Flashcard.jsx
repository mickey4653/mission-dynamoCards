// import React from "react";
import PropTypes from "prop-types";

function Flashcard({ term, definition, onDiscard }){
    return(
        <div className="flashcard">
            <h3>{term}</h3>
            <p>{definition}</p>
            <button onClick={onDiscard} style={{marginTop: "10px"}}>
                Discard
            </button>
        </div>
    );

}

// Prop types validation
Flashcard.propTypes = {
    term: PropTypes.string.isRequired,
    definition: PropTypes.string.isRequired,
    onDiscard: PropTypes.func.isRequired,
  };

export default Flashcard;