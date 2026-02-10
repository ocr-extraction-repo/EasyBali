import { Outlet, RouterProvider, createBrowserRouter } from "react-router-dom";
import NotFound from "./page/notFound";
import Login from "./page/account/login";
import ResetPassword from "./page/account/resetPassword";
import Verify from "./page/account/verify";
import Forget from "./page/account/forget";
import Register from "./page/account/register";
import Components from "./components/components";
import Home from "./page/home";
import Chat from "./components/chatbot/chat";
import TripServices from "./components/services/Categories";
import SubCategories from "./components/services/Subcategories"
import ServiceItems from "./components/services/serviceItems";
import PrivacyPolicy from "./components/termspages/privacy-policy/PrivacyPolicy";
import TermsConditons from "./components/termspages/terms-conditions/TermsConditons";
import ContactUs from "./components/termspages/privacy-policy/contact-us/ContactUs";
import PlanMyTrip from "./pages/tools/PlanMyTrip";
import CurrencyConverter from "./pages/tools/CurrencyConverter";
import VoiceTranslator from "./pages/tools/VoiceTranslator";
import WhatToDoToday from "./pages/tools/WhatToDoToday";
import GeneralChat from "./pages/tools/GeneralChat";
const AppLayout = () => {
  return (
    <>
      <RouterProvider router={appRouter} />
    </>
  );
};

const appRouter = createBrowserRouter([
  {
    path: "*",
    element: <NotFound />,
  },
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/categories",
    element: <TripServices />
  },
  {
    path: "/subcategories",
    element: <SubCategories />
  },
  {
    path: "/serviceitems",
    element: <ServiceItems />
  },
  {
    path: "/privacy-policy",
    element: <PrivacyPolicy />
  },
  {
    path: "/terms-and-conditions",
    element: <TermsConditons />
  },
  {
    path: "/contact-us",
    element: <ContactUs />
  },
  {
    path: "/chatbot",
    element: <GeneralChat />,
  },
  {
    path: "/tools/plan-my-trip",
    element: <PlanMyTrip />,
  },
  {
    path: "/tools/currency-converter",
    element: <CurrencyConverter />,
  },
  {
    path: "/tools/voice-translator",
    element: <VoiceTranslator />,
  },
  {
    path: "/tools/what-to-do-today",
    element: <WhatToDoToday />,
  },

  // {
  //   path: "/",
  //   element: <Dashboard />,
  //   children: [
  //     {
  //       path: "/dashboard",
  //       element: <Dashboardoutlet />,
  //       children: [
  //         {
  //           path: "/dashboard",
  //           element: <Dashboardmain />,
  //         },
  //       ],
  //     },
  //   ],
  // },
]);
export default AppLayout;
