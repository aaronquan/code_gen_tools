import * as Shader from './../../shader';
import * as WebGL from './../../../globals';

const Texture = `precision mediump float;

varying vec2 v_position;
varying vec2 v_relative;


uniform sampler2D u_texture_id;

void main(){
    gl_FragColor = texture2D(u_texture_id, v_relative);
}`;

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
      if(!TextureFragmentShader.shader){
        TextureFragmentShader.load();
      }
      this.program.addFragment(TextureFragmentShader.shader!);
    }
    protected override addFragmentUniformLocations(): void{
      this.texture_id_uniform_location = this.program.getUniformLocation('u_texture_id');
    }
    setTextureId(i: GLint){
      this.program.setInt(this.texture_id_uniform_location!, i);
    }
  }
}
