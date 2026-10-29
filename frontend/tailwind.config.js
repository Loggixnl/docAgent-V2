/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        limeGreen: '#7FB800',
        lightTeal: '#57A3AF',
        darkTeal: '#41808B',
        coralOrange: '#F46036',
        lightGrey: '#E5ECE9',
        bgBase: '#E5ECE9',
        textMain: '#0F172A',
        textMuted: '#475569'
      },
      fontFamily: {
        sans: ['Open Sans', 'sans-serif'],
        heading: ['Open Sans', 'sans-serif']
      }
    },
  },
  plugins: [],
}
