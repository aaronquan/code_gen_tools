import MultiColourCentreCirclePath from './../Source/multi_colour_centre_circle_path.frag?raw';
import * as Shader from './../../shader';

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
      if(MultiColourCentreCirclePathFragmentShader.shader){
        this.program.addFragment(MultiColourCentreCirclePathFragmentShader.shader)
      }else{
        throw new Error(`${this.fragment_name} not loaded`);
      }
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
    setRightColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.right_colour_uniform_location!, a, b, c);
    }
    setTopColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.top_colour_uniform_location!, a, b, c);
    }
    setBotColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.bot_colour_uniform_location!, a, b, c);
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
    setBackgroundColour(a: GLfloat, b: GLfloat, c: GLfloat){
      this.program.setFloat3(this.background_colour_uniform_location!, a, b, c);
    }
  }
}
