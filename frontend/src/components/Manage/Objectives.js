import React from 'react';
import ObjectiveList from './ObjectiveList';
import './Objectives.css'; // Make sure the path is correct
import { Button } from 'react-bootstrap';

const Objectives = () => {
    return (
        <div className="objectives-container">
            <div className="objective_main">
                <p className="instruction-text">Choose one objective to prioritize!</p>
                <div className="objective-list">
                    <ObjectiveList />
                </div>
                <Button className="submit-button">Submit</Button>
            </div>
        </div>
    );
};

export default Objectives;
