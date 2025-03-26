import pynvml
import time
import pymongo
import sys
import bcrypt
from datetime import datetime
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

class EnergyMonitor:
    def __init__(self):
        self.energy_consumed = 0
        self.start_time = None
        self.running = False
        self.user_id = None  # Store logged-in user ID
        self.project_name = None  # Store project name
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["EnergyDB"]
        self.users = self.db["users"]


    def start(self, project_name):
        """Starts monitoring GPU power consumption and auto-saves progress."""
        if not self.running:
            # Check if the user is logged in
            if not self.user_id:
                print("Please log in first.")
                return
            
            # Check if the project exists
            user_data = self.users.find_one({"_id": ObjectId(self.user_id)})
            if project_name not in user_data.get("projects", {}):
                create_project = input(f"Project '{project_name}' not found. Do you want to create a new project? (Y/N): ").strip().upper()
                if create_project != "Y":
                    print("Operation canceled. Exiting...")
                    sys.exit(1)  # Exit the program
            
            # Initialize GPU monitoring
            pynvml.nvmlInit()
            self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            self.energy_consumed = 0
            self.start_time = time.time()
            self.running = True
            self.project_name = project_name  # Store project name

            # Create an empty project entry if it doesn't exist
            self.users.update_one(
                {"_id": ObjectId(self.user_id)},
                {"$set": {f"projects.{project_name}": {}}}
            )

            print(f"Energy monitoring started for project: {project_name}...")


    def stop(self):
        """Stops monitoring and stores total energy consumed in a new run in the database."""
        if self.running:
            duration = time.time() - self.start_time
            pynvml.nvmlShutdown()
            energy_kwh = self.energy_consumed / 3_600_000  # Convert J to kWh

            if self.user_id:
                timestamp = datetime.utcnow()

                # Fetch existing runs for the project
                user_data = self.users.find_one({"_id": ObjectId(self.user_id)})
                existing_runs = user_data.get("projects", {}).get(self.project_name, {}).keys()
                
                # Generate a new run key (e.g., run1, run2, run3, ...)
                new_run_key = f"run{len(existing_runs) + 1}"

                # Store the new energy data in the database
                self.users.update_one(
                    {"_id": ObjectId(self.user_id)},
                    {
                        "$set": {f"projects.{self.project_name}.{new_run_key}": {
                            "timestamp": timestamp,
                            "duration": duration,
                            "energy": self.energy_consumed,
                            "energy_kwh": energy_kwh
                        }}
                    }
                )
                print(f"Energy data stored under {self.project_name} -> {new_run_key}.")
            else:
                print("No logged-in user. Data not stored.")

            self.running = False

    def update_energy(self):
        """Updates energy consumption every second (to be run in a loop)."""
        while self.running:
            power_usage = pynvml.nvmlDeviceGetPowerUsage(self.gpu_handle) / 1000  # Convert mW to W
            self.energy_consumed += power_usage
            time.sleep(1)

    def login(self, username, password):
        """Authenticates the user with hashed password verification."""
        user = self.users.find_one({"username": username})
        
        if not user:
            print("No username found.")
            sys.exit(1)
        
        if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            print("Password incorrect.")
            sys.exit(1)
        
        self.user_id = str(user["_id"])  # Store logged-in user ID
        print("Login successful.")
        return True
