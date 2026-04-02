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
    
    def markComplete(self) -> None:
        """Mark the task as completed."""
        pass
    
    def updatePriority(self, priority: int) -> None:
        """Update the task priority."""
        pass
    
    def updateDuration(self, minutes: int) -> None:
        """Update the task duration."""
        pass
    
    def getTaskInfo(self) -> Dict:
        """Return task information as a dictionary."""
        pass


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
        pass
    
    def removeTask(self, taskId: str) -> None:
        """Remove a task by ID from the pet's task list."""
        pass
    
    def getTasks(self) -> List[Task]:
        """Return the list of tasks for this pet."""
        pass
    
    def updateInfo(self, species: str, age: int) -> None:
        """Update the pet's species and age information."""
        pass


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
        pass
    
    def removePet(self, petId: str) -> None:
        """Remove a pet by ID from the owner's pet list."""
        pass
    
    def updateAvailableTime(self, minutes: int) -> None:
        """Update the owner's available time in minutes."""
        pass
    
    def getPreferences(self) -> Dict:
        """Return the owner's preferences."""
        pass
    
    def getPets(self) -> List[Pet]:
        """Return the list of pets owned by this owner."""
        pass


class Scheduler:
    """Handles scheduling and task planning for pet care."""
    
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner
        self.tasks: List[Task] = []
    
    def generateDailyPlan(self) -> List[Task]:
        """Generate an optimal daily plan based on available time and task priorities."""
        pass
    
    def filterTasksByTime(self, tasks: List[Task], availableTime: int) -> List[Task]:
        """Filter tasks to include only those that fit within the available time."""
        pass
    
    def sortByPriority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority in descending order."""
        pass
    
    def selectOptimalTasks(self, tasks: List[Task], timeAvailable: int) -> List[Task]:
        """Select the optimal set of tasks that fit within available time and maximize priority."""
        pass
