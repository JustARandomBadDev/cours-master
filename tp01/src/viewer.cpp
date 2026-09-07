#include "viewer.hpp"
#include <GL/gl.h>
#include <cmath>

const float SIZE = 1.f;
const float DETAILS = 120.f;
const int REPEAT = 240;
const float STEP = SIZE / DETAILS;
const float ANGLE = M_PI*2/REPEAT;

void Viewer::init()
{
    glDisable(GL_LIGHTING);
    setSceneRadius(15.f);
    showEntireScene();
}

void Viewer::draw()
{
    int colorIndex = 2;

    // glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

    glBegin(GL_TRIANGLES);
        for (float angle = 0.f; angle < M_PI*2-ANGLE*0.5f; angle+=ANGLE) {
            for (float t = 0.f; t <= SIZE-STEP*0.5f; t += STEP) {
                switch (colorIndex % 3) {
                    case 0:
                        glColor3f(1.0f, 0.0f, 0.0f);
                        break;
                    case 1:
                        glColor3f(0.0f, 0.0f, 1.0f);
                        break;
                    case 2:
                        glColor3f(0.0f, 1.0f, 0.0f);
                        break;
                }

                Point p1 = calculatePoint(t);
                p1 = rotatePoint(p1, angle);

                Point p2 = calculatePoint(t+STEP);
                p2 = rotatePoint(p2, angle);

                Point p3 = calculatePoint(t);
                p3 = rotatePoint(p3, angle+ANGLE);

                Point p4 = calculatePoint(t+STEP);
                p4 = rotatePoint(p4, angle+ANGLE);

                drawTriangle(p1, p2, p3);
                drawTriangle(p2, p3, p4);

                colorIndex++;
            }
            colorIndex++;
        }
    glEnd();
}

void Viewer::drawTriangle(Point p1, Point p2, Point p3) {
    glVertex3f(p1.x, p1.y, p1.z);
    glVertex3f(p2.x, p2.y, p2.z);
    glVertex3f(p3.x, p3.y, p3.z);
}

Point Viewer::calculatePoint(float t) {
    return {
        static_cast<float>(10.f + 4.f * sin(t*M_PI*2)),
        static_cast<float>(4.f * cos(t*M_PI*2)),
        0.f
    };
}

Point Viewer::rotatePoint(Point p, float angle) {
    return {
        p.z * sin(angle) + p.x * cos(angle),
        p.y,
        p.z * cos(angle) - p.x * sin(angle)
    };
}
