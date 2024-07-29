import React, { useState, useEffect } from 'react';
import { Container, Col, Row, Table } from 'react-bootstrap';
import Particle from '../Particle';
import Gantt from '../Chart/Gantt';
import UploadFile from './UploadFile';
import UploadFile1 from './UploadFile1';
import axios from 'axios';
import Papa from 'papaparse'; // CSV parsing library
import ChooseBox from '../Manage/ChooseBox';
import ProgressBar from './Stepper';
import Instructions from './Instructions';
import { Stepper } from '@mui/material';
import ProgressBar from './ProgressBar';

function Manage() {
  const [csvData, setCsvData] = useState([]);
  const [csvData1, setCsvData1] = useState([]);

  useEffect(() => {
    // Retrieve data from sessionStorage on component mount
    const savedCsvData = sessionStorage.getItem('csvData');
    const savedCsvData1 = sessionStorage.getItem('csvData1');
    if (savedCsvData) setCsvData(JSON.parse(savedCsvData));
    if (savedCsvData1) setCsvData1(JSON.parse(savedCsvData1));
  }, []);

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
            sessionStorage.setItem('csvData', JSON.stringify(result.data));
          },
        });
      };
      reader.readAsText(response.data);
    } catch (error) {
      console.error('Error reading CSV file', error);
    }
  };

  const handleUploadSuccess1 = (fileName) => {
    handleReadCsv1(fileName);
  };

  const handleReadCsv1 = async (filename) => {
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
            setCsvData1(result.data);
            sessionStorage.setItem('csvData1', JSON.stringify(result.data));
          },
        });
      };
      reader.readAsText(response.data);
    } catch (error) {
      console.error('Error reading CSV file', error);
    }
  };

  return (
    <>
      <Row>
        <div style={{ position: 'absolute', paddingTop: "100px" }} >
          <ProgressBar />
        </div>
      </Row>

      <div className="central-container">
        <Instructions />
      </div>

      <Container fluid>
        <Row>
          <Col>
            <div className="left-roundedge-section">
              <Col className="drag-drop-section-manage">
                <UploadFile onUploadSuccess={handleUploadSuccess} endpoint="http://127.0.0.1:8000/uploadfile/" />
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
                <UploadFile1 onUploadSuccess={handleUploadSuccess1} endpoint="http://127.0.0.1:8000/uploadfile/" />
                <div className="table-container">
                  {csvData1.length > 0 && (
                    <Table striped bordered hover className="custom-table">
                      <thead>
                        <tr>
                          {Object.keys(csvData1[0]).map((header, index) => (
                            <th key={index}>{header}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {csvData1.map((row, rowIndex) => (
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

          <Container>
            <Row>
              <Col>
                <ChooseBox />
              </Col>
            </Row>
          </Container>


          <Col className="right-gantt-chart">
            <div style={{ maxHeight: '800px', overflowY: 'auto', marginTop: '20px' }}>
              <Gantt />
            </div>
          </Col>
        </Row>

        <Row>
          <Col>
            <div style={{ height: '200px' }}></div> {/* Adjust the height as needed */}
          </Col>
        </Row>

      </Container>

    </>
  );
}

export default Manage;



// import React, { useState } from 'react';
// import { Container, Col, Card, Form, Row, Table, Navbar } from 'react-bootstrap';
// import Particle from '../Particle';
// import Gantt from '../Chart/Gantt';
// import UploadFile from './UploadFile';
// import UploadFile1 from './UploadFile1';
// import axios from 'axios';
// import Papa from 'papaparse'; // CSV parsing library
// import { AiOutlineDelete } from "react-icons/ai";
// import { Button } from 'antd';
// import ChooseBox from '../Manage/ChooseBox';
// import SampleImage from '../../Assets/instructions_image.jpg';
// import './Manage.css';
// import Instructions from './Instructions';
// import { Stepper } from '@mui/material';
// import ProgressBar from './Stepper';

// function Manage() {
//   const [uploadedFileName, setUploadedFileName] = useState(null);
//   const [csvData, setCsvData] = useState([]);
//   const [csvData1, setCsvData1] = useState([]);
//   const [selectedCards, setSelectedCards] = useState([]);

  

//   const handleUploadSuccess = (fileName) => {
//     handleReadCsv(fileName);
//   };

//   const handleReadCsv = async (filename) => {
//     try {
//       const response = await axios.get(`http://127.0.0.1:8000/static/files/${filename}`, {
//         responseType: 'blob',
//       });
//       const reader = new FileReader();
//       reader.onload = (e) => {
//         const text = e.target.result;
//         Papa.parse(text, {
//           header: true,
//           complete: (result) => {
//             setCsvData(result.data);
//           },
//         });
//       };
//       reader.readAsText(response.data);
//     } catch (error) {
//       console.error('Error reading CSV file', error);
//     }
//   };

//   const handleUploadSuccess1 = (fileName) => {
//     handleReadCsv1(fileName);
//   };

//   const handleReadCsv1 = async (filename) => {
//     try {
//       const response = await axios.get(`http://127.0.0.1:8000/static/files/${filename}`, {
//         responseType: 'blob',
//       });
//       const reader = new FileReader();
//       reader.onload = (e) => {
//         const text = e.target.result;
//         Papa.parse(text, {
//           header: true,
//           complete: (result) => {
//             setCsvData1(result.data);
//           },
//         });
//       };
//       reader.readAsText(response.data);
//     } catch (error) {
//       console.error('Error reading CSV file', error);
//     }
//   };

//   return (
//     <>
//     <Row>
//       <div style={{ position:'absolute', paddingTop:"100px"}} >
//       <ProgressBar/>
//       </div>
//     </Row>

//     <div className="central-container">
//       <Instructions />
//     </div>
    
//       <Container fluid>
//         <Row>
//           <Col>
//             <div className="left-roundedge-section">
//               <Col className="drag-drop-section-manage">
//                 <UploadFile onUploadSuccess={handleUploadSuccess} endpoint="http://127.0.0.1:8000/uploadfile/" />
//                 <div className="table-container">
//                   {csvData.length > 0 && (
//                     <Table striped bordered hover className="custom-table">
//                       <thead>
//                         <tr>
//                           {Object.keys(csvData[0]).map((header, index) => (
//                             <th key={index}>{header}</th>
//                           ))}
//                         </tr>
//                       </thead>
//                       <tbody>
//                         {csvData.map((row, rowIndex) => (
//                           <tr key={rowIndex}>
//                             {Object.values(row).map((value, colIndex) => (
//                               <td key={colIndex}>{value}</td>
//                             ))}
//                           </tr>
//                         ))}
//                       </tbody>
//                     </Table>
//                   )}
//                 </div>
//               </Col>
//             </div>
//           </Col>
//           <Col>
//             <div className="left-roundedge-section" >
//               <Col className="drag-drop-section-manage">
//                 <UploadFile1 onUploadSuccess={handleUploadSuccess1} endpoint="http://127.0.0.1:8000/uploadfile/" />
//                 <div className="table-container">
//                   {csvData1.length > 0 && (
//                     <Table striped bordered hover className="custom-table">
//                       <thead>
//                         <tr>
//                           {Object.keys(csvData1[0]).map((header, index) => (
//                             <th key={index}>{header}</th>
//                           ))}
//                         </tr>
//                       </thead>
//                       <tbody>
//                         {csvData1.map((row, rowIndex) => (
//                           <tr key={rowIndex}>
//                             {Object.values(row).map((value, colIndex) => (
//                               <td key={colIndex}>{value}</td>
//                             ))}
//                           </tr>
//                         ))}
//                       </tbody>
//                     </Table>
//                   )}

//                 </div>
//               </Col>
//             </div>
//           </Col>

//           <Container>
//             <Row>
//               <Col className="choose-box-section">
//                 <ChooseBox />
//               </Col>
//             </Row>
//           </Container>
          
  
//             <Col className="right-gantt-chart">
//               <div style={{ maxHeight: '800px', overflowY: 'auto', marginTop: '20px' }}>
//                 <Gantt />
//               </div>
//             </Col>
//           </Row>

//           <Row>
//             <Col>
//               <div style={{ height: '200px' }}></div> {/* Adjust the height as needed */}
//             </Col>
//           </Row>
    
//       </Container>

//     </>
//   );
// }

// export default Manage;

