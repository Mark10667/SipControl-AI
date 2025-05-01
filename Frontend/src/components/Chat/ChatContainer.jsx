// src/components/Chat/ChatContainer.jsx
import React, { useState, useRef, useEffect, useContext } from 'react';
import { UserContext } from '../../context/UserContext';

import Message from './Message';
import InputBar from './InputBar';
import './ChatContainer.css';

function ChatContainer() {
  // Messages state
  const { user } = useContext(UserContext);

  const [messages, setMessages] = useState([
    // Initial welcome message
    { 
      id: 1, 
      text: `Good morning ${user?.name || 'there'}! How did you sleep last night? Any cravings or challenges so far today?`, 
      sender: 'bot' 
    }
  ]);
  
  // Loading state for waiting on API
  const [isLoading, setIsLoading] = useState(false);
  
  // Reference for auto-scrolling
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // Handle sending a new message
  const handleSendMessage = async (text) => {
    if (!text.trim()) return;
    
    // Add user message to the chat
    const newUserMessage = {
      id: Date.now(),
      text,
      sender: 'user'
    };
    
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);
    
    try {
      // Call the API
      const response = await fetch('http://127.0.0.1:5000/api/chat', { // to be edited
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          user_id: 'demo-user-123' 
        }),
      });
      
      const data = await response.json();
      console.log(data);
      
      if (data.status === 'success') {
        // Parse the response to determine if it contains special content
        let specialType = null;
        
        // Simple detection of special content based on keywords in the response
        // In a real app, the backend would provide structured data
        if (data.response.includes('tips') || data.response.includes('Tips')) {
          specialType = 'tips';
        } else if (data.response.includes('days') && (data.response.includes('sober') || data.response.includes('goal'))) {
          specialType = 'celebration';
        }
        
        // Add bot response to the chat
        const botResponse = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'bot',
          specialType
        };
        
        setMessages(prev => [...prev, botResponse]);
      } else {
        // Handle error response
        const errorResponse = {
          id: Date.now() + 1,
          text: "Sorry, I'm having trouble connecting right now. Please try again later.",
          sender: 'bot'
        };
        
        setMessages(prev => [...prev, errorResponse]);
      }
    } catch (error) {
      console.error('Error calling chat API:', error);
      
      // Add error message to chat
      const errorResponse = {
        id: Date.now() + 1,
        text: "Sorry, I'm having trouble connecting right now. Please try again later.",
        sender: 'bot'
      };
      
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="chat-container">
      <div className="messages-area">
        {messages.map(message => (
          <Message 
            key={message.id}
            text={message.text}
            sender={message.sender}
            specialType={message.specialType}
          />
        ))}
        
        {isLoading && (
          <div className="message bot">
            <div className="message-bubble typing">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <InputBar onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
}

export default ChatContainer;