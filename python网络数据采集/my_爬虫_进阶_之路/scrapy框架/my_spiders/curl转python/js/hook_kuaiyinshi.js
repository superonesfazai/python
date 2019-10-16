function ab3d7fc(t, s) {
    var e = []
      , i = t.split(":");
    delete i[0];
    var a = [];
    s.split("").forEach(function(t) {
        a.push(t.charCodeAt())
    });
    var n = a.length;
    i.forEach(function(t, s) {
        e.push(parseInt(t) - (255 & a[(s - 1) % n]))
    });
    var o = "";
    return e.forEach(function(t) {
        o += String.fromCharCode(t)
    }),
    o
}