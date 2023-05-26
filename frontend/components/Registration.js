import React, { useState } from 'react';
import axios from 'axios';

const Registeration = () => {
  const [formData, setFormData] = useState({
    name: '',
    id: '',
    password: '',
    email: '',
    deviceId: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
  
    // Send the form data using Axios
    axios.post('http://localhost:8000/api/register/', formData)
      .then(response => {
        // Handle the response
        console.log(response.data);
      })
      .catch(error => {
        // Handle the error
        console.error(error);
      });
  
    // Reset the form after submission
    setFormData({
      name: '',
      id: '',
      password: '',
      email: '',
      deviceId: ''
    });
  
  };

  return (
    <div className="w-full h-full flex items-center justify-center min-h-screen bg-green-100">
      <div className="w-[150px] max-w-md bg-white rounded-lg shadow-md p-8">
        <h2 className="text-3xl font-semibold text-center mb-6">Register</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="name" className="block mb-2 font-medium">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded border-green-300 focus:outline-none focus:border-green-500"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="id" className="block mb-2 font-medium">ID</label>
            <input
              type="text"
              id="id"
              name="id"
              value={formData.id}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded border-green-300 focus:outline-none focus:border-green-500"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="password" className="block mb-2 font-medium">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded border-green-300 focus:outline-none focus:border-green-500"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="email" className="block mb-2 font-medium">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded border-green-300 focus:outline-none focus:border-green-500"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="deviceId" className="block mb-2 font-medium">Device ID</label>
            <input
              type="text"
              id="deviceId"
              name="deviceId"
              value={formData.deviceId}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded border-green-300 focus:outline-none focus:border-green-500"
              />
            </div>
            <div className="mt-6">
              <button
                type="submit"
                className="w-full px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600 focus:outline-none focus:bg-green-600"
              >
                Register
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };
  
  export default Registeration;
  
             
