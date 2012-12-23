int gridSize = 30;
int density = 7;

void setup(){
  size(480, 720);
  background(255);
  
  stroke(0);
  strokeWeight(1);
  float padding = gridSize/(float)density;    // even spacing for lines
          
  int rows = height/gridSize;
  int cols = width/gridSize;
  
  for(int i = 0; i < rows; i++){        // iterate over the # of rows (top to bottom)
    for(int j = 0; j < cols; j++){      // iterate over the # of columns (left to right)
      
      pushMatrix();
      translate(j*gridSize, i*gridSize);      // move to grid location
      translate(gridSize/2.f, gridSize/2.f);  // move to rotate around center
      
      float prob = map(j/(float)cols, 0, 1, .2, .8);  // probability between .2 and .8
      if(random(1) < prob)             // higher probability vertical on the left side
        rotate(3*PI/2);                // rotate horizontal
      else
        rotate(PI);
        
      for(int k = 0; k < density; k++){          // draw # of lines based on density with even spacing
        float _x = (k - density/2.f) * padding;  
        line(_x, -gridSize/2.f, _x, gridSize/2.f);
      }
      popMatrix();
    }
  }
}
