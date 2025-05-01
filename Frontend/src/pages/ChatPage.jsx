// src/pages/ChatPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TipsList from '../components/Chat/TipsList';
import '../styles/ChatPage.css';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'agent',
      content: "Hi there! 👋 How's your day going? Just checking in — no pressure at all.",
      timestamp: new Date().toISOString()
    }
  ]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [showTyping, setShowTyping] = useState(false);
  const [showTips, setShowTips] = useState(false);

  const handleSendMessage = () => {
    if (!currentMessage.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      sender: 'user',
      content: currentMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setShowTyping(true);

    // Check if the message contains keywords that should trigger tips
    const triggerWords = ['party', 'social', 'drink', 'bar', 'club', 'friends'];
    const shouldShowTips = triggerWords.some(word => 
      currentMessage.toLowerCase().includes(word)
    );

    if (shouldShowTips) {
      setShowTips(true);
    }

    // Simulate agent response after a delay
    setTimeout(() => {
      let agentResponse;
      switch (messages.length) {
        case 1:
          agentResponse = {
            id: messages.length + 2,
            sender: 'agent',
            content: "Thanks for sharing — I hear you, long days can really take a toll.\nQuick question: did you happen to have anything to drink today?",
            timestamp: new Date().toISOString()
          };
          break;
        case 3:
          agentResponse = {
            id: messages.length + 2,
            sender: 'agent',
            content: "Thanks for being honest, and no worries at all — I'm here for you, not to judge.\nRemember, we set the goal together to stick with 2 glasses of red wine a day for 7 days straight? You were doing great — today was just a small bump. You almost had a perfect streak! I truly believe you can bounce back tomorrow. 🙌",
            timestamp: new Date().toISOString()
          };
          break;
        case 4:
          agentResponse = {
            id: messages.length + 2,
            sender: 'agent',
            content: "Just checking in — how are you feeling right now? Do you think today's drinking might be connected to how your day went?",
            timestamp: new Date().toISOString()
          };
          break;
        case 6:
          agentResponse = {
            id: messages.length + 2,
            sender: 'agent',
            content: "Totally understandable. Stressful workdays can feel overwhelming, and you've been doing a lot lately. I'm here to help lighten that load however I can.\n\nLet's try something simple but powerful: a journaling exercise designed to ease pressure and reconnect with what brings you joy. ✍️\n\nHere's the prompt:\n\nThink about the things that bring a smile to your face. Write down ten things that make you smile. Feel free to elaborate on them and describe specific instances of happiness.\n\nTake your time — there's no right or wrong way to do it. I'll be right here if you want to share or reflect afterward.",
            timestamp: new Date().toISOString()
          };
          break;
        case 8:
          agentResponse = {
            id: messages.length + 2,
            sender: 'agent',
            content: "Perfect — I'm proud of you for taking this step. You've got this. 💪\nI'll check in again tomorrow — but remember, you can always reach out anytime. Sleep well tonight. 💤",
            timestamp: new Date().toISOString()
          };
          break;
        default:
          agentResponse = {
            id: messages.length + 2,
            sender: 'agent',
            content: "I understand. How can I support you today?",
            timestamp: new Date().toISOString()
          };
      }

      setMessages(prev => [...prev, agentResponse]);
      setShowTyping(false);
    }, 1500);
  };

  const handleCloseTips = () => {
    setShowTips(false);
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        <div className="messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender === 'user' ? 'user' : 'agent'}`}
            >
              <div className="message-content">
                {message.content.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
              <div className="message-time">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))}
          {showTyping && (
            <div className="message agent">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </div>
        
        {showTips && (
          <div className="tips-overlay">
            <button className="close-tips" onClick={handleCloseTips}>×</button>
            <TipsList />
          </div>
        )}

        <div className="input-area">
          <input
            type="text"
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type your message..."
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;