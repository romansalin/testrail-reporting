import '../less/app.less';

import 'bootstrap-less';
import 'bootstrap-material-design';
import moment from 'moment';
import $ from 'jquery';

import React from 'react';
import ReactDOM from 'react-dom';
import createBrowserHistory from 'history/lib/createBrowserHistory';
import { Router, Route, Link, browserHistory, DefaultRoute, Routes, NotFoundRoute } from 'react-router';

import TestRail from './components/TestRail';

moment().format();
$.material.init();

ReactDOM.render((
  <Router history={createBrowserHistory()}>
    <Route path="/" component={TestRail} />
  </Router>
), document.getElementById('testrail'));
