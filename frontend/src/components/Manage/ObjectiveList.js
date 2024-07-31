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
                <input type="radio" name="objective" value="Minimise Makespan" onChange={handleObjectiveChange}/>
                Minimise Makespan
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise WIP Holding Costs" onChange={handleObjectiveChange}/>
                Minimise WIP Holding Costs
            </label>
            {/* <label className="objective-option">
                <input type="radio" name="objective" value="Minimise Runtime" onChange={handleObjectiveChange}/>
                Minimise Runtime
            </label> */}
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise Tardiness" onChange={handleObjectiveChange}/>
                Minimise Number of Tardy Jobs
            </label>
        </div>
    );
};

export default ObjectiveList;
