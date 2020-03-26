let dictionary;
let maxCentroid;
let minCentroid;
let numbersOnly;
let featureCounter = 0;

let centroid_data_points = [];

function setup() {
  button = createButton("test send OSC SC");
  button.position(0, 0);
  button.mousePressed(() => sendOsc("/testSC", "hello Supercollider"));
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


function gotData(data) {
  console.log("DATA!");
  dictionary = data;
  const features = Object.keys(dictionary);
  for(i=0; i < features.length; i++){
      createDataPoints(dictionary, features[i]);
      createDiv(features[i]);
      featureCounter = featureCounter + 1;
  }
  //createDiv(JSON.stringify(dictionary.centroid.sample_rate));
}

function createDataPoints(dictionary, feature) {
  createDiv(typeof feature);
  featureName = feature;
  numbersOnly = Object.keys(dictionary[featureName].by_values);
  let feature_sampleRate = dictionary[featureName].sample_rate;
  let feature_fftSize = dictionary[featureName].fft_size;
  minValue = min(numbersOnly);
  maxValue = max(numbersOnly);
  for (i = 0; i < numbersOnly.length; i++) {
    data_value = numbersOnly[i];
    let x = map(data_value, minValue, maxValue, 0, width);
    let y = 100 + (featureCounter * 200);
    let r = 16;
    let col = color(255, y, 0, 10);
    let { path, time_pos } = dictionary[featureName].by_values[data_value];
    let start_sample = time_pos * feature_sampleRate;
    let frame_dur = feature_fftSize / feature_sampleRate;
    let feature_name = featureName; // TODO: right now is "centroid", but it could be anything
    let data_for_sc = [
        path,
        start_sample,
        frame_dur,
        feature_name
    ];
    let sendDataToSC = () => {
      console.log(data_for_sc);
      sendOsc("/data", data_for_sc);
    };
    let c = new DataPoint(x, y, r, col, sendDataToSC);
    centroid_data_points.push(c);
  }
}

class DataPoint {
  constructor(x, y, r, c, onHoveredCb) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.onHoveredCb = onHoveredCb;
    this.defaultColor = c;
    this.currentColor = this.defaultColor;
    this.hoveredColor = color(0, 255, 0, 10);
  }

  onHovered(px, py) {
    let d = dist(px, py, this.x, this.y);
    if (d < this.r) {
      this.currentColor = this.hoveredColor;
      this.onHoveredCb();
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
