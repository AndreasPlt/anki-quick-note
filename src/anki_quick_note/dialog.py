"""The input window: one line, Enter saves, Esc cancels.

A window of its own rather than a widget inside the main window: the reviewer's
shortcuts (1-4, space, ...) only fire while the main window is active, so typing
here cannot answer the card.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from aqt.qt import QDialog, QLabel, QLineEdit, Qt, QVBoxLayout


class NoteDialog(QDialog):
    def __init__(
        self,
        parent,
        title: str,
        existing: Sequence[str],
        on_save: Callable[[str], None],
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setMinimumWidth(420)
        self._on_save = on_save

        layout = QVBoxLayout(self)
        if existing:
            noted = QLabel("\n".join(f"• {line}" for line in existing))
            noted.setWordWrap(True)
            noted.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(noted)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter saves, Esc cancels")
        self.input.returnPressed.connect(self.accept)
        layout.addWidget(self.input)

    def accept(self) -> None:
        text = self.input.text().strip()
        if text:
            self._on_save(text)
        super().accept()
