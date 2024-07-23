import React , {useState} from 'react';
import { Container, Col, Card, Form, Row,Table } from 'react-bootstrap';
import Particle from '../Particle';
import Gantt from '../Chart/Gantt';
import UploadFile from './UploadFile'
import axios from 'axios';
import Papa from 'papaparse'; // CSV parsing library
import { AiOutlineDelete } from "react-icons/ai";
import { Button } from 'antd';
import ChooseBox from '../Manage/ChooseBox';


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
      <Container fluid>
        <Row>
          <Col xs={4}>
            <div className="left-roundedge-section">
              <Col className="drag-drop-section-manage">
                <UploadFile onUploadSuccess={handleUploadSuccess} endpoint="http://127.0.0.1:8000/uploadfile/" />
                <Particle />
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
  
          <Col className="right-gantt-chart" xs={8}>
            <div style={{ maxHeight: '300px', overflowY: 'auto', marginTop: '20px' }}>
              <Gantt />
            </div>
          </Col>
        </Row>
  
        <Container>
          <Row>
            <Col md={8} className="choose-box-section">
              <ChooseBox />
            </Col>
          </Row>
        </Container>
      </Container>
    </>
  );
  
}

export default Manage;