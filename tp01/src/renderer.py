import glm
import glfw
import moderngl as gl
import numpy as np

from pathlib import Path
from typing import cast

class Renderer :
    def __init__(self,
                 p_width: int,
                 p_height: int,
                 p_vertex_path: Path,
                 p_fragment_path: Path,
                 p_reserved: int) -> None:
        self.__initWindow(p_width, p_height)
        self.__initContext()
        self.__initShaders(p_vertex_path, p_fragment_path)
        self.__initBuffers(p_reserved)
        
    def __initWindow(self, p_width: int, p_height: int) -> None:
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.__window = glfw.create_window(
            p_width,
            p_height,
            "ModernGL Triangle",
            None,
            None,
        )

        if not self.__window:
            glfw.terminate()
            raise RuntimeError("Failed to create window")

        glfw.make_context_current(self.__window)
        
    def __initContext(self) -> None:
        self.ctx = gl.create_context()
        self.ctx.enable(gl.DEPTH_TEST)
        self.ctx.enable(gl.CULL_FACE)
        self.ctx.clear(0.05, 0.05, 0.08)
        
    def __initShaders(self, p_vertex_path: Path, p_fragment_path: Path) -> None:
        vertex_shader: str
        fragment_shader: str
        
        with open(p_vertex_path) as f:
            vertex_shader = f.read()
            
        with open(p_fragment_path) as f:
            fragment_shader = f.read()
        
        self.__program = self.ctx.program(
            vertex_shader,
            fragment_shader
        )

    def __initBuffers(self, p_reserved: int) -> None:
        self.__vbo = self.ctx.buffer(reserve=p_reserved)
        self.__ibo = self.ctx.buffer(reserve=p_reserved)

        self.__vao: gl.VertexArray = self.ctx.vertex_array(  # pyright: ignore[reportUnknownMemberType]
            self.__program,
            [
                (
                    self.__vbo,
                    "3f 3f",
                    "in_position",
                    "in_color",
                )
            ],
            index_buffer=self.__ibo,
            index_element_size=4,
        )
        
        self.__projection_uniform = cast(
            gl.Uniform,
            self.__program["projection"]
        )
        
        self.__model_uniform = cast(
            gl.Uniform,
            self.__program["model"]
        )
        
        self.__view_uniform = cast(
            gl.Uniform,
            self.__program["view"]
        )
        
    def updateBuffer(self, p_vertex: np.ndarray, p_index: np.ndarray) -> None:
        self.__vbo.write(p_vertex.tobytes())
        self.__ibo.write(p_index.tobytes())
    
    def updateUniform(self,
                      p_model: glm.mat4x4,
                      p_projection: glm.mat4x4,
                      p_view: glm.mat4x4) -> None:
        self.__model_uniform.write(p_model)
        self.__projection_uniform.write(p_projection)
        self.__view_uniform.write(p_view)
        
    def render(self) -> None:
        glfw.poll_events()

        self.ctx.clear(0.05, 0.05, 0.08)
        self.__vao.render(gl.TRIANGLES)

        glfw.swap_buffers(self.__window)
        
    def shouldClose(self) -> int:
        return glfw.window_should_close(self.__window)
    
    def cleanup(self) -> None:
        self.__vao.release()
        self.__vbo.release()
        self.__program.release()

        glfw.destroy_window(self.__window)
        glfw.terminate()
