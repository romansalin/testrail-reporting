import React from 'react';
import { render } from 'react-dom';
import { Router, Route, Link, DefaultRoute, Routes, NotFoundRoute } from 'react-router';

import '../less/app.less';

import 'bootstrap-less/js/bootstrap.min';
import 'moment/min/moment.min.js';
import 'bootstrap-material-design/dist/js/material.min';
import 'bootstrap-material-design/dist/js/ripples.min';

import TestRail from './components/TestRail';

render(<TestRail />, document.getElementById('testrail'));
