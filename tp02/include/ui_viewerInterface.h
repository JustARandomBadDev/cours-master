#ifndef UI_VIEWERINTERFACE_H
#define UI_VIEWERINTERFACE_H

#include <QObject>
#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QSlider>
#include "Viewer.h"


QT_BEGIN_NAMESPACE

class Ui_Dialog
{
public:
    QVBoxLayout *vboxLayout;
    Viewer *viewer;
    QHBoxLayout *hboxLayout;
    QSlider *slider1;
    QSlider *slider2;
    QSlider *slider3;
    QSlider *slider4;
    QSlider *slider5;
    //TODO : Add additional sliders here

    void setupUi(QDialog *Dialog)
    {
        if (Dialog->objectName().isEmpty())
            Dialog->setObjectName(QString::fromUtf8("Dialog"));
        Dialog->resize(650, 468);
        vboxLayout = new QVBoxLayout(Dialog);
        vboxLayout->setObjectName(QString::fromUtf8("vboxLayout"));
        vboxLayout->setContentsMargins(8, 8, 8, 8);
        viewer = new Viewer(Dialog);
        viewer->setObjectName(QString::fromUtf8("viewer"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(1);
        sizePolicy.setHeightForWidth(viewer->sizePolicy().hasHeightForWidth());
        viewer->setSizePolicy(sizePolicy);

        vboxLayout->addWidget(viewer);
        
        //TODO : Instantiate additional sliders here

        slider1 = new QSlider(Qt::Horizontal, Dialog);
        slider2 = new QSlider(Qt::Horizontal, Dialog);
        slider3 = new QSlider(Qt::Horizontal, Dialog);
        slider4 = new QSlider(Qt::Horizontal, Dialog);
        slider5 = new QSlider(Qt::Horizontal, Dialog);
        vboxLayout->addWidget(slider1);
        vboxLayout->addWidget(slider2);
        vboxLayout->addWidget(slider3);
        vboxLayout->addWidget(slider4);
        vboxLayout->addWidget(slider5);

        retranslateUi(Dialog);
        
        //Connect sliders to code SIGNAL(valueChanged(int)), SLOT in viewer

        QObject::connect(
            slider1,
            &QSlider::valueChanged,
            viewer,
            &Viewer::setWeight1
        );

        QObject::connect(
            slider2,
            &QSlider::valueChanged,
            viewer,
            &Viewer::setWeight2
        );

        QObject::connect(
            slider3,
            &QSlider::valueChanged,
            viewer,
            &Viewer::setWeight3
        );

        QObject::connect(
            slider4,
            &QSlider::valueChanged,
            viewer,
            &Viewer::setWeight4
        );

        QObject::connect(
            slider5,
            &QSlider::valueChanged,
            viewer,
            &Viewer::setWeight5
        );

        QMetaObject::connectSlotsByName(Dialog);
    } // setupUi

    void retranslateUi(QDialog *Dialog)
    {
        Dialog->setWindowTitle(QCoreApplication::translate("Dialog", "BlendShapes", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Dialog: public Ui_Dialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_VIEWERINTERFACE_H
