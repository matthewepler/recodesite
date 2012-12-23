int[] preset = { 4294967295l, 100675584l, 2146959392l, 4293918847l };

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
