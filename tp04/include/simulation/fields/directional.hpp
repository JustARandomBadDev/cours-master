#ifndef DIRECTIONAL_HPP
#define DIRECTIONAL_HPP

#include "simulation/field.hpp"
#include <glm/ext/vector_float3.hpp>

class Directional : public Field {
  public:
    Directional(glm::vec3 p_position, glm::vec3 p_direction)
        : Field(p_position), _direction(p_direction) {}

    void step(ParticleData &p_particles) override;

  private:
    glm::vec3 _direction;
};

#endif