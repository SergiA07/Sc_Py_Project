let dictionary;

function preload() {
  // Get the most recent earthquake in the database
  let url =
   'http://127.0.0.1:5002/analysis';
   dictionary = loadJSON(url);
   console.log(dictionary);
}




function setup() {
  createCanvas(400, 400)
  createDiv(JSON.stringify(dictionary))
}

function draw() {
    if (!dictionary) {
    // Wait until the earthquake data has loaded before drawing.
    background(0, 0, 0);
    return;
  }


  background(200, 100, 300)
  textSize(10)
  text("fast", random(10,300), random(10,300))
}
