import '../less/app.less';

import 'bootstrap-less/js/bootstrap.min';
import 'bootstrap-material-design/dist/js/material.min';
import 'bootstrap-material-design/dist/js/ripples.min';
import moment from 'moment/min/moment.min';

import React from 'react';
import { render } from 'react-dom';
import { Router, Route, Link, DefaultRoute, Routes, NotFoundRoute } from 'react-router';
import { Input, Panel, Button, Navbar, NavBrand, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';

import TestRail from './components/TestRail';

moment().format();
$.material.init();

render(<TestRail />, document.getElementById('testrail'));
