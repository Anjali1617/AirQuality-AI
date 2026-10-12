import React from 'react';

const FormField = ({
  label,
  name,
  value,
  onChange,
  type = 'number',
  step = 'any',
  placeholder,
  unit,
  helperText,
  error,
  required = false
}) => {
  return (
    <div className="form-group">
      <label className="form-label" htmlFor={name}>
        {label} {required && <span style={{ color: '#ef4444' }}>*</span>}
      </label>
      <div className="input-container">
        <input
          id={name}
          name={name}
          type={type}
          step={step}
          value={value ?? ''}
          onChange={onChange}
          placeholder={placeholder}
          className="form-input"
          style={error ? { borderColor: '#ef4444' } : {}}
        />
        {unit && <span className="input-unit">{unit}</span>}
      </div>
      {error && <span style={{ color: '#ef4444', fontSize: '0.78rem' }}>{error}</span>}
      {helperText && !error && <span className="form-helper">{helperText}</span>}
    </div>
  );
};

export default FormField;
