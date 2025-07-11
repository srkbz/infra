from framework.models import Task


def planner(tasks: list[Task]):
    result: list[Task] = []
    dependencies: dict[Task, set[Task]] = {}

    for task in tasks:
        if task._enabled:
            dependencies[task] = set()

    for task in tasks:
        if task._enabled:
            for subtask in task.requires:
                if subtask._enabled:
                    dependencies[task].add(subtask)
            for subtask in task.required_by:
                if subtask._enabled:
                    dependencies[subtask].add(task)

    while True:
        if not dependencies:
            break

        tasks_to_pop = []

        for task in dependencies:
            if not dependencies[task]:
                result.append(task)
                tasks_to_pop.append(task)

                for t in dependencies:
                    if task in dependencies[t]:
                        dependencies[t].remove(task)

        if not tasks_to_pop:
            raise Exception("Cyclic dependency")

        for task in tasks_to_pop:
            dependencies.pop(task)

    return result
