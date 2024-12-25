from fastapi import FastAPI
from datetime import datetime
import random
from typing import List, Dict
import uvicorn

app = FastAPI(title="Industrial Edge Gateway Simulator")

# Define a list of machine IDs to simulate
MACHINE_IDS = ["MACHINE_001", "MACHINE_002", "MACHINE_003", "MACHINE_004", "MACHINE_005"]

def generate_machine_data(machine_id: str) -> Dict:
    """Simulate data from a specific machine"""
    # Simulate normal operating conditions with occasional anomalies
    is_anomaly = random.random() < 0.05  # 5% chance of anomaly
    
    # Different machines can have different baseline characteristics
    machine_baselines = {
        "MACHINE_001": {"temp": 70, "vib": 0.5, "rpm": 1000},  # Standard machine
        "MACHINE_002": {"temp": 65, "vib": 0.4, "rpm": 1200},  # High-speed, cooler
        "MACHINE_003": {"temp": 75, "vib": 0.6, "rpm": 800},   # Heavy duty, hotter
        "MACHINE_004": {"temp": 72, "vib": 0.45, "rpm": 1100}, # Medium duty
        "MACHINE_005": {"temp": 68, "vib": 0.55, "rpm": 950},  # Standard variant
    }
    
    baseline = machine_baselines[machine_id]
    
    temperature = random.gauss(baseline["temp"], 2)
    vibration = random.gauss(baseline["vib"], 0.1)
    rpm = random.gauss(baseline["rpm"], 50)
    
    if is_anomaly:
        temperature += random.gauss(15, 5)
        vibration *= 1.5
        rpm += random.gauss(100, 30)
    
    return {
        "machine_id": machine_id,
        "timestamp": datetime.now().isoformat(),
        "readings": {
            "temperature": round(temperature, 2),
            "vibration": round(vibration, 3),
            "rpm": round(rpm, 0),
        },
        "status": "warning" if is_anomaly else "normal"
    }

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "edge-gateway-simulator"}

@app.get("/data")
async def get_machine_data(machine_id: str = "MACHINE_001") -> Dict:
    """Endpoint that simulates an edge gateway sending machine data"""
    if machine_id not in MACHINE_IDS:
        machine_id = "MACHINE_001"
    return generate_machine_data(machine_id)

@app.get("/batch")
async def get_batch_data(size: int = 10) -> List[Dict]:
    """Get multiple readings at once from random machines"""
    return [
        generate_machine_data(random.choice(MACHINE_IDS)) 
        for _ in range(size)
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)