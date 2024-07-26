import React from 'react';
import './Objectives.css'; // Make sure the path is correct

const ObjectiveList = () => {
    return (
        <div className="objective-list-container">
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise Makespan" />
                Minimise Makespan
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise WIP Holding Costs" />
                Minimise WIP Holding Costs
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise Runtime" />
                Minimise Runtime
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise Tardiness" />
                Minimise Tardiness
            </label>
        </div>
    );
};

export default ObjectiveList;
