from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # Create an Owner
    owner = Owner(name="Alice Johnson", email="alice@example.com", availableTime=120)  # 120 minutes available
    
    # Create two Pets
    pet1 = Pet(petId="pet001", name="Buddy", species="Dog", age=3)
    pet2 = Pet(petId="pet002", name="Whiskers", species="Cat", age=2)
    
    # Add pets to owner
    owner.addPet(pet1)
    owner.addPet(pet2)
    
    # Create Tasks with different durations and times (out of order)
    task1 = Task(taskId="task001", name="Morning Walk", description="Take Buddy for a walk", duration=30, priority=5, time="08:00", frequency="daily")
    task2 = Task(taskId="task002", name="Feed Pets", description="Feed both pets", duration=15, priority=4, time="12:00", frequency="daily")
    task3 = Task(taskId="task003", name="Play Time", description="Play with Whiskers", duration=45, priority=3, time="10:00", frequency="weekly")
    task4 = Task(taskId="task004", name="Evening Walk", description="Take Buddy for evening walk", duration=30, priority=4, time="18:00")
    task5 = Task(taskId="task005", name="Grooming", description="Groom Whiskers", duration=20, priority=2, time="14:00")
    task6 = Task(taskId="task006", name="Vet Check", description="Check Buddy's health", duration=60, priority=5, time="12:00")  # Same time as task2
    
    # Mark some tasks as completed
    task1.markComplete()
    task5.markComplete()
    
    # Add tasks to pets
    pet1.addTask(task1)
    pet1.addTask(task2)
    pet1.addTask(task4)
    pet1.addTask(task6)
    pet2.addTask(task3)
    pet2.addTask(task5)
    
    # Create Scheduler
    scheduler = Scheduler(owner)
    
    # Generate daily plan
    daily_plan = scheduler.generateDailyPlan()
    
    # Print Today's Schedule
    print("Today's Schedule:")
    if not daily_plan:
        print("No tasks scheduled.")
    else:
        for task in daily_plan:
            # Find pet name by petId
            pet_name = next((p.name for p in owner.getPets() if p.petId == task.petId), "Unknown Pet")
            print(f"- {task.name} for {pet_name} ({task.duration} minutes, Priority: {task.priority})")
    
    # Demonstrate sorting and filtering
    print("\nAll Tasks (unsorted):")
    all_tasks = scheduler.gatherAllTasks()
    for task in all_tasks:
        pet_name = next((p.name for p in owner.getPets() if p.petId == task.petId), "Unknown Pet")
        status = "Completed" if task.isCompleted else "Pending"
        print(f"- {task.name} for {pet_name} at {task.time} ({status})")
    
    # Check for time conflicts
    conflicts = scheduler.detect_time_conflicts(all_tasks)
    if conflicts:
        print("\nTime Conflicts Detected:")
        for warning in conflicts:
            print(warning)
    
    print("\nTasks Sorted by Time:")
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    for task in sorted_tasks:
        pet_name = next((p.name for p in owner.getPets() if p.petId == task.petId), "Unknown Pet")
        status = "Completed" if task.isCompleted else "Pending"
        print(f"- {task.name} for {pet_name} at {task.time} ({status})")
    
    print("\nPending Tasks (filtered by completion status):")
    pending_tasks = scheduler.filter_tasks(all_tasks, is_completed=False)
    for task in pending_tasks:
        pet_name = next((p.name for p in owner.getPets() if p.petId == task.petId), "Unknown Pet")
        print(f"- {task.name} for {pet_name} at {task.time}")
    
    print("\nTasks for Buddy (filtered by pet name):")
    buddy_tasks = scheduler.filter_tasks(all_tasks, pet_name="Buddy")
    for task in buddy_tasks:
        status = "Completed" if task.isCompleted else "Pending"
        print(f"- {task.name} at {task.time} ({status})")
    
    # Demonstrate completing a recurring task
    print("\nCompleting a daily task (Morning Walk)...")
    morning_walk = next((t for t in all_tasks if t.name == "Morning Walk"), None)
    if morning_walk:
        scheduler.complete_task(morning_walk)
        print("Task completed. New recurring task created.")
    
    print("\nAll Tasks after completing Morning Walk:")
    all_tasks_after = scheduler.gatherAllTasks()
    for task in all_tasks_after:
        pet_name = next((p.name for p in owner.getPets() if p.petId == task.petId), "Unknown Pet")
        status = "Completed" if task.isCompleted else "Pending"
        freq = f" ({task.frequency})" if task.frequency != "once" else ""
        print(f"- {task.name} for {pet_name} at {task.time} on {task.due_date}{freq} ({status})")

if __name__ == "__main__":
    main()
