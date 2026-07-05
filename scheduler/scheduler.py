from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
from models import Owner, Pet, Task, PlannedTask, DailyPlan, Priority

class Scheduler:  # ✅ Fixed: PascalCase
    def __init__(
        self,
        owner: Owner,
        pet: Pet,
        tasks: List[Task],
        working_hours: Tuple[int, int] = (360, 1320)  # 6am - 10pm
    ):
        self.owner_ = owner
        self.pet_ = pet
        self.tasks_ = tasks
        self.working_hours_ = working_hours
    
    def generate_daily_plan(self, date: str = None) -> DailyPlan:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        plan = DailyPlan(
            self.pet_.get_name(),  # ✅ Fixed: positional arguments
            self.owner_.get_name(),
            self.owner_.get_time_limit()
        )
        plan.set_date(date)
        
        filtered_tasks = self.filter_tasks_by_recurrence(self.tasks_, date)
        sorted_tasks = self.sort_tasks(filtered_tasks)
        scheduled, excluded = self.schedule_with_conflicts_handling(  # ✅ Fixed: method name
            sorted_tasks,
            self.owner_.get_time_limit(),
            self.working_hours_
        )
        
        for planned_task in scheduled:
            plan.add_planned_task(planned_task)
        
        for task, reason in excluded:
            plan.add_excluded_task(task, reason)
        
        plan.generate_summary()
        return plan
    
    def filter_tasks_by_recurrence(self, tasks: List[Task], date: str) -> List[Task]:
        filtered_tasks = []
        for task in tasks:
            if task.occurs_on(date):  # ✅ Fixed: uses occurs_on
                filtered_tasks.append(task)
        return filtered_tasks
    
    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: (
            -t.get_priority(),  # Negative for descending
            t.get_duration()
        ))
    
    def schedule_with_conflicts_handling(  # ✅ Fixed: method name
        self,
        sorted_tasks: List[Task],
        time_limit: int,
        working_hours: Tuple[int, int]
    ) -> Tuple[List[PlannedTask], List[Tuple[Task, str]]]:
        scheduled: List[PlannedTask] = []
        excluded: List[Tuple[Task, str]] = []
        total_time_used = 0
        day_start, day_end = working_hours
        
        for task in sorted_tasks:
            task_duration = task.get_duration()
            
            # Check time limit
            if total_time_used + task_duration > time_limit:
                excluded.append((
                    task,
                    f"Insufficient remaining time "
                    f"(needs {task_duration} min, only {time_limit - total_time_used} min left)"
                ))
                continue
            
            # Find earliest available slot
            start_time = self.find_earliest_available_time(  # ✅ Fixed: method name
                task, scheduled, day_start, day_end
            )
            
            if start_time is None:
                excluded.append((
                    task,
                    "No available time slot within working hours (6 AM - 10 PM)"
                ))
                continue
            
            # Create planned task with explanation
            reason = self.explain_scheduling_decision(task, start_time, scheduled)  # ✅ Fixed: method name
            planned = PlannedTask(task, start_time, reason)
            scheduled.append(planned)
            total_time_used += task_duration
        
        return scheduled, excluded
    
    def find_earliest_available_time(  # ✅ Fixed: method name
        self,
        task: Task,
        scheduled: List[PlannedTask],
        day_start: int,
        day_end: int
    ) -> Optional[int]:
        task_duration = task.get_duration()
        candidate_time = day_start
        checked_positions = set()  # ✅ Added: to avoid infinite loops
        
        while candidate_time + task_duration <= day_end:
            if candidate_time in checked_positions:
                break
            checked_positions.add(candidate_time)
            
            overlap_found = False
            
            for planned in scheduled:
                planned_start = planned.get_start_time()
                planned_end = planned.get_end_time()
                
                # Check if candidate slot overlaps with this planned task
                if not (candidate_time + task_duration <= planned_start or
                        candidate_time >= planned_end):
                    overlap_found = True
                    candidate_time = planned_end
                    break
            
            if not overlap_found:
                return candidate_time
        
        return None
    
    def explain_scheduling_decision(  # ✅ Fixed: removed trailing underscore
        self,
        task: Task,
        start_time: int,
        scheduled: List[PlannedTask]
    ) -> str:
        reasons = []
        
        # Priority-based explanation
        if task.is_critical():
            reasons.append("Critical task prioritized above all others")
        elif task.is_high_priority():
            reasons.append("High-priority task scheduled to ensure completion")
        elif task.get_priority() == Priority.MEDIUM:
            reasons.append("Medium-priority task scheduled when time available")
        else:
            reasons.append("Low-priority task scheduled in remaining time")
        
        # Time-based explanation
        hour = start_time // 60
        if 5 <= hour < 12:
            reasons.append("Scheduled in the morning to align with daily routine")
        elif 12 <= hour < 17:
            reasons.append("Scheduled in the afternoon as a midday activity")
        else:
            reasons.append("Scheduled in the evening to complete daily care")
        
        # Preferred time matching
        preferred = task.get_preferred_time()
        if preferred:
            if (preferred == "morning" and 5 <= hour < 12) or \
               (preferred == "afternoon" and 12 <= hour < 17) or \
               (preferred == "evening" and 17 <= hour < 23):
                reasons.append(f"Matches owner's preference for {preferred} time")
            else:
                reasons.append(f"Could not schedule at preferred {preferred} time due to conflicts")
        
        # Context-based explanation
        if scheduled:
            nearest = min(scheduled, key=lambda p: abs(p.get_start_time() - start_time))
            gap = abs(start_time - nearest.get_end_time()) if start_time > nearest.get_start_time() else abs(nearest.get_start_time() - (start_time + task.get_duration()))
            
            if gap <= 15:
                if start_time > nearest.get_start_time():
                    reasons.append(f"Scheduled after {nearest.get_task().get_description()}")
                else:
                    reasons.append(f"Scheduled before {nearest.get_task().get_description()}")
        
        # Pet special needs
        if self.pet_.has_medical_condition("diabetic") and task.get_category() == "feed":  # ✅ Fixed: method name
            reasons.append("Scheduled at consistent time for diabetic pet management")
        elif self.pet_.has_medical_condition("allergies") and task.get_category() == "med":
            reasons.append("Scheduled to maintain consistent medication timing for allergies")
        elif self.pet_.has_medical_condition("arthritis") and task.get_category() == "walk":
            reasons.append("Scheduled during warmer part of day for arthritic pet comfort")
        
        if reasons:
            return "; ".join(reasons)
        return "Scheduled at this time based on availability"
    
    def calculate_priority_score(self, task: Task) -> float:  # ✅ Fixed: spelling
        score = task.get_priority() * 100
        
        duration = task.get_duration()
        if duration <= 5:
            score += 20
        elif duration <= 15:
            score += 10
        elif duration > 60:
            score -= 20
        
        if task.get_category() in ["med", "feed"]:
            score += 15
        elif task.get_category() == "walk":
            score += 5
        
        return score
    
    def get_available_time_slots(
        self,
        date: str = None
    ) -> List[Tuple[int, int]]:
        plan = self.generate_daily_plan(date)
        scheduled = plan.get_scheduled_tasks()
        
        day_start, day_end = self.working_hours_
        available = []
        current_time = day_start
        
        sorted_scheduled = sorted(scheduled, key=lambda p: p.get_start_time())
        for planned in sorted_scheduled:
            if planned.get_start_time() > current_time:
                available.append((current_time, planned.get_start_time()))
            current_time = planned.get_end_time()
        
        if current_time < day_end:
            available.append((current_time, day_end))
        
        return available
    
    def get_statistics(self, date: str = None) -> Dict[str, Any]:
        plan = self.generate_daily_plan(date)
        
        categories = {}
        for planned in plan.get_scheduled_tasks():
            task = planned.get_task()
            category = task.get_category()
            if category not in categories:
                categories[category] = []
            categories[category].append(task.get_duration())
        
        stats = {
            "total_scheduled": len(plan.get_scheduled_tasks()),
            "total_excluded": len(plan.get_excluded_tasks()),
            "total_minutes": plan.get_total_planned_minutes(),
            "available_minutes": plan.get_total_available_minutes(),  # ✅ Fixed
            "remaining_minutes": plan.get_remaining_minutes(),
            "utilization_percentage": (
                plan.get_total_planned_minutes() / plan.get_total_available_minutes() * 100
                if plan.get_total_available_minutes() > 0 else 0
            ),
            "categories": {
                cat: {
                    "count": len(durations),
                    "total_minutes": sum(durations),
                    "average_minutes": sum(durations) / len(durations) if durations else 0
                }
                for cat, durations in categories.items()
            }
        }
        return stats
    
    def __repr__(self) -> str:
        return f"Scheduler(owner='{self.owner_.get_name()}', pet='{self.pet_.get_name()}', tasks={len(self.tasks_)})"