// src/components/Home/GoalProgress.jsx
import React from 'react';

function GoalProgress({ current, target }) {
  const percentage = Math.min(Math.round((current / target) * 100), 100);
  
  return (
    <div className="goal-progress">
      <div className="progress-header">
        <h3>Progress toward your goal</h3>
        <span className="progress-percentage">{percentage}%</span>
      </div>
      
      <div className="progress-bar-container">
        <div 
          className="progress-bar-fill"
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      
      <div className="progress-stats">
        <div className="progress-stat">
          <span className="stat-label">Current</span>
          <span className="stat-value">{current} days</span>
        </div>
        
        <div className="progress-stat">
          <span className="stat-label">Target</span>
          <span className="stat-value">{target} days</span>
        </div>
      </div>
    </div>
  );
}

export default GoalProgress;