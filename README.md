# Pylite Chart Library

Pylite is a lightweight Python library for creating interactive and customizable charts. It is designed to be easy to use while providing powerful charting capabilities. This library is particularly suitable for financial charting applications.

## Installation

You can install `pylitechart` using `pip`:

```bash
pip install pylitechart
```

# ChartWidget Methods - Details

The `ChartWidget` class in the `pylite` library provides methods for creating, modifying, and removing financial charts. Below is an overview of key methods available in the `ChartWidget` class.

## Main Chart Methods

### `mainChart_addCandlestickSeries(symbol, data)`

Adds a candlestick series to the main chart.

- **Parameters:**
  - `symbol` (str): Stock symbol (e.g., "AAPL").
  - `data` (pandas.DataFrame): Historical stock data.

### `mainChart_removeCandlestickSeries()`

Removes the candlestick series from the main chart.

### `mainChart_addVolumeSeries()`

Adds a volume series to the main chart.

### `mainChart_removeVolumeSeries()`

Removes the volume series from the main chart.

### `mainChart_addLineSeries(data, value_name, title, ...)`

Adds a line series to the main chart.

- **Parameters:**
  - `data` (pandas.DataFrame): Data for the line series.
  - `value_name` (str): Name of the value column.
  - `title` (str): Title of the line series.
  - Additional optional parameters for line appearance and behavior.

### `mainChart_removeLineSeries(title)`

Removes a line series from the main chart.

- **Parameters:**
  - `title` (str): Title of the line series to be removed.

## Subchart Methods

### `addSubChart()`

Adds a new subchart to the main chart.

### `removeSubChart(subchart_id)`

Removes a subchart from the main chart.

- **Parameters:**
  - `subchart_id` (str): ID of the subchart to be removed.

### `subChart_addCandlestickSeries(subchart_id)`

Adds a candlestick series to a subchart.

### `subChart_removeCandlestickSeries(subchart_id)`

Removes the candlestick series from a subchart.

### `subChart_addVolumeSeries(subchart_id)`

Adds a volume series to a subchart.

### `subChart_removeVolumeSeries(subchart_id)`

Removes the volume series from a subchart.

### `subChart_addLineSeries(subchart_id, data, value_name, title, ...)`

Adds a line series to a subchart.

- **Parameters:**
  - `subchart_id` (str): ID of the subchart.
  - `data` (pandas.DataFrame): Data for the line series.
  - `value_name` (str): Name of the value column.
  - `title` (str): Title of the line series.
  - Additional optional parameters for line appearance and behavior.

### `subChart_removeLineSeries(subchart_id, title)`

Removes a line series from a subchart.

- **Parameters:**
  - `subchart_id` (str): ID of the subchart.
  - `title` (str): Title of the line series to be removed.

## Other Methods

### `runJs(script)`

Executes JavaScript code within the web view.

- **Parameters:**
  - `script` (str): JavaScript code to be executed.

### `convert_data_to_js_format(stock_data)`

Converts historical stock data to a JavaScript-friendly format.

- **Parameters:**
  - `stock_data` (pandas.DataFrame): Historical stock data.


# EXAMPLE
Use the `example.py` as a reference to test the features of `pylitechart` library.

---
This README provides a brief overview of the key methods available in the `ChartWidget` class. Refer to the source code and official documentation for detailed information on parameters and usage.
