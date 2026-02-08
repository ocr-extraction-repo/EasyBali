// src/services/chatApi.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_BASE_URL || 'https://easy-bali.onrender.com';

export const chatAPI = {
  // Send message to specific chat endpoint
  sendMessage: async (chatType, userId, query) => {
    const endpoints = {
      'what-to-do': 'what-to-do/chat',
      'currency-converter': 'currency-converter/chat',
      'plan-my-trip': 'plan-my-trip/chat',
      'general': 'chatbot/generate-response',
      'things-to-do-in-bali': "things-to-do-in-bali/chat"
    };

    const endpoint = endpoints[chatType] || endpoints.general;

    try {
      const response = await axios.post(
        `${API_BASE_URL}/${endpoint}`,
        { query },
        { params: { user_id: userId } }
      );
      return response.data;
    } catch (error) {
      console.error(`Error in ${chatType} chat:`, error);
      throw error;
    }
  },

  // Get or create user ID
  getUserId: () => {
    let userId = localStorage.getItem('userId');
    if (!userId) {
      userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('userId', userId);
    }
    return userId;
  },

  // Save chat history
  saveChatHistory: (userId, chatType, messages) => {
    const key = `chat_history_${chatType}_${userId}`;
    localStorage.setItem(key, JSON.stringify(messages));
  },

  // Load chat history
  loadChatHistory: (userId, chatType) => {
    const key = `chat_history_${chatType}_${userId}`;
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : [];
  }
};