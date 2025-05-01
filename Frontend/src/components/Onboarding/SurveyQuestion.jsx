// src/components/Onboarding/SurveyQuestion.jsx
import React from 'react';
import './Survey.css';

function SurveyQuestion({ question, value, onChange }) {
  const { id, text, type, options, min, max, unit } = question;

  // Different question types based on the Figma design
  switch (type) {
    case 'select':
      return (
        <div className="survey-question">
          <h2 className="question-text">{text}</h2>
          <div className="options-container">
            {options.map((option, index) => (
              <button
                key={index}
                className={`option-button ${value === option ? 'selected' : ''}`}
                onClick={() => onChange(option)}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      );
    
    case 'radio':
      return (
        <div className="survey-question">
          <h2 className="question-text">{text}</h2>
          <div className="radio-options">
            {options.map((option, index) => (
              <label key={index} className="radio-option">
                <input
                  type="radio"
                  name={id}
                  checked={value === option}
                  onChange={() => onChange(option)}
                />
                <span className="radio-label">{option}</span>
              </label>
            ))}
          </div>
        </div>
      );
    
    case 'slider':
      return (
        <div className="survey-question">
          <h2 className="question-text">{text}</h2>
          <div className="numeric-container">
            <div className="numeric-value">
              {value || min || 0}
              <span className="unit-label">{unit}</span>
            </div>
          </div>
          <div className="slider-container">
            <input
              type="range"
              min={min || 0}
              max={max || 100}
              value={value || min || 0}
              onChange={(e) => onChange(parseInt(e.target.value))}
              className="slider-input"
              step="1"
            />
          </div>
        </div>
      );
    
    case 'numeric-display':
      // For height/weight display with figure
      return (
        <div className="survey-question">
          <h2 className="question-text">{text}</h2>
          <div className="measurement-display">
            <div className="measurement-value">
              {value}<span className="unit-label">{unit}</span>
            </div>
            <div className="measurement-figure">
              {/* Here you would add your figure/illustration */}
              <div className="figure-placeholder"></div>
            </div>
          </div>
        </div>
      );
      
    case 'date-range':
      return (
        <div className="survey-question">
          <h2 className="question-text">{text}</h2>
          <div className="date-range-container">
            {options.map((option, index) => (
              <button
                key={index}
                className={`date-option ${value === option ? 'selected' : ''}`}
                onClick={() => onChange(option)}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      );
    
    case 'multi-select':
      return (
        <div className="survey-question">
          <h2 className="question-text">{text}</h2>
          <div className="multi-select-container">
            {options.map((option, index) => {
              const isSelected = Array.isArray(value) && value.includes(option);
              
              const handleToggle = () => {
                if (Array.isArray(value)) {
                  if (isSelected) {
                    onChange(value.filter(item => item !== option));
                  } else {
                    onChange([...value, option]);
                  }
                } else {
                  onChange([option]);
                }
              };
              
              return (
                <div 
                  key={index} 
                  className={`multi-select-option ${isSelected ? 'selected' : ''}`}
                  onClick={handleToggle}
                >
                  <div className="checkbox"></div>
                  <span>{option}</span>
                </div>
              );
            })}
          </div>
        </div>
      );
    
    default:
      return (
        <div className="survey-question">
          <h2 className="question-text">{text}</h2>
          <input
            type="text"
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            className="text-input"
            placeholder="Type your answer..."
          />
        </div>
      );
  }
}

export default SurveyQuestion;