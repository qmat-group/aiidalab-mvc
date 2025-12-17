from .model import Model
from .view import View
from .controller import Controller
from IPython.display import display

def run_app():
    """
    Initialize and display the application.
    """
    model = Model()
    view = View()
    controller = Controller(model, view)
    
    display(view)

if __name__ == "__main__":
    run_app()
