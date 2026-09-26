#include "simulation/particles_simulator.hpp"

#include "glm/ext/vector_float3.hpp"
#include "simulation/fields/directional.hpp"
#include "simulation/fields/sink.hpp"
#include "simulation/fields/source.hpp"
#include "simulation/fields/vortex.hpp"
#include "simulation/physics_constants.hpp"

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <memory>
#include <random>

void ParticlesSimulator::init() {
    _particle_system.init();

    _fields.push_back(std::make_unique<Sink>(glm::vec3{.0f, .0f, .0f}));
    _fields.push_back(std::make_unique<Vortex>(glm::vec3{.0f, .0f, .0f}, glm::vec3{0.f, 1.f, 0.f}));

    std::size_t n = 40;
    std::size_t circle_count = 1;
    double r = 50.;

    for (std::size_t circle = 1; circle <= circle_count; circle++) {
        double circle_radius =
            r * static_cast<double>(circle) / circle_count;

        std::size_t circle_n = static_cast<std::size_t>(
            n * circle_radius / r
        );

        for (std::size_t i = 0; i < circle_n; i++) {
            double angle = 2. * M_PI / circle_n * i;

            _fields.push_back(
                std::make_unique<Source>(
                    glm::vec3{
                        cos(angle) * circle_radius,
                        -5.f,
                        sin(angle) * circle_radius
                    }
                )
            );
        }
    }
}

const ParticleData &ParticlesSimulator::update(float p_dt) {
    const float dt = std::clamp(p_dt, 0.0f, MAX_DT);

    _spawn_elapsed += dt;

    while (_spawn_elapsed >= _spawn_interval) {
        spawnParticle();
        _spawn_elapsed -= _spawn_interval;
    }

    for (auto &field : _fields) {
        field->step(_particle_system.particles());
    }

    _particle_system.integrate(dt);

    return _particle_system.particles();
}

void ParticlesSimulator::spawnParticle() {
    std::uniform_real_distribution<float> velocity_distribution(
        -_max_spawn_velocity,
        _max_spawn_velocity
    );

    const glm::vec3 velocity{velocity_distribution(_random_engine),
        velocity_distribution(_random_engine),
        velocity_distribution(_random_engine)};

    _particle_system.addParticle(_spawn_position, velocity);
}
