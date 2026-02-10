import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import bottomRightPng from "../../assets/images/right-bottom.png";
import topLeftPng from "../../assets/images/top-left.png";
import { getSubMenu } from '../services/api';

const ChatbotLayout = ({ children, currentTool }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [loading, setLoading] = useState(false);

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

    // Helper function to convert menu item names to route slugs
    const getToolRoute = (itemName) => {
        const routeMap = {
            "Plan My Trip!": "/tools/plan-my-trip",
            "Currency Converter": "/tools/currency-converter",
            "Voice Translator": "/tools/voice-translator",
            "What To Do Today?": "/tools/what-to-do-today",
            "Local Guide": "/tools/local-guide",
            "Recommendations": "/tools/recommendations",
            "Discount & Promotions": "/tools/discount-promotions",
            "Passport Submission": "/tools/passport-submission"
        };
        return routeMap[itemName] || "/tools";
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
        <div className="chat relative flex gap-5 p-2 md:p-2 min-h-screen">
            <img
                src={topLeftPng}
                alt="Top Left Icon"
                className="absolute top-[10px] left-[0px] sm:left-[150px] md:left-[270px] w-[350px] sm:w-[200px] md:w-[450px] opacity-60 z-0"
            />
            <img
                src={bottomRightPng}
                alt="Bottom Right Icon"
                className="absolute bottom-0 right-0 w-[390px] sm:w-[250px] md:w-[450px] opacity-60 z-0"
            />
            {isMobileMenuOpen && (
                <div
                    className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
                    onClick={() => setIsMobileMenuOpen(false)}
                />
            )}
            <div
                className={`asidebar flex flex-col gap-10 items-center w-[320px] bg-[#DEDEDE] rounded-[30px] p-5 transition-transform duration-300 ease-in-out
        ${isMobileMenuOpen ? "translate-x-0" : "translate-x-full"}
        md:translate-x-0 md:static fixed top-2 right-2 bottom-2 z-50 md:z-auto
      `}
            >
                <div className="flex justify-between items-center w-full md:justify-center">
                    <img
                        src="/assets/balilogo.svg"
                        alt="Logo"
                        className="w-[136px] h-9 cursor-pointer"
                        onClick={() => navigate('/')}
                    />
                    <button
                        className="md:hidden p-2"
                        onClick={() => setIsMobileMenuOpen(false)}
                    >
                        <svg
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                        >
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                </div>
                <div className="flex flex-col w-full">
                    {menuItems.map((item) => (
                        <button
                            key={item.name}
                            onClick={
                                item.name === "Order Services"
                                    ? handleOrderServicesClick
                                    : () => navigate(getToolRoute(item.name))
                            }
                            className={`text-[16px] flex items-center justify-start gap-3 font-medium w-full px-4 py-5 rounded-[50px] transition hover:bg-[#FF8000] hover:text-white group shadow-none ${loading && item.name === "Order Services"
                                ? "opacity-50 cursor-not-allowed"
                                : ""
                                } ${item.name !== "Order Services" && currentTool === item.name
                                    ? "bg-[#FF8000] text-white"
                                    : ""
                                }`}
                            disabled={loading && item.name === "Order Services"}
                            aria-disabled={loading && item.name === "Order Services"}
                        >
                            <img
                                src={item.icon}
                                alt={item.name}
                                className={`w-5 h-5 transition group-hover:filter group-hover:invert group-hover:brightness-0 ${loading && item.name === "Order Services" ? "animate-spin" : ""
                                    } ${item.name !== "Order Services" && currentTool === item.name
                                        ? "filter invert brightness-0"
                                        : ""
                                    }`}
                            />
                            {loading && item.name === "Order Services" ? "Loading..." : item.name}
                        </button>
                    ))}
                </div>
            </div>
            <div className="right w-full flex flex-col justify-between relative z-10">
                <div className="header shadow-md flex justify-between items-center w-full h-[84px] lg:h-[97px] p-5 rounded-[50px] bg-white mb-5">
                    <div className="flex items-center gap-4">
                        <button
                            className="md:hidden p-2"
                            onClick={() => setIsMobileMenuOpen(true)}
                        >
                            <svg
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                            >
                                <line x1="3" y1="6" x2="21" y2="6"></line>
                                <line x1="3" y1="12" x2="21" y2="12"></line>
                                <line x1="3" y1="18" x2="21" y2="18"></line>
                            </svg>
                        </button>
                        <h5 className="font-bold text-[18px] md:text-[24px] md:px-6">
                            Chat with our AI Bot
                        </h5>
                    </div>
                    <div className="flex justify-center items-center size-12 md:size-16 rounded-full border-[1px] border-solid border-black">
                        <h6 className="font-semibold text-sm md:text-base">EN</h6>
                    </div>
                </div>
                {children}
            </div>
        </div>
    );
};

export default ChatbotLayout;
