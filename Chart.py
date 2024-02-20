
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
import os
from datetime import datetime
from dateutil import tz

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
            self.load_script = custom_script_file.read()

        # Connect the loadFinished signal to onPageLoadFinished
        self.webview.loadFinished.connect(self._onPageLoadFinished)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.webview)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def _onPageLoadFinished(self):
        # Do nothing on page load finished
        self.runJs(self.load_script)
        chart_script = f"""
            const myChart = new window.Chart('chart-container');
        """
        self.runJs(chart_script)

    def _convert_data_to_js_format(self, stock_data):
        # Specify the desired timezone
        local_timezone = tz.gettz('Asia/Kolkata')  # Change 'Asia/Kolkata' to your desired timezone

        # Convert stock data to a list of dictionaries in JavaScript format
        js_data = []
        for index, row in stock_data.iterrows():
            t_utc = int(index.timestamp()) 
            # Get the UTC offset dynamically based on the local timezone
            local_time = datetime.fromtimestamp(t_utc, tz=local_timezone)
            utc_offset = local_time.utcoffset().total_seconds()

            # Add the timezone offset to the UTC timestamp
            t_local = t_utc + utc_offset

            o = row['Open']
            l = row['Low']
            h = row['High']
            c = row['Close']
            v = row['Volume']

            js_data.append({'time': t_local, 'open': o, 'low': l, 'high': h, 'close': c, 'volume': v})
        return js_data

    def runJs(self, script):
        # Execute the JavaScript code
        self.webview.page().runJavaScript(script)

    def createCandlestickChartWithData(self,symbol,data):
        self.width = self.webview.width()
        self.height = self.webview.height()
        self.data = data
        self.symbol = symbol
        # Convert stock data to JavaScript-friendly format
        self.js_data = self._convert_data_to_js_format(self.data)

        chart_script = f"""
            myChart.createCandlestickChartWithData({self.width}, {self.height}, '{self.symbol}',{self.js_data});
        """
        self.runJs(chart_script)

