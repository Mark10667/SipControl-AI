// src/components/Home/MoodTracker.jsx
import React, { useState } from 'react';

function MoodTracker() {
  const [selectedMood, setSelectedMood] = useState(null);
  const [savedMoods, setSavedMoods] = useState([]);
  
  const moods = [
    { emoji: '😀', name: 'Happy' },
    { emoji: '😊', name: 'Content' },
    { emoji: '😐', name: 'Neutral' },
    { emoji: '😔', name: 'Sad' },
    { emoji: '😠', name: 'Angry' },
    { emoji: '😴', name: 'Tired' }
  ];
  
  const handleSaveMood = () => {
    if (selectedMood !== null) {
      const newMood = {
        mood: moods[selectedMood],
        timestamp: new Date().toISOString()
      };
      
      setSavedMoods([newMood, ...savedMoods]);
      setSelectedMood(null);
    }
  };
  
  return (
    <div className="mood-tracker">
      <h3>How are you feeling today?</h3>
      
      <div className="mood-selector">
        {moods.map((mood, index) => (
          <button
            key={index}
            className={`mood-button ${selectedMood === index ? 'selected' : ''}`}
            onClick={() => setSelectedMood(index)}
          >
            <span className="mood-emoji">{mood.emoji}</span>
          </button>
        ))}
      </div>
      
      {selectedMood !== null && (
        <button 
          className="save-mood-button"
          onClick={handleSaveMood}
        >
          Save Mood
        </button>
      )}
      
      {savedMoods.length > 0 && (
        <div className="mood-history">
          <h4>Recent Moods</h4>
          <div className="mood-history-list">
            {savedMoods.slice(0, 5).map((entry, index) => (
              <div key={index} className="mood-history-item">
                <span className="mood-history-emoji">{entry.mood.emoji}</span>
                <span className="mood-history-time">
                  {new Date(entry.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default MoodTracker;