import React from 'react'; 
import './App.css';

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

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="pdf-selector-container">
      <div className="pdf-selector-card">
        <div className="pdf-icon-main">
            <polyline points="14 2 14 8 20 8" />
            <path d="M10 9H8v6h2a2 2 0 0 0 0-4h-2" />
            <path d="M16 9h-2v6h2a2 2 0 0 0 0-4h-2" />
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
          className="select-file-btn"
        >
          Choose PDF File
        </button>
        
        <p className="file-requirements">
          Maximum file size: 10MB • Only .pdf files
        </p>
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
              <div className="file-preview-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#dc2626" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
              </div>
              <div className="file-preview-info">
                <h4 className="file-name">{file.name}</h4>
              </div>
            </div>
            
            <div className="file-actions">
              <button 
                type="button" 
                onClick={removeFile}
                className="remove-file-btn"
              >
                Remove
              </button>
              <button 
                type="button" 
                onClick={handleButtonClick}
                className="change-file-btn"
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
        <h1>Select Your PDF File</h1>
        <PDFFileSelector />
      </header>
    </div>
  );
}

export default MainWork;