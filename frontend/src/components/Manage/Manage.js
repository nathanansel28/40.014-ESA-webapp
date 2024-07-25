import React , {useState} from 'react';
import { Container, Col, Card, Form, Row,Table, Navbar } from 'react-bootstrap';
import Particle from '../Particle';
import Gantt from '../Chart/Gantt';
import UploadFile from './UploadFile'
import axios from 'axios';
import Papa from 'papaparse'; // CSV parsing library
import { AiOutlineDelete } from "react-icons/ai";
import { Button } from 'antd';
import ChooseBox from '../Manage/ChooseBox';
import SampleImage from '../../Assets/instructions_image.jpg';
import './Manage.css';

function Manage() {
  const [uploadedFileName, setUploadedFileName] = useState(null);
  const [csvData, setCsvData] = useState([]);
  const [selectedCards, setSelectedCards] = useState([]);
  const handleUploadSuccess = (fileName) => {
    handleReadCsv(fileName);
  };


  const handleReadCsv = async (filename) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/static/files/${filename}`, {
        responseType: 'blob',
      });
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target.result;
        Papa.parse(text, {
          header: true,
          complete: (result) => {
            setCsvData(result.data);
          },
        });
      };
      reader.readAsText(response.data);
    } catch (error) {
      console.error('Error reading CSV file', error);
    }
  };

  // const handleCheckboxChange = (row) => {
  //   setSelectedCards((prevSelectedCards) => {
  //     if (prevSelectedCards.some((selectedRow) => selectedRow.operation === row.operation)) {
  //       return prevSelectedCards.filter((selectedRow) => selectedRow.operation !== row.operation);
  //     } else {
  //       return [...prevSelectedCards, row];
  //     }
  //   });
  // };

  return (
    <>
    {/* <Row className="instruction-section">
  <Col md={8} style={{ textAlign: 'left', backgroundColor: 'transparent', color: 'white' }}>
    <Card style={{ backgroundColor: 'transparent', color: 'white', border: 'none' }}>
      <Card.Body>
        <Card.Title style={{ textAlign: 'center', fontWeight: 'bold' }}>Instructions for Uploading CSV Files</Card.Title>
        <Card.Text>
          <h5>Step 1: Prepare your CSV File</h5>
          <p>Ensure your CSV file follows the format provided in the sample file:</p>
          <img src={SampleImage} alt="Sample CSV Format" style={{ width: '100%', marginBottom: '20px' }} />
          <ul>
            <li><strong>OperationID</strong>: A unique identifier for each operation.</li>
            <li><strong>Operation</strong>: A common label for each operation.</li>
            <li><strong>Machine</strong>: The identifier of the machine on which the operation will run.</li>
            <li><strong>Start Date</strong>: The start date of the operation.</li>
            <li><strong>End Date</strong>: The end date of the operation.</li>
            <li><strong>Duration</strong>: The duration of the operation.</li>
            <li><strong>Percent Completion</strong>: The percentage of completion for each operation.</li>
            <li><strong>Predecessors</strong>: The predecessors constraint for each operation (Please strictly follow the format from the image above!).</li>
          </ul>
          <h5>Step 2: Upload the CSV File</h5>
          <ul>
            <li>Navigate to the upload section on the platform.</li>
            <li>Click on the 'Upload file' button.</li>
            <li>Select the CSV file from your device that matches the format described above.</li>
          </ul>
          <h5>Step 3: Select your minimization objective</h5>
          <ul>
            <li>After successfully uploading your CSV file you will be prompted to choose the objective you wish to minimize. The minimization objectives include:</li>
            <ul>
              <li>Minimize makespan</li>
              <li>Minimize WIP holding cost</li>
              <li>Minimize runtime</li>
              <li>Minimize Number of Tardy jobs</li>
            </ul>
          </ul>
          <h5>Step 4: Generating Gantt Chart</h5>
          <p>Once your CSV file is uploaded and your minimization objective is selected, the Gantt Chart will be automatically generated. Please review the Gantt Chart to ensure it accurately represents your schedule.</p>
          <h5>Additional Notes:</h5>
          <ul>
            <li>Ensure all dates, duration, and percent completion are in the correct unit of measure (i.e. Short Date, Number, and Number respectively).</li>
            <li>Double-check for any missing or incorrect data before uploading.</li>
          </ul>
        </Card.Text>
      </Card.Body>
    </Card>
  </Col>
</Row> */}

      <Container fluid>
        <Row>
          <Col>
            <div className="left-roundedge-section">
              <Col className="drag-drop-section-manage">
                <UploadFile onUploadSuccess={handleUploadSuccess} endpoint="http://127.0.0.1:8000/uploadfile/" />
                {/* <Particle /> */}
                <div className="table-container">
                  {csvData.length > 0 && (
                    <Table striped bordered hover className="custom-table">
                      <thead>
                        <tr>
                          {Object.keys(csvData[0]).map((header, index) => (
                            <th key={index}>{header}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {csvData.map((row, rowIndex) => (
                          <tr key={rowIndex}>
                            {Object.values(row).map((value, colIndex) => (
                              <td key={colIndex}>{value}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                  )}
                </div>
              </Col>
            </div>
          </Col>
          <Col>
            <div className="left-roundedge-section">
              <Col className="drag-drop-section-manage">
                <UploadFile onUploadSuccess={handleUploadSuccess} endpoint="http://127.0.0.1:8000/uploadfile/" />
                {/* <Particle /> */}
                <div className="table-container">
                  {csvData.length > 0 && (
                    <Table striped bordered hover className="custom-table">
                      <thead>
                        <tr>
                          {Object.keys(csvData[0]).map((header, index) => (
                            <th key={index}>{header}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {csvData.map((row, rowIndex) => (
                          <tr key={rowIndex}>
                            {Object.values(row).map((value, colIndex) => (
                              <td key={colIndex}>{value}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                  )}
                </div>
              </Col>
            </div>
          </Col>
          
  
          <Col className="right-gantt-chart">
            <div className="gantt-chart-wrapper">
              <div className="gantt-chart-container">
                <Gantt />
              </div>
            </div>
          </Col>
          </Row>
    
          {/* <Container>
            <Row>
              <Col md={8} className="choose-box-section">
                <ChooseBox />
              </Col>
            </Row>
          </Container> */}
      </Container>

    </>
  );
  
}

export default Manage;