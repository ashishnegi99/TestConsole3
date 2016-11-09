$(function () {
    Highcharts.chart('container2', {
        credits: {
            enabled: false
        },
        chart: {
            type: 'area'
        },
        title: {
            text: 'Test Cases Pass Trend'
        },
        xAxis: {
            categories: chartData.dates,
            allowDecimals: false,
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: 'Cumulative Pass Count'
            },
            labels: {
                formatter: function () {
                    return this.value / 1000 + 'k';
                }
            }
        },
        plotOptions: {
            area: {
  
            }
        },
        series: [{
            name: 'Pass',
            data: chartData.passNums
        }]
    });
});