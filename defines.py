
from PyQt5.QtGui import QColor

# Mode of operation
MASTER = 1
SLAVE = 2

# Mode of coms
# MASTER_COM = 1
# SLAVE_COM = 2

# Settings File Name
FN_SETTINGS = "eGard02M.ini"
# DATA_SETTINGS = "eGardner.dat"

# General
DAY = 1
NIGHT = 2
MANUAL = -1
ON = 1
OFF = 0
ON_RELAY = 0
OFF_RELAY = 1
UNSET = -1
FEED = 1
FLUSH = 2
TAB = "    "
OPEN = 1
CLOSED = 0
COOL = 1
WARM = 2
NORMAL = 0

# Date formats
DF_DMY = "%d/%m/%y"
DF_YMD = "%y/%m/%d"
DF_HMS = "%H/%M/%S"

# Error Levels
CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
# Other levels
OK = INFO
PENDING = 2
OPERATE = 3

WATER_ONLY = "Water Only"
WATER_ONLY_IDX = 100

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
MONTHS_S = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# colours
OK_BG = "springgreen"
OK_FG = "black"
PENDING_BG = "darkturquoise"
PENDING_FG = "black"
OPERATE_BG = "skyblue"
OPERATE_FG = "black"
CRITICAL_BG = "red"
CRITICAL_FG = "yellow"
ERROR_BG = "orangered"
ERROR_FG = "white"
WARNING_BG = "orange"
WARNING_FG = "black"
INFO_BG = "limegreen"
INFO_FG = "black"
BACKGROUND_DEFAULT = "background-color: #f0f0f0;"
CRITICAL_FG_QT = QColor(CRITICAL_FG)
CRITICAL_BG_QT = QColor(CRITICAL_BG)    # .lighter(130)
ERROR_FG_QT = QColor(ERROR_FG)
ERROR_BG_QT = QColor(ERROR_BG)
WARNING_FG_QT = QColor(WARNING_FG)
WARNING_BG_QT = QColor(WARNING_BG)
INFO_FG_QT = QColor(INFO_FG)
INFO_BG_QT = QColor(INFO_BG)

# Access Control
# Mode
ACM_SLEEP = 1024
ACM_OPENING = 2048
ACM_CLOSING = 4096
ACM_AUTO_SET = 8192
# Status
ACS_DOOR_LOCKED = 1
ACS_COVER_LOCKED = 2
ACS_OPENING = 4
ACS_CLOSING = 8
ACS_STOPPED = 16
ACS_AUTO_SET = 32
ACS_AUTO_ARMED = 64
ACS_DOOR_CLOSED = 128
ACS_COVER_CLOSED = 256
ACS_COVER_OPEN = 512

# After load actions - thing user has to answer
ALA_SET_LAST_FEED_DATE_1 = 1
ALA_SET_LAST_FEED_DATE_2 = 2
ALA_MISSING_TEMPERATURE_SCHEDULE_1 = 5
ALA_MISSING_TEMPERATURE_SCHEDULE_2 = 6
ALA_MISSING_FEED_SCHEDULE = 8

# Access Update Items
AUD_DOOR = 1
AUD_COVER_OPEN = 2
AUD_COVER_CLOSED = 3
AUD_AUTO_SET = 4
AUD_SLEEP = 5

# Config table titles and keys
CFT_ACCESS = "access"
CFT_AREA = "area"
CFT_DE_UNIT = "module de"
CFT_DISPATCH = "dispatch"
CFT_DRYING = "drying"
CFT_FANS = "fans"
CFT_FEEDER = "feeder"
CFT_IO_UNIT = "module io"
CFT_LOGGER = "logger"
CFT_PROCESS = "process"
CFT_SS_UNIT = "module ss"
CFT_NETWORK = "network"
CFT_MODULES = "modules"
CFT_NOTIFIER = "notifier"
CFT_SOIL_SENSORS = "soil sensor"
CFT_SYSTEM = "system"
CFT_SCALES = "scales"
CFT_SOIL_LIMITS = "soil limits"
CFT_WATER_HEATER = "water heater"
CFT_WATER_SUPPLY = "water supply"
CFT_WORKSHOP_HEATER = "workshop heater"


# Communication commands
COM_SENSOR_READ = "sensor_read"
COM_SOIL_READ = "soil_reading"
COM_US_READ = "us reading"
COM_OTHER_READINGS = "other_reading"
COM_OW_COUNT = "ow_sensor_refresh"
COM_OW_SCAN = "ow_scan"
COM_FANS = "fans"               # This is the temperature reading from the sensors for the fans
COM_FLOAT_SWITCHES = "float"
CMD_SWITCH = "switch"
COM_SWITCH_POS = "pos_sw"
CMD_FEEDER_OPERATE = "feeder operate"
COM_IO_REBOOT = "reboot"            # Reboot IO
CMD_IO_RESTART = "BOOT"          # IO Unit has rebooted
CMD_SET_FAN_SENSOR = "f_sensor fan"       # Set sensor number for fan, send fan num, sensor num
CMD_GET_FAN_SPEED = "g_fan speed"       # Get fan speed
# CMD_SET_FAN_SENSOR = "sensor fan"       # Set sensor number for fan, send fan num, sensor num
CMD_GET_FAN_SENSOR = "get fan"       # Get sensor number for fan current set in IO unit, send fan num
CMD_FAN_SPEED = "speed"                 # Set fan speed  fan number, speed

# Feeder Unit
CMD_CANCEL_SW = "cancel_sw"
COM_DRAIN_END = "drain_end"
CMD_FU_BOOT = "BOOT_FU"                     # IO Unit has rebooted
COM_FU_RESTART = "reboot"
COM_FEEDER_STATUS = "feeder status"
COM_FILL_END = "fill_end"
COM_MIX_READ_LEVEL = "read_scale"
COM_MIX_FILL = "mix_fill"                   # Fill mix tank to required level. Send required level in millilitres, tank to fill from
COM_MIX_TARE = "tare_1"
COM_MIX_CAL_1 = "cal_1a"
COM_MIX_CAL_2 = "cal_1b"
COM_MIX_SET_CAL = "set_cal"
COM_MIX_POWER = "scales_power"
COM_MIX_GET_CAL = "get_cal"
COM_MIX_FILL_END = "mix_fill_end"           # Received only, indicates mix fill is finished
COM_MIX_FILL_STALL = "mix_fill_stall"       # Mix tank filling has stopped filling before required level, empty water tank
COM_MIX_OVER_STATUS = "mix overflow status"
COM_MIX_FILL_STOP = "stop_m_fill"
COM_MIX_DISPENSE = "mix_dispense"           # Pumps out from mix tank required amount. Send millilitres to be left in tank when finished
COM_MIX_DISPENSE_END = "mix_dispense_end"   # Received only, indicates mix dispense is finished
COM_MIX_DISPENSE_STOP = "stop_dispense"
COM_MIX_EMPTY = "empty_mix"                 # Empty's mix tank
COM_SERVO_POS = "servo_pos"                 # Get servo pos, send servo number
COM_SERVO_REPORT = "report_servos"          # Get position of all 9 servo valves
COM_SERVOS_CLOSE = "close_all"              # Closes All servos
COM_SIGNAL_INPUT = "signal_input"           # Read the input signal pin, send signal number 1 or 2
COM_STOP_DRAIN = "stop_drain"
COM_STOP_FILL = "stop_fill"
CMD_SWITCH_TIMED = "sw_timed"               # Timed switch, send sw number, state, duration in milliseconds
COM_TANK_LEVEL = "tank_level"               # Request water tank level, send tank number
COM_TANK_FILL = "fill_tank"                 # Fill water tank to required level. Send tank number and required Reading
COM_TANK_DRAIN = "tank_drain"               # Drain tank, send tank number and required reading
COM_TRAY_POS = "tray_pos"                   # Tray positions
CMD_VALVE_CLUSTER = "cluster"
CMD_VALVE = "valve"                         # Operate servo valve

# DE Module
COM_WATTS = "watts"
COM_KWH = "kWh"
COM_COVER_POSITION = "cover pos"    # Requests the cover position
COM_DOOR_POSITION = "door pos"      # Requests the door position
COM_AUTO_SET = "auto set"           # Requests the auto set value. Unlikely to used as this will always be 1 unless button is pressed
COM_COVER_CLOSED = "reserved"       # The limit switch at the cover closed position
CMD_SET_KWH = "set kwh"             # Sets a new stored kWh value
COM_READ_KWH = "read kwh"           # Get a kWh reading
COM_KWH_DIF = "kw dif"              # the kWh difference between each store. If this value is to large data may be lost during low power consumption
CMD_KWH_DIF = "set kw dif"          # sets above
COM_SEND_FREQ = "send freq"         # how often the watts reading is sent
CMD_SEND_FREQ = "set send freq"     # sets above
COM_PULSES = "get pulses"
CMD_SET_PULSES = "set pulses"
CMD_REBOOT = "reboot"               # Reboots the unit


# Table Names
DB_AREAS = "areas"                              # What processes and items are in what area
DB_CLIENTS = "clients"
DB_CLIENT_PLANS = "client_plans"
DB_CONFIG = "config"
DB_DISPATCH = "dispatch"
DB_FANS = "fans"
DB_FEED_SCHEDULES = "feed_schedules"
DB_FEED_SCHEDULE_NAMES = "feed_schedule_names"
DB_FEEDER_POTS = "feeder_pots"
DB_FLUSHING = "flushing"
DB_ELECTRIC = "electrict_price"
DB_JARS = "storage"
DB_LIGHT = "lightschedules"
DB_LIGHT_NAMES = "light_schedule_names"
DB_LOCATIONS = "locations"
DB_MESSAGES = "messages"
DB_MESSAGE_SYSTEM = "message_system"
DB_NUTRIENTS_NAMES = "nutrient_names"
DB_NUTRIENT_PROPERTIES = "nutrient_properties"
DB_ONE_WIRE = "one_wires"
DB_OUTPUTS = "outputs"
DB_PROCESS = "processes"
DB_PROCESS_ADJUSTMENTS = "process_adjustments"
DB_PROCESS_DRYING = "process_drying"
DB_PROCESS_FEED_ADJUSTMENTS = "process_feed_adjustments"
DB_PROCESS_PATTERNS = "process_patterns"
DB_PROCESS_TEMPERATURE = "process_temperature_adjustments"
DB_PROCESS_MIXES = "mixes"
DB_PATTERN_NAMES = "pattern_names"
DB_PROCESS_STRAINS = "process_strains"
DB_RANGES = "rangevalues"
DB_RECIPE_NAMES = "recipe_names"
DB_RECIPES = "recipes"
DB_RECIPE_CHANGES = "recipe_changes"
DB_RECIPE_SUPPLEMENTS = "recipe_supplements"
DB_STAGE_NAMES = "stage_names"
DB_STAGE_PATTERNS = "stage_patterns"
DB_STRAINS = "strains"
DB_SENSORS_CONFIG = "sensor_config"
DB_SOIL_SENSORS = "soil_sensors"
DB_TANK_CONVERSION = "tank_reading_to_litres"
DB_TEMPERATURES = "temperature_ranges"
DB_TEMPERATURES_DEFAULT = "temperature_defaults"
DB_TEMPERATURE_NAMES = "temperature_range_names"

# Detection types - type of sensor change to trigger output
DET_NONE = 0
DET_RISE = 1    # Trig output when sensor value rises to limit
DET_FALL = 2    # Trig output when sensor value falls to limit
DET_TIMER = 4   # Output is trig by timer. Can be OR with above

# Display IDs
DID_OUTSIDE_H = 0
DID_OUTSIDE_T = 1
DID_A1_H = 2
DID_A1_T = 3
DID_A1_PROCESS = 4
DID_A1_CORE = 5
DID_A2_H = 6
DID_A2_T = 7
DID_A2_PROCESS = 8
DID_A2_CORE = 9
DID_WORKSHOP = 10
DID_A3_H = 11
DID_A3_T = 12

# Float switch states
FLOAT_UP = 0
FLOAT_DOWN = 1

# Feed modes
FEED_MANUAL = 1
FEED_SEMI = 2
FEED_AUTO = 3

# Info names
IF_ID = 1
IF_STAGE_NAME = 2
IF_STAGE_INFO = 3
IF_DRYING = 4

# Logs
LOG_DATA = 1
LOG_EVENTS = 2
LOG_JOURNAL = 3
LOG_SYSTEM = 4
LOG_FEED = 5
LOG_DISPATCH = 6
LOG_ACCESS = 7
LOG_SOIL = 8
LOG_MAX_MIN = 9

# Manual Feed Actions
MFA_NONE = 0
MFA_READ = 1
MFA_FILL = 2
MFA_NUT = 10    # Plus nutrient id
MFA_MIX = 7
MFA_FEED_1 = 3
MFA_FEED_2 = 4
MFA_FLUSH_1 = 5
MFA_FLUSH_2 = 6

# Max Min Types - Reset option
MMT_CLOCK = 1       # By clock ie midnight and midday
MMT_PROCESS = 2     # By process ie light switch

# Msg Codes
MSG_1 = 1
MSG_DATA_LINK = 2   # Master/Slave Data link lost
MSG_DATABASE = 3    # Master db unavailable using localhost
MSG_DATABASE_DEBUG = 4    # Using localhost debug db
MSG_DATABASE_BACKUP = 5     # Db has been backed up
MSG_FAN_START = 6
MSG_UPCOMING = 7   # Upcoming start
MSG_FLOAT = 11   # Tank 1
MSG_FLOAT_2 = 12   # Tank 2
MSG_FLOAT_HEATER = 13   # Tank 1 float down when heater is required
MSG_FLOAT_HEATER_2 = 14
MSG_FLOAT_FEEDING = 15  # Tank 1 float down during feed time
MSG_FLOAT_FEEDING_2 = 16
MSG_FEED_DATE = 18  #
MSG_IO_BOOT = 30
MSG_FU_BOOT = 40
MSG_LOGGING = 50

# To locations - For the client so correct ip address can be connected to, to send
MODULE_IO = 0
MODULE_DE = 1
MODULE_FU = 2
MODULE_SL = 10  # The slave PC. Although not a module as such, named so to keep location names similar
MODULE_NWC = 100    # For testing NWC, send it to it's self so you can test how other PC will handle it

# Network commands - These are only Master to slave to master
NWC_ACCESS_OPERATE = "access_operate"       # The Access operate button press forwarded to other pc
NWC_ACCESS_BOOST = "access_boost"           # Access auto boost changed
NWC_CHANGE_TO_FLUSHING = "move_flushing"      # Plant has changed to flushing
NWC_DRYING_AREA = "drying_area"             # Reload drying area settings
NWC_FAN_SENSOR = "fan sensor"               # Fan sensor has changed, fan num, new sensor id
NWC_FAN_SPEED = "fan speed"                 # Fan speed has been changed Manually, fan num, speed
NWC_FAN_MODE = "fan mode"                   # Fan mode has changed, fan num, mode
NWC_FAN_PID = "fan pid"                     # Fan PID values has changed, fan num
NWC_FAN_REQUIRED = "fan required"           # Fan required temperature has changed, fan num, value
NWC_FAN_UPDATE = "fan update"               # Update slaves fan speeds, fan 1 speed, fan 2 speed  100, 100 for speed is a request
NWC_FEEDER_UPDATE = "feeder_update"         # A communication was received from the FU
NWC_FEEDER_CONFIG = "feeder_config"         # Feeder reload configs,
NWC_FINISH_ITEM = "finish item"             # An item has finished (drying), item num
NWC_MESSAGE = "message"                     # Refresh msg sys
NWC_MODULES_STATUS = "modules_status"       # I/O D/E modules on/off line
NWC_MOVE_TO_FINISHING = "move_finishing"    # Plant has moved to finishing
NWC_NUTRIENTS_AUTO_STIR = "nutrients auto"  # The nutrient auto stir time has changed
NWC_OUTPUT = "output"                       # An output has operated, which output, state
NWC_OUTPUT_MODE = "output mode"             # An output mode has changed, send output id, mode
NWC_OUTPUT_SENSOR = "output sensor"         # An output sensor has changed, send area
NWC_OUTPUT_RANGE = "output range"           # An output range has changed, send output id
NWC_OUTPUT_TRIGGER = "output trigger"       # An output trigger (rise/fall etc) has changed
NWC_OUTPUT_LOCK = "output lock"             # An output lock has changed
NWC_PROCESS_FEED_MODE = "feed mode"         # A feed mode has been changed, send location
NWC_PROCESS_MIX_CHANGE = "mix change"       # A feed mix has been changed, send location
NWC_QUE_STATUS = "que_status"               # The que status
NWC_RELOAD_PROCESSES = "process reload"     # A change has been made in other unit the requires the processes to be reloaded
NWC_SENSOR_RELOAD = "sensor reload"         # A sensor temperature setting has been changed, send location, sensor id
NWC_SLAVE_START = "slave start"             # Slave has started, send all prams
NWC_STAGE_ADJUST = "stage adjust"           # The number of stage days has been changed, send area
NWC_SOIL_ITEM = "soil sensor item"          # The item has changes for a soil sensor send sensor,
NWC_SOIL_LOAD = "soil_load"                 # Reload soil sensors, send area
NWC_STOCK_TOTAL = "stock total"             # The stock total has changed
NWC_SWITCH = "switch"                       # switch number, on or off
NWC_SWITCH_TIMED = "switch timed"           # A timed switch output. Only available to/from Feeder Unit
NWC_SWITCH_REQUEST = "request switch"       # Request the actual position of the switch, pin number
NWC_WORKSHOP_BOOST = "workshop_boost"       # Workshop heater auto boost setting changed, boost setting
NWC_WORKSHOP_FROST = "workshop frost"       # Workshop heater frost setting changed, frost setting
NWC_WORKSHOP_DURATION = "workshop duration"  # Workshop duration has changed
NWC_WORKSHOP_HEATER = "workshop_heater"     # Reload workshop heater settings
NWC_WORKSHOP_RANGES = "workshop_ranges"     # Reload workshop max, mix and frost values
NWC_WH_DURATION = "water heater duration"   # The water heater duration has changed, heater pin id, new duration in minutes
NWC_WH_FREQUENCY = "water heater frequency"  # The water heater frequency has changed, heater pin id, new freq in days
NWC_WH_FLOAT_USE = "water heater float use"  # The water heater float use has changed, heater pin id, in use
NWC_WATER_REQUIRED = "water required"       # The water requried has been changed
NWC_WATER_LEVELS = "water levels"           # Request water levels from master

NWC_ACCESS_DURATION = "access_duration"     # The Access cover duration relay to other pc
NWC_ACKNOWLEDGE = "acknowledged"
NWC_CONFIG = "config"               # A generic command to get the other unit to reload values from config table (title_c)
NWC_FEED = "feed"                   # Manual feed done (location)
NWC_FEED_DATE = "feed date"                 # A feed has been changed, send location
NWC_FEED_ADJUST = "feed adjust"     # Nutrient changes This covers both nutrient change and litres change, Send location
NWC_FEED_ITEMS = "feed items"            # Mix feed items changed, send area
NWC_FEEDER_POT_TOP_UP = "pot top up"     # Changes are in db so just reload section
NWC_FEEDER_NUT_TOP_UP = "nut top up"     # Changes are in db so just reload section
NWC_FEEDER_STATUS = "feeder status"
NWC_JOURNAL_ADD = "journal write"   # An entry has been writen into journal (location, entry)
NWC_QUANTITY = "quantity"           # A process quantity has changed, send location
NWC_SENSOR_READ = COM_SENSOR_READ
NWC_SOIL_READ = COM_SOIL_READ
NWC_US_READ = COM_US_READ

# Output Types
OUT_TYPE = ("None", "Manual", "Sensor", "Timer", "Both", "All Day", "All Night", "Process")

# Output classes
OP_HEATER_1A = 1
OP_HEATER_1B = 2
OP_AUX_1 = 3
OP_HEATER_2A = 4
OP_HEATER_2B = 5
OP_AUX_2 = 6
OP_HEATER_DRY = 7
OP_HEATER_WS = 8
OP_SPARE_1 = 9
OP_SPARE_2 = 10
OP_W_HEATER_1 = 11
OP_W_HEATER_2 = 12

# Outputs
OUT_LIGHT_1 = 0x00
OUT_LIGHT_2 = 0x01
OUT_HEATER_11 = 0x08
OUT_HEATER_12 = 0x09
OUT_HEATER_21 = 0x07
OUT_HEATER_22 = 0x04
OUT_HEATER_31 = 0x03
OUT_HEATER_ROOM = 0x02
OUT_WATER_HEATER_1 = 0x06
OUT_WATER_HEATER_2 = 0x05
OUT_WATER_SUPPLY_1 = 0xA
OUT_WATER_SUPPLY_2 = 0xB
OUT_DRY_FAN = 0xC
OUT_AUX_1 = 0x1E
OUT_AUX_2 = 0x1F
OUT_SPARE_1 = 0x0F
OUT_SPARE_2 = 0x0E

# FU Unit
OUT_PP_1 = 22
OUT_PP_2 = 23
OUT_PP_3 = 24
OUT_PP_4 = 25
OUT_PP_5 = 26
OUT_PP_6 = 27
OUT_PP_7 = 27
OUT_PP_8 = 29
OUT_NUT_STIR = 31
OUT_MIX_STIR = 30
OUT_MIX_PUMP = 32
OUT_TANK_1 = 33
OUT_TANK_2 = 34
OUT_SERVO_PSU = 35

OUT_FEED_1 = 0x1C
OUT_FEED_2 = 0x1D
OUT_DRAIN_1 = 0x1E
OUT_DRAIN_2 = 0x1F
OUT_FAN_BASE = 0x20     # 32    Fan A 21,22,23,24,25   Fan B 26,24,28,29,2A
OUT_TRANSFORMER = 0x2B
OUT_FEEDER_ACTIVE = 128

# Process Adjustment
PA_STAGE_DAY_ADJUST = "stage duration"
# PA_TEMPERATURE = "stage temperature"
# PA_FEED = "feed litres"
PA_FEED_DATE = "feed date"
# PA_QUANTITY = "quantity"

# Sensor map   Sensor number: Display position
# sensor_map = {0: 0,
#               1: 1,
#               2: 2,
#               3: 3,
#               4: 6,
#               5: 7,
#               6: 11,
#               7: 12,
#               8: 10,
#               9: 4,
#               10: 5,
#               11: 8,
#               12: 9}

# sensor_names = ["H 1", "T 1", "H 2", "T 2", "H 3", "T 3", "H 4", "T 4", "TO 1", "TO 2", "TO 3", "TO 4", "TO 5", "TO 6",
#                 "TO 7", "TO 8"]

# Status bar panels
SBP_MODE = 1
# SBP_COMS = 2
SBP_QUE = 2
SBP_WATER = 3
SBP_FEEDER = 4
SBP_NUTRIENTS = 5
SBP_SERVER = 6
SBP_REMOTE_IO = 7
SBP_BOOT_TIME = 8
SBP_REMOTE_SS = 9
SBP_STOCK = 10

# Sounds
SND_CLICK = [600, 15]
SND_OK = [1300, 30, 1500, 40]
SND_ACTION = [1000, 100, 1000, 100]
SND_OFF = [100, 50]         # , 120, 50
SND_ON = [1120, 50]         # 1000, 50,
SND_ON1 = [1000, 50, 2200, 100]
SND_OFF1 = [2200, 50, 1000, 100]
SND_ATTENTION = [1200, 250, 1500, 350, 1800, 150]
SND_ERROR = [180, 200]
SND_ACCESS_WARN = [900, 200, 800, 200, 900, 200, 800, 200, 900, 200, 800, 200]
SND_CHECK_OUT_ERROR = [2000, 50, 1700, 50, 2000, 50, 1700, 50, 2000, 50]

# Sensors
SR_OUT_H = 1
SR_OUT_T = 2
SR_PREP_H = 3
SR_PREP_T = 4
SR_FINISH_H = 5
SR_FINISH_T = 6
SR_DRY_H = 7
SR_DRY_T = 8
SR_WS_T = 9
SR_PREP_P = 10
SR_PREP_C = 11
SR_FINISH_P = 12
SR_FINISH_C = 13

# Switch pins
SW_LIGHT_1 = 0
SW_LIGHT_2 = 1
SW_WORKSHOP = 2
SW_WATER_HEATER_1 = 6
SW_WATER_HEATER_2 = 5
# SW_WATER_MAINS_1 = 13
# SW_WATER_MAINS_2 = 12
SW_DHT_POWER = 10
SW_DRY_FAN = 11
SW_FANS_POWER = 37

SW_FAN_1_OFF = 22
SW_FAN_2_OFF = 23

# Switch pins Feeder
# SW_PARA_PUMP_BASE = 3   # 17
SW_PARA_PUMP_1 = 22
SW_PARA_PUMP_2 = 23
SW_PARA_PUMP_3 = 24
SW_PARA_PUMP_4 = 25
SW_PARA_PUMP_5 = 26
SW_PARA_PUMP_6 = 27
SW_PARA_PUMP_7 = 28
SW_PARA_PUMP_8 = 29
SW_MIX_STIR = 30
SW_NUTRIENT_STIR = 31
SW_FEED_PUMP = 32
SW_FEEDER_SPARE = 33
SW_WATER_MAINS_1 = 34
SW_WATER_MAINS_2 = 35
SW_MAN_FEED = 38
SW_A1_FEED = 39
SW_A1_DRAIN = 41
SW_A2_FEED = 40
SW_A2_DRAIN = 42

# DE Module
SW_COVER_LOCK = 22
SW_DOOR_LOCK = 23
SW_COVER_CLOSE = 24
SW_COVER_OPEN = 25

# Servo Valves
SV_TANK_1 = 1
SV_TANK_2 = 2
SV_FEED_1 = 3
SV_FEED_2 = 4
SV_DRAIN_1 = 5
SV_DRAIN_2 = 6

# Servo degrees for positions.
VALVE_CLOSED = 90
VALVE_OPEN = 0
# VALVE_POS_A = 0
# VALVE_POS_B = 155


