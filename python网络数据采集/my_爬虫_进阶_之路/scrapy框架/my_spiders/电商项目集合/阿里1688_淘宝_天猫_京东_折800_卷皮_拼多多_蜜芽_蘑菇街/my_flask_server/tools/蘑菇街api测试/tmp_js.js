! function() {
    window.$ && window.require && (window.modJsRequire = function(e, n, t, o) {
        "function" == typeof n && (t = arguments[1], o = arguments[2], n = null), require(e, function() {
            var e = Array.from ? Array.from(arguments) : Array.prototype.slice.call(arguments),
                o = this;
            n && $(n).length ? $(n).each(function(n, r) {
                t && t.apply(o, e.concat([r, n]))
            }) : t && t.apply(this, e)
        }, o)
    })
}(), define("core/core", [], function() {
    var e = {
        Config: {
            debug: "@DEBUG@"
        },
        version: "undefined@",
        appEnv: "Env",
        data: {},
        widget: {},
        _global: {}
    };
    return window.MoGu = window.MoGu || {}, $.extend(window.MoGu, e), window.MoGu
}), define("core/evoke", ["core/core"], function(e) {
    function n(e) {
        this.options = {
            opentype: "index",
            param: null,
            downUrl: "https://a.app.qq.com/o/simple.jsp?pkgname=com.mogujie&g_f=991699"
        }, this.ua = null, this.src = null, this.merge(e), this.getUA(), this.getSrc(), this.evoke()
    }
    return n.prototype = {
        merge: function(e) {
            if ("object" != typeof e) return !1;
            var n = this.options;
            for (var t in n)("object" == typeof e[t] || e[t]) && (n[t] = e[t])
        },
        getUA: function() {
            var e = navigator.userAgent.toLowerCase(),
                n = this;
            n.ua = {
                mobile: !!e.match(/applewebKit.*mobile.*/),
                ios: !!e.match(/\(i[^;]+;( u;)? cpu.+mac os x/),
                chrome: e.indexOf("chrome") > -1,
                isVessel: e.indexOf("mogujie") > -1,
                isNative: e.indexOf("mogujie") > -1 && e.indexOf("nonative") == -1
            }
        },
        evoke: function() {
            var e = this;
            e.ua.isNative ? window.location.href = "mgj://" + e.src : e.ua.ios ? e.iosEvoke() : e.ua.chrome ? e.androidChrome() : e.androidNotChrome()
        },
        iosEvoke: function() {
            var e = this,
                n = new Date;
            return window.setTimeout(function() {
                var t = new Date;
                t - n < 5e3 && "object" != typeof e.options.downUrl ? window.location = e.options.downUrl : window.close()
            }, 25), "object" != typeof e.options.downUrl && void(window.location = "mogujie://open?url=" + encodeURIComponent("mgj://" + e.src))
        },
        androidNotChrome: function() {
            var e = this,
                n = "mogujie://index?url=" + encodeURIComponent("mgj://" + e.src),
                t = document.createElement("iframe");
            return t.src = n, t.style.display = "none", document.body.appendChild(t), "object" != typeof e.options.downUrl && void(window.location = e.options.downUrl)
        },
        androidChrome: function() {
            var e = this,
                n = "intent://index?url=" + e.src + "#Intent;scheme=mogujie;package=com.mogujie;end",
                t = document.createElement("a");
            return t.href = n, t.style.display = "none", document.body.appendChild(t), setTimeout(function() {
                t.click()
            }, 1e3), "object" != typeof e.options.downUrl && void(window.href = e.options.downUrl)
        },
        getSrc: function() {
            var e = this,
                n = e.options.param,
                t = "";
            if (n && "object" == typeof n)
                for (var o in n) t = t ? t + "&" : "?" + t, t = t + o + "=" + n[o];
            e.src = e.options.opentype + t
        }
    }, e.Evoke = n, e
}), define("core/const", ["core/core"], function(e) {
    return e.Const = {}, e
}), define("core/polyfill", ["core/core"], function(e) {
    return function() {
        for (var e = 0, n = ["ms", "moz", "webkit", "o"], t = 0; t < n.length && !window.requestAnimationFrame; ++t) window.requestAnimationFrame = window[n[t] + "RequestAnimationFrame"], window.cancelAnimationFrame = window[n[t] + "CancelAnimationFrame"] || window[n[t] + "CancelRequestAnimationFrame"];
        window.requestAnimationFrame || (window.requestAnimationFrame = function(n, t) {
            var o = +new Date,
                r = Math.max(0, 16 - (o - e)),
                i = window.setTimeout(function() {
                    n(o + r)
                }, r);
            return e = o + r, i
        }), window.cancelAnimationFrame || (window.cancelAnimationFrame = function(e) {
            clearTimeout(e)
        })
    }(), e
}), define("core/ua", ["core/core"], function(e) {
    $.extend(e, {
        ua: function() {
            var n = navigator.userAgent.toLowerCase(),
                t = {};
            return t["native"] = n.indexOf("mogujie") > -1 && n.indexOf("nonative") < 0, t.wechat = n.indexOf("micromessenger") > -1, t["native"] && window.mgj && mgj.device && mgj.device.getInfo(function(n) {
                e && e.ua && $.extend(e.ua, {
                    appInfo: n
                })
            }), $.os ? t = $.extend(!0, t, $.os) : t.phone = !1, t
        }()
    });
    var n = navigator.userAgent.toLowerCase(),
        t = new RegExp("(^|\\?|&)_f_channel=([^&]*)(\\s|&|$)", "i"),
        o = t.test(window.location.href.split("#")[0]) ? RegExp.$2.replace(/\+/g, " ") : "";
    return e.channel = "", e.isMeiliIncApp = !1, /mogujie/.test(n) ? (e.isMeiliIncApp = !0, e.channel = "MOGUJIE") : /meilishuo/.test(n) ? (e.isMeiliIncApp = !0, e.channel = "MEILISHUO") : /amcustomer/.test(n) ? (e.isMeiliIncApp = !0, e.channel = "TAOSHIJIE") : /go4iphone/.test(n) || /go4android/.test(n) ? (e.isMeiliIncApp = !0, e.channel = "GO") : o && (e.channel = o), e.addChannelParam = function(n) {
        $.extend(n, {
            channel: e.channel
        })
    }, e
}), define("core/error", ["core/core", "core/ua"], function(e) {
    return $.extend(e, {
        error: function(n) {
            if (console && console.log(n), e.ua["native"] && window.MOGU_DEV) {
                var t = $("#notice_error");
                t.length || (t = $('<div id="notice_error"></div>').prependTo($("body"))), t.prepend("<p>" + n + "</p>")
            }
        }
    }), e
}), define("fnExtend", ["core/core"], function(e) {
    var n = function(e) {
            var n = typeof e;
            return "function" === n || "object" === n && !!e
        },
        t = function(e, n) {
            return void 0 === n ? e : function() {
                return e.apply(n, arguments)
            }
        },
        o = function(e, n, o) {
            return null == e ? e || null : $.isFunction(e) ? t(e, n, o) : function(n) {
                return n[e]
            }
        };
    return {
        parseJson: JSON.parse,
        escapeHtml: function(e) {
            return e.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;")
        },
        formatPrice: function(e) {
            return null == e ? "-" : (e / 100).toFixed(2)
        },
        formatDate: function(e, n) {
            var t, o, r = this,
                i = ["Sun", "Mon", "Tues", "Wednes", "Thurs", "Fri", "Satur", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                a = /\\?(.?)/gi,
                u = function(e, n) {
                    return o[e] ? o[e]() : n
                },
                c = function(e, n) {
                    for (e = String(e); e.length < n;) e = "0" + e;
                    return e
                };
            return o = {
                d: function() {
                    return c(o.j(), 2)
                },
                D: function() {
                    return o.l().slice(0, 3)
                },
                j: function() {
                    return t.getDate()
                },
                l: function() {
                    return i[o.w()] + "day"
                },
                N: function() {
                    return o.w() || 7
                },
                S: function() {
                    var e = o.j(),
                        n = e % 10;
                    return n <= 3 && 1 == parseInt(e % 100 / 10, 10) && (n = 0), ["st", "nd", "rd"][n - 1] || "th"
                },
                w: function() {
                    return t.getDay()
                },
                z: function() {
                    var e = new Date(o.Y(), o.n() - 1, o.j()),
                        n = new Date(o.Y(), 0, 1);
                    return Math.round((e - n) / 864e5)
                },
                W: function() {
                    var e = new Date(o.Y(), o.n() - 1, o.j() - o.N() + 3),
                        n = new Date(e.getFullYear(), 0, 4);
                    return c(1 + Math.round((e - n) / 864e5 / 7), 2)
                },
                F: function() {
                    return i[6 + o.n()]
                },
                m: function() {
                    return c(o.n(), 2)
                },
                M: function() {
                    return o.F().slice(0, 3)
                },
                n: function() {
                    return t.getMonth() + 1
                },
                t: function() {
                    return new Date(o.Y(), o.n(), 0).getDate()
                },
                L: function() {
                    var e = o.Y();
                    return e % 4 === 0 & e % 100 !== 0 | e % 400 === 0
                },
                o: function() {
                    var e = o.n(),
                        n = o.W(),
                        t = o.Y();
                    return t + (12 === e && n < 9 ? 1 : 1 === e && n > 9 ? -1 : 0)
                },
                Y: function() {
                    return t.getFullYear()
                },
                y: function() {
                    return o.Y().toString().slice(-2)
                },
                a: function() {
                    return t.getHours() > 11 ? "pm" : "am"
                },
                A: function() {
                    return o.a().toUpperCase()
                },
                B: function() {
                    var e = 3600 * t.getUTCHours(),
                        n = 60 * t.getUTCMinutes(),
                        o = t.getUTCSeconds();
                    return c(Math.floor((e + n + o + 3600) / 86.4) % 1e3, 3)
                },
                g: function() {
                    return o.G() % 12 || 12
                },
                G: function() {
                    return t.getHours()
                },
                h: function() {
                    return c(o.g(), 2)
                },
                H: function() {
                    return c(o.G(), 2)
                },
                i: function() {
                    return c(t.getMinutes(), 2)
                },
                s: function() {
                    return c(t.getSeconds(), 2)
                },
                u: function() {
                    return c(1e3 * t.getMilliseconds(), 6)
                },
                e: function() {
                    throw "Not supported (see source code of date() for timezone on how to add support)"
                },
                I: function() {
                    var e = new Date(o.Y(), 0),
                        n = Date.UTC(o.Y(), 0),
                        t = new Date(o.Y(), 6),
                        r = Date.UTC(o.Y(), 6);
                    return e - n !== t - r ? 1 : 0
                },
                O: function() {
                    var e = t.getTimezoneOffset(),
                        n = Math.abs(e);
                    return (e > 0 ? "-" : "+") + c(100 * Math.floor(n / 60) + n % 60, 4)
                },
                P: function() {
                    var e = o.O();
                    return e.substr(0, 3) + ":" + e.substr(3, 2)
                },
                T: function() {
                    return "UTC"
                },
                Z: function() {
                    return 60 * -t.getTimezoneOffset()
                },
                c: function() {
                    return "Y-m-d\\TH:i:sP".replace(a, u)
                },
                r: function() {
                    return "D, d M Y H:i:s O".replace(a, u)
                },
                U: function() {
                    return t / 1e3 | 0
                }
            }, this.date = function(e, n) {
                return r = this, t = void 0 === n ? new Date : n instanceof Date ? new Date(n) : new Date(1e3 * n), e.replace(a, u)
            }, this.date(e, n)
        },
        has: function(e, n) {
            return null != e && e.hasOwnProperty(n)
        },
        keys: function(e) {
            var t = Object.keys;
            if (!n(e)) return [];
            if (t) return t(e);
            var o = [];
            for (var r in e) e.hasOwnProperty(r) && o.push(r);
            return o
        },
        values: function(e) {
            var n = this.keys(e);
            return n.map(function(n) {
                return e[n]
            })
        },
        map: function(e, n, t) {
            if (null == e) return [];
            n = o(n, t);
            var r, i, a = e.length;
            a !== +a && (i = this.keys(e), a = i.length);
            for (var u = new Array(a), c = 0; c < a; c++) r = i ? i[c] : c, u[c] = n(e[r], r, e);
            return u
        },
        now: function() {
            return +Date.now() || +new Date
        },
        throttle: function(e, n, t) {
            var o, r, i, a = this,
                u = null,
                c = 0;
            t || (t = {});
            var s = function() {
                c = t.leading === !1 ? 0 : a.now(), u = null, i = e.apply(o, r), u || (o = r = null)
            };
            return function() {
                var f = a.now();
                c || t.leading !== !1 || (c = f);
                var l = n - (f - c);
                return o = this, r = arguments, l <= 0 || l > n ? (clearTimeout(u), u = null, c = f, i = e.apply(o, r), u || (o = r = null)) : u || t.trailing === !1 || (u = setTimeout(s, l)), i
            }
        },
        debounce: function(e, n, t) {
            var o, r, i, a, u, c = this,
                s = function() {
                    var f = c.now() - a;
                    f < n && f > 0 ? o = setTimeout(s, n - f) : (o = null, t || (u = e.apply(i, r), o || (i = r = null)))
                };
            return function() {
                i = this, r = arguments, a = c.now();
                var f = t && !o;
                return o || (o = setTimeout(s, n)), f && (u = e.apply(i, r), i = r = null), u
            }
        },
        login: function(n) {
            if (n = n || location.href, e.ua["native"] && "object" == typeof mgj) location.href = logger && logger.generatePtpParams("mgj://login") || "mgj://login";
            else {
                var t = "https://h5.mogujie.com/user-process/login.html?redirect_url=" + encodeURIComponent(n);
                location.href = logger && logger.generatePtpParams(t) || t
            }
        },
        parseUrl: function(e) {
            return {}
        },
        toFixed: function(e, n) {
            var t, o = 0;
            n = n || 2;
            var r = Math.pow(10, n || 0);
            t = String(Math.round(e * r) / r);
            var i = t.split(".")[1];
            i ? o = i.length : n != o && (t += ".");
            for (var a = 0; a < n - o; a++) t += "0";
            return t
        },
        formatTime: function(e, n) {
            var t = new Date(parseInt(1e3 * e));
            n = n || "YY-MM-DD";
            var o = t.getFullYear(),
                r = parseInt(t.getMonth()),
                i = parseInt(t.getDate()),
                a = o,
                u = r > 8 ? r + 1 : "0" + (r + 1),
                c = i > 9 ? i : "0" + i;
            return n.replace(/YY/i, a).replace(/MM/i, u).replace(/DD/i, c)
        }
    }
}), define("fn/fn", ["core/core", "fnExtend"], function(e, n) {
    return e.fn = {
        set: function(n, t) {
            e._global[n] && e.error(n + "\u5305\u5c06\u88ab\u66ff\u6362"), e._global[n] = t
        },
        get: function(n) {
            return e._global[n] || !1
        },
        getQueryString: function(e, n) {
            n = n || location.href, n = n.split("#")[0];
            var t = new RegExp("(^|\\?|&)" + e + "=([^&]*)(\\s|&|$)", "i");
            return t.test(n) ? RegExp.$2.replace(/\+/g, " ") : ""
        },
        setCookie: function(e, n, t) {
            t = t || {}, null === n && (n = "", t.expires = -1);
            var o = "";
            if (t.expires && ("number" == typeof t.expires || t.expires.toUTCString)) {
                var r;
                "number" == typeof t.expires ? (r = new Date, r.setTime(r.getTime() + 864e5 * t.expires)) : r = t.expires, o = "; expires=" + r.toUTCString()
            }
            var i = t.path ? "; path=" + t.path : "",
                a = t.secure ? "; secure" : "",
                u = "";
            t.domain ? u = "; domain=" + t.domain : (u = document.domain.toString().split("."), u = "; domain=." + u[1] + "." + u[2]), document.cookie = [e, "=", encodeURIComponent(n), o, i, u, a].join("")
        },
        getCookie: function(e) {
            var n = document.cookie.match(new RegExp("(^| )" + e + "=([^;]*)(;|$)"));
            return null !== n ? decodeURIComponent(n[2]) : ""
        },
        removeCookie: function(n) {
            e.util.setCookie(n, null, {
                expires: -1
            })
        },
        idtourl: function(e) {
            if (e) return 1 + (2 * e + 56).toString(36)
        },
        urltoid: function(e) {
            return (parseInt(e.substring(1), 36) - 56) / 2
        },
        walkThrough: function(e, n) {
            n = n || window;
            var t = (e || "").split("."),
                o = !!t.length;
            return $(t).each(function(e, t) {
                return o = o && null !== n[t] && void 0 !== n[t], o === !1 ? o : void(n = n[t])
            }), o
        },
        cAjax: function(e) {
            return $.ajax(e)
        }
    }, $.extend(e.fn, n), e
}), define("uiExtend", [], function() {
    function e() {
        t.css("display", "block")
    }

    function n() {
        t.css("display", "none")
    }
    var t = $("#M_Loading");
    return {
        showMask: function(e) {
            e = e || $("#M_Mask"), e.show()
        },
        hideMask: function(e) {
            e = e || $("#M_Mask"), e.hide()
        },
        showLoading: function() {
            MoGu.ua["native"] ? "undefined" != typeof mgj && mgj.progress ? (MoGu.ui.showLoading = mgj.progress.show, n(), mgj.progress.show()) : e() : (e(), MoGu.ui.showLoading = e)
        },
        hideLoading: function() {
            n(), MoGu.ua["native"] ? "undefined" != typeof mgj && mgj.progress && (MoGu.ui.hideLoading = mgj.progress.hide, mgj.progress.hide()) : MoGu.ui.hideLoading = n
        },
        initRem: function(e) {
            e = +e || 100;
            var n = window.document.documentElement,
                t = Math.min(n.clientWidth, 750);
            n.style.fontSize = t / (750 / e) + "px"
        }
    }
}), define("lib/doT", [], function() {
    function e() {
        var e = {
                "&": "&#38;",
                "<": "&#60;",
                ">": "&#62;",
                '"': "&#34;",
                "'": "&#39;",
                "/": "&#47;"
            },
            n = /&(?!#?\w+;)|<|>|"|'|\//g;
        return function() {
            return this ? this.replace(n, function(n) {
                return e[n] || n
            }) : this
        }
    }

    function n(e, t, o) {
        return ("string" == typeof t ? t : t.toString()).replace(e.define || i, function(n, t, r, i) {
            return 0 === t.indexOf("def.") && (t = t.substring(4)), t in o || (":" === r ? (e.defineParams && i.replace(e.defineParams, function(e, n, r) {
                o[t] = {
                    arg: n,
                    text: r
                }
            }), t in o || (o[t] = i)) : new Function("def", "def['" + t + "']=" + i)(o)), ""
        }).replace(e.use || i, function(t, r) {
            e.useParams && (r = r.replace(e.useParams, function(e, n, t, r) {
                if (o[t] && o[t].arg && r) {
                    var i = (t + ":" + r).replace(/'|\\/g, "_");
                    return o.__exp = o.__exp || {}, o.__exp[i] = o[t].text.replace(new RegExp("(^|[^\\w$])" + o[t].arg + "([^\\w$])", "g"), "$1" + r + "$2"), n + "def.__exp['" + i + "']"
                }
            }));
            var i = new Function("def", "return " + r)(o);
            return i ? n(e, i, o) : i
        })
    }

    function t(e) {
        return e.replace(/\\('|\\)/g, "$1").replace(/[\r\t\n]/g, " ")
    }
    var o = {
        version: "1.0.1",
        templateSettings: {
            evaluate: /\{\{([\s\S]+?(\}?)+)\}\}/g,
            interpolate: /\{\{=([\s\S]+?)\}\}/g,
            encode: /\{\{!([\s\S]+?)\}\}/g,
            use: /\{\{#([\s\S]+?)\}\}/g,
            useParams: /(^|[^\w$])def(?:\.|\[[\'\"])([\w$\.]+)(?:[\'\"]\])?\s*\:\s*([\w$\.]+|\"[^\"]+\"|\'[^\']+\'|\{[^\}]+\})/g,
            define: /\{\{##\s*([\w\.$]+)\s*(\:|=)([\s\S]+?)#\}\}/g,
            defineParams: /^\s*([\w$]+):([\s\S]+)/,
            conditional: /\{\{\?(\?)?\s*([\s\S]*?)\s*\}\}/g,
            iterate: /\{\{~\s*(?:\}\}|([\s\S]+?)\s*\:\s*([\w$]+)\s*(?:\:\s*([\w$]+))?\s*\}\})/g,
            varname: "it",
            strip: !0,
            append: !0,
            selfcontained: !1
        },
        template: void 0,
        compile: void 0
    };
    String.prototype.encodeHTML = e();
    var r = {
            append: {
                start: "'+(",
                end: ")+'",
                endencode: "||'').toString().encodeHTML()+'"
            },
            split: {
                start: "';out+=(",
                end: ");out+='",
                endencode: "||'').toString().encodeHTML();out+='"
            }
        },
        i = /$^/;
    return o.template = function(a, u, c) {
        u = u || o.templateSettings;
        var s, f, l = u.append ? r.append : r.split,
            d = 0,
            p = u.use || u.define ? n(u, a, c || {}) : a;
        p = ("var out='" + (u.strip ? p.replace(/(^|\r|\n)\t* +| +\t*(\r|\n|$)/g, " ").replace(/\r|\n|\t|\/\*[\s\S]*?\*\//g, "") : p).replace(/'|\\/g, "\\$&").replace(u.interpolate || i, function(e, n) {
            return l.start + t(n) + l.end
        }).replace(u.encode || i, function(e, n) {
            return s = !0, l.start + t(n) + l.endencode
        }).replace(u.conditional || i, function(e, n, o) {
            return n ? o ? "';}else if(" + t(o) + "){out+='" : "';}else{out+='" : o ? "';if(" + t(o) + "){out+='" : "';}out+='"
        }).replace(u.iterate || i, function(e, n, o, r) {
            return n ? (d += 1, f = r || "i" + d, n = t(n), "';var arr" + d + "=" + n + ";if(arr" + d + "){var " + o + "," + f + "=-1,l" + d + "=arr" + d + ".length-1;while(" + f + "<l" + d + "){" + o + "=arr" + d + "[" + f + "+=1];out+='") : "';} } out+='"
        }).replace(u.evaluate || i, function(e, n) {
            return "';" + t(n) + "out+='"
        }) + "';return out;").replace(/\n/g, "\\n").replace(/\t/g, "\\t").replace(/\r/g, "\\r").replace(/(\s|;|\}|^|\{)out\+='';/g, "$1").replace(/\+''/g, "").replace(/(\s|;|\}|^|\{)out\+=''\+/g, "$1out+="), s && u.selfcontained && (p = "String.prototype.encodeHTML=(" + e.toString() + "());" + p);
        try {
            return new Function(u.varname, p)
        } catch (e) {
            throw "undefined" != typeof console && console.log("Could not create a template function: " + p), e
        }
    }, o.compile = function(e, n) {
        return o.template(e, null, n)
    }, o
}), define("ui/ui", ["uiExtend", "lib/doT"], function(e, n) {
    return MoGu.ui = {
        jsMbSubstr: function(e, n, t) {
            if (!e) return "";
            var o = /[\u1100-\u115F\u11A3-\u11A7\u11FA-\u11FF\u2329\u232A\u2E80-\u303E\u3040-\u4DBF\u4E00-\uA4CF\uA960-\uA97F\uAC00-\uD7FF\uF900-\uFAFF\uFE10-\uFE1F\uFE30-\uFE6F\uFF01-\uFF60\uFFE0-\uFFE7]/,
                r = 0;
            for (n = 2 * n; n > 0;) {
                var i = o.test(e.charAt(r)) ? 2 : 1;
                n -= i, r++
            }
            return r += n, e.substring(0, r) + (t || "")
        },
        getPicExtension: function(e) {
            var n = e.match(/.+\.(.+)$/);
            return n ? n[1] : ""
        },
        getTemplate: function(e, t) {
            try {
                return n.template(e)(t)
            } catch (e) {
                return e
            }
        },
        getdoT: function() {
            return n
        }
    }, $.extend(MoGu.ui, e), MoGu
}), define("ui/tips", ["fn/fn"], function(e) {
    "use strict";
    var n = {
            duration: 1500
        },
        t = function(e) {
            var t = $.extend({}, n, e);
            this.duration = t.duration, this.init()
        };
    t.prototype = {
        init: function() {
            this.elem = $("#M_Tips"), this.elem.get(0) || (this.elem = $("<div id='M_Tips' class='ui-tips' style='display:none;'><span class='ui-tips-text'></span></div>"), this.elem.appendTo("body")), this.text = this.elem.find(".ui-tips-text")
        },
        show: function(e, n, t) {
            var o = this;
            o.elem.show(), e && "string" == typeof e && o.text.html(e).removeClass("fadeOut").addClass("fadeIn"), isNaN(n) && !$.isFunction(t) && t !== !1 && (t = n, n = o.duration), 0 != n && o.hide(n, t)
        },
        hide: function(e, n) {
            var t = this,
                o = null;
            o = setTimeout(function() {
                t.text.removeClass("fadeIn").addClass("fadeOut"), setTimeout(function() {
                    t.elem.hide(), n && n()
                }, 500)
            }, e || t.duration)
        }
    }, e.fn.set("tip", t);
    var o = new t;
    return $.extend(e.fn, {
        tips: o
    }), o
}), define("core/cube/app", ["core/ua", "fn/fn"], function(e) {
    function n(n, t) {
        e.ua["native"] && (t = t || $("body"), t.off("click", n, i).on("click", n, i))
    }

    function t() {
        if (!e.ua["native"]) return -1;
        var n = new RegExp("(^|[?]|&)_av=([0-9]{3})", "i"),
            t = window.location.search.match(n);
        if (t && t[2] > 400) return parseInt(t[2]);
        var o = window.navigator.userAgent,
            r = "",
            i = "";
        return $.os.iphone && (r = new RegExp("(mogujie4iphone).*/([0-9]{3})", "i"), i = o.match(r), i && i[2] > 400) ? parseInt(i[2]) : $.os.android && (r = new RegExp("(mogujie4android).*/([0-9]{3})", "i"), i = o.match(r), i && i[2] > 400) ? parseInt(i[2]) : void 0
    }

    function o(e) {
        document.addEventListener("deviceready", function() {
            return window.mgj && mgj.device && mgj.device.getInfo ? void mgj.device.getInfo(function(n) {
                "string" == typeof n && (n = JSON.parse(n)), e(+n.appVersion)
            }, function() {
                e(-1)
            }) : void e(-1)
        })
    }

    function r(n) {
        return e.ua["native"] && e.ua["native"] && hdp ? void hdp["do"]("mgj.device.signParams", {}).then(function(e) {
            return "string" == typeof e && (e = JSON.parse(e)), n && "string" == typeof n ? e[n] : e._did
        })["catch"](function(e) {
            return e || -1
        }) : -1
    }
    var i = function() {
        if (e.ua["native"]) {
            var n = $(this),
                t = n.attr("href");
            if (t.indexOf("mgj://") >= 0 || t.indexOf("javascript") >= 0) return;
            if (t = logger && logger.generatePtpParams(t) || t, window.hdp) return window.hdp["do"]("mgj.navigation.pushWindow", t), !1;
            if (window.mgj) return window.location.href = "mgj://web?url=" + encodeURIComponent(t), !1
        }
    };
    return $(document).on("click", "[push-window]", i), $.extend(e.fn, {
        openLinkView: n,
        getAppVersion: t,
        getAppVersionAsync: o,
        platform: e.ua.phone ? e.ua["native"] ? "app" : "wap" : "pc",
        getDeviceId: r
    }), e
}), define("core/cube/lazyload", ["core/core"], function() {}), define("fn/time", ["fn/fn"], function() {
    MoGu.fn = $.extend({}, MoGu.fn, {
        getServerTime: function(e) {
            return M.getServerTime(!1).then(function(n) {
                e(n.time)
            })
        }
    })
}), define("fn/modacm", ["fn/fn", "core/ua", "core/cube/app"], function() {
    MoGu.fn = $.extend({}, MoGu.fn, {
        getModAcm: function(e) {
            if (!e) return "";
            var n = $(e),
                t = n.parents(),
                o = "module_row",
                r = null;
            return $(t).each(function(e, n) {
                $(n).hasClass(o) && (r = $(n))
            }), r ? $(r).attr("data-acm") : ""
        }
    })
}), define("fn/showlog", ["fn/fn", "core/ua", "core/cube/app"], function() {
    function e(e) {
        return "none" != e.css("display") && "hidden" != e.css("visibility") && 0 != e.css("opacity") && e.width() && e.height()
    }

    function n(n) {
        var t = n.offset().top,
            o = n.height(),
            r = n.offset().left,
            i = n.offset().width,
            a = $(window).scrollTop(),
            u = $(window).scrollLeft(),
            c = $(window).width(),
            s = $(window).height(),
            f = t >= a && t < a + s,
            l = t + o > a && t + o <= a + s,
            d = t < a && t + o > a + s,
            p = r >= u && r < u + c,
            g = r + i > u && r + i <= u + c,
            m = r < u && r + i > u + c;
        return e(n) && (f || l || d) && (p || g || m)
    }

    function t() {
        if (w.length || j.length || C.length || b.length || M || F.length) {
            var e = function(e) {
                if (o || (o = e), j && j.length) {
                    var n = j.splice(0, m),
                        t = v.splice(0, m);
                    S("0x00000000", {
                        acms: n,
                        indexs: t,
                        type: 5,
                        ver: o || ""
                    })
                } else if (C && C.length) {
                    var n = C.splice(0, m),
                        t = y.splice(0, m);
                    S("0x00000000", {
                        acms: n,
                        indexs: t,
                        type: 5,
                        ver: o || ""
                    })
                } else if (b && b.length) {
                    var n = b.splice(0, m),
                        t = x.splice(0, m),
                        r = A.splice(0, m);
                    S("0x00000000", {
                        acms: n,
                        indexs: t,
                        type: 4,
                        iids: r,
                        ver: o || ""
                    })
                } else if (M) M.ver = o || "", S(h || 70500, M), M = null, h = null;
                else if (w && w.length) {
                    var n = w.splice(0, m),
                        t = T.splice(0, m),
                        r = A.splice(0, m);
                    S(h || 70500, {
                        acms: n,
                        iids: r,
                        indexs: t,
                        ver: o || ""
                    }), h = null
                } else if (F && F.length) {
                    var i = F.shift();
                    S("0x00000000", $.extend({
                        acms: i.params.acms,
                        indexs: i.params.indexs,
                        iids: i.params.iids,
                        ver: o || ""
                    }, i.params.customParams))
                }
            };
            !o && MoGu.ua["native"] && MoGu && MoGu.fn && MoGu.fn.getAppVersionAsync ? MoGu.fn.getAppVersionAsync(e) : e(o)
        }
        r = !0, window.setTimeout(function() {
            w.length || j.length || C.length || b.length || M || F.length ? t() : r = !1
        }, 1e3)
    }
    var o = "",
        r = !1,
        i = "module_row",
        a = "cube-acm-node",
        u = "has-log-mod",
        c = "rec-show-log",
        s = "show-log-item",
        f = "waiting-log",
        l = "log-custom",
        d = "data-log-content",
        p = "data-log-iid",
        g = "preserve-log",
        m = ($("." + c), 50),
        h = null,
        w = [],
        v = [],
        y = [],
        x = [],
        M = null,
        j = [],
        C = [],
        b = [],
        F = [],
        A = [],
        T = [],
        S = function(e, n) {
            var t = window && window.logger && window.logger.log;
            t && t(e, n)
        },
        D = function(e) {
            var n = e.attr(d),
                t = n.split(";");
            $(t).each(function(e, n) {
                var t = n.split("="),
                    o = t[0];
                o && (M = M || {}, M[o] = M[o] || [], M[o].push(n.replace(o + "=", "")))
            })
        },
        E = function() {
            $("." + i).each(function(e, t) {
                var o = $(t),
                    r = o.attr("data-acm") || "",
                    i = r.split(".");
                if (r && n(o)) {
                    var c = o.find("." + a + ",.anchor,." + s),
                        f = c.length,
                        d = null,
                        g = o.find(".param-dom");
                    $(g).each(function(e, n) {
                        var t = $(n).data("param-key"),
                            o = $(n).data("param-value");
                        if (t) {
                            var i = {};
                            i[t] = o, d = d || {}, d.key = r, d.params = $.extend(d.params || {}, i)
                        }
                    }), o.hasClass(u) || (j.push(r + "-mfs_" + f), v.push(e), o.addClass(u));
                    var m = [],
                        h = [],
                        w = [];
                    if (f && $(c).each(function(e, t) {
                            var o = $(t),
                                a = !o.hasClass(l) && o.attr("data-log-content") || "",
                                c = o.attr(p) || "";
                            !o.hasClass(u) && n(o) && (a && i[6] ? ((d ? m : b).push(a + "-" + i[6] + "-idx_" + e + "-mfs_" + f), (d ? w : x).push(e), c && (d ? h : A).push(c), o.addClass(u)) : ((d ? m : C).push(r + "-idx_" + e + "-mfs_" + f), (d ? w : y).push(e), o.addClass(u)))
                        }), d && m && m.length) {
                        var M = -1;
                        $(F).each(function(e, n) {
                            n.key === d.key && (M = e)
                        }), M === -1 && (F.push({
                            key: d.key
                        }), M = F.length - 1), F[M].params = F[M].params ? {
                            customParams: d.params,
                            acms: F[M].params.acms.concat(m),
                            iids: F[M].params.iids.concat(h),
                            indexs: F[M].params.indexs.concat(w)
                        } : {
                            customParams: d.params,
                            acms: m,
                            iids: h,
                            indexs: w
                        }
                    }
                }
            }), $("." + c).each(function(e, t) {
                var o = $(t);
                if (n(o) || o.hasClass(f)) {
                    o.removeClass(f);
                    var r = o.attr(g),
                        i = o.find("." + l);
                    i.length ? $(i).each(function(e, t) {
                        var r = $(t);
                        if (n(r) || r.hasClass(f)) {
                            if (r.removeClass(f), h && h !== o.data("eventid")) return o.addClass(f), void r.addClass(f);
                            r.hasClass(l) && D(r), h = o.data("eventid"), r.removeClass(l)
                        }
                    }) : r || o.removeClass(c)
                }
            }), (w.length || j.length || C.length || b.length || M || F.length) && !r && t()
        },
        k = function() {
            $(function() {
                window.setTimeout(function() {
                    $(window).scroll(E), E && E()
                }, 1e3)
            })
        };
    k(), MoGu.fn = $.extend({}, MoGu.fn, {
        showLog: E
    })
}), define("base/MoGu", ["core/core", "core/const", "core/polyfill", "core/error", "core/ua", "fn/fn", "fn/time", "fn/modacm", "fn/showlog", "ui/ui", "ui/tips", "core/cube/lazyload", "core/cube/app"], function(e) {
    return e
}), define("jQuery", function() {
    return $
}), require(["base/MoGu"], function(e) {
    return e
});
! function(t) {
    t.MWP = function() {
        "use strict";

        function t(t, e) {
            function n() {
                this.constructor = t
            }
            S(t, e), t.prototype = null === e ? Object.create(e) : (n.prototype = e.prototype, new n)
        }

        function e(t, e) {
            void 0 === e && (e = !0);
            var n = t.split(O),
                r = e ? decodeURIComponent : E;
            return n.reduce(function(t, e) {
                e = e.replace(T, "%20");
                var n, o, i = e.indexOf("=");
                return 0 > i ? (n = e, o = "") : (n = e.slice(0, i), o = e.slice(i + 1)), n = r(n), o = r(o), j.call(t, n) ? Array.isArray(t[n]) ? t[n].push(o) : t[n] = [t[n], o] : t[n] = o, t
            }, {})
        }

        function n(t, e) {
            if (void 0 === e && (e = !0), !t) return "";
            var n = e ? encodeURIComponent : E;
            return Object.keys(t).map(function(e) {
                var r = t[e];
                return e = n(e), Array.isArray(r) ? r.map(function(t, r) {
                    return e + "[" + r + "]=" + n(t)
                }).join("&") : e + "=" + n(r)
            }).join("&")
        }

        function r(t) {
            return "undefined" != typeof FormData && t instanceof FormData
        }

        function o(t) {
            var e = document.head || document.getElementsByTagName("head")[0];
            e.appendChild(t)
        }

        function i(t, e, n) {
            function r() {
                i.parentNode && i.parentNode.removeChild(i);
                try {
                    delete window[s]
                } catch (t) {
                    window[s] = void 0
                }
            }
            var i, s = e.jsonpCallback || "httpCb" + h();
            window[s] = function(t) {
                r(), n(null, t), n = null
            }, t = c(t, Object.assign({}, e.data, {
                callback: s,
                _: Date.now()
            })), i = document.createElement("script"), i.src = t, i.type = "text/javascript", i.async = !0;
            var a = function(t) {
                (t && "error" === t.type || null !== n) && (r(), n(new Error(C)))
            };
            M && "onreadystatechange" in i ? i.onreadystatechange = function() {
                "complete" === i.readyState && (i.onreadystatechange = null, o(i), a({
                    type: "load "
                }));
                var t = i.readyState;
                try {
                    i.children
                } catch (e) {}
                "loaded" === t && "loading" === i.readyState && (i.onreadystatechange = null, a({
                    type: "error"
                }))
            } : (i.onload = i.onerror = a, o(i))
        }

        function s(t, e, o) {
            var i = e.data,
                s = new XMLHttpRequest;
            "GET" === e.method && (t = c(t, i), i = null), s.open(e.method, t), s.withCredentials = "omit" !== e.credentials, s.onreadystatechange = function() {
                if (s.readyState === XMLHttpRequest.DONE)
                    if (s.onreadystatechange = function() {}, 200 === s.status) try {
                        var t;
                        t = "json" === e.dataType ? "" === s.responseText ? null : JSON.parse(s.responseText) : s.responseText, o(null, t)
                    } catch (n) {
                        o(n)
                    } else o(new Error(C))
            };
            try {
                var a = e.headers;
                r(i) && delete a["content-type"], Object.keys(a).forEach(function(t) {
                    s.setRequestHeader(t, a[t])
                }), i ? r(i) ? s.send(i) : a["content-type"].indexOf(R.json) >= 0 ? s.send(JSON.stringify(i)) : s.send(n(i)) : s.send(null)
            } catch (u) {
                o(u)
            }
        }

        function a(t, e, o) {
            var i = e.data,
                s = {
                    method: e.method,
                    headers: e.headers,
                    credentials: e.credentials
                };
            "GET" === e.method ? t = c(t, i) : i && (r(i) ? (s.body = i, delete s.headers["content-type"]) : e.headers["content-type"].indexOf(R.json) >= 0 ? s.body = JSON.stringify(i) : s.body = n(i)), u(t) || (s.mode = "cors"), k(t, s).then(function(t) {
                switch (e.dataType) {
                    case "json":
                        return t.json();
                    case "text":
                    default:
                        return t.text()
                }
            }).then(function(t) {
                o(null, t)
            })["catch"](function() {
                o(new Error(C))
            })
        }

        function u(t) {
            try {
                var e = document.createElement("a");
                return e.href = t, e.href = e.href, e.protocol === x.protocol && e.hostname === x.hostname && e.port === x.port
            } catch (n) {
                return !0
            }
        }

        function c(t, r) {
            if (r) {
                var o = t.split("?"),
                    i = o[0],
                    s = o[1];
                s && (r = Object.assign(e(s), r));
                var a = n(r);
                a && (t = i + "?" + a)
            }
            return t
        }

        function h() {
            return String(Date.now()) + String((90 * Math.random() | 0) + 10)
        }

        function p(t, e, n) {
            n = n || {}, null === e && (e = "", n.expires = -1);
            var r = "";
            if (n.expires && ("number" == typeof n.expires || n.expires.toUTCString)) {
                var o;
                "number" == typeof n.expires ? (o = new Date, o.setTime(o.getTime() + 864e5 * n.expires)) : o = n.expires, r = "; expires=" + o.toUTCString()
            }
            var i = n.path ? "; path=" + n.path : "",
                s = n.secure ? "; secure" : "",
                a = "";
            n.domain ? a = "; domain=" + n.domain : (a = document.domain.toString().split("."), a = "; domain=." + a[1] + "." + a[2]), document.cookie = [t, "=", encodeURIComponent(e), r, i, a, s].join("")
        }

        function f(t) {
            var e = document.cookie.match(new RegExp("(^| )" + t + "=([^;]*)(;|$)"));
            return null !== e ? decodeURIComponent(e[2]) : ""
        }

        function d() {
            return ++window._mwpJsonpID || (window._mwpJsonpID = 1)
        }

        function l(t) {
            if (t.ret === N.Success) return t.data;
            throw Object.assign(Object.create(new Error(t.msg || D)), {
                code: t.ret,
                payload: t
            })
        }

        function m() {
            if (window.M_ENV) switch (window.M_ENV) {
                case "test":
                    return I.Develop;
                case "develop":
                case "pre":
                    return I.PreRelease
            }
        }

        function y(t) {
            if (!t) return Promise.resolve(!1);
            var e = window.hdp;
            try {
                if (e && e.isApp()) return e.getObj("mgj").then(function(t) {
                    return t.mwpEnable
                }, function() {
                    return Promise.resolve(!1)
                });
                var n = navigator.userAgent.toLowerCase();
                return t.test(n) ? window.mgj ? Promise.resolve(window.mgj.mwpEnable === !0) : new Promise(function(t) {
                    document.addEventListener("deviceready", function() {
                        try {
                            t(window.mgj.mwpEnable === !0)
                        } catch (e) {
                            t(!1)
                        }
                    }, !1)
                }) : Promise.resolve(!1)
            } catch (r) {
                return Promise.resolve(!1)
            }
        }

        function g(t) {
            return t && "function" == typeof t.then
        }

        function v(t, e) {
            return e = {
                exports: {}
            }, t(e, e.exports), e.exports
        }

        function w(t) {
            return !!t.constructor && "function" == typeof t.constructor.isBuffer && t.constructor.isBuffer(t)
        }

        function b(t) {
            return "function" == typeof t.readFloatLE && "function" == typeof t.slice && w(t.slice(0, 0))
        }

        function _(t) {
            return t ? "string" == typeof t ? t : JSON.stringify(t) : ""
        }
        var P, S = Object.setPrototypeOf || {
            __proto__: []
        }
        instanceof Array && function(t, e) {
            t.__proto__ = e
        } || function(t, e) {
            for (var n in e) e.hasOwnProperty(n) && (t[n] = e[n])
        }, O = /&/, T = /\+/g, j = Object.prototype.hasOwnProperty, E = function(t) {
            return t
        }, k = window.fetch, x = window.location, R = {
            text: "text/plain",
            form: "application/x-www-form-urlencoded",
            json: "application/json"
        }, M = window.navigator.userAgent.indexOf("MSIE 8.0") >= 0, C = "\u7f51\u7edc\u9519\u8bef\uff0c\u8bf7\u7a0d\u5019\u518d\u8bd5", D = "\u670d\u52a1\u5668\u5f00\u5c0f\u5dee\u4e86\uff0c\u8bf7\u7a0d\u5019\u518d\u8bd5";
        ! function(t) {
            t.MGJ = "mgj", t.MLS = "mls", t.XD = "xd"
        }(P || (P = {}));
        var A, I = {
                Develop: "DEVELOP",
                PreRelease: "PRE_RELEASE",
                Release: "RELEASE"
            },
            N = {
                Success: "SUCCESS",
                NeedHttps: "FAIL_SYS_NEED_HTTPS",
                TokenNeedRenew: "FAIL_SYS_TOKEN_NEED_RENEW",
                SessionInvalid: "FAIL_BIZ_SESSION_INVALID"
            },
            H = function() {
                try {
                    var t = location.hostname;
                    if (/(mogujie\.org|meili-inc\.com)$/.test(t)) return "nsh5"
                } catch (e) {}
                return "h5"
            }(),
            L = (A = {}, A[P.MGJ] = {
                Develop: "devapi.mogujie.com",
                PreRelease: "newpreapi.mogujie.com",
                Release: "api.mogujie.com"
            }, A[P.MLS] = {
                Develop: "devapi.meilishuo.com",
                PreRelease: "preapi.meilishuo.com",
                Release: "api.meilishuo.com"
            }, A[P.XD] = {
                Develop: "devapi.xiaodian.com",
                PreRelease: "preapi.xiaodian.com",
                Release: "api.xiaodian.com"
            }, A),
            W = "_mwp_h5_token",
            B = "__mgjuuid",
            J = function() {
                function t() {
                    this.data = {}
                }
                return t.prototype.add = function(t, e, n) {
                    return void 0 === n && (n = null), this.data[t + "." + e] = n, this
                }, t.prototype.toObject = function() {
                    return this.data
                }, t
            }(),
            U = function() {
                function t(t) {
                    this.callbacks = {}, this.Request = t
                }
                return t.prototype.addParameter = function(t, e, n) {
                    return this.parameter || (this.parameter = new J), this.parameter.add(t, e, n), this
                }, t.prototype.request = function(t, e, n, r) {
                    var o, i = this;
                    return n instanceof J ? o = n.toObject() : (o = this.parameter ? this.parameter.toObject() : null, r || (r = n || {})), this.promise = this.Request.request(t, e, o, r).then(function(t) {
                        return i.result = t, i.Request.filterResult(t)
                    }).then(function(t) {
                        var e = Object.keys(t).filter(function(t) {
                            return t in i.callbacks
                        }).map(function(e) {
                            return i.callbacks[e](t[e])
                        }).filter(g);
                        return e.length > 0 ? i.Request.Promise.all(e).then(function() {
                            return i.result
                        }) : i.result
                    }), this
                }, t.prototype.on = function(t, e) {
                    return this.callbacks[t] || (this.callbacks[t] = e), this
                }, t.prototype.then = function(t, e) {
                    return this.promise = this.promise.then(t, e), this
                }, t.prototype["catch"] = function(t) {
                    return this.promise = this.promise["catch"](t), this
                }, t.Parameter = J, t
            }(),
            q = v(function(t) {
                ! function() {
                    var e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
                        n = {
                            rotl: function(t, e) {
                                return t << e | t >>> 32 - e
                            },
                            rotr: function(t, e) {
                                return t << 32 - e | t >>> e
                            },
                            endian: function(t) {
                                if (t.constructor == Number) return 16711935 & n.rotl(t, 8) | 4278255360 & n.rotl(t, 24);
                                for (var e = 0; e < t.length; e++) t[e] = n.endian(t[e]);
                                return t
                            },
                            randomBytes: function(t) {
                                for (var e = []; t > 0; t--) e.push(Math.floor(256 * Math.random()));
                                return e
                            },
                            bytesToWords: function(t) {
                                for (var e = [], n = 0, r = 0; n < t.length; n++, r += 8) e[r >>> 5] |= t[n] << 24 - r % 32;
                                return e
                            },
                            wordsToBytes: function(t) {
                                for (var e = [], n = 0; n < 32 * t.length; n += 8) e.push(t[n >>> 5] >>> 24 - n % 32 & 255);
                                return e
                            },
                            bytesToHex: function(t) {
                                for (var e = [], n = 0; n < t.length; n++) e.push((t[n] >>> 4).toString(16)), e.push((15 & t[n]).toString(16));
                                return e.join("")
                            },
                            hexToBytes: function(t) {
                                for (var e = [], n = 0; n < t.length; n += 2) e.push(parseInt(t.substr(n, 2), 16));
                                return e
                            },
                            bytesToBase64: function(t) {
                                for (var n = [], r = 0; r < t.length; r += 3)
                                    for (var o = t[r] << 16 | t[r + 1] << 8 | t[r + 2], i = 0; 4 > i; i++) 8 * r + 6 * i <= 8 * t.length ? n.push(e.charAt(o >>> 6 * (3 - i) & 63)) : n.push("=");
                                return n.join("")
                            },
                            base64ToBytes: function(t) {
                                t = t.replace(/[^A-Z0-9+\/]/gi, "");
                                for (var n = [], r = 0, o = 0; r < t.length; o = ++r % 4) 0 != o && n.push((e.indexOf(t.charAt(r - 1)) & Math.pow(2, -2 * o + 8) - 1) << 2 * o | e.indexOf(t.charAt(r)) >>> 6 - 2 * o);
                                return n
                            }
                        };
                    t.exports = n
                }()
            }),
            G = {
                utf8: {
                    stringToBytes: function(t) {
                        return G.bin.stringToBytes(unescape(encodeURIComponent(t)))
                    },
                    bytesToString: function(t) {
                        return decodeURIComponent(escape(G.bin.bytesToString(t)))
                    }
                },
                bin: {
                    stringToBytes: function(t) {
                        for (var e = [], n = 0; n < t.length; n++) e.push(255 & t.charCodeAt(n));
                        return e
                    },
                    bytesToString: function(t) {
                        for (var e = [], n = 0; n < t.length; n++) e.push(String.fromCharCode(t[n]));
                        return e.join("")
                    }
                }
            },
            X = G,
            K = function(t) {
                return null != t && (w(t) || b(t) || !!t._isBuffer)
            },
            F = v(function(t) {
                ! function() {
                    var e = q,
                        n = X.utf8,
                        r = K,
                        o = X.bin,
                        i = function(t, s) {
                            t.constructor == String ? t = s && "binary" === s.encoding ? o.stringToBytes(t) : n.stringToBytes(t) : r(t) ? t = Array.prototype.slice.call(t, 0) : Array.isArray(t) || (t = t.toString());
                            for (var a = e.bytesToWords(t), u = 8 * t.length, c = 1732584193, h = -271733879, p = -1732584194, f = 271733878, d = 0; d < a.length; d++) a[d] = 16711935 & (a[d] << 8 | a[d] >>> 24) | 4278255360 & (a[d] << 24 | a[d] >>> 8);
                            a[u >>> 5] |= 128 << u % 32, a[(u + 64 >>> 9 << 4) + 14] = u;
                            for (var l = i._ff, m = i._gg, y = i._hh, g = i._ii, d = 0; d < a.length; d += 16) {
                                var v = c,
                                    w = h,
                                    b = p,
                                    _ = f;
                                c = l(c, h, p, f, a[d + 0], 7, -680876936), f = l(f, c, h, p, a[d + 1], 12, -389564586), p = l(p, f, c, h, a[d + 2], 17, 606105819), h = l(h, p, f, c, a[d + 3], 22, -1044525330), c = l(c, h, p, f, a[d + 4], 7, -176418897), f = l(f, c, h, p, a[d + 5], 12, 1200080426), p = l(p, f, c, h, a[d + 6], 17, -1473231341), h = l(h, p, f, c, a[d + 7], 22, -45705983), c = l(c, h, p, f, a[d + 8], 7, 1770035416), f = l(f, c, h, p, a[d + 9], 12, -1958414417), p = l(p, f, c, h, a[d + 10], 17, -42063), h = l(h, p, f, c, a[d + 11], 22, -1990404162), c = l(c, h, p, f, a[d + 12], 7, 1804603682), f = l(f, c, h, p, a[d + 13], 12, -40341101), p = l(p, f, c, h, a[d + 14], 17, -1502002290), h = l(h, p, f, c, a[d + 15], 22, 1236535329), c = m(c, h, p, f, a[d + 1], 5, -165796510), f = m(f, c, h, p, a[d + 6], 9, -1069501632), p = m(p, f, c, h, a[d + 11], 14, 643717713), h = m(h, p, f, c, a[d + 0], 20, -373897302), c = m(c, h, p, f, a[d + 5], 5, -701558691), f = m(f, c, h, p, a[d + 10], 9, 38016083), p = m(p, f, c, h, a[d + 15], 14, -660478335), h = m(h, p, f, c, a[d + 4], 20, -405537848), c = m(c, h, p, f, a[d + 9], 5, 568446438), f = m(f, c, h, p, a[d + 14], 9, -1019803690), p = m(p, f, c, h, a[d + 3], 14, -187363961), h = m(h, p, f, c, a[d + 8], 20, 1163531501), c = m(c, h, p, f, a[d + 13], 5, -1444681467), f = m(f, c, h, p, a[d + 2], 9, -51403784), p = m(p, f, c, h, a[d + 7], 14, 1735328473), h = m(h, p, f, c, a[d + 12], 20, -1926607734), c = y(c, h, p, f, a[d + 5], 4, -378558), f = y(f, c, h, p, a[d + 8], 11, -2022574463), p = y(p, f, c, h, a[d + 11], 16, 1839030562), h = y(h, p, f, c, a[d + 14], 23, -35309556), c = y(c, h, p, f, a[d + 1], 4, -1530992060), f = y(f, c, h, p, a[d + 4], 11, 1272893353), p = y(p, f, c, h, a[d + 7], 16, -155497632), h = y(h, p, f, c, a[d + 10], 23, -1094730640), c = y(c, h, p, f, a[d + 13], 4, 681279174), f = y(f, c, h, p, a[d + 0], 11, -358537222), p = y(p, f, c, h, a[d + 3], 16, -722521979), h = y(h, p, f, c, a[d + 6], 23, 76029189), c = y(c, h, p, f, a[d + 9], 4, -640364487), f = y(f, c, h, p, a[d + 12], 11, -421815835), p = y(p, f, c, h, a[d + 15], 16, 530742520), h = y(h, p, f, c, a[d + 2], 23, -995338651), c = g(c, h, p, f, a[d + 0], 6, -198630844), f = g(f, c, h, p, a[d + 7], 10, 1126891415), p = g(p, f, c, h, a[d + 14], 15, -1416354905), h = g(h, p, f, c, a[d + 5], 21, -57434055), c = g(c, h, p, f, a[d + 12], 6, 1700485571), f = g(f, c, h, p, a[d + 3], 10, -1894986606), p = g(p, f, c, h, a[d + 10], 15, -1051523), h = g(h, p, f, c, a[d + 1], 21, -2054922799), c = g(c, h, p, f, a[d + 8], 6, 1873313359), f = g(f, c, h, p, a[d + 15], 10, -30611744), p = g(p, f, c, h, a[d + 6], 15, -1560198380), h = g(h, p, f, c, a[d + 13], 21, 1309151649), c = g(c, h, p, f, a[d + 4], 6, -145523070), f = g(f, c, h, p, a[d + 11], 10, -1120210379), p = g(p, f, c, h, a[d + 2], 15, 718787259), h = g(h, p, f, c, a[d + 9], 21, -343485551), c = c + v >>> 0, h = h + w >>> 0, p = p + b >>> 0, f = f + _ >>> 0
                            }
                            return e.endian([c, h, p, f])
                        };
                    i._ff = function(t, e, n, r, o, i, s) {
                        var a = t + (e & n | ~e & r) + (o >>> 0) + s;
                        return (a << i | a >>> 32 - i) + e
                    }, i._gg = function(t, e, n, r, o, i, s) {
                        var a = t + (e & r | n & ~r) + (o >>> 0) + s;
                        return (a << i | a >>> 32 - i) + e
                    }, i._hh = function(t, e, n, r, o, i, s) {
                        var a = t + (e ^ n ^ r) + (o >>> 0) + s;
                        return (a << i | a >>> 32 - i) + e
                    }, i._ii = function(t, e, n, r, o, i, s) {
                        var a = t + (n ^ (e | ~r)) + (o >>> 0) + s;
                        return (a << i | a >>> 32 - i) + e
                    }, i._blocksize = 16, i._digestsize = 16, t.exports = function(t, n) {
                        if (void 0 === t || null === t) throw new Error("Illegal argument " + t);
                        var r = e.wordsToBytes(i(t, n));
                        return n && n.asBytes ? r : n && n.asString ? o.bytesToString(r) : e.bytesToHex(r)
                    }
                }()
            }),
            V = "mw-ttid",
            Y = "mw-t",
            Q = "data",
            $ = "mw-appkey",
            z = "mw-sign",
            Z = "mw-did",
            tt = "mw-uid",
            et = "mw-cmd-v",
            nt = "mw-uuid",
            rt = ["mw-pv", "mw-sid", Z];
        "function" != typeof Date.now && (Date.now = function() {
            return (new Date).getTime()
        });
        var ot = function() {
            function t() {
                this._params = {}, this._omitted = {}
            }
            return t.prototype.add = function(t, e) {
                return rt.indexOf(t) >= 0 ? (this._omitted[t] = e, this) : ((e || "data" === t) && (this._params[t] = e), this)
            }, t.prototype.sign = function(t, e, n, r) {
                var o = this._params,
                    i = Object.keys(o);
                return i.sort(), F(i.map(function(t) {
                    return o[t]
                }).concat([t, e, F(n), r]).join("&"))
            }, t.prototype.getSignedParams = function(t) {
                var e = this,
                    n = t.constructor;
                this.add($, n.AppKey).add(Y, String(Date.now())).add(nt, t.getUUID()).add(V, n.TTID);
                var r = t.getMWPCookieHeader();
                Object.keys(r).forEach(function(t) {
                    t.startsWith("mw-cookie-") && e.add(t, r[t])
                });
                var o = _(t.data);
                return this.add(z, this.sign(t.api, t.version, o, t.getToken())).add(Q, o), Object.assign({}, this._omitted, this._params)
            }, t.getSignedParams = function(e) {
                return (new t).getSignedParams(e)
            }, t
        }();
        ! function(t) {
            t.Key = {
                KEY_DEVICE_ID: Z,
                KEY_UID: tt,
                KEY_CMD_V: et
            }
        }(ot || (ot = {}));
        var it, st = ot,
            at = function() {
                function t(t) {
                    var e = this;
                    this.callback = t, this.promise = new Promise(function(t, n) {
                        e.resolve = t, e.reject = n
                    })
                }
                return t.prototype.exec = function() {
                    return this.callback().then(this.resolve, this.reject)
                }, t.prototype.then = function(t, e) {
                    return this.promise = this.promise.then(t, e)
                }, t.prototype["catch"] = function(t) {
                    return this.promise = this.promise["catch"](t)
                }, t
            }(),
            ut = function() {
                function t() {
                    this.tasks = []
                }
                return t.createQueue = function() {
                    var t = new this;
                    return this.instances.push(t), t
                }, t.getQueue = function() {
                    return this.instances[0]
                }, t.prototype.add = function(t) {
                    try {
                        var e = new at(t);
                        return this.tasks.push(e), e
                    } catch (n) {
                        return null
                    }
                }, t.prototype.exec = function() {
                    var e = this;
                    t.instances = t.instances.filter(function(t) {
                        return e !== t
                    });
                    var n = function() {
                        return e.tasks = null
                    };
                    return Promise.all(this.tasks.map(function(t) {
                        return t.exec()
                    })).then(n, n)
                }, t.instances = [], t
            }(),
            ct = function() {
                function t(t, e, n) {
                    void 0 === n && (n = {}), this.retries = 1, this.api = t, this.version = e;
                    var r = this.constructor.defaultOptions;
                    this.options = Object.assign({}, r, n), this.options.headers = Object.assign({}, r.headers, n.headers)
                }
                return t.getContext = function(t, e, n) {
                    return new this(t, e, n)
                }, t.request = function(t, e, n, r) {
                    return this.getContext(t, e, r).request(n)
                }, t.setHeader = function(t, e) {
                    var n = this.defaultOptions;
                    n.headers || (n.headers = {}), n.headers[t] = e
                }, t.getDSL = function() {
                    return new U(this)
                }, t.getDSLParameter = function() {
                    return new U.Parameter
                }, t.setGlobalEnv = function(t) {
                    t && (this.defaultOptions.env = t)
                }, t.getGlobalEnv = function() {
                    return this.defaultOptions.env
                }, t.getMWPCookies = function(t, e) {
                    return this.MWPCookieJar.getCookies(this.getContext(t, e))
                }, t.prototype.shouldRetry = function() {
                    return this.retries < 5
                }, t.prototype.getToken = function() {
                    throw new Error("Method not implemented.")
                }, t.prototype.getUUID = function() {
                    return ""
                }, t.prototype.getParams = function() {
                    return st.getSignedParams(this)
                }, t.prototype.getHostname = function() {
                    var t = this.constructor.Hostname;
                    switch (this.options.env) {
                        case I.Develop:
                            return t.Develop;
                        case I.PreRelease:
                            return t.PreRelease;
                        default:
                            return t.Release
                    }
                }, t.prototype.getOrigin = function() {
                    var t = this.options,
                        e = t.useHTTPS ? "https:" : "http:";
                    return e + "//" + this.getHostname()
                }, t.prototype.getURL = function() {
                    return this.getOrigin() + "/" + H + "/" + this.api + "/" + this.version + "/"
                }, t.prototype.getHeaders = function() {
                    return Object.assign({}, this.options.headers)
                }, t.prototype.getMWPCookies = function() {
                    return this.constructor.MWPCookieJar.getCookies(this)
                }, t.prototype.getMWPCookieHeader = function() {
                    var t = {},
                        e = this.getMWPCookies();
                    return Object.keys(e).length > 0 && (t["mw-cookie-" + this.api.replace(/\./g, "") + this.version] = Object.keys(e).map(function(t) {
                        return t + "=" + e[t]
                    }).join("; ") + ";"), t
                }, t.prototype.request = function(t) {
                    return this.data = t, this.getToken() ? this._fetch() : this.enqueue()
                }, t.prototype.fetch = function(t, e) {
                    e(new Error("Please implement `fetch` method in your own subclass"))
                }, t.prototype.handleResponse = function(t) {
                    switch (t.ret) {
                        case N.TokenNeedRenew:
                            return this._fetch();
                        case N.NeedHttps:
                            return this.options.useHTTPS = !0, this._fetch();
                        default:
                            return this.constructor.Promise.resolve(t)
                    }
                }, t.prototype._fetch = function() {
                    var t = this;
                    return new this.constructor.Promise(function(e, n) {
                        return t.shouldRetry() ? (t.retries++, void t.fetch(e, n)) : (console.warn("Have retried too much times"), n(new Error(D)))
                    }).then(function(e) {
                        return t.handleResponse(e)
                    })
                }, t.prototype.enqueue = function() {
                    var t = ut.getQueue();
                    if (t) {
                        var e = t.add(this._fetch.bind(this));
                        return null === e ? this._fetch() : e
                    }
                    t = ut.createQueue();
                    var n = this._fetch(),
                        r = t.exec.bind(t);
                    return n.then(r, r), n
                }, t.Promise = Promise, t.Env = I, t.Hostname = L[P.MGJ], t.Code = N, t.defaultOptions = {
                    useHTTPS: !1,
                    env: I.Release
                }, t.v = "3.1.1", t.filterResult = l, t
            }(),
            ht = /iPhone|iPad|iPod|Android|BlackBerry|IEMobile|Opera Mini/i;
        ! function(t) {
            t.PC = "pc", t.H5 = "h5"
        }(it || (it = {}));
        var pt, ft, dt, lt = (pt = {}, pt[P.MGJ] = /\.mogujie\.com$/, pt[P.MLS] = /\.meilishuo\.com$/, pt[P.XD] = /\.xiaodian\.com$/, pt),
            mt = (ft = {}, ft[P.MGJ] = /mogujie4/, ft[P.XD] = /xiaodian4/, ft),
            yt = (dt = {}, dt[P.MGJ] = "100028", dt[P.MLS] = "100066", dt[P.XD] = "100028", dt),
            gt = function() {
                function t(e) {
                    void 0 === e && (e = location.hostname), this.userAgent = navigator.userAgent.toLowerCase(), this.version = "1.0", this.type = t.getType(e), this.platform = t.getPlatform(this.userAgent)
                }
                return t.getType = function(t) {
                    var e = P.MGJ;
                    return Object.keys(lt).some(function(n) {
                        return lt[n].test(t) ? (e = n, !0) : !1
                    }), e
                }, t.getPlatform = function(e) {
                    return t.isMobile(e) ? it.H5 : it.PC
                }, t.isMobile = function(t) {
                    return ht.test(t)
                }, t.prototype.getHostname = function() {
                    return L[this.type]
                }, t.prototype.getUserAgentTester = function() {
                    return mt[this.type]
                }, t.prototype.getTTID = function() {
                    return "NMMain@" + [this.type, this.platform, this.version].join("_")
                }, t.prototype.getAppKey = function() {
                    return yt[this.type]
                }, t
            }(),
            vt = function() {},
            wt = function(e) {
                function r() {
                    var t = null !== e && e.apply(this, arguments) || this;
                    return t.retriesOnSignError = !1, t
                }
                return t(r, e), r.config = function(t) {
                    void 0 === t && (t = {});
                    var e = this.adaptor;
                    ["type", "platform", "version"].forEach(function(n) {
                        t[n] && (e[n] = t[n])
                    }), this.AppKey = e.getAppKey(), this.TTID = e.getTTID(), this.Hostname = e.getHostname(), this.useNativeMWP = y(e.getUserAgentTester()), this.setGlobalEnv(t.env)
                }, r.prototype.request = function(t) {
                    var n = this;
                    return r.useNativeMWP.then(function(r) {
                        return r ? (n.data = t, n._fetch()) : e.prototype.request.call(n, t)
                    })
                }, r.prototype.getToken = function() {
                    return f(W)
                }, r.prototype.getUUID = function() {
                    return f(B)
                }, r.prototype.getParams = function() {
                    var t = new st,
                        e = this.options.headers;
                    return e && Object.keys(e).forEach(function(n) {
                        n.startsWith("mw-") && t.add(n, e[n])
                    }), t.getSignedParams(this)
                }, r.prototype.fetch = function(t, e) {
                    var n = this;
                    return this.options.forceJSONP ? void this._fetchByWeb(t, e) : void r.useNativeMWP.then(function(r) {
                        r ? n._fetchByNative(t, e) : n._fetchByWeb(t, e)
                    })
                }, r.prototype.getMWPCookieHeader = function() {
                    return {}
                }, r.prototype.getMWPCookies = function() {
                    return {}
                }, r.prototype._fetchByNative = function(t, e) {
                    "number" == typeof this.version && (this.version = String(this.version)), window.mgj.ajax.mwp(t, e, this.api, this.version, this.data, "get", !this.options.useHTTPS)
                }, r.prototype._fetchByWeb = function(t, e) {
                    var n = function(n, r) {
                        return n ? void e(n) : void t(r)
                    };
                    this.options.cors === !0 ? this._fetchWithCORS(n) : this._fetchWithJSONP(n)
                }, r.prototype._fetchWithJSONP = function(t) {
                    var e = this.getURL(),
                        r = this.getParams(),
                        o = "mwpCb" + d();
                    this.constructor.adaptor.userAgent.indexOf("xcore") > -1 ? (window[o] = function(e) {
                        t(null, e)
                    }, r.callback = o, r._ = Date.now(), loader.script(e + (~e.indexOf("?") ? "&" : "?") + n(r), vt, t)) : i(e, {
                        data: r,
                        jsonpCallback: o
                    }, t)
                }, r.prototype._fetchWithCORS = function(t) {
                    var e = this.getURL(),
                        n = this.getParams(),
                        r = {
                            method: this.options.method,
                            data: n,
                            dataType: "json",
                            credentials: "include",
                            headers: {
                                "content-type": R.form
                            }
                        };
                    "function" == typeof fetch ? a(e, r, t) : XMLHttpRequest ? s(e, r, t) : this._fetchWithJSONP(t)
                }, r.prototype.handleResponse = function(t) {
                    return "FAIL_SYS_SIGN_ERROR" !== t.ret || this.retriesOnSignError ? e.prototype.handleResponse.call(this, t) : (this.retriesOnSignError = !0, ut.getQueue() || p("_mwp_h5_token", null, {
                        domain: ".meilishuo.com",
                        path: "/"
                    }), this.enqueue())
                }, r.adaptor = new gt, r.Platform = {
                    PC: it.PC,
                    H5: it.H5
                }, r.Type = {
                    MGJ: P.MGJ,
                    MLS: P.MLS,
                    XD: P.XD
                }, r.defaultOptions = Object.assign({}, ct.defaultOptions, {
                    useHTTPS: "https:" === location.protocol,
                    method: "GET"
                }), r
            }(ct);
        return wt.config(), wt.setGlobalEnv(m()), wt
    }()
}(this.M || this.MoGu || this);

function makeCallBackDelay(e, a) {
    return function() {
        var t = a.offset().top,
            n = 0,
            o = arguments,
            r = !1;
        if (t > window.innerHeight && 0 === $(window).scrollTop()) {
            n = 1500;
            var c = setTimeout(function() {
                r = !0, e.apply(a, o)
            }, n);
            $(document).one("touchmove scroll", function() {
                c && clearTimeout(c), r || (r = !0, e.apply(a, o))
            })
        } else e.apply(a, o)
    }
}
$.fn.listenToLazyData = function(e) {
    var a = $(this).attr("data-source-key"),
        t = $(this).attr("data-refresh-type");
    return t && (a = a + "" + t), MoGu && MoGu.lazyInstance && MoGu.lazyInstance._cache && MoGu.lazyInstance._cache[a] ? void makeCallBackDelay(e, $(this))({}, !0, "", a, MoGu.lazyInstance._cache[a] || [], !1) : void $(this).one("receive-data", makeCallBackDelay(e, $(this)))
}, define("base/core/datalazy", ["base/MoGu"], function(e) {
    function a(e) {
        window.console && console.warn && console.warn.apply && console.warn.apply && console.log.apply(console, arguments)
    }

    function t(e) {
        window.console && console.error && console.error.apply && console.error.apply(console, arguments)
    }

    function n(e, a, t) {
        var n = e.top,
            o = n + e.height;
        return t = t || 0, !(o < a - t || n > a + m + t)
    }

    function o(e) {
        return "none" != e.css("display") && "hidden" != e.css("visibility") && 0 != e.css("opacity") && e.width()
    }

    function r(e) {
        var a = {},
            t = e.split(";");
        return $(t).each(function(e, t) {
            var n = t.split("="),
                o = n[0];
            o && (a[o] = t.replace(o + "=", ""))
        }), a
    }

    function c(e) {
        return e.split(";").sort().join("")
    }

    function i(a, t, n) {
        var o = a.find("#template-tpl").html(),
            r = e.ui.getTemplate(o, t || []),
            c = a.find(a.attr("data-placeholder") || ".entry-wrap");
        n ? c.append(r) : c.html(r)
    }

    function p(e) {
        !this instanceof p && t("please new function"), this.init(e)
    }
    "function" != typeof Object.assign && ! function() {
        Object.assign = function(e) {
            "use strict";
            if (void 0 === e || null === e) throw new TypeError("Cannot convert undefined or null to object");
            for (var a = Object(e), t = 1; t < arguments.length; t++) {
                var n = arguments[t];
                if (void 0 !== n && null !== n)
                    for (var o in n) n.hasOwnProperty(o) && (a[o] = n[o])
            }
            return a
        }
    }(), Object.keys || (Object.keys = function() {
        "use strict";
        var e = Object.prototype.hasOwnProperty,
            a = !{
                toString: null
            }.propertyIsEnumerable("toString"),
            t = ["toString", "toLocaleString", "valueOf", "hasOwnProperty", "isPrototypeOf", "propertyIsEnumerable", "constructor"],
            n = t.length;
        return function(o) {
            if ("object" != typeof o && ("function" != typeof o || null === o)) throw new TypeError("Object.keys called on non-object");
            var r, c, i = [];
            for (r in o) e.call(o, r) && i.push(r);
            if (a)
                for (c = 0; c < n; c++) e.call(o, t[c]) && i.push(t[c]);
            return i
        }
    }()), Array.prototype.forEach || (Array.prototype.forEach = function(e, a) {
        var t, n;
        if (null == this) throw new TypeError("this is null or not defined");
        var o = Object(this),
            r = o.length >>> 0;
        if ("function" != typeof e) throw new TypeError(e + " is not a function");
        for (arguments.length > 1 && (t = a), n = 0; n < r;) {
            var c;
            n in o && (c = o[n], e.call(t, c, n, o)), n++
        }
    });
    var u = {
            dynamic: {
                url: "//mce.mogucdn.com/jsonp/multiget/3",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/get/3",
                param: "pids",
                backupParam: "pid",
                type: "jsonp"
            },
            merge: {
                url: "//mce.mogucdn.com/jsonp/multiget/3",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/get/3",
                param: "pids",
                backupParam: "pid",
                type: "jsonp"
            },
            appolo: {
                url: "//mce.mogucdn.com/jsonp/multiget/3",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/get/3",
                param: "pids",
                backupParam: "pid",
                type: "jsonp"
            },
            mceats: {
                url: "//mce.mogucdn.com/jsonp/multiget/3",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/get/3",
                param: "pids",
                backupParam: "pid",
                type: "jsonp"
            },
            mcereconline: {
                url: "mwp.darwin.multiget",
                versionNum: "4",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/multiget/3",
                param: "pids",
                backupParam: "pids",
                type: "mwp"
            },
            mcereconlyonline: {
                url: "mwp.darwin.get",
                versionNum: "4",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/get/3",
                param: "pid",
                backupParam: "pid",
                type: "mwp"
            },
            mce: {
                url: "//mce.mogucdn.com/jsonp/multiget/3",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/multiget/3",
                param: "pids",
                backupParam: "pids",
                type: "jsonp"
            },
            mceonly: {
                url: "//mce.mogucdn.com/jsonp/get/3",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/get/3",
                param: "pid",
                backupParam: "pid",
                type: "jsonp"
            },
            mceonline: {
                url: "mwp.darwin.multiget",
                versionNum: "3",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/multiget/3",
                param: "pids",
                backupParam: "pids",
                type: "mwp"
            },
            mceonlyonline: {
                url: "mwp.darwin.get",
                versionNum: "3",
                backupUrl: "//mcebackup.mogucdn.com/jsonp/get/3",
                param: "pid",
                backupParam: "pid",
                type: "mwp"
            }
        },
        s = 20,
        l = 80,
        d = {
            loading: 1,
            success: 2,
            paging: 3,
            error: 4
        },
        m = $(window).height();
    return p.DEFAULT_CONFIG = {
        timeout: 8e3,
        deviation: m,
        SELECTORS: {
            COLD: ".coldData",
            AJAX: ".lazyData"
        }
    }, p.prototype = {
        _cache: {},
        _ajaxMap: {},
        _hasReRendered: !1,
        handler: null,
        destory: function() {
            $(window).off("scroll touchmove resize", this.handler)
        },
        init: function(e) {
            var a = this;
            this.config = $.extend({}, p.DEFAULT_CONFIG, e), this.prepareAjaxData(), this.loadAjaxData(), this.handler = function() {
                a.loadAjaxData.call(a)
            }, $(window).on("scroll touchmove resize", this.handler)
        },
        prepareAjaxData: function(e) {
            var t = this.config.SELECTORS,
                n = $(t.AJAX),
                o = this,
                i = {},
                p = {},
                d = {};
            n.length;
            this.$elems = n, n.each(function(t) {
                var n = $(this),
                    m = n.attr("data-source-type"),
                    f = +n.attr("data-floornum") || s,
                    h = n.attr("data-source-alone") || "",
                    y = n.attr("data-extra-param") || "",
                    g = n.offset(),
                    w = e ? "" + +new Date : "";
                if (!u[m]) return void a("unknown data source type", m);
                if (y) {
                    var v = c(y);
                    d[v] ? w = d[v] : d[v] = w = "" + +new Date, y = r(y)
                }
                h && (w = "" + +new Date), m += w, i[m] = i[m] ? i[m] : 0, p[m] = p[m] ? p[m] : 1, i[m] += f, i[m] > l && (i[m] = 0, p[m]++), m += p[m];
                var j = o._ajaxMap[m] = o._ajaxMap[m] || {
                    source: $.extend({}, u[n.data("source-type")], {
                        data: y || {}
                    }),
                    refreshType: w,
                    list: [],
                    offset: g
                };
                j.list.push({
                    key: n.attr("data-source-key"),
                    dom: n,
                    offset: g,
                    param: null
                }), g.top < j.offset.top && $.extend(j.offset, g), n.attr("data-source-type", ""), w && n.attr("data-refresh-type", w)
            })
        },
        updateAjaxMap: function(e) {
            if (e = "boolean" == typeof e && e, this._hasReRendered && (e = !0, this._hasReRendered = !1), e) {
                var t = this._ajaxMap;
                Object.keys(t).forEach(function(e) {
                    var n = t[e],
                        o = n.list;
                    if (!n.status)
                        for (var r = 0; r < o.length; r++) {
                            var c = o[r],
                                i = c.dom,
                                p = i.offset(),
                                u = i.attr("data-source-key");
                            u || a("source-key of the current dom should exist"), u !== c.key && a("source-key[", u, "] of the current dom should match", c.key), c.offset = p
                        }
                })
            }
        },
        loadAjaxData: function() {
            this.updateAjaxMap();
            var e = this._ajaxMap,
                t = $(window).scrollTop(),
                r = this._cache,
                c = this;
            for (var p in e) ! function(p) {
                var u = e[p];
                if (!u.status) {
                    for (var s = u.list, l = u.source, m = u.refreshType, f = !1, h = 0; !f && h < s.length; h++) f = f || n(s[h].offset, t, c.config.deviation) && o(s[h].dom);
                    if (f) {
                        for (var y = [], h = 0; h < s.length; h++) y.push(s[h].key);
                        y = y.join(",");
                        var g = function(e) {
                                var a = {};
                                for (var t in e) e.hasOwnProperty(t) && (a[t + m] = e[t].list);
                                $.extend(r, a);
                                for (var n = 0; n < s.length; n++) {
                                    var o = s[n],
                                        p = $(o.dom),
                                        l = o.key + m;
                                    r[l] && (p.attr("data-manual") || i(p, r[l]), p.trigger("receive-data", [!0, "", l, r[l] || []]))
                                }
                                u.status = d.success, setTimeout(function() {
                                    c._hasReRendered = !0, $(window).trigger("scroll")
                                }, 50)
                            },
                            w = function(e) {
                                if (e && e.success && e.returnCode && "SUCCESS" == e.returnCode) {
                                    var a = {};
                                    e.data && e.data.list ? a[y] = e.data : a = e.data, g(a)
                                } else v(new Error(e && e.returnCode || "error interface"))
                            },
                            v = function(e) {
                                var t = null;
                                if (!e) return t = $.Deferred(), t.resolve(null), t;
                                if (a("use backup url due to", e.toString()), !l.backupUrl) return void a("no backupUrl");
                                var n = $.ajax;
                                $._ajax && "jsonp" === l.type && (n = $._ajax);
                                var o = $.extend({}, l.data),
                                    r = "jsonp" + y.replace(/,/g, "_") + "backup";
                                n.call($, {
                                    url: l.backupUrl,
                                    type: "GET",
                                    dataType: "jsonp",
                                    cache: !0,
                                    beforeSend: function(e, a) {
                                        a.url = a.url.substring(0, a.url.indexOf("?"));
                                        var t = "";
                                        t = window && "h5" == window.MOGU_PLATFORM ? "&appPlat=m" : window && "pc" == window.MOGU_PLATFORM ? "&appPlat=pc" : "", a.url += "%3F" + l.backupParam + "=" + y + t + "&callback=" + r
                                    },
                                    jsonpCallback: r,
                                    data: o
                                }).then(function(e) {
                                    j.call(this, e, y)
                                })
                            },
                            j = function(e, a) {
                                if (e && e.success && e.returnCode && "SUCCESS" == e.returnCode) {
                                    var t = {};
                                    e.data && e.data.list ? t[a] = e.data : t = e.data, g(t)
                                }
                            };
                        u.status = d.loading;
                        var b = $.ajax;
                        $._ajax && "jsonp" === l.type && (b = $._ajax);
                        var k = {};
                        if ($(".page_activity").hasClass("debug") && (k = $.extend(k, {
                                testing: 1
                            })), window && "h5" == window.MOGU_PLATFORM) var O = $.extend(k, l.data, {
                            appPlat: "m"
                        });
                        else if (window && "pc" == window.MOGU_PLATFORM) var O = $.extend(k, l.data, {
                            appPlat: "pc"
                        });
                        else var O = $.extend(k, l.data);
                        O[l.param] = y;
                        var x = "jsonp" + y.replace(/,/g, "_");
                        x && window[x] && "function" == typeof window[x] && (x += "new");
                        var _ = function() {
                                b.call($, {
                                    url: l.url,
                                    type: "jsonp" !== l.type ? l.type : "GET",
                                    dataType: "jsonp" !== l.type ? "json" : "jsonp",
                                    data: O,
                                    cache: !0,
                                    timeout: c.config.timeout,
                                    jsonpCallback: x
                                }).done(w).fail(v)
                            },
                            P = function(e) {
                                M && M.MWP && M.MWP.request(l.url, l.versionNum, e).then(function(e) {
                                    if (e && e.ret && "SUCCESS" == e.ret) {
                                        var a = Object.assign({}, e);
                                        a.returnCode = e.ret, a.success = !0, w(a)
                                    } else v(new Error(e && e.ret || "error return null"))
                                })["catch"](function(e) {
                                    v(e)
                                })
                            };
                        "mwp" == l.type ? M && M.ua && M.ua["native"] && window.hdp ? document.addEventListener("deviceready", function() {
                            mgj.device.signParams(function(e) {
                                "string" == typeof e && (e = JSON.parse(e)), O.did = e._did, P(O)
                            }, function() {
                                P(O)
                            }, {})
                        }, !1) : P(O) : _()
                    }
                }
            }(p)
        }
    }, p
}), require(["base/MoGu", "base/core/datalazy"], function(e, a) {
    $(function() {
        var t = new a;
        return e.lazyInstance = t, e
    })
});
! function() {
    window.PTP_PARAMS = window.PTP_PARAMS || {};
    var a = "cube-acm-node",
        t = "show-log-item",
        n = "anchor",
        e = "module_row",
        r = function(a, t) {
            t = t || location.href, t = t.split("#")[0];
            var n = new RegExp("(^|\\?|&)" + a + "=([^&]*)(\\s|&|$)", "i");
            return n.test(t) ? RegExp.$2.replace(/\+/g, " ") : ""
        };
    $.extend(window.PTP_PARAMS, {
        urlExtendFn: function(s) {
            var l, i = $(s),
                o = i.parents(),
                c = i.attr("data-ext-acm") || "",
                h = i.attr("href") || "",
                f = h && h.indexOf("acm=") !== -1,
                d = i.hasClass(a) || i.hasClass(n) || i.hasClass(t) ? i : null,
                m = 0,
                u = 0;
            $(o).each(function(n, r) {
                d || !$(r).hasClass(a) && !$(r).hasClass(t) || (d = $(r)), $(r).hasClass(e) && (l = $(r))
            });
            var g = null;
            l && l.length && (g = $(l).find("." + a + ",." + n + ",." + t), u = g && g.length), g && g.length && d && d.length && g.each(function(a, t) {
                $(t)[0] === d[0] && (m = a)
            });
            var x = l && l.attr("data-acm") || "";
            if (x) {
                if (f && !c) {
                    if (h && h.indexOf("mf_") !== -1) return;
                    c = r("acm", h)
                }
                x = x.split(".");
                var w = "";
                return c.indexOf("mf_") === -1 && (w = c + (c ? x[6] ? "-" + x[6] : "" : x.join("."))), w && d && d.length && (w += "-idx_" + m), w && g && g.length && (w += "-mfs_" + u), !d && c && i && i.removeAttr && i.removeAttr("data-ext-acm"), {
                    acm: w ? w : c
                }
            }
        }
    })
}();
! function(e) {
    function n(i) {
        if (o[i]) return o[i].exports;
        var t = o[i] = {
            exports: {},
            id: i,
            loaded: !1
        };
        return e[i].call(t.exports, t, t.exports, n), t.loaded = !0, t.exports
    }
    var o = {};
    return n.m = e, n.c = o, n.p = "", n(0)
}([function(e, n, o) {
    var i = o(1),
        t = (Date.now || function() {
            return (new Date).getTime()
        }, function(e) {
            this.opts = $.extend({}, this.defaults, e), this.scrollIndTime = i.is_ie_old ? 400 : 200, this.fistCheck = !1, this.imgErrorClock = {}, this.logInfo = {
                type: i.loadType,
                protocol: i.protocol,
                num: 0,
                succ: 0,
                err: 0,
                domainInfo: {}
            }, this.logTimer = 0, this.init()
        });
    t.prototype = {
        init: function() {
            var e = this,
                n = 0;
            $(window).scroll(function(o) {
                clearTimeout(n), n = setTimeout(function() {
                    e.checkImages()
                }, e.scrollIndTime)
            }), setTimeout(function() {
                i.checkNeedCdnBanlance(), e.fistCheck = !0, e.checkImages()
            }, 0), _imgLog(e.logInfo), e.logTimer = setTimeout(e.pubInfoLog.bind(e), 3e3)
        },
        getInActiveFlag: function(e, n) {
            var o, i, t, a, r = n[0],
                d = r.getBoundingClientRect && r.getBoundingClientRect();
            d ? (o = d.top + e.scrollTop, i = d.bottom + e.scrollTop, t = d.left, a = d.right) : (o = n.offset().top, i = o + n.height(), t = n.offset().left, a = t + n.width());
            var l = i > e.top && o < e.bot,
                s = a > e.left && t < e.right;
            return !(!l || !s) && !("none" == n.css("display") || "hidden" == n.css("visibility") || 0 == n.css("opacity") || !n[0].offsetWidth)
        },
        checkModRow: function(e) {
            var n = this,
                o = $(".mod_row");
            return o.each(function(o, i) {
                var t = $(i);
                n.getInActiveFlag(e, t) ? t.addClass("J_mod_row_show") : t.removeClass("J_mod_row_show")
            }), $(".J_mod_row_show")
        },
        checkImages: function(e) {
            var n = this;
            if (n.fistCheck) {
                var o = document.documentElement.scrollTop || document.body.scrollTop,
                    t = n.opts.showDistance,
                    a = {};
                a.top = o - t, a.bot = o + (i.clientHeight || document.documentElement.clientHeight || document.body.clientHeight) + t, a.left = 0, a.right = i.clientWidth, a.scrollTop = o;
                var r = $("body");
                e ? r = e : window.MOGU_MF_DEVELOP_ENV && $(".mod_row").length > 0 && (r = n.checkModRow(a)), setTimeout(function() {
                    for (var e = r.hasClass(n.opts.objsClassName) ? r : r.find("." + n.opts.objsClassName), o = e.length, i = 0; i < o; i++) {
                        var t = e.eq(i);
                        if (t.attr("img-src")) {
                            var d = t.hasClass("J_loading_success"),
                                l = t.hasClass("J_loading"),
                                s = t.attr("need-remove") ? t.attr("need-remove") : "no";
                            if (!d || "yes" == s) {
                                var g = n.getInActiveFlag(a, t);
                                if (g) d || l || n.getLoadImage(t);
                                else if ("yes" == s && (d || l))
                                    if (t.removeClass("J_loading"), t.removeClass("J_loading_success"), "background" == t.attr("insert-model")) t[0].style.backgroundImage = "none";
                                    else {
                                        var c = t.find(".J_dynamic_img");
                                        c.remove()
                                    }
                            }
                        }
                    }
                }, 0)
            }
        },
        preloadImages: function(e) {
            var n = this;
            setTimeout(function() {
                if (e && e.length && e.hasClass && e.find)
                    for (var o = e.hasClass(n.opts.objsClassName) ? e : e.find("." + n.opts.objsClassName), i = o.length, t = 0; t < i; t++) {
                        var a = o.eq(t);
                        if (a.attr("img-src")) {
                            var r = a.hasClass("J_loading_success"),
                                d = a.hasClass("J_loading");
                            r || d || (a.attr("need-remove", "no"), n.getLoadImage(a))
                        }
                    }
            }, 0)
        },
        getLoadImage: function(e) {
            var n = this;
            if (!e.hasClass("J_loading")) {
                var o = e.attr("img-src"),
                    t = {
                        type: i.loadType,
                        protocol: i.protocol,
                        domain: "",
                        boxId: e.attr("id") ? e.attr("id") : o,
                        loadNum: 0,
                        suffixUrl: o,
                        finalUrl: o,
                        imgUrl: o,
                        width: e.attr("suffix-width") ? e.attr("suffix-width") : e.width(),
                        ratio: e.attr("suffix-ratio"),
                        imgCode: e.attr("suffix-code"),
                        model: e.attr("suffix-model"),
                        useWebp: "no" != e.attr("use-webp"),
                        insert: e.attr("insert-model")
                    };
                (e.hasClass("full-width-wrap") || "no" == t.width) && (t.width = 9999), t.imgCode ? t.suffixUrl = i.getCodeSuffix(t.imgUrl, t.imgCode, t.useWebp) : !t.ratio || "1:1" != t.ratio && "7:9" != t.ratio && "3:4" != t.ratio && "2:3" != t.ratio ? "orig_narrow" == t.model ? t.suffixUrl = i.getHalfSuffix(t.imgUrl, t.useWebp) : t.suffixUrl = i.getWidthSuffix(t.imgUrl, t.width, t.useWebp) : t.suffixUrl = i.getGoodsRatioSuffix(t.imgUrl, t.width, t.ratio, t.useWebp), t.finalUrl = i.getCdnBanlanceUrl(t.suffixUrl), t.domain = n.getImageDomain(t.finalUrl), n.loadingImage(e, t)
            }
        },
        loadingImage: function(e, n) {
            var o = this;
            e.addClass("J_loading");
            var t = n.finalUrl;
            if (!(o.imgErrorClock[n.imgUrl] >= 4)) {
                var a = new Image;
                a.src = t, a.complete ? o.insertImg(a, e, n) : (a.onload = function() {
                    o.insertImg(a, e, n)
                }, a.onerror = function() {
                    o.imgErrorClock[n.imgUrl] ? o.imgErrorClock[n.imgUrl]++ : o.imgErrorClock[n.imgUrl] = 1, n.loadNum++, n.type == i.loadType && (o.pushErrorLog(n), o.addLogInfo(n, "err")), o.imgErrorClock[n.imgUrl] < 4 && n.loadNum < 4 ? (n.type = 3, n.suffixUrl != n.finalUrl && (n.domain = o.getImageDomain(n.suffixUrl), n.finalUrl = n.suffixUrl), o.loadingImage(e, n)) : o.pushErrorLog(n)
                })
            }
        },
        insertImg: function(e, n, o) {
            var i = this;
            i.addLogInfo(o, "succ"), n.hasClass("J_loading") && (n.removeClass("J_loading").addClass("J_loading_success"), "background" == o.insert ? (n[0].style.backgroundImage = "url(" + e.src + ")", n[0].style.backgroundRepeat = "no-repeat") : n.append('<img class="J_dynamic_img fill_img" src="' + e.src + '" alt=""/>'))
        },
        getImageDomain: function(e) {
            try {
                var n = /^([\w\d]*)\/\/([\w\d\-_]+(?:\.[\w\d\-_]+)*)/,
                    o = e.match(n);
                if (o && o.length > 2) return o[2]
            } catch (i) {}
            return ""
        },
        addLogInfo: function(e, n) {
            var o = this;
            o.logInfo.num++, o.logInfo[n]++, e.domain && (o.logInfo.domainInfo[e.domain] || (o.logInfo.domainInfo[e.domain] = {
                succ: 0,
                err: 0,
                num: 0
            }), o.logInfo.domainInfo[e.domain].num++, o.logInfo.domainInfo[e.domain][n]++), o.logInfo.num >= 30 && o.pubInfoLog()
        },
        pubInfoLog: function() {
            var e = this;
            if (clearTimeout(e.logTimer), e.logInfo.num > 0) {
                if (e.logInfo.type = i.loadType, _imgLog("\u89e6\u53d1\u5168\u5c40\u56fe\u7247\u52a0\u8f7d\u4fe1\u606f\u6253\u70b9\uff0c\u6253\u70b9\u683c\u5f0f\u5982\u4e0b"), _imgLog(e.logInfo), window.logger && logger.log) try {
                    logger.log("016010004", e.logInfo)
                } catch (n) {
                    _imgLog(n)
                }
                e.logInfo = {
                    type: i.loadType,
                    protocol: i.protocol,
                    num: 0,
                    succ: 0,
                    err: 0,
                    domainInfo: {}
                }
            }
            e.logTimer = setTimeout(e.pubInfoLog.bind(e), 3e3)
        },
        pushErrorLog: function(e) {
            if (window._trace && _trace.sendMsg) {
                var n = $.extend({}, e, {
                    url: e.finalUrl,
                    _author: "lanpang,yanchen,suling"
                });
                _trace.sendMsg(new Error(e.domain), n), _imgLog("\u89e6\u53d1\u56fe\u7247\u52a0\u8f7d\u9519\u8bef\u6253\u70b9\uff0c\u6253\u70b9\u683c\u5f0f\u5982\u4e0b"), _imgLog(n)
            }
        },
        destroy: function() {},
        defaults: {
            objsClassName: "J_dynamic_imagebox",
            showDistance: 0
        }
    }, M.DynamicImage = t;
    var a = M.dynamicImage;
    a || (a = new t({
        showDistance: $(window).height()
    }), M.dynamicImage = a), MoGu.dynamicImage = M.dynamicImage, e.exports = a
}, function(e, n) {
    window.MoGu = window.MoGu || {}, window.M = window.M || {}, window._imgLog = function(e) {
        var n = window.location.href,
            o = n.indexOf("isLog=true");
        o > -1 && window.console && console.log && console.log(e)
    };
    var o = navigator.userAgent;
    M.isUseWebp = !1;
    var i = {
        imgKeyArr: ["80", "100", "160", "180", "200", "240", "280", "300", "320", "360", "400", "440", "480", "520", "540", "560", "600", "640"],
        imgKeyMap: {
            80: {
                "1:1": "80x80",
                "7:9": "80x103",
                "3:4": "80x107",
                "2:3": "80x120",
                999: "80x999"
            },
            100: {
                "1:1": "100x100",
                "7:9": "100x129",
                "3:4": "100x134",
                "2:3": "100x150",
                999: "100x999"
            },
            160: {
                "1:1": "160x160",
                "7:9": "160x206",
                "3:4": "160x214",
                "2:3": "160x240",
                999: "160x999"
            },
            180: {
                "1:1": "180x180",
                "7:9": "180x232",
                "3:4": "180x240",
                "2:3": "180x270",
                999: "180x999"
            },
            200: {
                "1:1": "200x200",
                "7:9": "200x258",
                "3:4": "200x268",
                "2:3": "200x300",
                999: "200x999"
            },
            240: {
                "1:1": "240x240",
                "7:9": "240x308",
                "3:4": "240x320",
                "2:3": "240x360",
                999: "240x999"
            },
            280: {
                "1:1": "280x280",
                "7:9": "280x360",
                "3:4": "280x374",
                "2:3": "280x420",
                999: "280x999"
            },
            300: {
                "1:1": "300x300",
                "7:9": "300x386",
                "3:4": "300x400",
                "2:3": "300x450",
                999: "300x999"
            },
            320: {
                "1:1": "320x320",
                "7:9": "320x412",
                "3:4": "320x428",
                "2:3": "320x480",
                999: "320x999"
            },
            360: {
                "1:1": "360x360",
                "7:9": "360x463",
                "3:4": "360x480",
                "2:3": "360x540",
                999: "360x999"
            },
            400: {
                "1:1": "400x400",
                "7:9": "400x515",
                "3:4": "400x534",
                "2:3": "400x600",
                999: "400x999"
            },
            440: {
                "1:1": "440x440",
                "7:9": "440x566",
                "3:4": "440x587",
                "2:3": "440x660",
                999: "440x999"
            },
            480: {
                "1:1": "480x480",
                "7:9": "480x618",
                "3:4": "480x640",
                "2:3": "480x720",
                999: "480x999"
            },
            520: {
                "1:1": "520x520",
                "7:9": "520x670",
                "3:4": "520x694",
                "2:3": "520x780",
                999: "520x999"
            },
            540: {
                "1:1": "540x540",
                "7:9": "540x695",
                "3:4": "540x720",
                "2:3": "540x810",
                999: "540x999"
            },
            560: {
                "1:1": "560x560",
                "7:9": "560x720",
                "3:4": "560x747",
                "2:3": "560x840",
                999: "560x999"
            },
            600: {
                "1:1": "600x600",
                "7:9": "600x772",
                "3:4": "600x800",
                "2:3": "600x900",
                999: "600x999"
            },
            640: {
                "1:1": "640x640",
                "7:9": "640x824",
                "3:4": "640x854",
                "2:3": "640x960",
                999: "640x999"
            }
        },
        imgQuality: 70,
        dprDefMaxWidth: 640,
        dprDefRatio: "999",
        defCode: "999x999.v1c0",
        clientHeight: null,
        clientWidth: null,
        dpr: null,
        dprClentWidth: null,
        loadType: 1,
        protocol: "http",
        domainArr: [],
        domainHistoryCache: {},
        domainIndex: 0,
        domainLength: 0
    };
    i.ua = o, i.android = o.match(/(Android);?[\s\/]+([\d.]+)?/), i.ios = o.match(/(iPad).*OS\s([\d_]+)/) || o.match(/(iPod)(.*OS\s([\d_]+))?/) || o.match(/(iPhone\sOS)\s([\d_]+)/), i.wp = o.match(/Windows Phone ([\d.]+)/), i.is_mobile = i.android || i.ios || i.wp, i.is_ie_old = o.indexOf("MSIE") > 0, i.init = function() {
        var e = this;
        e.clientHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight, e.clientWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth, window.addEventListener && window.addEventListener("resize", function() {
            e.clientHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight, e.clientWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth
        }, !1), e.dpr = window.devicePixelRatio >= 1 ? window.devicePixelRatio : 1, e.dprClentWidth = e.clientWidth * e.dpr, window.location.href.split && (e.protocol = window.location.href.split("://")[0]), e.checkSupportWebp(), e.checkNeedCdnBanlance(), e.is_mobile && e.getAppInfo()
    }, i.setWebpFlag = function(e) {
        M.isUseWebp = !!e
    }, i.checkSupportWebp = function() {
        var e = this,
            n = new Image;
        n.onload = function() {
            e.setWebpFlag(!0)
        }, n.onerror = function() {
            e.ios && "undefined" != typeof localStorage ? e.setWebpFlag("true" === localStorage.getItem("isWebpEnable")) : e.setWebpFlag(!1)
        }, n.src = "data:image/webp;base64,UklGRkoAAABXRUJQVlA4WAoAAAAQAAAAAAAAAAAAQUxQSAsAAAABBxAREYiI/gcAAABWUDggGAAAADABAJ0BKgEAAQABABwlpAADcAD+/gbQAA=="
    }, i.checkNeedCdnBanlance = function() {
        var e = this;
        if (!e.domainLength) try {
            if (window.ImgCdnBanlance && ImgCdnBanlance instanceof Array && ImgCdnBanlance.length > 0) {
                for (var n = ImgCdnBanlance.length, o = 0; o < n; o++) {
                    var i = ImgCdnBanlance[o];
                    if (i.domain && i.domain.indexOf("mogucdn") > 0 && i.weight && parseInt(i.weight) > 0)
                        for (var t = parseInt(i.weight), a = 0; a < t; a++) e.domainArr.push(i.domain), e.domainLength++
                }
                e.domainLength && (e.loadType = 2)
            }
        } catch (r) {
            e.loadType = 1
        }
    }, i.getCdnDomain = function() {
        var e = this;
        e.domainIndex >= e.domainLength && (e.domainIndex = 0);
        var n = e.domainArr[e.domainIndex];
        return e.domainIndex++, n
    }, i.getCdnBanlanceUrl = function(e) {
        var n = this;
        if (2 != n.loadType || !e || "string" != typeof e) return e;
        if (n.domainHistoryCache[e]) return n.domainHistoryCache[e];
        var o = e.split("mogucdn.com/");
        if (2 != o.length) return e;
        var i = n.getCdnDomain();
        if (i) {
            o[0] = "//" + i;
            var t = o.join("/");
            return n.domainHistoryCache[e] = t, t
        }
        return e
    }, i.getDefSuffix = function(e, n) {
        var o = this,
            i = "";
        if (o.android || o.ios || o.wp) {
            var t = o.dprClentWidth;
            t <= 375 ? i = "375x9999.v1c7E" : 375 < t && t <= 750 ? i = "750x9999.v1c7E" : 750 < t && (i = "1125x9999.v1c7E")
        } else i = o.defCode;
        return o.getCodeSuffix(e, i, n)
    }, i.getWidthSuffix = function(e, n, o, i) {
        var t = this;
        "undefined" == typeof i && (i = !0);
        var a = t.defCode,
            r = i ? t.dpr : 1,
            d = parseInt(n) * r;
        return d && d > 0 && d < 1950 && (d += 50, a = 100 * Math.ceil(d / 100) + "x9999.v1c7E"), t.getCodeSuffix(e, a, o)
    }, i.getGoodsRatioSuffix = function(e, n, o, i, t) {
        var a = this;
        "undefined" == typeof t && (t = !0);
        var r = a.defCode,
            d = "",
            l = ".v1cAC",
            s = t ? a.dpr : 1;
        switch (o) {
            case "1:1":
            case "7:9":
            case "3:4":
            case "2:3":
                d = o;
                break;
            default:
                d = a.dprDefRatio, l = ".v1c96"
        }
        var g = parseInt(n) * s;
        (!g || g < 0 || g > a.dprDefMaxWidth) && (g = a.dprDefMaxWidth);
        for (var c = 0; c < a.imgKeyArr.length; c++) {
            var f = a.imgKeyArr[c];
            if (g <= f || f == a.dprDefMaxWidth) {
                r = a.imgKeyMap[f][d] + l;
                break
            }
        }
        return a.getCodeSuffix(e, r, i)
    }, i.getHalfSuffix = function(e, n) {
        var o = this,
            i = "";
        return o.dpr < 2 ? (i = "50000x50000.v1c7E", e = o.getCodeSuffix(e, i, n)) : e = o.getDefSuffix(e, n), e
    }, i.getCodeSuffix = function(e, n, o) {
        var i = this;
        if (!e || !n || "no" == n || e.indexOf(".webp") > 0 || e.indexOf(".gif") > 0) return e;
        if (e.indexOf("mogucdn") === -1) return e;
        if (e.indexOf(".jpg") < 0 && e.indexOf(".png") < 0) return e;
        if (e.indexOf(".jpg") > 0 && e.indexOf(".png") > 0) return e;
        e.indexOf("https:") >= 0 && (e = e.split("https:")[1]), e.indexOf("http:") >= 0 && (e = e.split("http:")[1]);
        var t = e,
            a = "",
            r = e.split(".");
        if ("jpg" == r[r.length - 1]) a = "jpg";
        else {
            if ("png" != r[r.length - 1]) return e;
            a = "png"
        }
        var n = "_" + n,
            d = "." + i.imgQuality + ".";
        if (e.indexOf(".png_") < 0 && e.indexOf(".jpg_") < 0 && e.indexOf("." + a) == e.length - 4 && (e = e + n + d + a), M.isUseWebp && o !== !1) {
            if (e.indexOf("." + a + "_") > 0) {
                var l = e.split(".");
                l[l.length - 1] == a && (l[l.length - 1] = "webp", e = l.join("."))
            }
        } else if ("png" == a) return t;
        return e
    }, i.getAppInfo = function() {
        var e = this;
        "undefined" != typeof hdp ? (hdp["do"]("mgj.device.getInfo").then(function(n) {
            n && n.networkType && 4 != n.networkType && 5 != n.networkType && (e.imgQuality = 50)
        })["catch"](function(e) {}), e.ios && "undefined" != typeof localStorage && hdp["do"]("hybrid.settings.getWebpEnabled").then(function(e) {
            localStorage.setItem("isWebpEnable", e)
        })["catch"](function() {
            localStorage.setItem("isWebpEnable", !1)
        })) : "undefined" != typeof document && document.addEventListener && document.addEventListener("deviceready", function() {
            window.mgj && mgj.device && mgj.device.getInfo && mgj.device.getInfo(function(n) {
                n && n.networkType && 4 != n.networkType && 5 != n.networkType && (e.imgQuality = 50)
            }), e.ios && "undefined" != typeof localStorage && window.hybrid && hybrid.settings && hybrid.settings.getWebpEnabled && hybrid.settings.getWebpEnabled(function(e) {
                localStorage.setItem("isWebpEnable", e)
            }, function() {
                localStorage.setItem("isWebpEnable", !1)
            })
        }, function() {})
    }, M.ImgUrlTool || (i.init(), M.ImgUrlTool = i), MoGu.ImgUrlTool = M.ImgUrlTool, e.exports = M.ImgUrlTool
}]);
! function() {
    "use strict";

    function e() {
        var e = "1";
        return T.isMobile && (e = "m1"), T.isIos && T.isNative ? e = "am0" : T.isAndroid && T.isNative && (e = "am1"), e
    }

    function t() {
        var e = k.getValue(j.ptp_cnt_b);
        if (e) return e;
        var t = "",
            n = location.href.split("?")[0];
        return t = q.pageHash(n)
    }

    function n() {
        var e = k.getCookieOrFunc(j.cpsinfo);
        return e ? e = e.replace("-", ",") : ""
    }

    function r(e) {
        if (e) {
            var t = k.getValue(j.urlExtendFn, e);
            return k.hasKey(t) ? t : void 0
        }
    }

    function i(e) {
        if (e) {
            e.length && (e = e[0]);
            var t = k.getValue(j.ptp_cnt_c_d, e);
            if (t) return t;
            var n = e.getAttribute("data-ptp-customc");
            if (n) return {
                c: n,
                d: U.getIndex("data-ptp-customc", n, e)
            };
            if (e = U.getParents(e, "data-ptp-customc")) return n = e.getAttribute("data-ptp-customc"), n ? {
                c: n,
                d: U.getIndex("data-ptp-customc", n, e)
            } : void 0
        }
    }

    function o() {
        return k.getCookieOrFunc(j.uuid)
    }

    function a() {
        window.PTP_PARAMS && k.extend(j, window.PTP_PARAMS);
        var e = navigator.userAgent.toLocaleLowerCase();
        return T.isNative = j.isNativeRe.test(e), {
            time: k.getTime(),
            ver: "1.1.4",
            uid: k.getCookieOrFunc(j.uid),
            _channel: "",
            "tid-token": "",
            launchTime: k.getTime(),
            active: 0,
            deviceName: "",
            os_ver: "",
            root: 0,
            network: 0,
            provider: "",
            url: location.href,
            refer: document.referrer,
            ptp_url: k.getQuery("ptp", location.search),
            ptp_ref: k.getQuery("ptp", document.referrer ? document.referrer : ""),
            eid: "0",
            ext: {
                cpsparam: k.getCookie("__cps"),
                cpsinfo: n(),
                _notNative: !T.isNative
            }
        }
    }

    function u() {
        H.a = e(), H.b = t(), H.c = 0, H.d = 0
    }

    function c(e, t) {
        t = t || {};
        var n = [];
        for (var r in t) {
            var i = t[r];
            i || (i = ""), i = encodeURIComponent(i), n.push(r + "=" + i)
        }
        n = n.join("&"), e = e.indexOf("?") > -1 ? e + "&" + n : e + "?" + n;
        var o = new Image;
        o.src = e
    }

    function d(e, t) {
        e += "?web=1", t = t || {};
        var n, r = z++;
        try {
            n = document.createElement('<iframe name="' + r + '">')
        } catch (i) {
            n = document.createElement("iframe"), n.setAttribute("name", r)
        }
        try {
            n.style.display = "none", document.body.appendChild(n), n.contentWindow.name = r;
            var o = document.createElement("form");
            o.setAttribute("method", "POST"), o.setAttribute("action", e), o.setAttribute("target", r);
            for (var a in t)
                if (t.hasOwnProperty(a)) {
                    var u = document.createElement("input");
                    u.setAttribute("type", "hidden"), u.setAttribute("name", a), u.setAttribute("value", t[a]), o.appendChild(u)
                }
            document.body.appendChild(o), o.submit(), k.registerEvent(n, "load", function() {
                try {
                    document.body.removeChild(o), document.body.removeChild(n)
                } catch (e) {}
            })
        } catch (i) {
            window.M && M.log(i)
        }
    }

    function f() {
        if (!K) {
            K = !0;
            for (var e = 0; e < J.length; e++) J[e].fn.call(window, J[e].ctx);
            J = []
        }
    }

    function s() {
        "complete" === document.readyState && f()
    }

    function p(e, t) {
        return K ? void setTimeout(function() {
            e(t)
        }, 1) : (J.push({
            fn: e,
            ctx: t
        }), void("complete" === document.readyState || !document.attachEvent && "interactive" === document.readyState ? setTimeout(f, 1) : W || (document.addEventListener ? (document.addEventListener("DOMContentLoaded", f, !1), window.addEventListener("load", f, !1)) : (document.attachEvent("onreadystatechange", s), window.attachEvent("onload", f)), W = !0)))
    }

    function l() {
        return X
    }

    function g(e, t, n) {
        "undefined" != typeof e && (t = t || {}, n && window.M && M.web.AB && (t.abinfo = M.web.AB.formatAB(n)), p(function() {
            var n = V.getPtpInfoAndExtra(t);
            n.eid = e + "", l() ? D.logData("e", k.extend({}, n)) : k.listenTo("LoggerReady", function() {
                var e = V.getPtpInfoAndExtra(t);
                D.logData("e", k.extend({}, e))
            }), window.MtaH5 && MtaH5.clickStat && MtaH5.clickStat(e, t)
        }))
    }

    function v() {
        var e = V.getPtpInfoAndExtra(),
            t = k.getValue(j.pEventId);
        e.eid = t, D.logData("p", e)
    }

    function m() {
        if (T.isNative) {
            var e = V.getPtpCnt();
            window.M && M.web.AB && M.web.AB.isAB ? M.web.AB.collectExps().then(function(t) {
                t.length ? D.logAppPevent(e, t) : D.logAppPevent(e)
            }) : D.logAppPevent(e)
        } else l() ? v() : k.listenTo("LoggerReady", function() {
            v()
        })
    }

    function h() {
        p(function() {
            V.refreshPtp(), V.refreshE(), m()
        })
    }

    function w(e) {
        var t = e.href;
        if (!(t.indexOf("mogujie.com/mtalk/") > -1) && (j.hrefRe.test(t) || j.mgjRe.test(t))) {
            var n = e.getAttribute("data-ptp-cache-id");
            t = e.getAttribute("href"), n && j.ptpRe.test(n) || (n = V.createPtpCnt(e), e.setAttribute("data-ptp-cache-id", n)), e.href = V.makeUrl(t, n, e)
        }
    }

    function y(e) {
        if (e.getAttribute) {
            var t = e.getAttribute("href");
            if (null === t) return !1;
            if (0 === t.indexOf("#") && "_blank" !== e.getAttribute("target")) return !1
        }
        return !0
    }

    function x(e) {
        var t = e || window.event,
            n = t.target || t.srcElement,
            r = U.getA(n),
            i = "AREA" === n.nodeName ? n : null;
        i && (r = i), r && (r.href && r.href.indexOf("javascript:") > -1 || y(r) && w(r))
    }

    function A(e, t) {
        if ("undefined" == typeof e) return "";
        var n = "";
        return n = t ? V.createPtpCnt(t) : V.getPtpCnt(), V.makeUrl(e, n, t)
    }

    function E() {
        var e = A("");
        e = e.split("?")[1], e = e.split("&");
        for (var t, n = "", r = 0, i = e.length; r < i; r++) t = e[r].split("="), n += '<input type="hidden" name="' + t[0] + '" value="' + (t[1] ? t[1] : "") + '"/>';
        return n
    }

    function P(e) {
        e && "string" == typeof e && (e = A(e), window.location.href = e)
    }
    var _ = 1001,
        b = {},
        C = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#x27;",
            "`": "&#x60;"
        },
        L = /(&|<|>|"|`|')/g,
        k = {
            escapeHtml: function(e) {
                return e.replace(L, function(e) {
                    return C[e]
                })
            },
            isIE: function(e) {
                var t = document.createElement("b");
                return t.innerHTML = "<!--[if IE " + e + "]><i></i><![endif]-->", 1 === t.getElementsByTagName("i").length
            },
            stringify: function(e) {
                var t = this;
                if ("undefined" != typeof JSON) return JSON.stringify(e);
                var n = typeof e;
                if ("object" != n || null === e) return "string" == n && (e = '"' + e + '"'), String(e);
                var r, i, o = [],
                    a = e && e.constructor == Array;
                for (r in e) i = e[r], n = typeof i, e.hasOwnProperty(r) && ("string" == n ? i = '"' + i + '"' : "object" == n && null !== i && (i = t.stringify(i)), o.push((a ? "" : '"' + r + '":') + String(i)));
                return (a ? "[" : "{") + String(o) + (a ? "]" : "}")
            },
            isArray: function(e) {
                return "[object Array]" == Object.prototype.toString.call(e)
            },
            getCookieInArray: function(e) {
                for (var t = this, n = 0, r = e.length; n < r; n++) {
                    var i = t.getCookie(e[n]);
                    if (i) return i
                }
                return ""
            },
            getCookieOrFunc: function(e) {
                return "function" == typeof e ? this.getValue(e) : this.getCookie(e)
            },
            getCookie: function(e) {
                if (this.isArray(e)) return this.getCookieInArray(e);
                var t = document.cookie.match(new RegExp("(^| )" + e + "=([^;]*)(;|$)"));
                return null !== t ? decodeURIComponent(t[2]) : ""
            },
            getQuery: function(e, t) {
                "undefined" == typeof t && (t = location.search);
                var n = "(^|&|\\?)" + e + "=([^&]*)(&|$)",
                    r = new RegExp(n, "i"),
                    i = t.substr(1).match(r);
                return null !== i ? this.escapeHtml(decodeURIComponent(i[2])) : ""
            },
            setQuery: function(e, t, n) {
                var r = new RegExp("([?&])" + t + "=.*?(&|$)", "i"),
                    i = e.indexOf("?") !== -1 ? "&" : "?";
                return e.match(r) ? e.replace(r, "$1" + t + "=" + n + "$2") : e + i + t + "=" + n
            },
            getTime: function() {
                return (new Date).getTime()
            },
            registerEvent: function(e, t, n) {
                window.attachEvent ? e.attachEvent("on" + t, n) : e.addEventListener(t, n, !1)
            },
            extend: function() {
                for (var e = arguments, t = arguments[0], n = 1; n < e.length; n++) {
                    var r = e[n];
                    for (var i in r) r.hasOwnProperty(i) && (t[i] = r[i])
                }
                return t
            },
            getValue: function(e) {
                if (e) {
                    if ("function" == typeof e) try {
                        var t = Array.prototype.slice.call(arguments, 1);
                        return e.apply(null, t)
                    } catch (n) {
                        return window.M && window.M.log("**logger.js---\u6253\u70b9\u51fa\u9519:" + n), ""
                    }
                    return e
                }
            },
            loadScript: function(e, t, n) {
                if (window["callback_" + _] = function(e) {
                        t && t(e)
                    }, e = this.setQuery(e, "callback", "callback_" + _), _ += 1, n) window.loader.script(e, function() {}, function() {});
                else {
                    var r = document.createElement("script");
                    r.src = e;
                    var i = document.getElementsByTagName("head")[0];
                    i && i.appendChild(r)
                }
            },
            listenTo: function(e, t) {
                b[e] || (b[e] = []), b[e].push(t)
            },
            fire: function(e) {
                var t = b[e];
                if (t && t.length) {
                    for (var n = 0, r = t.length; n < r; n++) t[n].call();
                    b[e] = []
                }
            },
            hasKey: function(e) {
                if (!e) return !1;
                for (var t in e)
                    if (e.hasOwnProperty(t)) return !0;
                return !1
            }
        },
        I = "https:" === location.protocol ? "https:" : "http:",
        N = "mogujie";
    location.host.indexOf("meilishuo") != -1 && (N = "meilishuo");
    var j = {
            LogUrl: I + "//log.mogujie.com/log",
            CookieUrl: I + "//portal." + N + ".com/api/util/getUuid",
            shouldRequestCookie: function() {
                var e = k.getCookieOrFunc(this.uuid);
                return !e
            },
            uuid: ["__mgjuuid", "__xduuid"],
            uid: "__ud_",
            cpsinfo: "__cpsinfo",
            ptp_cnt_a: "",
            ptp_cnt_b: "",
            ptp_cnt_c_d: "",
            platform: function() {
                var e = navigator.userAgent.toLowerCase();
                if (/qq\/([\d\.]+)/.test(e) || /qzone\//.test(e)) return 48
            },
            pEventId: "0",
            isMobileRe: /iphone|android|ipad/i,
            ptpRe: /[a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+/i,
            hrefRe: /http[s]?:\/\/(\w+\.){1,2}(mogujie|meilishuo|xiaodian|uniny)\.com([\/]|\/.*|)$/,
            mgjRe: /(mgj|mls):\/\//,
            mtRe: /\?.*[&]?mt=([^\.]+)\.([^\.]+)\.([^\.&#]+)/,
            chasing: ["f", "f2", "mlf", "s", "_fu", "_wvx"],
            urlExtend: ["acm", "cparam"],
            urlExtendFn: function() {},
            extra: {},
            isNativeRe: /(mogujie|meilishuo|mls|mgjtuangou|xiaodian|xcore)/i,
            nativeLog: {}
        },
        O = navigator.userAgent.toLocaleLowerCase(),
        R = !1,
        S = O.indexOf("xcore") > -1;
    S && window.loader && window.loader.script && (R = !0);
    var T = {
            isWX: O.indexOf("micromessenger") > -1,
            isApp: j.isNativeRe.test(O),
            isNative: j.isNativeRe.test(O),
            isMobile: j.isMobileRe.test(O),
            isIos: O.indexOf("iphone") > -1,
            isAndroid: O.indexOf("android") > -1,
            isLowIE: !R && (k.isIE(6) || k.isIE(7) || k.isIE(8)),
            xcore: R
        },
        B = window.jQuery || window.Zepto,
        Q = function(e, t) {
            for (var n = 0, r = e.length; n < r; n++)
                if (e[n] == t) return n + 1;
            return -1
        },
        U = {
            getA: function(e) {
                var t = e;
                if ("A" == t.tagName) return e;
                for (; t.parentNode;)
                    if (t = t.parentNode, "A" == t.tagName) return t
            },
            getParentByClass: function(e, t) {
                if (e) {
                    if (B) return $(e).parents("." + t);
                    for (var n, r = e; r.parentNode;)
                        if (r = r.parentNode, n = r.className && r.className.indexOf(t) != -1) return r
                }
            },
            getParents: function(e, t) {
                if (e) {
                    if (t = t || "", B) return t = "[" + t + "]", $(e).parents(t)[0];
                    for (var n, r = e; r.parentNode;)
                        if (r = r.parentNode, n = r.getAttribute && r.getAttribute(t)) return r
                }
            },
            getIndex: function(e, t, n) {
                if (!e || !t || !n) return 0;
                if (B) return $("[" + e + '="' + t + '"]').index($(n)) + 1;
                if (document.querySelectorAll) {
                    var r = document.querySelectorAll("[" + e + '="' + t + '"]');
                    return Q(r, n)
                }
                return 1
            },
            getElemIndex: function(e, t, n) {
                if (!e || !t || !n) return 0;
                if (B) return $(e).find(t).index($(n)) + 1;
                if (e.querySelectorAll) {
                    var r = e.querySelectorAll(t);
                    return Q(r, n)
                }
                return 1
            },
            is: function(e, t) {
                return !(!e || !t) && (e.length && (e = e[0]), e.nodeName.toLowerCase() === t.toLowerCase() || void 0)
            }
        },
        q = {
            arr: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            rand: function(e) {
                var t, n, r = this,
                    i = "",
                    o = 0;
                for (t = 0; t < e; t++) n = parseInt(Math.random() * r.arr.length, 10), i += r.arr.charAt(n), o += r.arr.charCodeAt(n);
                return i += this.arr.charAt(o % this.arr.length)
            },
            pageHash: function(e) {
                var t = this,
                    n = 5381,
                    r = e.length - 1;
                if ("string" == typeof e)
                    for (; r > -1; r--) n += (n << 5) + e.charCodeAt(r);
                else
                    for (; r > -1; r--) n += (n << 5) + e[r];
                var i = 2147483647 & n,
                    o = "";
                do o += t.arr.charAt(61 & i), i >>= 6; while (i);
                return o
            }
        },
        F = a(),
        H = {
            a: e(),
            b: t(),
            c: 0,
            d: 0,
            e: j.ptp_cnt_e ? j.ptp_cnt_e : q.rand(6)
        },
        V = {
            getPlatform: function() {
                var e = k.getValue(j.platform);
                return e ? e : T.isMobile ? 32 : 31
            },
            getPtpByType: function(e) {
                var t = [0, o(), e];
                return t
            },
            getPtpCnt: function(e, t) {
                return e || (e = H.c), t || (t = H.d), [H.a, H.b, e, t, H.e].join(".")
            },
            getPtpInfo: function(e, t) {
                var n = {};
                return k.extend(n, F, {
                    ptp_cnt: this.getPtpCnt(e, t)
                })
            },
            getPtpInfoAndExtra: function(e) {
                e = e || {};
                var t = this.getPtpInfo(e.ptp_c, e.ptp_d),
                    n = {};
                if (j.extra)
                    for (var r in j.extra) j.extra.hasOwnProperty(r) && (n[r] = k.getValue(j.extra[r]));
                var i = k.extend({}, t.ext, n, e);
                return k.extend({}, t, {
                    ext: i
                })
            },
            createPtpCnt: function(e) {
                var t = i(e),
                    n = 0,
                    r = 0;
                if (t) return this.getPtpCnt(t.c, t.d);
                var o = U.getParents(e, "data-ptp"),
                    a = U.getParentByClass(e, "data-ptp-item");
                return o && (n = o.getAttribute("data-ptp"), r = a ? U.getElemIndex(o, ".data-ptp-item", a) : U.getElemIndex(o, "a", e)), r || (r = 0), this.getPtpCnt(n, r)
            },
            makeUrl: function(e, t, n) {
                var r = e.match(/(#.+)$/);
                return e = e.replace(/(#.+)$/, ""), e = k.setQuery(e, "ptp", t), e = this.getChasingParams(e), e = this.getExtendParams(n, e), r && (e += r[1]), e
            },
            getChasingParams: function(e) {
                "undefined" == typeof e && (e = "");
                var t = e;
                if (!j.chasing) return t;
                j.chasing.length || (j.chasing = [j.chasing]);
                for (var n, r, i = 0, o = j.chasing.length; i < o; i++) n = j.chasing[i], r = k.getQuery(n), r && (t = k.setQuery(t, n, r));
                for (var a = location.search, u = /[\?&](_f_[^=]+)=([^&]+)/g, c = u.exec(a); c && 3 == c.length;) t = k.setQuery(t, c[1], c[2]), c = u.exec(a);
                return t
            },
            getExtendParams: function(e, t) {
                var n = t;
                if (!e || !U.is(e, "a")) return n;
                var i = r(e);
                if (i)
                    for (var o in i) i.hasOwnProperty(o) && (n = k.setQuery(n, o, i[o]));
                else {
                    e.length && (e = e[0]);
                    for (var a = j.urlExtend || [], u = 0, c = a.length; u < c; u++) {
                        var d = a[u],
                            f = e.getAttribute("data-ext-" + d);
                        f && (n = k.setQuery(n, d, f))
                    }
                }
                return n
            },
            refreshPtp: function() {
                F = a(), u()
            },
            refreshE: function() {
                H && (H.e = q.rand(6))
            }
        },
        z = 0,
        D = {
            sendLog: function(e, t) {
                T.isLowIE ? d(e, t) : c(e, t)
            },
            sendAppLog: function(e, t) {
                return e += "", j.nativeLog && j.nativeLog.logE ? j.nativeLog.logE(e, t) : void(window.hdp && window.hdp.exec ? hdp.exec("mgj.tracker.sendEvent", e, t) : document.addEventListener("deviceready", function() {
                    window.mgj && mgj.tracker && mgj.tracker.sendEvent && mgj.tracker.sendEvent(e, t)
                }, !1))
            },
            logAppPevent: function(e, t) {
                return j.nativeLog && j.nativeLog.logP ? j.nativeLog.logP(e, t) : void(window.hdp && window.hdp.exec ? hdp.exec("mgj.pevent", e, t).then(function() {}, function() {}) : document.addEventListener("deviceready", function() {
                    window.mgj && mgj.pevent && mgj.pevent(function() {}, null, e)
                }, !1))
            },
            logData: function(e, t) {
                var n = V.getPtpByType(e),
                    r = t.eid;
                if (n.push(k.stringify(t)), T.isNative) {
                    var i = t.ext;
                    i.ptp_cnt = t.ptp_cnt, i.ptp_url = t.ptp_url, i.ptp_ref = t.ptp_ref, i.uid = t.uid, i._11_url = location.href, i._11_refer = document.referrer || "", D.sendAppLog(r, i)
                } else D.sendLog(j.LogUrl, {
                    v: 2,
                    pt: k.getTime(),
                    pf: V.getPlatform(),
                    data: n.join("\t")
                })
            }
        },
        J = [],
        K = !1,
        W = !1,
        X = T.isNative || !j.shouldRequestCookie();
    X || k.loadScript(j.CookieUrl, function() {
        X = !0, k.fire("LoggerReady")
    }, T.xcore), "undefined" == typeof location.search && (location.search = location.href.split("#")[0]);
    var Z = {
        version: "1.1.4",
        ptp: V,
        config: j,
        util: k,
        info: T,
        send: D,
        refreshPevent: h,
        log: g,
        generatePtpParams: A,
        generatePtpForm: E,
        goTo: P
    };
    if (window.logger = Z, !T.xcore) {
        var G = "tap" in document.createElement("div") ? "tap" : "mousedown";
        k.registerEvent(document, G, x), k.registerEvent(document, "touchstart", x)
    }
    return p(function() {
        V.refreshPtp(), m()
    }), Z
}();
"undefined" == typeof console && (console = {
    log: function() {}
}), window.detePtp = {
    triggerLog: function() {
        console.log("**************************:detePtp.triggerLog已经不再支持了，请尽快换用新版打点接口")
    },
    logFromtSend: function() {
        console.log("**************************:detePtp.logFromtSend已经不再支持了，请尽快换用新版打点接口")
    }
};
var trace = function() {
    "use strict";

    function extend() {
        var arguments$1 = arguments;
        var target = arguments[0];
        var argsLen = arguments.length;
        for (var i = 1; i < argsLen; i++) {
            var source = arguments$1[i];
            for (var p in source) {
                if (source.hasOwnProperty(p)) {
                    target[p] = source[p]
                }
            }
        }
        return target
    }

    function getValue(fn) {
        if (typeof fn !== "function") {
            return fn
        }
        return fn()
    }
    var config = {
        customUrl: function customUrl() {},
        getExtraTime: function getExtraTime() {
            return 0
        },
        blankTime: "__trace__headendt"
    };

    function getFormatUrl(url) {
        url = url || location.href;
        var customUrl = getValue(config.customUrl);
        if (customUrl) {
            customUrl = customUrl.split("https://").join("").split("http://").join("");
            return customUrl
        }
        if (typeof url === "string") {
            url = url.split("?")[0].split("#")[0].split("https://").join("").split("http://").join("");
            if (url.charAt(url.length - 1) === "/") {
                url = url.substr(0, url.length - 1)
            }
        }
        return url
    }
    var CHROME_IE_STACK_REGEXP = /^\s*at .*(\S+\:\d+|\(native\))/m;
    var SAFARI_NATIVE_CODE_REGEXP = /^(eval@)?(\[native code\])?$/;

    function _map(array, fn, thisArg) {
        if (typeof Array.prototype.map === "function") {
            return array.map(fn, thisArg)
        } else {
            var output = new Array(array.length);
            for (var i = 0; i < array.length; i++) {
                output[i] = fn.call(thisArg, array[i])
            }
            return output
        }
    }

    function _filter(array, fn, thisArg) {
        if (typeof Array.prototype.filter === "function") {
            return array.filter(fn, thisArg)
        } else {
            var output = [];
            for (var i = 0; i < array.length; i++) {
                if (fn.call(thisArg, array[i])) {
                    output.push(array[i])
                }
            }
            return output
        }
    }

    function _indexOf(array, target) {
        if (typeof Array.prototype.indexOf === "function") {
            return array.indexOf(target)
        } else {
            for (var i = 0; i < array.length; i++) {
                if (array[i] === target) {
                    return i
                }
            }
            return -1
        }
    }
    var ErrorStackParser = {
        parse: function ErrorStackParser$$parse(error) {
            if (error.stack && error.stack.match(CHROME_IE_STACK_REGEXP)) {
                return this.parseV8OrIE(error)
            } else if (error.stack) {
                return this.parseFFOrSafari(error)
            } else {
                return []
            }
        },
        extractLocation: function ErrorStackParser$$extractLocation(urlLike) {
            if (urlLike.indexOf(":") === -1) {
                return [urlLike]
            }
            var regExp = /(.+?)(?:\:(\d+))?(?:\:(\d+))?$/;
            var parts = regExp.exec(urlLike.replace(/[\(\)]/g, ""));
            return [parts[1], parts[2] || undefined, parts[3] || undefined]
        },
        parseV8OrIE: function ErrorStackParser$$parseV8OrIE(error) {
            var filtered = _filter(error.stack.split("\n"), function(line) {
                return !!line.match(CHROME_IE_STACK_REGEXP)
            }, this);
            return _map(filtered, function(line) {
                if (line.indexOf("(eval ") > -1) {
                    line = line.replace(/eval code/g, "eval").replace(/(\(eval at [^\()]*)|(\)\,.*$)/g, "")
                }
                var tokens = line.replace(/^\s+/, "").replace(/\(eval code/g, "(").split(/\s+/).slice(1);
                var locationParts = this.extractLocation(tokens.pop());
                var functionName = tokens.join(" ") || undefined;
                var fileName = _indexOf(["eval", "<anonymous>"], locationParts[0]) > -1 ? undefined : locationParts[0];
                return {
                    functionName: functionName,
                    filename: fileName,
                    row: locationParts[1],
                    column: locationParts[2],
                    line: line
                }
            }, this)
        },
        parseFFOrSafari: function ErrorStackParser$$parseFFOrSafari(error) {
            var filtered = _filter(error.stack.split("\n"), function(line) {
                return !line.match(SAFARI_NATIVE_CODE_REGEXP)
            }, this);
            return _map(filtered, function(line) {
                if (line.indexOf(" > eval") > -1) {
                    line = line.replace(/ line (\d+)(?: > eval line \d+)* > eval\:\d+\:\d+/g, ":$1")
                }
                if (line.indexOf("@") === -1 && line.indexOf(":") === -1) {
                    return {
                        functionName: line
                    }
                } else {
                    var tokens = line.split("@");
                    var locationParts = this.extractLocation(tokens.pop());
                    var functionName = tokens.join("@") || undefined;
                    return {
                        functionName: functionName,
                        filename: locationParts[0],
                        row: locationParts[1],
                        column: locationParts[2],
                        line: line
                    }
                }
            }, this)
        }
    };
    var parser = {
        ErrorStackParser: ErrorStackParser,
        parse: function parse(error) {
            var r = ErrorStackParser.parse(error);
            if (!r || r.length <= 0) {
                return error.message
            }
            var info = r[0];
            var strs = [];
            if (info.filename) {
                var filename = info.filename;
                if (filename.lastIndexOf("/") > -1) {
                    filename = info.filename.slice(info.filename.lastIndexOf("/"))
                }
                strs.push(filename)
            }
            if (info.functionName) {
                strs.push("@" + info.functionName)
            }
            if (info.row) {
                strs.push(" " + info.row)
            }
            return error.message + " - " + strs.join("")
        },
        normalize: function normalize(error) {
            var r = ErrorStackParser.parse(error);
            return r
        }
    };

    function getPlatform() {
        var ua = navigator.userAgent.toLowerCase();
        return /iphone|android|ipad/i.test(ua) ? "h5" : "pc"
    }

    function getBrowser() {
        var nAgt = navigator.userAgent;
        var unknown = "其它";
        var browser = unknown;
        var version = "";
        var majorVersion = "";
        var verOffset;
        var ix;
        if ((verOffset = nAgt.indexOf("Opera")) !== -1) {
            browser = "Opera";
            version = nAgt.substring(verOffset + 6);
            if ((verOffset = nAgt.indexOf("Version")) !== -1) {
                version = nAgt.substring(verOffset + 8)
            }
        }
        if ((verOffset = nAgt.indexOf("OPR")) !== -1) {
            browser = "Opera";
            version = nAgt.substring(verOffset + 4)
        } else if (nAgt.indexOf("MicroMessenger") !== -1) {
            browser = "Wechat"
        } else if (nAgt.indexOf("QQ") !== -1) {
            browser = "QQ"
        } else if ((verOffset = nAgt.indexOf("MSIE")) !== -1) {
            browser = "IE";
            version = nAgt.substring(verOffset + 5)
        } else if ((verOffset = nAgt.indexOf("Chrome")) !== -1) {
            browser = "Chrome";
            version = nAgt.substring(verOffset + 7)
        } else if ((verOffset = nAgt.indexOf("Firefox")) !== -1) {
            browser = "Firefox";
            version = nAgt.substring(verOffset + 8)
        } else if (nAgt.indexOf("Trident/") !== -1) {
            browser = "IE";
            version = nAgt.substring(nAgt.indexOf("rv:") + 3)
        } else if ((verOffset = nAgt.indexOf("Safari")) !== -1 || nAgt.indexOf("iPhone") !== -1) {
            browser = "Safari";
            version = nAgt.substring(verOffset + 7);
            if ((verOffset = nAgt.indexOf("Version")) !== -1) {
                version = nAgt.substring(verOffset + 8)
            }
        }
        if ((ix = version.indexOf(";")) !== -1) {
            version = version.substring(0, ix)
        }
        if ((ix = version.indexOf(" ")) !== -1) {
            version = version.substring(0, ix)
        }
        if ((ix = version.indexOf(")")) !== -1) {
            version = version.substring(0, ix)
        }
        if (version) {
            majorVersion = parseInt("" + version, 10);
            if (isNaN(majorVersion)) {
                version = "" + parseFloat(navigator.appVersion);
                majorVersion = parseInt(navigator.appVersion, 10)
            }
        }
        return majorVersion ? browser + "_" + majorVersion : browser + "_unknown"
    }

    function getOs() {
        var unknown = "其它";
        var os = unknown;
        var nAgt = navigator.userAgent;
        var clientStrings = [{
            s: "Windows 10",
            r: /(Windows 10.0|Windows NT 10.0)/
        }, {
            s: "Windows 8.1",
            r: /(Windows 8.1|Windows NT 6.3)/
        }, {
            s: "Windows 8",
            r: /(Windows 8|Windows NT 6.2)/
        }, {
            s: "Windows 7",
            r: /(Windows 7|Windows NT 6.1)/
        }, {
            s: "Windows Vista",
            r: /Windows NT 6.0/
        }, {
            s: "Windows Server 2003",
            r: /Windows NT 5.2/
        }, {
            s: "Windows XP",
            r: /(Windows NT 5.1|Windows XP)/
        }, {
            s: "Windows 2000",
            r: /(Windows NT 5.0|Windows 2000)/
        }, {
            s: "Windows ME",
            r: /(Win 9x 4.90|Windows ME)/
        }, {
            s: "Windows 98",
            r: /(Windows 98|Win98)/
        }, {
            s: "Windows 95",
            r: /(Windows 95|Win95|Windows_95)/
        }, {
            s: "Windows NT 4.0",
            r: /(Windows NT 4.0|WinNT4.0|WinNT|Windows NT)/
        }, {
            s: "Windows CE",
            r: /Windows CE/
        }, {
            s: "Windows 3.11",
            r: /Win16/
        }, {
            s: "Android",
            r: /Android/
        }, {
            s: "Open BSD",
            r: /OpenBSD/
        }, {
            s: "Sun OS",
            r: /SunOS/
        }, {
            s: "Linux",
            r: /(Linux|X11)/
        }, {
            s: "iOS",
            r: /(iPhone|iPad|iPod)/
        }, {
            s: "Mac OS X",
            r: /Mac OS X/
        }, {
            s: "Mac OS",
            r: /(MacPPC|MacIntel|Mac_PowerPC|Macintosh)/
        }, {
            s: "QNX",
            r: /QNX/
        }, {
            s: "UNIX",
            r: /UNIX/
        }, {
            s: "BeOS",
            r: /BeOS/
        }, {
            s: "OS/2",
            r: /OS\/2/
        }, {
            s: "Search Bot",
            r: /(nuhk|Googlebot|Yammybot|Openbot|Slurp|MSNBot|Ask Jeeves\/Teoma|ia_archiver)/
        }];
        for (var id in clientStrings) {
            var cs = clientStrings[id];
            if (cs.r.test(nAgt)) {
                os = cs.s;
                break
            }
        }
        var osVersion = unknown;
        if (/Windows/.test(os)) {
            osVersion = /Windows (.*)/.exec(os)[1];
            os = "Windows"
        }
        switch (os) {
            case "Mac OS X":
                osVersion = "";
                break;
            case "Android":
                var matched = /Android( |\/)([\.\_\d]+)/.exec(nAgt);
                if (matched && matched.length > 0) {
                    var arr = (matched[2] || "").split(".").slice(0, 2);
                    osVersion = arr.join(".")
                }
                break;
            case "iOS":
                osVersion = /OS (\d+)_(\d+)_?(\d+)?/.exec(nAgt);
                if (osVersion && osVersion.length > 0) {
                    osVersion = osVersion[1] + "." + osVersion[2]
                }
                break
        }
        return os === unknown ? os : os + osVersion
    }

    function getScreen() {
        var _screen = window.screen;
        var width;
        var height;
        var screenSize = "";
        if (_screen && _screen.width) {
            width = _screen.width ? _screen.width : "";
            height = _screen.height ? _screen.height : "";
            screenSize += "" + width + "x" + height
        }
        return screenSize
    }

    function getDevicePixelRatio() {
        var dpr = (window.devicePixelRatio ? window.devicePixelRatio : 1) - 0;
        return dpr.toFixed(1)
    }

    function getDeviceInfo() {
        return {
            platform: getPlatform(),
            screen: getScreen(),
            os: getOs(),
            browser: getBrowser(),
            devicePixelRatio: getDevicePixelRatio()
        }
    }
    var Promise = window.Promise;

    function getPerformanceInfo() {
        var timing = window.performance && window.performance.timing;
        if (!timing) {
            return Promise.resolve({})
        }
        var blankTime = window[config.blankTime];
        if (!blankTime) {
            blankTime = timing.domContentLoadedEventStart
        }
        var res = {
            dns: timing.domainLookupEnd - timing.domainLookupStart,
            tcp: timing.connectEnd - timing.connectStart,
            request: timing.responseStart - timing.requestStart,
            response: timing.responseEnd - timing.responseStart,
            domContentLoad: timing.domContentLoadedEventEnd - timing.navigationStart,
            blankTime: blankTime - timing.navigationStart,
            readyTime: timing.domInteractive - timing.navigationStart,
            onloadTime: timing.loadEventEnd - timing.navigationStart,
            extraTime: getValue(config.getExtraTime) || 0
        };
        return Promise.resolve(res)
    }

    function _log() {
        var logger = window.logger;
        if (!logger) {
            return
        }
        var info = getDeviceInfo();
        getPerformanceInfo().then(function(performance) {
            logger.log && logger.log("016000001", extend({
                formatUrl: getFormatUrl()
            }, info, performance))
        })
    }
    var queue = [];

    function isNewError(msg, file, line, col) {
        var flag = true;
        for (var i = 0; i < queue.length; i++) {
            var item = queue[i] || {};
            if (item.msg === msg && item.file === file && item.line === line && item.col === col) {
                flag = false;
                break
            }
        }
        if (flag) {
            queue.push({
                msg: msg,
                file: file,
                line: line,
                col: col
            })
        }
        return flag
    }

    function onErrorHandler(msg, file, line, col, err) {
        if (!isNewError(msg, file, line, col)) {
            return
        }
        var stack = "";
        if (err) {
            if (err.hasReported) {
                return
            }
            stack = err.stack || ""
        }
        queue.push({
            msg: msg,
            file: file,
            line: line,
            col: col
        });
        var logger = window.logger;
        if (!logger || !logger.log) {
            return
        }
        if (typeof stack !== "string") {
            stack = "" + stack
        }
        var data = {
            type: 0,
            msg: msg,
            stack: stack,
            ua: navigator.userAgent,
            formatUrl: getFormatUrl()
        };
        try {
            JSON.stringify(data);
            logger.log("016000011", data)
        } catch (_) {}
    }
    var regParsePattern = /^\s*('?undefined'?|object|null) is not (a function|an object)\s*$/i;

    function shouldParse(msg) {
        if (!msg) {
            return false
        }
        if (regParsePattern.test(msg)) {
            return true
        }
        if (msg.toLowerCase() === "cannot convert undefined or null to object") {
            return true
        }
        return false
    }

    function getErrorInfo(error, useParser) {
        if (!error) {
            return null
        }
        var data = {};
        if (typeof error === "object") {
            data.msg = error.message || "";
            data.stack = error.stack || "";
            data.stack = data.stack;
            if (typeof data.stack !== "string") {
                data.stack = "" + data.stack
            }
        } else {
            data.msg = error
        }
        data.ua = navigator.userAgent;
        data.type = 1;
        if (shouldParse(data.msg) && typeof error === "object" && error.stack) {
            try {
                data.msg = parser.parse(error)
            } catch (err) {}
        }
        if (!isNewError(data.msg, data.stack)) {
            return null
        }
        return data
    }
    var Logger = {
        init: function init() {
            var interval = setInterval(function() {
                var timing = window.performance && window.performance.timing;
                if (timing && timing.loadEventEnd === 0) {
                    return
                }
                clearInterval(interval);
                setTimeout(function() {
                    _log()
                }, 10)
            }, 300);
            window.onerror = onErrorHandler
        },
        sendMsg: function sendMsg(error, extra, useParser) {
            if (extra === void 0) extra = null;
            if (useParser === void 0) useParser = false;
            var data = getErrorInfo(error, useParser);
            var logger = window.logger;
            if (!data || !logger || !logger.log) {
                return
            }
            var extraJSON = "";
            if (extra) {
                try {
                    extraJSON = JSON.stringify(extra);
                    if (extraJSON.length > 1024) {
                        throw new Error("extra contains too much information")
                    }
                } catch (e) {
                    extraJSON = "";
                    console && console.warn && console.warn(e)
                }
            }
            extend(data, {
                formatUrl: getFormatUrl(),
                extra: extraJSON
            });
            try {
                JSON.stringify(data);
                logger.log("016000011", data)
            } catch (err) {}
        }
    };

    function isIE() {
        var myNav = navigator.userAgent.toLowerCase();
        return myNav.indexOf("msie") !== -1 ? parseInt(myNav.split("msie")[1], 10) : false
    }

    function _report(err) {
        if (typeof err === "string") {
            err = new Error(err)
        }
        if (err.hasReported) {
            return
        }
        err.hasReported = true;
        Logger.sendMsg(err, null, true)
    }

    function _inject(fn) {
        if (typeof fn.apply !== "function") {
            return fn
        }
        return function() {
            try {
                return fn.apply(this, arguments)
            } catch (err) {
                _report(err);
                console && console.warn && console.warn(err);
                throw err
            }
        }
    }

    function _transform(fn) {
        if (!fn || typeof fn.apply !== "function") {
            return fn
        }
        return function() {
            var arguments$1 = arguments;
            var args = [];
            var arg;
            for (var i = 0, l = arguments.length; i < l; i++) {
                arg = arguments$1[i];
                if (typeof arg === "function") {
                    arg = _inject(arguments$1[i])
                }
                args.push(arg)
            }
            return fn.apply(this, args)
        }
    }

    function _mix(target, src) {
        for (var key in src) {
            target[key] = src[key]
        }
    }

    function injectjQuery() {
        var $ = window.$;
        if (!$ || $ !== window.jQuery && $ !== window.Zepto) {
            return
        }
        var _ready = $.fn.ready;
        $.fn.ready = _transform(_ready);
        var _ajax = $.ajax;
        if (typeof _ajax === "function" && typeof _ajax.apply === "function") {
            $.ajax = function(url, options) {
                var target = null;
                if (typeof options === "undefined" && typeof url === "object") {
                    target = url
                } else if (typeof options === "object") {
                    target = options
                }
                if (target) {
                    if (typeof target.success === "function") {
                        target.success = _inject(target.success)
                    }
                    if (typeof target.complete === "function") {
                        target.complete = _inject(target.complete)
                    }
                }
                return _ajax.apply($, arguments)
            }
        }
    }

    function injectRequireJS() {
        var _require = window.require;
        var _define = window.define;
        if (_define && _define.amd && _require) {
            window.require = _transform(_require);
            _mix(window.require, _require);
            window.define = _transform(_define);
            _mix(window.define, _define)
        }
    }

    function injectSystem() {
        var _setTimeout = window.setTimeout;
        window.setTimeout = function(fn, ms) {
            if (typeof fn === "function") {
                fn = _inject(fn)
            }
            switch (arguments.length) {
                case 0:
                    return _setTimeout();
                case 1:
                    return _setTimeout(fn);
                default:
                    return _setTimeout(fn, ms)
            }
        };
        var _setInterval = window.setInterval;
        window.setInterval = _transform(_setInterval);
        var _requestAnimationFrame = window.requestAnimationFrame;
        if (typeof _requestAnimationFrame === "function") {
            window.requestAnimationFrame = _transform(_requestAnimationFrame)
        }
        if (window.EventTarget && window.EventTarget.prototype.addEventListener) {
            var addEventListener = window.EventTarget.prototype.addEventListener;
            window.EventTarget.prototype.addEventListener = function(event, callback, bubble) {
                if (callback && typeof callback.handleEvent === "function") {
                    callback.handleEvent = _inject(callback.handleEvent);
                    return addEventListener.call(this, event, callback, bubble)
                } else {
                    if (!callback.___wrapper) {
                        callback.___wrapper = _inject(callback)
                    }
                    return addEventListener.call(this, event, callback.___wrapper, bubble)
                }
            };
            var removeEventListener = window.EventTarget.prototype.removeEventListener;
            window.EventTarget.prototype.removeEventListener = function(event, callback, bubble) {
                if (!callback) {
                    return removeEventListener.call(this, event, callback, bubble)
                } else {
                    return removeEventListener.call(this, event, callback.___wrapper || callback, bubble)
                }
            }
        }
    }
    var Inject = {
        init: function init() {
            if (isIE() && isIE() < 9) {
                return
            }
            injectjQuery();
            injectRequireJS();
            injectSystem()
        }
    };
    var exit = false;
    if (window._trace) {
        console && console.warn && console.warn("WARNING: you already import trace");
        exit = true
    }
    try {
        if (localStorage.__disable__trace__) {
            console.warn("trace is disabled");
            exit = true
        }
    } catch (err) {}
    if (!/^https?/.test(location.protocol)) {
        console.warn("trace will work only under http or https protocol page");
        exit = true
    }
    if (!/(meilishuo|mogujie|xiaodian|uniny|meili-inc)\.com/.test(location.host)) {
        console.warn("trace will work only under *.(meilishuo|mogujie|xiaodian|uniny|meili-inc).com");
        exit = true
    }
    var M = window.M;
    if (!M) {
        console.warn("M is required before using trace");
        exit = true
    } else if (typeof M.isDev === "function" && M.isDev()) {
        console.warn("trace will work only under production mode");
        exit = true
    }
    if (typeof window.console === "undefined") {
        window.console = {
            log: function() {},
            warn: function() {}
        }
    }
    if (!exit) {
        Logger.init();
        Inject.init()
    }
    window._trace = {
        send: function send() {},
        sendImmediately: function sendImmediately() {},
        version: "1.2.3",
        config: config,
        sendMsg: Logger.sendMsg
    };
    var index = {};
    return index
}();
var ftx = function(t) {
    function e(n) {
        if (r[n]) return r[n].exports;
        var o = r[n] = {
            exports: {},
            id: n,
            loaded: !1
        };
        return t[n].call(o.exports, o, o.exports, e), o.loaded = !0, o.exports
    }
    var r = {};
    return e.m = t, e.c = r, e.p = "", e(0)
}([function(t, e, r) {
    function n(t, e) {
        var r = new i.FilterCSS(e);
        return r.process(t)
    }
    var o = r(10),
        i = r(2),
        a = r(8),
        s = r(13);
    "undefined" != typeof window && (window.FTX = {
        filterCSS: n,
        filterHTML: o,
        isDomainAllowed: a,
        safeParamParse: s
    }), t.exports = {
        filterCSS: n,
        filterHTML: o,
        isDomainAllowed: a,
        safeParamParse: s
    }
}, function(t, e, r) {
    function n() {
        return Array.prototype.concat.apply([], arguments)
    }

    function o(t, e) {
        for (var r = 0; e[r]; r++)
            if (e[r] === t) return !0;
        return !1
    }

    function i(t, e) {
        var r, n;
        if (Array.prototype.indexOf) return t.indexOf(e);
        for (r = 0, n = t.length; r < n; r++)
            if (t[r] === e) return r;
        return -1
    }
    var a = r(14),
        s = r(5);
    t.exports = {
        indexOf: i,
        inArray: o,
        arrayMerge: n,
        isDomainAllowed: function(t, e) {
            var r = a("hostname", t),
                i = [];
            e && e.exception && (s = n([], s, e.exception));
            for (var c = 0; c < s.length; c++) i.push((!!~r.indexOf(s[c])).toString());
            return !(s.length && !o("true", i))
        },
        forEach: function(t, e, r) {
            var n, o;
            if (Array.prototype.forEach) return t.forEach(e, r);
            for (n = 0, o = t.length; n < o; n++) e.call(r, t[n], n, t)
        },
        trim: function(t) {
            return String.prototype.trim ? t.trim() : t.replace(/(^\s*)|(\s*$)/g, "")
        },
        trimRight: function(t) {
            return String.prototype.trimRight ? t.trimRight() : t.replace(/(\s*$)/g, "")
        },
        extend: function(t) {
            t = t || {};
            for (var e = 1; e < arguments.length; e++)
                if (arguments[e])
                    for (var r in arguments[e]) arguments[e].hasOwnProperty(r) && (t[r] = arguments[e][r]);
            return t
        },
        getExtensionFileName: function(t) {
            var e = /(\\+)/g,
                r = t.replace(e, "#"),
                n = r.split("#"),
                o = n[n.length - 1],
                i = o.split(".");
            return i[i.length - 1]
        },
        parseUrl: a
    }
}, function(t, e, r) {
    function n(t) {
        return void 0 === t || null === t
    }

    function o(t) {
        var e = {};
        for (var r in t) e[r] = t[r];
        return e
    }

    function i(t) {
        t = o(t || {}), t.whiteList = c.extend(t.whiteList || a.whiteList, t.exception), t.onAttr = t.onAttr || a.onAttr, t.onIgnoreAttr = t.onIgnoreAttr || a.onIgnoreAttr, t.safeAttrValue = t.safeAttrValue || a.safeAttrValue, this.options = t
    }
    var a = r(6),
        s = r(7),
        c = r(1);
    i.prototype.process = function(t) {
        if (t = t || "", t = t.toString(), !t) return "";
        var e = this,
            r = e.options,
            o = r.whiteList,
            i = r.onAttr,
            a = r.onIgnoreAttr,
            c = r.safeAttrValue,
            l = s(t, function(t, e, r, s, l) {
                var u = o[r],
                    g = !1;
                if (u === !0 ? g = u : "function" == typeof u ? g = u(s) : u instanceof RegExp && (g = u.test(s)), g !== !0 && (g = !1), s = c(r, s)) {
                    var f, m = {
                        position: e,
                        sourcePosition: t,
                        source: l,
                        isWhite: g
                    };
                    return g ? (f = i(r, s, m), n(f) ? (~s.indexOf("!") && ~s.indexOf("important") && (s = s.replace(/!/, "").replace(/important/, "").trim()), r + ":" + s) : f) : (f = a(r, s, m), n(f) ? void 0 : f)
                }
            });
        return l
    }, t.exports = {
        FilterCSS: i,
        getDefaultWhiteList: a.getDefaultWhiteList
    }
}, , , function(t, e) {
    var r = [".mogujie.com", ".xiaodian.com", ".meilishuo.com", ".mogucdn.com", ".meili-inc.com", ".mogujie.org", ".mogutestcdn.com", ".uniny.com", ".taoshij.com", ".snobten.com", ".mogujie.cn", ".juangua.com", ".qq.com", ".myqcloud.com", ".emarbox.com", ".baidu.com", ".googleadservices.com", ".google-analytics.com", ".googletagmanager.com", ".google.com", ".letv.com", ".lecloud.com", ".letvcloud.com", ".gtimg.cn", ".idqqimg.com", "127.0.0.1", "localhost"];
    t.exports = r
}, function(t, e) {
    function r() {
        var t = {};
        return t["align-content"] = !1, t["align-items"] = !1, t["align-self"] = !1, t["alignment-adjust"] = !1, t["alignment-baseline"] = !1, t.all = !1, t["anchor-point"] = !1, t.animation = !1, t["animation-delay"] = !1, t["animation-direction"] = !1, t["animation-duration"] = !1, t["animation-fill-mode"] = !1, t["animation-iteration-count"] = !1, t["animation-name"] = !1, t["animation-play-state"] = !1, t["animation-timing-function"] = !1, t.azimuth = !1, t["backface-visibility"] = !1, t.background = !0, t["background-attachment"] = !0, t["background-clip"] = !0, t["background-color"] = !0, t["background-image"] = !0, t["background-origin"] = !0, t["background-position"] = !0, t["background-repeat"] = !0, t["background-size"] = !0, t["baseline-shift"] = !1, t.binding = !1, t.bleed = !1, t["bookmark-label"] = !1, t["bookmark-level"] = !1, t["bookmark-state"] = !1, t.border = !0, t["border-bottom"] = !0, t["border-bottom-color"] = !0, t["border-bottom-left-radius"] = !0, t["border-bottom-right-radius"] = !0, t["border-bottom-style"] = !0, t["border-bottom-width"] = !0, t["border-collapse"] = !0, t["border-color"] = !0, t["border-image"] = !0, t["border-image-outset"] = !0, t["border-image-repeat"] = !0, t["border-image-slice"] = !0, t["border-image-source"] = !0, t["border-image-width"] = !0, t["border-left"] = !0, t["border-left-color"] = !0, t["border-left-style"] = !0, t["border-left-width"] = !0, t["border-radius"] = !0, t["border-right"] = !0, t["border-right-color"] = !0, t["border-right-style"] = !0, t["border-right-width"] = !0, t["border-spacing"] = !0, t["border-style"] = !0, t["border-top"] = !0, t["border-top-color"] = !0, t["border-top-left-radius"] = !0, t["border-top-right-radius"] = !0, t["border-top-style"] = !0, t["border-top-width"] = !0, t["border-width"] = !0, t.bottom = !1, t["box-align"] = !1, t["box-decoration-break"] = !1, t["box-direction"] = !1, t["box-flex"] = !1, t["box-flex-group"] = !1, t["box-lines"] = !1, t["box-ordinal-group"] = !0, t["box-orient"] = !1, t["box-pack"] = !0, t["box-shadow"] = !0, t["box-sizing"] = !0, t["box-snap"] = !0, t["box-suppress"] = !0, t["break-after"] = !0, t["break-before"] = !0, t["break-inside"] = !0, t["caption-side"] = !1, t.chains = !1, t.clear = !0, t.clip = !1, t["clip-path"] = !1, t["clip-rule"] = !1, t.color = !0, t["color-interpolation-filters"] = !0, t["column-count"] = !1, t["column-fill"] = !1, t["column-gap"] = !1, t["column-rule"] = !1, t["column-rule-color"] = !1, t["column-rule-style"] = !1, t["column-rule-width"] = !1, t["column-span"] = !1, t["column-width"] = !1, t.columns = !1, t.contain = !1, t.content = !1, t["counter-increment"] = !1, t["counter-reset"] = !1, t["counter-set"] = !1, t.crop = !1, t.cue = !1, t["cue-after"] = !1, t["cue-before"] = !1, t.cursor = !1, t.direction = !1, t.display = !0, t["display-inside"] = !0, t["display-list"] = !0, t["display-outside"] = !0, t["dominant-baseline"] = !1, t.elevation = !1, t["empty-cells"] = !1, t.filter = !1, t.flex = !1, t["flex-basis"] = !1, t["flex-direction"] = !1, t["flex-flow"] = !1, t["flex-grow"] = !1, t["flex-shrink"] = !1, t["flex-wrap"] = !1, t.float = !1, t["float-offset"] = !1, t["flood-color"] = !1, t["flood-opacity"] = !1, t["flow-from"] = !1, t["flow-into"] = !1, t.font = !0, t["font-family"] = !0, t["font-feature-settings"] = !0, t["font-kerning"] = !0, t["font-language-override"] = !0, t["font-size"] = !0, t["font-size-adjust"] = !0, t["font-stretch"] = !0, t["font-style"] = !0, t["font-synthesis"] = !0, t["font-variant"] = !0, t["font-variant-alternates"] = !0, t["font-variant-caps"] = !0, t["font-variant-east-asian"] = !0, t["font-variant-ligatures"] = !0, t["font-variant-numeric"] = !0, t["font-variant-position"] = !0, t["font-weight"] = !0, t.grid = !1, t["grid-area"] = !1, t["grid-auto-columns"] = !1, t["grid-auto-flow"] = !1, t["grid-auto-rows"] = !1, t["grid-column"] = !1, t["grid-column-end"] = !1, t["grid-column-start"] = !1, t["grid-row"] = !1, t["grid-row-end"] = !1, t["grid-row-start"] = !1, t["grid-template"] = !1, t["grid-template-areas"] = !1, t["grid-template-columns"] = !1, t["grid-template-rows"] = !1, t["hanging-punctuation"] = !1, t.height = !0, t.hyphens = !1, t.icon = !1, t["image-orientation"] = !1, t["image-resolution"] = !1, t["ime-mode"] = !1, t["initial-letters"] = !1, t["inline-box-align"] = !1, t["justify-content"] = !1, t["justify-items"] = !1, t["justify-self"] = !1, t.left = !1, t["letter-spacing"] = !0, t["lighting-color"] = !0, t["line-box-contain"] = !1, t["line-break"] = !1, t["line-grid"] = !1, t["line-height"] = !1, t["line-snap"] = !1, t["line-stacking"] = !1, t["line-stacking-ruby"] = !1, t["line-stacking-shift"] = !1, t["line-stacking-strategy"] = !1, t["list-style"] = !0, t["list-style-image"] = !0, t["list-style-position"] = !0, t["list-style-type"] = !0, t.margin = !0, t["margin-bottom"] = !0, t["margin-left"] = !0, t["margin-right"] = !0, t["margin-top"] = !0, t["marker-offset"] = !1, t["marker-side"] = !1, t.marks = !1, t.mask = !1, t["mask-box"] = !1, t["mask-box-outset"] = !1, t["mask-box-repeat"] = !1, t["mask-box-slice"] = !1, t["mask-box-source"] = !1, t["mask-box-width"] = !1, t["mask-clip"] = !1, t["mask-image"] = !1, t["mask-origin"] = !1, t["mask-position"] = !1, t["mask-repeat"] = !1, t["mask-size"] = !1, t["mask-source-type"] = !1, t["mask-type"] = !1, t["max-height"] = !0, t["max-lines"] = !1, t["max-width"] = !0, t["min-height"] = !0, t["min-width"] = !0, t.monochrome = !1, t["move-to"] = !1, t["nav-down"] = !1, t["nav-index"] = !1, t["nav-left"] = !1, t["nav-right"] = !1, t["nav-up"] = !1, t["object-fit"] = !1, t["object-position"] = !1, t.opacity = !1, t.order = !1, t.orphans = !1, t.outline = !1, t["outline-color"] = !1, t["outline-offset"] = !1, t["outline-style"] = !1, t["outline-width"] = !1, t.overflow = !1, t["overflow-wrap"] = !1, t["overflow-x"] = !1, t["overflow-y"] = !1, t.padding = !0, t["padding-bottom"] = !0, t["padding-left"] = !0, t["padding-right"] = !0, t["padding-top"] = !0, t.page = !1, t["page-break-after"] = !1, t["page-break-before"] = !1, t["page-break-inside"] = !1, t["page-policy"] = !1, t.pause = !1, t["pause-after"] = !1, t["pause-before"] = !1, t.perspective = !1, t["perspective-origin"] = !1, t.pitch = !1, t["pitch-range"] = !1, t["play-during"] = !1, t.position = !1, t["presentation-level"] = !1, t.quotes = !1, t["region-fragment"] = !1, t.resize = !1, t.rest = !1, t["rest-after"] = !1, t["rest-before"] = !1, t.richness = !1, t.right = !1, t.rotation = !1, t["rotation-point"] = !1, t["ruby-align"] = !1, t["ruby-merge"] = !1, t["ruby-position"] = !1, t.scan = !1, t["shape-image-threshold"] = !1, t["shape-outside"] = !1, t["shape-margin"] = !1, t.size = !1, t.speak = !1, t["speak-as"] = !1, t["speak-header"] = !1, t["speak-numeral"] = !1, t["speak-punctuation"] = !1, t["speech-rate"] = !1, t.stress = !1, t["string-set"] = !1, t["tab-size"] = !1, t["table-layout"] = !1, t["text-align"] = !0, t["text-align-last"] = !0, t["text-combine-upright"] = !0, t["text-decoration"] = !0, t["text-decoration-color"] = !0, t["text-decoration-line"] = !0, t["text-decoration-skip"] = !0, t["text-decoration-style"] = !0, t["text-emphasis"] = !0, t["text-emphasis-color"] = !0, t["text-emphasis-position"] = !0, t["text-emphasis-style"] = !0, t["text-height"] = !0, t["text-indent"] = !0, t["text-justify"] = !0, t["text-orientation"] = !0, t["text-overflow"] = !0, t["text-shadow"] = !0, t["text-space-collapse"] = !0, t["text-transform"] = !0, t["text-underline-position"] = !0, t["text-wrap"] = !0, t.top = !1, t.transform = !1, t["transform-origin"] = !1, t["transform-style"] = !1, t.transition = !1, t["transition-delay"] = !1, t["transition-duration"] = !1, t["transition-property"] = !1, t["transition-timing-function"] = !1, t["unicode-bidi"] = !1, t["vertical-align"] = !1, t.visibility = !1, t["voice-balance"] = !1, t["voice-duration"] = !1, t["voice-family"] = !1, t["voice-pitch"] = !1, t["voice-range"] = !1, t["voice-rate"] = !1, t["voice-stress"] = !1, t["voice-volume"] = !1, t.volume = !1, t["white-space"] = !1, t.widows = !1, t.width = !0, t["will-change"] = !1, t["word-break"] = !0, t["word-spacing"] = !0, t["word-wrap"] = !0, t["wrap-flow"] = !1, t["wrap-through"] = !1, t["writing-mode"] = !1, t["z-index"] = !1, t.zoom = !0, t
    }

    function n(t, e, r) {}

    function o(t, e, r) {}

    function i(t, e) {
        return a.test(e) ? "" : s.test(e) ? "" : e
    }
    var a = /javascript\s*\:/gim,
        s = /expression/gim;
    e.whiteList = r(), e.getDefaultWhiteList = r, e.onAttr = n, e.onIgnoreAttr = o, e.safeAttrValue = i
}, function(t, e, r) {
    function n(t, e) {
        function r() {
            if (!i) {
                var r = o.trim(t.slice(a, s)),
                    n = r.indexOf(":");
                if (n !== -1) {
                    var l = o.trim(r.slice(0, n)),
                        u = o.trim(r.slice(n + 1));
                    if (l) {
                        var g = e(a, c.length, l, u, r);
                        g && (c += g + "; ")
                    }
                }
            }
            a = s + 1
        }
        t = o.trimRight(t), ";" !== t[t.length - 1] && (t += ";");
        for (var n = t.length, i = !1, a = 0, s = 0, c = ""; s < n; s++) {
            var l = t[s];
            if ("/" === l && "*" === t[s + 1]) {
                var u = t.indexOf("*/", s + 2);
                if (u === -1) break;
                s = u + 1, a = s + 1, i = !1
            } else "(" === l ? i = !0 : ")" === l ? i = !1 : ";" === l ? i || r() : "\n" === l && r()
        }
        return o.trim(c)
    }
    var o = r(1);
    t.exports = n
}, function(t, e, r) {
    var n = window.FTX || {},
        o = r(1);
    n.isDomainAllowed = o.isDomainAllowed, window.FTX = n, t.exports = o.isDomainAllowed
}, function(t, e, r) {
    function n() {
        return {
            a: ["target", "href", "title"],
            abbr: ["title"],
            address: [],
            area: ["shape", "coords", "href", "alt"],
            article: [],
            aside: [],
            audio: ["autoplay", "controls", "loop", "preload", "src"],
            b: [],
            body: [],
            bdi: ["dir"],
            bdo: ["dir"],
            big: [],
            blockquote: ["cite"],
            br: [],
            button: [],
            caption: [],
            center: [],
            cite: [],
            code: [],
            col: ["align", "valign", "span", "width"],
            colgroup: ["align", "valign", "span", "width"],
            dd: [],
            del: ["datetime"],
            details: ["open"],
            div: [],
            dl: [],
            dt: [],
            em: [],
            font: ["color", "size", "face"],
            footer: [],
            h1: [],
            h2: [],
            h3: [],
            h4: [],
            h5: [],
            h6: [],
            head: [],
            header: [],
            hr: [],
            html: ["lang"],
            i: [],
            img: ["src", "alt", "title", "width", "height"],
            ins: ["datetime"],
            li: [],
            link: ["rel", "href", "type"],
            mark: [],
            meta: ["name", "content", "charset"],
            nav: [],
            ol: [],
            p: [],
            pre: [],
            s: [],
            section: [],
            small: [],
            span: [],
            sub: [],
            sup: [],
            strong: [],
            table: ["width", "border", "align", "valign"],
            tbody: ["align", "valign"],
            td: ["width", "rowspan", "colspan", "align", "valign"],
            tfoot: ["align", "valign"],
            th: ["width", "rowspan", "colspan", "align", "valign"],
            thead: ["align", "valign"],
            title: [],
            tr: ["rowspan", "align", "valign"],
            tt: [],
            u: [],
            ul: [],
            video: ["autoplay", "controls", "loop", "preload", "src", "height", "width"]
        }
    }

    function o(t, e, r) {}

    function i(t, e, r) {}

    function a(t, e, r) {}

    function s(t, e, r) {}

    function c(t) {
        return t.replace(I, "&lt;").replace(j, "&gt;")
    }

    function l(t, e, r, n) {
        if (r = d(r), "href" === e || "src" === e) {
            if (r = A.trim(r), "#" === r) return "#";
            if (!A.isDomainAllowed(r)) return "";
            if ("http://" !== r.substr(0, 7) && "https://" !== r.substr(0, 8) && "mailto:" !== r.substr(0, 7) && "#" !== r[0] && "/" !== r[0]) return "";
            if ("img" === t && "src" === e) {
                var o = A.getExtensionFileName(r);
                if (!~["jpg", "jpeg", "png", "gif", "webp"].indexOf(o)) return ""
            }
        } else if ("background" === e) {
            if (q.lastIndex = 0, q.test(r)) return ""
        } else if ("style" === e) {
            if (O.lastIndex = 0, O.test(r)) return "";
            if (D.lastIndex = 0, D.test(r) && (q.lastIndex = 0, q.test(r))) return "";
            n !== !1 && (n = n || T, r = n.process(r))
        }
        return r = h(r)
    }

    function u(t) {
        return t.replace(S, "&quot;")
    }

    function g(t) {
        return t.replace(z, '"')
    }

    function f(t) {
        return t.replace(C, function(t, e) {
            return "x" === e[0] || "X" === e[0] ? String.fromCharCode(parseInt(e.substr(1), 16)) : String.fromCharCode(parseInt(e, 10))
        })
    }

    function m(t) {
        return t.replace(F, ":").replace(L, " ")
    }

    function p(t) {
        for (var e = "", r = 0, n = t.length; r < n; r++) e += t.charCodeAt(r) < 32 ? " " : t.charAt(r);
        return A.trim(e)
    }

    function d(t) {
        return t = g(t), t = f(t), t = m(t), t = p(t)
    }

    function h(t) {
        return t = u(t), t = c(t)
    }

    function b() {
        return ""
    }

    function v(t, e) {
        function r(e) {
            return !!n || A.indexOf(t, e) !== -1
        }
        "function" != typeof e && (e = function() {});
        var n = !Array.isArray(t),
            o = [],
            i = !1;
        return {
            onIgnoreTag: function(t, n, a) {
                if (r(t)) {
                    if (a.isClosing) {
                        var s = "[/removed]",
                            c = a.position + s.length;
                        return o.push([i !== !1 ? i : a.position, c]), i = !1, s
                    }
                    return i || (i = a.position), "[removed]"
                }
                return e(t, n, a)
            },
            remove: function(t) {
                var e = "",
                    r = 0;
                return A.forEach(o, function(n) {
                    e += t.slice(r, n[0]), r = n[1]
                }), e += t.slice(r)
            }
        }
    }

    function x(t) {
        return t.replace(V, "")
    }

    function w(t) {
        var e = t.split("");
        return e = e.filter(function(t) {
            var e = t.charCodeAt(0);
            return 127 !== e && (!(e <= 31) || (10 === e || 13 === e))
        }), e.join("")
    }
    var y = r(2).FilterCSS,
        k = r(2).getDefaultWhiteList,
        A = r(1),
        T = new y,
        I = /</g,
        j = />/g,
        S = /"/g,
        z = /&quot;/g,
        C = /&#([a-zA-Z0-9]*);?/gim,
        F = /&colon;?/gim,
        L = /&newline;?/gim,
        q = /((j\s*a\s*v\s*a|v\s*b|l\s*i\s*v\s*e)\s*s\s*c\s*r\s*i\s*p\s*t\s*|m\s*o\s*c\s*h\s*a)\:/gi,
        O = /e\s*x\s*p\s*r\s*e\s*s\s*s\s*i\s*o\s*n\s*\(.*/gi,
        D = /u\s*r\s*l\s*\(.*/gi,
        V = /<!--[\s\S]*?-->/g;
    e.whiteList = n(), e.getDefaultWhiteList = n, e.onTag = o, e.onIgnoreTag = i, e.onTagAttr = a, e.onIgnoreTagAttr = s, e.safeAttrValue = l, e.escapeHtml = c, e.escapeQuote = u, e.unescapeQuote = g, e.escapeHtmlEntities = f, e.escapeDangerHtml5Entities = m, e.clearNonPrintableCharacter = p, e.friendlyAttrValue = d, e.escapeAttrValue = h, e.onIgnoreTagStripAll = b, e.StripTagBody = v, e.stripCommentTag = x, e.stripBlankChar = w, e.cssFilter = T, e.getDefaultCSSWhiteList = k
}, function(t, e, r) {
    function n(t, e) {
        var r = new o(e);
        return r.process(t)
    }
    var o = r(12);
    t.exports = n
}, function(t, e, r) {
    function n(t) {
        var e, r = t.indexOf(" ");
        return e = r === -1 ? t.slice(1, -1) : t.slice(1, r + 1), e = g.trim(e).toLowerCase(), "/" === e.slice(0, 1) && (e = e.slice(1)), "/" === e.slice(-1) && (e = e.slice(0, -1)), e
    }

    function o(t) {
        return "</" === t.slice(0, 2)
    }

    function i(t, e, r) {
        var i = "",
            a = 0,
            s = !1,
            c = !1,
            l = 0,
            u = t.length,
            g = "",
            f = "";
        for (l = 0; l < u; l++) {
            var m = t.charAt(l);
            if (s === !1) {
                if ("<" === m) {
                    s = l;
                    continue
                }
            } else if (c === !1) {
                if ("<" === m) {
                    i += r(t.slice(a, l)), s = l, a = l;
                    continue
                }
                if (">" === m) {
                    i += r(t.slice(a, s)), g = t.slice(s, l + 1), f = n(g), i += e(s, i.length, f, g, o(g)), a = l + 1, s = !1;
                    continue
                }
                if (('"' === m || "'" === m) && "=" === t.charAt(l - 1)) {
                    c = m;
                    continue
                }
            } else if (m === c) {
                c = !1;
                continue
            }
        }
        return a < t.length && (i += r(t.substr(a))), i
    }

    function a(t, e) {
        function r(t, r) {
            if (t = g.trim(t), t = t.replace(f, "").toLowerCase(), !(t.length < 1)) {
                var n = e(t, r || "");
                n && o.push(n)
            }
        }
        for (var n = 0, o = [], i = !1, a = t.length, l = 0; l < a; l++) {
            var m, p, d = t.charAt(l);
            if (i !== !1 || "=" !== d)
                if (i === !1 || l !== n || '"' !== d && "'" !== d || "=" !== t.charAt(l - 1))
                    if (" " !== d);
                    else {
                        if (i === !1) {
                            if (p = s(t, l), p === -1) {
                                m = g.trim(t.slice(n, l)), r(m), i = !1, n = l + 1;
                                continue
                            }
                            l = p - 1;
                            continue
                        }
                        if (p = c(t, l - 1), p === -1) {
                            m = g.trim(t.slice(n, l)), m = u(m), r(i, m), i = !1, n = l + 1;
                            continue
                        }
                    }
            else {
                if (p = t.indexOf(d, l + 1), p === -1) break;
                m = g.trim(t.slice(n + 1, p)), r(i, m), i = !1, l = p, n = l + 1
            } else i = t.slice(n, l), n = l + 1
        }
        return n < t.length && (i === !1 ? r(t.slice(n)) : r(i, u(g.trim(t.slice(n))))), g.trim(o.join(" "))
    }

    function s(t, e) {
        for (; e < t.length; e++) {
            var r = t[e];
            if (" " !== r) return "=" === r ? e : -1
        }
    }

    function c(t, e) {
        for (; e > 0; e--) {
            var r = t[e];
            if (" " !== r) return "=" === r ? e : -1
        }
    }

    function l(t) {
        return '"' === t[0] && '"' === t[t.length - 1] || "'" === t[0] && "'" === t[t.length - 1]
    }

    function u(t) {
        return l(t) ? t.substr(1, t.length - 2) : t
    }
    var g = r(1),
        f = /[^a-zA-Z0-9_:\.\-]/gim;
    e.parseTag = i, e.parseAttr = a
}, function(t, e, r) {
    function n(t) {
        return void 0 === t || null === t
    }

    function o(t) {
        var e = t.indexOf(" ");
        if (e === -1) return {
            html: "",
            closing: "/" === t[t.length - 2]
        };
        t = f.trim(t.slice(e + 1, -1));
        var r = "/" === t[t.length - 1];
        return r && (t = f.trim(t.slice(0, -1))), {
            html: t,
            closing: r
        }
    }

    function i(t) {
        var e = {};
        for (var r in t) e[r] = t[r];
        return e
    }

    function a(t) {
        t = i(t || {}), t.stripIgnoreTag && (t.onIgnoreTag && console.error('Notes: cannot use these two options "stripIgnoreTag" and "onIgnoreTag" at the same time'), t.onIgnoreTag = c.onIgnoreTagStripAll), t.whiteList = f.extend(t.whiteList || c.whiteList, t.exception), t.onTag = t.onTag || c.onTag, t.onTagAttr = t.onTagAttr || c.onTagAttr, t.onIgnoreTag = t.onIgnoreTag || c.onIgnoreTag, t.onIgnoreTagAttr = t.onIgnoreTagAttr || c.onIgnoreTagAttr, t.safeAttrValue = t.safeAttrValue || c.safeAttrValue, t.escapeHtml = t.escapeHtml || c.escapeHtml, this.options = t, t.inlineStyleFilter === !1 ? this.cssFilter = !1 : "boolean" == typeof t.inlineStyleFilter && t.inlineStyleFilter ? this.cssFilter = new s : (t.cssFilter = t.inlineStyleFilter || null, this.cssFilter = new s(t.cssFilter))
    }
    var s = r(2).FilterCSS,
        c = r(9),
        l = r(11),
        u = l.parseTag,
        g = l.parseAttr,
        f = r(1);
    a.prototype.process = function(t) {
        if (t = t || "", t = t.toString(), !t) return "";
        var e = this,
            r = e.options,
            i = r.whiteList,
            a = r.onTag,
            s = r.onIgnoreTag,
            l = r.onTagAttr,
            m = r.onIgnoreTagAttr,
            p = r.safeAttrValue,
            d = r.escapeHtml,
            h = e.cssFilter;
        r.stripBlankChar && (t = c.stripBlankChar(t)), r.allowCommentTag || (t = c.stripCommentTag(t));
        var b = !1;
        if (r.stripIgnoreTagBody) {
            var b = c.StripTagBody(r.stripIgnoreTagBody, s);
            s = b.onIgnoreTag
        }
        var v = u(t, function(t, e, r, c, u) {
            var b = {
                    sourcePosition: t,
                    position: e,
                    isClosing: u,
                    isWhite: r in i
                },
                v = a(r, c, b);
            if (!n(v)) return v;
            if (b.isWhite) {
                if (b.isClosing) return "</" + r + ">";
                var x = o(c),
                    w = i[r];
                w.push("id", "class", "style");
                var y = g(x.html, function(t, e) {
                        var o = f.indexOf(w, t) !== -1,
                            i = l(r, t, e, o);
                        if (!n(i)) return i;
                        if (o) return e = p(r, t, e, h), e ? t + '="' + e + '"' : t;
                        var i = m(r, t, e, o);
                        return n(i) ? void 0 : i
                    }),
                    c = "<" + r;
                return y && (c += " " + y), x.closing && (c += " /"), c += ">"
            }
            var v = s(r, c, b);
            return n(v) ? d(c) : v
        }, d);
        return b && (v = b.remove(v)), v
    }, t.exports = a
}, function(t, e) {
    function r(t) {
        return t.replace(/^\s+|\s+$/gm, "")
    }

    function n(t) {
        return "string" == typeof t && t ? (t = r(t), /^[\],:{}\s]*$/.test(t.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@").replace(/(?:'|")[^'"\\\n\r]*('|")|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:\s*\[)+/g, ":").replace(/\w*\s*\:/g, ":")) ? new Function("return " + t)() : {}) : {}
    }

    function o(t) {
        t = r(t.replace(/\(|\]\.|\+|\)|\\|new\s/g, "@"));
        try {
            return n(t)
        } catch (t) {}
    }
    t.exports = o
}, function(t, e) {
    function r() {
        return new RegExp(/(.*?)\.?([^\.]*?)\.?(com|net|org|biz|ws|in|me|co\.uk|co|org\.uk|ltd\.uk|plc\.uk|me\.uk|edu|mil|br\.com|cn\.com|eu\.com|hu\.com|no\.com|qc\.com|sa\.com|se\.com|se\.net|us\.com|uy\.com|ac|co\.ac|gv\.ac|or\.ac|ac\.ac|af|am|as|at|ac\.at|co\.at|gv\.at|or\.at|asn\.au|com\.au|edu\.au|org\.au|net\.au|id\.au|be|ac\.be|adm\.br|adv\.br|am\.br|arq\.br|art\.br|bio\.br|cng\.br|cnt\.br|com\.br|ecn\.br|eng\.br|esp\.br|etc\.br|eti\.br|fm\.br|fot\.br|fst\.br|g12\.br|gov\.br|ind\.br|inf\.br|jor\.br|lel\.br|med\.br|mil\.br|net\.br|nom\.br|ntr\.br|odo\.br|org\.br|ppg\.br|pro\.br|psc\.br|psi\.br|rec\.br|slg\.br|tmp\.br|tur\.br|tv\.br|vet\.br|zlg\.br|br|ab\.ca|bc\.ca|mb\.ca|nb\.ca|nf\.ca|ns\.ca|nt\.ca|on\.ca|pe\.ca|qc\.ca|sk\.ca|yk\.ca|ca|cc|ac\.cn|com\.cn|edu\.cn|gov\.cn|org\.cn|bj\.cn|sh\.cn|tj\.cn|cq\.cn|he\.cn|nm\.cn|ln\.cn|jl\.cn|hl\.cn|js\.cn|zj\.cn|ah\.cn|gd\.cn|gx\.cn|hi\.cn|sc\.cn|gz\.cn|yn\.cn|xz\.cn|sn\.cn|gs\.cn|qh\.cn|nx\.cn|xj\.cn|tw\.cn|hk\.cn|mo\.cn|cn|cx|cz|de|dk|fo|com\.ec|tm\.fr|com\.fr|asso\.fr|presse\.fr|fr|gf|gs|co\.il|net\.il|ac\.il|k12\.il|gov\.il|muni\.il|ac\.in|co\.in|org\.in|ernet\.in|gov\.in|net\.in|res\.in|is|it|ac\.jp|co\.jp|go\.jp|or\.jp|ne\.jp|ac\.kr|co\.kr|go\.kr|ne\.kr|nm\.kr|or\.kr|li|lt|lu|asso\.mc|tm\.mc|com\.mm|org\.mm|net\.mm|edu\.mm|gov\.mm|ms|nl|no|nu|pl|ro|org\.ro|store\.ro|tm\.ro|firm\.ro|www\.ro|arts\.ro|rec\.ro|info\.ro|nom\.ro|nt\.ro|se|si|com\.sg|org\.sg|net\.sg|gov\.sg|sk|st|tf|ac\.th|co\.th|go\.th|mi\.th|net\.th|or\.th|tm|to|com\.tr|edu\.tr|gov\.tr|k12\.tr|net\.tr|org\.tr|com\.tw|org\.tw|net\.tw|ac\.uk|uk\.com|uk\.net|gb\.com|gb\.net|vg|sh|kz|ch|info|ua|gov|name|pro|ie|hk|com\.hk|org\.hk|net\.hk|edu\.hk|us|tk|cd|by|ad|lv|eu\.lv|bz|es|jp|cl|ag|mobi|eu|co\.nz|org\.nz|net\.nz|maori\.nz|iwi\.nz|io|la|md|sc|sg|vc|tw|travel|my|se|tv|pt|com\.pt|edu\.pt|asia|fi|com\.ve|net\.ve|fi|org\.ve|web\.ve|info\.ve|co\.ve|tel|im|gr|ru|net\.ru|org\.ru|hr|com\.hr|ly|xyz)$/)
    }

    function n(t) {
        return decodeURIComponent(t.replace(/\+/g, " "))
    }

    function o(t, e) {
        var r = t.charAt(0),
            n = e.split(r);
        return r === t ? n : (t = parseInt(t.substring(1), 10), n[t < 0 ? n.length + t : t - 1])
    }

    function i(t, e) {
        for (var r = t.charAt(0), o = e.split("&"), i = [], a = {}, s = [], c = t.substring(1), l = 0, u = o.length; l < u; l++)
            if (i = o[l].match(/(.*?)=(.*)/), i || (i = [o[l], o[l], ""]), "" !== i[1].replace(/\s/g, "")) {
                if (i[2] = n(i[2] || ""), c === i[1]) return i[2];
                s = i[1].match(/(.*)\[([0-9]+)\]/), s ? (a[s[1]] = a[s[1]] || [], a[s[1]][s[2]] = i[2]) : a[i[1]] = i[2]
            }
        return r === t ? a : a[c]
    }

    function a(t, e) {
        var n, a = {};
        if ("tld?" === t) return r();
        if (e = e || window.location.toString(), !t) return e;
        if (t = t.toString(), n = e.match(/^mailto:([^\/].+)/)) a.protocol = "mailto", a.email = n[1];
        else {
            if ((n = e.match(/(.*?)\/#\!(.*)/)) && (e = n[1] + n[2]), (n = e.match(/(.*?)#(.*)/)) && (a.hash = n[2], e = n[1]), a.hash && t.match(/^#/)) return i(t, a.hash);
            if ((n = e.match(/(.*?)\?(.*)/)) && (a.query = n[2], e = n[1]), a.query && t.match(/^\?/)) return i(t, a.query);
            if ((n = e.match(/(.*?)\:?\/\/(.*)/)) && (a.protocol = n[1].toLowerCase(), e = n[2]), (n = e.match(/(.*?)(\/.*)/)) && (a.path = n[2], e = n[1]), a.path = (a.path || "").replace(/^([^\/])/, "/$1"), t.match(/^[\-0-9]+$/) && (t = t.replace(/^([^\/])/, "/$1")), t.match(/^\//)) return o(t, a.path.substring(1));
            if (n = o("/-1", a.path.substring(1)), n && (n = n.match(/(.*?)\.(.*)/)) && (a.file = n[0], a.filename = n[1], a.fileext = n[2]), (n = e.match(/(.*)\:([0-9]+)$/)) && (a.port = n[2], e = n[1]), (n = e.match(/(.*?)@(.*)/)) && (a.auth = n[1], e = n[2]), a.auth && (n = a.auth.match(/(.*)\:(.*)/), a.user = n ? n[1] : a.auth, a.pass = n ? n[2] : void 0), a.hostname = e.toLowerCase(), "." === t.charAt(0)) return o(t, a.hostname);
            r() && (n = a.hostname.match(r()), n && (a.tld = n[3], a.domain = n[2] ? n[2] + "." + n[3] : void 0, a.sub = n[1] || void 0)), a.port = a.port || ("https" === a.protocol ? "443" : "80"), a.protocol = a.protocol || ("443" === a.port ? "https" : "http")
        }
        return t in a ? a[t] : "{}" === t ? a : void 0
    }
    t.exports = a
}]);
window.vue = function(e) {
    function t(r) {
        if (n[r]) return n[r].exports;
        var i = n[r] = {
            exports: {},
            id: r,
            loaded: !1
        };
        return e[r].call(i.exports, i, i.exports, t), i.loaded = !0, i.exports
    }
    var n = {};
    return t.m = e, t.c = n, t.p = "", t(0)
}({
    0: function(e, t, n) {
        function r(e) {
            return e && e.__esModule ? e : {
                default: e
            }
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var i = n(19),
            o = r(i);
        t["default"] = o["default"], e.exports = t["default"]
    },
    19: function(e, t, n) {
        (function(t) {
            function n(e) {
                return void 0 === e || null === e
            }

            function r(e) {
                return void 0 !== e && null !== e
            }

            function i(e) {
                return e === !0
            }

            function o(e) {
                return e === !1
            }

            function a(e) {
                return "string" == typeof e || "number" == typeof e
            }

            function s(e) {
                return null !== e && "object" === ("undefined" == typeof e ? "undefined" : Hi(e))
            }

            function c(e) {
                return "[object Object]" === Ui.call(e)
            }

            function u(e) {
                return "[object RegExp]" === Ui.call(e)
            }

            function l(e) {
                return null == e ? "" : "object" === ("undefined" == typeof e ? "undefined" : Hi(e)) ? JSON.stringify(e, null, 2) : String(e)
            }

            function f(e) {
                var t = parseFloat(e);
                return isNaN(t) ? e : t
            }

            function p(e, t) {
                for (var n = Object.create(null), r = e.split(","), i = 0; i < r.length; i++) n[r[i]] = !0;
                return t ? function(e) {
                    return n[e.toLowerCase()]
                } : function(e) {
                    return n[e]
                }
            }

            function d(e, t) {
                if (e.length) {
                    var n = e.indexOf(t);
                    if (n > -1) return e.splice(n, 1)
                }
            }

            function v(e, t) {
                return zi.call(e, t)
            }

            function h(e) {
                var t = Object.create(null);
                return function(n) {
                    var r = t[n];
                    return r || (t[n] = e(n))
                }
            }

            function m(e, t) {
                function n(n) {
                    var r = arguments.length;
                    return r ? r > 1 ? e.apply(t, arguments) : e.call(t, n) : e.call(t)
                }
                return n._length = e.length, n
            }

            function g(e, t) {
                t = t || 0;
                for (var n = e.length - t, r = new Array(n); n--;) r[n] = e[n + t];
                return r
            }

            function y(e, t) {
                for (var n in t) e[n] = t[n];
                return e
            }

            function _(e) {
                for (var t = {}, n = 0; n < e.length; n++) e[n] && y(t, e[n]);
                return t
            }

            function b() {}

            function $(e) {
                return e.reduce(function(e, t) {
                    return e.concat(t.staticKeys || [])
                }, []).join(",")
            }

            function w(e, t) {
                var n = s(e),
                    r = s(t);
                if (!n || !r) return !n && !r && String(e) === String(t);
                try {
                    return JSON.stringify(e) === JSON.stringify(t)
                } catch (i) {
                    return e === t
                }
            }

            function x(e, t) {
                for (var n = 0; n < e.length; n++)
                    if (w(e[n], t)) return n;
                return -1
            }

            function C(e) {
                var t = !1;
                return function() {
                    t || (t = !0, e.apply(this, arguments))
                }
            }

            function k(e) {
                var t = (e + "").charCodeAt(0);
                return 36 === t || 95 === t
            }

            function A(e, t, n, r) {
                Object.defineProperty(e, t, {
                    value: n,
                    enumerable: !!r,
                    writable: !0,
                    configurable: !0
                })
            }

            function O(e) {
                if (!ro.test(e)) {
                    var t = e.split(".");
                    return function(e) {
                        for (var n = 0; n < t.length; n++) {
                            if (!e) return;
                            e = e[t[n]]
                        }
                        return e
                    }
                }
            }

            function S(e, t, n) {
                if (to.errorHandler) to.errorHandler.call(null, e, t, n);
                else {
                    if (!ao || "undefined" == typeof console) throw e;
                    console.error(e)
                }
            }

            function T(e) {
                return "function" == typeof e && /native code/.test(e.toString())
            }

            function E(e) {
                ko.target && Ao.push(ko.target), ko.target = e
            }

            function j() {
                ko.target = Ao.pop()
            }

            function N(e, t) {
                e.__proto__ = t
            }

            function L(e, t, n) {
                for (var r = 0, i = n.length; r < i; r++) {
                    var o = n[r];
                    A(e, o, t[o])
                }
            }

            function I(e, t) {
                if (s(e)) {
                    var n;
                    return v(e, "__ob__") && e.__ob__ instanceof jo ? n = e.__ob__ : Eo.shouldConvert && !bo() && (Array.isArray(e) || c(e)) && Object.isExtensible(e) && !e._isVue && (n = new jo(e)), t && n && n.vmCount++, n
                }
            }

            function D(e, t, n, r) {
                var i = new ko,
                    o = Object.getOwnPropertyDescriptor(e, t);
                if (!o || o.configurable !== !1) {
                    var a = o && o.get,
                        s = o && o.set,
                        c = I(n);
                    Object.defineProperty(e, t, {
                        enumerable: !0,
                        configurable: !0,
                        get: function() {
                            var t = a ? a.call(e) : n;
                            return ko.target && (i.depend(), c && c.dep.depend(), Array.isArray(t) && R(t)), t
                        },
                        set: function(t) {
                            var r = a ? a.call(e) : n;
                            t === r || t !== t && r !== r || (s ? s.call(e, t) : n = t, c = I(t), i.notify())
                        }
                    })
                }
            }

            function M(e, t, n) {
                if (Array.isArray(e) && "number" == typeof t) return e.length = Math.max(e.length, t), e.splice(t, 1, n), n;
                if (v(e, t)) return e[t] = n, n;
                var r = e.__ob__;
                return e._isVue || r && r.vmCount ? n : r ? (D(r.value, t, n), r.dep.notify(), n) : (e[t] = n, n)
            }

            function P(e, t) {
                if (Array.isArray(e) && "number" == typeof t) return void e.splice(t, 1);
                var n = e.__ob__;
                e._isVue || n && n.vmCount || v(e, t) && (delete e[t], n && n.dep.notify())
            }

            function R(e) {
                for (var t = void 0, n = 0, r = e.length; n < r; n++) t = e[n], t && t.__ob__ && t.__ob__.dep.depend(), Array.isArray(t) && R(t)
            }

            function F(e, t) {
                if (!t) return e;
                for (var n, r, i, o = Object.keys(t), a = 0; a < o.length; a++) n = o[a], r = e[n], i = t[n], v(e, n) ? c(r) && c(i) && F(r, i) : M(e, n, i);
                return e
            }

            function B(e, t) {
                return t ? e ? e.concat(t) : Array.isArray(t) ? t : [t] : e
            }

            function H(e, t) {
                var n = Object.create(e || null);
                return t ? y(n, t) : n
            }

            function U(e) {
                var t = e.props;
                if (t) {
                    var n, r, i, o = {};
                    if (Array.isArray(t))
                        for (n = t.length; n--;) r = t[n], "string" == typeof r && (i = Ki(r), o[i] = {
                            type: null
                        });
                    else if (c(t))
                        for (var a in t) r = t[a], i = Ki(a), o[i] = c(r) ? r : {
                            type: r
                        };
                    e.props = o
                }
            }

            function V(e) {
                var t = e.directives;
                if (t)
                    for (var n in t) {
                        var r = t[n];
                        "function" == typeof r && (t[n] = {
                            bind: r,
                            update: r
                        })
                    }
            }

            function z(e, t, n) {
                function r(r) {
                    var i = No[r] || Lo;
                    c[r] = i(e[r], t[r], n, r)
                }
                "function" == typeof t && (t = t.options), U(t), V(t);
                var i = t["extends"];
                if (i && (e = z(e, i, n)), t.mixins)
                    for (var o = 0, a = t.mixins.length; o < a; o++) e = z(e, t.mixins[o], n);
                var s, c = {};
                for (s in e) r(s);
                for (s in t) v(e, s) || r(s);
                return c
            }

            function J(e, t, n, r) {
                if ("string" == typeof n) {
                    var i = e[t];
                    if (v(i, n)) return i[n];
                    var o = Ki(n);
                    if (v(i, o)) return i[o];
                    var a = qi(o);
                    if (v(i, a)) return i[a];
                    var s = i[n] || i[o] || i[a];
                    return s
                }
            }

            function K(e, t, n, r) {
                var i = t[e],
                    o = !v(n, e),
                    a = n[e];
                if (Z(Boolean, i.type) && (o && !v(i, "default") ? a = !1 : Z(String, i.type) || "" !== a && a !== Zi(e) || (a = !0)), void 0 === a) {
                    a = q(r, i, e);
                    var s = Eo.shouldConvert;
                    Eo.shouldConvert = !0, I(a), Eo.shouldConvert = s
                }
                return a
            }

            function q(e, t, n) {
                if (v(t, "default")) {
                    var r = t["default"];
                    return e && e.$options.propsData && void 0 === e.$options.propsData[n] && void 0 !== e._props[n] ? e._props[n] : "function" == typeof r && "Function" !== W(t.type) ? r.call(e) : r
                }
            }

            function W(e) {
                var t = e && e.toString().match(/^\s*function (\w+)/);
                return t ? t[1] : ""
            }

            function Z(e, t) {
                if (!Array.isArray(t)) return W(t) === W(e);
                for (var n = 0, r = t.length; n < r; n++)
                    if (W(t[n]) === W(e)) return !0;
                return !1
            }

            function G(e) {
                return new Io(void 0, void 0, void 0, String(e))
            }

            function Y(e) {
                var t = new Io(e.tag, e.data, e.children, e.text, e.elm, e.context, e.componentOptions);
                return t.ns = e.ns, t.isStatic = e.isStatic, t.key = e.key, t.isComment = e.isComment, t.isCloned = !0, t
            }

            function Q(e) {
                for (var t = e.length, n = new Array(t), r = 0; r < t; r++) n[r] = Y(e[r]);
                return n
            }

            function X(e) {
                function t() {
                    var e = arguments,
                        n = t.fns;
                    if (!Array.isArray(n)) return n.apply(null, arguments);
                    for (var r = 0; r < n.length; r++) n[r].apply(null, e)
                }
                return t.fns = e, t
            }

            function ee(e, t, r, i, o) {
                var a, s, c, u;
                for (a in e) s = e[a], c = t[a], u = Ro(a), n(s) || (n(c) ? (n(s.fns) && (s = e[a] = X(s)), r(u.name, s, u.once, u.capture, u.passive)) : s !== c && (c.fns = s, e[a] = c));
                for (a in t) n(e[a]) && (u = Ro(a), i(u.name, t[a], u.capture))
            }

            function te(e, t, o) {
                function a() {
                    o.apply(this, arguments), d(s.fns, a)
                }
                var s, c = e[t];
                n(c) ? s = X([a]) : r(c.fns) && i(c.merged) ? (s = c, s.fns.push(a)) : s = X([c, a]), s.merged = !0, e[t] = s
            }

            function ne(e, t, i) {
                var o = t.options.props;
                if (!n(o)) {
                    var a = {},
                        s = e.attrs,
                        c = e.props;
                    if (r(s) || r(c))
                        for (var u in o) {
                            var l = Zi(u);
                            re(a, c, u, l, !0) || re(a, s, u, l, !1)
                        }
                    return a
                }
            }

            function re(e, t, n, i, o) {
                if (r(t)) {
                    if (v(t, n)) return e[n] = t[n], o || delete t[n], !0;
                    if (v(t, i)) return e[n] = t[i], o || delete t[i], !0
                }
                return !1
            }

            function ie(e) {
                for (var t = 0; t < e.length; t++)
                    if (Array.isArray(e[t])) return Array.prototype.concat.apply([], e);
                return e
            }

            function oe(e) {
                return a(e) ? [G(e)] : Array.isArray(e) ? se(e) : void 0
            }

            function ae(e) {
                return r(e) && r(e.text) && o(e.isComment)
            }

            function se(e, t) {
                var o, s, c, u = [];
                for (o = 0; o < e.length; o++) s = e[o], n(s) || "boolean" == typeof s || (c = u[u.length - 1], Array.isArray(s) ? u.push.apply(u, se(s, (t || "") + "_" + o)) : a(s) ? ae(c) ? c.text += String(s) : "" !== s && u.push(G(s)) : ae(s) && ae(c) ? u[u.length - 1] = G(c.text + s.text) : (i(e._isVList) && r(s.tag) && n(s.key) && r(t) && (s.key = "__vlist" + t + "_" + o + "__"), u.push(s)));
                return u
            }

            function ce(e, t) {
                return s(e) ? t.extend(e) : e
            }

            function ue(e, t, o) {
                if (i(e.error) && r(e.errorComp)) return e.errorComp;
                if (r(e.resolved)) return e.resolved;
                if (i(e.loading) && r(e.loadingComp)) return e.loadingComp;
                if (!r(e.contexts)) {
                    var a = e.contexts = [o],
                        c = !0,
                        u = function() {
                            for (var e = 0, t = a.length; e < t; e++) a[e].$forceUpdate()
                        },
                        l = C(function(n) {
                            e.resolved = ce(n, t), c || u()
                        }),
                        f = C(function(t) {
                            r(e.errorComp) && (e.error = !0, u())
                        }),
                        p = e(l, f);
                    return s(p) && ("function" == typeof p.then ? n(e.resolved) && p.then(l, f) : r(p.component) && "function" == typeof p.component.then && (p.component.then(l, f), r(p.error) && (e.errorComp = ce(p.error, t)), r(p.loading) && (e.loadingComp = ce(p.loading, t), 0 === p.delay ? e.loading = !0 : setTimeout(function() {
                        n(e.resolved) && n(e.error) && (e.loading = !0, u())
                    }, p.delay || 200)), r(p.timeout) && setTimeout(function() {
                        n(e.resolved) && f(null)
                    }, p.timeout))), c = !1, e.loading ? e.loadingComp : e.resolved
                }
                e.contexts.push(o)
            }

            function le(e) {
                if (Array.isArray(e))
                    for (var t = 0; t < e.length; t++) {
                        var n = e[t];
                        if (r(n) && r(n.componentOptions)) return n
                    }
            }

            function fe(e) {
                e._events = Object.create(null), e._hasHookEvent = !1;
                var t = e.$options._parentListeners;
                t && ve(e, t)
            }

            function pe(e, t, n) {
                n ? Mo.$once(e, t) : Mo.$on(e, t)
            }

            function de(e, t) {
                Mo.$off(e, t)
            }

            function ve(e, t, n) {
                Mo = e, ee(t, n || {}, pe, de, e)
            }

            function he(e) {
                var t = /^hook:/;
                e.prototype.$on = function(e, n) {
                    var r = this,
                        i = this;
                    if (Array.isArray(e))
                        for (var o = 0, a = e.length; o < a; o++) r.$on(e[o], n);
                    else(i._events[e] || (i._events[e] = [])).push(n), t.test(e) && (i._hasHookEvent = !0);
                    return i
                }, e.prototype.$once = function(e, t) {
                    function n() {
                        r.$off(e, n), t.apply(r, arguments)
                    }
                    var r = this;
                    return n.fn = t, r.$on(e, n), r
                }, e.prototype.$off = function(e, t) {
                    var n = this,
                        r = this;
                    if (!arguments.length) return r._events = Object.create(null), r;
                    if (Array.isArray(e)) {
                        for (var i = 0, o = e.length; i < o; i++) n.$off(e[i], t);
                        return r
                    }
                    var a = r._events[e];
                    if (!a) return r;
                    if (1 === arguments.length) return r._events[e] = null, r;
                    for (var s, c = a.length; c--;)
                        if (s = a[c], s === t || s.fn === t) {
                            a.splice(c, 1);
                            break
                        }
                    return r
                }, e.prototype.$emit = function(e) {
                    var t = this,
                        n = t._events[e];
                    if (n) {
                        n = n.length > 1 ? g(n) : n;
                        for (var r = g(arguments, 1), i = 0, o = n.length; i < o; i++) n[i].apply(t, r)
                    }
                    return t
                }
            }

            function me(e, t) {
                var n = {};
                if (!e) return n;
                for (var r = [], i = 0, o = e.length; i < o; i++) {
                    var a = e[i];
                    if (a.context !== t && a.functionalContext !== t || !a.data || null == a.data.slot) r.push(a);
                    else {
                        var s = a.data.slot,
                            c = n[s] || (n[s] = []);
                        "template" === a.tag ? c.push.apply(c, a.children) : c.push(a)
                    }
                }
                return r.every(ge) || (n["default"] = r), n
            }

            function ge(e) {
                return e.isComment || " " === e.text
            }

            function ye(e, t) {
                t = t || {};
                for (var n = 0; n < e.length; n++) Array.isArray(e[n]) ? ye(e[n], t) : t[e[n].key] = e[n].fn;
                return t
            }

            function _e(e) {
                var t = e.$options,
                    n = t.parent;
                if (n && !t["abstract"]) {
                    for (; n.$options["abstract"] && n.$parent;) n = n.$parent;
                    n.$children.push(e)
                }
                e.$parent = n, e.$root = n ? n.$root : e, e.$children = [], e.$refs = {}, e._watcher = null, e._inactive = null, e._directInactive = !1, e._isMounted = !1, e._isDestroyed = !1, e._isBeingDestroyed = !1
            }

            function be(e) {
                e.prototype._update = function(e, t) {
                    var n = this;
                    n._isMounted && Ae(n, "beforeUpdate");
                    var r = n.$el,
                        i = n._vnode,
                        o = Fo;
                    Fo = n, n._vnode = e, i ? n.$el = n.__patch__(i, e) : n.$el = n.__patch__(n.$el, e, t, !1, n.$options._parentElm, n.$options._refElm), Fo = o, r && (r.__vue__ = null), n.$el && (n.$el.__vue__ = n), n.$vnode && n.$parent && n.$vnode === n.$parent._vnode && (n.$parent.$el = n.$el)
                }, e.prototype.$forceUpdate = function() {
                    var e = this;
                    e._watcher && e._watcher.update()
                }, e.prototype.$destroy = function() {
                    var e = this;
                    if (!e._isBeingDestroyed) {
                        Ae(e, "beforeDestroy"), e._isBeingDestroyed = !0;
                        var t = e.$parent;
                        !t || t._isBeingDestroyed || e.$options["abstract"] || d(t.$children, e), e._watcher && e._watcher.teardown();
                        for (var n = e._watchers.length; n--;) e._watchers[n].teardown();
                        e._data.__ob__ && e._data.__ob__.vmCount--, e._isDestroyed = !0, e.__patch__(e._vnode, null), Ae(e, "destroyed"), e.$off(), e.$el && (e.$el.__vue__ = null), e.$options._parentElm = e.$options._refElm = null
                    }
                }
            }

            function $e(e, t, n) {
                e.$el = t, e.$options.render || (e.$options.render = Po), Ae(e, "beforeMount");
                var r;
                return r = function() {
                    e._update(e._render(), n)
                }, e._watcher = new qo(e, r, b), n = !1, null == e.$vnode && (e._isMounted = !0, Ae(e, "mounted")), e
            }

            function we(e, t, n, r, i) {
                var o = !!(i || e.$options._renderChildren || r.data.scopedSlots || e.$scopedSlots !== no);
                if (e.$options._parentVnode = r, e.$vnode = r, e._vnode && (e._vnode.parent = r), e.$options._renderChildren = i, t && e.$options.props) {
                    Eo.shouldConvert = !1;
                    for (var a = e._props, s = e.$options._propKeys || [], c = 0; c < s.length; c++) {
                        var u = s[c];
                        a[u] = K(u, e.$options.props, t, e)
                    }
                    Eo.shouldConvert = !0, e.$options.propsData = t
                }
                if (n) {
                    var l = e.$options._parentListeners;
                    e.$options._parentListeners = n, ve(e, n, l)
                }
                o && (e.$slots = me(i, r.context), e.$forceUpdate())
            }

            function xe(e) {
                for (; e && (e = e.$parent);)
                    if (e._inactive) return !0;
                return !1
            }

            function Ce(e, t) {
                if (t) {
                    if (e._directInactive = !1, xe(e)) return
                } else if (e._directInactive) return;
                if (e._inactive || null === e._inactive) {
                    e._inactive = !1;
                    for (var n = 0; n < e.$children.length; n++) Ce(e.$children[n]);
                    Ae(e, "activated")
                }
            }

            function ke(e, t) {
                if (!(t && (e._directInactive = !0, xe(e)) || e._inactive)) {
                    e._inactive = !0;
                    for (var n = 0; n < e.$children.length; n++) ke(e.$children[n]);
                    Ae(e, "deactivated")
                }
            }

            function Ae(e, t) {
                var n = e.$options[t];
                if (n)
                    for (var r = 0, i = n.length; r < i; r++) try {
                        n[r].call(e)
                    } catch (o) {
                        S(o, e, t + " hook")
                    }
                e._hasHookEvent && e.$emit("hook:" + t)
            }

            function Oe() {
                Jo = Bo.length = Ho.length = 0, Uo = {}, Vo = zo = !1
            }

            function Se() {
                zo = !0;
                var e, t;
                for (Bo.sort(function(e, t) {
                        return e.id - t.id
                    }), Jo = 0; Jo < Bo.length; Jo++) e = Bo[Jo], t = e.id, Uo[t] = null, e.run();
                var n = Ho.slice(),
                    r = Bo.slice();
                Oe(), je(n), Te(r), $o && to.devtools && $o.emit("flush")
            }

            function Te(e) {
                for (var t = e.length; t--;) {
                    var n = e[t],
                        r = n.vm;
                    r._watcher === n && r._isMounted && Ae(r, "updated")
                }
            }

            function Ee(e) {
                e._inactive = !1, Ho.push(e)
            }

            function je(e) {
                for (var t = 0; t < e.length; t++) e[t]._inactive = !0, Ce(e[t], !0)
            }

            function Ne(e) {
                var t = e.id;
                if (null == Uo[t]) {
                    if (Uo[t] = !0, zo) {
                        for (var n = Bo.length - 1; n > Jo && Bo[n].id > e.id;) n--;
                        Bo.splice(n + 1, 0, e)
                    } else Bo.push(e);
                    Vo || (Vo = !0, xo(Se))
                }
            }

            function Le(e) {
                Wo.clear(), Ie(e, Wo)
            }

            function Ie(e, t) {
                var n, r, i = Array.isArray(e);
                if ((i || s(e)) && Object.isExtensible(e)) {
                    if (e.__ob__) {
                        var o = e.__ob__.dep.id;
                        if (t.has(o)) return;
                        t.add(o)
                    }
                    if (i)
                        for (n = e.length; n--;) Ie(e[n], t);
                    else
                        for (r = Object.keys(e), n = r.length; n--;) Ie(e[r[n]], t)
                }
            }

            function De(e, t, n) {
                Zo.get = function() {
                    return this[t][n]
                }, Zo.set = function(e) {
                    this[t][n] = e
                }, Object.defineProperty(e, n, Zo)
            }

            function Me(e) {
                e._watchers = [];
                var t = e.$options;
                t.props && Pe(e, t.props), t.methods && Ve(e, t.methods), t.data ? Re(e) : I(e._data = {}, !0), t.computed && Be(e, t.computed), t.watch && ze(e, t.watch)
            }

            function Pe(e, t) {
                var n = e.$options.propsData || {},
                    r = e._props = {},
                    i = e.$options._propKeys = [],
                    o = !e.$parent;
                Eo.shouldConvert = o;
                var a = function(o) {
                    i.push(o);
                    var a = K(o, t, n, e);
                    D(r, o, a), o in e || De(e, "_props", o)
                };
                for (var s in t) a(s);
                Eo.shouldConvert = !0
            }

            function Re(e) {
                var t = e.$options.data;
                t = e._data = "function" == typeof t ? Fe(t, e) : t || {}, c(t) || (t = {});
                for (var n = Object.keys(t), r = e.$options.props, i = n.length; i--;) r && v(r, n[i]) || k(n[i]) || De(e, "_data", n[i]);
                I(t, !0)
            }

            function Fe(e, t) {
                try {
                    return e.call(t)
                } catch (n) {
                    return S(n, t, "data()"), {}
                }
            }

            function Be(e, t) {
                var n = e._computedWatchers = Object.create(null);
                for (var r in t) {
                    var i = t[r],
                        o = "function" == typeof i ? i : i.get;
                    n[r] = new qo(e, o, b, Go), r in e || He(e, r, i)
                }
            }

            function He(e, t, n) {
                "function" == typeof n ? (Zo.get = Ue(t), Zo.set = b) : (Zo.get = n.get ? n.cache !== !1 ? Ue(t) : n.get : b, Zo.set = n.set ? n.set : b), Object.defineProperty(e, t, Zo)
            }

            function Ue(e) {
                return function() {
                    var t = this._computedWatchers && this._computedWatchers[e];
                    if (t) return t.dirty && t.evaluate(), ko.target && t.depend(), t.value
                }
            }

            function Ve(e, t) {
                e.$options.props;
                for (var n in t) e[n] = null == t[n] ? b : m(t[n], e)
            }

            function ze(e, t) {
                for (var n in t) {
                    var r = t[n];
                    if (Array.isArray(r))
                        for (var i = 0; i < r.length; i++) Je(e, n, r[i]);
                    else Je(e, n, r)
                }
            }

            function Je(e, t, n) {
                var r;
                c(n) && (r = n, n = n.handler), "string" == typeof n && (n = e[n]), e.$watch(t, n, r)
            }

            function Ke(e) {
                var t = {};
                t.get = function() {
                    return this._data
                };
                var n = {};
                n.get = function() {
                    return this._props
                }, Object.defineProperty(e.prototype, "$data", t), Object.defineProperty(e.prototype, "$props", n), e.prototype.$set = M, e.prototype.$delete = P, e.prototype.$watch = function(e, t, n) {
                    var r = this;
                    n = n || {}, n.user = !0;
                    var i = new qo(r, e, t, n);
                    return n.immediate && t.call(r, i.value),
                        function() {
                            i.teardown()
                        }
                }
            }

            function qe(e) {
                var t = e.$options.provide;
                t && (e._provided = "function" == typeof t ? t.call(e) : t)
            }

            function We(e) {
                var t = Ze(e.$options.inject, e);
                t && Object.keys(t).forEach(function(n) {
                    D(e, n, t[n])
                })
            }

            function Ze(e, t) {
                if (e) {
                    for (var n = Array.isArray(e), r = Object.create(null), i = n ? e : wo ? Reflect.ownKeys(e) : Object.keys(e), o = 0; o < i.length; o++)
                        for (var a = i[o], s = n ? a : e[a], c = t; c;) {
                            if (c._provided && s in c._provided) {
                                r[a] = c._provided[s];
                                break
                            }
                            c = c.$parent
                        }
                    return r
                }
            }

            function Ge(e, t, n, i, o) {
                var a = {},
                    s = e.options.props;
                if (r(s))
                    for (var c in s) a[c] = K(c, s, t || {});
                else r(n.attrs) && Ye(a, n.attrs), r(n.props) && Ye(a, n.props);
                var u = Object.create(i),
                    l = function(e, t, n, r) {
                        return rt(u, e, t, n, r, !0)
                    },
                    f = e.options.render.call(null, l, {
                        data: n,
                        props: a,
                        children: o,
                        parent: i,
                        listeners: n.on || {},
                        injections: Ze(e.options.inject, i),
                        slots: function() {
                            return me(o, i)
                        }
                    });
                return f instanceof Io && (f.functionalContext = i, f.functionalOptions = e.options, n.slot && ((f.data || (f.data = {})).slot = n.slot)), f
            }

            function Ye(e, t) {
                for (var n in t) e[Ki(n)] = t[n]
            }

            function Qe(e, t, o, a, c) {
                if (!n(e)) {
                    var u = o.$options._base;
                    if (s(e) && (e = u.extend(e)), "function" == typeof e && (!n(e.cid) || (e = ue(e, u, o), void 0 !== e))) {
                        _t(e), t = t || {}, r(t.model) && nt(e.options, t);
                        var l = ne(t, e, c);
                        if (i(e.options.functional)) return Ge(e, l, t, o, a);
                        var f = t.on;
                        t.on = t.nativeOn, i(e.options["abstract"]) && (t = {}), et(t);
                        var p = e.options.name || c,
                            d = new Io("vue-component-" + e.cid + (p ? "-" + p : ""), t, void 0, void 0, void 0, o, {
                                Ctor: e,
                                propsData: l,
                                listeners: f,
                                tag: c,
                                children: a
                            });
                        return d
                    }
                }
            }

            function Xe(e, t, n, i) {
                var o = e.componentOptions,
                    a = {
                        _isComponent: !0,
                        parent: t,
                        propsData: o.propsData,
                        _componentTag: o.tag,
                        _parentVnode: e,
                        _parentListeners: o.listeners,
                        _renderChildren: o.children,
                        _parentElm: n || null,
                        _refElm: i || null
                    },
                    s = e.data.inlineTemplate;
                return r(s) && (a.render = s.render, a.staticRenderFns = s.staticRenderFns), new o.Ctor(a)
            }

            function et(e) {
                e.hook || (e.hook = {});
                for (var t = 0; t < Qo.length; t++) {
                    var n = Qo[t],
                        r = e.hook[n],
                        i = Yo[n];
                    e.hook[n] = r ? tt(i, r) : i
                }
            }

            function tt(e, t) {
                return function(n, r, i, o) {
                    e(n, r, i, o), t(n, r, i, o)
                }
            }

            function nt(e, t) {
                var n = e.model && e.model.prop || "value",
                    i = e.model && e.model.event || "input";
                (t.props || (t.props = {}))[n] = t.model.value;
                var o = t.on || (t.on = {});
                r(o[i]) ? o[i] = [t.model.callback].concat(o[i]) : o[i] = t.model.callback
            }

            function rt(e, t, n, r, o, s) {
                return (Array.isArray(n) || a(n)) && (o = r, r = n, n = void 0), i(s) && (o = ea), it(e, t, n, r, o)
            }

            function it(e, t, n, i, o) {
                if (r(n) && r(n.__ob__)) return Po();
                if (!t) return Po();
                Array.isArray(i) && "function" == typeof i[0] && (n = n || {}, n.scopedSlots = {
                    default: i[0]
                }, i.length = 0), o === ea ? i = oe(i) : o === Xo && (i = ie(i));
                var a, s;
                if ("string" == typeof t) {
                    var c;
                    s = to.getTagNamespace(t), a = to.isReservedTag(t) ? new Io(to.parsePlatformTagName(t), n, i, void 0, void 0, e) : r(c = J(e.$options, "components", t)) ? Qe(c, n, e, i, t) : new Io(t, n, i, void 0, void 0, e)
                } else a = Qe(t, n, e, i);
                return r(a) ? (s && ot(a, s), a) : Po()
            }

            function ot(e, t) {
                if (e.ns = t, "foreignObject" !== e.tag && r(e.children))
                    for (var i = 0, o = e.children.length; i < o; i++) {
                        var a = e.children[i];
                        r(a.tag) && n(a.ns) && ot(a, t)
                    }
            }

            function at(e, t) {
                var n, i, o, a, c;
                if (Array.isArray(e) || "string" == typeof e)
                    for (n = new Array(e.length), i = 0, o = e.length; i < o; i++) n[i] = t(e[i], i);
                else if ("number" == typeof e)
                    for (n = new Array(e), i = 0; i < e; i++) n[i] = t(i + 1, i);
                else if (s(e))
                    for (a = Object.keys(e), n = new Array(a.length), i = 0, o = a.length; i < o; i++) c = a[i], n[i] = t(e[c], c, i);
                return r(n) && (n._isVList = !0), n
            }

            function st(e, t, n, r) {
                var i = this.$scopedSlots[e];
                if (i) return n = n || {}, r && y(n, r), i(n) || t;
                var o = this.$slots[e];
                return o || t
            }

            function ct(e) {
                return J(this.$options, "filters", e, !0) || Yi
            }

            function ut(e, t, n) {
                var r = to.keyCodes[t] || n;
                return Array.isArray(r) ? r.indexOf(e) === -1 : r !== e
            }

            function lt(e, t, n, r) {
                if (n)
                    if (s(n)) {
                        Array.isArray(n) && (n = _(n));
                        var i;
                        for (var o in n) {
                            if ("class" === o || "style" === o) i = e;
                            else {
                                var a = e.attrs && e.attrs.type;
                                i = r || to.mustUseProp(t, a, o) ? e.domProps || (e.domProps = {}) : e.attrs || (e.attrs = {})
                            }
                            o in i || (i[o] = n[o])
                        }
                    } else;
                return e
            }

            function ft(e, t) {
                var n = this._staticTrees[e];
                return n && !t ? Array.isArray(n) ? Q(n) : Y(n) : (n = this._staticTrees[e] = this.$options.staticRenderFns[e].call(this._renderProxy), dt(n, "__static__" + e, !1), n)
            }

            function pt(e, t, n) {
                return dt(e, "__once__" + t + (n ? "_" + n : ""), !0), e
            }

            function dt(e, t, n) {
                if (Array.isArray(e))
                    for (var r = 0; r < e.length; r++) e[r] && "string" != typeof e[r] && vt(e[r], t + "_" + r, n);
                else vt(e, t, n)
            }

            function vt(e, t, n) {
                e.isStatic = !0, e.key = t, e.isOnce = n
            }

            function ht(e) {
                e._vnode = null, e._staticTrees = null;
                var t = e.$vnode = e.$options._parentVnode,
                    n = t && t.context;
                e.$slots = me(e.$options._renderChildren, n), e.$scopedSlots = no, e._c = function(t, n, r, i) {
                    return rt(e, t, n, r, i, !1)
                }, e.$createElement = function(t, n, r, i) {
                    return rt(e, t, n, r, i, !0)
                }
            }

            function mt(e) {
                e.prototype.$nextTick = function(e) {
                    return xo(e, this)
                }, e.prototype._render = function() {
                    var e = this,
                        t = e.$options,
                        n = t.render,
                        r = t.staticRenderFns,
                        i = t._parentVnode;
                    if (e._isMounted)
                        for (var o in e.$slots) e.$slots[o] = Q(e.$slots[o]);
                    e.$scopedSlots = i && i.data.scopedSlots || no, r && !e._staticTrees && (e._staticTrees = []), e.$vnode = i;
                    var a;
                    try {
                        a = n.call(e._renderProxy, e.$createElement)
                    } catch (s) {
                        S(s, e, "render function"), a = e._vnode
                    }
                    return a instanceof Io || (a = Po()), a.parent = i, a
                }, e.prototype._o = pt, e.prototype._n = f, e.prototype._s = l, e.prototype._l = at, e.prototype._t = st, e.prototype._q = w, e.prototype._i = x, e.prototype._m = ft, e.prototype._f = ct, e.prototype._k = ut, e.prototype._b = lt, e.prototype._v = G, e.prototype._e = Po, e.prototype._u = ye
            }

            function gt(e) {
                e.prototype._init = function(e) {
                    var t = this;
                    t._uid = ta++;
                    t._isVue = !0, e && e._isComponent ? yt(t, e) : t.$options = z(_t(t.constructor), e || {}, t), t._renderProxy = t, t._self = t, _e(t), fe(t), ht(t), Ae(t, "beforeCreate"), We(t), Me(t), qe(t), Ae(t, "created"), t.$options.el && t.$mount(t.$options.el)
                }
            }

            function yt(e, t) {
                var n = e.$options = Object.create(e.constructor.options);
                n.parent = t.parent, n.propsData = t.propsData, n._parentVnode = t._parentVnode, n._parentListeners = t._parentListeners, n._renderChildren = t._renderChildren, n._componentTag = t._componentTag, n._parentElm = t._parentElm, n._refElm = t._refElm, t.render && (n.render = t.render, n.staticRenderFns = t.staticRenderFns)
            }

            function _t(e) {
                var t = e.options;
                if (e["super"]) {
                    var n = _t(e["super"]),
                        r = e.superOptions;
                    if (n !== r) {
                        e.superOptions = n;
                        var i = bt(e);
                        i && y(e.extendOptions, i), t = e.options = z(n, e.extendOptions), t.name && (t.components[t.name] = e)
                    }
                }
                return t
            }

            function bt(e) {
                var t, n = e.options,
                    r = e.extendOptions,
                    i = e.sealedOptions;
                for (var o in n) n[o] !== i[o] && (t || (t = {}), t[o] = $t(n[o], r[o], i[o]));
                return t
            }

            function $t(e, t, n) {
                if (Array.isArray(e)) {
                    var r = [];
                    n = Array.isArray(n) ? n : [n], t = Array.isArray(t) ? t : [t];
                    for (var i = 0; i < e.length; i++)(t.indexOf(e[i]) >= 0 || n.indexOf(e[i]) < 0) && r.push(e[i]);
                    return r
                }
                return e
            }

            function wt(e) {
                this._init(e)
            }

            function xt(e) {
                e.use = function(e) {
                    if (e.installed) return this;
                    var t = g(arguments, 1);
                    return t.unshift(this), "function" == typeof e.install ? e.install.apply(e, t) : "function" == typeof e && e.apply(null, t), e.installed = !0, this
                }
            }

            function Ct(e) {
                e.mixin = function(e) {
                    return this.options = z(this.options, e), this
                }
            }

            function kt(e) {
                e.cid = 0;
                var t = 1;
                e.extend = function(e) {
                    e = e || {};
                    var n = this,
                        r = n.cid,
                        i = e._Ctor || (e._Ctor = {});
                    if (i[r]) return i[r];
                    var o = e.name || n.options.name,
                        a = function(e) {
                            this._init(e)
                        };
                    return a.prototype = Object.create(n.prototype), a.prototype.constructor = a, a.cid = t++, a.options = z(n.options, e), a["super"] = n, a.options.props && At(a), a.options.computed && Ot(a), a.extend = n.extend, a.mixin = n.mixin, a.use = n.use, Xi.forEach(function(e) {
                        a[e] = n[e]
                    }), o && (a.options.components[o] = a), a.superOptions = n.options, a.extendOptions = e, a.sealedOptions = y({}, a.options), i[r] = a, a
                }
            }

            function At(e) {
                var t = e.options.props;
                for (var n in t) De(e.prototype, "_props", n)
            }

            function Ot(e) {
                var t = e.options.computed;
                for (var n in t) He(e.prototype, n, t[n])
            }

            function St(e) {
                Xi.forEach(function(t) {
                    e[t] = function(e, n) {
                        return n ? ("component" === t && c(n) && (n.name = n.name || e, n = this.options._base.extend(n)), "directive" === t && "function" == typeof n && (n = {
                            bind: n,
                            update: n
                        }), this.options[t + "s"][e] = n, n) : this.options[t + "s"][e]
                    }
                })
            }

            function Tt(e) {
                return e && (e.Ctor.options.name || e.tag)
            }

            function Et(e, t) {
                return "string" == typeof e ? e.split(",").indexOf(t) > -1 : !!u(e) && e.test(t)
            }

            function jt(e, t, n) {
                for (var r in e) {
                    var i = e[r];
                    if (i) {
                        var o = Tt(i.componentOptions);
                        o && !n(o) && (i !== t && Nt(i), e[r] = null)
                    }
                }
            }

            function Nt(e) {
                e && e.componentInstance.$destroy()
            }

            function Lt(e) {
                var t = {};
                t.get = function() {
                    return to
                }, Object.defineProperty(e, "config", t), e.util = {
                    warn: io,
                    extend: y,
                    mergeOptions: z,
                    defineReactive: D
                }, e.set = M, e["delete"] = P, e.nextTick = xo, e.options = Object.create(null), Xi.forEach(function(t) {
                    e.options[t + "s"] = Object.create(null)
                }), e.options._base = e, y(e.options.components, ia), xt(e), Ct(e), kt(e), St(e)
            }

            function It(e) {
                for (var t = e.data, n = e, i = e; r(i.componentInstance);) i = i.componentInstance._vnode, i.data && (t = Dt(i.data, t));
                for (; r(n = n.parent);) n.data && (t = Dt(t, n.data));
                return Mt(t)
            }

            function Dt(e, t) {
                return {
                    staticClass: Pt(e.staticClass, t.staticClass),
                    class: r(e["class"]) ? [e["class"], t["class"]] : t["class"]
                }
            }

            function Mt(e) {
                var t = e["class"],
                    n = e.staticClass;
                return r(n) || r(t) ? Pt(n, Rt(t)) : ""
            }

            function Pt(e, t) {
                return e ? t ? e + " " + t : e : t || ""
            }

            function Rt(e) {
                if (n(e)) return "";
                if ("string" == typeof e) return e;
                var t = "";
                if (Array.isArray(e)) {
                    for (var i, o = 0, a = e.length; o < a; o++) r(e[o]) && r(i = Rt(e[o])) && "" !== i && (t += i + " ");
                    return t.slice(0, -1)
                }
                if (s(e)) {
                    for (var c in e) e[c] && (t += c + " ");
                    return t.slice(0, -1)
                }
                return t
            }

            function Ft(e) {
                return ka(e) ? "svg" : "math" === e ? "math" : void 0
            }

            function Bt(e) {
                if (!ao) return !0;
                if (Oa(e)) return !1;
                if (e = e.toLowerCase(), null != Sa[e]) return Sa[e];
                var t = document.createElement(e);
                return e.indexOf("-") > -1 ? Sa[e] = t.constructor === window.HTMLUnknownElement || t.constructor === window.HTMLElement : Sa[e] = /HTMLUnknownElement/.test(t.toString())
            }

            function Ht(e) {
                if ("string" == typeof e) {
                    var t = document.querySelector(e);
                    return t ? t : document.createElement("div")
                }
                return e
            }

            function Ut(e, t) {
                var n = document.createElement(e);
                return "select" !== e ? n : (t.data && t.data.attrs && void 0 !== t.data.attrs.multiple && n.setAttribute("multiple", "multiple"), n)
            }

            function Vt(e, t) {
                return document.createElementNS(xa[e], t)
            }

            function zt(e) {
                return document.createTextNode(e)
            }

            function Jt(e) {
                return document.createComment(e)
            }

            function Kt(e, t, n) {
                e.insertBefore(t, n)
            }

            function qt(e, t) {
                e.removeChild(t)
            }

            function Wt(e, t) {
                e.appendChild(t)
            }

            function Zt(e) {
                return e.parentNode
            }

            function Gt(e) {
                return e.nextSibling
            }

            function Yt(e) {
                return e.tagName
            }

            function Qt(e, t) {
                e.textContent = t
            }

            function Xt(e, t, n) {
                e.setAttribute(t, n)
            }

            function en(e, t) {
                var n = e.data.ref;
                if (n) {
                    var r = e.context,
                        i = e.componentInstance || e.elm,
                        o = r.$refs;
                    t ? Array.isArray(o[n]) ? d(o[n], i) : o[n] === i && (o[n] = void 0) : e.data.refInFor ? Array.isArray(o[n]) && o[n].indexOf(i) < 0 ? o[n].push(i) : o[n] = [i] : o[n] = i
                }
            }

            function tn(e, t) {
                return e.key === t.key && e.tag === t.tag && e.isComment === t.isComment && r(e.data) === r(t.data) && nn(e, t)
            }

            function nn(e, t) {
                if ("input" !== e.tag) return !0;
                var n, i = r(n = e.data) && r(n = n.attrs) && n.type,
                    o = r(n = t.data) && r(n = n.attrs) && n.type;
                return i === o
            }

            function rn(e, t, n) {
                var i, o, a = {};
                for (i = t; i <= n; ++i) o = e[i].key, r(o) && (a[o] = i);
                return a
            }

            function on(e) {
                function t(e) {
                    return new Io(E.tagName(e).toLowerCase(), {}, [], void 0, e)
                }

                function o(e, t) {
                    function n() {
                        0 === --n.listeners && s(e)
                    }
                    return n.listeners = t, n
                }

                function s(e) {
                    var t = E.parentNode(e);
                    r(t) && E.removeChild(t, e)
                }

                function c(e, t, n, o, a) {
                    if (e.isRootInsert = !a, !u(e, t, n, o)) {
                        var s = e.data,
                            c = e.children,
                            l = e.tag;
                        r(l) ? (e.elm = e.ns ? E.createElementNS(e.ns, l) : E.createElement(l, e), g(e), v(e, c, t), r(s) && m(e, t), d(n, e.elm, o)) : i(e.isComment) ? (e.elm = E.createComment(e.text), d(n, e.elm, o)) : (e.elm = E.createTextNode(e.text), d(n, e.elm, o))
                    }
                }

                function u(e, t, n, o) {
                    var a = e.data;
                    if (r(a)) {
                        var s = r(e.componentInstance) && a.keepAlive;
                        if (r(a = a.hook) && r(a = a.init) && a(e, !1, n, o), r(e.componentInstance)) return l(e, t), i(s) && f(e, t, n, o), !0
                    }
                }

                function l(e, t) {
                    r(e.data.pendingInsert) && t.push.apply(t, e.data.pendingInsert), e.elm = e.componentInstance.$el, h(e) ? (m(e, t), g(e)) : (en(e), t.push(e))
                }

                function f(e, t, n, i) {
                    for (var o, a = e; a.componentInstance;)
                        if (a = a.componentInstance._vnode, r(o = a.data) && r(o = o.transition)) {
                            for (o = 0; o < S.activate.length; ++o) S.activate[o](ja, a);
                            t.push(a);
                            break
                        }
                    d(n, e.elm, i)
                }

                function d(e, t, n) {
                    r(e) && (r(n) ? n.parentNode === e && E.insertBefore(e, t, n) : E.appendChild(e, t))
                }

                function v(e, t, n) {
                    if (Array.isArray(t))
                        for (var r = 0; r < t.length; ++r) c(t[r], n, e.elm, null, !0);
                    else a(e.text) && E.appendChild(e.elm, E.createTextNode(e.text))
                }

                function h(e) {
                    for (; e.componentInstance;) e = e.componentInstance._vnode;
                    return r(e.tag)
                }

                function m(e, t) {
                    for (var n = 0; n < S.create.length; ++n) S.create[n](ja, e);
                    A = e.data.hook, r(A) && (r(A.create) && A.create(ja, e), r(A.insert) && t.push(e))
                }

                function g(e) {
                    for (var t, n = e; n;) r(t = n.context) && r(t = t.$options._scopeId) && E.setAttribute(e.elm, t, ""), n = n.parent;
                    r(t = Fo) && t !== e.context && r(t = t.$options._scopeId) && E.setAttribute(e.elm, t, "")
                }

                function y(e, t, n, r, i, o) {
                    for (; r <= i; ++r) c(n[r], o, e, t)
                }

                function _(e) {
                    var t, n, i = e.data;
                    if (r(i))
                        for (r(t = i.hook) && r(t = t.destroy) && t(e), t = 0; t < S.destroy.length; ++t) S.destroy[t](e);
                    if (r(t = e.children))
                        for (n = 0; n < e.children.length; ++n) _(e.children[n])
                }

                function b(e, t, n, i) {
                    for (; n <= i; ++n) {
                        var o = t[n];
                        r(o) && (r(o.tag) ? ($(o), _(o)) : s(o.elm))
                    }
                }

                function $(e, t) {
                    if (r(t) || r(e.data)) {
                        var n, i = S.remove.length + 1;
                        for (r(t) ? t.listeners += i : t = o(e.elm, i), r(n = e.componentInstance) && r(n = n._vnode) && r(n.data) && $(n, t), n = 0; n < S.remove.length; ++n) S.remove[n](e, t);
                        r(n = e.data.hook) && r(n = n.remove) ? n(e, t) : t()
                    } else s(e.elm)
                }

                function w(e, t, i, o, a) {
                    for (var s, u, l, f, p = 0, d = 0, v = t.length - 1, h = t[0], m = t[v], g = i.length - 1, _ = i[0], $ = i[g], w = !a; p <= v && d <= g;) n(h) ? h = t[++p] : n(m) ? m = t[--v] : tn(h, _) ? (x(h, _, o), h = t[++p], _ = i[++d]) : tn(m, $) ? (x(m, $, o), m = t[--v], $ = i[--g]) : tn(h, $) ? (x(h, $, o), w && E.insertBefore(e, h.elm, E.nextSibling(m.elm)), h = t[++p], $ = i[--g]) : tn(m, _) ? (x(m, _, o), w && E.insertBefore(e, m.elm, h.elm), m = t[--v], _ = i[++d]) : (n(s) && (s = rn(t, p, v)), u = r(_.key) ? s[_.key] : null, n(u) ? (c(_, o, e, h.elm), _ = i[++d]) : (l = t[u], tn(l, _) ? (x(l, _, o), t[u] = void 0, w && E.insertBefore(e, _.elm, h.elm), _ = i[++d]) : (c(_, o, e, h.elm), _ = i[++d])));
                    p > v ? (f = n(i[g + 1]) ? null : i[g + 1].elm, y(e, f, i, d, g, o)) : d > g && b(e, t, p, v)
                }

                function x(e, t, o, a) {
                    if (e !== t) {
                        if (i(t.isStatic) && i(e.isStatic) && t.key === e.key && (i(t.isCloned) || i(t.isOnce))) return t.elm = e.elm, void(t.componentInstance = e.componentInstance);
                        var s, c = t.data;
                        r(c) && r(s = c.hook) && r(s = s.prepatch) && s(e, t);
                        var u = t.elm = e.elm,
                            l = e.children,
                            f = t.children;
                        if (r(c) && h(t)) {
                            for (s = 0; s < S.update.length; ++s) S.update[s](e, t);
                            r(s = c.hook) && r(s = s.update) && s(e, t)
                        }
                        n(t.text) ? r(l) && r(f) ? l !== f && w(u, l, f, o, a) : r(f) ? (r(e.text) && E.setTextContent(u, ""), y(u, null, f, 0, f.length - 1, o)) : r(l) ? b(u, l, 0, l.length - 1) : r(e.text) && E.setTextContent(u, "") : e.text !== t.text && E.setTextContent(u, t.text), r(c) && r(s = c.hook) && r(s = s.postpatch) && s(e, t)
                    }
                }

                function C(e, t, n) {
                    if (i(n) && r(e.parent)) e.parent.data.pendingInsert = t;
                    else
                        for (var o = 0; o < t.length; ++o) t[o].data.hook.insert(t[o])
                }

                function k(e, t, n) {
                    t.elm = e;
                    var i = t.tag,
                        o = t.data,
                        a = t.children;
                    if (r(o) && (r(A = o.hook) && r(A = A.init) && A(t, !0), r(A = t.componentInstance))) return l(t, n), !0;
                    if (r(i)) {
                        if (r(a))
                            if (e.hasChildNodes()) {
                                for (var s = !0, c = e.firstChild, u = 0; u < a.length; u++) {
                                    if (!c || !k(c, a[u], n)) {
                                        s = !1;
                                        break
                                    }
                                    c = c.nextSibling
                                }
                                if (!s || c) return !1
                            } else v(t, a, n);
                        if (r(o))
                            for (var f in o)
                                if (!j(f)) {
                                    m(t, n);
                                    break
                                }
                    } else e.data !== t.text && (e.data = t.text);
                    return !0
                }
                var A, O, S = {},
                    T = e.modules,
                    E = e.nodeOps;
                for (A = 0; A < Na.length; ++A)
                    for (S[Na[A]] = [], O = 0; O < T.length; ++O) r(T[O][Na[A]]) && S[Na[A]].push(T[O][Na[A]]);
                var j = p("attrs,style,class,staticClass,staticStyle,key");
                return function(e, o, a, s, u, l) {
                    if (n(o)) return void(r(e) && _(e));
                    var f = !1,
                        p = [];
                    if (n(e)) f = !0, c(o, p, u, l);
                    else {
                        var d = r(e.nodeType);
                        if (!d && tn(e, o)) x(e, o, p, s);
                        else {
                            if (d) {
                                if (1 === e.nodeType && e.hasAttribute(Qi) && (e.removeAttribute(Qi), a = !0), i(a) && k(e, o, p)) return C(o, p, !0), e;
                                e = t(e)
                            }
                            var v = e.elm,
                                m = E.parentNode(v);
                            if (c(o, p, v._leaveCb ? null : m, E.nextSibling(v)), r(o.parent)) {
                                for (var g = o.parent; g;) g.elm = o.elm, g = g.parent;
                                if (h(o))
                                    for (var y = 0; y < S.create.length; ++y) S.create[y](ja, o.parent)
                            }
                            r(m) ? b(m, [e], 0, 0) : r(e.tag) && _(e)
                        }
                    }
                    return C(o, p, f), o.elm
                }
            }

            function an(e, t) {
                (e.data.directives || t.data.directives) && sn(e, t)
            }

            function sn(e, t) {
                var n, r, i, o = e === ja,
                    a = t === ja,
                    s = cn(e.data.directives, e.context),
                    c = cn(t.data.directives, t.context),
                    u = [],
                    l = [];
                for (n in c) r = s[n], i = c[n], r ? (i.oldValue = r.value, ln(i, "update", t, e), i.def && i.def.componentUpdated && l.push(i)) : (ln(i, "bind", t, e), i.def && i.def.inserted && u.push(i));
                if (u.length) {
                    var f = function() {
                        for (var n = 0; n < u.length; n++) ln(u[n], "inserted", t, e)
                    };
                    o ? te(t.data.hook || (t.data.hook = {}), "insert", f) : f()
                }
                if (l.length && te(t.data.hook || (t.data.hook = {}), "postpatch", function() {
                        for (var n = 0; n < l.length; n++) ln(l[n], "componentUpdated", t, e)
                    }), !o)
                    for (n in s) c[n] || ln(s[n], "unbind", e, e, a)
            }

            function cn(e, t) {
                var n = Object.create(null);
                if (!e) return n;
                var r, i;
                for (r = 0; r < e.length; r++) i = e[r], i.modifiers || (i.modifiers = Ia), n[un(i)] = i, i.def = J(t.$options, "directives", i.name, !0);
                return n
            }

            function un(e) {
                return e.rawName || e.name + "." + Object.keys(e.modifiers || {}).join(".")
            }

            function ln(e, t, n, r, i) {
                var o = e.def && e.def[t];
                if (o) try {
                    o(n.elm, e, n, r, i)
                } catch (a) {
                    S(a, n.context, "directive " + e.name + " " + t + " hook")
                }
            }

            function fn(e, t) {
                if (!n(e.data.attrs) || !n(t.data.attrs)) {
                    var i, o, a, s = t.elm,
                        c = e.data.attrs || {},
                        u = t.data.attrs || {};
                    r(u.__ob__) && (u = t.data.attrs = y({}, u));
                    for (i in u) o = u[i], a = c[i], a !== o && pn(s, i, o);
                    uo && u.value !== c.value && pn(s, "value", u.value);
                    for (i in c) n(u[i]) && (ba(i) ? s.removeAttributeNS(_a, $a(i)) : ga(i) || s.removeAttribute(i))
                }
            }

            function pn(e, t, n) {
                ya(t) ? wa(n) ? e.removeAttribute(t) : e.setAttribute(t, t) : ga(t) ? e.setAttribute(t, wa(n) || "false" === n ? "false" : "true") : ba(t) ? wa(n) ? e.removeAttributeNS(_a, $a(t)) : e.setAttributeNS(_a, t, n) : wa(n) ? e.removeAttribute(t) : e.setAttribute(t, n)
            }

            function dn(e, t) {
                var i = t.elm,
                    o = t.data,
                    a = e.data;
                if (!(n(o.staticClass) && n(o["class"]) && (n(a) || n(a.staticClass) && n(a["class"])))) {
                    var s = It(t),
                        c = i._transitionClasses;
                    r(c) && (s = Pt(s, Rt(c))), s !== i._prevClass && (i.setAttribute("class", s), i._prevClass = s)
                }
            }

            function vn(e) {
                function t() {
                    (a || (a = [])).push(e.slice(v, i).trim()), v = i + 1
                }
                var n, r, i, o, a, s = !1,
                    c = !1,
                    u = !1,
                    l = !1,
                    f = 0,
                    p = 0,
                    d = 0,
                    v = 0;
                for (i = 0; i < e.length; i++)
                    if (r = n, n = e.charCodeAt(i), s) 39 === n && 92 !== r && (s = !1);
                    else if (c) 34 === n && 92 !== r && (c = !1);
                else if (u) 96 === n && 92 !== r && (u = !1);
                else if (l) 47 === n && 92 !== r && (l = !1);
                else if (124 !== n || 124 === e.charCodeAt(i + 1) || 124 === e.charCodeAt(i - 1) || f || p || d) {
                    switch (n) {
                        case 34:
                            c = !0;
                            break;
                        case 39:
                            s = !0;
                            break;
                        case 96:
                            u = !0;
                            break;
                        case 40:
                            d++;
                            break;
                        case 41:
                            d--;
                            break;
                        case 91:
                            p++;
                            break;
                        case 93:
                            p--;
                            break;
                        case 123:
                            f++;
                            break;
                        case 125:
                            f--
                    }
                    if (47 === n) {
                        for (var h = i - 1, m = void 0; h >= 0 && (m = e.charAt(h), " " === m); h--);
                        m && Ra.test(m) || (l = !0)
                    }
                } else void 0 === o ? (v = i + 1, o = e.slice(0, i).trim()) : t();
                if (void 0 === o ? o = e.slice(0, i).trim() : 0 !== v && t(), a)
                    for (i = 0; i < a.length; i++) o = hn(o, a[i]);
                return o
            }

            function hn(e, t) {
                var n = t.indexOf("(");
                if (n < 0) return '_f("' + t + '")(' + e + ")";
                var r = t.slice(0, n),
                    i = t.slice(n + 1);
                return '_f("' + r + '")(' + e + "," + i
            }

            function mn(e) {
                console.error("[Vue compiler]: " + e)
            }

            function gn(e, t) {
                return e ? e.map(function(e) {
                    return e[t]
                }).filter(function(e) {
                    return e
                }) : []
            }

            function yn(e, t, n) {
                (e.props || (e.props = [])).push({
                    name: t,
                    value: n
                })
            }

            function _n(e, t, n) {
                (e.attrs || (e.attrs = [])).push({
                    name: t,
                    value: n
                })
            }

            function bn(e, t, n, r, i, o) {
                (e.directives || (e.directives = [])).push({
                    name: t,
                    rawName: n,
                    value: r,
                    arg: i,
                    modifiers: o
                })
            }

            function $n(e, t, n, r, i, o) {
                r && r.capture && (delete r.capture, t = "!" + t), r && r.once && (delete r.once, t = "~" + t), r && r.passive && (delete r.passive, t = "&" + t);
                var a;
                r && r["native"] ? (delete r["native"], a = e.nativeEvents || (e.nativeEvents = {})) : a = e.events || (e.events = {});
                var s = {
                        value: n,
                        modifiers: r
                    },
                    c = a[t];
                Array.isArray(c) ? i ? c.unshift(s) : c.push(s) : c ? a[t] = i ? [s, c] : [c, s] : a[t] = s
            }

            function wn(e, t, n) {
                var r = xn(e, ":" + t) || xn(e, "v-bind:" + t);
                if (null != r) return vn(r);
                if (n !== !1) {
                    var i = xn(e, t);
                    if (null != i) return JSON.stringify(i)
                }
            }

            function xn(e, t) {
                var n;
                if (null != (n = e.attrsMap[t]))
                    for (var r = e.attrsList, i = 0, o = r.length; i < o; i++)
                        if (r[i].name === t) {
                            r.splice(i, 1);
                            break
                        }
                return n
            }

            function Cn(e, t, n) {
                var r = n || {},
                    i = r.number,
                    o = r.trim,
                    a = "$$v",
                    s = a;
                o && (s = "(typeof " + a + " === 'string'? " + a + ".trim(): " + a + ")"), i && (s = "_n(" + s + ")");
                var c = kn(t, s);
                e.model = {
                    value: "(" + t + ")",
                    expression: '"' + t + '"',
                    callback: "function (" + a + ") {" + c + "}"
                }
            }

            function kn(e, t) {
                var n = An(e);
                return null === n.idx ? e + "=" + t : "var $$exp = " + n.exp + ", $$idx = " + n.idx + ";if (!Array.isArray($$exp)){" + e + "=" + t + "}else{$$exp.splice($$idx, 1, " + t + ")}"
            }

            function An(e) {
                if (aa = e, oa = aa.length, ca = ua = la = 0, e.indexOf("[") < 0 || e.lastIndexOf("]") < oa - 1) return {
                    exp: e,
                    idx: null
                };
                for (; !Sn();) sa = On(), Tn(sa) ? jn(sa) : 91 === sa && En(sa);
                return {
                    exp: e.substring(0, ua),
                    idx: e.substring(ua + 1, la)
                }
            }

            function On() {
                return aa.charCodeAt(++ca)
            }

            function Sn() {
                return ca >= oa
            }

            function Tn(e) {
                return 34 === e || 39 === e
            }

            function En(e) {
                var t = 1;
                for (ua = ca; !Sn();)
                    if (e = On(), Tn(e)) jn(e);
                    else if (91 === e && t++, 93 === e && t--, 0 === t) {
                    la = ca;
                    break
                }
            }

            function jn(e) {
                for (var t = e; !Sn() && (e = On(), e !== t););
            }

            function Nn(e, t, n) {
                fa = n;
                var r = t.value,
                    i = t.modifiers,
                    o = e.tag,
                    a = e.attrsMap.type;
                if ("select" === o) Dn(e, r, i);
                else if ("input" === o && "checkbox" === a) Ln(e, r, i);
                else if ("input" === o && "radio" === a) In(e, r, i);
                else if ("input" === o || "textarea" === o) Mn(e, r, i);
                else if (!to.isReservedTag(o)) return Cn(e, r, i), !1;
                return !0
            }

            function Ln(e, t, n) {
                var r = n && n.number,
                    i = wn(e, "value") || "null",
                    o = wn(e, "true-value") || "true",
                    a = wn(e, "false-value") || "false";
                yn(e, "checked", "Array.isArray(" + t + ")?_i(" + t + "," + i + ")>-1" + ("true" === o ? ":(" + t + ")" : ":_q(" + t + "," + o + ")")), $n(e, Ba, "var $$a=" + t + ",$$el=$event.target,$$c=$$el.checked?(" + o + "):(" + a + ");if(Array.isArray($$a)){var $$v=" + (r ? "_n(" + i + ")" : i) + ",$$i=_i($$a,$$v);if($$c){$$i<0&&(" + t + "=$$a.concat($$v))}else{$$i>-1&&(" + t + "=$$a.slice(0,$$i).concat($$a.slice($$i+1)))}}else{" + kn(t, "$$c") + "}", null, !0)
            }

            function In(e, t, n) {
                var r = n && n.number,
                    i = wn(e, "value") || "null";
                i = r ? "_n(" + i + ")" : i, yn(e, "checked", "_q(" + t + "," + i + ")"), $n(e, Ba, kn(t, i), null, !0)
            }

            function Dn(e, t, n) {
                var r = n && n.number,
                    i = 'Array.prototype.filter.call($event.target.options,function(o){return o.selected}).map(function(o){var val = "_value" in o ? o._value : o.value;return ' + (r ? "_n(val)" : "val") + "})",
                    o = "$event.target.multiple ? $$selectedVal : $$selectedVal[0]",
                    a = "var $$selectedVal = " + i + ";";
                a = a + " " + kn(t, o), $n(e, "change", a, null, !0)
            }

            function Mn(e, t, n) {
                var r = e.attrsMap.type,
                    i = n || {},
                    o = i.lazy,
                    a = i.number,
                    s = i.trim,
                    c = !o && "range" !== r,
                    u = o ? "change" : "range" === r ? Fa : "input",
                    l = "$event.target.value";
                s && (l = "$event.target.value.trim()"), a && (l = "_n(" + l + ")");
                var f = kn(t, l);
                c && (f = "if($event.target.composing)return;" + f), yn(e, "value", "(" + t + ")"), $n(e, u, f, null, !0), (s || a || "number" === r) && $n(e, "blur", "$forceUpdate()")
            }

            function Pn(e) {
                var t;
                r(e[Fa]) && (t = co ? "change" : "input", e[t] = [].concat(e[Fa], e[t] || []), delete e[Fa]), r(e[Ba]) && (t = vo ? "click" : "change", e[t] = [].concat(e[Ba], e[t] || []), delete e[Ba])
            }

            function Rn(e, t, n, r, i) {
                if (n) {
                    var o = t,
                        a = pa;
                    t = function(n) {
                        var i = 1 === arguments.length ? o(n) : o.apply(null, arguments);
                        null !== i && Fn(e, t, r, a)
                    }
                }
                pa.addEventListener(e, t, ho ? {
                    capture: r,
                    passive: i
                } : r)
            }

            function Fn(e, t, n, r) {
                (r || pa).removeEventListener(e, t, n)
            }

            function Bn(e, t) {
                if (!n(e.data.on) || !n(t.data.on)) {
                    var r = t.data.on || {},
                        i = e.data.on || {};
                    pa = t.elm, Pn(r), ee(r, i, Rn, Fn, t.context)
                }
            }

            function Hn(e, t) {
                if (!n(e.data.domProps) || !n(t.data.domProps)) {
                    var i, o, a = t.elm,
                        s = e.data.domProps || {},
                        c = t.data.domProps || {};
                    r(c.__ob__) && (c = t.data.domProps = y({}, c));
                    for (i in s) n(c[i]) && (a[i] = "");
                    for (i in c)
                        if (o = c[i], "textContent" !== i && "innerHTML" !== i || (t.children && (t.children.length = 0), o !== s[i]))
                            if ("value" === i) {
                                a._value = o;
                                var u = n(o) ? "" : String(o);
                                Un(a, t, u) && (a.value = u)
                            } else a[i] = o
                }
            }

            function Un(e, t, n) {
                return !e.composing && ("option" === t.tag || Vn(e, n) || zn(e, n))
            }

            function Vn(e, t) {
                return document.activeElement !== e && e.value !== t
            }

            function zn(e, t) {
                var n = e.value,
                    i = e._vModifiers;
                return r(i) && i.number || "number" === e.type ? f(n) !== f(t) : r(i) && i.trim ? n.trim() !== t.trim() : n !== t
            }

            function Jn(e) {
                var t = Kn(e.style);
                return e.staticStyle ? y(e.staticStyle, t) : t
            }

            function Kn(e) {
                return Array.isArray(e) ? _(e) : "string" == typeof e ? Va(e) : e
            }

            function qn(e, t) {
                var n, r = {};
                if (t)
                    for (var i = e; i.componentInstance;) i = i.componentInstance._vnode, i.data && (n = Jn(i.data)) && y(r, n);
                (n = Jn(e.data)) && y(r, n);
                for (var o = e; o = o.parent;) o.data && (n = Jn(o.data)) && y(r, n);
                return r
            }

            function Wn(e, t) {
                var i = t.data,
                    o = e.data;
                if (!(n(i.staticStyle) && n(i.style) && n(o.staticStyle) && n(o.style))) {
                    var a, s, c = t.elm,
                        u = o.staticStyle,
                        l = o.normalizedStyle || o.style || {},
                        f = u || l,
                        p = Kn(t.data.style) || {};
                    t.data.normalizedStyle = r(p.__ob__) ? y({}, p) : p;
                    var d = qn(t, !0);
                    for (s in f) n(d[s]) && Ka(c, s, "");
                    for (s in d) a = d[s], a !== f[s] && Ka(c, s, null == a ? "" : a)
                }
            }

            function Zn(e, t) {
                if (t && (t = t.trim()))
                    if (e.classList) t.indexOf(" ") > -1 ? t.split(/\s+/).forEach(function(t) {
                        return e.classList.add(t)
                    }) : e.classList.add(t);
                    else {
                        var n = " " + (e.getAttribute("class") || "") + " ";
                        n.indexOf(" " + t + " ") < 0 && e.setAttribute("class", (n + t).trim())
                    }
            }

            function Gn(e, t) {
                if (t && (t = t.trim()))
                    if (e.classList) t.indexOf(" ") > -1 ? t.split(/\s+/).forEach(function(t) {
                        return e.classList.remove(t)
                    }) : e.classList.remove(t);
                    else {
                        for (var n = " " + (e.getAttribute("class") || "") + " ", r = " " + t + " "; n.indexOf(r) >= 0;) n = n.replace(r, " ");
                        e.setAttribute("class", n.trim())
                    }
            }

            function Yn(e) {
                if (e) {
                    if ("object" === ("undefined" == typeof e ? "undefined" : Hi(e))) {
                        var t = {};
                        return e.css !== !1 && y(t, Ga(e.name || "v")), y(t, e), t
                    }
                    return "string" == typeof e ? Ga(e) : void 0
                }
            }

            function Qn(e) {
                is(function() {
                    is(e)
                })
            }

            function Xn(e, t) {
                (e._transitionClasses || (e._transitionClasses = [])).push(t), Zn(e, t)
            }

            function er(e, t) {
                e._transitionClasses && d(e._transitionClasses, t), Gn(e, t)
            }

            function tr(e, t, n) {
                var r = nr(e, t),
                    i = r.type,
                    o = r.timeout,
                    a = r.propCount;
                if (!i) return n();
                var s = i === Qa ? ts : rs,
                    c = 0,
                    u = function() {
                        e.removeEventListener(s, l), n()
                    },
                    l = function(t) {
                        t.target === e && ++c >= a && u()
                    };
                setTimeout(function() {
                    c < a && u()
                }, o + 1), e.addEventListener(s, l)
            }

            function nr(e, t) {
                var n, r = window.getComputedStyle(e),
                    i = r[es + "Delay"].split(", "),
                    o = r[es + "Duration"].split(", "),
                    a = rr(i, o),
                    s = r[ns + "Delay"].split(", "),
                    c = r[ns + "Duration"].split(", "),
                    u = rr(s, c),
                    l = 0,
                    f = 0;
                t === Qa ? a > 0 && (n = Qa, l = a, f = o.length) : t === Xa ? u > 0 && (n = Xa, l = u, f = c.length) : (l = Math.max(a, u), n = l > 0 ? a > u ? Qa : Xa : null, f = n ? n === Qa ? o.length : c.length : 0);
                var p = n === Qa && os.test(r[es + "Property"]);
                return {
                    type: n,
                    timeout: l,
                    propCount: f,
                    hasTransform: p
                }
            }

            function rr(e, t) {
                for (; e.length < t.length;) e = e.concat(e);
                return Math.max.apply(null, t.map(function(t, n) {
                    return ir(t) + ir(e[n])
                }))
            }

            function ir(e) {
                return 1e3 * Number(e.slice(0, -1))
            }

            function or(e, t) {
                var i = e.elm;
                r(i._leaveCb) && (i._leaveCb.cancelled = !0, i._leaveCb());
                var o = Yn(e.data.transition);
                if (!n(o) && !r(i._enterCb) && 1 === i.nodeType) {
                    for (var a = o.css, c = o.type, u = o.enterClass, l = o.enterToClass, p = o.enterActiveClass, d = o.appearClass, v = o.appearToClass, h = o.appearActiveClass, m = o.beforeEnter, g = o.enter, y = o.afterEnter, _ = o.enterCancelled, b = o.beforeAppear, $ = o.appear, w = o.afterAppear, x = o.appearCancelled, k = o.duration, A = Fo, O = Fo.$vnode; O && O.parent;) O = O.parent, A = O.context;
                    var S = !A._isMounted || !e.isRootInsert;
                    if (!S || $ || "" === $) {
                        var T = S && d ? d : u,
                            E = S && h ? h : p,
                            j = S && v ? v : l,
                            N = S ? b || m : m,
                            L = S && "function" == typeof $ ? $ : g,
                            I = S ? w || y : y,
                            D = S ? x || _ : _,
                            M = f(s(k) ? k.enter : k),
                            P = a !== !1 && !uo,
                            R = cr(L),
                            F = i._enterCb = C(function() {
                                P && (er(i, j), er(i, E)), F.cancelled ? (P && er(i, T), D && D(i)) : I && I(i), i._enterCb = null
                            });
                        e.data.show || te(e.data.hook || (e.data.hook = {}), "insert", function() {
                            var t = i.parentNode,
                                n = t && t._pending && t._pending[e.key];
                            n && n.tag === e.tag && n.elm._leaveCb && n.elm._leaveCb(), L && L(i, F)
                        }), N && N(i), P && (Xn(i, T), Xn(i, E), Qn(function() {
                            Xn(i, j), er(i, T), F.cancelled || R || (sr(M) ? setTimeout(F, M) : tr(i, c, F))
                        })), e.data.show && (t && t(), L && L(i, F)), P || R || F()
                    }
                }
            }

            function ar(e, t) {
                function i() {
                    x.cancelled || (e.data.show || ((o.parentNode._pending || (o.parentNode._pending = {}))[e.key] = e), v && v(o), b && (Xn(o, l), Xn(o, d), Qn(function() {
                        Xn(o, p), er(o, l), x.cancelled || $ || (sr(w) ? setTimeout(x, w) : tr(o, u, x))
                    })), h && h(o, x), b || $ || x())
                }
                var o = e.elm;
                r(o._enterCb) && (o._enterCb.cancelled = !0, o._enterCb());
                var a = Yn(e.data.transition);
                if (n(a)) return t();
                if (!r(o._leaveCb) && 1 === o.nodeType) {
                    var c = a.css,
                        u = a.type,
                        l = a.leaveClass,
                        p = a.leaveToClass,
                        d = a.leaveActiveClass,
                        v = a.beforeLeave,
                        h = a.leave,
                        m = a.afterLeave,
                        g = a.leaveCancelled,
                        y = a.delayLeave,
                        _ = a.duration,
                        b = c !== !1 && !uo,
                        $ = cr(h),
                        w = f(s(_) ? _.leave : _),
                        x = o._leaveCb = C(function() {
                            o.parentNode && o.parentNode._pending && (o.parentNode._pending[e.key] = null), b && (er(o, p), er(o, d)), x.cancelled ? (b && er(o, l), g && g(o)) : (t(), m && m(o)), o._leaveCb = null
                        });
                    y ? y(i) : i()
                }
            }

            function sr(e) {
                return "number" == typeof e && !isNaN(e)
            }

            function cr(e) {
                if (n(e)) return !1;
                var t = e.fns;
                return r(t) ? cr(Array.isArray(t) ? t[0] : t) : (e._length || e.length) > 1
            }

            function ur(e, t) {
                t.data.show !== !0 && or(t)
            }

            function lr(e, t, n) {
                var r = t.value,
                    i = e.multiple;
                if (!i || Array.isArray(r)) {
                    for (var o, a, s = 0, c = e.options.length; s < c; s++)
                        if (a = e.options[s], i) o = x(r, pr(a)) > -1, a.selected !== o && (a.selected = o);
                        else if (w(pr(a), r)) return void(e.selectedIndex !== s && (e.selectedIndex = s));
                    i || (e.selectedIndex = -1)
                }
            }

            function fr(e, t) {
                for (var n = 0, r = t.length; n < r; n++)
                    if (w(pr(t[n]), e)) return !1;
                return !0
            }

            function pr(e) {
                return "_value" in e ? e._value : e.value
            }

            function dr(e) {
                e.target.composing = !0
            }

            function vr(e) {
                e.target.composing && (e.target.composing = !1, hr(e.target, "input"))
            }

            function hr(e, t) {
                var n = document.createEvent("HTMLEvents");
                n.initEvent(t, !0, !0), e.dispatchEvent(n)
            }

            function mr(e) {
                return !e.componentInstance || e.data && e.data.transition ? e : mr(e.componentInstance._vnode)
            }

            function gr(e) {
                var t = e && e.componentOptions;
                return t && t.Ctor.options["abstract"] ? gr(le(t.children)) : e
            }

            function yr(e) {
                var t = {},
                    n = e.$options;
                for (var r in n.propsData) t[r] = e[r];
                var i = n._parentListeners;
                for (var o in i) t[Ki(o)] = i[o];
                return t
            }

            function _r(e, t) {
                if (/\d-keep-alive$/.test(t.tag)) return e("keep-alive", {
                    props: t.componentOptions.propsData
                })
            }

            function br(e) {
                for (; e = e.parent;)
                    if (e.data.transition) return !0
            }

            function $r(e, t) {
                return t.key === e.key && t.tag === e.tag
            }

            function wr(e) {
                e.elm._moveCb && e.elm._moveCb(), e.elm._enterCb && e.elm._enterCb()
            }

            function xr(e) {
                e.data.newPos = e.elm.getBoundingClientRect()
            }

            function Cr(e) {
                var t = e.data.pos,
                    n = e.data.newPos,
                    r = t.left - n.left,
                    i = t.top - n.top;
                if (r || i) {
                    e.data.moved = !0;
                    var o = e.elm.style;
                    o.transform = o.WebkitTransform = "translate(" + r + "px," + i + "px)", o.transitionDuration = "0s"
                }
            }

            function kr(e, t) {
                var n = document.createElement("div");
                return n.innerHTML = '<div a="' + e + '">', n.innerHTML.indexOf(t) > 0
            }

            function Ar(e) {
                return ys = ys || document.createElement("div"), ys.innerHTML = e, ys.textContent
            }

            function Or(e, t) {
                var n = t ? ic : rc;
                return e.replace(n, function(e) {
                    return nc[e]
                })
            }

            function Sr(e, t) {
                function n(t) {
                    p += t, e = e.substring(t)
                }

                function r() {
                    var t = e.match(Ts);
                    if (t) {
                        var r = {
                            tagName: t[1],
                            attrs: [],
                            start: p
                        };
                        n(t[0].length);
                        for (var i, o; !(i = e.match(Es)) && (o = e.match(As));) n(o[0].length), r.attrs.push(o);
                        if (i) return r.unarySlash = i[1], n(i[0].length), r.end = p, r
                    }
                }

                function i(e) {
                    var n = e.tagName,
                        r = e.unarySlash;
                    u && ("p" === s && ws(n) && o(s), f(n) && s === n && o(n));
                    for (var i = l(n) || "html" === n && "head" === s || !!r, a = e.attrs.length, p = new Array(a), d = 0; d < a; d++) {
                        var v = e.attrs[d];
                        Ds && v[0].indexOf('""') === -1 && ("" === v[3] && delete v[3], "" === v[4] && delete v[4], "" === v[5] && delete v[5]);
                        var h = v[3] || v[4] || v[5] || "";
                        p[d] = {
                            name: v[1],
                            value: Or(h, t.shouldDecodeNewlines)
                        }
                    }
                    i || (c.push({
                        tag: n,
                        lowerCasedTag: n.toLowerCase(),
                        attrs: p
                    }), s = n), t.start && t.start(n, p, i, e.start, e.end)
                }

                function o(e, n, r) {
                    var i, o;
                    if (null == n && (n = p), null == r && (r = p), e && (o = e.toLowerCase()), e)
                        for (i = c.length - 1; i >= 0 && c[i].lowerCasedTag !== o; i--);
                    else i = 0;
                    if (i >= 0) {
                        for (var a = c.length - 1; a >= i; a--) t.end && t.end(c[a].tag, n, r);
                        c.length = i, s = i && c[i - 1].tag
                    } else "br" === o ? t.start && t.start(e, [], !0, n, r) : "p" === o && (t.start && t.start(e, [], !1, n, r), t.end && t.end(e, n, r))
                }
                for (var a, s, c = [], u = t.expectHTML, l = t.isUnaryTag || Gi, f = t.canBeLeftOpenTag || Gi, p = 0; e;) {
                    if (a = e, s && ec(s)) {
                        var d = s.toLowerCase(),
                            v = tc[d] || (tc[d] = new RegExp("([\\s\\S]*?)(</" + d + "[^>]*>)", "i")),
                            h = 0,
                            m = e.replace(v, function(e, n, r) {
                                return h = r.length, ec(d) || "noscript" === d || (n = n.replace(/<!--([\s\S]*?)-->/g, "$1").replace(/<!\[CDATA\[([\s\S]*?)]]>/g, "$1")), t.chars && t.chars(n), ""
                            });
                        p += e.length - m.length, e = m, o(d, p - h, p)
                    } else {
                        var g = e.indexOf("<");
                        if (0 === g) {
                            if (Ls.test(e)) {
                                var y = e.indexOf("-->");
                                if (y >= 0) {
                                    n(y + 3);
                                    continue
                                }
                            }
                            if (Is.test(e)) {
                                var _ = e.indexOf("]>");
                                if (_ >= 0) {
                                    n(_ + 2);
                                    continue
                                }
                            }
                            var b = e.match(Ns);
                            if (b) {
                                n(b[0].length);
                                continue
                            }
                            var $ = e.match(js);
                            if ($) {
                                var w = p;
                                n($[0].length), o($[1], w, p);
                                continue
                            }
                            var x = r();
                            if (x) {
                                i(x);
                                continue
                            }
                        }
                        var C = void 0,
                            k = void 0,
                            A = void 0;
                        if (g >= 0) {
                            for (k = e.slice(g); !(js.test(k) || Ts.test(k) || Ls.test(k) || Is.test(k) || (A = k.indexOf("<", 1), A < 0));) g += A, k = e.slice(g);
                            C = e.substring(0, g), n(g)
                        }
                        g < 0 && (C = e, e = ""), t.chars && C && t.chars(C)
                    }
                    if (e === a) {
                        t.chars && t.chars(e);
                        break
                    }
                }
                o()
            }

            function Tr(e, t) {
                var n = t ? sc(t) : oc;
                if (n.test(e)) {
                    for (var r, i, o = [], a = n.lastIndex = 0; r = n.exec(e);) {
                        i = r.index, i > a && o.push(JSON.stringify(e.slice(a, i)));
                        var s = vn(r[1].trim());
                        o.push("_s(" + s + ")"), a = i + r[0].length
                    }
                    return a < e.length && o.push(JSON.stringify(e.slice(a))), o.join("+")
                }
            }

            function Er(e, t) {
                function n(e) {
                    e.pre && (s = !1), Hs(e.tag) && (c = !1)
                }
                Ms = t.warn || mn, Vs = t.getTagNamespace || Gi, Us = t.mustUseProp || Gi, Hs = t.isPreTag || Gi, Fs = gn(t.modules, "preTransformNode"), Rs = gn(t.modules, "transformNode"), Bs = gn(t.modules, "postTransformNode"), Ps = t.delimiters;
                var r, i, o = [],
                    a = t.preserveWhitespace !== !1,
                    s = !1,
                    c = !1;
                return Sr(e, {
                    warn: Ms,
                    expectHTML: t.expectHTML,
                    isUnaryTag: t.isUnaryTag,
                    canBeLeftOpenTag: t.canBeLeftOpenTag,
                    shouldDecodeNewlines: t.shouldDecodeNewlines,
                    start: function(e, a, u) {
                        function l(e) {}
                        var f = i && i.ns || Vs(e);
                        co && "svg" === f && (a = Zr(a));
                        var p = {
                            type: 1,
                            tag: e,
                            attrsList: a,
                            attrsMap: Kr(a),
                            parent: i,
                            children: []
                        };
                        f && (p.ns = f), Wr(p) && !bo() && (p.forbidden = !0);
                        for (var d = 0; d < Fs.length; d++) Fs[d](p, t);
                        if (s || (jr(p), p.pre && (s = !0)), Hs(p.tag) && (c = !0), s) Nr(p);
                        else {
                            Dr(p), Mr(p), Br(p), Lr(p), p.plain = !p.key && !a.length, Ir(p), Hr(p), Ur(p);
                            for (var v = 0; v < Rs.length; v++) Rs[v](p, t);
                            Vr(p)
                        }
                        if (r ? o.length || r["if"] && (p.elseif || p["else"]) && (l(p), Fr(r, {
                                exp: p.elseif,
                                block: p
                            })) : (r = p, l(r)), i && !p.forbidden)
                            if (p.elseif || p["else"]) Pr(p, i);
                            else if (p.slotScope) {
                            i.plain = !1;
                            var h = p.slotTarget || '"default"';
                            (i.scopedSlots || (i.scopedSlots = {}))[h] = p
                        } else i.children.push(p), p.parent = i;
                        u ? n(p) : (i = p, o.push(p));
                        for (var m = 0; m < Bs.length; m++) Bs[m](p, t)
                    },
                    end: function() {
                        var e = o[o.length - 1],
                            t = e.children[e.children.length - 1];
                        t && 3 === t.type && " " === t.text && !c && e.children.pop(), o.length -= 1, i = o[o.length - 1], n(e)
                    },
                    chars: function(e) {
                        if (i && (!co || "textarea" !== i.tag || i.attrsMap.placeholder !== e)) {
                            var t = i.children;
                            if (e = c || e.trim() ? qr(i) ? e : hc(e) : a && t.length ? " " : "") {
                                var n;
                                !s && " " !== e && (n = Tr(e, Ps)) ? t.push({
                                    type: 2,
                                    expression: n,
                                    text: e
                                }) : " " === e && t.length && " " === t[t.length - 1].text || t.push({
                                    type: 3,
                                    text: e
                                })
                            }
                        }
                    }
                }), r
            }

            function jr(e) {
                null != xn(e, "v-pre") && (e.pre = !0)
            }

            function Nr(e) {
                var t = e.attrsList.length;
                if (t)
                    for (var n = e.attrs = new Array(t), r = 0; r < t; r++) n[r] = {
                        name: e.attrsList[r].name,
                        value: JSON.stringify(e.attrsList[r].value)
                    };
                else e.pre || (e.plain = !0)
            }

            function Lr(e) {
                var t = wn(e, "key");
                t && (e.key = t)
            }

            function Ir(e) {
                var t = wn(e, "ref");
                t && (e.ref = t, e.refInFor = zr(e))
            }

            function Dr(e) {
                var t;
                if (t = xn(e, "v-for")) {
                    var n = t.match(lc);
                    if (!n) return;
                    e["for"] = n[2].trim();
                    var r = n[1].trim(),
                        i = r.match(fc);
                    i ? (e.alias = i[1].trim(), e.iterator1 = i[2].trim(), i[3] && (e.iterator2 = i[3].trim())) : e.alias = r
                }
            }

            function Mr(e) {
                var t = xn(e, "v-if");
                if (t) e["if"] = t, Fr(e, {
                    exp: t,
                    block: e
                });
                else {
                    null != xn(e, "v-else") && (e["else"] = !0);
                    var n = xn(e, "v-else-if");
                    n && (e.elseif = n)
                }
            }

            function Pr(e, t) {
                var n = Rr(t.children);
                n && n["if"] && Fr(n, {
                    exp: e.elseif,
                    block: e
                })
            }

            function Rr(e) {
                for (var t = e.length; t--;) {
                    if (1 === e[t].type) return e[t];
                    e.pop()
                }
            }

            function Fr(e, t) {
                e.ifConditions || (e.ifConditions = []), e.ifConditions.push(t)
            }

            function Br(e) {
                var t = xn(e, "v-once");
                null != t && (e.once = !0)
            }

            function Hr(e) {
                if ("slot" === e.tag) e.slotName = wn(e, "name");
                else {
                    var t = wn(e, "slot");
                    t && (e.slotTarget = '""' === t ? '"default"' : t), "template" === e.tag && (e.slotScope = xn(e, "scope"))
                }
            }

            function Ur(e) {
                var t;
                (t = wn(e, "is")) && (e.component = t), null != xn(e, "inline-template") && (e.inlineTemplate = !0)
            }

            function Vr(e) {
                var t, n, r, i, o, a, s, c = e.attrsList;
                for (t = 0, n = c.length; t < n; t++)
                    if (r = i = c[t].name, o = c[t].value, uc.test(r))
                        if (e.hasBindings = !0, a = Jr(r), a && (r = r.replace(vc, "")), dc.test(r)) r = r.replace(dc, ""), o = vn(o), s = !1, a && (a.prop && (s = !0, r = Ki(r), "innerHtml" === r && (r = "innerHTML")), a.camel && (r = Ki(r)), a.sync && $n(e, "update:" + Ki(r), kn(o, "$event"))), s || Us(e.tag, e.attrsMap.type, r) ? yn(e, r, o) : _n(e, r, o);
                        else if (cc.test(r)) r = r.replace(cc, ""), $n(e, r, o, a, !1, Ms);
                else {
                    r = r.replace(uc, "");
                    var u = r.match(pc),
                        l = u && u[1];
                    l && (r = r.slice(0, -(l.length + 1))), bn(e, r, i, o, l, a)
                } else {
                    _n(e, r, JSON.stringify(o))
                }
            }

            function zr(e) {
                for (var t = e; t;) {
                    if (void 0 !== t["for"]) return !0;
                    t = t.parent
                }
                return !1
            }

            function Jr(e) {
                var t = e.match(vc);
                if (t) {
                    var n = {};
                    return t.forEach(function(e) {
                        n[e.slice(1)] = !0
                    }), n
                }
            }

            function Kr(e) {
                for (var t = {}, n = 0, r = e.length; n < r; n++) t[e[n].name] = e[n].value;
                return t
            }

            function qr(e) {
                return "script" === e.tag || "style" === e.tag
            }

            function Wr(e) {
                return "style" === e.tag || "script" === e.tag && (!e.attrsMap.type || "text/javascript" === e.attrsMap.type)
            }

            function Zr(e) {
                for (var t = [], n = 0; n < e.length; n++) {
                    var r = e[n];
                    mc.test(r.name) || (r.name = r.name.replace(gc, ""), t.push(r))
                }
                return t
            }

            function Gr(e, t) {
                e && (zs = yc(t.staticKeys || ""), Js = t.isReservedTag || Gi, Qr(e), Xr(e, !1))
            }

            function Yr(e) {
                return p("type,tag,attrsList,attrsMap,plain,parent,children,attrs" + (e ? "," + e : ""))
            }

            function Qr(e) {
                if (e["static"] = ti(e), 1 === e.type) {
                    if (!Js(e.tag) && "slot" !== e.tag && null == e.attrsMap["inline-template"]) return;
                    for (var t = 0, n = e.children.length; t < n; t++) {
                        var r = e.children[t];
                        Qr(r), r["static"] || (e["static"] = !1)
                    }
                }
            }

            function Xr(e, t) {
                if (1 === e.type) {
                    if ((e["static"] || e.once) && (e.staticInFor = t), e["static"] && e.children.length && (1 !== e.children.length || 3 !== e.children[0].type)) return void(e.staticRoot = !0);
                    if (e.staticRoot = !1, e.children)
                        for (var n = 0, r = e.children.length; n < r; n++) Xr(e.children[n], t || !!e["for"]);
                    e.ifConditions && ei(e.ifConditions, t)
                }
            }

            function ei(e, t) {
                for (var n = 1, r = e.length; n < r; n++) Xr(e[n].block, t)
            }

            function ti(e) {
                return 2 !== e.type && (3 === e.type || !(!e.pre && (e.hasBindings || e["if"] || e["for"] || Vi(e.tag) || !Js(e.tag) || ni(e) || !Object.keys(e).every(zs))))
            }

            function ni(e) {
                for (; e.parent;) {
                    if (e = e.parent, "template" !== e.tag) return !1;
                    if (e["for"]) return !0
                }
                return !1
            }

            function ri(e, t, n) {
                var r = t ? "nativeOn:{" : "on:{";
                for (var i in e) {
                    var o = e[i];
                    r += '"' + i + '":' + ii(i, o) + ","
                }
                return r.slice(0, -1) + "}"
            }

            function ii(e, t) {
                if (!t) return "function(){}";
                if (Array.isArray(t)) return "[" + t.map(function(t) {
                    return ii(e, t)
                }).join(",") + "]";
                var n = bc.test(t.value),
                    r = _c.test(t.value);
                if (t.modifiers) {
                    var i = "",
                        o = "",
                        a = [];
                    for (var s in t.modifiers) xc[s] ? (o += xc[s], $c[s] && a.push(s)) : a.push(s);
                    a.length && (i += oi(a)), o && (i += o);
                    var c = n ? t.value + "($event)" : r ? "(" + t.value + ")($event)" : t.value;
                    return "function($event){" + i + c + "}"
                }
                return n || r ? t.value : "function($event){" + t.value + "}"
            }

            function oi(e) {
                return "if(!('button' in $event)&&" + e.map(ai).join("&&") + ")return null;"
            }

            function ai(e) {
                var t = parseInt(e, 10);
                if (t) return "$event.keyCode!==" + t;
                var n = $c[e];
                return "_k($event.keyCode," + JSON.stringify(e) + (n ? "," + JSON.stringify(n) : "") + ")"
            }

            function si(e, t) {
                e.wrapData = function(n) {
                    return "_b(" + n + ",'" + e.tag + "'," + t.value + (t.modifiers && t.modifiers.prop ? ",true" : "") + ")"
                }
            }

            function ci(e, t) {
                var n = Ys,
                    r = Ys = [],
                    i = Qs;
                Qs = 0, Xs = t, Ks = t.warn || mn, qs = gn(t.modules, "transformCode"), Ws = gn(t.modules, "genData"), Zs = t.directives || {}, Gs = t.isReservedTag || Gi;
                var o = e ? ui(e) : '_c("div")';
                return Ys = n, Qs = i, {
                    render: "with(this){return " + o + "}",
                    staticRenderFns: r
                }
            }

            function ui(e) {
                if (e.staticRoot && !e.staticProcessed) return li(e);
                if (e.once && !e.onceProcessed) return fi(e);
                if (e["for"] && !e.forProcessed) return vi(e);
                if (e["if"] && !e.ifProcessed) return pi(e);
                if ("template" !== e.tag || e.slotTarget) {
                    if ("slot" === e.tag) return Oi(e);
                    var t;
                    if (e.component) t = Si(e.component, e);
                    else {
                        var n = e.plain ? void 0 : hi(e),
                            r = e.inlineTemplate ? null : $i(e, !0);
                        t = "_c('" + e.tag + "'" + (n ? "," + n : "") + (r ? "," + r : "") + ")"
                    }
                    for (var i = 0; i < qs.length; i++) t = qs[i](e, t);
                    return t
                }
                return $i(e) || "void 0"
            }

            function li(e) {
                return e.staticProcessed = !0, Ys.push("with(this){return " + ui(e) + "}"), "_m(" + (Ys.length - 1) + (e.staticInFor ? ",true" : "") + ")"
            }

            function fi(e) {
                if (e.onceProcessed = !0, e["if"] && !e.ifProcessed) return pi(e);
                if (e.staticInFor) {
                    for (var t = "", n = e.parent; n;) {
                        if (n["for"]) {
                            t = n.key;
                            break
                        }
                        n = n.parent
                    }
                    return t ? "_o(" + ui(e) + "," + Qs++ + (t ? "," + t : "") + ")" : ui(e)
                }
                return li(e)
            }

            function pi(e) {
                return e.ifProcessed = !0, di(e.ifConditions.slice())
            }

            function di(e) {
                function t(e) {
                    return e.once ? fi(e) : ui(e)
                }
                if (!e.length) return "_e()";
                var n = e.shift();
                return n.exp ? "(" + n.exp + ")?" + t(n.block) + ":" + di(e) : "" + t(n.block)
            }

            function vi(e) {
                var t = e["for"],
                    n = e.alias,
                    r = e.iterator1 ? "," + e.iterator1 : "",
                    i = e.iterator2 ? "," + e.iterator2 : "";
                return e.forProcessed = !0, "_l((" + t + "),function(" + n + r + i + "){return " + ui(e) + "})"
            }

            function hi(e) {
                var t = "{",
                    n = mi(e);
                n && (t += n + ","), e.key && (t += "key:" + e.key + ","), e.ref && (t += "ref:" + e.ref + ","), e.refInFor && (t += "refInFor:true,"), e.pre && (t += "pre:true,"), e.component && (t += 'tag:"' + e.tag + '",');
                for (var r = 0; r < Ws.length; r++) t += Ws[r](e);
                if (e.attrs && (t += "attrs:{" + Ti(e.attrs) + "},"), e.props && (t += "domProps:{" + Ti(e.props) + "},"), e.events && (t += ri(e.events, !1, Ks) + ","), e.nativeEvents && (t += ri(e.nativeEvents, !0, Ks) + ","), e.slotTarget && (t += "slot:" + e.slotTarget + ","), e.scopedSlots && (t += yi(e.scopedSlots) + ","), e.model && (t += "model:{value:" + e.model.value + ",callback:" + e.model.callback + ",expression:" + e.model.expression + "},"), e.inlineTemplate) {
                    var i = gi(e);
                    i && (t += i + ",")
                }
                return t = t.replace(/,$/, "") + "}", e.wrapData && (t = e.wrapData(t)), t
            }

            function mi(e) {
                var t = e.directives;
                if (t) {
                    var n, r, i, o, a = "directives:[",
                        s = !1;
                    for (n = 0, r = t.length; n < r; n++) {
                        i = t[n], o = !0;
                        var c = Zs[i.name] || Cc[i.name];
                        c && (o = !!c(e, i, Ks)), o && (s = !0, a += '{name:"' + i.name + '",rawName:"' + i.rawName + '"' + (i.value ? ",value:(" + i.value + "),expression:" + JSON.stringify(i.value) : "") + (i.arg ? ',arg:"' + i.arg + '"' : "") + (i.modifiers ? ",modifiers:" + JSON.stringify(i.modifiers) : "") + "},")
                    }
                    return s ? a.slice(0, -1) + "]" : void 0
                }
            }

            function gi(e) {
                var t = e.children[0];
                if (1 === t.type) {
                    var n = ci(t, Xs);
                    return "inlineTemplate:{render:function(){" + n.render + "},staticRenderFns:[" + n.staticRenderFns.map(function(e) {
                        return "function(){" + e + "}"
                    }).join(",") + "]}"
                }
            }

            function yi(e) {
                return "scopedSlots:_u([" + Object.keys(e).map(function(t) {
                    return _i(t, e[t])
                }).join(",") + "])"
            }

            function _i(e, t) {
                return t["for"] && !t.forProcessed ? bi(e, t) : "{key:" + e + ",fn:function(" + String(t.attrsMap.scope) + "){return " + ("template" === t.tag ? $i(t) || "void 0" : ui(t)) + "}}"
            }

            function bi(e, t) {
                var n = t["for"],
                    r = t.alias,
                    i = t.iterator1 ? "," + t.iterator1 : "",
                    o = t.iterator2 ? "," + t.iterator2 : "";
                return t.forProcessed = !0, "_l((" + n + "),function(" + r + i + o + "){return " + _i(e, t) + "})"
            }

            function $i(e, t) {
                var n = e.children;
                if (n.length) {
                    var r = n[0];
                    if (1 === n.length && r["for"] && "template" !== r.tag && "slot" !== r.tag) return ui(r);
                    var i = t ? wi(n) : 0;
                    return "[" + n.map(ki).join(",") + "]" + (i ? "," + i : "")
                }
            }

            function wi(e) {
                for (var t = 0, n = 0; n < e.length; n++) {
                    var r = e[n];
                    if (1 === r.type) {
                        if (xi(r) || r.ifConditions && r.ifConditions.some(function(e) {
                                return xi(e.block)
                            })) {
                            t = 2;
                            break
                        }(Ci(r) || r.ifConditions && r.ifConditions.some(function(e) {
                            return Ci(e.block)
                        })) && (t = 1)
                    }
                }
                return t
            }

            function xi(e) {
                return void 0 !== e["for"] || "template" === e.tag || "slot" === e.tag
            }

            function Ci(e) {
                return !Gs(e.tag)
            }

            function ki(e) {
                return 1 === e.type ? ui(e) : Ai(e)
            }

            function Ai(e) {
                return "_v(" + (2 === e.type ? e.expression : Ei(JSON.stringify(e.text))) + ")"
            }

            function Oi(e) {
                var t = e.slotName || '"default"',
                    n = $i(e),
                    r = "_t(" + t + (n ? "," + n : ""),
                    i = e.attrs && "{" + e.attrs.map(function(e) {
                        return Ki(e.name) + ":" + e.value
                    }).join(",") + "}",
                    o = e.attrsMap["v-bind"];
                return !i && !o || n || (r += ",null"), i && (r += "," + i), o && (r += (i ? "" : ",null") + "," + o), r + ")"
            }

            function Si(e, t) {
                var n = t.inlineTemplate ? null : $i(t, !0);
                return "_c(" + e + "," + hi(t) + (n ? "," + n : "") + ")"
            }

            function Ti(e) {
                for (var t = "", n = 0; n < e.length; n++) {
                    var r = e[n];
                    t += '"' + r.name + '":' + Ei(r.value) + ","
                }
                return t.slice(0, -1)
            }

            function Ei(e) {
                return e.replace(/\u2028/g, "\\u2028").replace(/\u2029/g, "\\u2029")
            }

            function ji(e, t) {
                var n = Er(e.trim(), t);
                Gr(n, t);
                var r = ci(n, t);
                return {
                    ast: n,
                    render: r.render,
                    staticRenderFns: r.staticRenderFns
                }
            }

            function Ni(e, t) {
                try {
                    return new Function(e)
                } catch (n) {
                    return t.push({
                        err: n,
                        code: e
                    }), b
                }
            }

            function Li(e) {
                function t(t, n) {
                    var r = Object.create(e),
                        i = [],
                        o = [];
                    if (r.warn = function(e, t) {
                            (t ? o : i).push(e)
                        }, n) {
                        n.modules && (r.modules = (e.modules || []).concat(n.modules)), n.directives && (r.directives = y(Object.create(e.directives), n.directives));
                        for (var a in n) "modules" !== a && "directives" !== a && (r[a] = n[a])
                    }
                    var s = ji(t, r);
                    return s.errors = i, s.tips = o, s
                }

                function n(e, n, i) {
                    n = n || {};
                    var o = n.delimiters ? String(n.delimiters) + e : e;
                    if (r[o]) return r[o];
                    var a = t(e, n),
                        s = {},
                        c = [];
                    s.render = Ni(a.render, c);
                    var u = a.staticRenderFns.length;
                    s.staticRenderFns = new Array(u);
                    for (var l = 0; l < u; l++) s.staticRenderFns[l] = Ni(a.staticRenderFns[l], c);
                    return r[o] = s
                }
                var r = Object.create(null);
                return {
                    compile: t,
                    compileToFunctions: n
                }
            }

            function Ii(e, t) {
                var n = (t.warn || mn, xn(e, "class"));
                n && (e.staticClass = JSON.stringify(n));
                var r = wn(e, "class", !1);
                r && (e.classBinding = r)
            }

            function Di(e) {
                var t = "";
                return e.staticClass && (t += "staticClass:" + e.staticClass + ","), e.classBinding && (t += "class:" + e.classBinding + ","), t
            }

            function Mi(e, t) {
                var n = (t.warn || mn, xn(e, "style"));
                if (n) {
                    e.staticStyle = JSON.stringify(Va(n))
                }
                var r = wn(e, "style", !1);
                r && (e.styleBinding = r)
            }

            function Pi(e) {
                var t = "";
                return e.staticStyle && (t += "staticStyle:" + e.staticStyle + ","), e.styleBinding && (t += "style:(" + e.styleBinding + "),"), t
            }

            function Ri(e, t) {
                t.value && yn(e, "textContent", "_s(" + t.value + ")")
            }

            function Fi(e, t) {
                t.value && yn(e, "innerHTML", "_s(" + t.value + ")")
            }

            function Bi(e) {
                if (e.outerHTML) return e.outerHTML;
                var t = document.createElement("div");
                return t.appendChild(e.cloneNode(!0)), t.innerHTML
            }
            var Hi = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
                    return typeof e
                } : function(e) {
                    return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
                },
                Ui = Object.prototype.toString,
                Vi = p("slot,component", !0),
                zi = Object.prototype.hasOwnProperty,
                Ji = /-(\w)/g,
                Ki = h(function(e) {
                    return e.replace(Ji, function(e, t) {
                        return t ? t.toUpperCase() : ""
                    })
                }),
                qi = h(function(e) {
                    return e.charAt(0).toUpperCase() + e.slice(1)
                }),
                Wi = /([^-])([A-Z])/g,
                Zi = h(function(e) {
                    return e.replace(Wi, "$1-$2").replace(Wi, "$1-$2").toLowerCase()
                }),
                Gi = function() {
                    return !1
                },
                Yi = function(e) {
                    return e
                },
                Qi = "data-server-rendered",
                Xi = ["component", "directive", "filter"],
                eo = ["beforeCreate", "created", "beforeMount", "mounted", "beforeUpdate", "updated", "beforeDestroy", "destroyed", "activated", "deactivated"],
                to = {
                    optionMergeStrategies: Object.create(null),
                    silent: !1,
                    productionTip: !1,
                    devtools: !1,
                    performance: !1,
                    errorHandler: null,
                    ignoredElements: [],
                    keyCodes: Object.create(null),
                    isReservedTag: Gi,
                    isReservedAttr: Gi,
                    isUnknownElement: Gi,
                    getTagNamespace: b,
                    parsePlatformTagName: Yi,
                    mustUseProp: Gi,
                    _lifecycleHooks: eo
                },
                no = Object.freeze({}),
                ro = /[^\w.$]/,
                io = b,
                oo = "__proto__" in {},
                ao = "undefined" != typeof window,
                so = ao && window.navigator.userAgent.toLowerCase(),
                co = so && /msie|trident/.test(so),
                uo = so && so.indexOf("msie 9.0") > 0,
                lo = so && so.indexOf("edge/") > 0,
                fo = so && so.indexOf("android") > 0,
                po = so && /iphone|ipad|ipod|ios/.test(so),
                vo = so && /chrome\/\d+/.test(so) && !lo,
                ho = !1;
            if (ao) try {
                var mo = {};
                Object.defineProperty(mo, "passive", {
                    get: function() {
                        ho = !0
                    }
                }), window.addEventListener("test-passive", null, mo)
            } catch (go) {}
            var yo, _o, bo = function() {
                    return void 0 === yo && (yo = !ao && "undefined" != typeof t && "server" === t.process.env.VUE_ENV), yo
                },
                $o = ao && window.__VUE_DEVTOOLS_GLOBAL_HOOK__,
                wo = "undefined" != typeof Symbol && T(Symbol) && "undefined" != typeof Reflect && T(Reflect.ownKeys),
                xo = function() {
                    function e() {
                        r = !1;
                        var e = n.slice(0);
                        n.length = 0;
                        for (var t = 0; t < e.length; t++) e[t]()
                    }
                    var t, n = [],
                        r = !1;
                    if ("undefined" != typeof Promise && T(Promise)) {
                        var i = Promise.resolve(),
                            o = function(e) {
                                console.error(e)
                            };
                        t = function() {
                            i.then(e)["catch"](o), po && setTimeout(b)
                        }
                    } else if ("undefined" == typeof MutationObserver || !T(MutationObserver) && "[object MutationObserverConstructor]" !== MutationObserver.toString()) t = function() {
                        setTimeout(e, 0)
                    };
                    else {
                        var a = 1,
                            s = new MutationObserver(e),
                            c = document.createTextNode(String(a));
                        s.observe(c, {
                            characterData: !0
                        }), t = function() {
                            a = (a + 1) % 2, c.data = String(a)
                        }
                    }
                    return function(e, i) {
                        var o;
                        if (n.push(function() {
                                if (e) try {
                                    e.call(i)
                                } catch (t) {
                                    S(t, i, "nextTick")
                                } else o && o(i)
                            }), r || (r = !0, t()), !e && "undefined" != typeof Promise) return new Promise(function(e, t) {
                            o = e
                        })
                    }
                }();
            _o = "undefined" != typeof Set && T(Set) ? Set : function() {
                function e() {
                    this.set = Object.create(null)
                }
                return e.prototype.has = function(e) {
                    return this.set[e] === !0
                }, e.prototype.add = function(e) {
                    this.set[e] = !0
                }, e.prototype.clear = function() {
                    this.set = Object.create(null)
                }, e
            }();
            var Co = 0,
                ko = function() {
                    this.id = Co++, this.subs = []
                };
            ko.prototype.addSub = function(e) {
                this.subs.push(e)
            }, ko.prototype.removeSub = function(e) {
                d(this.subs, e)
            }, ko.prototype.depend = function() {
                ko.target && ko.target.addDep(this)
            }, ko.prototype.notify = function() {
                for (var e = this.subs.slice(), t = 0, n = e.length; t < n; t++) e[t].update()
            }, ko.target = null;
            var Ao = [],
                Oo = Array.prototype,
                So = Object.create(Oo);
            ["push", "pop", "shift", "unshift", "splice", "sort", "reverse"].forEach(function(e) {
                var t = Oo[e];
                A(So, e, function() {
                    for (var n = arguments, r = arguments.length, i = new Array(r); r--;) i[r] = n[r];
                    var o, a = t.apply(this, i),
                        s = this.__ob__;
                    switch (e) {
                        case "push":
                            o = i;
                            break;
                        case "unshift":
                            o = i;
                            break;
                        case "splice":
                            o = i.slice(2)
                    }
                    return o && s.observeArray(o), s.dep.notify(), a
                })
            });
            var To = Object.getOwnPropertyNames(So),
                Eo = {
                    shouldConvert: !0,
                    isSettingProps: !1
                },
                jo = function(e) {
                    if (this.value = e, this.dep = new ko, this.vmCount = 0, A(e, "__ob__", this), Array.isArray(e)) {
                        var t = oo ? N : L;
                        t(e, So, To), this.observeArray(e)
                    } else this.walk(e)
                };
            jo.prototype.walk = function(e) {
                for (var t = Object.keys(e), n = 0; n < t.length; n++) D(e, t[n], e[t[n]])
            }, jo.prototype.observeArray = function(e) {
                for (var t = 0, n = e.length; t < n; t++) I(e[t])
            };
            var No = to.optionMergeStrategies;
            No.data = function(e, t, n) {
                return n ? e || t ? function() {
                    var r = "function" == typeof t ? t.call(n) : t,
                        i = "function" == typeof e ? e.call(n) : void 0;
                    return r ? F(r, i) : i
                } : void 0 : t ? "function" != typeof t ? e : e ? function() {
                    return F(t.call(this), e.call(this))
                } : t : e
            }, eo.forEach(function(e) {
                No[e] = B
            }), Xi.forEach(function(e) {
                No[e + "s"] = H
            }), No.watch = function(e, t) {
                if (!t) return Object.create(e || null);
                if (!e) return t;
                var n = {};
                y(n, e);
                for (var r in t) {
                    var i = n[r],
                        o = t[r];
                    i && !Array.isArray(i) && (i = [i]), n[r] = i ? i.concat(o) : [o];
                }
                return n
            }, No.props = No.methods = No.computed = function(e, t) {
                if (!t) return Object.create(e || null);
                if (!e) return t;
                var n = Object.create(null);
                return y(n, e), y(n, t), n
            };
            var Lo = function(e, t) {
                    return void 0 === t ? e : t
                },
                Io = function(e, t, n, r, i, o, a) {
                    this.tag = e, this.data = t, this.children = n, this.text = r, this.elm = i, this.ns = void 0, this.context = o, this.functionalContext = void 0, this.key = t && t.key, this.componentOptions = a, this.componentInstance = void 0, this.parent = void 0, this.raw = !1, this.isStatic = !1, this.isRootInsert = !0, this.isComment = !1, this.isCloned = !1, this.isOnce = !1
                },
                Do = {
                    child: {}
                };
            Do.child.get = function() {
                return this.componentInstance
            }, Object.defineProperties(Io.prototype, Do);
            var Mo, Po = function() {
                    var e = new Io;
                    return e.text = "", e.isComment = !0, e
                },
                Ro = h(function(e) {
                    var t = "&" === e.charAt(0);
                    e = t ? e.slice(1) : e;
                    var n = "~" === e.charAt(0);
                    e = n ? e.slice(1) : e;
                    var r = "!" === e.charAt(0);
                    return e = r ? e.slice(1) : e, {
                        name: e,
                        once: n,
                        capture: r,
                        passive: t
                    }
                }),
                Fo = null,
                Bo = [],
                Ho = [],
                Uo = {},
                Vo = !1,
                zo = !1,
                Jo = 0,
                Ko = 0,
                qo = function(e, t, n, r) {
                    this.vm = e, e._watchers.push(this), r ? (this.deep = !!r.deep, this.user = !!r.user, this.lazy = !!r.lazy, this.sync = !!r.sync) : this.deep = this.user = this.lazy = this.sync = !1, this.cb = n, this.id = ++Ko, this.active = !0, this.dirty = this.lazy, this.deps = [], this.newDeps = [], this.depIds = new _o, this.newDepIds = new _o, this.expression = "", "function" == typeof t ? this.getter = t : (this.getter = O(t), this.getter || (this.getter = function() {})), this.value = this.lazy ? void 0 : this.get()
                };
            qo.prototype.get = function() {
                E(this);
                var e, t = this.vm;
                if (this.user) try {
                    e = this.getter.call(t, t)
                } catch (n) {
                    S(n, t, 'getter for watcher "' + this.expression + '"')
                } else e = this.getter.call(t, t);
                return this.deep && Le(e), j(), this.cleanupDeps(), e
            }, qo.prototype.addDep = function(e) {
                var t = e.id;
                this.newDepIds.has(t) || (this.newDepIds.add(t), this.newDeps.push(e), this.depIds.has(t) || e.addSub(this))
            }, qo.prototype.cleanupDeps = function() {
                for (var e = this, t = this.deps.length; t--;) {
                    var n = e.deps[t];
                    e.newDepIds.has(n.id) || n.removeSub(e)
                }
                var r = this.depIds;
                this.depIds = this.newDepIds, this.newDepIds = r, this.newDepIds.clear(), r = this.deps, this.deps = this.newDeps, this.newDeps = r, this.newDeps.length = 0
            }, qo.prototype.update = function() {
                this.lazy ? this.dirty = !0 : this.sync ? this.run() : Ne(this)
            }, qo.prototype.run = function() {
                if (this.active) {
                    var e = this.get();
                    if (e !== this.value || s(e) || this.deep) {
                        var t = this.value;
                        if (this.value = e, this.user) try {
                            this.cb.call(this.vm, e, t)
                        } catch (n) {
                            S(n, this.vm, 'callback for watcher "' + this.expression + '"')
                        } else this.cb.call(this.vm, e, t)
                    }
                }
            }, qo.prototype.evaluate = function() {
                this.value = this.get(), this.dirty = !1
            }, qo.prototype.depend = function() {
                for (var e = this, t = this.deps.length; t--;) e.deps[t].depend()
            }, qo.prototype.teardown = function() {
                var e = this;
                if (this.active) {
                    this.vm._isBeingDestroyed || d(this.vm._watchers, this);
                    for (var t = this.deps.length; t--;) e.deps[t].removeSub(e);
                    this.active = !1
                }
            };
            var Wo = new _o,
                Zo = {
                    enumerable: !0,
                    configurable: !0,
                    get: b,
                    set: b
                },
                Go = {
                    lazy: !0
                },
                Yo = {
                    init: function(e, t, n, r) {
                        if (!e.componentInstance || e.componentInstance._isDestroyed) {
                            var i = e.componentInstance = Xe(e, Fo, n, r);
                            i.$mount(t ? e.elm : void 0, t)
                        } else if (e.data.keepAlive) {
                            var o = e;
                            Yo.prepatch(o, o)
                        }
                    },
                    prepatch: function(e, t) {
                        var n = t.componentOptions,
                            r = t.componentInstance = e.componentInstance;
                        we(r, n.propsData, n.listeners, t, n.children)
                    },
                    insert: function(e) {
                        var t = e.context,
                            n = e.componentInstance;
                        n._isMounted || (n._isMounted = !0, Ae(n, "mounted")), e.data.keepAlive && (t._isMounted ? Ee(n) : Ce(n, !0))
                    },
                    destroy: function(e) {
                        var t = e.componentInstance;
                        t._isDestroyed || (e.data.keepAlive ? ke(t, !0) : t.$destroy())
                    }
                },
                Qo = Object.keys(Yo),
                Xo = 1,
                ea = 2,
                ta = 0;
            gt(wt), Ke(wt), he(wt), be(wt), mt(wt);
            var na = [String, RegExp],
                ra = {
                    name: "keep-alive",
                    abstract: !0,
                    props: {
                        include: na,
                        exclude: na
                    },
                    created: function() {
                        this.cache = Object.create(null)
                    },
                    destroyed: function() {
                        var e = this;
                        for (var t in e.cache) Nt(e.cache[t])
                    },
                    watch: {
                        include: function(e) {
                            jt(this.cache, this._vnode, function(t) {
                                return Et(e, t)
                            })
                        },
                        exclude: function(e) {
                            jt(this.cache, this._vnode, function(t) {
                                return !Et(e, t)
                            })
                        }
                    },
                    render: function() {
                        var e = le(this.$slots["default"]),
                            t = e && e.componentOptions;
                        if (t) {
                            var n = Tt(t);
                            if (n && (this.include && !Et(this.include, n) || this.exclude && Et(this.exclude, n))) return e;
                            var r = null == e.key ? t.Ctor.cid + (t.tag ? "::" + t.tag : "") : e.key;
                            this.cache[r] ? e.componentInstance = this.cache[r].componentInstance : this.cache[r] = e, e.data.keepAlive = !0
                        }
                        return e
                    }
                },
                ia = {
                    KeepAlive: ra
                };
            Lt(wt), Object.defineProperty(wt.prototype, "$isServer", {
                get: bo
            }), Object.defineProperty(wt.prototype, "$ssrContext", {
                get: function() {
                    return this.$vnode.ssrContext
                }
            }), wt.version = "2.3.3";
            var oa, aa, sa, ca, ua, la, fa, pa, da, va = p("style,class"),
                ha = p("input,textarea,option,select"),
                ma = function(e, t, n) {
                    return "value" === n && ha(e) && "button" !== t || "selected" === n && "option" === e || "checked" === n && "input" === e || "muted" === n && "video" === e
                },
                ga = p("contenteditable,draggable,spellcheck"),
                ya = p("allowfullscreen,async,autofocus,autoplay,checked,compact,controls,declare,default,defaultchecked,defaultmuted,defaultselected,defer,disabled,enabled,formnovalidate,hidden,indeterminate,inert,ismap,itemscope,loop,multiple,muted,nohref,noresize,noshade,novalidate,nowrap,open,pauseonexit,readonly,required,reversed,scoped,seamless,selected,sortable,translate,truespeed,typemustmatch,visible"),
                _a = "http://www.w3.org/1999/xlink",
                ba = function(e) {
                    return ":" === e.charAt(5) && "xlink" === e.slice(0, 5)
                },
                $a = function(e) {
                    return ba(e) ? e.slice(6, e.length) : ""
                },
                wa = function(e) {
                    return null == e || e === !1
                },
                xa = {
                    svg: "http://www.w3.org/2000/svg",
                    math: "http://www.w3.org/1998/Math/MathML"
                },
                Ca = p("html,body,base,head,link,meta,style,title,address,article,aside,footer,header,h1,h2,h3,h4,h5,h6,hgroup,nav,section,div,dd,dl,dt,figcaption,figure,hr,img,li,main,ol,p,pre,ul,a,b,abbr,bdi,bdo,br,cite,code,data,dfn,em,i,kbd,mark,q,rp,rt,rtc,ruby,s,samp,small,span,strong,sub,sup,time,u,var,wbr,area,audio,map,track,video,embed,object,param,source,canvas,script,noscript,del,ins,caption,col,colgroup,table,thead,tbody,td,th,tr,button,datalist,fieldset,form,input,label,legend,meter,optgroup,option,output,progress,select,textarea,details,dialog,menu,menuitem,summary,content,element,shadow,template"),
                ka = p("svg,animate,circle,clippath,cursor,defs,desc,ellipse,filter,font-face,foreignObject,g,glyph,image,line,marker,mask,missing-glyph,path,pattern,polygon,polyline,rect,switch,symbol,text,textpath,tspan,use,view", !0),
                Aa = function(e) {
                    return "pre" === e
                },
                Oa = function(e) {
                    return Ca(e) || ka(e)
                },
                Sa = Object.create(null),
                Ta = Object.freeze({
                    createElement: Ut,
                    createElementNS: Vt,
                    createTextNode: zt,
                    createComment: Jt,
                    insertBefore: Kt,
                    removeChild: qt,
                    appendChild: Wt,
                    parentNode: Zt,
                    nextSibling: Gt,
                    tagName: Yt,
                    setTextContent: Qt,
                    setAttribute: Xt
                }),
                Ea = {
                    create: function(e, t) {
                        en(t)
                    },
                    update: function(e, t) {
                        e.data.ref !== t.data.ref && (en(e, !0), en(t))
                    },
                    destroy: function(e) {
                        en(e, !0)
                    }
                },
                ja = new Io("", {}, []),
                Na = ["create", "activate", "update", "remove", "destroy"],
                La = {
                    create: an,
                    update: an,
                    destroy: function(e) {
                        an(e, ja)
                    }
                },
                Ia = Object.create(null),
                Da = [Ea, La],
                Ma = {
                    create: fn,
                    update: fn
                },
                Pa = {
                    create: dn,
                    update: dn
                },
                Ra = /[\w).+\-_$\]]/,
                Fa = "__r",
                Ba = "__c",
                Ha = {
                    create: Bn,
                    update: Bn
                },
                Ua = {
                    create: Hn,
                    update: Hn
                },
                Va = h(function(e) {
                    var t = {},
                        n = /;(?![^(]*\))/g,
                        r = /:(.+)/;
                    return e.split(n).forEach(function(e) {
                        if (e) {
                            var n = e.split(r);
                            n.length > 1 && (t[n[0].trim()] = n[1].trim())
                        }
                    }), t
                }),
                za = /^--/,
                Ja = /\s*!important$/,
                Ka = function(e, t, n) {
                    if (za.test(t)) e.style.setProperty(t, n);
                    else if (Ja.test(n)) e.style.setProperty(t, n.replace(Ja, ""), "important");
                    else {
                        var r = Wa(t);
                        if (Array.isArray(n))
                            for (var i = 0, o = n.length; i < o; i++) e.style[r] = n[i];
                        else e.style[r] = n
                    }
                },
                qa = ["Webkit", "Moz", "ms"],
                Wa = h(function(e) {
                    if (da = da || document.createElement("div"), e = Ki(e), "filter" !== e && e in da.style) return e;
                    for (var t = e.charAt(0).toUpperCase() + e.slice(1), n = 0; n < qa.length; n++) {
                        var r = qa[n] + t;
                        if (r in da.style) return r
                    }
                }),
                Za = {
                    create: Wn,
                    update: Wn
                },
                Ga = h(function(e) {
                    return {
                        enterClass: e + "-enter",
                        enterToClass: e + "-enter-to",
                        enterActiveClass: e + "-enter-active",
                        leaveClass: e + "-leave",
                        leaveToClass: e + "-leave-to",
                        leaveActiveClass: e + "-leave-active"
                    }
                }),
                Ya = ao && !uo,
                Qa = "transition",
                Xa = "animation",
                es = "transition",
                ts = "transitionend",
                ns = "animation",
                rs = "animationend";
            Ya && (void 0 === window.ontransitionend && void 0 !== window.onwebkittransitionend && (es = "WebkitTransition", ts = "webkitTransitionEnd"), void 0 === window.onanimationend && void 0 !== window.onwebkitanimationend && (ns = "WebkitAnimation", rs = "webkitAnimationEnd"));
            var is = ao && window.requestAnimationFrame ? window.requestAnimationFrame.bind(window) : setTimeout,
                os = /\b(transform|all)(,|$)/,
                as = ao ? {
                    create: ur,
                    activate: ur,
                    remove: function(e, t) {
                        e.data.show !== !0 ? ar(e, t) : t()
                    }
                } : {},
                ss = [Ma, Pa, Ha, Ua, Za, as],
                cs = ss.concat(Da),
                us = on({
                    nodeOps: Ta,
                    modules: cs
                });
            uo && document.addEventListener("selectionchange", function() {
                var e = document.activeElement;
                e && e.vmodel && hr(e, "input")
            });
            var ls = {
                    inserted: function(e, t, n) {
                        if ("select" === n.tag) {
                            var r = function() {
                                lr(e, t, n.context)
                            };
                            r(), (co || lo) && setTimeout(r, 0)
                        } else "textarea" !== n.tag && "text" !== e.type && "password" !== e.type || (e._vModifiers = t.modifiers, t.modifiers.lazy || (e.addEventListener("change", vr), fo || (e.addEventListener("compositionstart", dr), e.addEventListener("compositionend", vr)), uo && (e.vmodel = !0)))
                    },
                    componentUpdated: function(e, t, n) {
                        if ("select" === n.tag) {
                            lr(e, t, n.context);
                            var r = e.multiple ? t.value.some(function(t) {
                                return fr(t, e.options)
                            }) : t.value !== t.oldValue && fr(t.value, e.options);
                            r && hr(e, "change")
                        }
                    }
                },
                fs = {
                    bind: function(e, t, n) {
                        var r = t.value;
                        n = mr(n);
                        var i = n.data && n.data.transition,
                            o = e.__vOriginalDisplay = "none" === e.style.display ? "" : e.style.display;
                        r && i && !uo ? (n.data.show = !0, or(n, function() {
                            e.style.display = o
                        })) : e.style.display = r ? o : "none"
                    },
                    update: function(e, t, n) {
                        var r = t.value,
                            i = t.oldValue;
                        if (r !== i) {
                            n = mr(n);
                            var o = n.data && n.data.transition;
                            o && !uo ? (n.data.show = !0, r ? or(n, function() {
                                e.style.display = e.__vOriginalDisplay
                            }) : ar(n, function() {
                                e.style.display = "none"
                            })) : e.style.display = r ? e.__vOriginalDisplay : "none"
                        }
                    },
                    unbind: function(e, t, n, r, i) {
                        i || (e.style.display = e.__vOriginalDisplay)
                    }
                },
                ps = {
                    model: ls,
                    show: fs
                },
                ds = {
                    name: String,
                    appear: Boolean,
                    css: Boolean,
                    mode: String,
                    type: String,
                    enterClass: String,
                    leaveClass: String,
                    enterToClass: String,
                    leaveToClass: String,
                    enterActiveClass: String,
                    leaveActiveClass: String,
                    appearClass: String,
                    appearActiveClass: String,
                    appearToClass: String,
                    duration: [Number, String, Object]
                },
                vs = {
                    name: "transition",
                    props: ds,
                    abstract: !0,
                    render: function(e) {
                        var t = this,
                            n = this.$slots["default"];
                        if (n && (n = n.filter(function(e) {
                                return e.tag
                            }), n.length)) {
                            var r = this.mode,
                                i = n[0];
                            if (br(this.$vnode)) return i;
                            var o = gr(i);
                            if (!o) return i;
                            if (this._leaving) return _r(e, i);
                            var s = "__transition-" + this._uid + "-";
                            o.key = null == o.key ? s + o.tag : a(o.key) ? 0 === String(o.key).indexOf(s) ? o.key : s + o.key : o.key;
                            var c = (o.data || (o.data = {})).transition = yr(this),
                                u = this._vnode,
                                l = gr(u);
                            if (o.data.directives && o.data.directives.some(function(e) {
                                    return "show" === e.name
                                }) && (o.data.show = !0), l && l.data && !$r(o, l)) {
                                var f = l && (l.data.transition = y({}, c));
                                if ("out-in" === r) return this._leaving = !0, te(f, "afterLeave", function() {
                                    t._leaving = !1, t.$forceUpdate()
                                }), _r(e, i);
                                if ("in-out" === r) {
                                    var p, d = function() {
                                        p()
                                    };
                                    te(c, "afterEnter", d), te(c, "enterCancelled", d), te(f, "delayLeave", function(e) {
                                        p = e
                                    })
                                }
                            }
                            return i
                        }
                    }
                },
                hs = y({
                    tag: String,
                    moveClass: String
                }, ds);
            delete hs.mode;
            var ms = {
                    props: hs,
                    render: function(e) {
                        for (var t = this.tag || this.$vnode.data.tag || "span", n = Object.create(null), r = this.prevChildren = this.children, i = this.$slots["default"] || [], o = this.children = [], a = yr(this), s = 0; s < i.length; s++) {
                            var c = i[s];
                            if (c.tag)
                                if (null != c.key && 0 !== String(c.key).indexOf("__vlist")) o.push(c), n[c.key] = c, (c.data || (c.data = {})).transition = a;
                                else;
                        }
                        if (r) {
                            for (var u = [], l = [], f = 0; f < r.length; f++) {
                                var p = r[f];
                                p.data.transition = a, p.data.pos = p.elm.getBoundingClientRect(), n[p.key] ? u.push(p) : l.push(p)
                            }
                            this.kept = e(t, null, u), this.removed = l
                        }
                        return e(t, null, o)
                    },
                    beforeUpdate: function() {
                        this.__patch__(this._vnode, this.kept, !1, !0), this._vnode = this.kept
                    },
                    updated: function() {
                        var e = this.prevChildren,
                            t = this.moveClass || (this.name || "v") + "-move";
                        if (e.length && this.hasMove(e[0].elm, t)) {
                            e.forEach(wr), e.forEach(xr), e.forEach(Cr);
                            var n = document.body;
                            n.offsetHeight;
                            e.forEach(function(e) {
                                if (e.data.moved) {
                                    var n = e.elm,
                                        r = n.style;
                                    Xn(n, t), r.transform = r.WebkitTransform = r.transitionDuration = "", n.addEventListener(ts, n._moveCb = function i(e) {
                                        e && !/transform$/.test(e.propertyName) || (n.removeEventListener(ts, i), n._moveCb = null, er(n, t))
                                    })
                                }
                            })
                        }
                    },
                    methods: {
                        hasMove: function(e, t) {
                            if (!Ya) return !1;
                            if (null != this._hasMove) return this._hasMove;
                            var n = e.cloneNode();
                            e._transitionClasses && e._transitionClasses.forEach(function(e) {
                                Gn(n, e)
                            }), Zn(n, t), n.style.display = "none", this.$el.appendChild(n);
                            var r = nr(n);
                            return this.$el.removeChild(n), this._hasMove = r.hasTransform
                        }
                    }
                },
                gs = {
                    Transition: vs,
                    TransitionGroup: ms
                };
            wt.config.mustUseProp = ma, wt.config.isReservedTag = Oa, wt.config.isReservedAttr = va, wt.config.getTagNamespace = Ft, wt.config.isUnknownElement = Bt, y(wt.options.directives, ps), y(wt.options.components, gs), wt.prototype.__patch__ = ao ? us : b, wt.prototype.$mount = function(e, t) {
                return e = e && ao ? Ht(e) : void 0, $e(this, e, t)
            }, setTimeout(function() {
                to.devtools && $o && $o.emit("init", wt)
            }, 0);
            var ys, _s = !!ao && kr("\n", "&#10;"),
                bs = p("area,base,br,col,embed,frame,hr,img,input,isindex,keygen,link,meta,param,source,track,wbr"),
                $s = p("colgroup,dd,dt,li,options,p,td,tfoot,th,thead,tr,source"),
                ws = p("address,article,aside,base,blockquote,body,caption,col,colgroup,dd,details,dialog,div,dl,dt,fieldset,figcaption,figure,footer,form,h1,h2,h3,h4,h5,h6,head,header,hgroup,hr,html,legend,li,menuitem,meta,optgroup,option,param,rp,rt,source,style,summary,tbody,td,tfoot,th,thead,title,tr,track"),
                xs = /([^\s"'<>\/=]+)/,
                Cs = /(?:=)/,
                ks = [/"([^"]*)"+/.source, /'([^']*)'+/.source, /([^\s"'=<>`]+)/.source],
                As = new RegExp("^\\s*" + xs.source + "(?:\\s*(" + Cs.source + ")\\s*(?:" + ks.join("|") + "))?"),
                Os = "[a-zA-Z_][\\w\\-\\.]*",
                Ss = "((?:" + Os + "\\:)?" + Os + ")",
                Ts = new RegExp("^<" + Ss),
                Es = /^\s*(\/?)>/,
                js = new RegExp("^<\\/" + Ss + "[^>]*>"),
                Ns = /^<!DOCTYPE [^>]+>/i,
                Ls = /^<!--/,
                Is = /^<!\[/,
                Ds = !1;
            "x".replace(/x(.)?/g, function(e, t) {
                Ds = "" === t
            });
            var Ms, Ps, Rs, Fs, Bs, Hs, Us, Vs, zs, Js, Ks, qs, Ws, Zs, Gs, Ys, Qs, Xs, ec = p("script,style,textarea", !0),
                tc = {},
                nc = {
                    "&lt;": "<",
                    "&gt;": ">",
                    "&quot;": '"',
                    "&amp;": "&",
                    "&#10;": "\n"
                },
                rc = /&(?:lt|gt|quot|amp);/g,
                ic = /&(?:lt|gt|quot|amp|#10);/g,
                oc = /\{\{((?:.|\n)+?)\}\}/g,
                ac = /[-.*+?^${}()|[\]\/\\]/g,
                sc = h(function(e) {
                    var t = e[0].replace(ac, "\\$&"),
                        n = e[1].replace(ac, "\\$&");
                    return new RegExp(t + "((?:.|\\n)+?)" + n, "g")
                }),
                cc = /^@|^v-on:/,
                uc = /^v-|^@|^:/,
                lc = /(.*?)\s+(?:in|of)\s+(.*)/,
                fc = /\((\{[^}]*\}|[^,]*),([^,]*)(?:,([^,]*))?\)/,
                pc = /:(.*)$/,
                dc = /^:|^v-bind:/,
                vc = /\.[^.]+/g,
                hc = h(Ar),
                mc = /^xmlns:NS\d+/,
                gc = /^NS\d+:/,
                yc = h(Yr),
                _c = /^\s*([\w$_]+|\([^)]*?\))\s*=>|^function\s*\(/,
                bc = /^\s*[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*|\['.*?']|\[".*?"]|\[\d+]|\[[A-Za-z_$][\w$]*])*\s*$/,
                $c = {
                    esc: 27,
                    tab: 9,
                    enter: 13,
                    space: 32,
                    up: 38,
                    left: 37,
                    right: 39,
                    down: 40,
                    delete: [8, 46]
                },
                wc = function(e) {
                    return "if(" + e + ")return null;"
                },
                xc = {
                    stop: "$event.stopPropagation();",
                    prevent: "$event.preventDefault();",
                    self: wc("$event.target !== $event.currentTarget"),
                    ctrl: wc("!$event.ctrlKey"),
                    shift: wc("!$event.shiftKey"),
                    alt: wc("!$event.altKey"),
                    meta: wc("!$event.metaKey"),
                    left: wc("'button' in $event && $event.button !== 0"),
                    middle: wc("'button' in $event && $event.button !== 1"),
                    right: wc("'button' in $event && $event.button !== 2")
                },
                Cc = {
                    bind: si,
                    cloak: b
                },
                kc = (new RegExp("\\b" + "do,if,for,let,new,try,var,case,else,with,await,break,catch,class,const,super,throw,while,yield,delete,export,import,return,switch,default,extends,finally,continue,debugger,function,arguments".split(",").join("\\b|\\b") + "\\b"), new RegExp("\\b" + "delete,typeof,void".split(",").join("\\s*\\([^\\)]*\\)|\\b") + "\\s*\\([^\\)]*\\)"), {
                    staticKeys: ["staticClass"],
                    transformNode: Ii,
                    genData: Di
                }),
                Ac = {
                    staticKeys: ["staticStyle"],
                    transformNode: Mi,
                    genData: Pi
                },
                Oc = [kc, Ac],
                Sc = {
                    model: Nn,
                    text: Ri,
                    html: Fi
                },
                Tc = {
                    expectHTML: !0,
                    modules: Oc,
                    directives: Sc,
                    isPreTag: Aa,
                    isUnaryTag: bs,
                    mustUseProp: ma,
                    canBeLeftOpenTag: $s,
                    isReservedTag: Oa,
                    getTagNamespace: Ft,
                    staticKeys: $(Oc)
                },
                Ec = Li(Tc),
                jc = Ec.compileToFunctions,
                Nc = h(function(e) {
                    var t = Ht(e);
                    return t && t.innerHTML
                }),
                Lc = wt.prototype.$mount;
            wt.prototype.$mount = function(e, t) {
                if (e = e && Ht(e), e === document.body || e === document.documentElement) return this;
                var n = this.$options;
                if (!n.render) {
                    var r = n.template;
                    if (r)
                        if ("string" == typeof r) "#" === r.charAt(0) && (r = Nc(r));
                        else {
                            if (!r.nodeType) return this;
                            r = r.innerHTML
                        }
                    else e && (r = Bi(e));
                    if (r) {
                        var i = jc(r, {
                                shouldDecodeNewlines: _s,
                                delimiters: n.delimiters
                            }, this),
                            o = i.render,
                            a = i.staticRenderFns;
                        n.render = o, n.staticRenderFns = a
                    }
                }
                return Lc.call(this, e, t)
            }, wt.compile = jc, e.exports = wt
        }).call(t, function() {
            return this
        }())
    }
});
window.installVueWx = function(e) {
    function t(o) {
        if (n[o]) return n[o].exports;
        var i = n[o] = {
            exports: {},
            id: o,
            loaded: !1
        };
        return e[o].call(i.exports, i, i.exports, t), i.loaded = !0, i.exports
    }
    var n = {};
    return t.m = e, t.c = n, t.p = "", t(0)
}([function(e, t, n) {
    function o(e) {
        return e && e.__esModule ? e : {
            default: e
        }
    }
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var i = n(10),
        r = o(i);
    t["default"] = r["default"], e.exports = t["default"]
}, , function(e, t) {
    ! function() {
        e.exports = window.vue
    }()
}, function(e, t, n) {
    function o(e) {
        return e && e.__esModule ? e : {
            default: e
        }
    }
    var i = Object.assign || function(e) {
        for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var o in n) Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
        }
        return e
    };
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var r = n(2),
        a = o(r);
    t["default"] = function(e) {
        function t(e) {
            return e && e.__extraState__ && e.__extraState__.lazyDataPrepared
        }

        function n(e, t) {
            return e && e.__extraState__ && e.__extraState__.lazyDataReceived && e.__extraState__.lazyDataReceived[t]
        }

        function o(e) {
            var t = e.top,
                n = e.bottom;
            return p = p || window.innerHeight, !(t > p || n < 0)
        }

        function r(e) {
            var t = "";
            if (e && "[object Object]" == Object.prototype.toString.call(e)) {
                var n = Object.keys(e);
                n && n.length && n.sort().forEach(function(n) {
                    t += n + "=" + e[n] + ";"
                })
            }
            return t
        }

        function c() {
            return "_" + parseInt(new Date)
        }
        var u = {
                mce: {
                    url: "//mce.mogucdn.com/jsonp/multiget/3",
                    backupUrl: "//mce.mogujie.com/jsonp/multiget/3",
                    param: "pids",
                    backupParam: "pids",
                    type: "jsonp"
                },
                mceonly: {
                    url: "//mce.mogucdn.com/jsonp/get/3",
                    backupUrl: "//mce.mogujie.com/jsonp/get/3",
                    param: "pid",
                    backupParam: "pid",
                    type: "jsonp"
                },
                mceonline: {
                    url: "mwp.darwin.multiget",
                    versionNum: "3",
                    backupUrl: "//mcebackup.mogucdn.com/jsonp/multiget/3",
                    param: "pids",
                    backupParam: "pids",
                    type: "mwp"
                },
                mceats: {
                    url: "//mce.mogucdn.com/jsonp/multiget/3",
                    backupUrl: "//mce.mogujie.com/jsonp/multiget/3",
                    param: "pids",
                    backupParam: "pids",
                    type: "jsonp"
                },
                makeup: {
                    url: "mwp.darwin.makeup",
                    versionNum: "3",
                    backupUrl: "//mcebackup.mogucdn.com/jsonp/makeup/3",
                    param: "pid",
                    backupParam: "pid",
                    type: "mwp"
                },
                mceonlyonline: {
                    url: "mwp.darwin.get",
                    versionNum: "3",
                    backupUrl: "//mcebackup.mogucdn.com/jsonp/get/3",
                    param: "pid",
                    backupParam: "pid",
                    type: "mwp"
                },
                mcereconline: {
                    url: "mwp.darwin.multiget",
                    versionNum: "3",
                    backupUrl: "//mcebackup.mogucdn.com/jsonp/multiget/3",
                    param: "pids",
                    backupParam: "pids",
                    type: "mwp"
                },
                mcereconlyonline: {
                    url: "mwp.darwin.get",
                    versionNum: "3",
                    backupUrl: "//mcebackup.mogucdn.com/jsonp/get/3",
                    param: "pid",
                    backupParam: "pid",
                    type: "mwp"
                }
            },
            l = window.MWP || window.M.MWP,
            s = 20,
            d = 80,
            f = {
                loading: 1,
                success: 2,
                paging: 3,
                error: 4
            },
            p = void 0,
            h = {
                timeout: 8e3,
                items: [],
                _cache: {},
                _contextCache: {},
                _ajaxMap: {},
                _hasReRendered: !1,
                _loadComplete: !1,
                init: function() {
                    this._loadComplete = !1, this._hasReRendered = !1, this.walkModules(), this.prepareAjaxData(), this.loadAjaxData(), this.bindEvent()
                },
                walkModules: function() {
                    var t = [],
                        o = e.$components;
                    for (var i in o) {
                        var r = o[i],
                            a = r.config.formData;
                        for (var c in a) {
                            var u = a[c] && a[c].models;
                            if (u && u.length)
                                for (var l in u) {
                                    var s = u[l];
                                    if (s) {
                                        var d = s.sourceKey;
                                        d && s.sourceType && !n(r, d) && !s["request-self"] && t.push({
                                            vm: r,
                                            elm: r.$el,
                                            sourceKey: d,
                                            sourceType: s.sourceType,
                                            sourceAlone: s.sourceAlone,
                                            extraParam: s.extraParam,
                                            requestFirst: s.requestFirst,
                                            size: s.size
                                        })
                                    }
                                }
                        }
                    }
                    this.items = t
                },
                bindEvent: function() {
                    var e = this;
                    this._hasEventBind || (this._hasEventBind = !0, M.lib.PubSub.$on("__body-scroll__", function() {
                        e.loadAjaxData()
                    }))
                },
                prepareAjaxData: function(e) {
                    var n = this;
                    void 0 == this.mergeSize && (this.mergeSize = {}), void 0 == this.mergeIndex && (this.mergeIndex = {}), void 0 == this.typeOfparam && (this.typeOfparam = {}), this.items = this.items.filter(function(e) {
                        return !t(e.vm)
                    }), this.items.forEach(function(t, o) {
                        var a = t.size || s,
                            l = t.sourceAlone || "",
                            f = t.requestFirst || "",
                            p = t.extraParam || "",
                            h = t.elm.getBoundingClientRect(),
                            m = h.top,
                            g = h.bottom,
                            v = t.sourceType,
                            _ = e ? c() : "";
                        if (u[v] || console.warn("unknow data source type", v), n.mergeSize[v] = n.mergeSize[v] || 0, n.mergeIndex[v] = n.mergeIndex[v] || 1, n.mergeSize[v] += parseInt(a), n.mergeSize[v] > d && (n.mergeSize[v] = 0, n.mergeIndex[v]++), p) {
                            var w = r(p);
                            w && (n.typeOfparam[w] ? _ = typeOfparam[w] : typeOfparam[w] = _ = c())
                        }
                        if ((l || f) && (_ = c()), v = "makeup" == v ? v + "_" + t.sourceKey + _ : v + n.mergeIndex[v] + _, n._cache[v]) return n.emitData(n._cache[v], t, t.sourceKey, n._contextCache[v]), !1;
                        var b = i(u[t.sourceType], {
                            data: p
                        });
                        n._ajaxMap[v] = n._ajaxMap[v] || {
                            source: b,
                            type: v,
                            sourceType: t.sourceType,
                            refreshType: _,
                            requestFirst: f,
                            list: [],
                            top: m,
                            bottom: g
                        };
                        var y = n._ajaxMap[v];
                        y.list.push({
                            key: t.sourceKey,
                            elm: t.elm,
                            vm: t.vm,
                            param: null
                        }), y.top = Math.min(y.top, m), y.bottom = Math.max(y.bottom, g), t.vm.__extraState__.lazyDataPrepared = !0
                    })
                },
                updateAjaxMap: function(e) {
                    var t = this;
                    if (this._hasReRendered && (e = !0, this._hasReRendered = !1), !e) return !1;
                    var n = function(e) {
                        var n = t._ajaxMap[e],
                            o = [n.top],
                            i = [n.bottom];
                        if (n.status) return "continue";
                        n.list.map(function(e) {
                            var t = e.elm.getBoundingClientRect();
                            return e.top = t.top, e.bottom = t.bottom, o.push(e.top), i.push(e.bottom), e
                        });
                        var r = o.sort(function(e, t) {
                                return e - t
                            }),
                            a = i.sort(function(e, t) {
                                return e - t
                            });
                        n.top = r[0], n.bottom = a[a.length - 1]
                    };
                    for (var o in this._ajaxMap) {
                        n(o)
                    }
                },
                loadAjaxData: function() {
                    var e = this;
                    if (this.updateAjaxMap(!0), !this._loadComplete) {
                        var t = !1,
                            n = function(n) {
                                var r = {},
                                    a = e._ajaxMap[n],
                                    u = a.source,
                                    l = a.list.map(function(e) {
                                        return e.key
                                    }).filter(function(e) {
                                        return !r[e] && (r[e] = !0, !0)
                                    }).join(",");
                                if (a.status) return "continue";
                                if (t = !0, !o({
                                        top: a.top,
                                        bottom: a.bottom
                                    }) && !a.requestFirst) return "continue";
                                a.status = f.loading;
                                var s = i({}, u.data);
                                s[u.param] = l, s.appPlat = "m";
                                var d = "jsonp" + l.replace(/,/g, "_");
                                "function" == typeof window[d] && (d += c()), e.sendRequset(u, s, l, a, d)
                            };
                        for (var r in this._ajaxMap) {
                            n(r)
                        }
                        t || (this._loadComplete = !0)
                    }
                },
                sendRequset: function(e, t, n, o, r) {
                    var a = this,
                        c = function() {
                            var i = "jsonp" === e.type ? M.http.jsonp : M.http.get;
                            i(e.url, {
                                data: t,
                                timeout: a.timeout,
                                jsonpCallback: r
                            }).then(function(e) {
                                a.ajaxHandler(e, n, o)
                            })["catch"](function(e) {
                                a.ajaxRetry(e, n, o)
                            })
                        },
                        u = function(t) {
                            l && l.request(e.url, e.versionNum, t).then(function(e) {
                                if (e && e.ret && "SUCCESS" == e.ret) {
                                    var t = i({}, e);
                                    t.returnCode = e.ret, t.success = !0, a.ajaxHandler(t, n, o)
                                } else a.ajaxRetry(new Error(e && e.ret || "error return null"), n, o)
                            })["catch"](function(e) {
                                a.ajaxRetry(e, n, o)
                            })
                        };
                    "mwp" != e.type ? c() : u(t)
                },
                emitData: function(e, t, o, i) {
                    if (!n(t.vm, o)) {
                        t.vm.__extraState__.lazyDataReceived = t.vm.__extraState__.lazyDataReceived || {}, t.vm.__extraState__.lazyDataReceived[o] = !0, t.vm.$emit("__lazy-data__", e, o, i);
                        for (var r in t.vm.$children) {
                            var a = t.vm.$children[r];
                            a.$emit("__lazy-data__", e, o, i)
                        }
                    }
                },
                afterReceiveData: function(e, t) {
                    var n = this,
                        o = {},
                        r = {};
                    if ("makeup" == t.sourceType) {
                        o[t.type] = e, r[t.type] = {}, i(this._cache, o), i(this._contextCache, r);
                        for (var c in t.list) {
                            var u = t.list[c];
                            this._cache[t.type] && this.emitData(this._cache[t.type], u, u.key, this._contextCache[t.type])
                        }
                    } else {
                        for (var l in e) o[l + t.refreshType] = e[l].list, r[l + t.refreshType] = e[l].context;
                        i(this._cache, o), i(this._contextCache, r);
                        for (var s in t.list) {
                            var d = t.list[s],
                                p = d.key + t.refreshType;
                            this._cache[p] && this.emitData(this._cache[p], d, d.key, this._contextCache[p])
                        }
                    }
                    t.status = f.success, a["default"].nextTick(function() {
                        n._hasReRendered = !0, window.setTimeout(function() {
                            M && M.lib && M.lib.PubSub && M.lib.PubSub.$emit("__body-scroll__", null)
                        }, 0)
                    })
                },
                ajaxHandler: function(e, t, n) {
                    if (e && e.success && e.returnCode && "SUCCESS" == e.returnCode) {
                        var o = {};
                        "makeup" == n.sourceType ? o = e.data : e.data && e.data.list ? o[t] = e.data : o = e.data, this.afterReceiveData(o, n)
                    } else {
                        var i = new Error(e && e.returnCode || "error interface");
                        this.ajaxRetry(i, t, n)
                    }
                },
                ajaxRetry: function(e, t, n) {
                    var o = this;
                    console.warn("use backup url due to", e.toString());
                    var i = n.source;
                    return i.backupUrl ? void M.http.jsonp(i.backupUrl + ("mwp" === i.type ? "%3F" : "?") + i.backupParam + "=" + t + "&appPlat=m&callback=jsonp" + t.replace(/,/g, "_") + "backup", {
                        jsonpCallback: "jsonp" + t.replace(/,/g, "_") + "backup",
                        cache: !0,
                        timeout: 8e3
                    }).then(function(e) {
                        o.ajaxHandler(e, t, n)
                    }) : (console.warn("no backupUrl"), !1)
                }
            };
        h.init(), e.LazyData = h
    }
}, function(e, t, n) {
    var o = Object.assign || function(e) {
        for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var o in n) Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
        }
        return e
    };
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    n(5);
    t["default"] = function(e) {
        function t(e) {
            var t = e.__logData__[w],
                n = (t || "").split(";");
            n.forEach(function(e) {
                var t = e.split("=");
                if (t[0] && t[1]) {
                    var n = t[0];
                    B = B || {}, B[n] = B[n] || [], B[n].push(t[1])
                }
            })
        }

        function n(e) {
            var t = {};
            if (e) {
                var n = e.split(";");
                for (var o in n) {
                    var i = n[o],
                        r = i.split("=");
                    t[r[0]] = r[1]
                }
            }
            return t
        }

        function i(e) {
            var t = [];
            return e.child ? t = t.concat(i(e.child._vnode)) : (t.push(e), e.children && e.children.forEach(function(e) {
                t = t.concat(i(e))
            })), t
        }

        function r() {
            var t = e.$components;
            t.forEach(function(e, t) {
                var n = e.$el,
                    o = !1,
                    r = e.__extraState__ && e.__extraState__.acm || "",
                    a = e.__extraState__ && e.__extraState__.moduleNode,
                    c = n.__logData__ && n.__logData__[x] || "";
                try {
                    o = !!e.$root.$children[0].$options._alwaysShow
                } catch (u) {}
                for (var l = a.querySelectorAll(".anchor") || [], s = 0; s < l.length; s++)(!l[s].className || l[s].className && l[s].className.indexOf("has-log-mod") === -1) && (l[s].className += " has-log-mod");
                if (!(r.indexOf(".") <= 0)) {
                    var d = r.split(".");
                    if (f(n) || o) {
                        var p = i(e._vnode).filter(function(e) {
                                var t = e.elm;
                                return t && t.__logData__ && !t.__hasLoged__ && (t.__logData__[g] || t.__logData__[k] || t.__logData__[v])
                            }),
                            h = a.querySelectorAll(".anchor") || [];
                        e.__extraState__[C] || (L.push(r + "-mfs_" + p.length), E.push(t), e.__extraState__[C] = !0);
                        var m = p.length + h.length;
                        if (m) {
                            var S = [],
                                M = [],
                                j = [];
                            p.forEach(function(e, t) {
                                var n = e.elm,
                                    o = !n.__logData__[_] && n.__logData__[w] || "",
                                    i = n.__logData__[b] || "",
                                    a = n.__logData__[y] || "";
                                if (!n[C] && f(n))
                                    if (a && $.push(a), o && d[6]) {
                                        var u = c ? S : q,
                                            l = c ? j : R,
                                            s = c ? M : U;
                                        u.push(o + "-" + d[6] + "-idx_" + t + "-mfs_" + m), l.push(t), i && s.push(i), n[C] = !0
                                    } else N.push(r + "-idx_" + t + "-mfs_" + m), D.push(t), n[C] = !0
                            });
                            for (var P = 0; P < h.length; P++)
                                if (!h[P].__hasLoged__) {
                                    var O = p.length + P;
                                    N.push(r + "-idx_" + O + "-mfs_" + m), D.push(O), h[P].__hasLoged__ = !0
                                }
                            c && S.length && z.push({
                                acms: S,
                                iids: M,
                                idx: j,
                                params: c
                            })
                        }
                    }
                }
            })
        }

        function a() {
            var n = e.$components;
            n.forEach(function(e, n) {
                var o = (e.$el, i(e._vnode).filter(function(e) {
                    var t = e.elm;
                    return t && t.__logData__ && t.__logData__[S]
                }));
                o.forEach(function(e) {
                    var n = e.elm,
                        o = i(e).filter(function(e) {
                            var t = e.elm;
                            return t && t.__logData__ && t.__logData__[_]
                        });
                    o.length ? o.forEach(function(e, o) {
                        var i = e.elm;
                        if (f(i) || i[j]) {
                            if (i[j] = !1, T && T !== n.__logData__.eventid) return n[j] = !0, void(i[j] = !0);
                            i.__logData__[_] && t(i), T = n.__logData__.eventid, delete i.__logData__[_]
                        }
                    }) : delete n.__logData__[S]
                })
            })
        }

        function c(e, t) {
            var n = window && window.logger && window.logger.log;
            n && n(e, t)
        }

        function u() {
            if (L && L.length) L.splice(0, P), E.splice(0, P);
            else if (N && N.length) c("0x00000000", {
                acms: N.splice(0, P),
                indexs: D.splice(0, P),
                type: 5,
                ver: O || ""
            });
            else if (q && q.length) c("0x00000000", {
                acms: q.splice(0, P),
                indexs: R.splice(0, P),
                type: 4,
                iids: U.splice(0, P),
                ver: O || ""
            });
            else if (B) B.ver = O || "", c(T || "0x00000000", B), B = null, T = null;
            else if (I && I.length) c(T || "0x00000000", {
                acms: I.splice(0, P),
                iids: U.splice(0, P),
                indexs: W.splice(0, P),
                ver: O || ""
            }), T = null;
            else if (z && z.length) {
                var e = z.shift();
                c("0x00000000", o({
                    acms: e.acms,
                    indexs: e.idx,
                    iids: e.iids,
                    ver: O || ""
                }, n(e.params)))
            } else $ && $.length && c("70005", {
                cparams: $.splice(0, P)
            })
        }

        function l() {
            (I.length || L.length || N.length || q.length || z.length || $.length || B) && (p(u), A = !0, setTimeout(function() {
                I.length || L.length || N.length || q.length || z.length || $.length || B ? l() : A = !1
            }, 1e3))
        }

        function s() {
            r(), a(), (I.length || L.length || N.length || q.length || B || $.length || z.length) && !A && l()
        }

        function d() {
            M.lib.PubSub.$on("__body-scroll__", function() {
                s()
            }), s()
        }

        function f(e) {
            if (e.getBoundingClientRect) {
                var t = (M.scope.cube._body, e.getBoundingClientRect()),
                    n = t.top,
                    o = t.bottom,
                    i = t.left,
                    r = t.right;
                return F = F || window.innerHeight, V = V || window.innerWidth, !(n > F || o < 0 || i > V || r < 0)
            }
            return !1
        }

        function p(e) {
            O ? e(O) : M.ua["native"] && M.h5 && M.h5.hdp ? (M.h5.hdp.exec("mgj.device.getInfo").then(function(t) {
                O = t.appVersion, e(O)
            })["catch"](function(t) {
                e("")
            }), setTimeout(function() {
                O = O || "unknow"
            }, 5e3)) : e("")
        }

        function h(e, t) {
            c("0x00000000", {
                acms: e,
                indexs: t,
                type: 5,
                ver: O || ""
            })
        }

        function m(e, t, n) {
            c("0x00000000", {
                acms: e,
                indexs: t,
                type: 4,
                iids: n,
                ver: O || ""
            })
        }
        var g = "cube-acm-node",
            v = "anchor",
            _ = "log-custom",
            w = "data-log-content",
            b = "data-log-iid",
            y = "data-log-cparam",
            x = "custom-param",
            S = "rec-show-log",
            k = "show-log-item",
            C = "__has-log-mod__",
            j = "__waiting-log__",
            P = 50,
            O = "",
            A = !1,
            T = null,
            I = [],
            E = [],
            D = [],
            R = [],
            B = null,
            L = [],
            N = [],
            q = [],
            z = [],
            $ = [],
            U = [],
            W = [],
            F = void 0,
            V = void 0;
        d(), e.appVer = O, e.pitLog = h, e.goodLog = m, e.showLog = s
    }
}, function(e, t) {
    function n(e) {
        for (var t = null; e && 9 != e.nodeType;) {
            if (e.className && e.className.indexOf("module_row") != -1) {
                t = e;
                break
            }
            e = e.parentNode
        }
        return t
    }

    function o(e) {
        for (var t = null; e && 9 != e.nodeType;) e && e.getAttribute && e.getAttribute("acm") && (t = e), e = e.parentNode;
        return t
    }

    function i(e) {
        return e && e.className && e.className.indexOf("anchor") != -1
    }

    function r() {
        if (window.M && !window.M.SILoaded) {
            var e = window.document.createElement("script");
            e.onload = function() {
                window.M.SILoaded = !0
            }, e.src = "https://shieldironman.mogujie.com/coa", window.document.head.appendChild(e)
        }
    }

    function a(e) {
        var t = e || {},
            n = window._v_pa ? window._v_pa : "",
            o = window._f_pa ? window._f_pa : "";
        return t.proba = n, t.probb = o, t.platform = "h5", t
    }

    function c() {
        var e = window._v_pa || "",
            t = window._f_pa || "",
            n = "h5",
            o = new Promise(function(o, i) {
                o({
                    proba: e,
                    probb: t,
                    platform: n
                })
            });
        return o
    }

    function u() {
        if (null === v) {
            v = window.document.body.clientWidth;
            var e = window.navigator.userAgent.toLowerCase();
            if (e.indexOf("android") > -1 && e.indexOf("screenwidthresolution") > -1 && e.indexOf("screendensity") > -1) {
                var t = /screenwidthresolution=(\d*)/,
                    n = /screendensity=([\d|\.]*)/,
                    o = 0,
                    i = 1,
                    r = e.match(t);
                r && r[1] && !isNaN(r[1]) && (o = +r[1]);
                var a = e.match(n);
                a && a[1] && !isNaN(a[1]) && (i = +a[1]), 0 !== o && (v = Math.round(o / i))
            }
        }
        return v
    }

    function l(e) {
        return Math.round(e * u() / g)
    }

    function s(e, t, n) {
        var o = void 0;
        return e[t] && "function" == typeof e[t] && (o = e[t].call(e, n)), e.$children && e.$children.forEach(function(e) {
            var i = s(e, t, n);
            o || (o = i)
        }), o
    }

    function d(e) {
        return void 0 !== e && null !== e && (document.documentElement.scrollTop = e, document.body.scrollTop = e), document.documentElement.scrollTop || document.body.scrollTop
    }

    function f(e) {
        return void 0 !== e && null !== e && (document.documentElement.scrollLeft = e, document.body.scrollLeft = e), document.documentElement.scrollLeft || document.body.scrollLeft
    }

    function p(e) {
        return (e + "").replace(/([A-Z])/g, function(e, t, n) {
            return 0 === n ? e.toLowerCase() : "-" + e.toLowerCase()
        })
    }

    function h(e) {
        var t = void 0,
            n = [];
        if ("string" != typeof e) try {
            var o = e;
            Object.keys(o).forEach(function(e) {
                var t = p(e);
                n.push(t + ":" + o[e])
            }), t = n.join(";") + ";"
        } catch (i) {
            return ""
        } else t = e;
        if (!t || !t.split) return t;
        var r = t.split(";");
        return r = (r || []).map(function(e) {
            var t = e.split(":");
            if (t && t.length > 1) {
                var n = t[1].split(" ");
                n = (n || []).map(function(e) {
                    return e = e.replace(/rpx/g, "px"), e.indexOf("px") != -1 ? e.replace(/(([+-]?)\d*(\.?\d*))px/g, function(e, t) {
                        return t / 100 + "rem"
                    }).trim() : e
                }), t[1] = n.join(" ")
            }
            return t.join(":")
        }), r.join(";")
    }

    function m(e) {
        return e && e.formData && Object.keys(e.formData).forEach(function(t) {
            t && e.formData[t] && (e[t] = e.formData[t].models)
        }), e
    }
    Object.defineProperty(t, "__esModule", {
        value: !0
    }), t.findModParent = n, t.findAcmParent = o, t.isAnchorNode = i, t.initShieldIronman = r, t.addShieldParam = a, t.getShieldParam = c, t.Ruler = l, t.callMethodRecursive = s, t.bodyScrollTop = d, t.bodyScrollLeft = f, t.kebabize = p, t.transformStyleCode = h, t.formatModuleConfig = m;
    var g = 750,
        v = null
}, function(e, t, n) {
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var o = n(5);
    t["default"] = function(e) {
        function t(e, t) {
            t = t.split("#")[0];
            var n = new RegExp("(^|\\?|&)" + e + "=([^&]*)(\\s|&|$)", "i");
            return n.test(t) ? RegExp.$2.replace(/\+/g, " ") : ""
        }

        function n(e, t, n, o, i) {
            var r = "",
                a = t;
            if (e && (e = e.split(".")), e && a.indexOf("mf_") === -1) {
                var c = e[6] ? "-" + e[6] : "";
                r = a + (a ? c : e.join("."))
            }
            return r && (r += "-idx_" + n), r && o && (r += "-mfs_" + o), i ? {
                acm: r || a,
                cparam: i || ""
            } : {
                acm: r || a
            }
        }

        function i(e) {
            for (var t = e.querySelectorAll("*"), n = [], i = 0; i < t.length; i++) t[i] && (t[i].__logData__ || (0, o.isAnchorNode)(t[i])) && n.push(t[i]);
            return n
        }
        window.PTP_PARAMS = window.PTP_PARAMS || {};
        var r = window.PTP_PARAMS.urlExtendFn;
        window.PTP_PARAMS.urlExtendFn = function(e) {
            if (!window.PTP_PARAMS.urlExtendFn || !e.getAttribute("acm") && !e.__hasLoged__) return r(e);
            var a = (0, o.findModParent)(e),
                c = e.__logData__ || (0, o.isAnchorNode)(e) ? e : null,
                u = a.getAttribute("data-acm") || "",
                l = e.getAttribute("href"),
                s = l && l.indexOf("acm=") != -1,
                d = l && l.indexOf("cparam=") != -1,
                f = e.getAttribute("acm") || "",
                p = e.getAttribute("data-cparam") || "",
                h = 0,
                m = 0;
            if (!c) {
                for (var g = e; null != g && 9 != g.nodeType && !g.__logData__;) g = g.parentNode;
                c = g
            }
            if (!c || 9 == c.nodeType) return {
                acm: f
            };
            if (s) {
                if (l && l.indexOf("mf_") >= 0) return;
                f || (f = t("acm", l))
            }
            if (u) {
                var v = i(a);
                if (m = v.length)
                    for (var _ = 0; _ < v.length; _++)
                        if (v[_] == c) {
                            h = _;
                            break
                        }
                return n(u, f, h, m, d ? "" : p)
            }
        }
    }
}, function(e, t, n) {
    function o(e) {
        return e && e.__esModule ? e : {
            default: e
        }
    }
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var i = n(2),
        r = o(i),
        a = n(5);
    t["default"] = function(e) {
        var t = {
            imgKeyArr: ["80", "100", "160", "180", "200", "240", "280", "300", "320", "360", "400", "440", "480", "520", "540", "560", "600", "640"],
            imgKeyMap: {
                80: {
                    "1:1": "80x80",
                    "7:9": "80x103",
                    "3:4": "80x107",
                    "2:3": "80x120",
                    999: "80x999"
                },
                100: {
                    "1:1": "100x100",
                    "7:9": "100x129",
                    "3:4": "100x134",
                    "2:3": "100x150",
                    999: "100x999"
                },
                160: {
                    "1:1": "160x160",
                    "7:9": "160x206",
                    "3:4": "160x214",
                    "2:3": "160x240",
                    999: "160x999"
                },
                180: {
                    "1:1": "180x180",
                    "7:9": "180x232",
                    "3:4": "180x240",
                    "2:3": "180x270",
                    999: "180x999"
                },
                200: {
                    "1:1": "200x200",
                    "7:9": "200x258",
                    "3:4": "200x268",
                    "2:3": "200x300",
                    999: "200x999"
                },
                240: {
                    "1:1": "240x240",
                    "7:9": "240x308",
                    "3:4": "240x320",
                    "2:3": "240x360",
                    999: "240x999"
                },
                280: {
                    "1:1": "280x280",
                    "7:9": "280x360",
                    "3:4": "280x374",
                    "2:3": "280x420",
                    999: "280x999"
                },
                300: {
                    "1:1": "300x300",
                    "7:9": "300x386",
                    "3:4": "300x400",
                    "2:3": "300x450",
                    999: "300x999"
                },
                320: {
                    "1:1": "320x320",
                    "7:9": "320x412",
                    "3:4": "320x428",
                    "2:3": "320x480",
                    999: "320x999"
                },
                360: {
                    "1:1": "360x360",
                    "7:9": "360x463",
                    "3:4": "360x480",
                    "2:3": "360x540",
                    999: "360x999"
                },
                400: {
                    "1:1": "400x400",
                    "7:9": "400x515",
                    "3:4": "400x534",
                    "2:3": "400x600",
                    999: "400x999"
                },
                440: {
                    "1:1": "440x440",
                    "7:9": "440x566",
                    "3:4": "440x587",
                    "2:3": "440x660",
                    999: "440x999"
                },
                480: {
                    "1:1": "480x480",
                    "7:9": "480x618",
                    "3:4": "480x640",
                    "2:3": "480x720",
                    999: "480x999"
                },
                520: {
                    "1:1": "520x520",
                    "7:9": "520x670",
                    "3:4": "520x694",
                    "2:3": "520x780",
                    999: "520x999"
                },
                540: {
                    "1:1": "540x540",
                    "7:9": "540x695",
                    "3:4": "540x720",
                    "2:3": "540x810",
                    999: "540x999"
                },
                560: {
                    "1:1": "560x560",
                    "7:9": "560x720",
                    "3:4": "560x747",
                    "2:3": "560x840",
                    999: "560x999"
                },
                600: {
                    "1:1": "600x600",
                    "7:9": "600x772",
                    "3:4": "600x800",
                    "2:3": "600x900",
                    999: "600x999"
                },
                640: {
                    "1:1": "640x640",
                    "7:9": "640x824",
                    "3:4": "640x854",
                    "2:3": "640x960",
                    999: "640x999"
                }
            },
            imgQuality: 70,
            dprDefMaxWidth: 640,
            dprDefRatio: "999",
            defCode: "999x999.v1c0",
            clientHeight: null,
            clientWidth: null,
            dpr: 1,
            dprClentWidth: null,
            webpSupport: !1
        };
        t.init = function() {
            this.clientHeight = window.screen.height, this.clientWidth = window.screen.width, this.dpr = window.devicePixelRatio, this.dprClentWidth = this.clientWidth * this.dpr, this.webpSupport = localStorage.getItem("webpSupport"), this.checkSupportWebp(), this.webpPngSupport = this.webpPngSupport(), this.getAppInfo()
        }, t.getAppInfo = function() {
            var e = this;
            window.M && window.M.h5 && window.M.h5.hdp && M.h5.hdp.exec("mgj.device.getInfo").then(function(t) {
                t && t.networkType && 4 != t.networkType && 5 != t.networkType && (e.imgQuality = 50)
            })["catch"](function(e) {})
        }, t.checkSupportWebp = function() {
            var e = this,
                t = new Image;
            t.onload = function() {
                e.webpSupport = !0, localStorage.setItem("webpSupport", 1)
            }, t.onerror = function(t) {
                e.webpSupport = !1
            }, t.src = "data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA"
        }, t.getDefSuffix = function(e) {
            var t = !(arguments.length > 1 && void 0 !== arguments[1]) || arguments[1],
                n = "",
                o = this.dprClentWidth;
            return o <= 375 ? n = "375x9999.v1c7E" : 375 < o && o <= 750 ? n = "750x9999.v1c7E" : 750 < o && (n = "1125x9999.v1c7E"), this.getCodeSuffix(e, n, t)
        }, t.getWidthSuffix = function(e, t) {
            var n = !(arguments.length > 2 && void 0 !== arguments[2]) || arguments[2],
                o = !(arguments.length > 3 && void 0 !== arguments[3]) || arguments[3],
                i = this.defCode,
                r = o ? this.dpr : 1,
                a = parseInt(t) * r;
            return a && a > 0 && a < 1950 && (a += 50, i = 100 * Math.ceil(a / 100) + "x9999.v1c7E"), this.getCodeSuffix(e, i, n)
        }, t.getGoodsRatioSuffix = function(e, t, n) {
            var o = !(arguments.length > 3 && void 0 !== arguments[3]) || arguments[3],
                i = !(arguments.length > 4 && void 0 !== arguments[4]) || arguments[4],
                r = this.defCode,
                a = "",
                c = ".v1cAC",
                u = i ? this.dpr : 1;
            switch (n) {
                case "1:1":
                case "7:9":
                case "3:4":
                case "2:3":
                    a = n;
                    break;
                default:
                    a = this.dprDefRatio, c = ".v1c96"
            }
            var l = parseInt(t) * u;
            (!l || l < 0 || l > this.dprDefMaxWidth) && (l = this.dprDefMaxWidth);
            for (var s in this.imgKeyArr) {
                var d = this.imgKeyArr[s];
                if (l <= d || d == this.dprDefMaxWidth) {
                    r = this.imgKeyMap[d][a] + c;
                    break
                }
            }
            return this.getCodeSuffix(e, r, o)
        }, t.getHalfSuffix = function(e) {
            var t = !(arguments.length > 1 && void 0 !== arguments[1]) || arguments[1],
                n = "";
            return this.dpr < 2 ? (n = "50000x50000.v1c7E", e = this.getCodeSuffix(e, n, t)) : e = this.getDefSuffix(e, t), e
        }, t.getCodeSuffix = function(e, t) {
            var n = !(arguments.length > 2 && void 0 !== arguments[2]) || arguments[2],
                o = e;
            if (!e || !t || "no" == t || e.indexOf(".webp") > 0 || e.indexOf(".gif") > 0) return e;
            if (e.indexOf("mogucdn") === -1) return e;
            if (e.indexOf(".jpg") < 0 && e.indexOf(".png") < 0) return e;
            if (e.indexOf(".jpg") > 0 && e.indexOf(".png") > 0) return e;
            if (e.indexOf(".png") > 0 && !this.webpPngSupport) return e;
            var i = "",
                r = e.split(".");
            if ("jpg" == r[r.length - 1]) i = "jpg";
            else {
                if ("png" != r[r.length - 1]) return e;
                i = "png"
            }
            t = "_" + t;
            var a = "." + this.imgQuality + ".";
            if (e.indexOf(".png_") < 0 && e.indexOf(".jpg_") < 0 && e.indexOf("." + i) == e.length - 4 && (e = e + t + a + i), this.webpSupport && n !== !1) {
                if (e.indexOf("." + i + "_") > 0) {
                    var c = e.split(".");
                    c[c.length - 1] == i && (c[c.length - 1] = "webp", e = c.join("."))
                }
            } else if ("png" == i) return o;
            return e
        }, t.getAddCodeUrl = function(e, n) {
            var o = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {},
                i = o["suffix-ratio"],
                r = o["suffix-code"],
                a = o["suffix-model"],
                c = "no" != o["use-webp"],
                u = o.mode;
            if (n = o["suffix-width"] ? o["suffix-width"] : n, (o["full-width-wrap"] || "no" == n) && (n = 9999), r) return t.getCodeSuffix(e, r, c);
            if ("goods" == u) {
                if ("1:1" == i || "7:9" == i || "3:4" == i || "2:3" == i) return t.getGoodsRatioSuffix(e, n, i, c)
            } else {
                if ("orig_narrow" == a) return t.getHalfSuffix(e, c);
                if ("width" == u) return t.getWidthSuffix(e, n, c);
                if ("no-resize" == u) return t.getCodeSuffix(e, "999x999.v1c0", c)
            }
            return t.getDefSuffix(e, c)
        }, t.webpPngSupport = function() {
            var e = !0,
                t = navigator.userAgent,
                n = t.match(/android\s([0-9\.]*)/i),
                o = null;
            return n && n[1] && (o = parseFloat(n[1])), o && o < 4.3 && (e = !1), e
        }, t.initDirective = function() {
            var e = function(e, n, o) {
                    return t ? t.getAddCodeUrl(e, n, o) : e
                },
                n = function(t, n, o, i) {
                    if ("image" !== o.tag && "img" !== o.tag || (t.setAttribute && (t._originSetAttribute || (t._originSetAttribute = t.setAttribute), t.setAttribute = function(t, n) {
                            var o = "no";
                            t.data && t.data.baseStyle && t.data.baseStyle.width && (o = (0, a.Ruler)(t.data.baseStyle.width));
                            var i = n.value;
                            return function(t, n) {
                                "src" === t && n.indexOf("mogucdn") > 0 && (n = e(n, o, i)), this._originSetAttribute(t, n)
                            }
                        }(o, n), o.data && o.data.attrs && o.data.attrs.src && o.data.attrs.src.indexOf("mogucdn") > 0 && (o.data.attrs.fixture && t.setAttribute("src", o.data.attrs.src), t.setAttribute("src", o.data.attrs.src))), t.setAttribution && (t._originSetAttribution || (t._originSetAttribution = t.setAttribution), t.setAttribution = function(t, n) {
                            var o = "no";
                            t.data && t.data.baseStyle && t.data.baseStyle.width && (o = (0, a.Ruler)(t.data.baseStyle.width));
                            var i = n.value;
                            return function(t) {
                                t && "string" == typeof t.src && t.src.indexOf("mogucdn") > 0 && (t.src = e(t.src, o, i)), this._originSetAttribution(t)
                            }
                        }(o, n))), o.tag.indexOf("mvw-image") != -1) {
                        var r = "no";
                        o.data && o.data.baseStyle && o.data.baseStyle.width && (r = (0, a.Ruler)(o.data.baseStyle.width));
                        var c = n.value;
                        if (o.componentInstance && o.componentInstance.src && o.componentInstance.src.indexOf("mogucdn") > 0) {
                            var u = o.componentInstance.src,
                                l = t.getAttribute("style");
                            l = l.replace(/background-image:(\s)*url\(([\S\s]*?)\)/g, "background-image:url(" + e(u, r, c) + ")"), t.setAttribute("style", l)
                        }
                    }
                    if (o.tag.indexOf("lazy-image") != -1) {
                        var r = "no";
                        o.data && o.data.baseStyle && o.data.baseStyle.width && (r = (0, a.Ruler)(o.data.baseStyle.width));
                        var c = n.value;
                        if (o.componentInstance && o.componentInstance.src && o.componentInstance.src.indexOf("mogucdn") > 0) {
                            var u = o.componentInstance.src;
                            o.componentInstance.codeSrc = e(u, r, c)
                        }
                    }
                },
                o = function(e, t, n, o) {
                    "image" !== n.tag && "img" !== n.tag || (e._originSetAttribute && (e.setAttribute = e._originSetAttribute), e._originSetAttribution && (e.setAttribution = e._originSetAttribution))
                };
            r["default"].directive("suffix", {
                bind: function(e, t, o, i) {
                    n(e, t, o, i)
                },
                update: function(e, t, o, i) {
                    n(e, t, o, i)
                },
                unbind: function(e, t, n, i) {
                    o(e, t, n, i)
                }
            })
        }, t.init(), t.initDirective(), e.ImgUrlTool = t
    }
}, function(e, t, n) {
    function o() {
        var e = document.documentElement.scrollTop || document.body.scrollTop,
            t = window.innerHeight,
            n = {};
        return n.top = e - t, n.bot = e + (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) + t, n.left = 0, n.right = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth, n.scrollTop = e, n
    }

    function i(e, t) {
        var n, o, i, r, a = t,
            c = a.getBoundingClientRect && a.getBoundingClientRect();
        c && (n = c.top + e.scrollTop, o = c.bottom + e.scrollTop, i = c.left, r = c.right);
        var u = o > e.top && n < e.bot,
            l = r > e.left && i < e.right;
        if (u && l) {
            var s = a.style;
            return !s || !("none" == s.display || "hidden" == s.visibility || "0" === s.opacity || !a.offsetWidth)
        }
        return !1
    }
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var r = n(5);
    t["default"] = function(e) {
        var t = e.$components,
            n = 300,
            a = function(e) {
                t && t.forEach(function(t) {
                    t.$el && i(e, t.$el) ? (0, r.callMethodRecursive)(t, "modInView", null) : (0, r.callMethodRecursive)(t, "modNotInView", null)
                })
            },
            c = void 0;
        M.lib.PubSub.$on("__body-scroll__", function() {
            window.clearTimeout(c), c = window.setTimeout(function() {
                var e = o();
                a(e)
            }, n)
        })
    }
}, function(e, t) {
    function n(e, t) {
        if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
    }
    var o = Object.assign || function(e) {
        for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var o in n) Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
        }
        return e
    };
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var i = function() {
            function e(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, o.key, o)
                }
            }
            return function(t, n, o) {
                return n && e(t.prototype, n), o && e(t, o), t
            }
        }(),
        r = function() {
            function e(t, o) {
                n(this, e), this.data = t || {}, this.callback = o
            }
            return i(e, [{
                key: "setGlobal",
                value: function(e) {
                    this.data = o(this.data, e), this.callGlobal(this.data)
                }
            }, {
                key: "getGlobal",
                value: function() {
                    return this.data
                }
            }, {
                key: "callGlobal",
                value: function(e) {
                    this.callback && this.callback(e)
                }
            }]), e
        }();
    t["default"] = r
}, function(e, t, n) {
    function o(e) {
        if (e && e.__esModule) return e;
        var t = {};
        if (null != e)
            for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && (t[n] = e[n]);
        return t["default"] = e, t
    }

    function i(e) {
        return e && e.__esModule ? e : {
            default: e
        }
    }

    function r() {
        U || (M.MWP && window.location.href.indexOf("__mwpEnv") == -1 && M.MWP.setGlobalEnv(M.MWP.Env.Release), d["default"].directive("log", {
            bind: function(e, t, n) {
                e.__logData__ = t.value
            }
        }), (0, w["default"])(M.scope.cube), U = !0)
    }

    function a(e, t) {
        if (d["default"] && e) {
            if (d["default"]._isInitConfig || (Object.defineProperty(d["default"].prototype, "config", {
                    get: function() {
                        return this && this.$root && this.$root.$options && this.$root.$options.config || {}
                    }
                }), Object.defineProperty(d["default"].prototype, "__extraState__", {
                    get: function() {
                        return this && this.$root && this.$root.$options && this.$root.$options.__extraState__ || {}
                    }
                }), Object.defineProperty(d["default"].prototype, "env", {
                    get: function() {
                        return {
                            M_ENV: window.M_ENV,
                            PAGE_STAGE: window.PAGE_STAGE,
                            MOGU_MF_DEVELOP_ENV: window.MOGU_MF_DEVELOP_ENV
                        }
                    }
                }), d["default"]._isInitConfig = !0), !d["default"]._isInitGlobalConfig) {
                var n = {};
                if (window.__moduleIdToSystemId && window._cubeConfig)
                    for (var o in window.__moduleIdToSystemId) {
                        var i = window.__moduleIdToSystemId[o];
                        if (i) {
                            var r = window && window._cubeConfig && window._cubeConfig["MCUBE_MOD_ID_" + i.originId][i.index];
                            n[o] = A.formatModuleConfig(JSON.parse(JSON.stringify(r)))
                        }
                    }
                for (var a = [], c = document.querySelectorAll(".module_row"), u = 0; u < c.length; u++) {
                    var s = c[u] && c[u].className || "",
                        f = s.match(/module_row_(\d*)/);
                    f && f.length && f[1] && (f = f[1], a.push(f))
                }
                var p = new C["default"]({
                    modulesData: n,
                    moduleIds: a
                }, function() {
                    M.scope.cube.$components.forEach(function(e) {
                        A.callMethodRecursive(e, "onGlobal", null)
                    })
                });
                Object.defineProperty(d["default"].prototype, "setGlobal", {
                    get: function() {
                        return function(e) {
                            p.setGlobal(e)
                        }
                    }
                }), Object.defineProperty(d["default"].prototype, "getGlobal", {
                    get: function() {
                        return function() {
                            return p.getGlobal()
                        }
                    }
                }), Object.defineProperty(d["default"].prototype, "vxCollectMwpRequest", {
                    get: function() {
                        return function(e, t, n) {
                            var o = e + "_" + t;
                            return window.__vx_mwpRequestQueue[o] || (window.__vx_mwpRequestQueue[o] = M.MWP.request(e, t, n)), window.__vx_mwpRequestQueue[o]
                        }
                    }
                }), Object.defineProperty(d["default"].prototype, "showToast", {
                    get: function() {
                        return I["default"].show.bind(I["default"])
                    }
                }), Object.defineProperty(d["default"].prototype, "hideToast", {
                    get: function() {
                        return I["default"].hide.bind(I["default"])
                    }
                }), Object.defineProperty(d["default"].prototype, "vxShowLoading", {
                    get: function() {
                        return D["default"].show.bind(D["default"])
                    }
                }), Object.defineProperty(d["default"].prototype, "vxHideLoading", {
                    get: function() {
                        return D["default"].hide.bind(D["default"])
                    }
                }), Object.defineProperty(d["default"].prototype, "vxShowDialog", {
                    get: function() {
                        return B["default"].show.bind(B["default"])
                    }
                }), Object.defineProperty(d["default"].prototype, "vxHideDialog", {
                    get: function() {
                        return B["default"].hide.bind(B["default"])
                    }
                }), Object.defineProperty(d["default"].prototype, "triggerLazyMotion", {
                    get: function() {
                        return function() {
                            window.setTimeout(function() {
                                M.lib.PubSub.$emit("__body-scroll__", null)
                            }, 0)
                        }
                    }
                }), Object.defineProperty(d["default"].prototype, "transformStyleCode", {
                    get: function() {
                        return A.transformStyleCode
                    }
                }), Object.defineProperty(d["default"].prototype, "$vm", {
                    get: function() {
                        return this
                    }
                }), Object.defineProperty(d["default"].prototype, "getShieldParam", {
                    get: function() {
                        return function() {
                            return {
                                platform: "h5",
                                _did: M.scope.cube._did || ""
                            }
                        }
                    }
                }), Object.defineProperty(d["default"].prototype, "$vx_getSystemInfo", {
                    get: function() {
                        var e = "",
                            t = "";
                        return window.M && window.M.ua && (e = M.ua.iphone ? "iOS " + M.ua.osVersion : "Android " + M.ua.osVersion, t = M.ua.iphone ? "ios" : "android"),
                            function() {
                                return {
                                    brand: "",
                                    model: "",
                                    pixelRatio: window.devicePixelRatio,
                                    screenWidth: window.screen.width,
                                    screenHeight: window.screen.height,
                                    windowWidth: window.screen.availWidth,
                                    windowHeight: window.screen.availHeight,
                                    language: "zh_CN",
                                    version: "",
                                    system: e,
                                    platform: t,
                                    fontSizeSetting: "",
                                    SDKVersion: ""
                                }
                            }
                    }
                }), Object.defineProperty(d["default"].prototype, "$logE", {
                    get: function() {
                        return window && window.logger && window.logger.log
                    }
                }), d["default"]._isInitGlobalConfig = !0
            }
            if (!d["default"]._isInitShareConfig) {
                Object.defineProperty(d["default"].prototype, "setScrollInfo", {
                    get: function() {
                        return function(e) {
                            if (window.__vx_scrollInfo = e, e && e.scrollIntoView) {
                                var t = window.document.querySelector("#" + e.scrollIntoView);
                                if (t) {
                                    var n = t.getBoundingClientRect();
                                    A.bodyScrollTop(window.pageYOffset + n.top)
                                }
                            } else e && e.scrollTop && A.bodyScrollTop(e.scrollTop)
                        }
                    }
                }), Object.defineProperty(d["default"].prototype, "setShareInfo", {
                    get: function() {
                        return function(e) {
                            window.__vx_shareInfo = l({}, window.__vx_shareInfo, e), window && window.M && window.M.h5 && window.M.h5.share && M.scope.cube._setShareInfo && M.scope.cube._setShareInfo()
                        }
                    }
                });
                var h = function(e, t, n) {
                    var o = n,
                        i = e;
                    "string" != typeof e && (o = e, i = o.target && o.target.href);
                    var r = i;
                    r = o ? logger && logger.generatePtpParams(i, N(o.target)) : logger && logger.generatePtpParams(i), window.location.href = r
                };
                Object.defineProperty(d["default"].prototype, "vx_navigate", {
                    get: function() {
                        return h
                    }
                }), Object.defineProperty(d["default"].prototype, "vx_redirect", {
                    get: function() {
                        return h
                    }
                }), Object.defineProperty(d["default"].prototype, "vx_launch", {
                    get: function() {
                        return h
                    }
                }), d["default"]._isInitShareConfig = !0
            }
            var m = /MCUBE_MOD_ID_(\d*)/,
                g = /MOD_ID_(\d*)/,
                v = /module_row_(\d*)/,
                _ = t.match(m);
            if (!_ || !_.length || !_[1]) throw new Error("\u4e0d\u5141\u8bb8\u4f20\u5165\u4e0d\u5305\u542b\u6a21\u5757id\u7684\u9009\u62e9\u7b26\uff0c\u53ef\u80fd\u9020\u6210\u6a21\u5757\u95f4\u7684\u51b2\u7a81");
            var w = 0,
                b = document.querySelectorAll(t),
                y = Array.prototype.slice.call(b);
            y.forEach(function(t) {
                var n = L(t),
                    o = n.getAttribute("class"),
                    i = void 0,
                    r = void 0,
                    a = _[1];
                o && (i = o.match(g), r = o.match(v)), i && i.length && i[1] && (a = i[1]), r && r.length && r[1] && (r = r[1]);
                var c = {};
                if (window.__moduleIdToSystemId && r) {
                    var u = window.__moduleIdToSystemId[r];
                    c = window && window._cubeConfig && window._cubeConfig["MCUBE_MOD_ID_" + u.originId][u.index]
                } else c = window && window._cubeConfig && window._cubeConfig["MCUBE_MOD_ID_" + a] && window._cubeConfig["MCUBE_MOD_ID_" + a][w];
                c && c.formData && (c = A.formatModuleConfig(JSON.parse(JSON.stringify(c)))), M.scope.cube.$components.push(new d["default"]({
                    __extraState__: {
                        moduleNode: n,
                        acm: n && n.getAttribute("data-acm")
                    },
                    el: t,
                    config: c,
                    render: function(t) {
                        return window.setTimeout(function() {
                            M.lib.PubSub.$emit("__body-rendered__")
                        }, 0), t(e)
                    }
                })), w++
            })
        }
    }

    function c() {
        M.lib.PubSub.$on("__body-rendered__", function(e) {
            window.__wx_firstInit || ((0, p["default"])(M.scope.cube), (0, m["default"])(M.scope.cube), (0, y["default"])(M.scope.cube), window.__wx_firstInit = !0), d["default"].nextTick(function() {
                M.lib.PubSub.$emit("__body-scroll__", null)
            })
        })
    }

    function u(e, t, n) {
        r(), a(t, n), c()
    }
    var l = Object.assign || function(e) {
        for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var o in n) Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
        }
        return e
    };
    Object.defineProperty(t, "__esModule", {
        value: !0
    }), t["default"] = u;
    var s = n(2),
        d = i(s),
        f = n(3),
        p = i(f),
        h = n(4),
        m = i(h),
        g = n(6),
        v = i(g),
        _ = n(7),
        w = i(_),
        b = n(8),
        y = i(b),
        x = n(11),
        S = i(x),
        k = n(9),
        C = i(k),
        j = n(12),
        P = i(j),
        O = n(5),
        A = o(O),
        T = n(13),
        I = i(T),
        E = n(14),
        D = i(E),
        R = n(16),
        B = i(R),
        L = A.findModParent,
        N = A.findAcmParent;
    if (!M.scope.cube) {
        var q = new d["default"];
        M.scope.cube = {
            utils: A,
            PubSub: q
        }, M.lib.PubSub = q, (0, S["default"])(M), M.scope.cube.$components = [], M.scope.cube._body = window.document.body, window.wx = P["default"], window.wx.isH5 = !0, window.__vx_mwpRequestQueue = window.__vx_mwpRequestQueue || {}, (0, v["default"])(M.scope.cube), M && M.ua && M.ua["native"] && window.hdp && window.hdp["do"]("mgj.device.signParams", {}).then(function(e) {
            "string" == typeof e && (e = JSON.parse(e)), M.scope.cube._did = e._did
        });
        var z = 0,
            $ = 0;
        window.document.addEventListener("DOMContentLoaded", function() {
            M.scope.cube.$components.forEach(function(e) {
                A.callMethodRecursive(e, "onReady", null)
            })
        }), window.onunload = function() {
            M.scope.cube.$components.forEach(function(e) {
                A.callMethodRecursive(e, "onUnload", null)
            })
        }, window.addEventListener("scroll", function(e) {
            M.lib.PubSub.$emit("__body-scroll__", e), M.scope.cube.$components.forEach(function(t) {
                var n = A.bodyScrollTop(),
                    o = A.bodyScrollLeft(),
                    i = window.document.body.scrollHeight,
                    r = window.document.body.scrollWidth,
                    a = window.innerHeight,
                    c = window.__vx_scrollInfo || {},
                    u = c["lower-threshold"] || 50,
                    l = z > n ? "up" : "down",
                    s = {
                        scrollTop: n,
                        scrollHeight: i,
                        scrollLeft: o,
                        scrollWidth: r,
                        deltaX: $ - o,
                        deltaY: z - n
                    };
                e.detail = s, A.callMethodRecursive(t, "scroll", e), A.callMethodRecursive(t, "onPageScroll", {
                    scrollTop: n
                }), z = n, $ = o, i - n - a < u && "down" === l && (A.callMethodRecursive(t, "lower", e), i - n - a == 0 && A.callMethodRecursive(t, "onReachBottom", e));
                var d = c["upper-threshold"] || 50;
                n < d && "up" === l && A.callMethodRecursive(t, "upper", e)
            })
        })
    }
    var U = !1
}, function(e, t) {
    function n(e) {
        e.MCE || (e.MCE = a)
    }
    var o = Object.assign || function(e) {
        for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var o in n) Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
        }
        return e
    };
    Object.defineProperty(t, "__esModule", {
        value: !0
    }), t["default"] = n;
    var i, r = (Object.prototype.hasOwnProperty, i = {}, i.get = "3", i.multiget = "3", i.makeup = "3", i.recommend = "4", i.multirecommend = "4", i),
        a = function() {
            function e(t, n) {
                this.type = t, this.version = r[t], this.data = n;
                var o = e.defaultOptions.appPlat;
                o && (this.data.appPlat = o)
            }
            return e.config = function(e) {
                o(this.defaultOptions, e)
            }, e.request = function(t, n, o) {
                return new e(t, n).request(o)
            }, e.get = function(t, n) {
                return e.request("get", t, n)
            }, e.multiget = function(t, n) {
                return e.request("multiget", t, n)
            }, e.makeup = function(t) {
                return e.request("makeup", t)
            }, e.recommend = function(t) {
                return e.request("recommend", t)
            }, e.multirecommend = function(t) {
                return e.request("multirecommend", t)
            }, e.prototype.request = function(e) {
                var t = this;
                return this.getStrategy(e).reduce(function(e, n) {
                    return e ? e["catch"](function() {
                        return t[n]()
                    }) : t[n]()
                }, null)
            }, e.prototype.requestMWP = function() {
                var t = e.defaultOptions,
                    n = t.headers,
                    o = void 0 === n ? {} : n,
                    i = t.group;
                return i && (o["mw-group"] = i), M.MWP.request("mwp.darwin." + this.type, this.version, this.data, {
                    headers: o
                }).then(M.MWP.filterResult)
            }, e.prototype.requestCDN = function() {
                var e = this;
                return new Promise(function(t, n) {
                    var o = "" + (e.data && e.data.pids ? e.data.pids : e.data.pid);
                    M.http.jsonp("//mce.mogucdn.com/jsonp/" + e.type + "/" + e.version, {
                        data: e.data,
                        cache: !0,
                        timeout: 8e3,
                        jsonpCallback: "jsonp" + o.replace(",", "_")
                    }).then(function(o) {
                        e._handleHTTPResponse(o, t, n)
                    })["catch"](function(e) {
                        n(new Error(e.errMsg))
                    })
                })
            }, e.prototype.requestBackup = function() {
                var e = this;
                return new Promise(function(t, n) {
                    var i = e.data.pids && e.data.pids.split(",") || [e.data.pid],
                        r = [];
                    i.forEach(function(t) {
                        r.push(new Promise(function(n, o) {
                            M.http.jsonp("//mcebackup.mogucdn.com/jsonp/multiget/" + e.version + "%3Fpids=" + t + "&callback=jsonp" + t + "backup", {
                                jsonpCallback: "jsonp" + t + "backup",
                                cache: !0,
                                timeout: 8e3
                            }).then(function(e) {
                                n(e)
                            })["catch"](function(e) {
                                o(new Error(e.errMsg))
                            })
                        }))
                    }), Promise.all(r).then(function(i) {
                        var r = {};
                        i.forEach(function(e) {
                            r = o(r, e.data)
                        }), r = o(i[0], {
                            data: r
                        }), e._handleHTTPResponse(r, t, n)
                    })["catch"](function(e) {
                        n(new Error("\u5bb9\u707e\u5931\u8d25"))
                    })
                })
            }, e.prototype.getStrategy = function(e) {
                return void 0 === e && (e = !1), "undefined" != typeof this.data.cKey && (e = !0), e || "get" !== this.type && "multiget" !== this.type ? ["requestMWP", "requestBackup", "requestCDN"] : ["requestCDN", "requestBackup", "requestMWP"]
            }, e.prototype._handleHTTPResponse = function(e, t, n) {
                e.success && "SUCCESS" === e.returnCode ? t(e.data) : n(new Error(e.returnMessage))
            }, e.defaultOptions = {
                appPlat: "m"
            }, e
        }()
}, function(e, t, n) {
    function o(e) {
        return e && e.__esModule ? e : {
            default: e
        }
    }

    function i(e, t) {
        if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
    }

    function r() {
        console.log("\u8be5\u65b9\u6cd5\u5c5e\u4e8e\u5fae\u4fe1\u5185\u90e8\u65b9\u6cd5, h5\u8c03\u7528\u5c06\u6beb\u65e0\u6548\u679c")
    }

    function a() {
        return r(), {}
    }
    var c = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
        return typeof e
    } : function(e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
    };
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var u = "function" == typeof Symbol && "symbol" === c(Symbol.iterator) ? function(e) {
            return "undefined" == typeof e ? "undefined" : c(e)
        } : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : "undefined" == typeof e ? "undefined" : c(e)
        },
        l = Object.assign || function(e) {
            for (var t = 1; t < arguments.length; t++) {
                var n = arguments[t];
                for (var o in n) Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
            }
            return e
        },
        s = function() {
            function e(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, o.key, o)
                }
            }
            return function(t, n, o) {
                return n && e(t.prototype, n), o && e(t, o), t
            }
        }(),
        d = n(13),
        f = o(d),
        p = n(14),
        h = o(p),
        m = n(16),
        g = o(m),
        v = n(5),
        _ = window.M,
        w = function() {
            function e(t) {
                i(this, e), this.selectorQuery = t, this._nodeQueue = []
            }
            return s(e, [{
                key: "boundingClientRect",
                value: function(e) {
                    return this._nodeQueue.push({
                        type: "bound",
                        cb: e
                    }), this.selectorQuery
                }
            }, {
                key: "fields",
                value: function(e, t) {
                    return this._nodeQueue.push({
                        type: "field",
                        fields: e,
                        cb: t
                    }), this.selectorQuery
                }
            }, {
                key: "scrollOffset",
                value: function(e) {
                    return this._nodeQueue.push({
                        type: "scroll",
                        cb: e
                    }), this.selectorQuery
                }
            }]), e
        }(),
        b = function() {
            function e(t) {
                i(this, e), this.bodyDom = t, this._queue = []
            }
            return s(e, [{
                key: "select",
                value: function(e) {
                    var t = new w(this);
                    return this._queue.push({
                        type: "select",
                        selector: e,
                        nodesRef: t
                    }), t
                }
            }, {
                key: "selectAll",
                value: function(e) {
                    var t = new w(this);
                    return this._queue.push({
                        type: "selectAll",
                        selector: e,
                        nodesRef: t
                    }), t
                }
            }, {
                key: "selectViewport",
                value: function() {
                    var e = new w(this);
                    return this._queue.push({
                        type: "view",
                        nodesRef: e
                    }), e
                }
            }, {
                key: "exec",
                value: function(e) {
                    var t = this,
                        n = [];
                    this._queue.forEach(function(e) {
                        var o = void 0;
                        switch (e.type) {
                            case "select":
                                o = t.bodyDom.querySelector(e.selector);
                                break;
                            case "selectAll":
                                o = t.bodyDom.querySelectorAll(e.selector);
                                break;
                            case "view":
                                o = window.document
                        }
                        e.nodesRef._nodeQueue.forEach(function(t) {
                            if (o && 0 !== o.length) {
                                o.length || (o = [o]);
                                var i = [],
                                    r = null;
                                switch (t.type) {
                                    case "bound":
                                        for (var a = 0; a < o.length; a++) {
                                            var c = o[a].getBoundingClientRect();
                                            c.id = o[a].id, c.dataset = o[a].dataset, i.push(c)
                                        }
                                        "select" === e.type || "view" === e.type ? (n.push(i[0]), r = i[0]) : "selectAll" === e.type && (n.push(i), r = i), t.cb && t.cb(r);
                                        break;
                                    case "field":
                                        for (var a = 0; a < o.length; a++) {
                                            var u = {};
                                            (t.fields.rect || t.fields.size) && (u = o[a].getBoundingClientRect()), t.fields.id && (u.id = o[a].id), t.fields.dataset && (u.dataset = o[a].dataset), t.fields.scrollOffset && (9 === o[a].nodeType ? (o[a] = o[a].defaultView, u.scrollLeft = o[a].pageXOffset, u.scrollTop = o[a].pageYOffset) : (u.scrollLeft = o[a].scrollLeft, u.scrollTop = o[a].scrollTop)), i.push(u)
                                        }
                                        "select" === e.type || "view" === e.type ? (n.push(i[0]), r = i[0]) : "selectAll" === e.type && (n.push(i), r = i), t.cb && t.cb(r);
                                        break;
                                    case "scroll":
                                        for (var a = 0; a < o.length; a++) {
                                            var l = {};
                                            9 === o[a].nodeType ? (o[a] = o[a].defaultView, l = {
                                                id: "",
                                                dataset: {},
                                                scrollLeft: o[a].pageXOffset,
                                                scrollTop: o[a].pageYOffset
                                            }) : l = {
                                                id: o[a].id,
                                                dataset: o[a].dataset,
                                                scrollLeft: o[a].scrollLeft,
                                                scrollTop: o[a].scrollTop
                                            }, i.push(l)
                                        }
                                        "select" === e.type || "view" === e.type ? (n.push(i[0]), r = i[0]) : "selectAll" === e.type && (n.push(i), r = i), t.cb && t.cb(r)
                                }
                            } else "select" === e.type || "view" === e.type ? n.push(null) : "selectAll" === e.type && n.push([])
                        })
                    }), e && e(n)
                }
            }]), e
        }();
    t["default"] = {
        request: function(e) {
            _ && e && _.http.request(e.url, l({}, e, {
                error: e.fail
            }))
        },
        uploadFile: r,
        downloadFile: r,
        connectSocket: r,
        onSocketOpen: r,
        onSocketError: r,
        sendSocketMessage: r,
        onSocketMessage: r,
        closeSocket: r,
        onSocketClose: r,
        chooseImage: r,
        previewImage: r,
        getImageInfo: function(e) {
            if (e && e.src) {
                var t = new Image;
                t.onload = function(n) {
                    e.success && e.success({
                        width: t.width,
                        height: t.height,
                        path: e.src
                    }), e.complete && e.complete()
                }, t.onerror = function(t) {
                    e.fail && e.fail({
                        e: t
                    }), e.complete && e.complete()
                }, t.src = e.src
            }
        },
        saveImageToPhotosAlbum: r,
        startRecord: r,
        stopRecord: r,
        playVoice: r,
        pauseVoice: r,
        stopVoice: r,
        getBackgroundAudioPlayerState: r,
        playBackgroundAudio: r,
        pauseBackgroundAudio: r,
        seekBackgroundAudio: r,
        stopBackgroundAudio: r,
        onBackgroundAudioPlay: r,
        onBackgroundAudioPause: r,
        onBackgroundAudioStop: r,
        getBackgroundAudioManager: r,
        chooseVideo: r,
        saveVideoToPhotosAlbum: r,
        createVideoContext: r,
        saveFile: r,
        getFileInfo: r,
        getSavedFileList: r,
        getSavedFileInfo: r,
        removeSavedFile: r,
        openDocument: r,
        setStorage: function(e) {
            if (window.localStorage && e && e.key) {
                var t = !0;
                try {
                    var n = window.localStorage,
                        o = "object" === u(e.data) && null != e.data ? JSON.stringify(e.data) : e.data;
                    n.setItem(e.key, o)
                } catch (i) {
                    t = !1
                }
                e.success && t ? e.success() : e.fail && !t && e.fail()
            } else e.fail && e.fail();
            e.complete && e.complete()
        },
        setStorageSync: function(e, t) {
            if (window.localStorage && e) {
                var n = window.localStorage,
                    o = "object" === ("undefined" == typeof t ? "undefined" : u(t)) && null != t ? JSON.stringify(t) : t;
                n.setItem(e, o)
            }
        },
        getStorage: function(e) {
            var t;
            if (window.localStorage && e && e.key) {
                var n = window.localStorage;
                t = n.getItem(e.key) || "", e.success && e.success({
                    data: t
                })
            } else e.fail && e.fail();
            e.complete && e.complete()
        },
        getStorageSync: function(e) {
            var t;
            if (window.localStorage) {
                var n = window.localStorage;
                t = n.getItem(e) || ""
            } else console.log("not support localstorage");
            return t
        },
        getStorageInfo: function(e) {
            if (window.localStorage) {
                for (var t = window.localStorage, n = [], o = 0; o < t.length; o++) n.push(t.key(o));
                e.success && e.success({
                    keys: n,
                    currentSize: t.length,
                    limitSize: 0
                })
            } else e.fail && e.fail();
            e.complete && e.complete()
        },
        getStorageInfoSync: function() {
            if (window.localStorage) {
                for (var e = window.localStorage, t = [], n = 0; n < e.length; n++) t.push(e.key(n));
                return {
                    keys: t,
                    currentSize: e.length,
                    limitSize: 0
                }
            }
        },
        removeStorage: function(e) {
            if (window.localStorage && e && e.key) {
                var t = window.localStorage,
                    n = t.getItem(e.key);
                t.removeItem(e.key), e.success && e.success(n)
            } else e.fail && e.fail();
            e.complete && e.complete()
        },
        removeStorageSync: function(e) {
            if (window.localStorage && e) {
                var t = window.localStorage,
                    n = t.getItem(e);
                return t.removeItem(e), n
            }
        },
        clearStorage: function() {
            if (window.localStorage) {
                var e = window.localStorage;
                e.clear()
            }
        },
        clearStorageSync: function() {
            if (window.localStorage) {
                var e = window.localStorage;
                e.clear()
            }
        },
        getLocation: r,
        chooseLocation: r,
        openLocation: r,
        createMapContext: r,
        getSystemInfo: r,
        getSystemInfoSync: a,
        canIUse: function() {
            return console.log("\u8be5\u65b9\u6cd5\u5c5e\u4e8e\u5fae\u4fe1\u5185\u90e8\u65b9\u6cd5, h5\u8c03\u7528\u5c06\u6beb\u65e0\u6548\u679c"), !1
        },
        getNetworkType: r,
        onNetworkStatusChange: r,
        onAccelerometerChange: r,
        startAccelerometer: r,
        stopAccelerometer: r,
        onCompassChange: r,
        startCompass: r,
        stopCompass: r,
        makePhoneCall: r,
        scanCode: r,
        setClipboardData: r,
        getClipboardData: r,
        openBluetoothAdapter: r,
        closeBluetoothAdapter: r,
        getBluetoothAdapterState: r,
        onBluetoothAdapterStateChange: r,
        startBluetoothDevicesDiscovery: r,
        stopBluetoothDevicesDiscovery: r,
        getBluetoothDevices: r,
        getConnectedBluetoothDevices: r,
        onBluetoothDeviceFound: r,
        createBLEConnection: r,
        closeBLEConnection: r,
        getBLEDeviceServices: r,
        getBLEDeviceCharacteristics: r,
        readBLECharacteristicValue: r,
        writeBLECharacteristicValue: r,
        notifyBLECharacteristicValueChange: r,
        onBLEConnectionStateChange: r,
        onBLECharacteristicValueChange: r,
        startBeaconDiscovery: r,
        stopBeaconDiscovery: r,
        getBeacons: r,
        onBeaconUpdate: r,
        onBeaconServiceChange: r,
        setScreenBrightness: r,
        getScreenBrightness: r,
        setKeepScreenOn: r,
        onUserCaptureScreen: r,
        vibrateLong: r,
        vibrateShort: r,
        addPhoneContact: r,
        showToast: function(e) {
            f["default"].show(e.title, e.duration, e.success)
        },
        showLoading: function(e) {
            h["default"].show(e)
        },
        hideToast: function() {
            f["default"].hide()
        },
        hideLoading: function(e) {
            h["default"].hide()
        },
        showModal: function(e) {
            g["default"].show(e)
        },
        showActionSheet: r,
        setNavigationBarTitle: r,
        showNavigationBarLoading: r,
        hideNavigationBarLoading: r,
        setNavigationBarColor: r,
        setTopBarText: r,
        navigateTo: function(e) {
            e.url && (window.location.href = e.url)
        },
        redirectTo: function(e) {
            e.url && window.location.replace(e.url)
        },
        switchTab: function(e) {
            e.url && window.location.replace(e.url)
        },
        navigateBack: function(e) {
            window.history && e && window.history.go(-e.delta)
        },
        reLaunch: function(e) {
            e.url && window.location.replace(e.url)
        },
        createAnimation: r,
        pageScrollTo: function(e) {
            e && (0, v.bodyScrollTop)(e.scrollTop)
        },
        createSelectorQuery: function() {
            var e = window.document.body;
            return new b(e)
        },
        stopPullDownRefresh: r,
        getExtConfig: r,
        getExtConfigSync: r,
        login: function(e) {
            e = e || location.href;
            var t = window.logger,
                n = (navigator.userAgent.toLowerCase(), _ && _.isApp(_.MGJ)),
                o = window.mgj;
            if (n && "object" === ("undefined" == typeof o ? "undefined" : u(o))) location.href = t && t.generatePtpParams("mgj://login") || "mgj://login";
            else {
                var i = "http://portal.mogujie.com/login?redirect_url=" + encodeURIComponent(e);
                location.href = t && t.generatePtpParams(i) || i
            }
        },
        checkSession: r,
        authorize: r,
        getUserInfo: r,
        requestPayment: r,
        showShareMenu: r,
        hideShareMenu: r,
        updateShareMenu: r,
        getShareInfo: r,
        chooseAddress: r,
        addCard: r,
        openCard: r,
        openSetting: r,
        getSetting: r,
        getWeRunData: r,
        navigateToMiniProgram: r,
        navigateBackMiniProgram: r,
        arrayBufferToBase64: r,
        base64ToArrayBuffer: r
    }
}, function(e, t) {
    var n = Object.assign || function(e) {
        for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var o in n) Object.prototype.hasOwnProperty.call(n, o) && (e[o] = n[o])
        }
        return e
    };
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var o = {
            duration: 1500
        },
        i = function(e) {
            var t = n({}, o, e);
            this.duration = t.duration, this.init()
        };
    i.prototype = {
        init: function() {
            this.elem = document.body.querySelector("#M_Tips"), this.elem ? this.text = this.elem.querySelector(".ui-tips-text") : (this.elem = document.createElement("div"), this.elem.setAttribute("id", "M_Tips"), this.elem.setAttribute("class", "ui-tips"), this.elem.setAttribute("style", "display:none;"), this.text = document.createElement("span"), this.text.setAttribute("class", "ui-tips-text"), this.elem.appendChild(this.text), document.body.appendChild(this.elem))
        },
        show: function(e, t, n) {
            var o = this;
            o.elem.style.display = "", e && "string" == typeof e && (o.text.innerText = e, o.text.setAttribute("class", "ui-tips-text fadeIn")), !isNaN(t) || "function" == typeof n && "number" != typeof n.nodeType || n === !1 || (n = t, t = o.duration), 0 != t && o.hide(t, n)
        },
        hide: function(e, t) {
            var n = this,
                o = null;
            o = setTimeout(function() {
                n.text.setAttribute("class", "ui-tips-text fadeOut"), setTimeout(function() {
                    n.elem.style.display = "none", t && t()
                }, 500)
            }, e || n.duration)
        }
    };
    var r = new i;
    t["default"] = r
}, function(e, t, n) {
    function o(e) {
        return e && e.__esModule ? e : {
            default: e
        }
    }

    function i(e, t) {
        if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
    }
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var r = function() {
            function e(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, o.key, o)
                }
            }
            return function(t, n, o) {
                return n && e(t.prototype, n), o && e(t, o), t
            }
        }(),
        a = n(2),
        c = o(a),
        u = n(15),
        l = o(u),
        s = function() {
            function e() {
                i(this, e), this.dom = document.querySelector("#M_vx_Loadings"), this.dom && this.dom.length || (this.dom = document.createElement("div"), this.dom.id = "M_vx_Loadings", document.body.appendChild(this.dom)), this.inst = new c["default"]({
                    el: "#M_vx_Loadings",
                    components: {
                        MvwLoadding: l["default"]
                    },
                    data: {
                        show: !1
                    },
                    template: '<mvw-loadding :isShow="show"> </mvw-loadding>'
                })
            }
            return r(e, [{
                key: "show",
                value: function() {
                    this.inst.show = !0
                }
            }, {
                key: "hide",
                value: function() {
                    this.inst.show = !1
                }
            }]), e
        }(),
        d = new s;
    t["default"] = d
}, function(e, t) {
    var n = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
        return typeof e
    } : function(e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
    };
    e.exports = function(e) {
        function t(o) {
            if (n[o]) return n[o].exports;
            var i = n[o] = {
                exports: {},
                id: o,
                loaded: !1
            };
            return e[o].call(i.exports, i, i.exports, t), i.loaded = !0, i.exports
        }
        var n = {};
        return t.m = e, t.c = n, t.p = "/", t(0)
    }([function(e, t, n) {
        "use strict";

        function o(e) {
            return e && e.__esModule ? e : {
                default: e
            }
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var i = n(4),
            r = o(i);
        t["default"] = r["default"]
    }, function(e, t) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t["default"] = {
            name: "Loading",
            _timer: null,
            props: {
                isShow: {
                    type: Boolean,
                    default: !1
                },
                bgImg: {
                    type: String,
                    default: "https://s10.mogucdn.com/p2/170228/116560387_5c7fa526b9e23a4g8efgc8db3g2bi_200x200.png"
                },
                bgImgslip: {
                    type: String,
                    default: "https://s10.mogucdn.com/p2/170228/116560387_5e6e30e3ld0blkjijkj196eeh0b3b_200x200.png"
                },
                size: {
                    type: [Number, String],
                    default: ""
                },
                unit: {
                    type: String,
                    default: "px"
                }
            },
            data: function() {
                return {}
            },
            computed: {
                width: function() {
                    return this.size ? this.size + this.unit : ""
                }
            },
            methods: {
                show: function() {
                    var e = this;
                    this._timer && clearTimeout(this._timer), this.isShow = !0, this._timer = setTimeout(function() {
                        e._timer = null
                    }, 3e3)
                },
                hide: function() {
                    this._timer && (clearTimeout(this._timer), this._timer = null), this.isShow = !1
                }
            }
        }
    }, function(e, t, n) {
        t = e.exports = n(3)(), t.push([e.id, "\n.meili-mvw-loadding[data-v-f2c532c8] {\n  position: fixed;\n  display: -webkit-box;\n  display: -webkit-flex;\n  display: -moz-box;\n  display: -ms-flexbox;\n  display: flex;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n  -webkit-box-align: center;\n  -webkit-align-items: center;\n  -moz-box-align: center;\n  -ms-flex-align: center;\n  align-items: center;\n  -webkit-align-content: center;\n  -ms-flex-line-pack: center;\n  align-content: center;\n  z-index: 1000;\n}\n.loading[data-v-f2c532c8] {\n  position: relative;\n  margin: 0 auto;\n  pointer-events: auto;\n}\n@-webkit-keyframes loadingRotate {\n100% {\n    -webkit-transform: rotate(1turn);\n    transform: rotate(1turn);\n}\n}\n@keyframes loadingRotate {\n100% {\n    -webkit-transform: rotate(1turn);\n    transform: rotate(1turn);\n}\n}\n.loading-slip[data-v-f2c532c8] {\n  -webkit-animation: loadingRotate 1050ms infinite;\n  animation: loadingRotate 1050ms infinite;\n}\n.loading[data-v-f2c532c8],\n.loading-slip[data-v-f2c532c8] {\n  width: 1.6rem;\n  height: 1.6rem;\n  background-repeat: no-repeat;\n  background-size: cover;\n}", ""])
    }, function(e, t) {
        e.exports = function() {
            var e = [];
            return e.toString = function() {
                for (var e = [], t = 0; t < this.length; t++) {
                    var n = this[t];
                    n[2] ? e.push("@media " + n[2] + "{" + n[1] + "}") : e.push(n[1])
                }
                return e.join("")
            }, e.i = function(t, n) {
                "string" == typeof t && (t = [
                    [null, t, ""]
                ]);
                for (var o = {}, i = 0; i < this.length; i++) {
                    var r = this[i][0];
                    "number" == typeof r && (o[r] = !0)
                }
                for (i = 0; i < t.length; i++) {
                    var a = t[i];
                    "number" == typeof a[0] && o[a[0]] || (n && !a[2] ? a[2] = n : n && (a[2] = "(" + a[2] + ") and (" + n + ")"), e.push(a))
                }
            }, e
        }
    }, function(e, t, o) {
        var i, r;
        o(7), i = o(1);
        var a = o(5);
        r = i = i || {}, "object" !== n(i["default"]) && "function" != typeof i["default"] || (Object.keys(i).some(function(e) {
            return "default" !== e && "__esModule" !== e
        }) && console.error("named exports are not supported in *.vue files."), r = i = i["default"]), "function" == typeof r && (r = r.options), r.__file = "/Users/lingxiao/Projects/Component/meili-baymax/packages/mvw-loadding/src/index.vue", r.render = a.render, r.staticRenderFns = a.staticRenderFns, r._scopeId = "data-v-f2c532c8", r.functional && console.error("[vue-loader] index.vue: functional components are not supported and should be defined in plain js files using render functions."), e.exports = i
    }, function(e, t, n) {
        e.exports = {
            render: function() {
                var e = this,
                    t = e.$createElement;
                e._self._c || t;
                return e.isShow ? t("div", {
                    staticClass: "meili-mvw-loadding loadding"
                }, [t("div", {
                    staticClass: "loading",
                    style: {
                        "background-image": "url(" + e.bgImg + ")",
                        width: e.width,
                        height: e.width
                    }
                }, [t("div", {
                    staticClass: "loading-slip",
                    style: {
                        "background-image": "url(" + e.bgImgslip + ")",
                        width: e.width,
                        height: e.width
                    }
                })])]) : e._e()
            },
            staticRenderFns: []
        }
    }, function(e, t, n) {
        function o(e, t) {
            for (var n = 0; n < e.length; n++) {
                var o = e[n],
                    i = d[o.id];
                if (i) {
                    i.refs++;
                    for (var r = 0; r < i.parts.length; r++) i.parts[r](o.parts[r]);
                    for (; r < o.parts.length; r++) i.parts.push(u(o.parts[r], t))
                } else {
                    for (var a = [], r = 0; r < o.parts.length; r++) a.push(u(o.parts[r], t));
                    d[o.id] = {
                        id: o.id,
                        refs: 1,
                        parts: a
                    }
                }
            }
        }

        function i(e) {
            for (var t = [], n = {}, o = 0; o < e.length; o++) {
                var i = e[o],
                    r = i[0],
                    a = i[1],
                    c = i[2],
                    u = i[3],
                    l = {
                        css: a,
                        media: c,
                        sourceMap: u
                    };
                n[r] ? n[r].parts.push(l) : t.push(n[r] = {
                    id: r,
                    parts: [l]
                })
            }
            return t
        }

        function r(e, t) {
            var n = h(),
                o = v[v.length - 1];
            if ("top" === e.insertAt) o ? o.nextSibling ? n.insertBefore(t, o.nextSibling) : n.appendChild(t) : n.insertBefore(t, n.firstChild), v.push(t);
            else {
                if ("bottom" !== e.insertAt) throw new Error("Invalid value for parameter 'insertAt'. Must be 'top' or 'bottom'.");
                n.appendChild(t)
            }
        }

        function a(e) {
            e.parentNode.removeChild(e);
            var t = v.indexOf(e);
            t >= 0 && v.splice(t, 1)
        }

        function c(e) {
            var t = document.createElement("style");
            return t.type = "text/css", r(e, t), t
        }

        function u(e, t) {
            var n, o, i;
            if (t.singleton) {
                var r = g++;
                n = m || (m = c(t)), o = l.bind(null, n, r, !1), i = l.bind(null, n, r, !0)
            } else n = c(t), o = s.bind(null, n), i = function() {
                a(n)
            };
            return o(e),
                function(t) {
                    if (t) {
                        if (t.css === e.css && t.media === e.media && t.sourceMap === e.sourceMap) return;
                        o(e = t)
                    } else i()
                }
        }

        function l(e, t, n, o) {
            var i = n ? "" : o.css;
            if (e.styleSheet) e.styleSheet.cssText = _(t, i);
            else {
                var r = document.createTextNode(i),
                    a = e.childNodes;
                a[t] && e.removeChild(a[t]), a.length ? e.insertBefore(r, a[t]) : e.appendChild(r)
            }
        }

        function s(e, t) {
            var n = t.css,
                o = t.media,
                i = t.sourceMap;
            if (o && e.setAttribute("media", o), i && (n += "\n/*# sourceURL=" + i.sources[0] + " */", n += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(i)))) + " */"), e.styleSheet) e.styleSheet.cssText = n;
            else {
                for (; e.firstChild;) e.removeChild(e.firstChild);
                e.appendChild(document.createTextNode(n))
            }
        }
        var d = {},
            f = function(e) {
                var t;
                return function() {
                    return "undefined" == typeof t && (t = e.apply(this, arguments)), t
                }
            },
            p = f(function() {
                return /msie [6-9]\b/.test(window.navigator.userAgent.toLowerCase())
            }),
            h = f(function() {
                return document.head || document.getElementsByTagName("head")[0]
            }),
            m = null,
            g = 0,
            v = [];
        e.exports = function(e, t) {
            t = t || {}, "undefined" == typeof t.singleton && (t.singleton = p()), "undefined" == typeof t.insertAt && (t.insertAt = "bottom");
            var n = i(e);
            return o(n, t),
                function(e) {
                    for (var r = [], a = 0; a < n.length; a++) {
                        var c = n[a],
                            u = d[c.id];
                        u.refs--, r.push(u)
                    }
                    if (e) {
                        var l = i(e);
                        o(l, t)
                    }
                    for (var a = 0; a < r.length; a++) {
                        var u = r[a];
                        if (0 === u.refs) {
                            for (var s = 0; s < u.parts.length; s++) u.parts[s]();
                            delete d[u.id]
                        }
                    }
                }
        };
        var _ = function() {
            var e = [];
            return function(t, n) {
                return e[t] = n, e.filter(Boolean).join("\n")
            }
        }()
    }, function(e, t, n) {
        var o = n(2);
        "string" == typeof o && (o = [
            [e.id, o, ""]
        ]);
        n(6)(o, {});
        o.locals && (e.exports = o.locals)
    }])
}, function(e, t, n) {
    function o(e) {
        return e && e.__esModule ? e : {
            default: e
        }
    }

    function i(e, t) {
        if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
    }
    Object.defineProperty(t, "__esModule", {
        value: !0
    });
    var r = function() {
            function e(e, t) {
                for (var n = 0; n < t.length; n++) {
                    var o = t[n];
                    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, o.key, o)
                }
            }
            return function(t, n, o) {
                return n && e(t.prototype, n), o && e(t, o), t
            }
        }(),
        a = n(2),
        c = o(a),
        u = n(17),
        l = o(u),
        s = function() {
            function e() {
                i(this, e), this.dom = document.querySelector("#M_vx_Dialogs"), this.dom && this.dom.length || (this.dom = document.createElement("div"), this.dom.id = "M_vx_Dialogs", document.body.appendChild(this.dom)), this.inst = new c["default"]({
                    el: "#M_vx_Dialogs",
                    components: {
                        MvwDialog: l["default"]
                    },
                    data: {
                        title: "",
                        isShow: !1,
                        showCancel: !0,
                        cancelText: "\u53d6\u6d88",
                        cancelColor: "#000000",
                        confirmText: "\u786e\u5b9a",
                        confirmColor: "#3CC51F",
                        content: "",
                        success: function() {},
                        complete: this.completeFunc()
                    },
                    template: '<mvw-dialog :isShow="isShow" :title="title" :showCancel="showCancel" :cancelText="cancelText" :cancelColor="cancelColor" :confirmText="confirmText" :confirmColor="confirmColor" :content="content" :success="success" :complete="complete"> </mvw-dialog>'
                })
            }
            return r(e, [{
                key: "completeFunc",
                value: function(e) {
                    var t = this;
                    return function() {
                        e && e(), t.inst.isShow = !1
                    }
                }
            }, {
                key: "show",
                value: function(e) {
                    var t = this;
                    this.inst.isShow = !0, e.complete && (e.complete = this.completeFunc(e.complete)), (Object.keys(e || {}) || []).forEach(function(n) {
                        t.inst[n] = e[n]
                    })
                }
            }, {
                key: "hide",
                value: function() {
                    this.inst.isShow = !1
                }
            }]), e
        }(),
        d = new s;
    t["default"] = d
}, function(e, t) {
    var n = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e) {
        return typeof e
    } : function(e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
    };
    e.exports = function(e) {
        function t(o) {
            if (n[o]) return n[o].exports;
            var i = n[o] = {
                exports: {},
                id: o,
                loaded: !1
            };
            return e[o].call(i.exports, i, i.exports, t), i.loaded = !0, i.exports
        }
        var n = {};
        return t.m = e, t.c = n, t.p = "/", t(0)
    }([function(e, t, n) {
        "use strict";

        function o(e) {
            return e && e.__esModule ? e : {
                default: e
            }
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var i = n(4),
            r = o(i);
        t["default"] = r["default"]
    }, function(e, t) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t["default"] = {
            name: "mvw-dialog",
            components: {},
            props: {
                title: {
                    type: String,
                    default: ""
                },
                showCancel: {
                    type: Boolean,
                    default: !0
                },
                cancelText: {
                    type: String,
                    default: "\u53d6\u6d88"
                },
                cancelColor: {
                    type: String,
                    default: "#666"
                },
                confirmText: {
                    type: String,
                    default: "\u786e\u5b9a"
                },
                confirmColor: {
                    type: String,
                    default: "#666"
                },
                content: {
                    type: String,
                    default: ""
                },
                success: {
                    type: Function,
                    default: function() {}
                },
                complete: {
                    type: Function,
                    default: function() {}
                },
                isShow: {
                    type: Boolean,
                    default: !1
                }
            },
            data: function() {
                return {}
            },
            computed: {},
            watch: {},
            methods: {
                handleClose: function(e) {
                    this.success({
                        confirm: e,
                        cancel: !e
                    }), this.complete(), this.$emit("handle-close", e)
                }
            },
            filters: {},
            created: function() {},
            mounted: function() {}
        }
    }, function(e, t, n) {
        t = e.exports = n(3)(), t.push([e.id, "\n.u-mask {\n  position: fixed;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n  display: -webkit-box;\n  display: -webkit-flex;\n  display: -moz-box;\n  display: -ms-flexbox;\n  display: flex;\n  -webkit-box-orient: vertical;\n  -webkit-box-direction: normal;\n  -webkit-flex-direction: column;\n  -moz-box-orient: vertical;\n  -moz-box-direction: normal;\n  -ms-flex-direction: column;\n  flex-direction: column;\n  -webkit-box-pack: center;\n  -webkit-justify-content: center;\n  -moz-box-pack: center;\n  -ms-flex-pack: center;\n  justify-content: center;\n  -webkit-align-content: center;\n  -ms-flex-line-pack: center;\n  align-content: center;\n  z-index: 500;\n  background-color: rgba(0, 0, 0, .7);\n}\n.mvw-dialog {\n  display: -webkit-box;\n  display: -webkit-flex;\n  display: -moz-box;\n  display: -ms-flexbox;\n  display: flex;\n  -webkit-box-orient: vertical;\n  -webkit-box-direction: normal;\n  -webkit-flex-direction: column;\n  -moz-box-orient: vertical;\n  -moz-box-direction: normal;\n  -ms-flex-direction: column;\n  flex-direction: column;\n  position: absolute;\n  top: 50%;\n  left: 50%;\n  -webkit-transform: translate(-50%, -50%);\n  transform: translate(-50%, -50%);\n  width: 5.4rem;\n  min-height: 2.36rem;\n  background-color: #fff;\n  border-radius: 0.1rem;\n}\n.mvw-dialog__header {\n  padding-top: 0.4rem;\n  font-size: 0.4rem;\n  text-align: center;\n  color: #333;\n}\n.mvw-dialog__body {\n  -webkit-box-flex: 1;\n  -webkit-flex: 1;\n  -moz-box-flex: 1;\n  -ms-flex: 1;\n  flex: 1;\n  padding: 0.4rem 0.59rem;\n  font-size: 0.28rem;\n  color: #666;\n  text-align: center;\n}\n.mvw-dialog__footer {\n  display: -webkit-box;\n  display: -webkit-flex;\n  display: -moz-box;\n  display: -ms-flexbox;\n  display: flex;\n  height: 0.9rem;\n  font-size: 0.32rem;\n}\n.mvw-dialog__footer__btn {\n  -webkit-box-flex: 1;\n  -webkit-flex: 1;\n  -moz-box-flex: 1;\n  -ms-flex: 1;\n  flex: 1;\n  background-color: #fff;\n  font-size: 0.32rem;\n  border: none;\n  outline: none;\n  border-top: 0.01rem solid #e5e5e5;\n}\n.mvw-dialog__footer__btn:nth-child(n+2) {\n  border-left: 0.01rem solid #e5e5e5;\n}\n.mvw-dialog__footer__btn:first-child {\n  border-bottom-left-radius: 0.1rem;\n}\n.mvw-dialog__footer__btn:last-child {\n  border-bottom-right-radius: 0.1rem;\n}", ""])
    }, function(e, t) {
        e.exports = function() {
            var e = [];
            return e.toString = function() {
                for (var e = [], t = 0; t < this.length; t++) {
                    var n = this[t];
                    n[2] ? e.push("@media " + n[2] + "{" + n[1] + "}") : e.push(n[1])
                }
                return e.join("")
            }, e.i = function(t, n) {
                "string" == typeof t && (t = [
                    [null, t, ""]
                ]);
                for (var o = {}, i = 0; i < this.length; i++) {
                    var r = this[i][0];
                    "number" == typeof r && (o[r] = !0)
                }
                for (i = 0; i < t.length; i++) {
                    var a = t[i];
                    "number" == typeof a[0] && o[a[0]] || (n && !a[2] ? a[2] = n : n && (a[2] = "(" + a[2] + ") and (" + n + ")"), e.push(a))
                }
            }, e
        }
    }, function(e, t, o) {
        var i, r;
        o(7), i = o(1);
        var a = o(5);
        r = i = i || {}, "object" !== n(i["default"]) && "function" != typeof i["default"] || (Object.keys(i).some(function(e) {
            return "default" !== e && "__esModule" !== e
        }) && console.error("named exports are not supported in *.vue files."), r = i = i["default"]), "function" == typeof r && (r = r.options), r.__file = "/Users/lingxiao/Project/vue/meili-baymax/packages/mvw-dialog/src/index.vue", r.render = a.render, r.staticRenderFns = a.staticRenderFns, r.functional && console.error("[vue-loader] index.vue: functional components are not supported and should be defined in plain js files using render functions."), e.exports = i
    }, function(e, t, n) {
        e.exports = {
            render: function() {
                var e = this,
                    t = e.$createElement;
                e._self._c || t;
                return t("div", {
                    directives: [{
                        name: "show",
                        rawName: "v-show",
                        value: e.isShow,
                        expression: "isShow"
                    }],
                    staticClass: "u-mask"
                }, [t("div", {
                    staticClass: "meili-mvw-dialog mvw-dialog"
                }, [e.title ? t("div", {
                    staticClass: "mvw-dialog__header"
                }, [e._s(e.title)]) : e._e(), " ", t("div", {
                    staticClass: "mvw-dialog__body"
                }, [t("p", [e._s(e.content)]), " ", e._t("default")]), " ", t("div", {
                    staticClass: "mvw-dialog__footer"
                }, [e.showCancel ? t("button", {
                    staticClass: "mvw-dialog__footer__btn",
                    style: {
                        color: e.cancelColor
                    },
                    on: {
                        click: function(t) {
                            e.handleClose(!1)
                        }
                    }
                }, ["\n        " + e._s(e.cancelText) + "\n      "]) : e._e(), " ", t("button", {
                    staticClass: "mvw-dialog__footer__btn",
                    style: {
                        color: e.confirmColor
                    },
                    on: {
                        click: function(t) {
                            e.handleClose(!0)
                        }
                    }
                }, ["\n        " + e._s(e.confirmText) + "\n      "])])])])
            },
            staticRenderFns: []
        }
    }, function(e, t, n) {
        function o(e, t) {
            for (var n = 0; n < e.length; n++) {
                var o = e[n],
                    i = d[o.id];
                if (i) {
                    i.refs++;
                    for (var r = 0; r < i.parts.length; r++) i.parts[r](o.parts[r]);
                    for (; r < o.parts.length; r++) i.parts.push(u(o.parts[r], t))
                } else {
                    for (var a = [], r = 0; r < o.parts.length; r++) a.push(u(o.parts[r], t));
                    d[o.id] = {
                        id: o.id,
                        refs: 1,
                        parts: a
                    }
                }
            }
        }

        function i(e) {
            for (var t = [], n = {}, o = 0; o < e.length; o++) {
                var i = e[o],
                    r = i[0],
                    a = i[1],
                    c = i[2],
                    u = i[3],
                    l = {
                        css: a,
                        media: c,
                        sourceMap: u
                    };
                n[r] ? n[r].parts.push(l) : t.push(n[r] = {
                    id: r,
                    parts: [l]
                })
            }
            return t
        }

        function r(e, t) {
            var n = h(),
                o = v[v.length - 1];
            if ("top" === e.insertAt) o ? o.nextSibling ? n.insertBefore(t, o.nextSibling) : n.appendChild(t) : n.insertBefore(t, n.firstChild), v.push(t);
            else {
                if ("bottom" !== e.insertAt) throw new Error("Invalid value for parameter 'insertAt'. Must be 'top' or 'bottom'.");
                n.appendChild(t)
            }
        }

        function a(e) {
            e.parentNode.removeChild(e);
            var t = v.indexOf(e);
            t >= 0 && v.splice(t, 1)
        }

        function c(e) {
            var t = document.createElement("style");
            return t.type = "text/css", r(e, t), t
        }

        function u(e, t) {
            var n, o, i;
            if (t.singleton) {
                var r = g++;
                n = m || (m = c(t)), o = l.bind(null, n, r, !1), i = l.bind(null, n, r, !0)
            } else n = c(t),
                o = s.bind(null, n), i = function() {
                    a(n)
                };
            return o(e),
                function(t) {
                    if (t) {
                        if (t.css === e.css && t.media === e.media && t.sourceMap === e.sourceMap) return;
                        o(e = t)
                    } else i()
                }
        }

        function l(e, t, n, o) {
            var i = n ? "" : o.css;
            if (e.styleSheet) e.styleSheet.cssText = _(t, i);
            else {
                var r = document.createTextNode(i),
                    a = e.childNodes;
                a[t] && e.removeChild(a[t]), a.length ? e.insertBefore(r, a[t]) : e.appendChild(r)
            }
        }

        function s(e, t) {
            var n = t.css,
                o = t.media,
                i = t.sourceMap;
            if (o && e.setAttribute("media", o), i && (n += "\n/*# sourceURL=" + i.sources[0] + " */", n += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(i)))) + " */"), e.styleSheet) e.styleSheet.cssText = n;
            else {
                for (; e.firstChild;) e.removeChild(e.firstChild);
                e.appendChild(document.createTextNode(n))
            }
        }
        var d = {},
            f = function(e) {
                var t;
                return function() {
                    return "undefined" == typeof t && (t = e.apply(this, arguments)), t
                }
            },
            p = f(function() {
                return /msie [6-9]\b/.test(window.navigator.userAgent.toLowerCase())
            }),
            h = f(function() {
                return document.head || document.getElementsByTagName("head")[0]
            }),
            m = null,
            g = 0,
            v = [];
        e.exports = function(e, t) {
            t = t || {}, "undefined" == typeof t.singleton && (t.singleton = p()), "undefined" == typeof t.insertAt && (t.insertAt = "bottom");
            var n = i(e);
            return o(n, t),
                function(e) {
                    for (var r = [], a = 0; a < n.length; a++) {
                        var c = n[a],
                            u = d[c.id];
                        u.refs--, r.push(u)
                    }
                    if (e) {
                        var l = i(e);
                        o(l, t)
                    }
                    for (var a = 0; a < r.length; a++) {
                        var u = r[a];
                        if (0 === u.refs) {
                            for (var s = 0; s < u.parts.length; s++) u.parts[s]();
                            delete d[u.id]
                        }
                    }
                }
        };
        var _ = function() {
            var e = [];
            return function(t, n) {
                return e[t] = n, e.filter(Boolean).join("\n")
            }
        }()
    }, function(e, t, n) {
        var o = n(2);
        "string" == typeof o && (o = [
            [e.id, o, ""]
        ]);
        n(6)(o, {});
        o.locals && (e.exports = o.locals)
    }])
}]);
window.lazyImage = function(t) {
    function e(o) {
        if (i[o]) return i[o].exports;
        var n = i[o] = {
            exports: {},
            id: o,
            loaded: !1
        };
        return t[o].call(n.exports, n, n.exports, e), n.loaded = !0, n.exports
    }
    var i = {};
    return e.m = t, e.c = i, e.p = "", e(0)
}({
    0: function(t, e, i) {
        function o(t) {
            return t && t.__esModule ? t : {
                default: t
            }
        }
        Object.defineProperty(e, "__esModule", {
            value: !0
        });
        var n = i(18),
            r = o(n);
        e["default"] = r["default"], t.exports = e["default"]
    },
    18: function(t, e, i) {
        var o = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
            return typeof t
        } : function(t) {
            return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
        };
        t.exports = function(t) {
            function e(o) {
                if (i[o]) return i[o].exports;
                var n = i[o] = {
                    i: o,
                    l: !1,
                    exports: {}
                };
                return t[o].call(n.exports, n, n.exports, e), n.l = !0, n.exports
            }
            var i = {};
            return e.m = t, e.c = i, e.i = function(t) {
                return t
            }, e.d = function(t, i, o) {
                e.o(t, i) || Object.defineProperty(t, i, {
                    configurable: !1,
                    enumerable: !0,
                    get: o
                })
            }, e.n = function(t) {
                var i = t && t.__esModule ? function() {
                    return t["default"]
                } : function() {
                    return t
                };
                return e.d(i, "a", i), i
            }, e.o = function(t, e) {
                return Object.prototype.hasOwnProperty.call(t, e)
            }, e.p = "", e(e.s = 1)
        }([function(t, e, i) {
            function o(t) {
                i(7)
            }
            var n = i(5)(i(2), i(6), o, null, null);
            t.exports = n.exports
        }, function(t, e, i) {
            "use strict";

            function o(t) {
                return t && t.__esModule ? t : {
                    default: t
                }
            }
            Object.defineProperty(e, "__esModule", {
                value: !0
            });
            var n = i(0),
                r = o(n);
            e["default"] = r["default"]
        }, function(t, e, i) {
            "use strict";

            function o() {
                var t = document.documentElement.scrollTop || document.body.scrollTop,
                    e = window.innerHeight,
                    i = {};
                return i.top = t - e, i.bot = t + (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) + e, i.left = 0, i.right = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth, i.scrollTop = t, i
            }

            function n(t) {
                var e, i, n, r, a = o(),
                    s = t,
                    l = s.getBoundingClientRect && s.getBoundingClientRect();
                l && (e = l.top + a.scrollTop, i = l.bottom + a.scrollTop, n = l.left, r = l.right);
                var f = i > a.top && e < a.bot,
                    d = r > a.left && n < a.right;
                if (f && d) {
                    var u = s.style;
                    return !u || !("none" == u.display || "hidden" == u.visibility || "0" === u.opacity || !s.offsetWidth)
                }
                return !1
            }
            Object.defineProperty(e, "__esModule", {
                value: !0
            }), e["default"] = {
                name: "lazy-image",
                props: {
                    src: String,
                    mode: {
                        type: String,
                        default: "scaleToFill"
                    },
                    lazyLoad: {
                        type: Boolean,
                        default: !1
                    },
                    bindload: Function,
                    binderror: Function
                },
                data: function() {
                    return {
                        hasAddImg: !1,
                        widthLong: !1,
                        loadingClass: this.hasAddImg ? "" : " loading_bg-img"
                    }
                },
                watch: {
                    src: function(t) {
                        this.img && (this.img.remove(), this.hasAddImg = !1, this.loadImg())
                    }
                },
                mounted: function() {
                    this.lazyLoad || this.loadImg()
                },
                methods: {
                    getClass: function() {
                        var t = "widthFix" === this.mode ? "lazy-image-noheight" : "lazy-image";
                        switch (this.mode) {
                            case "scaleToFill":
                                t += " scale-fill";
                                break;
                            case "aspectFit":
                                t += " aspect-fit";
                                break;
                            case "aspectFill":
                                t += " aspect-fill";
                                break;
                            case "widthFix":
                                t += " width-fix";
                                break;
                            default:
                                t += " " + this.mode.split(" ").join("-") + "-fix"
                        }
                        return t
                    },
                    loadImg: function() {
                        var t = this,
                            e = this.$refs["lazy-image"];
                        if (!this.hasAddImg && e && (n(e) || !this.lazyLoad)) {
                            var i = new Image;
                            i.onload = function(e) {
                                e.detail = {
                                    width: i.width,
                                    height: i.height
                                }, t.widthLong = i.width > i.height, t.$emit("bindload", e)
                            }, i.onerror = function(e) {
                                e.detail = {
                                    errMsg: "\u672a\u52a0\u8f7d\u5230\u56fe\u7247"
                                }, t.$emit("binderror", e)
                            }, i.src = this.codeSrc ? this.codeSrc : this.src, this.img = i, e.appendChild(i), this.hasAddImg = !0, this.loadingClass = ""
                        }
                    },
                    modInView: function() {
                        this.loadImg()
                    }
                }
            }
        }, function(t, e, i) {
            e = t.exports = i(4)(), e.push([t.i, ".lazy-image{width:320px;height:240px;overflow:hidden;display:inline-block}.lazy-image-noheight{width:320px}.scale-fill img{width:100%;height:100%;display:block}.aspect-fit{position:relative}.aspect-fit.width-long img{position:absolute;top:50%;left:0;-webkit-transform:translateY(-50%);transform:translateY(-50%);width:100%;height:auto;display:block}.aspect-fit.height-long img{position:absolute;top:0;left:50%;-webkit-transform:translateX(-50%);transform:translateX(-50%);height:100%;width:auto;display:block}.aspect-fill{position:relative}.aspect-fill.width-long img{position:absolute;top:0;left:50%;-webkit-transform:translateX(-50%);transform:translateX(-50%);width:auto;height:100%;display:block}.aspect-fill.height-long img{position:absolute;top:50%;left:0;-webkit-transform:translateY(-50%);transform:translateY(-50%);height:auto;width:100%;display:block}.width-fix,.width-fix img{width:100%;display:block}.width-fix img{height:auto}.top-fix{position:relative}.top-fix img{position:absolute;top:0;left:50%;-webkit-transform:translateX(-50%);transform:translateX(-50%)}.bottom-fix{position:relative}.bottom-fix img{position:absolute;bottom:0;left:50%;-webkit-transform:translateX(-50%);transform:translateX(-50%)}.center-fix{position:relative}.center-fix img{position:absolute;top:50%;left:50%;-webkit-transform:translate(-50%,-50%);transform:translate(-50%,-50%)}.left-fix{position:relative}.left-fix img{position:absolute;top:50%;left:0;-webkit-transform:translateY(-50%);transform:translateY(-50%)}.right-fix{position:relative}.right-fix img{position:absolute;top:50%;right:0;-webkit-transform:translateY(-50%);transform:translateY(-50%)}.top-left-fix{position:relative}.top-left-fix img{position:absolute;top:0;left:0}.top-right-fix{position:relative}.top-right-fix img{position:absolute;top:0;right:0}.bottom-left-fix{position:relative}.bottom-left-fix img{position:absolute;bottom:0;left:0}.bottom-right-fix{position:relative}.bottom-right-fix img{position:absolute;bottom:0;right:0}", ""])
        }, function(t, e) {
            t.exports = function() {
                var t = [];
                return t.toString = function() {
                    for (var t = [], e = 0; e < this.length; e++) {
                        var i = this[e];
                        i[2] ? t.push("@media " + i[2] + "{" + i[1] + "}") : t.push(i[1])
                    }
                    return t.join("")
                }, t.i = function(e, i) {
                    "string" == typeof e && (e = [
                        [null, e, ""]
                    ]);
                    for (var o = {}, n = 0; n < this.length; n++) {
                        var r = this[n][0];
                        "number" == typeof r && (o[r] = !0)
                    }
                    for (n = 0; n < e.length; n++) {
                        var a = e[n];
                        "number" == typeof a[0] && o[a[0]] || (i && !a[2] ? a[2] = i : i && (a[2] = "(" + a[2] + ") and (" + i + ")"), t.push(a))
                    }
                }, t
            }
        }, function(t, e) {
            t.exports = function(t, e, i, n, r) {
                var a, s = t = t || {},
                    l = o(t["default"]);
                "object" !== l && "function" !== l || (a = t, s = t["default"]);
                var f = "function" == typeof s ? s.options : s;
                e && (f.render = e.render, f.staticRenderFns = e.staticRenderFns), n && (f._scopeId = n);
                var d;
                if (r ? (d = function(t) {
                        t = t || this.$vnode && this.$vnode.ssrContext || this.parent && this.parent.$vnode && this.parent.$vnode.ssrContext, t || "undefined" == typeof __VUE_SSR_CONTEXT__ || (t = __VUE_SSR_CONTEXT__), i && i.call(this, t), t && t._registeredComponents && t._registeredComponents.add(r)
                    }, f._ssrRegister = d) : i && (d = i), d) {
                    var u = f.functional,
                        c = u ? f.render : f.beforeCreate;
                    u ? f.render = function(t, e) {
                        return d.call(e), c(t, e)
                    } : f.beforeCreate = c ? [].concat(c, d) : [d]
                }
                return {
                    esModule: a,
                    exports: s,
                    options: f
                }
            }
        }, function(t, e) {
            t.exports = {
                render: function() {
                    var t = this,
                        e = t.$createElement,
                        i = t._self._c || e;
                    return i("div", {
                        ref: "lazy-image",
                        class: t.getClass() + (t.widthLong ? " width-long" : " height-long") + t.loadingClass
                    })
                },
                staticRenderFns: []
            }
        }, function(t, e, i) {
            var o = i(3);
            "string" == typeof o && (o = [
                [t.i, o, ""]
            ]), o.locals && (t.exports = o.locals);
            i(8)("3475aaac", o, !0)
        }, function(t, e, i) {
            function o(t) {
                for (var e = 0; e < t.length; e++) {
                    var i = t[e],
                        o = d[i.id];
                    if (o) {
                        o.refs++;
                        for (var n = 0; n < o.parts.length; n++) o.parts[n](i.parts[n]);
                        for (; n < i.parts.length; n++) o.parts.push(r(i.parts[n]));
                        o.parts.length > i.parts.length && (o.parts.length = i.parts.length)
                    } else {
                        for (var a = [], n = 0; n < i.parts.length; n++) a.push(r(i.parts[n]));
                        d[i.id] = {
                            id: i.id,
                            refs: 1,
                            parts: a
                        }
                    }
                }
            }

            function n() {
                var t = document.createElement("style");
                return t.type = "text/css", u.appendChild(t), t
            }

            function r(t) {
                var e, i, o = document.querySelector('style[data-vue-ssr-id~="' + t.id + '"]');
                if (o) {
                    if (h) return m;
                    o.parentNode.removeChild(o)
                }
                if (g) {
                    var r = p++;
                    o = c || (c = n()), e = a.bind(null, o, r, !1), i = a.bind(null, o, r, !0)
                } else o = n(), e = s.bind(null, o), i = function() {
                    o.parentNode.removeChild(o)
                };
                return e(t),
                    function(o) {
                        if (o) {
                            if (o.css === t.css && o.media === t.media && o.sourceMap === t.sourceMap) return;
                            e(t = o)
                        } else i()
                    }
            }

            function a(t, e, i, o) {
                var n = i ? "" : o.css;
                if (t.styleSheet) t.styleSheet.cssText = b(e, n);
                else {
                    var r = document.createTextNode(n),
                        a = t.childNodes;
                    a[e] && t.removeChild(a[e]), a.length ? t.insertBefore(r, a[e]) : t.appendChild(r)
                }
            }

            function s(t, e) {
                var i = e.css,
                    o = e.media,
                    n = e.sourceMap;
                if (o && t.setAttribute("media", o), n && (i += "\n/*# sourceURL=" + n.sources[0] + " */", i += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(n)))) + " */"), t.styleSheet) t.styleSheet.cssText = i;
                else {
                    for (; t.firstChild;) t.removeChild(t.firstChild);
                    t.appendChild(document.createTextNode(i))
                }
            }
            var l = "undefined" != typeof document,
                f = i(9),
                d = {},
                u = l && (document.head || document.getElementsByTagName("head")[0]),
                c = null,
                p = 0,
                h = !1,
                m = function() {},
                g = "undefined" != typeof navigator && /msie [6-9]\b/.test(navigator.userAgent.toLowerCase());
            t.exports = function(t, e, i) {
                h = i;
                var n = f(t, e);
                return o(n),
                    function(e) {
                        for (var i = [], r = 0; r < n.length; r++) {
                            var a = n[r],
                                s = d[a.id];
                            s.refs--, i.push(s)
                        }
                        e ? (n = f(t, e), o(n)) : n = [];
                        for (var r = 0; r < i.length; r++) {
                            var s = i[r];
                            if (0 === s.refs) {
                                for (var l = 0; l < s.parts.length; l++) s.parts[l]();
                                delete d[s.id]
                            }
                        }
                    }
            };
            var b = function() {
                var t = [];
                return function(e, i) {
                    return t[e] = i, t.filter(Boolean).join("\n")
                }
            }()
        }, function(t, e) {
            t.exports = function(t, e) {
                for (var i = [], o = {}, n = 0; n < e.length; n++) {
                    var r = e[n],
                        a = r[0],
                        s = r[1],
                        l = r[2],
                        f = r[3],
                        d = {
                            id: t + ":" + n,
                            css: s,
                            media: l,
                            sourceMap: f
                        };
                    o[a] ? o[a].parts.push(d) : i.push(o[a] = {
                        id: a,
                        parts: [d]
                    })
                }
                return i
            }
        }])
    }
});