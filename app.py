# app.py
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit,QGridLayout
import yfinance as yf
from Chart import ChartWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chart_widget = ChartWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_widget)

        glayout = QGridLayout()
        self.symbol_input = QLineEdit("TCS.NS")  # Default symbol
        glayout.addWidget(self.symbol_input, 0, 0)

        self.create_chart_button = QPushButton("Create Main Chart")
        self.create_chart_button.clicked.connect(self.create_main_chart_with_symbol)
        glayout.addWidget(self.create_chart_button, 0, 1)

        self.remove_chart_button = QPushButton("Remove Main Chart")
        self.remove_chart_button.clicked.connect(self.remove_main_chart)
        glayout.addWidget(self.remove_chart_button, 0, 2)

        self.create_subchart_button = QPushButton("Create Subchart")
        self.create_subchart_button.clicked.connect(self.create_subchart)
        glayout.addWidget(self.create_subchart_button, 0, 3)

        self.remove_subchart_button = QPushButton("Remove Subchart")
        self.remove_subchart_button.clicked.connect(self.remove_subchart)
        glayout.addWidget(self.remove_subchart_button, 0, 4)

        self.create_main_chart_line_button = QPushButton("Create Main Chart Line")
        self.create_main_chart_line_button.clicked.connect(self.create_main_chart_line)
        glayout.addWidget(self.create_main_chart_line_button, 0, 5)

        self.remove_main_chart_line_button = QPushButton("Remove Main Chart Line")
        self.remove_main_chart_line_button.clicked.connect(self.remove_main_chart_line)
        glayout.addWidget(self.remove_main_chart_line_button, 0, 6)

        self.create_subchart_line_button = QPushButton("Create Subchart Line")
        self.create_subchart_line_button.clicked.connect(self.create_subchart_line)
        glayout.addWidget(self.create_subchart_line_button, 0, 7)

        self.remove_subchart_line_button = QPushButton("Remove Subchart Line")
        self.remove_subchart_line_button.clicked.connect(self.remove_subchart_line)
        glayout.addWidget(self.remove_subchart_line_button, 0, 8)

        layout.addLayout(glayout)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.subcharts = []

    def create_main_chart_with_symbol(self):
        self.stock_symbol = self.symbol_input.text()
        self.stock_data = self.fetch_stock_data2(self.stock_symbol)
        self.chart_widget.mainChart_addCandlestickSeries(self.stock_symbol, self.stock_data)

    def remove_main_chart(self):
        self.chart_widget.mainChart_removeCandlestickSeries()

    def create_main_chart_line(self):
        self.chart_widget.mainChart_addLineSeries(self.stock_data, "close", "Main Chart Line")

    def remove_main_chart_line(self):
        self.chart_widget.mainChart_removeLineSeries("Main Chart Line")
        pass

    def create_subchart(self):
        subchart_id = self.chart_widget.addSubChart()
        self.chart_widget.subChart_addCandlestickSeries(subchart_id)
        self.subcharts.append(subchart_id)

    def remove_subchart(self):
        if self.subcharts:
            subchart_id = self.subcharts.pop(0)
            self.chart_widget.removeSubChart(subchart_id)

    def create_subchart_line(self):
        if self.subcharts:
            subchart_id = self.subcharts[0] 
            self.chart_widget.subChart_addLineSeries(subchart_id, self.stock_data, "close", "Subchart Line")

    def remove_subchart_line(self):
        if self.subcharts:
            subchart_id = self.subcharts[0]  # For simplicity, using the first subchart
            self.chart_widget.subChart_removeLineSeries(subchart_id,"Subchart Line")

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
