import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Any
import pandas as pd

# Import your models and scheduler
from models import Owner, Pet, Task, Priority
from scheduler import Scheduler

# Page configuration
st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        margin-bottom: 0.5rem;
    }
    .plan-card {
        background-color: #F0F8FF;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1rem 0;
    }
    .task-scheduled {
        background-color: #E8F5E9;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 3px solid #4CAF50;
    }
    .task-excluded {
        background-color: #FFEBEE;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 3px solid #F44336;
    }
    .priority-critical {
        color: #D32F2F;
        font-weight: bold;
    }
    .priority-high {
        color: #E65100;
        font-weight: bold;
    }
    .priority-medium {
        color: #F57C00;
    }
    .priority-low {
        color: #388E3C;
    }
    .reason-text {
        font-size: 0.9rem;
        color: #555;
        font-style: italic;
        margin-top: 0.25rem;
        padding-left: 1rem;
        border-left: 2px solid #90CAF9;
    }
    .stats-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
    }
    .scenario-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF9800;
        margin: 1rem 0;
    }
    .build-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    .demo-box {
        background-color: #F3E5F5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #9C27B0;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables."""
    if 'owner' not in st.session_state:
        st.session_state.owner = None
    if 'pet' not in st.session_state:
        st.session_state.pet = None
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    if 'scheduler' not in st.session_state:
        st.session_state.scheduler = None
    if 'daily_plan' not in st.session_state:
        st.session_state.daily_plan = None
    if 'task_counter' not in st.session_state:
        st.session_state.task_counter = 0
    if 'editing_task_index' not in st.session_state:
        st.session_state.editing_task_index = None
    if 'owner_saved' not in st.session_state:
        st.session_state.owner_saved = False
    if 'pet_saved' not in st.session_state:
        st.session_state.pet_saved = False
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
    if 'demo_tasks' not in st.session_state:
        st.session_state.demo_tasks = []

init_session_state()

# Helper functions
def get_priority_value(priority_label: str) -> int:
    """Convert priority label to numeric value."""
    mapping = {
        'low': Priority.LOW,
        'medium': Priority.MEDIUM,
        'high': Priority.HIGH,
        'critical': Priority.CRITICAL
    }
    return mapping.get(priority_label.lower(), Priority.MEDIUM)

def get_priority_label(priority_value: int) -> str:
    """Convert priority value to label."""
    mapping = {
        Priority.LOW: 'low',
        Priority.MEDIUM: 'medium',
        Priority.HIGH: 'high',
        Priority.CRITICAL: 'critical'
    }
    return mapping.get(priority_value, 'medium')

def get_priority_color(priority_value: int) -> str:
    """Get CSS color class for priority."""
    mapping = {
        Priority.CRITICAL: 'priority-critical',
        Priority.HIGH: 'priority-high',
        Priority.MEDIUM: 'priority-medium',
        Priority.LOW: 'priority-low'
    }
    return mapping.get(priority_value, '')

def create_task_from_form(description: str, duration: int, priority_label: str, 
                          category: str, preferred_time: str = None,
                          is_recurring: bool = False, 
                          recurring_pattern: str = 'daily',
                          recurring_days: List[str] = None) -> Task:
    """Create a Task object from form inputs."""
    priority = get_priority_value(priority_label)
    
    # Convert preferred time
    if preferred_time == 'None' or not preferred_time:
        preferred_time = None
    
    # Handle recurrence
    if is_recurring and recurring_pattern == 'weekly' and recurring_days:
        if isinstance(recurring_days, str):
            recurring_days = [day.strip() for day in recurring_days.split(',') if day.strip()]
        elif not recurring_days:
            recurring_days = []
    else:
        recurring_days = None
    
    return Task(
        description=description,
        duration_minutes=duration,
        priority=priority,
        category=category,
        preferred_time=preferred_time,
        is_recurring=is_recurring,
        recurring_pattern=recurring_pattern if is_recurring else None,
        recurring_days=recurring_days if is_recurring and recurring_pattern == 'weekly' else None
    )

def format_plan_for_display(plan) -> str:
    """Format the plan as a readable string."""
    lines = plan.get_formatted_plan()
    return "\n".join(lines)

# Main UI
st.markdown('<p class="main-header">🐾 PawPal+</p>', unsafe_allow_html=True)
st.caption("Your Pet Care Planning Assistant")

# Welcome/Intro section with Scenario and What you need to build
if st.session_state.show_welcome:
    with st.expander("📖 Scenario", expanded=True):
        st.markdown("""
        <div class="scenario-box">
        <h4>🐾 The Problem</h4>
        <p>
        A busy pet owner needs help staying consistent with pet care. They want an assistant that can:
        </p>
        <ul>
            <li>📝 Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)</li>
            <li>⏰ Consider constraints (time available, priority, owner preferences)</li>
            <li>📅 Produce a daily plan and <strong>explain why it chose that plan</strong></li>
        </ul>
        <p>
        <strong>PawPal+</strong> is a pet care planning assistant that helps pet owners plan care tasks
        for their pet(s) based on constraints like time, priority, and preferences.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🎯 What You Need to Build", expanded=True):
        st.markdown("""
        <div class="build-box">
        <h4>🔧 System Requirements</h4>
        <p>At minimum, your system should:</p>
        <ul>
            <li>✅ <strong>Represent pet care tasks</strong> - what needs to happen, how long it takes, priority</li>
            <li>✅ <strong>Represent the pet and the owner</strong> - basic info and preferences</li>
            <li>✅ <strong>Build a plan/schedule for a day</strong> - chooses and orders tasks based on constraints</li>
            <li>✅ <strong>Explain the plan</strong> - why each task was chosen and when it happens</li>
        </ul>
        <p>
        <strong>Ready to get started?</strong> Use the sidebar to enter your info, add tasks, and generate your first schedule!
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Demo Section (from original starter app)
    with st.expander("🚀 Quick Demo Inputs", expanded=True):
        st.markdown("""
        <div class="demo-box">
        <h4>⚡ Quick Start Demo</h4>
        <p>Try out PawPal+ with some sample inputs before setting up everything!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            demo_owner = st.text_input("Owner name", value="Jordan", key="demo_owner")
            demo_pet = st.text_input("Pet name", value="Mochi", key="demo_pet")
            demo_species = st.selectbox("Species", ["dog", "cat", "other"], key="demo_species")
        
        with col2:
            st.markdown("### Add a Task")
            demo_task_title = st.text_input("Task title", value="Morning walk", key="demo_task_title")
            demo_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="demo_duration")
            demo_priority = st.selectbox("Priority", ["low", "medium", "high","critical"], index=2, key="demo_priority")
            
            if st.button("➕ Add Demo Task", key="add_demo_task"):
                st.session_state.demo_tasks.append({
                    "title": demo_task_title,
                    "duration_minutes": int(demo_duration),
                    "priority": demo_priority
                })
                st.success(f"✅ Added: {demo_task_title}")
                st.rerun()
        
        if st.session_state.demo_tasks:
            st.write("Demo Tasks:")
            st.table(st.session_state.demo_tasks)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy to Main Tasks", key="copy_demo_tasks"):
                    for demo_task in st.session_state.demo_tasks:
                        # Convert demo task to real Task object
                        task = create_task_from_form(
                            description=demo_task["title"],
                            duration=demo_task["duration_minutes"],
                            priority_label=demo_task["priority"],
                            category="other",
                            preferred_time=None,
                            is_recurring=False
                        )
                        st.session_state.tasks.append(task)
                    
                    # Update scheduler
                    if st.session_state.owner and st.session_state.pet:
                        st.session_state.scheduler = Scheduler(
                            st.session_state.owner,
                            st.session_state.pet,
                            st.session_state.tasks
                        )
                    
                    st.success(f"✅ Copied {len(st.session_state.demo_tasks)} tasks to main tasks!")
                    st.session_state.demo_tasks = []
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Clear Demo Tasks", key="clear_demo_tasks"):
                    st.session_state.demo_tasks = []
                    st.rerun()
        else:
            st.info("No demo tasks yet. Add one above!")
    
    # Dismiss button
    if st.button("🚀 Get Started with Full App!", use_container_width=True):
        st.session_state.show_welcome = False
        st.rerun()
    
    st.divider()

# Sidebar for owner and pet info
with st.sidebar:
    st.header("📋 Owner & Pet Info")
    
    with st.expander("👤 Owner Details", expanded=not st.session_state.owner_saved):
        owner_name = st.text_input("Owner Name", value=st.session_state.owner.get_name() if st.session_state.owner else "Jordan", key="owner_name_input")
        daily_time_limit = st.number_input(
            "⏱️ Daily Time Limit (minutes)", 
            min_value=30, 
            max_value=720, 
            value=st.session_state.owner.get_time_limit() if st.session_state.owner else 120,
            step=15,
            key="time_limit_input",
            help="Maximum minutes per day you can dedicate to pet care"
        )
        
        owner_preferences = st.multiselect(
            "🎯 Owner Preferences",
            options=['morning_person', 'evening_person', 'prefer_walks', 'prefer_indoor', 'busy_mornings', 'busy_afternoons'],
            default=st.session_state.owner.get_all_preferences().keys() if st.session_state.owner else ['morning_person'],
            key="owner_prefs"
        )
    
    with st.expander("🐕 Pet Details", expanded=not st.session_state.pet_saved):
        pet_name = st.text_input("Pet Name", value=st.session_state.pet.get_name() if st.session_state.pet else "Mochi", key="pet_name_input")
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Rabbit", "Other"], 
                              index=0 if not st.session_state.pet else ["Dog", "Cat", "Bird", "Rabbit", "Other"].index(st.session_state.pet.get_species()) if st.session_state.pet.get_species() in ["Dog", "Cat", "Bird", "Rabbit", "Other"] else 0,
                              key="species_input")
        breed = st.text_input("Breed (optional)", value=st.session_state.pet.get_breed() if st.session_state.pet else "", key="breed_input")
        pet_age = st.number_input("Age (years)", min_value=0, max_value=30, 
                                 value=st.session_state.pet.get_age() if st.session_state.pet else 2, 
                                 key="age_input")
        pet_weight = st.number_input("Weight (kg)", min_value=0.0, max_value=100.0, 
                                    value=st.session_state.pet.get_weight() if st.session_state.pet else 0.0,
                                    step=0.5,
                                    key="weight_input")
        
        medical_conditions = st.multiselect(
            "🏥 Medical Conditions",
            options=['diabetic', 'allergies', 'arthritis', 'heart_condition', 'blind', 'deaf', 'senior', 'puppy'],
            default=st.session_state.pet.get_medical_conditions() if st.session_state.pet else [],
            key="medical_conditions"
        )
    
    # Save pet and owner info button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Info", key="save_info", use_container_width=True):
            # Create or update owner
            if st.session_state.owner is None:
                st.session_state.owner = Owner(owner_name, daily_time_limit)
            else:
                # Update existing owner
                st.session_state.owner = Owner(owner_name, daily_time_limit)
            
            for pref in owner_preferences:
                st.session_state.owner.set_preference(pref, True)
            st.session_state.owner_saved = True
            
            # Create or update pet
            st.session_state.pet = Pet(
                name=pet_name,
                species=species,
                breed=breed,
                age=pet_age,
                weight=pet_weight,
                medical_conditions=medical_conditions
            )
            st.session_state.pet_saved = True
            
            # Update scheduler if tasks exist
            if st.session_state.tasks:
                st.session_state.scheduler = Scheduler(
                    st.session_state.owner,
                    st.session_state.pet,
                    st.session_state.tasks
                )
            
            st.success(f"✅ Saved! {owner_name} & {pet_name}")
            st.balloons()
    
    with col2:
        if st.button("🔄 Reset", key="reset_info", use_container_width=True):
            st.session_state.owner = None
            st.session_state.pet = None
            st.session_state.owner_saved = False
            st.session_state.pet_saved = False
            st.session_state.daily_plan = None
            st.rerun()
    
    # Show current status
    if st.session_state.owner_saved and st.session_state.pet_saved:
        st.success(f"✅ {st.session_state.owner.get_name()} & {st.session_state.pet.get_name()}")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📝 Tasks", "📅 Schedule", "📊 Statistics", "ℹ️ About"])

# Tab 1: Task Management
with tab1:
    st.header("📝 Manage Tasks")
    
    # Check if owner and pet info is saved
    if not st.session_state.owner_saved or not st.session_state.pet_saved:
        st.warning("⚠️ Please save owner and pet info in the sidebar first!")
    
    # Add/Edit Task
    st.subheader("Add New Task" if st.session_state.editing_task_index is None else "✏️ Edit Task")
    
    with st.form(key="task_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_description = st.text_input(
                "Task Description *", 
                value="",
                key="task_desc"
            )
            task_duration = st.number_input(
                "⏱️ Duration (minutes) *", 
                min_value=1, 
                max_value=240, 
                value=30,
                key="task_duration"
            )
            task_priority = st.selectbox(
                "⭐ Priority *", 
                ["low", "medium", "high", "critical"],
                index=2,
                key="task_priority"
            )
        
        with col2:
            task_category = st.selectbox(
                "📂 Category",
                ["walk", "feed", "med", "enrichment", "groom", "vet", "training", "other"],
                index=0,
                key="task_category"
            )
            preferred_time = st.selectbox(
                "🕐 Preferred Time",
                ["None", "morning", "afternoon", "evening"],
                index=0,
                key="task_preferred_time"
            )
            
            is_recurring = st.checkbox("🔄 Recurring Task", key="task_recurring")
            
            if is_recurring:
                recurring_pattern = st.selectbox(
                    "Recurring Pattern",
                    ["daily", "weekly"],
                    key="task_recurring_pattern"
                )
                
                if recurring_pattern == "weekly":
                    recurring_days = st.multiselect(
                        "Days of Week",
                        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                        default=["Monday", "Wednesday", "Friday"],
                        key="task_recurring_days"
                    )
                else:
                    recurring_days = []
            else:
                recurring_pattern = "daily"
                recurring_days = []
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button(
                "💾 Save Task" if st.session_state.editing_task_index is None else "✏️ Update Task",
                use_container_width=True
            )
        with col2:
            if st.session_state.editing_task_index is not None:
                if st.form_submit_button("❌ Cancel Edit", use_container_width=True):
                    st.session_state.editing_task_index = None
                    st.rerun()
        
        if submit_button:
            if not task_description:
                st.error("Please enter a task description")
            else:
                try:
                    # Create task
                    task = create_task_from_form(
                        description=task_description,
                        duration=task_duration,
                        priority_label=task_priority,
                        category=task_category,
                        preferred_time=preferred_time if preferred_time != "None" else None,
                        is_recurring=is_recurring,
                        recurring_pattern=recurring_pattern,
                        recurring_days=recurring_days
                    )
                    
                    # Add or update task
                    if st.session_state.editing_task_index is not None:
                        st.session_state.tasks[st.session_state.editing_task_index] = task
                        st.session_state.editing_task_index = None
                        st.success("✅ Task updated!")
                    else:
                        st.session_state.tasks.append(task)
                        st.success("✅ Task added!")
                    
                    # Update scheduler
                    if st.session_state.owner and st.session_state.pet:
                        st.session_state.scheduler = Scheduler(
                            st.session_state.owner,
                            st.session_state.pet,
                            st.session_state.tasks
                        )
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error creating task: {str(e)}")
    
    # Task List
    st.subheader("📋 Your Tasks")
    
    if not st.session_state.tasks:
        st.info("No tasks yet. Add your first pet care task above!")
    else:
        # Display tasks in a nice format
        for idx, task in enumerate(st.session_state.tasks):
            priority_label = task.get_priority_label()
            color_class = get_priority_color(task.get_priority())
            
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([3, 1.5, 1.5, 1.5, 0.8, 0.8])
                
                with col1:
                    st.write(f"**{task.get_description()}**")
                with col2:
                    st.write(f"{task.get_duration()} min")
                with col3:
                    st.markdown(f'<span class="{color_class}">{priority_label.capitalize()}</span>', unsafe_allow_html=True)
                with col4:
                    st.write(task.get_category())
                with col5:
                    if task.get_is_recurring():
                        pattern = task.get_recurring_pattern()
                        if pattern == 'daily':
                            st.write("📅 Daily")
                        else:
                            st.write("📅 Weekly")
                    else:
                        st.write("❌")
                with col6:
                    if st.button("🗑️", key=f"delete_{idx}"):
                        st.session_state.tasks.pop(idx)
                        if st.session_state.scheduler and st.session_state.owner and st.session_state.pet:
                            st.session_state.scheduler = Scheduler(
                                st.session_state.owner,
                                st.session_state.pet,
                                st.session_state.tasks
                            )
                        st.rerun()
                
                # Show recurrence details
                if task.get_is_recurring() and task.get_recurring_pattern() == 'weekly':
                    days = task.get_recurring_days()
                    st.caption(f"📅 Repeats on: {', '.join(days)}")
                
                st.divider()
        
        st.caption(f"Total: {len(st.session_state.tasks)} tasks")

# Tab 2: Schedule Generation
with tab2:
    st.header("📅 Generate Daily Schedule")
    
    # Check if we have everything needed
    if not st.session_state.owner_saved or not st.session_state.pet_saved:
        st.warning("⚠️ Please save owner and pet info in the sidebar first!")
    elif not st.session_state.tasks:
        st.warning("⚠️ Please add at least one task in the Tasks tab!")
    else:
        # Schedule generation options
        col1, col2 = st.columns(2)
        with col1:
            schedule_date = st.date_input(
                "📅 Select Date",
                value=datetime.now(),
                key="schedule_date"
            )
        
        with col2:
            if st.session_state.scheduler is None:
                st.session_state.scheduler = Scheduler(
                    st.session_state.owner,
                    st.session_state.pet,
                    st.session_state.tasks
                )
            
            time_limit = st.number_input(
                "⏱️ Daily Time Limit (minutes)",
                min_value=30,
                max_value=720,
                value=st.session_state.owner.get_time_limit(),
                step=15,
                key="schedule_time_limit"
            )
            # Update owner time limit if changed
            if time_limit != st.session_state.owner.get_time_limit():
                st.session_state.owner.set_time_limit(time_limit)
        
        # Generate schedule button
        if st.button("🚀 Generate Schedule", use_container_width=True, key="generate_schedule"):
            with st.spinner("🧠 Generating schedule..."):
                try:
                    date_str = schedule_date.strftime('%Y-%m-%d')
                    
                    # Update scheduler with latest tasks
                    st.session_state.scheduler = Scheduler(
                        st.session_state.owner,
                        st.session_state.pet,
                        st.session_state.tasks
                    )
                    
                    # Generate plan
                    st.session_state.daily_plan = st.session_state.scheduler.generate_daily_plan(date_str)
                    
                    st.success("✅ Schedule generated successfully!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Error generating schedule: {str(e)}")
        
        # Display plan if it exists
        if st.session_state.daily_plan:
            plan = st.session_state.daily_plan
            
            # Summary
            st.markdown("### 📋 Schedule Summary")
            summary = plan.get_summary()
            st.info(summary)
            
            # Stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📋 Scheduled Tasks", len(plan.get_scheduled_tasks()))
            with col2:
                st.metric("❌ Excluded Tasks", len(plan.get_excluded_tasks()))
            with col3:
                st.metric("⏱️ Time Used", f"{plan.get_total_planned_minutes()} min")
            with col4:
                remaining = plan.get_remaining_minutes()
                st.metric("⏱️ Time Remaining", f"{remaining} min")
            
            # Scheduled tasks
            st.markdown("### ✅ Scheduled Tasks")
            scheduled = plan.get_scheduled_tasks()
            if scheduled:
                for planned in sorted(scheduled, key=lambda p: p.get_start_time()):
                    task = planned.get_task()
                    priority_label = task.get_priority_label()
                    color_class = get_priority_color(task.get_priority())
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="task-scheduled">
                            <strong>🕐 {planned.get_start_time_str()} – {task.get_description()}</strong>
                            <span style="float: right;">({task.get_duration()} min)</span>
                            <br>
                            <span class="{color_class}">Priority: {priority_label}</span>
                            <span style="margin-left: 1rem;">Category: {task.get_category()}</span>
                            <div class="reason-text">
                                💡 {planned.get_reason()}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No tasks scheduled for this day.")
            
            # Excluded tasks
            st.markdown("### ❌ Excluded Tasks")
            excluded = plan.get_excluded_tasks()
            if excluded:
                for task, reason in excluded:
                    with st.container():
                        st.markdown(f"""
                        <div class="task-excluded">
                            <strong>{task.get_description()}</strong>
                            <span style="float: right;">({task.get_duration()} min)</span>
                            <br>
                            Priority: {task.get_priority_label()}
                            <div class="reason-text">
                                ℹ️ {reason}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("🎉 All tasks were successfully scheduled!")
            
            # Download plan as text
            if st.button("📥 Download Plan as Text", key="download_plan"):
                plan_text = format_plan_for_display(plan)
                st.download_button(
                    label="📄 Download Plan",
                    data=plan_text,
                    file_name=f"pawpal_plan_{schedule_date.strftime('%Y-%m-%d')}.txt",
                    mime="text/plain"
                )

# Tab 3: Statistics
with tab3:
    st.header("📊 Schedule Statistics")
    
    if st.session_state.daily_plan is None:
        st.info("Generate a schedule first to see statistics!")
    else:
        plan = st.session_state.daily_plan
        
        # Overall stats
        col1, col2, col3 = st.columns(3)
        with col1:
            utilization = (plan.get_total_planned_minutes() / plan.get_total_available_minutes() * 100)
            st.metric("📈 Utilization Rate", f"{utilization:.1f}%")
        with col2:
            total_tasks = len(plan.get_scheduled_tasks()) + len(plan.get_excluded_tasks())
            success_rate = len(plan.get_scheduled_tasks()) / total_tasks * 100 if total_tasks > 0 else 0
            st.metric("🎯 Success Rate", f"{success_rate:.1f}%")
        with col3:
            avg_duration = plan.get_total_planned_minutes() / len(plan.get_scheduled_tasks()) if plan.get_scheduled_tasks() else 0
            st.metric("⏱️ Avg Task Duration", f"{avg_duration:.0f} min")
        
        # Category breakdown
        st.markdown("### 📊 Task Categories")
        categories = {}
        for planned in plan.get_scheduled_tasks():
            task = planned.get_task()
            category = task.get_category()
            if category not in categories:
                categories[category] = {'count': 0, 'total_minutes': 0}
            categories[category]['count'] += 1
            categories[category]['total_minutes'] += task.get_duration()
        
        if categories:
            cat_data = []
            for cat, data in categories.items():
                cat_data.append({
                    'Category': cat.capitalize(),
                    'Count': data['count'],
                    'Total Minutes': data['total_minutes'],
                    'Avg Minutes': data['total_minutes'] / data['count']
                })
            df_cat = pd.DataFrame(cat_data)
            st.table(df_cat)
            
            # Bar chart
            st.bar_chart(df_cat.set_index('Category')['Count'])
        else:
            st.info("No scheduled tasks to analyze")
        
        # Priority breakdown
        st.markdown("### 🎯 Priority Distribution")
        priorities = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for planned in plan.get_scheduled_tasks():
            task = planned.get_task()
            label = task.get_priority_label()
            priorities[label] = priorities.get(label, 0) + 1
        
        if any(priorities.values()):
            priority_df = pd.DataFrame({
                'Priority': list(priorities.keys()),
                'Count': list(priorities.values())
            })
            st.bar_chart(priority_df.set_index('Priority'))
        
        # Time of day distribution
        st.markdown("### 🌅 Time Distribution")
        time_slots = {'Morning (6-12)': 0, 'Afternoon (12-17)': 0, 'Evening (17-22)': 0}
        for planned in plan.get_scheduled_tasks():
            start = planned.get_start_time()
            hour = start // 60
            if 6 <= hour < 12:
                time_slots['Morning (6-12)'] += 1
            elif 12 <= hour < 17:
                time_slots['Afternoon (12-17)'] += 1
            else:
                time_slots['Evening (17-22)'] += 1
        
        if any(time_slots.values()):
            time_df = pd.DataFrame({
                'Time Slot': list(time_slots.keys()),
                'Tasks': list(time_slots.values())
            })
            st.bar_chart(time_df.set_index('Time Slot'))
        
        # Schedule efficiency
        st.markdown("### 📈 Schedule Efficiency")
        col1, col2 = st.columns(2)
        with col1:
            scheduled_minutes = plan.get_total_planned_minutes()
            available_minutes = plan.get_total_available_minutes()
            st.metric(
                "⏱️ Time Used vs Available",
                f"{scheduled_minutes} / {available_minutes} min",
                delta=f"{available_minutes - scheduled_minutes} min remaining"
            )
        with col2:
            task_count = len(plan.get_scheduled_tasks())
            excluded_count = len(plan.get_excluded_tasks())
            st.metric(
                "📋 Tasks Scheduled vs Excluded",
                f"{task_count} / {excluded_count}",
                delta=f"{excluded_count} excluded"
            )

# Tab 4: About
with tab4:
    st.header("ℹ️ About PawPal+")
    
    st.markdown("""
    ### 🐾 PawPal+ - Smart Pet Care Planning
    
    PawPal+ helps busy pet owners stay consistent with pet care by:
    
    1. **📝 Tracking Tasks**: Keep track of all your pet care tasks
    2. **🧠 Smart Scheduling**: Automatically schedules tasks based on priorities and constraints
    3. **💡 Explains Decisions**: Each task comes with a reason for its scheduling
    4. **🔄 Adaptable**: Handles recurring tasks, preferences, and special needs
    
    ### How It Works
    
    **Scheduling Logic:**
    - Tasks are sorted by priority (Critical > High > Medium > Low)
    - Within same priority, shorter tasks are scheduled first
    - Tasks are placed in the earliest available time slots
    - If a task doesn't fit, it's excluded with an explanation
    
    **Constraints Considered:**
    - ⏱️ Daily time limit
    - 🕐 Working hours (6:00 AM - 10:00 PM)
    - ⭐ Task priorities
    - 👤 Owner preferences
    - 🏥 Pet medical conditions
    - 🔄 Task recurrence
    
    ### Technologies Used
    - **Streamlit**: Interactive web interface
    - **Python**: Core logic and scheduling
    - **Pytest**: Unit testing
    - **Pandas**: Data manipulation
    
    ### Getting Started
    1. 👤 Enter owner and pet info in the sidebar
    2. 📝 Add your pet care tasks in the Tasks tab
    3. 📅 Generate a schedule in the Schedule tab
    4. 📊 View statistics and insights in the Statistics tab
    
    ### Future Improvements
    - Multiple pet support
    - Calendar integration
    - Mobile notifications
    - AI-powered scheduling optimization
    - Social features (share with family)
    
    ---
    *Built as a Module 2 Project* 🎓
    """)

# Footer
st.divider()
st.caption("🐾 PawPal+ - Your Pet Care Planning Assistant | Made with ❤️")

# Debug information (hidden by default)
with st.expander("🔧 Debug Info (for developers)"):
    st.json({
        "owner": str(st.session_state.owner) if st.session_state.owner else None,
        "pet": str(st.session_state.pet) if st.session_state.pet else None,
        "tasks_count": len(st.session_state.tasks),
        "scheduler": str(st.session_state.scheduler) if st.session_state.scheduler else None,
        "plan_exists": st.session_state.daily_plan is not None,
        "owner_saved": st.session_state.owner_saved,
        "pet_saved": st.session_state.pet_saved,
        "editing_task": st.session_state.editing_task_index,
        "show_welcome": st.session_state.show_welcome,
        "demo_tasks_count": len(st.session_state.demo_tasks)
    })
