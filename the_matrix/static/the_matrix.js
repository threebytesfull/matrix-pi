function matrixRequest(url, callback, context) {
  $.ajax({
    url: url,
    method: 'GET',
  }).done(function(msg) {
    if (callback) {
      callback(context);
    }
  });
}

function matrixPostRequest(url, data, callback, context) {
  $.ajax({
    url: url,
    method: 'POST',
    data: data,
  }).done(function(msg) {
    if (callback) {
      callback(context);
    }
  });
}

function reset() {
  matrixRequest('/reset', function() {
    $('.led').removeClass('on');
  });
}

function allOn() {
    matrixRequest('/allOn', function() {
      $('.led').addClass('on');
    });
}

function allOff() {
    matrixRequest('/allOff', function() {
      $('.led').removeClass('on');
    });
}

function toggleLED() {
  var led = $(this);
  var coords = [led.data('x') + ',' + led.data('y')];
  if ($(this).hasClass('on')) {
    matrixPostRequest('/clearPixel', {coords:coords}, function() {
      led.removeClass('on');
    });
  } else {
    matrixPostRequest('/setPixel', {coords:coords}, function() {
      led.addClass('on');
    });
  }
}

function toggleLEDs(leds) {
  var leds_on = leds.filter(function(){ return $(this).hasClass('on') });
  var leds_off = leds.filter(function(){ return !$(this).hasClass('on') });
  if (leds_on.length) {
    var coords = leds_on.map(function(){ return $(this).data('x') + ',' + $(this).data('y') }).toArray();
    matrixPostRequest('/clearPixel', {coords:coords}, function() {
      leds_on.removeClass('on');
    });
  }
  if (leds_off.length) {
    var coords = leds_off.map(function(){ return $(this).data('x') + ',' + $(this).data('y') }).toArray();
    matrixPostRequest('/setPixel', {coords:coords}, function() {
      leds_off.addClass('on');
    });
  }
}

function listLEDs(leds) {
  return leds.map(function(){ return $(this).attr('id') + '[' + ($(this).hasClass('on') ? 'on' : 'off') + ']' }).toArray().join(', ');
}

function toggleColumn() {
  var x = $(this).data('column');
  leds = $('.led[data-x=' + x + ']');
  toggleLEDs(leds);
}

function toggleRow() {
  var y = $(this).data('row');
  leds = $('.led[data-y=' + y + ']');
  toggleLEDs(leds);
}

function toggleReversed() {
  var isReversed = $(this).is(':checked');
  matrixRequest('/setReversed/' + (isReversed ? 1 : 0), function() {
    location.reload(true); // too lazy to write ajax refresh right now!
  });
}

function setCurrent() {
  var newCurrent = parseInt($(this).val()) || 1;
  var current = Math.min(Math.max(newCurrent, 0), 30);
  $(this).val(current);
  matrixRequest('/setCurrent/' + current);
}

function hiSignal() {
  var signal = $(this).data('signal');
  var leds = $('.led').filter(function(){ return $(this).data('anode') == signal });
  toggleLEDs(leds);
}

function loSignal(pin) {
  var signal = $(this).data('signal');
  var leds = $('.led').filter(function(){ return $(this).data('cathode') == signal });
  toggleLEDs(leds);
}

function ledAt(x, y) {
  return $('.led[id="led_' + x + '_' + y + '"]');
}

$(document).ready(function() {
  // Annotate LEDs with connection information for control by signals later
  $(chip).each(function(i, item){
    $(item.anode_leds).each(function(i, anode_led) {
      ledAt(anode_led[0], anode_led[1]).data('anode', item.label);
    });
    $(item.cathode_leds).each(function(i, cathode_led) {
      ledAt(cathode_led[0], cathode_led[1]).data('cathode', item.label);
    });
  });
  // Attach handlers
  $('.led_col').on('click', toggleColumn);
  $('.led_row').on('click', toggleRow);
  $('.led').on('click', toggleLED);
  $('input[name="reversed"]').on('change', toggleReversed);
  $('#current').on('change', setCurrent);
  $('.clickable.lo').on('click', loSignal);
  $('.clickable.hi').on('click', hiSignal);
});
