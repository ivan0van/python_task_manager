import datetime
import os.path


class TaskConsts:
    """All constants for Tasks"""

    class Ranges:
        """Ranges of attributes values"""
        priority = [1, 2, 3]
        difficult = [1, 2, 3, 4, 5]

    class Default:
        """Default values of attributes"""
        id = None
        name = "*Your task name here*"
        minimal_date = datetime.date(1, 1, 1)
        date = datetime.date.today().strftime("%d.%m.%Y")
        tags = tuple()
        priority = 3
        difficult = 1
        date_format = "%d.%m.%Y"


class PathConsts:
    """All constants for path to files"""
    path_to_completed_dir = "data"
    completed_tasks_name = "CompletedTasks.json"
    path_to_following_dir = "data"
    following_tasks_name = "FollowingTasks.json"
    path_to_config_dir = "data"
    config_name = "Config.json"
    path_to_following = os.path.join(path_to_following_dir,
                                     following_tasks_name)
    path_to_completed = os.path.join(path_to_completed_dir,
                                     completed_tasks_name)
    path_to_config = os.path.join(path_to_config_dir, config_name)


class MessageConsts:
    """All constants for messages to user"""
    already_exist_text = "A task with the same already exists. If you still " \
                         "want to add a task click \"Add\" again"
    wrong_date_text = "Wrong date, change it"
    not_digits_fields_text = "The following fields must be filled with " \
                             "numbers: "
    empty_fields_text = "The following fields must not be empty: "
    wrong_range_fields_text = "the values of the following fields are not in " \
                              "the valid range: "


class GeneralLayoutConsts:
    """All constants for general layout of application"""

    class Keys:
        """All keys to events and values of general layout"""
        checkbox_task = "checkbox_task_"
        tag = "tag_"
        add_task = "add_task"
        ch_tags = "change_tags"
        clear_tags = "clear_tags"
        ch_type = "change_type_"
        ch_task = "change_task_"
        ch_following = "change_following"
        ch_completed = "change_completed"
        delete_task = "delete_task_"

    class Sizes:
        """All sizes of elements of general layout"""
        tag = (14, 1)
        task = (30, 1)
        state_column = (200, 100)
        tags_column = (200, 500)
        tasks_column = (1000, 600)
        difficult = (15, 1)

    colors_by_priority = ["#DF3838", "#DA8686", "#A7C1B4"]


class TaskLayoutConsts:
    """All constants for task layout of application"""

    class Keys:
        """All keys to events and values of task layout"""
        submit = "Submit"
        id = "id"
        name = "name"
        date = "date"
        tags = "tags"
        priority = "priority"
        difficult = "difficult"

    class Sizes:
        """All sizes of elements of task layout"""
        standard = (7, 1)
        task_name = (20, 1)
        tags = (20, 5)
        date = (10, 1)
