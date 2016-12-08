$(function () {
    Highcharts.theme = {
        colors: ['rgb(80,180,50)', 'rgb(180,00,00)', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
    }
    
    Highcharts.setOptions(Highcharts.theme);
    
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