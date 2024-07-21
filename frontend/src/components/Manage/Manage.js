import React , {useState} from 'react';
import { Container, Col, Card, Form, Row } from 'react-bootstrap';
import Particle from '../Particle';
import DragDrop from './DragDrop';
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

  const handleCheckboxChange = (row) => {
    setSelectedCards((prevSelectedCards) => {
      if (prevSelectedCards.some((selectedRow) => selectedRow.operation === row.operation)) {
        return prevSelectedCards.filter((selectedRow) => selectedRow.operation !== row.operation);
      } else {
        return [...prevSelectedCards, row];
      }
    });
  };

  return (
    <>
      <Container fluid height>

      <Row>
        <Col xs={4}>
        <div className="left-roundedge-section">
            <Col className="drag-drop-section-manage">
              <UploadFile onUploadSuccess={handleUploadSuccess} endpoint="http://127.0.0.1:8000/uploadfile/" />
              <Particle />
              <div style={{ maxHeight: '400px', overflowY: 'auto', marginTop: '20px' }}>
                {csvData.length > 0 && csvData.map((row, index) => (
                  <Card key={index} style={{ margin: '10px 0' }}>
                    <Card.Body style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Card.Title style={{ margin: 0, color: '#000' }}>{row.operation}</Card.Title>
                      <Form.Check
                        type="checkbox"
                        onChange={() => handleCheckboxChange(row)}
                        checked={selectedCards.some((selectedRow) => selectedRow.operation === row.operation)}
                      />
                    </Card.Body>
                  </Card>
                ))}
              </div>
          </Col>
          </div>
          
        </Col>

        <Col className="selected-cards-section" xs={8}>
          <div style={{ maxHeight: '300px', overflowY: 'auto', marginTop: '20px' }}>
            {selectedCards.length > 0 && selectedCards.map((row, index) => (
              <Card key={index} style={{ margin: '10px 0' }}>
                <Card.Body style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Card.Title style={{ margin: 0, color: '#000' }}>{row.operation}</Card.Title>
                  <Button  className="ant-btn" icon={<AiOutlineDelete />} size="large" onClick={()=>handleCheckboxChange(row)} />
                </Card.Body>
              </Card>
            ))}
          </div>
        </Col>

        <Container>
          <Row>
            <Col md={8} className="choose-box-section">
              <ChooseBox/>
            </Col>
          </Row>
        </Container>

        
      </Row>
    </Container>

    </>
  )
}

export default Manage;