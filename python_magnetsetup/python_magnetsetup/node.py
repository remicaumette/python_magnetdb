import enum
from dataclasses import dataclass

from .job import JobManager, JobManagerType


class NodeType(str, enum.Enum):
    compute = "compute"
    visu = "visu"


@dataclass
class NodeSpec:
    name: str
    dns: str
    otype: NodeType = NodeType.compute
    smp: bool = True
    manager: JobManager = JobManager(JobManagerType.none)
    cores: int = 2
    multithreading: bool = True
    mgkeydir: str = r"/opt/MeshGems"
