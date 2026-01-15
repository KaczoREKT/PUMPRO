from Controller.controller import Controller
from Model.main import Model
from View.main import View

if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()
   