# from xpinyin import Pinyin
from pypinyin import pinyin, Style
import re

dict0 = {
    'shi': '⠱', 'si': '⠎',
    'chi': '⠟', 'ci': '⠉',
    'zhi': '⠌','zi': '⠵',
    # 'ju': '⠛⠬',
    '，': '⠐','。': '⠐⠆', '?': '⠐⠄', '！': '⠰⠂','；': '⠆⠂', '：': '⠒⠂',
    'wen': '⠒⠆', 'wei': '⠺', 'wan': '⠻', 'wo': '⠕', 'wang': '⠶',
    'yun': '⠸', 'ya': '⠫', 'yuan': '⠯', 'yue': '⠾', 'you': '⠳', 'yi': '⠊', 'yan': '⠩',
}
dict1 = {
    'b': '⠃', 'p': '⠏', 'm': '⠍', 'f': '⠋',
    'd': '⠙', 't': '⠞', 'n': '⠝', 'l': '⠇',
    'g': '⠛', 'k': '⠅', 'h': '⠓', 'j': '⠛',
    'q': '⠅', 'x': '⠓', 'zh': '⠌', 'ch': '⠟',
    'sh': '⠱', 'r': '⠚', 'z': '⠵', 'c': '⠉',
    's': '⠎',
}
dict2 = {
    'iang': '⠭', 'uang': '⠶', 'iong': '⠹',
    'uan': '⠻', 'ian': '⠩', 'ing': '⠡', 'ong': '⠲', 'ang': '⠦',
    'uai': '⠽', 'iao': '⠜', 'uei': '⠺', 'eng': '⠼',
    'van': '⠯', 'ai': '⠪', 'ei': '⠮', 'ao': '⠖',
    'ou': '⠷', 'ia': '⠫', 'ie': '⠑', 'iu': '⠳',
    'ua': '⠿', 'uo': '⠕', 'ue': '⠾', 'an': '⠧',
    'en': '⠝', 'in': '⠣', 'un': '⠒', 'vn': '⠇',
    'a': '⠔', 'o': '⠢', 'e': '⠢', 'i': '⠊', 'u': '⠥', 'v': '⠬'
}
dict3 = {
    '1': '⠁', '2': '⠂', '3': '⠄', '4': '⠆'
}
num_dict = {
    '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉',
    '4': '⠙', '5': '⠑', '6': '⠋', '7': '⠛',
    '8': '⠓', '9': '⠊'
}

def ch_to_py(chtxt):
    ret = [item[0] for item in pinyin(chtxt, style=Style.TONE3)]
    return ret

def sp_py(pytxt):
    initials = ['zh', 'ch', 'sh', 'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'r', 'z', 'c', 's']
    initial = ''
    final = pytxt
    for s in initials:
        if pytxt.startswith(s):
            initial = s
            final = pytxt[len(s):]
            break
    if not initial:
        single_initials = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'r', 'z', 'c', 's']
        if pytxt and pytxt[0] in single_initials:
            initial = pytxt[0]
            final = pytxt[1:]
    if initial in ['j', 'q', 'x'] and final.startswith('u'):
        final = 'v' + final[1:]
    return initial, final

def se_is_ts(txt):
    ret = ''
    for char in txt:
        if re.match('[\u4e00-\u9fff]', char):
            pys = ch_to_py(char)
            for py in pys:
                tone = py[-1] if py[-1].isdigit() else ''
                py_body = py[:-1] if tone else py
                if py_body in dict0:
                    ret += dict0[py_body] + dict3.get(tone, '')
                else:
                    shengmu, yunmu = sp_py(py_body)
                    sm_braille = dict1.get(shengmu, '')
                    ym_braille = dict2.get(yunmu, '')
                    tone_braille = dict3.get(tone, '')
                    ret += sm_braille + ym_braille + tone_braille
        else:
            if char in dict0:
                ret += dict0[char]
            elif char.isdigit():
                braille_num = '⠼' + num_dict.get(char, '')
                ret += braille_num
            else:
                ret += char
    return ret

if __name__ == '__main__':
    print(se_is_ts("窗前明月光"))  # 测试示例输出