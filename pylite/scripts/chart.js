// chart.js

if (!window.CrosshairManager) {
    const CrosshairManager = {
        charts: [],

        subscribeChart(chart) {
            this.charts.push(chart);
            chart.legend.createLegend();
            this.syncChartsTimeScale();
            this.syncChartsCrosshairMove();
        },

        unsubscribeChart(chart) {
            this.charts = this.charts.filter(c => c !== chart);
        },

        syncChartsTimeScale() {
            this.charts.forEach((chart1, index1) => {
                this.charts.forEach((chart2, index2) => {
                    if (index1 !== index2) {
                        chart1.chart.timeScale().subscribeVisibleLogicalRangeChange(timeRange => {
                            chart2.chart.timeScale().setVisibleLogicalRange(timeRange);
                        });
                        chart2.chart.timeScale().subscribeVisibleLogicalRangeChange(timeRange => {
                            chart1.chart.timeScale().setVisibleLogicalRange(timeRange);
                        });
                    }
                });
            });
        },

        syncChartsCrosshairMove() {
            this.charts.forEach((chart1, index1) => {
                this.charts.forEach((chart2, index2) => {
                    if (index1 !== index2) {
                        chart1.chart.subscribeCrosshairMove(param => {
                            const dataPoint = getCrosshairDataPoint(chart1.CandlestickSeries, param);
                            syncCrosshair(chart2, chart2.CandlestickSeries, dataPoint, param);
                        });

                        chart2.chart.subscribeCrosshairMove(param => {
                            const dataPoint = getCrosshairDataPoint(chart2.CandlestickSeries, param);
                            syncCrosshair(chart1, chart1.CandlestickSeries, dataPoint, param);
                        });
                    }
                });
            });
        },
    };

    window.CrosshairManager = CrosshairManager;
}

if (!window.Legend) {
    class Legend {
        constructor(chartContainerId) {
            this.legend = null; 
            this.chartContainerId = chartContainerId;
        }

        createLegend() {
            if (!this.legend) {
                const chartContainer = document.getElementById(this.chartContainerId);
                this.legend = document.createElement('div');
                this.legend.style = `
                    position: absolute;
                    top: 0;
                    left: 12px;
                    z-index: 1;
                    font-size: 14px;
                    font-family: sans-serif;
                    line-height: 18px;
                    font-weight: 300;
                    color: white; // Set legend text color
                `;

                chartContainer.style.position = 'relative';
                chartContainer.appendChild(this.legend);
            }
        }

        updateLegend(param, chart) {
            if (!this.legend) {
                return;
            }

            const validCrosshairPoint = !(
                param === undefined || param.time === undefined || param.point.x < 0 || param.point.y < 0
            );

            if (validCrosshairPoint) {
                let legendText = "<div style='font-size: 18px; margin: 4px 0px;'>";
            
                if (chart.Symbol) {
                    const symbol = chart.Symbol;
                    legendText += `${symbol} : `;
                }
            
                if (chart.CandlestickSeries) {
                    const olhc = param.seriesData.get(chart.CandlestickSeries);
                    const time = new Date(olhc.time * 1000).toUTCString().slice(4, -4);
                    legendText += `Time: ${time} `;
                    legendText += `Open: ${olhc.open.toFixed(2)} High: ${olhc.high.toFixed(2)} `;
                    legendText += `Low: ${olhc.low.toFixed(2)} Close: ${olhc.close.toFixed(2)} `;
                }
            
                if (chart.VolumeSeries) {
                    const volume = param.seriesData.get(chart.VolumeSeries).value.toFixed(2);
                    legendText += `Volume: ${volume} `;
                }
            
                if (chart.LineSeriesList && chart.LineSeriesList.length > 0) {
                    const lineSeriesData = chart.LineSeriesList.map((lineSeries) => {
                        const lineData = param.seriesData.get(lineSeries);
                        return `${lineSeries.title}: ${lineData.value.toFixed(2)}`;
                    }).join(', ');
            
                    legendText += `${lineSeriesData} `;
                }
            
                legendText += "</div>";
            
                this.legend.innerHTML = legendText.trim(); 
            } else {
                this.legend.innerHTML = ""; 
            }
        }

        removeLegend() {
            if (this.legend) {
                this.legend.remove();
                this.legend = null;
            }
        }
    }

    window.Legend = Legend;
}

const MainchartOptions = {
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
        scaleMargins: { top: 0.1, bottom: 0 },
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
};

const SubchartOptions = {
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
};

if (!window.Chart) {
    class Chart {
        constructor(chartContainerId) {
            this.chartContainerId = chartContainerId;
            this.chart = null;
            this.CandlestickSeries = null;
            this.LineSeriesList = [];
            this.VolumeSeries = null;
            this.Symbol = null;
            this.legend = new Legend(chartContainerId);
        }

        createChart(width, height, chartOptions = MainchartOptions) {
            if (!this.chart) {
                this.chart = LightweightCharts.createChart(
                    document.getElementById(this.chartContainerId),
                    {
                        width: width,
                        height: height,
                        ...chartOptions,
                    }
                );

                window.CrosshairManager.subscribeChart(this);
                this.chart.subscribeCrosshairMove(param => this.legend.updateLegend(param, this));
            }
        }

        addCandlestickSeries(Symbol, data) {
            if (!this.CandlestickSeries) {
                this.CandlestickSeries = this.chart.addCandlestickSeries({
                    color: 'rgb(0, 120, 255)',
                    lineWidth: 2,
                });
            }

            this.Symbol = Symbol;
            this.CandlestickSeries.setData(data);
        }

        removeCandlestickSeries() {
            if (this.CandlestickSeries) {
                const seriesToRemove = this.CandlestickSeries;
                this.chart.removeSeries(seriesToRemove);
                this.CandlestickSeries = null;
            }
        }

        addVolumeSeries(data, value_name) {
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

        addLineSeries(data, value_name, title,lineStyleOptions) {
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

            const options = { ...defaultOptions, ...lineStyleOptions };
            let lineSeries = this.chart.addLineSeries(options);
            lineSeries.title = title; 

            lineSeries.setData(
                data.map((d) => ({
                    time: d.time,
                    value: d[value_name],
                }))
            );

            this.LineSeriesList.push(lineSeries);
        }

        removeallLineSeries() {
            this.LineSeriesList.forEach((lineSeries) => {
                this.chart.removeSeries(lineSeries);
            });
            this.LineSeriesList = [];
        }

        removeLineSeries(title) {
            const lineSeriesToRemove = this.LineSeriesList.find(series => series.title === title);

            if (lineSeriesToRemove) {
                const index = this.LineSeriesList.indexOf(lineSeriesToRemove);
                this.chart.removeSeries(lineSeriesToRemove);
                this.LineSeriesList.splice(index, 1);
            }
        }
    }

    window.Chart = Chart;
}

if (!window.ParentChart) {
    class ParentChart extends Chart {
        constructor(chartContainerId, width, height) {
            super(chartContainerId);
            this.subCharts = [];
            this.createMainChartContainer();
            this.createChart(width, height);
        }

        createMainChartContainer() {
            let container = document.getElementById(this.chartContainerId);
            if (!container) {
                const wrapper = document.getElementById('wrapper');
                container = document.createElement('div');
                container.id = this.chartContainerId;
                container.style.flex = '4';
                container.style.width = '100%';
                container.style.height = '0';
                container.style.minHeight = '400px';
                container.style.overflow = 'hidden';
                wrapper.appendChild(container);
            }
        }

        addSubChart(subChartContainerId, width, height) {
            const existingSubChart = this.subCharts.find(subChart => subChart.chartContainerId === subChartContainerId);
            if (!existingSubChart)
            {
                this.createSubchartContainer(subChartContainerId);
                const subChart = new Chart(subChartContainerId);
                subChart.createChart(width, height, SubchartOptions);
                this.subCharts.push(subChart);

                return subChart;
            }
            return existingSubChart;
        }

        createSubchartContainer(subChartContainerId) {
            const subChartContainer = document.createElement('div');
            subChartContainer.id = subChartContainerId;
            subChartContainer.className = 'subchart';
            subChartContainer.style.flex = '1';
            subChartContainer.style.width = '100%';
            subChartContainer.style.height = '0';
            subChartContainer.style.minHeight = '100px';
            subChartContainer.style.overflow = 'hidden';
            const wrapper = document.getElementById('wrapper');
            wrapper.appendChild(subChartContainer);
        }

        removeSubChart(subChart) {
            const index = this.subCharts.indexOf(subChart);
            if (index !== -1) {
                this.subCharts.splice(index, 1);

                const subChartContainer = document.getElementById(subChart.chartContainerId);
                if (subChartContainer) {
                    subChartContainer.innerHTML = '';
                    subChartContainer.remove();
                }
            }
        }

    }

    window.ParentChart = ParentChart;
}

function getCrosshairDataPoint(series, param) {
    if (!param.time) {
        return null;
    }
    const dataPoint = param.seriesData.get(series);
    return dataPoint || null;
}

function syncCrosshair(chart, series, dataPoint, param) {

    if (dataPoint) {
        chart.chart.setCrosshairPosition(dataPoint.value, dataPoint.time, series);
        return;
    }
    chart.chart.clearCrosshairPosition();
}