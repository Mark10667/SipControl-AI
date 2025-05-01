import React, { useState } from 'react';
import { Mic, Send } from 'lucide-react';
import './InputBar.css';

function InputBar({ onSendMessage, disabled }) {
  const [message, setMessage] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };
  
  return (
    <form className="input-bar" onSubmit={handleSubmit}>
        <button 
            type="button" 
            className="voice-button"
            disabled={disabled}
            aria-label='voice-button'
        >
            <div>
                <Mic className='input-icon-mic' size={24} strokeWidth={2}/>
            </div>
        
      </button>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Send a message ..."
        className="message-input"
        disabled={disabled}
      />
      <button type="submit" className="send-button" disabled={disabled}>
        <div>
            <Send />
        </div>
      </button>
    </form>
  );
}

export default InputBar;