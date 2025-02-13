from enum import IntEnum, StrEnum

DOMAIN = 'hitachi'
CONF_REFRESH_TOKEN = 'refresh_token'

class CodeEnum(StrEnum):
    OK = '200'
    INVALID_LOGIN = '202' # 账号密码错误
    MULTIPLE_LOGIN = '203' # 您的账号已在其他地方登录

KEY_CODE = 'xkqCode'
KEY_NAME = 'xkqName'
KEY_HEAT_MAX = 'heatMax'
KEY_HEAT_MIN = 'heatMin'
KEY_COLD_MAX = 'coldMax'
KEY_COLD_MIN = 'coldMin'
KEY_MAC = 'macImei'
KEY_HOME_ID = 'homeId'
KEY_STATE = 'xkq18Onoff'
KEY_TARGET_TEMP = 'xkq19Temp'
KEY_HUMI = 'xkq20Humi'
KEY_MODE = 'xkq21Mode'
KEY_WIND = 'xkq23Wind'
#KEY_ECO = 'xkqSxc24Af'
#KEY_SILENT = 'xkqSxc25Af'
#KEY_DRY_FLOOR = 'xkqSxc28Af'
KEY_LOCK = 'xkq44KeyLock'
KEY_KEY_TONE = 'xkq50KeyTone'
KEY_SCREEN_BRIGHT = 'xkq47ScreenBright'
KEY_LED_BRIGHT = 'xkq45RunLedBright'
#KEY_OUTLET_TEMP = 'xkqSxc56Two'
#KEY_INLET_TEMP = 'xkqSxc57Twi'
KEY_CUR_TEMP = 'xkq70IndoorTemp'
KEY_TS = 'timestamp'
KEY_DEVICE_TYPE = 'deviceType'
KEY_XKQ_TYPE = 'xkqType'
KEY_IEZCODE = 'iezCode'
KEY_SYSTEMNO = 'systemNo'
KEY_IUNO = 'iuNo'
KEY_IUTYPE = 'iuType'
KEY_IUSN = 'iuSn'


class ModeEnum(IntEnum):
    COLD = 0
    HEAT = 1
    FLOOR_HEAT = 2

class SensorEnum(StrEnum):
    target = KEY_TARGET_TEMP
    #outlet = KEY_OUTLET_TEMP
    #inlet = KEY_INLET_TEMP
    current = KEY_CUR_TEMP

class SwitchEnum(StrEnum):
    switch = KEY_STATE
    #eco = KEY_ECO
    #silent = KEY_SILENT
    #dryfloor = KEY_DRY_FLOOR
    lock = KEY_LOCK
    # keytone = KEY_KEY_TONE
    # led = KEY_LED_BRIGHT
