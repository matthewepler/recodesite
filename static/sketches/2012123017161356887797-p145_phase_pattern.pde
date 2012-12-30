/* 
Part of the ReCode Project (http://recodeproject.com)
A series of 2 plotter drawings, ink on paper, 50cm x 50cm each, (c) 1973 by Manfred Mohr
First published in Catalog Manfred Mohr, "Drawings Dessins Zeichnungen Dibujos",
Galerie Weiller, Paris and Galerie Gilles Gheerbrant, Montreal, 1974
Re-published in "Computer Graphics and Art" Vol.1 No.4, 1976
https://github.com/downloads/matthewepler/ReCode_Project/COMPUTER_GRAPHICS_AND_ART_Nov1976.pdf
Copyright (c) 2012 Golan Levin - OSI/MIT license (http://recodeproject/license).
*/

int   nLinesAcross  = 133;        // 133 Number of lines across, counted per original
float marginPercent = 0.02857;    // Thickness of margin, measured per original
float strokePercent = 0.25;       // StrokeWeight as a % of horizontal step, estimated per original
int   seriesMode    = 0;          // 0 or 1, depending which member of the series we're rendering

float margin; 
float xLeft, xRight;
float yTop, yBottom; 

int seed1; 
int seed2;
int clickTime = 0;

FPoint storedCurve[];
class FPoint {
  float x; 
  float y;
}


//==========================================================
void setup() {
  size (560, 560, P2D);

  reseed();
  storedCurve = new FPoint[nLinesAcross];
  for (int i=0; i<nLinesAcross; i++) {
    storedCurve[i] = new FPoint();
  }

  margin  = marginPercent * width; 
  xLeft   = margin;
  xRight  = width - margin;
  yTop    = margin;
  yBottom = height - margin;
}


void keyPressed(){
  seriesMode = 1 - seriesMode; 
}

void mousePressed() {
  reseed();
}
void reseed() {
  seed1 = (int) random(10000);
  seed2 = (int) random(10000);
  clickTime = millis(); 
}


//==========================================================
void draw() {
  background (25); 
  stroke (240); 
  strokeCap (ROUND);
  noFill(); 
  smooth(); 

  float stepSize = (xRight-xLeft) / (float)nLinesAcross;
  float lineThickness = strokePercent * stepSize;
  strokeWeight (lineThickness); 

  noiseDetail(2, 0.8); 
  float noiseScale1 = 0.0050;
  float noiseScale2 = 0.0047;
  float minYPercent = 0.30; // determined by inspection of the original
  float maxYPercent = 1.0 - minYPercent;
  float minY = yTop + minYPercent*(yBottom - yTop); 
  float maxY = yTop + maxYPercent*(yBottom - yTop);

  // compute and store first curve
  noiseSeed (seed1); 
  for (int i=0; i<nLinesAcross; i++) {
    float x = map(i, 0, (nLinesAcross-1), xLeft, xRight); 
    float n = noise (x * noiseScale1 +clickTime); 
    float y = map(n, 0, 1, minY, maxY);
    storedCurve[i].x = x; 
    storedCurve[i].y = y;
  }

  // draw first set of vertical lines
  for (int i=0; i<nLinesAcross; i++) {
    float x = storedCurve[i].x;
    float y = storedCurve[i].y;
    line (x, y, x, yBottom);
  }

  beginShape(); 
  for (int i=0; i<nLinesAcross; i++) {
    vertex (storedCurve[i].x, storedCurve[i].y);
  }
  endShape(); 


  // find top of storedCurve
  float curveTop = yBottom; 
  float curveBottom = 0; 
  for (int i=0; i<nLinesAcross; i++) {
    float y = storedCurve[i].y;
    if (y < curveTop) {
      curveTop = y;
    }
    if (y >  curveBottom) {
      curveBottom = y;
    }
  }

  // draw horizontal lines
  boolean bDrawHorizontalLines = true; 
  if (bDrawHorizontalLines) {
    for (int i=0; i<nLinesAcross; i++) {
      float y = map(i, 0, (nLinesAcross-1), yTop, yBottom); 
      if (y <= curveTop) {
        line (xLeft, y, xRight, y);
      } 
      else if ( y > curveBottom) {
        ; // draw no line
      } 
      else {

        float px0 = xLeft;
        int UNDEFINED_EDGE = -1;
        int RISING_EDGE = 0;
        int FALLING_EDGE = 1;
        int mostRecentIntersection = UNDEFINED_EDGE;

        for (int j=0; j<(nLinesAcross-1); j++) {
          float xj = storedCurve[j].x;
          float yj = storedCurve[j].y;
          float xk = storedCurve[j+1].x;
          float yk = storedCurve[j+1].y;
          boolean bIntersectionOnRisingEdge  = ((y <= yj) && (y >= yk));
          boolean bIntersectionOnFallingEdge = ((y >= yj) && (y <= yk));
          boolean bOnLastLine = (j == (nLinesAcross-2));

          if (bIntersectionOnRisingEdge) {
            float px1 = xj + (yj - y)/(yj - yk)*(xk-xj);  
            line (px0, y, px1, y);
            mostRecentIntersection = RISING_EDGE;
            px0 = px1;
          } 
          else if (bIntersectionOnFallingEdge) {
            px0 = xj + (y - yj)/(yk - yj)*(xk-xj); 
            mostRecentIntersection = FALLING_EDGE;
          } 
          else if (bOnLastLine && (mostRecentIntersection == FALLING_EDGE)) {
            line (px0, y, xk, y);
          }
        }
      }
    }
  }


  // Draw second set of vertical lines.
  // Note: noiseSeed() does not seem to be working in ProcessingJS. 
  // The +seed2 and clicktime below are a workaround to overcome this bug. 
  noiseSeed (seed2);
  for (int i=0; i<nLinesAcross; i++) {
    float x = map(i, 0, (nLinesAcross-1), xLeft, xRight); 
    float n = noise (x*noiseScale2 +seed2+clickTime); // see above note. 
    float y = map(n, 0, 1, minY, maxY);
    if (seriesMode == 0){
      line (x+lineThickness+1, yTop, x+lineThickness, y);
    } else {
      line (x+lineThickness+1, y, x+lineThickness, yBottom);
    }
  }
}
