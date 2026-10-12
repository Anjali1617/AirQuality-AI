import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import PredictPollution from './pages/PredictPollution';
import HistoricalData from './pages/HistoricalData';
import ModelPerformance from './pages/ModelPerformance';
import AboutProject from './pages/AboutProject';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Sidebar />
        <div className="main-content">
          <Navbar />
          <main>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/predict" element={<PredictPollution />} />
              <Route path="/history" element={<HistoricalData />} />
              <Route path="/performance" element={<ModelPerformance />} />
              <Route path="/about" element={<AboutProject />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
