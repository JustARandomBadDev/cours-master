#version 330 core

in vec3 in_position;
in vec3 in_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 color;

void main() {
    color = in_color;
    gl_Position = projection * view * model * vec4(in_position, 1.0);
}
