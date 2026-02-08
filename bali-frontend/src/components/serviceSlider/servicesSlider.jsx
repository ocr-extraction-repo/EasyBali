import React from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay } from "swiper/modules";
import "swiper/css";

const ServicesSlider = () => {
  return (
    <div className="relative w-full">
      {/* Left gradient */}
      <div className="absolute left-0 top-0 h-full w-[80px] z-10 pointer-events-none bg-gradient-to-r from-white to-transparent"></div>

      {/* Right gradient */}
      <div className="absolute right-0 top-0 h-full w-[80px] z-10 pointer-events-none bg-gradient-to-l from-white to-transparent"></div>

      <Swiper
        modules={[Autoplay]}
        spaceBetween={0}
        slidesPerView={1.2}
        centeredSlides={true}
        loop={true}
        autoplay={{
          delay: 1000,
          disableOnInteraction: false,
        }}
        breakpoints={{
          640: { slidesPerView: 2.2 },
          1024: { slidesPerView: 3.2 },
        }}
      >
        <SwiperSlide>
          <div className="card">Card 1</div>
        </SwiperSlide>
        <SwiperSlide>
          <div className="card">Card 2</div>
        </SwiperSlide>
        <SwiperSlide>
          <div className="card">Card 3</div>
        </SwiperSlide>
        <SwiperSlide>
          <div className="card">Card 4</div>
        </SwiperSlide>{" "}
        <SwiperSlide>
          <div className="card">Card 4</div>
        </SwiperSlide>{" "}
        <SwiperSlide>
          <div className="card">Card 4</div>
        </SwiperSlide>{" "}
        <SwiperSlide>
          <div className="card">Card 4</div>
        </SwiperSlide>{" "}
        <SwiperSlide>
          <div className="card">Card 4</div>
        </SwiperSlide>
      </Swiper>
    </div>
  );
};

export default ServicesSlider;
