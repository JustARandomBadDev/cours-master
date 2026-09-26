#include "simulation/particle_system.hpp"
#include "glm/ext/vector_float3.hpp"
#include "simulation/physics_constants.hpp"

#include <cstddef>
#include <cstdlib>

void ParticleSystem::init() {
    clear();

    _particles.position.resize(MAX_PARTICLES);
    _particles.velocity.resize(MAX_PARTICLES);
    _particles.force.resize(MAX_PARTICLES);
}

void ParticleSystem::addParticle(const glm::vec3 p_position) {
    addParticle(p_position, {0.f, 0.f, 0.f});
}

void ParticleSystem::addParticle(
    const glm::vec3 p_position,
    const glm::vec3 p_velocity
) {
    std::size_t &count = _particles.count;

    if (count >= MAX_PARTICLES) {
        _particles.position[_index] = p_position;
        _particles.velocity[_index] = p_velocity;
        _particles.force[_index] = glm::vec3(0.0f);

        _index ++;

        if (_index >= MAX_PARTICLES) _index = 0;

        return;
    }

    _particles.position[count] = p_position;
    _particles.velocity[count] = p_velocity;
    _particles.force[count] = glm::vec3(0.0f);

    count++;
}

void ParticleSystem::removeParticle(std::size_t p_index) {
    std::size_t &count = _particles.count;

    if (p_index >= count) return;

    const std::size_t last = count - 1;

    _particles.position[p_index] = _particles.position[last];
    _particles.velocity[p_index] = _particles.velocity[last];
    _particles.force[p_index] = _particles.force[last];

    count--;
}

void ParticleSystem::integrate(float p_dt) {
    glm::vec3 total_force;
    glm::vec3 acceleration;

    for (std::size_t i = 0; i < _particles.count; i++) {
        auto &position = _particles.position[i];
        auto &velocity = _particles.velocity[i];
        auto &force = _particles.force[i];

        total_force = force - DAMPING * velocity;
        acceleration = total_force / PARTICLE_MASS + GRAVITY;

        velocity += acceleration * p_dt;
        position += velocity * p_dt;

        if (position.y < 0.0f) {
            position.y = 0.0f;

            if (velocity.y < 0.0f) {
                velocity.y = -velocity.y * GROUND_RESTITUTION;
            }
        }

        force = glm::vec3(0.f);
    }
}

void ParticleSystem::clear() noexcept {
    _particles.count = 0;
}

const ParticleData &ParticleSystem::particles() const noexcept {
    return _particles;
}

ParticleData &ParticleSystem::particles() noexcept {
    return _particles;
}

std::size_t ParticleSystem::count() const noexcept {
    return _particles.count;
}
