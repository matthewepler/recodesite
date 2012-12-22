void setup()
{
 size(500, 500); 
}

void draw()
{
 ranX = random( 0, width );
 ranY = random( 0, height );
 
 fill( random( 0, 255 ), random( 0, 255 ), random( 0, 255 ) );
 noStroke();
 ellipse( ranX, ranY, 50, 50 ); 
}
