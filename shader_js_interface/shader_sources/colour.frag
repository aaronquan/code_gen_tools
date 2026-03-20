precision mediump float;



uniform vec3 colour; //colour

void main(){
  gl_FragColor = vec4(colour, 1.0);
}