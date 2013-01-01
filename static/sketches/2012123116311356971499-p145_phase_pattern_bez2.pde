/*
Part of the ReCode Project (http://recodeproject.com)
A series of 2 plotter drawings, ink on paper, 50cm x 50cm each, (c) 1973 by Manfred Mohr
First published in Catalog Manfred Mohr, "Drawings Dessins Zeichnungen Dibujos",
Galerie Weiller, Paris and Galerie Gilles Gheerbrant, Montreal, 1974
Re-published in "Computer Graphics and Art" Vol.1 No.4, 1976
https://github.com/downloads/matthewepler/ReCode_Project/COMPUTER_GRAPHICS_AND_ART_Nov1976.pdf
Copyright (c) 2012 Golan Levin - OSI/MIT license (http://recodeproject/license).

This version reproduces the exact 3rd-order spline curves used in Mohr's original. 
See: http://www.emohr.com/sc69-73/vfile_145.html
*/


int   nLinesAcross  = 133;        // Number of lines across, counted per original
float marginPercent = 0.02857;    // Thickness of margin, measured per original
float strokePercent = 0.25;       // StrokeWeight as a % of line step, estimated per original
int   seriesMode    = 0;          // 0 or 1, depending which of the series we're rendering

float margin; 
float xLeft, xRight;
float yTop, yBottom; 

SplineSegmentCollection curveA;
SplineSegmentCollection curveB; 

FPoint storedCurve[];
class FPoint {
  float x; 
  float y;
}


//==========================================================
void setup() {
  size (560, 560, P2D);

  storedCurve = new FPoint[nLinesAcross];
  for (int i=0; i<nLinesAcross; i++) {
    storedCurve[i] = new FPoint();
  }

  margin  = marginPercent * width; 
  xLeft   = margin;
  xRight  = width - margin;
  yTop    = margin;
  yBottom = height - margin;

  initializeSplineSegmentCollections();
  
  // Compute and store first curve
  for (int i=0; i<nLinesAcross; i++) {
    float x = map(i, 0, (nLinesAcross-1), 0, 1);
    float y = curveA.cubicBezierLookup (x); 
    x = map(x, 0, 1, xLeft, xRight); 
    y = map(y, 0, 1, yTop, yBottom); 
    storedCurve[i].x = x; 
    storedCurve[i].y = y;
  }
}


//==========================================================
void initializeSplineSegmentCollections() {
  
  // These are cubic Bezier control points in the format {x,y,x,y,x,y,x,y}
  // which duplicate, to the best of my abilities, the cubic splines used in
  // the original by Manfred Mohr: http://www.emohr.com/sc69-73/vfile_145.html.
  // Mohr's original randomization technique for producing these is otherwise unknown.
  // The numbers have been normalized in the range 0...1. 

  float ctrlPtsA0[] = {-0.09318,0.65749, 0.00986,0.65749, 0.02457,0.46173, 0.08051,0.46173};
  float ctrlPtsA1[] = { 0.08051,0.46173, 0.10847,0.46173, 0.14233,0.60598, 0.17324,0.60598};
  float ctrlPtsA2[] = { 0.17324,0.60598, 0.22328,0.60598, 0.32043,0.39402, 0.43818,0.39402};
  float ctrlPtsA3[] = { 0.43818,0.39402, 0.47792,0.39402, 0.53533,0.41169, 0.57948,0.41169};
  float ctrlPtsA4[] = { 0.57948,0.41169, 0.64719,0.41169, 0.73992,0.39255, 0.81646,0.39255};
  float ctrlPtsA5[] = { 0.81646,0.39255, 0.95629,0.39255, 1.10201,0.57654, 1.13733,0.57654};

  float ctrlPtsB0[] = {-0.15500,0.34987,-0.10790,0.34987, 0.00544,0.52355, 0.13202,0.52355};
  float ctrlPtsB1[] = { 0.13202,0.52355, 0.24094,0.52355, 0.27333,0.38666, 0.31012,0.38666};
  float ctrlPtsB2[] = { 0.31012,0.38666, 0.34251,0.38666, 0.41905,0.57507, 0.47056,0.57507};
  float ctrlPtsB3[] = { 0.47056,0.57507, 0.50000,0.57507, 0.50883,0.52797, 0.53238,0.52797};
  float ctrlPtsB4[] = { 0.53238,0.52797, 0.55004,0.52797, 0.56624,0.53680, 0.58684,0.53680};
  float ctrlPtsB5[] = { 0.58684,0.53680, 0.66191,0.53680, 0.71048,0.45731, 0.81204,0.45731};
  float ctrlPtsB6[] = { 0.81204,0.45731, 0.94893,0.45731, 1.04166,0.55299, 1.10495,0.55299};

  // Init the first curve, using those control points. 
  float ctrlPtsA[][] = new float[6][];
  ctrlPtsA[0] = ctrlPtsA0;
  ctrlPtsA[1] = ctrlPtsA1;
  ctrlPtsA[2] = ctrlPtsA2;
  ctrlPtsA[3] = ctrlPtsA3;
  ctrlPtsA[4] = ctrlPtsA4;
  ctrlPtsA[5] = ctrlPtsA5;
  curveA = new SplineSegmentCollection(6, ctrlPtsA); 
 
  // Init the second curve, using those control points. 
  float ctrlPtsB[][] = new float[7][];
  ctrlPtsB[0] = ctrlPtsB0;
  ctrlPtsB[1] = ctrlPtsB1;
  ctrlPtsB[2] = ctrlPtsB2;
  ctrlPtsB[3] = ctrlPtsB3;
  ctrlPtsB[4] = ctrlPtsB4;
  ctrlPtsB[5] = ctrlPtsB5;
  ctrlPtsB[6] = ctrlPtsB6;
  curveB = new SplineSegmentCollection(7, ctrlPtsB);
}

//==========================================================
void keyPressed() {
  seriesMode = 1 - seriesMode;
}

//==========================================================
void mousePressed() {
  seriesMode = 1 - seriesMode;
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

  // Draw first set of vertical lines, down from the first curve
  for (int i=0; i<nLinesAcross; i++) {
    float x = storedCurve[i].x;
    float y = storedCurve[i].y;
    line (x, y, x, yBottom);
  }

  // Draw the outline of the first curve, itself
  beginShape(); 
  for (int i=0; i<nLinesAcross; i++) {
    vertex (storedCurve[i].x, storedCurve[i].y);
  }
  endShape(); 


  // Search for top and bottom of storedCurve
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

  // Draw horizontal lines
  for (int i=0; i<nLinesAcross; i++) {
    float y = map(i, 0, (nLinesAcross-1), yTop, yBottom); 
    if (y <= curveTop) {
      line (xLeft+lineThickness, y, xRight, y);
    } 
    else if ( y > curveBottom) {
      ; // draw no line
    } 
    else {

      float px0 = xLeft + lineThickness;
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

  // Draw the second set of vertical lines.
  for (int i=0; i<nLinesAcross; i++) {
    float x = map(i, 0, (nLinesAcross-1), 0, 1); 
    float y = curveB.cubicBezierLookup (x); 
    x = map(x, 0, 1, xLeft, xRight); 
    y = map(y, 0, 1, yTop, yBottom); 

    if (seriesMode == 0) {
      line (x+lineThickness+1, yTop, x+lineThickness, y);
    } 
    else {
      line (x+lineThickness+1, y, x+lineThickness, yBottom);
    }
  }
}



//==========================================================
class SplineSegmentCollection {
  int nSplineSegments;
  SplineSegment segments[];

  SplineSegmentCollection (int nSegs, float[][] controlPoints) {
    nSplineSegments = nSegs;
    segments = new SplineSegment[nSplineSegments]; 
    for (int i=0; i<nSplineSegments; i++) {
      segments[i] = new SplineSegment(); 

      segments[i].x0 = controlPoints[i][0];
      segments[i].y0 = controlPoints[i][1];
      segments[i].x1 = controlPoints[i][2];
      segments[i].y1 = controlPoints[i][3];
      segments[i].x2 = controlPoints[i][4];
      segments[i].y2 = controlPoints[i][5];
      segments[i].x3 = controlPoints[i][6];
      segments[i].y3 = controlPoints[i][7];
    }
  }
  
  //---------------------------------------
  float cubicBezierLookup (float x) {
    float y = 0; 
    int whichSegment = inWhichSegmentIsXValueContained (x); 
    if (whichSegment != -1) {
      y = segments[whichSegment].cubicBezierLookup (x);
    }
    return y;
  }

  //---------------------------------------
  int inWhichSegmentIsXValueContained(float x) {
    int whichSegment = -1; 
    for (int s=0; s<nSplineSegments; s++) {
      if ((x >= segments[s].x0) && (x <= segments[s].x3)) {
        whichSegment = s;
      }
    }
    return whichSegment;
  }

}


//==========================================================
class SplineSegment {
  float x0;  // initial x 
  float y0;  // initial y
  float x1;  // 1st influence x 
  float y1;  // 1st influence y   
  float x2;  // 2nd influence x
  float y2;  // 2nd influence y
  float x3;  // final x 
  float y3;  // final y 

  //---------------------------------------
  float cubicBezierLookup (float queryx) {

    // Assume control points of (0,0), (a,b), (c,d), and (1,1); 
    // Given horizontal query point x between 0...1 
    // Return function value y (also in the range 0...1).

    // Adapted from BEZMATH.PS (1993) by Don Lancaster, Synergetics Inc. 
    // http://www.tinaja.com/text/bezmath.html

    float A =   x3 - 3*x2 + 3*x1 - x0;
    float B = 3*x2 - 6*x1 + 3*x0;
    float C = 3*x1 - 3*x0;   
    float D =   x0;

    float E =   y3 - 3*y2 + 3*y1 - y0;    
    float F = 3*y2 - 6*y1 + 3*y0;             
    float G = 3*y1 - 3*y0;             
    float H =   y0;

    // Solve for t given x (using Newton-Raphelson), then solve for y given t.
    // Assume for the first guess that t = 0.5. (Could also use queryx if in 0...1)
    float currentt = 0.5; 
    int nRefinementIterations = 5;
    for (int i=0; i<nRefinementIterations; i++) {
      float currentx = xFromT (currentt, A, B, C, D); 
      float currentslope = slopeFromT (currentt, A, B, C);
      currentt -= (currentx - queryx)*(currentslope);
      currentt = constrain(currentt, 0, 1);
    } 

    float y = yFromT (currentt, E, F, G, H);
    return y;
  }

  //----------------------------------------------------------
  float slopeFromT (float t, float A, float B, float C) {
    float dtdx = 1.0/(3.0*A*t*t + 2.0*B*t + C); 
    return dtdx;
  }
  //----------------------------------------------------------
  float xFromT (float t, float A, float B, float C, float D) {
    float x = A*(t*t*t) + B*(t*t) + C*t + D;
    return x;
  }
  //----------------------------------------------------------
  float yFromT (float t, float E, float F, float G, float H) {
    float y = E*(t*t*t) + F*(t*t) + G*t + H;
    return y;
  }
}
