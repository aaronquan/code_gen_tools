import ColourTexture from './../Source/colour_texture.frag?raw';
import * as Shader from './../../shader';
import * as WebGL from './../../../globals';

export class ColourTextureFragmentShader{
  static shader?: Shader.FragmentShader;
  static load(){
    if(this.shader == undefined){
      this.shader = new Shader.FragmentShader();
      if(!this.shader.addSource(ColourTexture)){
        console.log('ColourTexture: fragment source not added');
      }
    }
  }
}

export function ColourTextureShaderProgramMix<TBase extends Shader.CustomShaderProgramable>(Base: TBase){
  return class ColourTexture extends Base{
    protected override setupFragment(){
      this.fragment_name = 'ColourTextureShader';
      if(!ColourTextureFragmentShader.shader){
        ColourTextureFragmentShader.load();
      }
      this.program.addFragment(ColourTextureFragmentShader.shader!);
    }
    protected override addFragmentUniformLocations(): void{
    }
  }
}
