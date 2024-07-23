// Objectives.js (or your component file)
import React from 'react';
import ObjectiveList from './ObjectiveList';
import './Objectives.css'; // Make sure the path is correct
import { Button } from 'react-bootstrap';

const Objectives = () => {
    return ( 
        <div className="objective_main">
            <p style={{color:"white"}}>Choose one objective to prioritize!</p>
            <div className="objective_title">
                <ObjectiveList/> 

                <Button type="primary">Submit</Button>
            </div>
        </div>
  );
};

export default Objectives;
