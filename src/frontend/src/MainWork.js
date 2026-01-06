import React, { useState } from 'react';
import './MainWork.css';
import './Home.css'
function MainWork() {
    const [name, setName] = useState("");
    const [selectedFile, setSelectedFile] = useState(null);


  const handleFileChange = (event) => {
    alert("FILE RECEIVED!");   
   const file = event.target.files[0];
    setSelectedFile(file) // Get the file from the event    
  }
    const handleUpload = () => {
        alert("retrieving successful!")
    const formData = new FormData();
    formData.append('pdf_file', selectedFile);
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
    <div> 
        <button className= "lets-go-btn" style = {{marginTop: '20%'}} onClick= {handleUpload} > Let's go </button>
    </div>
        </header>
    </div>
    

    );
}
export default MainWork;
