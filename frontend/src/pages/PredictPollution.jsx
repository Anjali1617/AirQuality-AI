import React, { useState, useEffect } from 'react';
import {
  Gauge,
  Sparkles,
  RefreshCw,
  AlertCircle,
  CheckCircle2,
  Sliders,
  History,
  Info
} from 'lucide-react';
import { createPrediction, getPredictionHistory } from '../services/api';
import FormField from '../components/FormField';
import RiskBadge from '../components/RiskBadge';
import LoadingSpinner from '../components/LoadingSpinner';

const benchmarkPresets = {
  moderate: {
    label: 'Typical Observation (Moderate)',
    values: {
      'PT08.S1(CO)': 1046,
      'PT08.S2(NMHC)': 909,
      'PT08.S3(NOx)': 806,
      'PT08.S4(NO2)': 1463,
      'PT08.S5(O3)': 963,
      T: 17.8,
      RH: 49.6,
      AH: 0.995,
      Hour: 14,
      DayOfWeek: 2
    }
  },
  low: {
    label: 'Clean Air / Low Exposure',
    values: {
      'PT08.S1(CO)': 780,
      'PT08.S2(NMHC)': 580,
      'PT08.S3(NOx)': 1400,
      'PT08.S4(NO2)': 1100,
      'PT08.S5(O3)': 550,
      T: 14.5,
      RH: 58.0,
      AH: 0.72,
      Hour: 4,
      DayOfWeek: 6
    }
  },
  high: {
    label: 'Rush Hour Congestion (High)',
    values: {
      'PT08.S1(CO)': 1550,
      'PT08.S2(NMHC)': 1450,
      'PT08.S3(NOx)': 650,
      'PT08.S4(NO2)': 1850,
      'PT08.S5(O3)': 1600,
      T: 19.5,
      RH: 64.0,
      AH: 1.25,
      Hour: 19,
      DayOfWeek: 4
    }
  }
};

const PredictPollution = () => {
  const [formData, setFormData] = useState({
    'PT08.S1(CO)': 1046,
    'PT08.S2(NMHC)': 909,
    'PT08.S3(NOx)': 806,
    'PT08.S4(NO2)': 1463,
    'PT08.S5(O3)': 963,
    T: 17.8,
    RH: 49.6,
    AH: 0.995,
    Hour: 14,
    DayOfWeek: 2
  });

  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [predictionResult, setPredictionResult] = useState(null);
  const [apiError, setApiError] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const fetchHistory = async () => {
    setLoadingHistory(true);
    try {
      const data = await getPredictionHistory(10);
      setHistory(data);
    } catch {
      // Ignore initial history failure
    } finally {
      setLoadingHistory(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value === '' ? '' : Number(value)
    }));

    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  const loadPreset = (presetKey) => {
    setFormData(benchmarkPresets[presetKey].values);
    setErrors({});
    setApiError(null);
  };

  const validate = () => {
    const errs = {};
    if (formData['PT08.S2(NMHC)'] === '' || formData['PT08.S2(NMHC)'] < 200 || formData['PT08.S2(NMHC)'] > 3000) {
      errs['PT08.S2(NMHC)'] = 'Titania sensor value should be between 200 and 3,000.';
    }
    if (formData.T !== '' && (formData.T < -20 || formData.T > 60)) {
      errs.T = 'Temperature must be between -20°C and 60°C.';
    }
    if (formData.RH !== '' && (formData.RH < 0 || formData.RH > 100)) {
      errs.RH = 'Relative Humidity must be between 0% and 100%.';
    }
    if (formData.Hour !== '' && (formData.Hour < 0 || formData.Hour > 23)) {
      errs.Hour = 'Hour must be between 0 and 23.';
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    setApiError(null);

    try {
      const res = await createPrediction(formData);
      setPredictionResult(res);
      fetchHistory();
    } catch (err) {
      setApiError(err.response?.data?.detail || err.message || 'Prediction request failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page-container">
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
          Pollution Concentration & Risk Predictor
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
          Estimate continuous Benzene (C₆H₆) concentration and categorized health risk from multi-sensor responses.
        </p>
      </div>

      {/* Preset Quick Fill Buttons */}
      <div className="panel" style={{ padding: '16px 20px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <span style={{ fontSize: '0.88rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
            Quick Benchmark Presets:
          </span>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {Object.entries(benchmarkPresets).map(([k, p]) => (
              <button
                key={k}
                type="button"
                onClick={() => loadPreset(k)}
                className="btn btn-secondary"
                style={{ padding: '6px 14px', fontSize: '0.82rem' }}
              >
                <Sparkles size={14} color="#0d9488" /> {p.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '28px' }}>
        {/* Input Form */}
        <div className="panel">
          <div className="panel-header">
            <h3 className="panel-title">
              <Sliders size={18} color="#0d9488" /> Sensor Responses & Meteorological Inputs
            </h3>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <FormField
                label="PT08.S2 (NMHC/C6H6 Sensor)"
                name="PT08.S2(NMHC)"
                value={formData['PT08.S2(NMHC)']}
                onChange={handleChange}
                placeholder="e.g. 909"
                unit="res."
                helperText="Primary Titania hydrocarbon sensor (Key predictor)"
                error={errors['PT08.S2(NMHC)']}
                required
              />

              <FormField
                label="PT08.S1 (CO Sensor)"
                name="PT08.S1(CO)"
                value={formData['PT08.S1(CO)']}
                onChange={handleChange}
                placeholder="e.g. 1046"
                unit="res."
                helperText="Tin oxide multi-sensor response"
              />

              <FormField
                label="PT08.S3 (NOx Sensor)"
                name="PT08.S3(NOx)"
                value={formData['PT08.S3(NOx)']}
                onChange={handleChange}
                placeholder="e.g. 806"
                unit="res."
                helperText="Tungsten oxide multi-sensor response"
              />

              <FormField
                label="PT08.S4 (NO2 Sensor)"
                name="PT08.S4(NO2)"
                value={formData['PT08.S4(NO2)']}
                onChange={handleChange}
                placeholder="e.g. 1463"
                unit="res."
                helperText="Tungsten oxide multi-sensor response"
              />

              <FormField
                label="PT08.S5 (O3 Sensor)"
                name="PT08.S5(O3)"
                value={formData['PT08.S5(O3)']}
                onChange={handleChange}
                placeholder="e.g. 963"
                unit="res."
                helperText="Indium oxide multi-sensor response"
              />

              <FormField
                label="Ambient Temperature (T)"
                name="T"
                value={formData.T}
                onChange={handleChange}
                placeholder="e.g. 17.8"
                unit="°C"
                helperText="Sensor array housing temperature"
                error={errors.T}
              />

              <FormField
                label="Relative Humidity (RH)"
                name="RH"
                value={formData.RH}
                onChange={handleChange}
                placeholder="e.g. 49.6"
                unit="%"
                helperText="Atmospheric relative humidity"
                error={errors.RH}
              />

              <FormField
                label="Absolute Humidity (AH)"
                name="AH"
                value={formData.AH}
                onChange={handleChange}
                placeholder="e.g. 0.995"
                unit="g/m³"
                helperText="Specific air moisture content"
              />

              <FormField
                label="Hour of the Day"
                name="Hour"
                value={formData.Hour}
                onChange={handleChange}
                placeholder="0-23"
                unit="hr"
                helperText="Local observation hour (0 to 23)"
                error={errors.Hour}
              />

              <FormField
                label="Day of Week"
                name="DayOfWeek"
                value={formData.DayOfWeek}
                onChange={handleChange}
                placeholder="0-6"
                unit="day"
                helperText="0=Monday, 6=Sunday"
              />
            </div>

            {apiError && (
              <div className="alert alert-error">
                <AlertCircle size={18} />
                <span>{apiError}</span>
              </div>
            )}

            <button
              type="submit"
              className="btn btn-primary"
              disabled={submitting}
              style={{ width: '100%', padding: '12px', fontSize: '1rem' }}
            >
              {submitting ? 'Running ML Inference...' : 'Predict Concentration & Health Risk'}
            </button>
          </form>
        </div>

        {/* Prediction Results Display */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="panel" style={{ flex: 1 }}>
            <div className="panel-header">
              <h3 className="panel-title">
                <Gauge size={18} color="#0d9488" /> Prediction Outcome
              </h3>
            </div>

            {!predictionResult ? (
              <div style={{ padding: '60px 20px', textAlign: 'center', color: '#94a3b8' }}>
                <Gauge size={44} style={{ marginBottom: '12px', opacity: 0.5 }} />
                <p style={{ fontSize: '0.95rem' }}>Submit the form to compute real-time model inference.</p>
                <span style={{ fontSize: '0.8rem', display: 'block', marginTop: '6px' }}>
                  Pipeline: Random Forest Regressor (Trained on authentic UCI data)
                </span>
              </div>
            ) : (
              <div>
                <div
                  style={{
                    padding: '24px',
                    borderRadius: 'var(--radius-lg)',
                    backgroundColor: 'var(--bg-subtle)',
                    border: '1px solid var(--border-color)',
                    marginBottom: '20px',
                    textAlign: 'center'
                  }}
                >
                  <div style={{ fontSize: '0.86rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>
                    Predicted {predictionResult.target_name}
                  </div>
                  <div style={{ fontSize: '2.8rem', fontWeight: 800, color: '#0f172a', margin: '8px 0' }}>
                    {predictionResult.predicted_concentration}{' '}
                    <span style={{ fontSize: '1.2rem', fontWeight: 600, color: '#64748b' }}>
                      {predictionResult.unit}
                    </span>
                  </div>
                  <div style={{ display: 'inline-block', marginTop: '6px' }}>
                    <RiskBadge category={predictionResult.risk_category} />
                  </div>
                </div>

                <div className="alert alert-info" style={{ marginBottom: '16px' }}>
                  <Info size={20} />
                  <div style={{ fontSize: '0.88rem' }}>
                    <strong>Risk Advisory:</strong> {predictionResult.risk_description}
                  </div>
                </div>

                <div style={{ fontSize: '0.82rem', color: '#64748b', borderTop: '1px solid #e2e8f0', paddingTop: '12px' }}>
                  <div><strong>Model Version:</strong> {predictionResult.model_version}</div>
                  <div><strong>Prediction Target:</strong> {predictionResult.target}</div>
                  <div><strong>Audited:</strong> Logged to local SQLite database</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Prediction History Table */}
      <div className="panel" style={{ marginTop: '28px' }}>
        <div className="panel-header">
          <h3 className="panel-title">
            <History size={18} color="#0d9488" /> Session Prediction History
          </h3>
          <button
            onClick={fetchHistory}
            className="btn btn-secondary"
            style={{ padding: '6px 12px', fontSize: '0.82rem' }}
          >
            <RefreshCw size={14} /> Refresh
          </button>
        </div>

        {history.length === 0 ? (
          <div style={{ padding: '32px', textAlign: 'center', color: '#94a3b8' }}>
            No past prediction history recorded yet.
          </div>
        ) : (
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Timestamp</th>
                  <th>Target</th>
                  <th>Predicted Concentration</th>
                  <th>Risk Category</th>
                  <th>Model Version</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.id}>
                    <td>#{item.id}</td>
                    <td>{new Date(item.timestamp).toLocaleString()}</td>
                    <td>{item.target}</td>
                    <td><strong>{item.predicted_concentration} {item.unit}</strong></td>
                    <td><RiskBadge category={item.risk_category} /></td>
                    <td><code>{item.model_version}</code></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictPollution;
