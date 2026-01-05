function MainWork() {

  // This function runs when the user picks a file
  const handleFileChange = (event) => {
    const file = event.target.files[0]; // Get the file from the event
    
    if (!file) return;

    // Same "Package and Ship" logic as before
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
        {/* In React, we use the onChange prop instead of addEventListener */}
        <input 
            type="file" 
            accept=".pdf" 
            onChange={handleFileChange} 
        />
        </div>   
        </header>
    </div>

    );
    }

export default MainWork;
