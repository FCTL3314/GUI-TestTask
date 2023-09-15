import sqlite3


class TodoAppDBManager:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite3.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT, task_text TEXT
            )
        ''')
        self.conn.commit()

    def get_task_id_by_index(self, index: int) -> None | int:
        data = self.cursor.execute("SELECT id FROM tasks")
        task_ids = data.fetchall()
        if index < len(task_ids):
            return task_ids[index][0]
        return None

    def load_tasks(self) -> list[str]:
        data = self.cursor.execute("SELECT task_text FROM tasks")
        return data.fetchall()

    def add_task(self, task) -> None:
        self.cursor.execute(f"INSERT INTO tasks (task_text) VALUES ('{task}')")
        self.conn.commit()

    def edit_task(self, task_id, new_task) -> None:
        self.cursor.execute(f"UPDATE tasks SET task_text = '{new_task}' WHERE id = {task_id}")
        self.conn.commit()

    def remove_task(self, task_id) -> None:
        self.cursor.execute(f"DELETE FROM tasks WHERE id = {task_id}")
        self.conn.commit()
