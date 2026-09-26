#ifndef SINK_HPP
#define SINK_HPP

#include "glm/ext/vector_float3.hpp"
#include "simulation/field.hpp"

class Sink : public Field {
  public:
    Sink(glm::vec3 p_position) : Field(p_position) {}

    void step(ParticleData &p_particles) override;
};

#endif