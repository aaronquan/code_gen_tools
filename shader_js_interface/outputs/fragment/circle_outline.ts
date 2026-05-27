import * as Shader from './../../shader';
import * as WebGL from './../../../globals';

const CircleOutline = `precision mediump float;

varying vec2 v_position;
varying vec2 v_relative;

uniform vec2 u_centre;
uniform float u_radius;
uniform float u_outline_radius;

uniform vec4 u_outline_colour;
uniform vec4 u_background_colour;

void main(){
  vec2 middle = vec2(u_centre);
  float d = distance(middle, v_relative);
  float circle = step(d, u_radius);
  float centre_circle = step(d, u_radius-u_outline_radius);

  float in_outline = circle-centre_circle;

  vec4 col = u_outline_colour*in_outline;
  gl_FragColor = col;
}`;

export class CircleOutlineFragmentShader{
  static shader?: Shader.FragmentShader;
  static load(){
    if(this.shader == undefined){
      this.shader = new Shader.FragmentShader();
      if(!this.shader.addSource(CircleOutline)){
        console.log('CircleOutline: fragment source not added');
      }
    }
  }
}

export function CircleOutlineShaderProgramMix<TBase extends Shader.CustomShaderProgramable>(Base: TBase){
  return class CircleOutline extends Base{
    private declare centre_uniform_location: WebGLUniformLocation | null;
    private declare radius_uniform_location: WebGLUniformLocation | null;
    private declare outline_radius_uniform_location: WebGLUniformLocation | null;
    private declare outline_colour_uniform_location: WebGLUniformLocation | null;
    private declare background_colour_uniform_location: WebGLUniformLocation | null;
    protected override setupFragment(){
      this.fragment_name = 'CircleOutlineShader';
      if(!CircleOutlineFragmentShader.shader){
        CircleOutlineFragmentShader.load();
      }
      this.program.addFragment(CircleOutlineFragmentShader.shader!);
    }
    protected override addFragmentUniformLocations(): void{
      this.centre_uniform_location = this.program.getUniformLocation('u_centre');
      this.radius_uniform_location = this.program.getUniformLocation('u_radius');
      this.outline_radius_uniform_location = this.program.getUniformLocation('u_outline_radius');
      this.outline_colour_uniform_location = this.program.getUniformLocation('u_outline_colour');
      this.background_colour_uniform_location = this.program.getUniformLocation('u_background_colour');
    }
    setCentre(a: GLfloat, b: GLfloat){
      this.program.setFloat2(this.centre_uniform_location!, a, b);
    }
    setRadius(a: GLfloat){
      this.program.setFloat(this.radius_uniform_location!, a);
    }
    setOutlineRadius(a: GLfloat){
      this.program.setFloat(this.outline_radius_uniform_location!, a);
    }
    setOutlineColour(a: GLfloat, b: GLfloat, c: GLfloat, d: GLfloat){
      this.program.setFloat4(this.outline_colour_uniform_location!, a, b, c, d);
    }
    setBackgroundColour(a: GLfloat, b: GLfloat, c: GLfloat, d: GLfloat){
      this.program.setFloat4(this.background_colour_uniform_location!, a, b, c, d);
    }
  }
}
