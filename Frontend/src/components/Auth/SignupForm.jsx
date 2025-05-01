// src/components/Auth/SignupForm.jsx
import React, { useState } from 'react';

function SignupForm({ onSignupSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      // For hackathon purposes, mock the API call
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Mock successful signup
      const userData = {
        id: new Date().getTime().toString(),
        email,
        name: email.split('@')[0],
        hasCompletedOnboarding: false,
        soberDays: 0
      };
      
      onSignupSuccess(userData);
    } catch (err) {
      setError('Something went wrong. Please try again.');
        console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <div className="auth-logo">Sign up</div>
      
      
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
      
      <div className="form-group">
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm Password"
          required
          className="auth-input"
        />
      </div>
      
      <button 
        type="submit" 
        className="auth-button"
        disabled={isLoading}
      >
        {isLoading ? 'Creating account...' : 'Sign Up'}
      </button>
      
      <div className="terms-privacy">
        <p>
          By signing up, you agree to our <a href="#">Terms</a> and <a href="#">Privacy Policy</a>
        </p>
      </div>
    </form>
  );
}

export default SignupForm;