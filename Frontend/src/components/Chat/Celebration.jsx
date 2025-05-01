// src/components/Chat/Celebration.jsx
import React from 'react';
import './Celebration.css';

function Celebration() {
  return (
    <div className="celebration">
      <div className="confetti-container">
        {/* Simple confetti animation */}
        {Array.from({ length: 50 }).map((_, i) => (
          <div 
            key={i} 
            className="confetti"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              backgroundColor: `hsl(${Math.random() * 360}, 80%, 60%)`
            }}
          />
        ))}
      </div>
      <div className="milestone">
        <h3>5 days</h3>
        <p>Stay sober 3 more days until you reach your goal!</p>
      </div>
    </div>
  );
}

export default Celebration;