import React from 'react';
import { render } from 'react-dom';
import { Router, Route, Link, DefaultRoute, Routes, NotFoundRoute } from 'react-router';
import { Input, Panel, Button, Navbar, NavBrand, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';

import '../less/app.less';

import moment from 'moment/min/moment.min';
import jQuery from 'jquery/dist/jquery.min';
import 'bootstrap-less/js/bootstrap.min';
import 'bootstrap-material-design/dist/js/material.min';
import 'bootstrap-material-design/dist/js/ripples.min';

import TestRail from './components/TestRail';

//render(<TestRail />, document.getElementById('testrail'));

jQuery(() => {
  moment().format();
  $.material.init();

  render((
    <Router>
      <Route path="/" component={TestRail} />
    </Router>
  ), document.getElementById('testrail'));
});
