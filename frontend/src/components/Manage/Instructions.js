import React from 'react';
import { Row, Col, Card } from 'react-bootstrap';
// import SampleImage from '../../Assets/instructions_image.png';
// import './Manage.css';
import './Instructions.css';

const Instructions = () => (
  <div className="instructions-container">
    <Row>
      <Col md={11} style={{ textAlign: 'left', backgroundColor: 'transparent', color: 'white' }}>
        <Card style={{ backgroundColor: 'transparent', color: 'white', border: 'none' }}>
          <Card.Body>
            <Card.Title style={{ textAlign: 'center', fontWeight: 'bold' }}>✨Instructions for Uploading CSV Files✨ </Card.Title>
            <Card.Text>
              <h5 style={{textAlign:'center'}}>Step 1: Prepare your CSV File 📝</h5>
              <p style={{textAlign:'center'}}>Ensure your CSV file follows the format provided in the sample file:</p>
              {/* <img src={SampleImage} alt="Sample CSV Format" style={{ width: '70%', marginBottom: '20px' }} /> */}
              <table border="1">
                <thead>
                  <tr> 
                    <th>operation</th>
                    <th>predecessors_operations</th>
                    <th>processing_time</th>
                    <th>machine</th>
                    <th>workcenter</th>
                    <th>due_date</th>
                    <th>end_product</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>J.1</td>
                    <td>[]</td>
                    <td>1</td>
                    <td>M1</td>
                    <td>WC#3</td>
                    <td></td>
                    <td></td>
                  </tr>
                  <tr>
                    <td>J.2</td>
                    <td>[]</td>
                    <td>1</td>
                    <td>M1</td>
                    <td>WC#2</td>
                    <td></td>
                    <td></td>
                  </tr>
                  <tr>
                    <td>J.3</td>
                    <td>['J.1', 'J.2']</td>
                    <td>1</td>
                    <td>M1</td>
                    <td>WC#3</td>
                    <td></td>
                    <td></td>
                  </tr>
                  <tr>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                  </tr>
                  <tr>
                    <td>J.30</td>
                    <td>['J.29']</td>
                    <td>2</td>
                    <td>M1</td>
                    <td>WC#1</td>
                    <td>47</td>
                    <td>1</td>
                  </tr>
                </tbody>
              </table>
              <ul>
                {/* <li><strong>OperationID</strong>: A unique identifier for each operation.</li> */}
                <li><strong>Operation</strong>: A common label for each operation.</li>
                <li><strong>Predecessors</strong>: The predecessors constraint for each operation (Please strictly follow the format from the image above!).</li>
                <li><strong>Processing Time</strong>:Processing time required.</li>
                <li><strong>Machine</strong>: The identifier of the machine on which the operation will run.</li>
                <li><strong>Workcenter</strong>: Workcenter for each operation.</li>
                <li><strong>Due Date</strong>: Due date for the job.</li>
                <li><strong>End Product</strong>: The number of end product being produced.</li>
              </ul>
              <h5 style={{textAlign:'center'}}>Step 2: Upload the CSV File 📤</h5>
              <ul>
                <li>Navigate to the upload section on the platform.</li>
                <li>Click on the 'Upload file' button.</li>
                <li>Select the CSV file from your device that matches the format described above.</li>
              </ul>
              <h5 style={{textAlign:'center'}}>Step 3: Select your heuristic approach👆</h5>
              <ul>
                <li>After successfully uploading your CSV file you will be prompted to choose the algorithm you wish to utilise. The heuristic algorithms include:</li>
                <ul>
                  <li>Lead Time Evaluation and Scheduling Algorithm (LETSA): Minimises makespan, algorithmic runtime, and WIP cost</li>
                  <li>Earliest Due Date (EDD): Minimises algorithmic runtime and number of tardy jobs</li>
                  <li>Lagrangian Relaxation (LR): Minimise algorithmic runtime and provides lower bound of the optimality</li>
                  <li>Simulated Annealing (SA): Maximises solution quality</li>
                </ul>
              </ul>
              <h5 style={{textAlign:'center'}}>Step 4: Generating Gantt Chart ⟳</h5>
              <p>Once your CSV file is uploaded and your heuristc algorithm is selected, the Gantt Chart will be automatically generated. Please review the Gantt Chart as it may makes mistake.</p>
              <h5 style={{textAlign:'center'}}>💡 Additional Notes:</h5>
              <ul>
                <li>Ensure all variables are in the correct unit of measure (i.e. Number and Text).</li>
                <li>Double-check for any missing or incorrect data before uploading.</li>
                <li>Ensure that only last row contains the 'due date' and 'end product' information.</li>
                <li>This CSV file will be your "df_BOM" file</li>
              </ul>
            </Card.Text>
          </Card.Body>
        </Card>
      </Col>
    </Row>
  </div>
);

export default Instructions;