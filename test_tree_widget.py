"""
Quick GUI test to verify tree widget display
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

def test_tree_widget():
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("Tree Widget Test")
    window.setGeometry(100, 100, 600, 400)
    
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout()
    central_widget.setLayout(layout)
    
    # Create tree widget with two columns
    tree = QTreeWidget()
    tree.setHeaderLabels(["Property", "Value"])
    tree.setColumnWidth(0, 300)
    
    # Add test data
    cpu_item = QTreeWidgetItem(tree, ["CPU Information", ""])
    QTreeWidgetItem(cpu_item, ["Name", "Intel Core i7-1165G7"])
    QTreeWidgetItem(cpu_item, ["Cores Physical", "4"])
    QTreeWidgetItem(cpu_item, ["Cores Logical", "8"])
    QTreeWidgetItem(cpu_item, ["Frequency Current", "2803.0 MHz"])
    
    memory_item = QTreeWidgetItem(tree, ["Memory Information", ""])
    QTreeWidgetItem(memory_item, ["Total", "15.56 GB"])
    QTreeWidgetItem(memory_item, ["Available", "2.99 GB"])
    QTreeWidgetItem(memory_item, ["Used", "12.57 GB"])
    QTreeWidgetItem(memory_item, ["Percentage", "80.8%"])
    
    tree.expandAll()
    layout.addWidget(tree)
    
    window.show()
    print("Tree widget test window opened. Check if Property and Value columns are visible.")
    print("You should see hardware information with proper property-value pairs.")
    
    return app.exec()

if __name__ == "__main__":
    test_tree_widget()