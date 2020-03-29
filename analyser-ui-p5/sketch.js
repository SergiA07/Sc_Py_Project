let dictionary;
let featureCounter = 0;
let data_points = [];
//let config;

function preload() {
    //config = loadJSON("/Users/Sergi/Documents/SuperCollider/Proyectos/Lluis/Python_SC_Pde/config/osc_config.json");
    setupOsc(13000, 57120); //TODO: take from config.json
}


function setup() {
  createCanvas(windowWidth, windowHeight);
  loadJSON("http://127.0.0.1:5002/analysis", gotData); // TODO: The route is hardcoded, should have these constants in config
}

function draw() {
  background(0);
  if (data_points.length > 0) {
    background(80);
    for (let i = 0; i < data_points.length; i++) {
      data_points[i].show();
      data_points[i].onHovered(mouseX, mouseY);
    }
  }
  /*
  button = createButton("test send OSC SC");
  button.position(0, 0);
  button.mousePressed(() => sendOsc("/testSC", "hello Supercollider"));
  */
}


function gotData(data) {
  console.log("DATA!");
  dictionary = data;
  const features = Object.keys(dictionary);
  for(let i=0; i < features.length; i++){
    createDataPoints(dictionary, features[i]);
    featureCounter = featureCounter + 1;
  }
  //createDiv(JSON.stringify(dictionary.centroid.sample_rate));
}

function createDataPoints(dictionary, feature) {
  featureName = feature;
  featureValue = Object.keys(dictionary[featureName].by_values);
  feature_sampleRate = dictionary[featureName].sample_rate;
  feature_fftSize = dictionary[featureName].fft_size;
  minValue = min(featureValue);
  maxValue = max(featureValue);
  for (i = 0; i < featureValue.length; i++) {
    data_value = featureValue[i];
    x = map(data_value, minValue, maxValue, 0, width);
    y = 100 + (featureCounter * 100);
    r = 12;
    col = color(255, y, 0, 50);
    let { path, time_pos } = dictionary[featureName].by_values[data_value];
    start_sample = time_pos * feature_sampleRate;
    frame_dur = feature_fftSize / feature_sampleRate;
    feature_name = featureName;
    data_for_sc = [
        path,
        start_sample,
        frame_dur,
        feature_name
    ];
    sendDataToSC = () => {
      console.log(data_for_sc);
      sendOsc("/data", data_for_sc);
    };
    valuePoint = new DataPoint(x, y, r, featureName, col, sendDataToSC);
    data_points.push(valuePoint);
    }
}

class DataPoint {
  constructor(x, y, r, feature, c, onHoveredCb) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.feature = feature;
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
