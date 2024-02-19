// chart.js

if(!window.CandlestickChart)
{
    class CandlestickChart {
        constructor(chartContainerId) {
            this.chartContainerId = chartContainerId;
            this.chart = null;
            this.series = null;
        }
    
        createChart(width, height, data) {
            // Check if chart and series already exist
            if (!this.chart || !this.series) {
                // Create a new chart if not exists
                this.chart = LightweightCharts.createChart(document.getElementById(this.chartContainerId), {
                    width: width,
                    height: height
                });
    
                this.series = this.chart.addCandlestickSeries({ color: 'rgb(0, 120, 255)', lineWidth: 2 });
            }
    
            // Update the series data
            this.series.setData(data);
        }
    }

    window.CandlestickChart = CandlestickChart;
}

