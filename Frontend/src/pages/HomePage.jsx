// src/pages/HomePage.jsx
import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import DailyStats from '../components/Home/DailyStats';
import GoalProgress from '../components/Home/GoalProgress';
import MoodTracker from '../components/Home/MoodTracker';

import '../styles/HomePage.css'

function HomePage() {
  const { user, logout } = useContext(UserContext);
  const navigate = useNavigate();
  
  // Mock data for hackathon
  const savedAmount = 265; // dollars
  const drinkReduction = 30; // percent

  const handleLogout = () => {
        logout();
  };
  
  return (
    <div className="home-page">
      <header className="home-header">
        <div className="user-info">
          <h1>Hi, {user?.name || 'Friend'}!</h1>
          <div className="user-avatar">
            {/* User avatar could be dynamically loaded */}
            <div className="avatar-placeholder"></div>
          </div>
        </div>
        
        <div className="chat-button-container">
          <button 
            onClick={() => navigate('/chat')}
            className="chat-button"
          >
            Chat with SipControl
          </button>
          <button onClick={handleLogout}>
        Logout
        </button>
        </div>
  
        

      </header>
      
      <main className="home-content">
        <section className="stats-section">
          <DailyStats days={user?.soberDays || 5} />
        </section>
        
        <section className="savings-section">
          <div className="savings-card">
            <div className="savings-item">
              <span className="savings-label">Money Saved</span>
              <span className="savings-value">${savedAmount}</span>
            </div>
            <div className="savings-item">
              <span className="savings-label">Drink Reduction</span>
              <span className="savings-value">{drinkReduction}%</span>
            </div>
          </div>
        </section>
        
        <section className="progress-section">
        <GoalProgress 
            current={user?.soberDays || 5} 
            target={user?.targetDays || 30} 
          />
        </section>
        
        <section className="mood-section">
          <MoodTracker />
        </section>
        
        
      </main>
    </div>
  );
}

export default HomePage;