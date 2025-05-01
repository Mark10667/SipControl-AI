// src/components/Onboarding/SurveyContainer.jsx
import React from 'react';
import './Survey.css';

function SurveyContainer({ children }) {
  return (
    <div className="survey-container">
      <div className="survey-card">
        {children}
      </div>
    </div>
  );
}

export default SurveyContainer;