from framework import runner, task, shell


with runner():

    class Something:

        def __init__(self, message: str):
            self.message = message

            task(tags={"message": message})(self.hehe)

        def do_something(self):
            print(self.message)

        def hehe(self):
            self.do_something()

    something = Something("something!")
    something_else = Something("something else!")

    @task()
    def hello_world():
        shell("echo 'Hello world!'")

    @task(required_by=[hello_world, something.hehe])
    def first():
        print("This goes first")

    @task(requires=[hello_world])
    def last():
        print("Bye!")
