var path = require('path');
var webpack = require('webpack');

module.exports = {
  debug: process.env.NODE_ENV !== 'production',
  entry: path.resolve(__dirname, 'testrail_reporting/static/js/app.js'),
  output: {
    path: path.resolve(__dirname, 'testrail_reporting/static/build'),
    filename: 'bundle.js'
  },
  resolve: {
    modulesDirectories: ['node_modules', 'testrail_reporting/static/js']
  },
  module: {
    loaders: [
      { test: /\.json$/, loader: 'json-loader' },
      { test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader' },
      { test: /\.css$/, loader: 'style!css' },
      { test: /\.less$/, loader: 'style!css!less' },
      { test: /\.(png|jpg|gif)$/, loader: 'url-loader?limit=10000' },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: 'url-loader?limit=10000&mimetype=application/font-woff'
      },
      { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'file-loader' }
    ]
  },
  //devServer: {
  //  port: 3000,
  //  contentBase: 'testrail_reporting/static/build',
  //  hot: true,
  //  stats: {
  //    colors: true
  //  },
  //  historyApiFallback: false,
  //  headers: {
  //    'Access-Control-Allow-Origin': 'http://localhost:3001',
  //    'Access-Control-Allow-Headers': 'X-Requested-With'
  //  }
  //}
};
