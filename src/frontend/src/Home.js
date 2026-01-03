import logo from './logo.png';
import './App.css';
import './Home.css';
import MainWork from './MainWork';
import React, { useState } from 'react';

function Home() {
    const [showMainWork, setShowMainWork] = useState(false);

  const goToMainWork = () => {
    setShowMainWork(true);
  };

  if (showMainWork) {
    return <MainWork />;
  }

  return (
    <div className="App">
      <header className="App-header">
      <h1>Syllabus to Calendar App</h1>
      <h3>Le Talent N'existe pas</h3> 
      <button className="lets-go-btn" onClick={goToMainWork}>Let's go</button>

        <img src={logo} className="App-logo" alt="logo" />
      </header>
    </div>
  );
}
export default Home;
