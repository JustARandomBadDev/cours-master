#include "node_spring.h"


#if defined __linux__ || defined WIN32
	#include <GL/gl.h>
	#include <GL/glu.h>
#elif defined __APPLE__
	#include <gl.h>
	#include <glu.h>
#endif

using namespace std;
using namespace qglviewer;

Node::Node()
:
position( 0.0, 0.0, 0.0 ),
vitesse(0.0, 0.0, 0.0 ),
acceleration(0.0, 0.0, 0.0 ),
force(0.0, 0.0, 0.0 ),
mass(0)
{
	
}

Node::Node(const Vec& p)
:
vitesse(0.0, 0.0, 0.0 ),
acceleration(0.0, 0.0, 0.0 ),
force(0.0, 0.0, 0.0 ),
mass(0)
{
	 position = p;
}

Node::Node(const Vec& p, double m)
:
vitesse(0.0, 0.0, 0.0 ),
acceleration(0.0, 0.0, 0.0 ),
force(0.0, 0.0, 0.0 )
{
    position = p;
    mass = m;
}

void Node::draw()
{
    //Fixed nodes are red, others are white
    if (mass == 0)
        glColor3f(1,0,0);
    else
        glColor3f(1,1,1);
    glPointSize(5);
    glBegin(GL_POINTS);
    glVertex3fv(position);
    glEnd();
}

Spring::Spring()
{}

Spring::Spring(Node *origin, Node *target, double s, double d)
{
    p0 = origin;
    p1 = target;
    stiffness = s;
    damping = d;
    Vec sp = p1->position - p0->position;
    restLength = sp.norm();
}


Spring::Spring(const Spring& s)
{
    cout << "Spring : Copy constructor not implemented." << endl;
}

void Spring::draw()
{
    glColor3f(1,1,0);
    glLineWidth(3);
    glBegin(GL_LINES);
    glVertex3fv(p0->position);
    glVertex3fv(p1->position);
    glEnd();
}
