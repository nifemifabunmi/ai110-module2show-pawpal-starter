from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date, timedelta


@dataclass
class Task:
    """Represents a pet care task."""
    taskId: str
    name: str
    description: str
    duration: int  # in minutes
    priority: int  # 1-5 scale
    time: str = ""  # Scheduled time in "HH:MM" format
    due_date: date = field(default_factory=date.today)  # Due date
    frequency: str = "once"  # "once", "daily", "weekly"
    notes: str = ""
    isCompleted: bool = False
    petId: str = ""  # Reference to the pet this task belongs to
    
    def markComplete(self) -> None:
        """Mark the task as completed."""
        self.isCompleted = True
    
    def updatePriority(self, priority: int) -> None:
        """Update the task priority."""
        self.priority = priority
    
    def updateDuration(self, minutes: int) -> None:
        """Update the task duration."""
        self.duration = minutes
    
    def getTaskInfo(self) -> Dict:
        """Return task information as a dictionary."""
        return {
            "taskId": self.taskId,
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
            "priority": self.priority,
            "time": self.time,
            "due_date": self.due_date.isoformat(),
            "frequency": self.frequency,
            "notes": self.notes,
            "isCompleted": self.isCompleted,
            "petId": self.petId
        }


@dataclass
class Pet:
    """Represents a pet."""
    petId: str
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    
    def addTask(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        task.petId = self.petId  # Set the pet reference
        self.tasks.append(task)
    
    def removeTask(self, taskId: str) -> None:
        """Remove a task by ID from the pet's task list."""
        self.tasks = [t for t in self.tasks if t.taskId != taskId]
    
    def getTasks(self) -> List[Task]:
        """Return the list of tasks for this pet."""
        return self.tasks
    
    def updateInfo(self, species: str, age: int) -> None:
        """Update the pet's species and age information."""
        self.species = species
        self.age = age


class Owner:
    """Represents a pet owner."""
    
    def __init__(self, name: str, email: str, availableTime: int = 0):
        """Initialize an owner with name, email, and available time."""
        self.name = name
        self.email = email
        self.availableTime = availableTime
        self.preferences: Dict = {}
        self.pets: List[Pet] = []
    
    def addPet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)
    
    def removePet(self, petId: str) -> None:
        """Remove a pet by ID from the owner's pet list."""
        self.pets = [p for p in self.pets if p.petId != petId]
    
    def updateAvailableTime(self, minutes: int) -> None:
        """Update the owner's available time in minutes."""
        self.availableTime = minutes
    
    def getPreferences(self) -> Dict:
        """Return the owner's preferences."""
        return self.preferences
    
    def getPets(self) -> List[Pet]:
        """Return the list of pets owned by this owner."""
        return self.pets


class Scheduler:
    """Handles scheduling and task planning for pet care."""
    
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner
        self.tasks: List[Task] = []
    
    def gatherAllTasks(self) -> List[Task]:
        """Gather all tasks from all pets owned by the owner."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks
    
    def generateDailyPlan(self) -> List[Task]:
        """Generate an optimal daily plan based on available time and task priorities."""
        all_tasks = self.gatherAllTasks()
        # Filter out completed tasks
        pending_tasks = [t for t in all_tasks if not t.isCompleted]
        # Sort by priority
        sorted_tasks = self.sortByPriority(pending_tasks)
        # Select optimal tasks within time
        return self.selectOptimalTasks(sorted_tasks, self.owner.availableTime)
    
    def filterTasksByTime(self, tasks: List[Task], availableTime: int) -> List[Task]:
        """Filter tasks to include only those that fit within the available time."""
        filtered = []
        total_time = 0
        for task in tasks:
            if total_time + task.duration <= availableTime:
                filtered.append(task)
                total_time += task.duration
        return filtered
    
    def sortByPriority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority in descending order."""
        return sorted(tasks, key=lambda t: t.priority, reverse=True)
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled time in ascending order.
        
        Converts the time string in "HH:MM" format to total minutes for accurate sorting.
        
        Args:
            tasks: List of Task objects to sort.
            
        Returns:
            A new list of tasks sorted by time.
            
        Example:
            >>> tasks = [Task(time="10:00"), Task(time="08:00")]
            >>> sorted_tasks = scheduler.sort_by_time(tasks)
            >>> [t.time for t in sorted_tasks]
            ['08:00', '10:00']
        """
        return sorted(tasks, key=lambda t: int(t.time.split(':')[0]) * 60 + int(t.time.split(':')[1]))
    
    def filter_tasks(self, tasks: List[Task], is_completed: bool = None, pet_name: str = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.
        
        Args:
            tasks: List of Task objects to filter.
            is_completed: If True, return only completed tasks; if False, only pending; if None, ignore status.
            pet_name: Name of the pet to filter tasks for; if None, ignore pet.
            
        Returns:
            A filtered list of tasks matching the criteria.
            
        Example:
            >>> pending_tasks = scheduler.filter_tasks(all_tasks, is_completed=False)
            >>> buddy_tasks = scheduler.filter_tasks(all_tasks, pet_name="Buddy")
        """
        filtered = tasks
        if is_completed is not None:
            filtered = [t for t in filtered if t.isCompleted == is_completed]
        if pet_name is not None:
            # Find pet ID by name
            pet_id = None
            for pet in self.owner.pets:
                if pet.name == pet_name:
                    pet_id = pet.petId
                    break
            if pet_id is not None:
                filtered = [t for t in filtered if t.petId == pet_id]
        return filtered
    
    def complete_task(self, task: Task) -> None:
        """Mark a task as completed and create a new recurring task if applicable.
        
        For recurring tasks ("daily" or "weekly"), automatically creates a new task instance
        with an updated due date using datetime.timedelta.
        
        Args:
            task: The Task object to mark as completed.
            
        Example:
            >>> daily_task = Task(frequency="daily", due_date=date.today())
            >>> scheduler.complete_task(daily_task)
            # Creates a new task for tomorrow
        """
        task.markComplete()
        if task.frequency == "daily":
            new_due_date = task.due_date + timedelta(days=1)
        elif task.frequency == "weekly":
            new_due_date = task.due_date + timedelta(weeks=1)
        else:
            return  # No recurrence
        
        # Create a new task instance
        new_task = Task(
            taskId=f"{task.taskId}_recurring_{new_due_date.isoformat()}",
            name=task.name,
            description=task.description,
            duration=task.duration,
            priority=task.priority,
            time=task.time,
            due_date=new_due_date,
            frequency=task.frequency,
            notes=task.notes,
            petId=task.petId
        )
        
        # Add to the appropriate pet
        for pet in self.owner.pets:
            if pet.petId == task.petId:
                pet.addTask(new_task)
                break
    
    def detect_time_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect tasks scheduled at the same time and return warning messages.
        
        Groups tasks by their time attribute and identifies any time slots with multiple tasks.
        Returns human-readable warning messages for conflicts, without raising exceptions.
        
        Args:
            tasks: List of Task objects to check for conflicts.
            
        Returns:
            List of warning strings describing conflicts, empty if no conflicts.
            
        Example:
            >>> conflicts = scheduler.detect_time_conflicts(all_tasks)
            >>> for warning in conflicts:
            ...     print(warning)
            Warning: Multiple tasks scheduled at 12:00: Feed Pets, Vet Check for pets Buddy, Buddy
        """
        warnings = []
        time_groups = {}
        for task in tasks:
            if task.time not in time_groups:
                time_groups[task.time] = []
            time_groups[task.time].append(task)
        
        for time, task_list in time_groups.items():
            if len(task_list) > 1:
                pet_names = [next((p.name for p in self.owner.pets if p.petId == t.petId), "Unknown Pet") for t in task_list]
                task_names = [t.name for t in task_list]
                warnings.append(f"Warning: Multiple tasks scheduled at {time}: {', '.join(task_names)} for pets {', '.join(pet_names)}")
        return warnings
    
    def selectOptimalTasks(self, tasks: List[Task], timeAvailable: int) -> List[Task]:
        """Select the optimal set of tasks that fit within available time and maximize priority."""
        selected = []
        total_time = 0
        for task in tasks:
            if total_time + task.duration <= timeAvailable:
                selected.append(task)
                total_time += task.duration
        return selected
