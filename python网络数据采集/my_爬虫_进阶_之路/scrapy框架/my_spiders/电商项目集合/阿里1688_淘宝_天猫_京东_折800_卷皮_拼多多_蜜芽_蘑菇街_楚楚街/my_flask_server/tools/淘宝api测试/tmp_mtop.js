define("mui/mtop/index", ["mui/mtb-windvane/", "mui/babel-polyfill/"], function(e, t, n) {
    "use strict";
    var o = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function(e) {
        return typeof e
    } : function(e) {
        return e && typeof Symbol === "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
    };
    e("mui/mtb-windvane/");
    e("mui/babel-polyfill/");
    typeof window === "undefined" && (window = {
        ctrl: {},
        lib: {}
    });
    !window.ctrl && (window.ctrl = {});
    !window.lib && (window.lib = {});
    ! function(e, t) {
        function n() {
            var e = {},
                t = new g(function(t, n) {
                    e.resolve = t, e.reject = n
                });
            return e.promise = t, e
        }

        function i(e, t) {
            for (var n in t) {
                void 0 === e[n] && (e[n] = t[n])
            }
            return e
        }

        function r(e) {
            var t = document.getElementsByTagName("head")[0] || document.getElementsByTagName("body")[0] || document.firstElementChild || document;
            t.appendChild(e)
        }

        function s(e) {
            var t = [];
            for (var n in e) {
                e[n] && t.push(n + "=" + encodeURIComponent(e[n]))
            }
            return t.join("&")
        }

        function a(e) {
            return e.substring(e.lastIndexOf(".", e.lastIndexOf(".") - 1) + 1)
        }

        function p(e) {
            function t(e, t) {
                return e << t | e >>> 32 - t
            }

            function n(e, t) {
                var n, o, i, r, s;
                return i = 2147483648 & e, r = 2147483648 & t, n = 1073741824 & e, o = 1073741824 & t, s = (1073741823 & e) + (1073741823 & t), n & o ? 2147483648 ^ s ^ i ^ r : n | o ? 1073741824 & s ? 3221225472 ^ s ^ i ^ r : 1073741824 ^ s ^ i ^ r : s ^ i ^ r
            }

            function o(e, t, n) {
                return e & t | ~e & n
            }

            function i(e, t, n) {
                return e & n | t & ~n
            }

            function r(e, t, n) {
                return e ^ t ^ n
            }

            function s(e, t, n) {
                return t ^ (e | ~n)
            }

            function a(e, i, r, s, a, p, u) {
                return e = n(e, n(n(o(i, r, s), a), u)), n(t(e, p), i)
            }

            function p(e, o, r, s, a, p, u) {
                return e = n(e, n(n(i(o, r, s), a), u)), n(t(e, p), o)
            }

            function u(e, o, i, s, a, p, u) {
                return e = n(e, n(n(r(o, i, s), a), u)), n(t(e, p), o)
            }

            function c(e, o, i, r, a, p, u) {
                return e = n(e, n(n(s(o, i, r), a), u)), n(t(e, p), o)
            }

            function d(e) {
                for (var t, n = e.length, o = n + 8, i = (o - o % 64) / 64, r = 16 * (i + 1), s = new Array(r - 1), a = 0, p = 0; n > p;) {
                    t = (p - p % 4) / 4, a = p % 4 * 8, s[t] = s[t] | e.charCodeAt(p) << a, p++
                }
                return t = (p - p % 4) / 4, a = p % 4 * 8, s[t] = s[t] | 128 << a, s[r - 2] = n << 3, s[r - 1] = n >>> 29, s
            }

            function l(e) {
                var t, n, o = "",
                    i = "";
                for (n = 0; 3 >= n; n++) {
                    t = e >>> 8 * n & 255, i = "0" + t.toString(16), o += i.substr(i.length - 2, 2)
                }
                return o
            }

            function f(e) {
                e = e.replace(/\r\n/g, "\n");
                for (var t = "", n = 0; n < e.length; n++) {
                    var o = e.charCodeAt(n);
                    128 > o ? t += String.fromCharCode(o) : o > 127 && 2048 > o ? (t += String.fromCharCode(o >> 6 | 192), t += String.fromCharCode(63 & o | 128)) : (t += String.fromCharCode(o >> 12 | 224), t += String.fromCharCode(o >> 6 & 63 | 128), t += String.fromCharCode(63 & o | 128))
                }
                return t
            }
            var m, h, g, v, _, y, R, w, E, S = [],
                O = 7,
                b = 12,
                T = 17,
                q = 22,
                A = 5,
                x = 9,
                C = 14,
                N = 20,
                J = 4,
                k = 11,
                L = 16,
                D = 23,
                I = 6,
                P = 10,
                F = 15,
                j = 21;
            for (e = f(e), S = d(e), y = 1732584193, R = 4023233417, w = 2562383102, E = 271733878, m = 0; m < S.length; m += 16) {
                h = y, g = R, v = w, _ = E, y = a(y, R, w, E, S[m + 0], O, 3614090360), E = a(E, y, R, w, S[m + 1], b, 3905402710), w = a(w, E, y, R, S[m + 2], T, 606105819), R = a(R, w, E, y, S[m + 3], q, 3250441966), y = a(y, R, w, E, S[m + 4], O, 4118548399), E = a(E, y, R, w, S[m + 5], b, 1200080426), w = a(w, E, y, R, S[m + 6], T, 2821735955), R = a(R, w, E, y, S[m + 7], q, 4249261313), y = a(y, R, w, E, S[m + 8], O, 1770035416), E = a(E, y, R, w, S[m + 9], b, 2336552879), w = a(w, E, y, R, S[m + 10], T, 4294925233), R = a(R, w, E, y, S[m + 11], q, 2304563134), y = a(y, R, w, E, S[m + 12], O, 1804603682), E = a(E, y, R, w, S[m + 13], b, 4254626195), w = a(w, E, y, R, S[m + 14], T, 2792965006), R = a(R, w, E, y, S[m + 15], q, 1236535329), y = p(y, R, w, E, S[m + 1], A, 4129170786), E = p(E, y, R, w, S[m + 6], x, 3225465664), w = p(w, E, y, R, S[m + 11], C, 643717713), R = p(R, w, E, y, S[m + 0], N, 3921069994), y = p(y, R, w, E, S[m + 5], A, 3593408605), E = p(E, y, R, w, S[m + 10], x, 38016083), w = p(w, E, y, R, S[m + 15], C, 3634488961), R = p(R, w, E, y, S[m + 4], N, 3889429448), y = p(y, R, w, E, S[m + 9], A, 568446438), E = p(E, y, R, w, S[m + 14], x, 3275163606), w = p(w, E, y, R, S[m + 3], C, 4107603335), R = p(R, w, E, y, S[m + 8], N, 1163531501), y = p(y, R, w, E, S[m + 13], A, 2850285829), E = p(E, y, R, w, S[m + 2], x, 4243563512), w = p(w, E, y, R, S[m + 7], C, 1735328473), R = p(R, w, E, y, S[m + 12], N, 2368359562), y = u(y, R, w, E, S[m + 5], J, 4294588738), E = u(E, y, R, w, S[m + 8], k, 2272392833), w = u(w, E, y, R, S[m + 11], L, 1839030562), R = u(R, w, E, y, S[m + 14], D, 4259657740), y = u(y, R, w, E, S[m + 1], J, 2763975236), E = u(E, y, R, w, S[m + 4], k, 1272893353), w = u(w, E, y, R, S[m + 7], L, 4139469664), R = u(R, w, E, y, S[m + 10], D, 3200236656), y = u(y, R, w, E, S[m + 13], J, 681279174), E = u(E, y, R, w, S[m + 0], k, 3936430074), w = u(w, E, y, R, S[m + 3], L, 3572445317), R = u(R, w, E, y, S[m + 6], D, 76029189), y = u(y, R, w, E, S[m + 9], J, 3654602809), E = u(E, y, R, w, S[m + 12], k, 3873151461), w = u(w, E, y, R, S[m + 15], L, 530742520), R = u(R, w, E, y, S[m + 2], D, 3299628645), y = c(y, R, w, E, S[m + 0], I, 4096336452), E = c(E, y, R, w, S[m + 7], P, 1126891415), w = c(w, E, y, R, S[m + 14], F, 2878612391), R = c(R, w, E, y, S[m + 5], j, 4237533241), y = c(y, R, w, E, S[m + 12], I, 1700485571), E = c(E, y, R, w, S[m + 3], P, 2399980690), w = c(w, E, y, R, S[m + 10], F, 4293915773), R = c(R, w, E, y, S[m + 1], j, 2240044497), y = c(y, R, w, E, S[m + 8], I, 1873313359), E = c(E, y, R, w, S[m + 15], P, 4264355552), w = c(w, E, y, R, S[m + 6], F, 2734768916), R = c(R, w, E, y, S[m + 13], j, 1309151649), y = c(y, R, w, E, S[m + 4], I, 4149444226), E = c(E, y, R, w, S[m + 11], P, 3174756917), w = c(w, E, y, R, S[m + 2], F, 718787259), R = c(R, w, E, y, S[m + 9], j, 3951481745), y = n(y, h), R = n(R, g), w = n(w, v), E = n(E, _)
            }
            var H = l(y) + l(R) + l(w) + l(E);
            return H.toLowerCase()
        }

        function u(e) {
            return "[object Object]" == {}.toString.call(e)
        }

        function c(e, t, n) {
            var o = n || {};
            document.cookie = e.replace(/[^+#$&^`|]/g, encodeURIComponent).replace("(", "%28").replace(")", "%29") + "=" + t.replace(/[^+#$&\/:<-\[\]-}]/g, encodeURIComponent) + (o.domain ? ";domain=" + o.domain : "") + (o.path ? ";path=" + o.path : "") + (o.secure ? ";secure" : "") + (o.httponly ? ";HttpOnly" : "")
        }

        function d(e) {
            var t = new RegExp("(?:^|;\\s*)" + e + "\\=([^;]+)(?:;\\s*|$)").exec(document.cookie);
            return t ? t[1] : void 0
        }

        function l(e, t, n) {
            var o = new Date;
            o.setTime(o.getTime() - 864e5);
            var i = "/";
            document.cookie = e + "=;path=" + i + ";domain=." + t + ";expires=" + o.toGMTString(), document.cookie = e + "=;path=" + i + ";domain=." + n + "." + t + ";expires=" + o.toGMTString()
        }

        function f() {
            var t = e.location.hostname;
            if (!t) {
                var n = e.parent.location.hostname;
                n && ~n.indexOf("zebra.alibaba-inc.com") && (t = n)
            }
            var o = ["taobao.net", "taobao.com", "tmall.com", "tmall.hk", "alibaba-inc.com"],
                i = new RegExp("([^.]*?)\\.?((?:" + o.join(")|(?:").replace(/\./g, "\\.") + "))", "i"),
                r = t.match(i) || [],
                s = r[2] || "taobao.com",
                a = r[1] || "m";
            "taobao.net" !== s || "x" !== a && "waptest" !== a && "daily" !== a ? "taobao.net" === s && "demo" === a ? a = "demo" : "alibaba-inc.com" === s && "zebra" === a ? a = "zebra" : "waptest" !== a && "wapa" !== a && "m" !== a && (a = "m") : a = "waptest";
            var p = "h5api";
            _.mainDomain = s, _.subDomain = a, _.prefix = p
        }

        function m() {
            var t = e.navigator.userAgent,
                n = t.match(/WindVane[\/\s]([\d\.\_]+)/);
            n && (_.WindVaneVersion = n[1]);
            var o = t.match(/AliApp\(([^\/]+)\/([\d\.\_]+)\)/i);
            o && (_.AliAppName = o[1], _.AliAppVersion = o[2])
        }

        function h(e) {
            this.id = ++E, this.params = i(e || {}, {
                v: "*",
                data: {},
                type: "get",
                dataType: "jsonp"
            }), this.params.type = this.params.type.toLowerCase(), "object" == o(this.params.data) && (this.params.data = JSON.stringify(this.params.data)), this.middlewares = y.slice(0)
        }
        var g = e.Promise,
            v = (g || {
                resolve: function e() {
                    return void 0
                }
            }).resolve();
        String.prototype.trim || (String.prototype.trim = function() {
            return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "")
        });
        var _ = {
                useJsonpResultType: !1,
                safariGoLogin: !0,
                useAlipayJSBridge: !1
            },
            y = [],
            R = {
                ERROR: -1,
                SUCCESS: 0,
                TOKEN_EXPIRED: 1,
                SESSION_EXPIRED: 2
            };
        f(), m();
        var w = "AP" === _.AliAppName && parseFloat(_.AliAppVersion) >= 10.1,
            E = 0,
            S = "2.4.8";
        h.prototype.use = function(e) {
            if (!e) throw new Error("middleware is undefined");
            return this.middlewares.push(e), this
        }, h.prototype.__processRequestMethod = function(e) {
            var t = this.params,
                n = this.options;
            "get" === t.type && "jsonp" === t.dataType ? n.getJSONP = !0 : "get" === t.type && "originaljsonp" === t.dataType ? n.getOriginalJSONP = !0 : "get" === t.type && "json" === t.dataType ? n.getJSON = !0 : "post" === t.type && (n.postJSON = !0), e()
        }, h.prototype.__processRequestType = function(n) {
            var o = this,
                i = this.params,
                r = this.options;
            if (_.H5Request === !0 && (r.H5Request = !0), _.WindVaneRequest === !0 && (r.WindVaneRequest = !0), r.H5Request === !1 && r.WindVaneRequest === !0) {
                if (!w && (!t.windvane || parseFloat(r.WindVaneVersion) < 5.4)) throw new Error("WINDVANE_NOT_FOUND::\u7f3a\u5c11WindVane\u73af\u5883");
                if (w && !e.AlipayJSBridge) throw new Error("ALIPAY_NOT_READY::\u652f\u4ed8\u5b9d\u901a\u9053\u672a\u51c6\u5907\u597d\uff0c\u652f\u4ed8\u5b9d\u8bf7\u89c1 https://lark.alipay.com/mtbsdkdocs/mtopjssdkdocs/pucq6z")
            } else if (r.H5Request === !0) r.WindVaneRequest = !1;
            else if ("undefined" == typeof r.WindVaneRequest && "undefined" == typeof r.H5Request && (t.windvane && parseFloat(r.WindVaneVersion) >= 5.4 ? r.WindVaneRequest = !0 : r.H5Request = !0, w))
                if (r.WindVaneRequest = r.H5Request = void 0, e.AlipayJSBridge) {
                    if (u(i.data)) r.WindVaneRequest = !0;
                    else try {
                        u(JSON.parse(i.data)) ? r.WindVaneRequest = !0 : r.H5Request = !0
                    } catch (e) {
                        r.H5Request = !0
                    }
                } else r.H5Request = !0;
            var s = e.navigator.userAgent.toLowerCase();
            return s.indexOf("youku") > -1 && r.mainDomain.indexOf("youku.com") < 0 && (r.WindVaneRequest = !1, r.H5Request = !0), r.mainDomain.indexOf("youku.com") > -1 && s.indexOf("youku") < 0 && (r.WindVaneRequest = !1, r.H5Request = !0), n ? n().then(function() {
                var e = r.retJson.ret;
                if (e instanceof Array && (e = e.join(",")), r.WindVaneRequest === !0 && w && r.retJson.error || !e || e.indexOf("PARAM_PARSE_ERROR") > -1 || e.indexOf("HY_FAILED") > -1 || e.indexOf("HY_NO_HANDLER") > -1 || e.indexOf("HY_CLOSED") > -1 || e.indexOf("HY_EXCEPTION") > -1 || e.indexOf("HY_NO_PERMISSION") > -1) {
                    if (!w || !(isNaN(r.retJson.error) || e.indexOf("FAIL_SYS_ACCESS_DENIED") > -1)) return w && u(i.data) && (i.data = JSON.stringify(i.data)), _.H5Request = !0, o.__sequence([o.__processRequestType, o.__processToken, o.__processRequestUrl, o.middlewares, o.__processRequest]);
                    "undefined" == typeof r.retJson.api && "undefined" == typeof r.retJson.v && (r.retJson.api = i.api, r.retJson.v = i.v, r.retJson.ret = [r.retJson.error + "::" + r.retJson.errorMessage], r.retJson.data = {})
                }
            }) : void 0
        };
        var O = "_m_h5_c",
            b = "_m_h5_tk",
            T = "_m_h5_tk_enc";
        h.prototype.__getTokenFromAlipay = function() {
            var t = n(),
                o = this.options,
                i = (e.navigator.userAgent, !!location.protocol.match(/^https?\:$/));
            return o.useAlipayJSBridge === !0 && !i && w && e.AlipayJSBridge && e.AlipayJSBridge.call ? e.AlipayJSBridge.call("getMtopToken", function(e) {
                e && e.token && (o.token = e.token), t.resolve()
            }, function() {
                t.resolve()
            }) : t.resolve(), t.promise
        }, h.prototype.__getTokenFromCookie = function() {
            var e = this.options;
            return e.CDR && d(O) ? e.token = d(O).split(";")[0] : e.token = e.token || d(b), e.token && (e.token = e.token.split("_")[0]), g.resolve()
        }, h.prototype.__waitWKWebViewCookie = function(t) {
            var n = this.options;
            n.waitWKWebViewCookieFn && n.H5Request && e.webkit && e.webkit.messageHandlers ? n.waitWKWebViewCookieFn(t) : t()
        }, h.prototype.__processToken = function(e) {
            var t = this,
                n = this.options;
            this.params;
            return n.token && delete n.token, n.WindVaneRequest !== !0 ? v.then(function() {
                return t.__getTokenFromAlipay()
            }).then(function() {
                return t.__getTokenFromCookie()
            }).then(e).then(function() {
                var e = n.retJson,
                    o = e.ret;
                if (o instanceof Array && (o = o.join(",")), o.indexOf("TOKEN_EMPTY") > -1 || n.CDR === !0 && o.indexOf("ILLEGAL_ACCESS") > -1 || o.indexOf("TOKEN_EXOIRED") > -1) {
                    if (n.maxRetryTimes = n.maxRetryTimes || 5, n.failTimes = n.failTimes || 0, n.H5Request && ++n.failTimes < n.maxRetryTimes) return t.__sequence([t.__waitWKWebViewCookie, t.__processToken, t.__processRequestUrl, t.middlewares, t.__processRequest]);
                    n.maxRetryTimes > 0 && (l(O, n.pageDomain, "*"), l(b, n.mainDomain, n.subDomain), l(T, n.mainDomain, n.subDomain)), e.retType = R.TOKEN_EXPIRED
                }
            }) : void e()
        }, h.prototype.__processRequestUrl = function(t) {
            var n = this.params,
                o = this.options;
            if (o.hostSetting && o.hostSetting[e.location.hostname]) {
                var i = o.hostSetting[e.location.hostname];
                i.prefix && (o.prefix = i.prefix), i.subDomain && (o.subDomain = i.subDomain), i.mainDomain && (o.mainDomain = i.mainDomain)
            }
            if (o.H5Request === !0) {
                var r = "//" + (o.prefix ? o.prefix + "." : "") + (o.subDomain ? o.subDomain + "." : "") + o.mainDomain + "/h5/" + n.api.toLowerCase() + "/" + n.v.toLowerCase() + "/",
                    s = n.appKey || ("waptest" === o.subDomain ? "4272" : "12574478"),
                    a = (new Date).getTime(),
                    u = p(o.token + "&" + a + "&" + s + "&" + n.data),
                    c = {
                        jsv: S,
                        appKey: s,
                        t: a,
                        sign: u
                    },
                    d = {
                        data: n.data,
                        ua: n.ua
                    };

                //下面是我的调试代码
                console.log(o);

                Object.keys(n).forEach(function(e) {
                    "undefined" == typeof c[e] && "undefined" == typeof d[e] && (c[e] = n[e])
                }), o.getJSONP ? c.type = "jsonp" : o.getOriginalJSONP ? c.type = "originaljsonp" : (o.getJSON || o.postJSON) && (c.type = "originaljson"), "undefined" != typeof n.valueType && ("original" === n.valueType ? o.getJSONP || o.getOriginalJSONP ? c.type = "originaljsonp" : (o.getJSON || o.postJSON) && (c.type = "originaljson") : "string" === n.valueType && (o.getJSONP || o.getOriginalJSONP ? c.type = "jsonp" : (o.getJSON || o.postJSON) && (c.type = "json"))), o.useJsonpResultType === !0 && "originaljson" === c.type && delete c.type, o.dangerouslySetProtocol && (r = o.dangerouslySetProtocol + ":" + r), o.querystring = c, o.postdata = d, o.path = r
            }
            t()
        }, h.prototype.__processUnitPrefix = function(e) {
            e()
        };
        var q = 0;

        //下面是我调试的代码
        console.log(h);

        h.prototype.__requestJSONP = function(e) {
            function t(e) {
                if (c && clearTimeout(c), d.parentNode && d.parentNode.removeChild(d), "TIMEOUT" === e) window[u] = function() {
                    window[u] = void 0;
                    try {
                        delete window[u]
                    } catch (e) {}
                };
                else {
                    window[u] = void 0;
                    try {
                        delete window[u]
                    } catch (e) {}
                }
            }
            var o = n(),
                i = this.params,
                a = this.options,
                p = i.timeout || 2e4,
                u = "mtopjsonp" + (i.jsonpIncPrefix || "") + ++q,
                c = setTimeout(function() {
                    e(a.timeoutErrMsg || "TIMEOUT::\u63a5\u53e3\u8d85\u65f6"), t("TIMEOUT")
                }, p);
            a.querystring.callback = u;
            var d = document.createElement("script");
            return d.src = a.path + "?" + s(a.querystring) + "&" + s(a.postdata), d.async = !0, d.onerror = function() {
                t("ABORT"), e(a.abortErrMsg || "ABORT::\u63a5\u53e3\u5f02\u5e38\u9000\u51fa")
            }, window[u] = function() {
                a.results = Array.prototype.slice.call(arguments), t(), o.resolve()
            }, r(d), o.promise
        }, h.prototype.__requestJSON = function(t) {
            function o(e) {
                c && clearTimeout(c), "TIMEOUT" === e && p.abort()
            }
            var i = n(),
                r = this.params,
                a = this.options,
                p = new e.XMLHttpRequest,
                u = r.timeout || 2e4,
                c = setTimeout(function() {
                    t(a.timeoutErrMsg || "TIMEOUT::\u63a5\u53e3\u8d85\u65f6"), o("TIMEOUT")
                }, u);
            a.CDR && d(O) && (a.querystring.c = decodeURIComponent(d(O))), p.onreadystatechange = function() {
                if (4 == p.readyState) {
                    var e, n, r = p.status;
                    if (r >= 200 && 300 > r || 304 == r) {
                        o(), e = p.responseText, n = p.getAllResponseHeaders() || "";
                        try {
                            e = /^\s*$/.test(e) ? {} : JSON.parse(e), e.responseHeaders = n, a.results = [e], i.resolve()
                        } catch (e) {
                            t("PARSE_JSON_ERROR::\u89e3\u6790JSON\u5931\u8d25")
                        }
                    } else o("ABORT"), t(a.abortErrMsg || "ABORT::\u63a5\u53e3\u5f02\u5e38\u9000\u51fa")
                }
            };
            var l, f, m = a.path + "?" + s(a.querystring);
            if (a.getJSON ? (l = "GET", m += "&" + s(a.postdata)) : a.postJSON && (l = "POST", f = s(a.postdata)), p.open(l, m, !0), p.withCredentials = !0, p.setRequestHeader("Accept", "application/json"), p.setRequestHeader("Content-type", "application/x-www-form-urlencoded"), r.headers)
                for (var h in r.headers) {
                    p.setRequestHeader(h, r.headers[h])
                }
            return p.send(f), i.promise
        }, h.prototype.__requestWindVane = function(e) {
            function o(e) {
                s.results = [e], i.resolve()
            }
            var i = n(),
                r = this.params,
                s = this.options,
                a = r.data,
                p = r.api,
                u = r.v,
                c = s.postJSON ? 1 : 0,
                d = s.getJSON || s.postJSON || s.getOriginalJSONP ? "originaljson" : "";
            "undefined" != typeof r.valueType && ("original" === r.valueType ? d = "originaljson" : "string" === r.valueType && (d = "")), s.useJsonpResultType === !0 && (d = "");
            var l, f, m = "https" === location.protocol ? 1 : 0,
                h = r.isSec || 0,
                g = r.sessionOption || "AutoLoginOnly",
                v = r.ecode || 0;
            return f = "undefined" != typeof r.timer ? parseInt(r.timer) : "undefined" != typeof r.timeout ? parseInt(r.timeout) : 2e4, l = 2 * f, r.needLogin === !0 && "undefined" == typeof r.sessionOption && (g = "AutoLoginAndManualLogin"), "undefined" != typeof r.secType && "undefined" == typeof r.isSec && (h = r.secType), t.windvane.call("MtopWVPlugin", "send", {
                api: p,
                v: u,
                post: String(c),
                type: d,
                isHttps: String(m),
                ecode: String(v),
                isSec: String(h),
                param: JSON.parse(a),
                timer: f,
                sessionOption: g,
                ext_headers: {
                    referer: location.href
                }
            }, o, o, l), i.promise
        }, h.prototype.__requestAlipay = function(t) {
            function o(e) {
                s.results = [e], i.resolve()
            }
            var i = n(),
                r = this.params,
                s = this.options,
                a = {
                    apiName: r.api,
                    apiVersion: r.v,
                    needEcodeSign: !!r.ecode,
                    usePost: !!s.postJSON
                };
            return u(r.data) || (r.data = JSON.parse(r.data)), a.data = r.data, r.ttid && (a.ttid = r.ttid), (s.getJSON || s.postJSON || s.getOriginalJSONP) && (a.type = "originaljson"), "undefined" != typeof r.valueType && ("original" === r.valueType ? a.type = "originaljson" : "string" === r.valueType && delete a.type), s.useJsonpResultType === !0 && delete a.type, e.AlipayJSBridge.call("mtop", a, o), i.promise
        }, h.prototype.__processRequest = function(e, t) {
            var n = this;
            return v.then(function() {
                var e = n.options;
                if (e.H5Request && (e.getJSONP || e.getOriginalJSONP)) return n.__requestJSONP(t);
                if (e.H5Request && (e.getJSON || e.postJSON)) return n.__requestJSON(t);
                if (e.WindVaneRequest) return w ? n.__requestAlipay(t) : n.__requestWindVane(t);
                throw new Error("UNEXCEPT_REQUEST::\u9519\u8bef\u7684\u8bf7\u6c42\u7c7b\u578b")
            }).then(e).then(function() {
                var e = n.options,
                    t = (n.params, e.results[0]),
                    o = t && t.ret || [];
                t.ret = o, o instanceof Array && (o = o.join(","));
                var i = t.c;
                e.CDR && i && c(O, i, {
                    domain: e.pageDomain,
                    path: "/"
                }), o.indexOf("SUCCESS") > -1 ? t.retType = R.SUCCESS : t.retType = R.ERROR, e.retJson = t
            })
        }, h.prototype.__sequence = function(e) {
            function t(e) {
                if (e instanceof Array) e.forEach(t);
                else {
                    var s, a = n(),
                        p = n();
                    i.push(function() {
                        return a = n(), s = e.call(o, function(e) {
                            return a.resolve(e), p.promise
                        }, function(e) {
                            return a.reject(e), p.promise
                        }), s && (s = s["catch"](function(e) {
                            a.reject(e)
                        })), a.promise
                    }), r.push(function(e) {
                        return p.resolve(e), s
                    })
                }
            }
            var o = this,
                i = [],
                r = [];
            e.forEach(t);
            for (var s, a = v; s = i.shift();) {
                a = a.then(s)
            }
            for (; s = r.pop();) {
                a = a.then(s)
            }
            return a
        };
        var A = function e(t) {
                t()
            },
            x = function e(t) {
                t()
            };
        h.prototype.request = function(n) {
            var o = this;
            if (this.options = i(n || {}, _), !g) {
                var r = "\u5f53\u524d\u6d4f\u89c8\u5668\u4e0d\u652f\u6301Promise\uff0c\u8bf7\u5728windows\u5bf9\u8c61\u4e0a\u6302\u8f7dPromise\u5bf9\u8c61\u53ef\u53c2\u8003\uff08http://gitlab.alibaba-inc.com/mtb/lib-es6polyfill/tree/master\uff09\u4e2d\u7684\u89e3\u51b3\u65b9\u6848";
                throw t.mtop = {
                    ERROR: r
                }, new Error(r)
            }
            var s = g.resolve([A, x]).then(function(e) {
                var t = e[0],
                    n = e[1];
                return o.__sequence([t, o.__processRequestMethod, o.__processRequestType, o.__processToken, o.__processRequestUrl, o.middlewares, o.__processRequest, n])
            }).then(function() {
                var e = o.options.retJson;
                return e.retType !== R.SUCCESS ? g.reject(e) : o.options.successCallback ? void o.options.successCallback(e) : g.resolve(e)
            })["catch"](function(e) {
                var t;
                return e instanceof Error ? (console.error(e.stack), t = {
                    ret: [e.message],
                    stack: [e.stack],
                    retJson: R.ERROR
                }) : t = "string" == typeof e ? {
                    ret: [e],
                    retJson: R.ERROR
                } : void 0 !== e ? e : o.options.retJson, o.options.failureCallback ? void o.options.failureCallback(t) : g.reject(t)
            });
            return this.__processRequestType(), o.options.H5Request && (o.constructor.__firstProcessor || (o.constructor.__firstProcessor = s), A = function e(t) {
                o.constructor.__firstProcessor.then(t)["catch"](t)
            }), ("get" === this.params.type && "json" === this.params.dataType || "post" === this.params.type) && (n.pageDomain = n.pageDomain || a(e.location.hostname), n.mainDomain !== n.pageDomain && (n.maxRetryTimes = 4, n.CDR = !0)), s
        }, t.mtop = function(e) {
            return new h(e)
        }, t.mtop.request = function(e, t, n) {
            var o = {
                H5Request: e.H5Request,
                WindVaneRequest: e.WindVaneRequest,
                LoginRequest: e.LoginRequest,
                AntiCreep: e.AntiCreep,
                AntiFlood: e.AntiFlood,
                successCallback: t,
                failureCallback: n || t
            };
            return new h(e).request(o)
        }, t.mtop.H5Request = function(e, t, n) {
            var o = {
                H5Request: !0,
                successCallback: t,
                failureCallback: n || t
            };
            return new h(e).request(o)
        }, t.mtop.middlewares = y, t.mtop.config = _, t.mtop.RESPONSE_TYPE = R, t.mtop.CLASS = h
    }(window, window.lib || (window.lib = {})),
    function(e, t) {
        function n(e) {
            return e.preventDefault(), !1
        }

        function o(e) {
            var t = new RegExp("(?:^|;\\s*)" + e + "\\=([^;]+)(?:;\\s*|$)").exec(document.cookie);
            return t ? t[1] : void 0
        }

        function i(t, o) {
            var i = this,
                r = e.dpr || 1,
                s = document.createElement("div"),
                a = document.documentElement.getBoundingClientRect(),
                p = Math.max(a.width, window.innerWidth) / r,
                u = Math.max(a.height, window.innerHeight) / r;
            s.style.cssText = ["-webkit-transform:scale(" + r + ") translateZ(0)", "-ms-transform:scale(" + r + ") translateZ(0)", "transform:scale(" + r + ") translateZ(0)", "-webkit-transform-origin:0 0", "-ms-transform-origin:0 0", "transform-origin:0 0", "width:" + p + "px", "height:" + u + "px", "z-index:999999", "position:" + (p > 800 ? "fixed" : "absolute"), "left:0", "top:0px", "background:" + (p > 800 ? "rgba(0,0,0,.5)" : "#FFF"), "display:none"].join(";");
            var c = document.createElement("div");
            c.style.cssText = ["width:100%", "height:52px", "background:#EEE", "line-height:52px", "text-align:left", "box-sizing:border-box", "padding-left:20px", "position:absolute", "left:0", "top:0", "font-size:16px", "font-weight:bold", "color:#333"].join(";"), c.innerText = t;
            var d = document.createElement("a");
            d.style.cssText = ["display:block", "position:absolute", "right:0", "top:0", "height:52px", "line-height:52px", "padding:0 20px", "color:#999"].join(";"), d.innerText = "\u5173\u95ed";
            var l = document.createElement("iframe");
            l.style.cssText = ["width:100%", "height:100%", "border:0", "overflow:hidden"].join(";"), p > 800 && (c.style.cssText = ["width:370px", "height:52px", "background:#EEE", "line-height:52px", "text-align:left", "box-sizing:border-box", "padding-left:20px", "position:absolute", "left:" + (p / 2 - 185) + "px", "top:40px", "font-size:16px", "font-weight:bold", "color:#333"].join(";"), l.style.cssText = ["position:absolute", "top:92px", "left:" + (p / 2 - 185) + "px", "width:370px", "height:480px", "border:0", "background:#FFF", "overflow:hidden"].join(";")), c.appendChild(d), s.appendChild(c), s.appendChild(l), s.className = "J_MIDDLEWARE_FRAME_WIDGET", document.body.appendChild(s), l.src = o, d.addEventListener("click", function() {
                i.hide();
                var e = document.createEvent("HTMLEvents");
                e.initEvent("close", !1, !1), s.dispatchEvent(e)
            }, !1), this.addEventListener = function() {
                s.addEventListener.apply(s, arguments)
            }, this.removeEventListener = function() {
                s.removeEventListener.apply(s, arguments)
            }, this.show = function() {
                document.addEventListener("touchmove", n, !1), s.style.display = "block", window.scrollTo(0, 0)
            }, this.hide = function() {
                document.removeEventListener("touchmove", n), window.scrollTo(0, -a.top), s.parentNode && s.parentNode.removeChild(s)
            }
        }

        function r(e) {
            var n = this,
                o = this.options,
                i = this.params;
            return e().then(function() {
                var e = o.retJson,
                    r = e.ret,
                    s = navigator.userAgent.toLowerCase(),
                    a = s.indexOf("safari") > -1 && s.indexOf("chrome") < 0 && s.indexOf("qqbrowser") < 0;
                if (r instanceof Array && (r = r.join(",")), (r.indexOf("SESSION_EXPIRED") > -1 || r.indexOf("SID_INVALID") > -1 || r.indexOf("AUTH_REJECT") > -1 || r.indexOf("NEED_LOGIN") > -1) && (e.retType = d.SESSION_EXPIRED, !o.WindVaneRequest && (c.LoginRequest === !0 || o.LoginRequest === !0 || i.needLogin === !0))) {
                    if (!t.login) throw new Error("LOGIN_NOT_FOUND::\u7f3a\u5c11lib.login");
                    if (o.safariGoLogin !== !0 || !a || "taobao.com" === o.pageDomain) return t.login.goLoginAsync().then(function(e) {
                        return n.__sequence([n.__processToken, n.__processRequestUrl, n.__processUnitPrefix, n.middlewares, n.__processRequest])
                    })["catch"](function(e) {
                        throw "CANCEL" === e ? new Error("LOGIN_CANCEL::\u7528\u6237\u53d6\u6d88\u767b\u5f55") : new Error("LOGIN_FAILURE::\u7528\u6237\u767b\u5f55\u5931\u8d25")
                    });
                    t.login.goLogin()
                }
            })
        }

        function s(e) {
            var t = this.options;
            this.params;
            return t.H5Request !== !0 || c.AntiFlood !== !0 && t.AntiFlood !== !0 ? void e() : e().then(function() {
                var e = t.retJson,
                    n = e.ret;
                n instanceof Array && (n = n.join(",")), n.indexOf("FAIL_SYS_USER_VALIDATE") > -1 && e.data.url && (t.AntiFloodReferer ? location.href = e.data.url.replace(/(http_referer=).+/, "$1" + t.AntiFloodReferer) : location.href = e.data.url)
            })
        }

        function a(t) {
            var n = this,
                r = this.options,
                s = this.params;
            return s.forceAntiCreep !== !0 && r.H5Request !== !0 || c.AntiCreep !== !0 && r.AntiCreep !== !0 ? void t() : t().then(function() {
                var t = r.retJson,
                    a = t.ret;
                if (a instanceof Array && (a = a.join(",")), a.indexOf("RGV587_ERROR::SM") > -1 && t.data.url) {
                    var u = "_m_h5_smt",
                        c = o(u),
                        d = !1;
                    if (r.saveAntiCreepToken === !0 && c) {
                        c = JSON.parse(c);
                        for (var l in c) {
                            s[l] && (d = !0)
                        }
                    }
                    if (r.saveAntiCreepToken === !0 && c && !d) {
                        for (var l in c) {
                            s[l] = c[l]
                        }
                        return n.__sequence([n.__processToken, n.__processRequestUrl, n.__processUnitPrefix, n.middlewares, n.__processRequest])
                    }
                    return new p(function(o, a) {
                        function p() {
                            l.removeEventListener("close", p), e.removeEventListener("message", c), a("USER_INPUT_CANCEL::\u7528\u6237\u53d6\u6d88\u8f93\u5165")
                        }

                        function c(t) {
                            var i;
                            try {
                                i = JSON.parse(t.data) || {}
                            } catch (e) {}
                            if (i && "child" === i.type) {
                                l.removeEventListener("close", p), e.removeEventListener("message", c), l.hide();
                                var d;
                                try {
                                    d = JSON.parse(decodeURIComponent(i.content)), "string" == typeof d && (d = JSON.parse(d));
                                    for (var f in d) {
                                        s[f] = d[f]
                                    }
                                    r.saveAntiCreepToken === !0 ? (document.cookie = u + "=" + JSON.stringify(d) + ";", e.location.reload()) : n.__sequence([n.__processToken, n.__processRequestUrl, n.__processUnitPrefix, n.middlewares, n.__processRequest]).then(o)
                                } catch (e) {
                                    a("USER_INPUT_FAILURE::\u7528\u6237\u8f93\u5165\u5931\u8d25")
                                }
                            }
                        }
                        var d = t.data.url,
                            l = new i("", d);
                        l.addEventListener("close", p, !1), e.addEventListener("message", c, !1), l.show()
                    })
                }
            })
        }
        if (!t || !t.mtop || t.mtop.ERROR) throw new Error("Mtop \u521d\u59cb\u5316\u5931\u8d25\uff01\u8bf7\u53c2\u8003Mtop\u6587\u6863http://gitlab.alibaba-inc.com/mtb/lib-mtop");
        var p = e.Promise,
            u = t.mtop.CLASS,
            c = t.mtop.config,
            d = t.mtop.RESPONSE_TYPE;
        t.mtop.middlewares.push(r), t.mtop.loginRequest = function(e, t, n) {
            var o = {
                LoginRequest: !0,
                H5Request: !0,
                successCallback: t,
                failureCallback: n || t
            };
            return new u(e).request(o)
        }, t.mtop.antiFloodRequest = function(e, t, n) {
            var o = {
                AntiFlood: !0,
                successCallback: t,
                failureCallback: n || t
            };
            return new u(e).request(o)
        }, t.mtop.middlewares.push(s), t.mtop.antiCreepRequest = function(e, t, n) {
            var o = {
                AntiCreep: !0,
                successCallback: t,
                failureCallback: n || t
            };
            return new u(e).request(o)
        }, t.mtop.middlewares.push(a)
    }(window, window.lib || (window.lib = {}));
    n.exports = window.lib["mtop"];
    (function(e, t) {
        function n(e) {
            var t = this.options;
            var n = false;
            var o;
            if (t.LimitFlood) {
                n = t.LimitFlood.redirect;
                o = t.LimitFlood.url
            } else {
                var i = this.params;
                if (i && i.LimitFlood) {
                    n = i.LimitFlood.redirect;
                    o = i.LimitFlood.url
                }
            }
            if (n) {
                return e().then(function() {
                    var e = t.retJson;
                    var n = e.ret;
                    if (n instanceof Array) {
                        n = n.join(",")
                    }
                    if (n.indexOf("FAIL_LOCAL_ERROR_FANG_XUE_FENG") > -1 || n.indexOf("FAIL_SYS_TRAFFIC_LIMIT") > -1) {
                        if (!o) {
                            o = "https://pages.tmall.com/wow/act/15995/tmlimit?http_referer=" + location.href
                        }
                        location.href = o
                    }
                })
            } else {
                e()
            }
        }
        t.mtop.middlewares.push(n)
    })(window, window.lib || (window.lib = {}))
});


define("mui/mtb-windvane/index", function(e, t, n) {
    "use strict";
    var i = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
        return typeof e
    } : function(e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
    };
    "undefined" == typeof window && (window = {
        "ctrl": {},
        "lib": {}
    }), !window.ctrl && (window.ctrl = {}), !window.lib && (window.lib = {}), ! function(e, t) {
        function n(e, t) {
            e = e.toString().split("."), t = t.toString().split(".");
            for (var n = 0; n < e.length || n < t.length; n++) {
                var i = parseInt(e[n], 10),
                    r = parseInt(t[n], 10);
                if (window.isNaN(i) && (i = 0), window.isNaN(r) && (r = 0), i < r) return -1;
                if (i > r) return 1
            }
            return 0
        }
        var r = e.Promise,
            a = e.document,
            s = e.navigator.userAgent,
            o = /Windows\sPhone\s(?:OS\s)?[\d\.]+/i.test(s) || /Windows\sNT\s[\d\.]+/i.test(s),
            u = o && e.WindVane_Win_Private && e.WindVane_Win_Private.call,
            l = /iPhone|iPad|iPod/i.test(s),
            c = /Android/i.test(s),
            f = s.match(/WindVane[\/\s](\d+[._]\d+[._]\d+)/),
            d = Object.prototype.hasOwnProperty,
            h = t.windvane = e.WindVane || (e.WindVane = {}),
            m = (e.WindVane_Native, Math.floor(65536 * Math.random())),
            p = 1,
            v = [],
            w = 3,
            y = "hybrid",
            b = "wv_hybrid",
            g = "iframe_",
            _ = "param_",
            P = "chunk_",
            N = 6e5,
            S = 6e5,
            C = 6e4;
        f = f ? (f[1] || "0.0.0").replace(/\_/g, ".") : "0.0.0";
        var W = {
                "isAvailable": 1 === n(f, "0"),
                "call": function(e, t, n, i, a, s) {
                    var o, u;
                    "number" == typeof arguments[arguments.length - 1] && (s = arguments[arguments.length - 1]), "function" != typeof i && (i = null), "function" != typeof a && (a = null), r && (u = {}, u.promise = new r(function(e, t) {
                        u.resolve = e, u.reject = t
                    })), o = E.getSid();
                    var l = {
                        "success": i,
                        "failure": a,
                        "deferred": u
                    };
                    if (s > 0 && (l.timeout = setTimeout(function() {
                            W.onFailure(o, {
                                "ret": "HY_TIMEOUT"
                            })
                        }, s)), E.registerCall(o, l), E.registerGC(o, s), W.isAvailable ? E.callMethod(e, t, n, o) : W.onFailure(o, {
                            "ret": "HY_NOT_IN_WINDVANE"
                        }), u) return u.promise
                },
                "fireEvent": function(e, t, n) {
                    var i = a.createEvent("HTMLEvents");
                    i.initEvent(e, !1, !0), i.param = E.parseData(t || E.getData(n)), a.dispatchEvent(i)
                },
                "getParam": function(e) {
                    return E.getParam(e)
                },
                "setData": function(e, t) {
                    E.setData(e, t)
                },
                "onSuccess": function(e, t) {
                    E.onComplete(e, t, "success")
                },
                "onFailure": function(e, t) {
                    E.onComplete(e, t, "failure")
                }
            },
            E = {
                "params": {},
                "chunks": {},
                "calls": {},
                "getSid": function() {
                    return (m + p++) % 65536 + ""
                },
                "buildParam": function(e) {
                    return e && "object" == ("undefined" == typeof e ? "undefined" : i(e)) ? JSON.stringify(e) : e || ""
                },
                "getParam": function(e) {
                    return this.params[_ + e] || ""
                },
                "setParam": function(e, t) {
                    this.params[_ + e] = t
                },
                "parseData": function(e) {
                    var t;
                    if (e && "string" == typeof e) try {
                        t = JSON.parse(e)
                    } catch (e) {
                        t = {
                            "ret": ["WV_ERR::PARAM_PARSE_ERROR"]
                        }
                    } else t = e || {};
                    return t
                },
                "setData": function() {
                    this.chunks[P + sid] = this.chunks[P + sid] || [], this.chunks[P + sid].push(chunk)
                },
                "getData": function(e) {
                    return this.chunks[P + e] ? this.chunks[P + e].join("") : ""
                },
                "registerCall": function(e, t) {
                    this.calls[e] = t
                },
                "unregisterCall": function(e) {
                    var t = {};
                    return this.calls[e] && (t = this.calls[e], delete this.calls[e]), t
                },
                "useIframe": function(e, t) {
                    var n = g + e,
                        i = v.pop();
                    i || (i = a.createElement("iframe"), i.setAttribute("frameborder", "0"), i.style.cssText = "width:0;height:0;border:0;display:none;"), i.setAttribute("id", n), i.setAttribute("src", t), i.parentNode || setTimeout(function() {
                        a.body.appendChild(i)
                    }, 5)
                },
                "retrieveIframe": function(e) {
                    var t = g + e,
                        n = a.querySelector("#" + t);
                    v.length >= w ? a.body.removeChild(n) : v.indexOf(n) < 0 && v.push(n)
                },
                "callMethod": function(t, n, i, r) {
                    if (i = E.buildParam(i), o) u ? e.WindVane_Win_Private.call(t, n, r, i) : this.onComplete(r, {
                        "ret": "HY_NO_HANDLER_ON_WP"
                    }, "failure");
                    else {
                        var a = y + "://" + t + ":" + r + "/" + n + "?" + i;
                        if (l) this.setParam(r, i), this.useIframe(r, a);
                        else if (c) {
                            var s = b + ":";
                            window.prompt(a, s)
                        } else this.onComplete(r, {
                            "ret": "HY_NOT_SUPPORT_DEVICE"
                        }, "failure")
                    }
                },
                "registerGC": function(e, t) {
                    var n = this,
                        i = Math.max(t || 0, N),
                        r = Math.max(t || 0, C),
                        a = Math.max(t || 0, S);
                    setTimeout(function() {
                        n.unregisterCall(e)
                    }, i), l ? setTimeout(function() {
                        n.params[_ + e] && delete n.params[_ + e]
                    }, r) : c && setTimeout(function() {
                        n.chunks[P + e] && delete n.chunks[P + e]
                    }, a)
                },
                "onComplete": function(e, t, n) {
                    var i = this.unregisterCall(e),
                        r = i.success,
                        a = i.failure,
                        s = i.deferred,
                        o = i.timeout;
                    o && clearTimeout(o), t = t ? t : this.getData(e), t = this.parseData(t);
                    var u = t.ret;
                    "string" == typeof u && (t = t.value || t, t.ret || (t.ret = [u])), "success" === n ? (r && r(t), s && s.resolve(t)) : "failure" === n && (a && a(t), s && s.reject(t)), l ? (this.retrieveIframe(e), this.params[_ + e] && delete this.params[_ + e]) : c && this.chunks[P + e] && delete this.chunks[P + e]
                }
            };
        for (var T in W) d.call(h, T) || (h[T] = W[T])
    }(window, window.lib || (window.lib = {})), n.exports = window.lib.windvane
});
define("mui/mtb-login/index", function(e, n, t) {
    "use strict";
    "undefined" == typeof window && (window = {
            "ctrl": {},
            "lib": {}
        }), !window.ctrl && (window.ctrl = {}), !window.lib && (window.lib = {}),
        function(e, n, t) {
            function o(e) {
                var n = new RegExp("(?:^|;\\s*)" + e + "\\=([^;]+)(?:;\\s*|$)").exec(C.cookie);
                return n ? n[1] : t
            }

            function i(e) {
                return e.preventDefault(), !1
            }

            function r(n, t) {
                var o = this,
                    r = e.dpr || 1,
                    a = document.createElement("div"),
                    c = document.documentElement.getBoundingClientRect(),
                    l = Math.max(c.width, window.innerWidth) / r,
                    s = Math.max(c.height, window.innerHeight) / r;
                a.style.cssText = ["-webkit-transform:scale(" + r + ") translateZ(0)", "-ms-transform:scale(" + r + ") translateZ(0)", "transform:scale(" + r + ") translateZ(0)", "-webkit-transform-origin:0 0", "-ms-transform-origin:0 0", "transform-origin:0 0", "width:" + l + "px", "height:" + s + "px", "z-index:999999", "position:absolute", "left:0", "top:0px", "background:#FFF", "display:none"].join(";");
                var d = document.createElement("div");
                d.style.cssText = ["width:100%", "height:52px", "background:#EEE", "line-height:52px", "text-align:left", "box-sizing:border-box", "padding-left:20px", "position:absolute", "left:0", "top:0", "font-size:16px", "font-weight:bold", "color:#333"].join(";"), d.innerText = n;
                var u = document.createElement("a");
                u.style.cssText = ["display:block", "position:absolute", "right:0", "top:0", "height:52px", "line-height:52px", "padding:0 20px", "color:#999"].join(";"), u.innerText = "\u5173\u95ed";
                var g = document.createElement("iframe");
                g.style.cssText = ["width:100%", "height:100%", "border:0", "overflow:hidden"].join(";"), d.appendChild(u), a.appendChild(d), a.appendChild(g), C.body.appendChild(a), g.src = t, u.addEventListener("click", function() {
                    o.hide();
                    var e = C.createEvent("HTMLEvents");
                    e.initEvent("close", !1, !1), a.dispatchEvent(e)
                }, !1), this.addEventListener = function() {
                    a.addEventListener.apply(a, arguments)
                }, this.removeEventListener = function() {
                    a.removeEventListener.apply(a, arguments)
                }, this.show = function() {
                    document.addEventListener("touchmove", i, !1), a.style.display = "block", window.scrollTo(0, 0)
                }, this.hide = function() {
                    document.removeEventListener("touchmove", i), window.scrollTo(0, -c.top), C.body.removeChild(a)
                }
            }

            function a(e) {
                if (!e || "function" != typeof e || !n.mtop) {
                    return !!this.getUserNick()
                }
                n.mtop.request({
                    "api": "mtop.user.getUserSimple",
                    "v": "1.0",
                    "data": {
                        "isSec": 0
                    },
                    "H5Request": !0
                }, function(o) {
                    o.retType === n.mtop.RESPONSE_TYPE.SUCCESS ? e(!0, o) : o.retType === n.mtop.RESPONSE_TYPE.SESSION_EXPIRED ? e(!1, o) : e(t, o)
                })
            }

            function c(e) {
                var n;
                return b && (n = {}, n.promise = new b(function(e, t) {
                    n.resolve = e, n.reject = t
                })), this.isLogin(function(t, o) {
                    e && e(t, o), !0 === t ? n && n.resolve(o) : n && n.reject(o)
                }), n ? n.promise : void 0
            }

            function l(e) {
                if (!e || "function" != typeof e) {
                    var n = "",
                        i = o("_w_tb_nick"),
                        r = o("_nk_") || o("snk"),
                        a = o("sn");
                    return i && i.length > 0 && "null" != i ? n = decodeURIComponent(i) : r && r.length > 0 && "null" != r ? n = unescape(unescape(r).replace(/\\u/g, "%u")) : a && a.length > 0 && "null" != a && (n = decodeURIComponent(a)), n = n.replace(/\</g, "&lt;").replace(/\>/g, "&gt;")
                }
                this.isLogin(function(n, o) {
                    e(!0 === n && o && o.data && o.data.nick ? o.data.nick : !1 === n ? "" : t)
                })
            }

            function s(e) {
                var n;
                return b && (n = {}, n.promise = new b(function(e, t) {
                    n.resolve = e, n.reject = t
                })), this.getUserNick(function(t) {
                    e && e(t), t ? n && n.resolve(t) : n && n.reject()
                }), n ? n.promise : void 0
            }

            function d(e, t) {
                var o = "//" + A + "." + _.subDomain + "." + T + "/" + _[(e || "login") + "Name"];
                if (t) {
                    var i = [];
                    for (var r in t) i.push(r + "=" + encodeURIComponent(t[r]));
                    o += "?" + i.join("&")
                }
                var a = n.login.config.loginUrlParams;
                if (a) {
                    var c = [];
                    for (var l in a) c.push(l + "=" + encodeURIComponent(a[l]));
                    o += /\?/.test(o) ? "&" + c.join("&") : "?" + i.join("&")
                }
                return o
            }

            function u(e, n) {
                n ? location.replace(e) : location.href = e
            }

            function g(n, t, o) {
                function i(n) {
                    s.removeEventListener("close", i), e.removeEventListener("message", a), o("CANCEL")
                }

                function a(n) {
                    var t = n.data || {};
                    t && "child" === t.type && t.content.indexOf("SUCCESS") > -1 ? (s.removeEventListener("close", i), e.removeEventListener("message", a), s.hide(), o("SUCCESS")) : o("FAILURE")
                }
                var c = location.protocol + "//h5." + _.subDomain + ".taobao.com/" + ("waptest" === _.subDomain ? "src" : "other") + "/" + n + "end.html?origin=" + encodeURIComponent(location.protocol + "//" + location.hostname),
                    l = d(n, {
                        "ttid": "h5@iframe",
                        "redirectURL": c
                    }),
                    s = new r(t.title || "\u60a8\u9700\u8981\u767b\u5f55\u624d\u80fd\u7ee7\u7eed\u8bbf\u95ee", l);
                s.addEventListener("close", i, !1), e.addEventListener("message", a, !1), s.show()
            }

            function p(n, t, o) {
                var i = d(n, {
                    "wvLoginCallback": "wvLoginCallback"
                });
                e.wvLoginCallback = function(n) {
                    delete e.wvLoginCallback, o(n.indexOf(":SUCCESS") > -1 ? "SUCCESS" : n.indexOf(":CANCEL") > -1 ? "CANCEL" : "FAILURE")
                }, u(i)
            }

            function m(e, n, t) {
                if ("function" == typeof n ? (t = n, n = null) : "string" == typeof n && (n = {
                        "redirectUrl": n
                    }), n = n || {}, t && U) p(e, n, t);
                else if (t && !y && "login" === e) g(e, n, t);
                else {
                    var o = d(e, {
                        "redirectURL": n.redirectUrl || location.href
                    });
                    u(o, n.replace)
                }
            }

            function f(e, n, t) {
                var o;
                return b && (o = {}, o.promise = new b(function(e, n) {
                    o.resolve = e, o.reject = n
                })), m(e, n, function(e) {
                    t && t(e), "SUCCESS" === e ? o && o.resolve(e) : o && o.reject(e)
                }), o ? o.promise : void 0
            }

            function v(e) {
                m("login", e)
            }

            function h(e) {
                return f("login", e)
            }

            function w(e) {
                m("logout", e)
            }

            function E(e) {
                return f("logout", e)
            }
            var b = e.Promise,
                C = e.document,
                L = e.navigator.userAgent,
                x = location.hostname,
                S = (e.location.search, L.match(/WindVane[\/\s]([\d\.\_]+)/)),
                y = L.match(/AliApp\(([^\/]+)\/([\d\.\_]+)\)/i),
                U = !!(y && "TB" === y[1] && S && parseFloat(S[1]) > 5.2),
                k = ["taobao.net", "taobao.com"],
                R = new RegExp("([^.]*?)\\.?((?:" + k.join(")|(?:").replace(/\./g, "\\.") + "))", "i"),
                j = x.match(R) || [],
                T = function() {
                    return (j[2] || "taobao.com").match(/\.?taobao\.net$/) ? "taobao.net" : "taobao.com"
                }(),
                N = function() {
                    var e = T,
                        n = j[1] || "m";
                    return "taobao.net" === e && (n = "waptest"), "m" != n && "wapa" != n && "waptest" != n && (n = "m"), n
                }(),
                A = "login";
            n.login = n.login || {};
            var _ = {
                "loginName": "login.htm",
                "logoutName": "logout.htm",
                "subDomain": N
            };
            n.login.config = _, n.login.isLogin = a, n.login.isLoginAsync = c, n.login.getUserNick = l, n.login.getUserNickAsync = s, n.login.generateUrl = d, n.login.goLogin = v, n.login.goLoginAsync = h, n.login.goLogout = w, n.login.goLogoutAsync = E
        }(window, window.lib || (window.lib = {})), t.exports = window.lib.login
});
define("mui/weex-vue-patch/datahub", function(n, e, t) {
    function i(n, e) {
        if (!(n instanceof e)) throw new TypeError("Cannot call a class as a function")
    }
    var r = function() {
            function n(n, e) {
                for (var t = 0; t < e.length; t++) {
                    var i = e[t];
                    i.enumerable = i.enumerable || !1, i.configurable = !0, "value" in i && (i.writable = !0), Object.defineProperty(n, i.key, i)
                }
            }
            return function(e, t, i) {
                return t && n(e.prototype, t), i && n(e, i), e
            }
        }(),
        u = function() {
            function n() {
                i(this, n)
            }
            return r(n, [{
                "key": "install",
                "value": function(n, e) {
                    var t = {};
                    n.mixin({
                        "created": function() {
                            this._$setItem = function(n, e) {
                                t[n] = e
                            }, this._$getItem = function(n) {
                                return t[n]
                            }
                        }
                    })
                }
            }]), n
        }();
    t.exports = u
});
define("mui/weex-vue-patch/directives", function(n, e, t) {
    function i(n, e, t) {
        return e in n ? Object.defineProperty(n, e, {
            "value": t,
            "enumerable": !0,
            "configurable": !0,
            "writable": !0
        }) : n[e] = t, n
    }

    function a(n, e) {
        if (!(n instanceof e)) throw new TypeError("Cannot call a class as a function")
    }
    var r = function() {
            function n(n, e) {
                for (var t = 0; t < e.length; t++) {
                    var i = e[t];
                    i.enumerable = i.enumerable || !1, i.configurable = !0, "value" in i && (i.writable = !0), Object.defineProperty(n, i.key, i)
                }
            }
            return function(e, t, i) {
                return t && n(e.prototype, t), i && n(e, i), e
            }
        }(),
        o = function() {
            function n(e) {
                a(this, n), this.config = e
            }
            return r(n, [{
                "key": "install",
                "value": function(n, e) {
                    this.appendcells(n, e)
                }
            }, {
                "key": "appendcells",
                "value": function(n, e) {
                    function t(n, e) {
                        n.$dispatch("appendCells", {
                            "index": n.index,
                            "data": e
                        })
                    }

                    function a(n, e, t) {
                        for (var a = [], r = e.slice(0), o = n[t] && n[t].length || 2; r.length;) {
                            var u = r.splice(0, o);
                            a.push({
                                "index": n.index,
                                "name": n.name,
                                "moduleId": n.moduleId,
                                "data": i({}, t, u),
                                "$theme": n.theme,
                                "$config": n.config
                            })
                        }
                        return a
                    }

                    function r(n, e) {
                        var t = [];
                        return n.map(function(n, i) {
                            t = t.concat(n.data[e])
                        }), t
                    }

                    function o(n, e, i, o) {
                        u ? (o = o ? o.map(function(e) {
                            return e.index = n.index, e
                        }) : a(n, i, e), t(n, o)) : (i = o ? r(o, e) : i, n.isH5Appended = !0, n[e] = n[e].concat(i), n.$dispatch("appendCellsFinished", {}))
                    }
                    var u = this.config.isWeex;
                    n.directive("appendcells", {
                        "bind": function(n, e, t, i) {
                            var a, r, u = t.context,
                                c = e.value,
                                f = e.modifiers,
                                l = e.expression,
                                s = e.arg;
                            f.propsData && (r = c), f.watch && !a && (a = u.$watch(l, function(n, e) {
                                r ? o(u, s, "", n) : o(u, s, n)
                            }), u.$on("appendcells.unwatch", function() {
                                setTimeout(function() {
                                    a()
                                }, 2e3)
                            })), !u.isZebraModule && u.isH5Appended || !(c && c.length || r && r.length) || o(u, s, c, r)
                        }
                    })
                }
            }]), n
        }();
    t.exports = o
});
define("mui/weex-vue-patch/event", function(n, e, t) {
    function i(n, e) {
        if (!(n instanceof e)) throw new TypeError("Cannot call a class as a function")
    }
    var a = function() {
            function n(n, e) {
                for (var t = 0; t < e.length; t++) {
                    var i = e[t];
                    i.enumerable = i.enumerable || !1, i.configurable = !0, "value" in i && (i.writable = !0), Object.defineProperty(n, i.key, i)
                }
            }
            return function(e, t, i) {
                return t && n(e.prototype, t), i && n(e, i), e
            }
        }(),
        r = function() {
            function n() {
                i(this, n)
            }
            return a(n, [{
                "key": "install",
                "value": function(n, e) {
                    var t = new n;
                    n.mixin({
                        "created": function() {
                            this.$dispatch = function(n, e) {
                                t.$emit(n, e)
                            }, this.$broadcast = function(n, e) {
                                t.$emit(n, e)
                            }, this.$addEventListener = function(n, e) {
                                t.$on(n, e)
                            }
                        }
                    })
                }
            }]), n
        }();
    t.exports = r
});
define("mui/weex-vue-patch/global", function(e, n, t) {
    function i(e, n) {
        if (!(e instanceof n)) throw new TypeError("Cannot call a class as a function")
    }
    var a = function() {
            function e(e, n) {
                for (var t = 0; t < n.length; t++) {
                    var i = n[t];
                    i.enumerable = i.enumerable || !1, i.configurable = !0, "value" in i && (i.writable = !0), Object.defineProperty(e, i.key, i)
                }
            }
            return function(n, t, i) {
                return t && e(n.prototype, t), i && e(n, i), n
            }
        }(),
        o = function() {
            function e(n) {
                i(this, e), this.config = n
            }
            return a(e, [{
                "key": "install",
                "value": function(e, n) {
                    var t = this,
                        i = t.config.isWeex,
                        a = t.config.isWeb,
                        o = null;
                    e.mixin({
                        "beforeCreate": function() {
                            o || i || !a ? o || a || !i || (o = t.patchWeexGlobal(this)) : o = t.patchWebGlobal(this), this._app = this._app ? Object.assign(this._app, o) : o
                        }
                    })
                }
            }, {
                "key": "patchWebGlobal",
                "value": function(e) {
                    var n = {},
                        t = this.config.zebraUtils || {};
                    n.config = window.weex ? window.weex.config : this.getConfig(), n.zebraUtils = t || {}, n.isH5 = t.env.isWeb(), n.isTmall = t.env.isTmall(), n.isTaobao = t.env.isTaobao();
                    var i = document.querySelector("#vuePatchData"),
                        a = {};
                    try {
                        a = JSON.parse(i.value)
                    } catch (o) {
                        console && console.error("parse VuePatch data error @\u609f\u5bfb", i), console && console.info("\u4e09\u7aef\u7edf\u4e00\u7684\u4ee3\u7801\u4f9d\u8d56solution, \u63d0\u4f9b\u4e00\u4e9b\u5168\u5c40\u53d8\u91cf(#vuePatchData), \u8bf7\u53c2\u8003solution: zebra-native-vue/index.xtpl \u6539\u9020\u3002")
                    }
                    if (a.systemConfig) {
                        var r = a.systemConfig.serverTimeString;
                        a.systemConfig.serverTime = new Date(r).getTime(), a.systemConfig.clientTime = (new Date).getTime()
                    }
                    n.zebraConfig = a.zebraConfig || {}, n.systemConfig = a.systemConfig || {}, n.Dynamic_NotEmptyData = a.Dynamic_NotEmptyData, void 0 !== n.Dynamic_NotEmptyData && "" !== n.Dynamic_NotEmptyData || (n.Dynamic_NotEmptyData = !0), n.config.pageSpm = [a.zebraConfig.spma, a.zebraConfig.spmb, "0", "0"].join("."), n.headerModuleImageHeight = a.headerModuleImageHeight || 300, n.dynamicDataSpace = a.dynamicDataSpace || 200, n.forceDynamicParams = window.$zebra && window.$zebra.forceDynamicParams || {};
                    var c = window._weex_app_ext || {};
                    return this.extendApp(n, c), n
                }
            }, {
                "key": "extendApp",
                "value": function(e, n) {
                    if (e && n)
                        for (var t in n) n.hasOwnProperty(t) && (e[t] ? console.warn("not allow to extend a exist key: ", t) : e[t] = n[t])
                }
            }, {
                "key": "getConfig",
                "value": function() {
                    return {
                        "env": window.WXEnvironment || {},
                        "bundleUrl": window.location.href || ""
                    }
                }
            }, {
                "key": "patchWeexGlobal",
                "value": function(e) {
                    var n = {},
                        t = this.config.require,
                        i = t("zebraUtils"),
                        a = t("zebraConfig"),
                        o = t("zebraDoms"),
                        r = t("systemConfig") || {},
                        c = t("weexAppExt") || {};
                    n.zebraUtils = i, n.zebraConfig = a, n.zebraDoms = o, n.systemConfig = r;
                    try {
                        n.config = weex && weex.config || {}
                    } catch (u) {
                        n.config = e.$getConfig() || {}
                    }
                    return n.isH5 = i.env.isWeb(), n.isTmall = i.env.isTmall(), n.isTaobao = i.env.isTaobao(), n.Dynamic_NotEmptyData = !0, n.config.pageSpm = [a.spma, a.spmb, "0", "0"].join("."), n.headerModuleImageHeight = this.config.headerModuleImageHeight || 300, n.dynamicDataSpace = this.config.dynamicDataSpace || 200, this.extendApp(n, c), n
                }
            }]), e
        }();
    t.exports = o
});
define("mui/weex-vue-patch/index", function(e, n, t) {
    function i(e, n) {
        if (!(e instanceof n)) throw new TypeError("Cannot call a class as a function")
    }
    var a = function() {
            function e(e, n) {
                for (var t = 0; t < n.length; t++) {
                    var i = n[t];
                    i.enumerable = i.enumerable || !1, i.configurable = !0, "value" in i && (i.writable = !0), Object.defineProperty(e, i.key, i)
                }
            }
            return function(n, t, i) {
                return t && e(n.prototype, t), i && e(n, i), n
            }
        }(),
        o = function() {
            var e = null,
                n = function() {
                    function e(n) {
                        i(this, e), this.config = n, this._init()
                    }
                    return a(e, [{
                        "key": "_init",
                        "value": function() {
                            var e = this.config;
                            return e.Vue && e.require ? void this.installPlugins(e) : void(console && console.log("\u521b\u5efa VuePatch \u5b9e\u4f8b\u65f6\u7f3a\u5c11\u5fc5\u8981\u7684\u53c2\u6570: require, Vue, isWeex, isWeb"))
                        }
                    }, {
                        "key": "init",
                        "value": function(e) {
                            var n = this.config;
                            n.isWeex ? e && e() : Promise.all([this.waitPlugins]).then(function(n) {
                                e && e()
                            })["catch"](function(n) {
                                e && e(), console && console.log("VuePatch use plugins failed.")
                            })
                        }
                    }, {
                        "key": "installPlugins",
                        "value": function(e) {
                            var n = this,
                                t = e.require,
                                i = void 0,
                                a = void 0,
                                o = void 0,
                                r = void 0;
                            e.isWeex ? (i = t("mui/weex-vue-patch/global"), a = t("mui/weex-vue-patch/event"), o = t("mui/weex-vue-patch/datahub"), r = t("mui/weex-vue-patch/directives"), this.usePlugins(i, a, o, r)) : this.waitPlugins = new Promise(function(e, i) {
                                t(["mui/weex-vue-patch/global", "mui/weex-vue-patch/event", "mui/weex-vue-patch/datahub", "mui/weex-vue-patch/directives"], function(t, a, o, r) {
                                    n.usePlugins(t, a, o, r, e, i)
                                })
                            })
                        }
                    }, {
                        "key": "usePlugins",
                        "value": function(e, n, t, i, a, o) {
                            try {
                                var r = this.config,
                                    u = this.config.Vue,
                                    c = new n,
                                    s = new e(r),
                                    l = new i(r),
                                    f = new t(r);
                                u.use(c), u.use(f), u.use(l), u.use(s), a && a()
                            } catch (p) {
                                o && o()
                            }
                        }
                    }]), e
                }();
            return {
                "getInstance": function(t) {
                    return e || (e = new n(t)), e
                }
            }
        }();
    t.exports = o
});
define("mui/weex-zebra-utils/index", function(e, t, n) {
    t.version = "4.1.19", n.exports = function(e) {
        function t(r) {
            if (n[r]) return n[r].exports;
            var a = n[r] = {
                exports: {},
                id: r,
                loaded: !1
            };
            return e[r].call(a.exports, a, a.exports, t), a.loaded = !0, a.exports
        }
        var n = {};
        return t.m = e, t.c = n, t.p = "", t(0)
    }([function(e, t, n) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var r = n(1);
        Object.keys(r).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return r[e]
                }
            })
        })
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.extend = t.parseUrl = t.openUrl = t.getSpm = t.checkTheme = t.getConfig = t.$call = t.requireModule = t.require = t.geolocation = t.i18n = t.zebra = t.windvane = t.user = t.url = t.ui = t.tracker = t.tool = t.theme = t.share = t.network = t.navigator = t.modal = t.floorDynamic = t.env = t.dom = t.data = t.ctk = void 0;
        var a = n(2);
        Object.defineProperty(t, "require", {
            enumerable: !0,
            get: function() {
                return a._require
            }
        }), Object.defineProperty(t, "requireModule", {
            enumerable: !0,
            get: function() {
                return a.requireModule
            }
        }), Object.defineProperty(t, "$call", {
            enumerable: !0,
            get: function() {
                return a.$call
            }
        });
        var o = n(3);
        Object.defineProperty(t, "getConfig", {
            enumerable: !0,
            get: function() {
                return o.getConfig
            }
        });
        var i = n(27),
            c = r(i),
            u = n(28),
            s = r(u),
            l = n(42),
            f = r(l),
            p = n(4),
            d = r(p),
            m = n(43),
            g = r(m),
            _ = n(32),
            v = r(_),
            y = n(44),
            h = r(y),
            b = n(29),
            O = r(b),
            P = n(45),
            k = r(P),
            S = n(46),
            j = r(S),
            C = n(17),
            x = r(C),
            R = n(16),
            E = r(R),
            w = n(31),
            I = r(w),
            M = n(15),
            A = r(M),
            T = n(7),
            N = r(T),
            D = n(14),
            L = r(D),
            U = n(47),
            B = r(U),
            F = n(49),
            $ = r(F),
            q = n(51),
            G = r(q);
        t.ctk = c, t.data = s, t.dom = f, t.env = d, t.floorDynamic = g["default"], t.modal = v, t.navigator = h, t.network = O, t.share = k, t.theme = j, t.tool = x, t.tracker = E, t.ui = I, t.url = A, t.user = N, t.windvane = L, t.zebra = B, t.i18n = $, t.geolocation = G, t.checkTheme = j.checkTheme, t.getSpm = E.getSpm, t.openUrl = A.openUrl, t.parseUrl = A.parseUrl, t.extend = x.extend
    }, function(t, n) {
        "use strict";

        function r(t) {
            try {
                if (u(weex) && weex.requireModule) return t = s(t), weex.requireModule(t)
            } catch (n) {}
            try {
                if (u(__weex_require__)) return __weex_require__(t)
            } catch (n) {}
            try {
                if ("_require" === e.name) return e(t)
            } catch (n) {}
            return null
        }

        function a(e) {
            e = "string" == typeof e ? e : "";
            try {
                if (u(weex) && weex.requireModule) return e = s(e), weex.requireModule(e)
            } catch (t) {}
            e = l(e);
            try {
                if (u(weex) && weex.require) return r(e)
            } catch (t) {}
            return r(e)
        }

        function o(e, t, n) {
            var r = void 0,
                o = void 0,
                i = "object" === ("undefined" == typeof e ? "undefined" : p(e)) && "function" == typeof e.$getConfig;
            i ? (r = "string" == typeof t ? t : "", o = "string" == typeof n ? n : "") : (r = "string" == typeof e ? e : "", o = "string" == typeof t ? t : "");
            var c = a(r);
            if (i && !c && e.$call) {
                var u = [r, o];
                return Array.prototype.push.apply(u, Array.prototype.slice.call(arguments, 3)), e.$call.apply(e, u)
            }
            var s = c[o],
                l = i ? 3 : 2;
            return "function" == typeof s ? s.apply({}, Array.prototype.slice.call(arguments, l)) : null
        }

        function i() {
            try {
                if (u(weex) && weex.document) return weex.document
            } catch (e) {}
            try {
                if (u(__weex_document__)) return __weex_document__
            } catch (e) {}
            try {
                if (u(document) && c(document)) return document
            } catch (e) {}
            return null
        }

        function c(e) {
            return !(!e || !e.createTextNode)
        }

        function u(e) {
            return "undefined" != typeof e
        }

        function s(e) {
            return "string" == typeof e ? e.replace(d, "") : ""
        }

        function l(e) {
            return "string" == typeof e ? e.match(RegExp("^" + d)) ? e : d + e : ""
        }
        var f = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
            return typeof e
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        };
        Object.defineProperty(n, "__esModule", {
            value: !0
        });
        var p = "function" == typeof Symbol && "symbol" === f(Symbol.iterator) ? function(e) {
            return "undefined" == typeof e ? "undefined" : f(e)
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : "undefined" == typeof e ? "undefined" : f(e)
        };
        n._require = r, n.requireModule = a, n.$call = o, n.getDocument = i;
        var d = "@weex-module/"
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e) {
            if (_(e)) return e;
            var t = {};
            return t.$call = i.$call, t.$getConfig = o, t.$userTrack = function(e, t, n, r) {
                var a = (0, i.requireModule)("userTrack");
                return a.commit(e, t, n, r)
            }, t.$sendMtop = function(e, t) {
                if ((0, c.isWeb)()) {
                    var n = (0, i.requireModule)("stream");
                    return n.sendMtop(e, t)
                }
                return f.call({
                    "class": "MtopWVPlugin",
                    method: "send",
                    data: e
                }, t)
            }, t.$callWindvane = f.call, t.$openURL = d.openUrl, t.$setSpm = function(e, t) {
                var n = (0, i.requireModule)("pageInfo");
                return n && n.setSpm(e, t)
            }, t.$getUserInfo = s.getUserInfo, t.$login = s.login, t.$logout = s.logout, t
        }

        function o(e) {
            var t = (0, i.getDocument)(),
                n = {};
            try {
                n = WXEnvironment
            } catch (r) {}
            var a = {
                env: n,
                bundleVersion: "",
                bundleUrl: t && t.URL ? t.URL : (0, c.isWeb)() ? window.location.href : ""
            };
            return (0, p.isFunction)(e) && e(a), a
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isContext = void 0, t.getContext = a, t.getConfig = o;
        var i = n(2),
            c = n(4),
            u = n(7),
            s = r(u),
            l = n(14),
            f = r(l),
            p = n(12),
            d = n(15),
            m = n(10),
            g = r(m),
            _ = t.isContext = g.isContext
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a() {
            return "object" === (0, h._typeof)(WXEnvironment) ? WXEnvironment : {}
        }

        function o() {
            return b(["TM", "tm", "tmall", "Tmall", "澶╃尗"])
        }

        function i() {
            return o() && O()
        }

        function c() {
            return o() && !O()
        }

        function u() {
            return b(["DingTalk"])
        }

        function s() {
            return u() && O()
        }

        function l() {
            return u() && !O()
        }

        function f() {
            return b(["TB", "tb", "taobao", "Taobao", "娣樺疂"])
        }

        function p() {
            return b(["JU"])
        }

        function d() {
            return f() && O()
        }

        function m() {
            return f() && !O()
        }

        function g() {
            return b(["HTAO", "Htao", "htao"])
        }

        function _() {
            var e = WXEnvironment,
                t = [];
            return t.push(e.deviceModel + "(" + e.platform + "/" + e.osVersion + ")"), t.push("AliApp(" + e.appName + "/" + e.appVersion + ")"), t.push("Weex/" + e.weexVersion), t.push(e.deviceWidth + "x" + e.deviceHeight), t.join(" ")
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isAndroid = t.isIOS = t.isWeb = t.isClient = void 0, t.getEnv = a, t.isTmall = o, t.isTmallWeb = i, t.isTmallNative = c, t.isDingTalk = u, t.isDingTalkWeb = s, t.isDingTalkNative = l, t.isTaobao = f, t.isJU = p, t.isTaobaoWeb = d, t.isTaobaoNative = m, t.isHtao = g, t.getUA = _;
        var v = n(5),
            y = r(v),
            h = n(6),
            b = t.isClient = y.isApp,
            O = t.isWeb = y.isWeb;
        t.isIOS = y.isIOS, t.isAndroid = y.isAndroid
    }, function(e, t, n) {
        ! function(e, n) {
            n(t)
        }(this, function(e) {
            "use strict";

            function t(e) {
                return Object.prototype.toString.call(e).slice(8, -1).toLowerCase()
            }

            function n(e) {
                return "array" === t(e)
            }

            function r(e) {
                return "string" == typeof e
            }

            function a() {
                return WXEnvironment || {}
            }

            function o(e) {
                e = r(e) ? [e] : e, e = n(e) ? e : [];
                var t = a().appName || "";
                return e.indexOf(t) >= 0
            }

            function i() {
                var e = a().platform || "";
                return "object" == typeof window && "Web" === e
            }

            function c() {
                var e = "iOS",
                    t = a().platform || "",
                    n = a().osName || "";
                return t === e || n === e
            }

            function u() {
                var e = "android",
                    t = a().platform || "",
                    n = a().osName || "";
                return t.toLowerCase() === e || n.toLowerCase() === e
            }
            e.getEnv = a, e.isApp = o, e.isWeb = i, e.isIOS = c, e.isAndroid = u, Object.defineProperty(e, "__esModule", {
                value: !0
            })
        })
    }, function(e, t) {
        "use strict";

        function n(e) {
            return Object.prototype.toString.call(e).slice(8, -1).toLowerCase()
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t._typeof = n
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t) {
            var n = "getUserInfo";
            return (0, p.isContext)(arguments[0]) || (t = arguments[0]), e = (0, _.getContext)(arguments[0]), (0, m.isFunction)(t) ? (0, g.$call)(e, v, n, function(n) {
                n = c(n), t.call(e, n)
            }) : new Promise(function(t, r) {
                return u(e, n, t, r)
            })
        }

        function o(e, t) {
            var n = "login";
            return (0, p.isContext)(arguments[0]) || (t = arguments[0]), e = (0, _.getContext)(arguments[0]), (0, m.isFunction)(t) ? (0, g.$call)(e, v, n, function(n) {
                n = c(n), t.call(e, n)
            }) : new Promise(function(t, r) {
                return u(e, n, t, r)
            })
        }

        function i(e, t) {
            var n = "logout";
            return (0, p.isContext)(arguments[0]) || (t = arguments[0]), e = (0, _.getContext)(arguments[0]), (0, m.isFunction)(t) ? void(0, g.$call)(e, v, n, function(n) {
                n = c(n), t.call(e, n)
            }) : new Promise(function(t, r) {
                return u(e, n, t, r)
            })
        }

        function c(e) {
            if ((0, d.isString)(e)) try {
                e = JSON.parse(e)
            } catch (t) {
                f.error(t)
            }
            return e
        }

        function u(e, t, n, r) {
            return (0, g.$call)(e, v, t, function(t) {
                if ((0, d.isString)(t)) try {
                    t = JSON.parse(t)
                } catch (r) {
                    throw r
                }
                n.call(e, t)
            })
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.getUserInfo = a, t.login = o, t.logout = i;
        var s = n(8),
            l = (r(s), n(9)),
            f = r(l),
            p = n(10),
            d = (n(11), n(13)),
            m = n(12),
            g = n(2),
            _ = n(3),
            v = "user"
    }, function(e, t) {
        "use strict";

        function n() {
            for (var e = arguments[0] + "", t = 1; t < arguments.length; t++) e = e.replace(/\%s/i, arguments[t]);
            return e
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.msg = n;
        var r = t.ERROR_PARAM_IS_REQUIRED = "Param [%s] is required!",
            a = t.ERROR_SHOULD_BE = "%s should be %s.";
        t.ERROR_MISSING_PARAM_CONTEXT = n(a, "First param", "context(ctx)"), t.ERROR_MISSING_PARAM_URL = n(r, "params.url"), t.ERROR_MISSING_PARAM_URL2 = n(r, "url"), t.ERROR_MISSING_PARAM_ALL_LINK = n(r, "all-link"), t.ERROR_MISSING_GOLDLOG = n(r, "window.goldlog.record"), t.ERROR_MESSAGE_SHOULD_BE_STRING = n(a, "message", "string"), t.ERROR_MISSING_CLICKTRACKIINFO = n(r, "clickTrackInfo(string)"), t.ERROR_MISSING_TRACKIINFO = n(r, "trackInfo(string)"), t.ERROR_MISSING_EXPDATA = n(r, "expdata(string)"), t.ERROR_PARAM_SHOULE_BE_OBJECT = "params is not object!", t.ERROR_JSONP_TIMEOUT = "JSONP request to %s timed out", t.ERROR_SHARE_UNSUPPORT = "Currently env doesn`t support Share", t.ERROR_WRONG_URL_SCHEME = "Wrong uri scheme.", t.ERROR_MTOP_REQUEST = "Mtop鎺ュ彛璋冪敤澶辫触", t.ERROR_NEEDS_LOGIN = "Please login first", t.ERROR_MISSING_CTX_OR_EVENT_MODULE = "missing ctx or can not find event module"
    }, function(e, t) {
        (function(e) {
            "use strict";

            function n() {
                !c && console && console.debug && console.debug.apply(this, arguments)
            }

            function r() {
                !c && console && console.log && console.log.apply(this, arguments)
            }

            function a() {
                !c && console && console.info && console.info.apply(this, arguments)
            }

            function o() {
                !c && console && console.warm && console.warm.apply(this, arguments)
            }

            function i() {
                !c && console && console.error && console.error.apply(this, arguments)
            }
            Object.defineProperty(t, "__esModule", {
                value: !0
            }), t.debug = n, t.log = r, t.info = a, t.warm = o, t.error = i;
            var c = !0;
            try {
                c = "test" !== e.NODE_ENV
            } catch (u) {}
        }).call(t, function() {
            return this
        }())
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            var t = (0, a.isPlainObject)(e),
                n = t && (0, o.isFunction)(e.$getConfig);
            return !(!t || !n)
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isContext = r;
        var a = n(11),
            o = n(12)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            return "object" === (0, a._typeof)(e)
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isPlainObject = r;
        var a = n(6)
    }, function(e, t) {
        "use strict";

        function n(e) {
            return "function" == typeof e
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isFunction = n
    }, function(e, t) {
        "use strict";

        function n(e) {
            return "string" == typeof e
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isString = n
    }, function(e, t, n) {
        "use strict";

        function r(e, t) {
            if ((0, i.isWeb)()) return t(new Error(c + " on web"));
            t = (0, o.isFunction)(t) ? t : function() {};
            var n = (0, a.requireModule)("windvane");
            return n ? n.call(e, t) : t(new Error(c))
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.call = r;
        var a = n(2),
            o = n(12),
            i = n(4),
            c = "Cant finding windvane"
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t, n, r) {
            var a = void 0;
            (0, m.isContext)(arguments[0]) && (0, _.isPlainObject)(arguments[1]) ? (t = arguments[1].url, n = arguments[1].spmc, r = arguments[1].spmd, a = arguments[1].target) : !(0, m.isContext)(arguments[0]) && (0, _.isPlainObject)(arguments[0]) ? (t = arguments[0].url, n = arguments[0].spmc, r = arguments[0].spmd, a = arguments[0].target) : !(0, m.isContext)(arguments[0]) && (0, g.isString)(arguments[0]) && (r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, P.getContext)(arguments[0]);
            var i = o(e, t, n, r);
            if (b.isWeb() && window && window.WindVane) "_self" === a ? location.href = i : window.WindVane.call(b.isJU() ? "Base" : "WVNative", "openWindow", {
                url: i
            }, function(e) {}, function(e) {
                location.href = i
            });
            else {
                var c = (0, O.requireModule)("navigator");
                if (c && c.push) c.push({
                    url: i
                });
                else {
                    var u = (0, O.requireModule)("event");
                    if (u && u.openURL) u.openURL(i);
                    else {
                        if (!(0, m.isContext)(e) || !e.$openURL) throw new Error(y.ERROR_MISSING_CTX_OR_EVENT_MODULE);
                        e.$openURL(i)
                    }
                }
            }
            return i
        }

        function o(e, t, n, r) {
            if (!(0, m.isContext)(arguments[0]) && (0, g.isString)(arguments[0]) && (r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, P.getContext)(arguments[0]), !t) throw new Error(y.ERROR_MISSING_PARAM_URL2);
            t = c(t), n = n || 0, r = r || 0;
            var a = new i(t);
            if (!a.params.spm && n && r) {
                var o = d.getSpm(e, n, r);
                a.params.spm = o
            }
            return a.params._from = b.isWeb(e) ? "h5" : "weex", e && e._app && e._app.zebraConfig && (a.params.utpagename = e._app.zebraConfig.pageName || ""), a.toString()
        }

        function i(e) {
            var t = this,
                n = {};
            Object.defineProperty(this, "params", {
                set: function(e) {
                    if ("object" === ("undefined" == typeof e ? "undefined" : f(e))) {
                        for (var t in n) delete n[t];
                        for (var r in e) n[r] = e[r]
                    }
                },
                get: function() {
                    return n
                },
                enumerable: !0
            }), Object.defineProperty(this, "search", {
                set: function(e) {
                    if ("string" == typeof e) {
                        0 === e.indexOf("?") && (e = e.substr(1));
                        var t = e.split("&");
                        for (var r in n) delete n[r];
                        for (var a = 0; a < t.length; a++) {
                            var o = t[a].split("=");
                            if (o[0]) try {
                                n[decodeURIComponent(o[0])] = decodeURIComponent(o[1] || "")
                            } catch (i) {
                                n[o[0]] = o[1] || ""
                            }
                        }
                    }
                },
                get: function() {
                    var e = [];
                    for (var t in n)
                        if (n[t]) try {
                            e.push(encodeURIComponent(t) + "=" + encodeURIComponent(n[t]))
                        } catch (r) {} else try {
                            e.push(encodeURIComponent(t))
                        } catch (r) {}
                    return e.length ? "?" + e.join("&") : ""
                },
                enumerable: !0
            });
            var r = void 0;
            Object.defineProperty(this, "hash", {
                set: function(e) {
                    "string" == typeof e && (e && e.indexOf("#") < 0 && (e = "#" + e), r = e || "")
                },
                get: function() {
                    return r
                },
                enumerable: !0
            }), this.set = function(e) {
                var n = void 0;
                (n = e.match(new RegExp("^([a-z0-9-]+:)?[/]{2}(?:([^@/:?]+)(?::([^@/:]+))?@)?([^:/?#]+)(?:[:]([0-9]+))?([/][^?#]*)?(?:[?]([^?#]*))?(#[^#]*)?$", "i"))) ? (t.protocol = n[1] || "", t.username = n[2] || "", t.password = n[3] || "", t.hostname = t.host = n[4], t.port = n[5] || "", t.pathname = n[6] || "/", t.search = n[7] || "", t.hash = n[8] || "", t.origin = t.protocol + "//" + t.hostname) : (0, k.log)(y.ERROR_WRONG_URL_SCHEME, ": ", e)
            }, Object.defineProperty(this, "toString", {
                value: function() {
                    var n = t.protocol ? t.protocol + "//" : "";
                    return t.username && (n += t.username, t.password && (n += ":" + t.password), n += "@"), n += t.host ? t.host : "", t.port && "80" !== t.port && (n += ":" + t.port), t.pathname && (n += t.pathname), n ? (t.search && (n += t.search), t.hash && (n += t.hash), n) : e
                },
                enumerable: !0
            }), this.set(e.toString())
        }

        function c(e, t) {
            return e = e || "", t = t || "https", "string" == typeof e && e.match(/^\/\//) ? t + ":" + e : "string" == typeof e && e.match(/[a-z0-9\-]\:\/\//) ? e : t + "://" + e
        }

        function u(e) {
            e = (0, g.isString)(e) ? e : "";
            for (var t = {}, n = e.split("&"), r = 0; r < n.length; r++) {
                var a = n[r],
                    o = a.split("="),
                    i = decodeURIComponent(o[0]),
                    c = o[1] ? decodeURIComponent(o[1]) : o[1];
                i && (t[i] = c)
            }
            return t
        }

        function s(e) {
            var t = [];
            for (var n in e) {
                var r = n,
                    a = e[n];
                t.push(encodeURIComponent(r) + "=" + encodeURIComponent(a))
            }
            return t.join("&")
        }
        var l = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
            return typeof e
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        };
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var f = "function" == typeof Symbol && "symbol" === l(Symbol.iterator) ? function(e) {
            return "undefined" == typeof e ? "undefined" : l(e)
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : "undefined" == typeof e ? "undefined" : l(e)
        };
        t.openUrl = a, t.getSpmUrl = o, t.parseUrl = i, t.fixSchema = c, t.paramsToObj = u, t.objToParams = s;
        var p = n(16),
            d = r(p),
            m = n(10),
            g = n(13),
            _ = n(11),
            v = n(8),
            y = r(v),
            h = n(4),
            b = r(h),
            O = n(2),
            P = n(3),
            k = n(9)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t, n, r, a) {
            var o = "0";
            !(0, M.isContext)(arguments[0]) && arguments.length > 2 ? (a = arguments[3], r = arguments[2], n = arguments[1], t = arguments[0]) : !(0, M.isContext)(arguments[0]) && arguments.length < 3 ? (a = arguments[1] + "", r = arguments[0] + "", t = "", n = "") : (0, M.isContext)(arguments[0]) && 3 === arguments.length && (r = t ? t + "" : o, a = n ? n + "" : o, t = "", n = ""), e = (0, U.getContext)(arguments[0]);
            try {
                var i = (0, L.getDocument)(),
                    c = i.nodeMap._root.attr["spm-id"] || i.nodeMap._root.attr.spmId;
                if (c) {
                    var u = c.split(".");
                    t = u[0], n = u[1]
                } else t = i.nodeMap._root.attr.spma, n = i.nodeMap._root.attr.spmb
            } catch (s) {
                F.error(s)
            }
            return e && e._app && e._app.zebraConfig ? (t = e._app.zebraConfig.spma || o, n = e._app.zebraConfig.spmb || o) : (t = t || o, n = n || o, r = r || o, a = a || o), [t, n, r, a].join(".")
        }

        function o() {
            var e = (0, U.getContext)();
            return (0, L.$call)(e, $, "pageAppear")
        }

        function i() {
            var e = (0, U.getContext)();
            return (0, L.$call)(e, $, "pageDisAppear")
        }

        function c() {
            var e = (0, U.getContext)();
            return (0, L.$call)(e, $, "skipPage")
        }

        function u(e, t, n) {
            return (0, M.isContext)(e) || (n = arguments[1], t = arguments[0]), e = (0, U.getContext)(e), (0, M.isPlainObject)(t) && (n = (0, M.clone)(t), t = j()), !!(t && (0, M.isString)(t) && (0, M.isPlainObject)(n)) && (n = k(n, !0), n.customUrl || (n.url = S()), C(e) ? d(e, "enter", t, "", n) : (0, A.isTaobaoNative)(e) ? d(e, "enter", t, "", n) : (0, A.isTmallNative)(e) ? ((0, L.$call)(e, $, "enterEvent", t, n), !0) : m(e, t, "enter", "", "", "", n, !0))
        }

        function s(e, t) {
            return (0, M.isContext)(arguments[0]) || (t = arguments[0]), e = (0, U.getContext)(arguments[0]), !!(0, M.isString)(t) && ((0, L.$call)(e, $, "leaveEvent", t), !0)
        }

        function l(e, t) {
            (0, M.isContext)(arguments[0]) || (t = arguments[0]);
            var n = "";
            return e = (0, U.getContext)(e), t.pageName && (n = t.pageName, delete t.pageName), !!(0, M.isPlainObject)(t) && (0, L.$call)(e, $, "commit", "updateNextProp", n, "", t)
        }

        function f(e, t) {
            return (0, M.isContext)(arguments[0]) || (t = arguments[0]), e = (0, U.getContext)(e), !!(0, M.isPlainObject)(t) && (0, L.$call)(e, $, "updatePageUtparam", JSON.stringify(t))
        }

        function p(e, t) {
            return (0, M.isContext)(arguments[0]) || (t = arguments[0]), e = (0, U.getContext)(e), !!(0, M.isPlainObject)(t) && (0, L.$call)(e, $, "updateNextPageUtparam", JSON.stringify(t))
        }

        function d(e, t, n, r, a) {
            return (0, M.isContext)(arguments[0]) || (a = arguments[3], r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, U.getContext)(arguments[0]), !!((0, M.isString)(t) && (0, M.isString)(n) && (0, M.isString)(r) && (0, M.isPlainObject)(a)) && ((0, L.$call)(e, $, "commit", t, n, r, a), !0)
        }

        function m(e, t, n, r, a, o, i, c) {
            if ((0, M.isContext)(arguments[0]) || (c = arguments[6], i = arguments[5], o = arguments[4], a = arguments[3], r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, U.getContext)(arguments[0]), !c && F.error("姝ゆ帴鍙ｆ湭缁� UT 鍥㈤槦銆佹暟鎹洟闃熼獙璇侊紝鑻ュ洜涓烘鎺ュ彛閫犳垚闂璇疯嚜琛岃礋璐ｃ€�"), t = (0, M.isString)(t) ? t : "", t = t ? t : j(), r = (0, M.isString)(r) ? r : "", a = (0, M.isString)(a) ? a : "", o = (0, M.isString)(o) ? o : "", i = (0, M.isPlainObject)(i) ? i : {}, (0, M.isString)(n)) {
                if ("CLK" === n || "click" === n) return (0, L.$call)(e, $, "commitut", "click", 2101, t, r, "", "", "", i), !0;
                if ("EXP" === n || "pv" === n) return (0, L.$call)(e, $, "commitut", "expose", 2201, t, "", r, a, o, i), !0;
                if ("enter" === n) return (0, L.$call)(e, $, "commitut", (0, A.isTmallNative)(e) ? "enterEvent" : "enter", 2001, t, r, "", "", "", i), !0;
                if ("other" === n || "19999" === n) return "19999" === n ? (0, L.$call)(e, $, "commitEvent", t, 19999, r, a, o, i) : (0, L.$call)(e, $, "commitut", "other", 19999, t, "", r, "", "", i), !0
            }
            return !1
        }

        function g(e, t, n, r, a, o, i) {
            return (0, M.isContext)(arguments[0]) || (i = arguments[5], o = arguments[4], a = arguments[3], r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, U.getContext)(arguments[0]), (0, L.$call)(e, $, "customAdvance", t, n, r, a, o, i)
        }

        function _(e, t, n, r, a, o) {
            (0, M.isContext)(arguments[0]) || (o = arguments[4], a = arguments[3], r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, U.getContext)(arguments[0]);
            var i = !1,
                c = P(t, n);
            return arguments.length >= 4 ? ((0, M.isPlainObject)(r) && (c = (0, M.extend)(c, r)), i = C(e) ? m(e, j(), "EXP", t, "", "", c) : d(e, "expose", j(), "", c)) : i = m(e, t, "EXP", n, r, a, o), i
        }

        function v(e, t, n, r, a) {
            (0, M.isContext)(arguments[0]) || (a = arguments[3], r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, U.getContext)(arguments[0]);
            var o = void 0;
            return arguments.length >= 4 && (o = P(t, n), o._lka = JSON.stringify({
                gokey: r,
                gmkey: a
            })), m(e, arguments.length >= 4 ? j() : t, arguments.length >= 4 ? "19999" : "other", arguments.length >= 4 ? arguments[1] : n, "", "", o ? o : r)
        }

        function y(e, t, n, r) {
            return (0, M.isContext)(arguments[0]) || (r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, U.getContext)(arguments[0]), (0, M.isString)(n) ? d(e, "click", t, n, r) : (r = n, d(e, "click", t, "0", r))
        }

        function h(e, t, n, r, a) {
            (0, M.isContext)(arguments[0]) || (a = arguments[3], r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, U.getContext)(arguments[0]), a = (0, M.isString)(a) ? a : "";
            var o = a.split(";"),
                i = o[0] || "",
                c = o[1] || "",
                u = void 0;
            return i = i.replace(/^gostr\=/, ""), c = c.replace(/^locaid\=/, ""), o = o.slice(2), u = o.join(""), b(e, [i, t, n, r, c].join("."), "CLK", u, "")
        }

        function b(e, t, n, r, a, o) {
            if ((0, M.isContext)(arguments[0]) || (o = arguments[4], a = arguments[3], r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, U.getContext)(arguments[0]), t = (0, M.isString)(t) ? t : "", n = (0, M.isString)(n) ? n : "", r = (0, M.isString)(r) ? r : "", a = (0, M.isString)(a) ? a : "", o = (0, M.isString)(o) ? o : "", (0, A.isWeb)(e)) return O(t, n, r, a);
            var i = "gokey=" + r + "&gmkey=" + n;
            if ("" === n) return !1;
            if ("CLK" === n || "click" === n) {
                var c = P(t, i);
                o && (c.spm = o), c._lka = JSON.stringify({
                    gokey: r,
                    gmkey: n
                });
                var u = j();
                return C(e) ? g(e, u, 2101, t, "", "", c) : y(e, u, t, c)
            }
            return "EXP" === n || "pv" === n ? _(e, t, i, {
                _lka: JSON.stringify({
                    gokey: r,
                    gmkey: n
                })
            }) : v(e, t, i, r, n)
        }

        function O(e, t, n, r) {
            return window && window.goldlog && window.goldlog.record ? (window.goldlog.record(e, t, n, r), !0) : (F.error(D.ERROR_MISSING_GOLDLOG), !1)
        }

        function P(e, t) {
            var n = (0, M.isPlainObject)(t) ? t : (0, T.paramsToObj)(t);
            return {
                logkey: e,
                weex: n.weex ? n.weex : "1",
                autosend: "1",
                url: S(),
                cna: "",
                extendargs: JSON.stringify({}),
                isonepage: 0
            }
        }

        function k(e, t) {
            var n = (0, M.isPlainObject)(e) ? e : (0, T.paramsToObj)(e);
            return n.weex = n.weex ? n.weex : "1", n.autosend = "1", t ? n : (0, T.objToParams)(n)
        }

        function S(e) {
            var t = (0, U.getContext)();
            try {
                var n = t.$getConfig().bundleUrl || "";
                return e ? new T.parseUrl(n) : n
            } catch (r) {
                F.error(r)
            }
            return e ? {} : ""
        }

        function j() {
            var e = S(!0),
                t = e.origin || "",
                n = e.pathname || "";
            return t + n
        }

        function C() {
            var e = (0, U.getContext)(),
                t = e.$getConfig().env.appVersion || "";
            if ((0, A.isTmallNative)(e)) {
                if ((0, A.isAndroid)(e) && x(t, "5.23.0.2")) return !0;
                if ((0, A.isIOS)(e) && x(t, "5.23.0.2")) return !0
            } else if ((0, A.isTaobaoNative)(e)) {
                if ((0, A.isAndroid)(e) && x(t, "5.11.0.7")) return !0;
                if ((0, A.isIOS)(e) && x(t, "5.11.0")) return !0
            }
            return !1
        }

        function x(e, t) {
            e = (0, M.isString)(e) ? e : "", t = (0, M.isString)(t) ? t : "";
            for (var n = e.split(".").slice(0, 4), r = t.split(".").slice(0, 4), a = !0, o = 0; o < 4; o++) n[o] = parseInt(n[o], 10) || 0, r[o] = parseInt(r[o], 10) || 0, a && n[o] !== r[o] && (a = !1);
            if (a) return !1;
            for (var i = 0; i < 4; i++) {
                if (n[i] < r[i]) return !1;
                if (n[i] > r[i]) return !0
            }
            return !0
        }

        function R(e, t) {
            e = (0, M.isString)(e) ? e : "", t = (0, M.isString)(t) ? t : "-----";
            var n = e.split(t);
            return n.splice(1, 0, ""), n
        }

        function E(e, t) {
            if ((0, M.isContext)(arguments[0]) || (t = arguments[0]), e = (0, U.getContext)(arguments[0]), t = (0, M.isString)(t) ? t : "", !t) return new Error(D.ERROR_MISSING_CLICKTRACKIINFO);
            var n = R(t);
            return n[1] = "CLK", n[2] = "clicktrackinfo=" + n[2], b.apply(e, n)
        }

        function w(e, t) {
            if ((0, M.isContext)(arguments[0]) || (t = arguments[0]), e = (0, U.getContext)(arguments[0]), t = (0, M.isString)(t) ? t : "", !t) return new Error(D.ERROR_MISSING_CLICKTRACKIINFO);
            var n = R(t);
            return n[1] = "EXP", b.apply({}, n)
        }

        function I(e, t, n) {
            if ((0, M.isContext)(arguments[0]) || (t = arguments[0], n = arguments[1]), e = (0, U.getContext)(arguments[0]), n = (0, M.isString)(n) ? n : "", t = (0, M.isObject)(t) ? t : void 0, !n) return new Error(D.ERROR_MISSING_TRACKIINFO);
            if (!t) return new Error(D.ERROR_MISSING_EXPDATA);
            var r = R(n);
            return r[1] = "EXP", r[2] = "trackinfo=" + r[2] + "&expdata=" + JSON.stringify(t), b.apply({}, r)
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.getSpm = a, t.pageAppear = o, t.pageDisAppear = i, t.skipPage = c, t.pageEnter = u, t.pageLeave = s, t.updateNextProp = l, t.updatePageUtparam = f, t.updateNextPageUtparam = p, t.commit = d, t.commitEvent = m, t.customAdvance = g, t.exposure = _, t.other = v, t.click = y, t.goldlogClick = h, t.goldlog = b, t.clickTrackInfo = E, t.trackInfo = w, t.biTrackInfo = I;
        var M = n(17),
            A = n(4),
            T = n(15),
            N = n(8),
            D = r(N),
            L = n(2),
            U = n(3),
            B = n(9),
            F = r(B),
            $ = "userTrack"
    }, function(e, t, n) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var r = n(6);
        Object.keys(r).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return r[e]
                }
            })
        });
        var a = n(18);
        Object.keys(a).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return a[e]
                }
            })
        });
        var o = n(21);
        Object.keys(o).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return o[e]
                }
            })
        });
        var i = n(22);
        Object.keys(i).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return i[e]
                }
            })
        });
        var c = n(20);
        Object.keys(c).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return c[e]
                }
            })
        });
        var u = n(10);
        Object.keys(u).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return u[e]
                }
            })
        });
        var s = n(23);
        Object.keys(s).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return s[e]
                }
            })
        });
        var l = n(12);
        Object.keys(l).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return l[e]
                }
            })
        });
        var f = n(24);
        Object.keys(f).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return f[e]
                }
            })
        });
        var p = n(19);
        Object.keys(p).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return p[e]
                }
            })
        });
        var d = n(11);
        Object.keys(d).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return d[e]
                }
            })
        });
        var m = n(13);
        Object.keys(m).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return m[e]
                }
            })
        });
        var g = n(25);
        Object.keys(g).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return g[e]
                }
            })
        });
        var _ = n(26);
        Object.keys(_).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return _[e]
                }
            })
        })
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (!(0, a.isObject)(e)) return e;
            var t = (0, o.isArray)(e) ? [] : {},
                n = void 0,
                i = void 0;
            for (i in e) n = e[i], t[i] = (0, a.isObject)(n) ? r(n) : n;
            return t
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.clone = r;
        var a = n(19),
            o = n(20)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            return !(!(0, o.isPlainObject)(e) && !(0, a.isArray)(e))
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isObject = r;
        var a = n(20),
            o = n(11)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            return "array" === (0, a._typeof)(e)
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isArray = r;
        var a = n(6)
    }, function(e, t, n) {
        "use strict";

        function r(e, t) {
            if (t = (0, o.isFunction)(t) ? t : function() {}, (0, a.isArray)(e))
                for (var n = 0; n < e.length; n++) t(e[n], n);
            else if ((0, i.isPlainObject)(e))
                for (var r in e) t(e[r], r)
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.each = r;
        var a = n(20),
            o = n(12),
            i = n(11)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            for (var t = arguments.length, n = Array(t > 1 ? t - 1 : 0), o = 1; o < t; o++) n[o - 1] = arguments[o];
            if ((0, a.isFunction)(Object.assign)) Object.assign.apply(Object, [e].concat(n));
            else {
                var i = n.shift();
                for (var c in i) e[c] = i[c];
                n.length && r.apply(void 0, [e].concat(n))
            }
            return e
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.extend = r;
        var a = n(12)
    }, function(e, t) {
        "use strict";

        function n(e) {
            var t = void 0;
            for (t in e) return !1;
            return !0
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isEmptyObject = n
    }, function(e, t) {
        "use strict";

        function n(e) {
            return "number" == typeof e
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isNumber = n
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            var t = [];
            if ((0, a.isPlainObject)(e))
                for (var n in e) t.push(n);
            return t
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.keys = r;
        var a = n(11)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (!(0, a.isArray)(e)) return [];
            for (var t = arguments.length, n = Array(t > 1 ? t - 1 : 0), o = 1; o < t; o++) n[o - 1] = arguments[o];
            var i = n.shift();
            return (0, a.isArray)(i) && (i.map(function(t) {
                e.indexOf(t) < 0 && e.push(t)
            }), n.length && r.apply(void 0, [e].concat(n))), e
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.union = r;
        var a = n(20)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e) {
            if (Array.isArray(e)) {
                for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
                return n
            }
            return Array.from(e)
        }

        function o(e) {
            var t, n, r, a = [];
            for (t = 0, n = e.length; t < n; t++) r = e[t], "object" === ("undefined" == typeof r ? "undefined" : g(r)) ? a.push(JSON.stringify(r)) : null === r || void 0 === r ? a.push("") : a.push(r + "");
            for (t = a.length; t--;) a[t] = a[t].replace("|", "銆�").replace(";", "锛�");
            return a
        }

        function i() {
            for (var e = 0, t = new Array(256), n = 0; 256 !== n; ++n) {
                e = n;
                for (var r = 8; r--;) e = 1 & e ? -306674912 ^ e >>> 1 : e >>> 1;
                t[n] = e
            }
            return t
        }

        function c(e) {
            for (var t, n, r = -1, a = 0, o = e.length; a < o;) t = e.charCodeAt(a++), t < 128 ? r = r >>> 8 ^ S[255 & (r ^ t)] : t < 2048 ? (r = r >>> 8 ^ S[255 & (r ^ (192 | t >> 6 & 31))], r = r >>> 8 ^ S[255 & (r ^ (128 | 63 & t))]) : t >= 55296 && t < 57344 ? (t = (1023 & t) + 64, n = 1023 & e.charCodeAt(a++), r = r >>> 8 ^ S[255 & (r ^ (240 | t >> 8 & 7))], r = r >>> 8 ^ S[255 & (r ^ (128 | t >> 2 & 63))], r = r >>> 8 ^ S[255 & (r ^ (128 | n >> 6 & 15 | (3 & t) << 4))], r = r >>> 8 ^ S[255 & (r ^ (128 | 63 & n))]) : (r = r >>> 8 ^ S[255 & (r ^ (224 | t >> 12 & 15))], r = r >>> 8 ^ S[255 & (r ^ (128 | t >> 6 & 63))], r = r >>> 8 ^ S[255 & (r ^ (128 | 63 & t))]);
            return r ^ -1
        }

        function u(e) {
            return o([].concat(a(e), [1])).join("|")
        }

        function s(e, t, n, r) {
            return v.goldlog(e, n, "EXP", "msg=" + encodeURIComponent(t) + "&hash=" + c(t) + "&spm=" + v.getSpm(e), r), c(t)
        }

        function l(e, t) {
            var n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : "",
                r = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : "",
                a = arguments.length > 4 && void 0 !== arguments[4] ? arguments[4] : "";
            if (!(0, b.isContext)(e)) throw new Error(h.ERROR_MISSING_PARAM_CONTEXT);
            if (!t) return !1;
            var o = [t, n, r, a];
            return s(e, u(o), "/codetrack.1.4", "H46836989")
        }

        function f(e, t) {
            var n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : "codetrack.init",
                r = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : {};
            if (!(0, b.isContext)(e)) throw new Error(h.ERROR_MISSING_PARAM_CONTEXT);
            if (!t) return !1;
            r.module = r.module || "", r.type = r.type || "normal", r.msg = r.msg || "", r.version = r.version || "", P || (P = t);
            var a = +new Date;
            k[t] = a;
            var o = t === P ? 0 : a - (k[n || P] || k[P]),
                i = "error" === r.type ? 1 : 0,
                c = [t, n, r.module, r.version, r.msg, Math.max(o, 0), i];
            return s(e, u(c), "/codetrack.1.1", "H46836965")
        }

        function p(e, t) {
            var n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : [];
            if (!(0, b.isContext)(e)) throw new Error(h.ERROR_MISSING_PARAM_CONTEXT);
            if (!t) return !1;
            var r = n;
            return s(e, u(r), "/codetrack.1.3", "H46836988")
        }

        function d(e, t) {
            var n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : "";
            if (!(0, b.isContext)(e)) throw new Error(h.ERROR_MISSING_PARAM_CONTEXT);
            if (!t) return !1;
            var r = [t, n, +new Date - O];
            return s(e, u(r), "/codetrack.1.2", "H46836987")
        }
        var m = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
            return typeof e
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        };
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var g = "function" == typeof Symbol && "symbol" === m(Symbol.iterator) ? function(e) {
            return "undefined" == typeof e ? "undefined" : m(e)
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : "undefined" == typeof e ? "undefined" : m(e)
        };
        t.hash = c, t.formatLogInfo = u, t.domTrack = l, t.ctkTrack = f, t.tesTrack = p, t.spyTrack = d;
        var _ = n(16),
            v = r(_),
            y = n(8),
            h = r(y),
            b = n(17),
            O = +new Date,
            P = "",
            k = {},
            S = i()
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            return e && e.__esModule ? e : {
                "default": e
            }
        }

        function a(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function o(e) {
            var t = {
                    isDynamic: !1,
                    dataCount: 0,
                    data: []
                },
                n = function(e) {
                    if (!l.isPlainObject(e)) return !1;
                    var t = "jsonp" === e.__data_type,
                        n = "ald" === e.__data_source,
                        r = l.isString(e.__data_url),
                        a = l.isPlainObject(e.__data_param),
                        o = l.isObject(e.__data_default);
                    return !!(t && n && r && a && o)
                },
                r = function a(e) {
                    return l.isObject(e) && (n(e) ? (t.isDynamic = !0, t.dataCount = e.__data_default.length, t.data = e.__data_default) : l.each(e, function(e) {
                        return l.isPlainObject(e) ? n(e) ? (t.isDynamic = !0, t.data = l.isArray(e.__data_default) ? e.__data_default : [e.__data_default], t.dataCount = t.data.length) : t = a(e) : l.isArray(e) && (e[0] && n(e[0]) ? (t.isDynamic = !0, t.data = l.isArray(e[0].__data_default) ? e[0].__data_default : [e[0].__data_default], t.dataCount = t.data.length) : (t.dataCount = e.length, t.data = e)), t
                    })), t
                };
            return r(e)
        }

        function i(e, t, n) {
            if (!l.isObject(t)) return null;
            if (!(0, j.isContext)(e) || !e._app) throw new Error(b.ERROR_MISSING_PARAM_CONTEXT);
            return n = n || {}, new P["default"]({
                data: t,
                ctx: e,
                config: {
                    mtop: n.mtop || !0,
                    timeout: n.timeout,
                    duplication: n.duplication,
                    params: n.params || {},
                    mtopApiName: n.mtopApiName,
                    forceBackupHasParam: n.forceBackupHasParam,
                    backupParams: n.backupParams,
                    closeBackup: n.closeBackup,
                    closeAllBackup: n.closeAllBackup || !1,
                    plugins: n.plugins
                }
            })
        }

        function c(e, t) {
            if (!(0, j.isContext)(e) || !e._app) throw new Error(b.ERROR_MISSING_PARAM_CONTEXT);
            return t = t || {}, new S["default"]({
                ctx: e,
                mtop: t.mtop || !0,
                timeout: t.timeout,
                duplication: t.duplication,
                params: t.params || {},
                mtopApiName: t.mtopApiName,
                forceBackupHasParam: t.forceBackupHasParam !== !1,
                backupParams: t.backupParams,
                closeBackup: t.closeBackup,
                closeAllBackup: t.closeAllBackup || !1,
                plugins: t.plugins
            })
        }

        function u(e, t) {
            function n(e) {
                var t = this,
                    n = ("[object Array]" === Object.prototype.toString.call(e.ret) ? e.ret[0] : e.ret) || "FAIL_SYSTEM_ERROR:绯荤粺閿欒",
                    r = n.split("::");
                return {
                    code: r[0],
                    msg: r[1] || t.config.errMsg
                }
            }

            function r(t) {
                var r = n(t);
                switch (r.code) {
                    case "FAIL_SYS_SESSION_EXPIRED":
                    case "ERR_SID_INVALID":
                        throw new Error(b.ERROR_NEEDS_LOGIN);
                    case "SUCCESS":
                        return _.toast(e, c, 1), {
                            success: !0,
                            code: r.code,
                            msg: r.msg
                        };
                    case "FAIL_SYSTEM_ERROR":
                    case "FAIL_BIZ_EXCEPTION":
                    case "FAIL_BIZ_PARAM_ERROR":
                    case "FAIL_BIZ_RESULT_EMPTY":
                    case "FAIL_BIZ_CHECK_MTEE":
                    case "FAIL_BIZ_INTERFACE_ERROR":
                    case "FAIL_BIZ_SYSTEM_ERROR":
                    case "FAIL_BIZ_FIND_ACTIVITY_ERROR":
                    case "FAIL_BIZ_CHECK_FIND_BUYER_RECORD_ERROR":
                    case "FAIL_BIZ_CHECK_COUPON_ERROR":
                    case "FAIL_BIZ_ACTIVITY_APPLY_ILLEGAL":
                        return _.toast(e, i, 1), {
                            success: !1,
                            code: r.code,
                            msg: "System Error"
                        };
                    default:
                        return _.toast(e, r.msg, 1), {
                            success: !1,
                            code: r.code,
                            msg: "Biz Error"
                        }
                }
            }

            function a(e, t, n) {
                return y.getUserInfo(e).then(function(r) {
                    if (r.isLogin === !0 || "true" === r.isLogin) {
                        t = l.isString(t) ? t : "";
                        var a = new m.parseUrl(t),
                            o = a.params.activity_id || a.params.activityId || "",
                            i = a.params.seller_id || a.params.sellerId || "";
                        if (o && i) {
                            var c = {
                                api: "mtop.alibaba.marketing.couponcenter.applycouponforchannel",
                                v: "1.0",
                                ecode: 0,
                                isSec: 1,
                                secType: 2,
                                sessionOption: "AutoLoginOnly",
                                param: {
                                    activityId: o,
                                    sellerId: i,
                                    ua: n,
                                    asac: "1A17718T967KGL79J6T03W"
                                }
                            };
                            return p.mtop(e, c)
                        }
                        throw new Error("No Necessary Coupon Param")
                    }
                    throw new Error(b.ERROR_NEEDS_LOGIN)
                }).then(r, function(e) {
                    if (e.message) throw new Error(e.message);
                    return r(e)
                })["catch"](function(t) {
                    throw t.message === b.ERROR_NEEDS_LOGIN ? y.login(e) : _.toast(e, i), t
                })
            }

            function o() {
                return new Promise(function(e, t) {
                    x.isWeb() && window.feloader ? window.feloader.getScript("//g.alicdn.com/sd/ctl/ctl.js?" + (new Date).valueOf(), function() {
                        window.ctl.config("h5"), window.ctl.ready(e)
                    }) : t()
                })
            }
            if (!e) throw new Error(b.ERROR_MISSING_PARAM_CONTEXT);
            var i = "鎶辨瓑锛屽ソ澶氫汉鍦ㄦ帓闃熼鍒革紝璇风◢鍊欏啀璇曡瘯鍚э紒",
                c = "鎭枩鎮紝棰嗗埜鎴愬姛锛�";
            return x.isWeb() ? window.ctl ? a(e, t, window.ctl.getUA()) : o().then(function() {
                return a(e, t, window.ctl.getUA())
            }) : a(e, t)
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.checkDynamicData = o, t.dynamicData = i, t.dynamicChannel = c, t.getCoupon = u;
        var s = n(17),
            l = a(s),
            f = n(29),
            p = a(f),
            d = n(15),
            m = a(d),
            g = n(31),
            _ = a(g),
            v = n(7),
            y = a(v),
            h = n(8),
            b = a(h),
            O = n(33),
            P = r(O),
            k = n(41),
            S = r(k),
            j = n(3),
            C = n(4),
            x = a(C)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t, n, r) {
            function a() {
                for (var e = 0; e < arguments.length; e++) try {
                    arguments[e] = (0, _.isString)(arguments[e]) ? JSON.parse(arguments[e]) : arguments[e]
                } catch (t) {
                    d.error(t)
                }
                return arguments
            }
            if ((0, m.isContext)(arguments[0]) || (0, g.isPlainObject)(arguments[1]) || (r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, k.getContext)(arguments[0]), s.isWeb()) {
                var o = "mui/mtop/index";
                t.data = t.param, delete t.param;
                var i = function(e, t) {
                    var n = !window.lib.mtop;
                    (0, v.isFunction)(t) && n ? window.require(e, t) : t(window.lib.mtop)
                };
                return (0, v.isFunction)(n) ? i(o, function(e) {
                    var a = [t, n];
                    r && a.push(r), e.request.apply({}, a)
                }) : new Promise(function(e, n) {
                    i(o, function(r) {
                        r.request(t).then(e, n)
                    })
                })
            }
            var c = (0, P.requireModule)("mtop"),
                u = (0, v.isFunction)(e.$sendMtop) ? e.$sendMtop.bind(e) : c.request;
            if (t.param) {
                var l = t.param;
                l.isAsyn || (l.isAsyn = 1), l.isAsy || (l.isAsy = "1")
            } else {
                var f = {
                    isAsyn: 1,
                    isAsy: "1"
                };
                t.param = f
            }
            return (0, v.isFunction)(n) ? u(t, function() {
                var t = a.apply(this, arguments);
                n.apply(e, t)
            }, function(t) {
                n.apply(e, [null, t])
            }) : new Promise(function(n, r) {
                u(t, function() {
                    var t = a.apply(this, arguments);
                    n.apply(e, t)
                }, function(e) {
                    r(e)
                })
            })
        }

        function o(e, t, n, r) {
            function a(e) {
                try {
                    e = e.data ? e.data : e, e = e.trim(), e = e.match(/^{/) ? e.replace(/;$/g, "") : e.match(/^.*?[A-Za-z0-9_\.]*\[\"[A-Za-z0-9_\,]*\"\]\(/) ? e.replace(/^.*?[A-Za-z0-9_\.]*\[\"[A-Za-z0-9_\,]*\"\]\(|\);|\)$/g, "") : e.replace(/^[.\n]*?.*?[A-Za-z0-9_\.]*\(|\);|\)$/g, ""), e = JSON.parse(e)
                } catch (t) {}
                return e
            }

            function o() {
                return "jsonp_" + Date.now() % 1e5 + Math.ceil(1e3 * Math.random())
            }

            function i(e) {
                e.url = (0, _.isString)(e.url) ? e.url : "", e.body = (0, g.isPlainObject)(e.body) ? e.body : {};
                var n = new c.parseUrl(e.url);
                return n.params = (0, y.clone)((0, h.extend)(n.params, e.body)), "JSONP" !== t.method || n.params.callback || (n.params.callback = o()), n.toString()
            }

            function u(e, t) {
                if ((0, _.isString)(t)) try {
                    t = JSON.parse(t)
                } catch (n) {}
                return "JSONP" === e.method && (t = a(t)), t
            }(0, m.isContext)(arguments[0]) || (0, g.isPlainObject)(arguments[1]) || (r = arguments[2], n = arguments[1], t = arguments[0]), e = (0, k.getContext)(arguments[0]), t = (0, _.isString)(t) ? {
                url: t
            } : t, t = (0, g.isPlainObject)(t) ? t : {}, t.method = t.method || "GET", t.method = t.method.toUpperCase();
            var l = (0, P.requireModule)("stream"),
                p = l ? l.fetch : e.$sendHttp;
            if (!t.url) throw new Error(f.ERROR_MISSING_PARAM_URL);
            if (t.url = c.fixSchema(t.url), s.isWeb(e) && "JSONP" === t.method) return (0, O.jsonp)(t, n);
            var d = function() {
                    (0, v.isFunction)(r) && r.apply(e, arguments)
                },
                S = (0, y.clone)(t);
            if (S.method.match(/GET|JSONP/i)) {
                S.method = "GET", S.url = i(S);
                try {
                    delete S.body
                } catch (j) {}
            }
            if (!(0, v.isFunction)(n)) return new Promise(function(n, r) {
                function a(a) {
                    a = u(t, a), "error" === (0, b._typeof)(a) ? r.call(e, a) : n.call(e, a)
                }
                p.apply(e, [S, a, d])
            });
            var C = function(e) {
                e = u(t, e), n(e)
            };
            p.apply(e, [S, C, d])
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.mtop = a, t.fetch = o;
        var i = n(15),
            c = r(i),
            u = n(4),
            s = r(u),
            l = n(8),
            f = r(l),
            p = n(9),
            d = r(p),
            m = n(10),
            g = n(11),
            _ = n(13),
            v = n(12),
            y = n(18),
            h = n(22),
            b = n(6),
            O = n(30),
            P = n(2),
            k = n(3)
    }, function(e, t) {
        "use strict";

        function n(e, t) {
            function n(e) {
                return Object.prototype.toString.call(e).slice(8, -1).toLowerCase()
            }
            e = "string" == typeof e ? {
                url: e
            } : e, e = "object" === n(e) ? e : {};
            var r = e.url || "";
            return r ? "function" == typeof t ? window.require("mui/fetch/jsonp", function(n) {
                n(r, e).then(function(e) {
                    return e.json()
                }).then(function(e) {
                    t(e)
                })["catch"](function() {
                    t("JSONP request to " + r + " error")
                })
            }) : new Promise(function(t, n) {
                window.require("mui/fetch/jsonp", function(a) {
                    a(r, e).then(function(e) {
                        t(e.json())
                    })["catch"](function() {
                        n(new Error("JSONP request to " + r + " error"))
                    })
                })
            }) : Promise.reject(new Error("Param [params.url] is required!"))
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.jsonp = n
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t, n) {
            return (0, c.isContext)(arguments[0]) || (n = arguments[1], t = arguments[0]), e = (0, u.getContext)(arguments[0]), i.toast(e, {
                message: t,
                duration: n
            })
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.toast = a;
        var o = n(32),
            i = r(o),
            c = n(10),
            u = n(3)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t) {
            !(0, c.isContext)(arguments[0]) && (0, l.isPlainObject)(arguments[0]) && (t = arguments[0]), e = (0, p.getContext)(arguments[0]), t = (0, l.isPlainObject)(t) ? t : {};
            var n = (0, s.isNumber)(t.duration) ? t.duration : 2,
                r = (0, u.isString)(t.message) ? t.message : i.ERROR_MESSAGE_SHOULD_BE_STRING;
            return (0, f.$call)(e, d, "toast", {
                message: r,
                duration: n
            })
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.toast = a;
        var o = n(8),
            i = r(o),
            c = n(10),
            u = n(13),
            s = n(24),
            l = n(11),
            f = n(2),
            p = n(3),
            d = "modal"
    }, function(e, t, n) {
        "use strict";

        function r(e, t) {
            if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
        }
        var a = function() {
                function e(e, t) {
                    for (var n = 0; n < t.length; n++) {
                        var r = t[n];
                        r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, r.key, r)
                    }
                }
                return function(t, n, r) {
                    return n && e(t.prototype, n), r && e(t, r), t
                }
            }(),
            o = n(17),
            i = n(34),
            c = n(9),
            u = n(37),
            s = o.isPlainObject,
            l = function() {
                function e(t) {
                    r(this, e);
                    var n = this,
                        a = u.checkPlugins(t.config);
                    a ? u.usePlugins(a, "argumentPreprocess", t, function(e) {
                        n._init(e)
                    }) : n._init(t)
                }
                return a(e, [{
                    key: "_init",
                    value: function(e) {
                        if (this.cfg = e, this.config = e.config || {}, !this.cfg.data) throw new Error("conf鍙傛暟蹇呴』涓簀son");
                        return this.ready = !0, this._fire(), this
                    }
                }, {
                    key: "_stringfiyToResult",
                    value: function(e) {
                        var t = e.data;
                        return this._getData(t, e)
                    }
                }, {
                    key: "_getData",
                    value: function(e, t) {
                        var n = this;
                        if (this._parse(e), o.isEmptyObject(n.request.requestStack)) o.isFunction(t.callback) && t.callback(e, []);
                        else {
                            var r = this.cfg.ctx;
                            r._app.dynamicDataCnt ? r._app.dynamicDataCnt = r._app.dynamicDataCnt + 1 : r._app.dynamicDataCnt = 1, r._app.dynamicDataSpace || (r._app.dynamicDataSpace = 100), setTimeout(function() {
                                n.request.run(function(a) {
                                    var i = [];
                                    o.each(a, function(t, r) {
                                        t.exposureObj && i.push(t.exposureObj), o.each(n.xPathList, function(n, a) {
                                            if (r === n) {
                                                var o = a.split("."),
                                                    i = o.pop(),
                                                    c = e;
                                                o.forEach(function(e) {
                                                    e && (c = c[e])
                                                }), c[i] = t
                                            }
                                        })
                                    }), n.xPathList = {}, r._app.dynamicDataCnt = r._app.dynamicDataCnt - 1, o.isFunction(t.callback) && t.callback(e, i)
                                })
                            }.bind(this), (r._app.dynamicDataCnt - 1) * r._app.dynamicDataSpace)
                        }
                    }
                }, {
                    key: "_parse",
                    value: function(e, t) {
                        var n = this;
                        t = t || "";
                        var r = this._checkTagIsDynamic(e);
                        return r ? void this._push(e, r, t) : void o.each(e, function(e, r) {
                            n._isTag(e) && n._parse(e, t + "." + r)
                        })
                    }
                }, {
                    key: "_isTag",
                    value: function(e) {
                        return Array.isArray(e) || s(e)
                    }
                }, {
                    key: "_push",
                    value: function(e, t, n) {
                        this.xPathList[n] = t, this.request.push(e[0])
                    }
                }, {
                    key: "_checkTagIsDynamic",
                    value: function(e) {
                        var t = Array.isArray(e);
                        return !!t && (!(e.length > 1) && this._checkDataConfig(e[0]))
                    }
                }, {
                    key: "then",
                    value: function(e, t) {
                        var n = this;
                        return n.ready ? n._fire(e, t) : n.cache = {
                            callback: e,
                            errCallback: t
                        }, n
                    }
                }, {
                    key: "_fire",
                    value: function(e, t) {
                        var n = this;
                        e ? n._then(e, t) : n.cache && n.cache.callback ? n._then(n.cache.callback, n.cache.errCallback) : t && t()
                    }
                }, {
                    key: "_then",
                    value: function(e, t) {
                        var n = this,
                            r = parseInt(this.config.timeout, 10);
                        return r = r ? r > 100 ? r : 1e3 * r : 3e3, this.request = new i({
                            timeout: r,
                            ctx: n.cfg.ctx,
                            closeAllBackup: this.config.closeAllBackup || !1,
                            duplication: !!this.config.duplication,
                            mtop: this.config.mtop,
                            params: s(this.config.params) ? this.config.params : {},
                            mtopApiName: this.config.mtopApiName || "mtop.taobao.aladdin.service.AldRecommendService.tmall.recommend2",
                            forceBackupHasParam: this.config.forceBackupHasParam || !1,
                            backupParams: this.config.backupParams,
                            closeBackup: this.config.closeBackup
                        }), this.cfg.callback = e, this.cfg.errCallback = t, this.xPathList = {}, this._stringfiyToResult(this.cfg), this
                    }
                }, {
                    key: "catch",
                    value: function() {
                        return c.log("zebraDynamic鐨刢atch鏂规硶鐩墠鍙槸涓€涓┖鍑芥暟閬垮厤鎶ラ敊,娌℃湁浠讳綍鐢ㄥ"), this
                    }
                }, {
                    key: "_checkDataConfig",
                    value: function(e) {
                        if (!e || !s(e)) return !1;
                        var t = e.__data_type && e.__data_source && e.__data_url && e.__data_param && s(e.__data_param) && e.__data_default;
                        return !!t && e.__data_param.appId
                    }
                }]), e
            }();
        e.exports = l
    }, function(e, t, n) {
        "use strict";

        function r(e, t) {
            if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
        }
        var a = function() {
                function e(e, t) {
                    for (var n = 0; n < t.length; n++) {
                        var r = t[n];
                        r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, r.key, r)
                    }
                }
                return function(t, n, r) {
                    return n && e(t.prototype, n), r && e(t, r), t
                }
            }(),
            o = n(35),
            i = n(17),
            c = n(36),
            u = n(15),
            s = n(27),
            l = {
                timeout: 3e3,
                duplication: !1,
                mtop: !1,
                params: {}
            },
            f = (new Date).getTime(),
            p = /^(https?:|)\/\/(.*)data\.jsonp$/i,
            d = function(e) {
                return "[object Object]" === Object.prototype.toString.call(e)
            },
            m = function(e) {
                return "[object String]" === Object.prototype.toString.call(e)
            },
            g = function(e) {
                return e && m(e) && p.test(e)
            },
            _ = function(e) {
                var t = [];
                return e.forEach(function(e) {
                    t.indexOf(e) === -1 && t.push(e)
                }), t
            },
            v = function() {
                function e(t) {
                    var n = this;
                    if (r(this, e), this.cfg = Object.assign({}, l, t), this.cfg.forceBackupHasParam === !0 && !this.cfg.closeBackup) {
                        var a = [];
                        Object.keys(this.cfg.backupParams).forEach(function(e) {
                            void 0 !== n.cfg.params[e] ? (a.push(e), n.cfg.backupParams[e] = n.cfg.params[e]) : delete n.cfg.backupParams[e]
                        }), this.cfg.params.isbackup = !0, this.cfg.params.backupParams = a.join(",")
                    }
                    this.requestStack = {}, this.backUpDataList = {}, this.resultDataList = {};
                    var o = t.ctx;
                    o._app.__pvuuid ? f = o._app.__pvuuid : o._app.__pvuuid = f
                }
                return a(e, [{
                    key: "push",
                    value: function(e) {
                        var t = e.__data_url,
                            n = e.__data_param && e.__data_param.appId;
                        if (n) switch (this.checkBottomConfigVersion(e.__data_default)) {
                            case "v3":
                                this.isV3Config || (this.isV3Config = !0);
                                break;
                            case "v2":
                                this.backUpDataList[n] = {
                                    url: e.__data_default.url,
                                    length: e.__data_default.length
                                };
                                break;
                            case "v1":
                            default:
                                this.backUpDataList[n] = e.__data_default
                        }
                        this.requestStack[t] ? (this.requestStack[t].dataParam = this._mergeParams(this.requestStack[t].dataParam, e.__data_param), this.requestStack[t].dataDetection = this._mergeArray(this.requestStack[t].dataDetection, e.__data_detection)) : this.requestStack[t] = {
                            dataParam: e.__data_param,
                            dataType: this._getDataType(e.__data_type),
                            dataDetection: e.__data_detection || []
                        }, this.cfg.duplication || (this.requestStack[t].dataParam = this.requestStack[t].dataParam || {}, this.requestStack[t].dataParam._pvuuid = f)
                    }
                }, {
                    key: "checkBottomConfigVersion",
                    value: function(e) {
                        return d(e) && e.url && g(e.url) ? "v2" : d(e) && !e.url && e.length ? "v3" : "v1"
                    }
                }, {
                    key: "_mergeParams",
                    value: function(e, t) {
                        for (var n in e) e[n] && t[n] && ("" + e[n]).indexOf(t[n]) < 0 && (e[n] += "," + t[n]);
                        return Object.assign(t, e)
                    }
                }, {
                    key: "_mergeArray",
                    value: function(e, t) {
                        return t && t.forEach(function(t) {
                            e.indexOf(t) || e.push(t)
                        }), e
                    }
                }, {
                    key: "_getDataType",
                    value: function(e) {
                        var t = void 0;
                        switch (e) {
                            case "jsonp":
                                t = "jsonp";
                                break;
                            default:
                                t = "jsonp"
                        }
                        return t
                    }
                }, {
                    key: "_mergeData",
                    value: function(e, t, n) {
                        var r = this,
                            a = "string" == typeof e ? _(e.split(",")) : [e],
                            o = {},
                            c = function(e) {
                                Object.keys(e).forEach(function(t) {
                                    r.resultDataList[t] = e[t]
                                }), n && n(r.resultDataList)
                            };
                        a.forEach(function(e) {
                            o[e] = !1
                        }), a.forEach(function(e) {
                            var n = t && t[e],
                                a = i.isObject(n) && n.data,
                                s = i.isObject(n) && n.exposureParam,
                                l = i.isObject(n) && n.success,
                                f = {
                                    goldKeyPrefix: i.isObject(n) && n.goldKeyPrefix,
                                    goldKeySuffix: i.isObject(n) && n.goldKeySuffix,
                                    algorithmLog: i.isObject(n) && n.algorithmLog
                                };
                            if (f.algorithmLog && i.isFunction(r.cfg.ctx.$getConfig) && r.cfg.ctx.$getConfig().bundleUrl) {
                                var p = new u.parseUrl(r.cfg.ctx.$getConfig().bundleUrl),
                                    d = p.params;
                                f.algorithmLog += "&spm=" + d.spm
                            }
                            var m = r.cfg.isChannel ? n : a;
                            r._connectTagData(e, m, r.backUpDataList[e], s, l, function(t) {
                                var n = r.cfg.isChannel ? {} : [];
                                o[e] = t || n, t && f.goldKeyPrefix && f.goldKeySuffix && f.algorithmLog && (o[e].exposureObj = f);
                                var a = !0;
                                Object.keys(o).forEach(function(e) {
                                    o[e] || (a = !1)
                                }), a === !0 && c(o)
                            })
                        })
                    }
                }, {
                    key: "_connectTagData",
                    value: function(e, t, n, r, a, o) {
                        var c = this,
                            u = "" + a != "true" || c.cfg.ctx._app.Dynamic_NotEmptyData && t && t.length < 1;
                        "" + a != "true" ? t && i.isObject(s) && i.isFunction(s.tesTrack) && s.tesTrack(c.cfg.ctx, e + "error", [e, "error", "request." + (c.cfg.mtop ? "mtop" : "http") + ".ald", {
                            type: "dataError",
                            desc: "杩斿洖鏁版嵁寮傚父锛氳繑鍥瀞uccess瀛楁涓篺alse"
                        }, {
                            api: c.cfg.mtop ? c.cfg.mtopApiName : "//ald.taobao.com/recommend2.htm",
                            appId: e
                        }]) : (!t || "number" == typeof t.length && 0 === t.length || t && t.data && "number" == typeof t.data.length && 0 === t.data.length) && i.isObject(s) && i.isFunction(s.tesTrack) && s.tesTrack(c.cfg.ctx, e + "error", [e, "error", "request." + (c.cfg.mtop ? "mtop" : "http") + ".ald", {
                            type: "dataWarning",
                            desc: "鎺ュ彛鍙兘寮傚父锛氳繑鍥瀞uccess瀛楁涓簍rue锛屼絾鏁版嵁涓虹┖"
                        }, {
                            api: c.cfg.mtop ? c.cfg.mtopApiName : "//ald.taobao.com/recommend2.htm",
                            appId: e
                        }]), c.cfg.closeAllBackup || t && !u ? i.isFunction(o) && o(t) : c._dataBack(n, e, o)
                    }
                }, {
                    key: "_isCDNBack",
                    value: function(e) {
                        return d(e) && e.url && e.length
                    }
                }, {
                    key: "_dataBack",
                    value: function(e, t, n) {
                        var r = this;
                        if (this.cfg.closeBackup || this.cfg.closeAllBackup) return void(i.isFunction(n) && n(e));
                        if (this.isV3Config || this.cfg.forceBackupHasParam) {
                            var a = {
                                appId: t,
                                backupParams: this.cfg.backupParams
                            };
                            c.getBottom(this.cfg.ctx, a, function(e) {
                                e || i.isObject(s) && i.isFunction(s.tesTrack) && s.tesTrack(r.cfg.ctx, t + "error", [t, "error", "request.http.oss", {
                                    type: "backupErrorV3",
                                    desc: "鎵撳簳鏂规3.0鑾峰彇鏁版嵁澶辫触"
                                }, {
                                    api: c.createBottomUrl(a),
                                    appId: t
                                }]);
                                var o = c.mergeData(r.cfg.ctx, [t], e, !0, r.cfg.isChannel);
                                o && o[t] && (o[t].isBackupData = !0), i.isFunction(n) && n(o && o[t])
                            })
                        } else if (this._isCDNBack(e)) try {
                            o("http", {
                                ctx: this.cfg.ctx,
                                url: e.url,
                                dataType: "jsonp",
                                params: {},
                                timeout: 2e3,
                                callback: "callback_" + t.replace(/-/g, "_"),
                                realCallback: function(e) {
                                    r.cfg.isChannel ? i.isFunction(n) && n(e) : i.isFunction(n) && n(e.data)
                                },
                                errCallback: function() {
                                    i.isObject(s) && i.isFunction(s.tesTrack) && s.tesTrack(r.cfg.ctx, t + "error", [t, "error", "request.http.oss", {
                                        type: "backupErrorV2",
                                        desc: "鎵撳簳鏂规2.0鑾峰彇鏁版嵁澶辫触"
                                    }, {
                                        api: e.url,
                                        appId: t
                                    }]), i.isFunction(n) && n(void 0)
                                }
                            })
                        } catch (u) {
                            i.isObject(s) && i.isFunction(s.tesTrack) && s.tesTrack(r.cfg.ctx, t + "error", [t, "error", "request.http.oss", {
                                type: "backupErrorV2",
                                desc: "鎵撳簳鏂规2.0鑾峰彇鏁版嵁澶辫触"
                            }, {
                                api: e.url,
                                appId: t
                            }]), i.isFunction(n) && n(e)
                        } else i.isFunction(n) && n(e)
                    }
                }, {
                    key: "reset",
                    value: function() {
                        this.requestStack = {}, this.backUpDataList = {}, this.resultDataList = {}
                    }
                }, {
                    key: "run",
                    value: function(e) {
                        var t = this,
                            n = this.requestStack,
                            r = Object.assign({}, t.cfg),
                            a = {};
                        i.each(n, function(n, c) {
                            a[c] = !1;
                            var u = Object.assign(t.cfg.params, n.dataParam),
                                l = n.dataParam && n.dataParam.appId,
                                f = function(n) {
                                    t._mergeData(l, n, function(n) {
                                        delete t.requestStack[c], i.isEmptyObject(t.requestStack) && (i.isFunction(e) && e(n), t.reset())
                                    })
                                };
                            o(r.mtop ? "mtop" : "http", {
                                ctx: r.ctx,
                                url: c,
                                api: t.cfg.mtopApiName || void 0,
                                dataType: n.dataType,
                                params: u,
                                timeout: r.timeout,
                                realCallback: function(e) {
                                    f(e)
                                },
                                errCallback: function(e) {
                                    i.isObject(s) && i.isFunction(s.tesTrack) && s.tesTrack(t.cfg.ctx, u.appId + "error", [u.appId, "error", "request." + (t.cfg.mtop ? "mtop" : "http") + ".ald", {
                                        type: "fetchError",
                                        desc: "鑾峰彇鏁版嵁澶辫触锛�" + e
                                    }, {
                                        args: u,
                                        api: t.cfg.mtop ? t.cfg.mtopApiName : c,
                                        appId: u.appId
                                    }]), f(void 0)
                                }
                            })
                        })
                    }
                }]), e
            }();
        e.exports = v
    }, function(e, t, n) {
        "use strict";
        var r = n(29),
            a = n(17),
            o = {
                api: "mtop.taobao.aladdin.service.AldRecommendService.tmall.recommend2",
                dataType: "jsonp",
                v: "1.0",
                ecode: 0
            };
        e.exports = function(e, n) {
            switch (e) {
                case "mtop":
                    return t.mtop(n);
                case "http":
                default:
                    return t.http(n)
            }
        }, t.http = function(e) {
            a.isPlainObject(e.ctx._app.forceDynamicParams) && (e.params = Object.assign({}, e.params, e.ctx._app.forceDynamicParams));
            var t = {
                url: e.url,
                method: e.dataType || "JSONP",
                body: e.params,
                timeout: e.timeout
            };
            e.callback && (t.callback = e.callback);
            try {
                return r.fetch(t, function(t) {
                    var n = !0;
                    t && a.isPlainObject(t) || (n = !1), n ? a.isFunction(e.realCallback) && e.realCallback(t) : a.isFunction(e.errCallback) && e.errCallback()
                })
            } catch (n) {
                a.isFunction(e.errCallback) && e.errCallback(n)
            }
        }, t.mtop = function(e) {
            var t = Object.assign({}, o, {
                param: e.params,
                api: e.api || o.api,
                timer: e.timeout || 3e3
            });
            a.isPlainObject(e.ctx._app.forceDynamicParams) && (t.param = Object.assign({}, t.param, e.ctx._app.forceDynamicParams));
            try {
                return r.mtop(t, function(t) {
                    t && t.ret && t.ret[0] && t.ret[0].indexOf("SUCCESS") >= 0 ? a.isFunction(e.realCallback) && e.realCallback(t.data.resultValue) : a.isFunction(e.errCallback) && e.errCallback(t.ret && t.ret[0] || "Mtop鎺ュ彛璋冪敤澶辫触")
                }, function(t) {
                    a.isFunction(e.errCallback) && e.errCallback(t || "Mtop鎺ュ彛璋冪敤澶辫触")
                })
            } catch (n) {
                a.isFunction(e.errCallback) && e.errCallback(n || "Mtop鎺ュ彛璋冪敤澶辫触")
            }
        }
    }, function(e, t, n) {
        "use strict";
        var r = n(35),
            a = n(17),
            o = /^(http:|https:)?\/\//,
            i = {
                getBottom: function(e, t, n) {
                    var r = this;
                    return r.getBottomData(e, r.getBottomUrl(t), t, n)
                },
                getBottomUrl: function(e) {
                    var t = this.createBottomUrl(e);
                    return t
                },
                createBottomUrl: function() {
                    var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
                    if (!e.appId) return !1;
                    var t = e.appId.split(","),
                        n = e.backupParams || {},
                        r = "//aladdin.alicdn.com/bottom/" + t.sort().join("/");
                    return Object.keys(n).sort().forEach(function(e) {
                        r += "/" + e + "=" + n[e]
                    }), r += "/data.jsonp"
                },
                createBottomCallback: function() {
                    var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
                    if (!e.appId) return !1;
                    var t = e.appId.replace(/-/g, "_").split(",");
                    t = t.sort();
                    var n = e.backupParams || {},
                        r = "";
                    Object.keys(n).sort().forEach(function(e) {
                        r += "_" + e + "_" + n[e]
                    });
                    var a = "callback_" + t.join(",") + r;
                    return a
                },
                getBottomData: function(e, t, n, o) {
                    return r("http", {
                        ctx: e,
                        url: t,
                        dataType: "JSONP",
                        params: {},
                        timeout: 2e3,
                        callback: this.createBottomCallback(n),
                        realCallback: function(e) {
                            a.isFunction(o) && o(e)
                        },
                        errCallback: function() {
                            a.isFunction(o) && o()
                        }
                    })
                },
                mergeData: function(e, t, n, r, a) {
                    var o = {},
                        i = this;
                    if (n) return n && t.forEach(function(c) {
                        1 === t.length && r ? a ? o[c] = n : (o[c] = n.data, i.exposure(e, n.exposureParam)) : n[c] && n[c].hasOwnProperty("data") && (a ? o[c] = n[c] : o[c] = n[c].data)
                    }), o
                },
                exposure: function(e, t) {
                    t && o.test(t) && r("http", {
                        ctx: e,
                        url: t,
                        dataType: "GET"
                    })
                }
            };
        e.exports = i
    }, function(e, t, n) {
        "use strict";
        var r = n(17),
            a = n(38),
            o = n(39),
            i = n(40),
            c = {
                region: a,
                userId: o,
                chaoshi: i
            };
        e.exports = {
            checkPlugins: function(e) {
                var t = ["region", "userId"],
                    n = e ? e.plugins : t;
                return n + "" != "false" && (r.isArray(n) ? n.concat([]) : t)
            },
            usePlugins: function(e, t, n, a) {
                var o = this,
                    i = e.shift();
                if (i) {
                    var u = c[i];
                    u && r.isFunction(u[t]) ? u[t](n, function() {
                        o.usePlugins(e, t, n, a)
                    }) : o.usePlugins(e, t, n, a)
                } else a && a(n)
            }
        }
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            for (var t = i && i.getAllObjects || function() {}, n = t() || [], r = n.length, a = 0; a < r; a++)
                if (n[a].name === e) return n[a].value;
            return ""
        }

        function a() {
            var e = "hng",
                t = {},
                n = {
                    CN: 1,
                    HK: 81e4,
                    TW: 71e4,
                    MO: 82e4,
                    MY: 125,
                    SG: 190,
                    KR: 198,
                    AU: 16,
                    NZ: 150,
                    CA: 37,
                    US: 228,
                    JP: 104
                },
                a = 999999,
                o = r(e);
            if (o) {
                o = decodeURIComponent(o).split("|")[0];
                var i = n[o] || a;
                t = {
                    country_id: o,
                    countryCode: i
                }, t._cacheLevel = "hngCookie"
            } else t && (t._cacheLevel = "memory");
            return t
        }
        var o = n(2),
            i = o.requireModule("cookie");
        e.exports = {
            argumentPreprocess: function() {
                var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
                    t = arguments[1],
                    n = a(),
                    r = e.config || {};
                n.countryCode && 1 !== n.countryCode && (r.params = Object.assign({
                    smAreaId: n.countryCode
                }, r.params || {}), r.backupParams = Object.assign({
                    smAreaId: n.countryCode
                }, r.backupParams || {}), r.forceBackupHasParam = !0), t && t(e)
            }
        }
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            var t = "";
            try {
                var n = i.getContext(),
                    r = n.$getConfig().bundleUrl,
                    a = new o.parseUrl(r);
                t = a.params[e]
            } catch (c) {}
            return t
        }
        var a = n(2),
            o = n(15),
            i = n(3),
            c = a.requireModule("storage");
        e.exports = {
            argumentPreprocess: function() {
                var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
                    t = arguments[1];
                if (!c) return void(t && t(e));
                var n = e.config || {},
                    a = r("_oneId"),
                    o = r("alideviceid");
                a ? (n.params = Object.assign({
                    _oneId: a
                }, n.params || {}), c.removeItem("alideviceid"), c.setItem("_oneId", a), t && t(e)) : o ? (n.params = Object.assign({
                    alideviceid: o
                }, n.params || {}), c.removeItem("_oneId"), c.setItem("alideviceid", o), t && t(e)) : c.getItem("_oneId", function(r) {
                    "success" === r.result && r.data ? (n.params = Object.assign({
                        _oneId: r.data
                    }, n.params || {}), t && t(e)) : c.getItem("alideviceid", function(r) {
                        "success" === r.result && r.data && (n.params = Object.assign({
                            alideviceid: r.data
                        }, n.params || {})), t && t(e)
                    })
                })
            }
        }
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            for (var t = c && c.getAllObjects || function() {}, n = t() || [], r = n.length, a = 0; a < r; a++)
                if (n[a].name === e) return n[a].value;
            return ""
        }

        function a(e) {
            e.params = Object.assign({
                smAreaId: d
            }, e.params || {}), e.backupParams = Object.assign({
                smAreaId: d
            }, e.backupParams || {}), e.forceBackupHasParam = !0
        }

        function o() {
            return new Promise(function(e) {
                var t = this;
                f ? e(f) : (f = new Promise(function(e, n) {
                    s.mtop(t, {
                        api: "mtop.chaoshi.supermarket.getSiteInfoV11",
                        v: "1.0",
                        param: {
                            sysId: "index",
                            device: "phone",
                            h5: !0
                        },
                        ecode: 0
                    }).then(function(t) {
                        e(t)
                    }, function(e) {
                        n()
                    })
                }), e(f))
            })
        }
        var i = n(2),
            c = i.requireModule("cookie"),
            u = i.requireModule("storage"),
            s = n(29),
            l = "chaoshi_site_info_weex_stroage",
            f = void 0,
            p = "110100",
            d = void 0;
        e.exports = {
            argumentPreprocess: function() {
                var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
                    t = arguments[1];
                e.config = e.config || {};
                var n = e.config;
                return d ? (a(n), void(t && t(e))) : void u.getItem(l, function(i) {
                    d = r("sm4") || "";
                    var c = void 0;
                    if (i && i.data && i.data.length >= 2) {
                        c = i.data;
                        try {
                            c = JSON.parse(c)
                        } catch (i) {
                            c = {}
                        }
                    } else c = {};
                    return c.smAreaId && c.isCorrect && (d || (d = c.smAreaId), c.smAreaId == d) ? (a(n), void(t && t(e))) : void o().then(function(r) {
                        var o = r ? r.data || {} : {};
                        d = o.districtId || o.cityId || p, o.smAreaId = d, a(n), o.tpId && o.cityId && (o.isCorrect = !0), u.setItem(l, JSON.stringify(o)), t && t(e)
                    }, function() {
                        d = p, a(n), u.setItem(l, JSON.stringify({
                            smAreaId: d
                        })), t && t(e)
                    })
                })
            }
        }
    }, function(e, t, n) {
        "use strict";

        function r(e, t) {
            if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
        }
        var a = function() {
                function e(e, t) {
                    for (var n = 0; n < t.length; n++) {
                        var r = t[n];
                        r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, r.key, r)
                    }
                }
                return function(t, n, r) {
                    return n && e(t.prototype, n), r && e(t, r), t
                }
            }(),
            o = n(17),
            i = n(34),
            c = n(9),
            u = n(37),
            s = o.isPlainObject,
            l = o.isArray,
            f = {
                url: "//ald.taobao.com/recommend2.htm?",
                dataType: "jsonp"
            },
            p = function() {
                function e(t) {
                    r(this, e);
                    var n = this;
                    return new Promise(function(e, r) {
                        var a = u.checkPlugins(t);
                        a ? u.usePlugins(a, "argumentPreprocess", {
                            data: {},
                            ctx: t.ctx || {},
                            config: t
                        }, function(t) {
                            n._init(t.config), n._then(e, r)
                        }) : (n._init(t), n._then(e, r))
                    })
                }
                return a(e, [{
                    key: "_init",
                    value: function(e) {
                        if (!this._checkDataConfig(e.ctx, e)) throw new Error("config鍙傛暟蹇呴』涓簀son锛屾垨浼犲叆淇℃伅涓嶅叏");
                        return e.params.appId = "" + e.params.appId, e = Object.assign({}, f, e), this.cfg = e, this
                    }
                }, {
                    key: "_push",
                    value: function(e) {
                        var t = {
                            __data_param: e.params,
                            __data_type: e.dataType,
                            __data_url: e.url,
                            __data_default: {
                                length: 50
                            }
                        };
                        this.request.push(t)
                    }
                }, {
                    key: "_checkDataConfig",
                    value: function(e, t) {
                        return t.params && t.params.appId ? "string" == typeof t.params.appId || !l(t.params.appId) || (e.nativeLog && e.nativeLog("浼犲叆鐨刟ppId蹇呴』涓哄瓧绗︿覆鎴栨暟缁�"), !1) : (e.nativeLog && e.nativeLog("蹇呴』浼犲叆appId"), !1)
                    }
                }, {
                    key: "_getData",
                    value: function(e, t) {
                        var n = this;
                        return this._push(e), n.request.run(t)
                    }
                }, {
                    key: "_then",
                    value: function(e) {
                        var t = parseInt(this.cfg.timeout, 10),
                            n = this.cfg;
                        return t = t ? t > 100 ? t : 1e3 * t : 3e3, this.request = new i({
                            ctx: n.ctx,
                            isChannel: !0,
                            timeout: t,
                            closeAllBackup: n.closeAllBackup || !1,
                            closeBackup: n.closeBackup || !1,
                            duplication: !!n.duplication,
                            mtop: !!n.mtop,
                            mtopApiName: n.mtopApiName || "mtop.taobao.aladdin.service.AldRecommendService.tmall.recommend2",
                            params: n.params,
                            backupParams: s(n.backupParams) ? n.backupParams : {},
                            forceBackupHasParam: n.forceBackupHasParam || !1
                        }), this._getData(n, e), this
                    }
                }, {
                    key: "catch",
                    value: function() {
                        return c.log("zebraDynamic鐨刢atch鏂规硶鐩墠鍙槸涓€涓┖鍑芥暟閬垮厤鎶ラ敊,娌℃湁浠讳綍鐢ㄥ"), this
                    }
                }]), e
            }();
        e.exports = p
    }, function(e, t, n) {
        "use strict";

        function r(e, t) {
            function n(e) {
                var t = (0, c.extend)({}, e);
                return delete t.pureChildren, delete t.children, t
            }
            t = (0, a.isNumber)(t) ? t : -1;
            var r = [];
            if (!(0, o.isPlainObject)(e)) return r;
            e.level = 0;
            var u = [e];
            do {
                var s = u.shift();
                if (s) {
                    var l = (0, i.isArray)(s.pureChildren) ? s.pureChildren : [];
                    if (r.push(n(s)), l.length) {
                        for (var f = s.level + 1, p = l.length; p--;) l[p].level = f;
                        (t && s.level < t || t < 0) && (u = u.concat(l))
                    }
                }
            } while (u.length > 0);
            return r
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.flattenDom = r;
        var a = n(24),
            o = n(11),
            i = n(20),
            c = n(22)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t) {
            if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
        }
        var o = function() {
                function e(e, t) {
                    for (var n = 0; n < t.length; n++) {
                        var r = t[n];
                        r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, r.key, r)
                    }
                }
                return function(t, n, r) {
                    return n && e(t.prototype, n), r && e(t, r), t
                }
            }(),
            i = n(17),
            c = r(i),
            u = n(29),
            s = r(u),
            l = n(8),
            f = r(l),
            p = s.fetch,
            d = s.mtop,
            m = void 0,
            g = void 0,
            _ = function() {
                function e(t, n) {
                    if (a(this, e), !n.ossData || 0 === n.ossData.length) return nativeLog && nativeLog("浼犲叆ossData涓嶈兘涓簎ndefine鎴栫┖鏁扮粍"), Promise.reject(new Error("浼犲叆ossData涓嶈兘涓簎ndefine鎴栫┖鏁扮粍"));
                    m = t._app, g = m.__pvuuid, m.__pvuuid || (g = m.__pvuuid = (new Date).getTime());
                    var r = this;
                    return r.ctx = t, r.ossData = n.ossData, r.dynamicData = null, r.exposures = [], r.useMtop = !0, r.loadFloorDynamicData().then(function(e) {
                        return m.g_openSendExposure && r.sendExposure(), e
                    })
                }
                return o(e, [{
                    key: "loadFloorDynamicData",
                    value: function() {
                        var e = this,
                            t = e.ossData,
                            n = t[0].__data_default,
                            r = t[0].__data_url,
                            a = t[0].__data_param;
                        return a._pvuuid = g, this.dynamicIO(e.ctx, e.useMtop ? "mtop" : "http", {
                            url: r,
                            params: a
                        }).then(function(t) {
                            return e.parseResult(t)
                        }).then(function(t) {
                            return t.length !== n.length ? e.getDefaultData() : t
                        })["catch"](function(t) {
                            return e.getDefaultData()
                        })
                    }
                }, {
                    key: "getDefaultData",
                    value: function() {
                        var e = this,
                            t = e.ossData,
                            n = t[0].__data_default;
                        if (c.isArray(n)) return n = e.formatDefaultData(n), Promise.resolve(n);
                        var r = t[0].__data_param.appId;
                        return p(e.ctx, {
                            url: n.url,
                            method: "jsonp",
                            callback: "callback_" + r.replace(/-/g, "_"),
                            timeout: 1e4
                        }).then(function(t) {
                            return e.parseResult(t)
                        })
                    }
                }, {
                    key: "parseResult",
                    value: function(e) {
                        var t = this,
                            n = t.ossData,
                            r = n[0].__data_param.appId;
                        return new Promise(function(n, a) {
                            e = e[r] || e;
                            var o = e.data;
                            c.isArray(o) && o.length || n([]), t.exposures.push(e.exposureParam), o.forEach(function(e) {
                                t.formatFloorData(e)
                            }), n(o)
                        })
                    }
                }, {
                    key: "formatFloorData",
                    value: function(e) {
                        var t = this;
                        for (var n in e) {
                            var r = e[n];
                            e.hasOwnProperty(n) && c.isObject(r) && r.hasOwnProperty("data") && (t.exposures.push(r.exposureParam), r = r.data), e[n] = r
                        }
                    }
                }, {
                    key: "formatDefaultData",
                    value: function(e) {
                        for (var t = 0; t < e.length; t++) {
                            var n = e[t];
                            for (var r in n) {
                                var a = n[r];
                                c.isArray(a) && a.length && (a = a[0].__data_default), n[r] = a
                            }
                        }
                        return e
                    }
                }, {
                    key: "sendExposure",
                    value: function() {
                        var e = this,
                            t = parseInt(m.sendDelayTime) || 0;
                        setTimeout(function() {
                            e.exposures.forEach(function(t) {
                                t && p(e.ctx, t)
                            })
                        }, t)
                    }
                }, {
                    key: "dynamicIO",
                    value: function(e, t, n) {
                        return this.mtopRequst(e, n)
                    }
                }, {
                    key: "httpRequst",
                    value: function(e, t) {
                        return p(e, {
                            url: t.url,
                            method: "jsonp",
                            body: t.params
                        })
                    }
                }, {
                    key: "mtopRequst",
                    value: function(e, t) {
                        var n = c.extend({}, v, {
                            param: t.params
                        });
                        return d(e, n).then(function(e) {
                            if (e && e.ret && e.ret[0] && e.ret[0].indexOf("SUCCESS") >= 0) return e.data.resultValue;
                            throw new Error(f.ERROR_MTOP_REQUEST)
                        })
                    }
                }]), e
            }(),
            v = {
                api: "mtop.taobao.aladdin.service.AldRecommendService.tmall.recommend2",
                dataType: "jsonp",
                v: "1.0",
                ecode: 0
            };
        e.exports = _
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t, n) {
            var r = "setNavBarTitle";
            p.isContext(arguments[0]) || p.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(arguments[0]), t = p.isPlainObject(t) ? t : {};
            var a = e.$getConfig().bundleUrl.indexOf("wh_notSetTitle=1") > 0;
            return p.isFunction(n) ? a ? n({}) : (0, g.$call)(e, _, r, t, n) : new Promise(function(n, o) {
                a ? n({}) : (0, g.$call)(e, _, r, t, n)
            })
        }

        function o(e, t, n) {
            var r = "push";
            return p.isContext(arguments[0]) || p.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(e), t = p.isPlainObject(t) ? t : {}, p.isFunction(n) ? ((0, g.$call)(e, _, r, t, n), null) : new Promise(function(n, a) {
                (0, g.$call)(e, _, r, t, n)
            })
        }

        function i(e, t, n) {
            var r = "pop";
            return p.isContext(arguments[0]) || p.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(e), t = p.isPlainObject(t) ? t : {}, p.isFunction(n) ? ((0, g.$call)(e, _, r, t, n), null) : new Promise(function(n, a) {
                (0, g.$call)(e, _, r, t, n)
            })
        }

        function c(e, t, n) {
            var r = "setNavBarRightItem";
            return p.isContext(arguments[0]) || p.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(e), t = p.isPlainObject(t) ? t : {}, p.isFunction(n) ? ((0, g.$call)(e, _, r, t, n), null) : new Promise(function(n, a) {
                (0, g.$call)(e, _, r, t, n)
            })
        }

        function u(e, t, n) {
            var r = "clearNavBarRightItem";
            return p.isContext(arguments[0]) || p.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(e), p.isFunction(n) ? ((0, g.$call)(e, _, r, t, n), null) : new Promise(function(n, a) {
                (0, g.$call)(e, _, r, t, n)
            })
        }

        function s(e, t, n) {
            var r = "setNavBarMoreItem";
            return p.isContext(arguments[0]) || p.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(e), t = p.isPlainObject(t) ? t : {}, p.isFunction(n) ? ((0, g.$call)(e, _, r, t, n), null) : new Promise(function(n, a) {
                (0, g.$call)(e, _, r, t, n)
            })
        }

        function l(e, t, n) {
            var r = "clearNavBarMoreItem";
            return p.isContext(arguments[0]) || p.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(e), p.isFunction(n) ? ((0, g.$call)(e, _, r, t, n), null) : new Promise(function(n, a) {
                (0, g.$call)(e, _, r, t, n)
            })
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.setTitle = a, t.push = o, t.pop = i, t.setNavBarRightItem = c, t.clearNavBarRightItem = u, t.setNavBarMoreItem = s, t.clearNavBarMoreItem = l;
        var f = n(17),
            p = r(f),
            d = n(8),
            m = (r(d), n(3)),
            g = n(2),
            _ = "navigator"
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t, n) {
            return u.isContext(arguments[0]) || u.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(e), t = u.isPlainObject(t) ? t : {}, l.isTaobao(e) ? this.taobao.call(e, t, n) : l.isTmall(e) ? (t["pc-image"] = t["pc-image"] || t.image, t["mobile-image"] = t["mobile-image"] || t.image, t["iphone-link"] = t["iphone-link"] || t.url, t["ipad-link"] = t["ipad-link"] || t.url, t["tmallapp-link"] = t["tmallapp-link"] || t.url, t["aliapp-link"] = t["aliapp-link"] || t.url, t["mobile-link"] = t["mobile-link"] || t.url, t["pc-link"] = t["pc-link"] || t.url, t["all-link"] = t["all-link"] || t.url, t["share-title"] = t["share-title"] || t.title, t["share-intro"] = t["share-intro"] || t.text, this.tmall.call(e, t, n)) : new Error(p.ERROR_SHARE_UNSUPPORT)
        }

        function o(e, t, n) {
            if (u.isContext(arguments[0]) || u.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(arguments[0]), n = (0, d.isFunction)(n) ? n : function() {}, !u.isPlainObject(t)) throw new Error(p.ERROR_PARAM_SHOULE_BE_OBJECT);
            if (!t["all-link"]) throw new Error(p.ERROR_MISSING_PARAM_ALL_LINK);
            return (0, g.$call)(e, _, v, t, n)
        }

        function i(e, t, n) {
            if (u.isContext(arguments[0]) || u.isPlainObject(arguments[1]) || (n = arguments[1], t = arguments[0]), e = (0, m.getContext)(arguments[0]), n = (0, d.isFunction)(n) ? n : function() {}, !u.isPlainObject(t)) throw new Error(p.ERROR_PARAM_SHOULE_BE_OBJECT);
            return (0, g.$call)(e, _, v, t, n)
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.toggle = a, t.tmall = o, t.taobao = i;
        var c = n(17),
            u = r(c),
            s = n(4),
            l = r(s),
            f = n(8),
            p = r(f),
            d = n(12),
            m = n(3),
            g = n(2),
            _ = "share",
            v = "doShare"
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            if (e && e.__esModule) return e;
            var t = {};
            if (null != e)
                for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
            return t["default"] = e, t
        }

        function a(e, t, n) {
            2 === arguments.length && (n = arguments[1], t = arguments[0]), e = (0, l.getContext)(e), t = u.isPlainObject(t) ? t : {}, n = u.isPlainObject(n) ? n : {};
            var r = u.clone(t);
            for (var a in n) {
                var o = n[a];
                o && (u.isString(o) && o.match(/px$/i) && (o = e ? i(e, o) : parseInt(o, 10) || 0), r[a] = o)
            }
            return r
        }

        function o(e, t) {
            e = u.isPlainObject(e) ? e : {}, t = u.isPlainObject(t) ? t : {};
            var n = u.clone(e);
            for (var r in t) {
                var a = u.isPlainObject(t[r]) && t[r].title ? t[r].value : t[r];
                "undefined" !== u._typeof(a) && "" !== a && (n[r] = a)
            }
            return n
        }

        function i(e, t) {
            return u.isContext(arguments[0]) || (t = arguments[0]), e = (0, l.getContext)(arguments[0]), u.isString(t) ? t = parseInt(t, 10) || 0 : u.isNumber(t) || (t = 0), 2 * t
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.checkTheme = a, t.checkConfig = o, t.toPixel = i;
        var c = n(17),
            u = r(c),
            s = n(4),
            l = (r(s), n(3))
    }, function(e, t, n) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var r = n(48);
        Object.keys(r).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return r[e]
                }
            })
        });
        var a = n(28);
        Object.keys(a).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return a[e]
                }
            })
        });
        var o = n(46);
        Object.keys(o).forEach(function(e) {
            "default" !== e && "__esModule" !== e && Object.defineProperty(t, e, {
                enumerable: !0,
                get: function() {
                    return o[e]
                }
            })
        })
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            var t = !1;
            if (!(0, o.isString)(e)) return t;
            for (var n = (0, a._require)("zebraDoms") || [], r = 0; r < n.length; r++)
                if (n[r].name === e) {
                    t = !0;
                    break
                }
            return t
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.isModuleExist = r;
        var a = n(2),
            o = n(13)
    }, function(e, t, n) {
        "use strict";

        function r(e) {
            return function() {
                var t = [].slice.call(arguments),
                    n = t[0];
                return "string" != typeof n ? "[" + ("undefined" == typeof n ? "undefined" : o(n)) + "]" : (t[0] = e[n] || n, i.format.apply(null, t))
            }
        }
        var a = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
            return typeof e
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        };
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var o = "function" == typeof Symbol && "symbol" === a(Symbol.iterator) ? function(e) {
            return "undefined" == typeof e ? "undefined" : a(e)
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : "undefined" == typeof e ? "undefined" : a(e)
        };
        t.init = r;
        var i = n(50)
    }, function(e, t) {
        "use strict";

        function n(e) {
            if ("string" != typeof e) {
                for (var t = new Array(arguments.length), n = 0; n < arguments.length; n++) t[n] = o(arguments[n]);
                return t.join(" ")
            }
            var a = arguments.length;
            if (1 === a) return e;
            for (var i = "", c = 1, u = 0, s = 0; s < e.length;) {
                if (37 === e.charCodeAt(s) && s + 1 < e.length) switch (e.charCodeAt(s + 1)) {
                    case 100:
                        if (c >= a) break;
                        u < s && (i += e.slice(u, s)), i += Number(arguments[c++]), u = s += 2;
                        continue;
                    case 106:
                        if (c >= a) break;
                        u < s && (i += e.slice(u, s)), i += r(arguments[c++]), u = s += 2;
                        continue;
                    case 115:
                        if (c >= a) break;
                        u < s && (i += e.slice(u, s)), i += String(arguments[c++]), u = s += 2;
                        continue;
                    case 37:
                        u < s && (i += e.slice(u, s)), i += "%", u = s += 2;
                        continue
                }++s
            }
            for (0 === u ? i = e : u < e.length && (i += e.slice(u)); c < a;) {
                var l = arguments[c++];
                i += null === l || "object" !== ("undefined" == typeof l ? "undefined" : o(l)) && "symbol" !== ("undefined" == typeof l ? "undefined" : o(l)) ? " " + l : " " + ("undefined" == typeof l ? "undefined" : o(l))
            }
            return i
        }

        function r(e) {
            try {
                return JSON.stringify(e)
            } catch (t) {
                return "[Circular]"
            }
        }
        var a = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
            return typeof e
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        };
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var o = "function" == typeof Symbol && "symbol" === a(Symbol.iterator) ? function(e) {
            return "undefined" == typeof e ? "undefined" : a(e)
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : "undefined" == typeof e ? "undefined" : a(e)
        };
        t.format = n
    }, function(e, t, n) {
        "use strict";

        function r(e, t, n) {
            try {
                navigator && "https:" === location.protocol.toLowerCase() ? navigator.geolocation.getCurrentPosition(e, t, n) : t(new Error("geolocation feature only available in secure contexts"))
            } catch (r) {
                a(e, t, n)
            }
        }

        function a(e, t, n) {
            var r = (0, o.requireModule)("windvane");
            r && r.call2 ? r.call2("WVLocation.getLocation", n, e, t) : t(new Error("unkndown error when getCurrentPosition"))
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.getCurrentPosition = r;
        var o = n(2)
    }])
}), define("mui/weex-zebra-utils", function(e, t, n) {
    n.exports = e("mui/weex-zebra-utils/index")
}), define("@ali/WeexUtils", function(e, t, n) {
    n.exports = e("mui/weex-zebra-utils/index")
}), define("weex-zebra-utils", function(e, t, n) {
    n.exports = e("mui/weex-zebra-utils/index")
}), define("zebraUtils", function(e, t, n) {
    n.exports = e("mui/weex-zebra-utils/index")
});
define("mui/weex-component-link/index", ["mui/weex-zebra-utils/index"], function(t, e, i) {
    "use strict";
    var r = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
        return typeof t
    } : function(t) {
        return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
    };
    i.exports = function(t) {
        function e(r) {
            if (i[r]) return i[r].exports;
            var n = i[r] = {
                "exports": {},
                "id": r,
                "loaded": !1
            };
            return t[r].call(n.exports, n, n.exports, e), n.loaded = !0, n.exports
        }
        var i = {};
        return e.m = t, e.c = i, e.p = "", e(0)
    }([function(t, e, i) {
        var r = i(1)(i(2), null, null, null);
        t.exports = r.exports
    }, function(t, e) {
        t.exports = function(t, e, i, n) {
            var o, s = t = t || {},
                a = r(t["default"]);
            "object" !== a && "function" !== a || (o = t, s = t["default"]);
            var c = "function" == typeof s ? s.options : s;
            if (e && (c.render = e.render, c.staticRenderFns = e.staticRenderFns), i && (c._scopeId = i), n) {
                var h = Object.create(c.computed || null);
                Object.keys(n).forEach(function(t) {
                    var e = n[t];
                    h[t] = function() {
                        return e
                    }
                }), c.computed = h
            }
            return {
                "esModule": o,
                "exports": s,
                "options": c
            }
        }
    }, function(t, e, i) {
        function r(t) {
            for (var e = t.match(/\-\w/g), i = 0; i < e.length; i++) {
                var r = e[i].charAt(1).toUpperCase();
                t = t.replace(e[i], r)
            }
            return t
        }
        var n = i(3),
            o = (n.requireModule("dom"), "0"),
            s = "component-name",
            a = r(s);
        t.exports = {
            "render": function(t) {
                this.appearOnFirstScreen();
                var e = {
                        "component-name": "link",
                        "href": this.href,
                        "trackinfo": this.trackinfo,
                        "clicktrackinfo": this.clicktrackinfo,
                        "data-spm": this.spmd
                    },
                    i = this.isWeb || this.isNativeATag ? "a" : "div";
                this.isWeb && (e.target = "_blank", this.isDebug && (e["wx-spm-anchor-id"] = this.spmAnchorId));
                var r = this,
                    n = {
                        "click": function(t) {
                            r.isWeb ? r.doWebClick() : r.doclick()
                        }
                    };
                this.trackinfo && (n.appear = function(t) {
                    r.doappear()
                }), this.event && (n[this.event] = function(t) {
                    r.doEvent(t)
                });
                var o = t("div", {
                        "style": {
                            "width": "100%",
                            "position": "absolute",
                            "top": 0,
                            "backgroundColor": "rgba(0, 255, 0, 0.5)"
                        }
                    }, [t("text", {
                        "style": {
                            "color": "#ff0000",
                            "fontSize": 20
                        }
                    }, [this._v(this._s(this.spmAnchorId))])]),
                    s = [this.$slots["default"]];
                return !this.isNativeATag && this.isDebug && this.showSpm && s.push(o), t(i, {
                    "ref": "link",
                    "attrs": e,
                    "on": n
                }, s)
            },
            "data": function() {
                return {
                    "isSend": !1,
                    "isNativeATag": !1,
                    "isDebug": !1,
                    "showSpm": !1,
                    "spmAnchorId": "",
                    "maskWidth": 0
                }
            },
            "props": {
                "href": {
                    "type": String,
                    "default": function() {
                        return ""
                    }
                },
                "trackinfo": String,
                "clicktrackinfo": String,
                "bitrackinfo": String,
                "bitrackInfo": String,
                "event": String,
                "dataSpm": String,
                "data-spm": String,
                "spm": String
            },
            "computed": {
                "spmd": function() {
                    return this.spm || this.dataSpm || this["data-spm"] || ""
                },
                "isWeb": function() {
                    return n.env.isWeb()
                },
                "pBiTrackInfo": function() {
                    return this.bitrackinfo || this.bitrackInfo || ""
                }
            },
            "mounted": function() {
                var t = this,
                    e = weex.config.bundleUrl || "";
                this.isWeb || (this.isNativeATag = e.indexOf("vue_test_atag=1") >= 0), this.isDebug = e.indexOf("debug_mode=1") >= 0, this.showSpm = e.indexOf("show_spm=1") >= 0, this.isDebug && (this.spmAnchorId = this.getSpm(), this.showSpm && !this.isWeb && setTimeout(function() {
                    weex.requireModule("dom").getComponentRect(t.$refs.link, function(e) {
                        t.maskWidth = e.size.width * (t.isWeb ? WXEnvironment.deviceWidth / window.innerWidth : 1)
                    })
                }, 500))
            },
            "methods": {
                "doEvent": function(t) {
                    this.$emit(t.type, t)
                },
                "doappear": function() {
                    this.sendExposure(!0)
                },
                "doWebClick": function() {
                    this.$emit("doclick"), this.sendClick()
                },
                "doclick": function() {
                    var t = this;
                    this.$emit("doclick"), this.sendClick();
                    var e = this.href + "",
                        i = !1;
                    try {
                        WXLINK_BEFORE_OPEN(e, function(i) {
                            t.doOpenUrl(i + "");
                            try {
                                WXLINK_AFTER_OPEN(e, _urlObj.toString())
                            } catch (r) {}
                        }) === undefined && (i = !0)
                    } catch (r) {}
                    try {
                        sinkParams && n.tool.isArray(sinkParams) && function() {
                            var t = weex.config.bundleUrl || "",
                                i = new n.url.parseUrl(t),
                                r = new n.url.parseUrl(e),
                                o = function(t) {
                                    sinkParams.forEach(function(e) {
                                        t === e && (r.params[t] = i.params[t])
                                    })
                                };
                            for (var s in i.params) o(s);
                            e = r.toString()
                        }()
                    } catch (r) {}
                    i || this.doOpenUrl(e + "");
                    try {
                        WXLINK_AFTER_OPEN(e, _urlObj.toString())
                    } catch (r) {}
                },
                "doOpenUrl": function(t) {
                    if (!t) return void(console && console.error && console.error("Missing href!"));
                    var e = new n.url.parseUrl(t),
                        i = this.getSpm();
                    if (this.isDebug && console.log("spm:" + i), e.params.spm = i, this.pBiTrackInfo) {
                        var r = {};
                        r.scm = this.pBiTrackInfo.scm, r.sxm = this.pBiTrackInfo.sxm, r.spm = i, n.tracker.updateNextPageUtparam({
                            "clickinfo": r
                        })
                    }
                    n.url.openUrl(e.toString())
                },
                "getSpm": function() {
                    return [this.getSpmAB(), this.getSpmCD()].join(".")
                },
                "getSpmAB": function() {
                    var t = [o, o].join(".");
                    try {
                        if (this.isWeb) {
                            for (var e = document.getElementsByTagName("META"), i = 0; i < e.length; i++)
                                if ("spm-id" === e[i].name) {
                                    t = e[i].content;
                                    break
                                }
                        } else {
                            var n = this.$root.$document.body,
                                s = n.attr,
                                a = "spm-id",
                                c = r(a);
                            t = s[a] || s[c] || [o, o].join(".")
                        }
                    } catch (h) {}
                    return t
                },
                "getSpmCD": function() {
                    return this.doTrace(this.$vnode.elm)
                },
                "doTrace": function(t) {
                    var e = this.spmGetParentSPMId(t);
                    if (e.spm_c) {
                        var i = e.spm_c,
                            r = e.el,
                            n = [];
                        if (this.isWeb) {
                            if (r.parentNode) {
                                var o = r.parentNode;
                                if (o.children)
                                    for (var s = 0; s < o.children.length; s++) i === this.tryToGetAttribute(o.children[s], "data-spm") && n.push(o.children[s])
                            }
                        } else {
                            for (var a = r;
                                (a = a.parentNode) && "list" !== a.type;);
                            if (a && a.children)
                                for (var c = 0; c < a.children.length; c++) {
                                    var h = a.children[c];
                                    if ("cell" === h.type && h.children)
                                        for (var u = 0; u < h.children.length; u++) {
                                            var f = h.children[u];
                                            i === (this.tryToGetAttribute(f, "data-spm") || this.tryToGetAttribute(f, "dataSpm")) && n.push(f)
                                        }
                                }
                        }
                        0 == n.length && n.push(r);
                        for (var d = [], p = 0; p < n.length; p++) d = d.concat(this.spmGetModuleLinks(n[p]));
                        for (var l = 0, m = 0, v = d.length; l < v; l++) {
                            var b = d[l];
                            if (this.tryToGetAttribute(b, "href")) {
                                var g = this.tryToGetAttribute(b, "dataSpmAnchorId");
                                if (!g && (m++, g = i + "." + (this.spmd || m), b === this.$vnode.elm)) return g
                            }
                        }
                    }
                    return "0.0"
                },
                "spmGetParentSPMId": function(t) {
                    for (var e, i, r = t; t && (t = t.parentNode);)
                        if (i = this.isWeb ? this.tryToGetAttribute(t, "data-spm") : this.tryToGetAttribute(t, "data-spm") || this.tryToGetAttribute(t, "dataSpm")) {
                            e = i, r = t;
                            break
                        }
                    return e && !/^[\w\-\.\/]+$/.test(e) && (e = "0"), {
                        "spm_c": e,
                        "el": r
                    }
                },
                "spmGetModuleLinks": function(t) {
                    var e = void 0,
                        i = void 0,
                        r = void 0,
                        n = [],
                        o = void 0;
                    i = this.getLinkElements(t);
                    for (var s = 0; s < i.length; s++) {
                        for (o = !1, r = e = i[s];
                            (r = r.parentNode) && r != t;)
                            if (this.isWeb ? this.tryToGetAttribute(r, "data-spm") : this.tryToGetAttribute(r, "data-spm") || this.tryToGetAttribute(r, "dataSpm")) {
                                o = !0;
                                break
                            }
                        o || n.push(e)
                    }
                    return n
                },
                "tryToGetAttribute": function(t, e) {
                    return this.isWeb ? t.getAttribute(e) : t.attr && t.attr[e]
                },
                "getLinkElements": function(t) {
                    var e = [];
                    if (t.children && t.children.length > 0)
                        for (var i = t.children, r = 0; r < i.length; r++) {
                            var n = i[r],
                                o = this.tryToGetAttribute(n, s) || this.tryToGetAttribute(n, a);
                            if ("link" === o && e.push(n), n.children && n.children.length > 0) {
                                var c = this.getLinkElements(n);
                                c && c.length > 0 && (e = e.concat(c))
                            }
                        }
                    return e
                },
                "appearOnFirstScreen": function() {},
                "parseInfo": function(t) {
                    t = "string" == typeof t ? t : "";
                    var e = "-----",
                        i = t.split(e);
                    return {
                        "a": i[0] || "",
                        "c": i[1] || "",
                        "d": i[2] || ""
                    }
                },
                "sendExposure": function(t) {
                    function e() {
                        n.tracker.trackInfo(i.trackinfo), i.isSend = !0
                    }
                    if (this.trackinfo && !this.isSend) {
                        var i = this;
                        e()
                    }
                },
                "sendClick": function() {
                    this.clicktrackinfo && n.tracker.clickTrackInfo(this.clicktrackinfo)
                },
                "isFirstScreen": function(t) {
                    if (!this.isNativeRender(t)) return !1;
                    for (var e = t.size, i = [
                            [e.left, e.top],
                            [e.left, e.bottom],
                            [e.right, e.top],
                            [e.right, e.bottom]
                        ], r = 0; r < i.length; r++)
                        if (this.isInScreen.apply(this, i[r])) return !0;
                    return !1
                },
                "isNativeRender": function(t) {
                    var e = t.size ? t.size : {};
                    for (var i in e)
                        if (0 !== e[i]) return !0;
                    return !1
                },
                "isInScreen": function(t, e) {
                    return t < WXEnvironment.deviceWidth && t >= 0 && e < WXEnvironment.deviceHeight && e >= 0
                }
            }
        }
    }, function(e, i) {
        e.exports = t("mui/weex-zebra-utils/index")
    }])
});