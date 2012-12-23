int cols = 10;
int rows = 80;
int counter = 0;

void setup() {
  size(540, 800);
  background(255);
  stroke(0);

  float horiz = width/cols;
  float vert = horiz/2;

  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      float rand = random(0, 2);    
      if (rand > 1) {
        //draw vertical lines
        for (float k = 0; k < horiz; k+=horiz/8) {
          line(j*horiz+k, i*vert, j*horiz+k, i*vert+vert);
        }
      } 
      else {
        //draw horizontal lines
        for(float k = 0; k < vert; k+=vert/8) {
          line(j*horiz, i*vert+k, j*horiz+horiz, i*vert + k);
        }
      }
    }
  }
}

void draw() {
}

void keyPressed() {
  //saveFrame("Reiner_Schneeberger_Untitled2_####.jpg");
}
