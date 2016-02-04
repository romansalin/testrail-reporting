var path = require('path');
var webpack = require('webpack');
var production = process.env.NODE_ENV === 'production';

var config = {
  // for faster builds use 'eval'
  devtool: 'eval-source-map',
  debug: true,
  entry: {
    main: path.resolve(__dirname, 'testrail_reporting/static/js/app.jsx')
  },
  output: {
    path: path.resolve(__dirname, 'testrail_reporting/static/build'),
    publicPath: '/build/',
    filename: 'bundle.js'
  },
  resolve: {
    modulesDirectories: ['node_modules', 'testrail_reporting/static/js'],
    extensions: ['', '.js', '.jsx']
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
  plugins: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      'window.jQuery': 'jquery'
    })
  ]
};

if (production) {
  config.devtool = null;
  config.debug = false;

  config.plugins.push(
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin({
      minimize: true
    })
  );
} else {
  // webpack-dev-server config
  config.devServer = {
    // enable iframe mode (open http://localhost:8080/webpack-dev-server/)
    contentBase: 'http://127.0.0.1:5000/',

    // embed the webpack-dev-server runtime into the bundle
    inline: false,

    // suppress boring information
    noInfo: true
  };
}

module.exports = config;
