from todo_app import TodoAppBuilder, TodoApp


def main():
    todo_app = TodoAppBuilder(TodoApp).build()
    todo_app.run()


if __name__ == "__main__":
    main()
