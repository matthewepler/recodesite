int n = 5;           // bits per dimension
int d = 1<<n;        // cells per dimension
int led = 10;        // size of the dot
int w = led * d + 1; // screen size

int[] preset = { 1087, 1087, 1157, 1157 };
int[] offset = { 2, 31, 9, 15 }; 
int pick;


void setup() {
 size(w, w);
 ellipseMode(CORNER); 
 stroke(255);
 fill(0); 
 smooth();
}


void draw() {
  
  int p = preset[pick];
  int i = offset[pick];
  
  // create empty field
  boolean[] field = new boolean[d*d];

  // find all cells in the orbit
  while(!field[i]) {
    field[i] = true;
    i *= 2; 
    if(i >= d*d )  i ^= p;
  } 
  
  // draw display
  background(255); 
  for(i = 0; i < d*d; i++) {
    if(field[i]) { 
      ellipse( led * (i % d), led * (i / d), led, led);
    }
  }
   
}


void keyPressed() {
  pick = (pick + 1) % preset.length;
}
