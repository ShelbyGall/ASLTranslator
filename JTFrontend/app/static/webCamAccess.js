// This is how we establish connection to the server from the client-side
// i.e. this is the url we go to on the browser
var socket = io.connect("http://" + document.domain + ":" + location.port);
// Array to store the letter sequence being sent over
const letterSequence = [];

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

// this is just the dimensions of the video
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
// We are sending 1 frame to the backend every 10,000 milliseconds / 10 seconds

setInterval(() => {
  // the dimensions of the canvas will be the same as the dimensions of the video
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
}, 2500); //100000 / FPS 10000

// Function to print last element of array
// This is a temporary method I made to get the last element/ current ASL translation
// Then we print out the last element of the array
function printArrayToHTML(array) {
    // This links the html element with id = 'arrayOutput' to this variable in javascript
    const arrayOutputDiv = document.getElementById('arrayOutput');

    // This clears the output from the previous iteration
    // E.g. if an 'A' is displayed, it will clear that by displaying '' which is nothing
    arrayOutputDiv.innerHTML = '';

    const lastElement = array[array.length - 1];
    arrayOutputDiv.innerHTML = lastElement;

}

// we receive the new frame/image back that has been processed by ASL detection and then we
// update the new source for the image being displayed
socket.on("letter", function (letter) {
  // we push to the global array we made
  letterSequence.push(letter);
  // we then print the sequence
  // currently, it's only printing the last ASL Translation (for testing purposes)
  printArrayToHTML(letterSequence)
});

