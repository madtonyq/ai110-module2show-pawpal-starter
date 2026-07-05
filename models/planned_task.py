from typing import Optional
from .task import Task

class PlannedTask:
    def __init__(self, task: Task, start_minutes: int, reason: str = ""):
        self.task_ = task
        self.start_time_ = start_minutes
        self.end_time_ = start_minutes + task.get_duration()
        self.reason_ = reason
    
    def get_task(self) -> Task:
        return self.task_
    
    def get_start_time(self) -> int:
        return self.start_time_
    
    def get_end_time(self) -> int:
        return self.end_time_
    
    def get_reason(self) -> str:
        return self.reason_
    
    def set_reason(self, reason: str) -> None:
        self.reason_ = reason
    
    def get_start_time_str(self) -> str:
        hours = self.start_time_ // 60
        minutes = self.start_time_ % 60
        return f"{hours:02d}:{minutes:02d}"
    
    def get_end_time_str(self) -> str:
        hours = self.end_time_ // 60
        minutes = self.end_time_ % 60
        
        # Handle wrapping past midnight
        if hours >= 24:
            hours = hours % 24
        
        return f"{hours:02d}:{minutes:02d}"
    
    def overlaps_with(self, other: "PlannedTask") -> bool:
        return not (self.end_time_ <= other.start_time_ or self.start_time_ >= other.end_time_)
    
    def __repr__(self) -> str:
        return (f"PlannedTask(task={self.task_}, "
                f"start_time={self.start_time_}, start_time_str='{self.get_start_time_str()}', "
                f"end_time={self.end_time_}, end_time_str='{self.get_end_time_str()}', "
                f"reason='{self.reason_}')")