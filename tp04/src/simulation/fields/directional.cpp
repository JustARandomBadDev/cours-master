#include "simulation/fields/directional.hpp"

#include <glm/geometric.hpp>

#include "simulation/fields_constants.hpp"

void Directional::step(ParticleData &p_particles) {
    const float l2_direction =
        _direction.x * _direction.x +
        _direction.y * _direction.y +
        _direction.z * _direction.z;

    if (l2_direction <= DIRECTIONAL_MIN_DISTANCE_SQUARED) {
        return;
    }

    const auto dir = glm::normalize(_direction);
    const auto force = DIRECTIONAL_STRENGHT * dir;

    for (std::size_t index = 0; index < p_particles.count; index++) {
        p_particles.force[index] += force;
    }
}