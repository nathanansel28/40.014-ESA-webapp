import React from 'react';
import { Container, Col, Row } from 'react-bootstrap';
import GanttChart from './GanttChart';
import './Gantt.css';


function Gantt() {
  return (
    <div className="gantt-container">
      <header className="gantt-header">
        {/* <h1>Assembly Line Scheduling</h1> */}
      </header>
      <GanttChart />
    </div>
  )
}

export default Gantt;