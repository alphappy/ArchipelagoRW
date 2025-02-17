from .classes import RegionData, ConnectionData
from ..options import RainWorldOptions

fundamental = ("Menu", "Early Passages", "PPwS Passages", "Late Passages")
regions = {
    **{r: RegionData(r) for r in fundamental},
    "Food Quest": RegionData("Food Quest", lambda options: options.msc_enabled)
}
connections = [
    ConnectionData("Menu", "Early Passages"),
    ConnectionData("Menu", "Food Quest"),
    ConnectionData("Early Passages", "Late Passages"),
    ConnectionData("Late Passages", "PPwS Passages"),
]


def generate(_: RainWorldOptions) -> tuple[list[RegionData], list[ConnectionData]]:
    return list(regions.values()), connections
