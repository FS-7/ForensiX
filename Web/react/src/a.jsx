import React, { useState } from 'react';
import './A.css';

function A() {
  const [cases, setCases] = useState([
    { id: 1, name: 'Case 1' },
    { id: 2, name: 'Case 2' },
    { id: 3, name: 'Case 3' },
    { id: 4, name: 'Case 4' },
    { id: 5, name: 'Case 5' }
  ]);

  const handleDelete = (id) => {
    setCases(cases.filter(case_ => case_.id !== id));
  };

  const handleDetails = (id) => {
    alert(`Viewing details for ${cases.find(case_ => case_.id === id)?.name}`);
  };

  return (
    <div className="app">
      <div className="header"></div>
      <div className="main-container">
        <div className="sidebar"></div>
        <div className="content">
          <div className="search-bar"></div>
          <div className="cases-list">
            {cases.map(case_ => (
              <div key={case_.id} className="case-item">
                <span className="case-name">{case_.name}</span>
                <div className="case-actions">
                  <button 
                    className="details-btn"
                    onClick={() => handleDetails(case_.id)}
                  >
                    Details
                  </button>
                  <button 
                    className="delete-btn"
                    onClick={() => handleDelete(case_.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default A;