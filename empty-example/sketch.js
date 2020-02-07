
let dictionary;
let maxCentroid
let minCentroid
let numbersOnly

let centroid_data_points = [];

function gotData(data) {
    console.log('DATA!')
    dictionary = data;
    createDiv(JSON.stringify(dictionary.centroid.sample_rate));
    createCentroidDataPoints(dictionary)

    createDiv(numbersOnly);
    createDiv(min)
}

function createCentroidDataPoints(dictionary){
    numbersOnly = Object.keys(dictionary.centroid.by_values);
    minCentroid = min(numbersOnly)
    maxCentroid = max(numbersOnly)
    for (i=0; i<numbersOnly.length; i++) {
        data_value = numbersOnly[i];
        let x = map(data_value, minCentroid, maxCentroid, 0, width);
        let y = 100;
        let r = 16;
        let col = color(255,0,0, 10);
        let c = new DataPoint(x,y,r,col);
        centroid_data_points.push(c);
  }
}

function setup() {
  createCanvas(1000, 800)
  loadJSON('http://127.0.0.1:5002/analysis', gotData);
}

function draw() {
    background(0);
    if (centroid_data_points.length > 0) {
        //randomSeed(4);
        background(100);
        for(let i = 0; i<centroid_data_points.length; i++) {
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
    this.currentColor = this.defaultColor
    this.hoveredColor =  color(0,255,0,10)
}

  onHovered(px, py) {
    let d = dist(px, py, this.x, this.y);
    if (d < this.r) {
        this.currentColor = this.hoveredColor;
    } else{
        this.currentColor = this.defaultColor
    }
  }

  show() {
    noStroke();
    fill(this.currentColor);
    circle(this.x, this.y, this.r * 2);
  }
}
