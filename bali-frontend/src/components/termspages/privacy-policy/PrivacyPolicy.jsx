import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import balilogo from "../../../assets/images/balilogo.svg";
import secondlogo from "../../../assets/images/secondlogo.svg";
import bottomRightPng from "../../../assets/images/right-bottom.png";
import topLeftPng from "../../../assets/images/top-left.png";
import Footer from "../../layout/footer";
const PrivacyPolicy = () => {
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
              Privacy Policy
            </h1>
            <div className="w-[80px] h-[4px] bg-[#FF8000] mx-auto rounded-full"></div>
          </div>

          <div className="bg-white rounded-[30px] shadow-[0_8px_30px_rgba(0,0,0,0.12)] p-[24px] sm:p-[40px] lg:p-[60px]">
            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">1.</span> Introduction
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                EASY Bali ("we," "us," or "our") is committed to protecting your
                privacy. This Privacy Policy outlines how we collect, use,
                disclose, and protect the personal data of users ("Users,"
                "you") who interact with our platform through our website,
                WhatsApp, Messenger, and Instagram DM. By using EASY Bali, you
                consent to the practices described in this Privacy Policy.
              </p>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">2.</span> Definitions
              </h2>
              <div className="space-y-[12px]">
                <div className="bg-[#FFF5EB] rounded-[20px] p-[16px] sm:p-[20px]">
                  <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                    <strong className="text-[#FF8000]">"Personal Data"</strong>{" "}
                    – Any information related to an identifiable individual,
                    such as name, and contact details.
                  </p>
                </div>
                <div className="bg-[#FFF5EB] rounded-[20px] p-[16px] sm:p-[20px]">
                  <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                    <strong className="text-[#FF8000]">"Processing"</strong> –
                    Any action performed on Personal Data, including collection,
                    storage, use, or sharing.
                  </p>
                </div>
                <div className="bg-[#FFF5EB] rounded-[20px] p-[16px] sm:p-[20px]">
                  <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                    <strong className="text-[#FF8000]">
                      "Data Controller"
                    </strong>{" "}
                    – EASY Bali, responsible for determining the purposes of
                    data processing.
                  </p>
                </div>
                <div className="bg-[#FFF5EB] rounded-[20px] p-[16px] sm:p-[20px]">
                  <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                    <strong className="text-[#FF8000]">
                      "Service Provider"
                    </strong>{" "}
                    – Third-party vendors offering hospitality services through
                    EASY Bali.
                  </p>
                </div>
              </div>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">3.</span> Information We
                Collect
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[20px]">
                We collect different types of Personal Data, including:
              </p>

              <div className="space-y-[24px]">
                <div>
                  <h3 className="text-[18px] sm:text-[20px] lg:text-[24px] font-semibold text-[#FF8000] mb-[12px]">
                    3.1 Information You Provide Directly
                  </h3>
                  <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                    <li>
                      Name, email address, and phone number when you register or
                      contact us.
                    </li>
                    <li>
                      Preferences and special requests related to hospitality
                      services.
                    </li>
                    <li>
                      Passport details (when submitted for host verification
                      purposes).
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-[18px] sm:text-[20px] lg:text-[24px] font-semibold text-[#FF8000] mb-[12px]">
                    3.2 Information Collected Automatically
                  </h3>
                  <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                    <li>
                      Device and browser information (IP address, operating
                      system, device type).
                    </li>
                    <li>
                      Usage data, such as pages visited, chat interactions, and
                      service requests.
                    </li>
                    <li>
                      Cookies and similar technologies (refer to Section 9:
                      Cookies & Tracking Technologies).
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-[18px] sm:text-[20px] lg:text-[24px] font-semibold text-[#FF8000] mb-[12px]">
                    3.3 Information from Third Parties
                  </h3>
                  <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                    <li>
                      Data from integrated third-party platforms (e.g., social
                      media, messaging apps).
                    </li>
                    <li>
                      Information received from Service Providers regarding
                      service fulfillment.
                    </li>
                  </ul>
                </div>
              </div>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">4.</span> How We Use Your
                Information
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[20px]">
                EASY Bali processes Personal Data for the following purposes:
              </p>
              <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                <li>
                  To facilitate bookings and transactions between Users and
                  Service Providers.
                </li>
                <li>To provide customer support and service updates.</li>
                <li>
                  To personalize recommendations and improve user experience.
                </li>
                <li>
                  To ensure compliance with local laws (e.g., passport
                  submission for hosts).
                </li>
                <li>
                  To conduct marketing campaigns and promotions (with user
                  consent).
                </li>
                <li>To prevent fraud and enhance security.</li>
              </ul>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">5.</span> Legal Basis for
                Processing Personal Data
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[20px]">
                We process Personal Data under the following legal grounds:
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-[16px]">
                <div className="border-l-4 border-[#FF8000] bg-[#FFF5EB] rounded-[12px] p-[16px] sm:p-[20px]">
                  <h4 className="font-semibold text-[#FF8000] mb-[8px] text-[16px] sm:text-[18px]">
                    Consent
                  </h4>
                  <p className="text-[14px] sm:text-[15px] text-[#555]">
                    When you provide explicit permission for marketing
                    communications.
                  </p>
                </div>
                <div className="border-l-4 border-[#FF8000] bg-[#FFF5EB] rounded-[12px] p-[16px] sm:p-[20px]">
                  <h4 className="font-semibold text-[#FF8000] mb-[8px] text-[16px] sm:text-[18px]">
                    Contractual Obligation
                  </h4>
                  <p className="text-[14px] sm:text-[15px] text-[#555]">
                    When data is necessary to fulfill a service you requested.
                  </p>
                </div>
                <div className="border-l-4 border-[#FF8000] bg-[#FFF5EB] rounded-[12px] p-[16px] sm:p-[20px]">
                  <h4 className="font-semibold text-[#FF8000] mb-[8px] text-[16px] sm:text-[18px]">
                    Legal Compliance
                  </h4>
                  <p className="text-[14px] sm:text-[15px] text-[#555]">
                    When required by local regulations (e.g., passport
                    verification for hosts).
                  </p>
                </div>
                <div className="border-l-4 border-[#FF8000] bg-[#FFF5EB] rounded-[12px] p-[16px] sm:p-[20px]">
                  <h4 className="font-semibold text-[#FF8000] mb-[8px] text-[16px] sm:text-[18px]">
                    Legitimate Interest
                  </h4>
                  <p className="text-[14px] sm:text-[15px] text-[#555]">
                    When processing improves our services without overriding
                    your rights.
                  </p>
                </div>
              </div>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">6.</span> Data Sharing and
                Disclosure
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[20px]">
                EASY Bali does not sell your Personal Data. However, we may
                share data in the following circumstances:
              </p>

              <div className="space-y-[24px]">
                <div>
                  <h3 className="text-[18px] sm:text-[20px] lg:text-[24px] font-semibold text-[#FF8000] mb-[12px]">
                    6.1 With Service Providers
                  </h3>
                  <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                    <li>
                      To fulfill requested services (e.g., sharing guest
                      information with massage or transport providers, etc).
                    </li>
                    <li>
                      To facilitate passport verification required by local
                      laws.
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-[18px] sm:text-[20px] lg:text-[24px] font-semibold text-[#FF8000] mb-[12px]">
                    6.2 With Third-Party Partners
                  </h3>
                  <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                    <li>Payment processors to handle transactions securely.</li>
                    <li>
                      IT service providers for technical infrastructure and
                      support.
                    </li>
                    <li>
                      Marketing and analytics tools for performance tracking
                      (only non-identifiable data).
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-[18px] sm:text-[20px] lg:text-[24px] font-semibold text-[#FF8000] mb-[12px]">
                    6.3 Legal Compliance & Security
                  </h3>
                  <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                    <li>
                      If required by law, such as regulatory authorities
                      requesting passport data.
                    </li>
                    <li>
                      In case of disputes or legal proceedings involving a User
                      or Service Provider.
                    </li>
                    <li>
                      To protect the security and integrity of EASY Bali and its
                      Users.
                    </li>
                  </ul>
                </div>
              </div>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">7.</span> Data Retention
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[20px]">
                We retain Personal Data only as long as necessary:
              </p>
              <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed ml-[12px]">
                <li>
                  Marketing preferences are stored until the User opts out.
                </li>
                <li>
                  Passport submission data is not stored by EASY Bali beyond
                  host verification facilitation.
                </li>
                <li>
                  When no longer needed, data is securely deleted or anonymized.
                </li>
              </ul>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">8.</span> Data Security
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[20px]">
                EASY Bali implements strict security measures:
              </p>
              <div className="bg-gradient-to-r from-[#4169E1] to-[#5B7FE8] rounded-[20px] p-[20px] sm:p-[30px] mb-[16px]">
                <ul className="list-disc list-inside space-y-[8px] text-[15px] sm:text-[16px] lg:text-[18px] text-white leading-relaxed ml-[12px]">
                  <li>Encryption to protect payment details.</li>
                  <li>
                    Access control limiting employee access to sensitive data.
                  </li>
                  <li>
                    Secure servers and firewalls to prevent unauthorized
                    breaches.
                  </li>
                </ul>
              </div>
              <p className="text-[14px] sm:text-[15px] lg:text-[16px] text-[#666] italic">
                While we take strong precautions, no system is 100% secure.
                Users are responsible for safeguarding their login credentials.
              </p>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">9.</span> Cookies & Tracking
                Technologies
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[20px]">
                EASY Bali uses cookies and similar tools to enhance user
                experience:
              </p>
              <div className="space-y-[12px]">
                <div className="flex items-start gap-[12px] bg-white border-2 border-[#FF8000] rounded-[16px] p-[16px] sm:p-[20px]">
                  <span className="text-[24px]">🍪</span>
                  <div>
                    <h4 className="font-semibold text-[#FF8000] mb-[4px] text-[16px] sm:text-[18px]">
                      Essential Cookies
                    </h4>
                    <p className="text-[14px] sm:text-[15px] text-[#555]">
                      Necessary for platform functionality.
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-[12px] bg-white border-2 border-[#FF8000] rounded-[16px] p-[16px] sm:p-[20px]">
                  <span className="text-[24px]">📊</span>
                  <div>
                    <h4 className="font-semibold text-[#FF8000] mb-[4px] text-[16px] sm:text-[18px]">
                      Performance Cookies
                    </h4>
                    <p className="text-[14px] sm:text-[15px] text-[#555]">
                      Help improve website and service performance.
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-[12px] bg-white border-2 border-[#FF8000] rounded-[16px] p-[16px] sm:p-[20px]">
                  <span className="text-[24px]">📢</span>
                  <div>
                    <h4 className="font-semibold text-[#FF8000] mb-[4px] text-[16px] sm:text-[18px]">
                      Marketing Cookies
                    </h4>
                    <p className="text-[14px] sm:text-[15px] text-[#555]">
                      Used for personalized advertisements (only with user
                      consent).
                    </p>
                  </div>
                </div>
              </div>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">10.</span> Children's Privacy
              </h2>
              <div className="bg-[#FFF5EB] border-l-4 border-[#FF8000] rounded-[16px] p-[20px] sm:p-[24px]">
                <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                  EASY Bali does not knowingly collect data from children under
                  16. If a parent/guardian believes a child's data has been
                  collected, they should contact us immediately.
                </p>
              </div>
            </section>

            <section className="mb-[40px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">11.</span> Policy Updates
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed">
                We may update this Privacy Policy periodically.
              </p>
            </section>

            <section className="mb-[0px]">
              <h2 className="text-[24px] sm:text-[28px] lg:text-[32px] font-bold text-[#333] mb-[16px] flex items-center gap-[12px]">
                <span className="text-[#FF8000]">12.</span> Contact Information
              </h2>
              <p className="text-[15px] sm:text-[16px] lg:text-[18px] text-[#555] leading-relaxed mb-[20px]">
                For privacy-related inquiries, please contact:
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
            </section>

            <div className="mt-[40px] text-center">
              <div className="inline-block bg-[#FFF5EB] rounded-[20px] px-[24px] sm:px-[40px] py-[16px] sm:py-[20px]">
                <p className="text-[14px] sm:text-[15px] lg:text-[16px] text-[#555] italic">
                  By using EASY Bali, you acknowledge and accept this Privacy
                  Policy.
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

export default PrivacyPolicy;
