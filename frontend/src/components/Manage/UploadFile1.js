import React from 'react';
import { Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';
import { InboxOutlined } from '@ant-design/icons';
import confetti from 'canvas-confetti';

function generateConfetti() {
  confetti({
    spread: 90,
    particleCount: 80,
    origin: { y: 0.5 },
    ticks: 300
  });
}

const { Dragger } = Upload;

const UploadFile = ({ onUploadSuccess, endpoint, acceptedFileTypes, label }) => {
  const handleUpload = async ({ file }) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data);
      message.success('File uploaded successfully');
      console.log("message should show up");
      generateConfetti();
      onUploadSuccess(file.name);
    } catch (error) {
      console.error('Error uploading file', error);
      message.error('Failed to upload file');
    }
  };

  return (
    <div style={{textAlign:'center', marginBottom: '20px'}}>
      <h5>{label}</h5>
    <Dragger
      customRequest={handleUpload}
      showUploadList={false}
      accept={acceptedFileTypes}
    >
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <p className="ant-upload-drag-icon" style={{ margin: '0 10px 0 0' }}>
          <InboxOutlined style={{ fontSize: '24px' }} />
        </p>
        <p className="ant-upload-text">Click or drag file to this area to upload</p>
      </div>
    </Dragger>
    </div>
  );
};

export default UploadFile;



// import React from 'react';
// import { Upload, Button, message } from 'antd';
// import { UploadOutlined } from '@ant-design/icons';
// import axios from 'axios';
// import { InboxOutlined } from '@ant-design/icons';
// import confetti from 'canvas-confetti';


// function generateConfetti() {
//     confetti({
//       spread: 90,
//       particleCount: 80,
//       origin: { y: 0.5 },
//       ticks: 300
//     });
//   }
// const { Dragger } = Upload;


// const UploadFile = ({ onUploadSuccess }) => {
//   const handleUpload = async ({ file }) => {
//     const formData = new FormData();
//     formData.append('file', file);

//     try {
//       const response = await axios.post('http://127.0.0.1:8000/uploadfile/', formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//         },
//       });
//       console.log(response.data);
//       message.success('File uploaded successfully');
//       generateConfetti();
//       onUploadSuccess(file.name);
//     } catch (error) {
//       console.error('Error uploading file', error);
//       message.error('Failed to upload file');
//     }
//   };

//   return (
//     <Dragger customRequest={handleUpload} showUploadList={false}>
//       <div style={{ display: 'flex', alignItems: 'center' }}>
//         <p className="ant-upload-drag-icon" style={{ margin: '0 10px 0 0' }}>
//           <InboxOutlined style={{ fontSize: '24px' }} />
//         </p>
//         <p className="ant-upload-text">Click or drag file to this area to upload</p>
//       </div>
//     </Dragger>
//   );
// };

// export default UploadFile;
