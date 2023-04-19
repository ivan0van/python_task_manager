from datetime import datetime, date

from Globals import MessageConsts, TaskConsts


class Task:
    """Task is basic class, which describe basic object - task.
    here and below task_attributes - dict of attributes.
    task attributes description (in braces type for task_attributes):
    id: int - id of task
    name: string - task name
    date: datetime.date, (string, that need to be correct date) -
    deadline of the task
    tags: set of strings (string of tags split by '\n') - tags assigned to
    the task
    priority: int (string that need to be int) - task priority. The less, the
     more important
    difficult: int (string that need to be int) - task difficult. The more,
    the more difficult
      """

    @staticmethod
    def check_task_attributes(task_attributes: dict) -> str:
        """Checks task attributes from user input for correctness and the
        ability to create a task from them. If it is incorrect attributes
        return error string, that describe which fields and why are incorrect"""

        def make_error_string(error: str, fields: list) -> str:
            """Creates an error message from error and fields in which it
            happened"""
            res = error + ", ".join(fields) + '\n'
            return res

        empty_fields = list()
        for [field, value] in task_attributes.items():
            if value == "":
                empty_fields.append(field)
        not_digit_fields = list()
        wrong_range_fields = list()
        digit_fields = ["priority", "difficult"]
        ranges = {"priority": TaskConsts.Ranges.priority,
                  "difficult": TaskConsts.Ranges.difficult}
        for field in digit_fields:
            if not str(task_attributes[field]).isdigit():
                not_digit_fields.append(field)
            else:
                if int(task_attributes[field]) not in ranges[field]:
                    wrong_range_fields.append(field)
        wrong_date = False
        try:
            datetime.strptime(task_attributes["date"], "%d.%m.%Y")
        except ValueError:
            wrong_date = True
        errors = ""
        if len(empty_fields) > 0:
            errors += make_error_string(MessageConsts.empty_fields_text,
                                        empty_fields)
        if len(not_digit_fields) > 0:
            errors += make_error_string(MessageConsts.not_digits_fields_text,
                                        not_digit_fields)
        if len(wrong_range_fields) > 0:
            errors += make_error_string(MessageConsts.wrong_range_fields_text,
                                        wrong_range_fields)
        if wrong_date:
            errors += MessageConsts.wrong_date_text
        return errors

    def __init__(self, task_attributes: dict):
        """Creates Task object from task_attributes"""
        self.__id = task_attributes["id"]
        self.__name = task_attributes["name"]
        self.__date = datetime.strptime(task_attributes["date"], "%d.%m.%Y")
        tags = filter(lambda tag: tag != "", task_attributes["tags"])
        self.__tags = set(tags)
        self.__priority = int(task_attributes["priority"])
        self.__difficult = int(task_attributes["difficult"])

    @property
    def date(self) -> date:
        return self.__date

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def tags(self) -> set:
        return self.__tags

    @property
    def priority(self) -> int:
        return self.__priority

    @property
    def difficult(self) -> int:
        return self.__difficult

    @property
    def date_str(self) -> str:
        """Returns string format date"""
        return self.__date.strftime(TaskConsts.Default.date_format)

    def get_attributes(self) -> dict:
        """Returns task_attributes"""
        task_attributes = dict()
        task_attributes["id"] = self.__id
        task_attributes["name"] = self.__name
        task_attributes["date"] = self.date_str
        task_attributes["tags"] = tuple(self.__tags)
        task_attributes["priority"] = self.__priority
        task_attributes["difficult"] = self.__difficult
        return task_attributes
