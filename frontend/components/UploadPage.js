import React, { useState } from 'react';
import axios from 'axios';

const UploadPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('image', selectedFile);
    console.log(selectedFile);

    axios
      .post('http://localhost:8000/api/upload/', formData)
      .then((response) => {
        // Handle response from the server
        console.log(response.data);
      })
      .catch((error) => {
        // Handle error
        console.error(error);
      });
  };

  return (
    <div>
      <h1>Upload Page</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default UploadPage;
