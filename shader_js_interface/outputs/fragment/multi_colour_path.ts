import * as Shader from './../../shader';
import * as WebGL from './../../../globals';

const MultiColourPath = `precision mediump float;

varying vec2 v_position;
varying vec2 v_relative;

uniform vec3 u_left_colour; //colour
uniform vec3 u_right_colour; //colour
uniform vec3 u_top_colour; // colour
uniform vec3 u_bot_colour; //colour
uniform vec3 u_mid_colour; //colour
uniform float u_size; // between 0 and 0.5
uniform vec3 u_background_colour; //colour

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
}`;

export class MultiColourPathFragmentShader{
  static shader?: Shader.FragmentShader;
  static load(){
    if(this.shader == undefined){
      this.shader = new Shader.FragmentShader();
      if(!this.shader.addSource(MultiColourPath)){
        console.log('MultiColourPath: fragment source not added');
      }
    }
  }
}

export function MultiColourPathShaderProgramMix<TBase extends Shader.CustomShaderProgramable>(Base: TBase){
  return class MultiColourPath extends Base{
    private declare left_colour_uniform_location: WebGLUniformLocation | null;
    private declare right_colour_uniform_location: WebGLUniformLocation | null;
    private declare top_colour_uniform_location: WebGLUniformLocation | null;
    private declare bot_colour_uniform_location: WebGLUniformLocation | null;
    private declare mid_colour_uniform_location: WebGLUniformLocation | null;
    private declare size_uniform_location: WebGLUniformLocation | null;
    private declare background_colour_uniform_location: WebGLUniformLocation | null;
    protected override setupFragment(){
      this.fragment_name = 'MultiColourPathShader';
      if(!MultiColourPathFragmentShader.shader){
        MultiColourPathFragmentShader.load();
      }
      this.program.addFragment(MultiColourPathFragmentShader.shader!);
    }
    protected override addFragmentUniformLocations(): void{
      this.left_colour_uniform_location = this.program.getUniformLocation('u_left_colour');
      this.right_colour_uniform_location = this.program.getUniformLocation('u_right_colour');
      this.top_colour_uniform_location = this.program.getUniformLocation('u_top_colour');
      this.bot_colour_uniform_location = this.program.getUniformLocation('u_bot_colour');
      this.mid_colour_uniform_location = this.program.getUniformLocation('u_mid_colour');
      this.size_uniform_location = this.program.getUniformLocation('u_size');
      this.background_colour_uniform_location = this.program.getUniformLocation('u_background_colour');
    }
    setLeftColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.left_colour_uniform_location!, a, b, c);
    }
    setLeftColourFromColourRGB(colour: WebGL.Colour.ColourRGB){
      this.program.setFloat3(this.left_colour_uniform_location!, colour.red, colour.green, colour.blue);
    }
    setRightColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.right_colour_uniform_location!, a, b, c);
    }
    setRightColourFromColourRGB(colour: WebGL.Colour.ColourRGB){
      this.program.setFloat3(this.right_colour_uniform_location!, colour.red, colour.green, colour.blue);
    }
    setTopColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.top_colour_uniform_location!, a, b, c);
    }
    setTopColourFromColourRGB(colour: WebGL.Colour.ColourRGB){
      this.program.setFloat3(this.top_colour_uniform_location!, colour.red, colour.green, colour.blue);
    }
    setBotColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.bot_colour_uniform_location!, a, b, c);
    }
    setBotColourFromColourRGB(colour: WebGL.Colour.ColourRGB){
      this.program.setFloat3(this.bot_colour_uniform_location!, colour.red, colour.green, colour.blue);
    }
    setMidColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.mid_colour_uniform_location!, a, b, c);
    }
    setMidColourFromColourRGB(colour: WebGL.Colour.ColourRGB){
      this.program.setFloat3(this.mid_colour_uniform_location!, colour.red, colour.green, colour.blue);
    }
    setSize(a: GLfloat){
      this.program.setFloat(this.size_uniform_location!, a);
    }
    setBackgroundColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.background_colour_uniform_location!, a, b, c);
    }
    setBackgroundColourFromColourRGB(colour: WebGL.Colour.ColourRGB){
      this.program.setFloat3(this.background_colour_uniform_location!, colour.red, colour.green, colour.blue);
    }
  }
}
