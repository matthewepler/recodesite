// This sketch is part of the ReCode Project - http://recodeproject.com
// From Computer Graphics and Art vol2 no4 cover
// by Roger Coqart
// "From the Square Series"
// 
// Benjamin Fox
// 2012
// Creative Commons license CC BY-SA 3.0

int margin = 40;

//specify rows & cols of grid on screen
int screenRows = 3;
int screenCols = 3;
int numScreenCells = screenRows * screenCols;

//specify rows & cols of a grid of tiles
int n = 7;//we're defining as a single var as we want it square
int tileSize = 35;// w / h of the lined tile
int numTiles = n * n;
int centerTile = n/2;

ArrayList lines;

void setup() {
  //set screen size
  int sW = screenRows * n * tileSize + margin;
  int sH = screenCols * n * tileSize + margin;
  size(sW, sH);
  
  //for use later when randomising the lines to draw
  lines = new ArrayList();
  for (int i = 1; i <= 8; i++) {
    lines.add((int) i);
  }
}

void draw() {
  stroke(255);
  strokeWeight(2);
  background(0);
  
  pushMatrix();
  translate(margin/2, margin/2);
  
  for (int i = 0; i < numScreenCells; i++) {
    int x = i % screenRows;
    int y = i / screenCols;
    
    //decides on the density of tiles for the cell we are filling
    if (i % 2 == 0) {
      tile(x, y, 8, 2);//max 8 lines per tile, reducing by 2 from center
    } else {
      tile(x, y, 4, 1);//max 4 lines per tile, reducing by 1 from center
    }
  }
  
  popMatrix();
  
  noLoop();
}

void mouseReleased() {
  loop();
}

void drawLines(int l) {
  //lets randomise the order of lines to draw
  Collections.shuffle(lines);
  
  for (int j = 0; j < l; j++) {
    
    int i = (Integer) lines.get(j);
  
    switch (i) {
      case 1:
        line(0, 0, tileSize, tileSize);
        break;
      case 2:
        line(0, tileSize, tileSize, 0);
        break;
      case 3:
        line(0, tileSize/2, tileSize, tileSize/2);
        break;
      case 4:
        line(tileSize/2, 0, tileSize/2, tileSize);
        break;
      case 5:
        line(0, tileSize/2, tileSize/2, 0);
        break;
      case 6:
        line(tileSize/2, 0, tileSize, tileSize/2);
        break;
      case 7:
        line(tileSize, tileSize/2, tileSize/2, tileSize);
        break;
      case 8:
        line(tileSize/2, tileSize, 0, tileSize/2);
        break;
    }
  }
}

void tile(int col, int row, int maxLines, int reducer) {
  
  pushMatrix();
  translate(col * n * tileSize, row * n * tileSize);
  
  for (int i = 0; i < numTiles; i++) {
    int c = i % n;
    int r = i / n;
    
    int numLines = maxLines - (reducer * max(abs(r - centerTile), abs(c - centerTile)));
    
    pushMatrix();
    translate(c * tileSize, r * tileSize);
    drawLines(numLines);
    
    popMatrix();
  }
  
  popMatrix();
  
}

