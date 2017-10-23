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
cookies = '_uab_collina=150865866624817348375888; UM_distinctid=15f430e953225c-0995179d5e4ade-31657c00-fa000-15f430e95334e1; JSESSIONID=yS3Zvub-uxYYgD3TCXFcjTKID5-V4XdlYQ-Zmb; h_keys="%u4e0b%u67b6"; ad_prefer="2017/10/22 16:51:13"; ali_ab=218.108.97.82.1508658639482.0; alicnweb=touch_tb_at%3D1508741818652; _umdata=55F3A8BFC9C50DDA5A9113682A1E2B5E3A0F7BE3E5975FD935A9BB9BF81F537B37E54122A90113A9CD43AD3E795C914CDDC048A671562E32B38D9FE9E8361227; cookie1=UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D; cookie2=1d7f072008e7b4382f4de1c39715c413; cookie17=UUplY9Ft9xwldQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; t=39c31685a5f4ebc8b58fb9f880a2c9e9; _tb_token_=e3e6e76303e81; sg=%E4%BA%BA73; __cn_logon__=true; __cn_logon_id__=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA; ali_apache_track="c_ms=1|c_mid=b2b-2242024317|c_lid=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"; ali_apache_tracktmp="c_w_signed=Y"; cn_tmp="Z28mC+GqtZ2INLnWg2jSa2e3CGk80yHNd0P50kQ54H1LE3aoyIbBLInC65atnrS47Cm8qnjwqH8NnvM/L/PL3M3ckvhJcfAbSClVCF95xpX5gZHXUJezyLTpxmALODaSB3xuPedti9ekkGfpeJZ0cNJvXRMPjqzybzbivF89XTkz0ptY+votZaNSBgGskzxVQfB7faJuuUiGOF8xTOCElWTWZT8nkIPz06suCmcy5BvYKfDEY4zEvX+v2pSeyuvJ"; _cn_slid_="eEqvacXW%2FQ"; tbsnid=gmYiKIGv7Mf%2B7J6E%2B1Zn89pjrLzx15zALQxPUPhDotY6sOlEpJKl9g%3D%3D; LoginUmid="uoPP%2FwcICEU%2BvCOLbNBazma7%2F95UnztUcfOUw5NS2ZHmkdAiNY8Cqw%3D%3D"; userID="0eSDLTAmofsL67RXnSBAFwkwpsuwsEP%2BAU5n2L44pVU6sOlEpJKl9g%3D%3D"; last_mid=b2b-2242024317; unb=2242024317; __last_loginid__="%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"; login="kFeyVBJLQQI%3D"; _csrf_token=1508743237918; cna=djtzEjGArAoCAdpsYVInKSbN; CNZZDATA1253659577=1148026705-1508656403-null%7C1508742803; userIDNum=JG1hTHTu5MzRqUsxcJimIg%3D%3D; _nk_=NhOVmlLYn22Ov9IJnn3S0Tqw6USkkqX2; _is_show_loginId_change_block_=b2b-2242024317_false; _show_force_unbind_div_=b2b-2242024317_false; _show_sys_unbind_div_=b2b-2242024317_false; _show_user_unbind_div_=b2b-2242024317_false; _tmp_ck_0="HYP1z9lZIkgNFcWPRAlCNdNqD96zipOUNBWMlwWtrc1m075Ap6h2JgvHpx%2BqvEw4SuxRSoXXVMBZJz4wPEJt7GlbDClwiHq4bxpcaBxdDIfV3iYR2Y3l4rDH5rAMutV%2BA0qINBMfSTKKjSJw2QmRiYlGWFDLlkpPf2ol2y8nyJ3bg4635veAsyofRs40D2up7Kzo7n%2FpQco3UNFkYhKkbUXMcKxhyjk1GSRltfPJpvsrQNHdEMjHKAd4CY3%2Byfc1DbhuDRcWdl%2BztGo4tfT6x47Bc%2BVIkVFvb0lVhEKn0e0oB8JZaJi84mWsmL%2FSg5mVjHcuP2%2FRmvGI7zLuHtORdZPuXufa75gEiB%2Frgh3BkhXwcHNuGZogO7xqUNCrulcfNcFIAUqn2%2BIiCPnLruyWpooyJi%2B0G0OdMRXIdFAue%2By8ERTdmY7Q1gJTLHC5NeU49vX7NAOy01gKqEcUi3qfYl2vuBBpIgzdBLT4K1auf5vEioM2kYlwq0aZ7N2VLPW8dYjCP7%2Bm1CvUTSHHExF%2FhRsUoydUjQwa"; __rn_alert__=false; isg=Al5e5W8Qi2R8Ht-GGJxz3EA5r_JgtyPmku6LPQjnyKGcK_4Fca9yqYTJVQHc'
pprint(stringToDict(cookies))