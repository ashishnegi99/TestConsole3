$(function () {
    Highcharts.setOptions({
     colors: ['rgb(80,180,50)', 'rgb(180,00,00)', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4']
    });

    Highcharts.chart('container3', {
        credits: {
            enabled: false
        },
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Pie Chart for Pass Percentage'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} % <br> Total : {point.total} </br>',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: 'Test Cases',
            colorByPoint: true,
            data: [{
                    name: 'Pass',
                    y: chartData.totalPass
                }, 
                {
                    name: 'Fail',
                    y: chartData.totalFail,
                    selected: true
            }]
        }]
    });
});