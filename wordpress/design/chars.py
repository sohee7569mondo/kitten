# -*- coding: utf-8 -*-
"""보내주신 캐릭터 그림체로 SVG 대역을 그립니다.
   굵은 갈색 외곽선 · 파스텔 채움 · 볼터치 · 점 눈."""

LINE = '#5A4038'

def _wrap(body):
    return ('<svg viewBox="0 0 120 120" width="100%" height="100%" '
            'style="display:block">' + body + '</svg>')

def bunny(body_fill='#FFFFFF', ear_fill='#F7C6D3', belly='#FBF0DC', closed=False):
    eyes = (f'<path d="M44 60q6 6 12 0" fill="none" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M64 60q6 6 12 0" fill="none" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>'
            if closed else
            f'<circle cx="50" cy="61" r="3.6" fill="{LINE}"/><circle cx="70" cy="61" r="3.6" fill="{LINE}"/>')
    return _wrap(
        f'<g stroke="{LINE}" stroke-width="4.5" stroke-linejoin="round">'
        f'<ellipse cx="45" cy="31" rx="9" ry="25" fill="{body_fill}" transform="rotate(-9 45 31)"/>'
        f'<ellipse cx="75" cy="31" rx="9" ry="25" fill="{body_fill}" transform="rotate(9 75 31)"/>'
        f'<ellipse cx="60" cy="88" rx="31" ry="26" fill="{body_fill}"/>'
        f'<circle cx="60" cy="63" r="27" fill="{body_fill}"/>'
        f'</g>'
        f'<ellipse cx="45" cy="30" rx="4" ry="15" fill="{ear_fill}" transform="rotate(-9 45 30)"/>'
        f'<ellipse cx="75" cy="30" rx="4" ry="15" fill="{ear_fill}" transform="rotate(9 75 30)"/>'
        f'<ellipse cx="60" cy="95" rx="14" ry="12" fill="{belly}"/>'
        f'{eyes}'
        f'<ellipse cx="40" cy="70" rx="6.5" ry="4.5" fill="#F7A8BC"/>'
        f'<ellipse cx="80" cy="70" rx="6.5" ry="4.5" fill="#F7A8BC"/>'
        f'<ellipse cx="60" cy="69" rx="4" ry="3" fill="#EE8FA8"/>')

def cat(body_fill='#F5DFAF', patch='#B98A5A'):
    return _wrap(
        f'<g stroke="{LINE}" stroke-width="4.5" stroke-linejoin="round">'
        f'<path d="M38 46 L34 22 L56 34 Z" fill="{body_fill}"/>'
        f'<path d="M82 46 L86 22 L64 34 Z" fill="{body_fill}"/>'
        f'<path d="M92 96q10 4 8 12" fill="none" stroke-linecap="round"/>'
        f'<ellipse cx="60" cy="88" rx="30" ry="25" fill="{body_fill}"/>'
        f'<circle cx="60" cy="58" r="28" fill="{body_fill}"/>'
        f'</g>'
        f'<path d="M76 34a13 13 0 0 1 11 12a28 28 0 0 0-13-9z" fill="{patch}"/>'
        f'<ellipse cx="60" cy="94" rx="14" ry="12" fill="#FBF0DC"/>'
        f'<circle cx="50" cy="56" r="3.6" fill="{LINE}"/><circle cx="70" cy="56" r="3.6" fill="{LINE}"/>'
        f'<ellipse cx="40" cy="66" rx="6.5" ry="4.5" fill="#F7A8BC"/>'
        f'<ellipse cx="80" cy="66" rx="6.5" ry="4.5" fill="#F7A8BC"/>'
        f'<ellipse cx="60" cy="65" rx="3.5" ry="2.6" fill="{LINE}"/>'
        f'<g stroke="{LINE}" stroke-width="2.4" stroke-linecap="round">'
        f'<path d="M30 62h-9M30 68l-9 3M90 62h9M90 68l9 3"/></g>')

def cow():
    return _wrap(
        f'<g stroke="{LINE}" stroke-width="4.5" stroke-linejoin="round">'
        f'<path d="M40 32q-7-11 1-15q7-3 8 9z" fill="#D9C9A8"/>'
        f'<path d="M80 32q7-11-1-15q-7-3-8 9z" fill="#D9C9A8"/>'
        f'<ellipse cx="33" cy="50" rx="11" ry="8" fill="#8E8E96" transform="rotate(-14 33 50)"/>'
        f'<ellipse cx="87" cy="50" rx="11" ry="8" fill="#FFFFFF" transform="rotate(14 87 50)"/>'
        f'<ellipse cx="60" cy="92" rx="29" ry="23" fill="#FFFFFF"/>'
        f'<circle cx="60" cy="56" r="27" fill="#FFFFFF"/>'
        f'</g>'
        f'<path d="M41 38a28 28 0 0 1 14-7a16 16 0 0 0-9 13z" fill="#8E8E96"/>'
        f'<ellipse cx="60" cy="97" rx="13" ry="10" fill="#F1F1F3"/>'
        f'<circle cx="49" cy="53" r="3.6" fill="{LINE}"/>'
        f'<path d="M65 53q6 5 12 0" fill="none" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>'
        f'<ellipse cx="60" cy="66" rx="13" ry="9" fill="#F5B8C6" stroke="{LINE}" stroke-width="3"/>'
        f'<ellipse cx="55" cy="64" rx="1.8" ry="2.6" fill="{LINE}"/>'
        f'<ellipse cx="65" cy="64" rx="1.8" ry="2.6" fill="{LINE}"/>'
        f'<ellipse cx="36" cy="64" rx="6.5" ry="4.5" fill="#F7A8BC"/>'
        f'<ellipse cx="84" cy="64" rx="6.5" ry="4.5" fill="#F7A8BC"/>'
        f'<path d="M46 82q14 7 28 0" fill="none" stroke="#D9566E" stroke-width="5" stroke-linecap="round"/>'
        f'<circle cx="60" cy="88" r="5.5" fill="#E8B23C" stroke="{LINE}" stroke-width="3"/>')

def peek_bunny():
    """카드 모서리를 붙잡고 빼꼼 — 보내주신 두 번째 그림의 자세"""
    return _wrap(
        f'<g stroke="{LINE}" stroke-width="4.5" stroke-linejoin="round">'
        f'<ellipse cx="44" cy="30" rx="8.5" ry="23" fill="#FFFFFF" transform="rotate(-12 44 30)"/>'
        f'<ellipse cx="72" cy="28" rx="8.5" ry="23" fill="#FFFFFF" transform="rotate(9 72 28)"/>'
        f'<circle cx="58" cy="62" r="27" fill="#FFFFFF"/>'
        f'<ellipse cx="34" cy="88" rx="9" ry="7" fill="#FFFFFF"/>'
        f'<ellipse cx="82" cy="88" rx="9" ry="7" fill="#FFFFFF"/>'
        f'</g>'
        f'<ellipse cx="44" cy="29" rx="3.8" ry="14" fill="#F7C6D3" transform="rotate(-12 44 29)"/>'
        f'<ellipse cx="72" cy="27" rx="3.8" ry="14" fill="#F7C6D3" transform="rotate(9 72 27)"/>'
        f'<circle cx="49" cy="61" r="3.6" fill="{LINE}"/><circle cx="68" cy="61" r="3.6" fill="{LINE}"/>'
        f'<ellipse cx="39" cy="70" rx="6.5" ry="4.5" fill="#F7A8BC"/>'
        f'<ellipse cx="78" cy="70" rx="6.5" ry="4.5" fill="#F7A8BC"/>'
        f'<ellipse cx="58" cy="69" rx="4" ry="3" fill="#EE8FA8"/>')

CHARS = {
    'bunny_white': bunny(),
    'bunny_happy': bunny(closed=True),
    'bunny_pink':  bunny('#F7C6D3', '#EDA0B6', '#FBF0DC'),
    'cat_cream':   cat(),
    'cow':         cow(),
    'bunny_peek':  peek_bunny(),
}

if __name__ == '__main__':
    import io, sys
    for k, v in CHARS.items():
        print(k, len(v), 'bytes' if '&' not in v else 'AMPERSAND!')
