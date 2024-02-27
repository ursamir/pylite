# app.py
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
import yfinance as yf
import pandas as pd
import os
from Chart import ChartWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chart_widget = ChartWidget(self)

        self.button = QPushButton("Create Chart")
        self.symbol_input = QLineEdit("TCS.NS")  # Default symbol
        self.button.clicked.connect(self.create_chart_with_symbol)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_widget)
        layout.addWidget(self.symbol_input)
        layout.addWidget(self.button)

        self.create_subchart_button = QPushButton("Create Subchart")
        self.create_subchart_button.clicked.connect(self.create_subchart)
        layout.addWidget(self.create_subchart_button)

        self.remove_subchart_button = QPushButton("Remove Subchart")
        self.remove_subchart_button.clicked.connect(self.remove_subchart)
        layout.addWidget(self.remove_subchart_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.subchart = []

    def create_chart_with_symbol(self):
        stock_symbol = self.symbol_input.text()  # Get symbol from input
        stock_data = self.fetch_stock_data2(stock_symbol)
        self.chart_widget.createCandlestickChartWithData(stock_symbol,stock_data)

    def create_subchart(self):
        self.subchart.append(self.chart_widget.addSubChart())

    def remove_subchart(self):
        if len(self.subchart) > 0:
            self.chart_widget.removeSubChart(self.subchart.pop(0))

    def fetch_stock_data1(self, symbol, period="1mo"):
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data
    def fetch_stock_data2(self, symbol, period="7d"):
        data = yf.download(symbol,period=period,interval='1m')
        return data


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
