from dataclasses import dataclass
from framework import runner, task, get_runner, shell


class Something:

    def __init__(self, message: str):
        self.message = message

        task(title=message, tags=[AptData(["ssh"])])(self.hehe)

    def do_something(self):
        print(self.message)

    def hehe(self):
        self.do_something()


@dataclass(frozen=True)
class AptData:
    packages: list[str]


with runner():

    something = Something("something!")
    something_else = Something("something else!")

    @task()
    def hello_world():
        shell("echo 'Hello world!'")

    @task(required_by=[hello_world, something.hehe])
    def first():
        print("This goes first")

    @task(requires=[hello_world], tags=[AptData(["vim"])])
    def last():
        print("Bye!")

    tasks_with_apt = [task for task in get_runner().tasks if task.get_tags(AptData)]
    packages_to_install = list(
        dict.fromkeys(
            [
                package
                for task in tasks_with_apt
                for tag in task.get_tags(AptData)
                for package in tag.packages
            ]
        )
    )

    @task(required_by=tasks_with_apt)
    def apt():
        print("Installing shiet with APT")
        for package in packages_to_install:
            print(package)
