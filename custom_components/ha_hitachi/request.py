import httpx
import time
import logging
import asyncio
from functools import partial
from .const import (
    CodeEnum, KEY_CODE, KEY_DEVICE_TYPE, KEY_XKQ_TYPE, KEY_HOME_ID, 
    KEY_IEZCODE, KEY_SYSTEMNO, KEY_IUNO, KEY_IUTYPE, KEY_IUSN
)
from homeassistant.helpers.httpx_client import get_async_client

_LOGGER = logging.getLogger(__name__)


def _log(s: str) -> object:
    s = str(s)
    for i in s.split("\n"):
        _LOGGER.debug(i)


_jgRegId = '191e35f7e14d78078b4'
_token = ''
_hass = None

_client = None

def set_hass(hass):
    global _hass
    _hass = hass

def _gen_headers():
    return {
        'user-agent': 'Dart/3.3 (dart:io)',
        'accept-encoding': 'gzip',
        'x-his-appid': 'com.hisensehitachi.iez2',
        'x-his-apikey': '1QiLCJhbGciOiJIUzI1NiJ9',
        'x-his-version': '7.3.1.241219_release',
        'authorization': (f'Bearer {_token}').strip(),
        'content-type': 'application/json',
        'x-his-os': 'IOS',
        'x-his-locale': 'zh_CN',
        'x-his-apptag': 'V3',
        'x-his-timestamp': f'{int(time.time()*1000)}',
        'host': '1app.hicloud.hisensehitachi.com',
    }

_domain = 'https://1app.hicloud.hisensehitachi.com/'

async def _post(url, payload):
    get_client = None
    if _hass:
        get_client = partial(get_async_client, _hass)
    else:
        get_client = httpx.AsyncClient
    async with get_client() as client:
        response = await client.post(f'{_domain}{url}', json=payload, headers=_gen_headers())
        return response.json()

async def _get(url):
    async with get_async_client(_hass) as client:
        response = await client.get(f'{_domain}{url}', headers=_gen_headers())
        return response.json()

def set_token(token):
    global _token
    _token = token

async def login(username, password):
    _LOGGER.debug('login')
    return await _post('login', {
        'phoneNo': username,
        'password': password,
        'jgRegId': _jgRegId,
        'version': 0,
    })

async def rt_login(username, refresh_token):
    _LOGGER.debug('rt_login')
    return await _post('rtLogin', {
        'jgRegId': _jgRegId,
        'loginType': '0',
        'phoneNo': username,
        'refreshToken': refresh_token,
        'version': 1
    })

def parse_auth_res(res):
    _LOGGER.debug(res)
    if res['code'] == CodeEnum.OK.value:
        user = res['data']['user']
        token = user['token']
        refresh_token = user['refreshToken']
        set_token(token)
        return token, refresh_token, res
    return None

async def refresh_auth(username, password, token=None, refresh_token=None):
    _LOGGER.debug('refresh_auth')

    if token:
        set_token(token)
    # refresh_token doesn't work
    # if refresh_token:
    #     _LOGGER.debug('refresh_auth call rt login')
    #     par = parse_auth_res(await rt_login(username, refresh_token))
    #     if par is not None:
    #         return par
    par = parse_auth_res(await login(username, password))
    if par is not None:
        return par
    return None

async def req_homes(home_id):
    url = f'api/apphome/homes/{home_id}'
    return await _get(url)

async def req_status(home_id,iezcode, xkq_list, iu_list):
    url = f'api/appstatus/homes/{home_id}/status'
    return await _post(url, {        
        'homeId': int(home_id),
        "noNetTip": null,
        'iuIdList': [
            {
                "iezCode": iezcode,
                "iuIds" : iu_list,
            }
        ],        
        'boxList': [],
        'xkqList': xkq_list,
        'iuIdListGjy': [],
        'xkqListGjy': [],
        'deviceListGjy': [],
    })

async def req_cmd(device_info, cmd_dict):
    url = 'api/appcontrol/cmds/multiIuOuCtrl'
    payload = {
        "regionCode": "000000",
        "positionLng": 0,
        "positionLat": 0,
        "position1": "",
        "position2": "",
        "positionCity": "",
        "ctrlList": [],
        "xkqCtrlList": [
            {
                "ctrlJson": cmd_dict,
                "xkqCode": device_info[KEY_CODE],
                "deviceType": device_info[KEY_DEVICE_TYPE],
                "xkqType": device_info[KEY_XKQ_TYPE],
            }
        ],
        "homeId": device_info[KEY_HOME_ID],
        "ctrlType": "HA420",
    }
    _LOGGER.debug(payload)
    res = await _post(url, payload)
    await asyncio.sleep(3)
    return res

async def req_cmd_iu(device_info, cmd_dict):
    url = 'api/appcontrol/cmds/multiIuOuCtrl'
    payload = {
        "regionCode": "000000",
        "positionLng": 0,
        "positionLat": 0,
        "position1": "",
        "position2": "",
        "positionCity": "",
        "ctrlList": [
             {"iezCode": device_info[KEY_IEZCODE],
              "deviceType": "3",
              "versionModbusProtocol": 11,
              "iuCtrlInfo":[
                  {
                      "systemNo": device_info[KEY_SYSTEMNO],
                       "iuNo": device_info[KEY_IUNO],
                       "iuType": device_info[KEY_IUTYPE],
                       "iuSn": device_info[KEY_IUSN],
                       "ctrlJson": cmd_dict,
                  }
                ],
                "ouCtrlInfo":[]
             }            
        ],
        "xkqCtrlList": [],
        "homeId": device_info[KEY_HOME_ID],
        "ctrlType": "HA420",
    }
    _LOGGER.debug(payload)
    res = await _post(url, payload)
    await asyncio.sleep(3)
    return res
