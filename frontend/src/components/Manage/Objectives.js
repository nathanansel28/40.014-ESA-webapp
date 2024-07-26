// Objectives.js (or your component file)
import React from 'react';
import ObjectiveList from './ObjectiveList';
import './Objectives.css'; // Make sure the path is correct
import { Button } from 'react-bootstrap';

const Objectives = () => {
    return (
        <div className="objectives-container">
          <div className="objective_main">
            <p style={{color:"white"}}>Choose one objective to prioritize!</p>
            <div className="objective-title">
              <ObjectiveList />
              <Button type="primary">Submit</Button>
            </div>
          </div>
        {/* <div className="objective_main">
          <p style={{color:"white"}}>Results:</p>
          <div className="objective-title">
            Results... 
          </div>
        </div> */}
      </div>
    );
  };
  
  export default Objectives;
  
