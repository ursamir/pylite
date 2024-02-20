// chart.js

if (!window.Chart) {
    class Chart {
        constructor(chartContainerId) {
            this.chartContainerId = chartContainerId;
            this.chart = null;
            this.CandlestickSeries = null;
            this.LineSeriesList = [];
            this.VolumeSeries = null;
            this.legend = null; // Legend HTML element
            this.Symbol = null;
        }

        createChart(width, height) {
            if (!this.chart) {
                this.chart = LightweightCharts.createChart(
                    document.getElementById(this.chartContainerId),
                    {
                        width: width,
                        height: height,
                        layout: {
                            textColor: '#d8d9db',
                            background: {
                                color: '#001B1B',
                                type: LightweightCharts.ColorType.Solid,
                            },
                            fontSize: 12,
                        },
                        autoSize: true,
                        rightPriceScale: {
                            scaleMargins: { top: 0, bottom: 0 },
                        },
                        timeScale: {
                            timeVisible: true,
                            secondsVisible: false,
                        },
                        crosshair: {
                            mode: LightweightCharts.CrosshairMode.Normal,
                            vertLine: {
                                labelBackgroundColor: 'rgb(46, 46, 46)',
                            },
                            horzLine: {
                                labelBackgroundColor: 'rgb(55, 55, 55)',
                            },
                        },
                        grid: {
                            vertLines: { color: 'rgba(29, 30, 38, 5)' },
                            horzLines: { color: 'rgba(29, 30, 58, 5)' },
                        },
                        handleScroll: { vertTouchDrag: true },
                    }
                );

                this.chart.subscribeCrosshairMove(this.updateLegend.bind(this));
            }
        }

        addCandlestickSeries(Symbol,data) {
            // Check if a series already exists and remove it if it does
            this.removeCandlestickSeries();

            this.Symbol = Symbol; // Set Symbol;
            this.CandlestickSeries = this.chart.addCandlestickSeries({
                color: 'rgb(0, 120, 255)',
                lineWidth: 2,
            });

            this.CandlestickSeries.setData(data);
        }

        removeCandlestickSeries() {
            if (this.CandlestickSeries) {
                this.chart.removeSeries(this.CandlestickSeries);
                this.CandlestickSeries = null;
            }
        }

        addVolumeSeries(data, value_name) {
            // Check if a series already exists and remove it if it does
            this.removeVolumeSeries();

            this.VolumeSeries = this.chart.addHistogramSeries({
                priceFormat: { type: 'volume' },
                priceScaleId: '',
            });

            this.VolumeSeries.setData(
                data.map((d) => ({
                    time: d.time,
                    value: d[value_name],
                    color: d.close > d.open ? '#26a69aaa' : '#ef5350aa',
                }))
            );
        }

        removeVolumeSeries() {
            if (this.VolumeSeries) {
                this.chart.removeSeries(this.VolumeSeries);
                this.VolumeSeries = null;
            }
        }

        addLineSeries(lineStyleOptions, data, value_name, title) {
            const defaultOptions = {
                color: '#ffffffaa',
                lineWidth: 1,
                lineType: 0,
                lineStyle: LightweightCharts.LineStyle.Solid,
                lineVisible: true,
                pointMarkersVisible: false,
                pointMarkersRadius: undefined,
                crosshairMarkerVisible: true,
                crosshairMarkerRadius: 4,
                crosshairMarkerBorderColor: '',
                crosshairMarkerBackgroundColor: '',
                crosshairMarkerBorderWidth: 2,
                lastPriceAnimation: LightweightCharts.LastPriceAnimationMode.Disabled,
            };
        
            // Merge default options with provided options
            const options = {...defaultOptions, ...lineStyleOptions};
            const lineSeries = this.chart.addLineSeries(options);
            lineSeries.title = title; // Store the title
        
            lineSeries.setData(
                data.map((d) => ({
                    time: d.time,
                    value: d[value_name],
                }))
            );
        
            this.LineSeriesList.push(lineSeries);
        }        

        removeLineSeries() {
            this.LineSeriesList.forEach((lineSeries) => {
                this.chart.removeSeries(lineSeries);
            });
            this.LineSeriesList = [];
        }

        createLegend() {
            // Check if a legend already exists
            if (!this.legend) {
                // Create a legend HTML element and position it
                const container = document.getElementById(this.chartContainerId);
                this.legend = document.createElement('div');
                this.legend.style = `
                    position: absolute;
                    left: 12px;
                    top: 12px;
                    z-index: 1;
                    font-size: 14px;
                    font-family: sans-serif;
                    line-height: 18px;
                    font-weight: 300;
                    color: white; // Set legend text color
                `;
                container.appendChild(this.legend);
            }
        }

        addLegendEntry(name, color) {
            // Add an entry to the legend
            const legendEntry = document.createElement('div');
            legendEntry.innerHTML = name;
            legendEntry.style.color = color;
            this.legend.appendChild(legendEntry);
        }

        updateLegend(param) {
            // Check if legend exists proceed else do nothing
            if (!this.legend) {
                return;
            }
            
            const validCrosshairPoint = !(
                param === undefined || param.time === undefined || param.point.x < 0 || param.point.y < 0
            );
            
            if (validCrosshairPoint) {
                const olhc = param.seriesData.get(this.CandlestickSeries);
                
                const time = new Date(olhc.time * 1000).toUTCString().slice(4, -4);
                const open = olhc.open.toFixed(2);
                const high = olhc.high.toFixed(2);
                const low = olhc.low.toFixed(2);
                const close = olhc.close.toFixed(2);

                const volume = param.seriesData.get(this.VolumeSeries).value.toFixed(2);

                const lineSeriesData = this.LineSeriesList.map((lineSeries) => {
                    const lineData = param.seriesData.get(lineSeries);
                    return `${lineSeries.title}: ${lineData.value.toFixed(2)}`;
                });

                const legendText = `
                    <div style="font-size: 18px; margin: 4px 0px;"> ${this.Symbol} : ${time}</div>
                    <div>Open: ${open} High: ${high} Low: ${low} Close: ${close} Volume: ${volume}</div>
                    <div>${lineSeriesData.join(', ')}</div>
                `;
                
                this.legend.innerHTML = legendText;
            } else {
                this.legend.innerHTML = ""; // Clear legend if no valid data
            }
        }

        removeLegend() {
            if (this.legend) {
                this.legend.remove();
                this.legend = null;
            }
        }
        
        createCandlestickChartWithData(width, height, Symbol,data) {
            this.createChart(width, height);
            this.addCandlestickSeries(Symbol,data);
            this.CandlestickSeries.priceScale().applyOptions({
                scaleMargins: { top: 0.2, bottom: 0.21 },
            });
            this.addVolumeSeries(data, 'volume');
            this.VolumeSeries.priceScale().applyOptions({
                scaleMargins: { top: 0.8, bottom: 0 },
            });
            this.removeLineSeries();
            this.addLineSeries({ color: '#ffffffaa', lineWidth: 1 }, data, 'close','Line1');
            this.addLineSeries({ color: '#ffffffaa', lineWidth: 1 }, data, 'open','Line2');

            // clear legend if it exists
            this.removeLegend();
            this.createLegend();
        }
    }

    window.Chart = Chart;
}
