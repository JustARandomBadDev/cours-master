#ifndef APPLICATION_HPP
#define APPLICATION_HPP

#include "core/timer.hpp"
#include "simulation/particles_simulator.hpp"
#include <QGLViewer/qglviewer.h>

#include <glm/glm.hpp>

class Application : public QGLViewer {
  protected:
    virtual void draw();
    virtual void init();
    virtual void animate();
    virtual void keyPressEvent(QKeyEvent *e);

  private:
    Timer _timer;
    ParticlesSimulator _particle_simulator;

    bool _draw_fields = true;
};

#endif