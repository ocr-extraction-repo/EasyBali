import React, { useState } from "react";
import { Modal, Select } from "antd";
import Button from "../shared/button";
import { useNavigate } from "react-router-dom";

const { Option } = Select;

const Hero = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedVilla, setSelectedVilla] = useState(null);
  const [chatInput, setChatInput] = useState("");
  const navigate = useNavigate();

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleVillaChange = (value) => {
    setSelectedVilla(value);
  };

  const handleChat = async () => {
    if (!chatInput.trim()) {
      message.warning("Please enter a message");
      return;
    }

    // Get or create user ID
    let userId = localStorage.getItem('userId');
    if (!userId) {
      userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('userId', userId);
    }

    // Navigate to chatbot with general chat type
    navigate("/chatbot", { 
      state: { 
        chatType: 'general', // This is the general chatbot
        userId: userId,
        activeTab: 'Chat', // Or whatever you want to call it
        initialMessage: {
          id: Date.now(),
          text: chatInput,
          sender: "user",
          timestamp: new Date().toLocaleTimeString([], { 
            hour: "2-digit", 
            minute: "2-digit" 
          })
        }
      } 
    });
    setChatInput("");
  };


  const handleKeyPress = (e) => {
    if (e.key === "Enter" && chatInput.trim()) {
      handleChat();
    }
  };

  const handleChatButtonClick = () => {
    handleChat();
  };

  const villas = [
    "Villa Sunset Paradise",
    "Villa Ocean View",
    "Villa Mountain Retreat",
    "Villa Tropical Garden",
    "Villa Beachfront Bliss",
  ];

  return (
    <>
      <section className="hero relative max-w-[1392px] w-full flex flex-col justify-center items-center gap-[12px] rounded-[35px] sm:rounded-[50px] h-[500px] sm:h-[711px] z-[1] bg-no-repeat bg-cover bg-center">
        <img
         src="/assets/logo.svg"
         alt="logo"
         className="hero-logo absolute top-[30px] left-[30px]"
        />
        <div
          className="language cursor-pointer flex justify-center items-center absolute top-[30px] right-[30px] rounded-full size-9 sm:size-[60px] border-[2px] border-solid border-white"
          onClick={showModal}
        >
          <h5 className="text-[10px] sm:text-[22px] font-semibold text-white">
            EN
          </h5>
        </div>
        <div className="hero-chat-input absolute -bottom-[7%] sm:-bottom-[10%] left-[12px] sm:left-0 z-[3] w-[90%] lg:w-full">
          <input
            type="text"
            placeholder="Chat with our AI Bot"
            className="w-full px-5 sm:px-10 pr-[100px] sm:pr-[150px] py-7 sm:py-10 rounded-[50px] text-[#8e8e8e] text-[16px] sm:text-[18px] border border-[#c6c6c6] placeholder:text-[#8e8e8e] outline-none focus:outline-none focus:border-[#c6c6c6] bg-white"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <div className="btns flex items-center justify-center gap-3 sm:gap-[30px] absolute bottom-6 sm:bottom-[17px] right-[35px]">
            <img src="/assets/mic.svg" alt="" className="cursor-pointer" />
            <img
              src="/assets/chat-btn.svg"
              alt=""
              className="cursor-pointer sm:size-full size-[33px]"
              onClick={handleChatButtonClick}
            />
          </div>
        </div>
      </section>

      <Modal
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
        className="scan-modal"
        width="90%"
        style={{ maxWidth: "1030px" }}
        centered
      >
        <div className="scan-modal-content">
          <div className="modal-inner-content">
            <h2 className="modal-title">Please Scan The QR Code</h2>
            <p className="modal-subtitle">
              Welcome to EASY Bali! If you discovered us in your villa, please
              scan the QR code placed there.
            </p>
            <div className="qr-image-wrapper">
              <img src="/images/scanner.png" alt="img" className="qr-image" />
            </div>
            <p className="modal-description">
              You can also do this later if you would like to order any of our
              services.
            </p>
            <Button text="Skip" className="btn-primary modal-skip-btn" />
            <div className="villa-dropdown-wrapper">
              <Select
                placeholder="Select Villas from Our List Here"
                className="villa-dropdown"
                onChange={handleVillaChange}
                value={selectedVilla}
                suffixIcon={
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M6 9l6 6 6-6"
                      stroke="white"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                }
              >
                {villas.map((villa, index) => (
                  <Option key={index} value={villa}>
                    {villa}
                  </Option>
                ))}
              </Select>
            </div>
          </div>
        </div>
      </Modal>
    </>
  );
};

export default Hero;