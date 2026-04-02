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
    
    # Create Tasks with different durations
    task1 = Task(taskId="task001", name="Morning Walk", description="Take Buddy for a walk", duration=30, priority=5)
    task2 = Task(taskId="task002", name="Feed Pets", description="Feed both pets", duration=15, priority=4)
    task3 = Task(taskId="task003", name="Play Time", description="Play with Whiskers", duration=45, priority=3)
    
    # Add tasks to pets
    pet1.addTask(task1)
    pet1.addTask(task2)
    pet2.addTask(task3)
    
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

if __name__ == "__main__":
    main()
