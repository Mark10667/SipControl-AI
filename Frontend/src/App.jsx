// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import { UserContext } from './context/UserContext';
import { UserProvider } from './context/UserProvider';
import AuthPage from './pages/AuthPage';
import OnboardingPage from './pages/OnboardingPage';
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';


import './App.css';

// Protected route component
function ProtectedRoute({ children, requiresOnboarding = true }) {
  const { user, loading } = useContext(UserContext);
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  if (!user) {
    return <Navigate to="/auth" />;
  }
  
  if (requiresOnboarding && !user.hasCompletedOnboarding) {
    return <Navigate to="/onboarding" />;
  }
  
  return children;
}

function AppRoutes() {
  const { user } = useContext(UserContext);
  
  return (
    <Routes>
      {/* Auth route - redirect if logged in */}
      <Route 
        path="/auth" 
        element={user ? <Navigate to="/home" /> : <AuthPage />} 
      />
      
      {/* Onboarding route - requires auth but no onboarding */}
      <Route 
        path="/onboarding" 
        element={
          <ProtectedRoute requiresOnboarding={false}>
            {user?.hasCompletedOnboarding ? <Navigate to="/home" /> : <OnboardingPage />}
          </ProtectedRoute>
        } 
      />
      
      {/* Home route - requires auth and onboarding */}
      <Route 
        path="/home" 
        element={
          <ProtectedRoute>
            <HomePage />
          </ProtectedRoute>
        } 
      />
      
      {/* Chat routes - requires auth and onboarding */}
      <Route 
        path="/chat" 
        element={
          <ProtectedRoute>
            <ChatPage />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/chat/:mode" 
        element={
          <ProtectedRoute>
            <ChatPage />
          </ProtectedRoute>
        } 
      />
      
      {/* Default redirect */}
      <Route path="/" element={<Navigate to={user ? "/home" : "/auth"} />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

function App() {
  return (
    <div className="App">
        <UserProvider>
            <BrowserRouter>
                <AppRoutes />
            </BrowserRouter>
        </UserProvider>    
    </div>
    
  );
}

export default App;


