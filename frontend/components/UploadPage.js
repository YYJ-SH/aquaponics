import React, { useState } from 'react';
import axios from 'axios';
import { Image } from 'antd';

const UploadPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [responseData, setResponseData] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);

    const reader = new FileReader();
    reader.onload = () => {
      setPreviewImage(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('image', selectedFile);

    axios
      .post('http://localhost:8000/api/upload/', formData)
      .then((response) => {
        setResponseData(response.data); // Set the response data in state
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const displayData = typeof responseData === 'number' ? 'No disease found' : responseData;

  let parsedData = null;
  if (typeof displayData === 'object') {
    parsedData = JSON.parse(JSON.stringify(displayData));
  }

  return (
    <div>
      <h1>Upload Page</h1>
      <input type="file" onChange={handleFileChange} />
      {previewImage && (
        <div className='w-full h-full rounded-lg'><Image src={previewImage} style={{ maxWidth: '100%', marginTop: '10px', borderRadious:"12px"}} /></div>
      )}
      <button onClick={handleUpload}>Upload</button>
      {parsedData && (
        <div>
          <h3>Response Data:</h3>
          <p>{parsedData.results}</p>
          <p>발견한 질병: {parsedData.results=="gray" ? "잿빛곰팡이병" : (parsedData.results=="downy" ? "노균병": "발견된 질병이 없습니다.")}</p>
        </div>
      )}
    </div>
  );
};

export default UploadPage;
