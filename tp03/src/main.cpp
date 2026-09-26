#include <qapplication.h>

#include "mass_spring.h"

int main(int argc, char **argv) {
  QApplication application(argc, argv);

  Viewer viewer;
  viewer.setWindowTitle("Mass Spring Simulation");
  viewer.show();

  return application.exec();
}
