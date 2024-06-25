// src/components/VideoUpload.js
import React, { useState } from 'react';
import axios from 'axios';

const VideoUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [videoSrc, setVideoSrc] = useState(null);

  const onFileChange = event => {
    setSelectedFile(event.target.files[0]);
  };

  const onFileUpload = () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    axios.post('detect/video', formData, {
      responseType: 'blob',
    }).then(response => {
      const url = URL.createObjectURL(new Blob([response.data]));
      setVideoSrc(url);
    }).catch(error => {
      console.error('Error uploading the video:', error);
    });
    alert("file has been uploaded")
  };

  return (
    <div>
      <h2>Video Upload</h2>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>Upload</button>
      {videoSrc && (
        <div>
          <h3>Detected Video</h3>
          <video src={videoSrc} controls autoPlay />
        </div>
      )}
    </div>
  );
};

export default VideoUpload;
