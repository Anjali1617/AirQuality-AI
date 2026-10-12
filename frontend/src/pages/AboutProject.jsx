import React from 'react';
import {
  Info,
  Globe2,
  Cpu,
  Target,
  FileCheck2,
  Layers,
  HeartPulse,
  Building2,
  TreeDeciduous,
  AlertTriangle
} from 'lucide-react';

const AboutProject = () => {
  return (
    <div className="page-container">
      <div style={{ marginBottom: '28px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--text-primary)' }}>
          About AirQuality-AI System
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.94rem' }}>
          Air Quality and Pollution Risk Prediction System &mdash; Architectural Documentation & Environmental Research Overview.
        </p>
      </div>

      {/* Grid: Problem Statement & Objectives */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px', marginBottom: '28px' }}>
        <div className="panel">
          <div className="panel-header">
            <h3 className="panel-title">
              <AlertTriangle size={18} color="#f59e0b" /> Problem Statement
            </h3>
          </div>
          <p style={{ fontSize: '0.9rem', color: '#475569', lineHeight: 1.6 }}>
            Accurate urban air pollution assessment is traditionally constrained by the prohibitively high cost of certified reference monitoring stations (spectrophotometers and gas chromatographs). Solid-state chemical sensor arrays provide cost-effective alternative field deployments, but suffer from significant cross-sensitivity, non-linear calibration drift, and severe meteorological interference.
          </p>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3 className="panel-title">
              <Target size={18} color="#0d9488" /> Project Objectives
            </h3>
          </div>
          <ul style={{ paddingLeft: '20px', fontSize: '0.9rem', color: '#475569', lineHeight: 1.7 }}>
            <li>Ingest and preprocess multi-sensor chemical time-series data without data leakage.</li>
            <li>Train non-linear ensemble machine learning pipelines to reconstruct reference pollutant concentrations.</li>
            <li>Map predicted concentrations into documented environmental health risk bands.</li>
            <li>Deliver an accessible, real-time analytics dashboard with audited prediction history.</li>
          </ul>
        </div>
      </div>

      {/* Dataset & Critical Constraints */}
      <div className="panel" style={{ marginBottom: '28px' }}>
        <div className="panel-header">
          <h3 className="panel-title">
            <Globe2 size={18} color="#0d9488" /> Dataset Source & Transparency Notice
          </h3>
        </div>
        <p style={{ fontSize: '0.9rem', color: '#475569', lineHeight: 1.6, marginBottom: '16px' }}>
          <strong>Primary Benchmark Dataset:</strong> S. Vito, E. Massera, M. Piga, L. Martinotto, G. Di Francia (2008), <em>On field calibration of an electronic nose for benzene estimation in an urban environment</em>, Sensors and Actuators B: Chemical. Distributed via the UCI Machine Learning Repository under Creative Commons Attribution 4.0 International (CC BY 4.0).
        </p>
        <div className="alert alert-warning" style={{ margin: 0 }}>
          <Info size={20} />
          <div style={{ fontSize: '0.88rem' }}>
            <strong>Geographical Notice:</strong> The UCI dataset reflects historical observations recorded from an Italian city roadside station over 13 continuous months (March 2004 – April 2005). It is <em>not</em> live Indian or Ahmedabad real-time data. Predictions are based on the genuine physical sensor responses recorded during that observation period.
          </div>
        </div>
      </div>

      {/* Sustainable Development Goals (SDG) Alignment */}
      <div className="panel" style={{ marginBottom: '28px' }}>
        <div className="panel-header">
          <h3 className="panel-title">
            <HeartPulse size={18} color="#10b981" /> United Nations Sustainable Development Goals (SDG) Mapping
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
          <div style={{ padding: '18px', borderRadius: '10px', backgroundColor: '#ecfdf5', border: '1px solid #a7f3d0' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <HeartPulse size={22} color="#059669" />
              <h4 style={{ fontWeight: 700, color: '#065f46' }}>SDG 3: Good Health & Well-Being</h4>
            </div>
            <p style={{ fontSize: '0.86rem', color: '#047857', lineHeight: 1.5 }}>
              Target 3.9: Substantially reduce the number of deaths and illnesses from hazardous chemicals and air pollution through preventive exposure warnings.
            </p>
          </div>

          <div style={{ padding: '18px', borderRadius: '10px', backgroundColor: '#f0fdfa', border: '1px solid #99f6e4' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <Building2 size={22} color="#0d9488" />
              <h4 style={{ fontWeight: 700, color: '#115e59' }}>SDG 11: Sustainable Cities</h4>
            </div>
            <p style={{ fontSize: '0.86rem', color: '#0f766e', lineHeight: 1.5 }}>
              Target 11.6: Reduce the adverse per capita environmental impact of cities, by paying special attention to air quality and municipal environmental management.
            </p>
          </div>

          <div style={{ padding: '18px', borderRadius: '10px', backgroundColor: '#f0fdf4', border: '1px solid #bbf7d0' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <TreeDeciduous size={22} color="#16a34a" />
              <h4 style={{ fontWeight: 700, color: '#14532d' }}>SDG 13: Climate Action</h4>
            </div>
            <p style={{ fontSize: '0.86rem', color: '#15803d', lineHeight: 1.5 }}>
              Target 13.3: Improve education, awareness-raising, and institutional capacity on climate change mitigation, adaptation, impact reduction, and early warning.
            </p>
          </div>
        </div>
      </div>

      {/* Technology Stack Grid */}
      <div className="panel" style={{ marginBottom: '28px' }}>
        <div className="panel-header">
          <h3 className="panel-title">
            <Cpu size={18} color="#0d9488" /> Technology Architecture
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
          <div style={{ padding: '14px', borderRadius: '8px', backgroundColor: '#f8fafc', border: '1px solid #e2e8f0' }}>
            <strong style={{ color: '#0f172a' }}>Frontend</strong>
            <p style={{ fontSize: '0.84rem', color: '#64748b', marginTop: '4px' }}>React 18, Vite, React Router, CSS Design Tokens</p>
          </div>
          <div style={{ padding: '14px', borderRadius: '8px', backgroundColor: '#f8fafc', border: '1px solid #e2e8f0' }}>
            <strong style={{ color: '#0f172a' }}>Visualizations</strong>
            <p style={{ fontSize: '0.84rem', color: '#64748b', marginTop: '4px' }}>Recharts, Lucide React Icons</p>
          </div>
          <div style={{ padding: '14px', borderRadius: '8px', backgroundColor: '#f8fafc', border: '1px solid #e2e8f0' }}>
            <strong style={{ color: '#0f172a' }}>Backend API</strong>
            <p style={{ fontSize: '0.84rem', color: '#64748b', marginTop: '4px' }}>FastAPI, Uvicorn, Pydantic v2</p>
          </div>
          <div style={{ padding: '14px', borderRadius: '8px', backgroundColor: '#f8fafc', border: '1px solid #e2e8f0' }}>
            <strong style={{ color: '#0f172a' }}>Machine Learning</strong>
            <p style={{ fontSize: '0.84rem', color: '#64748b', marginTop: '4px' }}>Scikit-learn, Pandas, NumPy, Joblib</p>
          </div>
          <div style={{ padding: '14px', borderRadius: '8px', backgroundColor: '#f8fafc', border: '1px solid #e2e8f0' }}>
            <strong style={{ color: '#0f172a' }}>Persistence & Testing</strong>
            <p style={{ fontSize: '0.84rem', color: '#64748b', marginTop: '4px' }}>SQLite3 History, Pytest, FastAPI TestClient</p>
          </div>
        </div>
      </div>

      {/* Future Scope */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">
            <Layers size={18} color="#0d9488" /> Future Enhancement Scope
          </h3>
        </div>
        <ul style={{ paddingLeft: '20px', fontSize: '0.9rem', color: '#475569', lineHeight: 1.7 }}>
          <li>Integration with the Central Pollution Control Board (CPCB) India Open Data API for national particulate sub-indices (PM2.5 / PM10).</li>
          <li>Spatial dispersion Kriging interpolation across multi-sensor grid deployments.</li>
          <li>Automated model drift detection with progressive online learning.</li>
          <li>Exportable PDF compliance reports for municipal environmental audits.</li>
        </ul>
      </div>
    </div>
  );
};

export default AboutProject;
