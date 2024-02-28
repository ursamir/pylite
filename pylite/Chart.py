# Chart.py
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
import os
from datetime import datetime
from dateutil import tz
import uuid
from enum import Enum

class LineStyle(Enum):
    Solid = 0
    Dotted = 1
    Dashed = 2
    LargeDashed = 3
    SparseDotted = 4

class LastPriceAnimationMode(Enum):
    Disabled = 0
    Continuous = 1
    OnDataUpdate = 2

def convert_data_to_js_format(stock_data):
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

class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the web view
        self.webview = QWebEngineView()

        # Load the HTML file
        script_dir = os.path.dirname(os.path.realpath(__file__))
        html_file_path = os.path.join(script_dir, "scripts", "lightweight_chart.html")
        self.webview.load(QUrl.fromLocalFile(html_file_path))

        # Connect the loadFinished signal to onPageLoadFinished
        self.webview.loadFinished.connect(self._onPageLoadFinished)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.webview)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.subCharts = []

    def _onPageLoadFinished(self):
        _script = f"""
            const mainChart = new window.ParentChart('main-chart',800,600);
        """
        self.runJs(_script)

    def runJs(self, script):
        # Execute the JavaScript code
        self.webview.page().runJavaScript(script)

    def mainChart_addCandlestickSeries(self,symbol,data):
        self.width = self.webview.width()
        self.height = self.webview.height()
        self.data = data
        self.symbol = symbol
        # Convert stock data to JavaScript-friendly format
        self.js_data = convert_data_to_js_format(self.data)

        _script = f"""
            mainChart.addCandlestickSeries('{self.symbol}',{self.js_data});
        """
        self.runJs(_script)

    def mainChart_removeCandlestickSeries(self):
        _script = f"""
            mainChart.removeCandlestickSeries();
        """
        self.runJs(_script)

    def mainChart_addVolumeSeries(self):
        _script = f"""
            mainChart.CandlestickSeries.priceScale().applyOptions({{
                scaleMargins: {{ top: 0.1, bottom: 0.21 }},
            }});
            mainChart.addVolumeSeries({self.js_data}, 'volume');
            mainChart.VolumeSeries.priceScale().applyOptions({{
                scaleMargins: {{ top: 0.8, bottom: 0 }},
            }});
        """
        self.runJs(_script)

    def mainChart_removeVolumeSeries(self):
        _script = f"""
            mainChart.removeVolumeSeries();
            mainChart.CandlestickSeries.priceScale().applyOptions({{
                scaleMargins: {{ top: 0.1, bottom: 0.0 }},
            }});
        """
        self.runJs(_script)

    def mainChart_addLineSeries(self, 
                                data, 
                                value_name, 
                                title,
                                color = '#ffffffaa',
                                line_width = 1,
                                line_type = 0,
                                line_style = LineStyle.Solid.value,
                                line_visible = True,
                                point_markers_visible = False,
                                crosshair_marker_visible = True,
                                crosshair_marker_radius = 4,
                                crosshair_marker_border_color = '',
                                crosshair_marker_background_color = '',
                                crosshair_marker_border_width = 2,
                                last_price_animation = LastPriceAnimationMode.Disabled.value
                                ):
        
        js_data = convert_data_to_js_format(data)

        _script = f"""
            lineOptions = {{
                color: '{color}',
                lineWidth: {line_width},
                lineType: {line_type},
                lineStyle: {line_style},
                lineVisible: {str(line_visible).lower()},  
                pointMarkersVisible: {str(point_markers_visible).lower()}, 
                pointMarkersRadius: undefined,
                crosshairMarkerVisible: {str(crosshair_marker_visible).lower()}, 
                crosshairMarkerRadius: {crosshair_marker_radius},
                crosshairMarkerBorderColor: '{crosshair_marker_border_color}',
                crosshairMarkerBackgroundColor: '{crosshair_marker_background_color}',
                crosshairMarkerBorderWidth: {crosshair_marker_border_width},
                lastPriceAnimation: {last_price_animation},
            }};
            mainChart.addLineSeries({js_data}, '{value_name}', '{title}', lineOptions);
        """
        self.runJs(_script)

    def mainChart_removeLineSeries(self,title):
        _script = f"""
            mainChart.removeLineSeries('{title}');
        """
        self.runJs(_script)

    def addSubChart(self):
        subchart_id = f'sub_chart_{uuid.uuid4().hex}'
        _script = f"""
            let {subchart_id} = mainChart.addSubChart('{subchart_id}', {self.width}, {self.height});
            
        """
        self.runJs(_script)
        self.subCharts.append(subchart_id)
        return subchart_id

    def removeSubChart(self, subchart_id):
        if subchart_id in self.subCharts:
            # Remove the subchart from the list
            self.subCharts.remove(subchart_id)

            # Remove the subchart in JavaScript
            _script = f"""
                mainChart.removeSubChart({subchart_id});
            """
            self.runJs(_script)

    def subChart_addCandlestickSeries(self,subchart_id):
        _script = f"""
            {subchart_id}.addCandlestickSeries('{self.symbol}',{self.js_data});
        """
        self.runJs(_script)

    def subChart_removeCandlestickSeries(self,subchart_id):
        _script = f"""
            {subchart_id}.removeCandlestickSeries();
        """
        self.runJs(_script)

    def subChart_addVolumeSeries(self,subchart_id):
        _script = f"""
            {subchart_id}.CandlestickSeries.priceScale().applyOptions({{
                scaleMargins: {{ top: 0.1, bottom: 0.21 }},
            }});
            {subchart_id}.addVolumeSeries({self.js_data}, 'volume');
            {subchart_id}.VolumeSeries.priceScale().applyOptions({{
                scaleMargins: {{ top: 0.8, bottom: 0 }},
            }});
        """
        self.runJs(_script)

    def subChart_removeVolumeSeries(self,subchart_id):
        _script = f"""
            {subchart_id}.removeVolumeSeries();
            {subchart_id}.CandlestickSeries.priceScale().applyOptions({{
                scaleMargins: {{ top: 0.1, bottom: 0.0 }},
            }});
        """
        self.runJs(_script)

    def subChart_addLineSeries(self,subchart_id, 
                                data, 
                                value_name, 
                                title,
                                color = '#ffffffaa',
                                line_width = 1,
                                line_type = 0,
                                line_style = LineStyle.Solid.value,
                                line_visible = True,
                                point_markers_visible = False,
                                crosshair_marker_visible = True,
                                crosshair_marker_radius = 4,
                                crosshair_marker_border_color = '',
                                crosshair_marker_background_color = '',
                                crosshair_marker_border_width = 2,
                                last_price_animation = LastPriceAnimationMode.Disabled.value
                                ):
        
        js_data = convert_data_to_js_format(data)

        _script = f"""
            lineOptions = {{
                color: '{color}',
                lineWidth: {line_width},
                lineType: {line_type},
                lineStyle: {line_style},
                lineVisible: {str(line_visible).lower()},  
                pointMarkersVisible: {str(point_markers_visible).lower()}, 
                pointMarkersRadius: undefined,
                crosshairMarkerVisible: {str(crosshair_marker_visible).lower()}, 
                crosshairMarkerRadius: {crosshair_marker_radius},
                crosshairMarkerBorderColor: '{crosshair_marker_border_color}',
                crosshairMarkerBackgroundColor: '{crosshair_marker_background_color}',
                crosshairMarkerBorderWidth: {crosshair_marker_border_width},
                lastPriceAnimation: {last_price_animation},
            }};
            {subchart_id}.addLineSeries({js_data}, '{value_name}', '{title}', lineOptions);
        """
        self.runJs(_script)

    def subChart_removeLineSeries(self,subchart_id,title):
        _script = f"""
            {subchart_id}.removeLineSeries('{title}');
        """
        self.runJs(_script)
