from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
import yfinance as yf
import pandas as pd
import os

class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.webview = QWebEngineView()

        # Load the HTML file
        script_dir = os.path.dirname(os.path.realpath(__file__))
        html_file_path = os.path.join(script_dir, "scripts", "lightweight_chart.html")
        self.webview.load(QUrl.fromLocalFile(html_file_path))

        custom_script_path = os.path.join(script_dir, "scripts", "chart.js")
        with open(custom_script_path, 'r') as custom_script_file:
            self.custom_script_content = custom_script_file.read()

        # Connect the loadFinished signal to onPageLoadFinished
        self.webview.loadFinished.connect(self.onPageLoadFinished)

        layout = QVBoxLayout(self)
        layout.addWidget(self.webview)

        self.width = 800
        self.height = 600

    def onPageLoadFinished(self):
        # Do nothing on page load finished
        self.runJs(self.custom_script_content)

    def createChart(self, stock_data):
        # Convert stock data to JavaScript-friendly format
        js_data = self.convert_data_to_js_format(stock_data)

        chart_script = f"""
            const myChart = new window.CandlestickChart('chart-container');
            myChart.createChart({self.width}, {self.height}, {js_data});
        """
        self.runJs(chart_script)

    def runJs(self, script):
        # Execute the JavaScript code
        self.webview.page().runJavaScript(script)

    def convert_data_to_js_format(self, stock_data):
        # Convert stock data to a list of dictionaries in JavaScript format
        js_data = []
        for index, row in stock_data.iterrows():
            time = index.strftime('%Y-%m-%d')
            open_price = row['Open']
            low_price = row['Low']
            high_price = row['High']
            close_price = row['Close']
            volume = row['Volume']

            js_data.append({
                'time': time,
                'open': open_price,
                'low': low_price,
                'high': high_price,
                'close': close_price,
                'volume': volume
            })
        return js_data


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

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def create_chart_with_symbol(self):
        stock_symbol = self.symbol_input.text()  # Get symbol from input
        stock_data = self.fetch_stock_data(stock_symbol)
        self.chart_widget.createChart(stock_data)

    def fetch_stock_data(self, symbol, period="3mo"):
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
