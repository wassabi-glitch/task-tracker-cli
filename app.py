import sys
import json
import os
from datetime import datetime

DATA_FILE = "data.json"
VALID_STATUSES = ["todo", "in-progress", "done"]


def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


def load_tasks():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def now():
    return datetime.now().isoformat(timespec="seconds")


def get_next_id(tasks):
    return max((task["id"] for task in tasks), default=0) + 1


def add_task(description, status):

    if status not in VALID_STATUSES:
        print(f"Invalid status. Use one of: {', '.join(VALID_STATUSES)}")
        return
    tasks = load_tasks()
    task = {
        "id": get_next_id(tasks),
        "description": description,
        "status": status,
        "createdAt": now(),
        "updatedAt": now()
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")


def update_task(task_id, description, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["status"] = status
            task["updatedAt"] = now()
            save_tasks(tasks)
            print("Task updated.")
            return
    print("Task not found.")


def delete_task(task_id):
    # 1.LOADING ALL TASKS
    tasks = load_tasks()
    # 2.CREATING A NEW ARRAY TO INLCUDE ALL THE TASKS EXCEPT THE ONE THAT HAS BEEN PASSED TO THIS FUNCTION
    new_tasks = [t for t in tasks if t["id"] != task_id]
    # 3.IF LENGTH OF THE NEW ARRAY IS EQUAL TO THE TASKS ARRAY,
    # WE PRINT TASK NOT FOUND.FOR EXAMPLE,LETS SAY WE HAVE 3 TASKS ON OUR JSON FILE
    # [1,2,3],AND WE PASS DOWN ID OF 0 TO THIS FUNCTION, THEN LOGICALLY THE NEW ARRAY
    # WILL STORE 3 ELEMENTS AS WELL.
    if len(new_tasks) == len(tasks):
        print("Task not found.")
    # 4.IF THE LENGTH OF OUR NEW ARRAY DOES NOT MATCH THE LENGTH OF TASKS, THEN IT MEANS THE ID WE PASSED DOWN TO THIS FUNCTION GOT FILTERED OUT AND SO WE SAVE THE NEW TASKS ARRAY TO OUR JSON FILE AND THUS DELETING A TASK BY ITS ID THAT HAS BEEN PASSED DOWN TO THIS FUNCTIION
    else:
        save_tasks(new_tasks)
        print("Task deleted.")


def mark_task(task_id, status):
    if status not in VALID_STATUSES:
        print(f"Invalid status. Use one of: {', '.join(VALID_STATUSES)}")
        return
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = now()
            save_tasks(tasks)
            print("Task status updated.")
            return
    print("Task not found.")


def list_tasks(filter_status=None):
    tasks = load_tasks()
    filtered = tasks if filter_status is None or filter_status == "all" else [
        t for t in tasks if t["status"] == filter_status
    ]
    if not filtered:
        print("No tasks found.")
        return
    for task in filtered:
        print(f"[{task['id']}] {task['description']} ({task['status']})")


def print_help():
    print("""
Usage:
  python app.py add "description" status
  python app.py update id "new description" status
  python app.py delete id
  python app.py mark id status
  python app.py list [all|todo|in-progress|done]
""")


def main():
    ensure_data_file()
    args = sys.argv[1:]
    if not args:
        print_help()
        return

    command = args[0]

    try:
        if command == "add" and len(args) == 3:
            add_task(args[1], args[2])
        elif command == "update" and len(args) == 4:
            update_task(int(args[1]), args[2], args[3])
        elif command == "delete" and len(args) == 2:
            delete_task(int(args[1]))
        elif command == "mark" and len(args) == 3:
            mark_task(int(args[1]), args[2])
        elif command == "list":
            status = args[1] if len(args) > 1 else "all"
            list_tasks(status)
        else:
            print_help()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
