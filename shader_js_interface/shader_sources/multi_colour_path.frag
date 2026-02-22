precision mediump float;

varying vec2 v_position;
varying vec2 v_relative;

uniform vec3 u_left_colour;
uniform vec3 u_right_colour;
uniform vec3 u_top_colour; // colour
uniform vec3 u_bot_colour;
uniform vec3 u_mid_colour;
uniform float u_size; // between 0 and 0.5
uniform vec3 u_background_colour;

void main(){
  vec2 uv = v_relative;
  float sz = u_size/2.;

  float vertical = step(abs(0.5-uv.x), sz);
  float horizontal = step(abs(0.5-uv.y), sz);
  
  float top = vertical*step(0.5+sz, uv.y);
  float bottom = vertical*step(uv.y, 0.5-sz);
  float left = horizontal*step(uv.x, 0.5-sz);
  float right = horizontal*step(0.5+sz, uv.x);
  
  float mid = horizontal*vertical;

  float background = 1.0-(top+bottom+left+right+mid);

  vec3 colour = top*u_top_colour+bottom*u_bot_colour+left*u_left_colour+right*u_right_colour+mid*u_mid_colour+background*u_background_colour;

  gl_FragColor = vec4(colour, 1.0);
}