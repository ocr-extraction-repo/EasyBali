import React from "react";
import Button from "../shared/button";

const TryUs = () => {
  const handleWhatsAppClick = () => {
    window.open('https://wa.me/6282247959788', '_blank');
  };
  
  return (
    <div className="experience flex flex-col sm:flex-row items-center justify-between gap-12 relative">
      <div className="left w-full sm:w-3/6 flex relative hidden lg:block">
        <img
          src="/assets/tryus.png"
          alt=""
          className="max-w-[610px] w-full rounded-[30px] sm:rounded-[50px] relative"
        />
        <img
          src="/assets/orange-box.png"
          alt=""
          className="absolute top-[10px] sm:top-[14px] left-[10px] sm:left-[14px] -z-10"
        />
      </div>
      
      <div className="right flex justify-center w-full sm:w-3/6 relative hidden lg:block">
        <div className="max-w-[502px] flex flex-col gap-5">
          <h2 className="font-semibold">Try Us on WhatsApp</h2>
          <p className="font-medium">
            Questions, want to order a service, or just curious? We're one tap away on WhatsApp. Get quick responses, personalized help, and that warm Bali hospitality — all in real time. Because we're here to make it EASY.
          </p>
          <div className="deals flex flex-col gap-2">
            <p className="font-bold">
              Chat with us now and experience the easiest way to reach out! 
            </p>
          </div>
          <Button
            text="Chat on WhatsApp"
            className="w-[236px] h-[58px] btn-primary text-sm font-semibold"
            onClick={handleWhatsAppClick}
          />
        </div>
      </div>
      
      <div className="block lg:hidden flex flex-col shadow-lg rounded-[30px] w-full min-h-[300px] px-[21px] py-[25px] relative overflow-hidden" 
           style={{
             backgroundImage: 'url("/assets/tryus.png")',
             backgroundSize: 'cover',
             backgroundPosition: 'center',
             backgroundRepeat: 'no-repeat'
           }}>
        <div className="absolute inset-0 bg-black bg-opacity-60 rounded-[30px]"></div>
        <div className="relative z-10 flex flex-col h-full">
          <h2 className="font-semibold text-white">Try Us on WhatsApp</h2>
          <p className="font-medium mt-[15px] text-white">
            Questions, want to order a service, or just curious? We're one tap away on WhatsApp. Get quick responses, personalized help, and that warm Bali hospitality — all in real time. Because we're here to make it EASY.
          </p>
          <p className="flex items-center font-bold text-white mt-[15px]"> 
            Chat with us now and experience the easiest way to reach out!
          </p>
          <Button
            text="Chat On WhatsApp"
            className="w-full h-full max-w-[179px] min-h-[53px] btn-primary mt-[19px] text-sm font-semibold"
            onClick={handleWhatsAppClick}
          />
        </div>
      </div>
      
      <img 
        src="/assets/whatsapp.png" 
        alt="" 
        className="w-[105px] h-[105px] hidden sm:block absolute -bottom-12 right-0 animate-float cursor-pointer"  
        onClick={handleWhatsAppClick}
      />
    </div>
  );
};

export default TryUs;