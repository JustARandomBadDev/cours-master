#ifndef PARTICLE_SYSTEM_HPP
#define PARTICLE_SYSTEM_HPP

#include <cstddef>
#include <glm/ext/vector_float3.hpp>

#include "simulation/particles_data.hpp"

class ParticleSystem {
  public:
    static constexpr std::size_t MAX_PARTICLES = 3000;

    void init();

    void addParticle(const glm::vec3 p_position);
    void addParticle(const glm::vec3 p_position, const glm::vec3 p_velocity);
    void removeParticle(std::size_t p_index);

    void integrate(float p_dt);

    void clear() noexcept;

    const ParticleData &particles() const noexcept;
    ParticleData &particles() noexcept;
    std::size_t count() const noexcept;

  private:
    ParticleData _particles;

    std::size_t _index = 0.f;
};

#endif
