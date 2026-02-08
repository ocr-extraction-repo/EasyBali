import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import balilogo from '../../../../assets/images/balilogo.svg'
import secondlogo from '../../../../assets/images/secondlogo.svg'
import bottomRightPng from '../../../../assets/images/right-bottom.png'
import topLeftPng from '../../../../assets/images/top-left.png'
import Footer from '../../../layout/footer'

const ContactUs = () => {
  const navigate = useNavigate();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className='bg-white  flex flex-col background-class relative'> 
      <img src={topLeftPng} alt="Top Left Icon" className="absolute top-[0px] left-[0px] sm:left-[0px] md:left-[0px] w-[350px] sm:w-[200px] md:w-[400px] opacity-60 z-0" />
      <img src={bottomRightPng} alt="Bottom Right Icon" className="absolute bottom-0 right-0 w-[300px] sm:w-[250px] md:w-[450px] opacity-60 z-0" />
    

      <div className='relative z-10'>
        <div className='flex items-center justify-between px-[24px] lg:px-[100px] py-[24px] lg:py-[40px]'>
          <img src={balilogo} alt='Bali' onClick={() => navigate('/')} className='cursor-pointer h-[30px] lg:h-auto' />
          <img src={secondlogo} alt='Second Logo' className='w-[62px] h-[32px] lg:h-[40px] cursor-pointer'/>
        </div>
      </div>

      <div className='relative z-10 flex-1 px-[24px] lg:px-[100px] pb-[40px] lg:pb-[60px]'>
        <div className='max-w-[1200px] mx-auto'>
       
          <div className='text-center mb-[40px] lg:mb-[60px]'>
            <h1 className='text-[32px] sm:text-[40px] lg:text-[48px] font-bold text-[#FF8000] mb-[16px]'>
              Contact Us
            </h1>
            <div className='w-[80px] h-[4px] bg-[#FF8000] mx-auto rounded-full'></div>
          </div>

   
          <div className='bg-white rounded-[30px] shadow-[0_8px_30px_rgba(0,0,0,0.12)] p-[24px] sm:p-[40px] lg:p-[60px]'>
            
        
            <div className='text-center mb-[40px] sm:mb-[50px]'>
              <p className='text-[16px] sm:text-[18px] lg:text-[20px] text-[#555] leading-relaxed max-w-[800px] mx-auto'>
                We'd love to hear from you! Whether you have a question, feedback, or just want to say hello, feel free to reach out to us through any of the methods below.
              </p>
            </div>

       
            <div className='grid grid-cols-1 md:grid-cols-2 gap-[24px] lg:gap-[32px] mb-[40px] sm:mb-[50px]'>
              
      
              <div className='bg-gradient-to-br from-[#FF8000] to-[#FF9933] rounded-[24px] p-[24px] sm:p-[32px] text-white shadow-lg hover:shadow-xl transition-shadow duration-300'>
                <div className='flex items-start gap-[16px]'>
                  <div className='text-[40px] sm:text-[48px]'>📧</div>
                  <div className='flex-1'>
                    <h3 className='text-[20px] sm:text-[24px] font-bold mb-[12px]'>Email</h3>
                    <p className='text-[14px] sm:text-[15px] mb-[12px] opacity-90'>For general inquiries and user support:</p>
                    <a href='mailto:info@easy-bali.com' className='text-[16px] sm:text-[18px] font-semibold hover:underline block break-all'>
                      info@easy-bali.com
                    </a>
                  </div>
                </div>
              </div>

      
              <div className='bg-gradient-to-br from-[#4169E1] to-[#5B7FE8] rounded-[24px] p-[24px] sm:p-[32px] text-white shadow-lg hover:shadow-xl transition-shadow duration-300'>
                <div className='flex items-start gap-[16px]'>
                  <div className='text-[40px] sm:text-[48px]'>📞</div>
                  <div className='flex-1'>
                    <h3 className='text-[20px] sm:text-[24px] font-bold mb-[12px]'>Phone</h3>
                    <p className='text-[14px] sm:text-[15px] mb-[8px] opacity-90'>Call us at:</p>
                    <a href='tel:+6281999281660' className='text-[18px] sm:text-[20px] font-semibold hover:underline block mb-[12px]'>
                      +62 81 999 281 660
                    </a>
                    <p className='text-[13px] sm:text-[14px] opacity-90'>Monday – Friday, 9:00 AM – 5:00 PM</p>
                    <p className='text-[13px] sm:text-[14px] opacity-90'>(Bali Time/GMT +8)</p>
                  </div>
                </div>
              </div>

            </div>

            <div className='mb-[40px] sm:mb-[50px]'>
              <div className='bg-[#FFF5EB] border-l-4 border-[#FF8000] rounded-[20px] p-[24px] sm:p-[32px]'>
                <div className='flex items-start gap-[16px]'>
                  <div className='text-[40px] sm:text-[48px]'>🏢</div>
                  <div className='flex-1'>
                    <h3 className='text-[24px] sm:text-[28px] font-bold text-[#FF8000] mb-[16px]'>Address</h3>
                    <div className='text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed space-y-[4px]'>
                      <p className='font-semibold'>Jimbaran Hub, J-Loft 1F</p>
                      <p>Jl Karang Mas Jimbaran</p>
                      <p>Badung, Bali, 80361</p>
                      <p className='font-semibold'>Indonesia</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

         
            <div className='text-center'>
              <h3 className='text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[20px]'>
                Follow Us
              </h3>
              <p className='text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] mb-[24px]'>
                Stay connected on social media:
              </p>
              
              <div className='flex justify-center items-center gap-[20px] sm:gap-[32px]'>
            
                <a 
                  href='https://www.facebook.com/profile.php?id=61570896083765#' 
                  target='_blank' 
                  rel='noopener noreferrer'
                  className='group flex flex-col items-center gap-[8px] transition-transform duration-300 hover:scale-110'
                >
                  <div className='w-[60px] h-[60px] sm:w-[80px] sm:h-[80px] rounded-full bg-gradient-to-br from-[#1877F2] to-[#0C63D4] flex items-center justify-center shadow-lg group-hover:shadow-xl transition-shadow duration-300'>
                    <svg className='w-[30px] h-[30px] sm:w-[40px] sm:h-[40px] text-white' fill='currentColor' viewBox='0 0 24 24'>
                      <path d='M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z'/>
                    </svg>
                  </div>
                  <span className='text-[14px] sm:text-[16px] font-semibold text-[#333] group-hover:text-[#FF8000] transition-colors duration-300'>Facebook</span>
                </a>

                <a 
                  href='https://www.instagram.com/easybaliforyou/' 
                  target='_blank' 
                  rel='noopener noreferrer'
                  className='group flex flex-col items-center gap-[8px] transition-transform duration-300 hover:scale-110'
                >
                  <div className='w-[60px] h-[60px] sm:w-[80px] sm:h-[80px] rounded-full bg-gradient-to-br from-[#E1306C] via-[#C13584] to-[#833AB4] flex items-center justify-center shadow-lg group-hover:shadow-xl transition-shadow duration-300'>
                    <svg className='w-[30px] h-[30px] sm:w-[40px] sm:h-[40px] text-white' fill='currentColor' viewBox='0 0 24 24'>
                      <path d='M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06l.045.03zm0 3.678c-3.405 0-6.162 2.76-6.162 6.162 0 3.405 2.76 6.162 6.162 6.162 3.405 0 6.162-2.76 6.162-6.162 0-3.405-2.76-6.162-6.162-6.162zM12 16c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm7.846-10.405c0 .795-.646 1.44-1.44 1.44-.795 0-1.44-.646-1.44-1.44 0-.794.646-1.439 1.44-1.439.793-.001 1.44.645 1.44 1.439z'/>
                    </svg>
                  </div>
                  <span className='text-[14px] sm:text-[16px] font-semibold text-[#333] group-hover:text-[#FF8000] transition-colors duration-300'>Instagram</span>
                </a>
              </div>
            </div>

          
            <div className='mt-[50px] text-center'>
              <div className='inline-block bg-gradient-to-r from-[#FFF5EB] to-[#FFE8CC] rounded-[20px] px-[24px] sm:px-[40px] py-[16px] sm:py-[20px] border-2 border-[#FF8000]'>
                <p className='text-[14px] sm:text-[15px] lg:text-[16px] text-white font-medium'>
                  💬 We look forward to hearing from you!
                </p>
              </div>
            </div>

          </div>
        </div>
      </div>


             <Footer />
      
    </div>
  )
}

export default ContactUs