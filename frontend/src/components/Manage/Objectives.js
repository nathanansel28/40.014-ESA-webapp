import React, { useState } from 'react';
import ObjectiveList from './ObjectiveList';
import './Objectives.css'; // Make sure the path is correct
import { Button } from 'react-bootstrap';

const Objectives = () => {
    const[selectedObjective, setSelectedObjective] = useState ('');
    const handleObjectiveSelection = (objective) => {
        setSelectedObjective(objective);
    };
    const handleSubmit = async () => {
        try {
          const response = await fetch('/api/submit-objective', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ selectedObjective }), // Send the selected objective
          });
      
          if (response.ok) {
            // Handle success (e.g., show a success message)
            console.log('Objective submitted successfully!');
          } else {
            // Handle error (e.g., show an error message)
            console.error('Error submitting objective');
          }
        } catch (error) {
          console.error('Network error:', error);
        }
      };
      

    return (
      <>
        <div className="objectives-container">
            <div className="objective_main">
                <p className="instruction-text">Choose one objective to prioritize!</p>
                <div className="objective-list">
                    <ObjectiveList onSelect={handleObjectiveSelection}/>
                </div>
                <Button className="submit-button" onClick={handleSubmit}>Submit</Button>
            </div>
        </div>

          {/* <div className="objective_main">
            <p style={{color:"white"}}>Choose one objective to prioritize!</p>
            <div className="objective-title">
              <ObjectiveList />
              <Button type="primary">Submit</Button>
            </div>
          </div> */}
        {/* <div className="objective_main">
          <p style={{color:"white"}}>Results:</p>
          <div className="objective-title">
            Results... 
          </div>
        </div> */}
      </>
    );
};

export default Objectives;
