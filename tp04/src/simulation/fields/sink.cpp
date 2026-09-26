#include "simulation/fields/sink.hpp"

#include <cmath>
#include <cstddef>

#include "simulation/fields_constants.hpp"

void Sink::step(ParticleData &p_particles) {
    for (std::size_t index = 0; index < p_particles.count; index++) {
        const auto &pos = p_particles.position[index];
        const auto Cp = pos - _position;
        float l2_Cp = Cp.x * Cp.x + Cp.y * Cp.y + Cp.z * Cp.z;

        if (l2_Cp <= SINK_MIN_DISTANCE_SQUARED ||
            l2_Cp > SINK_MAX_DISTANCE_SQUARED)
            continue;

        const float l_Cp = std::sqrt(l2_Cp);
        const auto dir = Cp / l_Cp;

        const auto force =
            -(SINK_STRENGHT / ((SINK_STRENGHT / MAX_SINK_STRENGHT) + l2_Cp)) *
            dir;

        p_particles.force[index] += force;
    }
}
