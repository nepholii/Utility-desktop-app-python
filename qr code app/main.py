import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
    QMainWindow, QSizePolicy, QStackedWidget, QLineEdit, QGridLayout,QProgressBar
)
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPropertyAnimation
from googletrans import Translator

from generator import *
from language import *

class Home(QWidget):
    def __init__(self, parent: QWidget = None, flags: Qt.WindowFlags = Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)
        self.initUI()
        self.settings()

    def initUI(self):
        # Create the stacked widget
        self.stacked_widget = QStackedWidget()

        # Create the combo box and connect its signal
        self.combo_box = QComboBox()
        options = ["Qr code", "BMI", "Calculator", "Translator"]
        self.combo_box.addItems(options)
        self.combo_box.currentIndexChanged.connect(self.switch_layout)
        self.combo_box.setStyleSheet("""
            QComboBox {
                border: 2px solid #A3C1DA;
                border-radius: 10px;
                padding: 5px;
                background-color: #EAF7FF;
                color: #333;
                font-size: 20px;
                min-width: 150px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 2px;
                border-left-color: #A3C1DA;
                border-left-style: solid;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                background-color: #A3C1DA;
            }
            QComboBox::down-arrow {
                image: url(/path/to/cloud-icon.png);
                width: 15px;
                height: 15px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #A3C1DA;
                selection-background-color: #BEE3F7;
                background-color: #EAF7FF;
                color: #333;
                padding: 5px;
            }
        """)


        # Create the QR code layout
        self.qr_layout = self.create_qr_layout()

        # Create the BMI layout
        self.bmi_layout = self.create_bmi_layout()

        # Create the Calculator layout
        self.calculator_layout = self.create_calculator_layout()

        self.translator_layout = self.create_translator_layout()

        # Add layouts to the stacked widget
        self.stacked_widget.addWidget(self.qr_layout)
        self.stacked_widget.addWidget(self.bmi_layout)
        self.stacked_widget.addWidget(self.calculator_layout)
        self.stacked_widget.addWidget(self.translator_layout)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.combo_box)
        self.main_layout.addWidget(self.stacked_widget)

        self.setLayout(self.main_layout)
        self.resize(400, 300)

    def create_qr_layout(self):
        widget = QWidget()
        vbox = QVBoxLayout(widget)

        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #A3C1DA;
                border-radius: 10px;
                padding: 10px;
                background-color: #EAF7FF;
                color: #333;
                font-size: 16px;
            }
            QTextEdit QScrollBar:vertical {
                border: none;
                background: #EAF7FF;
                width: 12px;
                margin: 3px 0 3px 0;
                border-radius: 4px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background: #A3C1DA;
                min-height: 20px;
                border-radius: 4px;
            }
            QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        self.generate_button = QPushButton("Generate QR Code")
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #87CEEB; /* SkyBlue */
                border: 2px solid #00BFFF; /* DeepSkyBlue */
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00BFFF; /* DeepSkyBlue */
                border: 2px solid #1E90FF; /* DodgerBlue */
            }
            QPushButton:pressed {
                background-color: #1E90FF; /* DodgerBlue */
                border: 2px solid #4169E1; /* RoyalBlue */
            }
            """)
        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #87CEEB; /* SkyBlue */
                border: 2px solid #00BFFF; /* DeepSkyBlue */
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00BFFF; /* DeepSkyBlue */
                border: 2px solid #1E90FF; /* DodgerBlue */
            }
            QPushButton:pressed {
                background-color: #1E90FF; /* DodgerBlue */
                border: 2px solid #4169E1; /* RoyalBlue */
            }
        """)
        self.qr_code_label = QLabel()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        image_path = "empty.jpg"
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)
        self.label.setStyleSheet("""
            QLabel {
                border-left: 1px solid #1E90FF; /* DodgerBlue */
                border-right: 1px solid #1E90FF; /* DodgerBlue */
                padding-left: 100px;
                padding-right: 100px;
                background-color: #EAF7FF; /* Light sky color */
            }
            QLabel::before {
                content: '';
                display: inline-block;
                width: 56px;
                height: 100%;
                background-color: #1E90FF; /* DodgerBlue */
            }
            QLabel::after {
                content: '';
                display: inline-block;
                width: 56px;
                height: 100%;
                background-color: #1E90FF; /* DodgerBlue */
            }
        """)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.generate_button.clicked.connect(self.qr_click)
        self.reset_button.clicked.connect(self.reset_app)

        vbox.addWidget(self.text_edit)
        vbox.addWidget(self.generate_button)
        vbox.addWidget(self.label)
        vbox.addWidget(self.reset_button)
        vbox.addWidget(self.qr_code_label)
        
        return widget

    def create_bmi_layout(self):
        widget = QWidget()
        vbox = QVBoxLayout(widget)

        self.weight_edit = QTextEdit()
        self.weight_edit.setPlaceholderText("Enter weight (kg)")
        self.height_edit = QTextEdit()
        self.height_edit.setPlaceholderText("Enter height (cm)")
        self.calculate_bmi_button = QPushButton("Calculate BMI")
        self.bmi_result_label = QLabel("")
        self.meter = QProgressBar()
        self.meter.setMinimum(15)
        self.meter.setMaximum(35)
        self.meter.setValue(15)  

        self.calculate_bmi_button.clicked.connect(self.calculate_bmi)

        vbox.addWidget(self.weight_edit)
        vbox.addWidget(self.height_edit)
        vbox.addWidget(self.calculate_bmi_button)
        vbox.addWidget(self.bmi_result_label)
        vbox.addWidget(self.meter)
        
        return widget

    def create_calculator_layout(self):
        widget = QWidget()
        widget.setObjectName("translatorWidget") 
        grid = QGridLayout(widget)

       

        self.calc_display = QLineEdit()
        self.calc_display.setReadOnly(True)
        self.calc_display.setAlignment(Qt.AlignRight)
        self.calc_display.setFixedHeight(75)
        self.calc_display.setStyleSheet(""" 
            QLineEdit {
                border: 2px solid #A3C1DA;
                border-radius: 10px;
                padding: 10px;
                background-color: #EAF7FF;
                color: #333;
                font-size: 30px;
            }""")
        self.clear = QPushButton("Clear")
        self.clear.setStyleSheet("""
             QPushButton {
                border: 2px solid #A3C1DA;
                border-radius: 10px;
                padding: 10px;
                background-color: #EAF7FF;
                color: #333;
                font-size: 24px;
            }""")
        self.clear.clicked.connect(self.on_calc_button_click)
        
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]

        for (text, row, col) in buttons:
            button = QPushButton(text)
            button.setStyleSheet("""
            QPushButton {
                border: 2px solid #A3C1DA;
                border-radius: 10px;
                padding: 10px;
                background-color: #EAF7FF;
                color: #333;
                font-size: 24px;
            }
        """)
            button.setFixedSize(200, 200)
            button.clicked.connect(self.on_calc_button_click)
            grid.addWidget(button, row, col)

        grid.addWidget(self.calc_display, 0, 0, 1, 4)
        grid.addWidget(self.clear,5,0,1,4)
        widget.setStyleSheet("""
        QWidget#translatorWidget {
            background-color: #333; /* Darker background color */
            color: #fff; /* Text color */
        }

        QWidget#translatorWidget QPushButton {
            background-color: #66a3ff; /* Lighter background color for buttons */
            color: #333; /* Text color for buttons */
            border: 1px solid #fff; /* White border for buttons */
            border-radius: 5px; /* Rounded corners for buttons */
            padding: 5px 10px; /* Padding for buttons */
        }

        QWidget#translatorWidget QPushButton:hover {
            background-color: #3399ff; /* Lighter background color for buttons on hover */
        }
    """)

        return widget
    
    def create_translator_layout(self):
        widget = QWidget()
        grid = QGridLayout(widget)
        self.input_box = QTextEdit()
        self.output_box = QTextEdit()
        self.reverse = QPushButton("Reverse")
        self.reset = QPushButton("Reset")
        self.submit = QPushButton("Translate Now")
        self.input_option = QComboBox()
        self.output_option = QComboBox()
        self.title = QLabel("Translator")
        self.title.setFont(QFont("Helvetica",45))
        self.input=QLabel("Input language")
        self.Output=QLabel("Output language")
        
        self.input_option.addItems(values)
        self.output_option.addItems(values)
        
        grid.addWidget(self.title)
        grid.addWidget(self.input)
        grid.addWidget(self.input_option)
        grid.addWidget(self.Output)
        grid.addWidget(self.output_option)
        grid.addWidget(self.input_box)
        grid.addWidget(self.submit)    
        grid.addWidget(self.reverse)
        grid.addWidget(self.output_box)
        grid.addWidget(self.reset)
        self.submit.clicked.connect(self.translate_click)
        self.reverse.clicked.connect(self.rev_click)
        self.reset.clicked.connect(self.reset_apps)
        widget.setStyleSheet("""
        

            QPushButton {
                background-color: #87CEEB; /* Lighter background color for buttons */
                color: #333; /* Text color for buttons */
                border: 1px solid #fff; /* White border for buttons */
                border-radius: 5px; /* Rounded corners for buttons */
                padding: 5px 10px; /* Padding for buttons */
            }

            QPushButton:hover {
                background-color: #3399ff; /* Lighter background color for buttons on hover */
            }
        """)
    
        return widget

    def switch_layout(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def settings(self):
        self.setWindowTitle("Utility Application")
        self.setGeometry(250, 250, 1920, 1080)


    def qr_click(self):
        data = self.text_edit.toPlainText()
        qrgenerator(data)
        image_path = "MyQRCode1.png"
        self.label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def reset_app(self):
        self.text_edit.clear()
        self.qr_code_label.clear()
        self.label.setPixmap(QPixmap("empty.jpg"))

    def calculate_bmi(self):
        self.animation = QPropertyAnimation(self.meter, b"value")
        self.animation.setDuration(2000)  # 2 seconds duration
        self.animation.setStartValue(0)
        
        
        try:
            weight = float(self.weight_edit.toPlainText())
            height = float(self.height_edit.toPlainText()) / 100  # Convert height to meters
            bmi = weight / (height * height)
            self.bmi_result_label.setText(f"BMI: {bmi:.2f}")
        except ValueError:
            self.bmi_result_label.setText("Please enter valid numbers for weight and height")
        self.animation.setEndValue(bmi)
        self.animation.start()

    def on_calc_button_click(self):
        button = self.sender()
        if button.text() == '=':
            try:
                result = str(eval(self.calc_display.text()))
                self.calc_display.setText(result)
            except Exception as e:
                self.calc_display.setText("Error")
        elif button.text()=="Clear":
            self.calc_display.setText("")
        else:
            self.calc_display.setText(self.calc_display.text() + button.text())

    def translate_text(self,text,dest_lang,source_lang):
        speaker=Translator()
        translation=speaker.translate(text,dest_lang,source_lang)
        return translation.text
    def translate_click(self):
        try:
            value_to_key1 = self.output_option.currentText()
            value_to_key2 = self.input_option.currentText()
            key_to_value1 = [k for k,v in LANGUAGES.items() if v == value_to_key1]

            key_to_value2 = [k for k,v in LANGUAGES.items() if v == value_to_key2]
            self.script = self.translate_text(self.input_box.toPlainText(), key_to_value1[0],key_to_value2[0])
            self.output_box.setText(self.script)
        except Exception as e:
            print("Exception:", e)
            self.input_box.setText("You must enter text to translate here...")

    def reset_apps(self):
        self.input_box.clear()
        self.output_box.clear()
    
    def rev_click(self):
        s1,l1 = self.input_box.toPlainText(),self.input_option.currentText()
        s2,l2 = self.output_box.toPlainText(),self.output_option.currentText()
        
        self.input_box.setText(s2)
        self.output_box.setText(s1)
        self.input_option.setCurrentText(l2)
        self.output_option.setCurrentText(l1)

if __name__ == "__main__":
    app = QApplication([])
    main = Home()
    main.show()
    app.exec_()
