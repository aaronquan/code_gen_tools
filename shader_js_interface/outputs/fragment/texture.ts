import Texture from './../Source/texture.frag?raw';
import * as Shader from './../../shader';

export class TextureFragmentShader{
  static shader?: Shader.FragmentShader;
  static load(){
    if(this.shader == undefined){
      this.shader = new Shader.FragmentShader();
      if(!this.shader.addSource(Texture)){
        console.log('Texture: fragment source not added');
      }
    }
  }
}

export function TextureShaderProgramMix<TBase extends Shader.CustomShaderProgramable>(Base: TBase){
  return class Texture extends Base{
    private declare texture_id_uniform_location: WebGLUniformLocation | null;
    protected override setupFragment(){
      this.fragment_name = 'TextureShader';
      if(TextureFragmentShader.shader){
        this.program.addFragment(TextureFragmentShader.shader)
      }else{
        throw new Error(`${this.fragment_name} not loaded`);
      }
    }
    protected override addFragmentUniformLocations(): void{
      this.texture_id_uniform_location = this.program.getUniformLocation('u_texture_id');
    }
    setTextureId(i: GLint){
      this.program.setInt(this.texture_id_uniform_location!, i);
    }
  }
}
