import React from "react";
import {useNavigate } from "react-router-dom";

const Footer = () => {
  const navigate = useNavigate();
  return (
    <div className="w-full flex sm:flex-row flex-col justify-between gap-5 items-center bg-[#FF8000] px-5 sm:px-20 py-10 mt-10">
      <h6 className="font-semibold text-white">
        © 2025 EASY Bali | PT SARANA MUDAH BALI.
      </h6>
      <div className="flex flex-col sm:flex-row items-center gap-5">
        <div className="flex items-center gap-2">
          <h6 className="font-semibold text-white cursor-pointer" onClick={() => navigate('/terms-and-conditions')}>Terms & Conditions</h6>
          <div className="w-[2px] h-[20px] bg-white"></div>
          <h6 className="font-semibold text-white cursor-pointer " onClick={() => navigate('/privacy-policy')}>Privacy Policy</h6>
          <div className="w-[2px] h-[20px] bg-white"></div>
          <h6 className="font-semibold text-white cursor-pointer" onClick={() => navigate('/contact-us')}>Contact Us</h6>
        </div>
        <div className="flex gap-2">
        <img src="/assets/facebook.svg" alt="" className="cursor-pointer size-[46px]" onClick={() => window.open('https://www.facebook.com/profile.php?id=61570896083765#', '_blank')}/>
        <img src="/assets/instagram.svg" alt="" className="cursor-pointer size-[46px]" onClick={() => window.open('https://www.instagram.com/easybaliforyou/', '_blank')}/>
        </div>
      </div>
    </div>
  );
};

export default Footer;
