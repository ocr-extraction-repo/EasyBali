import React, { useState, useEffect } from "react";
import ChatbotLayout from "../../components/chatbot/ChatbotLayout";
import Chat from "../../components/chatbot/chat";
import { chatAPI } from "../../api/chatApi";

const VoiceTranslator = () => {
    const [initialMessage, setInitialMessage] = useState(null);
    const [userId, setUserId] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const initializeChat = async () => {
            try {
                const currentUserId = chatAPI.getUserId();
                setUserId(currentUserId);

                // Send "Hi" to get bot's greeting
                const response = await chatAPI.sendMessage('voice-translator', currentUserId, "Hi");

                const botMessage = {
                    id: Date.now(),
                    text: response.response,
                    sender: "bot",
                    timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
                };

                setInitialMessage(botMessage);
                setLoading(false);
            } catch (error) {
                console.error('Error initializing Voice Translator:', error);
                setLoading(false);
            }
        };

        initializeChat();
    }, []);

    if (loading) {
        return (
            <ChatbotLayout currentTool="Voice Translator">
                <div className="flex items-center justify-center h-full">
                    <div className="text-center">Loading...</div>
                </div>
            </ChatbotLayout>
        );
    }

    return (
        <ChatbotLayout currentTool="Voice Translator">
            <Chat
                chatType="voice-translator"
                toolName="Voice Translator"
                userId={userId}
                initialBotMessage={initialMessage}
            />
        </ChatbotLayout>
    );
};

export default VoiceTranslator;
