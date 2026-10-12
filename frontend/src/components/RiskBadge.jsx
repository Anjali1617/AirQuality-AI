import React from 'react';
import { ShieldCheck, AlertTriangle, AlertOctagon, Flame } from 'lucide-react';

const RiskBadge = ({ category = 'Low' }) => {
  const getBadgeConfig = (cat) => {
    switch (cat?.toLowerCase()) {
      case 'low':
        return {
          className: 'badge badge-low',
          icon: <ShieldCheck size={14} />,
          label: 'Low Risk'
        };
      case 'moderate':
        return {
          className: 'badge badge-moderate',
          icon: <AlertTriangle size={14} />,
          label: 'Moderate Risk'
        };
      case 'high':
        return {
          className: 'badge badge-high',
          icon: <Flame size={14} />,
          label: 'High Risk'
        };
      case 'very high':
      case 'very_high':
        return {
          className: 'badge badge-very-high',
          icon: <AlertOctagon size={14} />,
          label: 'Very High Risk'
        };
      default:
        return {
          className: 'badge',
          icon: null,
          label: category || 'Unknown'
        };
    }
  };

  const config = getBadgeConfig(category);

  return (
    <span className={config.className}>
      {config.icon}
      <span>{config.label}</span>
    </span>
  );
};

export default RiskBadge;
