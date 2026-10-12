import React, { useState, useEffect } from 'react';
import { Activity, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';
import { getHealth } from '../services/api';

const Navbar = () => {
  const [health, setHealth] = useState({ status: 'checking', model_loaded: false });
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString());

  const checkStatus = async () => {
    try {
      const data = await getHealth();
      setHealth(data);
    } catch {
      setHealth({ status: 'offline', model_loaded: false });
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    const timeTimer = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString());
    }, 1000);

    return () => {
      clearInterval(interval);
      clearInterval(timeTimer);
    };
  }, []);

  const isOnline = health.status === 'healthy';

  return (
    <header className="navbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <h1 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-primary)' }}>
          Air Quality & Pollution Risk Analytics
        </h1>
        <span
          style={{
            backgroundColor: 'var(--bg-subtle)',
            color: 'var(--text-secondary)',
            fontSize: '0.75rem',
            padding: '3px 8px',
            borderRadius: 'var(--radius-sm)',
            fontWeight: 600
          }}
        >
          UCI Sensor Lab
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>
          {currentTime}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '4px 10px',
              borderRadius: 'var(--radius-full)',
              fontSize: '0.78rem',
              fontWeight: 600,
              backgroundColor: isOnline ? '#ecfdf5' : '#fef2f2',
              color: isOnline ? '#059669' : '#dc2626',
              border: `1px solid ${isOnline ? '#a7f3d0' : '#fecaca'}`
            }}
          >
            {isOnline ? <CheckCircle2 size={13} /> : <AlertCircle size={13} />}
            {isOnline ? 'API & Model Online' : 'Backend Offline'}
          </span>

          <button
            onClick={checkStatus}
            title="Refresh status"
            style={{
              background: 'none',
              border: '1px solid var(--border-color)',
              borderRadius: 'var(--radius-md)',
              padding: '6px',
              cursor: 'pointer',
              color: 'var(--text-secondary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <RefreshCw size={14} />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
