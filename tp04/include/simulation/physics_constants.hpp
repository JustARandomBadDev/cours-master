#ifndef PHYSICS_CONSTANTS_HPP
#define PHYSICS_CONSTANTS_HPP

#include <glm/vec3.hpp>

inline constexpr float PARTICLE_MASS = 1.0f;

inline constexpr glm::vec3 GRAVITY{0.0f, -9.8f, 0.0f};

inline constexpr float DAMPING = 0.15f;
inline constexpr float GROUND_RESTITUTION = 0.5f;
inline constexpr float MAX_DT = 0.05f;

#endif
