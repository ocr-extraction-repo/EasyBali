import React from "react";
import { useLocation } from "react-router-dom";
import ChatbotLayout from "../../components/chatbot/ChatbotLayout";
import Chat from "../../components/chatbot/chat";
import { chatAPI } from "../../api/chatApi";

const GeneralChat = () => {
    const location = useLocation();

    // Check if we came from hero input with location.state
    const hasLocationState = location.state?.chatType && location.state?.userId;

    // If user came from hero/homepage with location.state, render Chat WITHOUT props
    // so it uses its legacy location.state handling (which supports initialMessage)
    if (hasLocationState) {
        return (
            <ChatbotLayout>
                <Chat />
            </ChatbotLayout>
        );
    }

    // Default: show general chat with bot greeting and proper initialization
    const userId = chatAPI.getUserId();
    const initialMessage = {
        id: Date.now(),
        text: "Hello! How can I assist you with your Bali trip today? 🌺",
        sender: "bot",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    return (
        <ChatbotLayout>
            <Chat
                chatType="general"
                userId={userId}
                initialBotMessage={initialMessage}
            />
        </ChatbotLayout>
    );
};

export default GeneralChat;
