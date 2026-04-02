# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design focused on four main classes: Owner, Pet, Task, and Scheduler. I chose these classes because they matched the main parts of the problem and made the system easier to organize. The Owner class was responsible for storing the user’s basic information, available time, preferences, and the pets they manage.
The Pet class stored information about each pet, such as its name, species, age, and assigned care tasks. The Task class represented individual care activities like feeding, walks, medication, grooming, or enrichment, and included attributes such as duration, priority, notes, and completion status. The Scheduler class was designed to handle the decision-making part of the app by selecting and organizing tasks into a daily plan. Overall, my initial design aimed to separate data storage from planning logic, which made the system more structured and easier to build incrementally.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed slightly as I thought more carefully about the scheduling requirement. At first, I mostly treated the app like a task tracker, where pets simply had a list of tasks. However, during planning I realized that the app also needed to behave more like a planner, not just a storage system. Because of that, I expanded the Scheduler class to include more responsibility for sorting and selecting tasks based on available time and priority. I also added attributes like duration, priority, and owner preferences because those details are necessary for generating a realistic daily plan. This change made the design more aligned with the actual goal of the project.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler is designed to consider a few main constraints:
  Time available — how many minutes the owner has in a day
  Task priority — which tasks are most important
  Owner preferences — optional preferences for how tasks should be handled
  Task duration — whether a task can realistically fit into the schedule
I decided these constraints mattered most because they directly affect whether a daily plan is actually useful. For example, even if a task is important, it may not fit if the owner has very limited time. Likewise, not all tasks are equally urgent, so priority helps the scheduler make better choices. Out of these, I considered time and priority to be the most important because they are the clearest and most practical constraints for this scenario.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is that it may leave out lower-priority tasks if there is not enough time to complete everything in a day. This tradeoff is reasonable because the app is meant to help a busy pet owner stay consistent with the most important parts of pet care first. In a real-world situation, it is better to make sure critical tasks like feeding, medication, or walks are completed than to force every possible task into the schedule and create an unrealistic plan. This makes the planner more practical rather than overly idealistic.

---

## 3. AI Collaboration

**a. How you used AI**, 

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI mainly for design brainstorming, UML planning, class structuring, and early code scaffolding. For example, I used AI to: 
  brainstorm what classes and relationships made sense for the system,
  generate a Mermaid.js UML diagram,
  create Python class skeletons using dataclasses, and 
  review whether my design was missing any important relationships or logic.
The most helpful prompts were the ones that were specific and structured, such as asking AI to:
  create a UML diagram for a pet care scheduling app,
  generate Python stubs based on the diagram, or
  review my file for possible missing logic or design bottlenecks.
Those kinds of prompts gave much better results than vague questions.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not accept an AI suggestion exactly as given was when the early design leaned too much toward being a basic pet tracker instead of a planning and scheduling system. I evaluated the suggestion by comparing it back to the project README and requirements. Since the app needed to generate a daily plan based on constraints and priorities, I realized the original version was too simple. I adjusted the design by making the Scheduler class more central and adding attributes like duration, priority, and time available. This helped me use AI as a starting point rather than treating its output as automatically correct.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The most important behaviors I would test in this project are whether tasks are sorted correctly by priority, whether tasks that exceed the owner’s available time are excluded, whether the scheduler can generate a daily plan from a list of tasks,and whether tasks can be added, removed, or updated correctly. These tests are important because they focus on the app’s core purpose: creating a realistic and useful schedule instead of just storing information.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am reasonably confident in the overall design of the scheduler because the logic is structured around clear rules like priority and available time. However, I would want more testing before being fully confident in all cases. If I had more time, I would test edge cases such as when there are no tasks, when all tasks exceed available time, when multiple tasks have the same priority, when a pet has a very large number of tasks, or when the owner has unusual or conflicting preferences. Testing those cases would make the scheduler more reliable and robust.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part of this project I am most satisfied with is the system design. I think I created a clean structure that separates the different responsibilities well, especially between the data-focused classes and the scheduling logic. I am also satisfied that the design is simple enough to implement, while still being flexible enough to support the app’s main features.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the scheduler by making it more intelligent and personalized. I would consider task categories with different urgency levels, preferred times of day,recurring tasks, and maybe even more advanced scheduling rules. I would also improve the explanation feature so the app could better justify why certain tasks were included or excluded from the daily plan.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned from this project is that good system design matters a lot before coding begins. Spending time thinking about classes, relationships, and responsibilities made the project feel much more manageable. I also learned that AI is most useful when used as a collaborative tool for brainstorming and refinement, not as something to copy without thinking. The best results came from combining AI suggestions with my own judgment and the actual project requirements.
