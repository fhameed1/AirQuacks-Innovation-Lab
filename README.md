# Industrial IoT Analytics Platform

A real-time industrial IoT sensor monitoring and analytics platform that demonstrates modern data stack integration using FastAPI, Airbyte, and Motherduck.

## Project Components

### 1. IoT Sensor Simulator (FastAPI)
- Simulates industrial machine sensor data
- Generates temperature, vibration, and RPM readings
- Includes anomaly simulation
- REST API endpoints for single and batch readings

### 2. Data Pipeline
- Uses Airbyte Cloud for data ingestion
- ngrok for exposing local API
- Motherduck (DuckDB) for analytics storage
- Real-time data processing and analysis

### 3. Analytics Dashboard (Streamlit)
- Real-time sensor monitoring
- Interactive visualizations
- Anomaly detection
- Natural language querying using Motherduck's pragma prompt_query

## Setup Instructions

### Prerequisites
- Python 3.9+
- ngrok account
- Airbyte Cloud account
- Motherduck account

### Environment Setup
```bash
# Create conda environment
conda create -n iot-dashboard python=3.9
conda activate iot-dashboard

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

1. Start the FastAPI Sensor Simulator:
```bash
python edge_gateway.py
```

2. Expose API using ngrok:
```bash
ngrok http 8001
```

3. Configure Airbyte Cloud:
- Create a new custom source
- Use the ngrok URL as the base URL
- Configure sync to Motherduck destination

4. Run the Streamlit Dashboard:
```bash
streamlit run app.py
```

## Project Structure
```
.
├── README.md
├── requirements.txt
├── edge_gateway.py          # FastAPI sensor simulator
├── app.py                   # Streamlit dashboard
└── sql/
    └── schema.sql          # Database schema and transformations
```

## Requirements
```
fastapi>=0.68.0
uvicorn>=0.15.0
streamlit==1.24.0
plotly
duckdb
pandas
```

## Database Schema

### Raw Data Table
```sql
CREATE TABLE sensor_data_flattened (
    rpm FLOAT,
    temperature FLOAT,
    vibration FLOAT,
    timestamp TIMESTAMP,
    machine_id VARCHAR,
    status VARCHAR,
    _airbyte_raw_id VARCHAR
);
```

## Features
- Real-time sensor data simulation
- Automated data pipeline using Airbyte
- Interactive analytics dashboard
- Natural language data querying
- Anomaly detection
- Time-series visualizations

## Demo Setup Guide

1. Clone the repository
2. Set up the conda environment
3. Configure your Motherduck token
4. Start the FastAPI server
5. Set up ngrok tunnel
6. Configure Airbyte connection
7. Launch the Streamlit dashboard

## Notes
- The FastAPI server runs on port 8001
- Ensure your Motherduck token is properly configured
- Keep the ngrok tunnel running for Airbyte connectivity
- Monitor the Airbyte sync logs for data pipeline health

## Future Enhancements
- Multiple machine simulation
- Advanced anomaly detection algorithms
- Predictive maintenance features
- Additional sensor types
- Machine learning integration

## Contributing
Feel free to submit issues and enhancement requests!