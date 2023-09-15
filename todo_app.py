import tkinter
from tkinter import messagebox

from base import TodoAppWithDB
from managers import TodoAppDBManager


class TodoApp(TodoAppWithDB):
    def __init__(
            self,
            width: int,
            height: int,
            title: str,
            text_color: str,
            bg_color: str,
            bg_secondary_color: str,
            btn_color: str,
            btn_hover_color: str,
            db_manager: type[TodoAppDBManager],
    ):
        super().__init__(
            width,
            height,
            title,
            text_color,
            bg_color,
            bg_secondary_color,
            btn_color,
            btn_hover_color,
            db_manager,
        )
        self.root = tkinter.Tk()

        self.label_title = self.create_title()
        self.input = self.create_input()

        self.tasks_frame = self.create_tasks_frame()
        self.tasks_listbox = self.create_tasks_listbox()
        self.tasks_listbox_scrollbar = self.create_tasks_listbox_scrollbar()

        self.add_task_btn = self.create_add_task_btn()
        self.edit_task_btn = self.create_edit_task_btn()
        self.remove_task_btn = self.create_remove_task_btn()

        self.load_tasks()

    def run(self) -> None:
        """
        Starts the application.
        """
        self.configure()
        self.root.mainloop()

    def configure(self) -> None:
        """
        Configures the application, the interaction of
        different parts of applications with each other.
        """
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg=self.bg_color)
        self.tasks_listbox.config(yscrollcommand=self.tasks_listbox_scrollbar.set)
        self.tasks_listbox_scrollbar.config(command=self.tasks_listbox.yview)

    def load_tasks(self):
        for task in self.db_manager.load_tasks():
            self.tasks_listbox.insert(tkinter.END, task[0])

    def create_title(self) -> tkinter.Label:
        """
        Creates and returns the title label of the application.
        """
        title = tkinter.Label(
            self.root,
            text="Daily Tasks",
            font=("Helvetica", 24),
            fg=self.text_color,
            background=self.bg_color,
        )
        title.pack(pady=(30, 20))
        return title

    def create_input(self) -> tkinter.Entry:
        """
        Creates and returns the field for entering a task.
        """
        entry = tkinter.Entry(
            self.root,
            font=("Helvetica", 14),
            fg=self.text_color,
            background=self.bg_secondary_color,
        )
        entry.pack(fill=tkinter.BOTH)
        return entry

    def create_tasks_frame(self) -> tkinter.Frame:
        """
        Creates and returns the tasks frame.
        """
        frame = tkinter.Frame(
            self.root,
            background=self.bg_secondary_color,
            height=200,
        )
        frame.pack(pady=(0, 20), fill=tkinter.BOTH)
        return frame

    def create_tasks_listbox_scrollbar(self) -> tkinter.Scrollbar:
        """
        Creates and returns the tasks frame's listbox scrollbar.
        """
        scrollbar = tkinter.Scrollbar(self.tasks_frame)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        return scrollbar

    def create_tasks_listbox(self) -> tkinter.Listbox:
        """
        Creates and returns the tasks frame's listbox.
        """
        listbox = tkinter.Listbox(
            self.tasks_frame,
            selectmode=tkinter.EXTENDED,
        )
        listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        return listbox

    def add_task(self) -> None:
        """
        Callback function to add a task to the task list.
        """
        task = self.input.get()
        if task:
            self.tasks_listbox.insert(tkinter.END, task)
            self.input.delete(0, tkinter.END)
            self.db_manager.add_task(task)
        else:
            messagebox.showwarning(
                "Empty task",
                "Please, enter a task.",
            )

    def create_add_task_btn(self) -> tkinter.Button:
        """
        Creates and returns the add task button.
        """
        button = tkinter.Button(
            self.root,
            text="Add",
            font=("Helvetica", 12),
            command=self.add_task,
            fg=self.text_color,
            bg=self.btn_color,
            border=0,
        )
        self.create_btn_hover(button)
        button.pack(pady=(0, 10))
        return button

    def edit_task(self) -> None:
        """
        Callback function to edit a task of the task list.
        """
        new_task_text = self.input.get()
        if not new_task_text:
            messagebox.showwarning(
                "Empty task",
                "Please, enter a new task.",
            )
        else:
            try:
                selected_tasks = self.tasks_listbox.curselection()
                for task_index in selected_tasks:
                    task_id = self.db_manager.get_task_id_by_index(task_index)
                    if task_id is not None:
                        self.db_manager.edit_task(task_id, new_task_text)
                    self.tasks_listbox.delete(task_index)
                    self.tasks_listbox.insert(task_index, new_task_text)
                    self.input.delete(0, tkinter.END)
            except IndexError:
                messagebox.showwarning(
                    "No task selected",
                    "Please, select a task to edit.",
                )

    def create_edit_task_btn(self) -> tkinter.Button:
        """
        Creates and returns the edit task button.
        """
        button = tkinter.Button(
            self.root,
            text="Edit",
            font=("Helvetica", 12),
            command=self.edit_task,
            fg=self.text_color,
            bg=self.btn_color,
            border=0,
        )
        self.create_btn_hover(button)
        button.pack(pady=(0, 10))
        return button

    def remove_task(self) -> None:
        """
        Callback function to remove a task from the task list.
        """
        selected_tasks = self.tasks_listbox.curselection()
        if not selected_tasks:
            messagebox.showwarning(
                "Нет выбранной задачи",
                "Пожалуйста, выберите задачу для удаления.",
            )
        for task_index in selected_tasks[::-1]:
            task_id = self.db_manager.get_task_id_by_index(task_index)
            if task_id is not None:
                self.db_manager.remove_task(task_id)
            self.tasks_listbox.delete(task_index)

    def create_remove_task_btn(self) -> tkinter.Button:
        """
        Creates and returns the remove task button.
        """
        button = tkinter.Button(
            self.root,
            text="Remove",
            font=("Helvetica", 12),
            command=self.remove_task,
            fg=self.text_color,
            bg=self.btn_color,
            border=0,
        )
        self.create_btn_hover(button)
        button.pack(pady=(0, 10))
        return button

    def create_btn_hover(self, button) -> None:
        """
        Sets the behavior of the button when hovering over it.
        """
        button.bind(
            "<Enter>",
            lambda event: button.config(bg=self.btn_hover_color),
        )
        button.bind(
            "<Leave>",
            lambda event: button.config(bg=self.btn_color),
        )


class TodoAppBuilder:
    width = 750
    height = 450
    title = "Todo App"
    text_color = "white"
    bg_color = "gray16"
    bg_secondary_color = "gray26"
    btn_color = "dodgerblue3"
    btn_hover_color = "dodgerblue4"

    def __init__(self, app: type[TodoAppWithDB]):
        self.app = app

    def build(self) -> TodoAppWithDB:
        return self.app(
            self.width,
            self.height,
            self.title,
            self.text_color,
            self.bg_color,
            self.bg_secondary_color,
            self.btn_color,
            self.btn_hover_color,
            TodoAppDBManager,
        )
