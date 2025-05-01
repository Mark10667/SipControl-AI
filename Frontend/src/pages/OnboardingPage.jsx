// src/pages/OnboardingPage.jsx
import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import SurveyContainer from '../components/Onboarding/SurveyContainer';
import SurveyQuestion from '../components/Onboarding/SurveyQuestion';
import SurveyNavigation from '../components/Onboarding/SurveyNavigation';
import SurveyProgress from '../components/Onboarding/SurveyProgress';

import '../components/Onboarding/Survey.css';

function OnboardingPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const { updateUser } = useContext(UserContext);
  const navigate = useNavigate();
  
  // Define survey questions based on your Figma screens
  const questions = [
    {
      id: 'drinkReason',
      text: 'What often do you have a drink containing alcohol?',
      type: 'select',
      options: ['Never', '1-2 times/month', '2-4 times/month', '2-3 times/week', '4+ times/week']
    },
    {
      id: 'drinkGoal',
      text: 'What is your typical day goal with SipControl?',
      type: 'select',
      options: ['Maintain sobriety', 'Reduce drinking', 'Track consumption']
    },
    {
      id: 'target',
      text: 'What type of goal do you want to set?',
      type: 'select',
      options: ['30-day sobriety', '90-day sobriety', 'Reduce to 1 drink/week', 'Custom']
    },
    {
      id: 'motivation',
      text: 'What are your main reasons for seeking this change?',
      type: 'multi-select',
      options: ['Health', 'Relationships', 'Work/studies', 'Financial', 'Other']
    },
    {
      id: 'challenges',
      text: 'Have you experienced any of these challenges?',
      type: 'multi-select',
      options: ['Health issues', 'Relationship problems', 'Work impacts', 'Financial strain', 'None']
    },
    {
      id: 'support',
      text: 'Does someone in your life support your change?',
      type: 'radio',
      options: ['Yes', 'No', 'Not sure']
    },
    {
      id: 'height',
      text: 'What\'s your height?',
      type: 'slider',
      min: 140,
      max: 210,
      unit: 'cm'
    },
    {
      id: 'weight',
      text: 'What\'s your weight?',
      type: 'slider',
      min: 40,
      max: 150,
      unit: 'kg'
    }
    // Add more questions to match your Figma screens
  ];
  
  const handleAnswer = (answer) => {
    setAnswers(prev => ({
      ...prev,
      [questions[currentStep].id]: answer
    }));
  };
  
  const handleNext = () => {
    if (currentStep < questions.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      // Last step completed - finalize onboarding
      completeOnboarding();
    }
  };
  
  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };
  
  const completeOnboarding = () => {
    // Process the collected answers
    const onboardingData = {
      ...answers,
      hasCompletedOnboarding: true,
      soberDays: 0, // Starting point
      targetDays: 30, // Default
      onboardingDate: new Date().toISOString()
    };
    
    // Update user context with onboarding data
    updateUser(onboardingData);
    
    // Navigate to home page
    navigate('/home');
  };
  
  const currentQuestion = questions[currentStep];
  const hasAnswer = !!answers[currentQuestion.id];
  
  // For multi-select, check if at least one option is selected
  const canContinue = 
    currentQuestion.type === 'multi-select' 
      ? Array.isArray(answers[currentQuestion.id]) && answers[currentQuestion.id].length > 0
      : hasAnswer;
  
  return (
    <div className="onboarding-page">
      <div className="app-title">SipControl</div>
      
      <SurveyProgress 
        currentStep={currentStep} 
        totalSteps={questions.length} 
      />
      
      <SurveyContainer>
        <SurveyQuestion
          question={currentQuestion}
          value={answers[currentQuestion.id] || (currentQuestion.type === 'multi-select' ? [] : '')}
          onChange={handleAnswer}
        />
        
        <SurveyNavigation
          isFirstStep={currentStep === 0}
          isLastStep={currentStep === questions.length - 1}
          onNext={handleNext}
          onPrevious={handlePrevious}
          canProgress={canContinue}
        />
      </SurveyContainer>
    </div>
  );
}

export default OnboardingPage;