#include "application.hpp"

#include <GL/gl.h>
#include <QKeyEvent>
#include <cstddef>
#include <math.h>
#include <stdlib.h> // RAND_MAX

void Application::init() {
    glDisable(GL_LIGHTING);
    glPointSize(3.0);
    setSceneRadius(1000);

    _particle_simulator.init();
    showEntireScene();
}

void Application::draw() {
    const int gridWidth = 100;
    const int gridHeight = 100;
    const float cellSize = 10.f;

    const float width = gridWidth * cellSize;
    const float height = gridHeight * cellSize;

    glColor3f(.5f, .5f, .5f);
    glLineWidth(2.f);
    glBegin(GL_LINES);

    // Lines parallel to Z
    for (int x = -gridWidth; x <= gridWidth; x++) {
        const float px = x * cellSize;

        glVertex3f(px, 0.0f, -height);
        glVertex3f(px, 0.0f, height);
    }

    // Lines parallel to X
    for (int y = -gridHeight; y <= gridHeight; y++) {
        const float pz = y * cellSize;

        glVertex3f(-width, 0.0f, pz);
        glVertex3f(width, 0.0f, pz);
    }

    glEnd();

    const auto &data = _particle_simulator.particles();

    glColor3f(1.f, 0.f, 0.f);
    glPointSize(7.5f);
    glBegin(GL_POINTS);

    for (std::size_t i = 0; i < data.count; i++) {
        glVertex3f(data.position[i].x, data.position[i].y, data.position[i].z);
    }

    glEnd();

    if (!_draw_fields) return;

    glColor3f(1.f, 1.f, 0.f);
    glPointSize(10.0f);
    glBegin(GL_POINTS);

    for (const auto &field : _particle_simulator.fields()) {
        glVertex3f(
            field->position().x,
            field->position().y,
            field->position().z
        );
    }

    glEnd();
}

void Application::animate() {
    _timer.update();
    _particle_simulator.update(_timer.getDeltaTime());
}

void Application::keyPressEvent(QKeyEvent *e) {
    const Qt::KeyboardModifiers modifiers = e->modifiers();

    if ((e->key() == Qt::Key_P) && (modifiers == Qt::NoButton)) {
        startAnimation();
        update();
    }

    if ((e->key() == Qt::Key_F)) {
        _draw_fields = !_draw_fields;
    }

    QGLViewer::keyPressEvent(e);
}