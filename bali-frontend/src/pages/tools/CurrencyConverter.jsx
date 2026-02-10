import React, { useState, useEffect } from "react";
import ChatbotLayout from "../../components/chatbot/ChatbotLayout";
import Chat from "../../components/chatbot/chat";
import { chatAPI } from "../../api/chatApi";

const CurrencyConverter = () => {
    const [userId, setUserId] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const currentUserId = chatAPI.getUserId();
        setUserId(currentUserId);
        setLoading(false);
    }, []);

    // Hardcoded initial message matching production exactly
    const initialMessage = {
        id: Date.now(),
        text: "Hello! 🌟 How can I assist you with currency conversion for your Bali trip today? 🌺 ✨ If you provide your currency and amount, I can help convert it to Indonesian Rupiah (IDR) for you.",
        sender: "bot",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    if (loading) {
        return (
            <ChatbotLayout currentTool="Currency Converter">
                <div className="flex items-center justify-center h-full">
                    <div className="text-center">Loading...</div>
                </div>
            </ChatbotLayout>
        );
    }

    return (
        <ChatbotLayout currentTool="Currency Converter">
            <Chat
                chatType="currency-converter"
                toolName="Currency Converter"
                userId={userId}
                initialBotMessage={initialMessage}
            />
        </ChatbotLayout>
    );
};

export default CurrencyConverter;
