from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer, QPoint, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel,QSplashScreen 
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor,QPixmap
from PyQt5 import QtCore, QtGui
import sys 
import cv2
import os 
from encode_faces import trainModel
global name
import imutils
name = ''
import time

class Window(QDialog): 
  
    # constructor 
    def __init__(self): 
        super(Window, self).__init__() 
  
        # setting window title 
        self.setWindowTitle("Photo Window") 
  
        # setting geometry to the window 
        self.setGeometry(100, 100, 300, 400) 
  
        # creating a group box 
        self.formGroupBox = QGroupBox("Enter settings for batch photo") 
  
        # creating spin box to select age 
        
        # creating a line edit 
        self.nameLineEdit = QLineEdit() 

        # creating a line edit 
        # self.emailLineEdit = QLineEdit() 

        # creating a line edit 
        self.iPLineEdit = QLineEdit()

        self.number = QLineEdit()
        
        self.statusLabel = QLabel('')
        
        # calling the method that create the form 
        self.createForm() 

        self.PhotoButton = QPushButton(self.tr("&Click Photo"))


        # creating a dialog button for ok and cancel 
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) 

        # self.PhotoButton = QPushButton('Click Photo')
        
        self.CancelButton = QPushButton('Cancel')
        
        self.trainModel = QPushButton('Train Model')
        
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(0)
        self.hbox.setSpacing(100)
        
        self.hbox.addWidget(self.trainModel)
        self.hbox.addWidget(self.CancelButton)
        
        # adding action when form is accepted 
        self.PhotoButton.clicked.connect(self.clickPhoto)
         
        self.trainModel.clicked.connect(self.startTraining)
  
        # addding action when form is rejected 
        self.CancelButton.clicked.connect(self.reject)


        # creating a vertical layout 
        mainLayout = QVBoxLayout() 
  
        # adding form group box to the layout 
        mainLayout.addWidget(self.formGroupBox) 
  
        # adding button box to the layout 
        mainLayout.addLayout(self.hbox) 

        mainLayout.addWidget(self.PhotoButton) 
  
        # setting lay out 
        self.setLayout(mainLayout) 
    
    def startTraining(self):
        
        self.statusLabel.setText("Please wait...")
        time.sleep(2.0)
        time.sleep(3.0)
        checkFlag=trainModel()
        if checkFlag == 1:
            self.statusLabel.setText("Training completed")
        else:
            self.statusLabel.setText("Training failed, try again")
            
        
    def clickPhoto(self):
        # self.statusLabel.setText("No Scan initalization")
        self.name=self.nameLineEdit.text()
        count=int(self.number.text())
        self.camIP = self.iPLineEdit.text()
        if self.camIP == "0":
            camIP=0
        elif self.camIP == "1":
            camIP =1
        else:
            camIP = "http://"+str(self.camIP)+"/mjpeg/1"
        
        print("pressed")
        name = self.name
        # camIP = self.camIP
        FrameCount = count
        captureFlag=False
        # FrameCount=int(self.count)
        StoragePath = os.path.join('dataset/'+name+'/')
        isExist = os.path.exists(StoragePath)  
        if isExist:
            pass
        else:
            os.mkdir(StoragePath) 

            
        cap = cv2.VideoCapture(camIP)
        while(True):
            if cap.grab():
                # Capture frame-by-frame
                ret, frame = cap.read(0)
                frame = imutils.resize(frame,width=400,height=400)

                key = cv2.waitKey(1)
                
                # frame = imutils.resize(frame,400,400)
                
                if key == ord('p'):
                    captureFlag=True
                    FrameCount=count
                
                if captureFlag==True:
                    cv2.imwrite(StoragePath+str(count-FrameCount)+'.png',frame)
                    FrameCount= FrameCount-1
                    
                    cv2.putText(frame,"Taking Pictures",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
                    
                    if FrameCount<1:
                        break 
                else:
                    cv2.putText(frame,"Press 'P' to take pictures" ,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)

                
                
                # Our operations on the frame come here
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Display the resulting frame
                
                cv2.imshow('frame',frame)
                
                
                if FrameCount<1 or cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()


        
    def getText(self):
        count=0
        while(1):
            
            text, okPressed = QInputDialog.getText(self, "Activation","Enter Password:", QLineEdit.Normal, "")
            if okPressed and text != '':
                state,days_remaining=check_Password(text)
                # print(state)
                if state==1:
                    QMessageBox.information(self, "Alert", "Days remaining "+str(days_remaining))
                    break
                elif state==2:
                    QMessageBox.warning(self, "Error", "Kindly renew your subscription")
                    sys.exit()
                elif state==3:
                    QMessageBox.warning(self, "Error", "MAC ID has not registered")
                    MAC = str(':'.join(re.findall('..', '%012x' % uuid.getnode())))
                    QMessageBox.information(self, "Alert","The MAC ID of your Computer is :"+MAC)
                    sys.exit()
                else:
                    count=count+1
                    # print(count)
                    if(count>2):
                        sys.exit()
                    continue
  
    # creat form method 
    def createForm(self): 
  
        # creating a form layout 
        layout = QFormLayout() 
  
        # adding rows 
        # for name and adding input text 
        layout.addRow(QLabel("Name:"), self.nameLineEdit) 
  
        # for degree and adding combo box 
        # layout.addRow(QLabel("Email"), self.emailLineEdit) 
  
        # for age and adding spin box 
        layout.addRow(QLabel("Camera-IP:"), self.iPLineEdit) 
  
        layout.addRow(QLabel("Number of photos:"), self.number)
        
        # layout.addRow(QLabel("Status:"),self.statusLabel)

        # setting layout 
        self.formGroupBox.setLayout(layout)


# class SetupWindow(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)
#         layout = QGridLayout()
#         self.setLayout(layout)

#         button = QPushButton("Proceed", self) 
  
#         # setting geometry of button 
#         button.setGeometry(200, 150, 100, 30) 
#         layout.addWidget(button, 1, 0)
#         # adding action to a button 
#         button.clicked.connect(self.getText) 
        
#     def getText(self):
#         global name
#         count = 0
#         name, okPressed = QInputDialog.getText(self, "BatchPhoto","Enter Name:", QLineEdit.Normal, "")
#         camera_ip, okPressed2 = QInputDialog.getText(self, "BatchPhoto","Enter Camera IP:", QLineEdit.Normal, "") 
#         self.close()
  
if __name__ == '__main__':
    state = QApplication(sys.argv)
    screen = Window()
    screen.show()
    state.exec()