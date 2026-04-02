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
