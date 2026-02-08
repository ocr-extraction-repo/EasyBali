import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import balilogo from "../../../assets/images/balilogo.svg";
import secondlogo from "../../../assets/images/secondlogo.svg";
import bottomRightPng from "../../../assets/images/right-bottom.png";
import topLeftPng from "../../../assets/images/top-left.png";
import Footer from "../../layout/footer";

const TermsConditons = () => {
  const navigate = useNavigate();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="bg-white min-h-screen flex flex-col background-class relative">
      <img
        src={topLeftPng}
        alt="Top Left Icon"
        className="absolute top-[0px] left-[0px] sm:left-[0px] md:left-[0px] w-[350px] sm:w-[200px] md:w-[400px] opacity-60 z-0"
      />
      <img
        src={bottomRightPng}
        alt="Bottom Right Icon"
        className="absolute bottom-0 right-0 w-[300px] sm:w-[250px] md:w-[450px] opacity-60 z-0"
      />

      <div className="relative z-10">
        <div className="flex items-center justify-between px-[24px] lg:px-[100px] py-[24px] lg:py-[40px]">
          <img
            src={balilogo}
            alt="Bali"
            onClick={() => navigate("/")}
            className="cursor-pointer h-[30px] lg:h-auto"
          />
          <img
            src={secondlogo}
            alt="Second Logo"
            className="w-[62px] h-[32px] lg:h-[40px] cursor-pointer"
          />
        </div>
      </div>

      <div className="relative z-10 flex-1 px-[24px] lg:px-[100px] pb-[40px] lg:pb-[60px]">
        <div className="max-w-[1200px] mx-auto">
          <div className="text-center mb-[40px] lg:mb-[60px]">
            <h1 className="text-[32px] sm:text-[40px] lg:text-[48px] font-bold text-[#FF8000] mb-[16px]">
              Terms & Conditions
            </h1>
            <div className="w-[80px] h-[4px] bg-[#FF8000] mx-auto rounded-full"></div>
          </div>

          <div className="bg-white rounded-[30px] shadow-[0_8px_30px_rgba(0,0,0,0.12)] p-[24px] sm:p-[40px] lg:p-[60px]">
            <section className="mb-[40px]">
              {/* <h2 className='text-[28px] sm:text-[32px] lg:text-[36px] font-bold text-[#FF8000] mb-[24px] text-center'>
                1. Terms and Conditions for Users
              </h2> */}

              <div className="mb-[32px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.1</span> Introduction
                </h3>
                <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                  Welcome to EASYBali! These Terms and Conditions ("Terms")
                  govern your use of our platform. By accessing and using
                  EASYBali, you agree to comply with these Terms. Please read
                  them carefully before using our services.
                </p>
              </div>

              <div className="mb-[32px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.2</span> Definitions
                </h3>
                <div className="space-y-[12px]">
                  <div className="bg-[#FFF5EB] rounded-[20px] p-[16px] sm:p-[20px]">
                    <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                      <strong className="text-[#FF8000]">"User"</strong> – Any
                      individual who accesses or uses EASYBali's platform,
                      including guests staying in partnered villas and others
                      utilizing our services.
                    </p>
                  </div>
                  <div className="bg-[#FFF5EB] rounded-[20px] p-[16px] sm:p-[20px]">
                    <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                      <strong className="text-[#FF8000]">"Platform"</strong> –
                      EASYBali's services provided via website, WhatsApp,
                      Messenger, and Instagram DM.
                    </p>
                  </div>
                  <div className="bg-[#FFF5EB] rounded-[20px] p-[16px] sm:p-[20px]">
                    <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                      <strong className="text-[#FF8000]">
                        "Service Providers"
                      </strong>{" "}
                      – Third-party vendors offering hospitality-related
                      services through EASYBali.
                    </p>
                  </div>
                  <div className="bg-[#FFF5EB] rounded-[20px] p-[16px] sm:p-[20px]">
                    <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                      <strong className="text-[#FF8000]">"Host"</strong> –
                      Property owners or managers using EASYBali's services to
                      facilitate villa operations.
                    </p>
                  </div>
                </div>
              </div>

              <div className="mb-[32px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.3</span> Service Overview
                </h3>
                <div className="bg-[#FFF5EB] border-l-4 border-[#FF8000] rounded-[16px] p-[20px] sm:p-[24px] mb-[20px]">
                  <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[16px]">
                    EASYBali is a hospitality service facilitator connecting
                    Users with third-party Service Providers and Hosts. EASYBali
                    does not directly provide any hospitality services and is
                    not responsible for service quality, fulfillment, or any
                    liabilities arising from third-party providers or Hosts. Our
                    role is strictly to facilitate interactions between Users,
                    Service Providers, and Hosts.
                  </p>
                </div>
                <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[16px]">
                  We facilitate access to hospitality-related services, such as:
                </p>
                <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px] mb-[16px]">
                  <li>
                    <strong>Service Booking:</strong> Reserve wellness
                    treatments, transportation, dining, and more.
                  </li>
                  <li>
                    <strong>AI Concierge:</strong> Receive personalized travel
                    support and recommendations.
                  </li>
                  <li>
                    <strong>Passport Submission:</strong> Assist Hosts in
                    collecting necessary guest passport details.
                  </li>
                  <li>
                    <strong>Feedback Management:</strong> Provide service and
                    stay reviews to enhance quality.
                  </li>
                  <li>
                    <strong>Maintenance Requests:</strong> Report issues or
                    request amenities seamlessly.
                  </li>
                  <li>
                    <strong>Host Information:</strong> Access villa guidelines
                    and check-in/check-out procedures.
                  </li>
                  <li>
                    <strong>Travel Tools:</strong> Utilize currency converters,
                    voice translators, and event calendars.
                  </li>
                  <li>
                    <strong>Exclusive Offers:</strong> Benefit from special
                    promotions and deals.
                  </li>
                </ul>
                <p className="text-[14px] sm:text-[15px] lg:text-[16px] text-[#666] italic">
                  EASYBali does not guarantee the quality, availability, or
                  fulfillment of services provided by third-party providers or
                  Hosts. Users acknowledge that engagement with Service
                  Providers and Hosts is at their own discretion and risk.
                </p>
              </div>

              <div className="mb-[32px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.4</span> Payments and Fees
                </h3>
                <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                  <li>
                    Payments for services booked through EASYBali are processed
                    via a secure payment gateway.
                  </li>
                  <li>
                    All pricing is determined by Service Providers, and Users
                    are responsible for reviewing the service terms before
                    booking.
                  </li>
                </ul>
              </div>

              <div className="mb-[32px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.5</span> User Conduct and
                  Responsibilities
                </h3>
                <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                  <li>
                    Users must provide accurate information and comply with
                    local regulations.
                  </li>
                  <li>
                    EASYBali is not responsible for any damages, disputes, or
                    misunderstandings between Users and Service Providers and
                    Hosts.
                  </li>
                  <li>
                    Refrain from using EASYBali for unlawful activities or
                    misrepresenting service requests.
                  </li>
                  <li>
                    Provide accurate personal and payment information when
                    booking services.
                  </li>
                  <li>
                    Comply with local regulations and villa policies when using
                    services facilitated through EASYBali.
                  </li>
                  <li>Respect Service Providers, Hosts, and other Users.</li>
                </ul>
              </div>

              <div className="mb-[32px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.6</span> Cancellations &
                  Refunds Policy
                </h3>

                <div className="space-y-[24px]">
                  <div>
                    <h4 className="text-[18px] sm:text-[20px] lg:text-[22px] font-semibold text-[#FF8000] mb-[12px]">
                      User-Initiated Cancellations (Ordering Services):
                    </h4>
                    <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                      <li>
                        Users cannot receive a refund once a booking is
                        confirmed, regardless of when they cancel.
                      </li>
                      <li>
                        Users may request a reschedule, but this is subject to
                        the Service Provider's availability.
                      </li>
                      <li>
                        EASYBali does not guarantee rescheduling for
                        cancellations made by Users.
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h4 className="text-[18px] sm:text-[20px] lg:text-[22px] font-semibold text-[#FF8000] mb-[12px]">
                      Service Provider Failures or Disruptions:
                    </h4>
                    <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                      <li>
                        If a Service Provider fails to deliver the agreed-upon
                        service, provides inadequate service, or breaches
                        service expectations, Users must promptly report the
                        issue through the EASYBali email or phone number.
                      </li>
                      <li>
                        If a Service Provider fails to show up without prior
                        notice, EASYBali may temporarily suspend or permanently
                        remove the Service Provider from the platform.
                      </li>
                      <li>
                        EASYBali will review the case and determine refund
                        eligibility at its discretion.
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h4 className="text-[18px] sm:text-[20px] lg:text-[22px] font-semibold text-[#FF8000] mb-[12px]">
                      EASYBali's Role & Liability:
                    </h4>
                    <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                      <li>
                        EASYBali acts solely as a facilitator and does not
                        directly provide services.
                      </li>
                      <li>
                        EASYBali is not liable for any losses, damages, or
                        inconveniences caused by Service Provider failures but
                        will assist in dispute resolution where appropriate.
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h4 className="text-[18px] sm:text-[20px] lg:text-[22px] font-semibold text-[#FF8000] mb-[12px]">
                      Dispute Resolution Process:
                    </h4>
                    <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                      <li>
                        EASYBali will conduct an internal review of disputes and
                        determine an appropriate course of action.
                      </li>
                      <li>
                        In cases where a Service Provider is found to be at
                        fault, EASYBali will work to facilitate a fair
                        resolution.
                      </li>
                      <li>
                        EASYBali reserves the right to decline refund requests
                        if sufficient evidence of service failure is not
                        provided.
                      </li>
                      <li>
                        Any refund or compensation provided by EASYBali is at
                        its sole discretion and does not establish a precedent
                        for future claims.
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h4 className="text-[18px] sm:text-[20px] lg:text-[22px] font-semibold text-[#FF8000] mb-[12px]">
                      Final Decision Authority:
                    </h4>
                    <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                      <li>
                        EASYBali has the final authority in determining
                        eligibility for refunds, rebookings, or credits.
                      </li>
                      <li>
                        Users agree that EASYBali's resolution of any dispute
                        shall be final and binding.
                      </li>
                    </ul>
                  </div>
                </div>

                <div className="mt-[16px] bg-[#FFF5EB] rounded-[16px] p-[16px] sm:p-[20px]">
                  <p className="text-[14px] sm:text-[15px] lg:text-[16px] text-[#555] italic">
                    By using EASYBali, Users acknowledge and accept these
                    cancellation and refund terms.
                  </p>
                </div>
              </div>

              <div className="mb-[32px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.7</span> Passport
                  Submission Facilitation
                </h3>
                <div className="bg-gradient-to-r from-[#4169E1] to-[#5B7FE8] rounded-[20px] p-[20px] sm:p-[30px]">
                  <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-white leading-relaxed ml-[12px]">
                    <li>
                      EASYBali provides a passport submission tool to help Hosts
                      request passport details from their guests as required by
                      local regulations.
                    </li>
                    <li>
                      EASYBali does not process, store, or take responsibility
                      for passport data beyond facilitating the submission
                      process.
                    </li>
                    <li>
                      Any misuse or mishandling of passport information is the
                      sole responsibility of the Host.
                    </li>
                  </ul>
                </div>
              </div>

              <div className="mb-[32px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.8</span> Limitation of
                  Liability
                </h3>
                <div className="border-2 border-[#FF8000] rounded-[20px] p-[20px] sm:p-[24px]">
                  <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                    <li>
                      EASYBali is not responsible for service failures, losses,
                      damages, or disputes between Users and Service Providers
                      or Hosts.
                    </li>
                    <li>
                      EASYBali does not endorse or verify Service Providers
                      beyond basic vetting.
                    </li>
                    <li>
                      EASYBali is not liable for any failures, non-performance,
                      or damages resulting from service interactions between
                      Users and Service Providers.
                    </li>
                    <li>
                      EASYBali does not guarantee availability, service
                      performance, or compliance of Service Providers or Hosts.
                    </li>
                    <li>
                      EASYBali is not liable for any indirect, incidental, or
                      consequential damages arising from platform use.
                    </li>
                  </ul>
                </div>
              </div>

              <div className="mb-[32px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.9</span> Amendments &
                  Updates
                </h3>
                <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                  <li>
                    EASYBali reserves the right to update these Terms at any
                    time.
                  </li>
                  <li>
                    Continued use of the platform after changes constitutes
                    acceptance of the revised Terms.
                  </li>
                </ul>
              </div>

              <div className="mb-[0px]">
                <h3 className="text-[20px] sm:text-[24px] lg:text-[28px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                  <span className="text-[#FF8000]">1.10</span> Contact
                  Information
                </h3>
                <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[20px]">
                  For any inquiries, please contact us at:
                </p>
                <div className="bg-gradient-to-r from-[#FF8000] to-[#FF9933] rounded-[20px] p-[24px] sm:p-[32px] text-white">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-around gap-[16px]">
                    <div className="flex items-center gap-[12px]">
                      <span className="text-[24px]">📧</span>
                      <div>
                        <p className="font-semibold text-[16px] sm:text-[18px]">
                          Email
                        </p>
                        <a
                          href="mailto:info@easy-bali.com"
                          className="text-[14px] sm:text-[15px] hover:underline"
                        >
                          info@easy-bali.com
                        </a>
                      </div>
                    </div>
                    <div className="flex items-center gap-[12px]">
                      <span className="text-[24px]">🌐</span>
                      <div>
                        <p className="font-semibold text-[16px] sm:text-[18px]">
                          Website
                        </p>
                        <a
                          href="https://www.easy-bali.com"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[14px] sm:text-[15px] hover:underline"
                        >
                          www.easy-bali.com
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <div className="mt-[40px] text-center">
              <div className="inline-block bg-[#FFF5EB] rounded-[20px] px-[24px] sm:px-[40px] py-[16px] sm:py-[20px]">
                <p className="text-[14px] sm:text-[15px] lg:text-[16px] text-[#555] italic">
                  By using EASYBali, you acknowledge and accept these Terms and
                  Conditions.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="h-[40px]">
        <Footer />
      </div>
    </div>
  );
};

export default TermsConditons;
