# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

# Daily plan for Mochi (Golden Retriever):
#   06:00 — Morning walk (15 min) [priority: high]
#     Reason: High-priority task scheduled to ensure completion; Scheduled in the morning to align with daily routine; Matches owner's preference for morning time
#
# ⏱️ Total planned: 15 min / 30 min available
# ⏱️ Remaining: 15 min
## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```
collected 36 items                                                                                                                          

test_models.py ....................................                                                                    

               [100%]

============================================================ 36 passed in 0.09s ============================================================
## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |  task is sorted by priority
| Filtering | | e.g., skip tasks if time runs out | it will skip tasks that are over the time limit 
| Conflict handling | | e.g., overlapping time slots | function is created in which it avoids overlapping time slots
| Recurring tasks | | e.g., daily vs. weekly | two functions are created to handle recurring tasks by weekly or daily 

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. You first enter your name 
2. You then enter your pet name and spieces
3. save user information 
4. Then you enter task related to the pet such as walking or feeding
5. You then added priority to the task based on the level of priority of the task
6. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
