from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QStackedWidget, QTextEdit, QTableWidget, QTableWidgetItem, QSizePolicy, QComboBox, QCheckBox, QScrollArea
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize, QFileInfo
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QGroupBox, QFormLayout
import pandas as pd
from PySide6.QtWidgets import QHeaderView, QGridLayout
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QStackedWidget, QTextEdit, QTableWidget, QTableWidgetItem, QSizePolicy, QComboBox, QCheckBox, QScrollArea
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QFrame, QApplication, QMainWindow, QToolBar, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QStackedWidget, QTextEdit, QTableWidget, QTableWidgetItem, QSizePolicy, QComboBox, QCheckBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QGroupBox, QFormLayout
import pandas as pd
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QGridLayout





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shazam")
        #self.resize(1600, 800)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #E6E6FA; /* Light lavender background */
            }
            QPushButton {
                background-color: white; /* White button background */
                color: #800080; /* Purple button text */
                border: 2px solid #800080; /* Purple border around buttons */
                padding: 10px 20px; /* Adjust padding for a larger button */
                border-radius: 0px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #9932CC; /* Lighter purple on hover */
                color: white;
            }
            QLabel {
                color: #800080; /* Purple text */
                font-size: 24px;
            }
            #titleBar {
                background-color: #800080; /* Purple title bar */
                color: white;
                font-size: 48px;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            }
            QPushButton#tabButton {
                background: #E6E6FA; /* Light lavender background */
                border: 2px solid #800080; /* Purple border around each tab */
                padding: 15px 30px; /* Larger padding for bigger tabs */
                font-size: 20px;
                font-weight: bold;
                color: #800080;
                margin: 0px;
              
            }
            QPushButton#tabButton:checked {
                background: #800080; /* Purple background for selected tabs */
                color: white;
                border-bottom: none; /* No bottom border for active tab */
            }
            QPushButton#tabButton:hover {
                background: #CDA8EF; /* Lighter purple on hover */
            }
            QFrame#tabBarFrame {
                background-color: #800080; /* Match the color of the active tab's bottom border */
            }
            QFrame#contentFrame {
                border: 2px solid #800080; /* Purple border around the content frame */
                padding: 0px; /* Remove padding for the content frame */
                margin: 0px; /* Remove margin for the content frame */
                background-color: #fff; /* White background for the content frame */
            }
            #navButtonBar {
                background-color: #800080; /* Purple background for navigation button bar */
                padding: 10px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create tab buttons layout
        tab_button_layout = QHBoxLayout()  # Use QHBoxLayout for full-width tabs

        # Create tab buttons
        self.load_file_tab = QPushButton("Load File", objectName="tabButton")
        self.load_checks_tab = QPushButton("Load Checks", objectName="tabButton")
        self.run_checks_tab = QPushButton("Run Checks", objectName="tabButton")
        self.result_tab = QPushButton("Result", objectName="tabButton")

        # Set checkable to true to simulate active tab
        self.load_file_tab.setCheckable(True)
        self.load_checks_tab.setCheckable(True)
        self.run_checks_tab.setCheckable(True)
        self.result_tab.setCheckable(True)

       

        # Add tab buttons to layout
        tab_button_layout.addWidget(self.load_file_tab)
        tab_button_layout.addWidget(self.load_checks_tab)
        tab_button_layout.addWidget(self.run_checks_tab)
        tab_button_layout.addWidget(self.result_tab)

        # Set alignment to ensure full width
        tab_button_layout.setStretch(0, 1)
        tab_button_layout.setStretch(1, 1)
        tab_button_layout.setStretch(2, 1)
        tab_button_layout.setStretch(3, 1)
        tab_button_layout.setContentsMargins(0, 0, 0, 0)

        # Create a frame to represent the extended bottom border of the active tab
        tab_bar_frame = QFrame()
        tab_bar_frame.setObjectName("tabBarFrame")
        tab_bar_frame.setFixedHeight(10)  # Height of the extended bottom border
        tab_bar_frame.setContentsMargins(0, 0, 0, 0)

        # Create the content frame
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)

        # Remove margins and spacing from the content layout
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Create the tab pages
        self.load_file_page = QWidget(objectName="loadFilePage")
        self.load_checks_page = QWidget(objectName="loadChecksPage")
        self.run_checks_page = QWidget(objectName="runChecksPage")
        self.result_page = QWidget(objectName="resultPage")

        # Stack the pages
        self.pages = QStackedWidget()
        self.pages.addWidget(self.load_file_page)
        self.pages.addWidget(self.load_checks_page)
        self.pages.addWidget(self.run_checks_page)
        self.pages.addWidget(self.result_page)

        content_layout.addWidget(self.pages)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Shazam", alignment=Qt.AlignCenter, objectName="titleBar"))
        main_layout.addLayout(tab_button_layout)
        main_layout.addWidget(tab_bar_frame)
        main_layout.addWidget(content_frame)

        # Add navigation buttons layout with styling
        nav_button_layout = QHBoxLayout()
        nav_button_layout.addStretch()  # Add stretch to push buttons to the right
        self.back_button = QPushButton("Back")
        self.next_button = QPushButton("Next")  # We'll update the label later

        self.back_button.clicked.connect(self.previous_tab)
        self.next_button.clicked.connect(self.next_tab)

        nav_button_layout.addWidget(self.back_button)
        nav_button_layout.addWidget(self.next_button)

        nav_button_bar = QWidget(objectName="navButtonBar")
        nav_button_bar.setLayout(nav_button_layout)

        main_layout.addWidget(nav_button_bar)
        self.central_widget.setLayout(main_layout)

        # Set default active tab
        self.pages.setCurrentIndex(0)

        self.load_file_tab.clicked.connect(lambda: self.set_active_tab(0))
        self.load_checks_tab.clicked.connect(lambda: self.set_active_tab(1))
        self.run_checks_tab.clicked.connect(lambda: self.set_active_tab(2))
        self.result_tab.clicked.connect(lambda: self.set_active_tab(3))

        self.setup_load_file_page()
        self.setup_load_checks_page()
        self.setup_run_checks_page()
        self.setup_result_page()

        self.update_navigation_buttons()

        # Update navigation buttons on tab change
        self.pages.currentChanged.connect(self.update_navigation_buttons)
        
                # Update tab_button_layout and other layouts to remove margins and spacing
        tab_button_layout.setContentsMargins(0, 0, 0, 0)
        tab_button_layout.setSpacing(0)
        
        tab_bar_frame.setContentsMargins(0, 0, 0, 0)
        tab_bar_frame.setStyleSheet("margin: 0px; padding: 0px;")
        
       
        
        # Remove margins and spacing from the content layout
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(0)

        
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        


    def setup_load_file_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Add margins for better spacing
        layout.setSpacing(20)  # Add spacing between widgets
    
        # Add the "Load File" label
        load_file_label = QLabel("Load File")
        load_file_label.setAlignment(Qt.AlignCenter)
        load_file_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(load_file_label)
    
        # Create a placeholder for the load image
        self.load_image = QLabel()
        self.load_image.setPixmap(QPixmap("file.png").scaled(150, 150, Qt.KeepAspectRatio))  # Adjust path and size as needed
        self.load_image.setAlignment(Qt.AlignCenter)
        self.load_image.mousePressEvent = self.load_file  # Make the image clickable
        layout.addWidget(self.load_image, alignment=Qt.AlignCenter)
    
        # Create a placeholder for the remove image (initially hidden)
        self.remove_image = QLabel()
        self.remove_image.setPixmap(QPixmap("document.png").scaled(150, 150, Qt.KeepAspectRatio))  # Adjust path and size as needed
        self.remove_image.setAlignment(Qt.AlignCenter)
        self.remove_image.setVisible(False)  # Initially hidden
        self.remove_image.mousePressEvent = self.remove_file  # Make the image clickable
        layout.addWidget(self.remove_image, alignment=Qt.AlignCenter)
    
        # Placeholder text before loading file
        self.file_placeholder = QLabel("Please import a file to see the output.")
        self.file_placeholder.setAlignment(Qt.AlignCenter)
        self.file_placeholder.setStyleSheet("font-size: 18px; color: grey;")
        layout.addWidget(self.file_placeholder)
    
        # Create a table widget for displaying file data (initially hidden)
        self.file_data_table = QTableWidget()
        self.file_data_table.setColumnCount(0)
        self.file_data_table.setRowCount(0)
        self.file_data_table.setStyleSheet("font-size: 16px;")
        self.file_data_table.setVisible(False)  # Initially hidden
        layout.addWidget(self.file_data_table)
    
        # Create a label for the file name (initially hidden)
        self.file_name_label = QLabel("")
        self.file_name_label.setAlignment(Qt.AlignCenter)
        self.file_name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #800080;")
        self.file_name_label.setVisible(False)  # Initially hidden
        layout.addWidget(self.file_name_label)
    
        self.load_file_page.setLayout(layout)









    from PySide6.QtWidgets import QScrollArea  # Ensure this import is included

    def setup_load_checks_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Add margins for better spacing
        layout.setSpacing(20)  # Add spacing between widgets
    
        # Add the "Select Checks" label
        select_checks_label = QLabel("Select Checks")
        select_checks_label.setAlignment(Qt.AlignCenter)
        select_checks_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(select_checks_label)
    
        # Create a scroll area for the checks
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: white;")  # Set background color to white
    
        # Create a widget to hold the grid layout
        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(10)
        grid_container.setStyleSheet("""
            QWidget {
                border: 1px solid #800080; 
                border-radius: 5px; 
                background-color: white;
            }
            QLabel {
                border: 1px solid #800080; 
                padding: 5px; 
                background-color: #E6E6FA;
            }
        """)  # Add border and background styling to the grid
    
        # Add headers with a single icon for select/deselect all in the third column
        headers = ["Check ID", "Check Description", "select"]
        for col, header in enumerate(headers):
            if col == 2:  # Add an icon in the third column header
                header_widget = QWidget()
                header_layout = QHBoxLayout(header_widget)
                header_layout.setAlignment(Qt.AlignCenter)
                header_label = QLabel(header)
                header_label.setStyleSheet("font-weight: bold; font-size: 18px; padding: 5px; border: 1px solid #800080; background-color: #9932CC; color: white;")
                
                self.toggle_all_icon = QLabel()
                self.select_all_pixmap = QPixmap("selection.png").scaled(20, 20, Qt.KeepAspectRatio)  # Adjust path and size as needed
                self.deselect_all_pixmap = QPixmap("square.png").scaled(20, 20, Qt.KeepAspectRatio)  # Adjust path and size as needed
                
                self.toggle_all_icon.setPixmap(self.select_all_pixmap)
                self.toggle_all_icon.mousePressEvent = self.select_all  # Set initial function to select all
                
                header_layout.addWidget(header_label)
                header_layout.addWidget(self.toggle_all_icon)
                grid_layout.addWidget(header_widget, 0, col)
            else:
                header_label = QLabel(header)
                header_label.setStyleSheet("font-weight: bold; font-size: 18px; padding: 5px; border: 1px solid #800080; background-color: #9932CC; color: white;")
                grid_layout.addWidget(header_label, 0, col)
            
        # Set column stretch factors to adjust widths
        grid_layout.setColumnStretch(0, 1)  
        grid_layout.setColumnStretch(1, 12)  
        grid_layout.setColumnStretch(2, 1)  
        # Store checkboxes for easy access
        self.checkboxes = []
    
        # Populate the grid with sample data
        checks = [("1", "Check 1 Description"), ("2", "Check 2 Description"), ("3", "Check 3 Description"), 
                  ("4", "Check 4 Description"), ("5", "Check 5 Description"), ("6", "Check 6 Description"), 
                  ("7", "Check 7 Description"), ("8", "Check 8 Description"), ("9", "Check 9 Description"), 
                  ("10", "Check 10 Description"), ("11", "Check 11 Description"), ("12", "Check 12 Description"), 
                  ("13", "Check 13 Description"), ("14", "Check 14 Description"), ("15", "Check 15 Description"), 
                  ("16", "Check 16 Description"), ("17", "Check 17 Description"), ("18", "Check 18 Description"), 
                  ("19", "Check 19 Description"), ("20", "Check 20 Description"), ("21", "Check 21 Description"), 
                  ("22", "Check 22 Description"), ("23", "Check 23 Description"), ("24", "Check 24 Description"), 
                  ("25", "Check 25 Description")]
    
        for row, (check_id, check_description) in enumerate(checks, start=1):
            check_id_label = QLabel(check_id)
            check_id_label.setStyleSheet("border: 1px solid #800080; padding: 5px; background-color: #E6E6FA; min-height: 30px;")
            grid_layout.addWidget(check_id_label, row, 0)
            
            description_label = QLabel(check_description)
            description_label.setStyleSheet("padding-left: 10px; border: 1px solid #800080; background-color: #E6E6FA; min-height: 30px;")
            grid_layout.addWidget(description_label, row, 1)
    
            checkbox = QCheckBox()
            checkbox.setStyleSheet("min-height: 40px; margin-left: 10px; padding-left: 5px; border: 1px solid #800080; background-color: white;")
            grid_layout.addWidget(checkbox, row, 2, alignment=Qt.AlignCenter)  # Center-align the checkbox
    
            self.checkboxes.append(checkbox)  # Store the checkbox
    
        # Add the grid container to the scroll area
        scroll_area.setWidget(grid_container)
    
        # Make the scroll area take up all the available space
        layout.addWidget(scroll_area, stretch=1)
    
        self.load_checks_page.setLayout(layout)










  
    def toggle_select_all(self, state):
        if state == Qt.Checked:
            for checkbox in self.checkboxes:
                checkbox.setChecked(True)
        else:
            for checkbox in self.checkboxes:
                checkbox.setChecked(False)





    
    def select_all(self, event):
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)
        self.toggle_all_icon.setPixmap(self.deselect_all_pixmap)  # Change to deselect all icon
        self.toggle_all_icon.mousePressEvent = self.deselect_all  # Change function to deselect all
    
    def deselect_all(self, event):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
        self.toggle_all_icon.setPixmap(self.select_all_pixmap)  # Change to select all icon
        self.toggle_all_icon.mousePressEvent = self.select_all  # Change function to select all



    
    def load_selected_checks(self):
        selected_checks = []
        for row in range(self.checks_table.rowCount()):
            checkbox = self.checks_table.cellWidget(row, 2)
            if checkbox and checkbox.isChecked():
                check_id = self.checks_table.item(row, 0).text()
                check_description = self.checks_table.item(row, 1).text()
                selected_checks.append((check_id, check_description))
        print("Selected Checks:", selected_checks)




    def setup_run_checks_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Add margins for better spacing
        layout.setSpacing(20)  # Add spacing between widgets
    
        # Add the "Run Checks" label
        run_checks_label = QLabel("Run Checks")
        run_checks_label.setAlignment(Qt.AlignCenter)
        run_checks_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(run_checks_label)
    
        # Create a scroll area for the checks
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: white;")  # Set background color to white
    
        # Create a widget to hold the grid layout
        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(10)
        grid_container.setStyleSheet("""
            QWidget {
                border: 1px solid #800080; 
                border-radius: 5px; 
                background-color: white;
            }
            QLabel {
                border: 1px solid #800080; 
                padding: 5px; 
                background-color: #E6E6FA;
            }
        """)  # Add border and background styling to the grid
    
        # Add headers
        headers = ["Check ID", "Check Description", "Status"]
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setStyleSheet("font-weight: bold; font-size: 18px; padding: 5px; border: 1px solid #800080; background-color: #9932CC; color: white;")
            grid_layout.addWidget(header_label, 0, col)
    
        # Set column stretch factors to adjust widths
        grid_layout.setColumnStretch(0, 1)  # Check ID
        grid_layout.setColumnStretch(1, 3)  # Check Description (wider)
        grid_layout.setColumnStretch(2, 1)  # Status
    
        # Sample status options
        status_options = ["Not Started", "In Progress", "Completed"]
    
        # Store checkboxes for easy access
        self.status_labels = []
    
        # Populate the grid with sample data
        checks = [("1", "Check 1 Description"), ("2", "Check 2 Description"), ("3", "Check 3 Description"), 
                  ("4", "Check 4 Description"), ("5", "Check 5 Description"), ("6", "Check 6 Description"), 
                  ("7", "Check 7 Description"), ("8", "Check 8 Description"), ("9", "Check 9 Description"), 
                  ("10", "Check 10 Description"), ("11", "Check 11 Description"), ("12", "Check 12 Description"), 
                  ("13", "Check 13 Description"), ("14", "Check 14 Description"), ("15", "Check 15 Description"), 
                  ("16", "Check 16 Description"), ("17", "Check 17 Description"), ("18", "Check 18 Description"), 
                  ("19", "Check 19 Description"), ("20", "Check 20 Description"), ("21", "Check 21 Description"), 
                  ("22", "Check 22 Description"), ("23", "Check 23 Description"), ("24", "Check 24 Description"), 
                  ("25", "Check 25 Description")]
    
        for row, (check_id, check_description) in enumerate(checks, start=1):
            check_id_label = QLabel(check_id)
            check_id_label.setStyleSheet("border: 1px solid #800080; padding: 5px; background-color: #E6E6FA; min-height: 30px;")
            grid_layout.addWidget(check_id_label, row, 0)
            
            description_label = QLabel(check_description)
            description_label.setStyleSheet("padding-left: 10px; border: 1px solid #800080; background-color: #E6E6FA; min-height: 30px;")
            grid_layout.addWidget(description_label, row, 1)
    
            status_label = QLabel(status_options[0])  # Initial status as "Not Started"
            status_label.setStyleSheet("border: 1px solid #800080; padding: 5px; background-color: #E6E6FA; min-height: 30px;")
            grid_layout.addWidget(status_label, row, 2, alignment=Qt.AlignCenter)  # Center-align the status label
    
            self.status_labels.append(status_label)  # Store the status label
    
        # Add the grid container to the scroll area
        scroll_area.setWidget(grid_container)
    
        # Make the scroll area take up all the available space
        layout.addWidget(scroll_area, stretch=1)
    
        """# Create a layout for the "Run Checks" button
        button_layout = QHBoxLayout()
        run_checks_button = QPushButton("Run Checks")
        run_checks_button.clicked.connect(self.run_checks)
    
        button_layout.addStretch()
        button_layout.addWidget(run_checks_button)
    
        layout.addLayout(button_layout)"""
    
        self.run_checks_page.setLayout(layout)


    
    def setup_result_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Add margins for better spacing
        layout.setSpacing(20)  # Add spacing between widgets
    
        # Add the "Results" label
        results_label = QLabel("Results")
        results_label.setAlignment(Qt.AlignCenter)
        results_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(results_label)
    
        # Create a table widget for displaying the file data
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(0)
        self.result_table.setRowCount(0)
        self.result_table.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.result_table)
    
        # Create a placeholder for the save image
        self.save_image = QLabel()
        self.save_image.setPixmap(QPixmap("save-file.png").scaled(50, 50, Qt.KeepAspectRatio))  # Adjust path and size as needed
        self.save_image.setAlignment(Qt.AlignCenter)
        self.save_image.mousePressEvent = self.save_file  # Make the image clickable
    
        layout.addWidget(self.save_image, alignment=Qt.AlignCenter)
    
        self.result_page.setLayout(layout)

    def display_result_data(self, df):
        self.result_table.setRowCount(0)  # Clear previous content
        self.result_table.setColumnCount(len(df.columns))
        self.result_table.setRowCount(len(df))
        self.result_table.setHorizontalHeaderLabels(df.columns)
        
        for row in range(len(df)):
            for col, (col_name, value) in enumerate(df.iloc[row].items()):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)  # Align text to the top-left
                self.result_table.setItem(row, col, item)
    
        self.result_table.resizeColumnsToContents()
        self.result_table.setWordWrap(True)
        self.result_table.resizeRowsToContents()  # Adjust row height to fit the wrapped text

    
    def save_file(self, event=None):
        if self.df is not None:  # Ensure there is a file loaded
            file_dialog = QFileDialog()
            save_path, _ = file_dialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx *.xls)")
            if save_path:
                self.df.to_excel(save_path, index=False)




    def load_file(self, event=None):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            # Update the file name label
            file_info = QFileInfo(file_path)
            self.file_name_label.setText(f"Loaded File: {file_info.fileName()}")
    
            # Read the Excel file using pandas
            df = pd.read_excel(file_path)
            self.df = df  # Save the data frame to the instance
    
            # Hide placeholder and show table and file name
            self.file_placeholder.hide()
            self.file_data_table.setVisible(True)
            self.file_name_label.setVisible(True)
            self.display_file_data(df.head(10))  # Display only top 10 rows
    
            # Update result page with loaded data
            self.display_result_data(df)
    
            # Hide load image and show remove image
            self.load_image.setVisible(False)
            self.remove_image.setVisible(True)









    
    def display_file_data(self, df):
        self.file_data_table.setRowCount(0)  # Clear previous content
        self.file_data_table.setColumnCount(len(df.columns))
        self.file_data_table.setRowCount(len(df))
        self.file_data_table.setHorizontalHeaderLabels(df.columns)
        self.file_data_table.horizontalHeader().setVisible(True)
        self.file_data_table.verticalHeader().setVisible(True)
    
        for row in range(len(df)):
            for col, (col_name, value) in enumerate(df.iloc[row].items()):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)  # Align text to the top-left
                item.setFlags(item.flags() | Qt.ItemIsEditable)  # Make cell editable if needed
                item.setToolTip(str(value))  # Add tooltip for full text
                self.file_data_table.setItem(row, col, item)
    
        self.file_data_table.resizeColumnsToContents()
    
        # Set word wrap
        self.file_data_table.setWordWrap(True)
        self.file_data_table.resizeRowsToContents()  # Adjust row height to fit the wrapped text








    def remove_file(self, event=None):
        # Remove data table content if it exists
        self.file_data_table.setRowCount(1)
        self.file_data_table.setColumnCount(1)
        self.file_data_table.setItem(0, 0, QTableWidgetItem("Please import a file to see the output."))
        self.file_data_table.horizontalHeader().setVisible(False)
        self.file_data_table.verticalHeader().setVisible(False)
        self.file_data_table.setVisible(False)  # Hide the table initially
    
        # Reset DataFrame
        self.df = None
    
        # Reset file name label
        self.file_name_label.setText("")
        self.file_name_label.setVisible(False)
    
        # Show the placeholder
        self.file_placeholder.setVisible(True)
    
        # Show load image and hide remove image
        self.load_image.setVisible(True)
        self.remove_image.setVisible(False)











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

    def set_active_tab(self, index):
        self.pages.setCurrentIndex(index)
        self.load_file_tab.setChecked(index == 0)
        self.load_checks_tab.setChecked(index == 1)
        self.run_checks_tab.setChecked(index == 2)
        self.result_tab.setChecked(index == 3)
        self.update_navigation_buttons()  # Ensure navigation buttons are updated

 
    def update_navigation_buttons(self):
        current_index = self.pages.currentIndex()
        self.back_button.setEnabled(current_index > 0)
        next_tab_text = ["Load Checks", "Run Checks", "Result", ""]  # Last tab has no next tab
        if current_index < len(next_tab_text) - 1:
            self.next_button.setText(next_tab_text[current_index])
        else:
            self.next_button.setText("Next")
        self.next_button.setEnabled(current_index < self.pages.count() - 1)

 
    def previous_tab(self):
        current_index = self.pages.currentIndex()
        if current_index > 0:
            self.set_active_tab(current_index - 1)
    
    def next_tab(self):
        current_index = self.pages.currentIndex()
        if current_index < self.pages.count() - 1:
            self.set_active_tab(current_index + 1)








    
    
    def clear_all_checks(self):
        for check in self.checks_type1 + self.checks_type2:
            check.setChecked(False)

   



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
