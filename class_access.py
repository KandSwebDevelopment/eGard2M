from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot
from defines import *
# from eGard import MainWindow


class Access(QObject):
    update_access_controls = pyqtSignal(int, int, name="updateAccessControl")   # An access control on main window needs updated. ctrl, state
    update_access = pyqtSignal(int)
    update_duration = pyqtSignal(int)

    def __init__(self, parent):
        super(Access, self).__init__()
        self.my_parent = parent
        self.status = 0
        # self.status_cover = 0
        # self.status_cover_lock = 0
        # self.status_cover_motor = 0
        self.status_cover_open_sw = 0
        self.status_cover_closed_sw = 0
        # self.status_door = 0
        # self.status_door_lock = 0
        self.auto_close = 0
        self.door_pos = 0
        self.cover_closed_sw = 0
        self.cover_open_sw = 0
        self.duration_remaining = 0

        self.timer_cover = QTimer()         # Cover move timer
        self.timer_cover.setInterval(1000)     # mS
        self.timer_cover.timeout.connect(self.cover_finished)

        self.timer_close = QTimer()         # The time the door has to be shut for before auto closing
        self.timer_close.setInterval(int(self.my_parent.db.get_config(CFT_ACCESS, "auto delay", 10)) * int(1000 / 2))  # mS
        self.timer_close.timeout.connect(self.close_timeout)

        self.timer_auto_close = QTimer()    # Times from auto set is pressed, stopped by door open, timeout cancels auto close
        self.timer_auto_close.setInterval(int(self.my_parent.db.get_config(CFT_ACCESS, "auto delay", 10)) * 1000)   # mS
        self.timer_auto_close.timeout.connect(self.auto_timeout)

        self.auto_close_duration = (int(self.my_parent.db.get_config(CFT_ACCESS, "auto delay", 10)) * 1000)   # mS
        self.auto_boost = int(self.my_parent.db.get_config(CFT_ACCESS, "auto boost", 1))
        self.cover_duration = int(self.my_parent.db.get_config(CFT_ACCESS, "cover time", 0))

        self.my_parent.coms_interface.update_access.connect(self.inputs_update)
        self.my_parent.coms_interface.update_switch.connect(self.switch_update)

        self.my_parent.coms_interface.send_data(COM_DOOR_POSITION, True, MODULE_DE)
        self.my_parent.coms_interface.send_data(COM_COVER_POSITION, True, MODULE_DE)
        self.my_parent.coms_interface.send_data(COM_COVER_CLOSED, True, MODULE_DE)

    @pyqtSlot(int, int, int, name="updateSwitch")   # Sw No, State, From Module
    def switch_update(self, sw, state, module):
        if not module == MODULE_DE:
            return
        if sw == SW_COVER_LOCK:
            if state == ON_RELAY:
                self.add_status(ACS_COVER_LOCKED)
                if not self.has_status(ACS_COVER_LOCKED):
                    self.my_parent.coms_interface.send_switch(SW_DOOR_LOCK, ON_RELAY, MODULE_DE)
            else:
                self.remove_status(ACS_COVER_LOCKED)
                if self.has_status(ACM_OPENING):
                    self.my_parent.coms_interface.send_switch(SW_COVER_OPEN, ON_RELAY, MODULE_DE)
                    print("open")

        elif sw == SW_DOOR_LOCK:
            if state == ON_RELAY:
                self.add_status(ACS_DOOR_LOCKED)
                if self.has_status(ACM_CLOSING):
                    self.my_parent.coms_interface.send_switch(SW_COVER_CLOSE, ON_RELAY, MODULE_DE)
                self.remove_status(ACS_AUTO_ARMED)
            else:
                self.remove_status(ACS_DOOR_LOCKED)

        elif sw == SW_COVER_OPEN:
            if state == ON_RELAY:     # Motor on to open
                self.add_status(ACS_OPENING)
                self.remove_status(ACS_COVER_CLOSED)
                if self.duration_remaining == 0:
                    self.duration_remaining = self.cover_duration
                self.timer_cover.start()
                self.update_duration.emit(self.duration_remaining)

            else:
                self.remove_status(ACS_OPENING)
                self.remove_status(ACM_OPENING)
                self.add_status(ACS_COVER_OPEN)

        elif sw == SW_COVER_CLOSE:
            if state == ON_RELAY:
                self.add_status(ACS_CLOSING)
                self.remove_status(ACS_COVER_OPEN)
                if self.duration_remaining == 0:
                    self.duration_remaining = self.cover_duration
                self.timer_cover.start()
                self.update_duration.emit(self.duration_remaining)
            else:
                self.remove_status(ACS_CLOSING)
                self.remove_status(ACM_CLOSING)
                self.add_status(ACS_COVER_CLOSED)
        self.update_access.emit(self.status)

    @pyqtSlot(int, int)
    def inputs_update(self, _input, _value):
        if _input == AUD_COVER_CLOSED:
            self.status_cover_closed_sw = _input
            if _value == 1:     # Cover not at closed
                if not self.has_status(ACM_CLOSING) and not self.has_status(ACM_OPENING):
                    # Don't send this if the cover is moving
                    self.my_parent.coms_interface.send_switch(SW_COVER_LOCK, OFF_RELAY, MODULE_DE)
            else:   # Cover at closed position
                self.my_parent.coms_interface.send_switch(SW_COVER_LOCK, ON_RELAY, MODULE_DE)
                if not self.has_status(ACS_COVER_LOCKED):
                    self.my_parent.coms_interface.send_switch(SW_DOOR_LOCK, ON_RELAY, MODULE_DE)
                self.add_status(ACS_COVER_CLOSED)
                self.remove_status(ACS_COVER_OPEN)
                self.remove_status(ACM_CLOSING)

        if _input == AUD_DOOR:
            self.door_pos = _value
            if _value == 0:     # Door open
                self.remove_status(ACS_DOOR_CLOSED)
                if self.has_status(ACS_AUTO_SET):   # Auto pressed, and door just opened
                    self.remove_status(ACS_AUTO_SET)
                    self.add_status(ACS_AUTO_ARMED)
                    self.timer_auto_close.stop()
                    self.timer_close.start()
            else:   # Door closed
                self.add_status(ACS_DOOR_CLOSED)
                if self.has_status(ACS_AUTO_ARMED):
                    self.timer_close.stop()
                    # self.remove_status(ACS_AUTO_ARMED)
                    self.my_parent.coms_interface.send_switch(SW_DOOR_LOCK, ON_RELAY, MODULE_DE)
        elif _input == AUD_COVER_OPEN:
            if _value == 1:     # Cover at open position
                self.add_status(ACS_COVER_OPEN)
                self.remove_status(ACS_COVER_CLOSED)
            else:
                self.remove_status(ACS_COVER_OPEN)
                self.add_status(ACS_COVER_CLOSED)

        if _input == AUD_AUTO_SET and _value == 1:    # Auto close has been pressed and released
            if self.door_pos != 1 or not self.has_status(ACS_COVER_OPEN):   # Only proceed if cover is open
                return
            self.auto_close = 1
            self.timer_auto_close.setInterval(self.auto_close_duration)
            self.timer_auto_close.start()
            self.add_status(ACS_AUTO_SET)
        self.update_access.emit(self.status)
        self.update_access_controls.emit(_input, _value)

    def cover_finished(self):
        if self.duration_remaining > 0:
            self.duration_remaining -= 1
            self.update_duration.emit(self.duration_remaining)
        else:
            self.timer_cover.stop()
            self.duration_remaining = 0
            self.update_duration.emit(-1)
            if self.has_status(ACS_OPENING):
                self.my_parent.coms_interface.send_switch(SW_COVER_OPEN, OFF_RELAY, MODULE_DE)
                self.my_parent.coms_interface.send_switch(SW_DOOR_LOCK, OFF_RELAY, MODULE_DE)
            else:   # Closing
                self.my_parent.coms_interface.send_switch(SW_COVER_CLOSE, OFF_RELAY, MODULE_DE)
                self.my_parent.coms_interface.send_switch(SW_COVER_LOCK, ON_RELAY, MODULE_DE)

    def open(self):
        self.add_status(ACM_OPENING)
        self.my_parent.coms_interface.send_switch(SW_COVER_LOCK, OFF_RELAY, MODULE_DE)

    def close_cover(self):
        self.add_status(ACM_CLOSING)
        self.my_parent.coms_interface.send_switch(SW_DOOR_LOCK, ON_RELAY, MODULE_DE)

    def add_status(self, status_to_add):
        self.status |= status_to_add

    def remove_status(self, status_to_remove):
        self.status &= ~status_to_remove

    def has_status(self, status_to_have):
        if self.status & status_to_have == status_to_have:
            return True
        return False

    def auto_timeout(self):
        # Auto close has timed out
        self.auto_close = 0
        self.remove_status(ACS_AUTO_SET)
        self.remove_status(ACS_AUTO_ARMED)
        self.update_access.emit(self.status)
        self.timer_auto_close.stop()

    def close_timeout(self):
        # Cancel auto close as door not closed in time
        self.remove_status(ACS_AUTO_ARMED)
        self.update_access.emit(self.status)
        self.timer_close.stop()
