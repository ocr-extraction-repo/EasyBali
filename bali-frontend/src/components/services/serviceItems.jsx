import React, { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import Slider from "react-slick"
import "slick-carousel/slick/slick.css"
import "slick-carousel/slick/slick-theme.css"
import { toast, ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import balilogo from '../../assets/images/balilogo.svg'
import secondlogo from '../../assets/images/secondlogo.svg'
import bottomRightPng from '../../assets/images/right-bottom.png'
import topLeftPng from '../../assets/images/top-left.png'
import { getServiceItems } from './api.jsx'

const ServiceItems = () => {  
  const navigate = useNavigate();
  const location = useLocation();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [screenSize, setScreenSize] = useState('desktop');
  const [sliderData, setSliderData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [buttonLoading, setButtonLoading] = useState(null);
  const [formData, setFormData] = useState({
    fullName: '',
    phoneNumber: '',
    countryCode: '+62',
    date: '',
    time: '12:00-14:00',
    noOfPerson: '2'
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiMessage, setApiMessage] = useState('');
  const [sessionId, setSessionId] = useState('');
   
  // Default fallback
  const defaultSliderData = [
    {
      id: 1,
      title: "Coming Soon",
      subtitle: "Coming Soon",
      description: "Service details coming soon!",
      buttonText: "IDR 0",
      image: "https://easybali.s3.ap-southeast-2.amazonaws.com/EASYBali+-+Web+Images/serviceitems/SI-Balinese.webp"
    }
  ];

  // Fetch API data on mount
  useEffect(() => {
    const fetchData = async () => {
      const mainMenu = location.state?.mainMenu;
      const passedData = location.state?.data;
      
      if (passedData && passedData.length > 0) {
        const transformedData = passedData.map((item, index) => ({
          id: index + 1,
          title: item.service_item,
          subtitle: item.service_item,
          description: item.description,
          buttonText: `IDR ${item.button}`,
          image: item.picture
        }));
        setSliderData(transformedData);
      } else if (mainMenu) {
        try {
          setLoading(true);
          const response = await getServiceItems(mainMenu);
          const transformedData = response.data.map((item, index) => ({
            id: index + 1,
            title: item.service_item,
            subtitle: item.service_item,
            description: item.description,
            buttonText: `IDR ${item.button}`,
            image: item.picture
          }));
          setSliderData(transformedData);
        } catch (err) {
          console.error('Error fetching service items:', err);
          setSliderData(defaultSliderData);
        }
      } else {
        setSliderData(defaultSliderData);
      }
      setLoading(false);
    };

    fetchData();
  }, [location.state]);

  // Screen size detection
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      if (width <= 768) setScreenSize('mobile');
      else if (width <= 1024) setScreenSize('tablet');
      else setScreenSize('desktop');
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleBookingClick = (slideId) => {
    const selected = sliderData.find(item => item.id === slideId);
    setSelectedItem(selected);
    setButtonLoading(slideId);
    setTimeout(() => {
      setIsModalOpen(true);
      setButtonLoading(null);
    }, 800);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedItem(null);
    setFormData({
      fullName: '',
      phoneNumber: '',
      countryCode: '+62',
      date: '',
      time: '12:00-14:00',
      noOfPerson: '2'
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const createSession = async (payload) => {
    try {
      const response = await fetch('https://easy-bali.onrender.com/create-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedItem) return;
    
    setIsSubmitting(true);
    
    try {
      const priceMatch = selectedItem.buttonText.match(/IDR\s*([\d\s]+)/);
      const price = priceMatch ? priceMatch[1].trim() : '0';
      
      const payload = {
        service_name: selectedItem.title,
        name: formData.fullName,
        date: `${formData.date}T${formData.time.split('-')[0]}:00`,
        time: formData.time.split('-')[0],
        price: price,
        no_of_person: formData.noOfPerson,
        phone_number: `${formData.countryCode}${formData.phoneNumber}`
      };
      
      console.log('API Payload:', payload);
      
      const response = await createSession(payload);
      console.log('API Response:', response);
      
      setApiMessage(response.message);
      setSessionId(response.session_id);
      
      handleCloseModal();
      navigate('/chatbot', { 
        state: { 
          message: response.message, 
          sessionId: response.session_id 
        } 
      });
      
    } catch (error) {
      console.error('Submission error:', error);
      alert('Something went wrong. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const CustomPrevArrow = ({ onClick }) => (
    <button className="absolute left-4 top-1/2 transform -translate-y-1/2 z-10 bg-white rounded-full w-12 h-12 flex items-center justify-center shadow-lg hover:shadow-xl transition-all" onClick={onClick}>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
        <path d="M15 18l-6-6 6-6" stroke="#333" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    </button>
  );

  const CustomNextArrow = ({ onClick }) => (
    <button className="absolute right-4 top-1/2 transform -translate-y-1/2 z-10 bg-white rounded-full w-12 h-12 flex items-center justify-center shadow-lg hover:shadow-xl transition-all" onClick={onClick}>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
        <path d="M9 18l6-6-6-6" stroke="#333" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    </button>
  );

  const getSliderSettings = () => {
    const baseSettings = {
      dots: false, infinite: true, speed: 500, swipe: true, swipeToSlide: true, 
      draggable: true, touchThreshold: 10, lazyLoad: false, accessibility: true,
      adaptiveHeight: false, arrows: true, autoplay: false, pauseOnHover: true,
      pauseOnFocus: true, pauseOnDotsHover: false
    };
    if (screenSize === 'mobile') return { ...baseSettings, slidesToShow: 1, slidesToScroll: 1, centerMode: false, centerPadding: "0px", focusOnSelect: false, arrows: false, variableWidth: false };
    else if (screenSize === 'tablet') return { ...baseSettings, slidesToShow: 3, slidesToScroll: 1, centerMode: true, centerPadding: "0", focusOnSelect: true, arrows: true, prevArrow: <CustomPrevArrow />, nextArrow: <CustomNextArrow />, variableWidth: false };
    else return { ...baseSettings, className: "center", slidesToShow: 5, slidesToScroll: 1, centerMode: true, centerPadding: "0", focusOnSelect: true, arrows: true, prevArrow: <CustomPrevArrow />, nextArrow: <CustomNextArrow />, variableWidth: false };
  };

  const settings = getSliderSettings();

  if (loading) {
    return (
      <div className='bg-white min-h-screen flex items-center justify-center'>
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#FF8000]"></div>
      </div>
    );
  }

  return (
    <div className='bg-white min-h-screen flex flex-col justify-between background-class relative'> 
      <img src={topLeftPng} alt="Top Left Icon" className="absolute top-[0px] left-[0px] sm:left-[0px] md:left-[0px] w-[350px] sm:w-[200px] md:w-[400px] opacity-60 z-0" />
      <img src={bottomRightPng} alt="Bottom Right Icon" className="absolute bottom-0 right-0 w-[300px] sm:w-[250px] md:w-[450px] opacity-60 z-0" />
      
      <div className='relative z-10'>
        <div className='flex items-center justify-between px-[24px] lg:px-[100px] py-[24px] lg:py-[40px]'>
          <img src={balilogo} alt='Bali' onClick={() => navigate('/')} className='cursor-pointer h-[30px] lg:h-auto' />
          <img src={secondlogo} alt='Second Logo' className='w-[62px] h-[32px] lg:h-[40px] cursor-pointer'/>
        </div>
      </div>
      
      <div className='relative z-10'>
        <Slider {...settings}>
         {sliderData.map((slide) => (
           <div key={slide.id} className='slider-item'>
             <div className='flex flex-col rounded-[50px] w-[295px] mx-auto bg-white px-[19px] pt-[20px] h-[540px] therapy-slider-card transition-all duration-300 shadow-lg overflow-hidden'>
               <img src={slide.image} alt='therapy' className='rounded-[50px] w-full h-[280px] object-cover flex-shrink-0' />
               <p className='text-[24px] font-bold text-black mt-[6px] ml-[6px] mr-[6px] flex-shrink-0'>
                 {slide.title}
               </p>
               <p className='text-[18px] font-normal text-gray-600 mt-[6px] ml-[6px] mr-[6px] flex-1 line-clamp-4'>
                 {slide.description}
               </p>
               <div className='px-[8px] w-full pt-[12px] pb-[12px] flex-shrink-0'>
                 <button 
                   className={`h-[63px] rounded-[50px] text-white font-medium w-full mb-[4px] transition-all flex items-center justify-center gap-2 ${
                     buttonLoading === slide.id 
                       ? 'bg-gray-400 cursor-not-allowed' 
                       : 'bg-[#FF8000] hover:bg-[#e6720a] cursor-pointer'
                   }`}
                   onClick={() => handleBookingClick(slide.id)}
                   disabled={buttonLoading === slide.id}
                 >
                   {buttonLoading === slide.id ? (
                     <>
                       <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                       Loading...
                     </>
                   ) : (
                     slide.buttonText
                   )}
                 </button>
               </div>
             </div>
           </div>
         ))}
       </Slider>
      </div>

      <div className='px-[24px] lg:px-[100px] z-10'>
        <div className='rounded-full bg-white shadow-lg flex px-[40px] py-[20px] items-center justify-between h-[85px] mb-[30px] border-class'>
          <input type="text" placeholder="Chat with our AI Bot" className="w-[90%] py-4 sm:py-6 rounded-[50px] text-[#8e8e8e] text-[16px] sm:text-[18px] placeholder:text-[#8e8e8e]" />
          <div className='flex items-center gap-4'>
            <img src="/assets/mic.svg" alt="" className="cursor-pointer" />
            <img src="/assets/chat-btn.svg" alt="" className="cursor-pointer w-[40px] h-[40px] sm:w-[50px] sm:h-[50px]" />
          </div>
        </div>
      </div>

      {isModalOpen && selectedItem && (
      <div className='fixed inset-0 bg-gray-800/20 backdrop-blur-md flex items-center justify-center z-50 p-4'>
        <div className='bg-white rounded-[30px] sm:rounded-[50px] py-4 sm:py-[20px] w-[370px] sm:w-[90vw] lg:w-[750px] max-w-[370px] sm:max-w-[90vw] lg:max-w-[750px] h-auto max-h-[870px] sm:max-h-[90vh] relative shadow-[0_0_40px_rgba(0,0,0,0.3)] overflow-y-auto'>
          
          {/* Header */}
          <div className='mb-4 sm:mb-8 mx-8 sm:mx-10 lg:mx-14 mt-4 sm:mt-6'>
            <h2 className='text-2xl sm:text-3xl lg:text-4xl font-bold text-black mb-2'>
              {selectedItem.title}
            </h2>
            <p className='text-gray-600 text-[14px] sm:text-[16px]'>
              {selectedItem.description}
            </p>
          </div>

          {/* Form */}
          <form className='space-y-6 sm:space-y-6 mx-7 sm:mx-10 lg:mx-14' onSubmit={handleSubmit}>
            
            {/* Full Name & Phone Number */}
            <div className='grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-2'>
              <div className='relative'>
                <label className='absolute -top-2 left-3 bg-white px-2 sm:px-5 text-[16px] sm:text-[18px] font-semibold text-gray-900 z-10'>
                  Full Name
                </label>
                <input 
                  type='text' 
                  name='fullName'
                  value={formData.fullName}
                  onChange={handleInputChange}
                  placeholder='Name here'
                  required
                  className='w-full h-[56px] sm:h-[70px] text-[16px] sm:text-[18px] px-4 sm:px-8 py-3 border border-black rounded-[20px] focus:outline-none focus:border-blue-400 text-black bg-white'
                />
              </div>
              
              <div className='relative'>
                <label className='absolute -top-2 left-3 bg-white px-2 text-[16px] sm:text-[18px] font-semibold text-gray-700 z-10'>
                  Phone Number
                </label>
                <div className='flex'>
                  <select 
                    name='countryCode'
                    value={formData.countryCode}
                    onChange={handleInputChange}
                    className='px-2 sm:px-3 py-3 border border-black rounded-l-[20px] bg-gray-50 text-black text-sm w-16 sm:w-20'
                  >
                    <option value='+62'>+62</option>
                    <option value='+1'>+1</option>
                    <option value='+44'>+44</option>
                  </select>
                  <input 
                    type='text' 
                    name='phoneNumber'
                    value={formData.phoneNumber}
                    onChange={handleInputChange}
                    placeholder='0812 3456 7890'
                    required
                    className='flex-1 h-[56px] sm:h-[70px] px-3 py-3 border border-black rounded-r-[20px] focus:outline-none focus:border-blue-400 text-black bg-white border-l-0'
                  />
                </div>
              </div>
            </div>

            {/* Select Date */}
            <div className='relative'>
              <label className='absolute -top-2 left-3 bg-white px-2 sm:px-5 text-[16px] sm:text-[18px] font-semibold text-gray-700 z-10'>
                Select Date
              </label>
              <input 
                type='date' 
                name='date'
                value={formData.date}
                onChange={handleInputChange}
                required
                className='w-full h-[56px] sm:h-[70px] px-4 sm:px-8 py-3 border border-black rounded-[20px] focus:outline-none focus:border-blue-400 text-black bg-white'
              />
              <p className='text-[12px] sm:text-[14px] text-gray-500 mt-2 px-2'>
                To avoid scheduling issues, please select a 2+ hour time window for your service. While our providers aim to start at your chosen time, this window helps prevent delays and ensures a smooth experience. Thanks for your understanding!
              </p>
            </div>

            {/* Select Time */}
            <div className='relative'>
              <label className='absolute -top-2 left-3 bg-white px-2 sm:px-5 text-[16px] sm:text-[18px] font-semibold text-gray-700 z-20'>
                Select Time
              </label>
              <select 
                name='time'
                value={formData.time}
                onChange={handleInputChange}
                className='w-full h-[56px] sm:h-[70px] px-4 sm:px-8 py-3 border border-black rounded-[20px] focus:outline-none focus:border-blue-400 bg-white appearance-none cursor-pointer text-black'
              >
                <option value="12:00-14:00" className='bg-white text-black hover:bg-blue-50'>12:00 PM - 02:00 PM</option>
                <option value="14:00-16:00" className='bg-white text-black hover:bg-blue-50'>02:00 PM - 04:00 PM</option>
                <option value="16:00-18:00" className='bg-white text-black hover:bg-blue-50'>04:00 PM - 06:00 PM</option>
              </select>
            </div>

            {/* No Of Person */}
            <div className='relative'>
              <label className='absolute -top-2 left-3 bg-white px-2 sm:px-5 text-[16px] sm:text-[18px] font-semibold text-gray-700 z-20'>
                No Of Person
              </label>
              <select 
                name='noOfPerson'
                value={formData.noOfPerson}
                onChange={handleInputChange}
                className='w-full h-[56px] sm:h-[70px] px-4 sm:px-8 py-3 border border-black rounded-[20px] focus:outline-none focus:border-blue-400 bg-white appearance-none cursor-pointer text-black'
              >
                <option value="1" className='bg-white text-black hover:bg-blue-50'>1</option>
                <option value="2" className='bg-white text-black hover:bg-blue-50'>2</option>
                <option value="3" className='bg-white text-black hover:bg-blue-50'>3</option>
                <option value="4" className='bg-white text-black hover:bg-blue-50'>4</option>
              </select>
            </div>

            {/* Phone Number Note */}
            <p className='text-[12px] sm:text-[16px] text-gray-500'>
              Please enter a valid Bali number (e.g 081234567890)
            </p>

            {/* Submit Button */}
            <button 
              type='submit'
              disabled={isSubmitting}
              className={`w-full h-[56px] sm:h-[70px] text-white text-[16px] sm:text-[18px] font-medium py-3 sm:py-4 rounded-[40px] transition-colors flex items-center justify-center gap-2 ${
                isSubmitting 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-[#FF8000] hover:bg-[#e6720a]'
              }`}
            >
              {isSubmitting ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Submitting...
                </>
              ) : (
                'Submit'
              )}
            </button>
          </form>

          {/* Close Button */}
          <button 
            onClick={handleCloseModal}
            className='absolute top-3 sm:top-5 right-3 sm:right-6 text-gray-500 hover:text-white hover:bg-[#FF8000] w-[30px] h-[30px] sm:w-[35px] sm:h-[35px] rounded-full transition-colors duration-200 flex items-center justify-center text-[16px] sm:text-xl'
          >
            ✕
          </button>
        </div>
      </div>
    )}
      
      <ToastContainer />
    </div>
  )
}

export default ServiceItems