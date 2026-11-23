import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer

from ui.sbh_hmi import Ui_MainWindow
from communication.fb107_comm import FB107Comm

from PyQt6.QtGui import QPixmap
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1250, 1000)
        ##self.ui.label_sbh.setGeometry(0,0,800,800)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "SBH")
        self.sbh_pixmap = QPixmap(image_path)

        
        self.ui.lbl_Control_Valve_Closed.setParent(self.ui.label_sbh)
        self.ui.lbl_Control_Valve_Opened.setParent(self.ui.label_sbh)
        self.ui.lbl_Safety_Valve_Closed.setParent(self.ui.label_sbh)
        self.ui.lbl_Safety_Valve_Opened.setParent(self.ui.label_sbh)
        self.ui.lbl_SOV_Energized.setParent(self.ui.label_sbh)
        self.ui.lbl_SOV_Denergized.setParent(self.ui.label_sbh)  
        self.ui.groupBox_1.setParent(self.ui.label_sbh)
        self.ui.groupBox_2.setParent(self.ui.label_sbh)
        #self.ui.edit_tic_sp.setParent(self.ui.label_sbh)


        self.load_image(self.ui.label_sbh, "SBH")
        self.load_image(self.ui.lbl_pilot_flame, "pilot_flame")
        self.load_image(self.ui.lbl_Burner_flame, "Burner_Flame")
        self.load_image(self.ui.lbl_Control_Valve_Closed, "Control_Valve_Closed")
        self.load_image(self.ui.lbl_Control_Valve_Opened, "Control_Valve_Opened")
        self.load_image(self.ui.lbl_Safety_Valve_Closed, "Safety_Valve_Closed")
        self.load_image(self.ui.lbl_Safety_Valve_Opened, "Safety_Valve_Opened")
        self.load_image(self.ui.lbl_SOV_Energized, "SOV_Energized")
        self.load_image(self.ui.lbl_SOV_Denergized, "SOV_Denergized")

        ##self.ui.edit_tic_sp.editingFinished.connect(self.write_tic_sp)
    
        # Communication

        self.fb107 = FB107Comm(
            port="COM6",
            baudrate=9600,
            slave_id=1
        )

        if self.fb107.connect():

            self.ui.lbl_comm_status.setText("CONNECTED")

        else:

            self.ui.lbl_comm_status.setText("DISCONNECTED")

        # Polling timer

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_process
        )

        self.timer.start(1000)

    
#################################################################################

    def load_image(self,label, image_name):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, image_name)

        pixmap = QPixmap(image_path)

        if not pixmap.isNull():
            label.setPixmap(
            pixmap.scaled(label.size())
            )
        else:
            print(f"Image not found: {image_path}")  
    
################################################################################

    def write_tic_sp(self):

        try:
            new_sp = int(
            self.ui.edit_tic_sp.text())

            reply = QMessageBox.question(
                self,
                "Confirm Setpoint Change",
                f"Do you want to change TIC SP to {new_sp} °C ?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success = self.fb107.write_register(
                    address=17,
                    value=new_sp
                )

            if success:
                QMessageBox.information(
                    self,
                    "Success",
                    f"Setpoint changed to {new_sp} °C"
                )

            else:

                QMessageBox.warning(
                    self,
                    "Write Error",
                    "Failed to write setpoint to FB107"
                )

        except ValueError:
            QMessageBox.warning(
                self,
            "Write Error",
            "Failed to write setpoint to FB107"
            )

############################################################################################


    def update_process(self):
        
        coil1 = self.fb107.read_registers( address = 2, count= 1)
        coil2 = self.fb107.read_registers( address = 3, count= 1)
        
        data = self.fb107.read_registers(address=4,count=2)
        data1 = self.fb107.read_registers(address=7,count=1)

        data2 = self.fb107.read_registers(address=8,count=1)

        pilot_flame = coil2[0]
        burner_flame = coil1[0]

        safe_sp = data[0]
        tic_sp = data[1]
        #print(data)

        tic_op = data2[0]
        
        trip = coil2[0]
        
        tic_pv = data1[0]
        safe_pv = data1[0]

        SOV_Denergized = coil2[0]
        sft_vlv = coil1[0]
        ctrl_vlv = coil1[0]
        print(coil1)
        # Flames

        self.ui.lbl_pilot_flame.setVisible(pilot_flame == 1)

        self.ui.lbl_Burner_flame.setVisible(burner_flame == 1 & pilot_flame == 1)

        self.ui.lbl_SOV_Denergized.setVisible(SOV_Denergized == 0)

        self.ui.lbl_SOV_Energized.setVisible(SOV_Denergized == 1)

        self.ui.lbl_Safety_Valve_Closed.setVisible(sft_vlv == 0)

        self.ui.lbl_Safety_Valve_Opened.setVisible(sft_vlv == 1)

        self.ui.lbl_Control_Valve_Closed.setVisible(ctrl_vlv == 0)
        
        self.ui.lbl_Control_Valve_Opened.setVisible(ctrl_vlv == 1) 

        # TIC

        self.ui.lbl_tic_sp.setText("TIC_SP  : " + str(tic_sp) + " °C")

        self.ui.lbl_tic_pv.setText("TIC_PV  : " + str(tic_pv) + " °C")

        self.ui.lbl_tic_op.setText("TIC_OP  : " + str(tic_op) + " %")

        # Safety TIC

        self.ui.lbl_safe_sp.setText("TC_SP  : " + str(safe_sp) + " °C")

        self.ui.lbl_safe_pv.setText("TC_PV  : " + str(safe_pv) + " °C")

        if trip:

            self.ui.lbl_safe_out.setText(
                "TRIP"
            )

        else:

            self.ui.lbl_safe_out.setText(
                "NORMAL"
            )


app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())