console.log("JavaScript loaded...")

$('.like').on('click', function(event){
  event.preventDefault();
  var element = $(this);
  $.ajax({
    url: '/like_cat/',
    method: 'GET',
    data: {cat_id: element.attr('data-id')},
    success: function(response){
      element.html('Likes: ' + response);
    }
  })
})



$(document).ready(function(){

  $('.responsive').slick({
  dots: true,
  infinite: false,
  speed: 300,
  slidesToShow: 3,
  slidesToScroll: 1,
  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 1,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 1
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
    // You can unslick at a given breakpoint now by adding:
    // settings: "unslick"
    // instead of a settings object
  ]
});




});
