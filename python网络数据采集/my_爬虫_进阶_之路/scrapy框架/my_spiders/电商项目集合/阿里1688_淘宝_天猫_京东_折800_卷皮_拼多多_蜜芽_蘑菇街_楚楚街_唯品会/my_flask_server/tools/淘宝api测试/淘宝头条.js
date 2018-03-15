! function(e) {
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
}([function(e, t, n) {
    "use strict";
    var r = n(1),
        i = n(4);
    r(), e.exports = i
}, function(e, t, n) {
    var r = n(2),
        i = n(4),
        o = n(15);
    e.exports = function() {
        try {
            if (!window) return;
            if (window.JSTracker2 && window.JSTracker2.version) return;
            var e = [];
            window.JSTracker2 && window.JSTracker2.length > 0 && (e = window.JSTracker2);
            var t;
            window.g_config && window.g_config.jstracker2 && (t = window.g_config.jstracker2), window.JSTracker2 = new i(t);
            for (var n = 0; n < e.length; n++) window.JSTracker2.push(e[n]);
            o.call(JSTracker2);
            var a = window.onerror;
            window.onerror = function() {
                try {
                    a && a.apply(window, arguments);
                    var e = r.apply(window, arguments);
                    window.JSTracker2.push(e)
                } catch (t) {}
            }
        } catch (s) {}
    }
}, function(e, t, n) {
    var r = n(3);
    e.exports = function(e, t, n, i, o) {
        var o = r(o).toString(),
            a = {
                msg: e,
                file: t,
                line: n,
                col: i,
                stack: o.substr(0, 1024)
            };
        return a
    }
}, function(e, t) {
    function n(e, t, n, r) {
        this.funcName = e, this.file = t, this.line = n, this.col = r
    }
    n.prototype.toString = function() {
        return [this.funcName, this.file, this.line, this.col].join("|")
    };
    var r = /\S+\:\d+/,
        i = /\s+at /,
        o = {
            parse: function(e) {
                return e ? "undefined" != typeof e.stacktrace || "undefined" != typeof e["opera#sourceloc"] ? this.parseOpera(e) : e.stack && e.stack.match(i) ? this.parseV8OrIE(e) : e.stack && e.stack.match(r) ? this.parseFFOrSafari(e) : "" : ""
            },
            extractLocation: function(e) {
                if (e.indexOf(":") === -1) return [e];
                var t = e.replace(/[\(\)\s]/g, "").split(":"),
                    n = t.pop(),
                    r = t[t.length - 1];
                if (!isNaN(parseFloat(r)) && isFinite(r)) {
                    var i = t.pop();
                    return [t.join(":"), i, n]
                }
                return [t.join(":"), n, void 0]
            },
            parseV8OrIE: function(e) {
                return e.stack.split("\n").slice(1).map(function(e) {
                    var t = e.replace(/^\s+/, "").split(/\s+/).slice(1),
                        r = this.extractLocation(t.pop()),
                        i = t[0] && "Anonymous" !== t[0] ? t[0] : void 0;
                    return new n(i, (void 0), r[0], r[1], r[2])
                }, this)
            },
            parseFFOrSafari: function(e) {
                return e.stack.split("\n").filter(function(e) {
                    return !!e.match(r)
                }, this).map(function(e) {
                    var t = e.split("@"),
                        r = this.extractLocation(t.pop()),
                        i = t.shift() || void 0;
                    return new n(i, (void 0), r[0], r[1], r[2])
                }, this)
            },
            parseOpera: function(e) {
                return !e.stacktrace || e.message.indexOf("\n") > -1 && e.message.split("\n").length > e.stacktrace.split("\n").length ? this.parseOpera9(e) : e.stack ? this.parseOpera11(e) : this.parseOpera10(e)
            },
            parseOpera9: function(e) {
                for (var t = /Line (\d+).*script (?:in )?(\S+)/i, r = e.message.split("\n"), i = [], o = 2, a = r.length; o < a; o += 2) {
                    var s = t.exec(r[o]);
                    s && i.push(new n((void 0), (void 0), s[2], s[1]))
                }
                return i
            },
            parseOpera10: function(e) {
                for (var t = /Line (\d+).*script (?:in )?(\S+)(?:: In function (\S+))?$/i, r = e.stacktrace.split("\n"), i = [], o = 0, a = r.length; o < a; o += 2) {
                    var s = t.exec(r[o]);
                    s && i.push(new n(s[3] || void 0, (void 0), s[2], s[1]))
                }
                return i
            },
            parseOpera11: function(e) {
                return e.stack.split("\n").filter(function(e) {
                    return !!e.match(r) && !e.match(/^Error created at/)
                }, this).map(function(e) {
                    var t, r = e.split("@"),
                        i = this.extractLocation(r.pop()),
                        o = r.shift() || "",
                        a = o.replace(/<anonymous function(: (\w+))?>/, "$2").replace(/\([^\)]*\)/g, "") || void 0;
                    o.match(/\(([^\)]*)\)/) && (t = o.replace(/^[^\(]+\(([^\)]*)\)$/, "$1"));
                    var s = void 0 === t || "[arguments not available]" === t ? void 0 : t.split(",");
                    return new n(a, s, i[0], i[1], i[2])
                }, this)
            }
        };
    e.exports = function(e) {
        var t = o.parse(e);
        return t
    }
}, function(e, t, n) {
    function r(e) {
        var t = {
            msg: "",
            file: "",
            line: "",
            col: "",
            stack: "",
            url: "",
            ua: "",
            screen: "",
            nick: "",
            dns: "",
            con: "",
            req: "",
            res: "",
            dcl: "",
            onload: "",
            type: "",
            ki: ""
        };
        this.version = "o4.2.0", t = {
            v: this.version,
            ua: o,
            screen: a,
            sampling: 100,
            nick: s,
            ki: c
        }, this._debug = location.href.indexOf("jt_debug") != -1, this._pushed_num = 0, this._config = u.merge(t, e)
    }
    var i = n(5),
        o = n(11),
        a = n(12),
        s = n(13),
        c = n(14),
        u = n(10);
    r.prototype.push = i, e.exports = r
}, function(e, t, n) {
    var r = n(6),
        i = n(7),
        o = n(9),
        a = n(8),
        s = n(10);
    e.exports = function(e) {
        try {
            if (!e) return;
            e && e.constructor === Object || (e = r(e)), e = s.merge(this._config, e);
            var t = a;
            e.t = t();
            for (var n in e) "" !== e[n] && null !== e[n] && void 0 !== e[n] || delete e[n];
            var c = s.stringify(e),
                u = e.sampling;
            if (u < 1 && (u = 9999999, "undefined" != typeof console && console.warn && console.warn("JSTracker2 sampling is invalid, please set a integer above 1!")), "__PV" !== e.msg && !this._debug && Math.random() * u > 1);
            else if (this._pushed_num < 10) {
                this._pushed_num++, this._debug && window.console && window.console.log(e);
                var p = o.call(this);
                i(p + c)
            }
        } catch (d) {}
    }
}, function(e, t, n) {
    var r = n(3);
    e.exports = function(e) {
        var t = {
            msg: e.message,
            file: "",
            line: "",
            col: "",
            stack: r(e).toString()
        };
        return t
    }
}, function(e, t, n) {
    var r = n(8);
    e.exports = function(e) {
        var t = window,
            n = "jsFeImage_" + r(),
            i = t[n] = new Image;
        i.onload = i.onerror = function() {
            t[n] = null
        }, i.src = e
    }
}, function(e, t) {
    var n = function() {
        return +new Date + ".r" + Math.floor(1e3 * Math.random())
    };
    e.exports = n
}, function(e, t) {
    e.exports = function() {
        var e = "//gm.mmstat.com";
        return this._config.server && (e = this._config.server), e + "/jstracker.3?"
    }
}, function(e, t) {
    e.exports = {
        merge: function(e, t) {
            var n = {};
            for (var r in e) n[r] = e[r];
            for (var r in t) n[r] = t[r];
            return n
        },
        stringify: function(e) {
            var t = [];
            for (var n in e) t.push(n + "=" + encodeURIComponent(e[n]));
            return t.join("&")
        },
        now: function() {
            return window.performance && window.performance.now ? window.performance.now() : Date && "function" == typeof Date.now ? Date.now() : new Date
        }
    }
}, function(e, t) {
    var n = function() {
        try {
            if (/UBrowser/i.test(navigator.userAgent)) return "";
            if ("undefined" != typeof window.scrollMaxX) return "";
            var e = "track" in document.createElement("track"),
                t = window.chrome && window.chrome.webstore ? Object.keys(window.chrome.webstore).length : 0;
            return window.clientInformation && window.clientInformation.languages && window.clientInformation.languages.length > 2 ? "" : e ? t > 1 ? " QIHU 360 EE" : " QIHU 360 SE" : ""
        } catch (n) {
            return ""
        }
    }();
    e.exports = navigator.userAgent + n
}, function(e, t) {
    e.exports = screen.width + "x" + screen.height
}, function(e, t) {
    var n = null;
    try {
        var r = /_nk_=([^;]+)/.exec(document.cookie) || /_w_tb_nick=([^;]+)/.exec(document.cookie) || /lgc=([^;]+)/.exec(document.cookie);
        r && (n = decodeURIComponent(r[1]))
    } catch (i) {}
    e.exports = n
}, function(e, t) {
    function n() {
        try {
            return KISSY.version
        } catch (e) {
            return null
        }
    }
    e.exports = n()
}, function(e, t, n) {
    var r = n(16),
        i = n(18);
    e.exports = function() {
        var e = this,
            t = 100;
        if (this._config.p_sampling && (t = this._config.p_sampling), this._debug || !(Math.random() * t > 1)) {
            if (this._cpu = new i, window.performance && window.performance.memory) try {
                var n = parseInt(window.performance.memory.usedJSHeapSize),
                    o = parseInt(window.performance.memory.totalJSHeapSize);
                n && (this._jsHeapSizeData = {
                    jsHeapUsed: n
                }, o && (this._jsHeapSizeData.jsHeapUsedRate = (n / o).toFixed(4)))
            } catch (a) {}
            setTimeout(function() {
                try {
                    var t = r.call(e);
                    window.JSTracker2.push(t)
                } catch (n) {}
            }, 2e4)
        }
    }
}, function(e, t, n) {
    var r = n(17),
        i = n(10);
    e.exports = function() {
        var e = {},
            t = window;
        if (t.performance) {
            var n = t.performance.timing;
            e.dns = n.domainLookupEnd - n.domainLookupStart, e.con = n.connectEnd - n.connectStart, e.req = n.responseStart - n.requestStart, e.res = n.responseEnd - n.responseStart, e.dcl = n.domContentLoadedEventEnd - n.domLoading, e.onload = n.loadEventStart - n.domLoading, e.type = window.performance.navigation.type, e.sampling = 100
        }
        e.msg = "__PV";
        var o = r.call(this);
        return e.stack = i.stringify(o), e
    }
}, function(e, t, n) {
    var r = n(10);
    e.exports = function() {
        var e = window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance,
            t = {};
        if (e) {
            var n = e.timing;
            if (n) {
                if (void 0 === t.firstPaint) {
                    var i = -1;
                    window.chrome && window.chrome.loadTimes ? (i = 1e3 * window.chrome.loadTimes().firstPaintTime, i -= 1e3 * window.chrome.loadTimes().startLoadTime) : "number" == typeof window.performance.timing.msFirstPaint && (i = window.performance.timing.msFirstPaint, t.firstPaint = i - window.performance.timing.navigationStart), t.firstPaint = Math.floor(i)
                }
                t.load = n.loadEventEnd - n.fetchStart, t.domReady = n.domComplete - n.domInteractive, t.readyStart = n.fetchStart - n.navigationStart, t.redirect = n.redirectEnd - n.redirectStart, t.appcache = n.domainLookupStart - n.fetchStart, t.unloadEvent = n.unloadEventEnd - n.unloadEventStart, t.lookupDomain = n.domainLookupEnd - n.domainLookupStart, t.connect = n.connectEnd - n.connectStart, t.request = n.responseEnd - n.requestStart, t.initDomTree = n.domInteractive - n.responseEnd, t.loadEvent = n.loadEventEnd - n.loadEventStart
            }
        }
        if (this._jsHeapSizeData && (t = r.merge(t, this._jsHeapSizeData)), this._cpu) {
            this._cpu.pause(), t.busy = Math.floor(this._cpu.getTotalSize(0, 15e3));
            for (var o = this._cpu.data.dataArray, a = -1, s = 0, c = 0; c < o.length && (o[c] <= .1 ? a++ : (s = c + 1, a = 0), !(a >= 5)); c++);
            t.avail = Math.floor(this._cpu.data.timeArray[s] - this._cpu.data.timeArray[0]), t.busyPer = Math.floor(this._cpu.getOverPerAmount(1, 0, 15e3) / this._cpu.getOverPerAmount(0, 0, 15e3) * 100), this._debug && window.console && window.console.log(t)
        }
        return t
    }
}, function(e, t) {
    ! function(e) {
        function t() {
            this.conf = {
                log: !1,
                consoleUI: !1,
                delay: 100,
                stat: !0,
                ui: !1
            }, this.log("start"), this.run(), this._lastTime = this.now(), this.data = {
                timeArray: [],
                per_line: [],
                time_line: [],
                size_line: [],
                averageTime: this.conf.delay,
                totalSize: 0,
                dataArray: [],
                timeArray: []
            }, this.log("end")
        }
        t.prototype.run = function() {
            var e, t = this;
            t.conf.ui, window.addEventListener && window.addEventListener("touchmove", function() {
                t.resumeFlag = !0
            }, !1), this._timerID = setTimeout(function() {
                if (!t.isPause) {
                    t.currentTime = t.now(), e = (t.currentTime - t._lastTime - t.conf.delay - 0) / t.conf.delay, e < 0 && (e = 0), e > 1 && (e = 1), t._lastTime = t.currentTime;
                    var n = t.getStepPer(t.now(), e),
                        r = Math.floor(n / .5) + 1;
                    if (r = r > 200 ? 200 : r, t.resumeFlag) t.resumeFlag = !1;
                    else
                        for (var i = 0; i < r; i++) t.logPercent(e);
                    t._timerID = setTimeout(arguments.callee, t.conf.delay)
                }
            }, t.conf.delay)
        }, t.prototype.now = function() {
            return window.performance && window.performance.now ? window.performance.now() : Date && "function" == typeof Date.now ? Date.now() : new Date
        }, t.prototype.log = function(t) {
            this.conf.log && e.console && e.console.log && e.console.log("### CPU Log:" + t)
        }, t.prototype.getStepPer = function(e, t) {
            var n = this.data;
            n.time_line.push(e);
            var r;
            n.per_line.push(t);
            var i = n.time_line.length;
            r = 1 == n.time_line.length ? n.averageTime : e - n.time_line[i - 2], r < n.averageTime && (r = n.averageTime);
            var o = (r - n.averageTime) / n.averageTime;
            return i >= 2 ? (n.totalSize += (n.per_line[i - 1] + n.per_line[i - 2]) * (n.time_line[i - 1] - n.time_line[i - 2]) / 2, n.size_line.push(n.totalSize)) : n.size_line.push(0), n.per_line.length > 2 && (n.per_line.shift(), n.time_line.shift()), o
        }, t.prototype.drawUIByConsole = function(e) {
            for (var t = Math.round(10 * e), n = "鈻�", r = t; r--;) n += "鈻�";
            n += Math.round(100 * e), this.log(n)
        }, t.prototype.pause = function() {
            clearTimeout(this._timerID), this.isPause = !0, this.log("###########################PAUSE!!!!!!!!!")
        }, t.prototype.resume = function() {
            (null == this.isPause || this.isPause) && (this._lastTime = this.now() + 1e4, this.isPause = !1, this.resumeFlag = !0, this.log("###########################RESUME!!!!!!!!!"), this.run())
        }, t.prototype.logPercent = function(e) {
            this.conf.stat && this.logStat(e), this.conf.ui, this.conf.consoleUI && this.drawUIByConsole(e)
        }, t.prototype.logStat = function(e) {
            var t = this.data;
            t.dataArray.push(e), t.timeArray.push(this.now())
        }, t.prototype.getCurrentCPU = function() {
            for (var e = this.data, t = e.dataArray, n = 0, r = t.length, i = 0, o = r - 1; o >= 0 && (i += t[o], n++, !(n >= 3)); o--);
            return 0 == n ? 0 : i / n
        }, t.prototype.getTimeIndex = function(e, t) {
            for (var n = this.data.timeArray, r = 0; r < n.length; r++)
                if (t) {
                    if (n[r] - n[0] > e) return r - 1
                } else if (n[r] - n[0] >= e) return r;
            return n.length
        }, t.prototype.getOverPerAmount = function(e, t, n) {
            for (var r = this.data, i = this.getTimeIndex(t), o = this.getTimeIndex(n, 1), a = r.dataArray, s = 0, c = i; c < o; c++) "undefined" != typeof a[c] && a[c] >= e && s++;
            return s
        }, t.prototype.getTotalSize = function(e, t) {
            var n = this.data,
                r = this.getTimeIndex(e),
                i = this.getTimeIndex(t, !0),
                o = n.size_line[i];
            o || (o = n.size_line[n.size_line.length - 1]);
            var a = o - n.size_line[r];
            return a
        }, e.cpu = t
    }(window), e.exports = cpu
}]);
! function(a, b) {
    function c(a, b) {
        a = a.toString().split("."), b = b.toString().split(".");
        for (var c = 0; c < a.length || c < b.length; c++) {
            var d = parseInt(a[c], 10),
                e = parseInt(b[c], 10);
            if (window.isNaN(d) && (d = 0), window.isNaN(e) && (e = 0), d < e) return -1;
            if (d > e) return 1
        }
        return 0
    }
    var d = a.Promise,
        e = a.document,
        f = a.navigator.userAgent,
        g = /Windows\sPhone\s(?:OS\s)?[\d\.]+/i.test(f) || /Windows\sNT\s[\d\.]+/i.test(f),
        h = g && a.WindVane_Win_Private && a.WindVane_Win_Private.call,
        i = /iPhone|iPad|iPod/i.test(f),
        j = /Android/i.test(f),
        k = f.match(/WindVane[\/\s](\d+[._]\d+[._]\d+)/),
        l = Object.prototype.hasOwnProperty,
        m = b.windvane = a.WindVane || (a.WindVane = {}),
        n = (a.WindVane_Native, Math.floor(65536 * Math.random())),
        o = 1,
        p = [],
        q = 3,
        r = "hybrid",
        s = "wv_hybrid",
        t = "iframe_",
        u = "param_",
        v = "chunk_",
        w = 6e5,
        x = 6e5,
        y = 6e4;
    k = k ? (k[1] || "0.0.0").replace(/\_/g, ".") : "0.0.0";
    var z = {
            isAvailable: 1 === c(k, "0"),
            call: function(a, b, c, e, f, g) {
                var h, i;
                "number" == typeof arguments[arguments.length - 1] && (g = arguments[arguments.length - 1]), "function" != typeof e && (e = null), "function" != typeof f && (f = null), d && (i = {}, i.promise = new d(function(a, b) {
                    i.resolve = a, i.reject = b
                })), h = A.getSid();
                var j = {
                    success: e,
                    failure: f,
                    deferred: i
                };
                if (g > 0 && (j.timeout = setTimeout(function() {
                        z.onFailure(h, {
                            ret: "HY_TIMEOUT"
                        })
                    }, g)), A.registerCall(h, j), A.registerGC(h, g), z.isAvailable ? A.callMethod(a, b, c, h) : z.onFailure(h, {
                        ret: "HY_NOT_IN_WINDVANE"
                    }), i) return i.promise
            },
            fireEvent: function(a, b, c) {
                var d = e.createEvent("HTMLEvents");
                d.initEvent(a, !1, !0), d.param = A.parseData(b || A.getData(c)), e.dispatchEvent(d)
            },
            getParam: function(a) {
                return A.getParam(a)
            },
            setData: function(a, b) {
                A.setData(a, b)
            },
            onSuccess: function(a, b) {
                A.onComplete(a, b, "success")
            },
            onFailure: function(a, b) {
                A.onComplete(a, b, "failure")
            }
        },
        A = {
            params: {},
            chunks: {},
            calls: {},
            getSid: function() {
                return (n + o++) % 65536 + ""
            },
            buildParam: function(a) {
                return a && "object" == typeof a ? JSON.stringify(a) : a || ""
            },
            getParam: function(a) {
                return this.params[u + a] || ""
            },
            setParam: function(a, b) {
                this.params[u + a] = b
            },
            parseData: function(a) {
                var b;
                if (a && "string" == typeof a) try {
                    b = JSON.parse(a)
                } catch (a) {
                    b = {
                        ret: ["WV_ERR::PARAM_PARSE_ERROR"]
                    }
                } else b = a || {};
                return b
            },
            setData: function() {
                this.chunks[v + sid] = this.chunks[v + sid] || [], this.chunks[v + sid].push(chunk)
            },
            getData: function(a) {
                return this.chunks[v + a] ? this.chunks[v + a].join("") : ""
            },
            registerCall: function(a, b) {
                this.calls[a] = b
            },
            unregisterCall: function(a) {
                var b = {};
                return this.calls[a] && (b = this.calls[a], delete this.calls[a]), b
            },
            useIframe: function(a, b) {
                var c = t + a,
                    d = p.pop();
                d || (d = e.createElement("iframe"), d.setAttribute("frameborder", "0"), d.style.cssText = "width:0;height:0;border:0;display:none;"), d.setAttribute("id", c), d.setAttribute("src", b), d.parentNode || setTimeout(function() {
                    e.body.appendChild(d)
                }, 5)
            },
            retrieveIframe: function(a) {
                var b = t + a,
                    c = e.querySelector("#" + b);
                p.length >= q ? e.body.removeChild(c) : p.indexOf(c) < 0 && p.push(c)
            },
            callMethod: function(b, c, d, e) {
                if (d = A.buildParam(d), g) h ? a.WindVane_Win_Private.call(b, c, e, d) : this.onComplete(e, {
                    ret: "HY_NO_HANDLER_ON_WP"
                }, "failure");
                else {
                    var f = r + "://" + b + ":" + e + "/" + c + "?" + d;
                    if (i) this.setParam(e, d), this.useIframe(e, f);
                    else if (j) {
                        var k = s + ":";
                        window.prompt(f, k)
                    } else this.onComplete(e, {
                        ret: "HY_NOT_SUPPORT_DEVICE"
                    }, "failure")
                }
            },
            registerGC: function(a, b) {
                var c = this,
                    d = Math.max(b || 0, w),
                    e = Math.max(b || 0, y),
                    f = Math.max(b || 0, x);
                setTimeout(function() {
                    c.unregisterCall(a)
                }, d), i ? setTimeout(function() {
                    c.params[u + a] && delete c.params[u + a]
                }, e) : j && setTimeout(function() {
                    c.chunks[v + a] && delete c.chunks[v + a]
                }, f)
            },
            onComplete: function(a, b, c) {
                var d = this.unregisterCall(a),
                    e = d.success,
                    f = d.failure,
                    g = d.deferred,
                    h = d.timeout;
                h && clearTimeout(h), b = b ? b : this.getData(a), b = this.parseData(b);
                var k = b.ret;
                "string" == typeof k && (b = b.value || b, b.ret || (b.ret = [k])), "success" === c ? (e && e(b), g && g.resolve(b)) : "failure" === c && (f && f(b), g && g.reject(b)), i ? (this.retrieveIframe(a), this.params[u + a] && delete this.params[u + a]) : j && this.chunks[v + a] && delete this.chunks[v + a]
            }
        };
    for (var B in z) l.call(m, B) || (m[B] = z[B])
}(window, window.lib || (window.lib = {}));
! function a(b, c, d) {
    function e(g, h) {
        if (!c[g]) {
            if (!b[g]) {
                var i = "function" == typeof require && require;
                if (!h && i) return i(g, !0);
                if (f) return f(g, !0);
                var j = new Error("Cannot find module '" + g + "'");
                throw j.code = "MODULE_NOT_FOUND", j
            }
            var k = c[g] = {
                exports: {}
            };
            b[g][0].call(k.exports, function(a) {
                var c = b[g][1][a];
                return e(c ? c : a)
            }, k, k.exports, a, b, c, d)
        }
        return c[g].exports
    }
    for (var f = "function" == typeof require && require, g = 0; g < d.length; g++) e(d[g]);
    return e
}({
    1: [function(a, b) {
        function c() {}
        var d = b.exports = {};
        d.nextTick = function() {
            var a = "undefined" != typeof window && window.setImmediate,
                b = "undefined" != typeof window && window.postMessage && window.addEventListener;
            if (a) return function(a) {
                return window.setImmediate(a)
            };
            if (b) {
                var c = [];
                return window.addEventListener("message", function(a) {
                        var b = a.source;
                        if ((b === window || null === b) && "process-tick" === a.data && (a.stopPropagation(), c.length > 0)) {
                            var d = c.shift();
                            d()
                        }
                    }, !0),
                    function(a) {
                        c.push(a), window.postMessage("process-tick", "*")
                    }
            }
            return function(a) {
                setTimeout(a, 0)
            }
        }(), d.title = "browser", d.browser = !0, d.env = {}, d.argv = [], d.on = c, d.addListener = c, d.once = c, d.off = c, d.removeListener = c, d.removeAllListeners = c, d.emit = c, d.binding = function() {
            throw new Error("process.binding is not supported")
        }, d.cwd = function() {
            return "/"
        }, d.chdir = function() {
            throw new Error("process.chdir is not supported")
        }
    }, {}],
    2: [function(a, b) {
        "use strict";

        function c(a) {
            function b(a) {
                return null === i ? void k.push(a) : void f(function() {
                    var b = i ? a.onFulfilled : a.onRejected;
                    if (null === b) return void(i ? a.resolve : a.reject)(j);
                    var c;
                    try {
                        c = b(j)
                    } catch (d) {
                        return void a.reject(d)
                    }
                    a.resolve(c)
                })
            }

            function c(a) {
                try {
                    if (a === l) throw new TypeError("A promise cannot be resolved with itself.");
                    if (a && ("object" == typeof a || "function" == typeof a)) {
                        var b = a.then;
                        if ("function" == typeof b) return void e(b.bind(a), c, g)
                    }
                    i = !0, j = a, h()
                } catch (d) {
                    g(d)
                }
            }

            function g(a) {
                i = !1, j = a, h()
            }

            function h() {
                for (var a = 0, c = k.length; c > a; a++) b(k[a]);
                k = null
            }
            if ("object" != typeof this) throw new TypeError("Promises must be constructed via new");
            if ("function" != typeof a) throw new TypeError("not a function");
            var i = null,
                j = null,
                k = [],
                l = this;
            this.then = function(a, c) {
                return new l.constructor(function(e, f) {
                    b(new d(a, c, e, f))
                })
            }, e(a, c, g)
        }

        function d(a, b, c, d) {
            this.onFulfilled = "function" == typeof a ? a : null, this.onRejected = "function" == typeof b ? b : null, this.resolve = c, this.reject = d
        }

        function e(a, b, c) {
            var d = !1;
            try {
                a(function(a) {
                    d || (d = !0, b(a))
                }, function(a) {
                    d || (d = !0, c(a))
                })
            } catch (e) {
                if (d) return;
                d = !0, c(e)
            }
        }
        var f = a("asap");
        b.exports = c
    }, {
        asap: 4
    }],
    3: [function(a, b) {
        "use strict";

        function c(a) {
            this.then = function(b) {
                return "function" != typeof b ? this : new d(function(c, d) {
                    e(function() {
                        try {
                            c(b(a))
                        } catch (e) {
                            d(e)
                        }
                    })
                })
            }
        }
        var d = a("./core.js"),
            e = a("asap");
        b.exports = d, c.prototype = d.prototype;
        var f = new c(!0),
            g = new c(!1),
            h = new c(null),
            i = new c(void 0),
            j = new c(0),
            k = new c("");
        d.resolve = function(a) {
            if (a instanceof d) return a;
            if (null === a) return h;
            if (void 0 === a) return i;
            if (a === !0) return f;
            if (a === !1) return g;
            if (0 === a) return j;
            if ("" === a) return k;
            if ("object" == typeof a || "function" == typeof a) try {
                var b = a.then;
                if ("function" == typeof b) return new d(b.bind(a))
            } catch (e) {
                return new d(function(a, b) {
                    b(e)
                })
            }
            return new c(a)
        }, d.all = function(a) {
            var b = Array.prototype.slice.call(a);
            return new d(function(a, c) {
                function d(f, g) {
                    try {
                        if (g && ("object" == typeof g || "function" == typeof g)) {
                            var h = g.then;
                            if ("function" == typeof h) return void h.call(g, function(a) {
                                d(f, a)
                            }, c)
                        }
                        b[f] = g, 0 === --e && a(b)
                    } catch (i) {
                        c(i)
                    }
                }
                if (0 === b.length) return a([]);
                for (var e = b.length, f = 0; f < b.length; f++) d(f, b[f])
            })
        }, d.reject = function(a) {
            return new d(function(b, c) {
                c(a)
            })
        }, d.race = function(a) {
            return new d(function(b, c) {
                a.forEach(function(a) {
                    d.resolve(a).then(b, c)
                })
            })
        }, d.prototype["catch"] = function(a) {
            return this.then(null, a)
        }
    }, {
        "./core.js": 2,
        asap: 4
    }],
    4: [function(a, b) {
        (function(a) {
            function c() {
                for (; e.next;) {
                    e = e.next;
                    var a = e.task;
                    e.task = void 0;
                    var b = e.domain;
                    b && (e.domain = void 0, b.enter());
                    try {
                        a()
                    } catch (d) {
                        if (i) throw b && b.exit(), setTimeout(c, 0), b && b.enter(), d;
                        setTimeout(function() {
                            throw d
                        }, 0)
                    }
                    b && b.exit()
                }
                g = !1
            }

            function d(b) {
                f = f.next = {
                    task: b,
                    domain: i && a.domain,
                    next: null
                }, g || (g = !0, h())
            }
            var e = {
                    task: void 0,
                    next: null
                },
                f = e,
                g = !1,
                h = void 0,
                i = !1;
            if ("undefined" != typeof a && a.nextTick) i = !0, h = function() {
                a.nextTick(c)
            };
            else if ("function" == typeof setImmediate) h = "undefined" != typeof window ? setImmediate.bind(window, c) : function() {
                setImmediate(c)
            };
            else if ("undefined" != typeof MessageChannel) {
                var j = new MessageChannel;
                j.port1.onmessage = c, h = function() {
                    j.port2.postMessage(0)
                }
            } else h = function() {
                setTimeout(c, 0)
            };
            b.exports = d
        }).call(this, a("_process"))
    }, {
        _process: 1
    }],
    5: [function() {
        "function" != typeof Promise.prototype.done && (Promise.prototype.done = function() {
            var a = arguments.length ? this.then.apply(this, arguments) : this;
            a.then(null, function(a) {
                setTimeout(function() {
                    throw a
                }, 0)
            })
        })
    }, {}],
    6: [function(a) {
        a("asap");
        "undefined" == typeof Promise && (Promise = a("./lib/core.js"), a("./lib/es6-extensions.js")), a("./polyfill-done.js")
    }, {
        "./lib/core.js": 2,
        "./lib/es6-extensions.js": 3,
        "./polyfill-done.js": 5,
        asap: 4
    }]
}, {}, [6]);
! function(a, b) {
    function c() {
        var a = {},
            b = new o(function(b, c) {
                a.resolve = b, a.reject = c
            });
        return a.promise = b, a
    }

    function d(a, b) {
        for (var c in b) void 0 === a[c] && (a[c] = b[c]);
        return a
    }

    function e(a) {
        var b = document.getElementsByTagName("head")[0] || document.getElementsByTagName("body")[0] || document.firstElementChild || document;
        b.appendChild(a)
    }

    function f(a) {
        var b = [];
        for (var c in a) a[c] && b.push(c + "=" + encodeURIComponent(a[c]));
        return b.join("&")
    }

    function g(a) {
        return a.substring(a.lastIndexOf(".", a.lastIndexOf(".") - 1) + 1)
    }

    function h(a) {
        function b(a, b) {
            return a << b | a >>> 32 - b
        }

        function c(a, b) {
            var c, d, e, f, g;
            return e = 2147483648 & a, f = 2147483648 & b, c = 1073741824 & a, d = 1073741824 & b, g = (1073741823 & a) + (1073741823 & b), c & d ? 2147483648 ^ g ^ e ^ f : c | d ? 1073741824 & g ? 3221225472 ^ g ^ e ^ f : 1073741824 ^ g ^ e ^ f : g ^ e ^ f
        }

        function d(a, b, c) {
            return a & b | ~a & c
        }

        function e(a, b, c) {
            return a & c | b & ~c
        }

        function f(a, b, c) {
            return a ^ b ^ c
        }

        function g(a, b, c) {
            return b ^ (a | ~c)
        }

        function h(a, e, f, g, h, i, j) {
            return a = c(a, c(c(d(e, f, g), h), j)), c(b(a, i), e)
        }

        function i(a, d, f, g, h, i, j) {
            return a = c(a, c(c(e(d, f, g), h), j)), c(b(a, i), d)
        }

        function j(a, d, e, g, h, i, j) {
            return a = c(a, c(c(f(d, e, g), h), j)), c(b(a, i), d)
        }

        function k(a, d, e, f, h, i, j) {
            return a = c(a, c(c(g(d, e, f), h), j)), c(b(a, i), d)
        }

        function l(a) {
            for (var b, c = a.length, d = c + 8, e = (d - d % 64) / 64, f = 16 * (e + 1), g = new Array(f - 1), h = 0, i = 0; c > i;) b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | a.charCodeAt(i) << h, i++;
            return b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | 128 << h, g[f - 2] = c << 3, g[f - 1] = c >>> 29, g
        }

        function m(a) {
            var b, c, d = "",
                e = "";
            for (c = 0; 3 >= c; c++) b = a >>> 8 * c & 255, e = "0" + b.toString(16), d += e.substr(e.length - 2, 2);
            return d
        }

        function n(a) {
            a = a.replace(/\r\n/g, "\n");
            for (var b = "", c = 0; c < a.length; c++) {
                var d = a.charCodeAt(c);
                128 > d ? b += String.fromCharCode(d) : d > 127 && 2048 > d ? (b += String.fromCharCode(d >> 6 | 192), b += String.fromCharCode(63 & d | 128)) : (b += String.fromCharCode(d >> 12 | 224), b += String.fromCharCode(d >> 6 & 63 | 128), b += String.fromCharCode(63 & d | 128))
            }
            return b
        }
        var o, p, q, r, s, t, u, v, w, x = [],
            y = 7,
            z = 12,
            A = 17,
            B = 22,
            C = 5,
            D = 9,
            E = 14,
            F = 20,
            G = 4,
            H = 11,
            I = 16,
            J = 23,
            K = 6,
            L = 10,
            M = 15,
            N = 21;
        for (a = n(a), x = l(a), t = 1732584193, u = 4023233417, v = 2562383102, w = 271733878, o = 0; o < x.length; o += 16) p = t, q = u, r = v, s = w, t = h(t, u, v, w, x[o + 0], y, 3614090360), w = h(w, t, u, v, x[o + 1], z, 3905402710), v = h(v, w, t, u, x[o + 2], A, 606105819), u = h(u, v, w, t, x[o + 3], B, 3250441966), t = h(t, u, v, w, x[o + 4], y, 4118548399), w = h(w, t, u, v, x[o + 5], z, 1200080426), v = h(v, w, t, u, x[o + 6], A, 2821735955), u = h(u, v, w, t, x[o + 7], B, 4249261313), t = h(t, u, v, w, x[o + 8], y, 1770035416), w = h(w, t, u, v, x[o + 9], z, 2336552879), v = h(v, w, t, u, x[o + 10], A, 4294925233), u = h(u, v, w, t, x[o + 11], B, 2304563134), t = h(t, u, v, w, x[o + 12], y, 1804603682), w = h(w, t, u, v, x[o + 13], z, 4254626195), v = h(v, w, t, u, x[o + 14], A, 2792965006), u = h(u, v, w, t, x[o + 15], B, 1236535329), t = i(t, u, v, w, x[o + 1], C, 4129170786), w = i(w, t, u, v, x[o + 6], D, 3225465664), v = i(v, w, t, u, x[o + 11], E, 643717713), u = i(u, v, w, t, x[o + 0], F, 3921069994), t = i(t, u, v, w, x[o + 5], C, 3593408605), w = i(w, t, u, v, x[o + 10], D, 38016083), v = i(v, w, t, u, x[o + 15], E, 3634488961), u = i(u, v, w, t, x[o + 4], F, 3889429448), t = i(t, u, v, w, x[o + 9], C, 568446438), w = i(w, t, u, v, x[o + 14], D, 3275163606), v = i(v, w, t, u, x[o + 3], E, 4107603335), u = i(u, v, w, t, x[o + 8], F, 1163531501), t = i(t, u, v, w, x[o + 13], C, 2850285829), w = i(w, t, u, v, x[o + 2], D, 4243563512), v = i(v, w, t, u, x[o + 7], E, 1735328473), u = i(u, v, w, t, x[o + 12], F, 2368359562), t = j(t, u, v, w, x[o + 5], G, 4294588738), w = j(w, t, u, v, x[o + 8], H, 2272392833), v = j(v, w, t, u, x[o + 11], I, 1839030562), u = j(u, v, w, t, x[o + 14], J, 4259657740), t = j(t, u, v, w, x[o + 1], G, 2763975236), w = j(w, t, u, v, x[o + 4], H, 1272893353), v = j(v, w, t, u, x[o + 7], I, 4139469664), u = j(u, v, w, t, x[o + 10], J, 3200236656), t = j(t, u, v, w, x[o + 13], G, 681279174), w = j(w, t, u, v, x[o + 0], H, 3936430074), v = j(v, w, t, u, x[o + 3], I, 3572445317), u = j(u, v, w, t, x[o + 6], J, 76029189), t = j(t, u, v, w, x[o + 9], G, 3654602809), w = j(w, t, u, v, x[o + 12], H, 3873151461), v = j(v, w, t, u, x[o + 15], I, 530742520), u = j(u, v, w, t, x[o + 2], J, 3299628645), t = k(t, u, v, w, x[o + 0], K, 4096336452), w = k(w, t, u, v, x[o + 7], L, 1126891415), v = k(v, w, t, u, x[o + 14], M, 2878612391), u = k(u, v, w, t, x[o + 5], N, 4237533241), t = k(t, u, v, w, x[o + 12], K, 1700485571), w = k(w, t, u, v, x[o + 3], L, 2399980690), v = k(v, w, t, u, x[o + 10], M, 4293915773), u = k(u, v, w, t, x[o + 1], N, 2240044497), t = k(t, u, v, w, x[o + 8], K, 1873313359), w = k(w, t, u, v, x[o + 15], L, 4264355552), v = k(v, w, t, u, x[o + 6], M, 2734768916), u = k(u, v, w, t, x[o + 13], N, 1309151649), t = k(t, u, v, w, x[o + 4], K, 4149444226), w = k(w, t, u, v, x[o + 11], L, 3174756917), v = k(v, w, t, u, x[o + 2], M, 718787259), u = k(u, v, w, t, x[o + 9], N, 3951481745), t = c(t, p), u = c(u, q), v = c(v, r), w = c(w, s);
        var O = m(t) + m(u) + m(v) + m(w);
        return O.toLowerCase()
    }

    function i(a, b, c) {
        var d = c || {};
        document.cookie = a.replace(/[^+#$&^`|]/g, encodeURIComponent).replace("(", "%28").replace(")", "%29") + "=" + b.replace(/[^+#$&\/:<-\[\]-}]/g, encodeURIComponent) + (d.domain ? ";domain=" + d.domain : "") + (d.path ? ";path=" + d.path : "") + (d.secure ? ";secure" : "") + (d.httponly ? ";HttpOnly" : "")
    }

    function j(a) {
        var b = new RegExp("(?:^|;\\s*)" + a + "\\=([^;]+)(?:;\\s*|$)").exec(document.cookie);
        return b ? b[1] : void 0
    }

    function k(a, b, c) {
        var d = new Date;
        d.setTime(d.getTime() - 864e5);
        var e = "/";
        document.cookie = a + "=;path=" + e + ";domain=." + b + ";expires=" + d.toGMTString(), document.cookie = a + "=;path=" + e + ";domain=." + c + "." + b + ";expires=" + d.toGMTString()
    }

    function l() {
        var b = a.location.hostname;
        if (!b) {
            var c = a.parent.location.hostname;
            c && ~c.indexOf("zebra.alibaba-inc.com") && (b = c)
        }
        var d = ["taobao.net", "taobao.com", "tmall.com", "tmall.hk", "alibaba-inc.com"],
            e = new RegExp("([^.]*?)\\.?((?:" + d.join(")|(?:").replace(/\./g, "\\.") + "))", "i"),
            f = b.match(e) || [],
            g = f[2] || "taobao.com",
            h = f[1] || "m";
        "taobao.net" !== g || "x" !== h && "waptest" !== h && "daily" !== h ? "taobao.net" === g && "demo" === h ? h = "demo" : "alibaba-inc.com" === g && "zebra" === h ? h = "zebra" : "waptest" !== h && "wapa" !== h && "m" !== h && (h = "m") : h = "waptest";
        var i = "api";
        ("taobao.com" === g || "tmall.com" === g) && (i = "h5api"), t.mainDomain = g, t.subDomain = h, t.prefix = i
    }

    function m() {
        var b = a.navigator.userAgent,
            c = b.match(/WindVane[\/\s]([\d\.\_]+)/);
        c && (t.WindVaneVersion = c[1]);
        var d = b.match(/AliApp\(([^\/]+)\/([\d\.\_]+)\)/i);
        d && (t.AliAppName = d[1], t.AliAppVersion = d[2])
    }

    function n(a) {
        this.id = ++w, this.params = d(a || {}, {
            v: "*",
            data: {},
            type: "get",
            dataType: "jsonp"
        }), this.params.type = this.params.type.toLowerCase(), "object" == typeof this.params.data && (this.params.data = JSON.stringify(this.params.data)), this.middlewares = u.slice(0)
    }
    var o = a.Promise;
    if (!o) {
        var p = "褰撳墠娴忚鍣ㄤ笉鏀寔Promise锛岃鍦╳indows瀵硅薄涓婃寕杞絇romise瀵硅薄鍙弬鑰冿紙http://gitlab.alibaba-inc.com/mtb/lib-es6polyfill/tree/master锛変腑鐨勮В鍐虫柟妗�";
        throw b.mtop = {
            ERROR: p
        }, new Error(p)
    }
    String.prototype.trim || (String.prototype.trim = function() {
        return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "")
    });
    var q, r = o.resolve();
    try {
        q = a.localStorage, q.setItem("@private", "false")
    } catch (s) {
        q = !1
    }
    var t = {
            useJsonpResultType: !1,
            safariGoLogin: !0,
            useAlipayJSBridge: !1
        },
        u = [],
        v = {
            ERROR: -1,
            SUCCESS: 0,
            TOKEN_EXPIRED: 1,
            SESSION_EXPIRED: 2
        };
    l(), m();
    var w = 0,
        x = "2.4.2";
    n.prototype.use = function(a) {
        if (!a) throw new Error("middleware is undefined");
        return this.middlewares.push(a), this
    }, n.prototype.__processRequestMethod = function(a) {
        var b = this.params,
            c = this.options;
        "get" === b.type && "jsonp" === b.dataType ? c.getJSONP = !0 : "get" === b.type && "originaljsonp" === b.dataType ? c.getOriginalJSONP = !0 : "get" === b.type && "json" === b.dataType ? c.getJSON = !0 : "post" === b.type && (c.postJSON = !0), a()
    }, n.prototype.__processRequestType = function(c) {
        var d = this,
            e = this.options;
        if (t.H5Request === !0 && (e.H5Request = !0), t.WindVaneRequest === !0 && (e.WindVaneRequest = !0), e.H5Request === !1 && e.WindVaneRequest === !0) {
            if (!b.windvane || parseFloat(e.WindVaneVersion) < 5.4) throw new Error("WINDVANE_NOT_FOUND::缂哄皯WindVane鐜")
        } else e.H5Request === !0 ? e.WindVaneRequest = !1 : "undefined" == typeof e.WindVaneRequest && "undefined" == typeof e.H5Request && (b.windvane && parseFloat(e.WindVaneVersion) >= 5.4 ? e.WindVaneRequest = !0 : e.H5Request = !0);
        var f = a.navigator.userAgent.toLowerCase();
        return f.indexOf("youku") > -1 && e.mainDomain.indexOf("youku.com") < 0 && (e.WindVaneRequest = !1, e.H5Request = !0), e.mainDomain.indexOf("youku.com") > -1 && f.indexOf("youku") < 0 && (e.WindVaneRequest = !1, e.H5Request = !0), c ? c().then(function() {
            var a = e.retJson.ret;
            return a instanceof Array && (a = a.join(",")), e.WindVaneRequest === !0 && (!a || a.indexOf("PARAM_PARSE_ERROR") > -1 || a.indexOf("HY_FAILED") > -1 || a.indexOf("HY_NO_HANDLER") > -1 || a.indexOf("HY_CLOSED") > -1 || a.indexOf("HY_EXCEPTION") > -1 || a.indexOf("HY_NO_PERMISSION") > -1) ? (t.H5Request = !0, d.__sequence([d.__processRequestType, d.__processToken, d.__processRequestUrl, d.middlewares, d.__processRequest])) : void 0
        }) : void 0
    };
    var y = "_m_h5_c",
        z = "_m_h5_tk",
        A = "_m_h5_tk_enc";
    n.prototype.__getTokenFromAlipay = function() {
        var b = c(),
            d = this.options,
            e = (a.navigator.userAgent, !!location.protocol.match(/^https?\:$/)),
            f = "AP" === d.AliAppName && parseFloat(d.AliAppVersion) >= 8.2;
        return d.useAlipayJSBridge === !0 && !e && f && a.AlipayJSBridge && a.AlipayJSBridge.call ? a.AlipayJSBridge.call("getMtopToken", function(a) {
            a && a.token && (d.token = a.token), b.resolve()
        }, function() {
            b.resolve()
        }) : b.resolve(), b.promise
    }, n.prototype.__getTokenFromCookie = function() {
        var a = this.options;
        return a.CDR && j(y) ? a.token = j(y).split(";")[0] : a.token = a.token || j(z), a.token && (a.token = a.token.split("_")[0]), o.resolve()
    }, n.prototype.__processToken = function(a) {
        var b = this,
            c = this.options;
        this.params;
        return c.token && delete c.token, c.WindVaneRequest !== !0 ? r.then(function() {
            return b.__getTokenFromAlipay()
        }).then(function() {
            return b.__getTokenFromCookie()
        }).then(a).then(function() {
            var a = c.retJson,
                d = a.ret;
            if (d instanceof Array && (d = d.join(",")), d.indexOf("TOKEN_EMPTY") > -1 || c.CDR === !0 && d.indexOf("ILLEGAL_ACCESS") > -1 || d.indexOf("TOKEN_EXOIRED") > -1) {
                if (c.maxRetryTimes = c.maxRetryTimes || 5, c.failTimes = c.failTimes || 0, c.H5Request && ++c.failTimes < c.maxRetryTimes) return b.__sequence([b.__processToken, b.__processRequestUrl, b.middlewares, b.__processRequest]);
                c.maxRetryTimes > 0 && (k(y, c.pageDomain, "*"), k(z, c.mainDomain, c.subDomain), k(A, c.mainDomain, c.subDomain)), a.retType = v.TOKEN_EXPIRED
            }
        }) : void a()
    }, n.prototype.__processRequestUrl = function(b) {
        var c = this.params,
            d = this.options;
        if (d.hostSetting && d.hostSetting[a.location.hostname]) {
            var e = d.hostSetting[a.location.hostname];
            e.prefix && (d.prefix = e.prefix), e.subDomain && (d.subDomain = e.subDomain), e.mainDomain && (d.mainDomain = e.mainDomain)
        }
        if (d.H5Request === !0) {
            var f = "//" + (d.prefix ? d.prefix + "." : "") + (d.subDomain ? d.subDomain + "." : "") + d.mainDomain + "/h5/" + c.api.toLowerCase() + "/" + c.v.toLowerCase() + "/",
                g = c.appKey || ("waptest" === d.subDomain ? "4272" : "12574478"),
                i = (new Date).getTime(),
                j = h(d.token + "&" + i + "&" + g + "&" + c.data),
                k = {
                    jsv: x,
                    appKey: g,
                    t: i,
                    sign: j
                },
                l = {
                    data: c.data,
                    ua: c.ua
                };
            Object.keys(c).forEach(function(a) {
                "undefined" == typeof k[a] && "undefined" == typeof l[a] && (k[a] = c[a])
            }), d.getJSONP ? k.type = "jsonp" : d.getOriginalJSONP ? k.type = "originaljsonp" : (d.getJSON || d.postJSON) && (k.type = "originaljson"), d.useJsonpResultType === !0 && "originaljson" === k.type && delete k.type, d.querystring = k, d.postdata = l, d.path = f
        }
        b()
    }, n.prototype.__processUnitPrefix = function(a) {
        a()
    };
    var B = 0;
    n.prototype.__requestJSONP = function(a) {
        function b(a) {
            if (k && clearTimeout(k), l.parentNode && l.parentNode.removeChild(l), "TIMEOUT" === a) window[j] = function() {
                window[j] = void 0;
                try {
                    delete window[j]
                } catch (a) {}
            };
            else {
                window[j] = void 0;
                try {
                    delete window[j]
                } catch (b) {}
            }
        }
        var d = c(),
            g = this.params,
            h = this.options,
            i = g.timeout || 2e4,
            j = "mtopjsonp" + (g.jsonpIncPrefix || "") + ++B,
            k = setTimeout(function() {
                a("TIMEOUT::鎺ュ彛瓒呮椂"), b("TIMEOUT")
            }, i);
        h.querystring.callback = j;
        var l = document.createElement("script");
        return l.src = h.path + "?" + f(h.querystring) + "&" + f(h.postdata), l.async = !0, l.onerror = function() {
            b("ABORT"), a("ABORT::鎺ュ彛寮傚父閫€鍑�")
        }, window[j] = function() {
            h.results = Array.prototype.slice.call(arguments), b(), d.resolve()
        }, e(l), d.promise
    }, n.prototype.__requestJSON = function(b) {
        function d(a) {
            l && clearTimeout(l), "TIMEOUT" === a && i.abort()
        }
        var e = c(),
            g = this.params,
            h = this.options,
            i = new a.XMLHttpRequest,
            k = g.timeout || 2e4,
            l = setTimeout(function() {
                b("TIMEOUT::鎺ュ彛瓒呮椂"), d("TIMEOUT")
            }, k);
        h.CDR && j(y) && (h.querystring.c = decodeURIComponent(j(y))), i.onreadystatechange = function() {
            if (4 == i.readyState) {
                var a, c, f = i.status;
                if (f >= 200 && 300 > f || 304 == f) {
                    d(), a = i.responseText, c = i.getAllResponseHeaders() || "";
                    try {
                        a = /^\s*$/.test(a) ? {} : JSON.parse(a), a.responseHeaders = c, h.results = [a], e.resolve()
                    } catch (g) {
                        b("PARSE_JSON_ERROR::瑙ｆ瀽JSON澶辫触")
                    }
                } else d("ABORT"), b("ABORT::鎺ュ彛寮傚父閫€鍑�")
            }
        };
        var m, n, o = h.path + "?" + f(h.querystring);
        if (h.getJSON ? (m = "GET", o += "&" + f(h.postdata)) : h.postJSON && (m = "POST", n = f(h.postdata)), i.open(m, o, !0), i.withCredentials = !0, i.setRequestHeader("Accept", "application/json"), i.setRequestHeader("Content-type", "application/x-www-form-urlencoded"), g.headers)
            for (var p in g.headers) i.setRequestHeader(p, g.headers[p]);
        return i.send(n), e.promise
    }, n.prototype.__requestWindVane = function(a) {
        function d(a) {
            g.results = [a], e.resolve()
        }
        var e = c(),
            f = this.params,
            g = this.options,
            h = f.data,
            i = f.api,
            j = f.v,
            k = g.postJSON ? 1 : 0,
            l = g.getJSON || g.postJSON ? "originaljson" : "";
        g.useJsonpResultType === !0 && (l = "");
        var m, n, o = "https" === location.protocol ? 1 : 0,
            p = f.isSec || 0,
            q = f.sessionOption || "AutoLoginOnly",
            r = f.ecode || 0;
        return n = "undefined" != typeof f.timer ? parseInt(f.timer) : "undefined" != typeof f.timeout ? parseInt(f.timeout) : 2e4, m = 2 * n, f.needLogin === !0 && "undefined" == typeof f.sessionOption && (q = "AutoLoginAndManualLogin"), "undefined" != typeof f.secType && "undefined" == typeof f.isSec && (p = f.secType), b.windvane.call("MtopWVPlugin", "send", {
            api: i,
            v: j,
            post: String(k),
            type: l,
            isHttps: String(o),
            ecode: String(r),
            isSec: String(p),
            param: JSON.parse(h),
            timer: n,
            sessionOption: q,
            ext_headers: {
                referer: location.href
            }
        }, d, d, m), e.promise
    }, n.prototype.__processRequest = function(a, b) {
        var c = this;
        return r.then(function() {
            var a = c.options;
            if (a.H5Request && (a.getJSONP || a.getOriginalJSONP)) return c.__requestJSONP(b);
            if (a.H5Request && (a.getJSON || a.postJSON)) return c.__requestJSON(b);
            if (a.WindVaneRequest) return c.__requestWindVane(b);
            throw new Error("UNEXCEPT_REQUEST::閿欒鐨勮姹傜被鍨�")
        }).then(a).then(function() {
            var a = c.options,
                b = (c.params, a.results[0]),
                d = b && b.ret || [];
            b.ret = d, d instanceof Array && (d = d.join(","));
            var e = b.c;
            a.CDR && e && i(y, e, {
                domain: a.pageDomain,
                path: "/"
            }), d.indexOf("SUCCESS") > -1 ? b.retType = v.SUCCESS : b.retType = v.ERROR, a.retJson = b
        })
    }, n.prototype.__sequence = function(a) {
        function b(a) {
            if (a instanceof Array) a.forEach(b);
            else {
                var g, h = c(),
                    i = c();
                e.push(function() {
                    return h = c(), g = a.call(d, function(a) {
                        return h.resolve(a), i.promise
                    }, function(a) {
                        return h.reject(a), i.promise
                    }), g && (g = g["catch"](function(a) {
                        h.reject(a)
                    })), h.promise
                }), f.push(function(a) {
                    return i.resolve(a), g
                })
            }
        }
        var d = this,
            e = [],
            f = [];
        a.forEach(b);
        for (var g, h = r; g = e.shift();) h = h.then(g);
        for (; g = f.pop();) h = h.then(g);
        return h
    };
    var C = function(a) {
            a()
        },
        D = function(a) {
            a()
        };
    n.prototype.request = function(b) {
        var c = this;
        this.options = d(b || {}, t);
        var e = o.resolve([C, D]).then(function(a) {
            var b = a[0],
                d = a[1];
            return c.__sequence([b, c.__processRequestMethod, c.__processRequestType, c.__processToken, c.__processRequestUrl, c.middlewares, c.__processRequest, d])
        }).then(function() {
            var a = c.options.retJson;
            return a.retType !== v.SUCCESS ? o.reject(a) : c.options.successCallback ? void c.options.successCallback(a) : o.resolve(a)
        })["catch"](function(a) {
            var b;
            return a instanceof Error ? (console.error(a.stack), b = {
                ret: [a.message],
                stack: [a.stack],
                retJson: v.ERROR
            }) : b = "string" == typeof a ? {
                ret: [a],
                retJson: v.ERROR
            } : void 0 !== a ? a : c.options.retJson, c.options.failureCallback ? void c.options.failureCallback(b) : o.reject(b)
        });
        return this.__processRequestType(), c.options.H5Request && (c.constructor.__firstProcessor || (c.constructor.__firstProcessor = e), C = function(a) {
            c.constructor.__firstProcessor.then(a)["catch"](a)
        }), ("get" === this.params.type && "json" === this.params.dataType || "post" === this.params.type) && (b.pageDomain = b.pageDomain || g(a.location.hostname), b.mainDomain !== b.pageDomain && (b.maxRetryTimes = 4, b.CDR = !0)), e
    }, b.mtop = function(a) {
        return new n(a)
    }, b.mtop.request = function(a, b, c) {
        var d = {
            H5Request: a.H5Request,
            WindVaneRequest: a.WindVaneRequest,
            LoginRequest: a.LoginRequest,
            AntiCreep: a.AntiCreep,
            AntiFlood: a.AntiFlood,
            successCallback: b,
            failureCallback: c || b
        };
        return new n(a).request(d)
    }, b.mtop.H5Request = function(a, b, c) {
        var d = {
            H5Request: !0,
            successCallback: b,
            failureCallback: c || b
        };
        return new n(a).request(d)
    }, b.mtop.middlewares = u, b.mtop.config = t, b.mtop.RESPONSE_TYPE = v, b.mtop.CLASS = n
}(window, window.lib || (window.lib = {})),
function(a, b) {
    function c(a) {
        return a.preventDefault(), !1
    }

    function d(a) {
        var b = new RegExp("(?:^|;\\s*)" + a + "\\=([^;]+)(?:;\\s*|$)").exec(document.cookie);
        return b ? b[1] : void 0
    }

    function e(b, d) {
        var e = this,
            f = a.dpr || 1,
            g = document.createElement("div"),
            h = document.documentElement.getBoundingClientRect(),
            i = Math.max(h.width, window.innerWidth) / f,
            j = Math.max(h.height, window.innerHeight) / f;
        g.style.cssText = ["-webkit-transform:scale(" + f + ") translateZ(0)", "-ms-transform:scale(" + f + ") translateZ(0)", "transform:scale(" + f + ") translateZ(0)", "-webkit-transform-origin:0 0", "-ms-transform-origin:0 0", "transform-origin:0 0", "width:" + i + "px", "height:" + j + "px", "z-index:999999", "position:" + (i > 800 ? "fixed" : "absolute"), "left:0", "top:0px", "background:" + (i > 800 ? "rgba(0,0,0,.5)" : "#FFF"), "display:none"].join(";");
        var k = document.createElement("div");
        k.style.cssText = ["width:100%", "height:52px", "background:#EEE", "line-height:52px", "text-align:left", "box-sizing:border-box", "padding-left:20px", "position:absolute", "left:0", "top:0", "font-size:16px", "font-weight:bold", "color:#333"].join(";"), k.innerText = b;
        var l = document.createElement("a");
        l.style.cssText = ["display:block", "position:absolute", "right:0", "top:0", "height:52px", "line-height:52px", "padding:0 20px", "color:#999"].join(";"), l.innerText = "鍏抽棴";
        var m = document.createElement("iframe");
        m.style.cssText = ["width:100%", "height:100%", "border:0", "overflow:hidden"].join(";"), i > 800 && (k.style.cssText = ["width:370px", "height:52px", "background:#EEE", "line-height:52px", "text-align:left", "box-sizing:border-box", "padding-left:20px", "position:absolute", "left:" + (i / 2 - 185) + "px", "top:40px", "font-size:16px", "font-weight:bold", "color:#333"].join(";"), m.style.cssText = ["position:absolute", "top:92px", "left:" + (i / 2 - 185) + "px", "width:370px", "height:480px", "border:0", "background:#FFF", "overflow:hidden"].join(";")), k.appendChild(l), g.appendChild(k), g.appendChild(m), g.className = "J_MIDDLEWARE_FRAME_WIDGET", document.body.appendChild(g), m.src = d, l.addEventListener("click", function() {
            e.hide();
            var a = document.createEvent("HTMLEvents");
            a.initEvent("close", !1, !1), g.dispatchEvent(a)
        }, !1), this.addEventListener = function() {
            g.addEventListener.apply(g, arguments)
        }, this.removeEventListener = function() {
            g.removeEventListener.apply(g, arguments)
        }, this.show = function() {
            document.addEventListener("touchmove", c, !1), g.style.display = "block", window.scrollTo(0, 0)
        }, this.hide = function() {
            document.removeEventListener("touchmove", c), window.scrollTo(0, -h.top), g.parentNode && g.parentNode.removeChild(g)
        }
    }

    function f(a) {
        var c = this,
            d = this.options,
            e = this.params;
        return a().then(function() {
            var a = d.retJson,
                f = a.ret,
                g = navigator.userAgent.toLowerCase(),
                h = g.indexOf("safari") > -1 && g.indexOf("chrome") < 0 && g.indexOf("qqbrowser") < 0;
            if (f instanceof Array && (f = f.join(",")), (f.indexOf("SESSION_EXPIRED") > -1 || f.indexOf("SID_INVALID") > -1 || f.indexOf("AUTH_REJECT") > -1 || f.indexOf("NEED_LOGIN") > -1) && (a.retType = l.SESSION_EXPIRED, !d.WindVaneRequest && (k.LoginRequest === !0 || d.LoginRequest === !0 || e.needLogin === !0))) {
                if (!b.login) throw new Error("LOGIN_NOT_FOUND::缂哄皯lib.login");
                if (d.safariGoLogin !== !0 || !h || "taobao.com" === d.pageDomain) return b.login.goLoginAsync().then(function(a) {
                    return c.__sequence([c.__processToken, c.__processRequestUrl, c.__processUnitPrefix, c.middlewares, c.__processRequest])
                })["catch"](function(a) {
                    throw "CANCEL" === a ? new Error("LOGIN_CANCEL::鐢ㄦ埛鍙栨秷鐧诲綍") : new Error("LOGIN_FAILURE::鐢ㄦ埛鐧诲綍澶辫触")
                });
                b.login.goLogin()
            }
        })
    }

    function g(a) {
        var b = this.options;
        this.params;
        return b.H5Request !== !0 || k.AntiFlood !== !0 && b.AntiFlood !== !0 ? void a() : a().then(function() {
            var a = b.retJson,
                c = a.ret;
            c instanceof Array && (c = c.join(",")), c.indexOf("FAIL_SYS_USER_VALIDATE") > -1 && a.data.url && (b.AntiFloodReferer ? location.href = a.data.url.replace(/(http_referer=).+/, "$1" + b.AntiFloodReferer) : location.href = a.data.url)
        })
    }

    function h(b) {
        var c = this,
            f = this.options,
            g = this.params;
        return g.forceAntiCreep !== !0 && f.H5Request !== !0 || k.AntiCreep !== !0 && f.AntiCreep !== !0 ? void b() : b().then(function() {
            var b = f.retJson,
                h = b.ret;
            if (h instanceof Array && (h = h.join(",")), h.indexOf("RGV587_ERROR::SM") > -1 && b.data.url) {
                var j = "_m_h5_smt",
                    k = d(j),
                    l = !1;
                if (f.saveAntiCreepToken === !0 && k) {
                    k = JSON.parse(k);
                    for (var m in k) g[m] && (l = !0)
                }
                if (f.saveAntiCreepToken === !0 && k && !l) {
                    for (var m in k) g[m] = k[m];
                    return c.__sequence([c.__processToken, c.__processRequestUrl, c.__processUnitPrefix, c.middlewares, c.__processRequest])
                }
                return new i(function(d, h) {
                    function i() {
                        m.removeEventListener("close", i), a.removeEventListener("message", k), h("USER_INPUT_CANCEL::鐢ㄦ埛鍙栨秷杈撳叆")
                    }

                    function k(b) {
                        var e;
                        try {
                            e = JSON.parse(b.data) || {}
                        } catch (l) {}
                        if (e && "child" === e.type) {
                            m.removeEventListener("close", i), a.removeEventListener("message", k), m.hide();
                            var n;
                            try {
                                n = JSON.parse(decodeURIComponent(e.content)), "string" == typeof n && (n = JSON.parse(n));
                                for (var o in n) g[o] = n[o];
                                f.saveAntiCreepToken === !0 ? (document.cookie = j + "=" + JSON.stringify(n) + ";", a.location.reload()) : c.__sequence([c.__processToken, c.__processRequestUrl, c.__processUnitPrefix, c.middlewares, c.__processRequest]).then(d)
                            } catch (l) {
                                h("USER_INPUT_FAILURE::鐢ㄦ埛杈撳叆澶辫触")
                            }
                        }
                    }
                    var l = b.data.url,
                        m = new e("", l);
                    m.addEventListener("close", i, !1), a.addEventListener("message", k, !1), m.show()
                })
            }
        })
    }
    if (!b || !b.mtop || b.mtop.ERROR) throw new Error("Mtop 鍒濆鍖栧け璐ワ紒璇峰弬鑰僊top鏂囨。http://gitlab.alibaba-inc.com/mtb/lib-mtop");
    var i = a.Promise,
        j = b.mtop.CLASS,
        k = b.mtop.config,
        l = b.mtop.RESPONSE_TYPE;
    b.mtop.middlewares.push(f), b.mtop.loginRequest = function(a, b, c) {
        var d = {
            LoginRequest: !0,
            H5Request: !0,
            successCallback: b,
            failureCallback: c || b
        };
        return new j(a).request(d)
    }, b.mtop.antiFloodRequest = function(a, b, c) {
        var d = {
            AntiFlood: !0,
            successCallback: b,
            failureCallback: c || b
        };
        return new j(a).request(d)
    }, b.mtop.middlewares.push(g), b.mtop.antiCreepRequest = function(a, b, c) {
        var d = {
            AntiCreep: !0,
            successCallback: b,
            failureCallback: c || b
        };
        return new j(a).request(d)
    }, b.mtop.middlewares.push(h)
}(window, window.lib || (window.lib = {}));
! function(a, b, c) {
    function d(a) {
        var b = new RegExp("(?:^|;\\s*)" + a + "\\=([^;]+)(?:;\\s*|$)").exec(v.cookie);
        return b ? b[1] : c
    }

    function e(a) {
        return a.preventDefault(), !1
    }

    function f(b, c) {
        var d = this,
            f = a.dpr || 1,
            g = document.createElement("div"),
            h = document.documentElement.getBoundingClientRect(),
            i = Math.max(h.width, window.innerWidth) / f,
            j = Math.max(h.height, window.innerHeight) / f;
        g.style.cssText = ["-webkit-transform:scale(" + f + ") translateZ(0)", "-ms-transform:scale(" + f + ") translateZ(0)", "transform:scale(" + f + ") translateZ(0)", "-webkit-transform-origin:0 0", "-ms-transform-origin:0 0", "transform-origin:0 0", "width:" + i + "px", "height:" + j + "px", "z-index:999999", "position:absolute", "left:0", "top:0px", "background:#FFF", "display:none"].join(";");
        var k = document.createElement("div");
        k.style.cssText = ["width:100%", "height:52px", "background:#EEE", "line-height:52px", "text-align:left", "box-sizing:border-box", "padding-left:20px", "position:absolute", "left:0", "top:0", "font-size:16px", "font-weight:bold", "color:#333"].join(";"), k.innerText = b;
        var l = document.createElement("a");
        l.style.cssText = ["display:block", "position:absolute", "right:0", "top:0", "height:52px", "line-height:52px", "padding:0 20px", "color:#999"].join(";"), l.innerText = "鍏抽棴";
        var m = document.createElement("iframe");
        m.style.cssText = ["width:100%", "height:100%", "border:0", "overflow:hidden"].join(";"), k.appendChild(l), g.appendChild(k), g.appendChild(m), v.body.appendChild(g), m.src = c, l.addEventListener("click", function() {
            d.hide();
            var a = v.createEvent("HTMLEvents");
            a.initEvent("close", !1, !1), g.dispatchEvent(a)
        }, !1), this.addEventListener = function() {
            g.addEventListener.apply(g, arguments)
        }, this.removeEventListener = function() {
            g.removeEventListener.apply(g, arguments)
        }, this.show = function() {
            document.addEventListener("touchmove", e, !1), g.style.display = "block", window.scrollTo(0, 0)
        }, this.hide = function() {
            document.removeEventListener("touchmove", e), window.scrollTo(0, -h.top), v.body.removeChild(g)
        }
    }

    function g(a) {
        if (!a || "function" != typeof a || !b.mtop) {
            var d = this.getUserNick();
            return !!d
        }
        b.mtop.request({
            api: "mtop.user.getUserSimple",
            v: "1.0",
            data: {
                isSec: 0
            },
            H5Request: !0
        }, function(d) {
            d.retType === b.mtop.RESPONSE_TYPE.SUCCESS ? a(!0, d) : d.retType === b.mtop.RESPONSE_TYPE.SESSION_EXPIRED ? a(!1, d) : a(c, d)
        })
    }

    function h(a) {
        var b;
        return u && (b = {}, b.promise = new u(function(a, c) {
            b.resolve = a, b.reject = c
        })), this.isLogin(function(c, d) {
            a && a(c, d), c === !0 ? b && b.resolve(d) : b && b.reject(d)
        }), b ? b.promise : void 0
    }

    function i(a) {
        if (!a || "function" != typeof a) {
            var b = "",
                e = d("_w_tb_nick"),
                f = d("_nk_") || d("snk"),
                g = d("sn");
            return e && e.length > 0 && "null" != e ? b = decodeURIComponent(e) : f && f.length > 0 && "null" != f ? b = unescape(unescape(f).replace(/\\u/g, "%u")) : g && g.length > 0 && "null" != g && (b = decodeURIComponent(g)), b = b.replace(/\</g, "&lt;").replace(/\>/g, "&gt;")
        }
        this.isLogin(function(b, d) {
            a(b === !0 && d && d.data && d.data.nick ? d.data.nick : b === !1 ? "" : c)
        })
    }

    function j(a) {
        var b;
        return u && (b = {}, b.promise = new u(function(a, c) {
            b.resolve = a, b.reject = c
        })), this.getUserNick(function(c) {
            a && a(c), c ? b && b.resolve(c) : b && b.reject()
        }), b ? b.promise : void 0
    }

    function k(a, b) {
        var c = "//" + G + "." + H.subDomain + "." + E + "/" + H[(a || "login") + "Name"];
        if (b) {
            var d = [];
            for (var e in b) d.push(e + "=" + encodeURIComponent(b[e]));
            c += "?" + d.join("&")
        }
        return c
    }

    function l(a, b) {
        b ? location.replace(a) : location.href = a
    }

    function m(b, c, d) {
        function e(b) {
            j.removeEventListener("close", e), a.removeEventListener("message", g), d("CANCEL")
        }

        function g(b) {
            var c = b.data || {};
            c && "child" === c.type && c.content.indexOf("SUCCESS") > -1 ? (j.removeEventListener("close", e), a.removeEventListener("message", g), j.hide(), d("SUCCESS")) : d("FAILURE")
        }
        var h = location.protocol + "//h5." + H.subDomain + ".taobao.com/" + ("waptest" === H.subDomain ? "src" : "other") + "/" + b + "end.html?origin=" + encodeURIComponent(location.protocol + "//" + location.hostname),
            i = k(b, {
                ttid: "h5@iframe",
                tpl_redirect_url: h
            }),
            j = new f(c.title || "鎮ㄩ渶瑕佺櫥褰曟墠鑳界户缁闂�", i);
        j.addEventListener("close", e, !1), a.addEventListener("message", g, !1), j.show()
    }

    function n(b, c, d) {
        var e = k(b, {
            wvLoginCallback: "wvLoginCallback"
        });
        a.wvLoginCallback = function(b) {
            delete a.wvLoginCallback, d(b.indexOf(":SUCCESS") > -1 ? "SUCCESS" : b.indexOf(":CANCEL") > -1 ? "CANCEL" : "FAILURE")
        }, l(e)
    }

    function o(a, b, c) {
        if ("function" == typeof b ? (c = b, b = null) : "string" == typeof b && (b = {
                redirectUrl: b
            }), b = b || {}, c && A) n(a, b, c);
        else if (c && !z && "login" === a) m(a, b, c);
        else {
            var d = k(a, {
                tpl_redirect_url: b.redirectUrl || location.href
            });
            l(d, b.replace)
        }
    }

    function p(a, b, c) {
        var d;
        return u && (d = {}, d.promise = new u(function(a, b) {
            d.resolve = a, d.reject = b
        })), o(a, b, function(a) {
            c && c(a), "SUCCESS" === a ? d && d.resolve(a) : d && d.reject(a)
        }), d ? d.promise : void 0
    }

    function q(a) {
        o("login", a)
    }

    function r(a) {
        return p("login", a)
    }

    function s(a) {
        o("logout", a)
    }

    function t(a) {
        return p("logout", a)
    }
    var u = a.Promise,
        v = a.document,
        w = a.navigator.userAgent,
        x = location.hostname,
        y = (a.location.search, w.match(/WindVane[\/\s]([\d\.\_]+)/)),
        z = w.match(/AliApp\(([^\/]+)\/([\d\.\_]+)\)/i),
        A = !!(z && "TB" === z[1] && y && parseFloat(y[1]) > 5.2),
        B = ["taobao.net", "taobao.com"],
        C = new RegExp("([^.]*?)\\.?((?:" + B.join(")|(?:").replace(/\./g, "\\.") + "))", "i"),
        D = x.match(C) || [],
        E = function() {
            var a = D[2] || "taobao.com";
            return a.match(/\.?taobao\.net$/) ? "taobao.net" : "taobao.com"
        }(),
        F = function() {
            var a = E,
                b = D[1] || "m";
            return "taobao.net" === a && (b = "waptest"), b
        }(),
        G = "login";
    b.login = b.login || {};
    var H = {
        loginName: "login.htm",
        logoutName: "logout.htm",
        subDomain: F
    };
    b.login.config = H, b.login.isLogin = g, b.login.isLoginAsync = h, b.login.getUserNick = i, b.login.getUserNickAsync = j, b.login.generateUrl = k, b.login.goLogin = q, b.login.goLoginAsync = r, b.login.goLogout = s, b.login.goLogoutAsync = t
}(window, window.lib || (window.lib = {}));
! function(e) {
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
}([function(e, t, n) {
    "use strict";
    var r = n(1),
        i = n(4);
    r(), e.exports = i
}, function(e, t, n) {
    var r = n(2),
        i = n(4),
        o = n(15);
    e.exports = function() {
        try {
            if (!window) return;
            if (window.JSTracker2 && window.JSTracker2.version) return;
            var e = [];
            window.JSTracker2 && window.JSTracker2.length > 0 && (e = window.JSTracker2);
            var t;
            window.g_config && window.g_config.jstracker2 && (t = window.g_config.jstracker2), window.JSTracker2 = new i(t);
            for (var n = 0; n < e.length; n++) window.JSTracker2.push(e[n]);
            o.call(JSTracker2);
            var a = window.onerror;
            window.onerror = function() {
                try {
                    a && a.apply(window, arguments);
                    var e = r.apply(window, arguments);
                    window.JSTracker2.push(e)
                } catch (t) {}
            }
        } catch (s) {}
    }
}, function(e, t, n) {
    var r = n(3);
    e.exports = function(e, t, n, i, o) {
        var o = r(o).toString(),
            a = {
                msg: e,
                file: t,
                line: n,
                col: i,
                stack: o.substr(0, 1024)
            };
        return a
    }
}, function(e, t) {
    function n(e, t, n, r) {
        this.funcName = e, this.file = t, this.line = n, this.col = r
    }
    n.prototype.toString = function() {
        return [this.funcName, this.file, this.line, this.col].join("|")
    };
    var r = /\S+\:\d+/,
        i = /\s+at /,
        o = {
            parse: function(e) {
                return e ? "undefined" != typeof e.stacktrace || "undefined" != typeof e["opera#sourceloc"] ? this.parseOpera(e) : e.stack && e.stack.match(i) ? this.parseV8OrIE(e) : e.stack && e.stack.match(r) ? this.parseFFOrSafari(e) : "" : ""
            },
            extractLocation: function(e) {
                if (e.indexOf(":") === -1) return [e];
                var t = e.replace(/[\(\)\s]/g, "").split(":"),
                    n = t.pop(),
                    r = t[t.length - 1];
                if (!isNaN(parseFloat(r)) && isFinite(r)) {
                    var i = t.pop();
                    return [t.join(":"), i, n]
                }
                return [t.join(":"), n, void 0]
            },
            parseV8OrIE: function(e) {
                return e.stack.split("\n").slice(1).map(function(e) {
                    var t = e.replace(/^\s+/, "").split(/\s+/).slice(1),
                        r = this.extractLocation(t.pop()),
                        i = t[0] && "Anonymous" !== t[0] ? t[0] : void 0;
                    return new n(i, (void 0), r[0], r[1], r[2])
                }, this)
            },
            parseFFOrSafari: function(e) {
                return e.stack.split("\n").filter(function(e) {
                    return !!e.match(r)
                }, this).map(function(e) {
                    var t = e.split("@"),
                        r = this.extractLocation(t.pop()),
                        i = t.shift() || void 0;
                    return new n(i, (void 0), r[0], r[1], r[2])
                }, this)
            },
            parseOpera: function(e) {
                return !e.stacktrace || e.message.indexOf("\n") > -1 && e.message.split("\n").length > e.stacktrace.split("\n").length ? this.parseOpera9(e) : e.stack ? this.parseOpera11(e) : this.parseOpera10(e)
            },
            parseOpera9: function(e) {
                for (var t = /Line (\d+).*script (?:in )?(\S+)/i, r = e.message.split("\n"), i = [], o = 2, a = r.length; o < a; o += 2) {
                    var s = t.exec(r[o]);
                    s && i.push(new n((void 0), (void 0), s[2], s[1]))
                }
                return i
            },
            parseOpera10: function(e) {
                for (var t = /Line (\d+).*script (?:in )?(\S+)(?:: In function (\S+))?$/i, r = e.stacktrace.split("\n"), i = [], o = 0, a = r.length; o < a; o += 2) {
                    var s = t.exec(r[o]);
                    s && i.push(new n(s[3] || void 0, (void 0), s[2], s[1]))
                }
                return i
            },
            parseOpera11: function(e) {
                return e.stack.split("\n").filter(function(e) {
                    return !!e.match(r) && !e.match(/^Error created at/)
                }, this).map(function(e) {
                    var t, r = e.split("@"),
                        i = this.extractLocation(r.pop()),
                        o = r.shift() || "",
                        a = o.replace(/<anonymous function(: (\w+))?>/, "$2").replace(/\([^\)]*\)/g, "") || void 0;
                    o.match(/\(([^\)]*)\)/) && (t = o.replace(/^[^\(]+\(([^\)]*)\)$/, "$1"));
                    var s = void 0 === t || "[arguments not available]" === t ? void 0 : t.split(",");
                    return new n(a, s, i[0], i[1], i[2])
                }, this)
            }
        };
    e.exports = function(e) {
        var t = o.parse(e);
        return t
    }
}, function(e, t, n) {
    function r(e) {
        var t = {
            msg: "",
            file: "",
            line: "",
            col: "",
            stack: "",
            url: "",
            ua: "",
            screen: "",
            nick: "",
            dns: "",
            con: "",
            req: "",
            res: "",
            dcl: "",
            onload: "",
            type: "",
            ki: ""
        };
        this.version = "o4.2.0", t = {
            v: this.version,
            ua: o,
            screen: a,
            sampling: 100,
            nick: s,
            ki: c
        }, this._debug = location.href.indexOf("jt_debug") != -1, this._pushed_num = 0, this._config = u.merge(t, e)
    }
    var i = n(5),
        o = n(11),
        a = n(12),
        s = n(13),
        c = n(14),
        u = n(10);
    r.prototype.push = i, e.exports = r
}, function(e, t, n) {
    var r = n(6),
        i = n(7),
        o = n(9),
        a = n(8),
        s = n(10);
    e.exports = function(e) {
        try {
            if (!e) return;
            e && e.constructor === Object || (e = r(e)), e = s.merge(this._config, e);
            var t = a;
            e.t = t();
            for (var n in e) "" !== e[n] && null !== e[n] && void 0 !== e[n] || delete e[n];
            var c = s.stringify(e),
                u = e.sampling;
            if (u < 1 && (u = 9999999, "undefined" != typeof console && console.warn && console.warn("JSTracker2 sampling is invalid, please set a integer above 1!")), "__PV" !== e.msg && !this._debug && Math.random() * u > 1);
            else if (this._pushed_num < 10) {
                this._pushed_num++, this._debug && window.console && window.console.log(e);
                var p = o.call(this);
                i(p + c)
            }
        } catch (d) {}
    }
}, function(e, t, n) {
    var r = n(3);
    e.exports = function(e) {
        var t = {
            msg: e.message,
            file: "",
            line: "",
            col: "",
            stack: r(e).toString()
        };
        return t
    }
}, function(e, t, n) {
    var r = n(8);
    e.exports = function(e) {
        var t = window,
            n = "jsFeImage_" + r(),
            i = t[n] = new Image;
        i.onload = i.onerror = function() {
            t[n] = null
        }, i.src = e
    }
}, function(e, t) {
    var n = function() {
        return +new Date + ".r" + Math.floor(1e3 * Math.random())
    };
    e.exports = n
}, function(e, t) {
    e.exports = function() {
        var e = "//gm.mmstat.com";
        return this._config.server && (e = this._config.server), e + "/jstracker.3?"
    }
}, function(e, t) {
    e.exports = {
        merge: function(e, t) {
            var n = {};
            for (var r in e) n[r] = e[r];
            for (var r in t) n[r] = t[r];
            return n
        },
        stringify: function(e) {
            var t = [];
            for (var n in e) t.push(n + "=" + encodeURIComponent(e[n]));
            return t.join("&")
        },
        now: function() {
            return window.performance && window.performance.now ? window.performance.now() : Date && "function" == typeof Date.now ? Date.now() : new Date
        }
    }
}, function(e, t) {
    var n = function() {
        try {
            if (/UBrowser/i.test(navigator.userAgent)) return "";
            if ("undefined" != typeof window.scrollMaxX) return "";
            var e = "track" in document.createElement("track"),
                t = window.chrome && window.chrome.webstore ? Object.keys(window.chrome.webstore).length : 0;
            return window.clientInformation && window.clientInformation.languages && window.clientInformation.languages.length > 2 ? "" : e ? t > 1 ? " QIHU 360 EE" : " QIHU 360 SE" : ""
        } catch (n) {
            return ""
        }
    }();
    e.exports = navigator.userAgent + n
}, function(e, t) {
    e.exports = screen.width + "x" + screen.height
}, function(e, t) {
    var n = null;
    try {
        var r = /_nk_=([^;]+)/.exec(document.cookie) || /_w_tb_nick=([^;]+)/.exec(document.cookie) || /lgc=([^;]+)/.exec(document.cookie);
        r && (n = decodeURIComponent(r[1]))
    } catch (i) {}
    e.exports = n
}, function(e, t) {
    function n() {
        try {
            return KISSY.version
        } catch (e) {
            return null
        }
    }
    e.exports = n()
}, function(e, t, n) {
    var r = n(16),
        i = n(18);
    e.exports = function() {
        var e = this,
            t = 100;
        if (this._config.p_sampling && (t = this._config.p_sampling), this._debug || !(Math.random() * t > 1)) {
            if (this._cpu = new i, window.performance && window.performance.memory) try {
                var n = parseInt(window.performance.memory.usedJSHeapSize),
                    o = parseInt(window.performance.memory.totalJSHeapSize);
                n && (this._jsHeapSizeData = {
                    jsHeapUsed: n
                }, o && (this._jsHeapSizeData.jsHeapUsedRate = (n / o).toFixed(4)))
            } catch (a) {}
            setTimeout(function() {
                try {
                    var t = r.call(e);
                    window.JSTracker2.push(t)
                } catch (n) {}
            }, 2e4)
        }
    }
}, function(e, t, n) {
    var r = n(17),
        i = n(10);
    e.exports = function() {
        var e = {},
            t = window;
        if (t.performance) {
            var n = t.performance.timing;
            e.dns = n.domainLookupEnd - n.domainLookupStart, e.con = n.connectEnd - n.connectStart, e.req = n.responseStart - n.requestStart, e.res = n.responseEnd - n.responseStart, e.dcl = n.domContentLoadedEventEnd - n.domLoading, e.onload = n.loadEventStart - n.domLoading, e.type = window.performance.navigation.type, e.sampling = 100
        }
        e.msg = "__PV";
        var o = r.call(this);
        return e.stack = i.stringify(o), e
    }
}, function(e, t, n) {
    var r = n(10);
    e.exports = function() {
        var e = window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance,
            t = {};
        if (e) {
            var n = e.timing;
            if (n) {
                if (void 0 === t.firstPaint) {
                    var i = -1;
                    window.chrome && window.chrome.loadTimes ? (i = 1e3 * window.chrome.loadTimes().firstPaintTime, i -= 1e3 * window.chrome.loadTimes().startLoadTime) : "number" == typeof window.performance.timing.msFirstPaint && (i = window.performance.timing.msFirstPaint, t.firstPaint = i - window.performance.timing.navigationStart), t.firstPaint = Math.floor(i)
                }
                t.load = n.loadEventEnd - n.fetchStart, t.domReady = n.domComplete - n.domInteractive, t.readyStart = n.fetchStart - n.navigationStart, t.redirect = n.redirectEnd - n.redirectStart, t.appcache = n.domainLookupStart - n.fetchStart, t.unloadEvent = n.unloadEventEnd - n.unloadEventStart, t.lookupDomain = n.domainLookupEnd - n.domainLookupStart, t.connect = n.connectEnd - n.connectStart, t.request = n.responseEnd - n.requestStart, t.initDomTree = n.domInteractive - n.responseEnd, t.loadEvent = n.loadEventEnd - n.loadEventStart
            }
        }
        if (this._jsHeapSizeData && (t = r.merge(t, this._jsHeapSizeData)), this._cpu) {
            this._cpu.pause(), t.busy = Math.floor(this._cpu.getTotalSize(0, 15e3));
            for (var o = this._cpu.data.dataArray, a = -1, s = 0, c = 0; c < o.length && (o[c] <= .1 ? a++ : (s = c + 1, a = 0), !(a >= 5)); c++);
            t.avail = Math.floor(this._cpu.data.timeArray[s] - this._cpu.data.timeArray[0]), t.busyPer = Math.floor(this._cpu.getOverPerAmount(1, 0, 15e3) / this._cpu.getOverPerAmount(0, 0, 15e3) * 100), this._debug && window.console && window.console.log(t)
        }
        return t
    }
}, function(e, t) {
    ! function(e) {
        function t() {
            this.conf = {
                log: !1,
                consoleUI: !1,
                delay: 100,
                stat: !0,
                ui: !1
            }, this.log("start"), this.run(), this._lastTime = this.now(), this.data = {
                timeArray: [],
                per_line: [],
                time_line: [],
                size_line: [],
                averageTime: this.conf.delay,
                totalSize: 0,
                dataArray: [],
                timeArray: []
            }, this.log("end")
        }
        t.prototype.run = function() {
            var e, t = this;
            t.conf.ui, window.addEventListener && window.addEventListener("touchmove", function() {
                t.resumeFlag = !0
            }, !1), this._timerID = setTimeout(function() {
                if (!t.isPause) {
                    t.currentTime = t.now(), e = (t.currentTime - t._lastTime - t.conf.delay - 0) / t.conf.delay, e < 0 && (e = 0), e > 1 && (e = 1), t._lastTime = t.currentTime;
                    var n = t.getStepPer(t.now(), e),
                        r = Math.floor(n / .5) + 1;
                    if (r = r > 200 ? 200 : r, t.resumeFlag) t.resumeFlag = !1;
                    else
                        for (var i = 0; i < r; i++) t.logPercent(e);
                    t._timerID = setTimeout(arguments.callee, t.conf.delay)
                }
            }, t.conf.delay)
        }, t.prototype.now = function() {
            return window.performance && window.performance.now ? window.performance.now() : Date && "function" == typeof Date.now ? Date.now() : new Date
        }, t.prototype.log = function(t) {
            this.conf.log && e.console && e.console.log && e.console.log("### CPU Log:" + t)
        }, t.prototype.getStepPer = function(e, t) {
            var n = this.data;
            n.time_line.push(e);
            var r;
            n.per_line.push(t);
            var i = n.time_line.length;
            r = 1 == n.time_line.length ? n.averageTime : e - n.time_line[i - 2], r < n.averageTime && (r = n.averageTime);
            var o = (r - n.averageTime) / n.averageTime;
            return i >= 2 ? (n.totalSize += (n.per_line[i - 1] + n.per_line[i - 2]) * (n.time_line[i - 1] - n.time_line[i - 2]) / 2, n.size_line.push(n.totalSize)) : n.size_line.push(0), n.per_line.length > 2 && (n.per_line.shift(), n.time_line.shift()), o
        }, t.prototype.drawUIByConsole = function(e) {
            for (var t = Math.round(10 * e), n = "鈻�", r = t; r--;) n += "鈻�";
            n += Math.round(100 * e), this.log(n)
        }, t.prototype.pause = function() {
            clearTimeout(this._timerID), this.isPause = !0, this.log("###########################PAUSE!!!!!!!!!")
        }, t.prototype.resume = function() {
            (null == this.isPause || this.isPause) && (this._lastTime = this.now() + 1e4, this.isPause = !1, this.resumeFlag = !0, this.log("###########################RESUME!!!!!!!!!"), this.run())
        }, t.prototype.logPercent = function(e) {
            this.conf.stat && this.logStat(e), this.conf.ui, this.conf.consoleUI && this.drawUIByConsole(e)
        }, t.prototype.logStat = function(e) {
            var t = this.data;
            t.dataArray.push(e), t.timeArray.push(this.now())
        }, t.prototype.getCurrentCPU = function() {
            for (var e = this.data, t = e.dataArray, n = 0, r = t.length, i = 0, o = r - 1; o >= 0 && (i += t[o], n++, !(n >= 3)); o--);
            return 0 == n ? 0 : i / n
        }, t.prototype.getTimeIndex = function(e, t) {
            for (var n = this.data.timeArray, r = 0; r < n.length; r++)
                if (t) {
                    if (n[r] - n[0] > e) return r - 1
                } else if (n[r] - n[0] >= e) return r;
            return n.length
        }, t.prototype.getOverPerAmount = function(e, t, n) {
            for (var r = this.data, i = this.getTimeIndex(t), o = this.getTimeIndex(n, 1), a = r.dataArray, s = 0, c = i; c < o; c++) "undefined" != typeof a[c] && a[c] >= e && s++;
            return s
        }, t.prototype.getTotalSize = function(e, t) {
            var n = this.data,
                r = this.getTimeIndex(e),
                i = this.getTimeIndex(t, !0),
                o = n.size_line[i];
            o || (o = n.size_line[n.size_line.length - 1]);
            var a = o - n.size_line[r];
            return a
        }, e.cpu = t
    }(window), e.exports = cpu
}]);
! function(a, b) {
    function c(a, b) {
        a = a.toString().split("."), b = b.toString().split(".");
        for (var c = 0; c < a.length || c < b.length; c++) {
            var d = parseInt(a[c], 10),
                e = parseInt(b[c], 10);
            if (window.isNaN(d) && (d = 0), window.isNaN(e) && (e = 0), d < e) return -1;
            if (d > e) return 1
        }
        return 0
    }
    var d = a.Promise,
        e = a.document,
        f = a.navigator.userAgent,
        g = /Windows\sPhone\s(?:OS\s)?[\d\.]+/i.test(f) || /Windows\sNT\s[\d\.]+/i.test(f),
        h = g && a.WindVane_Win_Private && a.WindVane_Win_Private.call,
        i = /iPhone|iPad|iPod/i.test(f),
        j = /Android/i.test(f),
        k = f.match(/WindVane[\/\s](\d+[._]\d+[._]\d+)/),
        l = Object.prototype.hasOwnProperty,
        m = b.windvane = a.WindVane || (a.WindVane = {}),
        n = (a.WindVane_Native, Math.floor(65536 * Math.random())),
        o = 1,
        p = [],
        q = 3,
        r = "hybrid",
        s = "wv_hybrid",
        t = "iframe_",
        u = "param_",
        v = "chunk_",
        w = 6e5,
        x = 6e5,
        y = 6e4;
    k = k ? (k[1] || "0.0.0").replace(/\_/g, ".") : "0.0.0";
    var z = {
            isAvailable: 1 === c(k, "0"),
            call: function(a, b, c, e, f, g) {
                var h, i;
                "number" == typeof arguments[arguments.length - 1] && (g = arguments[arguments.length - 1]), "function" != typeof e && (e = null), "function" != typeof f && (f = null), d && (i = {}, i.promise = new d(function(a, b) {
                    i.resolve = a, i.reject = b
                })), h = A.getSid();
                var j = {
                    success: e,
                    failure: f,
                    deferred: i
                };
                if (g > 0 && (j.timeout = setTimeout(function() {
                        z.onFailure(h, {
                            ret: "HY_TIMEOUT"
                        })
                    }, g)), A.registerCall(h, j), A.registerGC(h, g), z.isAvailable ? A.callMethod(a, b, c, h) : z.onFailure(h, {
                        ret: "HY_NOT_IN_WINDVANE"
                    }), i) return i.promise
            },
            fireEvent: function(a, b, c) {
                var d = e.createEvent("HTMLEvents");
                d.initEvent(a, !1, !0), d.param = A.parseData(b || A.getData(c)), e.dispatchEvent(d)
            },
            getParam: function(a) {
                return A.getParam(a)
            },
            setData: function(a, b) {
                A.setData(a, b)
            },
            onSuccess: function(a, b) {
                A.onComplete(a, b, "success")
            },
            onFailure: function(a, b) {
                A.onComplete(a, b, "failure")
            }
        },
        A = {
            params: {},
            chunks: {},
            calls: {},
            getSid: function() {
                return (n + o++) % 65536 + ""
            },
            buildParam: function(a) {
                return a && "object" == typeof a ? JSON.stringify(a) : a || ""
            },
            getParam: function(a) {
                return this.params[u + a] || ""
            },
            setParam: function(a, b) {
                this.params[u + a] = b
            },
            parseData: function(a) {
                var b;
                if (a && "string" == typeof a) try {
                    b = JSON.parse(a)
                } catch (a) {
                    b = {
                        ret: ["WV_ERR::PARAM_PARSE_ERROR"]
                    }
                } else b = a || {};
                return b
            },
            setData: function() {
                this.chunks[v + sid] = this.chunks[v + sid] || [], this.chunks[v + sid].push(chunk)
            },
            getData: function(a) {
                return this.chunks[v + a] ? this.chunks[v + a].join("") : ""
            },
            registerCall: function(a, b) {
                this.calls[a] = b
            },
            unregisterCall: function(a) {
                var b = {};
                return this.calls[a] && (b = this.calls[a], delete this.calls[a]), b
            },
            useIframe: function(a, b) {
                var c = t + a,
                    d = p.pop();
                d || (d = e.createElement("iframe"), d.setAttribute("frameborder", "0"), d.style.cssText = "width:0;height:0;border:0;display:none;"), d.setAttribute("id", c), d.setAttribute("src", b), d.parentNode || setTimeout(function() {
                    e.body.appendChild(d)
                }, 5)
            },
            retrieveIframe: function(a) {
                var b = t + a,
                    c = e.querySelector("#" + b);
                p.length >= q ? e.body.removeChild(c) : p.indexOf(c) < 0 && p.push(c)
            },
            callMethod: function(b, c, d, e) {
                if (d = A.buildParam(d), g) h ? a.WindVane_Win_Private.call(b, c, e, d) : this.onComplete(e, {
                    ret: "HY_NO_HANDLER_ON_WP"
                }, "failure");
                else {
                    var f = r + "://" + b + ":" + e + "/" + c + "?" + d;
                    if (i) this.setParam(e, d), this.useIframe(e, f);
                    else if (j) {
                        var k = s + ":";
                        window.prompt(f, k)
                    } else this.onComplete(e, {
                        ret: "HY_NOT_SUPPORT_DEVICE"
                    }, "failure")
                }
            },
            registerGC: function(a, b) {
                var c = this,
                    d = Math.max(b || 0, w),
                    e = Math.max(b || 0, y),
                    f = Math.max(b || 0, x);
                setTimeout(function() {
                    c.unregisterCall(a)
                }, d), i ? setTimeout(function() {
                    c.params[u + a] && delete c.params[u + a]
                }, e) : j && setTimeout(function() {
                    c.chunks[v + a] && delete c.chunks[v + a]
                }, f)
            },
            onComplete: function(a, b, c) {
                var d = this.unregisterCall(a),
                    e = d.success,
                    f = d.failure,
                    g = d.deferred,
                    h = d.timeout;
                h && clearTimeout(h), b = b ? b : this.getData(a), b = this.parseData(b);
                var k = b.ret;
                "string" == typeof k && (b = b.value || b, b.ret || (b.ret = [k])), "success" === c ? (e && e(b), g && g.resolve(b)) : "failure" === c && (f && f(b), g && g.reject(b)), i ? (this.retrieveIframe(a), this.params[u + a] && delete this.params[u + a]) : j && this.chunks[v + a] && delete this.chunks[v + a]
            }
        };
    for (var B in z) l.call(m, B) || (m[B] = z[B])
}(window, window.lib || (window.lib = {}));
! function a(b, c, d) {
    function e(g, h) {
        if (!c[g]) {
            if (!b[g]) {
                var i = "function" == typeof require && require;
                if (!h && i) return i(g, !0);
                if (f) return f(g, !0);
                var j = new Error("Cannot find module '" + g + "'");
                throw j.code = "MODULE_NOT_FOUND", j
            }
            var k = c[g] = {
                exports: {}
            };
            b[g][0].call(k.exports, function(a) {
                var c = b[g][1][a];
                return e(c ? c : a)
            }, k, k.exports, a, b, c, d)
        }
        return c[g].exports
    }
    for (var f = "function" == typeof require && require, g = 0; g < d.length; g++) e(d[g]);
    return e
}({
    1: [function(a, b) {
        function c() {}
        var d = b.exports = {};
        d.nextTick = function() {
            var a = "undefined" != typeof window && window.setImmediate,
                b = "undefined" != typeof window && window.postMessage && window.addEventListener;
            if (a) return function(a) {
                return window.setImmediate(a)
            };
            if (b) {
                var c = [];
                return window.addEventListener("message", function(a) {
                        var b = a.source;
                        if ((b === window || null === b) && "process-tick" === a.data && (a.stopPropagation(), c.length > 0)) {
                            var d = c.shift();
                            d()
                        }
                    }, !0),
                    function(a) {
                        c.push(a), window.postMessage("process-tick", "*")
                    }
            }
            return function(a) {
                setTimeout(a, 0)
            }
        }(), d.title = "browser", d.browser = !0, d.env = {}, d.argv = [], d.on = c, d.addListener = c, d.once = c, d.off = c, d.removeListener = c, d.removeAllListeners = c, d.emit = c, d.binding = function() {
            throw new Error("process.binding is not supported")
        }, d.cwd = function() {
            return "/"
        }, d.chdir = function() {
            throw new Error("process.chdir is not supported")
        }
    }, {}],
    2: [function(a, b) {
        "use strict";

        function c(a) {
            function b(a) {
                return null === i ? void k.push(a) : void f(function() {
                    var b = i ? a.onFulfilled : a.onRejected;
                    if (null === b) return void(i ? a.resolve : a.reject)(j);
                    var c;
                    try {
                        c = b(j)
                    } catch (d) {
                        return void a.reject(d)
                    }
                    a.resolve(c)
                })
            }

            function c(a) {
                try {
                    if (a === l) throw new TypeError("A promise cannot be resolved with itself.");
                    if (a && ("object" == typeof a || "function" == typeof a)) {
                        var b = a.then;
                        if ("function" == typeof b) return void e(b.bind(a), c, g)
                    }
                    i = !0, j = a, h()
                } catch (d) {
                    g(d)
                }
            }

            function g(a) {
                i = !1, j = a, h()
            }

            function h() {
                for (var a = 0, c = k.length; c > a; a++) b(k[a]);
                k = null
            }
            if ("object" != typeof this) throw new TypeError("Promises must be constructed via new");
            if ("function" != typeof a) throw new TypeError("not a function");
            var i = null,
                j = null,
                k = [],
                l = this;
            this.then = function(a, c) {
                return new l.constructor(function(e, f) {
                    b(new d(a, c, e, f))
                })
            }, e(a, c, g)
        }

        function d(a, b, c, d) {
            this.onFulfilled = "function" == typeof a ? a : null, this.onRejected = "function" == typeof b ? b : null, this.resolve = c, this.reject = d
        }

        function e(a, b, c) {
            var d = !1;
            try {
                a(function(a) {
                    d || (d = !0, b(a))
                }, function(a) {
                    d || (d = !0, c(a))
                })
            } catch (e) {
                if (d) return;
                d = !0, c(e)
            }
        }
        var f = a("asap");
        b.exports = c
    }, {
        asap: 4
    }],
    3: [function(a, b) {
        "use strict";

        function c(a) {
            this.then = function(b) {
                return "function" != typeof b ? this : new d(function(c, d) {
                    e(function() {
                        try {
                            c(b(a))
                        } catch (e) {
                            d(e)
                        }
                    })
                })
            }
        }
        var d = a("./core.js"),
            e = a("asap");
        b.exports = d, c.prototype = d.prototype;
        var f = new c(!0),
            g = new c(!1),
            h = new c(null),
            i = new c(void 0),
            j = new c(0),
            k = new c("");
        d.resolve = function(a) {
            if (a instanceof d) return a;
            if (null === a) return h;
            if (void 0 === a) return i;
            if (a === !0) return f;
            if (a === !1) return g;
            if (0 === a) return j;
            if ("" === a) return k;
            if ("object" == typeof a || "function" == typeof a) try {
                var b = a.then;
                if ("function" == typeof b) return new d(b.bind(a))
            } catch (e) {
                return new d(function(a, b) {
                    b(e)
                })
            }
            return new c(a)
        }, d.all = function(a) {
            var b = Array.prototype.slice.call(a);
            return new d(function(a, c) {
                function d(f, g) {
                    try {
                        if (g && ("object" == typeof g || "function" == typeof g)) {
                            var h = g.then;
                            if ("function" == typeof h) return void h.call(g, function(a) {
                                d(f, a)
                            }, c)
                        }
                        b[f] = g, 0 === --e && a(b)
                    } catch (i) {
                        c(i)
                    }
                }
                if (0 === b.length) return a([]);
                for (var e = b.length, f = 0; f < b.length; f++) d(f, b[f])
            })
        }, d.reject = function(a) {
            return new d(function(b, c) {
                c(a)
            })
        }, d.race = function(a) {
            return new d(function(b, c) {
                a.forEach(function(a) {
                    d.resolve(a).then(b, c)
                })
            })
        }, d.prototype["catch"] = function(a) {
            return this.then(null, a)
        }
    }, {
        "./core.js": 2,
        asap: 4
    }],
    4: [function(a, b) {
        (function(a) {
            function c() {
                for (; e.next;) {
                    e = e.next;
                    var a = e.task;
                    e.task = void 0;
                    var b = e.domain;
                    b && (e.domain = void 0, b.enter());
                    try {
                        a()
                    } catch (d) {
                        if (i) throw b && b.exit(), setTimeout(c, 0), b && b.enter(), d;
                        setTimeout(function() {
                            throw d
                        }, 0)
                    }
                    b && b.exit()
                }
                g = !1
            }

            function d(b) {
                f = f.next = {
                    task: b,
                    domain: i && a.domain,
                    next: null
                }, g || (g = !0, h())
            }
            var e = {
                    task: void 0,
                    next: null
                },
                f = e,
                g = !1,
                h = void 0,
                i = !1;
            if ("undefined" != typeof a && a.nextTick) i = !0, h = function() {
                a.nextTick(c)
            };
            else if ("function" == typeof setImmediate) h = "undefined" != typeof window ? setImmediate.bind(window, c) : function() {
                setImmediate(c)
            };
            else if ("undefined" != typeof MessageChannel) {
                var j = new MessageChannel;
                j.port1.onmessage = c, h = function() {
                    j.port2.postMessage(0)
                }
            } else h = function() {
                setTimeout(c, 0)
            };
            b.exports = d
        }).call(this, a("_process"))
    }, {
        _process: 1
    }],
    5: [function() {
        "function" != typeof Promise.prototype.done && (Promise.prototype.done = function() {
            var a = arguments.length ? this.then.apply(this, arguments) : this;
            a.then(null, function(a) {
                setTimeout(function() {
                    throw a
                }, 0)
            })
        })
    }, {}],
    6: [function(a) {
        a("asap");
        "undefined" == typeof Promise && (Promise = a("./lib/core.js"), a("./lib/es6-extensions.js")), a("./polyfill-done.js")
    }, {
        "./lib/core.js": 2,
        "./lib/es6-extensions.js": 3,
        "./polyfill-done.js": 5,
        asap: 4
    }]
}, {}, [6]);
! function(a, b) {
    function c() {
        var a = {},
            b = new o(function(b, c) {
                a.resolve = b, a.reject = c
            });
        return a.promise = b, a
    }

    function d(a, b) {
        for (var c in b) void 0 === a[c] && (a[c] = b[c]);
        return a
    }

    function e(a) {
        var b = document.getElementsByTagName("head")[0] || document.getElementsByTagName("body")[0] || document.firstElementChild || document;
        b.appendChild(a)
    }

    function f(a) {
        var b = [];
        for (var c in a) a[c] && b.push(c + "=" + encodeURIComponent(a[c]));
        return b.join("&")
    }

    function g(a) {
        return a.substring(a.lastIndexOf(".", a.lastIndexOf(".") - 1) + 1)
    }

    function h(a) {
        function b(a, b) {
            return a << b | a >>> 32 - b
        }

        function c(a, b) {
            var c, d, e, f, g;
            return e = 2147483648 & a, f = 2147483648 & b, c = 1073741824 & a, d = 1073741824 & b, g = (1073741823 & a) + (1073741823 & b), c & d ? 2147483648 ^ g ^ e ^ f : c | d ? 1073741824 & g ? 3221225472 ^ g ^ e ^ f : 1073741824 ^ g ^ e ^ f : g ^ e ^ f
        }

        function d(a, b, c) {
            return a & b | ~a & c
        }

        function e(a, b, c) {
            return a & c | b & ~c
        }

        function f(a, b, c) {
            return a ^ b ^ c
        }

        function g(a, b, c) {
            return b ^ (a | ~c)
        }

        function h(a, e, f, g, h, i, j) {
            return a = c(a, c(c(d(e, f, g), h), j)), c(b(a, i), e)
        }

        function i(a, d, f, g, h, i, j) {
            return a = c(a, c(c(e(d, f, g), h), j)), c(b(a, i), d)
        }

        function j(a, d, e, g, h, i, j) {
            return a = c(a, c(c(f(d, e, g), h), j)), c(b(a, i), d)
        }

        function k(a, d, e, f, h, i, j) {
            return a = c(a, c(c(g(d, e, f), h), j)), c(b(a, i), d)
        }

        function l(a) {
            for (var b, c = a.length, d = c + 8, e = (d - d % 64) / 64, f = 16 * (e + 1), g = new Array(f - 1), h = 0, i = 0; c > i;) b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | a.charCodeAt(i) << h, i++;
            return b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | 128 << h, g[f - 2] = c << 3, g[f - 1] = c >>> 29, g
        }

        function m(a) {
            var b, c, d = "",
                e = "";
            for (c = 0; 3 >= c; c++) b = a >>> 8 * c & 255, e = "0" + b.toString(16), d += e.substr(e.length - 2, 2);
            return d
        }

        function n(a) {
            a = a.replace(/\r\n/g, "\n");
            for (var b = "", c = 0; c < a.length; c++) {
                var d = a.charCodeAt(c);
                128 > d ? b += String.fromCharCode(d) : d > 127 && 2048 > d ? (b += String.fromCharCode(d >> 6 | 192), b += String.fromCharCode(63 & d | 128)) : (b += String.fromCharCode(d >> 12 | 224), b += String.fromCharCode(d >> 6 & 63 | 128), b += String.fromCharCode(63 & d | 128))
            }
            return b
        }
        var o, p, q, r, s, t, u, v, w, x = [],
            y = 7,
            z = 12,
            A = 17,
            B = 22,
            C = 5,
            D = 9,
            E = 14,
            F = 20,
            G = 4,
            H = 11,
            I = 16,
            J = 23,
            K = 6,
            L = 10,
            M = 15,
            N = 21;
        for (a = n(a), x = l(a), t = 1732584193, u = 4023233417, v = 2562383102, w = 271733878, o = 0; o < x.length; o += 16) p = t, q = u, r = v, s = w, t = h(t, u, v, w, x[o + 0], y, 3614090360), w = h(w, t, u, v, x[o + 1], z, 3905402710), v = h(v, w, t, u, x[o + 2], A, 606105819), u = h(u, v, w, t, x[o + 3], B, 3250441966), t = h(t, u, v, w, x[o + 4], y, 4118548399), w = h(w, t, u, v, x[o + 5], z, 1200080426), v = h(v, w, t, u, x[o + 6], A, 2821735955), u = h(u, v, w, t, x[o + 7], B, 4249261313), t = h(t, u, v, w, x[o + 8], y, 1770035416), w = h(w, t, u, v, x[o + 9], z, 2336552879), v = h(v, w, t, u, x[o + 10], A, 4294925233), u = h(u, v, w, t, x[o + 11], B, 2304563134), t = h(t, u, v, w, x[o + 12], y, 1804603682), w = h(w, t, u, v, x[o + 13], z, 4254626195), v = h(v, w, t, u, x[o + 14], A, 2792965006), u = h(u, v, w, t, x[o + 15], B, 1236535329), t = i(t, u, v, w, x[o + 1], C, 4129170786), w = i(w, t, u, v, x[o + 6], D, 3225465664), v = i(v, w, t, u, x[o + 11], E, 643717713), u = i(u, v, w, t, x[o + 0], F, 3921069994), t = i(t, u, v, w, x[o + 5], C, 3593408605), w = i(w, t, u, v, x[o + 10], D, 38016083), v = i(v, w, t, u, x[o + 15], E, 3634488961), u = i(u, v, w, t, x[o + 4], F, 3889429448), t = i(t, u, v, w, x[o + 9], C, 568446438), w = i(w, t, u, v, x[o + 14], D, 3275163606), v = i(v, w, t, u, x[o + 3], E, 4107603335), u = i(u, v, w, t, x[o + 8], F, 1163531501), t = i(t, u, v, w, x[o + 13], C, 2850285829), w = i(w, t, u, v, x[o + 2], D, 4243563512), v = i(v, w, t, u, x[o + 7], E, 1735328473), u = i(u, v, w, t, x[o + 12], F, 2368359562), t = j(t, u, v, w, x[o + 5], G, 4294588738), w = j(w, t, u, v, x[o + 8], H, 2272392833), v = j(v, w, t, u, x[o + 11], I, 1839030562), u = j(u, v, w, t, x[o + 14], J, 4259657740), t = j(t, u, v, w, x[o + 1], G, 2763975236), w = j(w, t, u, v, x[o + 4], H, 1272893353), v = j(v, w, t, u, x[o + 7], I, 4139469664), u = j(u, v, w, t, x[o + 10], J, 3200236656), t = j(t, u, v, w, x[o + 13], G, 681279174), w = j(w, t, u, v, x[o + 0], H, 3936430074), v = j(v, w, t, u, x[o + 3], I, 3572445317), u = j(u, v, w, t, x[o + 6], J, 76029189), t = j(t, u, v, w, x[o + 9], G, 3654602809), w = j(w, t, u, v, x[o + 12], H, 3873151461), v = j(v, w, t, u, x[o + 15], I, 530742520), u = j(u, v, w, t, x[o + 2], J, 3299628645), t = k(t, u, v, w, x[o + 0], K, 4096336452), w = k(w, t, u, v, x[o + 7], L, 1126891415), v = k(v, w, t, u, x[o + 14], M, 2878612391), u = k(u, v, w, t, x[o + 5], N, 4237533241), t = k(t, u, v, w, x[o + 12], K, 1700485571), w = k(w, t, u, v, x[o + 3], L, 2399980690), v = k(v, w, t, u, x[o + 10], M, 4293915773), u = k(u, v, w, t, x[o + 1], N, 2240044497), t = k(t, u, v, w, x[o + 8], K, 1873313359), w = k(w, t, u, v, x[o + 15], L, 4264355552), v = k(v, w, t, u, x[o + 6], M, 2734768916), u = k(u, v, w, t, x[o + 13], N, 1309151649), t = k(t, u, v, w, x[o + 4], K, 4149444226), w = k(w, t, u, v, x[o + 11], L, 3174756917), v = k(v, w, t, u, x[o + 2], M, 718787259), u = k(u, v, w, t, x[o + 9], N, 3951481745), t = c(t, p), u = c(u, q), v = c(v, r), w = c(w, s);
        var O = m(t) + m(u) + m(v) + m(w);
        return O.toLowerCase()
    }

    function i(a, b, c) {
        var d = c || {};
        document.cookie = a.replace(/[^+#$&^`|]/g, encodeURIComponent).replace("(", "%28").replace(")", "%29") + "=" + b.replace(/[^+#$&\/:<-\[\]-}]/g, encodeURIComponent) + (d.domain ? ";domain=" + d.domain : "") + (d.path ? ";path=" + d.path : "") + (d.secure ? ";secure" : "") + (d.httponly ? ";HttpOnly" : "")
    }

    function j(a) {
        var b = new RegExp("(?:^|;\\s*)" + a + "\\=([^;]+)(?:;\\s*|$)").exec(document.cookie);
        return b ? b[1] : void 0
    }

    function k(a, b, c) {
        var d = new Date;
        d.setTime(d.getTime() - 864e5);
        var e = "/";
        document.cookie = a + "=;path=" + e + ";domain=." + b + ";expires=" + d.toGMTString(), document.cookie = a + "=;path=" + e + ";domain=." + c + "." + b + ";expires=" + d.toGMTString()
    }

    function l() {
        var b = a.location.hostname;
        if (!b) {
            var c = a.parent.location.hostname;
            c && ~c.indexOf("zebra.alibaba-inc.com") && (b = c)
        }
        var d = ["taobao.net", "taobao.com", "tmall.com", "tmall.hk", "alibaba-inc.com"],
            e = new RegExp("([^.]*?)\\.?((?:" + d.join(")|(?:").replace(/\./g, "\\.") + "))", "i"),
            f = b.match(e) || [],
            g = f[2] || "taobao.com",
            h = f[1] || "m";
        "taobao.net" !== g || "x" !== h && "waptest" !== h && "daily" !== h ? "taobao.net" === g && "demo" === h ? h = "demo" : "alibaba-inc.com" === g && "zebra" === h ? h = "zebra" : "waptest" !== h && "wapa" !== h && "m" !== h && (h = "m") : h = "waptest";
        var i = "api";
        ("taobao.com" === g || "tmall.com" === g) && (i = "h5api"), t.mainDomain = g, t.subDomain = h, t.prefix = i
    }

    function m() {
        var b = a.navigator.userAgent,
            c = b.match(/WindVane[\/\s]([\d\.\_]+)/);
        c && (t.WindVaneVersion = c[1]);
        var d = b.match(/AliApp\(([^\/]+)\/([\d\.\_]+)\)/i);
        d && (t.AliAppName = d[1], t.AliAppVersion = d[2])
    }

    function n(a) {
        this.id = ++w, this.params = d(a || {}, {
            v: "*",
            data: {},
            type: "get",
            dataType: "jsonp"
        }), this.params.type = this.params.type.toLowerCase(), "object" == typeof this.params.data && (this.params.data = JSON.stringify(this.params.data)), this.middlewares = u.slice(0)
    }
    var o = a.Promise;
    if (!o) {
        var p = "褰撳墠娴忚鍣ㄤ笉鏀寔Promise锛岃鍦╳indows瀵硅薄涓婃寕杞絇romise瀵硅薄鍙弬鑰冿紙http://gitlab.alibaba-inc.com/mtb/lib-es6polyfill/tree/master锛変腑鐨勮В鍐虫柟妗�";
        throw b.mtop = {
            ERROR: p
        }, new Error(p)
    }
    String.prototype.trim || (String.prototype.trim = function() {
        return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "")
    });
    var q, r = o.resolve();
    try {
        q = a.localStorage, q.setItem("@private", "false")
    } catch (s) {
        q = !1
    }
    var t = {
            useJsonpResultType: !1,
            safariGoLogin: !0,
            useAlipayJSBridge: !1
        },
        u = [],
        v = {
            ERROR: -1,
            SUCCESS: 0,
            TOKEN_EXPIRED: 1,
            SESSION_EXPIRED: 2
        };
    l(), m();
    var w = 0,
        x = "2.4.2";
    n.prototype.use = function(a) {
        if (!a) throw new Error("middleware is undefined");
        return this.middlewares.push(a), this
    }, n.prototype.__processRequestMethod = function(a) {
        var b = this.params,
            c = this.options;
        "get" === b.type && "jsonp" === b.dataType ? c.getJSONP = !0 : "get" === b.type && "originaljsonp" === b.dataType ? c.getOriginalJSONP = !0 : "get" === b.type && "json" === b.dataType ? c.getJSON = !0 : "post" === b.type && (c.postJSON = !0), a()
    }, n.prototype.__processRequestType = function(c) {
        var d = this,
            e = this.options;
        if (t.H5Request === !0 && (e.H5Request = !0), t.WindVaneRequest === !0 && (e.WindVaneRequest = !0), e.H5Request === !1 && e.WindVaneRequest === !0) {
            if (!b.windvane || parseFloat(e.WindVaneVersion) < 5.4) throw new Error("WINDVANE_NOT_FOUND::缂哄皯WindVane鐜")
        } else e.H5Request === !0 ? e.WindVaneRequest = !1 : "undefined" == typeof e.WindVaneRequest && "undefined" == typeof e.H5Request && (b.windvane && parseFloat(e.WindVaneVersion) >= 5.4 ? e.WindVaneRequest = !0 : e.H5Request = !0);
        var f = a.navigator.userAgent.toLowerCase();
        return f.indexOf("youku") > -1 && e.mainDomain.indexOf("youku.com") < 0 && (e.WindVaneRequest = !1, e.H5Request = !0), e.mainDomain.indexOf("youku.com") > -1 && f.indexOf("youku") < 0 && (e.WindVaneRequest = !1, e.H5Request = !0), c ? c().then(function() {
            var a = e.retJson.ret;
            return a instanceof Array && (a = a.join(",")), e.WindVaneRequest === !0 && (!a || a.indexOf("PARAM_PARSE_ERROR") > -1 || a.indexOf("HY_FAILED") > -1 || a.indexOf("HY_NO_HANDLER") > -1 || a.indexOf("HY_CLOSED") > -1 || a.indexOf("HY_EXCEPTION") > -1 || a.indexOf("HY_NO_PERMISSION") > -1) ? (t.H5Request = !0, d.__sequence([d.__processRequestType, d.__processToken, d.__processRequestUrl, d.middlewares, d.__processRequest])) : void 0
        }) : void 0
    };
    var y = "_m_h5_c",
        z = "_m_h5_tk",
        A = "_m_h5_tk_enc";
    n.prototype.__getTokenFromAlipay = function() {
        var b = c(),
            d = this.options,
            e = (a.navigator.userAgent, !!location.protocol.match(/^https?\:$/)),
            f = "AP" === d.AliAppName && parseFloat(d.AliAppVersion) >= 8.2;
        return d.useAlipayJSBridge === !0 && !e && f && a.AlipayJSBridge && a.AlipayJSBridge.call ? a.AlipayJSBridge.call("getMtopToken", function(a) {
            a && a.token && (d.token = a.token), b.resolve()
        }, function() {
            b.resolve()
        }) : b.resolve(), b.promise
    }, n.prototype.__getTokenFromCookie = function() {
        var a = this.options;
        return a.CDR && j(y) ? a.token = j(y).split(";")[0] : a.token = a.token || j(z), a.token && (a.token = a.token.split("_")[0]), o.resolve()
    }, n.prototype.__processToken = function(a) {
        var b = this,
            c = this.options;
        this.params;
        return c.token && delete c.token, c.WindVaneRequest !== !0 ? r.then(function() {
            return b.__getTokenFromAlipay()
        }).then(function() {
            return b.__getTokenFromCookie()
        }).then(a).then(function() {
            var a = c.retJson,
                d = a.ret;
            if (d instanceof Array && (d = d.join(",")), d.indexOf("TOKEN_EMPTY") > -1 || c.CDR === !0 && d.indexOf("ILLEGAL_ACCESS") > -1 || d.indexOf("TOKEN_EXOIRED") > -1) {
                if (c.maxRetryTimes = c.maxRetryTimes || 5, c.failTimes = c.failTimes || 0, c.H5Request && ++c.failTimes < c.maxRetryTimes) return b.__sequence([b.__processToken, b.__processRequestUrl, b.middlewares, b.__processRequest]);
                c.maxRetryTimes > 0 && (k(y, c.pageDomain, "*"), k(z, c.mainDomain, c.subDomain), k(A, c.mainDomain, c.subDomain)), a.retType = v.TOKEN_EXPIRED
            }
        }) : void a()
    }, n.prototype.__processRequestUrl = function(b) {
        var c = this.params,
            d = this.options;
        if (d.hostSetting && d.hostSetting[a.location.hostname]) {
            var e = d.hostSetting[a.location.hostname];
            e.prefix && (d.prefix = e.prefix), e.subDomain && (d.subDomain = e.subDomain), e.mainDomain && (d.mainDomain = e.mainDomain)
        }
        if (d.H5Request === !0) {
            var f = "//" + (d.prefix ? d.prefix + "." : "") + (d.subDomain ? d.subDomain + "." : "") + d.mainDomain + "/h5/" + c.api.toLowerCase() + "/" + c.v.toLowerCase() + "/",
                g = c.appKey || ("waptest" === d.subDomain ? "4272" : "12574478"),
                i = (new Date).getTime(),
                j = h(d.token + "&" + i + "&" + g + "&" + c.data),
                k = {
                    jsv: x,
                    appKey: g,
                    t: i,
                    sign: j
                },
                l = {
                    data: c.data,
                    ua: c.ua
                };
            Object.keys(c).forEach(function(a) {
                "undefined" == typeof k[a] && "undefined" == typeof l[a] && (k[a] = c[a])
            }), d.getJSONP ? k.type = "jsonp" : d.getOriginalJSONP ? k.type = "originaljsonp" : (d.getJSON || d.postJSON) && (k.type = "originaljson"), d.useJsonpResultType === !0 && "originaljson" === k.type && delete k.type, d.querystring = k, d.postdata = l, d.path = f
        }
        b()
    }, n.prototype.__processUnitPrefix = function(a) {
        a()
    };
    var B = 0;
    n.prototype.__requestJSONP = function(a) {
        function b(a) {
            if (k && clearTimeout(k), l.parentNode && l.parentNode.removeChild(l), "TIMEOUT" === a) window[j] = function() {
                window[j] = void 0;
                try {
                    delete window[j]
                } catch (a) {}
            };
            else {
                window[j] = void 0;
                try {
                    delete window[j]
                } catch (b) {}
            }
        }
        var d = c(),
            g = this.params,
            h = this.options,
            i = g.timeout || 2e4,
            j = "mtopjsonp" + (g.jsonpIncPrefix || "") + ++B,
            k = setTimeout(function() {
                a("TIMEOUT::鎺ュ彛瓒呮椂"), b("TIMEOUT")
            }, i);
        h.querystring.callback = j;
        var l = document.createElement("script");
        return l.src = h.path + "?" + f(h.querystring) + "&" + f(h.postdata), l.async = !0, l.onerror = function() {
            b("ABORT"), a("ABORT::鎺ュ彛寮傚父閫€鍑�")
        }, window[j] = function() {
            h.results = Array.prototype.slice.call(arguments), b(), d.resolve()
        }, e(l), d.promise
    }, n.prototype.__requestJSON = function(b) {
        function d(a) {
            l && clearTimeout(l), "TIMEOUT" === a && i.abort()
        }
        var e = c(),
            g = this.params,
            h = this.options,
            i = new a.XMLHttpRequest,
            k = g.timeout || 2e4,
            l = setTimeout(function() {
                b("TIMEOUT::鎺ュ彛瓒呮椂"), d("TIMEOUT")
            }, k);
        h.CDR && j(y) && (h.querystring.c = decodeURIComponent(j(y))), i.onreadystatechange = function() {
            if (4 == i.readyState) {
                var a, c, f = i.status;
                if (f >= 200 && 300 > f || 304 == f) {
                    d(), a = i.responseText, c = i.getAllResponseHeaders() || "";
                    try {
                        a = /^\s*$/.test(a) ? {} : JSON.parse(a), a.responseHeaders = c, h.results = [a], e.resolve()
                    } catch (g) {
                        b("PARSE_JSON_ERROR::瑙ｆ瀽JSON澶辫触")
                    }
                } else d("ABORT"), b("ABORT::鎺ュ彛寮傚父閫€鍑�")
            }
        };
        var m, n, o = h.path + "?" + f(h.querystring);
        if (h.getJSON ? (m = "GET", o += "&" + f(h.postdata)) : h.postJSON && (m = "POST", n = f(h.postdata)), i.open(m, o, !0), i.withCredentials = !0, i.setRequestHeader("Accept", "application/json"), i.setRequestHeader("Content-type", "application/x-www-form-urlencoded"), g.headers)
            for (var p in g.headers) i.setRequestHeader(p, g.headers[p]);
        return i.send(n), e.promise
    }, n.prototype.__requestWindVane = function(a) {
        function d(a) {
            g.results = [a], e.resolve()
        }
        var e = c(),
            f = this.params,
            g = this.options,
            h = f.data,
            i = f.api,
            j = f.v,
            k = g.postJSON ? 1 : 0,
            l = g.getJSON || g.postJSON ? "originaljson" : "";
        g.useJsonpResultType === !0 && (l = "");
        var m, n, o = "https" === location.protocol ? 1 : 0,
            p = f.isSec || 0,
            q = f.sessionOption || "AutoLoginOnly",
            r = f.ecode || 0;
        return n = "undefined" != typeof f.timer ? parseInt(f.timer) : "undefined" != typeof f.timeout ? parseInt(f.timeout) : 2e4, m = 2 * n, f.needLogin === !0 && "undefined" == typeof f.sessionOption && (q = "AutoLoginAndManualLogin"), "undefined" != typeof f.secType && "undefined" == typeof f.isSec && (p = f.secType), b.windvane.call("MtopWVPlugin", "send", {
            api: i,
            v: j,
            post: String(k),
            type: l,
            isHttps: String(o),
            ecode: String(r),
            isSec: String(p),
            param: JSON.parse(h),
            timer: n,
            sessionOption: q,
            ext_headers: {
                referer: location.href
            }
        }, d, d, m), e.promise
    }, n.prototype.__processRequest = function(a, b) {
        var c = this;
        return r.then(function() {
            var a = c.options;
            if (a.H5Request && (a.getJSONP || a.getOriginalJSONP)) return c.__requestJSONP(b);
            if (a.H5Request && (a.getJSON || a.postJSON)) return c.__requestJSON(b);
            if (a.WindVaneRequest) return c.__requestWindVane(b);
            throw new Error("UNEXCEPT_REQUEST::閿欒鐨勮姹傜被鍨�")
        }).then(a).then(function() {
            var a = c.options,
                b = (c.params, a.results[0]),
                d = b && b.ret || [];
            b.ret = d, d instanceof Array && (d = d.join(","));
            var e = b.c;
            a.CDR && e && i(y, e, {
                domain: a.pageDomain,
                path: "/"
            }), d.indexOf("SUCCESS") > -1 ? b.retType = v.SUCCESS : b.retType = v.ERROR, a.retJson = b
        })
    }, n.prototype.__sequence = function(a) {
        function b(a) {
            if (a instanceof Array) a.forEach(b);
            else {
                var g, h = c(),
                    i = c();
                e.push(function() {
                    return h = c(), g = a.call(d, function(a) {
                        return h.resolve(a), i.promise
                    }, function(a) {
                        return h.reject(a), i.promise
                    }), g && (g = g["catch"](function(a) {
                        h.reject(a)
                    })), h.promise
                }), f.push(function(a) {
                    return i.resolve(a), g
                })
            }
        }
        var d = this,
            e = [],
            f = [];
        a.forEach(b);
        for (var g, h = r; g = e.shift();) h = h.then(g);
        for (; g = f.pop();) h = h.then(g);
        return h
    };
    var C = function(a) {
            a()
        },
        D = function(a) {
            a()
        };
    n.prototype.request = function(b) {
        var c = this;
        this.options = d(b || {}, t);
        var e = o.resolve([C, D]).then(function(a) {
            var b = a[0],
                d = a[1];
            return c.__sequence([b, c.__processRequestMethod, c.__processRequestType, c.__processToken, c.__processRequestUrl, c.middlewares, c.__processRequest, d])
        }).then(function() {
            var a = c.options.retJson;
            return a.retType !== v.SUCCESS ? o.reject(a) : c.options.successCallback ? void c.options.successCallback(a) : o.resolve(a)
        })["catch"](function(a) {
            var b;
            return a instanceof Error ? (console.error(a.stack), b = {
                ret: [a.message],
                stack: [a.stack],
                retJson: v.ERROR
            }) : b = "string" == typeof a ? {
                ret: [a],
                retJson: v.ERROR
            } : void 0 !== a ? a : c.options.retJson, c.options.failureCallback ? void c.options.failureCallback(b) : o.reject(b)
        });
        return this.__processRequestType(), c.options.H5Request && (c.constructor.__firstProcessor || (c.constructor.__firstProcessor = e), C = function(a) {
            c.constructor.__firstProcessor.then(a)["catch"](a)
        }), ("get" === this.params.type && "json" === this.params.dataType || "post" === this.params.type) && (b.pageDomain = b.pageDomain || g(a.location.hostname), b.mainDomain !== b.pageDomain && (b.maxRetryTimes = 4, b.CDR = !0)), e
    }, b.mtop = function(a) {
        return new n(a)
    }, b.mtop.request = function(a, b, c) {
        var d = {
            H5Request: a.H5Request,
            WindVaneRequest: a.WindVaneRequest,
            LoginRequest: a.LoginRequest,
            AntiCreep: a.AntiCreep,
            AntiFlood: a.AntiFlood,
            successCallback: b,
            failureCallback: c || b
        };
        return new n(a).request(d)
    }, b.mtop.H5Request = function(a, b, c) {
        var d = {
            H5Request: !0,
            successCallback: b,
            failureCallback: c || b
        };
        return new n(a).request(d)
    }, b.mtop.middlewares = u, b.mtop.config = t, b.mtop.RESPONSE_TYPE = v, b.mtop.CLASS = n
}(window, window.lib || (window.lib = {})),
function(a, b) {
    function c(a) {
        return a.preventDefault(), !1
    }

    function d(a) {
        var b = new RegExp("(?:^|;\\s*)" + a + "\\=([^;]+)(?:;\\s*|$)").exec(document.cookie);
        return b ? b[1] : void 0
    }

    function e(b, d) {
        var e = this,
            f = a.dpr || 1,
            g = document.createElement("div"),
            h = document.documentElement.getBoundingClientRect(),
            i = Math.max(h.width, window.innerWidth) / f,
            j = Math.max(h.height, window.innerHeight) / f;
        g.style.cssText = ["-webkit-transform:scale(" + f + ") translateZ(0)", "-ms-transform:scale(" + f + ") translateZ(0)", "transform:scale(" + f + ") translateZ(0)", "-webkit-transform-origin:0 0", "-ms-transform-origin:0 0", "transform-origin:0 0", "width:" + i + "px", "height:" + j + "px", "z-index:999999", "position:" + (i > 800 ? "fixed" : "absolute"), "left:0", "top:0px", "background:" + (i > 800 ? "rgba(0,0,0,.5)" : "#FFF"), "display:none"].join(";");
        var k = document.createElement("div");
        k.style.cssText = ["width:100%", "height:52px", "background:#EEE", "line-height:52px", "text-align:left", "box-sizing:border-box", "padding-left:20px", "position:absolute", "left:0", "top:0", "font-size:16px", "font-weight:bold", "color:#333"].join(";"), k.innerText = b;
        var l = document.createElement("a");
        l.style.cssText = ["display:block", "position:absolute", "right:0", "top:0", "height:52px", "line-height:52px", "padding:0 20px", "color:#999"].join(";"), l.innerText = "鍏抽棴";
        var m = document.createElement("iframe");
        m.style.cssText = ["width:100%", "height:100%", "border:0", "overflow:hidden"].join(";"), i > 800 && (k.style.cssText = ["width:370px", "height:52px", "background:#EEE", "line-height:52px", "text-align:left", "box-sizing:border-box", "padding-left:20px", "position:absolute", "left:" + (i / 2 - 185) + "px", "top:40px", "font-size:16px", "font-weight:bold", "color:#333"].join(";"), m.style.cssText = ["position:absolute", "top:92px", "left:" + (i / 2 - 185) + "px", "width:370px", "height:480px", "border:0", "background:#FFF", "overflow:hidden"].join(";")), k.appendChild(l), g.appendChild(k), g.appendChild(m), g.className = "J_MIDDLEWARE_FRAME_WIDGET", document.body.appendChild(g), m.src = d, l.addEventListener("click", function() {
            e.hide();
            var a = document.createEvent("HTMLEvents");
            a.initEvent("close", !1, !1), g.dispatchEvent(a)
        }, !1), this.addEventListener = function() {
            g.addEventListener.apply(g, arguments)
        }, this.removeEventListener = function() {
            g.removeEventListener.apply(g, arguments)
        }, this.show = function() {
            document.addEventListener("touchmove", c, !1), g.style.display = "block", window.scrollTo(0, 0)
        }, this.hide = function() {
            document.removeEventListener("touchmove", c), window.scrollTo(0, -h.top), g.parentNode && g.parentNode.removeChild(g)
        }
    }

    function f(a) {
        var c = this,
            d = this.options,
            e = this.params;
        return a().then(function() {
            var a = d.retJson,
                f = a.ret,
                g = navigator.userAgent.toLowerCase(),
                h = g.indexOf("safari") > -1 && g.indexOf("chrome") < 0 && g.indexOf("qqbrowser") < 0;
            if (f instanceof Array && (f = f.join(",")), (f.indexOf("SESSION_EXPIRED") > -1 || f.indexOf("SID_INVALID") > -1 || f.indexOf("AUTH_REJECT") > -1 || f.indexOf("NEED_LOGIN") > -1) && (a.retType = l.SESSION_EXPIRED, !d.WindVaneRequest && (k.LoginRequest === !0 || d.LoginRequest === !0 || e.needLogin === !0))) {
                if (!b.login) throw new Error("LOGIN_NOT_FOUND::缂哄皯lib.login");
                if (d.safariGoLogin !== !0 || !h || "taobao.com" === d.pageDomain) return b.login.goLoginAsync().then(function(a) {
                    return c.__sequence([c.__processToken, c.__processRequestUrl, c.__processUnitPrefix, c.middlewares, c.__processRequest])
                })["catch"](function(a) {
                    throw "CANCEL" === a ? new Error("LOGIN_CANCEL::鐢ㄦ埛鍙栨秷鐧诲綍") : new Error("LOGIN_FAILURE::鐢ㄦ埛鐧诲綍澶辫触")
                });
                b.login.goLogin()
            }
        })
    }

    function g(a) {
        var b = this.options;
        this.params;
        return b.H5Request !== !0 || k.AntiFlood !== !0 && b.AntiFlood !== !0 ? void a() : a().then(function() {
            var a = b.retJson,
                c = a.ret;
            c instanceof Array && (c = c.join(",")), c.indexOf("FAIL_SYS_USER_VALIDATE") > -1 && a.data.url && (b.AntiFloodReferer ? location.href = a.data.url.replace(/(http_referer=).+/, "$1" + b.AntiFloodReferer) : location.href = a.data.url)
        })
    }

    function h(b) {
        var c = this,
            f = this.options,
            g = this.params;
        return g.forceAntiCreep !== !0 && f.H5Request !== !0 || k.AntiCreep !== !0 && f.AntiCreep !== !0 ? void b() : b().then(function() {
            var b = f.retJson,
                h = b.ret;
            if (h instanceof Array && (h = h.join(",")), h.indexOf("RGV587_ERROR::SM") > -1 && b.data.url) {
                var j = "_m_h5_smt",
                    k = d(j),
                    l = !1;
                if (f.saveAntiCreepToken === !0 && k) {
                    k = JSON.parse(k);
                    for (var m in k) g[m] && (l = !0)
                }
                if (f.saveAntiCreepToken === !0 && k && !l) {
                    for (var m in k) g[m] = k[m];
                    return c.__sequence([c.__processToken, c.__processRequestUrl, c.__processUnitPrefix, c.middlewares, c.__processRequest])
                }
                return new i(function(d, h) {
                    function i() {
                        m.removeEventListener("close", i), a.removeEventListener("message", k), h("USER_INPUT_CANCEL::鐢ㄦ埛鍙栨秷杈撳叆")
                    }

                    function k(b) {
                        var e;
                        try {
                            e = JSON.parse(b.data) || {}
                        } catch (l) {}
                        if (e && "child" === e.type) {
                            m.removeEventListener("close", i), a.removeEventListener("message", k), m.hide();
                            var n;
                            try {
                                n = JSON.parse(decodeURIComponent(e.content)), "string" == typeof n && (n = JSON.parse(n));
                                for (var o in n) g[o] = n[o];
                                f.saveAntiCreepToken === !0 ? (document.cookie = j + "=" + JSON.stringify(n) + ";", a.location.reload()) : c.__sequence([c.__processToken, c.__processRequestUrl, c.__processUnitPrefix, c.middlewares, c.__processRequest]).then(d)
                            } catch (l) {
                                h("USER_INPUT_FAILURE::鐢ㄦ埛杈撳叆澶辫触")
                            }
                        }
                    }
                    var l = b.data.url,
                        m = new e("", l);
                    m.addEventListener("close", i, !1), a.addEventListener("message", k, !1), m.show()
                })
            }
        })
    }
    if (!b || !b.mtop || b.mtop.ERROR) throw new Error("Mtop 鍒濆鍖栧け璐ワ紒璇峰弬鑰僊top鏂囨。http://gitlab.alibaba-inc.com/mtb/lib-mtop");
    var i = a.Promise,
        j = b.mtop.CLASS,
        k = b.mtop.config,
        l = b.mtop.RESPONSE_TYPE;
    b.mtop.middlewares.push(f), b.mtop.loginRequest = function(a, b, c) {
        var d = {
            LoginRequest: !0,
            H5Request: !0,
            successCallback: b,
            failureCallback: c || b
        };
        return new j(a).request(d)
    }, b.mtop.antiFloodRequest = function(a, b, c) {
        var d = {
            AntiFlood: !0,
            successCallback: b,
            failureCallback: c || b
        };
        return new j(a).request(d)
    }, b.mtop.middlewares.push(g), b.mtop.antiCreepRequest = function(a, b, c) {
        var d = {
            AntiCreep: !0,
            successCallback: b,
            failureCallback: c || b
        };
        return new j(a).request(d)
    }, b.mtop.middlewares.push(h)
}(window, window.lib || (window.lib = {}));
! function(a, b, c) {
    function d(a) {
        var b = new RegExp("(?:^|;\\s*)" + a + "\\=([^;]+)(?:;\\s*|$)").exec(v.cookie);
        return b ? b[1] : c
    }

    function e(a) {
        return a.preventDefault(), !1
    }

    function f(b, c) {
        var d = this,
            f = a.dpr || 1,
            g = document.createElement("div"),
            h = document.documentElement.getBoundingClientRect(),
            i = Math.max(h.width, window.innerWidth) / f,
            j = Math.max(h.height, window.innerHeight) / f;
        g.style.cssText = ["-webkit-transform:scale(" + f + ") translateZ(0)", "-ms-transform:scale(" + f + ") translateZ(0)", "transform:scale(" + f + ") translateZ(0)", "-webkit-transform-origin:0 0", "-ms-transform-origin:0 0", "transform-origin:0 0", "width:" + i + "px", "height:" + j + "px", "z-index:999999", "position:absolute", "left:0", "top:0px", "background:#FFF", "display:none"].join(";");
        var k = document.createElement("div");
        k.style.cssText = ["width:100%", "height:52px", "background:#EEE", "line-height:52px", "text-align:left", "box-sizing:border-box", "padding-left:20px", "position:absolute", "left:0", "top:0", "font-size:16px", "font-weight:bold", "color:#333"].join(";"), k.innerText = b;
        var l = document.createElement("a");
        l.style.cssText = ["display:block", "position:absolute", "right:0", "top:0", "height:52px", "line-height:52px", "padding:0 20px", "color:#999"].join(";"), l.innerText = "鍏抽棴";
        var m = document.createElement("iframe");
        m.style.cssText = ["width:100%", "height:100%", "border:0", "overflow:hidden"].join(";"), k.appendChild(l), g.appendChild(k), g.appendChild(m), v.body.appendChild(g), m.src = c, l.addEventListener("click", function() {
            d.hide();
            var a = v.createEvent("HTMLEvents");
            a.initEvent("close", !1, !1), g.dispatchEvent(a)
        }, !1), this.addEventListener = function() {
            g.addEventListener.apply(g, arguments)
        }, this.removeEventListener = function() {
            g.removeEventListener.apply(g, arguments)
        }, this.show = function() {
            document.addEventListener("touchmove", e, !1), g.style.display = "block", window.scrollTo(0, 0)
        }, this.hide = function() {
            document.removeEventListener("touchmove", e), window.scrollTo(0, -h.top), v.body.removeChild(g)
        }
    }

    function g(a) {
        if (!a || "function" != typeof a || !b.mtop) {
            var d = this.getUserNick();
            return !!d
        }
        b.mtop.request({
            api: "mtop.user.getUserSimple",
            v: "1.0",
            data: {
                isSec: 0
            },
            H5Request: !0
        }, function(d) {
            d.retType === b.mtop.RESPONSE_TYPE.SUCCESS ? a(!0, d) : d.retType === b.mtop.RESPONSE_TYPE.SESSION_EXPIRED ? a(!1, d) : a(c, d)
        })
    }

    function h(a) {
        var b;
        return u && (b = {}, b.promise = new u(function(a, c) {
            b.resolve = a, b.reject = c
        })), this.isLogin(function(c, d) {
            a && a(c, d), c === !0 ? b && b.resolve(d) : b && b.reject(d)
        }), b ? b.promise : void 0
    }

    function i(a) {
        if (!a || "function" != typeof a) {
            var b = "",
                e = d("_w_tb_nick"),
                f = d("_nk_") || d("snk"),
                g = d("sn");
            return e && e.length > 0 && "null" != e ? b = decodeURIComponent(e) : f && f.length > 0 && "null" != f ? b = unescape(unescape(f).replace(/\\u/g, "%u")) : g && g.length > 0 && "null" != g && (b = decodeURIComponent(g)), b = b.replace(/\</g, "&lt;").replace(/\>/g, "&gt;")
        }
        this.isLogin(function(b, d) {
            a(b === !0 && d && d.data && d.data.nick ? d.data.nick : b === !1 ? "" : c)
        })
    }

    function j(a) {
        var b;
        return u && (b = {}, b.promise = new u(function(a, c) {
            b.resolve = a, b.reject = c
        })), this.getUserNick(function(c) {
            a && a(c), c ? b && b.resolve(c) : b && b.reject()
        }), b ? b.promise : void 0
    }

    function k(a, b) {
        var c = "//" + G + "." + H.subDomain + "." + E + "/" + H[(a || "login") + "Name"];
        if (b) {
            var d = [];
            for (var e in b) d.push(e + "=" + encodeURIComponent(b[e]));
            c += "?" + d.join("&")
        }
        return c
    }

    function l(a, b) {
        b ? location.replace(a) : location.href = a
    }

    function m(b, c, d) {
        function e(b) {
            j.removeEventListener("close", e), a.removeEventListener("message", g), d("CANCEL")
        }

        function g(b) {
            var c = b.data || {};
            c && "child" === c.type && c.content.indexOf("SUCCESS") > -1 ? (j.removeEventListener("close", e), a.removeEventListener("message", g), j.hide(), d("SUCCESS")) : d("FAILURE")
        }
        var h = location.protocol + "//h5." + H.subDomain + ".taobao.com/" + ("waptest" === H.subDomain ? "src" : "other") + "/" + b + "end.html?origin=" + encodeURIComponent(location.protocol + "//" + location.hostname),
            i = k(b, {
                ttid: "h5@iframe",
                tpl_redirect_url: h
            }),
            j = new f(c.title || "鎮ㄩ渶瑕佺櫥褰曟墠鑳界户缁闂�", i);
        j.addEventListener("close", e, !1), a.addEventListener("message", g, !1), j.show()
    }

    function n(b, c, d) {
        var e = k(b, {
            wvLoginCallback: "wvLoginCallback"
        });
        a.wvLoginCallback = function(b) {
            delete a.wvLoginCallback, d(b.indexOf(":SUCCESS") > -1 ? "SUCCESS" : b.indexOf(":CANCEL") > -1 ? "CANCEL" : "FAILURE")
        }, l(e)
    }

    function o(a, b, c) {
        if ("function" == typeof b ? (c = b, b = null) : "string" == typeof b && (b = {
                redirectUrl: b
            }), b = b || {}, c && A) n(a, b, c);
        else if (c && !z && "login" === a) m(a, b, c);
        else {
            var d = k(a, {
                tpl_redirect_url: b.redirectUrl || location.href
            });
            l(d, b.replace)
        }
    }

    function p(a, b, c) {
        var d;
        return u && (d = {}, d.promise = new u(function(a, b) {
            d.resolve = a, d.reject = b
        })), o(a, b, function(a) {
            c && c(a), "SUCCESS" === a ? d && d.resolve(a) : d && d.reject(a)
        }), d ? d.promise : void 0
    }

    function q(a) {
        o("login", a)
    }

    function r(a) {
        return p("login", a)
    }

    function s(a) {
        o("logout", a)
    }

    function t(a) {
        return p("logout", a)
    }
    var u = a.Promise,
        v = a.document,
        w = a.navigator.userAgent,
        x = location.hostname,
        y = (a.location.search, w.match(/WindVane[\/\s]([\d\.\_]+)/)),
        z = w.match(/AliApp\(([^\/]+)\/([\d\.\_]+)\)/i),
        A = !!(z && "TB" === z[1] && y && parseFloat(y[1]) > 5.2),
        B = ["taobao.net", "taobao.com"],
        C = new RegExp("([^.]*?)\\.?((?:" + B.join(")|(?:").replace(/\./g, "\\.") + "))", "i"),
        D = x.match(C) || [],
        E = function() {
            var a = D[2] || "taobao.com";
            return a.match(/\.?taobao\.net$/) ? "taobao.net" : "taobao.com"
        }(),
        F = function() {
            var a = E,
                b = D[1] || "m";
            return "taobao.net" === a && (b = "waptest"), b
        }(),
        G = "login";
    b.login = b.login || {};
    var H = {
        loginName: "login.htm",
        logoutName: "logout.htm",
        subDomain: F
    };
    b.login.config = H, b.login.isLogin = g, b.login.isLoginAsync = h, b.login.getUserNick = i, b.login.getUserNickAsync = j, b.login.generateUrl = k, b.login.goLogin = q, b.login.goLoginAsync = r, b.login.goLogout = s, b.login.goLogoutAsync = t
}(window, window.lib || (window.lib = {}));