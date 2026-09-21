"""Configuration and constants for Axelrod."""
import os
from pathlib import Path

# Model paths
MODEL_ID = os.getenv("MODEL_ID", "1HSGTNa48Ft3dgnhtDPufw321fphWf4kS")
SCALER_ID = os.getenv("SCALER_ID", "1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp")
MODEL_PATH = "rop_model.pkl"
SCALER_PATH = "scaler.pkl"

# App config
APP_TITLE = "Axelrod"
APP_VERSION = "2.0.1"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Prediction history
MAX_HISTORY_SIZE = 20

# Input fields in order (for validation)
INPUT_FIELDS = [
    "ad_rop_sp",
    "ad_torque_sp",
    "accum_trip_in",
    "datetime",
    "depth_of_cut",
    "hook_load",
    "total_gas",
    "wc_bit_weight",
]

# Output fields
OUTPUT_FIELDS = ["ROP_Average", "ROP_Cut_Unit", "ROP_Fast"]

# Paths
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
