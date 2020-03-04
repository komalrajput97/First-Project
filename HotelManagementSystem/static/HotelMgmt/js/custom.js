$(document).ready(function(){
  var width=$(window).width();
  var img_height=(width*501.5)/1284;

  $('.questions').hide();
  $('.current').show();

  $('#next').click(function(){
    updateQuestion(1)
  });

  $('#prev').click(function(){
    updateQuestion(-1)
  });

  function updateQuestion(index){
    $('div.questions').hide();
    var new_id=parseInt($('div.current').attr('id'))+index;
    $('div.current').removeClass('current').hide();
    $('#'+new_id).addClass('current').show();
    if(new_id>1){
      $('#prev').show();
      $('#next').show();
    }
    else{
      $('#prev').hide();
    }
    if(new_id == $('div.questions').length){
      $('#next').hide();
    }
  }
  
  // global variable pincode set to a default value, in case geocoder does not work data can be fetched using this pincode
  var pincode=382010;
  
  if(window.location.pathname=="/hotel/index/"){
    $('.wrapper').css('opacity','0');
    getPincodeFromLocation();
    getContentsFromPincode();
  }

  // function to get pincode from location
  function getPincodeFromLocation(){
    if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
   } else { 
     x.innerHTML = "Geolocation is not supported by this browser.";
   }
    function showPosition(position) {

     var lat=position.coords.latitude;
     var lng=position.coords.longitude;
     var latlng = new google.maps.LatLng(lat, lng);
      
      var geocoder = geocoder = new google.maps.Geocoder();
     
      geocoder.geocode({ 'latLng': latlng }, function (results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
              pincode=results[2].address_components[0].long_name;

              // load content by pincode of user's current location
              getContentsFromPincode(pincode);
          }
          else if(status=="OVER_QUERY_LIMIT"){
            getContentsFromPincode(pincode); 
          }
          else{
            // if geocoder is not working for other reasons then load data by default pincode
            getContentsFromPincode(pincode); 
          }
      });
      
    }
  }

  $('.slider-box .owl-carousel .owl-nav .owl-prev').css("top",img_height/2+"px");
  $('.slider-box .owl-carousel .owl-nav .owl-next').css("top",img_height/2+"px");

  // function to get menu items when category is selected
  $("#menu_categories").on('click','button[name="view_item_btn"]',function(){
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
      url:'/hotel/getmenuitems/',
      type:'POST',
      data:{
          'csrfmiddlewaretoken':csrf_token,
          'cat_id':$(this).attr('id')
      }
    }).then(function(result){
        $('#menu_items').html(result.menu_items_view);
    })
  });

  // function to get all things in index page according to pincode selected
  function getContentsFromPincode(){
      var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
          url:'/hotel/getoutletfrompincode/',
          type:'POST',
          data:{
            'csrfmiddlewaretoken':csrf_token,
            'pincode':pincode
          }
        }).then(function(result){
          if(result.status=="success"){
            $('#menu_categories').html(result.menu_categories_view);
            $('#menu_items').html('');
            $('.owl-carousel').trigger('replace.owl.carousel',result.hotel_outlet_images_view).trigger('refresh.owl.carousel');
            $('#outlet_name').html(result.outlet_name+" outlet");
            
            //hide loader when contents are loaded 
            $(".loader").hide();
            $(".wrapper").css('opacity','1');

          }
          else{
            alert(result.msg);
          }
            
        });
      }
    
  // function to get things in index page according to pincode entered by user in 
  $('.pincode_search input[type="submit"]').click(function(){
        getContentsFromPincode($('#pincode').val());
    });

 // function for keeping billing address same as shipping address if checkbox for it is checked 
 // called on change events of checkbox and shipping address input box
  
  $('#id_shipping_address').add($('input[name="address"]')).change(function(){
    if($('input[name="address"]').prop('checked')==true){
      $('#id_billing_address').val($('#id_shipping_address').val());
    }
    else{
      $('#id_billing_address').val('');
    }
  });

  $('#track_order').click(function(){
      var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
      // ajax function for getting status of order using token
      $.ajax({
          url:'/hotel/track_order/',
          type:'POST',
          data:{
            'token':$('input[name="token"]').val(),
            'csrfmiddlewaretoken':csrf_token
          },
      }).then(function(result){
          if(result.status=="success"){
            // if token is valid
            $('div.instruc').html("Order Status : "+result.order_status);
            $('input[name="token"]').val("");

          }
          else{
            // if token is invalid
            $('div.instruc').html("You entered invalid token.Please try again");
            $('input[name="token"]').val("");
          }
          
      });
  });

  // ajax function for updating quantity and total
  // when value in input of quantity changes

  $("input").change(function(){
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var item_id=$(this).parents('.cart_item').attr('id');
    var elem=$(this);
    $.ajax({
      url:'/hotel/updatecart/',
      type:'POST',
      data:{
        'csrfmiddlewaretoken':csrf_token,
        'cart_item_id':item_id,
        'operation':'quantity',
        'quantity':$(this).val()
      },
    }).then(function(result){
      if(result.status=="success"){
        $('.prod_qty .minus').css({
            "cursor": "pointer","pointer-events": "auto"});
            $(this).prev().val(parseInt($(this).prev().val())+1);
            if(result.total==0){
          $('#total').parent('h1').html("There are no items in the cart.");
        }
        else{
          $('#total').html("&#8377; "+result.total);
        }
      }
    });
  });

  // ajax function for removing items from cart
  $('.remove_btn').click(function(){
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var item_id=$(this).attr('id').split('_')[1];
    var elem=$(this);
    $.ajax({
      url:'/hotel/removefromcart/',
      type:'POST',
      data:{
        'csrfmiddlewaretoken':csrf_token,
        'cart_item_id':item_id
      },
    }).then(function(result){
      if(result.status=="success"){
        $('#'+item_id).hide();

        if(result.total==0){
          $('#total').parent('h1').html("There are no items in the cart.");
        }
        else{
          $('#total').html("&#8377; "+result.total);
        }     
      }
    });


  });

  // ajax function for updating quantity and total
  // when minus button is clicked

  $('.prod_qty .minus').click(function(){
     var new_value=parseInt($(this).next().val())-1;
     if(new_value==0 || parseInt($(this).next().val())==0)
     {
      // disabling the minus button if value in input is 1
      $('.prod_qty .minus').css({
      "cursor": "wait","pointer-events": "none"});
     }
     else{
      var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var item_id=$(this).parents('.cart_item').attr('id');
    var elem=$(this);
    $.ajax({
      url:'/hotel/updatecart/',
      type:'POST',
      data:{
        'csrfmiddlewaretoken':csrf_token,
        'cart_item_id':item_id,
        'operation':'minus'
      },
    }).then(function(result){
      if(result.status=="success"){
        // enabling the minus button if value in input becomes greater than 1
        $('.prod_qty .minus').css({
            "cursor": "pointer","pointer-events": "auto"});
            $(this).prev().val(parseInt($(this).prev().val())+1);
            if(result.total==0){
          $('#total').parent('h1').html("There are no items in the cart.");
        }
        else{
          $('#total').html("&#8377; "+result.total);
        }
        }
      
    });
      $(this).next().val(new_value);
      $('.prod_qty .minus').css({
      "cursor": "pointer","pointer-events": "auto"});
    }
    });

// ajax function for updating quantity and total
// when plus button is clicked

$('.prod_qty .plus').click(function(){
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
  var item_id=$(this).parents('.cart_item').attr('id');
  var elem=$(this);
  $.ajax({
    url:'../updatecart/',
    type:'POST',
    data:{
      'csrfmiddlewaretoken':csrf_token,
      'cart_item_id':item_id,
      'operation':'plus'
    },
  }).then(function(result){
    if(result.status=="success"){
      // enabling the minus button if value in input becomes greater than 1
      elem.prev().prev().css({
          "cursor": "pointer","pointer-events": "auto"});
        elem.prev().val(parseInt(elem.prev().val())+1);
          if(result.total==0){
        $('#total').parent('h1').html("There are no items in the cart.");
      }
      else{
        $('#total').html("&#8377; "+result.total);
      }
      }
  });

});

  $(window).resize(function(){
    var width=$(window).width();
    var img_height=(width*501.5)/1284;
    $('.slider-box .owl-carousel .owl-nav .owl-prev').css("top",img_height/2+"px");
    $('.slider-box .owl-carousel .owl-nav .owl-next').css("top",img_height/2+"px");
  });


// Function for reloading the page whenever back button is clicked
$(window).load(function() {
    // value of 2 means page was accessed by clicking back button
    if (!!window.performance && window.performance.navigation.type === 2) {
        window.location.reload(true);
    }
});

/////////////////////////////////////////////////////
//                  SLIDER JS                      //
/////////////////////////////////////////////////////

// slider for banner of hotel outlets in index page
$('.owlcarousel1').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    navText: [
      '<i class="fa fa-angle-left"></i>',
      '<i class="fa fa-angle-right"></i>'
    ],
    responsive:{
        0:{
            items:1
        },
        768:{
            items:1
        },
        991:{
            items:1
        }
    }
});

});


