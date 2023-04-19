import PySimpleGUI as Sg

from Globals import GeneralLayoutConsts, TaskLayoutConsts, TaskConsts
from Task import Task


class Layout:
    """Wrapper for all layouts functions"""
    @staticmethod
    def _get_task_layout_(task: Task, edition_type: str) -> list:
        """Returns task edition layout by task and type of edition (adding or
        changing)"""
        name = [Sg.Text("Name: ",
                        size=TaskLayoutConsts.Sizes.standard),
                Sg.InputText(key=TaskLayoutConsts.Keys.name,
                             default_text=task.name,
                             size=TaskLayoutConsts.Sizes.task_name)]
        date = [Sg.Text("Date: ",
                        size=TaskLayoutConsts.Sizes.standard),
                Sg.InputText(key=TaskLayoutConsts.Keys.date,
                             default_text=task.date_str,
                             size=TaskLayoutConsts.Sizes.date),
                Sg.CalendarButton("Select Date", close_when_date_chosen=True,
                                  target=TaskLayoutConsts.Keys.date,
                                  format="%d.%m.%Y")]
        tags_header = [Sg.Text("Tags:",
                               size=TaskLayoutConsts.Sizes.standard)]
        tags_string = "\n".join(task.tags)
        tags = [Sg.Multiline(key=TaskLayoutConsts.Keys.tags,
                             default_text=tags_string,
                             size=TaskLayoutConsts.Sizes.tags)]
        priority = [Sg.Text("Priority: ", size=TaskLayoutConsts.Sizes.standard),
                    Sg.Combo(TaskConsts.Ranges.priority,
                             key=TaskLayoutConsts.Keys.priority,
                             default_value=task.priority)]
        difficult = [Sg.Text("Difficult: ",
                             size=TaskLayoutConsts.Sizes.standard),
                     Sg.Combo(TaskConsts.Ranges.difficult,
                              key=TaskLayoutConsts.Keys.difficult,
                              default_value=task.difficult)]
        submit = [Sg.Submit(button_text=edition_type,
                            key=TaskLayoutConsts.Keys.submit)]
        message = [Sg.Text("", key="message")]
        task_layout = [name, date, tags_header, tags, priority, difficult,
                       submit, message]
        return task_layout

    @staticmethod
    def get_add_task_layout() -> list:
        """Returns task adding layout"""
        task_attributes = {"id": TaskConsts.Default.id,
                           "name": TaskConsts.Default.name,
                           "date": TaskConsts.Default.date,
                           "tags": TaskConsts.Default.tags,
                           "priority": TaskConsts.Default.priority,
                           "difficult": TaskConsts.Default.difficult}
        task = Task(task_attributes)
        edition_type = "Add"
        return Layout._get_task_layout_(task, edition_type)

    @staticmethod
    def get_change_task_layout(task: Task) -> list:
        """Returns tasks changing layout by task"""
        edition_type = "Change"
        return Layout._get_task_layout_(task, edition_type)

    @staticmethod
    def _get_states_frame_(is_completed: bool) -> Sg.Frame:
        """Returns frame with available states and already chosen state/
        is_completed == True is current section state is completed otherwise
        False"""
        states_layout = [[Sg.Radio("Following", "State",
                                   default=not is_completed,
                                   size=GeneralLayoutConsts.Sizes.tag,
                                   key=f"{GeneralLayoutConsts.Keys.ch_type}"
                                       f"following",
                                   enable_events=is_completed)],
                         [Sg.Radio("Completed", "State", default=is_completed,
                                   size=GeneralLayoutConsts.Sizes.tag,
                                   key=f"{GeneralLayoutConsts.Keys.ch_type}"
                                       f"completed",
                                   enable_events=not is_completed)]]
        states_column = Sg.Column(states_layout,
                                  size=GeneralLayoutConsts.Sizes.state_column,
                                  justification="left")
        states_frame = Sg.Frame("States", [[states_column]],
                                element_justification='l')
        return states_frame

    @staticmethod
    def _get_tags_frame_(tags: list, picked_tags: list) -> Sg.Frame:
        """Returns frame with available tags and already chosen tags.
        tags - list of all tags
        picked_tags - list of tags of current section"""
        tags_layout = []
        for tag in tags:
            is_picked = tag in picked_tags
            check_box = Sg.Checkbox(text=tag, default=is_picked,
                                    key=f"{GeneralLayoutConsts.Keys.tag}{tag}",
                                    size=GeneralLayoutConsts.Sizes.tag)
            tags_layout.append([check_box])
        tags_column = Sg.Column(tags_layout, scrollable=True,
                                size=GeneralLayoutConsts.Sizes.tags_column,
                                justification='left')
        change_tags_button = Sg.Button(button_text="Change tags",
                                       key=GeneralLayoutConsts.Keys.ch_tags)
        clear_tags_button = Sg.Button(button_text="Clear tags",
                                      key=GeneralLayoutConsts.Keys.clear_tags)
        tags_frame = Sg.Frame("Tags", [[tags_column], [change_tags_button],
                                       [clear_tags_button]],
                              element_justification='l')
        return tags_frame

    @staticmethod
    def _get_section_frame_(tags: list, picked_tags: list,
                            is_completed: bool) -> Sg.Frame:
        """Returns current section and section update frame by all tags, picked
        tags of current section and current state"""
        states_frame = Layout._get_states_frame_(is_completed)
        tags_frame = Layout._get_tags_frame_(tags, picked_tags)
        section_frame = Sg.Frame("Section", [[states_frame], [tags_frame]],
                                 element_justification="l")
        return section_frame

    @staticmethod
    def _get_tasks_frame_(tasks: list, is_completed: bool) -> Sg.Frame:
        """Return frame with all tasks of current section
        tasks - list of all tasks of current section
        is_completed == True is current section state is completed otherwise
        False"""
        cur_date = TaskConsts.Default.minimal_date
        tasks_layout = []
        for task in tasks:
            if task.date != cur_date:
                date = Sg.Text(task.date_str)
                tasks_layout.append([date])
                cur_date = task.date
            color = GeneralLayoutConsts.colors_by_priority[task.priority - 1]
            checkbox_key = f"{GeneralLayoutConsts.Keys.checkbox_task}"\
                           f"{task.id}"
            checkbox = Sg.Checkbox(text=task.name, default=is_completed,
                                   key=checkbox_key,
                                   background_color=color,
                                   enable_events=True,
                                   size=GeneralLayoutConsts.Sizes.task)
            difficult = Sg.Text(f"Difficult: {task.difficult}",
                                background_color=color,
                                size=GeneralLayoutConsts.Sizes.difficult)
            change = Sg.Button(button_text="Change",
                               key=f"{GeneralLayoutConsts.Keys.ch_task}"
                                   f"{task.id}")
            delete = Sg.Button(button_text="Delete",
                               key=f"{GeneralLayoutConsts.Keys.delete_task}"
                                   f"{task.id}")
            tasks_layout.append([checkbox, difficult, change, delete])
        task_column = Sg.Column(tasks_layout, scrollable=True,
                                size=GeneralLayoutConsts.Sizes.tasks_column,
                                justification='left')
        add_task_button = Sg.Button(button_text="Add task",
                                    key=GeneralLayoutConsts.Keys.add_task)
        tasks_frame = Sg.Frame("Tasks", [[task_column], [add_task_button]])
        return tasks_frame

    @staticmethod
    def get_general_layout(tasks: list, tags: list, picked_tags: list,
                           is_completed: bool) -> list:
        """Returns general layout with current section and opportunity to change
        it and all tasks of current sections"""
        section_frame = Layout._get_section_frame_(tags, picked_tags,
                                                   is_completed)
        tasks_frame = Layout._get_tasks_frame_(tasks, is_completed)
        general_layout = [[section_frame, tasks_frame]]
        return general_layout
