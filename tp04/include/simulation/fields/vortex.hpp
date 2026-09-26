#ifndef VORTEX_HPP
#define VORTEX_HPP

#include "glm/ext/vector_float3.hpp"
#include "simulation/field.hpp"

class Vortex : public Field {
  public:
    Vortex(glm::vec3 p_position, glm::vec3 p_axis)
        : Field(p_position), _axis(p_axis) {}

    void step(ParticleData &p_particles) override;

  private:
    glm::vec3 _axis{0.0f, 1.0f, 0.0f};
};

#endif