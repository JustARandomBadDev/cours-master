#include "simulation/fields/vortex.hpp"

#include <cmath>
#include <glm/geometric.hpp>

#include "simulation/fields_constants.hpp"

void Vortex::step(ParticleData &p_particles) {
    for (std::size_t index = 0; index < p_particles.count; index++) {
        const auto &pos = p_particles.position[index];
        const auto Cp = pos - _position;

        float l2_Cp = Cp.x * Cp.x + Cp.y * Cp.y + Cp.z * Cp.z;
        if (l2_Cp <= VORTEX_MIN_DISTANCE_SQUARED) {
            continue;
        }

        const auto Cp_cross_R = glm::cross(Cp, _axis);

        float l2_Cp_cross_R = Cp_cross_R.x * Cp_cross_R.x +
                              Cp_cross_R.y * Cp_cross_R.y +
                              Cp_cross_R.z * Cp_cross_R.z;

        if (l2_Cp_cross_R <= VORTEX_MIN_DISTANCE_SQUARED ||
            l2_Cp_cross_R > VORTEX_MAX_DISTANCE_SQUARED)
            continue;

        const float l_Cp_cross_R = std::sqrt(l2_Cp_cross_R);
        const auto dir = Cp_cross_R / l_Cp_cross_R;

        const auto force =
            (VORTEX_STRENGHT /
                ((VORTEX_STRENGHT / MAX_VORTEX_STRENGHT) + l2_Cp)) *
            dir;

        p_particles.force[index] += force;
    }
}