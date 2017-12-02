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
cookies = 'JSESSIONID=ZYCZ8ng-wkRY53gxcFmkihGPu6-JNyndXQ-Ob8u; cookie1=UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D; cookie2=1732fbb870d2dab49ac893b0c1a6ba3f; cookie17=UUplY9Ft9xwldQ%3D%3D; t=96cda190d48f880e4cc98760c1cde472; _tb_token_=f30665e157eed; sg=%E4%BA%BA73; __cn_logon__=true; __cn_logon_id__=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA; ali_apache_track="c_ms=1|c_mid=b2b-2242024317|c_lid=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"; ali_apache_tracktmp="c_w_signed=Y"; cn_tmp="Z28mC+GqtZ2INLnWg2jSa2e3CGk80yHNd0P50kQ54H1LE3aoyIbBLInC65atnrS47Cm8qnjwqH8NnvM/L/PL3M3ckvhJcfAbGAY6MVV2T8l8KAQxtbobshVPfHcZQPVnxi755fgm9veLNbyiHRiMpC0OuxnStL75pHIOatmbV7+U2lqKO9u/9SQbvQkVQzleLqsqDEOf7uQqVjUJGLdt2Yk+wEjg4tKdxCXw5SBygVDIG0DmbNwm5MfMACrkrtBB"; _cn_slid_="eEqvacXW%2FQ"; tbsnid=ZObL5KTM9ConxWbImp76NI4TuezGiFVSq5atTF%2Fpglo6sOlEpJKl9g%3D%3D; LoginUmid="uoPP%2FwcICEU%2BvCOLbNBazma7%2F95UnztUcfOUw5NS2ZHmkdAiNY8Cqw%3D%3D"; userID="0eSDLTAmofsL67RXnSBAFwkwpsuwsEP%2BAU5n2L44pVU6sOlEpJKl9g%3D%3D"; last_mid=b2b-2242024317; unb=2242024317; __last_loginid__="%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"; login="kFeyVBJLQQI%3D"; _csrf_token=1507626697806; landingPage=home; cna=s3xjEuAFcwECAXHXsaeMKJmb; UM_distinctid=15f058dcbb1afe-03acd53cb45583-31657c00-fa000-15f058dcbb278d; CNZZDATA1253645563=254815601-1507626649-%7C1507626649; _is_show_loginId_change_block_=b2b-2242024317_false; _show_force_unbind_div_=b2b-2242024317_false; _show_sys_unbind_div_=b2b-2242024317_false; _show_user_unbind_div_=b2b-2242024317_false; userIDNum=JG1hTHTu5MzRqUsxcJimIg%3D%3D; _nk_=NhOVmlLYn22Ov9IJnn3S0Tqw6USkkqX2; __rn_alert__=false; ali_ab=113.215.177.167.1507626703422.5; alicnweb=lastlogonid%3D%25E6%2588%2591%25E6%2598%25AF%25E5%25B7%25A5%25E5%258F%25B79527%25E6%259C%25AC%25E4%25BA%25BA%7Ctouch_tb_at%3D1507626705197%7Cshow_inter_tips%3Dfalse; isg=Alpa8UCt14kPVVslGpGemkCgqwa8I98adgIPSWTTWO241_sRTBoNdQvl0ZQx; _tmp_ck_0=Us6kfQ%2FxEOPCqgvcZeNWa3K6nyiIMAo%2BPVWMNjgnR%2BTxtgPPK6WZ66vetBTpUneZNViRa676duSByqd%2BCCJcInLV3fs3mdNs11S2WMchziPVHxdnIi4neBPDT%2B73NL%2BmCgCaeshCwv0gp5RRzizCUUIbvLZUlDKL24i%2B29JbPl4vMdSnHb9k%2FgOV5TP3JVx61S4vfJ43waxuLVy1m9XwDpwstnwEEpxOcEqyRi61FSfGUva%2FhtsMWvhkQk5Mms12vlUkNumcfktaIjimt5slqGRbT2VhNWqClbDQiBXHCfJrkfI%2F5jdF89AEJKcsKHsBC1PTrBLGPP7me5X%2BTExUrTD3zUMSpWNbkSjJFOaDjFJ14%2BPAic47fl2sfkbUByazYXqRK6s6ZnHiE1C5EZXRbjP6obiFUmHsv94e8A721liZfnznUF%2Bc2pkG%2Fy0l41RKdOZrKdB2Snd7hmpXsfqaZDRIbwSeHFA0%2FbFPZjbFRpm3FJIPBK6n9X2jZOK3TY1m66BH%2B9ktjWP4bkNK2oR3FGPYo7KceP7rPbjWBbAmIUg%3D'
pprint(stringToDict(cookies))