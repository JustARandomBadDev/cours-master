#include "viewer.hpp"

int main(int argc, char** argv)
{
    QApplication app(argc, argv);

    Viewer viewer;

    viewer.setWindowTitle("Triangle OpenGL moderne");
    viewer.resize(800, 600);
    viewer.show();

    return app.exec();
}
