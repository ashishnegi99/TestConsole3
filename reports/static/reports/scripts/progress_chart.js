$(function () {
    Highcharts.theme = {
        colors: ['rgb(80,180,50)', 'rgb(180,00,00)', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
    }
    Highcharts.setOptions(Highcharts.theme);
    Highcharts.chart('container1', {
         credits: {
            enabled: false
        },
        chart: {
            type: 'solidgauge',
            marginTop: 50
        },
        title: {
            text: "Today's Progress Chart",
            style: {
                fontSize: '24px'
            }
        },
        tooltip: {
            borderWidth: 0,
            backgroundColor: 'none',
            shadow: false,
            style: {
                fontSize: '16px'
            },
            pointFormat: '<br><span style="font-size:2em; color: {point.color}; font-weight: bold">{point.y}%</span>',
            positioner: function (labelWidth) {
                return {
                    x: 225 - labelWidth / 2,
                    y: 150
                };
            }
        },
        pane: {
            startAngle: 0,
            endAngle: 360,
            background: [{
                outerRadius: '112%',
                innerRadius: '88%',
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                borderWidth: 0,
            }]
        },

        yAxis: {
            min: 0,
            max: 100,
            lineWidth: 0,
            tickPositions: [],
            title: {
                text: chartData.todayTotal,
                style: {
                    fontSize: '72px'
                },
                verticalAlign: 'middle',
                y: 100
            }
        },

        plotOptions: {
            solidgauge: {
                borderWidth: '34px',
                dataLabels: {
                    enabled: false
                },
                linecap: 'round',
                stickyTracking: false
            }
        },

        series: [{
            name: 'Pass',
            borderColor: Highcharts.getOptions().colors[0],
            data: [{
                color: Highcharts.getOptions().colors[0],
                radius: '100%',
                innerRadius: '100%',
                y: Math.round((chartData.todayPass / chartData.todayTotal) * 100)
            }]
        }]
    },

    function callback() {

    });

});
