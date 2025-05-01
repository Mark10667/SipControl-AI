// src/components/Home/DailyStats.jsx
import React from 'react';

function DailyStats({ days }) {
  return (
    <div className="daily-stats">
      <div className="stat-circle">
        <span className="stat-value">{days}</span>
        <span className="stat-label">days</span>
      </div>
      <div className="stat-description">
        <p>Your current streak</p>
        <p className="stat-subtitle">Keep it going!</p>
      </div>
    </div>
  );
}

export default DailyStats;