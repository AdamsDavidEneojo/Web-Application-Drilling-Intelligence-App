"""Data validation schemas using Pydantic."""
import math

from pydantic import BaseModel, Field, validator


class ROPInput(BaseModel):
    """Drilling operation input signals for ROP prediction."""
    ad_rop_sp: float = Field(..., description="AD ROP setpoint")
    ad_torque_sp: float = Field(..., description="AD Torque setpoint")
    accum_trip_in: float = Field(..., description="Accumulator trip in")
    datetime: float = Field(..., description="Timestamp in milliseconds")
    depth_of_cut: float = Field(..., description="Depth of cut")
    hook_load: float = Field(..., description="Hook load")
    total_gas: float = Field(..., description="Total gas")
    wc_bit_weight: float = Field(..., description="Bit weight")

    @validator("*")
    def validate_finite(cls, v):
        """Ensure all values are finite numbers."""
        if not math.isfinite(v):
            raise ValueError("All inputs must be finite numbers")
        return v

    @validator("datetime")
    def validate_timestamp_ms(cls, v):
        """Accept plausible Unix timestamps expressed in milliseconds."""
        if not 0 <= v <= 1e14:
            raise ValueError("datetime must be a Unix timestamp in milliseconds")
        return v

    @validator(
        "ad_rop_sp", "ad_torque_sp", "accum_trip_in", "depth_of_cut",
        "hook_load", "total_gas", "wc_bit_weight",
    )
    def validate_measurement_range(cls, v):
        """Reject implausibly large sensor values without constraining timestamps."""
        if not -1e10 < v < 1e10:
            raise ValueError("Input values must be within the supported range")
        return v


class ROPOutput(BaseModel):
    """Rate of penetration prediction outputs."""
    ROP_Average: float
    ROP_Cut_Unit: float
    ROP_Fast: float


class HistoryEntry(BaseModel):
    """Single prediction history entry."""
    input: ROPInput
    output: ROPOutput


class HealthCheck(BaseModel):
    """Health check response."""
    status: str  # "ready" or "loading"
    message: str | None = None


class ModelInfo(BaseModel):
    """Model information response."""
    model: str
    framework: str
    inputs: int
    outputs: int
    status: str


class APIInfo(BaseModel):
    """API information response."""
    app: str
    version: str
    endpoints: list
