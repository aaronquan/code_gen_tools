import MultiColourCentreCirclePath from './../Source/multi_colour_centre_circle_path.frag?raw';
import * as Shader from './../../shader';
import * as WebGL from './../../../globals';

export class MultiColourCentreCirclePathFragmentShader{
  static shader?: Shader.FragmentShader;
  static load(){
    if(this.shader == undefined){
      this.shader = new Shader.FragmentShader();
      if(!this.shader.addSource(MultiColourCentreCirclePath)){
        console.log('MultiColourCentreCirclePath: fragment source not added');
      }
    }
  }
}

export function MultiColourCentreCirclePathShaderProgramMix<TBase extends Shader.CustomShaderProgramable>(Base: TBase){
  return class MultiColourCentreCirclePath extends Base{
    private declare left_colour_uniform_location: WebGLUniformLocation | null;
    private declare right_colour_uniform_location: WebGLUniformLocation | null;
    private declare top_colour_uniform_location: WebGLUniformLocation | null;
    private declare bot_colour_uniform_location: WebGLUniformLocation | null;
    private declare mid_colour_uniform_location: WebGLUniformLocation | null;
    private declare circle_radius_uniform_location: WebGLUniformLocation | null;
    private declare size_uniform_location: WebGLUniformLocation | null;
    private declare background_colour_uniform_location: WebGLUniformLocation | null;
    protected override setupFragment(){
      this.fragment_name = 'MultiColourCentreCirclePathShader';
      if(!MultiColourCentreCirclePathFragmentShader.shader){
        MultiColourCentreCirclePathFragmentShader.load();
      }
      this.program.addFragment(MultiColourCentreCirclePathFragmentShader.shader!);
    }
    protected override addFragmentUniformLocations(): void{
      this.left_colour_uniform_location = this.program.getUniformLocation('u_left_colour');
      this.right_colour_uniform_location = this.program.getUniformLocation('u_right_colour');
      this.top_colour_uniform_location = this.program.getUniformLocation('u_top_colour');
      this.bot_colour_uniform_location = this.program.getUniformLocation('u_bot_colour');
      this.mid_colour_uniform_location = this.program.getUniformLocation('u_mid_colour');
      this.circle_radius_uniform_location = this.program.getUniformLocation('u_circle_radius');
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
    setCircleRadius(a: GLfloat){
      this.program.setFloat(this.circle_radius_uniform_location!, a);
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
