import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Gauge,
  Database,
  LineChart,
  Info,
  Wind
} from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/predict', label: 'Predict Pollution', icon: Gauge },
    { path: '/history', label: 'Historical Data', icon: Database },
    { path: '/performance', label: 'Model Performance', icon: LineChart },
    { path: '/about', label: 'About Project', icon: Info },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon-wrapper">
          <Wind size={22} />
        </div>
        <div>
          <div className="brand-title">AirQuality-AI</div>
          <div className="brand-subtitle">Risk Prediction System</div>
        </div>
      </div>

      <ul className="nav-menu">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <li key={item.path} className="nav-item">
              <NavLink
                to={item.path}
                className={({ isActive }) => (isActive ? 'active' : '')}
                end={item.path === '/'}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </NavLink>
            </li>
          );
        })}
      </ul>

      <div className="sidebar-footer">
        <div><strong>Dataset:</strong> UCI Air Quality</div>
        <div><strong>Target:</strong> Benzene (C₆H₆)</div>
        <div style={{ marginTop: '4px' }}><strong>Status:</strong> Active Pipeline</div>
      </div>
    </aside>
  );
};

export default Sidebar;
