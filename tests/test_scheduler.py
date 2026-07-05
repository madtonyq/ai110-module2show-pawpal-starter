import pytest
from datetime import datetime
from models import Owner, Pet, Task, Priority
from scheduler import Scheduler  # ✅ Correct import


class TestScheduler:
    def setup_method(self):
        """Set up test fixtures."""
        self.owner = Owner("Alex", 120)
        self.pet = Pet("Biscuit", "Dog", "Golden Retriever", 3)
        self.tasks = [
            Task("Morning walk", 30, Priority.HIGH, "walk"),
            Task("Feeding", 15, Priority.HIGH, "feed"),
            Task("Medication", 5, Priority.CRITICAL, "med"),
        ]
        self.scheduler = Scheduler(self.owner, self.pet, self.tasks)
    
    def test_priority_sorting(self):
        """Test that critical tasks are scheduled before high priority tasks."""
        plan = self.scheduler.generate_daily_plan()
        scheduled = plan.get_scheduled_tasks()
        
        # Get priorities in order
        priorities = [p.get_task().get_priority() for p in scheduled]
        
        # Critical tasks should come first
        assert priorities[0] == Priority.CRITICAL
    
    def test_time_limit_respected(self):
        """Test that total planned time doesn't exceed owner's time limit."""
        plan = self.scheduler.generate_daily_plan()
        total_minutes = plan.get_total_planned_minutes()
        
        assert total_minutes <= self.owner.get_time_limit()
    
    def test_conflict_handling(self):
        """Test that two tasks don't overlap."""
        plan = self.scheduler.generate_daily_plan()
        scheduled = plan.get_scheduled_tasks()
        
        # Sort by start time
        sorted_tasks = sorted(scheduled, key=lambda p: p.get_start_time())
        
        # Check no overlaps
        for i in range(len(sorted_tasks) - 1):
            current_end = sorted_tasks[i].get_end_time()
            next_start = sorted_tasks[i + 1].get_start_time()
            assert current_end <= next_start
    
    def test_recurring_filter_daily(self):
        """Test that daily recurring tasks are always included."""
        daily_task = Task(
            "Daily walk", 30, Priority.MEDIUM, "walk",
            is_recurring=True, recurring_pattern="daily"
        )
        self.tasks.append(daily_task)
        self.scheduler = Scheduler(self.owner, self.pet, self.tasks)
        
        plan = self.scheduler.generate_daily_plan("2026-06-24")
        scheduled = plan.get_scheduled_tasks()
        
        assert any(p.get_task().get_description() == "Daily walk" 
                  for p in scheduled)
    
    def test_recurring_filter_weekly(self):
        """Test that weekly tasks are only included on specified days."""
        weekly_task = Task(
            "Weekly grooming", 45, Priority.LOW, "groom",
            is_recurring=True, recurring_pattern="weekly",
            recurring_days=["Monday", "Thursday"]
        )
        self.tasks.append(weekly_task)
        self.scheduler = Scheduler(self.owner, self.pet, self.tasks)

        # June 24, 2026 is a Wednesday ❌ - This will fail
        # Use a date that is actually a Monday or Thursday
        
        # June 22, 2026 is a Monday ✅
        # June 25, 2026 is a Thursday ✅
        
        # Test Monday (should be included)
        plan_monday = self.scheduler.generate_daily_plan("2026-06-22")  # This is a Monday
        scheduled_monday = plan_monday.get_scheduled_tasks()
        assert any(p.get_task().get_description() == "Weekly grooming"
                for p in scheduled_monday), "Task should be scheduled on June 22 (Monday)"

        # Test Tuesday (should NOT be included)
        plan_tuesday = self.scheduler.generate_daily_plan("2026-06-23")  # This is a Tuesday
        scheduled_tuesday = plan_tuesday.get_scheduled_tasks()
        assert not any(p.get_task().get_description() == "Weekly grooming"
                    for p in scheduled_tuesday), "Task should NOT be scheduled on June 23 (Tuesday)"
        
        # Test Thursday (should be included)
        plan_thursday = self.scheduler.generate_daily_plan("2026-06-25")  # This is a Thursday
        scheduled_thursday = plan_thursday.get_scheduled_tasks()
        assert any(p.get_task().get_description() == "Weekly grooming"
                for p in scheduled_thursday), "Task should be scheduled on June 25 (Thursday)"

    def test_exclusion_when_time_runs_out(self):
        """Test that tasks are excluded when time limit is reached."""
        # Add many tasks to exceed time limit
        for i in range(10):
            self.tasks.append(Task(f"Task {i}", 30, Priority.LOW, "other"))
        
        self.scheduler = Scheduler(self.owner, self.pet, self.tasks)
        plan = self.scheduler.generate_daily_plan()
        excluded = plan.get_excluded_tasks()
        
        assert len(excluded) > 0
        
        # All excluded tasks should have a reason
        for task, reason in excluded:
            assert reason is not None and len(reason) > 0
    
    def test_explanation_generation(self):
        """Test that each scheduled task has a meaningful explanation."""
        plan = self.scheduler.generate_daily_plan()
        scheduled = plan.get_scheduled_tasks()
        
        for planned in scheduled:
            reason = planned.get_reason()
            assert reason is not None
            assert len(reason) > 0
    
    def test_statistics_generation(self):
        """Test that statistics are correctly generated."""
        stats = self.scheduler.get_statistics()
        
        assert "total_scheduled" in stats
        assert "total_excluded" in stats
        assert "total_minutes" in stats
        assert "available_minutes" in stats
        assert "remaining_minutes" in stats
        assert "utilization_percentage" in stats
        assert "categories" in stats
    
    def test_available_time_slots(self):
        """Test that available time slots are correctly calculated."""
        slots = self.scheduler.get_available_time_slots()
        
        # Should return a list of tuples
        assert isinstance(slots, list)
        for slot in slots:
            assert isinstance(slot, tuple)
            assert len(slot) == 2
            assert slot[0] < slot[1]  # Start < End