import RectOutline from './../Source/rect_outline.frag?raw';
import * as Shader from './../../shader';
import * as WebGL from './../../../globals';

export class RectOutlineFragmentShader{
  static shader?: Shader.FragmentShader;
  static load(){
    if(this.shader == undefined){
      this.shader = new Shader.FragmentShader();
      if(!this.shader.addSource(RectOutline)){
        console.log('RectOutline: fragment source not added');
      }
    }
  }
}

export function RectOutlineShaderProgramMix<TBase extends Shader.CustomShaderProgramable>(Base: TBase){
  return class RectOutline extends Base{
    private declare outline_colour_uniform_location: WebGLUniformLocation | null;
    private declare outline_ratio_uniform_location: WebGLUniformLocation | null;
    protected override setupFragment(){
      this.fragment_name = 'RectOutlineShader';
      if(!RectOutlineFragmentShader.shader){
        RectOutlineFragmentShader.load();
      }
      this.program.addFragment(RectOutlineFragmentShader.shader!);
    }
    protected override addFragmentUniformLocations(): void{
      this.outline_colour_uniform_location = this.program.getUniformLocation('u_outline_colour');
      this.outline_ratio_uniform_location = this.program.getUniformLocation('u_outline_ratio');
    }
    setOutlineColour(a: GLfloat, b: GLfloat, c: GLfloat, d: GLfloat){
      this.program.setFloat4(this.outline_colour_uniform_location!, a, b, c, d);
    }
    setOutlineRatio(a: GLfloat){
      this.program.setFloat(this.outline_ratio_uniform_location!, a);
    }
  }
}
