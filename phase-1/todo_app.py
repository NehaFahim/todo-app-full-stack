class TodoManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        task = {"title": title, "completed": False}
        self.tasks.append(task)
        print(f"✅ Task '{title}' added!")

    def view_tasks(self):
        if not self.tasks:
            print("\n📭 List is empty.")
            return
        print("\n--- Your Todo List ---")
        for idx, task in enumerate(self.tasks, 1):
            status = "✔" if task["completed"] else "❌"
            print(f"{idx}. {task['title']} [{status}]")

    def complete_task(self, index):
        try:
            self.tasks[index-1]["completed"] = True
            print("⭐ Task marked as complete!")
        except IndexError:
            print("⚠ Invalid task number.")

    def delete_task(self, index):
        try:
            removed = self.tasks.pop(index-1)
            print(f"🗑 Deleted: {removed['title']}")
        except IndexError:
            print("⚠ Invalid task number.")

def main():
    manager = TodoManager()
    while True:
        print("\n1. Add | 2. View | 3. Complete | 4. Delete | 5. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            t = input("Task title: ")
            manager.add_task(t)
        elif choice == '2':
            manager.view_tasks()
        elif choice == '3':
            idx = int(input("Task number to complete: "))
            manager.complete_task(idx)
        elif choice == '4':
            idx = int(input("Task number to delete: "))
            manager.delete_task(idx)
        elif choice == '5':
            break
        else:
            print("Try again!")

if __name__ == "__main__":
    main()