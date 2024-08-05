import React, { useState } from 'react';
import './Objectives.css'; // Make sure the path is correct

const ObjectiveList = ({
  onSelect}) => {
    const[selectedObjective, setSelectedObjective] = useState('');

    const handleObjectiveChange = (event) => {
      const selectedValue = event.target.value;
        setSelectedObjective(selectedValue);
        onSelect(selectedValue);
    }
  
    return (
        <div className="objective-list-container">
            <label className="objective-option">
                <input type="radio" name="objective" value="LETSA" onChange={handleObjectiveChange}/>
                Lead Time Evaluation and Scheduling Algorithm (LETSA)
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="EDD" onChange={handleObjectiveChange}/>
                Earliest Due Date (EDD)
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="SA" />
                Simulated Annealing (SA)
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="SA" />
                Lagrangian Relaxation (LR)
            </label>
        </div>
    );
};

export default ObjectiveList;
