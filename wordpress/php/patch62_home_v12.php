<?php
/**
 * STELLA SAJU — 홈(페이지 62) 새 판 v12
 *
 *  바꾸는 것
 *    1. 첫 화면 문구를 새로 주신 것으로.
 *    2. 오늘의 운세 띠를 첫 화면 바로 다음에 놓았습니다 — 매일 오실 자리.
 *    3. 심심풀이에서 「운명의 책」을 뺐습니다 (일곱 칸이 어색해서). 여섯 칸입니다.
 *    4. 모바일에서 카드가 세로로 쌓이던 것을 옆으로 미는 슬라이드로
 *       (심심풀이 · 여섯 문 · 운명의 비율). 점으로 몇 번째인지 표시합니다.
 *    4. 「정답 말고 가벼운 질문」의 긴 설명을 걷어내고 한 장씩 넘기는 띠로.
 *    5. 스타운세는 매주 한 사람 이름이 바뀌고, 누르면 그 사람 사주로 갑니다.
 *       (이 기능이 돌려면 페이지 406 스니펫도 같이 돌리셔야 합니다)
 *    6. 색을 한 단계 밝게 — 카드 바탕, 배경 성운, 글자.
 *    7. 문 카드 오른쪽 위의 4,900원 배지를 뗐습니다. 값이 주제마다
 *       매겨지게 바뀌어 문 하나에 값 하나를 적으면 틀린 말이 됩니다.
 *    8. 위아래 여백을 줄여 모바일 스크롤을 줄였습니다.
 *
 *  내용은 base64 로 담았습니다. 워드프레스 편집기가 줄바꿈이나 따옴표를
 *  건드려도 글이 상하지 않습니다. 넣기 전에 sha1 로 맞는지 확인합니다.
 *
 *  쓰는 법 (WPCode Lite) — PHP · 자동 실행 안 함
 *    확인 : https://stellasaju.com/?stella_patch=dry
 *    적용 : https://stellasaju.com/?stella_patch=go
 *    되돌리기 : https://stellasaju.com/?stella_patch=undo
 *    다 되면 스니펫을 지우세요.
 */

add_action( 'init', function () {

	if ( ! isset( $_GET['stella_patch'] ) ) { return; }
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	$mode = sanitize_text_field( wp_unslash( $_GET['stella_patch'] ) );

	global $wpdb;
	$post_id = 62;
	$bak_key = 'stella_bak_62_v12';
	$expect_hash = 'fd9e09327d332c8d1c6017eb9ba8990c077bb0ea';
	$expect_len  = 45267;
	$expect_b64  = 16372;

	$b64 =
		'H4sIANoWlWoC/919a3MTV7bod37FHlPEViLJUuvhF3gOrzzuIcktIHdmau7UrbbUthsktUYtYxwf' .
		'qgwIxhM7EzOxQRCbiIkJkOtTEcYQc8o5t+r+lEydqVvu1n+4a+1H9+6HZBmcM8zJACO19l577bXW' .
		'Xq+99u6jv4jFyHR5eLJaLJBYbPTQUXhwiJBz50+fOXOcnDv+3z4hP80tk9bdedLXHyGEnPjkgzOn' .
		'hsmlpAJflISSjSUGY6nkIej00/LiT8tz//h/luhcrhFibWzvPt+wHu6Q3WcN+2Ud/iX2wgt7dcde' .
		'WCfWyiLp8j+AJmC+5n8SJPurRevL1dZyzWrM25+tk92tOevbDfv+Evnp5p9J6091e23LfjRHv00a' .
		'RY0/3rYf3aIf9wK/UrPu18lf5xbtaxv2vScI2G6s2Gt18v75D8/8de5zYm0vWw/W7LUase9sIXF2' .
		't+egmfVokRPMXli1nmwRa+mJtTBvLazHvUOYuYperhLrixrZ/WHbWpyzHqzCGADjobVUtz5bJrub' .
		'1xF86y6Mu926DfN87kL6T6HybvMqyoG18Bgoct++swQUWWKC8de5W6R1axUnCSJiLWwgyW4t2Xdk' .
		'NGFixF6vIU3gL/DDrm3b95bjnkGOjlVGCc4XWzaXd//PvH3/hoBg1b5B2lovdzg5XVq17i7DA0TK' .
		'atbt+lUPoT0jtK6vQre+owTGgY67zSV7YQfJG6HDAlr3migs1qN5B8G9qLP8X2K111F1uYqMMGou' .
		'7/47JQ/ps28uttY2gL31yCGcfTJO7M3/zUkvqQj7+jwV32+ATQ0quKs7+IDy87ErERSIAmz97jH8' .
		'ZK/twIB2DTq+3ILlvNucI8AA6EjZtL29u7lI7MUvYS1bn9fFerDrNwX077eBgYc4Z+zPNiwAuIaQ' .
		'+lAtrO1EQnCgKt0GeV3YaP15DpqT//sDzHvDrn2PE6Lf7m1Z393AxW69rNmrjxnaqTjVB40Va+E5' .
		'iMoSXfPNOWtzB9qDFM1Db1AM2G13Gx7U1ikQWN5Pf7Bvb1nXUEsIZFsrMOn7D+3lJyDi9d3Nx9az' .
		'LRRGaw2Evdm0avNtyZcGHny23roOUruF1MJej9aB9AzotQ3r/iIigZT4toYTBDAWYH4bPl2DlbIO' .
		'eEQFItZ8zXq4xVeW3Bv03jeCh2zV3JKxyDAsrm5YD9YpV9Zrdn1OWvsOi4EaTXsdOLta42oVqG01' .
		'n9JejXlYvEjG3ZeLiCoDIxHKrr20b9RhZSLr7PvzKAiMtFwzUTCPHqGoQBPryw2PCkL5RqmEGQ0L' .
		'lWuvzAuxW2m2Pt+xr6MtIaC9ABF4eKdpX2uiKkfB/tKnGQ45msBngqjw3lluLTThj8O8ZUGlb39s' .
		'fQb0bdTszS3a9JsffXxl7HgxZ335tFXfJtaf1/lqpCtrZbG1uGhtPqNEqq8jUvbKZ3TWazX7q4YE' .
		'jLoyZnWmoI2iaxMdM/Izs8YlrTJeMKZjl4cn9XxeK/1CL5aNSlUtVUdIUb0cm9bz1cnhZCJxaVr6' .
		'6QqZ1NS8VolPl2NjBSN3MVbViuWCWtViZbVSnS0bpl7VjdJwRYOH+iVNBvtpTC/ltcvDQ/Cf/HxM' .
		'zV2cqBhTpfzwYRjwhKJ4RjxsVrVCQa3E0HB3RPzK0X42Tz5foueP9ci9YznT7Bk9hGSYBe4bhUJs' .
		'TJtUL+lGZdgsGkZ1cuTKIUqfIE78l3hZndBiej6WVUhcK1UrM7GcUarCp2jwd4dKQJeqaDdbVCsT' .
		'eon/YlaBbsMJIhOkrObzemnC+/TKoUNeSoCUuIwqGSXNA4M9VqeqhvyY9qGjF7Tx6nBOLeT6Mokj' .
		'JEYywOhIeNOKPjG5Z9tQnPG5XyJcOUiMEImbuYJexg4S5asVtWSCXGkICn7qf1s2TqiZnfWDGnID' .
		'lgIo1lsPUDe0Vur2jWVc1agGQTHsPquherXrG1Zj27/WrOY6dLA+Az9xTvIpQAdQP5eaI+q24OK6' .
		'KlkOWI+t6yt0FeLQS/a9bXu+Dp6ga8P4CLdBkz/bQi28MI/aDd0K1PJrO9Rjaq7h0NRi7VhrPxL7' .
		'ux+ZWYuCwpy3Xn6FnqH9oAlfwN7WAVtY7HHydj+Aj8UuGborqPx7LK9p5eHDieOJgeTgCG1W0sam' .
		'CurwYSWTPJkeHHGexEwDpOFwKqlkM6dZ05xayQ8X9JIG4jZRUfM6MKEvmRnMaxPRw8ppJZUZJIkj' .
		'8FFJHk8rBIY+EnF7xib1tp1TJ5RTAwnW+YSSyKTlzgUdENFLplYlCZIsX4Z/KxNjap+SyUTF33hi' .
		'IBLFnxPwewr/iSUH4V/aMBHF/8UHMhxgeapSLmjDhweOZ06eTIw4T2ITIHbDtEsym4omlXRUSWej' .
		'8bTiYFJQc8OHTwwdV95V2KMJowBUPp04cXLg5Aj/zkl3Sjl+eiDtPCzoVRjz3cSpoeOc9LjO4Un2' .
		'3eTpAWymly6yrmx6MLSSTkaVVDIaHwQUeIu8XgxpkHVQLGn856QSTQ5koskETCGViNDlkjMKoNcu' .
		'qZU+NjztNQ5KKDauFvXCzHDvRwaoh3OwyMg/n+2NxtQyEsacATVTjPYex2/k3CnyHuhFPUc+0oze' .
		'aO+HamFiqsSf9UZN6BwztYo+7gCf1qi+SCWA2ohhbJI9SAJTRlgTU/9UG05my5ex07QB8jJW0dSL' .
		'wxdBYmNqoSAphumKWh6mv8aw4cghvx4kb3OFivrE0UJgVYzLOA5+G4OOWiUGT0CLejtPJqO+B4r/' .
		'QWo2nGw4aUo3Nv0QcnvoMUDpoVWrgAkotRwiVjIqRbUQQEqdZbD00iSABmVe1S5XYTnnjIpKdSlq' .
		'+0AvvTgxm9dNsMYzw9S2+Az5kRHCOYFWIdB9eNjUCloO4cvWj80HhTrinSKqmEgASpxjMOsh2Em9' .
		'9KlWEJQK9CkaJcPb4YMTH5L/XtAukw/hp94oNkCaBScdR/mYleaZVEAhjBAhEoTOVbJOCmgKtKVg' .
		'Szo5rCwsoM5mwFMlfa4ViqAG9qFkTsKKYIQU4w4qqMpGOlnDJGD1T0Utr6t97nRAaMqXI7Nk7xHS' .
		'WTrCFRJGH2n6SJ0rJLCI4iix5qxssMf1y1p+hFBljAtKMttlQy+hHGuXQLGbTBy9ppsaPaRx7SmG' .
		'Q0jN3c05auKYxQRf1r7+R0r52y8xFuHxO8Ynn4OD+281+NNa2eJGEz3b1gqP6JnVIwQti1pwLUxW' .
		'uTRN0oPwj1oF63CEpI9ECTMLSUWJDoGOhL+oH6NE8i1IVjkSiYZCzKQRosIgDilHiJIFkEzlgsVI' .
		'Dg5SyxFPpvwgE21BIn7pLAOZzh4hA4oAOZRldgiVuKJ0jSQFluLTHgQkhxwkPaYtOdg1ksl4BsSJ' .
		'/ctpqSScmcu2eMgLsx08hMZgDQKsZDisge5geXGDSZBsJhTe4H5xSwGswXDcsq+C2xDAy7zWXF3c' .
		'0pkjiF8YrMyr4JYEeJnM68zVxW0A6ZbZB26yCQla9PgFM2aUSLwC+kUtzBpoLaszqHgopHGwmiw2' .
		'wMDzN+AbgY7kvzHVxXuQ+JBJNNXUom5H51nQlHhGjeslZ+Bkm4ETEW5JflpZgj9yLow9eRP+hBgo' .
		'8CoMGj5CcCecMwj0J0d8T0x81NFkARDhcoyDuR4hakGfKMXA+y2a9ElMK4ENuTBlVvVxJ1Iezmlo' .
		'PrC38PN4MA/mxjQKzMlhn0L4hOjHxvWJqYrmMVjqGPSYgh6kapSHqbcF/nVGcnwGBo/IkfGIL4BG' .
		'hEIY/eu+WAYDFGneRIhGPE1d8Wlt7KJejRVV82JML6oTWiD6AY9xzKhWjaJXBeOCHoNA4yJJpp2P' .
		'1CLIrUChR6KHQhPQIePQeL3tMIrzcXDQN4wbh8nzyRlFSmJt2DSmKjkNiDAi4fJfZc6e+bhzpo4O' .
		'OlvYRi3BRKmsgQfGJPBdNa+BUh1kSgU+KSb1g6YhCjbRpbuozYxX1KJmEk+fWTJeMYqSbrsCUjsr' .
		'iRU6aSGCPzysjgNGszS+Y6upt3ckbBEEHLdkN46bX8vD+HoZJgZaPkMtd8L1LaLJZDQF3s9QOkJC' .
		'HqezEXRwvPQeCLLVP+RAAj0k0EfOoIPh/ozPTqEZirRRF5iRqqh6FekmIgWMBIRm4N88YQM4e/iM' .
		'R4+I3ZTJ1IlfayEJaath9POBAXqeuIETjfMjPCKdVPPQL0ESMDNoy1pJKYlIUM5AWj4pk6QjYUNe' .
		'Ces0XRoUhkSA7IsxdgEEG4QSNDJOyXniSBNT1Ogr7CM68RKcNR3KSsRmX0QalGqI4baByQQmlwua' .
		'Ot5Z13MwCaHfM8oRV/IzPiEPpKayCUxNEZ6bikr+Cc2iRSISi5M+FiOwELFz8B4eHtPAoGizXa1X' .
		'JoeBoUKyPJnOgzI14Yz5P5UBJRs+MFKQirUc3rOIX2Q+WMImnq1oxTa+EDeRjgIbaIvceHWWGmZg' .
		'VRtrm0woCMuzCoyyVjoD3XDTMW2S3NSYnouNaZ/qWqUvnsWUH9AmQuKpjovDQUHQh+W26UIPb0wb' .
		'8GbhDuiv+zi+QYTPYrfXR5iNzjGm2HOEvcbFIRG3LaG4os+KlqYT5XEZBkHTybwyaBdyqMISeyMd' .
		'vE2F58GoiylcSMmDGxhMsISiN9lDkjTRuIdOzfqs9n5UnYO7Oy6aAarlgqRkQwfMf/iqQm0Q8boG' .
		'nYKRoMugzWhjFWO6y+yatNjjAwpd7L6MZVxJw1P0k5EVLiJT5bJWyWFYFaJFQlV9mBiQyeSsi0Ku' .
		'oBbLfUzrRNNx5dJ0VIkPwZeIP7Gc4aLhWNe02BmgenMgCjpzEHMVbYclWpGPjBuHIjEbMpdwAGWx' .
		'qYe6FLnv7SqS/RFP/pvR1zORIf9EUJBQfrubSKxkVDUZlRQV/VdgPtX0vj0EviEBk2gf84ll2Sbi' .
		'IxNqeTjZlv8UfxLPq+Yk9xsYLQV9qGn056bb2F++vzupy1rFNXpcFlNphOkGit2Ef6nAPkpXNM0O' .
		'UoaHUzSo2fZwA5WOZkOaPImrFdQAklQMBvThmDHmBjGAVsyYAt+xNK6XdBqBe1UYtJ4Ffx+dyNn2' .
		'uijT7tcs1WmezAkWbrxYfoOyJntkUMaqbuY9iQk1ZTAYKijO2mMCMET5L+8JZRIJOYWil6g2aL+q' .
		'cPXQgaRcl5TZUkS2a1wvoNsuHtCFPFUxQe54AOh4mKE7STi9WLkC8lHxVEIE3OZUhrrNUqiDG58Q' .
		'lR0+OTR0PJNxtowOg4f9rnLav0dI98Q8YVGSau403dN19Lcn1Z4J83slhIcnMZQJl7yYQkUvrPfE' .
		'pGFWZ9u4+CHbX+5sPSopJEpNdBqRY9sRgsLyjD4QF/XcRej5Cro93K4rr23XkXchqkjLxbBoSNqk' .
		'y6YTwQAwlejUO86WwKxcvSJSeFKRCnsUVKZt4ZJJJcTjSKPHkeIeRyIT5nKkMx2AetyBZHfuQHwI' .
		'R93PJqBLWI93pYhAWkpM+2okQ4sjf17tiykf+y9XcQfQqdS1a6sUGVZeg+V1TrUnlnnymjYswHHx' .
		'b87RwsWtG1L9DhbnNZe9lXV3buJW4slz5wgW+3F7aJbUMmGQaGH28y3r6w1vJaNV+zIUx/o8LTaq' .
		'W19jLSxWgFN0nm1J1clBO5HXchedTfmJCigUuUaLOkOhoSf2i+dSs9jFLbEDGZoqlkyIjcqaWu0D' .
		'FTFeibTrnO2ysxA3kCAhbqD+IuAf5IkkhENMCIFErzKaIkZrL97hkGdpqlD2N70UDB3UXwxHYUil' .
		'ZkxLOA9mpDQekUUlVp0pa8OXQcWU8mrVqMyMOJlxpzNrjiq0akzlJmUYYzATaXOBxIqm1I/HGSwB' .
		'S5gsUE0h/Ap0/TFUImlPZjKm8DD3SjjFhocFjg4WjgRyax/aj4ySt2flyXvjbCQ9TVsOpI+0AxGH' .
		'2WoUjtN6sEPrEnVMve0xbYdSgqUDjSVWhfFoDoverO/+QKzNefvRNlcY9to2qoiQRWdUTe+UO4Yj' .
		'A5ItovqambFu1bBnNL+AhkTk2J7oPLyRs6Ltks1+38CbBWS1YJI/6DYH/y8Tsv8pHo60QS3eoQDI' .
		'dQzMnFrQwFSGpiHNab2ssdDLyweZzNQHCI17XiG2ynaIrfyuTlLZn50NToaVVwWM7DotIK0TVolP' .
		'i/f/XjELNWWP1rHe3vpyHUwmFoljyfzalr3aoBYNi2quY50sngJwjRhWv96v03J46WgHKzuHBvba' .
		'It2+sTbAOv4BC1gR6mqNFqdj6W07U1g18upMbEwtldjuVVud3i7wEXqvU0CSZAFJMGoAH5puUYnq' .
		'0zTuPB5WBpKn06fdPcAu0u7pTMS/Sll+0VHbaREOUoBObLNnUesQK2rFlGWaBkA0ixgMBwb8Kz5k' .
		'bUcFinRFdFjzqocvHWOnFK2ykOEGQ6GAJqiOxfJYDSj0OzO9XPnJuR32xUfYdIDjjByJ6EAUuYrF' .
		'ul0xLTLSSeJooUJer7CSumHmRuwvr+UNDpKZdpQg8eIrhGwiGxeqyTxaj1YtR9qPnu9UmOnZ68kE' .
		'NOoefK5erjI+J0mSBAIxjNjadcMaW3lohUdC4Y09wVXWl2MZDE+ysWgrDOKE4RfOdlG+HKopgVQO' .
		'TWVMT0JTyh507bD0MszOZLJtHF6PinTSS3QPg2Z9qI/IvJNgX7bQxOantLIyYStL6QTFERPBjwzj' .
		'R1jzEPYlBjs3L8/KDFPaN54wPHBTHA2v1ZWP7r3ROcPxiqbRwxFB7wqfhmkyOcEdxkFpswt3BLmY' .
		'hOySSXZIwMQF4fMcQ01GqO8YJWFupqxkeQW6L+14pS1RRCIs3LxE2u06s9K/UIKCyxZpM2BVnXgV' .
		'LRy+I5YM7pQIlNvl0sKxKqp6qXPiSD5W4NmS30+1PR3LnBqbDTjjQQ3XbvCOJyG865Mdpd1trtID' .
		'tBvb5I1bmHnDqLCFGbL7HLLqgkWLHReu14HxLfjQZelbRG29vZTk7QlA3qfygk619wFdCuyxXqWm' .
		'HX3FQe4rSpl9uh2bpae1lPaVT+3cyzYG3MGGxPXiBDvrEOShapaxqokenhlW+lNBDnYBeH9lPAlf' .
		'lWyHCrucXskVnAK7tHMawOPBJtNhtfuciNIhvo40wmKwbjBWhIcerBnDkt2uq8aUI+12qroQRSZf' .
		'FOdg1iGRjXTHM18VVJcsS+0RZ4LSA60p+JSIJtPRtOKrg3QfJ7MRkvHXnQ4qRzpPYaIwU56c7bKu' .
		'c88NeZhPu9Cli6NtrmFI0b2RECeZ72c49V8YAQXO66L6F8k7POb/Z/nOkDtL3lO58DM9V/vNjt1Y' .
		'5Sf+rUfru5uPMSOIJ93FPQZ2bTVKYfNkxp0lBpt+o/sKjauY9X+yRVoLc9a3TbyvgZ40cu4IoSkN' .
		'6Lp+iyYylur2tS28QYamTHYoHvfnOQzApXV1w75zgx5iYifD6F0L/GqTL2o0V1L7hl6O4731BTOa' .
		'ONZRkIMSyRVU0zzWU67oOQ38/vyE1jPK57vwkgwNJeyvlo72Y9NRQvqs7x7bt2/h7gTis/vDqv3y' .
		'Lvvk3Bdz/wHgY69/zgaLdDJ2JC4NO9umLJDZO7a3xj4LoUuHBebpbDSViQ4O8jOsnXdTfZvlCTmJ' .
		'Qk+qcA/3lR21Lop3ZJVRGjfCyCBqFZ0SQLfS1BuiZb3k6TRWdVIram+WBypjp1cL2kXf1nIHxSBH' .
		'wJ44kKUQfNH6niNrpS5zFCLr6ydHYjBID54XkZFJ7YFMXjNzgaoZeR99X6kGeZZGWc+ZMughBN05' .
		'PUXNGc0o0DRAZi9K0jEIqo7ZznlyKcURlmrzlDKk95Nu67S+MbNJ6enNm2W9sYP/Oh00IZ1uyvm5' .
		'AgQ8EVJR9ULHtLW7gdfdTuPr7zPub5fRQ3taIRkUIDHRLvYQgz1nfZNqs38o3Mh95f/9vgtVjbEx' .
		'rTqtYfxFaT+49/ZAqt32QDLFtwf4zRbUCz+spPGajA7bA3vlZ1ya083cNEvEvUYqJjTrEsaMPdMp' .
		'+0iZADgS//3svvxEdNHDc6S+yt1Mm/GmJw1ZQw50X8fqObPQzkYk091mzik2e2eJfWmZVOdanmC6' .
		'ExdQu5Rvm2StzBeetRkMy5BKt4O92RlSzDCJ9PcBqodDxN0/9BvTPRSGkminMLJiP1FRstkUns5G' .
		'hZFJnkoff0WFkZYVBi2BTCkdFMY+NrAlsnrSxUqbLfh2oWJINYME278NkAqpbw8rmvNAePU6fBlO' .
		'OeC3dVF+F7rnJEOlVb/dbfHszQkOTUqzdCC6vJp9lxGSN3Ehlyf1ws+31UEziexsZvdbHVdCcSxN' .
		'FbsMNpQ2G6KBwlCl/VB+dxwadyhbkUtdlTBvjYItqGNaITxMee3QLXxEzbNJkX61AybZtlvabezy' .
		'PkJZiqU/ekv6q/EHs/sJ3yjM30/5j9e0U6B70993sjLZbrtF2jb2VE13roD2iuRgp/kwoQxTsPL5' .
		'jEfz9qM569EfyT/A4YxxvaSC+qmqsyGcEUok65TphNxw0b1Gd8dyLmJKC8saYi5Zc9/Z6EH5IPpg' .
		'2Dn0xIGcQw8eQU+32YgJJUnHqRzoQfN2NG5TrJ+RqvVZqX7X6CNQb7F+uoO34EpDOsuL0bpajftC' .
		'h/oF8mnCbDsZ9Z8pmdIxD18Fqsz6jsCyU25hq2GPy11eQ7EzGvLLC5WokspGFVqJNxhpk7IDjcOX' .
		'XbmijWsVM1bR8lM5LR8rGhxJ/BoSPb3tu7PvbbFZF3zu3J4hH68L3J4qheL+30ICMfeKAjlJskcn' .
		'+RYb99qPPTqFX4yUDOJObWQQiyuH3CtywUZcJMB33H/QwOkswYLsIZNA+mM9k9Vq2Rzu70fGmhD9' .
		'GhMwvbJuxnNGsWd/fUEgq3qOdiS5imGaBiwNveQBQlEyJzWtKwT6c6ap/JJJ5THmsA1Pw2r7JzxO' .
		'l4W/oKvf4j+j7X2H2t53/vms2yrQAkjmNMCbK9Pw19cQxP8dFP93UPxZS97qLc72Y+a0WgbyHDqa' .
		'1y8FLh+GHwihv/BtH3rlXs/o0X54NooXduILJ964u6ToqzBww4pVRwrkUXzpjOAn0P0Eb6dElXOs' .
		'RzVnSrkeuR0X8x5iVnIua/VEfLpM+cmoZKoXpujX6bKIgfqnygVDzZv9uI3YnxjkLSsIlMGMT2tj' .
		'5V9WNFQ+x4bA2Cgnk6l04i3TLBxL9hC1UD3WgwmQG8t43oleYk7TysvL9u3tHrbNfawHOvZwi3Ws' .
		'B/v3kHGtmpssV3SQ1uoMIA2/ielKLHRWPnFuloBBK7oaYxb5WE+1MqU5PN6jO7UZ++kvXz/AsfM2' .
		'4Mf/e0bll5i8VQTYBmiKv9W//o9bP0qwQ6ALAw84IJuRHZTLBfXTmZ4g1w+Kw2JYD3/TCvI3q2T2' .
		'yV7o57IXustrjk4a153nVRbS6mtdbdJ3eSw/5iuB9phMjvIr8T9bJke14mhr7S4t/b+9bd/eOtoP' .
		'T/DuZnyZhfWshqfFvt0QTa2XXwWb0pYLL+2FBt6JibH9i4d8b/poP4zWFa72fbo9HES3PGp9cZdu' .
		'Hour/O27+HKFVf7MwRH3pxEVPPbGCv6th9v0Lny7to1XaCOAhVW71mDH6GS063jJv/3ZczqBR4u4' .
		'9/5si92Tf7S/7M7AL2J46B9YIu+I4w0AyCW29X3ug1+T9z45fvbUB8c/OueK78cfnSanTp87/8FH' .
		'vyHte8tLJ3wVSYflYaGcPPvxmTPyz/SUUs/oW3n4MMJAOIBgDKYWg/rbfxrkTVLe7v2xPdRM0cJj' .
		'WLxohsGkM+cx5mx0hyg+THy5GkcVj+UKZsK8FGHR++lv/U4nLzxWeOyTgiLHbgwsLjCgiHwdEWz1' .
		'MFw0PIUwfA1l9RYYtHq5KmEUurzCjvW4S4tpg9Sovxks2pSnDSxB6Gjf2WIvlpi37tfpCoNVMl/j' .
		'Z13l92U4iwovHf78a/E+IewiDr8SPlMA0hAFMlgTs+YojrI08Y50mABjDqt1d7tJ3qq4gi4Y3K/6' .
		'VlAHwX9zCrK7lH4siB3TNXNPMZd1hjjqzQNXLuvh9GVH9XtG34WByPlJ3SS/0rSLfoYEJU+mJNYE' .
		'fffEI3hHJ5VRuQ2Vjcc7dgNk6dul3c3HRNK/0Lbrodj7VDxDlUdbKwBrXRysRiP77HP6CgK/5NPd' .
		'eCGQUSrgj/GkpvRmGvF+oPrzoKS2dUfoIdVcivBjo0K75NWqSjetwXOT6a/69I4A41Scg7KRoIu6' .
		'cM4lx8iwQ3Rc7fvbY8V2z+jf7jxs87s5NdYTohmYCVHDkEUXaZ+4dsTN8e/CccOSN8clYOzviF4B' .
		'TcJB4vf/Nh90pB1I9eY8igwe2a+DdnmxbG8+7ojjp+CRqrmDRPKn+o0ukXTcqC5YzfCMzWhq5SCR' .
		'/dvy910iu9ZAfPdGdBqUVWEGuhfxfpUD5f6Tle5w5a69vbXW+uKPAWTbqwyjanINgR9RQ+wRXfm0' .
		'vHP0F7yKAprFwFUUjooN2s1ujOUbcDqiSyuJxWU/v4k8p18m702BTOlqyYwS/HoKB97TWNLS4nAb' .
		'ufvi6u72PH0N0MZ2VBQUY1nwnS2Zg3sZSTpEqG3EV48x/8sJPnnJML5bjXV03zLmjA8/Wg+3Ai+G' .
		'7N4YZruwgs5S4LWBjj8unmga6B/PCuTV896HtB4dluzVH/j66yYdwAPwbFoKwIcyKRG5P7qK74eg' .
		'IWXDlzvYd8YAp6NWcrg9n6vGL5QnRNYABj+inIRRedZgNKhysPbXO1taodszev790+T42ZPvf3D+' .
		'9MnzwX68UhY0lTyTNu00UHgnKbnJW2qxPAJOIFBhMqQ1rd3ksdCo/cNjLDW/tyUHPnTA+w8DT/Et' .
		'p1f9T1t/2KKvLfW1vbYRBvf+hrWxIz2V4l2/eegsWQXjkrYPufrb/NzBydWdZlu5eo2cFE4LZ1Ux' .
		'PVmp15WvMx//j9Nnz3USLnk6HYTrDODGRetDMEW6OqHtJVy7m81WfScgBDDgSiNENFr3FkNEjnkR' .
		'PvFco++OvPXaYjRJF8k+BOk//u3gFNRuc+XnEqTSVKU6VcE3KR6gKH30ydnzn5w9fbaDMHmm1EGY' .
		'3qd05+L0Lt0BCbbGIgsA+XQLoLohk70JWmje/Q420X7wVPp99YH9cvXVRWLcANKV9qVc/nXz4JQL' .
		'+Ao/k0yYmmoapYPVLudOHz/38Ucd1Ys8oQ4S8S4jO/kYj+Wd14taO3mwFrHa1OU3uOz29TXSWoPI' .
		'qCaJwULDuuGLP/YvDKpZrRj7EYX61wcoCk/tvyz+LKKA01J14+Bk4fi582ePf/BxZ0GQptNBEH6l' .
		'AaKVEjmOpC8YE20Vg7vzwa7Ko9cO0T0HvNwLh5tvvDrnq2rFqO6D828dHhoYSowcHPdX8FXJeJzx' .
		'Wv2AmV/JqSX14Fh/9uTxj453Yrw0kw58P48Eb8drfkKHnbmM8lOeuGlET+tgcLvwvA2v/3HD9/+0' .
		'A0pdxuiqedEMbOOwF2TsJ3IXx4D2jC4DIXKAIDzBYa/XvDGzKo3VISL1CNrvRUYIZGnDeb/un+km' .
		'K89grqy2bizSd//eXAQvtrWyha/NtZYa7I27vwxK7/Sk4QvfJAu1trP7bIdYX8x7JFdWLdBZFpw2' .
		'GiwwSSk48k8RkwLNpwSPbMBkm58Hp4cBGpVcejVqY6W1stf05ABCmh5z83EjeG0bvhz0JD2ue4CT' .
		't7fsxvdWcx0YRDeRm03gqr3ylNg7q/aNx/Y3jXbT8biwkptJ3VBkGHM4D3o6XrczMB92SyWK/dcb' .
		'TOjqdNmvLLKLKhkf/zJHrM/h6WatBXNc2aEKU27WjoWykybtTlBXC+dsL6zubh84C2XvKjBjuq8R' .
		'zHnjNEFyv9+m2p8uV1CyHTnq8Tyk2QnQBz0t2XUIMlIyZNajRSqcy0/xBd703eHrUr4wfDKSNZWc' .
		'4OvshD4ziK8woX1ZSW4CPNdC7FlY1EW6+s05StalRWQ1dq9vEuWTO6GJ7D2KCDyEw/fGP6u1bq0S' .
		'Jt70ygm2M8oLbnABfVujV1TQ2zudO6pDKg/ewve+42vf3e2So1rRmf1HKvqADAFabNShQIHhQD0Y' .
		'zN4sghMTxeslxNdANcJDaP0n+Tpu4ibbRR8wL2BeG0CE5r/j2kBlsEw15BfgKSx3rlJwN0aRAXx3' .
		'VEztPcPZixqrloj0EoAebjFp1IFXfM/JlQ1ha6ob6X8jjl51Kfh4wMMwjfLkzM+/Z0MjF3IOmPPW' .
		'4UElOTBikhNaQdfG9y5xoCQV9GxX4+At8ANmEvv62m7zKredDIi8e7NnDQG9qHov71bq5xxo8wZY' .
		'4mBXz2gqwRKfR7wJT39belpLCGebNjTXola1Nj+zcAsWMzqK11ZhJTbBZKELwBIsbunQFpCM0sdZ' .
		'vFbzFl4W8y1eaIO7UXT1eQraXmHqmX1N3bqxbTUedpj66XF0tDpOXngeYp7Eopf1sPRCo3V9Lc43' .
		'jOkmH3hW83XrwRp1vNBdvgsecx0vELK/BM02X8d9Ouzbul8/SLoo+xMJ2QUPo8tJVmUPC7wjbXjh' .
		'pcN2KhgilgC6gMP/+WPUvvbKvOOjvpizXtTou9gBCwwo6OPdzW375lJr5XFHqhxs9L6XhvDctiRX' .
		'uPqpwc62Cf3l1uq6NbYYq95aos82f6TbtQAcrNjaTpSIXYw5jE4Y+/ANEEgBdAc9JU2OFO4+3aam' .
		'mj7e3cYtYFijLtm6tTNv1mG7Lu1NrqoegJvlHoPqaHm8Z894afqbUIvevuTcl2wc3bugwZECvz2E' .
		'NtSrur2NBvNanRaVNtbpDWUQVQcKGcqj9vocLCC81QzCMKzOXlmMEk9ZBD7lt6ctP/EXRvhcNOGT' .
		'HWYlIX4XjL7XCJMO/tIWX33pfrwwiffSMbee0ROffHDmFLmUVNxAy71xjgMT/2fmKnq5Onqob3yq' .
		'REH30ZNkl1RwcwyjSo6RvJGbKoIgxCe06umChh9PzHyQ7+uVj/H00psd9PG+X2CvCAhqdapCj17i' .
		'9zjF8oxuVuOwCPp66YEt7AK/43Ha5Tn4QxwjTHZf4m12rHafZsrxJjzQdV9dFffF0R4H8gePyhIi' .
		'Zk9ADWsnKsZFrdQHyyfCzsQhNcaMy0AMeAaTMUzNrPb1et/pG/Wf/uzlb9Duw67/8i/YNxKnyiDO' .
		'Q1AA2IvH0XrFm0sosX4/pVVmzmkFYLVROV4o9PVCz95IHDyA02pu0uWUiyAQnmJmFMsFrapFZsWT' .
		'kgp8UAu/wvVHjh07RhLwm2+OI+QKHZzQ2QGDTuN7sJFbGgR2fb1apWJUeqNEkpAQEHSyV/w8BS8V' .
		'wn74gxWvGO1fq6O0HyD/9stp5CVESSDMJpC/DcH5WUJXqvt6PxCvPAcKfDxmapVLWqWX6CXQbaW8' .
		'MR3hnAAm9eEQ+rHEiE6OiqHiBa00UZ0c0d95B6jHH/5W/51/Zei4LCg3rhCtYGrEFUDdAHxL2jQJ' .
		'w8QVCmBdRddMjg4h/HtQejSnCZ2iFtdNF3IJJItocYZoOJK6EZ8qGWz8PtGUI4//XeHifyVKZqug' .
		'G81Jo5DH2/nFD4I0QcwKKMBG3AFecASMEFOr4jarMVX1qSz60vSO7BwuGdW+uF6KhC0mHNShB1V/' .
		'QG6tgFrvBN7UASQ5WcD7b84C3D6ODKddBW+WA2YzUYARYN28T80cUrHQnsk+OqUSiQRbR75V1OlN' .
		'ZTT/gG8FOuj1wvBr96IhqpNZth1PQIGzh6c1GkscUQgwMCsI7b79UbpNlDgzWNtB5W5v0m0gfCMZ' .
		'RrCtFelGUMyqYBzH3zXWWMJ7RO2XDadRnK3oamWGca4N93/rhLK/C2M8/uCw3tX0+DjOrqX9yMhr' .
		'XrgCKLrwv+t1hAE1BfQGpnP75zAZ4V7U86YAnANvPA+wo6QEj/AXriGi5KIErQRCpYSAg0G4lJ3/' .
		'8AxakV7RCfXPRXiSGCEXoTP0uUhVDvZQy2WtlD+JQ/c5Vj1X0SCs5oYdZLM3EvGiTd9/dIwCEFg7' .
		'gwmrWVZ16OxbQOB7iOmyw2T0NdzvcALQtcTsUj9RRjw9x8C84hyi9NMp+JjUhqLkQpTk4A/8zbvt' .
		'ccIX2IQvsAlfwAlLObwcp/BvL/xuRH6Mz3NxY3wcVApHTXwNwYsQnM2HanUyro6ZfdA7hjOMyC2A' .
		'Y3nAgSKNNOfI50fEjC64pCXSp73nAJAvUPuNgAA0MgXmwzQLJjNRCMCnGnHsRniT3jAEZG5X9RyK' .
		'T2mqUBAzo/wKugWMp16/QFaKCClEdIkYIlyRexAQcjWCynEw4dD6ivOJa9wgdiwgAewoCKe9AHjI' .
		'BXMlp1ZBH4CXE5kN6F2WUrkGym317+O0BBUyPTC3Mk/VPjvZai1sWI2H9N5lfqqmRi93ds/N0X1F' .
		'9mLGhYZ4jaMc3IOGZdDZ1dOoizEwgm4rO9Irs3AXD/d+IQpbW6QArq/tvrwaro6p8khwp+UUKBlB' .
		'd/xBK3YKLejhxl65eb5z81PqjGiOvkwR7W4xjnd7nGRhLHTvyyewJ0CuTvZFYLUn8Z9e+6tlZ1Vg' .
		'3zz2zfv6sq58Esw/6yA27gkNusFA/v4yE9jDwPzgF4vAf8zMPGnSa76dg2dgi+/SYBqnIEr0aVpn' .
		'vkYTzTTI5qCdF6mx/QvR1R3m2RbL+dBDBlSy6BXltLyfb+y4jT13jxNny6eGQ2Mk8WTLv/XipL/5' .
		'69haf9qxny3Zj261l8pz54+f/V8fHf/w9Dlg7W977NWGfR/i8rWeKMHq1lZ92/riLn6hr4P7cfeH' .
		'VfploYHnxe/8SJu9nNt9jk4Y/aVRa9Vr1sYW/8X+y43d5//KAdifvQQvhn9p3XsM8Sx+gXiWAcWM' .
		'GP30oGnfe9JaoY8xWvpq3mZf2MYxeEv4pbX4uLXQhEHol+ur9qOaaFZbx7zgF+zLzQfW4tzu1pxA' .
		'6U6TA8AynNV1u7EiQG9s27Vt+gUe/+UGVu3xCT7dsr57zKcO0wCM3Dm17tYF6PsPxS93ajSVvCx+' .
		'uVuzaxSa1VxBROtXabPbt4BcnN4IbR63lEWf5o/Qjf7yfNVqPgVmcBLba9u7LxY5ojBNgCEANK7y' .
		'3sAg62FDPL65yBkEwwMFgZVi+LUNEFI+CCAG3+mXb3aQj9/TERHF+bsS+e4xJtaeooJkoAAucNSl' .
		'mLW5DJNhVK7hqYHNZYFLrSEGufkA57iwJobHij9By92tW5wuVrNpbzb4L0i+9VuCykCX73fEOLA8' .
		'a0+FgMEvL0BqnEHnVwEJzkAQVw5q9weY5oqYWf2qXX/IZQ5kgWMJv7Tqq0JkQDDubHCRwR2WW0v2' .
		'gtNsZUvQCaj8Yo73QdDAV0ZLbAYkX2lI4jwvVhgoCHdQ9xeOAZ/mnR0Yngs6h8YkCwQDZAH4I+YM' .
		'8+HjIGvnONsAa2Qol/qbDwD07vMlIVmP5oQw3VzClPYjZ5zrqwK3Z8+R1ewXrKUC0F85MwXcmDyB' .
		'irWfOoIOWhEEh08B1tBKQ2iM5mNYJhxrnPa1xyB8rsoRAFZR5QC/GKIrNPm4JiTi+lWOAc50vg5r' .
		'16HordadRb7YEcDTLQ4AqAHi4iybFS4erbtPEPr3O5w6TAnScR7WYbFb3zwQ06Yw+BTgF5cG1nc3' .
		'BADQZPALbwZf1rb5oEBEmBJfXdZLJs43F5GWNaYvv1oSj1FKdjgWTJg4j3DqtVV7fY7PCQVwbVsI' .
		'IGhoThRYZ+u3+MpAAPeaAvQ3O8hxV5utz4kFhIg8FRoDotvNOc4GWi22JiYEROBfGivALRdL4OPu' .
		'NiPco3nExeEWxXLH0QarXJJQEEDG+MyA2Ouga7akZc71xGoDAThyiSuSYwDalwkLKEcUCU52mP3a' .
		'DrdC2KH21Gq8dL8IxQKuHwTk9x0zwVcl9p4TholJ5MK6q0n52sMOINVcVlHUxELEZqBO7tddFc+l' .
		'GPusz0kUW5wTihFYWQcGznNRgz9cXYN94gqLfbGbG4IT+Auj94sl1/oKQYQ5OMu0BbS5vyFx/fpV' .
		'0Qy5viYYAkZ6te6si8/hMVf2WGE3j+veXfQcAFVVQrmgeOJMGKueNrkKtL7lhHmKw3GSUcK4qkZo' .
		'sZUaeyOtMPF3hHBiPuV+ffcZYwUoA275rzXRkwJeNgUK1hb7RUYYcRSuQoOjRd+qQkkCvhN8EQN9' .
		'L1QOF6GzH7JfWPfP5sHh4t2RYHf/SCH8sNzzO9dnLxnTIc4/uMnJoYFELJGMJTKEZna+WrbvLeML' .
		'ZaT37T5t8tTPi7lWrUnTT6LKAbC7htvaNOF0448eN49HHeqMKYL18YIB0TViEP/k/Mk+QAo9+Xch' .
		'vPyNplb6IlHCH/G4wPnOkI6QfjKYTScSIjXHRsDT394R+uigMZLGHgNS0zILaF2f87d9fbT7EekZ' .
		'z/5gQBLyMKSlRGetwKP7Djs1rOLJE1EV3jPg4x693jPksIoOxDYXyiy6Z498wRKdMURW1gLeo9Ar' .
		'7S8gjPcMH4T3jDhunWF6Qipo+iV+PNYLcLRSzshrn5z94KRRLBslTFPRvgKuLxK7EkFRO9ovdrbo' .
		'JmL/dHl4slos4Lbh/wcjr30I07AAAA=='
;
	$checks = array(
		'여섯 문 카드' => 'class="door-card"',
		'심심풀이 카드' => 'class="free-card"',
		'가벼운 질문 카드' => 'class="ask"',
		'오늘의 운세 링크' => '/today/',
		'스타 이름 자리' => 'id="starName"',
		'값 배지 (0이어야) ' => '4,900',
		'script 열림' => '<script>',
		'script 닫힘' => '</script>',
		'앰퍼샌드 두 개 (0이어야)' => '&&',
	);
	$page_link = '홈';

	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<meta charset="utf-8"><style>body{font:15px/1.7 -apple-system,"Apple SD Gothic Neo",sans-serif;max-width:940px;margin:40px auto;padding:0 20px}';
	echo 'code{background:#f4f4f4;padding:1px 5px;border-radius:3px}';
	echo '.ok{color:#0a7a2f}.no{color:#c0392b;font-weight:700}.box{border:1px solid #ddd;border-radius:8px;padding:14px 18px;margin:14px 0}</style>';

	if ( 'undo' === $mode ) {
		$bak = get_option( $bak_key );
		if ( ! $bak ) { echo '<p class="no">되돌릴 백업이 없습니다.</p>'; exit; }
		if ( 'NEW' === $bak ) {
			wp_delete_post( (int) get_option( $bak_key . '_id' ), true );
			delete_option( $bak_key ); delete_option( $bak_key . '_id' );
			echo '<p class="ok">새로 만들었던 페이지를 지웠습니다.</p>'; exit;
		}
		$wpdb->update( $wpdb->posts, array( 'post_content' => $bak ), array( 'ID' => (int) get_option( $bak_key . '_id' ) ) );
		clean_post_cache( (int) get_option( $bak_key . '_id' ) );
		echo '<p class="ok">되돌렸습니다.</p>'; exit;
	}

	/* 2026-08-31 · 글을 gzip 으로 눌러 담았습니다.
	   눌러 담기 전에는 스니펫이 74KB 였고, 그 크기로 저장하면 중간에서 잘려
	   따옴표가 안 닫히고 → 문법 오류 → WPCode 가 스니펫을 꺼버려서
	   ?stella_patch=dry 를 열어도 아무 화면도 안 떴습니다.
	   이제 5분의 1 크기입니다. 잘렸는지도 아래에서 글자 수로 확인합니다. */
	$packed_txt = preg_replace( '/\s+/', '', $b64 );
	if ( strlen( $packed_txt ) !== $expect_b64 ) {
		echo '<p class="no">붙여넣기가 잘렸습니다. 담긴 글자 ' . strlen( $packed_txt );
		echo ' / 있어야 할 글자 ' . $expect_b64 . '<br>스니펫을 지우고 파일을 다시 통째로 붙여넣어 주세요.</p>';
		exit;
	}
	$packed = base64_decode( $packed_txt, true );
	$new    = ( false === $packed ) ? false : @gzdecode( $packed );
	if ( false === $new || '' === $new ) {
		echo '<p class="no">새 내용을 풀지 못했습니다. 붙여넣기가 잘린 것 같습니다.</p>'; exit;
	}

	$len_ok  = ( strlen( $new ) === $expect_len );
	$hash_ok = ( sha1( $new ) === $expect_hash );

	/* 슬러그로 찾습니다 — 없으면 새로 만듭니다 */
	$target = 0; $old = '';
	if ( is_numeric( $post_id ) ) {
		$target = (int) $post_id;
		$old = (string) $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", $target ) );
		if ( '' === $old ) { echo '<p class="no">페이지 ' . $target . ' 을 찾지 못했습니다.</p>'; exit; }
	} else {
		$found = get_page_by_path( $post_id, OBJECT, 'page' );
		if ( $found ) { $target = (int) $found->ID; $old = $found->post_content; }
	}

	echo '<h2>' . esc_html( $page_link ) . '</h2>';
	echo '<div class="box">';
	echo $target ? ( '지금 페이지 : <b>' . $target . '</b> · ' . strlen( $old ) . ' 바이트 · sha1 <code>' . substr( sha1( $old ), 0, 12 ) . '…</code>' )
	             : '<b>아직 없는 페이지입니다. 새로 만듭니다.</b>';
	echo '<br>넣을 내용 : <b>' . strlen( $new ) . '</b> 바이트 (기대 ' . $expect_len . ') ';
	echo $len_ok ? '<span class="ok">길이 맞음</span>' : '<span class="no">길이 다름</span>';
	echo ' · sha1 <code>' . substr( sha1( $new ), 0, 12 ) . '…</code> ';
	echo $hash_ok ? '<span class="ok">일치</span>' : '<span class="no">불일치</span>';
	echo '</div>';

	echo '<h3>넣을 글 살펴보기</h3><ul>';
	foreach ( $checks as $k => $needle ) {
		echo '<li>' . esc_html( $k ) . ' : <b>' . substr_count( $new, $needle ) . '</b></li>';
	}
	echo '</ul>';

	if ( ! $len_ok || ! $hash_ok ) {
		echo '<p class="no">내용이 온전하지 않아 아무것도 바꾸지 않았습니다. 스니펫을 다시 붙여넣어 주세요.</p>'; exit;
	}

	if ( 'go' !== $mode ) {
		echo '<p class="ok"><b>확인만 했습니다. 아무것도 바꾸지 않았습니다.</b></p>';
		echo '<p>이대로 넣으시려면 <code>?stella_patch=go</code> 로 여세요.</p>'; exit;
	}

	$had_backup = ( false !== get_option( $bak_key ) );
	if ( ! $target ) {
		$target = wp_insert_post( array(
			'post_title'   => $page_link,
			'post_name'    => is_numeric( $post_id ) ? '' : $post_id,
			'post_type'    => 'page',
			'post_status'  => 'publish',
			'post_content' => '',
			'comment_status' => 'closed',
		) );
		if ( ! $target || is_wp_error( $target ) ) { echo '<p class="no">페이지를 만들지 못했습니다.</p>'; exit; }
	/* 2026-08-31 · 백업은 처음 한 번만 남깁니다.
	   이 스니펫을 두 번 돌리시면 두 번째에는 「이미 고친 것」이 백업으로 덮여서
	   되돌리기가 원래 자리까지 못 갑니다. 그래서 백업이 이미 있으면 손대지 않습니다. */
		if ( ! $had_backup ) { update_option( $bak_key, 'NEW', false ); }
	} else {
	/* 2026-08-31 · 백업은 처음 한 번만 남깁니다.
	   이 스니펫을 두 번 돌리시면 두 번째에는 「이미 고친 것」이 백업으로 덮여서
	   되돌리기가 원래 자리까지 못 갑니다. 그래서 백업이 이미 있으면 손대지 않습니다. */
		if ( ! $had_backup ) { update_option( $bak_key, $old, false ); }
	}
	update_option( $bak_key . '_id', $target, false );

	/* kses 를 타지 않도록 곧장 씁니다 — script 가 살아 있어야 합니다 */
	$done = $wpdb->update( $wpdb->posts, array( 'post_content' => $new ), array( 'ID' => $target ) );
	clean_post_cache( $target );

	$check = (string) $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", $target ) );
	$ok = ( sha1( $check ) === $expect_hash );

	echo '<h3>' . ( $ok ? '<span class="ok">넣었습니다.</span>' : '<span class="no">확인 실패</span>' ) . '</h3>';
	echo '<p>페이지 <b>' . $target . '</b> · 쓰기 결과 <b>' . var_export( $done, true ) . '</b> · sha1 <code>' . substr( sha1( $check ), 0, 12 ) . '…</code></p>';
	echo '<p><a href="' . esc_url( get_permalink( $target ) ) . '">열어보기 &rarr;</a></p>';
	echo '<p>되돌리려면 <code>?stella_patch=undo</code>. <b>이 스니펫은 이제 지우셔도 됩니다.</b></p>';
	exit;
}, 1 );
