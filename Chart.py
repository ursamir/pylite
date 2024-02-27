# Chart.py
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
import os
from datetime import datetime
from dateutil import tz
import uuid

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
        
        self.subCharts = []
        

    def _onPageLoadFinished(self):
        chart_script = f"""
            const mainChart = new window.ParentChart('main-chart',800,600);
        """
        self.runJs(chart_script)

    def _convert_data_to_js_format(self, stock_data):
        local_timezone = tz.gettz('Asia/Kolkata') 

        js_data = []
        for index, row in stock_data.iterrows():
            t_utc = int(index.timestamp()) 
            local_time = datetime.fromtimestamp(t_utc, tz=local_timezone)
            utc_offset = local_time.utcoffset().total_seconds()

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
            mainChart.addCandlestickSeries('{self.symbol}',{self.js_data});
        """
        self.runJs(chart_script)

    
    def addSubChart(self, data = None ,symbol = None):
        if data is not None:
            self.data = data
        if symbol is not None:
            self.symbol = symbol
        self.width = self.webview.width()
        self.height = self.webview.height()
        # Convert stock data to JavaScript-friendly format
        self.js_data = self._convert_data_to_js_format(self.data)

        subchart_id = f'sub_chart_{uuid.uuid4().hex}'

        chart_script = f"""
            let {subchart_id} = mainChart.addSubChart('{subchart_id}', {self.width}, {self.height});
            {subchart_id}.addCandlestickSeries('{self.symbol}',{self.js_data});
        """
        self.runJs(chart_script)

        self.subCharts.append(subchart_id)

        return subchart_id

    def removeSubChart(self, subchart_id):
        if subchart_id in self.subCharts:
            # Remove the subchart from the list
            self.subCharts.remove(subchart_id)

            # Remove the subchart in JavaScript
            chart_script = f"""
                mainChart.removeSubChart({subchart_id});
            """
            self.runJs(chart_script)