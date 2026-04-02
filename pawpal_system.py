from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Task:
    """Represents a pet care task."""
    taskId: str
    name: str
    description: str
    duration: int  # in minutes
    priority: int  # 1-5 scale
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
    
    def selectOptimalTasks(self, tasks: List[Task], timeAvailable: int) -> List[Task]:
        """Select the optimal set of tasks that fit within available time and maximize priority."""
        selected = []
        total_time = 0
        for task in tasks:
            if total_time + task.duration <= timeAvailable:
                selected.append(task)
                total_time += task.duration
        return selected
