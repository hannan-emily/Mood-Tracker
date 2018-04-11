


color_dictionary = [

    "#F0D5E3",
    "#7571A1",
    "#FFE46B",
    "#48515C",
    "#FFC697",
    "#80B5A1",
    "#BDFFE1",
    "#98C2D9",
    "#F5B23E",
    "#6A8AC0",
    "#959EA8",
    "#E89BC6",
    "#C5BDEF",
    "#FFA275"
    ]


document.addEventListener('DOMContentLoaded', function() {

    bgcolor = color_dictionary.slice(0,values.length)
    var ctx1 = document.getElementById("pieChart").getContext('2d');
    var pieChart = new Chart(ctx1, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          backgroundColor: bgcolor,
          data: values
        }]
      }
    });

    var ctx2 = document.getElementById("barChart").getContext('2d');
    var options = {
        scales: {
            xAxes: [{
                display: true,
                gridLines: {
                    offsetGridLines: false
                }
            }],
            yAxes: [{
                display: false,
                ticks: {
                  min: 0
                },
                gridLines: {
                    offsetGridLines: false
                }
            }]
        }
    }
    var barChart = new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'mood',
          backgroundColor: bgcolor,
          data: values
        }]
      },
      options: options

    });


    var ctx3 = document.getElementById("samplePieChart").getContext('2d');
    var pieChart = new Chart(ctx3, {
      type: 'pie',
      data: {
        labels: ['happy', 'sad', 'disgusted', 'depressed', 'excited', 'surprised'],
        datasets: [{
          backgroundColor: color_dictionary.slice(0,6),
          data: [15, 4, 1, 1, 7, 3]
        }]
      }
    });

    var ctx4 = document.getElementById("sampleBarChart").getContext('2d');
    var options = {
        scales: {
            xAxes: [{
                display: true,
                gridLines: {
                    offsetGridLines: false
                }
            }],
            yAxes: [{
                display: false,
                ticks: {
                  min: 0
                },
                gridLines: {
                    offsetGridLines: false
                }
            }]
        }
    }
    var barChart = new Chart(ctx4, {
      type: 'bar',
      data: {
        labels: ['happy', 'sad', 'disgusted', 'depressed', 'excited', 'surprised'],
        datasets: [{
          label: 'mood',
          backgroundColor: color_dictionary.slice(0,6),
          data: [15, 4, 1, 1, 7, 3]
        }]
      },
      options: options

    });


})
