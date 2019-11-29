//  ===  G00303598 -- Morgan Reilly  ===
// ===  Emerging Technologies 2019  ===
// References:
// https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_usage

// -- POST URL --
var url = "localhost:5000/"

// -- Canvas Variables --
var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;

// -- Pen --
// x => Colour
// y => Thickness
var x = "white", y = 10;

// -- Initialize --
function init() {
    setUpCanvas();
    mouseInput();
    screenIntervalRegulator();
    mobileTouchInput();
}

// -- Canvas Setup --
function setUpCanvas() {
    // Canvas set up
    canvas = document.getElementById('canvasMNIST');
    ctx = canvas.getContext("2d");
    w = canvas.width;
    h = canvas.height;
}

// -- Mouse Input --
function mouseInput() {
    // Adapted from: http://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html
    canvas.addEventListener("mousemove", function (e) {
        findXY('move', e)
    }, false);
    canvas.addEventListener("mousedown", function (e) {
        findXY('down', e)
    }, false);
    canvas.addEventListener("mouseup", function (e) {
        findXY('up', e)
    }, false);
    canvas.addEventListener("mouseout", function (e) {
        findXY('out', e)
    }, false);
}

// -- Screen Regulator --
// Regular interval for drawing to screen, smoother
function screenIntervalRegulator() {
    // Adapted from: http://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html
    window.requestAnimationFrame(function (callback) {
        return window.requestAnimationFrame ||
            window.webkitRequestAnimationFrame ||
            window.mozRequestAnimationFrame ||
            window.oRequestAnimationFrame ||
            window.msRequestAnimaitonFrame ||
            function (callback) {
                window.setTimeout(callback, 1000 / 60);
            };
    });
}

// -- Allow Touch Input --
// Use for mobile
function mobileTouchInput() {
    // Adapted from: http://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html
    canvas.addEventListener("touchstart", function (e) {
        mouse_pos = getTouchPos(canvas, e);
        var touch = e.touches[0];
        var mouseEvent = new MouseEvent("mousedown", {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    }, false);
    canvas.addEventListener("touchend", function (e) {
        var mouseEvent = new MouseEvent("mouseup", {});
        canvas.dispatchEvent(mouseEvent);
    }, false);
    canvas.addEventListener("touchmove", function (e) {
        var touch = e.touches[0];
        var mouseEvent = new MouseEvent("mousemove", {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    }, false);
}

// -- Get Touch Position --
// Use for mobile input
function getTouchPos(canvasDom, touchEvent) {
    // Adapted from: http://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html
    var rect = canvasDom.getBoundingClientRect();
    return {
        x: touchEvent.touches[0].clientX - rect.left,
        y: touchEvent.touches[0].clientY - rect.top
    };
}

// -- Draw Line --
function draw() {
    // Adapted from: https://stackoverflow.com/a/8398189/8883485
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(currX, currY);
    ctx.strokeStyle = x;
    ctx.lineWidth = y;
    ctx.stroke();
    ctx.closePath();
}

// -- Erase Canvas --
function erase() {
    // Adapted from: https://stackoverflow.com/a/8398189/8883485
    ctx.clearRect(0, 0, w, h);
    document.getElementById("canvas_img").style.display = "none";
    document.getElementById("something").innerHTML = "new text";
}

// -- Canvas Send --
// Grab canvas
// Convert to dataURL
// Print -- Verify
// Send URL via POST with Ajax
function send() {
    // Adapted from: https://stackoverflow.com/a/8398189/8883485
    var canvas = document.getElementById("canvasMNIST");
    var dataURL = canvas.toDataURL();

    console.log("Data URL: " + dataURL);

    // Adapted from: https://stackoverflow.com/questions/34779799/upload-base64-image-with-ajax
    $.ajax({
        url: "/predict",
        type: "POST",
        data: {imageString: dataURL}
    }).done(function (e) {
        console.log("DONE");
        $("#prediction").empty().append(e);
    });
}

// -- Find X / Y Position --
function findXY(res, e) {
    // Adapted from: https://stackoverflow.com/a/8398189/8883485
    if (res == 'down') {
        prevX = currX;
        prevY = currY;
        currX = e.clientX - canvas.offsetLeft;
        currY = e.clientY - canvas.offsetTop;

        flag = true;
        dot_flag = true;
        if (dot_flag) {
            ctx.beginPath();
            ctx.fillStyle = x;
            ctx.fillRect(currX, currY, 2, 2);
            ctx.closePath();
            dot_flag = false;
        }
    }
    if (res == 'up' || res == "out") {
        flag = false;
    }
    if (res == 'move') {
        if (flag) {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;
            draw();
        }
    }
}