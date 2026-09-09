# 스텔라 랩 테스트 — 워드프레스에 붙이는 법

## 파일

| 파일 | 페이지 | 제목 | 그림 |
|---|---|---|---|
| `night-snack.block.html` | `/lab/night-snack/` | 편의점 야식 유형 · 5문항 | 없음 (이모지만) |
| `cafe.block.html` | `/lab/cafe/` | 카페에서 나는 · 8문항 | 없음 (이모지만) |
| `grocery.block.html` | `/lab/grocery/` | 장보기 스타일 · 8문항 | 없음 |
| `camping.block.html` | `/lab/camping/` | 캠핑 갔을 때 · 8문항 | 없음 |
| `money.block.html` | `/lab/money/` | 한 달 머니 스타일 · 8문항 | **20장 먼저 올려야 합니다** (`money-images/`) |
| `breakup.block.html` | `/lab/breakup/` | 헤어지고 나서 나는 · 8문항 | 없음 |
| (도쿄) | `/lab/tokyo/` | 도쿄 여행 MBTI · 8문항 | 32장, 이미 올라가 있음 |

## 목록 쪽에 카드 붙이기

`index-cards.block.html` 을 `/lab/` 쪽에 「사용자 정의 HTML」 블록으로
붙이면 일곱 장이 한꺼번에 뜹니다. 도쿄가 맨 위 큰 카드입니다.

★ 목록에 이미 도쿄 카드가 있으면 둘 중 하나만 남기세요.

자바스크립트도 그림도 안 씁니다. 붙여넣기만 하면 바로 보입니다.
390px 와 820px 에서 그려봤습니다 — 가로로 넘치지 않습니다.

## 붙이는 순서

1. 워드프레스 관리자 → 페이지 → 새 페이지
2. 제목을 넣고, **주소(슬러그)를 위 표대로** 맞춥니다
3. 블록 추가 → **「사용자 정의 HTML」**
4. 해당 `.block.html` 파일을 **통째로** 붙여넣기
5. 미리보기로 확인 → 발행

## money 만 다릅니다 — 그림 먼저

`money-images/` 안의 20장을 **미디어 라이브러리에 올린 뒤에** 붙여넣으세요.
파일 이름을 바꾸지 마세요. 코드가 이 이름 그대로 찾습니다.

    https://stellasaju.com/wp-content/uploads/2026/09/money-q1_save.jpg

올린 달이 2026/09 가 아니면 주소가 달라집니다. 그럴 땐 알려주세요 — 한 번에 고쳐드립니다.

## 손본 것

- `<!DOCTYPE>` · `<html>` · `<head>` · `<body>` 를 걷어냈습니다. 페이지 안에는 들어갈 수 없는 것들입니다.
- 글꼴 `<link>` 를 `<style>` 안의 `@import` 로 옮겼습니다. 워드프레스가 `<link>` 는 지웁니다.
- **겉모습 규칙을 전부 `.stq-lab` 안쪽으로 묶었습니다.** 원래 `body{...}` 로 되어 있어서
  그대로 붙이면 테마 전체를 덮어씁니다.
- **두 겹 앰퍼샌드를 없앴습니다.** 파일마다 한 군데씩 있었습니다.
  워드프레스가 이것을 바꿔치기해서 스크립트를 통째로 죽입니다 (페이지 137·160 이 이것 때문에 백지가 됐었습니다).
- 「당신」을 뺐습니다 (카페 하나, 머니 하나).
- money 의 `kitteninthesox.com` 을 `stellasaju.com` 으로 바꿨습니다.
- money 에 「← 스텔라 랩」 링크와 꼬리말을 다른 테스트와 같은 모양으로 넣었습니다.

## 확인한 것

크롬으로 실제로 그려봤습니다 (430px 화면).

- 네 개 모두 자바스크립트 오류 없음
- 네 개 모두 JSON 덩어리 정상
- 테마 머리말·꼬리말이 밀리지 않음, 가로 스크롤 없음
- money 는 첫 문제까지 눌러보고 그림 두 장이 뜨는 것까지 확인

## 아직 안 된 것

- **og 태그** (카톡·페북에 공유할 때 뜨는 그림과 글). 페이지 본문에는 못 넣습니다.
  SEO 플러그인이나 스니펫으로 따로 넣어야 합니다.
- **카카오 공유 SDK** — `<script src="…kakao.min.js">` 를 넣어뒀지만
  카카오 자바스크립트 키가 있어야 실제로 공유가 됩니다.

## 2026-09-09 · 스니펫으로 올리는 법 (랩이 스니펫이라서)

랩은 페이지가 아니라 **스니펫이 주소를 가로채는** 방식이었습니다.
그래서 `.block.html` 을 페이지에 붙이는 게 아니라, 스니펫으로 감싸서 넣습니다.

    snippets/snip_lab_night-snack.WPCODE.txt   -> /lab/night-snack/
    snippets/snip_lab_cafe.WPCODE.txt          -> /lab/cafe/
    snippets/snip_lab_camping.WPCODE.txt       -> /lab/camping/
    snippets/snip_lab_grocery.WPCODE.txt       -> /lab/grocery/
    snippets/snip_lab_money.WPCODE.txt         -> /lab/money/
    snippets/snip_lab_breakup.WPCODE.txt       -> /lab/breakup/
    snippets/snip_lab_tokyo.WPCODE.txt         -> /lab/tokyo/

각각 WPCode → 새 스니펫 → PHP Snippet → 「어디서나 실행」 → 저장 → Active.
스니펫 하나가 검사 하나입니다.

`make_snippets.py` 가 블록 파일을 읽어서 이 스니펫들을 만듭니다.
블록을 고치면 이 스크립트를 다시 돌리면 됩니다.

### 왜 이렇게 하나

랩 본체(804)는 `TESTS` 라는 제 나름의 틀로 검사를 그립니다.
오늘 만든 여섯은 저마다 자기 화면을 가지고 있어서 그 틀에 안 맞습니다.
본체를 안 건드리고 그 주소만 따로 맡는 쪽이 안전합니다.
우선순위 5 로 본체(10)보다 먼저 돌아서 부딪히지 않습니다.

### 확인한 것

    · 여섯 다 php -l 통과, 두 겹 앰퍼샌드 0개
    · 제 주소에서만 열리고 남의 주소에서는 아무것도 안 내놓음
    · /lab/cafe · /lab/cafe/ · /lab/cafe/?r=x 셋 다 열림 (공유 링크용)
    · 브라우저로 여섯 다 시작 -> 선택 -> 다음 문항까지 눌러봄. 오류 없음
    · 390px 에서 가로 넘침 없음

### 아직 남은 것

    · money 는 사진 20장을 미디어에 먼저 올려야 그림이 뜹니다.
    · breakup 은 806 MORE2 의 옛 판(열두 문항)을 가립니다. 끄면 옛 판으로 돌아갑니다.

## 2026-09-09 · 도쿄

`tokyo.block.html` 을 받아서 스니펫으로 만들었습니다. 그림 32장은 이미 올라가 있습니다.

★ 고친 곳 하나 — introSub 의 「당신의 선택이」를
  「도쿄 3박 4일, 여덟 번만 고르면 내 여행 유형이 나와요」로 바꿨습니다.
  글에서 「당신」을 쓰지 않기로 한 규칙입니다.
