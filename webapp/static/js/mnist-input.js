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
    y = 8;

function init() {
    canvas = document.getElementById('canvasMNIST');
    ctx = canvas.getContext("2d");
    w = canvas.width;
    h = canvas.height;

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
    //document.getElementById("prediction").style.display = "none";
}

// Sending the canvas image to Flask
function send() {
    var canvas = document.getElementById("canvasMNIST");
    var dataURL = canvas.toDataURL();

    console.log("Data URL: " + dataURL);

    // Adapted from: https://stackoverflow.com/questions/34779799/upload-base64-image-with-ajax
    $.ajax({
        url: "/upload",
        type: "POST",
        data: {imageString: dataURL}
    }).done(function(e){
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