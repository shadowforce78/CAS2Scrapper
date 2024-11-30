import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget


class DataRenderer(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Data Renderer")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.render_data()

    def render_data(self):
        self.text_edit.append("\nModules:")
        for module_code, module in self.data["relevé"]["ressources"].items():
            self.text_edit.append(f"  Module Code: {module_code}")
            self.text_edit.append(f"    Title: {module['titre']}")
            self.text_edit.append(f"    Apogee Code: {module['code_apogee']}")
            self.text_edit.append(f"    URL: {module['url']}")
            for evaluation in module.get("evaluations", []):
                self.text_edit.append(f"      Evaluation ID: {evaluation['id']}")
                self.text_edit.append(f"      Coefficient: {evaluation['coef']}")
                self.text_edit.append(f"      Description: {evaluation['description']}")
                self.text_edit.append(f"      Note: {evaluation['note']['value']}")


if __name__ == "__main__":
    app = QApplication([])
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    window = DataRenderer(data)
    window.show()
    app.exec_()
