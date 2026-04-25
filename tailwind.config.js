/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./docs/**/*.html', './docs/**/*.js'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
        },
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(96,165,250,0.2), 0 10px 30px rgba(30,41,59,0.35)',
      },
    },
  },
  plugins: [],
};
