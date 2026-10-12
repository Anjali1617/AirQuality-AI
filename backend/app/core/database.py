"""
SQLite persistence for prediction audit history.
"""

import sqlite3
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.core.config import settings


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes SQLite tables for prediction audit history.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            target TEXT NOT NULL,
            predicted_concentration REAL NOT NULL,
            unit TEXT NOT NULL,
            risk_category TEXT NOT NULL,
            risk_color TEXT NOT NULL,
            risk_description TEXT,
            inputs_json TEXT NOT NULL,
            model_version TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_prediction(
    target: str,
    predicted_concentration: float,
    unit: str,
    risk_category: str,
    risk_color: str,
    risk_description: str,
    inputs: Dict[str, Any],
    model_version: str = "1.0.0"
) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
        INSERT INTO prediction_history (
            timestamp, target, predicted_concentration, unit,
            risk_category, risk_color, risk_description, inputs_json, model_version
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now_iso, target, predicted_concentration, unit,
        risk_category, risk_color, risk_description, json.dumps(inputs), model_version
    ))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def get_recent_predictions(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, target, predicted_concentration, unit,
               risk_category, risk_color, risk_description, inputs_json, model_version
        FROM prediction_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "target": r["target"],
            "predicted_concentration": r["predicted_concentration"],
            "unit": r["unit"],
            "risk_category": r["risk_category"],
            "risk_color": r["risk_color"],
            "risk_description": r["risk_description"],
            "inputs": json.loads(r["inputs_json"]),
            "model_version": r["model_version"]
        })
    return history
