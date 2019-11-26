// Image URL for POST
var url = "localhost:5000/"

// Canvas creation variables
var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;

// Draw colour and size of pen
var x = "white",
    y = 10;

function init() {
    setUpCanvas();
    mouseInput();
    screenIntervalRegulator();
    mobileTouchInput();
}

function setUpCanvas() {
    // Canvas set up
    canvas = document.getElementById('canvasMNIST');
    ctx = canvas.getContext("2d");
    w = canvas.width;
    h = canvas.height;
}

function mouseInput() {
    // Adapted from: http://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html
    canvas.addEventListener("mousemove", function (e) {
        findxy('move', e)
    }, false);
    canvas.addEventListener("mousedown", function (e) {
        findxy('down', e)
    }, false);
    canvas.addEventListener("mouseup", function (e) {
        findxy('up', e)
    }, false);
    canvas.addEventListener("mouseout", function (e) {
        findxy('out', e)
    }, false);
}

function screenIntervalRegulator() {
    // Adapted from: http://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html
    // Regular interval for drawing to screen, smoother
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

function mobileTouchInput() {
    // Adapted from: http://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html
    // Allowing touch input
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

// Get the position of a touch relative to the canvas
function getTouchPos(canvasDom, touchEvent) {
    var rect = canvasDom.getBoundingClientRect();
    return {
        x: touchEvent.touches[0].clientX - rect.left,
        y: touchEvent.touches[0].clientY - rect.top
    };
}

function draw() {
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(currX, currY);
    ctx.strokeStyle = x;
    ctx.lineWidth = y;
    ctx.stroke();
    ctx.closePath();
}

function erase() {
    ctx.clearRect(0, 0, w, h);
    document.getElementById("canvas_img").style.display = "none";
    // document.getElementById("prediction").style.display = "none";
}

// Sending the canvas image to Flask
function send() {
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

function findxy(res, e) {
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