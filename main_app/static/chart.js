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
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          backgroundColor: 
          bgcolor,
          data: values
        }]
      }
    });
})
