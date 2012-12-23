int n = 5;           // bits per dimension
int d = 1<<n;        // cells per dimension
int led = 10;        // size of the dot
int w = led * d + 1; // screen size

int[] preset = {1087, 1157};
int pick = 0;
int p = preset[pick];

boolean debug = true;
int i0, bg;


void setup() {
  size(w, w);
  ellipseMode(CORNER); 
  noStroke();
}


void draw() {
  
  // adding some afterglow
  fill(bg, 30); rect(0, 0, w, w); fill(255 - bg);

  // use mouse coordinates to get initial cell
  int x = mouseX/led & (d-1);
  int y = mouseY/led & (d-1);
  int i = y * d + x;

  // create empty field
  boolean[] field = new boolean[d*d];

  // find all cells in the orbit
  i0 = d*d;
  while (!field[i]) {
    i0 = min(i, i0);
    field[i] = true;
    i *= 2; 
    if (i >= d*d )  i ^= p;
  } 

  // draw display
  for (i = 0; i < d*d; i++) {
    if (field[i]) {
      ellipse(led * (i % d), led * floor(i / d), led, led);
    }
  }
}


void keyPressed() {
  switch(key) {
    // switch between presets
    case ' ':  pick = (pick + 1) % preset.length;  p = preset[pick];  break;
    // next pattern
    case '+': p = (p + 1) | d; break; 
    // previous pattern
    case '-': p = (p - 1) | d; break;
    // toggle debugging
    case 'd': debug = !debug; break;
    // switch background color
    case 'b': bg = 255 - bg; break;
    default: return;
  }
}


void mouseClicked() {
  info();
}


// show generator polynomial + orbit entry point
void info() {
  if (debug) println("p = [" + binary((int) + p, d)+  "] = " + p + "; i0 = " + i0);
}

