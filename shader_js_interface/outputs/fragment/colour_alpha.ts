import * as Shader from './../../shader';
import * as WebGL from './../../../globals';

const ColourAlpha = `precision mediump float;

uniform vec4 colour; //coloura

void main(){
  gl_FragColor = vec4(colour);
}`;

export class ColourAlphaFragmentShader{
  static shader?: Shader.FragmentShader;
  static load(){
    if(this.shader == undefined){
      this.shader = new Shader.FragmentShader();
      if(!this.shader.addSource(ColourAlpha)){
        console.log('ColourAlpha: fragment source not added');
      }
    }
  }
}

export function ColourAlphaShaderProgramMix<TBase extends Shader.CustomShaderProgramable>(Base: TBase){
  return class ColourAlpha extends Base{
    private declare colour_uniform_location: WebGLUniformLocation | null;
    protected override setupFragment(){
      this.fragment_name = 'ColourAlphaShader';
      if(!ColourAlphaFragmentShader.shader){
        ColourAlphaFragmentShader.load();
      }
      this.program.addFragment(ColourAlphaFragmentShader.shader!);
    }
    protected override addFragmentUniformLocations(): void{
      this.colour_uniform_location = this.program.getUniformLocation('colour');
    }
    setColour(a: GLfloat, b: GLfloat, c: GLfloat, d: GLfloat){
      this.program.setFloat4(this.colour_uniform_location!, a, b, c, d);
    }
    setColourFromColourRGBA(colour: WebGL.Colour.ColourRGBA){
      this.program.setFloat4(this.colour_uniform_location!, colour.red, colour.green, colour.blue, colour.alpha);
    }
  }
}
