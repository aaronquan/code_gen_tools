precision medium float;

varying vec2 position;

uniform vec3 colour;

float circle(in vec2 _st, in float _radius){
    float radius = _radius*_radius;
    vec2 dist = _st-vec2(0.5);
	return 1.-smoothstep(radius-(radius*0.01),
                         radius+(radius*0.01),
                         dot(dist,dist)*4.0);
}

vec3 getColour();

void main(){
  float circ = circle(position, 1.0);
  vec3 colour = getColour()*circ;
	gl_FragColor = vec4(vec3(colour), circ);
}

vec3 getColour(){
    return vec3(colour);
}