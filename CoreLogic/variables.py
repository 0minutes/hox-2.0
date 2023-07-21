"""Contains all the return values for consistency"""
import dataclasses

@dataclasses.dataclass
class Variables:
    """Provides return codes for the output of different functions"""

    exerror: int = 100
    error: int = 101
    success: int = 102

    #LOGS

    logsoff: int = 300
    logson: int = 301

    quit: int = 200
