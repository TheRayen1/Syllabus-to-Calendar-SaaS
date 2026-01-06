import React, { useState } from 'react';
import './MainWork.css';

function MainWork() {
    const [name, setName] = useState("");

  const handleFileChange = (event) => {
    alert("FUNCTION TRIGGERED!");   



    const file = event.target.files[0]; // Get the file from the event
    
    if (!file) return;

    const formData = new FormData();
    formData.append('pdf_file', file);

    fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data));
  };

  return (
    <div className="App">
      <header className="App-header">

        <div>
        <h1>PDF Uploader</h1>
        <p>Upload your Syllabus: </p>

        <input 
            className= "modern-input2"

            type="file" 
            accept=".pdf" 
            onChange={handleFileChange} 
        />        </div>  
    <div> 
    <p>Enter Course Name: </p>

      <input
       className= "modern-input"
        type="text" 
        placeholder="Type something..."
        value={name} 
        onChange={(e) => setName(e.target.value)} 
      />
    </div>
        </header>
    </div>

    );
    }

export default MainWork;
