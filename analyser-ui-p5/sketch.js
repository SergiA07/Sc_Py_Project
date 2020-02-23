let dictionary;
let maxCentroid;
let minCentroid;
let numbersOnly;

let centroid_data_points = [];

function gotData(data) {
  console.log("DATA!");
  dictionary = data;
  createDiv(JSON.stringify(dictionary.centroid.sample_rate));
  createCentroidDataPoints(dictionary);

  createDiv(numbersOnly);
  createDiv(min);
}

function createCentroidDataPoints(dictionary) {
  numbersOnly = Object.keys(dictionary.centroid.by_values);
  minCentroid = min(numbersOnly);
  maxCentroid = max(numbersOnly);
  for (i = 0; i < numbersOnly.length; i++) {
    data_value = numbersOnly[i];
    let x = map(data_value, minCentroid, maxCentroid, 0, width);
    let y = 100;
    let r = 16;
    let col = color(255, 0, 0, 10);
    let c = new DataPoint(x, y, r, col);
    centroid_data_points.push(c);
  }
}

function sendTestOSCtoSC() {
  console.log("sending OSC");
  sendOsc("/testSC", "hello Supercollider");
}

function setup() {
  button = createButton("test send OSC SC");
  button.position(0, 0);
  button.mousePressed(sendTestOSCtoSC);
  createCanvas(1000, 800);
  setupOsc(13000, 57120); //TODO: take from config.json
  loadJSON("http://127.0.0.1:5002/analysis", gotData); // TODO: The route is hardcoded, should have these constants in config
}

function draw() {
  background(0);
  if (centroid_data_points.length > 0) {
    //randomSeed(4);
    background(100);
    for (let i = 0; i < centroid_data_points.length; i++) {
      centroid_data_points[i].show();
      centroid_data_points[i].onHovered(mouseX, mouseY);
    }
  }
}

class DataPoint {
  constructor(x, y, r, c) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.defaultColor = c;
    this.currentColor = this.defaultColor;
    this.hoveredColor = color(0, 255, 0, 10);
  }

  onHovered(px, py) {
    let d = dist(px, py, this.x, this.y);
    if (d < this.r) {
      this.currentColor = this.hoveredColor;
    } else {
      this.currentColor = this.defaultColor;
    }
  }

  show() {
    noStroke();
    fill(this.currentColor);
    circle(this.x, this.y, this.r * 2);
  }
}

//----  OSC -------
// TODO: Maybe wrap all this code in a class like OSCManager
let socket;

function receiveOsc(address, value) {
  console.log("received OSC: " + address + ", " + value);
  if (address == "/test") {
    x = value[0];
    y = value[1];
  }
}

function sendOsc(address = "/testSC", value = "testValue") {
  socket.emit("sendOSC", address, value);
}

function setupOsc(oscPortIn, oscPortOut) {
  console.log("setup OSC...");
  socket = io.connect("http://127.0.0.1:8081", {
    port: 8081,
    rememberTransport: false
  });
  socket.on("connect", function() {
    socket.emit("config", {
      server: { port: oscPortIn, host: "127.0.0.1" },
      client: { port: oscPortOut, host: "127.0.0.1" }
    });
  });
  socket.on("message", function(msg) {
    console.log("message!!");
    if (msg[0] == "#bundle") {
      for (var i = 2; i < msg.length; i++) {
        receiveOsc(msg[i][0], msg[i].splice(1));
      }
    } else {
      receiveOsc(msg[0], msg.splice(1));
    }
  });
  _socket = socket;
}
