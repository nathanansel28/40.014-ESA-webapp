import React from 'react';
import ObjectiveList from "./ObjectiveList";


const Objectives = () => {
    
    return ( 
    <div className="objective_main">
        <h className="objective_title">Choose one objective to prioritise!</h>
        <div className = "objective_title">    
                <ObjectiveList/>
        </div>
    </div>    

     );
}
 
export default Objectives;