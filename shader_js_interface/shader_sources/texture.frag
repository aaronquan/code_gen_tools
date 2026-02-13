precision mediump float;

varying vec2 v_position;
varying vec2 v_relative;


uniform sampler2D u_texture_id;

void main(){
    gl_FragColor = texture2D(u_texture_id, v_relative);
}