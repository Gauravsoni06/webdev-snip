import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QStackedWidget, QTextEdit, QTableWidget, QTableWidgetItem, QSizePolicy, QComboBox, QCheckBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QStackedWidget, QTextEdit, QTableWidget, QTableWidgetItem, QSizePolicy, QComboBox, QCheckBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QGroupBox, QFormLayout
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shazam")
        
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E6E6FA; /* Set the background color of the main window to a light lavender */
            }
            QPushButton {
                background-color: #800080; /* Set the button background color to purple */
                color: white; /* Set the button text color to white */
                border: none; /* Remove any border around the button */
                padding: 5px 10px; /* Add padding around button text */
                border-radius: 5px; /* Round the button edges slightly */
                min-width: 150px; /* Set the maximum width of the button */
                max-width: 150px; /* Set the maximum width of the button */
                font-size: 20px; /* Increase font size for labels */
            }
            QPushButton:hover {
                background-color: #9932CC; /* Change button background to a lighter purple on hover */
            }
            QLabel {
                color: #800080; /* Set label text color to purple */
                font-size: 24px; /* Increase font size for labels */
            }
            #titleBar {
                background-color: #800080; /* Set title bar background color to purple */
                color: white; /* Set title bar text color to white */
                font-size: 48px; /* Set a large font size for title text */
                font-weight: bold; /* Make title text bold */
                padding: 10px; /* Add padding inside the title bar */
                text-align: center; /* Center-align the title text */
            }
            QTabBar::tab {
                background: #E6E6FA; /* Set background color for each tab to light lavender */
                border: 1px solid #800080; /* Add a purple border around each tab */
                padding: 5px 10px; /* Add padding inside each tab */
                margin: 0px; /* Remove any spacing between tabs */
                font-size: 20px; /* Increase the font size for tab text */
                font-weight: bold; /* Make tab text bold */
                color: #800080; /* Set tab text color to purple */
                border-top-left-radius: 8px; /* Round the top-left corner of each tab */
                border-top-right-radius: 8px; /* Round the top-right corner of each tab */
            }
            QTabBar::tab:selected {
                background: #800080; /* Change background color to purple for selected tabs */
                color: white; /* Change text color to white for selected tabs */
            }
            QTabBar::tab:hover {
                background: #CDA8EF; /* Set a lighter purple background on tab hover */
            }
            """)




        # Create the central widget with tabs
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setStyleSheet("QTabBar::tab { height: 30px; width: 100px; }")

        # Align tabs in the center
        self.tab_widget.setStyleSheet("QTabWidget::pane { border: 0; } QTabWidget::tab-bar { alignment: center; } QTabBar::tab { min-width: 120px; }")

        # Create the tabs
        self.load_file_page = QWidget()
        self.load_checks_page = QWidget()
        self.run_checks_page = QWidget()
        self.result_page = QWidget()

        # Add tabs to the tab widget
        self.tab_widget.addTab(self.load_file_page, "Load File")
        self.tab_widget.addTab(self.load_checks_page, "Load Checks")
        self.tab_widget.addTab(self.run_checks_page, "Run Checks")
        self.tab_widget.addTab(self.result_page, "Result")

        # Create the main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 20)  # Remove margins
        main_layout.setSpacing(0)  # Remove spacing

        main_layout.addWidget(QLabel("Shazam", alignment=Qt.AlignCenter, objectName="titleBar"))
        main_layout.addSpacing(20)
        main_layout.addWidget(self.tab_widget)
        self.central_widget.setLayout(main_layout)

        # Initialize the navigation buttons
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.previous_tab)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_tab)

        # Update the navigation buttons based on the current tab
        self.update_navigation_buttons()

        # Create the Load File page
        self.setup_load_file_page()

        # Create the Load Checks page
        self.setup_load_checks_page()

        # Create the Run Checks page
        self.setup_run_checks_page()

        # Create the Result page
        self.setup_result_page()

        # Connect tab change signal to update navigation buttons
        self.tab_widget.currentChanged.connect(self.update_navigation_buttons)


    def setup_load_file_page(self):
        layout = QVBoxLayout()
        
        self.load_file_label = QLabel("Load File")
        self.file_name_label = QLabel("")
        load_file_button = QPushButton("Browse")
        load_file_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        load_file_button.clicked.connect(self.load_file)
        self.remove_file_button = QPushButton("✖")
        self.remove_file_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.remove_file_button.setVisible(False)
        self.remove_file_button.clicked.connect(self.remove_file)
        self.table_widget = QTableWidget()  # Add this line
    
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_name_label)
        file_layout.addWidget(self.remove_file_button)
    
        layout.addWidget(self.load_file_label)
        layout.addWidget(load_file_button, alignment=Qt.AlignLeft)
        layout.addLayout(file_layout)
        layout.addWidget(self.table_widget)  # Add the table widget to the layout
        layout.addStretch()  # Add stretch to push buttons to the bottom
    
        # Create a new layout for the navigation bar
        nav_bar_layout = QHBoxLayout()
        nav_bar_layout.addStretch()  # Add stretch to push buttons to the right
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.previous_tab)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_tab)
        nav_bar_layout.addWidget(self.back_button)
        nav_bar_layout.addWidget(self.next_button)
    
        # Add the navigation bar layout to the main layout
        layout.addLayout(nav_bar_layout)
    
        self.load_file_page.setLayout(layout)





    def setup_load_checks_page(self):
        layout = QVBoxLayout()
    
        groupbox1 = QGroupBox("Check Type 1")
        groupbox1.setStyleSheet("""
            QGroupBox { 
                border: 2px solid #800080; 
                border-radius: 5px; 
                margin-top: 1ex; 
            }
            QGroupBox::title {
                color: #800080; 
                subcontrol-origin: margin; 
                subcontrol-position: top center; /* Align the title center */
                padding: 0 3px;
            }
        """)
        groupbox1_layout = QVBoxLayout()
    
        self.checks_type1 = [
            QCheckBox("Check 1"),
            QCheckBox("Check 2"),
            QCheckBox("Check 3"),
            QCheckBox("Check 4")
        ]
    
        for check in self.checks_type1:
            check.setStyleSheet("color: black;")  # Set the font color to black
            groupbox1_layout.addWidget(check)
    
        groupbox1.setLayout(groupbox1_layout)
    
        groupbox2 = QGroupBox("Check Type 2")
        groupbox2.setStyleSheet("""
            QGroupBox { 
                border: 2px solid #800080; 
                border-radius: 5px; 
                margin-top: 1ex; 
            }
            QGroupBox::title {
                color: #800080; 
                subcontrol-origin: margin; 
                subcontrol-position: top center; /* Align the title center */
                padding: 0 3px;
            }
        """)
        groupbox2_layout = QVBoxLayout()
    
        self.checks_type2 = [
            QCheckBox("Check 5"),
            QCheckBox("Check 6"),
            QCheckBox("Check 7"),
            QCheckBox("Check 8")
        ]
    
        for check in self.checks_type2:
            check.setStyleSheet("color: black;")  # Set the font color to black
            groupbox2_layout.addWidget(check)
    
        groupbox2.setLayout(groupbox2_layout)
    
        layout.addWidget(groupbox1)
        layout.addWidget(groupbox2)
    
        # Create a layout for the buttons
        button_layout = QHBoxLayout()
        select_all_button = QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all_checks)
        clear_all_button = QPushButton("Clear All")
        clear_all_button.clicked.connect(self.clear_all_checks)
        load_checks_button = QPushButton("Load Selected Checks")
        load_checks_button.clicked.connect(self.load_selected_checks)
    
        button_layout.addWidget(select_all_button)
        button_layout.addWidget(clear_all_button)
        button_layout.addWidget(load_checks_button)
    
        layout.addLayout(button_layout)
        layout.addStretch()  # Add stretch to push buttons to the bottom
    
        self.checks_display = QTextEdit()
        self.checks_display.setReadOnly(True)
        layout.addWidget(self.checks_display)
    
        # Create a new layout for the navigation bar
        nav_bar_layout = QHBoxLayout()
        nav_bar_layout.addStretch()  # Add stretch to push buttons to the right
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.previous_tab)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_tab)
        nav_bar_layout.addWidget(back_button)
        nav_bar_layout.addWidget(next_button)
    
        # Add the navigation bar layout to the main layout
        layout.addLayout(nav_bar_layout)
    
        self.load_checks_page.setLayout(layout)






    def setup_run_checks_page(self):
        layout = QVBoxLayout()
        run_checks_button = QPushButton("Run Checks")
        run_checks_button.clicked.connect(self.run_checks)
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Check", "Result"])
        layout.addWidget(run_checks_button)
        layout.addWidget(self.results_table)
        layout.addStretch()  # Add stretch to push buttons to the bottom
    
        # Create a new layout for the navigation bar
        nav_bar_layout = QHBoxLayout()
        nav_bar_layout.addStretch()  # Add stretch to push buttons to the right
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.previous_tab)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_tab)
        nav_bar_layout.addWidget(back_button)
        nav_bar_layout.addWidget(next_button)
    
        # Add the navigation bar layout to the main layout
        layout.addLayout(nav_bar_layout)
    
        self.run_checks_page.setLayout(layout)

    
    def setup_result_page(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Result"))
        
        self.result_table_widget = QTableWidget()  # Create a table widget for the result page
        layout.addWidget(self.result_table_widget)
    
        layout.addStretch()  # Add stretch to push buttons to the bottom
    
        # Create a new layout for the navigation bar
        nav_bar_layout = QHBoxLayout()
        nav_bar_layout.addStretch()  # Add stretch to push buttons to the right
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.previous_tab)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_tab)
        nav_bar_layout.addWidget(self.back_button)
        nav_bar_layout.addWidget(self.next_button)
    
        # Add the navigation bar layout to the main layout
        layout.addLayout(nav_bar_layout)
    
        self.result_page.setLayout(layout)


    def load_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.file_name_label.setText(f"Loaded File: {file_path}")
            self.remove_file_button.setVisible(True)
    
            # Read the Excel file using pandas
            df = pd.read_excel(file_path)
            self.df = df  # Save the data frame to the instance
    
            # Display the first 10 rows in the table widget
            self.table_widget.setRowCount(10)
            self.table_widget.setColumnCount(len(df.columns))
            self.table_widget.setHorizontalHeaderLabels(df.columns)
    
            for row in range(10):
                for col in range(len(df.columns)):
                    self.table_widget.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))
    
            # Update the result table with the loaded data
            self.update_result_table()


    def remove_file(self):
        self.file_name_label.setText("")
        self.remove_file_button.setVisible(False)
        self.table_widget.setRowCount(0)  # Clear the table widget


    def load_selected_checks(self):
        selected_checks_type1 = [check.text() for check in self.checks_type1 if check.isChecked()]
        selected_checks_type2 = [check.text() for check in self.checks_type2 if check.isChecked()]

        all_selected_checks = selected_checks_type1 + selected_checks_type2

        if all_selected_checks:
            self.checks_display.setText("\n".join(all_selected_checks))
        else:
            self.checks_display.setText("No checks selected.")

    def run_checks(self):
        results = [
            ("Data completeness", "Passed"),
            ("Data format", "Passed"),
            ("Missing values", "Failed"),
            ("Duplicate entries", "Passed")
        ]
        self.results_table.setRowCount(len(results))
        for row, (check, result) in enumerate(results):
            self.results_table.setItem(row, 0, QTableWidgetItem(check))
            self.results_table.setItem(row, 1, QTableWidgetItem(result))

    def next_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index < self.tab_widget.count() - 1:
            self.tab_widget.setCurrentIndex(current_index + 1)
        self.update_navigation_buttons()

    def previous_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index > 0:
            self.tab_widget.setCurrentIndex(current_index - 1)
        self.update_navigation_buttons()


    def select_all_checks(self):
        for check in self.checks_type1 + self.checks_type2:
            check.setChecked(True)
    
    def clear_all_checks(self):
        for check in self.checks_type1 + self.checks_type2:
            check.setChecked(False)

    def update_navigation_buttons(self):
        current_index = self.tab_widget.currentIndex()
        self.back_button.setEnabled(current_index > 0)
        self.next_button.setEnabled(current_index < self.tab_widget.count() - 1)

    def update_result_table(self):
        if hasattr(self, 'df'):
            df = self.df
            self.result_table_widget.setRowCount(len(df))
            self.result_table_widget.setColumnCount(len(df.columns))
            self.result_table_widget.setHorizontalHeaderLabels(df.columns)
    
            for row in range(len(df)):
                for col in range(len(df.columns)):
                    self.result_table_widget.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))
    

    def closeEvent(self, event):
        print("Application is closing...")
        event.accept()

if __name__ == "__main__":
    app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
