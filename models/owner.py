from typing import Dict, Any, Optional

class Owner:  # ✅ Fixed: PascalCase
    def __init__(self, name: str, daily_time_limit_minutes: int = 120):
        self.name_ = name
        self.daily_time_limit_minutes_ = daily_time_limit_minutes
        self.preferences_: Dict[str, Any] = {}  # ✅ Fixed: spelling
    
    def get_name(self) -> str:
        return self.name_
    
    def get_time_limit(self) -> int:
        return self.daily_time_limit_minutes_
    
    def set_time_limit(self, new_limit: int) -> None:
        if new_limit <= 0:
            raise ValueError("Time limit must be positive")  # ✅ Added validation
        self.daily_time_limit_minutes_ = new_limit
    
    def set_preference(self, key: str, value: Any) -> None:
        self.preferences_[key] = value
    
    def get_preference(self, key: str, default: Any = None) -> Optional[Any]:  # ✅ Added default
        return self.preferences_.get(key, default)
    
    def get_all_preferences(self) -> Dict[str, Any]:
        return self.preferences_.copy()
    
    def __repr__(self) -> str:
        return f"Owner(name='{self.name_}', daily_time_limit_minutes={self.daily_time_limit_minutes_})"  # ✅ Fixed: quotes