from dataclasses import dataclass, field
from functools import lru_cache

from todoist_api_python.api_async import TodoistAPIAsync


@dataclass
class TodoistClient:
    """Class to represent a Todoist client"""
    api_key: str
    project: str
    api: TodoistAPIAsync = field(init=False)

    def __post_init__(self):
        self.api = TodoistAPIAsync(self.api_key)

    async def find_project_id(self):
        """Find the project ID for the given project name"""
        projects = await self.api.get_projects()
        for project in projects:
            if project.name == self.project:
                return project.id
        raise ValueError(f"Project '{self.project}' not found.")

    async def add_task(self, task_title: str, task_details: str = None):
        """Add a task to Todoist"""
        project_id = await self.find_project_id()
        task = await self.api.add_task(
            task_title,
            description=task_details,
        project_id=project_id,)
        return task
