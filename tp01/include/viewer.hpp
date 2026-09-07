#ifndef VIEWER_HPP
#define VIEWER_HPP

#include <QApplication>
#include <QGLViewer/qglviewer.h>
#include <QOpenGLFunctions_3_3_Core>
#include <QOpenGLShaderProgram>

struct Point {
    float x;
    float y;
    float z;
};

class Viewer : public QGLViewer
{
public:
    Viewer() = default;

protected:
    void init() override;
    void draw() override;

private:
    void drawTriangle(Point p1, Point p2, Point p3);
    Point calculatePoint(float t);
    Point rotatePoint(Point p, float angle);
};

#endif
