from typing import List, Tuple, Optional
from .planned_task import PlannedTask
from .task import Task

class DailyPlan:  # ✅ Fixed: PascalCase
    def __init__(self, pet_name: str, owner_name: str, available_minutes: int):
        self.date_ = ""  # ✅ Fixed: singular
        self.pet_name_ = pet_name
        self.owner_name_ = owner_name
        self.planned_tasks_: List[PlannedTask] = []
        self.excluded_tasks_: List[Tuple[Task, str]] = []
        self.total_planned_minutes_: int = 0
        self.available_minutes_: int = available_minutes
        self.summary_: str = ""
    
    def set_date(self, date: str):  # ✅ Fixed: singular
        self.date_ = date
    
    def add_planned_task(self, planned_task: PlannedTask):  # ✅ Fixed: parameter name
        self.planned_tasks_.append(planned_task)
        self.total_planned_minutes_ += planned_task.get_task().get_duration()
    
    def add_excluded_task(self, task: Task, reason: str):
        self.excluded_tasks_.append((task, reason))
    
    def get_scheduled_tasks(self) -> List[PlannedTask]:
        return self.planned_tasks_.copy()
    
    def get_excluded_tasks(self) -> List[Tuple[Task, str]]:
        return self.excluded_tasks_.copy()
    
    def get_total_planned_minutes(self) -> int:
        return self.total_planned_minutes_
    
    def get_total_available_minutes(self) -> int:  # ✅ Fixed: returns available minutes
        return self.available_minutes_
    
    def get_remaining_minutes(self) -> int:  # ✅ Added: missing method
        return self.available_minutes_ - self.total_planned_minutes_
    
    def get_summary(self) -> str:
        if not self.summary_:
            self.generate_summary()
        return self.summary_
    
    def generate_summary(self):  # ✅ Fixed: improved summary
        task_count = len(self.planned_tasks_)
        excluded_count = len(self.excluded_tasks_)
        remaining = self.get_remaining_minutes()
        
        summary_parts = []
        summary_parts.append(f"📋 Daily Plan for {self.pet_name_}")
        summary_parts.append(f"Owner: {self.owner_name_}")
        summary_parts.append(f"Date: {self.date_}")
        summary_parts.append("")
        summary_parts.append(f"✅ Scheduled {task_count} task(s) ({self.total_planned_minutes_} min / {self.available_minutes_} min available)")
        
        if excluded_count > 0:
            summary_parts.append(f"❌ {excluded_count} task(s) could not be scheduled")
        
        if remaining > 0:
            summary_parts.append(f"⏱️ {remaining} min remaining")
        else:
            summary_parts.append("⏱️ All available time used")
        
        self.summary_ = "\n".join(summary_parts)
        return self.summary_
    
    def get_formatted_plan(self) -> List[str]:  # ✅ Fixed: spelling
        lines = []
        
        # Header
        lines.append(f"Daily Plan for {self.pet_name_} on {self.date_}")
        lines.append(f"Owner: {self.owner_name_} ({self.available_minutes_} min daily limit)")
        lines.append("=" * 50)
        lines.append("")
        
        # Scheduled tasks
        if self.planned_tasks_:
            lines.append("✅ Scheduled Tasks:")
            lines.append("-" * 30)
            for planned in sorted(self.planned_tasks_, key=lambda p: p.get_start_time()):
                task = planned.get_task()
                lines.append(
                    f"  {planned.get_start_time_str()} – {task.get_description()} "
                    f"({task.get_duration()} min) [priority: {task.get_priority_label()}]"
                )
                if planned.get_reason():
                    lines.append(f"    Reason: {planned.get_reason()}")
                lines.append("")
        
        # Summary
        lines.append("")
        lines.append(f"⏱️ Total planned: {self.total_planned_minutes_} min / {self.available_minutes_} min available")
        lines.append("")
        
        # Excluded tasks
        if self.excluded_tasks_:
            lines.append("❌ Skipped Tasks (could not fit):")
            lines.append("-" * 30)
            for task, reason in self.excluded_tasks_:
                lines.append(
                    f"  - {task.get_description()} ({task.get_duration()} min) "
                    f"[priority: {task.get_priority_label()}]"
                )
                lines.append(f"    Reason: {reason}")
                lines.append("")
        
        return lines
    
    def __repr__(self) -> str:
        return f"DailyPlan(pet_name='{self.pet_name_}', owner_name='{self.owner_name_}', available_minutes={self.available_minutes_})"