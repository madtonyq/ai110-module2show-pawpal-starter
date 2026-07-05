import pytest
from models import Owner, Pet, Task, PlannedTask, DailyPlan, Priority  # ✅ Fixed: imports


class TestOwner:  # ✅ Fixed: PascalCase
    def test_owner_creation(self):
        owner = Owner("Alex", 120)
        assert owner.get_name() == "Alex"
        assert owner.get_time_limit() == 120
    
    def test_owner_preferences(self):
        owner = Owner("Alex")
        owner.set_preference("favorite_time", "morning")
        assert owner.get_preference("favorite_time") == "morning"
        assert owner.get_preference("nonexistent", "default") == "default"
    
    def test_owner_time_limit_validation(self):
        owner = Owner("Alex", 120)
        with pytest.raises(ValueError):
            owner.set_time_limit(-10)
    
    def test_owner_all_preferences(self):
        owner = Owner("Alex")
        owner.set_preference("key1", "value1")
        owner.set_preference("key2", "value2")
        prefs = owner.get_all_preferences()
        assert prefs["key1"] == "value1"
        assert prefs["key2"] == "value2"


class TestPet:  # ✅ Fixed: PascalCase
    def test_pet_creation(self):
        pet = Pet("Biscuit", "Dog", "Golden Retriever", 3)
        assert pet.get_name() == "Biscuit"
        assert pet.get_species() == "Dog"
        assert pet.get_breed() == "Golden Retriever"
        assert pet.get_age() == 3
    
    def test_pet_medical_conditions(self):  # ✅ Fixed: method name
        pet = Pet("Biscuit", "Dog", medical_conditions=["diabetic", "allergies"])
        assert pet.has_medical_condition("diabetic")
        assert pet.has_medical_condition("allergies")
        assert not pet.has_medical_condition("arthritis")
    
    def test_pet_medical_conditions_case_insensitive(self):  # ✅ Fixed: method name
        pet = Pet("Biscuit", "Dog", medical_conditions=["Diabetic"])
        assert pet.has_medical_condition("diabetic")
        assert pet.has_medical_condition("DIABETIC")
    
    def test_pet_add_remove_medical_conditions(self):  # ✅ Fixed: method name
        pet = Pet("Biscuit", "Dog")
        pet.add_medical_condition("diabetic")
        assert pet.has_medical_condition("diabetic")
        pet.remove_medical_condition("diabetic")
        assert not pet.has_medical_condition("diabetic")


class TestTask:  # ✅ Fixed: PascalCase
    def setup_method(self):
        Task._next_id = 1
    
    def test_task_creation(self):
        task = Task("Morning walk", 30, priority=Priority.HIGH, category="walk")
        assert task.get_description() == "Morning walk"
        assert task.get_duration() == 30
        assert task.get_priority() == Priority.HIGH
        assert task.get_category() == "walk"
        assert task.get_priority_label() == "high"
    
    def test_task_priority_labels(self):
        task_low = Task("Test", 10, Priority.LOW)
        task_med = Task("Test", 10, Priority.MEDIUM)
        task_high = Task("Test", 10, Priority.HIGH)
        task_critical = Task("Test", 10, Priority.CRITICAL)
        
        assert task_low.get_priority_label() == "low"
        assert task_med.get_priority_label() == "medium"
        assert task_high.get_priority_label() == "high"
        assert task_critical.get_priority_label() == "critical"
    
    def test_task_auto_increment_id(self):
        task1 = Task("First", 10)
        task2 = Task("Second", 20)
        task3 = Task("Third", 30)
        
        assert task1.get_id() == 1
        assert task2.get_id() == 2
        assert task3.get_id() == 3
    
    def test_task_priority_validation(self):
        with pytest.raises(ValueError, match="Priority must be between 1 and 4"):
            Task("Test", 10, priority=0)
        with pytest.raises(ValueError, match="Priority must be between 1 and 4"):
            Task("Test", 10, priority=5)
    
    def test_task_is_high_priority(self):
        low_task = Task("Low", 10, Priority.LOW)
        medium_task = Task("Medium", 10, Priority.MEDIUM)
        high_task = Task("High", 10, Priority.HIGH)
        critical_task = Task("Critical", 10, Priority.CRITICAL)
        
        assert not low_task.is_high_priority()
        assert not medium_task.is_high_priority()
        assert high_task.is_high_priority()
        assert critical_task.is_high_priority()
    
    def test_task_is_critical(self):
        low_task = Task("Low", 10, Priority.LOW)
        medium_task = Task("Medium", 10, Priority.MEDIUM)
        high_task = Task("High", 10, Priority.HIGH)
        critical_task = Task("Critical", 10, Priority.CRITICAL)
        
        assert not low_task.is_critical()
        assert not medium_task.is_critical()
        assert not high_task.is_critical()
        assert critical_task.is_critical()
    
    def test_task_setters(self):
        task = Task("Original", 30, Priority.MEDIUM, "walk")
        
        task.set_description("New description")
        assert task.get_description() == "New description"
        
        task.set_duration_minutes(45)
        assert task.get_duration() == 45
        
        with pytest.raises(ValueError, match="Duration must be positive"):
            task.set_duration_minutes(-5)
        
        task.set_priority(Priority.HIGH)
        assert task.get_priority() == Priority.HIGH
        
        task.set_category("feed")
        assert task.get_category() == "feed"
        
        task.set_preferred_time("morning")
        assert task.get_preferred_time() == "morning"
    
    def test_task_recurring_daily(self):
        task = Task(
            "Daily task",
            10,
            is_recurring=True,
            recurring_pattern="daily"
        )
        
        assert task.get_is_recurring()
        assert task.get_recurring_pattern() == "daily"
        
        assert task.occurs_on("2026-06-24")
        assert task.occurs_on("2026-06-25")
        assert task.occurs_on("2026-06-26")
    
    def test_task_recurring_weekly(self):
        """Test weekly recurring tasks."""
        task = Task(
            "Weekly task",
            10,
            is_recurring=True,
            recurring_pattern="weekly",
            recurring_days=["Monday", "Wednesday", "Friday"]
        )
        
        assert task.get_is_recurring()
        assert task.get_recurring_pattern() == "weekly"
        assert task.get_recurring_days() == ["Monday", "Wednesday", "Friday"]
        
        # Test specific dates - Using actual 2026 dates
        # July 6, 2026 is a Monday
        assert task.occurs_on("2026-07-06")  # Monday
        assert not task.occurs_on("2026-07-07")  # Tuesday
        assert task.occurs_on("2026-07-08")  # Wednesday
        assert not task.occurs_on("2026-07-09")  # Thursday
        assert task.occurs_on("2026-07-10")  # Friday
        assert not task.occurs_on("2026-07-11")  # Saturday
        assert not task.occurs_on("2026-07-12")  # Sunday
    
    def test_task_repr(self):
        """Test the string representation."""
        task = Task("Morning walk", 30, Priority.HIGH, "walk")
        repr_str = repr(task)
        assert "Morning walk" in repr_str
        assert "30" in repr_str
        assert "high" in repr_str
        assert "priority_label='high'" in repr_str


class TestPlannedTask:
    # ... other tests ...
    
    def test_planned_task_time_strings(self):
        """Test time string formatting."""
        task = Task("Test", 30)
        
        # 8:00 AM
        planned = PlannedTask(task, 480)
        assert planned.get_start_time_str() == "08:00"
        assert planned.get_end_time_str() == "08:30"
        
        # 2:30 PM (14:30)
        planned = PlannedTask(task, 870)
        assert planned.get_start_time_str() == "14:30"
        assert planned.get_end_time_str() == "15:00"
        
        # Midnight
        planned = PlannedTask(task, 0)
        assert planned.get_start_time_str() == "00:00"
        assert planned.get_end_time_str() == "00:30"
        
        # 11:59 PM
        planned = PlannedTask(task, 1439)
        assert planned.get_start_time_str() == "23:59"
        assert planned.get_end_time_str() == "00:29"  # Wraps to next day
    
    def test_planned_task_repr(self):
        """Test the string representation."""
        task = Task("Morning walk", 30)
        planned = PlannedTask(task, 480, "Scheduled in morning")
        repr_str = repr(planned)
        assert "08:00" in repr_str
        assert "08:30" in repr_str
        assert "Morning walk" in repr_str

class TestPlannedTask:  # ✅ Fixed: PascalCase
    def test_planned_task_creation(self):
        task = Task("Morning walk", 30, Priority.HIGH)
        planned = PlannedTask(task, 480)
        
        assert planned.get_task() == task
        assert planned.get_start_time() == 480
        assert planned.get_end_time() == 510
        assert planned.get_reason() == ""
    
    def test_planned_task_with_reason(self):
        task = Task("Morning walk", 30)
        reason = "High priority walk scheduled early"
        planned = PlannedTask(task, 480, reason)
        
        assert planned.get_reason() == reason
    
    def test_planned_task_set_reason(self):
        task = Task("Morning walk", 30)
        planned = PlannedTask(task, 480)
        assert planned.get_reason() == ""
        
        planned.set_reason("Updated reason")
        assert planned.get_reason() == "Updated reason"
    
    def test_planned_task_time_strings(self):
        """Test time string formatting."""
        task = Task("Test", 30)
        
        # 8:00 AM
        planned = PlannedTask(task, 480)
        assert planned.get_start_time_str() == "08:00"
        assert planned.get_end_time_str() == "08:30"
        
        # 2:30 PM (14:30)
        planned = PlannedTask(task, 870)
        assert planned.get_start_time_str() == "14:30"
        assert planned.get_end_time_str() == "15:00"
        
        # Midnight
        planned = PlannedTask(task, 0)
        assert planned.get_start_time_str() == "00:00"
        assert planned.get_end_time_str() == "00:30"
        
        # 11:59 PM (23:59)
        planned = PlannedTask(task, 1439)
        assert planned.get_start_time_str() == "23:59"
        # ✅ Fixed: Now correctly wraps to 00:29
        assert planned.get_end_time_str() == "00:29"
    
    def test_planned_task_overlap(self):
        task1 = Task("Task 1", 30)
        task2 = Task("Task 2", 20)
        
        planned1 = PlannedTask(task1, 480)
        planned2 = PlannedTask(task2, 510)
        assert not planned1.overlaps_with(planned2)
        assert not planned2.overlaps_with(planned1)
        
        planned1 = PlannedTask(task1, 480)
        planned2 = PlannedTask(task2, 495)
        assert planned1.overlaps_with(planned2)
        assert planned2.overlaps_with(planned1)
        
        planned1 = PlannedTask(task1, 480)
        planned2 = PlannedTask(task2, 510)
        assert not planned1.overlaps_with(planned2)
    
    def test_planned_task_repr(self):
        task = Task("Morning walk", 30)
        planned = PlannedTask(task, 480, "Scheduled in morning")
        repr_str = repr(planned)
        assert "08:00" in repr_str
        assert "08:30" in repr_str
        assert "Morning walk" in repr_str


class TestDailyPlan:  # ✅ Fixed: PascalCase
    def test_daily_plan_creation(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        assert plan.get_scheduled_tasks() == []
        assert plan.get_excluded_tasks() == []
        assert plan.get_total_planned_minutes() == 0
        assert plan.get_total_available_minutes() == 120
        assert plan.get_remaining_minutes() == 120
    
    def test_daily_plan_set_date(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        plan.set_date("2026-06-24")
        assert plan.get_summary() is not None
    
    def test_daily_plan_add_planned_task(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        
        task1 = Task("Walk", 30)
        task2 = Task("Feed", 15)
        
        planned1 = PlannedTask(task1, 480)
        planned2 = PlannedTask(task2, 520)
        
        plan.add_planned_task(planned1)
        assert len(plan.get_scheduled_tasks()) == 1
        assert plan.get_total_planned_minutes() == 30
        assert plan.get_remaining_minutes() == 90
        
        plan.add_planned_task(planned2)
        assert len(plan.get_scheduled_tasks()) == 2
        assert plan.get_total_planned_minutes() == 45
        assert plan.get_remaining_minutes() == 75
    
    def test_daily_plan_add_excluded_task(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        
        task = Task("Grooming", 45)
        reason = "Not enough time remaining"
        
        plan.add_excluded_task(task, reason)
        excluded = plan.get_excluded_tasks()
        
        assert len(excluded) == 1
        assert excluded[0][0] == task
        assert excluded[0][1] == reason
    
    def test_daily_plan_get_scheduled_tasks_returns_copy(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        task = Task("Walk", 30)
        planned = PlannedTask(task, 480)
        plan.add_planned_task(planned)
        
        tasks = plan.get_scheduled_tasks()
        tasks.append(PlannedTask(Task("Another", 10), 500))
        
        assert len(plan.get_scheduled_tasks()) == 1
    
    def test_daily_plan_get_excluded_tasks_returns_copy(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        task = Task("Grooming", 45)
        plan.add_excluded_task(task, "No time")
        
        excluded = plan.get_excluded_tasks()
        excluded.append((Task("Another", 10), "Test"))
        
        assert len(plan.get_excluded_tasks()) == 1
    
    def test_daily_plan_generate_summary(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        plan.set_date("2026-06-24")
        
        task1 = Task("Walk", 30)
        task2 = Task("Feed", 15)
        planned1 = PlannedTask(task1, 480)
        planned2 = PlannedTask(task2, 520)
        plan.add_planned_task(planned1)
        plan.add_planned_task(planned2)
        
        task3 = Task("Grooming", 45)
        plan.add_excluded_task(task3, "No time remaining")
        
        summary = plan.generate_summary()
        
        assert "Biscuit" in summary
        assert "Alex" in summary
        assert "2026-06-24" in summary
        assert "45 min" in summary
        assert "120" in summary
    
    def test_daily_plan_get_formatted_plan(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        plan.set_date("2026-06-24")
        
        task1 = Task("Morning walk", 30, Priority.HIGH, "walk")
        task2 = Task("Feeding", 15, Priority.CRITICAL, "feed")
        planned1 = PlannedTask(task1, 480, "High priority task")
        planned2 = PlannedTask(task2, 520, "Critical task")
        plan.add_planned_task(planned1)
        plan.add_planned_task(planned2)
        
        task3 = Task("Grooming", 45, Priority.LOW, "groom")
        plan.add_excluded_task(task3, "Not enough time")
        
        formatted = plan.get_formatted_plan()
        
        assert any("Daily Plan for Biscuit" in line for line in formatted)
        assert any("Morning walk" in line for line in formatted)
        assert any("Feeding" in line for line in formatted)
        assert any("Grooming" in line for line in formatted)
    
    def test_daily_plan_empty_plan(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        plan.set_date("2026-06-24")
        
        formatted = plan.get_formatted_plan()
        
        assert any("Daily Plan for Biscuit" in line for line in formatted)
    
    def test_daily_plan_only_excluded_tasks(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        plan.set_date("2026-06-24")
        
        task = Task("Grooming", 45)
        plan.add_excluded_task(task, "No time")
        
        formatted = plan.get_formatted_plan()
        
        assert any("Skipped Tasks" in line for line in formatted)
        assert any("Grooming" in line for line in formatted)
    
    def test_daily_plan_repr(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        plan.set_date("2026-06-24")
        
        task = Task("Walk", 30)
        planned = PlannedTask(task, 480)
        plan.add_planned_task(planned)
        
        repr_str = repr(plan)
        assert "Biscuit" in repr_str
    
    def test_daily_plan_remaining_minutes(self):
        plan = DailyPlan("Biscuit", "Alex", 120)
        assert plan.get_remaining_minutes() == 120
        
        task1 = Task("Task 1", 30)
        task2 = Task("Task 2", 45)
        plan.add_planned_task(PlannedTask(task1, 480))
        assert plan.get_remaining_minutes() == 90
        
        plan.add_planned_task(PlannedTask(task2, 520))
        assert plan.get_remaining_minutes() == 45