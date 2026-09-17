/****************************************************************************

 Copyright (C) 2002-2014 Gilles Debunne. All rights reserved.

 This file is part of the QGLViewer library version 2.8.0.

 http://www.libqglviewer.com - contact@libqglviewer.com

 This file may be used under the terms of the GNU General Public License 
 versions 2.0 or 3.0 as published by the Free Software Foundation and
 appearing in the LICENSE file included in the packaging of this file.
 In addition, as a special exception, Gilles Debunne gives you certain 
 additional rights, described in the file GPL_EXCEPTION in this package.

 libQGLViewer uses dual licensing. Commercial/proprietary software must
 purchase a libQGLViewer Commercial License.

 This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
 WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

*****************************************************************************/
#define GL_SILENCE_DEPRECATION

#include "Viewer.h"
#include "BlendShape.h"
#include <math.h>
#include <stdlib.h> // RAND_MAX

using namespace qglviewer;
using namespace std;

// Constructor must call the base class constructor.
Viewer::Viewer(QWidget *parent) : QGLViewer(parent)
{
  help();
}


void Viewer::updateBS()
{
    cout << "slider moved" << endl;
    //TODO : compute shape (blendshapes[0]) from the blendshapes and the weights

    for (size_t i = 0; i < blendshapes[0]->vertices.size(); ++i) {
        Vec position = blendshapes[0]->vertices[i]->position;

        for (size_t j = 1; j < blendshapes.size(); ++j) {
            position += blendshapes[j]->differences[i] * bs_weights[j];
        }
        
        blendshapes[0]->vertices[i]->positionCour = position;
    }
    
    update(); //To refresh rendering
    cout << "bs updated" << endl;
}

///////////////////////   V i e w e r  ///////////////////////
void Viewer::init() {
  
  //Load blendshapes
    BlendShape * bs = new BlendShape("./assets/bs/face_00.obj");
    blendshapes.push_back(bs);
    bs_weights.push_back(0);
    
    bs = new BlendShape("./assets/bs/face_01.obj", blendshapes[0]);
    blendshapes.push_back(bs);
    bs_weights.push_back(0);
    bs = new BlendShape("./assets/bs/face_02.obj", blendshapes[0]);
    blendshapes.push_back(bs);
    bs_weights.push_back(0);
    bs = new BlendShape("./assets/bs/face_03.obj", blendshapes[0]);
    blendshapes.push_back(bs);
    bs_weights.push_back(0);
    bs = new BlendShape("./assets/bs/face_04.obj", blendshapes[0]);
    blendshapes.push_back(bs);
    bs_weights.push_back(0);
    bs = new BlendShape("./assets/bs/face_05.obj", blendshapes[0]);
    blendshapes.push_back(bs);
    bs_weights.push_back(0);
    
    setGridIsDrawn();
    setSceneRadius(10);
    
}

void Viewer::draw()
{
    //draws neutral shape
  if (blendshapes.size() > 0)
  {
      blendshapes[0]->draw();
      glMatrixMode(GL_MODELVIEW);
      glPushMatrix();
      glTranslatef(0, 1.5, 0);
      blendshapes[1]->draw();
      glPopMatrix();
      glPushMatrix();
      glTranslatef(1, 1.5, 0);
      blendshapes[2]->draw();
      glPopMatrix();
      glPushMatrix();
      glTranslatef(1, 0, 0);
      blendshapes[3]->draw();
      glPopMatrix();
      glPushMatrix();
      glTranslatef(1, -1.5, 0);
      blendshapes[4]->draw();
      glPopMatrix();
      glPushMatrix();
      glTranslatef(0, -1.5, 0);
      blendshapes[5]->draw();
      glPopMatrix();

  }
}

void Viewer::animate()
{
  
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

void Viewer::setWeight1(int value)
{
    bs_weights[1] = value / 100.0f;
    updateBS();
}

void Viewer::setWeight2(int value)
{
    bs_weights[2] = value / 100.0f;
    updateBS();
}

void Viewer::setWeight3(int value)
{
    bs_weights[3] = value / 100.0f;
    updateBS();
}

void Viewer::setWeight4(int value)
{
    bs_weights[4] = value / 100.0f;
    updateBS();
}

void Viewer::setWeight5(int value)
{
    bs_weights[5] = value / 100.0f;
    updateBS();
}