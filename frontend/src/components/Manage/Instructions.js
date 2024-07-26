import React from 'react';
import { Divider } from 'antd';
import SampleImage from '../../Assets/instructions_image.jpg';

const Instructions = () => (
  <>
    <h5 style={{ textAlign: 'center', fontWeight: 'bold', color: 'white' }}>Instructions for Uploading CSV Files</h5>
    <Divider>Step 1: Prepare your CSV File</Divider>
    <p style={{ color: 'white' }}>Ensure your CSV file follows the format provided in the sample file:</p>
    <img src={SampleImage} alt="Sample CSV Format" style={{ width: '100%', marginBottom: '20px' }} />
    <ul style={{ color: 'white' }}>
      <li><strong>OperationID</strong>: A unique identifier for each operation.</li>
      <li><strong>Operation</strong>: A common label for each operation.</li>
      <li><strong>Machine</strong>: The identifier of the machine on which the operation will run.</li>
      <li><strong>Start Date</strong>: The start date of the operation.</li>
      <li><strong>End Date</strong>: The end date of the operation.</li>
      <li><strong>Duration</strong>: The duration of the operation.</li>
      <li><strong>Percent Completion</strong>: The percentage of completion for each operation.</li>
      <li><strong>Predecessors</strong>: The predecessors constraint for each operation (Please strictly follow the format from the image above!).</li>
    </ul>
    <Divider>Step 2: Upload the CSV File</Divider>
    <ul style={{ color: 'white' }}>
      <li>Navigate to the upload section on the platform.</li>
      <li>Click on the 'Upload file' button.</li>
      <li>Select the CSV file from your device that matches the format described above.</li>
    </ul>
    <Divider>Step 3: Select your minimization objective</Divider>
    <ul style={{ color: 'white' }}>
      <li>After successfully uploading your CSV file you will be prompted to choose the objective you wish to minimize. The minimization objectives include:</li>
      <ul>
        <li>Minimize makespan</li>
        <li>Minimize WIP holding cost</li>
        <li>Minimize runtime</li>
        <li>Minimize Number of Tardy jobs</li>
      </ul>
    </ul>
    <Divider>Step 4: Generating Gantt Chart</Divider>
    <p style={{ color: 'white' }}>Once your CSV file is uploaded and your minimization objective is selected, the Gantt Chart will be automatically generated. Please review the Gantt Chart to ensure it accurately represents your schedule.</p>
    <Divider>Additional Notes</Divider>
    <ul style={{ color: 'white' }}>
      <li>Ensure all dates, duration, and percent completion are in the correct unit of measure (i.e. Short Date, Number, and Number respectively).</li>
      <li>Double-check for any missing or incorrect data before uploading.</li>
    </ul>
  </>
);

export default Instructions;
