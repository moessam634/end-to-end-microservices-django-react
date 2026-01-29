import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';

// Configure axios base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
axios.defaults.baseURL = API_BASE_URL;

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  const logout = useCallback(() => {
    // Clear tokens
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    
    // Clear axios default header
    delete axios.defaults.headers.common['Authorization'];
    
    // Update state
    setToken(null);
    setUser(null);
  }, []);

  const fetchUser = useCallback(async () => {
    try {
      const response = await axios.get('/profile/');
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user:', error);
      logout();
    } finally {
      setLoading(false);
    }
  }, [logout]);

  // Configure axios defaults
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [token, fetchUser]);

  const login = async (email, password) => {
    try {
      const response = await axios.post('/auth/login/', {
        email,
        password,
      });
      
      const { access, refresh, user: userData } = response.data;
      
      // Store tokens
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      
      // Set axios default header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      // Update state
      setToken(access);
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      
      // Handle validation errors from Django
      if (error.response?.data) {
        const data = error.response.data;
        
        // If it's a field validation error, format it nicely
        if (typeof data === 'object' && !data.error) {
          const errors = [];
          for (const [field, messages] of Object.entries(data)) {
            if (Array.isArray(messages)) {
              errors.push(`${field}: ${messages.join(', ')}`);
            } else {
              errors.push(`${field}: ${messages}`);
            }
          }
          return {
            success: false,
            error: errors.join('; '),
          };
        }
        
        // If it's a simple error message
        return {
          success: false,
          error: data.error || 'Login failed',
        };
      }
      
      return {
        success: false,
        error: 'Login failed',
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await axios.post('/auth/register/', userData);
      
      const { access, refresh, user: newUser } = response.data;
      
      // Store tokens
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      
      // Set axios default header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      // Update state
      setToken(access);
      setUser(newUser);
      
      return { success: true };
    } catch (error) {
      console.error('Registration error:', error);
      
      // Handle validation errors from Django
      if (error.response?.data) {
        const data = error.response.data;
        
        // If it's a field validation error, format it nicely
        if (typeof data === 'object' && !data.error) {
          const errors = [];
          for (const [field, messages] of Object.entries(data)) {
            if (Array.isArray(messages)) {
              errors.push(`${field}: ${messages.join(', ')}`);
            } else {
              errors.push(`${field}: ${messages}`);
            }
          }
          return {
            success: false,
            error: errors.join('; '),
          };
        }
        
        // If it's a simple error message
        return {
          success: false,
          error: data.error || 'Registration failed',
        };
      }
      
      return {
        success: false,
        error: 'Registration failed',
      };
    }
  };

  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('refreshToken');
      if (!refresh) {
        throw new Error('No refresh token');
      }

      const response = await axios.post('/auth/refresh/', {
        refresh,
      });
      
      const { access } = response.data;
      
      // Update tokens
      localStorage.setItem('token', access);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      setToken(access);
      
      return true;
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
      return false;
    }
  };

  const updateUser = (userData) => {
    setUser(userData);
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    refreshToken,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
