import json

from Globals import PathConsts
from Section import Section
from Task import Task


class TaskManager:
    """Engine of application, the main interface for interacting with tasks
    following_section: Section - section with all following tasks,
    completed_section: Section - section with all completed tasks,
    current_section: Section - current section, that chosen by user,
    tags: set - all tags used at least once,
    max_id: int - max current id of all tasks"""

    def __init__(self):
        self.__following_section = Section()
        self.__completed_section = Section(is_completed=True)
        self.__current_section = self.__following_section
        self.__tags = set()
        with open(PathConsts.path_to_config, 'r') as config:
            config_json = config.read()
            config = json.loads(config_json)
        self.__max_id = int(config["max_id"])

    def check(self, task_id: int):
        """Marks the task by id as completed,
        used only by section with following state"""
        task = self.__following_section.get_task_by_id(task_id)
        self.__following_section.delete_task_by_id(task_id)
        self.__completed_section.add_task(task)

    def uncheck(self, task_id: int):
        """Unmarks the task by id, makes it following,
        used only by section with completed state"""
        task = self.__completed_section.get_task_by_id(task_id)
        self.__completed_section.delete_task_by_id(task_id)
        self.__following_section.add_task(task)

    def add_task(self, task_attributes, is_completed=True, in_any_case=False):
        """Add task by task_attributes to completed or following section,
        depends on value of is_completed
         If is_any_case is False doesn't add task if task with this name
         already exist otherwise add in any case"""
        new_task = False
        if task_attributes["id"] is None:
            task_attributes["id"] = self.__max_id + 1
            new_task = True
        task = Task(task_attributes)
        if is_completed:
            already_exists = \
                self.__completed_section.find_task_by_name(task.name)
        else:
            already_exists = \
                self.__following_section.find_task_by_name(task.name)
        if already_exists and not in_any_case:
            return False
        if is_completed:
            self.__completed_section.add_task(task)
        else:
            self.__following_section.add_task(task)
        if new_task:
            self.__max_id += 1
        self.update_config()
        return True

    def get_tasks(self) -> list:
        """Returns all tasks from this section"""
        return self.__current_section.get_tasks()

    def get_task_by_id(self, task_id: int) -> Task:
        """Returns task from this section by id"""
        return self.__current_section.get_task_by_id(task_id)

    def change_section_tags(self, tags: list, is_completed: bool):
        """Changes current section to section with needed tags and needed
        state depends on tags and is_completed value"""
        self.__current_section = Section(tags, is_completed=is_completed)

    def delete_task_by_id(self, task_id):
        """Deletes task by id"""
        if self.is_completed:
            self.__completed_section.delete_task_by_id(task_id)
        else:
            self.__following_section.delete_task_by_id(task_id)

    def update_config(self):
        """Update info about max_id in config file"""
        new_config = dict()
        new_config["max_id"] = self.__max_id
        with open(PathConsts.path_to_config, 'w', encoding="UTF-8") as config:
            config.write(json.dumps(new_config))

    @property
    def tags(self) -> list:
        """Returns all tags used at least once"""
        self.__tags = set()
        for task in self.__following_section.get_tasks():
            self.__tags |= task.tags
        for task in self.__completed_section.get_tasks():
            self.__tags |= task.tags
        return list(self.__tags)

    def get_section_tags(self) -> list:
        """Returns all tags of current_section"""
        return list(self.__current_section.tags)

    @property
    def is_completed(self) -> bool:
        """Returns True if state of current section is completed otherwise
        False"""
        return self.__current_section.is_completed
