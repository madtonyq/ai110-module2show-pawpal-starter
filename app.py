import streamlit as st
from datetime import datetime
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

# Custom CSS for better styling with darker, more comfortable colors
st.markdown("""
    <style>
    /* Main background - softer dark */
    .stApp {
        background-color: #1a1a2e;
        color: #e0e0e0;
    }
    
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4fc3f7;
        margin-bottom: 0.5rem;
    }
    
    /* All text elements */
    .stApp, .stMarkdown, .stText, .stCaption, label {
        color: #e0e0e0 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #4fc3f7 !important;
        font-weight: 600 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        color: #e0e0e0 !important;
        background-color: #1a1a3e !important;
        border-radius: 5px !important;
        font-weight: 600 !important;
        border: 1px solid #2a2a4e !important;
    }
    .streamlit-expanderContent {
        background-color: #16213e !important;
        border-radius: 0 0 5px 5px !important;
        border: 1px solid #2a2a4e !important;
        border-top: none !important;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1l02zno {
        background-color: #0f0f1f !important;
    }
    .css-1d391kg .stMarkdown, .css-1l02zno .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Plan output - exactly matching the requested format */
    .plan-output {
        font-family: 'Courier New', monospace;
        background-color: #0f1f2f;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #2a3a5e;
        color: #e0e0e0;
        white-space: pre-wrap;
        line-height: 1.8;
    }
    .plan-output .comment {
        color: #666;
        font-style: italic;
    }
    .plan-output .header {
        color: #4fc3f7;
        font-weight: bold;
    }
    .plan-output .time {
        color: #4fc3f7;
    }
    .plan-output .priority-high {
        color: #ff9800;
    }
    .plan-output .priority-critical {
        color: #ef5350;
    }
    .plan-output .priority-medium {
        color: #ffd54f;
    }
    .plan-output .priority-low {
        color: #81c784;
    }
    .plan-output .reason {
        color: #90caf9;
        font-style: italic;
        padding-left: 2rem;
    }
    .plan-output .summary {
        color: #81c784;
        margin-top: 0.5rem;
    }
    .plan-output .excluded {
        color: #ef9a9a;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1a3a5e !important;
        color: #e0e0e0 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        border: 1px solid #2a5a7e !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #2a5a7e !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 195, 247, 0.3) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #0f1f2f !important;
        color: #e0e0e0 !important;
        border: 1px solid #2a3a5e !important;
        border-radius: 4px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4fc3f7 !important;
        box-shadow: 0 0 0 2px rgba(79, 195, 247, 0.2) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #0f1f2f !important;
        color: #e0e0e0 !important;
        border: 1px solid #2a3a5e !important;
        border-radius: 4px !important;
    }
    
    /* Number inputs */
    .stNumberInput > div > div > input {
        background-color: #0f1f2f !important;
        color: #e0e0e0 !important;
        border: 1px solid #2a3a5e !important;
        border-radius: 4px !important;
    }
    
    /* Alert boxes */
    .stAlert {
        color: #e0e0e0 !important;
        border-radius: 6px !important;
        background-color: #1a2a3a !important;
        border: 1px solid #2a3a5e !important;
    }
    
    /* DataFrames */
    .dataframe {
        color: #e0e0e0 !important;
        background-color: #0f1f2f !important;
        border-radius: 6px !important;
        border: 1px solid #2a3a5e !important;
    }
    .dataframe th {
        color: #4fc3f7 !important;
        background-color: #1a2a4a !important;
    }
    .dataframe td {
        color: #e0e0e0 !important;
    }
    
    /* Metrics */
    .stMetric {
        background-color: #0f1f2f !important;
        padding: 0.75rem !important;
        border-radius: 8px !important;
        border: 1px solid #2a3a5e !important;
    }
    .stMetric label {
        color: #90caf9 !important;
    }
    .stMetric .stMetric-value {
        color: #4fc3f7 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0f1f2f !important;
        border-radius: 8px !important;
        border: 1px solid #2a3a5e !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #90caf9 !important;
        border-radius: 6px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #1a3a5e !important;
        color: #4fc3f7 !important;
    }
    
    /* Multi-select */
    .stMultiSelect > div > div {
        background-color: #0f1f2f !important;
        color: #e0e0e0 !important;
        border: 1px solid #2a3a5e !important;
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        color: #e0e0e0 !important;
    }
    
    /* Dividers */
    hr {
        border-color: #2a3a5e !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None
if "daily_plan" not in st.session_state:
    st.session_state.daily_plan = None
if "owner_saved" not in st.session_state:
    st.session_state.owner_saved = False
if "pet_saved" not in st.session_state:
    st.session_state.pet_saved = False
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

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

def format_plan_output(plan) -> str:
    """
    Format the plan exactly like:
    # Daily plan for Biscuit (Golden Retriever):
    #   08:00 — Morning walk (30 min) [priority: high]
    #   09:00 — Feeding (10 min) [priority: high]
    """
    lines = []
    pet_name = plan.pet_name_
    
    # Get the pet object to access breed
    pet = None
    if st.session_state.pet:
        pet = st.session_state.pet
    
    # Format: # Daily plan for Biscuit (Golden Retriever):
    if pet and pet.get_breed():
        lines.append(f"# Daily plan for {pet_name} ({pet.get_breed()}):")
    else:
        lines.append(f"# Daily plan for {pet_name}:")
    
    # Scheduled tasks with exact format: #   08:00 — Morning walk (30 min) [priority: high]
    scheduled = plan.get_scheduled_tasks()
    if scheduled:
        for planned in sorted(scheduled, key=lambda p: p.get_start_time()):
            task = planned.get_task()
            time_str = planned.get_start_time_str()
            description = task.get_description()
            duration = task.get_duration()
            priority = task.get_priority_label()
            
            # Exact format: #   08:00 — Morning walk (30 min) [priority: high]
            lines.append(f"#   {time_str} — {description} ({duration} min) [priority: {priority}]")
            
            # Add reason as a comment line (optional)
            if planned.get_reason():
                lines.append(f"#     Reason: {planned.get_reason()}")
    
    # Add empty line between scheduled tasks and summary
    lines.append("#")
    
    # Add summary
    total_planned = plan.get_total_planned_minutes()
    total_available = plan.get_total_available_minutes()
    remaining = plan.get_remaining_minutes()
    lines.append(f"# ⏱️ Total planned: {total_planned} min / {total_available} min available")
    lines.append(f"# ⏱️ Remaining: {remaining} min")
    
    # Add excluded tasks if any
    excluded = plan.get_excluded_tasks()
    if excluded:
        lines.append("#")
        lines.append("# ❌ Skipped Tasks (could not fit):")
        for task, reason in excluded:
            lines.append(f"#   - {task.get_description()} ({task.get_duration()} min) [priority: {task.get_priority_label()}]")
            lines.append(f"#     Reason: {reason}")
    
    return "\n".join(lines)

def create_task_from_dict(task_dict: Dict) -> Task:
    """Create a Task object from a dictionary."""
    priority_value = get_priority_value(task_dict.get('priority', 'medium'))
    return Task(
        description=task_dict.get('title', ''),
        duration_minutes=task_dict.get('duration_minutes', 30),
        priority=priority_value,
        category=task_dict.get('category', 'other'),
        preferred_time=task_dict.get('preferred_time', None),
        is_recurring=task_dict.get('is_recurring', False),
        recurring_pattern=task_dict.get('recurring_pattern', None),
        recurring_days=task_dict.get('recurring_days', [])
    )

def create_task_from_form(description: str, duration: int, priority_label: str, 
                          category: str, preferred_time: str = None,
                          is_recurring: bool = False, 
                          recurring_pattern: str = 'daily',
                          recurring_days: List[str] = None) -> Task:
    """Create a Task object from form inputs."""
    priority = get_priority_value(priority_label)
    if preferred_time == 'None' or not preferred_time:
        preferred_time = None
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

# Main UI
st.markdown('<p class="main-header">🐾 PawPal+</p>', unsafe_allow_html=True)
st.caption("Your Pet Care Planning Assistant")

# Welcome section with Scenario and What you need to build
if st.session_state.show_welcome:
    with st.expander("Scenario", expanded=True):
        st.markdown(
            """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
        )

    with st.expander("What you need to build", expanded=True):
        st.markdown(
            """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
        )
    
    if st.button("🚀 Get Started", use_container_width=True):
        st.session_state.show_welcome = False
        st.rerun()
    
    st.divider()

# Sidebar for owner and pet info
with st.sidebar:
    st.header("📋 Owner & Pet Info")
    
    with st.expander("Owner Details", expanded=not st.session_state.owner_saved):
        owner_name = st.text_input("Owner name", value="Jordan", key="owner_name")
        daily_time_limit = st.number_input(
            "Daily Time Limit (minutes)", 
            min_value=30, 
            max_value=720, 
            value=120,
            step=15,
            key="time_limit",
            help="Maximum minutes per day for pet care"
        )
        
        owner_preferences = st.multiselect(
            "Owner Preferences",
            options=['morning_person', 'evening_person', 'prefer_walks', 'prefer_indoor'],
            default=['morning_person'],
            key="owner_prefs"
        )
    
    with st.expander("Pet Details", expanded=not st.session_state.pet_saved):
        pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
        species = st.selectbox(
            "Species", 
            ["Dog", "Cat", "Bird", "Rabbit", "Hamster", "Guinea Pig", "Fish", "Reptile", "Horse", "Other"],
            key="species"
        )
        breed = st.text_input("Breed (optional)", value="Golden Retriever", key="breed")
        pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=2, key="age")
        
        medical_conditions = st.multiselect(
            "Medical Conditions",
            options=['diabetic', 'allergies', 'arthritis', 'heart_condition', 'blind', 'deaf'],
            default=[],
            key="medical_conditions"
        )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Info", use_container_width=True):
            st.session_state.owner = Owner(owner_name, daily_time_limit)
            for pref in owner_preferences:
                st.session_state.owner.set_preference(pref, True)
            st.session_state.owner_saved = True
            
            st.session_state.pet = Pet(
                name=pet_name,
                species=species,
                breed=breed,
                age=pet_age,
                medical_conditions=medical_conditions
            )
            st.session_state.pet_saved = True
            
            if st.session_state.tasks:
                st.session_state.scheduler = Scheduler(
                    st.session_state.owner,
                    st.session_state.pet,
                    [create_task_from_dict(t) for t in st.session_state.tasks]
                )
            
            st.success(f"✅ Saved! {owner_name} & {pet_name}")
            st.balloons()
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.owner = None
            st.session_state.pet = None
            st.session_state.owner_saved = False
            st.session_state.pet_saved = False
            st.session_state.daily_plan = None
            st.session_state.tasks = []
            st.rerun()
    
    if st.session_state.owner_saved and st.session_state.pet_saved:
        st.success(f"✅ {st.session_state.owner.get_name()} & {st.session_state.pet.get_name()}")

st.divider()

# Quick Demo Inputs section
st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan", key="demo_owner")
pet_name = st.text_input("Pet name", value="Biscuit", key="demo_pet")
species = st.selectbox(
    "Species", 
    ["dog", "cat", "bird", "rabbit", "hamster", "guinea pig", "fish", "reptile", "horse", "other"],
    key="demo_species"
)
breed = st.text_input("Breed (optional)", value="Golden Retriever", key="demo_breed")

st.markdown("### Tasks")
st.caption("Add a few tasks. These will feed into your scheduler.")

priority_options = ["low", "medium", "high", "critical"]

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30, key="duration")
with col3:
    priority = st.selectbox("Priority", priority_options, index=2, key="priority")

# Advanced options for tasks
with st.expander("Advanced Task Options"):
    category = st.selectbox("Category", ["walk", "feed", "med", "enrichment", "groom", "vet", "training", "other"], index=0)
    preferred_time = st.selectbox("Preferred Time", ["None", "morning", "afternoon", "evening"], index=0)
    is_recurring = st.checkbox("Recurring Task")
    if is_recurring:
        recurring_pattern = st.selectbox("Recurring Pattern", ["daily", "weekly"])
        if recurring_pattern == "weekly":
            recurring_days = st.multiselect(
                "Days of Week",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                default=["Monday", "Wednesday", "Friday"]
            )
        else:
            recurring_days = []
    else:
        recurring_pattern = "daily"
        recurring_days = []

if st.button("Add task", key="add_task"):
    task_dict = {
        "title": task_title,
        "duration_minutes": int(duration),
        "priority": priority,
        "category": category if st.session_state.get('category') else "other",
        "preferred_time": preferred_time if preferred_time != "None" else None,
        "is_recurring": is_recurring if st.session_state.get('is_recurring') else False,
        "recurring_pattern": recurring_pattern if is_recurring else None,
        "recurring_days": recurring_days if is_recurring and recurring_pattern == "weekly" else []
    }
    st.session_state.tasks.append(task_dict)
    st.success(f"✅ Added: {task_title}")
    st.rerun()

if st.session_state.tasks:
    st.write("Current tasks:")
    task_df = pd.DataFrame(st.session_state.tasks)
    st.dataframe(task_df, use_container_width=True)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule based on your tasks, priorities, and constraints.")

# Check if we have everything needed
if not st.session_state.owner_saved or not st.session_state.pet_saved:
    st.warning("⚠️ Please save owner and pet info in the sidebar first!")
elif not st.session_state.tasks:
    st.warning("⚠️ Please add at least one task above!")
else:
    # Convert dict tasks to Task objects
    task_objects = [create_task_from_dict(t) for t in st.session_state.tasks]
    
    # Update scheduler
    if st.session_state.scheduler is None:
        st.session_state.scheduler = Scheduler(
            st.session_state.owner,
            st.session_state.pet,
            task_objects
        )
    
    # Schedule options
    col1, col2 = st.columns(2)
    with col1:
        schedule_date = st.date_input("Select Date", value=datetime.now(), key="schedule_date")
    
    with col2:
        # Update scheduler with latest tasks
        st.session_state.scheduler = Scheduler(
            st.session_state.owner,
            st.session_state.pet,
            task_objects
        )
    
    if st.button("Generate schedule", key="generate_schedule"):
        with st.spinner("Generating schedule..."):
            try:
                date_str = schedule_date.strftime('%Y-%m-%d')
                st.session_state.daily_plan = st.session_state.scheduler.generate_daily_plan(date_str)
                st.success("✅ Schedule generated successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error generating schedule: {str(e)}")

# Display plan if it exists with the requested format
if st.session_state.daily_plan:
    plan = st.session_state.daily_plan
    
    st.divider()
    st.subheader("📋 Your Daily Plan")
    
    # Generate formatted plan output
    plan_text = format_plan_output(plan)
    
    # Display in a styled container
    st.markdown(f"""
    <div class="plan-output">
    {plan_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Download button for the plan
    if st.button("📥 Download Plan as Text"):
        st.download_button(
            label="📄 Download",
            data=plan_text,
            file_name=f"pawpal_plan_{schedule_date.strftime('%Y-%m-%d')}.txt",
            mime="text/plain"
        )
    
    # Statistics section
    with st.expander("📊 View Statistics"):
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Scheduled Tasks", len(plan.get_scheduled_tasks()))
        with col2:
            st.metric("Excluded Tasks", len(plan.get_excluded_tasks()))
        with col3:
            st.metric("Time Used", f"{plan.get_total_planned_minutes()} min")
        with col4:
            remaining = plan.get_remaining_minutes()
            st.metric("Time Remaining", f"{remaining} min")
        
        # Category breakdown
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
            st.dataframe(df_cat, use_container_width=True)
            st.bar_chart(df_cat.set_index('Category')['Count'])
        
        # Priority distribution
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

# Footer
st.divider()
st.caption("🐾 PawPal+ - Your Pet Care Planning Assistant | Made with ❤️")

# Debug info
with st.expander("🔧 Debug Info"):
    st.json({
        "owner": str(st.session_state.owner) if st.session_state.owner else None,
        "pet": str(st.session_state.pet) if st.session_state.pet else None,
        "tasks_count": len(st.session_state.tasks),
        "scheduler": str(st.session_state.scheduler) if st.session_state.scheduler else None,
        "plan_exists": st.session_state.daily_plan is not None,
        "owner_saved": st.session_state.owner_saved,
        "pet_saved": st.session_state.pet_saved
    })
