/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          800: '#0F172A',
          900: '#090D16',
          950: '#030712',
        },
        medical: {
          teal: '#06B6D4',
          blue: '#2563EB',
        }
      }
    },
  },
  plugins: [],
}
