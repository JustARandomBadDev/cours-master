#include <stdexcept>
#define GL_SILENCE_DEPRECATION
#include "BlendShape.h"


BlendShape::BlendShape(char *f)
{
    fileName = f;
    Model = glmReadOBJ(fileName); //Reads .obj model file

    /* On remplit la liste de triangles */
    GLfloat * v = Model->vertices;
    //GLfloat * nor = Model->normals;
    int n = Model->numvertices;
    cerr << "nb sommets = " << n << endl;
    
    vertices.clear();
    faces.clear();
   
    /* Store vertices */
    for (int i = 3; i< (int)(n+1)*3; i++)
    //for (int i = 0; i< (int)(n)*3; i++) //ne fonctionne pas, va savoir pkoi...
    {
        Vertex * p = new Vertex;
        p->position.setValue(v[i], v[i+1], v[i+2]);
        p->positionCour.setValue(v[i], v[i+1], v[i+2]);
        p->posSkinnee.setValue(v[i], v[i+1], v[i+2]);
        i+=2;
       
        //cout << "position = " << p->position[0] << " " << p->position[1] << " " << p->position[2] << endl;

        vertices.push_back(p);
    }
   
    /* Store faces */
    GLMtriangle * v2 = Model->triangles;
    n = Model->numtriangles;
    cerr << "nb faces = " << n << endl;
   
    for (int i = 0; i<n; i++)
    {
        faces.push_back( v2[i].vindices[0] - 1 ); //-1 car les vertices sont numerotes a partir de 1
        faces.push_back( v2[i].vindices[1] - 1 );
        faces.push_back( v2[i].vindices[2] - 1 );
    }
    
    computeNormals();
    cerr << "Model loaded (faces + texture)" << endl;

}

BlendShape::BlendShape(char *f, BlendShape * b0)
{
    fileName = f;
    Model = glmReadOBJ(fileName); //Reads .obj model file

    /* On remplit la liste de triangles */
    GLfloat * v = Model->vertices;
    //GLfloat * nor = Model->normals;
    int n = Model->numvertices;
    cerr << "nb sommets = " << n << endl;
    
    vertices.clear();
    faces.clear();
   
    /* Store vertices */
    for (int i = 3; i< (int)(n+1)*3; i++)
    //for (int i = 0; i< (int)(n)*3; i++) //ne fonctionne pas, va savoir pkoi...
    {
        Vertex * p = new Vertex;
        p->position.setValue(v[i], v[i+1], v[i+2]);
        p->positionCour.setValue(v[i], v[i+1], v[i+2]);
        p->posSkinnee.setValue(v[i], v[i+1], v[i+2]);
        i+=2;
       
        //cout << "position = " << p->position[0] << " " << p->position[1] << " " << p->position[2] << endl;

        vertices.push_back(p);
    }
   
    /* Store faces */
    GLMtriangle * v2 = Model->triangles;
    n = Model->numtriangles;
    cerr << "nb faces = " << n << endl;
   
    for (int i = 0; i<n; i++)
    {
        faces.push_back( v2[i].vindices[0] - 1 ); //-1 car les vertices sont numerotes a partir de 1
        faces.push_back( v2[i].vindices[1] - 1 );
        faces.push_back( v2[i].vindices[2] - 1 );
    }
    
    computeNormals();
    cerr << "Model loaded (faces + texture)" << endl;

    computeDifferences(b0);
    cerr << "Differences computed" << endl;
}

void BlendShape::computeDifferences(BlendShape * b0)
{
    if (vertices.size() != b0->vertices.size())
        throw std::runtime_error("Cannot compute differences if BlendShape don't have the same size !");

    differences.resize(
        vertices.size(),
        {0.f, 0.f, 0.f}
    );

    for (int i = 0; i < vertices.size(); i++) {
        differences[i] = vertices[i]->position - b0->vertices[i]->position;
    }
}

void BlendShape::computeNormals()
{
    cout << "faces.size = " << faces.size() << endl;
    faces_normals.clear();
    //Iteration sur tous les points pour mettre les normales a 0
    for (vector<Vertex*>::iterator vit = vertices.begin();
         vit != vertices.end(); vit++)
      { (*vit)->normal = Vec(0,0,0);}
    
    for (std::vector<int>::iterator fit = faces.begin();
               fit != faces.end(); ++fit)
    {
        Vertex * p1 = vertices[(* fit)];
        fit++;
        Vertex * p2 = vertices[(* fit)];
        fit++;
        Vertex * p3 = vertices[(* fit)];
        Vec n = (p2->position - p1->position) ^ (p3->position - p1->position);
        p1->normal += n;
        p2->normal += n;
        p3->normal += n;
        n.normalize();
        faces_normals.push_back(n);
    }
    //Normalisation des normales par point
    
    for (vector<Vertex*>::iterator vit = vertices.begin();
         vit != vertices.end(); vit++)
    { (*vit)->normal.normalize();}
    
}

void BlendShape::draw()
{
    bool showvertices = false;
    bool showtriangles = true;
    bool flatshaded = false;
    bool wireframe = false;
    
    //Draw vertices
    if (showvertices)
    {
        glColor3f(1.0, 0.0, 0.0);
        glBegin(GL_POINTS);
        for (vector<Vertex*>::iterator vit = vertices.begin();
             vit != vertices.end(); vit++)
        {
            (*vit)->drawCour();
            
        }
        glEnd();
    }

    //Draw triangles, wireframe or not
    if (showtriangles)
    {
        if (flatshaded)
            glShadeModel(GL_FLAT);
        else
            glShadeModel(GL_SMOOTH);
        
        if (wireframe)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE); //wireframe
        else
            glPolygonMode(GL_FRONT, GL_FILL);
        
        glColor4f( 0.87, 0.69, 0.58, 1.0 );
        
        glBegin( GL_TRIANGLES );
        int facenumber = 0;
        for (std::vector<int>::iterator fit = faces.begin();
             fit != faces.end(); ++fit)
        {
            if (flatshaded)
            {
                glNormal3fv(faces_normals[facenumber/3]); //FLAT SHADING
            }
            else
                glNormal3fv(vertices[(* fit)]->normal); //Normal per point
            
            vertices[(* fit)]->drawCour();
            
            facenumber++;
        }
        glEnd();
    }
}

