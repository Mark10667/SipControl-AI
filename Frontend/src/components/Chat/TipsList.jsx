// src/components/Chat/TipsList.jsx
import React from 'react';
import './TipsList.css';

function TipsList() {
  const tips = [
    {
      id: 1,
      title: "Plan Your Response",
      description: "Decide before the party how you'll respond if offered a drink. Simple, direct responses work well, such as:",
      examples: [
        "No, thanks.",
        "I'm driving tonight.",
        "I have an early morning tomorrow."
      ]
    },
    {
      id: 2,
      title: "Hold a Non-Alcoholic Drink",
      description: "Carry a soda, seltzer, or mocktail."
    },
    {
      id: 3,
      title: "Engage in Activities",
      description: "Focus on dancing, eating, or socializing to shift attention away from drinking."
    }
  ];
  
  return (
    <div className="tips-list">
      <h3>Tips for Handling Parties and Saying "No" to Alcohol</h3>
      
      {tips.map((tip) => (
        <div key={tip.id} className="tip-item">
          <h4>{tip.id}. {tip.title}</h4>
          <p>{tip.description}</p>
          
          {tip.examples && (
            <ul>
              {tip.examples.map((example, index) => (
                <li key={index}>{example}</li>
              ))}
            </ul>
          )}
        </div>
      ))}
      
      <div className="resources-link">
        <p>Looking for more tips? Check the sources below:</p>
        <div className="video-link">
          <img src="https://www.youtube.com/watch?v=IstU4uhe6fQ" alt="Video thumbnail" />
          <p>7 Ways to say no to a drink</p>
        </div>
      </div>
    </div>
  );
}

export default TipsList;