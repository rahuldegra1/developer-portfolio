class work:
    def __init__(self):
        self.tasks = []

    def add_task(self):
        new_task = input("Enter your task: ")
        self.tasks.append(new_task)
        print("Task successfully Added!")

    def view_task(self):
        if len(self.tasks) == 0:
            print("Your list is currently empty.")
        else:
            print("Your tasks")
            for task in self.tasks:
                print(task)

    def delete_task(self):
        task_to_delete = input("Which task you want to remove?... ")
        for tsk in self.tasks:
            if tsk == task_to_delete:
                self.tasks.remove(tsk)
                print("Task removed!")
                break
        else:
            print("Task not found.")


my_list = work()
while True:
    print("1. add new Task")
    print("2. view Tasks")
    print("3.quit")
    print("4. delete Task")

    user = input("Enter Choice...")

    if user == "1":
        my_list.add_task()

    elif user == "2":
        my_list.view_task()

    elif user == "3":
        break

    elif user == "4":
        my_list.delete_task()
