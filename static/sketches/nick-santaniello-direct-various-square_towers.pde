int cols = 11;
int rows = 10;
float offsetX;
float offsetY;
int sqSize= 100;
int sizeDifference = 17;

void setup() {
  size(1000, 1000);
  offsetX = random(-6, 6);
  offsetY = random(-6, 6);
  rectMode(CENTER);
  strokeWeight(2);
  fill(240);

  //for every row...
  for (int r = 0; r<rows; r++) {
    //for every column...
    for (int c = 0; c<cols; c++) {
      //choose a new offset
      offsetX = random(-7, 7);
      offsetY = random(-7, 7);
      rect(c*sqSize, r*sqSize, sqSize, sqSize);
      for (int i=1; i<6; i++) {
        rect((c*sqSize)+(i*offsetX), (r*sqSize)+(i*offsetY), sqSize - (i*sizeDifference), sqSize - (i*sizeDifference));
      }
    }
  }
}

void draw() {
}

