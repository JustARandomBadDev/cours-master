import glm

class Camera:
    def __init__(self, 
                 p_width: int, 
                 p_height: int,
                 p_position: glm.vec3 = glm.vec3(2.0, 0.0, 2.0)) -> None:
        self.position = p_position
        
        self.__model = glm.mat4x4(1.0)
        
        self.__projection = glm.perspective( # pyright: ignore[reportUnknownMemberType]
            glm.radians(70.0),               # pyright: ignore[reportUnknownMemberType]
            p_width / p_height,
            0.1, 10000
        )
        
        self.__view = glm.lookAt(            # pyright: ignore[reportUnknownMemberType]
            self.position,
            glm.vec3(0.0),
            glm.vec3(0.0, 1.0, 0.0)
            
        )
        
    def getModel(self) -> glm.mat4x4:
        return self.__model
    
    def getProjection(self) -> glm.mat4x4:
        return self.__projection
    
    def getView(self) -> glm.mat4x4:
        return self.__view