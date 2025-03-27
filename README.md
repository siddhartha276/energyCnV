# EnergyMonitor

## Overview
EnergyMonitor is a Python-based tool that tracks GPU power consumption using **NVIDIA Management Library (NVML)** and stores energy usage data in a **MongoDB database**. It allows users to log in, track energy consumption per project, and store run-specific energy data.

## Features
- **User Authentication**: Secure login using **bcrypt**.
- **Energy Monitoring**: Tracks GPU power usage using NVML.
- **Project-Based Tracking**: Associates energy consumption data with different projects.
- **Database Storage**: Saves energy consumption history in MongoDB.
- **Automatic Timing**: Energy tracking automatically starts and stops when monitoring begins and ends.

## Installation Requirements
Before using the tool, install the required dependencies:
```sh
pip install pymongo bcrypt pynvml
```
Ensure you have:
- A **MongoDB database** (e.g., MongoDB Atlas or a local instance).
- **NVIDIA GPU and drivers installed**.
- **NVML library** (included in the NVIDIA drivers).

## Usage
### 1. Import and Initialize
```python
from energy_monitor import EnergyMonitor
monitor = EnergyMonitor()
```

### 2. Login
Before tracking energy consumption, log in with:
```python
monitor.login("username", "password")
```

### 3. Start Monitoring
Start tracking energy consumption for a specific project:
```python
monitor.start("ProjectName")
```
- If the project does not exist, it prompts the user to create one.
- The timer **automatically starts** when monitoring begins.

### 4. Stop Monitoring
To stop tracking and save energy data:
```python
monitor.stop()
```
- This **automatically calculates** the total energy used and duration.
- Data is stored in the database.

## Functions
### `login(username, password)`
**Inputs:**
- `username` (str): The username of the user.
- `password` (str): The corresponding password.

**Functionality:**
- Authenticates the user with a hashed password.
- Stores the user ID after successful login.

### `start(project_name)`
**Inputs:**
- `project_name` (str): Name of the project to track energy usage.

**Functionality:**
- Initializes GPU energy monitoring.
- Checks if the project exists; if not, prompts user to create one.
- **Automatically starts the timer** when monitoring begins.

### `stop()`
**Functionality:**
- **Automatically stops the timer** and calculates energy consumption.
- Stores run details like duration, timestamp, and energy used.
- Saves data in MongoDB.

## Database Structure
Each user document in MongoDB follows this structure:
```json
{
    "_id": ObjectId("..."),
    "username": "user123",
    "password": "hashed_password",
    "projects": {
        "ProjectName": {
            "run1": {
                "timestamp": "2025-03-08T12:00:00Z",
                "duration": 3600,
                "energy": 500000,
                "energy_kwh": 0.138
            }
        }
    }
}
```

## Notes
- Make sure you **log in before starting monitoring**.
- Ensure your **GPU supports NVML**.
- **Timing is handled automatically**; no need for manual tracking.

## License
This project is open-source. Feel free to modify and extend it!

