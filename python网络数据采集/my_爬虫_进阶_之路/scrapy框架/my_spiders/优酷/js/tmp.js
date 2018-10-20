function get_sign(){
    var a = (new Date).getTime();
    var o = '24679788';
    var _data = '{"device": "H5", "layout_ver": "100000", "system_info": "{\\"device\\":\\"H5\\",\\"pid\\":\\"0d7c3ff41d42fcd9\\",\\"guid\\":\\"1533803300785Vp7\\",\\"utdid\\":\\"1533803300785Vp7\\",\\"ver\\":\\"1.0.0.0\\",\\"userAgent\\":\\"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36\\"}", "video_id": "XMzEyOTc2NTc0NA"}';
    var sign = u(r.token + "&" + a + "&" + o + "&" + _data);
}

// sign: f
// f = u(r.token + "&" + a + "&" + o + "&" + n.data)
// "a1d71ef5b54f43bb7fafc6e41f70f0b5"
// r.token = _m_h5_tk	_前面的值