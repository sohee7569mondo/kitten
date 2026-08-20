import math

# ---------- 기본 도구 ----------
def jd(y,m,d,h=0,mi=0,s=0):
    if m<=2: y-=1; m+=12
    A=y//100; B=2-A+A//4
    return (math.floor(365.25*(y+4716))+math.floor(30.6001*(m+1))
            +d+B-1524.5+(h+mi/60+s/3600)/24)

def sun_lon(jdv):
    """겉보기 황경(도). 정밀도 ~0.01도"""
    T=(jdv-2451545.0)/36525.0
    L0=(280.46646+36000.76983*T+0.0003032*T*T)%360
    M =(357.52911+35999.05029*T-0.0001537*T*T)%360
    Mr=math.radians(M)
    C =((1.914602-0.004817*T-0.000014*T*T)*math.sin(Mr)
        +(0.019993-0.000101*T)*math.sin(2*Mr)+0.000289*math.sin(3*Mr))
    true=L0+C
    om=125.04-1934.136*T
    return (true-0.00569-0.00478*math.sin(math.radians(om)))%360

def find_term(deg, y, mguess):
    """태양 황경이 deg 가 되는 순간(UT JD)"""
    lo=jd(y,mguess,1)-20; hi=lo+45
    def f(t):
        d=(sun_lon(t)-deg)%360
        return d-360 if d>180 else d
    for _ in range(80):
        mid=(lo+hi)/2
        if f(lo)*f(mid)<=0: hi=mid
        else: lo=mid
    return (lo+hi)/2

def jd2kst(j):
    j=j+9/24+0.5
    Z=math.floor(j); F=j-Z
    A=Z
    if Z>=2299161:
        a=math.floor((Z-1867216.25)/36524.25); A=Z+1+a-a//4
    B=A+1524; C=math.floor((B-122.1)/365.25); D=math.floor(365.25*C)
    E=math.floor((B-D)/30.6001)
    day=B-D-math.floor(30.6001*E)+F
    mo=E-1 if E<14 else E-13
    yr=C-4716 if mo>2 else C-4715
    di=int(day); fr=(day-di)*24
    return yr,mo,di,int(fr),int((fr-int(fr))*60)

GAN='갑을병정무기경신임계'; JI='자축인묘진사미신유술해'
GAN_L=['갑','을','병','정','무','기','경','신','임','계']
JI_L =['자','축','인','묘','진','사','오','미','신','유','술','해']
GAN_H=['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
JI_H =['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
GAN_EL=['목','목','화','화','토','토','금','금','수','수']
JI_EL =['수','토','목','목','토','화','화','토','금','금','토','수']

BIRTH=dict(y=1975,m=1,d=23,h=9,mi=35,lon=126.978,lat=37.4665)  # 서울 독산동

# ---------- 진태양시 ----------
jd_ut = jd(BIRTH['y'],BIRTH['m'],BIRTH['d'],BIRTH['h']-9,BIRTH['mi'])
T=(jd_ut-2451545.0)/36525.0
# 균시차
L0=(280.46646+36000.76983*T)%360
M =(357.52911+35999.05029*T)%360
e =0.016708634-0.000042037*T
eps=23.439291-0.0130042*T
yv=math.tan(math.radians(eps/2))**2
Mr=math.radians(M); L0r=math.radians(L0)
E=yv*math.sin(2*L0r)-2*e*math.sin(Mr)+4*e*yv*math.sin(Mr)*math.cos(2*L0r)-.5*yv*yv*math.sin(4*L0r)-1.25*e*e*math.sin(2*Mr)
eot=math.degrees(E)*4     # 분
lon_corr=(BIRTH['lon']-135.0)*4
print('=== 진태양시 ===')
print(' 시계시각        09:35')
print(' 경도 보정      %+.1f분  (서울 %.3f°E, 표준자오선 135°E)'%(lon_corr,BIRTH['lon']))
print(' 균시차         %+.1f분'%eot)
tot=9*60+35+lon_corr+eot
print(' 진태양시        %02d:%02d'%(int(tot//60),int(round(tot%60))))
print(' 경도만 보정 시  %02d:%02d'%(int((9*60+35+lon_corr)//60),int(round((9*60+35+lon_corr)%60))))

# ---------- 사주 ----------
sohan = find_term(285,1975,1)   # 소한
ipchun= find_term(315,1975,2)   # 입춘
print('\n=== 절기 (KST) ===')
print(' 소한  %d-%02d-%02d %02d:%02d'%jd2kst(sohan))
print(' 입춘  %d-%02d-%02d %02d:%02d'%jd2kst(ipchun))
print(' 출생은 소한 이후 · 입춘 이전  →  연주는 1974년 간지, 월주는 축월(丑月)')

# 일주: 1900-01-01 = 갑술일(甲戌) 기준
base=jd(1900,1,1); n=int(jd(1975,1,23)-base)
dg=(10+n)%10; dz=(10+n)%12   # 갑술 = gan0, ji10
dg=(0+n)%10; dz=(10+n)%12
print('\n=== 사주 원국 ===')
yg,yz=0,2      # 갑인
mg,mz=3,1      # 정축
print(' 연주 %s%s (%s%s)'%(GAN_H[yg],JI_H[yz],GAN_L[yg],JI_L[yz]))
print(' 월주 %s%s (%s%s)'%(GAN_H[mg],JI_H[mz],GAN_L[mg],JI_L[mz]))
print(' 일주 %s%s (%s%s)'%(GAN_H[dg],JI_H[dz],GAN_L[dg],JI_L[dz]))

for label,hz in (('사시(09-11) 시계시 기준',5),('진시(07-09) 진태양시 기준',4)):
    hg=(dg%5*2+hz)%10
    print(' 시주 %s%s  ← %s'%(GAN_H[hg],JI_H[hz],label))

# ---------- 오행 ----------
print('\n=== 오행 비율 ===')
for label,hg,hz in (('시주 己巳(사시)',5,5),('시주 戊辰(진시)',4,4)):
    cnt={e:0 for e in '목화토금수'}
    for g in (yg,mg,dg,hg): cnt[GAN_EL[g]]+=1
    for z in (yz,mz,dz,hz): cnt[JI_EL[z]]+=1
    tot8=sum(cnt.values())
    print(' '+label+' : '+'  '.join('%s %d (%.1f%%)'%(e,cnt[e],cnt[e]/tot8*100) for e in '목화토금수'))

# ---------- 대운 ----------
print('\n=== 대운 (연간 甲=양, 여성 → 역행) ===')
days=jd(1975,1,23,0,35)-sohan     # 역행: 직전 절기까지 거슬러
print(' 소한부터 출생까지 %.2f일  →  대운수 %.2f세'%(days,days/3))
start=days/3
for i in range(1,8):
    g=(mg-i)%10; z=(mz-i)%12
    a0=start+(i-1)*10
    print('  %5.1f~%5.1f세 (%d~%d)  %s%s'%(a0,a0+10,1975+int(a0),1975+int(a0)+10,GAN_H[g],JI_H[z]))

# ---------- 상승궁 / MC ----------
print('\n=== 점성 ===')
d0=jd_ut-2451545.0
gmst=(280.46061837+360.98564736629*d0)%360
lst=(gmst+BIRTH['lon'])%360
epsr=math.radians(eps); phir=math.radians(BIRTH['lat']); ramc=math.radians(lst)
mc=math.degrees(math.atan2(math.sin(ramc),math.cos(ramc)*math.cos(epsr)))%360
asc=math.degrees(math.atan2(math.cos(ramc),-(math.sin(epsr)*math.tan(phir)+math.cos(epsr)*math.sin(ramc))))%360
SIGN='양자리 황소자리 쌍둥이자리 게자리 사자자리 처녀자리 천칭자리 전갈자리 사수자리 염소자리 물병자리 물고기자리'.split()
def s(x): return '%s %.1f도'%(SIGN[int(x//30)],x%30)
print(' 태양      ',s(sun_lon(jd_ut)))
print(' 상승궁 ASC',s(asc))
print(' 천정 MC   ',s(mc))
