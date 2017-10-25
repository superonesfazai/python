# coding:utf-8

'''
@author = super_fazai
@File    : cookies_to_dict.py
@Time    : 2017/9/24 13:55
@connect : superonesfazai@gmail.com
'''

from pprint import pprint

def stringToDict(cookies):
    itemDict = {}
    items = cookies.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')  # 记得去除空格
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict


# cookies = 'SUV=1505446925567125; SMYUV=1505446925568464; UM_distinctid=15e83a1210450f-0767352fad6394-31637e01-fa000-15e83a12105261; ABTEST=0|1506166032|v1; IPLOC=CN1100; SUID=F28867D3232C940A0000000059C64510; SUID=0270820E1F13940A0000000059C64510; weixinIndexVisited=1; SNUID=82F916A3717529A8EF7CE70471D86921; JSESSIONID=aaauZkEn6Jewl6APb-y6v; sct=13'
cookies = '_med=dw:1280&dh:800&pw:2560&ph:1600&ist:0; miid=5163267521302899128; UM_distinctid=15f4454692b518-0555f1e7dd4c7e-31657c00-fa000-15f4454692c301; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; mt=np=&ci=45_1; tg=0; cookie2=77360468af87aa9138fe41cba09c84e4; v=0; _m_user_unitinfo_=unit|unshyun; _m_unitapi_v_=1508566261407; tk_trace=oTRxOWSBNwn9dPy4KVJVbutfzK5InlkjwbWpxHegXyGxPdWTLVRjn23RuZzZtB1ZgD6Khe0jl%2BAoo68rryovRBE2Yp933GccTPwH%2FTbWVnqEfudSt0ozZPG%2BkA1iKeVv2L5C1tkul3c1pEAfoOzBoBsNsJyTiWtijRcgaFl%2Bt7JBsrd0YGyuPHsVkeAd5WwiCJZELXrV25ia3NSCCQoIRmoJcswnfVxFDZBU4yg42Wi%2B%2B227Cm3SJ38qWJwfE58EYj5sCqIiLyHliYlQ01CLLl6PZ25m2ii9zafRBPfSCEB1U9B3h11vSg89gGmhxMMPOu1jw2cje1%2BZM3Z0QviQAow%3D; ctoken=WqhCFrPazVHsaXEg4Ehiiceland; tkmb=e=fRr_ET7d3Tx76dzr1za1jmU2OsBpQQtBU6BwbTrggWiEcBupLLJRFy_IAR7ok-npGtZYij25ERjBnG-T_Ndt1BakgVc6i1DDLo0nGD27QSPyaVHJGv0cvWSFatuabcoup7-KiODD93LlC0BlL2LLY3O4cSMzCSAFUD-4jMAaherx5SCReQ1jJwo5h4XpPi-KRerZkbgJIVQgpPIJRlJds_pbdVeC1AMtC9mw9d7zBv1T3slBGJ2d9MaRzg-l95YfaYNdMH-gY5mbsmX3Tm38gPzMtjdtihtuEh5lfNoHrQM4a3ITlE1jqKm2f1NjvLH3TJ2BLCpTJE8&iv=0&et=1508852150; linezing_session=YxTaEiFp5PgcCDsDUpv72smj_15089162078677dhg_4; _tb_token_=f7737e987379e; l=Alxc7z0vy02Xr2I-uw3Bx6KirHEOlgD/; _m_h5_tk=ba40d8148652aab780cd0a4676b7de78_1508939525308; _m_h5_tk_enc=657e3a29d2ed7960fc33a8f5eee71311; munb=2242024317; uc3=sg2=WqJ5CclAaAIRL%2BjSIx%2FSzyVuMbp8JSBthJSylPIhcsc%3D&nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dBzLEyGigU4e7%2Bk94%3D&lg2=W5iHLLyFOGW7aA%3D%3D; uc1=cookie14=UoTcBzbGCJIJUw%3D%3D&cookie21=VT5L2FSpdeCsOSyjpv%2FIyw%3D%3D&cookie15=UIHiLt3xD8xYTw%3D%3D; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; uss=WqJ%2BWRrAVClLpjGnzo4H1pA5ModQ2m%2BdZWZS3Had%2Blo508500XLOlKESsQ%3D%3D; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; sg=%E4%BA%BA73; cookie1=UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D; unb=2242024317; skt=46e576256f2dba98; t=39c31685a5f4ebc8b58fb9f880a2c9e9; _cc_=W5iHLLyFfA%3D%3D; _nk_=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; _l_g_=Ug%3D%3D; cookie17=UUplY9Ft9xwldQ%3D%3D; cna=djtzEjGArAoCAdpsYVInKSbN; isg=ArGxbJIcTLCyS-C4Z7Kwy0ciwDuLNiWD6R-UZJPGpHiXutEM2O414F_Qrngn'
pprint(stringToDict(cookies))