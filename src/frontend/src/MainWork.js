import React, { useState } from "react";
import "./MainWork.css";
import "./Home.css";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

function MainWork() {
  const [name, setName] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    // alert("FILE RECEIVED!");
    const file = event.target.files[0];
    setSelectedFile(file); // Get the file from the event
  };
  const handleUpload = () => {
    const formData = new FormData();
    formData.append("pdf_file", selectedFile);
    formData.append("course_name", name);

    fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData,
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        if (data.auth_url) {
          window.location.href = data.auth_url;
        }
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <h1>PDF Uploader</h1>
          <p>Upload your Syllabus: </p>

          <input
            className="modern-input2"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
          />
        </div>
        <div>
          <p>Enter Course Name: </p>

          <input
            className="modern-input"
            type="text"
            placeholder="Type something..."
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div>
          <button
            className="lets-go-btn"
            style={{ marginTop: "20%" }}
            onClick={handleUpload}
          >
            {" "}
            Let's go{" "}
          </button>
        </div>
      </header>
    </div>
  );
}
export default MainWork;
