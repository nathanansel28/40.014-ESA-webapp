import React from 'react';
import { Upload, message } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import axios from 'axios';
import confetti from 'canvas-confetti';
import './UploadFile.css'; // Import the custom CSS file

function generateConfetti() {
  confetti({
    spread: 90,
    particleCount: 80,
    origin: { y: 0.5 },
    ticks: 300,
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
      generateConfetti();
      onUploadSuccess(file.name);
    } catch (error) {
      console.error('Error uploading file', error);
      message.error('Failed to upload file');
    }
  };

  return (
    <div style={{ textAlign: 'center', marginBottom: '20px' }}>
      <h5>{label}</h5>
      <Dragger customRequest={handleUpload} showUploadList={false} accept={acceptedFileTypes}>
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
