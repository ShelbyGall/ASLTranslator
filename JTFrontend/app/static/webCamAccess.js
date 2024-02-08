//var socket = io.connect('http://192.168.1.171:5000'); //http://127.0.0.1:5000 http://192.168.1.171:5000
//window.location.protocol
// This is how we establish connection from the server to the client-side
// i.e. this is the url we go to on the browser
var socket = io.connect("http://" + document.domain + ":" + location.port);

// Essentially, This is a listener on the client-side when the server runs
// an event named 'connect', it'll print the following in the browser console window
socket.on("connect", function () {
  console.log("Connected...!", socket.connected);
});

// The canvas is where we'll be copying the video frame to
// The context is the special tool that we'll be using to copy the
// video to the canvas
var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");
const video = document.querySelector("#videoElement");

video.width = 400;
video.height = 300;

// Essentially, if there is input coming from the camera, we will display it
// where video/videoElement is on the HTML page and the video will play
// if there is an error, then nothing will happen
if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({video: true,})
    .then(function (stream) {video.srcObject = stream; video.play();})
    .catch(function (error) {});
}

// This is how many frames per second we are sending over to the backend/sever-side
// We are sending 1 frame every 100 milliseconds
const FPS = 10;
setInterval(() => {
  width = video.width;
  height = video.height;
  // this draws the image of the video to the canvas
  context.drawImage(video, 0, 0, width, height);
  // we convert the video frame to base64 (Binary to ASCII characters)
  // this conversion allows us to package the data to be sent to the backend
  var data = canvas.toDataURL("image/jpeg", 0.5);
  // we clear the canvas/set it up for the next frame to be copied
  context.clearRect(0, 0, width, height);
  // we send the data to the backend in which the method with @socketio.on("image")
  // handles the data
  socket.emit("image", data);
}, 1000 / FPS);

// we receive the new frame/image back that has been processed by ASL detection and then we
// update the new source for the image being displayed
socket.on("processed_image", function (image) {
  photo.setAttribute("src", image);
});