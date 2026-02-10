import React, { useState, useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import bottomRightPng from "../../assets/images/right-bottom.png";
import topLeftPng from "../../assets/images/top-left.png";
import { getSubMenu } from '../services/api';
import { chatAPI } from "../../api/chatApi"

const Chat = ({ chatType: propChatType, toolName: propToolName, userId: propUserId, initialBotMessage: propInitialBotMessage }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("Order Services");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const socketRef = useRef(null);
  const messagesEndRef = useRef(null);
  const [chatType, setChatType] = useState(null);
  const [userId, setUserId] = useState(null);
  const [apiLoading, setApiLoading] = useState(false);

  // ✅ NEW: Refs to prevent re-renders and duplicate connections
  const initialMessageProcessed = useRef(false);
  const hasInitialized = useRef(false);
  const isCleaningUp = useRef(false);

  // ✅ NEW: Timeout ref for 120 second auto-close
  const autoCloseTimeoutRef = useRef(null);

  const getCurrentTime = () => {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  // ✅ NEW: Helper functions for WebSocket message persistence
  const saveWebSocketMessages = (sessionId, messages) => {
    try {
      localStorage.setItem(`websocket_chat_${sessionId}`, JSON.stringify(messages));
      console.log("💾 Saved WebSocket messages to localStorage");
    } catch (error) {
      console.error("❌ Error saving WebSocket messages:", error);
    }
  };

  const loadWebSocketMessages = (sessionId) => {
    try {
      const savedMessages = localStorage.getItem(`websocket_chat_${sessionId}`);
      if (savedMessages) {
        const parsedMessages = JSON.parse(savedMessages);
        console.log("📂 Loaded WebSocket messages from localStorage:", parsedMessages.length);
        return parsedMessages;
      }
    } catch (error) {
      console.error("❌ Error loading WebSocket messages:", error);
    }
    return [];
  };

  const clearWebSocketMessages = (sessionId) => {
    try {
      localStorage.removeItem(`websocket_chat_${sessionId}`);
      console.log("🧹 Cleared WebSocket messages from localStorage");
    } catch (error) {
      console.error("❌ Error clearing WebSocket messages:", error);
    }
  };

  // ✅ NEW: Function to close WebSocket gracefully
  const closeWebSocketConnection = (reason = "Manual close") => {
    console.log(`🔌 Closing WebSocket connection: ${reason}`);

    // Clear auto-close timeout
    if (autoCloseTimeoutRef.current) {
      clearTimeout(autoCloseTimeoutRef.current);
      autoCloseTimeoutRef.current = null;
    }

    // Close the socket
    if (socketRef.current) {
      const state = socketRef.current.readyState;
      if (state === WebSocket.OPEN || state === WebSocket.CONNECTING) {
        socketRef.current.close(1000, reason);
      }
      socketRef.current = null;
    }
    setIsConnected(false);
  };

  // ✅ NEW: Start 120-second auto-close timer
  const startAutoCloseTimer = () => {
    // Clear any existing timeout
    if (autoCloseTimeoutRef.current) {
      clearTimeout(autoCloseTimeoutRef.current);
    }

    // Set new 120-second timeout
    autoCloseTimeoutRef.current = setTimeout(() => {
      console.log("⏰ 120 seconds elapsed - auto-closing WebSocket connection");
      closeWebSocketConnection("Auto-close after 120 seconds");
    }, 120000); // 120 seconds = 120000 milliseconds

    console.log("⏱️ Started 120-second auto-close timer");
  };

  const handleOrderServicesClick = async () => {
    try {
      setLoading(true);
      const response = await getSubMenu('Order Services');
      navigate('/categories', {
        state: {
          mainMenu: 'categories',
          data: response.data || []
        }
      });
    } catch (error) {
      console.error('Failed to fetch Order Services:', error);
      navigate('/services', {
        state: {
          mainMenu: 'services',
          data: [],
          error: 'Failed to load services. Please try again.'
        }
      });
    } finally {
      setLoading(false);
    }
  };

  // ✅ FIXED: Initialize only once on mount
  useEffect(() => {
    // Prevent multiple initializations
    if (hasInitialized.current) return;
    hasInitialized.current = true;

    console.log("=== CHATBOT COMPONENT - RECEIVED VALUES ===");
    console.log("Props ChatType:", propChatType);
    console.log("Props ToolName:", propToolName);
    console.log("Location state:", location.state);
    console.log("Location key:", location.key);

    initialMessageProcessed.current = false;

    // ✅ NEW: Prioritize props over location.state
    if (propChatType) {
      // Route-based initialization (new architecture)
      const userId = propUserId || chatAPI.getUserId();

      console.log(`Initializing ${propChatType} chat for user ${userId}`);
      setChatType(propChatType);
      setUserId(userId);
      setActiveTab(propToolName || "Chat");

      // Use initialBotMessage from props if provided
      if (propInitialBotMessage) {
        setMessages([propInitialBotMessage]);
        console.log("🆕 Starting with bot message from props");
        initialMessageProcessed.current = true;
      } else {
        // Load existing chat history
        const storedMessages = chatAPI.loadChatHistory(userId, propChatType);
        if (storedMessages && storedMessages.length > 0) {
          setMessages(storedMessages);
          console.log("📂 Loaded chat history:", storedMessages.length, "messages");
          initialMessageProcessed.current = true;
        } else {
          setMessages([]);
          console.log("🆕 Starting empty chat");
        }
      }
    }
    // Legacy: location.state based initialization (backward compatibility)
    else if (location.state?.chatType && location.state?.userId) {
      const currentChatType = location.state.chatType;
      const currentUserId = location.state.userId;

      console.log(`Initializing ${currentChatType} chat for user ${currentUserId}`);
      setChatType(currentChatType);
      setUserId(currentUserId);
      setActiveTab(location.state?.activeTab || "Chat");

      if (location.state?.initialBotMessage) {
        const botMsg = location.state.initialBotMessage;
        console.log("🤖 Starting with bot message:", botMsg.text);
        setMessages([botMsg]);
        initialMessageProcessed.current = true;
      }
      else if (location.state?.initialMessage) {
        const initialMsg = location.state.initialMessage;
        console.log("📩 New message from Hero:", initialMsg.text);
        setMessages([initialMsg]);
        initialMessageProcessed.current = false;
      }
      else {
        const storedMessages = chatAPI.loadChatHistory(currentUserId, currentChatType);

        if (storedMessages && storedMessages.length > 0) {
          setMessages(storedMessages);
          console.log("📂 Loaded chat history:", storedMessages.length, "messages");
          initialMessageProcessed.current = true;
        } else {
          setMessages([]);
          console.log("🆕 Starting empty chat");
        }
      }
    }
    // ✅ UPDATED: WebSocket-based order chat with persistence
    else if (location.state?.message && location.state?.sessionId) {
      console.log("📦 WebSocket order chat initialization");
      setChatType('order-service');

      const sessionId = location.state.sessionId;

      // ✅ Load existing WebSocket messages from localStorage
      const savedMessages = loadWebSocketMessages(sessionId);

      if (savedMessages.length > 0) {
        console.log("📂 Restored previous WebSocket chat:", savedMessages.length, "messages");
        setMessages(savedMessages);
      } else {
        const initialMessage = {
          id: Date.now(),
          text: location.state.message,
          sender: "bot",
          timestamp: getCurrentTime(),
        };
        setMessages([initialMessage]);
      }
    } else {
      console.log("No initial state provided");
    }
    console.log("===============================================");
  }, []); // ✅ Empty dependency array - only run once

  // ✅ Auto-send initial message for API-based chats
  useEffect(() => {
    const apiBasedChats = ['what-to-do', 'currency-converter', 'plan-my-trip', 'things-to-do-in-bali', 'general'];

    if (
      chatType &&
      userId &&
      apiBasedChats.includes(chatType) &&
      messages.length === 1 &&
      messages[0].sender === 'user' &&
      !apiLoading &&
      !initialMessageProcessed.current
    ) {
      console.log('🚀 Auto-sending initial message to API:', messages[0].text);
      initialMessageProcessed.current = true;
      sendMessageToAPI(messages[0].text);
    }
  }, [chatType, userId, messages.length, apiLoading]);

  // ✅ Save messages to localStorage for API-based chats
  useEffect(() => {
    const apiBasedChats = ['what-to-do', 'currency-converter', 'plan-my-trip', 'things-to-do-in-bali', 'general'];
    if (apiBasedChats.includes(chatType) && userId && messages.length > 0) {
      chatAPI.saveChatHistory(userId, chatType, messages);
      console.log("💾 Saved messages to localStorage");
    }
  }, [messages, userId, chatType]);

  // ✅ NEW: Save WebSocket messages to localStorage whenever they change
  useEffect(() => {
    const sessionId = location.state?.sessionId;
    if (chatType === 'order-service' && sessionId && messages.length > 0) {
      saveWebSocketMessages(sessionId, messages);
    }
  }, [messages, chatType, location.state?.sessionId]);

  // ✅ FIXED: WebSocket connection logic
  useEffect(() => {
    const sessionId = location.state?.sessionId;
    const apiBasedChats = ['what-to-do', 'currency-converter', 'plan-my-trip', 'general'];

    // Wait for chatType to be set
    if (!chatType) {
      console.log("⏳ Waiting for chat type to be set...");
      return;
    }

    // Only connect WebSocket for order services
    if (sessionId && !apiBasedChats.includes(chatType)) {
      console.log("=== ESTABLISHING WEBSOCKET CONNECTION ===");
      console.log("Session ID:", sessionId);
      console.log("Chat Type:", chatType);

      let ws = null;
      isCleaningUp.current = false;

      const baseUrl = import.meta.env.VITE_BASE_URL;
      if (!baseUrl) {
        console.error("❌ VITE_BASE_URL is not defined in environment variables");
        return;
      }
      const wsUrl = baseUrl.replace(/^http/, 'ws') + `/ws/${sessionId}`;

      console.log("🔗 WebSocket URL:", wsUrl);

      const connectWebSocket = () => {
        if (isCleaningUp.current) {
          console.log("⚠️ Component is cleaning up, skipping connection");
          return;
        }

        try {
          console.log("🔌 Attempting WebSocket connection...");
          ws = new WebSocket(wsUrl);

          ws.onopen = () => {
            if (isCleaningUp.current) return;
            console.log("✅ WebSocket connected successfully");
            setIsConnected(true);

            // ✅ NEW: Start 120-second auto-close timer
            startAutoCloseTimer();
          };

          ws.onmessage = (event) => {
            if (isCleaningUp.current) return;
            console.log("📨 Received WebSocket message:", event.data);

            try {
              const data = JSON.parse(event.data);

              // ✅ NEW: Handle "destroy" type message
              if (data.type === "destroy") {
                console.log("🛑 Received destroy message - closing connection");
                closeWebSocketConnection("Destroy message received");

                // Optional: Clear saved messages when destroy is received
                clearWebSocketMessages(sessionId);
                return;
              }

              const newMessage = {
                id: Date.now(),
                text: data.message || data.text || JSON.stringify(data),
                sender: "bot",
                timestamp: getCurrentTime(),
                type: data.type || "text", // ✅ Store message type
              };
              setMessages((prev) => [...prev, newMessage]);

              // ✅ NEW: Reset the 120-second timer on each message
              startAutoCloseTimer();

            } catch (e) {
              console.error("Error parsing message:", e);
              const newMessage = {
                id: Date.now(),
                text: event.data,
                sender: "bot",
                timestamp: getCurrentTime(),
              };
              setMessages((prev) => [...prev, newMessage]);
            }
          };

          ws.onerror = (error) => {
            if (isCleaningUp.current) return;
            console.error("❌ WebSocket error:", error);
            console.error("WebSocket readyState:", ws?.readyState);
            setIsConnected(false);
          };

          ws.onclose = (event) => {
            if (isCleaningUp.current) return;
            console.log("❌ WebSocket closed:", {
              code: event.code,
              reason: event.reason,
              wasClean: event.wasClean
            });
            setIsConnected(false);

            // ✅ Clear the auto-close timeout when connection closes
            if (autoCloseTimeoutRef.current) {
              clearTimeout(autoCloseTimeoutRef.current);
              autoCloseTimeoutRef.current = null;
            }

            // Auto-reconnect for abnormal closures
            if (event.code !== 1000 && event.code !== 1001 && !isCleaningUp.current) {
              console.log("🔄 Attempting to reconnect in 3 seconds...");
              setTimeout(() => {
                if (!isCleaningUp.current && sessionId) {
                  connectWebSocket();
                }
              }, 3000);
            }
          };

          socketRef.current = ws;
          setSocket(ws);

        } catch (error) {
          console.error("❌ Failed to create WebSocket connection:", error);
          setIsConnected(false);
        }
      };

      connectWebSocket();

      // ✅ Cleanup function
      return () => {
        isCleaningUp.current = true;
        console.log("🧹 Cleaning up WebSocket connection");

        // Clear auto-close timeout
        if (autoCloseTimeoutRef.current) {
          clearTimeout(autoCloseTimeoutRef.current);
          autoCloseTimeoutRef.current = null;
        }

        if (socketRef.current) {
          const state = socketRef.current.readyState;
          if (state === WebSocket.OPEN || state === WebSocket.CONNECTING) {
            socketRef.current.close(1000, "Component unmounting");
          }
          socketRef.current = null;
        }
        setIsConnected(false);
      };
    } else {
      if (!sessionId) {
        console.log("ℹ️ No session ID found, skipping WebSocket");
      } else if (apiBasedChats.includes(chatType)) {
        console.log("ℹ️ API-based chat, skipping WebSocket");
      }
    }
  }, [chatType]); // ✅ Only depend on chatType

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // ✅ Function to send message to API
  const sendMessageToAPI = async (userMessage) => {
    try {
      setApiLoading(true);
      console.log(`📤 Sending message to ${chatType} endpoint for user ${userId}`);

      const response = await chatAPI.sendMessage(chatType, userId, userMessage);

      const botMessage = {
        id: Date.now(),
        text: response.response,
        sender: "bot",
        timestamp: getCurrentTime(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("❌ Error sending message:", error);

      const errorMessage = {
        id: Date.now(),
        text: error.response?.data?.detail || "Sorry, I couldn't process that. Please try again! 🙏",
        sender: "bot",
        timestamp: getCurrentTime(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setApiLoading(false);
    }
  };

  // ✅ FIXED: Handle send click for both WebSocket and API
  const handleSendClick = () => {
    if (!inputMessage.trim()) return;

    const newUserMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: "user",
      timestamp: getCurrentTime(),
    };

    setMessages((prev) => [...prev, newUserMessage]);

    const apiBasedChats = ['what-to-do', 'currency-converter', 'plan-my-trip', 'general'];

    if (apiBasedChats.includes(chatType) && userId) {
      // API-based chat
      console.log("📤 Sending via API");
      sendMessageToAPI(inputMessage);
    } else if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      // WebSocket-based chat (Order Services)
      try {
        const payload = JSON.stringify({
          message: inputMessage,
          timestamp: getCurrentTime(),
          type: "user_message"
        });
        socketRef.current.send(payload);
        console.log("✅ Sent message via WebSocket:", inputMessage);

        // ✅ NEW: Reset the 120-second timer when user sends a message
        startAutoCloseTimer();

      } catch (error) {
        console.error("❌ Error sending WebSocket message:", error);
        const errorMessage = {
          id: Date.now(),
          text: "Failed to send message. Please check your connection.",
          sender: "bot",
          timestamp: getCurrentTime(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    } else {
      console.warn("⚠️ No active connection available");
      const warningMessage = {
        id: Date.now(),
        text: "Connection not established. Please wait or refresh the page.",
        sender: "bot",
        timestamp: getCurrentTime(),
      };
      setMessages((prev) => [...prev, warningMessage]);
    }

    setInputMessage("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSendClick();
    }
  };

  const renderBotMessage = (text) => {
    if (!text || typeof text !== "string") {
      return <span>Sorry, no message content available.</span>;
    }

    // Convert escaped newlines to real line breaks
    text = text.replace(/\\n/g, "\n");

    // Split message parts by markdown tokens
    const regex =
      /(\*\*\*[^\*]+\*\*\*|\*\*[^\*]+\*\*|\^\^[^\^]+\^\^|\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)|\n)/gi;

    const parts = text.split(regex).filter(Boolean);

    return parts.map((part, index) => {
      if (part === "\n") return <br key={index} />;

      // Bold + large
      if (part.startsWith("***") && part.endsWith("***")) {
        return (
          <span key={index} className="font-bold text-lg">
            {part.slice(3, -3)}
          </span>
        );
      }

      // Bold
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <span key={index} className="font-bold">
            {part.slice(2, -2)}
          </span>
        );
      }

      // Large
      if (part.startsWith("^^") && part.endsWith("^^")) {
        return (
          <span key={index} className="text-lg">
            {part.slice(2, -2)}
          </span>
        );
      }

      // ✅ Handle Markdown-style links
      const linkMatch = part.match(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/i);
      if (linkMatch) {
        const url = linkMatch[2];
        const isPaymentLink = /(xendit|stripe|paypal|checkout|paystack)/i.test(url);
        const isInvoiceLink = /(invoice|receipt|pdf|\.pdf)/i.test(url);

        if (isPaymentLink) {
          return (
            <a
              key={index}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-2 bg-white text-orange-600 font-semibold px-4 py-2 rounded-2xl shadow-md border border-white hover:bg-orange-600 hover:text-white transition"
            >
              💳 Pay Now
            </a>
          );
        }
        if (isInvoiceLink) {
          return (
            <a
              key={index}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-2 bg-white text-orange-600 font-semibold px-4 py-2 rounded-2xl shadow-md border border-white hover:bg-orange-600 hover:text-white transition"
            >
              📄 Download Invoice
            </a>
          );
        }

        // For normal links
        return (
          <a
            key={index}
            href={url}
            className="underline text-blue-200"
            target="_blank"
            rel="noopener noreferrer"
          >
            {linkMatch[1]}
          </a>
        );
      }

      // ❌ Skip plain leftover "link" text from Markdown
      if (part.trim() === "link" || part.match(/https?:\/\/[^\s]+/)) {
        return null;
      }

      return <span key={index}>{part}</span>;
    });
  };





  const menuItems = [
    { name: "Order Services", icon: "/chat-icons/order.svg" },
    { name: "Local Guide", icon: "/chat-icons/guide.svg" },
    { name: "Voice Translator", icon: "/chat-icons/translator.svg" },
    { name: "Currency Converter", icon: "/chat-icons/currency.svg" },
    { name: "What To Do Today?", icon: "/chat-icons/today.svg" },
    { name: "Plan My Trip!", icon: "/chat-icons/trip.svg" },
    { name: "Recommendations", icon: "/chat-icons/recommend.svg" },
    { name: "Discount & Promotions", icon: "/chat-icons/discount.svg" },
    { name: "Passport Submission", icon: "/chat-icons/passport.svg" },
  ];

  return (
    <>
      <div className="flex flex-col h-[calc(100vh-245px)] overflow-hidden gap-10">
        <div className="messages-container flex-1 overflow-y-auto px-5 z-10">
          <div className="flex flex-col gap-5">
            {messages.map((message) => (
              message.sender === "bot" ? (
                <div key={message.id} className="flex items-end gap-2">
                  <div className="w-10 h-10 rounded-full bg-[#FF8000] flex items-center justify-center flex-shrink-0">
                    <img
                      src="/assets/ai-chat-icon.png"
                      alt=""
                      className="w-10 h-10"
                    />
                  </div>
                  <div className="flex flex-col bg-[#FF8000] px-7 py-4 rounded-[25px] rounded-bl-none break-words max-w-[85%]">
                    <p className="text-white font-medium leading-relaxed" style={{ whiteSpace: 'pre-line' }}>
                      {renderBotMessage(message.text)}
                    </p>
                    <p className="text-white text-end font-bold text-sm mt-0">
                      {message.timestamp}
                    </p>
                  </div>
                </div>
              ) : (
                <div
                  key={message.id}
                  className="flex items-end gap-2 justify-end z-11"
                >
                  <div className="flex flex-col bg-white px-8 py-4 rounded-[25px] rounded-br-none shadow-md break-words max-w-[85%]">
                    <p className="text-black font-medium">{message.text}</p>
                    <p className="text-gray-500 text-end font-bold text-sm mt-2">
                      {message.timestamp}
                    </p>
                  </div>
                </div>
              )
            ))}
            {apiLoading && (
              <div className="flex items-end gap-2">
                <div className="w-10 h-10 rounded-full bg-[#FF8000] flex items-center justify-center flex-shrink-0">
                  <img
                    src="/assets/ai-chat-icon.png"
                    alt=""
                    className="w-10 h-10"
                  />
                </div>
                <div className="flex flex-col bg-[#FF8000] px-7 py-4 rounded-[25px] rounded-bl-none">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>
      <div className="px-[10px]">
        <div className="rounded-full bg-white shadow-lg flex px-[40px] py-[20px] items-center justify-between h-[85px] mb-[20px] border-class">
          <input
            type="text"
            placeholder="Chat with our AI Bot"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={apiLoading}
            className="w-[90%] py-4 sm:py-6 rounded-[50px] text-[#333] text-[16px] sm:text-[18px] placeholder:text-[#8e8e8e] disabled:opacity-50"
          />
          <div className="flex items-center gap-4">
            <img src="/assets/mic.svg" alt="" className="cursor-pointer" />
            <img
              src="/assets/chat-btn.svg"
              alt=""
              onClick={handleSendClick}
              className={`w-[35px] h-[35px] sm:w-[50px] sm:h-[50px] ${apiLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
                }`}
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default Chat;