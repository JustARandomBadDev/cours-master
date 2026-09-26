#include "mass_spring.h"

#include <QKeyEvent>

using namespace qglviewer;
using namespace std;

void State::resize(std::size_t size) {
    p0.resize(size);
    v0.resize(size);
    k1_p.resize(size);
    k1_v.resize(size);
    k2_p.resize(size);
    k2_v.resize(size);
    k3_p.resize(size);
    k3_v.resize(size);
    k4_p.resize(size);
    k4_v.resize(size);
}

void State::clear() {
    p0.clear();
    v0.clear();
    k1_p.clear();
    k1_v.clear();
    k2_p.clear();
    k2_v.clear();
    k3_p.clear();
    k3_v.clear();
    k4_p.clear();
    k4_v.clear();
}

///////////////////////   V i e w e r  ///////////////////////
void Viewer::init()
{
 
    glDisable(GL_LIGHTING);
  setGridIsDrawn();
    setSceneRadius(50);
  help();

    masses.clear();
    springs.clear();
    //Create springs here
    //1 spring
    Node* n1 = new Node(Vec(2,0,20), 1000000000000000000); //fixed node
    Node* n2 = new Node(Vec(2,0,15), 1); //mass 1kg
    Node* n3 = new Node(Vec(2,0,10), 1);
    masses.push_back(n1);
    masses.push_back(n2);
    masses.push_back(n3);
    Spring * s1 = new Spring(n1, n2, 5, 1);
    Spring * s2 = new Spring(n2, n3, 5, 1);
    springs.push_back(s1);
    springs.push_back(s2);
    
    dt = 0.01; //in seconds
    gravity = Vec(0,0,-0.1);
    setAnimationPeriod(10); //in milliseconds

    state.resize(masses.size());
}

void Viewer::draw()
{
    //Draw masses
    for (vector<Node *>::iterator nit = masses.begin();
         nit != masses.end(); nit++)
    {
        (*nit)->draw();
    }
    
    //Draw springs
    for (vector<Spring *>::iterator sit = springs.begin();
         sit != springs.end(); sit++)
    {
        (*sit)->draw();
    }

}

void Viewer::animate()
{
    const size_t count = masses.size();

    state.clear();
    state.resize(count);

    for (size_t i = 0; i < count; i++) {
        state.p0[i] = masses[i]->position;
        state.v0[i] = masses[i]->vitesse;
    }

    computeAccelerations();

    for (size_t i = 0; i < count; i++) {
        state.k1_p[i] = masses[i]->vitesse;
        state.k1_v[i] = masses[i]->acceleration;
    }

    rk(state.k1_p, state.k1_v, state.k2_p, state.k2_v, dt / 2.);
    rk(state.k2_p, state.k2_v, state.k3_p, state.k3_v, dt / 2.);
    rk(state.k3_p, state.k3_v, state.k4_p, state.k4_v, dt);
    
    for (size_t i = 0; i < count; i++) {
        if (masses[i]->mass <= 0.) {
            masses[i]->position = state.p0[i];
            masses[i]->vitesse = state.v0[i];
            continue;
        }

        masses[i]->position = state.p0[i] + (state.k1_p[i] + 2. * state.k2_p[i] + 2. * state.k3_p[i] + state.k4_p[i]) * (dt / 6.);
        masses[i]->vitesse = state.v0[i] + (state.k1_v[i] + 2. * state.k2_v[i] + 2. * state.k3_v[i] + state.k4_v[i]) * (dt / 6.);
    }
}

void Viewer::keyPressEvent(QKeyEvent *e) {
	// Get event modifiers key
	const Qt::KeyboardModifiers modifiers = e->modifiers();

	//Key to start animation
	if ((e->key() == Qt::Key_P) && (modifiers == Qt::NoButton))
	{
		startAnimation();
		masses[2]->position += Vec(0, 0, -10);
		update();
	}

	QGLViewer::keyPressEvent(e);
}

QString Viewer::helpString() const {
  QString text("<h2>A n i m a t i o n</h2>");
  text += "Use the <i>animate()</i> function to implement the animation part "
          "of your ";
  text += "application. Once the animation is started, <i>animate()</i> and "
          "<i>draw()</i> ";
  text += "are called in an infinite loop, at a frequency that can be "
          "fixed.<br><br>";
  text += "Press <b>Return</b> to start/stop the animation.";
  return text;
}

void Viewer::computeAccelerations() {
    for (const auto node : masses) {
        node->force = Vec(0, 0, 0);
    }
    
    for (const auto spring : springs) {
        auto n1 = spring->p0;
        auto n2 = spring->p1;

        Vec dt_v = n2->position - n1->position;
        double length = dt_v.norm();

        if (length == 0.0)
            continue;

        Vec n = dt_v / length;

        Vec force = (
            spring->stiffness *
            (length - spring->restLength) +
            spring->damping *
            ((n2->vitesse - n1->vitesse) * n)
        ) * n;

        n1->force += force;
        n2->force -= force;
    }

    for (const auto node : masses) {
        if (node->mass <= 0.0) {
            node->acceleration = Vec(0, 0, 0);
            continue;
        }

        node->acceleration = node->force / node->mass;
    }
}

void Viewer::rk(
    std::vector<Vec>& src_p,
    std::vector<Vec>& src_v,
    std::vector<Vec>& dst_p,
    std::vector<Vec>& dst_v,
    float p_dt
) {
    for (size_t i = 0; i < masses.size(); i++) {
        if (masses[i]->mass <= 0.0) continue;
        masses[i]->position = state.p0[i] + src_p[i] * p_dt;
        masses[i]->vitesse = state.v0[i] + src_v[i] * p_dt;
    }

    computeAccelerations();

    for (size_t i = 0; i < masses.size(); i++) {
        dst_p[i] = masses[i]->vitesse;
        dst_v[i] = masses[i]->acceleration;
    }
}