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
cookies = 'UM_distinctid=15f430e953225c-0995179d5e4ade-31657c00-fa000-15f430e95334e1; h_keys="%u4e0b%u67b6"; ad_prefer="2017/10/22 16:51:13"; JSESSIONID=8L785jNv1-qaYYibHFnzpoVLEm15-GLUk7ZQ-qSN1; ali_beacon_id=218.108.99.214.1508985316510.054017.6; ctoken=99MN4AheqYjZr3Vb6NQlzealot; _m_h5_tk=0e51b5a97674a972ad9f80bd4785232e_1508997014904; _m_h5_tk_enc=7ceabe20e6ac56eb3545b452842417c0; webp=1; cna=djtzEjGArAoCAdpsYVInKSbN; ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJzZWNyZXQiOiI1WGt2ZXNDemN3U2dDVGVwbEh4anZKdzEiLCJrb2EtZmxhc2giOnt9LCJfZXhwaXJlIjoxNTA5MDg0ODUzOTU1LCJfbWF4QWdlIjo4NjQwMDAwMH0=; cookie1=UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D; cookie2=77360468af87aa9138fe41cba09c84e4; cookie17=UUplY9Ft9xwldQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; t=39c31685a5f4ebc8b58fb9f880a2c9e9; _tb_token_=f7737e987379e; sg=%E4%BA%BA73; __cn_logon__=true; __cn_logon_id__=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA; ali_apache_track="c_ms=1|c_mid=b2b-2242024317|c_lid=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"; ali_apache_tracktmp="c_w_signed=Y"; cn_tmp="Z28mC+GqtZ2INLnWg2jSa2e3CGk80yHNd0P50kQ54H1LE3aoyIbBLInC65atnrS47Cm8qnjwqH8NnvM/L/PL3M3ckvhJcfAbqQEjtLsR4MD4NzvybSk5RF20QeZeZ8/HPhr46eUyqq8iFuNKyVsEYhhz+MUG5LC+CLx48OMsbVtJTatTi93lC/jd1KADpGrSKuJ2RgrOffNCI4UrmXZKBwHQuQ3HLdfKZ6dtOmUQOmAETilo2Ea5cJbl6LPYfM5N"; _cn_slid_="eEqvacXW%2FQ"; tbsnid=kFrw4lmAbj800Xd1052VYtsCW2aRp9L8WtUYmSNimzA6sOlEpJKl9g%3D%3D; LoginUmid="uoPP%2FwcICEU%2BvCOLbNBazma7%2F95UnztUcfOUw5NS2ZHmkdAiNY8Cqw%3D%3D"; userID="0eSDLTAmofsL67RXnSBAFwkwpsuwsEP%2BAU5n2L44pVU6sOlEpJKl9g%3D%3D"; last_mid=b2b-2242024317; unb=2242024317; __last_loginid__="%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"; login="kFeyVBJLQQI%3D"; _csrf_token=1508998515272; CNZZDATA1261011362=1725144690-1508655806-%7C1508996054; userIDNum=JG1hTHTu5MzRqUsxcJimIg%3D%3D; _nk_=NhOVmlLYn22Ov9IJnn3S0Tqw6USkkqX2; ali_ab=218.108.97.82.1508658639482.0; _is_show_loginId_change_block_=b2b-2242024317_false; _show_force_unbind_div_=b2b-2242024317_false; _show_sys_unbind_div_=b2b-2242024317_false; _show_user_unbind_div_=b2b-2242024317_false; __rn_alert__=false; isg=Ag0NWJBlaB1GuMwrn4kwmQ9UHC9HQkDR7RP40E-SSaQTRi34FzpRjFvUxuzb; _tmp_ck_0="Fl9S9nXmCJ%2FIXf02OVzIyLTOl1knmUQmrPEoB2MIVkysNKqev76qijH6ggJctfvKoc4bWK4TzLQzbaN27BFxsELPzbdPyT04XLvtydk8wCdEhKiZCWcWoU%2FyvRxG4%2FqAv7jgOHOtKz5fDc%2FL1hGdIQ9d43KNtZj5IleVOhjiPIcUPMeO%2FbO4%2FbqRXVBmvsadypZ0nF4Npv%2BZgwi1ZnzuttvuVFdl1rrUv%2FLEguFNP87cvdjQ0o6EQdfAdZlsXZ1O%2FDS2xBRpegUaAOROOn8dK7fCtL%2FbYQDlIxoUPLeVM1AhV6O6IurIQH3uSnUekntpPjaXMc2%2FejX7m4pSsQ9NfuVNhH1iHWLMkb57%2BywxAH96RlrGq4OB7aiMMykIsQDNV2RhFNU%2FI42r4f1YeDfuXxLG9V%2B8zb8vhsnGF0CwfePgomepTw4lQb2rvC%2BUym3Vf9GMvOtnTYHZ3H8G67vxFrKApdw9KrH31ctrDCJb3vM455PDN6RugF2lfeCeCANeyEGfP89jEtl5PaqBrpC2UfO41nL2iAebkOkipQP17o5ZPxXj2m9%2FCg%3D%3D"; alicnweb=touch_tb_at%3D1508996379118%7Clastlogonid%3D%25E6%2588%2591%25E6%2598%25AF%25E5%25B7%25A5%25E5%258F%25B79527%25E6%259C%25AC%25E4%25BA%25BA%7Cshow_inter_tips%3Dfalse'
pprint(stringToDict(cookies))