// this sketch simply creates the 4 patterns of the 3rd image 
// in the article from the pattern presets given below. 

// Press any key to switch between patterns

long[] preset = { 196632,  25362456l , 143654784, 4278196223l  };

int d = 1<<5;            // cells per dimension
int led = 10;            // size of the light bulb
int w = led * d + 1;     // display size
int p = 0;

void setup() {
 size(w, w);
}

void draw() {
  background(0);  
  for(int y = 0; y < d; y++) {
    for(int x = 0; x < d; x++) {
      if( (1l<<(x^y) & preset[p] ) > 0) {
        rect(led * x, led * y, led, led);
      }
    }
  }
}

void keyPressed() {
  p = (p + 1) % preset.length;
}
