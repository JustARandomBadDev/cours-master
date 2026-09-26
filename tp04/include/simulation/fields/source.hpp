#ifndef SOURCE_HPP
#define SOURCE_HPP

#include <glm/ext/vector_float3.hpp>

#include "simulation/field.hpp"

class Source : public Field {
  public:
    Source(glm::vec3 p_position) : Field(p_position) {}

    void step(ParticleData &p_particles) override;
};

#endif