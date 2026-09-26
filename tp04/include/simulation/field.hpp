#ifndef FIELD_HPP
#define FIELD_HPP

#include <glm/ext/vector_float3.hpp>

#include "particles_data.hpp"

class Field {
  public:
    Field(glm::vec3 p_position) : _position(p_position) {}

    virtual ~Field() = default;

    virtual void step(ParticleData &p_particles) = 0;

    const glm::vec3 &position() const {
        return _position;
    };

  protected:
    glm::vec3 _position;
};

#endif