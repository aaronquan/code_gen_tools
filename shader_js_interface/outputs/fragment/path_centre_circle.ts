import * as Shader from './../../shader';
import * as WebGL from './../../../globals';

const PathCentreCircle = `precision mediump float;

varying vec2 v_position;
varying vec2 v_relative;

uniform float u_left;
uniform float u_right;
uniform float u_top;
uniform float u_bot;
uniform vec3 u_mid_colour;
uniform float u_circle_radius;
uniform float u_size; // between 0 and 0.5
uniform vec3 u_colour;
uniform vec3 u_background_colour;

void main(){
  vec2 uv = v_relative;
  float sz = u_size/2.;

  float inside_top = step(abs(0.5-uv.x), sz)*step(0.5-sz, uv.y)*u_top;
  float inside_bot = step(abs(0.5-uv.x), sz)*step(uv.y, 0.5+sz)*u_bot;
  float inside_left = step(abs(0.5-uv.y), sz)*step(uv.x, 0.5-sz)*u_left;
  float inside_right = step(abs(0.5-uv.y), sz)*step(0.5-sz, uv.x)*u_right;

  vec2 middle = vec2(0.5, 0.5);
  float inside_circle = step(u_circle_radius, distance(middle, v_relative));
  float inside = clamp(inside_top+inside_bot+inside_left+inside_right+inside_circle, 0.0, 1.0);

  gl_FragColor = vec4(inside*u_colour+(1.0-inside)*u_background_colour, 1.0);
}`;

export class PathCentreCircleFragmentShader{
  static shader?: Shader.FragmentShader;
  static load(){
    if(this.shader == undefined){
      this.shader = new Shader.FragmentShader();
      if(!this.shader.addSource(PathCentreCircle)){
        console.log('PathCentreCircle: fragment source not added');
      }
    }
  }
}

export function PathCentreCircleShaderProgramMix<TBase extends Shader.CustomShaderProgramable>(Base: TBase){
  return class PathCentreCircle extends Base{
    private declare left_uniform_location: WebGLUniformLocation | null;
    private declare right_uniform_location: WebGLUniformLocation | null;
    private declare top_uniform_location: WebGLUniformLocation | null;
    private declare bot_uniform_location: WebGLUniformLocation | null;
    private declare mid_colour_uniform_location: WebGLUniformLocation | null;
    private declare circle_radius_uniform_location: WebGLUniformLocation | null;
    private declare size_uniform_location: WebGLUniformLocation | null;
    private declare colour_uniform_location: WebGLUniformLocation | null;
    private declare background_colour_uniform_location: WebGLUniformLocation | null;
    protected override setupFragment(){
      this.fragment_name = 'PathCentreCircleShader';
      if(!PathCentreCircleFragmentShader.shader){
        PathCentreCircleFragmentShader.load();
      }
      this.program.addFragment(PathCentreCircleFragmentShader.shader!);
    }
    protected override addFragmentUniformLocations(): void{
      this.left_uniform_location = this.program.getUniformLocation('u_left');
      this.right_uniform_location = this.program.getUniformLocation('u_right');
      this.top_uniform_location = this.program.getUniformLocation('u_top');
      this.bot_uniform_location = this.program.getUniformLocation('u_bot');
      this.mid_colour_uniform_location = this.program.getUniformLocation('u_mid_colour');
      this.circle_radius_uniform_location = this.program.getUniformLocation('u_circle_radius');
      this.size_uniform_location = this.program.getUniformLocation('u_size');
      this.colour_uniform_location = this.program.getUniformLocation('u_colour');
      this.background_colour_uniform_location = this.program.getUniformLocation('u_background_colour');
    }
    setLeft(a: GLfloat){
      this.program.setFloat(this.left_uniform_location!, a);
    }
    setRight(a: GLfloat){
      this.program.setFloat(this.right_uniform_location!, a);
    }
    setTop(a: GLfloat){
      this.program.setFloat(this.top_uniform_location!, a);
    }
    setBot(a: GLfloat){
      this.program.setFloat(this.bot_uniform_location!, a);
    }
    setMidColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.mid_colour_uniform_location!, a, b, c);
    }
    setCircleRadius(a: GLfloat){
      this.program.setFloat(this.circle_radius_uniform_location!, a);
    }
    setSize(a: GLfloat){
      this.program.setFloat(this.size_uniform_location!, a);
    }
    setColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.colour_uniform_location!, a, b, c);
    }
    setBackgroundColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.background_colour_uniform_location!, a, b, c);
    }
  }
}
