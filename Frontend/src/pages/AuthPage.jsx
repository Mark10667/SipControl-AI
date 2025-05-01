// src/pages/AuthPage.jsx
import { useState, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import LoginForm from '../components/Auth/LoginForm';
import SignupForm from '../components/Auth/SignupForm';

import '../styles/AuthPage.css'

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const { login } = useContext(UserContext);

  const handleLoginSuccess = (userData) => {
    login(userData);
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <h1>SipControl</h1>
        
        {isLogin ? (
          <>
            <LoginForm onLoginSuccess={handleLoginSuccess} />
            <p>
              Don't have an account?{' '}
              <button onClick={() => setIsLogin(false)}>Sign Up</button>
            </p>
          </>
        ) : (
          <>
            <SignupForm onSignupSuccess={handleLoginSuccess} />
            <p>
              Already have an account?{' '}
              <button onClick={() => setIsLogin(true)}>Login</button>
            </p>
          </>
        )}
      </div>
    </div>
  );
}

export default AuthPage;