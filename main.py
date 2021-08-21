import sys
from PyQt5 import QtWidgets
# the following try/except is in case we run mani.py from the parent directory (so the working directory would be ui in that case)

# THINGS TO REMEMBER WHEN RUNNING THIS ON A NEW PC:
# 1) [SOLVED] you don't need to do this anymore, it is automated -----> DON'T FORGET TO CREATE AN IMAGES FOLDER AT software\\back_end_logic\\ai_logic\\images
# 2) DON'T FORGET TO INSTALL opencv-contrib-python AS WELL AS REGULAR OPENCV
# 3) IF YOU GET THE cv2.cv2 does not have face error, delete and re-install opencv-contrib-python
# 4) Make sure to train a model with the ui before running the raspberry pi (if there is no ai model the raspberry pi won't work)


try:
    from mainapp import Ui_Dialog
except:
    from software.ui.mainapp import Ui_Dialog


#THIS FILE MUST BE IN THE PARENT WORKING DIRECTORY, OTHERWISE THE DATABASE WILL NOT WORK
class AppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog(self)
        self.show()



sys._excepthook = sys.excepthook

def exception_hook(exctype, value, traceback):

    #print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


app = QtWidgets.QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
