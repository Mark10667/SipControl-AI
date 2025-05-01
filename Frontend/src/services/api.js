// API service for backend communication
const API_BASE_URL = '/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
  try {
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Something went wrong');
    }
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Chat API
export const chat = async (message, userId = 'demo-user-123') => {
  try {
    console.log('Sending chat request:', { message, userId });
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        message,
        user_id: userId 
      }),
    });
    const data = await handleResponse(response);
    console.log('Chat response:', data);
    return data;
  } catch (error) {
    console.error('Chat error:', error);
    throw error;
  }
};

// User API
export const createUser = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/user`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });
  return handleResponse(response);
};

// Daily Log API
export const createDailyLog = async (logData) => {
  const response = await fetch(`${API_BASE_URL}/daily-log`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(logData),
  });
  return handleResponse(response);
};

// Relapse Support API
export const createRelapseSupport = async (supportData) => {
  const response = await fetch(`${API_BASE_URL}/relapse-support`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(supportData),
  });
  return handleResponse(response);
};

// Motivations API
export const getMotivations = async () => {
  const response = await fetch(`${API_BASE_URL}/motivations`);
  return handleResponse(response);
};

// Notifications API
export const getNotifications = async () => {
  const response = await fetch(`${API_BASE_URL}/notifications`);
  return handleResponse(response);
};

// History API
export const getHistory = async () => {
  const response = await fetch(`${API_BASE_URL}/history`);
  return handleResponse(response);
};

// File Upload API
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });
  return handleResponse(response);
}; 