import React from 'react'


const objectives = ["1","2","3","4"]
const ObjectiveList = () => {
  return (
    <div>
         {objectives.map((objective, index) => (
            <div key={index} className="objective_block">
                <input type="radio" name="objective" className="objective_button"/>
                <label className="objective_text">Objective: {objective}</label>
            </div>
        ))}
    </div>
  )
}


export default ObjectiveList;