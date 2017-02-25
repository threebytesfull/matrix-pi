function matrixRequest(url, callback, context) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    if (callback) {
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                callback(context);
            }
        };
    }
    xhr.send(null);
}
function matrixPostRequest(url, data, callback, context) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    if (callback) {
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                callback(context);
            }
        }
    }
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    dataKeys = Object.keys(data);
    var formFields = [];
    for (var i=0; i<dataKeys.length; i++) {
        value = data[dataKeys[i]];
        if (typeof(value) == 'string') { value = [value]; }
        formFields.push(dataKeys[i] + '=' + value.join(','));
    }
    xhr.send(formFields.join('&'));
}
function hasClass(element, className) {
    return ((' ' + element.className + ' ').replace(/[\r\n\t]/g, ' ').indexOf(' ' + className + ' ') > -1);
}
function addClass(element, className) {
    if (!hasClass(element, className)) {
        element.className = (element.className + ' ' + className).trim();
    }
}
function removeClass(element, className) {
    element.className = (' ' + element.className + ' ').replace(/[\r\n\t]/g, ' ').replace(' ' + className + ' ', '').trim();
}
function reset() {
    matrixRequest('/reset', function() {
        var leds = document.getElementsByClassName('led');
        for (var i=0; i<leds.length; i++) {
            removeClass(leds[i], 'on');
        }
        document.getElementById('current').value = 1;
    });
}
function allOn() {
    matrixRequest('/allOn', function() {
        var leds = document.getElementsByClassName('led');
        for (var i=0; i<leds.length; i++) {
            addClass(leds[i], 'on');
        }
    });
}
function allOff() {
    matrixRequest('/allOff', function() {
        var leds = document.getElementsByClassName('led');
        for (var i=0; i<leds.length; i++) {
            removeClass(leds[i], 'on');
        }
    });
}
function toggleLED(sender, x, y) {
    if (hasClass(sender, 'on')) {
        matrixPostRequest('/clearPixel', {coords:x+','+y}, function() {
            removeClass(sender, 'on');
        });
    } else {
        matrixPostRequest('/setPixel', {coords:x+','+y}, function() {
            addClass(sender, 'on');
        });
    }
}
function toggleColumn(x) {
    var setElements = [];
    var clearElements = [];
    var setCoords = [];
    var clearCoords = [];
    for (var y=0; y<height; y++) {
        element = document.getElementById('led_' + x + '_' + y);
        coords = x + ',' + y;
        if (hasClass(element, 'on')) {
            clearElements.push(element);
            clearCoords.push(coords);
        } else {
            setElements.push(element);
            setCoords.push(coords);
        }
    }
    if (clearElements.length) {
        matrixPostRequest('/clearPixel', {coords:clearCoords}, function() {
            for (var i=0; i<clearElements.length; i++) {
                removeClass(clearElements[i], 'on');
            }
        });
    }
    if (setElements.length) {
        matrixPostRequest('/setPixel', {coords:setCoords}, function() {
            for (var i=0; i<setElements.length; i++) {
                addClass(setElements[i], 'on');
            }
        });
    }
}
function toggleRow(y) {
    var setElements = [];
    var clearElements = [];
    var setCoords = [];
    var clearCoords = [];
    for (var x=0; x<width; x++) {
        element = document.getElementById('led_' + x + '_' + y);
        coords = x + ',' + y;
        if (hasClass(element, 'on')) {
            clearElements.push(element);
            clearCoords.push(coords);
        } else {
            setElements.push(element);
            setCoords.push(coords);
        }
    }
    if (clearElements.length) {
        matrixPostRequest('/clearPixel', {coords:clearCoords}, function() {
            for (var i=0; i<clearElements.length; i++) {
                removeClass(clearElements[i], 'on');
            }
        });
    }
    if (setElements.length) {
        matrixPostRequest('/setPixel', {coords:setCoords}, function() {
            for (var i=0; i<setElements.length; i++) {
                addClass(setElements[i], 'on');
            }
        });
    }
}
function toggleReversed(sender) {
    matrixRequest('/setReversed/' + (sender.checked ? 1 : 0), function() {
        location.reload(true); // too lazy to write ajax refresh right now!
    });
}
function setCurrent(sender) {
    var newCurrent = parseInt(sender.value) || 1
    var current = Math.min(Math.max(newCurrent, 0), 30);
    sender.value = current;
    matrixRequest('/setCurrent/' + current);
}
function hiSignal(pin) {
    var setElements = [];
    var clearElements = [];
    var setCoords = [];
    var clearCoords = [];
    for (var i=0; i<pin.anode_leds.length; i++) {
        pair = pin.anode_leds[i];
        var x = pair[0];
        var y = pair[1];
        element = document.getElementById('led_' + x + '_' + y);
        coords = x + ',' + y;
        if (hasClass(element, 'on')) {
            clearElements.push(element);
            clearCoords.push(coords);
        } else {
            setElements.push(element);
            setCoords.push(coords);
        }
    }
    if (clearElements.length) {
        matrixPostRequest('/clearPixel', {coords:clearCoords}, function() {
            for (var i=0; i<clearElements.length; i++) {
                removeClass(clearElements[i], 'on');
            }
        });
    }
    if (setElements.length) {
        matrixPostRequest('/setPixel', {coords:setCoords}, function() {
            for (var i=0; i<setElements.length; i++) {
                addClass(setElements[i], 'on');
            }
        });
    }
}
function loSignal(pin) {
    var setElements = [];
    var clearElements = [];
    var setCoords = [];
    var clearCoords = [];
    for (var i=0; i<pin.cathode_leds.length; i++) {
        pair = pin.cathode_leds[i];
        var x = pair[0];
        var y = pair[1];
        element = document.getElementById('led_' + x + '_' + y);
        coords = x + ',' + y;
        if (hasClass(element, 'on')) {
            clearElements.push(element);
            clearCoords.push(coords);
        } else {
            setElements.push(element);
            setCoords.push(coords);
        }
    }
    if (clearElements.length) {
        matrixPostRequest('/clearPixel', {coords:clearCoords}, function() {
            for (var i=0; i<clearElements.length; i++) {
                removeClass(clearElements[i], 'on');
            }
        });
    }
    if (setElements.length) {
        matrixPostRequest('/setPixel', {coords:setCoords}, function() {
            for (var i=0; i<setElements.length; i++) {
                addClass(setElements[i], 'on');
            }
        });
    }
}

