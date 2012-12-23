void setup() {

  size(800, 800);
  rectMode(CENTER);
  strokeWeight(2);
  // Create 36 crosses.
  Cross[] crosses;
  crosses = new Cross[36];
  translate(100, 300);

  //for every row...
  for (int r = 0; r<6; r++) {
    //for every column...
    for (int c = 0; c<6; c++) {
      pushMatrix();
      translate(80*c+r*40, -40*c + r*80);

      //rotate 180 degrees per column.
      rotate(PI* c);

      //rotate 90 degrees per row
      rotate(PI/2 * r);

      Cross newCross = new Cross(0, 0);
      newCross.display();
      popMatrix();
    }
  }
}

void draw() {
}

class Cross {

  int baseW = 40;
  int baseH = 120;
  int sizeDifference = 8;
  int x;
  int y;
  int offset = 2;

  Cross(int xVal, int yVal) {
    x = xVal;
    y = yVal;
  };

  void display() {
    
    //I draw each cross as two intersecting rectangles.
    //By drawing two rectangles and a small white square in the middle, I can leverage rectMode(CENTER) as opposed to maintaining 12 seperate line segments per cross. This is my justification for this hack.
   
    rect(x, y, baseW, baseH);
    rect(x, y, baseH, baseW);
    //draw the white box
    stroke(255);
    rect(x, y, baseW, baseW);
    stroke(0);
    
    //draw 4 crosses inside each cross.
    for (int i = 1; i<=4; i++) {
      int w = baseW - i*sizeDifference;
      int h = baseH - i*sizeDifference;
      rect(x, y+offset*i, w, h);
      rect(x, y+offset*i, h, w);
      stroke(255);
      rect(x, y+offset*i, w, w);
      stroke(0);
    }
  }
}