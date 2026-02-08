import React from "react";
import Hero from "../components/home/hero";
import Services from "../components/home/services";
import Experience from "../components/home/experience";
import TryUs from "../components/home/tryUs";
import Footer from "../components/layout/footer";

const Home = () => {
  return (
    <>
      <div className="relative flex flex-col justify-center items-center mx-3 sm:mx-5 mt-5">
        <Hero />
        <div className="container px-[18px] lg:px-[40px] flex flex-col relative mt-20 gap-16 pb-16">
          <Services />
          <Experience />
          <TryUs />
        </div>
        <img
          src="/images/star1.png"
          alt="img"
          className="absolute top-[15%] sm:top-[-1%] -z-10 left-[-7%] max-w-[237px] sm:max-w-[709px] w-full "
        />
        <img
          src="/images/star2.png"
          alt="img"
          className="absolute bottom-[11%] sm:bottom-[14%] -z-10 right-[-11px] max-width-[324px] sm:max-size-[709px]"
        />
        <img
          src="/images/star3.png"
          alt="img"
          className="absolute bottom-[-5%] -z-10 left-[-20px] max-size-[709px]"
        />
      </div>
      <Footer />
    </>
  );
};

export default Home;
