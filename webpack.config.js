var path = require("path");
var webpack = require('webpack');

module.exports = {
  debug: true,
  entry: path.join(__dirname, 'testrail_reporting/js/app.js'),
  output: {
    path: path.join(__dirname, 'testrail_reporting/js'),
    filename: "bundle.js"
  },
  module: {
    loaders: [
      {test: /\.js?$/, exclude: /node_modules/, loader: "babel-loader"},
      {test: /\.css$/, loader: "style!css"},
      {test: /\.less$/, loader: "style!css!less"},
      {test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9\.=]+)?$/, loader: 'file-loader'}
    ]
  }
};
