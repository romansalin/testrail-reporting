import React from 'react';

class TestRail extends React.Component {
  render() {
    return (
      <div>
        <h1 className="header">Dashboard</h1>
        <p>Get all data from TestRail in Excel format:</p>
        <a href="/testrail/reports/all" className="btn btn-raised btn-primary">Download</a>
      </div>
    );
  }
}

export default TestRail;
