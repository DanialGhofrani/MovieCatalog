const webpack = require('webpack');
const config = {
  entry: {
    index: __dirname + '/src/js/index.jsx'
  },
  output: {
    path: __dirname + '/dist',
    filename: '[name]-bundle.js'
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css']
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  }
};
module.exports = config;
