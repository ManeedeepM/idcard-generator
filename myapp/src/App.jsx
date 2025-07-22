import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [department, setDepartment] = useState('');
  const [photo, setPhoto] = useState(null);
  const [idCard, setIdCard] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('name', name);
    formData.append('department', department);
    formData.append('photo', photo);

    try {
      const res = await axios.post('http://localhost:5000/upload', formData);
      setIdCard(res.data);
    } catch (err) {
      console.error('Upload error:', err);
    }
  };

  return (
    <div className="container">
      <h2>ID Card Generator</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Department"
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
          required
        />
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setPhoto(e.target.files[0])}
          required
        />
        <button type="submit">Generate ID</button>
      </form>

      {idCard && (
        <div className="id-card">
          <img src={`http://localhost:5000${idCard.photo_url}`} alt="Uploaded" />
          <h4>{idCard.name}</h4>
          <p><strong>Department:</strong> {idCard.department}</p>
        </div>
      )}
    </div>
  );
}

export default App;
