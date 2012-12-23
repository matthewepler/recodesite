int d = 1<<5;            // cells per dimension
int led = 10;            // size of the light bulb
int w = led * d + 1;     // display size
int pick = 1;            // picked preset

// we need the long datatype, because we have 32 bit positive integers
long[] preset= { 4294967295l, 100675584l, 2146959392l, 4293918847l };

// there are 2^32 different patterns controlled by the 32 bits of p
long p = preset[pick];

// the generator is used to create a more interesting pattern sequence
long generator = 4299161607l; 

int frames = 60;
boolean animate = true;
boolean debug = true;
boolean glow = true;

void setup() {
 size(w, w);
 info();
}


void draw() {

  // add some afterglow
  fill(0, glow ? 30 : 255); rect(0, 0, w, w); fill(255);
  
  // draw the pattern
  for(int y = 0; y < d; y++) {
    for(int x = 0; x < d; x++) {
      
      // this is where the magic happens
      if( (1l<<(x ^ y) & p ) > 0) {   
        rect(led * x, led * y, led, led);
      }
      
    }
  }
  
  // jump to a different pattern
  if( animate && frameCount % frames == 0) {
    p *= 2;
    if(p >= 1l<<d) p ^= generator;
    info();
  } 
    
  // change the pattern using the mouse
  if(mousePressed) {
    int x = (mouseX/led) & d-1;
    int y = (mouseY/led) & d-1;
    long bit = 1l<<(x ^ y);
    p = mouseButton == LEFT ? p | bit : p & ~bit;
    info();
  }

}


void keyPressed() {
  
  switch(key) {
    // animation on/off
    case ' ': animate = ! animate;  return;
    // switch between presets
    case 'p': p = preset[pick = (pick + 1) % preset.length]; animate = false; break;
    // next pattern
    case '+': p++; break;
    // previous pattern
    case '-': p--; break;
    // toggle afterglow
    case 'g': glow = !glow; break;
    // toggle debugging
    case 'd': debug = !debug;
    default: return;
  }
  
  // constrain to 32 bits
  p &= ((1l<<d) - 1) ;
  info();
}


// show pattern input
void info() {
  if(debug) println("p = [" + binary((int) + p, d)+  "] = " + p ); 
}


