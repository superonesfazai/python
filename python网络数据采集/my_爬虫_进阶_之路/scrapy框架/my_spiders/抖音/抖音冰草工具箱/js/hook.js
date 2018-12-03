function generateStr(str) {
    var hash = md5(str);

    return hash
}

function generateRandom() {
    c = Math.random().toString(10).substring(2);
    return c
}

function get_r(scope_cursor, scope_count) {
    url = "dbTest?cursor=" + scope_cursor + "&count=" + scope_count;
    var r = generateRandom().toString();
    // var parseTempStr = url + '@&^' + r;
    // var e = generateStr(parseTempStr);

    return r
}