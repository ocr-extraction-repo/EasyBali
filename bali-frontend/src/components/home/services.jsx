import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getSubMenu } from '../services/api';
import { chatAPI } from '../../api/chatApi'; // Import the centralized API service

const Services = () => {
  const navigate = useNavigate();
  const [orderServicesLoading, setOrderServicesLoading] = useState(false);
  const [localGuideLoading, setLocalGuideLoading] = useState(false);
  const [recommendationsLoading, setRecommendationsLoading] = useState(false);
  const [whatToDoLoading, setWhatToDoLoading] = useState(false);
  const [currencyConverterLoading, setCurrencyConverterLoading] = useState(false);
  const [planMyTripLoading, setPlanMyTripLoading] = useState(false);

  const handleOrderServicesClick = async () => {
    try {
      setOrderServicesLoading(true);
      const response = await getSubMenu('Order Services');
      navigate('/categories', {
        state: {
          mainMenu: 'categories',
          data: response.data
        }
      });
    } catch (error) {
      console.error('Failed to fetch Order Services:', error);
      navigate('/services', {
        state: {
          mainMenu: 'services',
          data: []
        }
      });
    } finally {
      setOrderServicesLoading(false);
    }
  };

  const handlelocalGuideClick = async () => {
    try {
      setLocalGuideLoading(true);
      const response = await getSubMenu('Local Guide');
      navigate('/categories', {
        state: {
          mainMenu: 'categories',
          data: response.data
        }
      });
    } catch (error) {
      console.error('Failed to fetch Local Guide:', error);
      navigate('/services', {
        state: {
          mainMenu: 'services',
          data: []
        }
      });
    } finally {
      setLocalGuideLoading(false);
    }
  };

  const handleRecommendationsClick = async () => {
    try {
      setRecommendationsLoading(true);
      const response = await getSubMenu('Recommendations');
      navigate('/categories', {
        state: {
          mainMenu: 'categories',
          data: response.data
        }
      });
    } catch (error) {
      console.error('Failed to fetch Recommendations:', error);
      navigate('/services', {
        state: {
          mainMenu: 'services',
          data: []
        }
      });
    } finally {
      setRecommendationsLoading(false);
    }
  };

  // Generic function to initialize chat-based services
  const initializeChatService = async (chatType, activeTabName, setLoadingState) => {
    try {
      setLoadingState(true);
      
      // Get or create user ID
      const userId = chatAPI.getUserId();
      
      // Send initial "Hi" message to get bot's greeting
      const response = await chatAPI.sendMessage(chatType, userId, "Hi");
      
      // Create initial message object
      const initialMessage = {
        id: Date.now(),
        text: response.response,
        sender: "bot",
        timestamp: new Date().toLocaleTimeString([], { 
          hour: "2-digit", 
          minute: "2-digit" 
        }),
      };
      
      // Save to localStorage using the centralized API
      chatAPI.saveChatHistory(userId, chatType, [initialMessage]);
      
      // Navigate to chatbot
      navigate('/chatbot', {
        state: {
          activeTab: activeTabName,
          chatType: chatType,
          userId: userId,
          initialMessage: initialMessage
        }
      });
    } catch (error) {
      console.error(`Failed to initialize ${chatType} chat:`, error);
      alert('Failed to start chat. Please try again.');
    } finally {
      setLoadingState(false);
    }
  };

  const handleCurrencyConverterClick = () => {
    initializeChatService(
      'currency-converter',
      'Currency Converter',
      setCurrencyConverterLoading
    );
  };

  const handlePlanMyTripClick = () => {
    initializeChatService(
      'plan-my-trip',
      'Plan My Trip!',
      setPlanMyTripLoading
    );
  };

  const handleWhatToDoClick = () => {
    initializeChatService(
      'what-to-do',
      'What To Do Today?',
      setWhatToDoLoading
    );
  };

  return (
    <section className="services flex flex-col gap-[40px]">
      <h2 className="font-semibold text-black text-center">
        Everything You Need, Right At Your Fingertips
      </h2>

      <div className="service-cards grid grid-cols-2 md:grid-cols-3 gap-[12px] md:gap-[20px] place-items-center">
        {/* Card 1 - Order Services (API CALL) */}
        <div
          className={`card group max-w-[425px] w-full h-[101px] md:h-[200px] bg-white rounded-[20px] md:rounded-[50px] flex flex-col justify-center items-center gap-[10px] md:gap-[20px] shadow-[0_8px_24px_rgba(0,0,0,0.15)] transition-all duration-300 ease-in-out hover:bg-[#ff8000] hover:shadow-[0_12px_28px_rgba(0,0,0,0.25)] cursor-pointer ${
            orderServicesLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          onClick={!orderServicesLoading ? handleOrderServicesClick : undefined}
        >
          <div className="flex items-center justify-center">
            <img
              src="/assets/order.svg"
              alt="Order Services"
              className={`w-[34.25px] h-[34.25px] md:w-[56px] md:h-[56px] filter transition duration-300 ease-in-out group-hover:brightness-0 group-hover:invert ${
                orderServicesLoading ? 'animate-spin' : ''
              }`}
            />
          </div>
          <h5 className={`text-black font-semibold text-center text-[12px] md:text-[24px] transition duration-300 ease-in-out group-hover:text-white ${
            orderServicesLoading ? 'text-gray-400' : ''
          }`}>
            {orderServicesLoading ? 'Loading...' : 'Order Services'}
          </h5>
        </div>

        {/* Card 2 - Local Guide */}
        <div
          className={`card group max-w-[425px] w-full h-[101px] md:h-[200px] bg-white rounded-[20px] md:rounded-[50px] flex flex-col justify-center items-center gap-[10px] md:gap-[25px] shadow-[0_8px_24px_rgba(0,0,0,0.15)] transition-all duration-300 ease-in-out hover:bg-[#ff8000] hover:shadow-[0_12px_28px_rgba(0,0,0,0.25)] cursor-pointer ${
            localGuideLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          onClick={!localGuideLoading ? handlelocalGuideClick : undefined}
        >
          <div className="h-[34.25px] md:h-[54px] flex items-center justify-center">
            <img
              src="/assets/guide.svg"
              alt="Local Guide"
              className={`w-[42.78px] h-[42.78px] md:w-[90px] md:h-[90px] filter transition duration-300 ease-in-out group-hover:brightness-0 group-hover:invert ${
                localGuideLoading ? 'animate-spin' : ''
              }`}
            />
          </div>
          <h5 className={`text-black font-semibold text-center text-[12px] md:text-[24px] transition duration-300 ease-in-out group-hover:text-white ${
            localGuideLoading ? 'text-gray-400' : ''
          }`}>
            {localGuideLoading ? 'Loading...' : 'Local Guide'}
          </h5>
        </div>

        {/* Card 3 - Voice Translator */}
        <div className="card group max-w-[425px] w-full h-[101px] md:h-[200px] bg-white rounded-[20px] md:rounded-[50px] flex flex-col justify-center items-center gap-[10px] md:gap-[20px] shadow-[0_8px_24px_rgba(0,0,0,0.15)] transition-all duration-300 ease-in-out hover:bg-[#ff8000] hover:shadow-[0_12px_28px_rgba(0,0,0,0.25)] cursor-pointer">
          <img 
            src="/assets/translator.svg" 
            alt="Voice Translator" 
            className="w-[34.25px] h-[34.25px] md:w-[56px] md:h-[56px] filter transition duration-300 ease-in-out group-hover:brightness-0 group-hover:invert" 
          />
          <h5 className="text-black font-semibold text-center text-[12px] md:text-[24px] transition duration-300 ease-in-out group-hover:text-white">
            Voice Translator
          </h5>
        </div>

        {/* Card 4 - Currency Converter */}
        <div
          className={`card group max-w-[425px] w-full h-[101px] md:h-[200px] bg-white rounded-[20px] md:rounded-[50px] flex flex-col justify-center items-center gap-[10px] md:gap-[20px] shadow-[0_8px_24px_rgba(0,0,0,0.15)] transition-all duration-300 ease-in-out hover:bg-[#ff8000] hover:shadow-[0_12px_28px_rgba(0,0,0,0.25)] cursor-pointer ${
            currencyConverterLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          onClick={!currencyConverterLoading ? handleCurrencyConverterClick : undefined}
        >
          <img
            src="/assets/currency.svg"
            alt="Currency Converter"
            className={`w-[34.25px] h-[34.25px] md:w-[56px] md:h-[56px] filter transition duration-300 ease-in-out group-hover:brightness-0 group-hover:invert ${
              currencyConverterLoading ? 'animate-spin' : ''
            }`}
          />
          <h5 className={`text-black font-semibold text-center text-[12px] md:text-[24px] transition duration-300 ease-in-out group-hover:text-white ${
            currencyConverterLoading ? 'text-gray-400' : ''
          }`}>
            {currencyConverterLoading ? 'Loading...' : 'Currency Converter'}
          </h5>
        </div>

        {/* Card 5 - What To Do Today? */}
        <div
          className={`card group max-w-[425px] w-full h-[101px] md:h-[200px] bg-white rounded-[20px] md:rounded-[50px] flex flex-col justify-center items-center gap-[10px] md:gap-[20px] shadow-[0_8px_24px_rgba(0,0,0,0.15)] transition-all duration-300 ease-in-out hover:bg-[#ff8000] hover:shadow-[0_12px_28px_rgba(0,0,0,0.25)] cursor-pointer ${
            whatToDoLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          onClick={!whatToDoLoading ? handleWhatToDoClick : undefined}
        >
          <img
            src="/assets/today.svg"
            alt="What To Do Today?"
            className={`w-[34.25px] h-[34.25px] md:w-[56px] md:h-[56px] filter transition duration-300 ease-in-out group-hover:brightness-0 group-hover:invert ${
              whatToDoLoading ? 'animate-spin' : ''
            }`}
          />
          <h5 className={`text-black font-semibold text-center text-[12px] md:text-[24px] transition duration-300 ease-in-out group-hover:text-white ${
            whatToDoLoading ? 'text-gray-400' : ''
          }`}>
            {whatToDoLoading ? 'Loading...' : 'What To Do Today?'}
          </h5>
        </div>

        {/* Card 6 - Plan My Trip! */}
        <div
          className={`card group max-w-[425px] w-full h-[101px] md:h-[200px] bg-white rounded-[20px] md:rounded-[50px] flex flex-col justify-center items-center gap-[10px] md:gap-[20px] shadow-[0_8px_24px_rgba(0,0,0,0.15)] transition-all duration-300 ease-in-out hover:bg-[#ff8000] hover:shadow-[0_12px_28px_rgba(0,0,0,0.25)] cursor-pointer ${
            planMyTripLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          onClick={!planMyTripLoading ? handlePlanMyTripClick : undefined}
        >
          <img
            src="/assets/trip.svg"
            alt="Plan My Trip!"
            className={`w-[34.25px] h-[34.25px] md:w-[56px] md:h-[56px] filter transition duration-300 ease-in-out group-hover:brightness-0 group-hover:invert ${
              planMyTripLoading ? 'animate-spin' : ''
            }`}
          />
          <h5 className={`text-black font-semibold text-center text-[12px] md:text-[24px] transition duration-300 ease-in-out group-hover:text-white ${
            planMyTripLoading ? 'text-gray-400' : ''
          }`}>
            {planMyTripLoading ? 'Loading...' : 'Plan My Trip!'}
          </h5>
        </div>

        {/* Card 7 - Recommendations */}
        <div
          className={`card group max-w-[425px] w-full h-[101px] md:h-[200px] bg-white rounded-[20px] md:rounded-[50px] flex flex-col justify-center items-center gap-[10px] md:gap-[20px] shadow-[0_8px_24px_rgba(0,0,0,0.15)] transition-all duration-300 ease-in-out hover:bg-[#ff8000] hover:shadow-[0_12px_28px_rgba(0,0,0,0.25)] cursor-pointer ${
            recommendationsLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          onClick={!recommendationsLoading ? handleRecommendationsClick : undefined}
        >
          <div className="flex items-center justify-center">
            <img
              src="/assets/recommend.svg"
              alt="Recommendations"
              className={`w-[34.25px] h-[34.25px] md:w-[56px] md:h-[56px] filter transition duration-300 ease-in-out group-hover:brightness-0 group-hover:invert ${
                recommendationsLoading ? 'animate-spin' : ''
              }`}
            />
          </div>
          <h5 className={`text-black font-semibold text-center text-[12px] md:text-[24px] transition duration-300 ease-in-out group-hover:text-white ${
            recommendationsLoading ? 'text-gray-400' : ''
          }`}>
            {recommendationsLoading ? 'Loading...' : 'Recommendations'}
          </h5>
        </div>

        {/* Card 8 - Discount & Promotions */}
        <div className="card group max-w-[425px] w-full h-[101px] md:h-[200px] bg-white rounded-[20px] md:rounded-[50px] flex flex-col justify-center items-center gap-[10px] md:gap-[20px] shadow-[0_8px_24px_rgba(0,0,0,0.15)] transition-all duration-300 ease-in-out hover:bg-[#ff8000] hover:shadow-[0_12px_28px_rgba(0,0,0,0.25)] cursor-pointer">
          <img 
            src="/assets/discount.svg" 
            alt="Discount & Promotions" 
            className="w-[34.25px] h-[34.25px] md:w-[56px] md:h-[56px] filter transition duration-300 ease-in-out group-hover:brightness-0 group-hover:invert" 
          />
          <h5 className="text-black font-semibold text-center text-[12px] md:text-[24px] transition duration-300 ease-in-out group-hover:text-white">
            Discount & Promotions
          </h5>
        </div>

        {/* Card 9 - Passport Submission */}
        <div className="card group col-span-2 md:col-span-1 max-w-[425px] w-full h-[101px] md:h-[200px] bg-white rounded-[20px] md:rounded-[50px] flex flex-col justify-center items-center gap-[10px] md:gap-[20px] shadow-[0_8px_24px_rgba(0,0,0,0.15)] transition-all duration-300 ease-in-out hover:bg-[#ff8000] hover:shadow-[0_12px_28px_rgba(0,0,0,0.25)] cursor-pointer">
          <img 
            src="/assets/passport.svg" 
            alt="Passport Submission" 
            className="w-[34.25px] h-[34.25px] md:w-[56px] md:h-[56px] filter transition duration-300 ease-in-out group-hover:brightness-0 group-hover:invert" 
          />
          <h5 className="text-black font-semibold text-center text-[12px] md:text-[24px] transition duration-300 ease-in-out group-hover:text-white">
            Passport Submission
          </h5>
        </div>
      </div>
    </section>
  );
};

export default Services;