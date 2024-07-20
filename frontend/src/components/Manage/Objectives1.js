import React from 'react';
import { Col } from 'react-bootstrap';
import ObjectiveList from './ObjectiveList';

// Objectives1 Component
const Objectives1 = () => {
  return (
    <>
      <div className='objective_main'>
        <div className='objective-title'>
          <ObjectiveList />
        </div>
      </div>
    </>
  )
}
  
  export default Objectives1;