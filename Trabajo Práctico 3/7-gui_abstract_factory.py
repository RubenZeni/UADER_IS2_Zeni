# gui_abstract_factory.py
# Patrón Abstract Factory – ejemplo de GUI multiplataforma

from abc import ABC, abstractmethod

# Productos abstractos
class Label(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class Button(ABC):
    @abstractmethod
    def click(self) -> str:
        pass

# Fábrica abstracta
class GUIFactory(ABC):
    @abstractmethod
    def create_label(self) -> Label:
        pass

    @abstractmethod
    def create_button(self) -> Button:
        pass

# Implementaciones Windows
class WinLabel(Label):
    def render(self) -> str:
        return "[Label Windows]"

class WinButton(Button):
    def click(self) -> str:
        return "Click Windows"

class WinFactory(GUIFactory):
    def create_label(self) -> Label:
        return WinLabel()
    def create_button(self) -> Button:
        return WinButton()

# Implementaciones MacOS
class MacLabel(Label):
    def render(self) -> str:
        return "(Label MacOS)"

class MacButton(Button):
    def click(self) -> str:
        return "Click MacOS"

class MacFactory(GUIFactory):
    def create_label(self) -> Label:
        return MacLabel()
    def create_button(self) -> Button:
        return MacButton()

# Client code
def create_ui(factory: GUIFactory):
    label = factory.create_label()
    button = factory.create_button()
    print(label.render())
    print(button.click())

if __name__ == "__main__":
    print("UI Windows:")
    create_ui(WinFactory())
    print("\nUI MacOS:")
    create_ui(MacFactory())
