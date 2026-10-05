/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0a0c',
        surface: '#18181b',
        border: '#27272a',
        primary: '#3b82f6',
        primaryHover: '#2563eb',
        danger: '#ef4444',
        warning: '#f59e0b',
        success: '#10b981',
        brand: {
          dark: '#2d3a2e',
          green: '#3d5a3e',
          light: '#f5f3ef',
          cream: '#faf8f5'
        }
      },
      fontFamily: {
        'helvetica-neue': ['"Helvetica Neue Light"', 'Helvetica', 'Arial', 'sans-serif'],
        'playfair': ['"Playfair Display"', 'serif'],
        'oswald': ['"Oswald"', 'sans-serif'],
        'montserrat': ['"Montserrat"', 'sans-serif'],
        'roboto-slab': ['"Roboto Slab"', 'serif'],
        'raleway': ['"Raleway"', 'sans-serif']
      }
    },
  },
  plugins: [],
}
