var path = require('path');
var webpack = require('webpack');
var assetsPath = path.join(__dirname, 'testrail_reporting/static/js/build');

// TODO(rsalin): development and production mode
module.exports = {
  debug: true,
  entry: path.join(__dirname, 'testrail_reporting/static/js/app.js'),
  output: {
    path: assetsPath,
    //filename: '[name]-[hash].js',
    //chunkFilename: '[name]-[chunkhash].js'
    filename: 'bundle.js'
  },
  resolve: {
    modulesDirectories: ['node_modules', 'testrail_reporting/static/js']
  },
  module: {
    loaders: [
      {test: /\.json$/, loader: 'json-loader'},
      {test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader'},
      {test: /\.css$/, exclude: /node_modules/, loader: 'style!css'},
      {test: /\.less$/, exclude: /node_modules/, loader: 'style!css!less'},
      {test: /\.(png|jpg|gif)$/, loader: 'url-loader?limit=10000'},
      {test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'url-loader?limit=10000&mimetype=application/font-woff'},
      {test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'file-loader'}
    ]
  }
};
