import React from 'react';
import { Container, Col, Row } from 'react-bootstrap';
import GanttChart from './GanttChart';

function Gantt() {
  return (
    <div>
      <header>
        <h1>Assembly Line Scheduling</h1>
      </header>
      <GanttChart />
    </div>
  )
}

export default Gantt;