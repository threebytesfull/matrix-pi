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
  var address = $(this).data('address');
  matrixPostRequest('/reset', {address:address}, function() {
    $('.led[data-address=' + address + ']').removeClass('on');
    $('input.current[data-address=' + address + ']').val(resetCurrents[address]);
  });
}

function allOn() {
  var address = $(this).data('address');
  matrixPostRequest('/allOn', {address:address}, function() {
    $('.led[data-address=' + address + ']').addClass('on');
  });
}

function allOff() {
  var address = $(this).data('address');
  matrixPostRequest('/allOff', {address:address}, function() {
    $('.led[data-address=' + address + ']').removeClass('on');
  });
}

function toggleLED() {
  var led = $(this);
  var coords = [led.data('x') + ',' + led.data('y')];
  var address = led.data('address');
  if ($(this).hasClass('on')) {
    matrixPostRequest('/clearPixel', {coords:coords, address:address}, function() {
      led.removeClass('on');
    });
  } else {
    matrixPostRequest('/setPixel', {coords:coords, address:address}, function() {
      led.addClass('on');
    });
  }
}

function toggleLEDs(address, leds) {
  var leds_on = leds.filter(function(){ return $(this).hasClass('on') });
  var leds_off = leds.filter(function(){ return !$(this).hasClass('on') });
  if (leds_on.length) {
    var coords = leds_on.map(function(){ return $(this).data('x') + ',' + $(this).data('y') }).toArray();
    matrixPostRequest('/clearPixel', {coords:coords, address:address}, function() {
      leds_on.removeClass('on');
    });
  }
  if (leds_off.length) {
    var coords = leds_off.map(function(){ return $(this).data('x') + ',' + $(this).data('y') }).toArray();
    matrixPostRequest('/setPixel', {coords:coords, address:address}, function() {
      leds_off.addClass('on');
    });
  }
}

function toggleColumn() {
  var x = $(this).data('column');
  var address = $(this).data('address');
  var leds = $('.led[data-address='+address+'][data-x=' + x + ']');
  toggleLEDs(address, leds);
}

function toggleRow() {
  var y = $(this).data('row');
  var address = $(this).data('address');
  var leds = $('.led[data-address='+address+'][data-y=' + y + ']');
  toggleLEDs(address, leds);
}

function toggleReversed() {
  var isReversed = $(this).is(':checked');
  var address = $(this).data('address');
  matrixPostRequest('/setReversed', {address:address, reversed:isReversed}, function() {
    location.reload(true); // too lazy to write ajax refresh right now!
  });
}

function setCurrent() {
  var newCurrent = parseInt($(this).val()) || 1;
  var current = Math.min(Math.max(newCurrent, 0), 30);
  var address = $(this).data('address');
  $(this).val(current);
  matrixPostRequest('/setCurrent', {address:address, current:current});
}

function toggleSignal(address, signal, side) {
  var leds = $('.led[data-address=' + address + ']').filter(function(){ return $(this).data(side) == signal });
  toggleLEDs(address, leds);
}

function hiSignal() {
  var signal = $(this).data('signal');
  $(addresses).each(function(i, address) {
    if (isReversed[address]) {
      toggleSignal(address, signal, 'cathode');
    } else {
      toggleSignal(address, signal, 'anode');
    }
  });
}

function loSignal(pin) {
  var signal = $(this).data('signal');
  $(addresses).each(function(i, address) {
    if (isReversed[address]) {
      toggleSignal(address, signal, 'anode');
    } else {
      toggleSignal(address, signal, 'cathode');
    }
  });
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
  $('input.reversed').on('change', toggleReversed);
  $('input.current').on('change', setCurrent);
  $('.clickable.lo').on('click', loSignal);
  $('.clickable.hi').on('click', hiSignal);
  $('button.reset').on('click', reset);
  $('button.allOn').on('click', allOn);
  $('button.allOff').on('click', allOff);
});
