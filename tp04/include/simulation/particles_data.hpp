#ifndef PARTICLE_DATA_HPP
#define PARTICLE_DATA_HPP

#include <cstddef>
#include <glm/ext/vector_float3.hpp>
#include <vector>

struct ParticleData {
    std::vector<glm::vec3> position;
    std::vector<glm::vec3> velocity;
    std::vector<glm::vec3> force;

    std::size_t count{};
};

#endif