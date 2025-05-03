from framework import task, runner


with runner():

    @task()
    def hello_world():
        print("Hello world")

    @task(required_by=hello_world)
    def first():
        print("This goes first")
