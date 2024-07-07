const path = require('path');

module.exports = {
  entry: './resources/js/app.js',
  output: {
    filename: 'bundle.js', // Output bundle file name
    path: path.resolve(__dirname, 'assets/'), // Path to output folder
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader', // Transpile ES6+ to compatible JavaScript
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  }
};