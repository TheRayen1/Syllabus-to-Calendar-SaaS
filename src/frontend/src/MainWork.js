import React from 'react'; 
import './App.css';
import './MainWork.css';

const PDFFileSelector = () => {
  const [file, setFile] = React.useState(null);
  const [error, setError] = React.useState('');
  const fileInputRef = React.useRef(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setError('');
    
    if (!selectedFile) return;
    
    // Validate file type
    const isPDF = selectedFile.type === 'application/pdf' || 
                  selectedFile.name.toLowerCase().endsWith('.pdf');
    
    if (!isPDF) {
      setError('Only PDF files are allowed');
      event.target.value = ''; // Reset input
      return;
    }
    
    // Validate file size (10MB max)
    const maxSize = 10 * 1024 * 1024; // 10MB 
    if (selectedFile.size > maxSize) {
      setError('File is too large. Maximum size is 10MB');
      event.target.value = ''; // Reset input
      return;
    }
    
    setFile(selectedFile);
    console.log('Selected PDF:', selectedFile);
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const removeFile = () => {
    setFile(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };
  return (
    <div className="pdf-selector-container">
      <div className="pdf-selector-card">
        <div className="pdf-icon-main">
        </div>
        
        <p className="selector-subtitle">Choose a PDF document from your computer</p>
        
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        
        <button 
          type="button" 
          onClick={handleButtonClick}
          className="lets-go-btn"
        >
          Choose PDF File
        </button>
        
      </div>

      {error && (
        <div className="error-container">
          <span className="error-icon">⚠️</span>
          <span className="error-text">{error}</span>
        </div>
      )}

      {file && (
        <div className="file-preview-container">
          <div className="file-preview-card">
            <div className="file-preview-header">
              <div className="file-preview-info">
                <h4 className="file-name">{file.name}</h4>
              </div>
            </div>            
            <div className="file-actions">
              <button 
                type="button" 
                onClick={removeFile}
                className="file-change-btn"
              >
                Remove
              </button>
              <button 
                type="button" 
                onClick={handleButtonClick}
                className="file-change-btn"
              >
                Change File
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

function MainWork() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Select Your Syllabus File</h1>
        <PDFFileSelector />
      </header>
    </div>
  );
}

export default MainWork;