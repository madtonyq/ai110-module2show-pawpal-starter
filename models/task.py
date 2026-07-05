from typing import Optional, List
from enum import IntEnum

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Task:  # ✅ Fixed: PascalCase
    _next_id = 1
    
    def __init__(
        self,
        description: str,
        duration_minutes: int,
        priority: int = Priority.MEDIUM,
        category: str = "other",
        preferred_time: Optional[str] = None,
        is_recurring: bool = False,
        recurring_pattern: Optional[str] = None,
        recurring_days: Optional[List[str]] = None
    ):
        self.id_ = Task._next_id
        Task._next_id += 1
        self.description_ = description
        self.duration_minutes_ = duration_minutes
        self.priority_ = self._validate_priority(priority)  # ✅ Fixed: uses validation
        self.category_ = category
        self.preferred_time_ = preferred_time
        self.is_recurring_ = is_recurring
        self.recurring_pattern_ = recurring_pattern
        self.recurring_days_ = recurring_days if recurring_days else []
        self._validate_recurrence()

    def _validate_priority(self, priority: int) -> int:
        if priority < Priority.LOW or priority > Priority.CRITICAL:
            raise ValueError(f"Priority must be between {Priority.LOW} and {Priority.CRITICAL}.")
        return priority
    
    def _validate_recurrence(self) -> None:
        if self.is_recurring_:
            if self.recurring_pattern_ not in ["daily", "weekly"]:
                raise ValueError("Recurring pattern must be 'daily' or 'weekly' if the task is recurring.")
            if self.recurring_pattern_ == "weekly" and not self.recurring_days_:
                raise ValueError("Recurring days must be provided for weekly recurring tasks.")
    
    def get_id(self) -> int:
        return self.id_
    
    def get_description(self) -> str:
        return self.description_
    
    def get_duration(self) -> int:  # ✅ Added: for compatibility
        return self.duration_minutes_
    
    def get_duration_minutes(self) -> int:
        return self.duration_minutes_
    
    def get_priority(self) -> int:
        return self.priority_
    
    def get_category(self) -> str:
        return self.category_
    
    def get_preferred_time(self) -> Optional[str]:
        return self.preferred_time_
    
    def get_is_recurring(self) -> bool:
        return self.is_recurring_
    
    def get_recurring_pattern(self) -> Optional[str]:
        return self.recurring_pattern_
    
    def get_recurring_days(self) -> List[str]:  # ✅ Fixed: returns copy
        return self.recurring_days_.copy()
    
    def get_priority_label(self) -> str:
        labels = {
            Priority.LOW: "low",
            Priority.MEDIUM: "medium",
            Priority.HIGH: "high",
            Priority.CRITICAL: "critical"
        }
        return labels.get(self.priority_, "unknown")  # ✅ Fixed: uses self.priority_
    
    def is_high_priority(self) -> bool:
        return self.priority_ >= Priority.HIGH
    
    def is_critical(self) -> bool:
        return self.priority_ == Priority.CRITICAL
    
    def set_description(self, description: str) -> None:
        self.description_ = description
    
    def set_duration_minutes(self, duration_minutes: int) -> None:
        if duration_minutes <= 0:
            raise ValueError("Duration must be positive")
        self.duration_minutes_ = duration_minutes
    
    def set_priority(self, priority: int) -> None:
        self.priority_ = self._validate_priority(priority)
    
    def set_category(self, category: str) -> None:
        self.category_ = category
    
    def set_preferred_time(self, preferred_time: Optional[str]) -> None:
        self.preferred_time_ = preferred_time
    
    def set_recurring(
        self,
        is_recurring: bool,
        recurring_pattern: Optional[str] = None,
        recurring_days: Optional[List[str]] = None
    ) -> None:
        self.is_recurring_ = is_recurring
        self.recurring_pattern_ = recurring_pattern
        self.recurring_days_ = recurring_days if recurring_days else []
        self._validate_recurrence()
    
    def occurs_on(self, date_str: str) -> bool:  # ✅ Fixed: renamed from occurs_on_day
        if not self.is_recurring_:
            return True  # Non-recurring tasks always occur
        
        if self.recurring_pattern_ == "daily":
            return True
        
        if self.recurring_pattern_ == "weekly":
            from datetime import datetime
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = date_obj.strftime("%A")
            return day_name in self.recurring_days_
        
        return False
    
    def __repr__(self) -> str:
        return (f"Task(id={self.id_}, description='{self.description_}', "
            f"duration_minutes={self.duration_minutes_}, priority={self.priority_}, "
            f"priority_label='{self.get_priority_label()}', "  # ✅ Added priority_label
            f"category='{self.category_}', preferred_time={self.preferred_time_}, "  # ✅ Fixed: removed quotes around None
            f"is_recurring={self.is_recurring_}, recurring_pattern='{self.recurring_pattern_}', "
            f"recurring_days={self.recurring_days_})")