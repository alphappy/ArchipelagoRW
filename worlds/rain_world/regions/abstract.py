from .classes import RegionData, ConnectionData
from ..options import RainWorldOptions

fundamental = ("Menu", "Early Passages", "PPwS Passages", "Late Passages", "Events")
regions = {
    **{r: RegionData(r) for r in fundamental},
    "Food Quest": RegionData("Food Quest", lambda options: options.msc_enabled)
}
connections = [
    ConnectionData("Menu", "Early Passages")
]


def generate(_: RainWorldOptions) -> tuple[list[RegionData], list[ConnectionData]]:
    return list(regions.values()), connections
