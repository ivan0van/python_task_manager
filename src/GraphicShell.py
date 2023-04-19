import PySimpleGUI as Sg

from Globals import MessageConsts, GeneralLayoutConsts, TaskLayoutConsts
from Layout import Layout
from Task import Task
from TaskManager import TaskManager


class GraphicShell:
    """Graphic shell for TaskManager engine
    manager: TaskManager - engine of application"""

    def __init__(self):
        self.__manager = TaskManager()
        Sg.theme("GreenMono")

    @property
    def _is_completed_(self):
        """Returns True if state of current section is completed otherwise
        False"""
        return self.__manager.is_completed

    @staticmethod
    def get_id(key: str, event: str):
        """Return task or tag id by key of event and event"""
        id_start = len(key)
        return int(event[id_start:])

    def task_window(self, title: str, layout: list,
                    task_id: int | None) -> bool:
        """Draws the window of tasks edition and handling user input
        title - title of window (can only be "Add task" or "Change task")
        layout - layout of task edition, depends on type of edition (adding
        or changing),
        task_id - id of edition task, int for changing, None for adding
        Returns True if edition completed successfully otherwise False"""
        window = Sg.Window(title, layout)
        in_any_case = False
        is_ok = False
        while True:
            event, values = window.read()
            if event in (None, "Exit", "Cancel"):
                break
            if event == TaskLayoutConsts.Keys.submit:
                task_attributes = dict()
                task_attributes["id"] = task_id
                task_attributes["name"] = values["name"]
                task_attributes["date"] = values["date"]
                task_attributes["tags"] = list(values["tags"].split('\n'))
                task_attributes["priority"] = values["priority"]
                task_attributes["difficult"] = values["difficult"]
                message = Task.check_task_attributes(task_attributes)
                if message != "":
                    window["message"].update(message)
                    continue
                done = self.__manager.add_task(task_attributes,
                                               is_completed=self._is_completed_,
                                               in_any_case=in_any_case)
                if not done:
                    window["message"].update(MessageConsts.already_exist_text)
                    in_any_case = True
                else:
                    is_ok = True
                    break
        window.close()
        return is_ok

    def add_task(self):
        """Draws add task window and handling user input"""
        layout = Layout.get_add_task_layout()
        self.task_window("Add task", layout, None)

    def delete_task(self, event: str):
        """Deletes task by event of deletion"""
        task_id = self.get_id(GeneralLayoutConsts.Keys.delete_task, event)
        self.__manager.delete_task_by_id(task_id)

    def change_task(self, event: str):
        """Draws change task window and handling user input"""
        task_id = self.get_id(GeneralLayoutConsts.Keys.ch_task, event)
        task = self.__manager.get_task_by_id(task_id)
        self.__manager.delete_task_by_id(task_id)
        layout = Layout.get_change_task_layout(task)
        is_ok = self.task_window("Change task", layout, task_id)
        if not is_ok:
            self.__manager.add_task(task.get_attributes(),
                                    is_completed=self._is_completed_,
                                    in_any_case=True)

    def get_general_window(self) -> Sg.Window:
        """Returns general window by current section"""
        tasks = self.__manager.get_tasks()
        tags = self.__manager.tags
        picked_tags = self.__manager.get_section_tags()
        layout = Layout.get_general_layout(tasks, tags, picked_tags,
                                           self._is_completed_)
        window = Sg.Window("Task manager", layout)
        return window

    def update_task(self, event: str):
        """Checks or unchecks task by event depends on current section state"""
        task_id = self.get_id(GeneralLayoutConsts.Keys.checkbox_task, event)
        if self._is_completed_:
            self.__manager.uncheck(task_id)
        else:
            self.__manager.check(task_id)

    def change_tags(self, values: dict):
        """Changes current section tags by new chosen tag"""
        tag_key = GeneralLayoutConsts.Keys.tag
        tag_start = len(tag_key)
        chosen_tags_items = filter(lambda item: tag_key in item[0] and item[1],
                                   values.items())
        chosen_tags = list(map(lambda item: item[0][tag_start:],
                               chosen_tags_items))
        self.__manager.change_section_tags(chosen_tags, self._is_completed_)

    def change_type(self, event):
        """Change current section type to opposite"""
        type_start = len(GeneralLayoutConsts.Keys.ch_type)
        is_completed = event[type_start:] == "completed"
        tags = self.__manager.get_section_tags()
        self.__manager.change_section_tags(tags, is_completed)

    def clear_tags(self):
        """Uncheck all chosen tags"""
        self.__manager.change_section_tags([], self._is_completed_)

    def general(self):
        """handles user requests to the general window"""
        window = self.get_general_window()
        while True:
            event, values = window.read()
            if event in (None, "Exit", "Cancel"):
                break
            elif GeneralLayoutConsts.Keys.checkbox_task in event:
                self.update_task(event)
            elif event == GeneralLayoutConsts.Keys.add_task:
                self.add_task()
            elif GeneralLayoutConsts.Keys.ch_tags in event:
                self.change_tags(values)
            elif GeneralLayoutConsts.Keys.ch_type in event:
                self.change_type(event)
            elif GeneralLayoutConsts.Keys.ch_task in event:
                self.change_task(event)
            elif GeneralLayoutConsts.Keys.delete_task in event:
                self.delete_task(event)
            elif GeneralLayoutConsts.Keys.clear_tags in event:
                self.clear_tags()
            window.close()
            window = self.get_general_window()
        window.close()
