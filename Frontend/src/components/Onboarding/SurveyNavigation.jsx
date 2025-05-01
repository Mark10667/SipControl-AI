// src/components/Onboarding/SurveyNavigation.jsx
import React from 'react';
import './Survey.css';

function SurveyNavigation({ isFirstStep, isLastStep, onNext, onPrevious, canProgress }) {
  return (
    <div className="survey-navigation">
      {!isFirstStep && (
        <button 
          onClick={onPrevious}
          className="nav-button previous-button"
        >
          Previous
        </button>
      )}
      
      <button 
        onClick={onNext}
        disabled={!canProgress}
        className={`nav-button continue-button ${!canProgress ? 'disabled' : ''}`}
      >
        {isLastStep ? 'Finish' : 'Continue'}
      </button>
    </div>
  );
}

export default SurveyNavigation;