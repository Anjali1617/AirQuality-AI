import React from 'react';
import { Activity, Wind, CloudRain, Cpu, AlertCircle } from 'lucide-react';

const iconMap = {
  observations: Activity,
  pollutant: Wind,
  reading: CloudRain,
  model: Cpu,
  default: Activity
};

const StatCard = ({ title, value, unit, subtext, trend, status = 'normal', iconType = 'default' }) => {
  const IconComponent = iconMap[iconType] || iconMap.default;

  return (
    <div className={`stat-card stat-status-${status}`}>
      <div>
        <div className="stat-header">
          <span className="stat-title">{title}</span>
          <div className="stat-icon">
            <IconComponent size={18} />
          </div>
        </div>
        <div className="stat-value-container">
          <span className="stat-value">{value}</span>
          {unit && <span className="stat-unit">{unit}</span>}
        </div>
        {subtext && <div className="stat-subtext">{subtext}</div>}
      </div>
      {trend && (
        <div style={{ marginTop: '12px', fontSize: '0.8rem', color: '#0d9488', fontWeight: 500 }}>
          {trend}
        </div>
      )}
    </div>
  );
};

export default StatCard;
