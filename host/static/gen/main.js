//$('#predict').click(function() {
//
//    var timerId, percent;
//
//    // reset progress bar
//    percent = 0;
//    $('#predict').attr('disabled', true);
//    $('#load').css('width', '0px');
//    $('#load').addClass('progress-bar-striped active');
//
//    timerId = setInterval(function() {
//
//        // increment progress bar
//        percent += 5;
//        $('#load').css('width', percent + '%');
//        $('#load').html(percent + '%');
//
//
//        if (percent >= 100) {
//            clearInterval(timerId);
//            $('#predict').attr('disabled', false);
//            $('#load').removeClass('progress-bar-striped active');
//            $('#load').html('Prediction Successful!');
//        }
//    }, 200)
//})
var i = 0;
function move() {
  if (i == 0) {
    i = 1;
    var elem = document.getElementById("predict");
    var width = 10;
    var id = setInterval(frame, 150);
    function frame() {
      if (width >= 100) {
        clearInterval(id);
        i = 0;
      } else {
        width++;
        elem.style.width = width + "%";
        elem.innerHTML = width  + "%";
      }
    }
  }
}