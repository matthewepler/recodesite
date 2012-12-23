/*
 methods:
 1. vernacular
   preserve the spirit of the image
   least work
   but the influence of the original tool is lost
 2. rosetta
   preserve the spirit of the code itself
   connects old languages to new languages
 3. revival
   write a parser to run the original code
   most work
   preserves everything but the output medium (plotter)
*/

/*
// JOB
// FOR RDMSQ
*NONPROCESS PROGRAM
*ONE WORD INTEGERS
*LIST SOURCE PROGRAM
*INCS(CARD,1443 PRINTER)
C******************PROGRAMMED FOR COMPUTER GRAPHICS AND ART BY BILL KULOMYJEC
      DIMENSION A(4,2),B(4,2),AA(4,2),BB(4,2)
C                  PROVIDE MEMORY FOR 2 SETS OF SQUARES, RANDOMIZE
      CALL RANST
C                  DEFINE VARIABLES
      NUMX=5
      NUMY=7
C                  BSS=THE SIZE OF THE SIDE OF THE SQUARE, SSPCT=THE PERCENT
C                  OF THE SIZE OF THE INSIDE SQUARE
      BSS=1.25
      SSPCT=0.20
      HFBSS=BSS/2.0
C                  VLIMIT IS THE MAXIMUM AMOUNT THE INNER SQUARE MAY VARY
      VLIMT=HFBSS-(BSS*SSPCT/2.0)
C                  SET UP CORNERS OF BIG SQUARE
      A(1,1)= HFBSS
      A(1,2)= HFBSS
      A(2,1)=-HFBSS
      A(2,2)= HFBSS
      A(3,1)=-HFBSS
      A(3,2)=-HFBSS
      A(4,1)= HFBSS
      A(4,2)=-HFBSS
C                  SCALE DOWN SMALL SQUARE BY SSPCT
      DO 100 J=1,4
      DO 100 K=1,2
  100 B(J,K)=A(J,K)*SSPCT
C                  INITIALIZE PLOTTER
      CALL HYPLT (0.,0.,0)
C                  BEGIN DRAWING RANDOM SQUARE MODULES
      DO 200 J=1,NUMY
      YC=FLOAT(J-1)*BSS
      DO 200 K=1,NUMX
      XC=FLOAT(K-1)*BSS
C                  ADJUST OUTER SQUARE TO RELATIVE LOCATION
      DO 201  L=1,4
      AA(L,1)=A(L,1)+XC
      AA(L,2)=A(L,2)+YC
  201 CONTINUE
C                  DETERMINE X AND Y VARIANCE BASED ON VLIMT
      XVAR=RANF(0)*VLIMT-(VLIMT/2.0)
      YVAR=RANF(0)*VLIMT-(VLIMT/2.0)
C                  ADJUST INNER SQUARE TO RELATIVE LOCATION, ADD VARIANCE
      DO 202 M=1,4
      BB(M,1)=B(M,1)+XVAR+XC
      BB(M,2)=B(M,2)+YVAR+YC
  202 CONTINUE
C                  DETERMINE RANDOM NUMBER OF INTERVALS (BETWEEN 2 AND 10)
      NSPCS=9*RANF(D)+2
C                  PLOT EACH MODULE
      DO 203 N=1,NSPCS
C                  P CALCULATES RELATIVE SPACING ON NSPCS
      P=FLOAT(N-1)/(NSPCS-1)
      X=AA(4,1)+P*(BB(4,1)-AA(4,1))
      Y=AA(4,2)+P*(BB(4,2)-AA(4,2))
C                  MOVE THE PEN TO THE LAST CORNER OF THE SQUARE
      CALL HYPLT (X,Y,2)
C                  PLOT INTERMEDIATE SQUARES
      DO 300 I=1,4
      X=AA(I,1)+P*(BB(I,1)-AA(I,1))
      Y=AA(I,2)+P*(BB(I,2)-AA(I,2))
  300 CALL HYPLT (X,Y,1)
  203 CONTINUE
  200 CONTINUE
C                  TERMINATE
      CALL HYPLT (0.,0.,-1)
      CALL EXIT
      END

FEATURES SUPPORTED
 NONPROCESS
 ONE WORD INTEGERS
 INCS

CORE REQUIREMENTS FOR RDMSQ
 COMMON    O  INSKEL COMMON    0  VARIABLES    110  PROGRAM    444
*/

void setup() {
  size(500, 700);
  background(255);
  noLoop();
}

void draw() {
  //vernacular();
  rosetta();
}

void vernacular() {
  rectMode(CENTER);
  noFill();
  float side = 100;
  for(int y = 0; y < 7; y++) {
    for(int x = 0; x < 5; x++) {
      int n = int(random(2, 11));
      float ox = random(side / 2) + side / 4;
      float oy = random(side / 2) + side / 4;
      for(int i = 0; i < n; i++) {
        float curSide = map(i, 0, n - 1, .2, 1) * side;
        float cx = x * side + map(i, 0, n - 1, ox, side / 2);
        float cy = y * side + map(i, 0, n - 1, oy, side / 2);
        rect(cx, cy, curSide, curSide);
      }
    }
  }
}



/*
 translation notes:
 * BASIC uses 1-indexed arrays, Java uses 0-indexed arrays
 * lines with  //? have no corollary in this environment
 * with a few exceptions, there is no decorative whitespace in the original code
 * RANF(0) corresponds to random(1)
 * the HYPLT plotter interface is replaced with beginShape/endShape helper functions
*/

void rosetta() {
  // ******************PROGRAMMED FOR COMPUTER GRAPHICS AND ART BY BILL KULOMYJEC
  float[][]
    A = new float[4][2],
    B = new float[4][2],
    AA = new float[4][2],
    BB = new float[4][2];
  // PROVIDE MEMORY FOR 2 SETS OF SQUARES, RANDOMIZE
  randomSeed(0); //CALL RANST
  // DEFINE VARIABLES
  int NUMX=5;
  int NUMY=7;
  // BSS=THE SIZE OF THE SIDE OF THE SQUARE, SSPCT=THE PERCENT
  // OF THE SIZE OF THE INSIDE SQUARE
  float BSS=1.25;
  float SSPCT=0.20;
  float HFBSS=BSS/2.0;
  // VLIMIT IS THE MAXIMUM AMOUNT THE INNER SQUARE MAY VARY
  float VLIMT=HFBSS-(BSS*SSPCT/2.0);
  // SET UP CORNERS OF BIG SQUARE
  A[0][0]= HFBSS;
  A[0][1]= HFBSS;
  A[1][0]=-HFBSS;
  A[1][1]= HFBSS;
  A[2][0]=-HFBSS;
  A[2][1]=-HFBSS;
  A[3][0]= HFBSS;
  A[3][1]=-HFBSS;
  // SCALE DOWN SMALL SQUARE BY SSPCT
  for(int J=0;J<4;J++) {
    for(int K=0;K<2;K++) {
      B[J][K]=A[J][K]*SSPCT;
    }
  }
  // INITIALIZE PLOTTER
  HYPLT(0.,0.,0);
  // BEGIN DRAWING RANDOM SQUARE MODULES
  for(int J=0;J<NUMY;J++) {
    float YC=float(J)*BSS;
    for(int K=0;K<NUMX;K++) {
      float XC=float(K)*BSS;
      // ADJUST OUTER SQUARE TO RELATIVE LOCATION
      for(int L=0;L<4;L++) {
        AA[L][0]=A[L][0]+XC;
        AA[L][1]=A[L][1]+YC;
      }
      // DETERMINE X AND Y VARIANCE BASED ON VLIMT
      float XVAR=random(1)*VLIMT-(VLIMT/2.0);
      float YVAR=random(1)*VLIMT-(VLIMT/2.0);
      // ADJUST INNER SQUARE TO RELATIVE LOCATION, ADD VARIANCE
      for(int M=0;M<4;M++) {
        BB[M][0]=B[M][0]+XVAR+XC;
        BB[M][1]=B[M][1]+YVAR+YC;
      }
      // DETERMINE RANDOM NUMBER OF INTERVALS (BETWEEN 2 AND 10)
      int NSPCS=int(9*random(1)+2);
      // PLOT EACH MODULE
      for(int N=0;N<NSPCS;N++) {
        // P CALCULATES RELATIVE SPACING ON NSPCS
        float P=float(N)/(NSPCS-1);
        float X=AA[3][0]+P*(BB[3][0]-AA[3][0]);
        float Y=AA[3][1]+P*(BB[3][1]-AA[3][1]);
        // MOVE THE PEN TO THE LAST CORNER OF THE SQUARE
        HYPLT(X,Y,2);
        // PLOT INTERMEDIATE SQUARES
        for(int I=0;I<4;I++) {
          X=AA[I][0]+P*(BB[I][0]-AA[I][0]);
          Y=AA[I][1]+P*(BB[I][1]-AA[I][1]);
          HYPLT(X,Y,1);
        }
      }
    }
  }
  // TERMINATE
  HYPLT(0.,0.,-1);
  // CALL EXIT //?
  // END //?
}

// HYPLT implementation with beginShape/endShape
int plotterState = UP;
void penDown() {
  if(plotterState == UP) {
    noFill();
    beginShape();
    plotterState = DOWN;
  }
}
void penUp() {
  if(plotterState == DOWN) {
    endShape(CLOSE);
    plotterState = UP;
  }
}
void penMove(float x, float y) {
  vertex(x,y);
}
void HYPLT(float x, float y, int mode) {
  if(mode == -1) { // finish
    penUp();
  } else if(mode == 0) { // initialize
    strokeWeight(0);
    noSmooth();
    // original used the range (-0.625, -0.625) to (5.625, 8.15)
    // perhaps in or cm? we use 80x zoom to convert to pixels.
    scale(80, 80);
    translate(.625,.625);
  } else if(mode == 1) { // down + move
    penDown();
    penMove(x, y);
  } else if(mode == 2) { // close/up
    penUp();
  }
}

