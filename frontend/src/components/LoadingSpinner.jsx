import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ message = 'Loading environmental data...', fullPage = false }) => {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: fullPage ? '80px 20px' : '40px 20px',
        gap: '12px',
        color: '#475569'
      }}
    >
      <Loader2
        size={32}
        className="animate-spin"
        style={{
          color: '#0d9488',
          animation: 'spin 1s linear infinite'
        }}
      />
      <span style={{ fontSize: '0.92rem', fontWeight: 500 }}>{message}</span>
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default LoadingSpinner;
