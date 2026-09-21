"""Prediction logic and business operations."""
import numpy as np
from typing import Dict, Any
from schemas import ROPInput, ROPOutput
from model_loader import get_model, get_scaler
from logger import setup_logger

logger = setup_logger(__name__)


def predict(data: ROPInput) -> ROPOutput:
    """
    Generate ROP predictions from drilling parameters.

    Args:
        data: Validated input signals

    Returns:
        ROPOutput with three ROP estimates

    Raises:
        ValueError: If model or scaler not available
        RuntimeError: If prediction fails
    """
    model = get_model()
    scaler = get_scaler()

    if model is None or scaler is None:
        logger.error("Prediction attempted but model/scaler not loaded")
        raise ValueError("Model not yet loaded. Please try again shortly.")

    try:
        # Prepare input array (8 fields in order)
        x = np.array([[
            data.ad_rop_sp,
            data.ad_torque_sp,
            data.accum_trip_in,
            data.datetime,
            data.depth_of_cut,
            data.hook_load,
            data.total_gas,
            data.wc_bit_weight,
        ]])

        logger.debug(f"Input shape: {x.shape}, Input values: {x}")

        # Scale and predict
        x_scaled = scaler.transform(x)
        pred = model.predict(x_scaled)

        logger.debug(f"Raw prediction shape: {pred.shape}, values: {pred}")

        # Extract three outputs
        result = ROPOutput(
            ROP_Average=float(pred[0][0]),
            ROP_Cut_Unit=float(pred[0][1]),
            ROP_Fast=float(pred[0][2]),
        )

        logger.info(f"Prediction successful: {result}")
        return result

    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise RuntimeError(f"Prediction failed: {str(e)}")
