import React from "react";
import Button from "../shared/button";

const Experience = () => {
  return (
    <div className="experience flex flex-col sm:flex-row items-start sm:items-center justify-between gap-12">
      <div className="hidden lg:block left w-full sm:w-3/6">
        <div className="max-w-[397px] flex flex-col gap-5">
          <h2 className="font-semibold">Plan Your Bali Experience the Easy Way</h2>
          <p className="font-medium">
            From spa treatments to villa experiences, local guides to instant
            translations — Easy Bali brings everything you need for a smooth and
            enjoyable journey.
          </p>
          <div className="deals flex flex-col gap-2">
            <p className="flex items-center gap-1 font-bold"> 
              <img src="/assets/checkbox.svg" alt="" />
              Book trusted services with ease
            </p>
            <p className="flex items-center gap-1 font-bold">
              <img src="/assets/checkbox.svg" alt="" />
              Save time & unlock exclusive deals
            </p>
            <p className="flex items-center gap-1 font-bold">
              <img src="/assets/checkbox.svg" alt="" />
              Travel like a local, stress-free
            </p>
          </div>
          <Button
            text="Start Exploring Now"
            className="w-[278px] h-[58px] btn-primary text-sm font-semibold"
          />
        </div>
      </div>

      <div className="block lg:hidden flex flex-col shadow-lg rounded-[30px] w-full h-[383px] px-[21px] py-[25px] relative overflow-hidden" 
           style={{
             backgroundImage: 'url("/assets/experience.png")',
             backgroundSize: 'cover',
             backgroundPosition: 'center',
             backgroundRepeat: 'no-repeat'
           }}>
        <div className="absolute inset-0 bg-black bg-opacity-60 rounded-[30px]"></div>
        <div className="relative z-10 flex flex-col h-full">
          <h2 className="font-semibold text-white">Plan Your Bali <br/> Experience <br/> the Easy Way</h2>
          <p className="font-medium mt-[15px] text-white">
            From spa treatments to villa experiences, local guides to instant
            translations — Easy Bali brings everything you need for a smooth and
            enjoyable journey.
          </p>
          <div className="deals flex flex-col gap-2 mt-[15px]">
            <p className="flex items-center gap-1 font-bold text-white"> 
              <img src="/assets/checkbox.svg" alt="" />
              Book trusted services with ease
            </p>
            <p className="flex items-center gap-1 font-bold text-white">
              <img src="/assets/checkbox.svg" alt="" />
              Save time & unlock exclusive deals
            </p>
            <p className="flex items-center gap-1 font-bold text-white">
              <img src="/assets/checkbox.svg" alt="" />
              Travel like a local, stress-free
            </p>
          </div>
          <Button
            text="Start Exploring Now"
            className="w-full h-full max-w-[179px] min-h-[53px] btn-primary mt-[19px] text-sm font-semibold"
          />
        </div>
      </div>
      
      <div className="hidden lg:block right w-full sm:w-3/6 flex justify-end relative">
        <img src="/assets/experience.png" alt="" className="max-w-[610px] w-full rounded-[30px] sm:rounded-[50px] relative"/>
        <img src="/assets/orange-box.png" alt="" className="absolute top-[10px] sm:top-[14px] right-[10px] sm:right-[14px] -z-10"/>
      </div>
    </div>
  );
};

export default Experience;