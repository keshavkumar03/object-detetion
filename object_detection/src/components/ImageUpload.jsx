// src/components/ImageUpload.js
// eslint-disable-next-line no-unused-vars
import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [detectedImage, setDetectedImage] = useState(null);

  const onFileChange = event => {
    setSelectedFile(event.target.files[0]);
  };

  const onFileUpload = () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    axios.post('http://localhost:8000/detect/image', formData, {
      responseType: 'blob',
    }).then(response => {
      const url = URL.createObjectURL(new Blob([response.data]));
      setDetectedImage(url);
    }).catch(error => {
      console.error('Error uploading the image:', error);
    });
  };

  return (
    <div>
      <h2>Image Upload</h2>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>Upload</button>
      {detectedImage && (
        <div>
          <h3>Detected Image</h3>
          <img src={detectedImage} alt="Detected" />
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
