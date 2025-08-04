import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // Commented out React.StrictMode as it interferes with react-beautiful-dnd
  // <React.StrictMode>
    <App />
  // </React.StrictMode>
); 