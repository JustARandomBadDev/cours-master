#ifndef ViewerHEADER
#define ViewerHEADER

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

#include <QGLViewer/qglviewer.h>
#include <vector>
#include "BlendShape.h"
#include <QObject>

using namespace qglviewer;
using namespace std;


class Viewer : public QGLViewer
{
    Q_OBJECT
    
public:
    Viewer(QWidget *parent);
    void updateBS();

protected:
  virtual void draw();
  virtual void init();
  virtual void animate();
  virtual QString helpString() const;

private:
    //Both vectors are the same size
    vector<BlendShape*> blendshapes;
    vector<float> bs_weights;
    
public Q_SLOTS:
    void setWeight1(int value);
    void setWeight2(int value);
    void setWeight3(int value);
    void setWeight4(int value);
    void setWeight5(int value);
};

#endif
