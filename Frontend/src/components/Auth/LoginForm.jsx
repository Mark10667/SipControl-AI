// src/components/Auth/LoginForm.jsx
import React, { useState } from 'react';

function LoginForm({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      // For hackathon purposes, mock the API call
      // In production, you would call your backend API
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Mock successful login
      const userData = {
        id: '1',
        email,
        name: email.split('@')[0],
        hasCompletedOnboarding: false,
        soberDays: 0
      };
      
      onLoginSuccess(userData);
    } catch (err) {
      setError('Invalid email or password. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <div className="auth-logo">Login</div>
      
      
      {error && <div className="auth-error">{error}</div>}
      
      <div className="form-group">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
          className="auth-input"
        />
      </div>
      
      <div className="form-group">
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          className="auth-input"
        />
      </div>
      
      <button 
        type="submit" 
        className="auth-button"
        disabled={isLoading}
      >
        {isLoading ? 'Signing in...' : 'Login'}
      </button>
      
      <div className="auth-alternative">
        <p>Forgot your password?</p>
      </div>
    </form>
  );
}

export default LoginForm;