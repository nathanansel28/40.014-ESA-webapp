import React from 'react';
import ObjectiveList from "./ObjectiveList";
import { Button } from "antd";


const Objectives = () => {
    
    return ( 
    <div className="objective_main">
        <h className="objective_title">Choose one objective to prioritise!</h>
        <div className = "objective_title">    
                <ObjectiveList/>
                <Button type="primary">Submit</Button>
                
               
        </div>
    </div>    

     );
}
 
export default Objectives;
