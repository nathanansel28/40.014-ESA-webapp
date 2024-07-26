import React from 'react';
import ObjectiveList from './ObjectiveList';
import './Objectives.css'; // Make sure the path is correct
import { Button } from 'react-bootstrap';

const Objectives = () => {
    return (
        <div className="objectives-container">
<<<<<<< HEAD
            <div className="objective_main">
                <p className="instruction-text">Choose one objective to prioritize!</p>
                <div className="objective-list">
                    <ObjectiveList />
                </div>
                <Button className="submit-button">Submit</Button>
            </div>
        </div>
=======
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
>>>>>>> 71d801f7e3825560f3fba08ffed6c8d7a7681257
    );
};

export default Objectives;
