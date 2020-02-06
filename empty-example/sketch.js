/*
let dictionary;

function preload() {
  // Get the most recent earthquake in the database
  let url =
   'http://127.0.0.1:5002/analysis';
   dictionary = loadJSON(url);
   console.log(dictionary);
}
*/

let dictionary;

function gotData(data) {
    dictionary = data;

}

function setup() {
  createCanvas(400, 400)
  loadJSON('http://127.0.0.1:5002/analysis', gotData);
  //createDiv(JSON.stringify(dictionary))
}

function draw() {
    background(0);
    if (dictionary) {
        //randomSeed(4);
        background(100);
        textSize(10)
        text(JSON.stringify(dictionary.centroid.by_values), random(10,300), random(10,300))
    }

    /*
    if (!data) {
    // Wait until the earthquake data has loaded before drawing.
    background(0, 0, 0);
    return;
  }


  background(200, 100, 300)
  textSize(10)
  text("fast", random(10,300), random(10,300))


  background(0);
  for (var i=0; i<data.centroid; i++) {
      fill(225);
      ellipse(random(width), random(height), 8, 8);
  }
  */
}
