import React, { useState, useEffect } from "react";
import ChatbotLayout from "../../components/chatbot/ChatbotLayout";
import Chat from "../../components/chatbot/chat";
import { chatAPI } from "../../api/chatApi";

const PlanMyTrip = () => {
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
        text: "Selamat pagi! Let's build your Bali plan. First crucial question: How many full days will you be exploring? 🌴✨",
        sender: "bot",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    if (loading) {
        return (
            <ChatbotLayout currentTool="Plan My Trip!">
                <div className="flex items-center justify-center h-full">
                    <div className="text-center">Loading...</div>
                </div>
            </ChatbotLayout>
        );
    }

    return (
        <ChatbotLayout currentTool="Plan My Trip!">
            <Chat
                chatType="plan-my-trip"
                toolName="Plan My Trip!"
                userId={userId}
                initialBotMessage={initialMessage}
            />
        </ChatbotLayout>
    );
};

export default PlanMyTrip;
