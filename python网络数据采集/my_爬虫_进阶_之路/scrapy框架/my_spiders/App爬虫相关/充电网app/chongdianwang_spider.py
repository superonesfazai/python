# coding:utf-8

'''
@author = super_fazai
@File    : chongdianwang_spider.py
@connect : superonesfazai@gmail.com
'''

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

async def _get_someplace_one_page_info(latitude:float, longitude:float, page_num:int) -> list:
    '''
    获取某坐标单页的充电桩信息
    :param latitude:
    :param longitude:
    :param page_num:
    :return:
    '''
    async def _get_headers() -> dict:
        return {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'br, gzip, deflate',
            # 'TOKEN': '30e76e4f7481b829e1ab2df4bba5403737da16ae',
            'timestamp': _t,    # '1546827077000'
            'Content-Type': 'application/x-www-form-urlencoded',
            'appId': '20171010',
            'DEVICE': 'ver=3.7.5.6&os_version=11.0&device_type=iPhone7,1&carrier=%E4%B8%AD%E5%9B%BD%E8%81%94%E9%80%9A&client=ios&pushtype=0&lan=ch&device_id=c0d9b7153be8ce96c329061d79ef9f6e&cityCode=&lat=30.190540&lng=120.201116&cityName=',
            'User-Agent': 'EVClub/3.7.5 (iPhone; iOS 11.0; Scale/3.00)',
            # 'signature': 'af767d7d87c0b33a9d29ecbd85011453',
            'Host': 'app-api.chargerlink.com',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'Accept': '*/*',
            # 'Content-Length': '96',
        }

    # cookies = {
    #     'cl_ssid': '30e76e4f7481b829e1ab2df4bba5403737da16ae',
    # }
    _t = str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))
    headers = await _get_headers()
    data = {
      'latitude': str(latitude),
      'longitude': str(longitude),
      'page': str(page_num),        # 1, ...
      'sort': '1',
      'userFilter[codeBitList]': '149'
    }
    url = 'https://app-api.chargerlink.com/spot/searchSpot'
    body = Requests.get_url_body(
        method='post',
        url=url,
        headers=headers,
        cookies=None,
        data=data,
        ip_pool_type=tri_ip_pool)
    data = json_2_dict(json_str=body, default_res={}).get('data', [])
    # print(data)
    # TODO 地址, 经纬度是加密的
    # 逆向后(search:codeBitList)得知其为Tea.decryptByDefaultKey(arrayOfByte)解码
    '''
    import com.mdroid.xxtea.Tea;
    
    public class f
      extends w<String>
    {
      private String a(String paramString)
      {
        byte[] arrayOfByte = Base64.decode(paramString, 0);
        if ((arrayOfByte == null) || (arrayOfByte.length == 0)) {}
        do
        {
          return paramString;
          arrayOfByte = Tea.decryptByDefaultKey(arrayOfByte);
        } while ((arrayOfByte == null) || (arrayOfByte.length == 0));
        return new String(arrayOfByte);
      }
      
      public String a(a parama)
        throws IOException
      {
        if (parama.f() == b.i)
        {
          parama.j();
          parama = null;
        }
        String str;
        do
        {
          return parama;
          str = parama.h();
          parama = str;
        } while (TextUtils.isEmpty(str));
        try
        {
          parama = a(str);
          return parama;
        }
        catch (Exception parama) {}
        return str;
      }
      
      public void a(c paramc, String paramString)
        throws IOException
      {
        if (paramString == null)
        {
          paramc.f();
          return;
        }
        paramc.b(paramString);
      }
    }
    '''
    pprint(data)
    for item in data:
        print(item['address'])
        address_bytes = b64decode_plus(item['address'].encode())
        # QUvZd5mSBl+PxFo8LFfHOdVRBxbdL6CC0JrFtY/DlOHZQuLhrnRzdUvdq4ZHTCWuNTWCm5/K/pQ8jw8FaX7tPW1QR7ik7FqvDrKIPPEg4n7PjQogcabkyA4cBKk=
        # print(address_bytes.decode())

    return data

loop = get_event_loop()
latitude = 30.19053993953403
longitude = 120.2011157401635
res = loop.run_until_complete(_get_someplace_one_page_info(latitude=latitude, longitude=longitude, page_num=1))

