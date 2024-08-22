/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/src/**/*.js',],
  theme: {
    extend: {
      screens: {
        'max-1200': { 'max': '1200px' },
        'max-1100': { 'max': '1100px' },
        'max-1000': { 'max': '1000px' },
        'max-900': { 'max': '900px' },
        'max-800': { 'max': '800px' },
        'max-700': { 'max': '700px' },
        'max-600': { 'max': '600px' },
        'max-500': { 'max': '500px' },
        'max-400': { 'max': '400px' },
        'max-300': { 'max': '300px' },
        'max-650': { 'max': '650px' },
        'max-750': { 'max': '750px' },
        'max-850': { 'max': '850px' },
      },
    },
  },
  plugins: [],
}

