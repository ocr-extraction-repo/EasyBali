import React, { useState, useEffect } from "react";
import ChatbotLayout from "../../components/chatbot/ChatbotLayout";
import Chat from "../../components/chatbot/chat";
import { chatAPI } from "../../api/chatApi";

const WhatToDoToday = () => {
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
        text: "Selamat pagi! ☀️ How's the Bali wonderlust going? Got your bags packed or just dreaming for now? ✈️✨ Let's stir up some island magic!",
        sender: "bot",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    if (loading) {
        return (
            <ChatbotLayout currentTool="What To Do Today?">
                <div className="flex items-center justify-center h-full">
                    <div className="text-center">Loading...</div>
                </div>
            </ChatbotLayout>
        );
    }

    return (
        <ChatbotLayout currentTool="What To Do Today?">
            <Chat
                chatType="what-to-do"
                toolName="What To Do Today?"
                userId={userId}
                initialBotMessage={initialMessage}
            />
        </ChatbotLayout>
    );
};

export default WhatToDoToday;
