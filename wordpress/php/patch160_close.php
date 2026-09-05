<?php
/**
 * STELLA SAJU — 직성의 신 여섯 주제 갈라 쓰기 (2/2) · 남은 96개 글
 *
 *  1부(patch160_career)에서 빗장은 풀렸는데 표가 비어 있어서,
 *  맺음말도 카드 문장도 여섯 주제가 아직 다 같은 글로 나오고 있었습니다.
 *  그 네 표를 채웁니다.
 *
 *    맺음말        여섯 주제 × 세 문단 = 18
 *    배웅 한 줄    여섯 주제        =  6
 *    카드 잇는 글  여섯 주제 × 세 자리 = 18
 *    세 장 겹쳐    여섯 주제 × 아홉 갈래 = 54
 *                                  합계 96
 *
 *  넣을 글은 gzip 으로 눌러 담았습니다. 그냥 적으면 스니펫이 너무 커져서
 *  저장할 때 잘리고, 잘리면 문법 오류로 스니펫이 통째로 꺼집니다.
 *  잘렸는지는 아래에서 글자 수로 바로 알려드립니다.
 *
 *  쓰는 법 (WPCode Lite) — 확인 ?stella_patch=dry · 적용 =go · 되돌리기 =undo
 *  ※ 다른 스텔라 스니펫은 전부 꺼두세요. 다 같은 주소를 듣습니다.
 */

add_action( 'init', function () {

	if ( ! isset( $_GET['stella_patch'] ) ) { return; }
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	$mode = sanitize_text_field( wp_unslash( $_GET['stella_patch'] ) );

	global $wpdb;
	$post_id = 160;
	$bak_key = 'stella_bak_160_close';
	$expect_from  = '59ac2e3f6d75176c1a740a582296d6dd1c44e377';
	$expect_hash  = 'a89b64d76a0bd688dbd95810ce37a5e6370e2ee9';
	$expect_delta = 27909;
	$expect_b64   = 9708;

	$edits_b64 =
		'H4sIABIdlWoC/9VdbW8b15X+K4N8kZNVmzQFFotsNkCbFIsC3fUi6be2KNLG2Q12YwfetEURGKCk' .
		'kUyJVERalDWySYaKKVNymHosjxVqLafA7j9Jv3Hu/Ic9r/feGQ4lxU5suQgam/N277nPOec5L/fm' .
		'V5+8cPHdDy+88FrwwjfNXpAO/sd06umgEXxTaQVmc2jCu4G5dWR67eD/NgMTjoJ0OEpru8G5N39x' .
		'/p2f/faX5//t52+++MJs8ML7H1x8D1/z64tBcOUf8f//+O7l4Bc/eeeXfNM/fYJ3Xb7wkd4UBLO/' .
		'vsh/ePml4JtWBf4JzGDOhPdMJwpMrRf871eFMXjjo/u/k394DPC/V1959e9/8Mo//ODHP8Ivp4eb' .
		'prtjOpUgu1ZJe6N0pZWuxkHWbI/jClwNzfUkMN0q/MuE7fxA4Q771vTObtpsBON4C99lZ5Buw3Tm' .
		'Oul8NL7fo/dsVs3Kg7RWTWv9H8p70gH+LTALVbzdtOb08ksv8/tnzFe7ZnPR3EhmXvuVflJ/xM/N' .
		'R+nOUWBud9I7i9lGBJMITOeIRjOopIP6LAi6L3eaLRxfl+7pNtLbQ3o0/loeMps4i8r4sOONM72+' .
		'iwIYhMF4f8F0kiA9qJjte9kGCgUFZTZCvBe/+dVI3ksCnE+8v/FdIIJ0NQrSjTr+lt3cNa0hjOhT' .
		'uGputH44M+tmuDkcj+LxYR1mEYzvjXAMUT/do6VIa4eAHhwM/Jxe78t3YPx4NetGNE4RfMkdpt1L' .
		'59tZtwpwrJhDFBoKC4SRJn1v7jghXtqKXDcwcnhpGt5CmYFExvePCAA7Sf53lPh4P4bLJItaP729' .
		'KK/1Z4lTuLfIYt1ChAEq4EvwjvTOw2xjz64CvGBQ9xYjne/hcv2tUgc50yfuPMQVDtumM4K//62y' .
		'GqT1CioZ3MPSpNfCqsC46MO6JPBFvB3QQ3NAuNSD8f37pgPfgfmZaoT4He/X8Q2w8ul6O72d6O84' .
		'Ilg8lNb4XgxLFJiDvfQgdMOf4Qn/ZlYxDUYANC+P6exG3cwPaYwrO2lvx7SPUCfGD5L0M4SQCLYE' .
		'2YQ7eLRbV0isNNyCB+nSuong8Ua60CAo9qppHJnuol1m1lx+RboW+iCOWymIGOaEK7AzCrK1ZRwL' .
		'QiW+6aDyeMhttQiNnZHpbcDrFK7y81IDRY1fup9MQyj8OB5VEfLpek81FMSC8gMbC7acjZWnpSIY' .
		'exWthawkzpGlDFIoKCQAB+/kVWJMD+F1qEAMWLOx4psNBqzZymkbiYYmV9A7NAC1NghpNkj3w6w2' .
		'QvyRbsWt8V8rFo1g7aq9AiiDtLHnaSyO/qCShTFNu9Y23aZb6wkkdhIEY8G6Rn8RbUGjiKZzFf74' .
		'eY2wxgNxRrMEj7Io6TAxm1fFFDFiKri880lu3vY7cN8u+ISKj0yaDs3c2hgZHUKyXhnHbQtftuio' .
		'MnHziWAJ5pJMRCROgRYMlh/GmrOpeBNfRXfXOWIlLcfpdjy+l4BrhQcYLICG3hyAgmUH74dHFmGe' .
		'1/okl96GODO1pV+NzJ1H3kKWGlGSzQhnCCNSEeOr2GQNj4UqfRKWEN2TXTy0gCx2eo3ZOAp4YGqm' .
		'53fzDoMACT+C9WKrgcZUYNaxPs8sD81NWIrmFFxmVxNQswIu4e0wUHBIPjTXwnTQYV2i3/aj9LMj' .
		'0rT9XVFOnwTYacGFbH5IYLjfA2gdywGQotD9rHabSySYvJgIu2RsOyG+trCECbwM0ffYbr7V0tv2' .
		'h/AXGq8YfVzxWRQ+Wm10YU7z5BUh+fDuDtC6XbgJ/raMcN49PM71m5CeTMMIVtMs7vK9bErrCqUV' .
		'eKpP5A1NGCrF3CREUW9AOUBFQNZroQLE/X3QQOzRy1fG+70SdJYZesAaDBDcY5GKeYqDitCqTPXY' .
		'dB1elREDY1YX5FYF1gNZBL2OyMkaW6PbU20qwGqSsfKPaKfYkKK4Okm22D7RnArBQVx0I3UP6rFQ' .
		'BeM9U+vkX+PZUIMPNSL/zsRzh/L28f3QLK1mG72yNyePh9osgnGgOlVzSLV/CZX0WaNSQHQ2N0Rz' .
		'Al/IvyDbgDU6HJnWHgzxM5q5d7kUzOJGgKAhXEHdkaaxZFC5kPSIfO88nOJAPK466JsDXrhomPb6' .
		'OeNaSlzR3usiMHN1q5YtPTCDETuuKsJi81OQLtgP+FNjFm0n29REHA6/bNDFW4nuilKChdXIQqgt' .
		'BW4iFPqysIcEFVV1QaQSVWmRi1juDtPhUQHL6VqVcLkfHsMBFghBylsGy56bnyCgss7pfpXYNdA9' .
		'GJ/8aLoLYhfIfWywLtS+VG9JsgR+glEUUY1dmDxN7AnJKTh4WSMm4jTrkBb0VszGfwC/EOfOPh0B' .
		'Jss9fxWisQfpTk+mJS7S9JtkbwQolI4g6JFxRyOe1Vu4jCBkYDWIVrEbTHMQsESQiYoCskq9iwdZ' .
		'Gf1BtYjXUjIAYkzX+/T85zWlxbCWLIqsvWfWR2hQUQwUg7GjY5LiYqtcYIVamwJfA0CRye5PCawe' .
		'+T5IHqIpKN0jR5bNxTSpCWp7TH7mymzgp4O24c2xubnI9qQfluSEzrnnpySBXn6pkFYxm7HL8CDd' .
		'G5AFA7GTWcXwXxIvsITtEG986/z5t/kj7wQENST9yzKvsqyS5JROSiblZ3fOjfPF0vzKDITvZA5Y' .
		'aZkXQQThWyNaExsDCSb5B8/6tmLy1/qYlxlh+7UsOqpWaeeIFxoMALIYQCjYqHCkTjq9zXZjQy/j' .
		'd/Y4ZzBhvBGttS2L54MtDelY/+hy1dEyZaTjUSL2CTm9p0d+tD4jNMQFyERI2hi71foUvtFAJZyZ' .
		'j8xcm/9mRTN86MnF3hyqA0zXtmCaFJ1KXoONDFo5UA7H1oRuOjm5/IG5DnFtjx6+3sNBiGmmVYDl' .
		'jEMhwHgt2g2c9oKKEf58Uj9TEitKiEhxQe2Acz0ceuuE2IELzdiTC5xgQLtSvIzfXtgRlsezjzxn' .
		'j8Ag78U5yYXOOJ5jT6GzN4tqHQH8MJpDc79B0sFBU4SV1h6w8wmzaEpGyg87lLOKxx60XVjm6wPd' .
		'RY6IB1obyhJ6oQGwqvyqQeSHuM1hXAVIQaGKhKIds9gizumifBc9kmjZ9dv7c6tS9zMfy0O9Bnwe' .
		'Oe09IpKc8lFWPFPCY2eU8bASEm6G7AMtjUGj9fVogrkw7YqvcdREyir+gMmHSMauMrCNnGhk2Ujv' .
		'r7KSUTSNCQZ0+0iH4zIRaSiAdoKGBjcx0+zZ2KCEDztePhFr+2xoxlw/wuT1DqU/cyFf0VyilxIK' .
		'wZCQnMH+JmVDIrdeJ6DEVL9Aw6OxeoKRMM5uJaIxdBscUM2WvdoqKIfxvRGJn4N0shcwoEbDT8zU' .
		'LUN0puBpur2Cs/4cGD/yA3jbVVLK4QhpwNQyDpvo4NybP3n7rd/+9O2fv/XPP8t5cKZIV3hleU5B' .
		'8P4fLv7+4w8uXQx+d/mD9/79wvn3z/3nhT+/6Bd25DHLsU72wqVuN+94P7G1lODipT8Fr7lrpFgA' .
		'OdbXfBIfV5NEguJ4/cKHb2jezdFYvI29LD/6+stwG0EMA+49z0liZYIyxJpj3657GWPVjlmNw7Wq' .
		'sDCXLbQZ2iMaK0CSyKUoOANKg4tZN89Lf7xwGebpqjDXH5IPGo1ket6EPBix26Zp+CHuSj/7dItc' .
		'ruoBBT5HaKLY789qbcLqPKiHl/rBvGwfZor09UjDKIwpSqKIIPj4Py5cfG3Gy06GXDoAF7U3WZRB' .
		'wsN5WkmceUPHaRJHYdkPZBVohvm8NQlEEo9A0JAQ6HMsj5LM1YwO+YoXFDg6M4k7vfY4uBMWKNbN' .
		'gpAyYqPjAchVhUKeHozEYTQdOgLETpIfHg7oZMBIuuDIc39sOQfbRCOQwrBVvd4suc1lvTDkgUVp' .
		'tjhb5t95auhgCUryiW46JAxc7ofToGNWDs0AnRUiR+S20BCaS+tiyw1eQpDyHYGSm2+PHkcCJ9Gj' .
		'1x7LahFVReqPSmoj69OgB8no/m4uNa2kyOYqSZxOHuBUS1LpFltcYugR2SANDVFqHnuYABTl9wsW' .
		'R6qOOF7l4ZwdimhJQXtZCro6j2V3PPCktb9qnO6NzA/RckgpMS9Op8BMZtdtDTJuyTdIK+Y6hemX' .
		'AcWj0hNAsdee0L0xBQM7joV9622moURoMiZYsGJTp7hYioESj4Au3R15kZF/udwM5WoSee91ohWS' .
		'hAalZhIsHc9Hs1IxoeltLknmBV8PQe/Nin8fxGi4GNVqOZItVGh4LU2VYaAssa+Xf7sZAj5IeRon' .
		'QMQreIAlib+2xunbWxIXXkxaEr32OACRUJPS7WxANoeno0FekKNzzuoN3xMUkwOezXBfnSAw6WDZ' .
		'8aFS84Fl2p2C+ZD0ORWfdhryAl5+DKi4KvoQ+1G0fPXY5KXogZz0ykyKpmt12afyFJEaGxEh5Ka7' .
		'7YPlWBvixVuTENFrT2JDIlG+U7kZECgXQudUQR1KOg1Zg5OBol/EqDGxJa86a9dJQNGc+51H4ucl' .
		'zw4/+AVAqeU6f4Pk9O4ovbWrOEFT0NVFfxK4lNkTNsyamZ6CEZADoX04Ii6bC41JZyktdUqzcrow' .
		'rhBS3pJAcUfzRabzCIP38phyI8y2lrFEg4nGc2+e/5efni9JDB8/nt9f+vB3l9559884ntng4lON' .
		'LD985bWZ1z96Q6YsEMTuLtKLbpN4LylLEXSYaucr59K9FqK2V3mRkp/kQXeI724uSf7o9Zc/emPG' .
		'fTYI/o4+yyPH/BjmNzf5s5zd3yMAgH8aNDNGPmjdeH+PRhT1tfxjl53Gp91dlLOuUJlli2r55pBs' .
		'DTK9JUB2W2rDLrvptaVpWTRKF0Ons+QIbmFi56otYGHwaHGM+ahRrHlU1LU9OzSYvKc8H/6IhD5V' .
		'gioEkCLPyoRdcVf+fE+QKJZEbiTYvGmFul+V0nEAYS32ciJDWpgbJxXOw8GCJRh6530i15ld3TRu' .
		'siSDtA1fuf8AxesoiDbv2NYzoMBp2OdKH7JlXAPXXeVV3Tlz2CK3AKwGW0NyHU1IxHo7sHLcDge/' .
		'P2ijwZY0WrMhKbEJcb96srg/+dcrVtySBnB5w3JRjx8MaYwcDADXNzf2pHuSAymBqAPThIOnlLXe' .
		'hsmwgxAEpH5qM047XDeL+pbgEQOnjPZ+YnvxWkVpKumRjCB6oL10u0MZb4ww+mj7sbpP7WV4H+i6' .
		't/qauAGTezgNxX/4iE0H5R9Vjlj6xp6nZk4rNYOf2IaT+b+Q97nW1wo3BMjbncA87NuCed5lToG7' .
		'honcAVrxKjgcr7AORySm2k4hxeKFfqtccjrsTWndE+sidXuZJN+2tAqmjpZihQh5qFhELaQoq8Zd' .
		'd5Ij1x4TwA8aC15sl9evMbwPQk7McsLKd8PFdXjv0p8ulqwEdtT1+ieuBNK20pUA278RfqvFUAGG' .
		'GqC0H+YJEQfN61zVx/ZbRKYQCPP5XBZVtLbiqQsoI7fu4Os83ZGVB0PPmRawyYBrZ/VIqvtxus35' .
		'pnkX8i1URdGIzUUNGkwnUV3gcgQYB/oXtWhMU4H3/+vdj0tEzwlEmKaghlptvXK6NjFE2HOizUPz' .
		'iVTf6asr0vx9kpWnuYEhX/mKHAZhMd/tCNA6JHY6EgeKH/B+A6rYeZR31qwcIIfPqKWBhM95UgQH' .
		'Cm0lEkOhytbGNJfkMLKtDVPrixdP9zfcqgkGmZ5jFgTrbfweVgaFy9YUgV/O0RWfq4jjKMpaVkBo' .
		'RF0cAOd9jucmwLqxJJgLEeU5D9+FnC2VFvNlUwQkI8vHEcmBfDBZDtk9EMmbwatl0QgWZZbkDxJ3' .
		'wmJlsHf4y+bpBMQ95c7w8o+LhI8GzoIUOUUVERtujmidSDkWa4FNLpY0HPGIZcp+t6ooV3uauXDT' .
		'8VL05OyZANzOPWhpWglSveK61+vp8qjhrVxlgjulXfOBNmAdI9X/zuEyT70K3MJJ+ZQC9tDLlREJ' .
		'W4ETICzQp4MsVsDB9TlInTSWMHehC4BqeJGqLcu6Vs33YiDFQjcH/2o22ERR8lWLr2Dnd7m/zI7H' .
		'axOAcAzJRSnsvemdWHw4i6EJJv24yUVseNZpgddRzszdxydHJxBJIL5vUadrfJOT2w3s7MdO5dtD' .
		'Gie3izjBunKIX9Fm2km2VuMV6R2vr4stKkYyZzAcAbjS7HOxiDO5HA0U3QhMHVO3cTv7dGQDEHBF' .
		'my72kJ0qujYTUYeFMsnJ5ZBtl7Y14s2J/rP9qhS006UK7/mgJceMUxnuv/+AZKINiYyEbMDzk24K' .
		'CC5RjuLphFfbC6l/D3usuXTi/8BrA+tMHghJAzcAjkfc0jhoMzsLsxurNBLOb8MKjEc1lH+tCkFj' .
		'2OEumdquaSOBIQR3t/FzU+O6sxSA1EBuDxAWuh/wu483vKQafsAGG/BV7Q/zEhrI7fBW3vkAd48f' .
		'YoOHrlI++si2BuPDCjfNYoIwH4Q8J9EHF2klnCBx9zbIlnKik5B+XCxeDbIWQs/0OtnKiNoPlhpa' .
		'jCsQmsn4Ja19ITdKcdrSl9oXgmIxC1zKAVnbBmeuOTtzt9AZH849FyEH8/1ORJsRm/kaNL11fiib' .
		'OZA2+zxf6VpJqFEld5t2Qgt3boREEzigTsHridTW2PLDTL4oqg5GkoM65WNsS5NsU1wLC1engvuZ' .
		'hRvKz+Ahrwub9sNo9xZvGoYbwXreaJn9L8uusR/V+btaB7W4Lj1QJ7fBsFHkSlFAGjS90EwyW81p' .
		'4vruYwu/iUSImCQA83VHTHNREyF6tw1Mj+E2EKLFMoGJognvp52yH1Sr2rwZVDXaejey17w9XZIH' .
		'QpFrbW5qj2QBtC9vawPBhuUXbdtTjyebFcAq1LgFwZoJ14r6bMONgZShVlu4CQG33hTNeml4UcmH' .
		'F1idgjfhPnRlIZViYBFXpMe1ULEjPkcbXw8qaetO1t06KaIobUg5kxEFLNydRbtBMZ9+pz9NjSa4' .
		'IQUoqzTA0lZzpB7t7FqV6LRkkCOpbtCmHLurR3MKzCKEXdhYwY/DLcWjTa119Yl8a3fxbFY5cJYL' .
		'c1QMp6+AGm9wjZUciCtoyMfjrzUHsOpV9lkMjcmGaNvck5Se9cDIlZ51SuDoDgavEvtUyxUuH56D' .
		'n2MdYIF6bem4TSudUiIqlIZnQfWDHsEO62G+rHIxFpUeONqogsXGVC/v4drOEaOpRQhsZ0gWz34V' .
		'YjxaFkakmtlWr+s+SBw1vkb8r85+ZLE64ZsmRuTABhHZJDOmICq/CVT3WttSBIWqq9Q3RLO2LeRn' .
		'ltJrQLvUkM6EXBHRLrYDtjMGVuCRBAWiKkeT/eu5gwxkZ4LNtuLeICyC2b0wt73NQKoPlqPKbgV8' .
		'3wCnqk19U0X9zNg8N/dby07PWIy5gkLRxpMIPhtaMknbwArMibs0pb1Hjg8ozX9PpLZXGvQCYp+0' .
		'GRUk3e6VsOdnQ9GxdS9f9cjTcy5FiYV3LFxsYwkLL2bqC0WBVd59MVESOKYWICXGCZL39AoAYg5O' .
		'Tv6jWSc7mUzJ/7ttBfZsj5JDPcLyIoDfN8ww8pL6ph8yOHUrDbN2xLYNzrUDITlTGX/cOFSvoEc9' .
		'TdZ/EGbXl0X/GtEkr5ZdVPAetia78BiBF3dSwYOJtos5im66Q5PgO2k5qABBCaRahQrwzRN4eXn/' .
		'75lsQnJH+ujGK84mJebW0emS/dwEUqTnIGbcbditFvPNvNvc7i9kG2MBvX6PQA3Xbmv/eK6Aqls4' .
		'E+o3xrWoTrq6M0bR8eQCIH1Yi9vogjTc+UJWc7y+o2JWX/P9zm3p2Ussj44nPlTt+Z700pAvAicD' .
		'VqDp7ypwWX1dkEHVO7nk2fL0Ym7fVi8xCa8zb5YCsM2J+6pqPddE1nuyk5KYveOuCDEJCbkKgokz' .
		'agXn8+vojBaim/j6qsgf3kHJ/bsjaudly/ocZO69F8shC6NYz5OhHFBCW3vIRRa/iLa8wGgnssri' .
		'521WfS/xqSnuA6fNchgoZvUGlT884uTn+9eOeEM37ycuknmXPno+OL07kYPSuHw44XFMPpt7lCul' .
		'aG6fTheSA/YmVvRwN53bVFw3ynOddrswcX02v3uJZ4hdLkArNs0znZtnMVC2THj8nr/th9bLfsUr' .
		'QeU+xEIGbG7teRa3xO/opmnZR59v3qFEPEcMmAQcxXgeinbHJozdWWn91ONXtIAli0AHLbWn5/qf' .
		'XcL+YIt2LUxN1qtbUV9SwcOyanb3WL5DSLeql2LU9Kom3qWKFLzlqB146Gc5XetjH5eQnadJ/S3d' .
		'Z2uiOiMFLc0KM8HEA2X9bq8JY9kZ0bk4o/F9CoCUyFTE03uboPCog+42kCjq7OFj46SeP9a0csPr' .
		'G7TxCO/nLDnEQeyqudtXM4f5KS7ml/QfPtNwwNtLZHuUMDZ9VGw2kY1klFqbj5WA4B6xioDKL/mA' .
		'48bWvc6IdVPdVe78Wnckx2Ql6NTbuc74pgMIE5VEfruGHjYJ9MQS+PIIbbDsPdCz6azSY3tOfl7j' .
		'pGkPRNqv6sFQX49MvyKNBVIF9U4JVtdBvZfPQa8PbZzTU0GO4fokD9B64gWq/u2HaXyd9r1QVbmk' .
		'nUdPubXdKbKrwKyPaJdMu8ebQKTvaHe8v/vUtw24bXT5bQNaRT9524DXN+CbR8VCD/fL8G/lhUuU' .
		'HTiQw7DYyovRmEfkMQnX5it1og5THcvZ4vPfX+/Nyb3+5PEa9kgcIe0T7f6wSOJbntde/2L/C8m4' .
		'H3LA5AjKdBRT/BNN6/1Nw/UMt7lONhIXMn2agie9MYcRkcyk2G5Dhkd6neRkLyAA91eL1ewz32vj' .
		'd9m4XruyYyPleCPrxBHyg6oWOPk0a21fBSQr5ydX8yAG203oX2pIQjvXKel1+3rmE55+xg00XQyK' .
		'Y73bI+M228NGjjZzym5pVHDgNrp7zZ1CSicd2t8XiGPROi6tK8WlPaGP02Lz1Jl5sVEGj9rsNHPZ' .
		'3/4xzNwdVJrvHEdNlSYb11fgA1MOmESTe1ARGXkkaKEqR1J5sF6Pvb4vZ1IkSNcd7Qkddjo91Hn6' .
		'fFz7ZPScvydrl/GP6veESDWmstaZQk++PU4MOYL3PnL53PR76u780v32Z5LDz8Wyj97boyrdHn1l' .
		'kX6MSoPMR8x5Vk8fWKjm/7MWCGOnCaVbiMXvo7m8tctVFMqy3g85DpOTenP7Fs94Pw0WnVi45e34' .
		'VtDeoRPcNeMH3LkLJ1L3+Z7fVGGPL0B2jNvcOuQbF+aU0LfiZ7IRmMQS0XEPt0NL7G0W7pQd+KUd' .
		'Xs6S2lOvVXGztS8VfoN6NndEhFkavPE/DyI9NHe+IKu/tmyW6no6BNhU5G6Nb5FYO0u99oe9dP2u' .
		'12v/fe70LXbKExzdsc+HdbS10r800aUf+q4OJtfl//wRrXj+P9HxfLXgTMj95HS99MqGtzB5LDD0' .
		'2/PH8Y3SzKd83kcs5zu1gdY7rJfO207OcnpeT4H1Inh5BZ1nri/zzgnPdcbzqeG8W/qqE6QK2J2s' .
		'brvll31HlTsiWw2cjaMAnGt4WiJQEz0tIL8NMrvZzJ08esab5S3lZ5wJ5cednNkCnkI9G3BWfpbc' .
		'/UGb9pNJaDC1Ycel3E21bQtLubamp07txSn32nnmtxYe0/vOrUrSMcTI9k6Xp99DTKvfSHI7Wpw7' .
		'8s7o5MOVc+EmAhVMzq267OTKVc3ImPDhEmSlrB+SmHRy0/jZSLWLoG2XH8dN5d3E1LPKGztPETDl' .
		'6bmQRCT+si8ZvIq0SeBmOjWCdutpCXnwmfypTx268pv/B05/lLgYcQAA'
;

	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<meta charset="utf-8"><style>body{font:15px/1.7 -apple-system,"Apple SD Gothic Neo",sans-serif;max-width:940px;margin:40px auto;padding:0 20px}';
	echo 'code{background:#f4f4f4;padding:1px 5px;border-radius:3px}';
	echo '.ok{color:#0a7a2f}.no{color:#c0392b;font-weight:700}.box{border:1px solid #ddd;border-radius:8px;padding:14px 18px;margin:14px 0}</style>';
	echo '<h2>페이지 160 · 직성의 신 남은 96개 글</h2>';

	if ( 'undo' === $mode ) {
		$bak = get_option( $bak_key );
		if ( ! $bak ) { echo '<p class="no">되돌릴 백업이 없습니다.</p>'; exit; }
		$wpdb->update( $wpdb->posts, array( 'post_content' => $bak ), array( 'ID' => $post_id ) );
		clean_post_cache( $post_id );
		echo '<p class="ok">되돌렸습니다.</p>'; exit;
	}

	$edits_txt = preg_replace( '/\s+/', '', $edits_b64 );
	if ( strlen( $edits_txt ) !== $expect_b64 ) {
		echo '<p class="no">붙여넣기가 잘렸습니다. 담긴 글자 ' . strlen( $edits_txt );
		echo ' / 있어야 할 글자 ' . $expect_b64;
		echo '<br>스니펫을 지우고 파일을 다시 통째로 붙여넣어 주세요.</p>'; exit;
	}
	$packed = base64_decode( $edits_txt, true );
	$edits  = ( false === $packed ) ? null : json_decode( (string) @gzdecode( $packed ), true );
	if ( ! is_array( $edits ) ) { echo '<p class="no">넣을 글을 풀지 못했습니다.</p>'; exit; }

	$content = $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", $post_id ) );
	if ( null === $content ) { echo '<p class="no">페이지 160 을 찾지 못했습니다.</p>'; exit; }

	$old_hash = sha1( $content );
	$from_ok  = ( $old_hash === $expect_from );
	echo '<div class="box">지금 길이 <b>' . strlen( $content ) . '</b> 바이트 · sha1 <code>' . substr( $old_hash, 0, 12 ) . '…</code> ';
	$already = ( $old_hash === $expect_hash );
	if ( $from_ok ) { echo '<span class="ok">(바탕이 맞습니다)</span>'; }
	elseif ( $already ) { echo '<span class="ok">(이미 다 들어간 모습입니다)</span>'; }
	else { echo '<span class="no">(제가 보고 만든 바탕과 다릅니다)</span>'; }
	echo '</div>';
	/* 2026-08-31 · 이미 들어간 상태를 「어긋남」이라고 잘못 말하던 것을 고칩니다.
	   두 번째로 여시면 지금 해시가 「고친 뒤」 해시와 같습니다. 그건 사고가 아니라
	   이미 성공했다는 뜻이므로, 빨간 글씨 대신 그렇게 알려드립니다. */
	if ( ! $from_ok && $already ) {
		echo '<p class="ok"><b>이미 들어가 있습니다.</b> 지금 페이지가 바로 「고친 뒤」의 모습입니다 ';
		echo '&mdash; sha1 <code>' . substr( $expect_hash, 0, 12 ) . '…</code> 가 그 증거입니다.</p>';
		echo '<p>더 하실 일이 없습니다. <b>이 스니펫은 지우셔도 됩니다.</b><br>';
		echo '되돌리시려면 <code>?stella_patch=undo</code> 로 여세요.</p>';
		exit;
	}
	if ( ! $from_ok ) { echo '<p class="no">바탕이 달라 아무것도 바꾸지 않았습니다. 이 화면을 그대로 보여주세요.</p>'; exit; }

	$fixnl = function ( $t ) { return str_replace( array( "\r\n", "\r" ), "\n", $t ); };
	$mkre  = function ( $find ) use ( $fixnl ) {
		$lines = explode( "\n", $fixnl( $find ) );
		foreach ( $lines as $i => $l ) { $lines[ $i ] = preg_quote( $l, '/' ); }
		return '/' . implode( '\r?\n', $lines ) . '/u';
	};

	$updated = $content;
	$fail    = false;
	echo '<h3>자리 찾기</h3><ol>';
	foreach ( $edits as $e ) {
		$re = $mkre( $e['find'] );
		$n  = preg_match_all( $re, $updated );
		echo '<li>' . esc_html( $e['name'] ) . ' — 찾은 수 <b class="' . ( 1 === $n ? 'ok' : 'no' ) . '">' . $n . '</b> / 1';
		if ( 1 !== $n ) { $fail = true; echo ' <span class="no">← 어긋납니다</span>'; }
		echo '</li>';
		if ( 1 === $n ) {
			$rp = $fixnl( $e['rep'] );
			$updated = preg_replace_callback( $re, function ( $m ) use ( $rp ) { return $rp; }, $updated, 1 );
		}
	}
	echo '</ol>';

	$len_ok  = ( ( strlen( $updated ) - strlen( $content ) ) === $expect_delta );
	$hash_ok = ( sha1( $updated ) === $expect_hash );
	echo '<div class="box">고친 뒤 <b>' . strlen( $updated ) . '</b> 바이트 (<b class="' . ( $len_ok ? 'ok' : 'no' ) . '">';
	echo sprintf( '%+d', strlen( $updated ) - strlen( $content ) ) . '</b> · 기대 ' . sprintf( '%+d', $expect_delta ) . ')<br>';
	echo 'sha1 <code>' . substr( sha1( $updated ), 0, 12 ) . '…</code> · 기대 <code>' . substr( $expect_hash, 0, 12 ) . '…</code> ';
	echo $hash_ok ? '<span class="ok">일치</span>' : '<span class="no">불일치</span>';
	echo '<br>앰퍼샌드 두 개 (0이어야) : <b>' . substr_count( $updated, '&&' ) . '</b></div>';
	if ( ! $len_ok || ! $hash_ok ) { $fail = true; }

	if ( $fail ) { echo '<p class="no">어긋난 곳이 있어 아무것도 바꾸지 않았습니다. 이 화면을 그대로 보여주세요.</p>'; exit; }

	if ( 'go' !== $mode ) {
		echo '<p class="ok"><b>확인만 했습니다. 아무것도 바꾸지 않았습니다.</b></p>';
		echo '<p>이대로 넣으시려면 <code>?stella_patch=go</code> 로 여세요.</p>'; exit;
	}

	/* 백업은 처음 한 번만 남깁니다 */
	if ( false === get_option( $bak_key ) ) { update_option( $bak_key, $content, false ); }
	$done = $wpdb->update( $wpdb->posts, array( 'post_content' => $updated ), array( 'ID' => $post_id ) );
	clean_post_cache( $post_id );
	$check = $wpdb->get_var( $wpdb->prepare( "SELECT post_content FROM {$wpdb->posts} WHERE ID = %d", $post_id ) );

	echo '<h3>' . ( sha1( $check ) === $expect_hash ? '<span class="ok">넣었습니다.</span>' : '<span class="no">확인 실패</span>' ) . '</h3>';
	echo '<p>쓰기 결과 <b>' . var_export( $done, true ) . '</b> · 지금 sha1 <code>' . substr( sha1( $check ), 0, 12 ) . '…</code></p>';
	echo '<p>되돌리려면 <code>?stella_patch=undo</code>. <b>이 스니펫은 이제 지우셔도 됩니다.</b></p>';
	exit;
}, 1 );
