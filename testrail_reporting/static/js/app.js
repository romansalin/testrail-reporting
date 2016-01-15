import React from 'react';
import TestRail from './components/TestRail';
import Router from 'react-router';
import {DefaultRoute, Route, Routes, NotFoundRoute} from 'react-router';

require("../less/app.less");

React.render(<TestRail />, document.getElementById('testrail'));
