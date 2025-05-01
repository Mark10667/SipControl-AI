// src/components/Chat/Message.jsx
import React from 'react';
import TipsList from './TipsList';
import Celebration from './Celebration';
import './Message.css';

function Message({ text, sender, specialType }) {
  return (
    <div className={`message ${sender}`}>
        <div className= {`message-avatar ${sender}`}>
            <div className="message-bubble">
            {text}
            </div>
                {sender === 'user' && <div className="user-avatar">
            </div>}
        </div>
      
        {specialType === 'tips' && <TipsList />}
        {specialType === 'celebration' && <Celebration />}
    </div>
  );
}

export default Message;