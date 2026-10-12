import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import RiskBadge from './RiskBadge';

const DataTable = ({
  columns = [],
  data = [],
  totalRecords = 0,
  page = 1,
  pageSize = 20,
  totalPages = 1,
  onPageChange,
  loading = false
}) => {
  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>
        Loading records...
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#94a3b8' }}>
        No historical records found matching filter criteria.
      </div>
    );
  }

  return (
    <div>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.key}>{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={row.id ?? idx}>
                {columns.map((col) => {
                  const val = row[col.key];
                  if (col.key === 'risk_category') {
                    return (
                      <td key={col.key}>
                        <RiskBadge category={val} />
                      </td>
                    );
                  }
                  return (
                    <td key={col.key}>
                      {val !== null && val !== undefined ? String(val) : <span style={{ color: '#cbd5e1' }}>—</span>}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="pagination-bar">
          <div style={{ fontSize: '0.84rem', color: '#64748b' }}>
            Showing page <strong>{page}</strong> of <strong>{totalPages}</strong> ({totalRecords.toLocaleString()} total entries)
          </div>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              className="btn btn-secondary"
              style={{ padding: '6px 12px', fontSize: '0.84rem' }}
              disabled={page <= 1}
              onClick={() => onPageChange && onPageChange(page - 1)}
            >
              <ChevronLeft size={16} /> Previous
            </button>
            <button
              className="btn btn-secondary"
              style={{ padding: '6px 12px', fontSize: '0.84rem' }}
              disabled={page >= totalPages}
              onClick={() => onPageChange && onPageChange(page + 1)}
            >
              Next <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataTable;
