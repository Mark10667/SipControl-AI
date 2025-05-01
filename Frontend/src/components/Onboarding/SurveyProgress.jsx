// src/components/Onboarding/SurveyProgress.jsx
import React from 'react';
import './Survey.css'

function SurveyProgress({ currentStep, totalSteps }) {
  return (
    <div className="survey-progress">
      <div className="progress-indicator">
        Step {currentStep + 1} of {totalSteps}
      </div>
      <div className="progress-bars">
        {Array.from({ length: totalSteps }).map((_, index) => (
          <div 
            key={index} 
            className={`progress-bar ${index <= currentStep ? 'active' : ''}`}
          ></div>
        ))}
      </div>
    </div>
  );
}

export default SurveyProgress;