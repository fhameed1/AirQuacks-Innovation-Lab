import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Duck theme colors - simplified palette
DUCK_COLORS = {
    'primary': '#4682B4',
    'secondary': '#FFA500',
    'accent': '#228B22'
}

# Page config - using wide layout
st.set_page_config(page_title="IoT Sensor Analytics", layout="wide", initial_sidebar_state="collapsed")

# Minimal CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4682B4;
        color: white;
        border: none;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #4682B4;
    }
    .streamlit-expanderHeader {
        background-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize connection
load_dotenv()

@st.cache(allow_output_mutation=True)
def init_connection():
    token = os.getenv('MOTHERDUCK_TOKEN')
    database = 'my_db'
    schema = 'main'
    conn = duckdb.connect(f'md:{database}?motherduck_token={token}')
    conn.execute(f'SET search_path = {schema}')
    return conn

conn = init_connection()

# Header with single logo aligned with title
col1, col2 = st.columns([3, 1])

with col1:
    st.write("")  # Add some padding
    st.title("IoT Sensor Analytics")

with col2:
    # Custom CSS to align logo
    st.markdown("""
        <style>
        [data-testid="column"] {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    try:
        st.image("assets/logo.png", width=120)  # Increased size from 80 to 120
    except Exception as e:
        st.error(f"Could not load logo: {str(e)}")

# Sidebar controls with minimal styling
with st.sidebar:
    st.markdown("### Dashboard Controls")
    
    machines_query = "SELECT DISTINCT machine_id FROM sensor_data_flattened ORDER BY machine_id"
    machines = conn.execute(machines_query).fetchall()
    machine_ids = [m[0] for m in machines]
    selected_machines = st.multiselect("Select Machines", machine_ids, default=machine_ids[:3])

    st.markdown("### Time Range")
    time_ranges = {
        "Last Hour": timedelta(hours=1),
        "Last 4 Hours": timedelta(hours=4),
        "Last 12 Hours": timedelta(hours=12),
        "Last 24 Hours": timedelta(hours=24),
        "Last Week": timedelta(days=7)
    }
    selected_range = st.select_slider(
        "Select Time Range",
        options=list(time_ranges.keys()),
        value="Last 4 Hours"
    )

    temp_query = """
        SELECT MIN(temperature) as min_temp, MAX(temperature) as max_temp 
        FROM sensor_data_flattened
    """
    temp_range = conn.execute(temp_query).fetchone()
    temp_min, temp_max = st.slider(
        "Temperature Range (°C)",
        float(temp_range[0]), float(temp_range[1]),
        (float(temp_range[0]), float(temp_range[1]))
    )

# Key Metrics with minimal decoration
metrics_query = f"""
    SELECT 
        AVG(temperature) as avg_temp,
        AVG(vibration) as avg_vib,
        AVG(rpm) as avg_rpm
    FROM sensor_data_flattened
    WHERE machine_id IN ({','.join([f"'{m}'" for m in selected_machines])})
    AND temperature BETWEEN {temp_min} AND {temp_max}
"""
metrics = conn.execute(metrics_query).fetchone()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Temperature", f"{metrics[0]:.1f}°C")
with col2:
    st.metric("Vibration", f"{metrics[1]:.2f}")
with col3:
    st.metric("RPM", f"{metrics[2]:.0f}")

# Charts section with minimal headers
col1, col2 = st.columns(2)

with col1:
    st.subheader("Temperature Trends")
    query = f"""
    SELECT 
        timestamp,
        temperature,
        machine_id
    FROM sensor_data_flattened
    WHERE machine_id IN ({','.join([f"'{m}'" for m in selected_machines])})
    AND temperature BETWEEN {temp_min} AND {temp_max}
    ORDER BY timestamp DESC
    """
    df_temp = conn.execute(query).df()
    fig_temp = px.line(df_temp, x='timestamp', y='temperature', color='machine_id',
                       color_discrete_sequence=[DUCK_COLORS['primary'], DUCK_COLORS['secondary'], DUCK_COLORS['accent']])
    fig_temp.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    st.subheader("Sensor Analysis")
    chart_type = st.radio("View", ["Scatter", "3D"], horizontal=True)
    
    if chart_type == "Scatter":
        query = f"""
        SELECT 
            vibration,
            rpm,
            machine_id,
            temperature
        FROM sensor_data_flattened
        WHERE machine_id IN ({','.join([f"'{m}'" for m in selected_machines])})
        AND temperature BETWEEN {temp_min} AND {temp_max}
        """
        df_vib = conn.execute(query).df()
        fig_vib = px.scatter(df_vib, x='rpm', y='vibration', color='temperature',
                            color_continuous_scale=['blue', 'orange'])
        fig_vib.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20)
        )
    else:
        query = f"""
        SELECT 
            vibration,
            rpm,
            temperature,
            machine_id
        FROM sensor_data_flattened
        WHERE machine_id IN ({','.join([f"'{m}'" for m in selected_machines])})
        AND temperature BETWEEN {temp_min} AND {temp_max}
        """
        df_3d = conn.execute(query).df()
        fig_vib = px.scatter_3d(df_3d, x='rpm', y='vibration', z='temperature',
                               color='machine_id',
                               color_discrete_sequence=[DUCK_COLORS['primary'], DUCK_COLORS['secondary'], DUCK_COLORS['accent']])
        fig_vib.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )
    
    st.plotly_chart(fig_vib, use_container_width=True)

# Natural Language Query with minimal decoration
with st.expander("Ask the Duck"):
    user_query = st.text_input("Ask a question about your sensor data:",
                              placeholder="e.g., What is the average temperature of Machine_001?")
    if user_query:
        with st.spinner('Analyzing...'):
            try:
                query = f"pragma prompt_query('{user_query}');"
                result = conn.execute(query).df()
                st.dataframe(result)
            except Exception as e:
                st.error(f"Query error: {str(e)}")

# Anomaly Detection in expander
with st.expander("Anomaly Detection"):
    std_dev_threshold = st.slider("Sensitivity (Standard Deviations)", 1.0, 5.0, 2.0, 0.1)

    anomaly_query = f"""
    WITH stats AS (
        SELECT 
            machine_id,
            avg(temperature) as mean_temp,
            stddev(temperature) as std_temp,
            avg(vibration) as mean_vib,
            stddev(vibration) as std_vib
        FROM sensor_data_flattened
        WHERE machine_id IN ({','.join([f"'{m}'" for m in selected_machines])})
        GROUP BY 1
    )
    SELECT 
        f.*,
        CASE 
            WHEN abs(f.temperature - s.mean_temp) > {std_dev_threshold} * s.std_temp 
            OR abs(f.vibration - s.mean_vib) > {std_dev_threshold} * s.std_vib
            THEN true 
            ELSE false 
        END as is_anomaly
    FROM sensor_data_flattened f
    JOIN stats s ON f.machine_id = s.machine_id
    WHERE is_anomaly = true
    AND f.machine_id IN ({','.join([f"'{m}'" for m in selected_machines])})
    ORDER BY timestamp DESC
    LIMIT 10
    """
    anomalies = conn.execute(anomaly_query).df()
    if not anomalies.empty:
        st.dataframe(anomalies.style.highlight_max(axis=0, subset=['temperature', 'vibration'], color='#4682B4'))
    else:
        st.info("No anomalies detected with current settings.")