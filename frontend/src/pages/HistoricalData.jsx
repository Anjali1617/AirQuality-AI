import React, { useState, useEffect } from 'react';
import {
  Database,
  Search,
  Filter,
  ArrowUpDown,
  RefreshCw,
  FileSpreadsheet
} from 'lucide-react';
import { getHistoricalData } from '../services/api';
import DataTable from '../components/DataTable';
import LoadingSpinner from '../components/LoadingSpinner';

const columns = [
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' },
  { key: 'c6h6_gt', label: 'Benzene (µg/m³)' },
  { key: 'co_gt', label: 'CO (mg/m³)' },
  { key: 'nox_gt', label: 'NOx (ppb)' },
  { key: 'no2_gt', label: 'NO2 (µg/m³)' },
  { key: 'pt08_s2', label: 'S2 NMHC Sensor' },
  { key: 'temperature', label: 'Temp (°C)' },
  { key: 'humidity', label: 'Humidity (%)' },
  { key: 'risk_category', label: 'Risk Band' }
];

const HistoricalData = () => {
  const [data, setData] = useState([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('All');
  const [sortBy, setSortBy] = useState('datetime');
  const [sortOrder, setSortOrder] = useState('desc');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await getHistoricalData({
        page,
        page_size: pageSize,
        search: search || undefined,
        risk_category: riskFilter === 'All' ? undefined : riskFilter,
        sort_by: sortBy,
        sort_order: sortOrder
      });
      setData(res.records);
      setTotalRecords(res.total_records);
      setTotalPages(res.total_pages);
    } catch (err) {
      setError(err.message || 'Failed to fetch historical observations.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [page, pageSize, riskFilter, sortBy, sortOrder]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    fetchData();
  };

  return (
    <div className="page-container">
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
          Historical Observations Archive
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
          Explore 9,357 verified hourly chemical sensor readings recorded between March 2004 and April 2005. Missing readings (-200 sentinels) are safely represented as dashes.
        </p>
      </div>

      {/* Filter and Control Toolbar */}
      <div className="panel" style={{ padding: '18px 22px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', alignItems: 'center', justifyContent: 'space-between' }}>
          <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '8px', flex: '1', minWidth: '260px' }}>
            <div className="input-container" style={{ flex: 1 }}>
              <input
                type="text"
                placeholder="Search by date (DD/MM/YYYY) or time..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="form-input"
              />
            </div>
            <button type="submit" className="btn btn-primary" style={{ padding: '8px 16px', fontSize: '0.86rem' }}>
              <Search size={15} /> Search
            </button>
          </form>

          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '0.84rem', color: '#64748b', fontWeight: 500 }}>Risk Filter:</span>
              <select
                value={riskFilter}
                onChange={(e) => { setRiskFilter(e.target.value); setPage(1); }}
                className="form-input"
                style={{ padding: '6px 12px', fontSize: '0.86rem', width: 'auto' }}
              >
                <option value="All">All Categories</option>
                <option value="Low">Low Risk</option>
                <option value="Moderate">Moderate Risk</option>
                <option value="High">High Risk</option>
                <option value="Very High">Very High Risk</option>
              </select>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '0.84rem', color: '#64748b', fontWeight: 500 }}>Sort By:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="form-input"
                style={{ padding: '6px 12px', fontSize: '0.86rem', width: 'auto' }}
              >
                <option value="datetime">Timestamp</option>
                <option value="benzene">Benzene C₆H₆</option>
                <option value="co">Carbon Monoxide CO</option>
                <option value="temperature">Temperature</option>
              </select>
              <button
                type="button"
                onClick={() => setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc')}
                className="btn btn-secondary"
                title={`Sorting ${sortOrder.toUpperCase()}`}
                style={{ padding: '6px 10px' }}
              >
                <ArrowUpDown size={14} />
              </button>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '0.84rem', color: '#64748b', fontWeight: 500 }}>Rows:</span>
              <select
                value={pageSize}
                onChange={(e) => { setPageSize(Number(e.target.value)); setPage(1); }}
                className="form-input"
                style={{ padding: '6px 10px', fontSize: '0.86rem', width: 'auto' }}
              >
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={50}>50</option>
              </select>
            </div>

            <button
              onClick={fetchData}
              className="btn btn-secondary"
              style={{ padding: '6px 12px', fontSize: '0.84rem' }}
              title="Refresh dataset"
            >
              <RefreshCw size={14} />
            </button>
          </div>
        </div>
      </div>

      {/* Dataset Table Panel */}
      <div className="panel">
        <DataTable
          columns={columns}
          data={data}
          totalRecords={totalRecords}
          page={page}
          pageSize={pageSize}
          totalPages={totalPages}
          onPageChange={(newPage) => setPage(newPage)}
          loading={loading}
        />
      </div>
    </div>
  );
};

export default HistoricalData;
