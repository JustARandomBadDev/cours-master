#ifndef BlendShapeHEADER
#define BlendShapeHEADER

#if defined(WIN32)
#  pragma warning (disable : 4786) // disable warn truncated name with STL
#endif


#include <QGLViewer/qglviewer.h>
#include "glm.h"
#include "Vertex.h"

using namespace std;
using namespace qglviewer;

class BlendShape
{
public:
    BlendShape(char *f);
    BlendShape(char *f, BlendShape * b0);

    void computeNormals();
    void computeDifferences(BlendShape * b0);
    void draw();
    
    char* fileName;
    GLMmodel *Model; // Model GLM
    
    vector<Vertex *> vertices;
    vector<int> faces;
    vector<Vec> faces_normals;
    
    vector<Vec> differences;
};


#endif
