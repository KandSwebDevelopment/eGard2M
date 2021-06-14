# Fault codes are 3 part, first is indicates what raised the fault and the second is an indicator of what the fault is,
# the 3rd part may be none but provides additional info
import collections

from defines import *

FC_MESSAGE = collections.defaultdict()
# Fault code sources
FCS_WATER_SUPPLY = 10
FCS_TANK_SYSTEM = 11
FCS_FEEDER = 15

# Fault code items
FC_NONE = 0                         # NO Faults
# Process
FC_P_NO_PROCESS = 0x20                 # No processes are running
FC_P_MANY_PROCESS = FC_P_NO_PROCESS + 1               # To many running processes have been loaded
FC_P_NO_RECIPE_STAGE_OVERRUN = FC_P_NO_PROCESS + 2    # No recipe as stage has over run
FC_P_NO_RECIPE_FOUND = FC_P_NO_PROCESS + 3            # No recipe could be found for stage and pattern
FC_P_TEMPERATURE_SCHEDULE_MISSING = FC_P_NO_PROCESS + 4
FC_P_LIGHT_SCHEDULE_MISSING = FC_P_NO_PROCESS + 5
FC_P_JOURNAL_MISSING = FC_P_NO_PROCESS + 6

# Arduino
FC_COM_COMMUTATION_OK = 0x80          # Has received command
FC_COM_HANDSHAKE_OK = FC_COM_COMMUTATION_OK + 1            # Handshake received
FC_COM_CONNECTED = FC_COM_COMMUTATION_OK + 2              # Connected to arduino
FC_COM_NO_CONNECTION = FC_COM_COMMUTATION_OK + 3           # Can not establish connection with arduino
FC_COM_HANDSHAKE_TIMEOUT = FC_COM_COMMUTATION_OK + 4       # Did not receive response to hello
FC_COM_HANDSHAKE_FAIL = FC_COM_COMMUTATION_OK + 5          # Handshake failed
FC_COM_COMMUTATION_LOST = FC_COM_COMMUTATION_OK + 6        # Coms lost
FC_COM_WAIT_REQUEST_FAILED = FC_COM_COMMUTATION_OK + 7      # A wait command wasn't received

# Feeder
FC_FR_OFF_LINE = 0x60
FC_FR_ON_LINE = FC_FR_OFF_LINE + 1
FC_FR_POT_LOW = FC_FR_OFF_LINE + 2
FC_FR_POT_RESERVE = FC_FR_OFF_LINE + 3
FC_FR_POT_EMPTY = FC_FR_OFF_LINE + 4
FC_FR_NUT_OK = FC_FR_OFF_LINE + 5
FC_FR_NUT_LOW = FC_FR_OFF_LINE + 6
FC_FR_NUT_CRITICAL = FC_FR_OFF_LINE + 7
FC_FR_NUT_EMPTY = FC_FR_OFF_LINE + 8
FC_FR_INITIALISING = FC_FR_OFF_LINE + 9

# Network
FC_NW_SERVER_FOUND = 0x40           # 64
FC_NW_SERVER_RUNNING = FC_NW_SERVER_FOUND + 1
FC_NW_SERVER_FAIL_IP = FC_NW_SERVER_FOUND + 2             # Server did not get ip address
FC_UDP_DROP = FC_NW_SERVER_FOUND + 3
FC_UDP_RUNNING = FC_NW_SERVER_FOUND + 4
FC_NW_IO_RUNNING = FC_NW_SERVER_FOUND + 5
FC_NW_SERVER_FAIL = FC_NW_SERVER_FOUND + 6
FC_NW_IO_LOST = FC_NW_SERVER_FOUND + 7
FC_NW_IO_IP_ADDRESS = FC_NW_SERVER_FOUND + 8
FC_NW_DE_LOST = FC_NW_SERVER_FOUND + 9
FC_NW_DE_FOUND = FC_NW_SERVER_FOUND + 10

# Water supply
FC_WS_CHECK = 0x50
FC_WS_CHECK_COMPLETE = FC_WS_CHECK + 1
FC_WS_MANUAL = FC_WS_CHECK + 2
FC_WS_US_READ_FAIL = FC_WS_CHECK + 3                # Reading can not be obtained from an us module, no reading came back.
FC_WS_US_TIME_OUT = FC_WS_US_READ_FAIL               # Timed out, tank didn't fill in allocated time
FC_WS_HEATER_FLOAT_DOWN = FC_WS_CHECK + 4           # Water heater on and float down
FC_WS_MIX_COMPLETE = FC_WS_CHECK + 5                # Mix completed
FC_WS_FILL_COMPLETE = FC_WS_CHECK + 6               # Fill completed
FC_WS_FLUSH_COMPLETE = FC_WS_CHECK + 7              # Flush complete
FC_WS_DRAIN_COMPLETE = FC_WS_CHECK + 8              # Drain complete
FC_WS_MIX_OVERFLOW = FC_WS_CHECK + 9                # Mix tank overflow

# Messages
FC_MESSAGE[FC_NONE] = {"msg": "..None..", "message": "...None...", "level": WARNING}

FC_MESSAGE[FC_COM_NO_CONNECTION] = {"msg": "Not Connected", "message": "Unable to connect to the interface unit", "level": WARNING}
FC_MESSAGE[FC_COM_CONNECTED] = {"msg": "Connected", "message": "Unable to connect to the interface unit", "level": PENDING}
FC_MESSAGE[FC_COM_COMMUTATION_OK] = {"msg": "Streaming", "message": "The interface unit is streaming data", "level": OK}
FC_MESSAGE[FC_COM_HANDSHAKE_OK] = {"msg": "Handshake OK", "message": "Connected to the interface unit", "level": PENDING}
FC_MESSAGE[FC_COM_HANDSHAKE_TIMEOUT] = {"msg": "Timeout", "message": "Connected to the interface unit but it is not responding", "level": WARNING}
FC_MESSAGE[FC_COM_HANDSHAKE_FAIL] = {"msg": "Handshake Fail", "message": "Connected to the interface unit but it is not responding", "level": WARNING}
FC_MESSAGE[FC_COM_COMMUTATION_LOST] = {"msg": "Lost", "message": "Communications with the interface unit has been lost", "level": WARNING}

FC_MESSAGE[FC_FR_ON_LINE] = {"msg": "On line", "message": "The Feeder is ready and online", "level": OK}
FC_MESSAGE[FC_FR_OFF_LINE] = {"msg": "OFF line", "message": "The Feeder has a fault and is OFF line", "level": CRITICAL}
FC_MESSAGE[FC_FR_INITIALISING] = {"msg": "Initialising", "message": "The Feeder is starting up", "level": OPERATE}
FC_MESSAGE[FC_FR_POT_LOW] = {"msg": "On line", "message": "Check the Feeder's pots, running low", "level": WARNING, "info": "The following pot{} are low. {}"}
FC_MESSAGE[FC_FR_POT_RESERVE] = {"msg": "On line", "message": "Top up the Feeder. Pot in reserve", "level": ERROR}
FC_MESSAGE[FC_FR_POT_EMPTY] = {"msg": "OFF line", "message": "The Feeder has a fault and is OFF line", "level": CRITICAL}
FC_MESSAGE[FC_FR_NUT_OK] = {"msg": "Ok", "message": "Nutrient levels OK", "level": OK}
FC_MESSAGE[FC_FR_NUT_LOW] = {"msg": "Low", "message": "Nutrient level low limited stock", "level": WARNING, "info": "The following pot{} are low. {}"}
FC_MESSAGE[FC_FR_NUT_CRITICAL] = {"msg": "Critical", "message": "Nutrient level critical and will run out soon", "level": ERROR}
FC_MESSAGE[FC_FR_NUT_EMPTY] = {"msg": "Empty", "message": "A nutrient has run out, how did you let that happen", "level": CRITICAL}

FC_MESSAGE[FC_P_NO_PROCESS] = {"msg": "", "message": "There are no processes currently running", "level": WARNING}
FC_MESSAGE[FC_P_MANY_PROCESS] = {"msg": "", "message": "There are more than 3 processes running", "level": WARNING}

FC_MESSAGE[FC_NW_SERVER_FOUND] = {"msg": "Server present", "message": "The server had been located", "level": PENDING}
FC_MESSAGE[FC_NW_SERVER_RUNNING] = {"msg": "Server running", "message": "The server is running", "level": OK}
# FC_MESSAGE[FC_NW_CLIENT_FOUND] = {"msg": "Remote Online", "message": "The client had been located", "level": OK}
FC_MESSAGE[FC_NW_SERVER_FAIL] = {"msg": "Dropped", "message": "The server was lost", "level": ERROR}
FC_MESSAGE[FC_NW_IO_RUNNING] = {"msg": "I/O Connected", "message": "The client has connected to the {} computer", "level": OK}
FC_MESSAGE[FC_NW_SERVER_FAIL_IP] = {"msg": "No Connection", "message": "The server was unable to start", "level": WARNING}
FC_MESSAGE[FC_NW_IO_LOST] = {"msg": "I/O Dropped", "message": "The IO is connected but dropped a packet", "level": WARNING}
FC_MESSAGE[FC_NW_IO_IP_ADDRESS] = {"msg": "I/O Address", "message": "There is no IP address for the I/O unit", "level": CRITICAL}
FC_MESSAGE[FC_NW_IO_LOST] = {"msg": "I/O Lost", "message": "Communications with the I/O unit has been lost", "level": WARNING}
FC_MESSAGE[FC_NW_DE_LOST] = {"msg": "D/E Lost", "message": "Communications with the D/E unit has been lost", "level": WARNING}
FC_MESSAGE[FC_NW_DE_FOUND] = {"msg": "D/E Connected", "message": "The D/E Unit is connected", "level": OK}

FC_MESSAGE[FC_WS_CHECK] = {"msg": "Checking", "message": "The water levels are being checked", "level": OPERATE}
FC_MESSAGE[FC_WS_CHECK_COMPLETE] = {"msg": "Levels Ok", "message": "The water levels have been checked", "level": OK}
FC_MESSAGE[FC_WS_US_READ_FAIL] = {"msg": "Fault", "message": "Tank level sensor has failed", "level": CRITICAL, 'info': ""}
FC_MESSAGE[FC_WS_MANUAL] = {"msg": "Manual", "message": "The water sypply is in manual mode", "level": INFO, 'info': "The tank {} has not filled within the allocated time"}
FC_MESSAGE[FC_WS_HEATER_FLOAT_DOWN] = {"msg": "Fault", "message": "The water heater was switched off due to low level", "level": WARNING, 'info': "The float switch in tank {} opened"}
FC_MESSAGE[FC_WS_MIX_OVERFLOW] = {"msg": "Fault", "message": "The mix tank has over filled", "level": WARNING, 'info': "The over fill sensor has tripped"}
