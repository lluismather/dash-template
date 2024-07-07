/** @type {import('tailwindcss').Config} */
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
module.exports = {
  corePlugins: {
    preflight: true,
  },
  content: [
    './app.py',
    './app/providers/**/*.{js,ts,jsx,tsx,py}',
    './resources/**/*.{js,ts,jsx,tsx,py}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          'LotaGrotesqueAlt3',
        ],
      },
      colors: {
        //
      },
      'aspectRatio': {
        'a4': '1 / 1.414',
      },
      'maxWidth': {
        'xs': '20rem',
      },
    },
  },
  plugins: [
    typography,
    forms,
  ],
}

