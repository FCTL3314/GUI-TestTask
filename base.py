from abc import ABC, abstractmethod

from managers import TodoAppDBManager


class AbstractGUIApp(ABC):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @abstractmethod
    def run(self) -> None:
        ...


class BaseTodoApp(AbstractGUIApp, ABC):
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
    ):
        super().__init__(width, height)
        self.title = title
        self.label_title = title
        self.text_color = text_color
        self.bg_color = bg_color
        self.bg_secondary_color = bg_secondary_color
        self.btn_color = btn_color
        self.btn_hover_color = btn_hover_color


class TodoAppWithDB(BaseTodoApp, ABC):
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
        )
        self.db_manager = db_manager()
