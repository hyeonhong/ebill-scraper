#!/usr/bin/env python
# -*- coding: utf-8 -*-
import log
import sys
from datetime import datetime, timedelta
import json
import requests
from win32com import client
from crypto import *
import pythoncom
from flask import abort

logger = log.init_logger(__name__)


def scraper(config_dict):

    fill_values(config_dict)

    '''
    ####################### 'crypto' package usage  #######################
    
    from crypto import *
    
    # to generate key
    key = generate_key()  # same key should be used for encryption & decryption

    # encryption
    plaintext = 'secret texts'
    encrypted_binary = encrypt(plaintext, key)
    encrypted_text = encrypted_binary.decode('latin-1')

    # decryption
    encrypted_binary = encrypted_text.encode('latin-1')
    decrypted = decrypt(encrypted_binary, key)
    print(decrypted.decode('utf-8'))
    
    #######################################################################
    '''

    note_type = config_dict["svcCd"]

    # Serialize JSON object to string
    config_string = json.dumps(config_dict, ensure_ascii=False)

    logger.info('Start scraping for the note {}'.format(note_type))
    logger.info('Sending request to the scrapping module <COM object>')

    response = None

    try:
        pythoncom.CoInitialize()
        com_object = client.Dispatch('iftWinExAdapter.clsAdapter')
        response = com_object.serviceCall2(config_string)
    except Exception as e:
        # print(e)
        logger.exception('Error: A connection with the <COM object> module could not be established')
        return abort(422, 'Error: A connection with the <COM object> module could not be established')

    try:
        result = json.loads(response[0])  # Convert string to JSON object

        if result["errYn"] == 'N':
            logger.info('Scraping operation for note {} is successful'.format(note_type))
        else:
            logger.error('Error: Error: <COM object> module returned the error message')
            return abort(422, 'Error: <COM object> module returned the error message')
    except Exception as e:
        # print(e)
        logger.error('Error: Failed to receive the response from the <COM object> module')
        return abort(422, 'Error: Failed to receive the response from the <COM object> module')

    logger.info('Here is the result for scraping the note {}'.format(note_type))
    logger.info(response[0])

    data = {"sSvcCode": "BILL", "sData": result}

    # Send HTTP POST to the given url
    # if not send_post('http://httpbin.org/post', data):
    #     return {"error": 400}

    return data


def fill_values(config_dict):

    # Retrieve the default values from 'default.json'
    with open('default.json', 'r', encoding='utf-8') as read_file:
        read_string = read_file.read()
    read_string = read_string.replace("\\", "\\\\")
    file_dict = json.loads(read_string)

    # Check if the received JSON form is in the correct form
    default = file_dict.keys()
    user_input = config_dict.keys()
    if len(default) != len(user_input) or set(default) != set(user_input):
        return abort(422, 'User sent the wrong JSON format')

    # temporary storage for user input
    _svcCd = None
    _billNo = None
    _detail = None
    _fromDate = None
    _toDate = None

    # Check the validity of note value
    note_list = {
        'B0001',  # 발행어음     미지급제시
        'B0011',  # 발행어음     결제어음
        'B0021',  # 발행어음     도어음
        'B1001',  # 배서어음     배서한어음
        'B1011',  # 배서어음     배서받은어음
        'B2001',  # 보유어음     결제받을어음
        'B2011',  # 보유어음     결제받은어음
        'B2021',  # 보유어음     부도어음
        'B3001',  # 보증어음     발행보증어음
        'B3011',  # 보증어음     배서보증어음
        'B4001',  # 반환어음     반환어음
        'B5001',  # 수령거부어음 수령거부어음
        'B6001',  # 부도반환어음 부도반환어음
        'B0101'   # 확인서       부도확인서
    }

    if config_dict["svcCd"] not in note_list:
        return abort(422, "Invalid value is passed in the 'svcCD' property")
    else:
        _svcCd = config_dict["svcCd"]  # save the value for later

    # 어음만기가 1년이므로 최대 1년 유효한 어음만 조회
    # 부도가 결정(만기+2영업일)되는 (연휴 등의 사유:최대 7일) 일자를 고려해서 15일을 더 추가하여 조회
    # last_effective_day = 1 year + 15 days

    # Set the default value for date
    if config_dict["fromDate"] == '' and config_dict["toDate"] == '':
        today = datetime.today()
        last_effective_day = today - timedelta(days=380)  # 380 days
        _fromDate = last_effective_day.strftime('%Y%m%d')
        _toDate = today.strftime('%Y%m%d')
    elif config_dict["fromDate"] == '' or config_dict["toDate"] == '':
        return abort(422, "Invalid value is passed in the 'fromDate' or 'toDate' property")
    else:
        try:
            _fromDate = datetime.strptime(config_dict["fromDate"], '%Y%m%d')
            _toDate = datetime.strptime(config_dict["toDate"], '%Y%m%d')
        except ValueError:
            logger.error("Error: Date value is not in the correct format")
            return abort(422, "Invalid format is passed in the 'fromDate' or 'toDate' property")

        if _fromDate > _toDate:
            return abort(422, "Invalid value: fromDate should be earlier than toDate")

        _fromDate = _fromDate.strftime('%Y%m%d')
        _toDate = _toDate.strftime('%Y%m%d')

    # Save the user input
    _billNo = config_dict["billNo"]
    _detail = config_dict["detail"]

    # Set the default values
    config_dict.update(file_dict)

    # Replace the default values with the user input
    config_dict["svcCd"] = _svcCd
    config_dict["billNo"] = _billNo
    config_dict["detail"] = _detail
    config_dict["fromDate"] = _fromDate
    config_dict["toDate"] = _toDate
    config_dict["signPw"] = decrypt_pw(config_dict["signPw"])


def decrypt_pw(encrypted_text):
    key = b'\x1df\xad\xfc\x95\x0f\x12B\xa7\xa3m\x14x\x86\x08\xa3'
    encrypted_binary = encrypted_text.encode('latin-1')
    decrypted_binary = decrypt(encrypted_binary, key)
    decrypted_text = decrypted_binary.decode('utf-8')
    return decrypted_text


# unused method
def send_post(url, payload):
    headers = {'Content-type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), headers=headers)
    except requests.RequestException as e:
        logger.info('Error has occurred: {}'.format(e))
        return False
    try:
        r.raise_for_status()  # Throw exception if the status_code is not 200
    except Exception as e:
        logger.error(e)
        return False
    logger.info('Here is the scraping result from the url {}'.format(url))
    logger.info("Successfully sent HTTP POST")
    logger.info(r.text)
    return True
