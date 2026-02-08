/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    container: {
      center: true,
      padding: {
        DEFAULT: "40px",
      },
    },

    extend: {
      screens: {
        sm: "600px",
        md: "780px",
        lg: "1024px",
        xl: "1280px",
        "2xl": "1440",
      },
      colors: {
        primary: "#0169E4",
        white: "#ffffff",
        secondarywhite: "#F7F8F9",
        light: "#f6f8f9",
        grey: "#616161",
        darkgrey: "#272626",
        lightgrey: "#6B6B6B",
        neutral: "#191D23",
        lightneutral: "#64748B",
        black: "#000000",
        secondaryblack: "#35332F",
        danger: "#FF0000",
      },

      backgroundImage: {
        "primary-gradient": "linear-gradient(90deg, #0C5B22 0%, #308748 100%)",
        "secondary-gradient":
          "linear-gradient(180deg, #0963ED 0%, #0B97EE 100%)",
        "light-green-gradient":
          "linear-gradient(180deg, #10E933 0%, #1AD4AE 100%)",
        "purple-gradient": "linear-gradient(180deg, #B710F6 0%, #931BE8 100%)",
        "orange-gradient": "linear-gradient(180deg, #ED8612 0%, #FE7E59 100%)",
        "primary-background":
          "linear-gradient(97deg, #fff 26.64%, rgba(242, 244, 246, 0) 94.3%)",
        "gradient-to-r": "linear-gradient(90deg, #3579F6 0%, #1F4790 100%)",
      },

      boxShadow: {
        "primary-shadow": "0px 0px 45px 19px rgba(0, 0, 0, 0.03)",
        "secondary-shadow": "0px 3.353px 8.382px 0px rgba(0, 0, 0, 0.10);",
        "red-shadow": "0px 10px 23px 0px rgba(245, 66, 69, 0.50);",
        "blue-shadow": "0px 10px 23px 0px rgba(26, 143, 251, 0.50);",
        "green-shadow": "0px 10px 23px 0px rgba(42, 187, 82, 0.50)",
        "purple-shadow": "0px 10px 23px 0px rgba(178, 61, 248, 0.50);",
        "yellow-shadow": "0px 10px 23px 0px rgba(243, 208, 24, 0.50);",
        "orange-shadow": "0px 10px 23px 0px rgba(243, 103, 24, 0.50)",
      },
    

      filter: {
        invert: "invert(1)",
        "brightness-0": "brightness(0)",
      },
      transitionProperty: {
        filter: "filter",
      },
    },
    variants: {
      extend: {
        filter: ["hover"],
        brightness: ["hover"],
      },
    },
  },
  plugins: [],
};
