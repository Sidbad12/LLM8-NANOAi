from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QListWidget, QPushButton, 
                             QLabel, QHBoxLayout, QFileDialog, QInputDialog,
                             QMessageBox,QListWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class ModelManagerDialog(QDialog):
    def __init__(self, model_manager, parent=None):
        super().__init__(parent)
        self.model_manager = model_manager
        self.setup_ui()
        self.load_models()
    
    def setup_ui(self):
        self.setWindowTitle("Model Management")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e293b;
            }
            QLabel {
                color: #e2e8f0;
                font-weight: bold;
            }
            QListWidget {
                background-color: #334155;
                color: #f1f5f9;
                border: 1px solid #475569;
                border-radius: 4px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("AI Model Management")
        title.setStyleSheet("font-size: 16px; color: #3b82f6;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Model list
        layout.addWidget(QLabel("Available Models:"))
        self.model_list = QListWidget()
        layout.addWidget(self.model_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Model")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.add_btn.clicked.connect(self.add_model)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #64748b;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """)
        self.close_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
         # Add status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
        layout.insertWidget(2, self.status_label)
        
        # Connect selection change
        self.model_list.currentItemChanged.connect(self.on_model_selected)
    
    def on_model_selected(self, current, previous):
        if current:
            model_name = current.text()
            is_available = self.model_manager.is_model_available(model_name)
            status = "Available" if is_available else "Missing "
            self.status_label.setText(f"Status: {status}")
    
    def load_models(self):
        self.model_list.clear()
        for model in self.model_manager.get_model_list():
            item = QListWidgetItem(model)
            
            # Color code based on availability
            if self.model_manager.is_model_available(model):
                item.setForeground(QColor('#4ade80'))  # Green for available
            else:
                item.setForeground(QColor('#ef4444'))  # Red for missing
            
            self.model_list.addItem(item)
    
    def add_model(self):
        model_path = QFileDialog.getExistingDirectory(self, "Select Model Directory")
        if model_path:
            model_name, ok = QInputDialog.getText(self, "Model Name", "Enter a name for this model:")
            if ok and model_name:
                try:
                    if self.model_manager.add_custom_model(model_name, model_path):
                        self.load_models()
                        QMessageBox.information(self, "Success", f"Model '{model_name}' added successfully!")
                    else:
                        QMessageBox.warning(self, "Error", "Failed to add model.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error adding model: {str(e)}")