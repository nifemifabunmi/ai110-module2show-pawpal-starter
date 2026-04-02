import pytest
from pawpal_system import Task, Pet

def test_task_completion():
    """Verify that calling markComplete() changes the task's status."""
    task = Task(taskId="test001", name="Test Task", description="A test task", duration=10, priority=3)
    
    # Initially, task should not be completed
    assert not task.isCompleted
    
    # Mark as complete
    task.markComplete()
    
    # Now it should be completed
    assert task.isCompleted

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(petId="pet001", name="Test Pet", species="Dog", age=2)
    
    # Initially, pet should have no tasks
    assert len(pet.tasks) == 0
    
    # Create and add a task
    task = Task(taskId="task001", name="Test Task", description="A test task", duration=10, priority=3)
    pet.addTask(task)
    
    # Now pet should have one task
    assert len(pet.tasks) == 1
    assert pet.tasks[0].taskId == "task001"
    assert pet.tasks[0].petId == "pet001"  # Verify petId is set


def test_sort_by_time_chronological_order():
    """Verify tasks are returned in chronological order by sort_by_time()."""
    from pawpal_system import Scheduler, Owner

    owner = Owner(name="Test Owner", email="owner@example.com")
    scheduler = Scheduler(owner=owner)

    task_a = Task(taskId="t1", name="Morning", description="", duration=10, priority=1, time="09:30")
    task_b = Task(taskId="t2", name="Noon", description="", duration=10, priority=1, time="12:00")
    task_c = Task(taskId="t3", name="Early", description="", duration=10, priority=1, time="07:15")

    tasks = [task_a, task_b, task_c]
    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [t.time for t in sorted_tasks] == ["07:15", "09:30", "12:00"]


def test_complete_task_creates_next_day_for_daily_recurring():
    """Confirm that completing a daily task creates a new task for the next day."""
    from pawpal_system import Scheduler, Owner, Pet
    from datetime import date, timedelta

    owner = Owner(name="Test Owner", email="owner@example.com")
    pet = Pet(petId="pet001", name="Fluffy", species="Cat", age=4)
    owner.addPet(pet)
    scheduler = Scheduler(owner=owner)

    today = date.today()
    daily_task = Task(taskId="d1", name="Feed", description="Feed pet", duration=15, priority=5, time="08:00", due_date=today, frequency="daily", petId="pet001")
    pet.addTask(daily_task)

    scheduler.complete_task(daily_task)

    # Original task should be completed
    assert daily_task.isCompleted

    # One new recurring task should now exist in pet tasks with tomorrow's date
    recurring_tasks = [t for t in pet.tasks if t.taskId != "d1"]
    assert len(recurring_tasks) == 1
    assert recurring_tasks[0].due_date == today + timedelta(days=1)
    assert recurring_tasks[0].frequency == "daily"


def test_detect_time_conflicts_reports_duplicate_times():
    """Verify scheduler flags duplicate times via detect_time_conflicts()."""
    from pawpal_system import Scheduler, Owner, Pet

    owner = Owner(name="Test Owner", email="owner@example.com")
    pet = Pet(petId="pet001", name="Buddy", species="Dog", age=3)
    owner.addPet(pet)
    scheduler = Scheduler(owner=owner)

    task1 = Task(taskId="c1", name="Walk", description="", duration=30, priority=3, time="17:00", petId="pet001")
    task2 = Task(taskId="c2", name="Vet", description="", duration=45, priority=4, time="17:00", petId="pet001")

    pet.addTask(task1)
    pet.addTask(task2)

    warnings = scheduler.detect_time_conflicts(pet.tasks)

    assert len(warnings) == 1
    assert "17:00" in warnings[0]
    assert "Walk" in warnings[0]
    assert "Vet" in warnings[0]

