import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# Initialize session state for Owner object
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", email="jordan@example.com")

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

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

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

if st.button("Update Owner Name"):
    st.session_state.owner.name = owner_name
    st.success(f"Owner name updated to {owner_name}")

pet_name = st.text_input("Pet name", value="Mochi")
pet_species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    # Generate unique pet ID
    pet_id = f"pet_{len(st.session_state.owner.getPets()) + 1}"
    new_pet = Pet(petId=pet_id, name=pet_name, species=pet_species, age=pet_age)
    st.session_state.owner.addPet(new_pet)
    st.success(f"Added pet {pet_name} ({pet_species})")

# Display current pets
if st.session_state.owner.getPets():
    st.markdown("### Current Pets")
    for pet in st.session_state.owner.getPets():
        with st.expander(f"{pet.name} ({pet.species}, {pet.age} years old)"):
            if pet.tasks:
                st.write("Tasks:")
                task_data = []
                for task in pet.tasks:
                    task_data.append({
                        "Name": task.name,
                        "Description": task.description,
                        "Duration": f"{task.duration} min",
                        "Priority": task.priority,
                        "Completed": "Yes" if task.isCompleted else "No"
                    })
                st.table(task_data)
            else:
                st.info("No tasks yet for this pet.")
else:
    st.info("No pets added yet.")

st.markdown("### Tasks")
st.caption("Add tasks to your pets. Tasks will be scheduled based on priority and time constraints.")

# Get list of pet names for selection
pet_options = [pet.name for pet in st.session_state.owner.getPets()]
if not pet_options:
    st.warning("Add a pet first before adding tasks.")
else:
    selected_pet_name = st.selectbox("Select pet for task", pet_options)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk")
        task_description = st.text_area("Task description", value="Take pet for a walk in the morning")
    with col2:
        task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        task_priority_options = {"low": 1, "medium": 3, "high": 5}
        priority_label = st.selectbox("Priority", list(task_priority_options.keys()), index=2)
        task_priority = task_priority_options[priority_label]

    if st.button("Add Task"):
        # Find the selected pet
        selected_pet = next(pet for pet in st.session_state.owner.getPets() if pet.name == selected_pet_name)
        
        # Generate unique task ID
        task_id = f"task_{len(selected_pet.tasks) + 1}"
        
        # Create task
        new_task = Task(
            taskId=task_id,
            name=task_name,
            description=task_description,
            duration=task_duration,
            priority=task_priority,
            petId=selected_pet.petId
        )
        
        # Add task to pet
        selected_pet.addTask(new_task)
        st.success(f"Added task '{task_name}' to {selected_pet_name}")
        st.rerun()  # Refresh to show updated tasks

st.divider()

st.subheader("Build Schedule")
st.caption("Use the scheduler to build a daily plan and show conflicts.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    plan_tasks = scheduler.generateDailyPlan()
    all_tasks = scheduler.gatherAllTasks()

    # Detect conflicts across all tasks
    conflict_messages = scheduler.detect_time_conflicts(all_tasks)
    if conflict_messages:
        for msg in conflict_messages:
            st.warning(msg)
    else:
        st.success("No scheduling conflicts detected.")

    if plan_tasks:
        st.success("Daily plan generated successfully.")
        plan_rows = []
        for task in scheduler.sort_by_time(plan_tasks):
            plan_rows.append({
                "Task": task.name,
                "Pet": next((p.name for p in st.session_state.owner.getPets() if p.petId == task.petId), "Unknown"),
                "Time": task.time,
                "Duration": f"{task.duration} min",
                "Priority": task.priority,
                "Completed": "Yes" if task.isCompleted else "No"
            })
        st.table(plan_rows)
    else:
        st.info("No tasks fit in the available time window (or no pending tasks exist).")

