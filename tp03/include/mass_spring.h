#include <QGLViewer/qglviewer.h>
#include <cstddef>

#include "node_spring.h"

using namespace std;
using namespace qglviewer;

struct State {
    std::vector<Vec> p0;
    std::vector<Vec> v0;

    std::vector<Vec> k1_p;
    std::vector<Vec> k1_v;

    std::vector<Vec> k2_p;
    std::vector<Vec> k2_v;

    std::vector<Vec> k3_p;
    std::vector<Vec> k3_v;

    std::vector<Vec> k4_p;
    std::vector<Vec> k4_v;

    void resize(std::size_t size);
    void clear();
};

class Viewer : public QGLViewer {
protected:
	virtual void draw();
	virtual void init();
	virtual void animate();
	virtual void keyPressEvent(QKeyEvent *e);
	virtual QString helpString() const;
	void computeNormals();
    
private:
    Node p1;
    Node p2;
    
    double stiffness;
    
    vector<Node *> masses;
    vector<Spring *> springs;

    double dt; //integration timestep

    Vec gravity;
    
    State state;

    void computeAccelerations();
    
    void rk(
        std::vector<Vec>& src_p,
        std::vector<Vec>& src_v,
        std::vector<Vec>& dst_p,
        std::vector<Vec>& dst_v,
        float p_dt
    );
};
