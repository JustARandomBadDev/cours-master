#ifndef PARTICLES_SIMULATOR_HPP
#define PARTICLES_SIMULATOR_HPP

#include "simulation/field.hpp"
#include "simulation/particle_system.hpp"
#include "simulation/particles_data.hpp"

#include <glm/vec3.hpp>

#include <memory>
#include <random>
#include <vector>

class ParticlesSimulator {
  public:
    ParticlesSimulator() = default;

    void init();
    const ParticleData &update(float dt);

    const std::vector<std::unique_ptr<Field>> &fields() const {
        return _fields;
    }

    const ParticleData &particles() const {
        return _particle_system.particles();
    }

  private:
    void spawnParticle();

    std::vector<std::unique_ptr<Field>> _fields;
    ParticleSystem _particle_system;

    float _spawn_elapsed = 0.0f;
    float _spawn_interval = 0.01f;
    float _max_spawn_velocity = 1.0f;

    glm::vec3 _spawn_position{0.0f, 20.0f, 0.0f};

    std::mt19937 _random_engine{std::random_device{}()};
};

#endif
