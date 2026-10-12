import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  RefreshCw,
  Gauge,
  Sliders,
  ShieldCheck,
  Flame,
  AlertOctagon
} from 'lucide-react';
import { getDashboardSummary, getPredictionHistory } from '../services/api';
import StatCard from '../components/StatCard';
import PollutionChart from '../components/PollutionChart';
import RiskBadge from '../components/RiskBadge';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [recentHistory, setRecentHistory] = useState([]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [summary, history] = await Promise.all([
        getDashboardSummary(),
        getPredictionHistory(5).catch(() => [])
      ]);
      setDashboardData(summary);
      setRecentHistory(history);
    } catch (err) {
      setError(err.message || 'Unable to connect to AirQuality-AI backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return <LoadingSpinner message="Aggregating air quality observations & model metrics..." fullPage />;
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="panel" style={{ textAlign: 'center', padding: '48px 24px' }}>
          <AlertTriangle size={48} color="#ef4444" style={{ marginBottom: '16px' }} />
          <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '8px' }}>
            Backend Connection Unavailable
          </h2>
          <p style={{ color: '#64748b', maxWidth: '500px', margin: '0 auto 24px' }}>
            {error} Make sure the FastAPI service is running at <code>http://localhost:8000</code>.
          </p>
          <button className="btn btn-primary" onClick={fetchData}>
            <RefreshCw size={16} /> Retry Connection
          </button>
        </div>
      </div>
    );
  }

  const { stat_cards, trend_data, risk_distribution, latest_reading, model_status } = dashboardData;

  return (
    <div className="page-container">
      {/* Top Banner Notice */}
      <div className="alert alert-info" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <strong>Ground-Truth Dataset Active:</strong> Analyzing 9,357 verified hourly chemical sensor readings from the UCI Air Quality repository. No simulated data.
        </div>
        <Link to="/predict" className="btn btn-primary" style={{ padding: '6px 14px', fontSize: '0.84rem' }}>
          <Gauge size={14} /> Predict Pollution
        </Link>
      </div>

      {/* Primary Stat Cards */}
      <div className="stats-grid">
        {stat_cards.map((card, idx) => (
          <StatCard
            key={idx}
            title={card.title}
            value={card.value}
            unit={card.unit}
            subtext={card.subtext}
            trend={card.trend}
            status={card.status}
            iconType={idx === 0 ? 'observations' : idx === 1 ? 'pollutant' : idx === 2 ? 'reading' : 'model'}
          />
        ))}
      </div>

      {/* Charts Section: 72-Hour Trend */}
      <div className="panel">
        <div className="panel-header">
          <div>
            <h2 className="panel-title">
              <Activity size={20} color="#0d9488" /> Atmospheric Multi-Pollutant Trend
            </h2>
            <p className="panel-subtitle">
              Chronological hourly concentrations of Benzene (C₆H₆) and Carbon Monoxide (CO)
            </p>
          </div>
          <button
            onClick={fetchData}
            className="btn btn-secondary"
            style={{ padding: '6px 12px', fontSize: '0.82rem' }}
          >
            <RefreshCw size={14} /> Refresh
          </button>
        </div>

        <PollutionChart
          data={trend_data}
          lines={[
            { key: 'benzene', name: 'Benzene C₆H₆ (µg/m³)', color: '#0d9488' },
            { key: 'co', name: 'Carbon Monoxide CO (mg/m³)', color: '#f59e0b' }
          ]}
          height={320}
        />
      </div>

      {/* Grid: Risk Category Breakdown & Recent Predictions */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px' }}>
        {/* Risk Distribution Card */}
        <div className="panel">
          <div className="panel-header">
            <h3 className="panel-title">
              <ShieldCheck size={18} color="#10b981" /> Historical Risk Category Distribution
            </h3>
          </div>
          <p style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '18px' }}>
            Based on European Environment Agency annual limits (&lt;5 µg/m³ = Low, 5–10 = Moderate, 10–20 = High, &gt;20 = Very High).
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {risk_distribution.map((item) => (
              <div key={item.category}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', fontSize: '0.86rem' }}>
                  <span style={{ fontWeight: 600 }}>{item.category}</span>
                  <span style={{ color: '#64748b' }}>
                    {item.count.toLocaleString()} records ({item.percentage}%)
                  </span>
                </div>
                <div style={{ width: '100%', height: '8px', backgroundColor: '#f1f5f9', borderRadius: '4px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${item.percentage}%`,
                      height: '100%',
                      backgroundColor: item.color,
                      borderRadius: '4px'
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Prediction Quick Action / Recent History */}
        <div className="panel">
          <div className="panel-header">
            <h3 className="panel-title">
              <Sliders size={18} color="#0d9488" /> Recent Prediction Logs
            </h3>
            <Link to="/predict" style={{ fontSize: '0.82rem', color: '#0d9488', textDecoration: 'none', fontWeight: 600 }}>
              New Prediction &rarr;
            </Link>
          </div>

          {recentHistory.length === 0 ? (
            <div style={{ padding: '32px 16px', textAlign: 'center', color: '#94a3b8' }}>
              <p style={{ fontSize: '0.9rem', marginBottom: '12px' }}>No predictions run in this session yet.</p>
              <Link to="/predict" className="btn btn-secondary" style={{ fontSize: '0.84rem' }}>
                Run Model Inference
              </Link>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {recentHistory.map((rec) => (
                <div
                  key={rec.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '10px 14px',
                    borderRadius: '8px',
                    backgroundColor: '#f8fafc',
                    border: '1px solid #e2e8f0'
                  }}
                >
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.94rem' }}>
                      {rec.predicted_concentration} {rec.unit}
                    </div>
                    <div style={{ fontSize: '0.76rem', color: '#94a3b8' }}>
                      {new Date(rec.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                    </div>
                  </div>
                  <RiskBadge category={rec.risk_category} />
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
