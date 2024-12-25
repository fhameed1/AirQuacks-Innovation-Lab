CREATE OR REPLACE TABLE sensor_data_flattened AS
SELECT 
    status,
    CAST(readings->>'rpm' AS FLOAT) as rpm,
    CAST(readings->>'temperature' AS FLOAT) as temperature,
    CAST(readings->>'vibration' AS FLOAT) as vibration,
    CAST(timestamp AS TIMESTAMP) as timestamp,
    machine_id,
    _airbyte_raw_id
  FROM data