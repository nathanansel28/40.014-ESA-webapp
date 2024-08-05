import React, { useState } from 'react';
import { Container, Col, Card, Row,  Table } from 'react-bootstrap';
import Papa from 'papaparse';
import axios from 'axios';
import UploadFile from '../Manage/UploadFile'; // Ensure this path is correct

function Orders() {
  const [csvData, setCsvData] = useState([]); // setting the csv useState
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

  return (
    <Container fluid className="orders-container">
      <Col className="drag-drop-section-orders">
        <UploadFile
          onUploadSuccess={handleUploadSuccess}
          endpoint="http://127.0.0.1:8000/uploadfile/"
          acceptedFileTypes=".csv"
        />
      </Col>
      <Row>
      {csvData.length > 0 && (
        <Row>
          <Col xs={12}>
            <div className="table-container">
              <Table className="custom-table">
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
            </div>
          </Col>
        </Row>
      )}
      </Row>
    </Container>
  );
}

export default Orders;



// import React, { useState } from 'react';
// import { Container, Col, Card, Row } from 'react-bootstrap';
// import Papa from 'papaparse';
// import axios from 'axios';
// import UploadFile from '../Manage/UploadFile'; // Make sure this is your file upload component

// function Orders() {
//     const [csvData, setCsvData] = useState([]);
//     const [selectedCards, setSelectedCards] = useState([]);
//     const handleUploadSuccess = (fileName) => {
//       handleReadCsv(fileName);
//     };
  
  
//     const handleReadCsv = async (filename) => {
//       try {
//         const response = await axios.get(`http://127.0.0.1:8000/static/files/${filename}`, {
//           responseType: 'blob',
//         });
//         const reader = new FileReader();
//         reader.onload = (e) => {
//           const text = e.target.result;
//           Papa.parse(text, {
//             header: true,
//             complete: (result) => {
//               setCsvData(result.data);
//             },
//           });
//         };
//         reader.readAsText(response.data);
//       } catch (error) {
//         console.error('Error reading CSV file', error);
//       }
//     }

//   return (
//     <>
//       <Container fluid className="orders-container">
//         <Col className="drag-drop-section-orders">
//           <UploadFile
//             onUploadSuccess={handleUploadSuccess}
//           />
//         </Col>
//         <Row>
//           {csvData.length > 0 && csvData.map((row, rowIndex) => (
//             <Col key={rowIndex} xs={12} md={6} lg={4} className="mb-3">
//               <Card>
//                 <Card.Body>
//                   {Object.entries(row).map(([key, value], index) => (
//                     <div key={index}>
//                       <strong>{key}:</strong> {value}
//                     </div>
//                   ))}
//                 </Card.Body>
//               </Card>
//             </Col>
//           ))}
//         </Row>
//       </Container>
//     </>
//   );
// }

// export default Orders;

// import React, { useState } from 'react';
// import { Container, Col, Table } from 'react-bootstrap';
// import UploadFile from '../Manage/UploadFile';
// import Papa from 'papaparse';

// function Orders() {
//   const [csvData, setCsvData] = useState([]);

//   const handleUploadSuccess = (file) => {
//     const reader = new FileReader();
//     reader.onload = (e) => {
//       const text = e.target.result;
//       Papa.parse(text, {
//         header: true,
//         complete: (result) => {
//           setCsvData(result.data);
//         },
//       });
//     };
//     reader.readAsText(file);
//   };

//   return (
//     <Container fluid className="orders-container">
//       <Col className="drag-drop-section-orders">
//         <UploadFile
//           onUploadSuccess={handleUploadSuccess}
//           endpoint="http://127.0.0.1:8000/uploadfile/"
//           acceptedFileTypes=".csv"
//         />
//         {csvData.length > 0 && (
//           <Table striped bordered hover size="sm" className="mt-4">
//             <thead>
//               <tr>
//                 {Object.keys(csvData[0]).map((header, index) => (
//                   <th key={index}>{header}</th>
//                 ))}
//               </tr>
//             </thead>
//             <tbody>
//               {csvData.map((row, rowIndex) => (
//                 <tr key={rowIndex}>
//                   {Object.values(row).map((value, colIndex) => (
//                     <td key={colIndex}>{value}</td>
//                   ))}
//                 </tr>
//               ))}
//             </tbody>
//           </Table>
//         )}
//       </Col>
//     </Container>
//   );
// }

// export default Orders;


// import React from 'react';
// import {Container, Col, Row} from'react-bootstrap';
// import UploadFile from '../Manage/UploadFile';


// function Orders() {
//     const handleUploadSuccess = (fileName) => {
//         console.log(`${fileName} uploaded successfully`);
//       };

//   return (
//     <>
//     <Container fluid className="orders-container">
//         <Col className="drag-drop-section-orders">
//         <UploadFile
//         onUploadSuccess={handleUploadSuccess}
//         endpoint="http://127.0.0.1:8000/uploadfile/"/>
//         </Col>

//     </Container>
//     </>
//   )
// }

// export default Orders;