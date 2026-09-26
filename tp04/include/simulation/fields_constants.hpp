#ifndef PHYSICS_CONSTANTS_HPP
#define PHYSICS_CONSTANTS_HPP

#include <glm/vec3.hpp>

// Source
inline constexpr float SOURCE_MIN_DISTANCE_SQUARED = 1e-8f;
inline constexpr float SOURCE_MAX_DISTANCE_SQUARED = 1e+8f;
inline constexpr float SOURCE_STRENGHT = 50.f;
inline constexpr float MAX_SOURCE_STRENGHT = 100.f;

// Sink
inline constexpr float SINK_MIN_DISTANCE_SQUARED = 1e-8f;
inline constexpr float SINK_MAX_DISTANCE_SQUARED = 1e+8f;
inline constexpr float SINK_STRENGHT = 50.f;
inline constexpr float MAX_SINK_STRENGHT = 100.f;

// Vortex
inline constexpr float VORTEX_MIN_DISTANCE_SQUARED = 1e-8f;
inline constexpr float VORTEX_MAX_DISTANCE_SQUARED = 1e+8f;
inline constexpr float VORTEX_STRENGHT = 100.f;
inline constexpr float MAX_VORTEX_STRENGHT = 100.f;

// Directional
inline constexpr float DIRECTIONAL_MIN_DISTANCE_SQUARED = 1e-8f;
inline constexpr float DIRECTIONAL_MAX_DISTANCE_SQUARED = 10.f;
inline constexpr float DIRECTIONAL_STRENGHT = 50.f;
inline constexpr float MAX_DIRECTIONAL_STRENGHT = 100.f;

#endif
