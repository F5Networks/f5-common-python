#!/usr/bin/python

import subprocess
import time
import argparse

SCAN_CODES = {
    '1': '02', '2': '03', '3': '04', '4': '05', '5': '06', '6': '07', '7': '08',
    '8': '09', '9': '0A', '0': '0B', '-': '0C', '=': '0D', '<bs>': '0E',
    '<tab>': '0F', 'q': '10', 'w': '11', 'e': '12', 'r': '13', 't': '14',
    'y': '15', 'u': '16', 'i': '17', 'o': '18', 'p': '19', '[': '1A',
    ']': '1B', '<enter>': '1C', '<ctrl>': '1D', 'a': '1E', 's': '1F',
    'd': '20', 'f': '21', 'g': '22', 'h': '23', 'j': '24', 'k': '25',
    'l': '26', ';': '27', '<shift>': '2A', 'z': '2C', 'x': '2D', 'c': '2E',
    'v': '2F', 'b': '30', 'n': '31', 'm': '32', ',': '33', '.': '34', '/': '35',
    ' ': '39'
}

def command(cmd):
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
    if stderr or 'pause' in stdout or 'savestate' in stdout:
        raise Exception(stderr)

def keyboardputscancode(vmname, codes):
    codes = reduce(lambda x,y: x + y, codes, [])
    cmd = [
        'vboxmanage',
        'controlvm',
        vmname,
        'keyboardputscancode'
    ]
    cmd += codes
    command(cmd)

def getBreakCode(key):
    if key not in SCAN_CODES:
        raise Exception('Undefined key: ' + key)
    makeCode = SCAN_CODES[key]
    a = int(makeCode, 16)
    b = int('80', 16)
    c = a + b
    d = format(c, 'x')
    return d

def toScanCode(s):
    result = []
    tmp = ''
    special = False

    for c in s:
        if c == '<':
            tmp = tmp + c
            special = True
            continue
        elif c == '>':
            tmp = tmp + c
            special = False
            c = tmp
            tmp = ''
        elif special:
            tmp = tmp + c
            continue

        if c == c.upper() and not c.isdigit() and c is not ' ':
            stopCodeShift = getBreakCode('<shift>')
            stopCodeInput = getBreakCode(c)
            result.append([
                SCAN_CODES['<shift>'],
                SCAN_CODES[c],
                stopCodeInput,
                stopCodeShift
            ])
        else:
            stopCode = getBreakCode(c)
            result.append([
                SCAN_CODES[c],
                stopCode
            ])
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Re-kicks dhclient after restoring snapshot'
    )
    parser.add_argument('--vmname',
                        help='The name of the virtual machine in Virtualbox',
                        required=True)
    args = parser.parse_args()

    codes = [
        'root<enter>',
        'default<enter>',
        'killall dhclient<enter>',
        'dhclient eth0<enter>',
        'exit<enter>'
    ]

    for code in codes:
        sc = toScanCode(code)
        keyboardputscancode(args.vmname, sc)
        time.sleep(.5)