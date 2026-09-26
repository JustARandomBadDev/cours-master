#ifndef NodeSpringHEADER
#define NodeSpringHEADER

#if defined(WIN32)
#  pragma warning (disable : 4786) // disable warn truncated name with STL
#endif

#include <QGLViewer/qglviewer.h>

using namespace std;
using namespace qglviewer;

class Node
{
public:
    Node();
    Node(const Vec& p); //construct node from position
    Node(const Vec& p, double m); //construct node from position with mass

    void draw();

    Vec position;
    Vec vitesse;
    Vec acceleration;
    Vec force;

    double mass; //if mass = 0, node does not move
};

class Spring
{
public:
    Spring();
    Spring(Node *origin, Node *target, double s, double d);
    Spring(const Spring& s); //copy constructor

    void draw();

    Node * p0;
    Node * p1;
    
    double stiffness;
    double damping;
    double restLength;
};

#endif
