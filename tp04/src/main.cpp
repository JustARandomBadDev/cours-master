#include <qapplication.h>

#include "application.hpp"

int main(int argc, char **argv) {
    QApplication application(argc, argv);

    Application app;
    app.setWindowTitle("Particles system");
    app.show();

    return application.exec();
}
