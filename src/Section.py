import json

from Globals import PathConsts
from Task import Task


class Section:
    """Section is a wrapper for all tasks with common tags and state
    (following/completed).
    path: string - path to file with tasks with this state,
    is_completed: bool - is this completed tasks,
    tags: set - tags of tasks,
    """

    def __init__(self, tags=None, is_completed=False):
        """Creates Section object from list of tags and state"""
        if tags is None:
            tags = list()
        if is_completed:
            self.__path = PathConsts.path_to_completed
        else:
            self.__path = PathConsts.path_to_following
        self.__is_completed = is_completed
        self.__tags = set(tags)

    def _rewrite_tasks_(self, tasks: list):
        """Rewrites tasks to file"""
        tasks_attributes = tuple(map(lambda task: task.get_attributes(), tasks))
        with open(self.__path, 'w', encoding="UTF-8") as file:
            file.write(json.dumps(tasks_attributes))

    def add_task(self, task: Task) -> None:
        """Adds task to this section, can be used only by
        __following_section and __completed_section attributes of TaskManager"""
        tasks = self.get_tasks()
        tasks.append(task)
        self._rewrite_tasks_(tasks)

    def delete_task_by_id(self, task_id: int):
        """Delete task from file by id, can be used only by
        __following_section and __completed_section attributes of TaskManager"""
        tasks_with_current = self.get_tasks()
        tasks = list(filter(lambda current_task: current_task.id != task_id,
                            tasks_with_current))
        self._rewrite_tasks_(tasks)

    def get_tasks(self) -> list:
        """Returns sorted by date, priority and difficult attributes list of
        all tasks from this section"""
        with open(self.__path, 'r', encoding="UTF-8") as file:
            json_tasks_attributes = file.read()
        tasks_attributes = []
        if len(json_tasks_attributes) != 0:
            tasks_attributes = json.loads(json_tasks_attributes)
        all_tasks = list(map(lambda task_attribute: Task(task_attribute),
                             tasks_attributes))
        tasks = list(filter(lambda task: self.__tags.issubset(task.tags),
                            all_tasks))
        tasks.sort(key=lambda task: (task.date, task.priority, -task.difficult))
        return tasks

    def find_task_by_name(self, task_name: str) -> bool:
        """Searches for a task with the same name among all tasks with the
        same state. Returns True if found otherwise False, can be used only by
        __following_section and __completed_section attributes of TaskManager"""
        tasks = self.get_tasks()
        result = False
        for task in tasks:
            if task.name == task_name:
                result = True
        return result

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Returns task by id if this task exist otherwise None"""
        tasks = self.get_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    @property
    def is_completed(self) -> bool:
        return self.__is_completed

    @property
    def tags(self) -> set:
        return self.__tags
