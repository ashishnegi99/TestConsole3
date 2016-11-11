$(function () {    
    Highcharts.chart('container4', {
        credits: {
            enabled: false
        },
        chart: {
            type: 'column'
        },
        title: {
            text: 'Test Cases Pass/Fail'
        },
        xAxis: {
            categories: chartData.jobNames
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Pass Numbers and Fail Numbers'
            },
            stackLabels: {
                enabled: true,
                style: {
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            }
        },
        legend: {
            align: 'right',
            x: -30,
            verticalAlign: 'top',
            y: 25,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
            borderColor: '#CCC',
            borderWidth: 1,
            shadow: false
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: false,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                }
            }
        },
        series: [{
            name: 'Pass',
            data: chartData.passNums
        }, {
            name: 'Fail',
            data: chartData.failNums
        }]
    });
});