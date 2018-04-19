window.jQuery || function(e, t) {
        "object" == typeof module && "object" == typeof module.exports ? module.exports = e.document ? t(e, !0) : function(e) {
            if (!e.document) throw new Error("jQuery requires a window with a document");
            return t(e)
        } : t(e)
    }("undefined" != typeof window ? window : this, function(e, t) {
        function n(e) {
            var t = e.length,
                n = Z.type(e);
            return "function" === n || Z.isWindow(e) ? !1 : 1 === e.nodeType && t ? !0 : "array" === n || 0 === t || "number" == typeof t && t > 0 && t - 1 in e
        }

        function r(e, t, n) {
            if (Z.isFunction(t)) return Z.grep(e, function(e, r) {
                return !!t.call(e, r, e) !== n
            });
            if (t.nodeType) return Z.grep(e, function(e) {
                return e === t !== n
            });
            if ("string" == typeof t) {
                if (ae.test(t)) return Z.filter(t, e, n);
                t = Z.filter(t, e)
            }
            return Z.grep(e, function(e) {
                return U.call(t, e) >= 0 !== n
            })
        }

        function i(e, t) {
            for (;
                (e = e[t]) && 1 !== e.nodeType;);
            return e
        }

        function o(e) {
            var t = he[e] = {};
            return Z.each(e.match(de) || [], function(e, n) {
                t[n] = !0
            }), t
        }

        function s() {
            J.removeEventListener("DOMContentLoaded", s, !1), e.removeEventListener("load", s, !1), Z.ready()
        }

        function a() {
            Object.defineProperty(this.cache = {}, 0, {
                get: function() {
                    return {}
                }
            }), this.expando = Z.expando + Math.random()
        }

        function u(e, t, n) {
            var r;
            if (void 0 === n && 1 === e.nodeType)
                if (r = "data-" + t.replace(be, "-$1").toLowerCase(), n = e.getAttribute(r), "string" == typeof n) {
                    try {
                        n = "true" === n ? !0 : "false" === n ? !1 : "null" === n ? null : +n + "" === n ? +n : xe.test(n) ? Z.parseJSON(n) : n
                    } catch (i) {}
                    ye.set(e, t, n)
                } else n = void 0;
            return n
        }

        function l() {
            return !0
        }

        function c() {
            return !1
        }

        function f() {
            try {
                return J.activeElement
            } catch (e) {}
        }

        function p(e, t) {
            return Z.nodeName(e, "table") && Z.nodeName(11 !== t.nodeType ? t : t.firstChild, "tr") ? e.getElementsByTagName("tbody")[0] || e.appendChild(e.ownerDocument.createElement("tbody")) : e
        }

        function d(e) {
            return e.type = (null !== e.getAttribute("type")) + "/" + e.type, e
        }

        function h(e) {
            var t = Fe.exec(e.type);
            return t ? e.type = t[1] : e.removeAttribute("type"), e
        }

        function g(e, t) {
            for (var n = 0, r = e.length; r > n; n++) ve.set(e[n], "globalEval", !t || ve.get(t[n], "globalEval"))
        }

        function m(e, t) {
            var n, r, i, o, s, a, u, l;
            if (1 === t.nodeType) {
                if (ve.hasData(e) && (o = ve.access(e), s = ve.set(t, o), l = o.events)) {
                    delete s.handle, s.events = {};
                    for (i in l)
                        for (n = 0, r = l[i].length; r > n; n++) Z.event.add(t, i, l[i][n])
                }
                ye.hasData(e) && (a = ye.access(e), u = Z.extend({}, a), ye.set(t, u))
            }
        }

        function v(e, t) {
            var n = e.getElementsByTagName ? e.getElementsByTagName(t || "*") : e.querySelectorAll ? e.querySelectorAll(t || "*") : [];
            return void 0 === t || t && Z.nodeName(e, t) ? Z.merge([e], n) : n
        }

        function y(e, t) {
            var n = t.nodeName.toLowerCase();
            "input" === n && Ne.test(e.type) ? t.checked = e.checked : ("input" === n || "textarea" === n) && (t.defaultValue = e.defaultValue)
        }

        function x(t, n) {
            var r, i = Z(n.createElement(t)).appendTo(n.body),
                o = e.getDefaultComputedStyle && (r = e.getDefaultComputedStyle(i[0])) ? r.display : Z.css(i[0], "display");
            return i.detach(), o
        }

        function b(e) {
            var t = J,
                n = $e[e];
            return n || (n = x(e, t), "none" !== n && n || (We = (We || Z("<iframe frameborder='0' width='0' height='0'/>")).appendTo(t.documentElement), t = We[0].contentDocument, t.write(), t.close(), n = x(e, t), We.detach()), $e[e] = n), n
        }

        function w(e, t, n) {
            var r, i, o, s, a = e.style;
            return n = n || _e(e), n && (s = n.getPropertyValue(t) || n[t]), n && ("" !== s || Z.contains(e.ownerDocument, e) || (s = Z.style(e, t)), Be.test(s) && Ie.test(t) && (r = a.width, i = a.minWidth, o = a.maxWidth, a.minWidth = a.maxWidth = a.width = s, s = n.width, a.width = r, a.minWidth = i, a.maxWidth = o)), void 0 !== s ? s + "" : s
        }

        function T(e, t) {
            return {
                get: function() {
                    return e() ? void delete this.get : (this.get = t).apply(this, arguments)
                }
            }
        }

        function C(e, t) {
            if (t in e) return t;
            for (var n = t[0].toUpperCase() + t.slice(1), r = t, i = Ge.length; i--;)
                if (t = Ge[i] + n, t in e) return t;
            return r
        }

        function N(e, t, n) {
            var r = ze.exec(t);
            return r ? Math.max(0, r[1] - (n || 0)) + (r[2] || "px") : t
        }

        function E(e, t, n, r, i) {
            for (var o = n === (r ? "border" : "content") ? 4 : "width" === t ? 1 : 0, s = 0; 4 > o; o += 2) "margin" === n && (s += Z.css(e, n + Te[o], !0, i)), r ? ("content" === n && (s -= Z.css(e, "padding" + Te[o], !0, i)), "margin" !== n && (s -= Z.css(e, "border" + Te[o] + "Width", !0, i))) : (s += Z.css(e, "padding" + Te[o], !0, i), "padding" !== n && (s += Z.css(e, "border" + Te[o] + "Width", !0, i)));
            return s
        }

        function k(e, t, n) {
            var r = !0,
                i = "width" === t ? e.offsetWidth : e.offsetHeight,
                o = _e(e),
                s = "border-box" === Z.css(e, "boxSizing", !1, o);
            if (0 >= i || null == i) {
                if (i = w(e, t, o), (0 > i || null == i) && (i = e.style[t]), Be.test(i)) return i;
                r = s && (Q.boxSizingReliable() || i === e.style[t]), i = parseFloat(i) || 0
            }
            return i + E(e, t, n || (s ? "border" : "content"), r, o) + "px"
        }

        function S(e, t) {
            for (var n, r, i, o = [], s = 0, a = e.length; a > s; s++) r = e[s], r.style && (o[s] = ve.get(r, "olddisplay"), n = r.style.display, t ? (o[s] || "none" !== n || (r.style.display = ""), "" === r.style.display && Ce(r) && (o[s] = ve.access(r, "olddisplay", b(r.nodeName)))) : (i = Ce(r), "none" === n && i || ve.set(r, "olddisplay", i ? n : Z.css(r, "display"))));
            for (s = 0; a > s; s++) r = e[s], r.style && (t && "none" !== r.style.display && "" !== r.style.display || (r.style.display = t ? o[s] || "" : "none"));
            return e
        }

        function j(e, t, n, r, i) {
            return new j.prototype.init(e, t, n, r, i)
        }

        function D() {
            return setTimeout(function() {
                Qe = void 0
            }), Qe = Z.now()
        }

        function A(e, t) {
            var n, r = 0,
                i = {
                    height: e
                };
            for (t = t ? 1 : 0; 4 > r; r += 2 - t) n = Te[r], i["margin" + n] = i["padding" + n] = e;
            return t && (i.opacity = i.width = e), i
        }

        function L(e, t, n) {
            for (var r, i = (nt[t] || []).concat(nt["*"]), o = 0, s = i.length; s > o; o++)
                if (r = i[o].call(n, t, e)) return r
        }

        function q(e, t, n) {
            var r, i, o, s, a, u, l, c, f = this,
                p = {},
                d = e.style,
                h = e.nodeType && Ce(e),
                g = ve.get(e, "fxshow");
            n.queue || (a = Z._queueHooks(e, "fx"), null == a.unqueued && (a.unqueued = 0, u = a.empty.fire, a.empty.fire = function() {
                a.unqueued || u()
            }), a.unqueued++, f.always(function() {
                f.always(function() {
                    a.unqueued--, Z.queue(e, "fx").length || a.empty.fire()
                })
            })), 1 === e.nodeType && ("height" in t || "width" in t) && (n.overflow = [d.overflow, d.overflowX, d.overflowY], l = Z.css(e, "display"), c = "none" === l ? ve.get(e, "olddisplay") || b(e.nodeName) : l, "inline" === c && "none" === Z.css(e, "float") && (d.display = "inline-block")), n.overflow && (d.overflow = "hidden", f.always(function() {
                d.overflow = n.overflow[0], d.overflowX = n.overflow[1], d.overflowY = n.overflow[2]
            }));
            for (r in t)
                if (i = t[r], Ke.exec(i)) {
                    if (delete t[r], o = o || "toggle" === i, i === (h ? "hide" : "show")) {
                        if ("show" !== i || !g || void 0 === g[r]) continue;
                        h = !0
                    }
                    p[r] = g && g[r] || Z.style(e, r)
                } else l = void 0;
            if (Z.isEmptyObject(p)) "inline" === ("none" === l ? b(e.nodeName) : l) && (d.display = l);
            else {
                g ? "hidden" in g && (h = g.hidden) : g = ve.access(e, "fxshow", {}), o && (g.hidden = !h), h ? Z(e).show() : f.done(function() {
                    Z(e).hide()
                }), f.done(function() {
                    var t;
                    ve.remove(e, "fxshow");
                    for (t in p) Z.style(e, t, p[t])
                });
                for (r in p) s = L(h ? g[r] : 0, r, f), r in g || (g[r] = s.start, h && (s.end = s.start, s.start = "width" === r || "height" === r ? 1 : 0))
            }
        }

        function H(e, t) {
            var n, r, i, o, s;
            for (n in e)
                if (r = Z.camelCase(n), i = t[r], o = e[n], Z.isArray(o) && (i = o[1], o = e[n] = o[0]), n !== r && (e[r] = o, delete e[n]), s = Z.cssHooks[r], s && "expand" in s) {
                    o = s.expand(o), delete e[r];
                    for (n in o) n in e || (e[n] = o[n], t[n] = i)
                } else t[r] = i
        }

        function O(e, t, n) {
            var r, i, o = 0,
                s = tt.length,
                a = Z.Deferred().always(function() {
                    delete u.elem
                }),
                u = function() {
                    if (i) return !1;
                    for (var t = Qe || D(), n = Math.max(0, l.startTime + l.duration - t), r = n / l.duration || 0, o = 1 - r, s = 0, u = l.tweens.length; u > s; s++) l.tweens[s].run(o);
                    return a.notifyWith(e, [l, o, n]), 1 > o && u ? n : (a.resolveWith(e, [l]), !1)
                },
                l = a.promise({
                    elem: e,
                    props: Z.extend({}, t),
                    opts: Z.extend(!0, {
                        specialEasing: {}
                    }, n),
                    originalProperties: t,
                    originalOptions: n,
                    startTime: Qe || D(),
                    duration: n.duration,
                    tweens: [],
                    createTween: function(t, n) {
                        var r = Z.Tween(e, l.opts, t, n, l.opts.specialEasing[t] || l.opts.easing);
                        return l.tweens.push(r), r
                    },
                    stop: function(t) {
                        var n = 0,
                            r = t ? l.tweens.length : 0;
                        if (i) return this;
                        for (i = !0; r > n; n++) l.tweens[n].run(1);
                        return t ? a.resolveWith(e, [l, t]) : a.rejectWith(e, [l, t]), this
                    }
                }),
                c = l.props;
            for (H(c, l.opts.specialEasing); s > o; o++)
                if (r = tt[o].call(l, e, c, l.opts)) return r;
            return Z.map(c, L, l), Z.isFunction(l.opts.start) && l.opts.start.call(e, l), Z.fx.timer(Z.extend(u, {
                elem: e,
                anim: l,
                queue: l.opts.queue
            })), l.progress(l.opts.progress).done(l.opts.done, l.opts.complete).fail(l.opts.fail).always(l.opts.always)
        }

        function M(e) {
            return function(t, n) {
                "string" != typeof t && (n = t, t = "*");
                var r, i = 0,
                    o = t.toLowerCase().match(de) || [];
                if (Z.isFunction(n))
                    for (; r = o[i++];) "+" === r[0] ? (r = r.slice(1) || "*", (e[r] = e[r] || []).unshift(n)) : (e[r] = e[r] || []).push(n)
            }
        }

        function F(e, t, n, r) {
            function i(a) {
                var u;
                return o[a] = !0, Z.each(e[a] || [], function(e, a) {
                    var l = a(t, n, r);
                    return "string" != typeof l || s || o[l] ? s ? !(u = l) : void 0 : (t.dataTypes.unshift(l), i(l), !1)
                }), u
            }
            var o = {},
                s = e === wt;
            return i(t.dataTypes[0]) || !o["*"] && i("*")
        }

        function P(e, t) {
            var n, r, i = Z.ajaxSettings.flatOptions || {};
            for (n in t) void 0 !== t[n] && ((i[n] ? e : r || (r = {}))[n] = t[n]);
            return r && Z.extend(!0, e, r), e
        }

        function R(e, t, n) {
            for (var r, i, o, s, a = e.contents, u = e.dataTypes;
                "*" === u[0];) u.shift(), void 0 === r && (r = e.mimeType || t.getResponseHeader("Content-Type"));
            if (r)
                for (i in a)
                    if (a[i] && a[i].test(r)) {
                        u.unshift(i);
                        break
                    }
            if (u[0] in n) o = u[0];
            else {
                for (i in n) {
                    if (!u[0] || e.converters[i + " " + u[0]]) {
                        o = i;
                        break
                    }
                    s || (s = i)
                }
                o = o || s
            }
            return o ? (o !== u[0] && u.unshift(o), n[o]) : void 0
        }

        function W(e, t, n, r) {
            var i, o, s, a, u, l = {},
                c = e.dataTypes.slice();
            if (c[1])
                for (s in e.converters) l[s.toLowerCase()] = e.converters[s];
            for (o = c.shift(); o;)
                if (e.responseFields[o] && (n[e.responseFields[o]] = t), !u && r && e.dataFilter && (t = e.dataFilter(t, e.dataType)), u = o, o = c.shift())
                    if ("*" === o) o = u;
                    else if ("*" !== u && u !== o) {
                if (s = l[u + " " + o] || l["* " + o], !s)
                    for (i in l)
                        if (a = i.split(" "), a[1] === o && (s = l[u + " " + a[0]] || l["* " + a[0]])) {
                            s === !0 ? s = l[i] : l[i] !== !0 && (o = a[0], c.unshift(a[1]));
                            break
                        }
                if (s !== !0)
                    if (s && e["throws"]) t = s(t);
                    else try {
                        t = s(t)
                    } catch (f) {
                        return {
                            state: "parsererror",
                            error: s ? f : "No conversion from " + u + " to " + o
                        }
                    }
            }
            return {
                state: "success",
                data: t
            }
        }

        function $(e, t, n, r) {
            var i;
            if (Z.isArray(t)) Z.each(t, function(t, i) {
                n || Et.test(e) ? r(e, i) : $(e + "[" + ("object" == typeof i ? t : "") + "]", i, n, r)
            });
            else if (n || "object" !== Z.type(t)) r(e, t);
            else
                for (i in t) $(e + "[" + i + "]", t[i], n, r)
        }

        function I(e) {
            return Z.isWindow(e) ? e : 9 === e.nodeType && e.defaultView
        }
        var B = [],
            _ = B.slice,
            X = B.concat,
            z = B.push,
            U = B.indexOf,
            Y = {},
            V = Y.toString,
            G = Y.hasOwnProperty,
            Q = {},
            J = e.document,
            K = "2.1.1",
            Z = function(e, t) {
                return new Z.fn.init(e, t)
            },
            ee = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,
            te = /^-ms-/,
            ne = /-([\da-z])/gi,
            re = function(e, t) {
                return t.toUpperCase()
            };
        Z.fn = Z.prototype = {
            jquery: K,
            constructor: Z,
            selector: "",
            length: 0,
            toArray: function() {
                return _.call(this)
            },
            get: function(e) {
                return null != e ? 0 > e ? this[e + this.length] : this[e] : _.call(this)
            },
            pushStack: function(e) {
                var t = Z.merge(this.constructor(), e);
                return t.prevObject = this, t.context = this.context, t
            },
            each: function(e, t) {
                return Z.each(this, e, t)
            },
            map: function(e) {
                return this.pushStack(Z.map(this, function(t, n) {
                    return e.call(t, n, t)
                }))
            },
            slice: function() {
                return this.pushStack(_.apply(this, arguments))
            },
            first: function() {
                return this.eq(0)
            },
            last: function() {
                return this.eq(-1)
            },
            eq: function(e) {
                var t = this.length,
                    n = +e + (0 > e ? t : 0);
                return this.pushStack(n >= 0 && t > n ? [this[n]] : [])
            },
            end: function() {
                return this.prevObject || this.constructor(null)
            },
            push: z,
            sort: B.sort,
            splice: B.splice
        }, Z.extend = Z.fn.extend = function() {
            var e, t, n, r, i, o, s = arguments[0] || {},
                a = 1,
                u = arguments.length,
                l = !1;
            for ("boolean" == typeof s && (l = s, s = arguments[a] || {}, a++), "object" == typeof s || Z.isFunction(s) || (s = {}), a === u && (s = this, a--); u > a; a++)
                if (null != (e = arguments[a]))
                    for (t in e) n = s[t], r = e[t], s !== r && (l && r && (Z.isPlainObject(r) || (i = Z.isArray(r))) ? (i ? (i = !1, o = n && Z.isArray(n) ? n : []) : o = n && Z.isPlainObject(n) ? n : {}, s[t] = Z.extend(l, o, r)) : void 0 !== r && (s[t] = r));
            return s
        }, Z.extend({
            expando: "jQuery" + (K + Math.random()).replace(/\D/g, ""),
            isReady: !0,
            error: function(e) {
                throw new Error(e)
            },
            noop: function() {},
            isFunction: function(e) {
                return "function" === Z.type(e)
            },
            isArray: Array.isArray,
            isWindow: function(e) {
                return null != e && e === e.window
            },
            isNumeric: function(e) {
                return !Z.isArray(e) && e - parseFloat(e) >= 0
            },
            isPlainObject: function(e) {
                return "object" !== Z.type(e) || e.nodeType || Z.isWindow(e) ? !1 : e.constructor && !G.call(e.constructor.prototype, "isPrototypeOf") ? !1 : !0
            },
            isEmptyObject: function(e) {
                var t;
                for (t in e) return !1;
                return !0
            },
            type: function(e) {
                return null == e ? e + "" : "object" == typeof e || "function" == typeof e ? Y[V.call(e)] || "object" : typeof e
            },
            globalEval: function(e) {
                var t, n = eval;
                e = Z.trim(e), e && (1 === e.indexOf("use strict") ? (t = J.createElement("script"), t.text = e, J.head.appendChild(t).parentNode.removeChild(t)) : n(e))
            },
            camelCase: function(e) {
                return e.replace(te, "ms-").replace(ne, re)
            },
            nodeName: function(e, t) {
                return e.nodeName && e.nodeName.toLowerCase() === t.toLowerCase()
            },
            each: function(e, t, r) {
                var i, o = 0,
                    s = e.length,
                    a = n(e);
                if (r) {
                    if (a)
                        for (; s > o && (i = t.apply(e[o], r), i !== !1); o++);
                    else
                        for (o in e)
                            if (i = t.apply(e[o], r), i === !1) break
                } else if (a)
                    for (; s > o && (i = t.call(e[o], o, e[o]), i !== !1); o++);
                else
                    for (o in e)
                        if (i = t.call(e[o], o, e[o]), i === !1) break;
                return e
            },
            trim: function(e) {
                return null == e ? "" : (e + "").replace(ee, "")
            },
            makeArray: function(e, t) {
                var r = t || [];
                return null != e && (n(Object(e)) ? Z.merge(r, "string" == typeof e ? [e] : e) : z.call(r, e)), r
            },
            inArray: function(e, t, n) {
                return null == t ? -1 : U.call(t, e, n)
            },
            merge: function(e, t) {
                for (var n = +t.length, r = 0, i = e.length; n > r; r++) e[i++] = t[r];
                return e.length = i, e
            },
            grep: function(e, t, n) {
                for (var r, i = [], o = 0, s = e.length, a = !n; s > o; o++) r = !t(e[o], o), r !== a && i.push(e[o]);
                return i
            },
            map: function(e, t, r) {
                var i, o = 0,
                    s = e.length,
                    a = n(e),
                    u = [];
                if (a)
                    for (; s > o; o++) i = t(e[o], o, r), null != i && u.push(i);
                else
                    for (o in e) i = t(e[o], o, r), null != i && u.push(i);
                return X.apply([], u)
            },
            guid: 1,
            proxy: function(e, t) {
                var n, r, i;
                return "string" == typeof t && (n = e[t], t = e, e = n), Z.isFunction(e) ? (r = _.call(arguments, 2), i = function() {
                    return e.apply(t || this, r.concat(_.call(arguments)))
                }, i.guid = e.guid = e.guid || Z.guid++, i) : void 0
            },
            now: Date.now,
            support: Q
        }), Z.each("Boolean Number String Function Array Date RegExp Object Error".split(" "), function(e, t) {
            Y["[object " + t + "]"] = t.toLowerCase()
        });
        var ie = function(e) {
            function t(e, t, n, r) {
                var i, o, s, a, u, l, f, d, h, g;
                if ((t ? t.ownerDocument || t : $) !== q && L(t), t = t || q, n = n || [], !e || "string" != typeof e) return n;
                if (1 !== (a = t.nodeType) && 9 !== a) return [];
                if (O && !r) {
                    if (i = ye.exec(e))
                        if (s = i[1]) {
                            if (9 === a) {
                                if (o = t.getElementById(s), !o || !o.parentNode) return n;
                                if (o.id === s) return n.push(o), n
                            } else if (t.ownerDocument && (o = t.ownerDocument.getElementById(s)) && R(t, o) && o.id === s) return n.push(o), n
                        } else {
                            if (i[2]) return Z.apply(n, t.getElementsByTagName(e)), n;
                            if ((s = i[3]) && w.getElementsByClassName && t.getElementsByClassName) return Z.apply(n, t.getElementsByClassName(s)), n
                        }
                    if (w.qsa && (!M || !M.test(e))) {
                        if (d = f = W, h = t, g = 9 === a && e, 1 === a && "object" !== t.nodeName.toLowerCase()) {
                            for (l = E(e), (f = t.getAttribute("id")) ? d = f.replace(be, "\\$&") : t.setAttribute("id", d), d = "[id='" + d + "'] ", u = l.length; u--;) l[u] = d + p(l[u]);
                            h = xe.test(e) && c(t.parentNode) || t, g = l.join(",")
                        }
                        if (g) try {
                            return Z.apply(n, h.querySelectorAll(g)), n
                        } catch (m) {} finally {
                            f || t.removeAttribute("id")
                        }
                    }
                }
                return S(e.replace(ue, "$1"), t, n, r)
            }

            function n() {
                function e(n, r) {
                    return t.push(n + " ") > T.cacheLength && delete e[t.shift()], e[n + " "] = r
                }
                var t = [];
                return e
            }

            function r(e) {
                return e[W] = !0, e
            }

            function i(e) {
                var t = q.createElement("div");
                try {
                    return !!e(t)
                } catch (n) {
                    return !1
                } finally {
                    t.parentNode && t.parentNode.removeChild(t), t = null
                }
            }

            function o(e, t) {
                for (var n = e.split("|"), r = e.length; r--;) T.attrHandle[n[r]] = t
            }

            function s(e, t) {
                var n = t && e,
                    r = n && 1 === e.nodeType && 1 === t.nodeType && (~t.sourceIndex || V) - (~e.sourceIndex || V);
                if (r) return r;
                if (n)
                    for (; n = n.nextSibling;)
                        if (n === t) return -1;
                return e ? 1 : -1
            }

            function a(e) {
                return function(t) {
                    var n = t.nodeName.toLowerCase();
                    return "input" === n && t.type === e
                }
            }

            function u(e) {
                return function(t) {
                    var n = t.nodeName.toLowerCase();
                    return ("input" === n || "button" === n) && t.type === e
                }
            }

            function l(e) {
                return r(function(t) {
                    return t = +t, r(function(n, r) {
                        for (var i, o = e([], n.length, t), s = o.length; s--;) n[i = o[s]] && (n[i] = !(r[i] = n[i]))
                    })
                })
            }

            function c(e) {
                return e && typeof e.getElementsByTagName !== Y && e
            }

            function f() {}

            function p(e) {
                for (var t = 0, n = e.length, r = ""; n > t; t++) r += e[t].value;
                return r
            }

            function d(e, t, n) {
                var r = t.dir,
                    i = n && "parentNode" === r,
                    o = B++;
                return t.first ? function(t, n, o) {
                    for (; t = t[r];)
                        if (1 === t.nodeType || i) return e(t, n, o)
                } : function(t, n, s) {
                    var a, u, l = [I, o];
                    if (s) {
                        for (; t = t[r];)
                            if ((1 === t.nodeType || i) && e(t, n, s)) return !0
                    } else
                        for (; t = t[r];)
                            if (1 === t.nodeType || i) {
                                if (u = t[W] || (t[W] = {}), (a = u[r]) && a[0] === I && a[1] === o) return l[2] = a[2];
                                if (u[r] = l, l[2] = e(t, n, s)) return !0
                            }
                }
            }

            function h(e) {
                return e.length > 1 ? function(t, n, r) {
                    for (var i = e.length; i--;)
                        if (!e[i](t, n, r)) return !1;
                    return !0
                } : e[0]
            }

            function g(e, n, r) {
                for (var i = 0, o = n.length; o > i; i++) t(e, n[i], r);
                return r
            }

            function m(e, t, n, r, i) {
                for (var o, s = [], a = 0, u = e.length, l = null != t; u > a; a++)(o = e[a]) && (!n || n(o, r, i)) && (s.push(o), l && t.push(a));
                return s
            }

            function v(e, t, n, i, o, s) {
                return i && !i[W] && (i = v(i)), o && !o[W] && (o = v(o, s)), r(function(r, s, a, u) {
                    var l, c, f, p = [],
                        d = [],
                        h = s.length,
                        v = r || g(t || "*", a.nodeType ? [a] : a, []),
                        y = !e || !r && t ? v : m(v, p, e, a, u),
                        x = n ? o || (r ? e : h || i) ? [] : s : y;
                    if (n && n(y, x, a, u), i)
                        for (l = m(x, d), i(l, [], a, u), c = l.length; c--;)(f = l[c]) && (x[d[c]] = !(y[d[c]] = f));
                    if (r) {
                        if (o || e) {
                            if (o) {
                                for (l = [], c = x.length; c--;)(f = x[c]) && l.push(y[c] = f);
                                o(null, x = [], l, u)
                            }
                            for (c = x.length; c--;)(f = x[c]) && (l = o ? te.call(r, f) : p[c]) > -1 && (r[l] = !(s[l] = f))
                        }
                    } else x = m(x === s ? x.splice(h, x.length) : x), o ? o(null, s, x, u) : Z.apply(s, x)
                })
            }

            function y(e) {
                for (var t, n, r, i = e.length, o = T.relative[e[0].type], s = o || T.relative[" "], a = o ? 1 : 0, u = d(function(e) {
                        return e === t
                    }, s, !0), l = d(function(e) {
                        return te.call(t, e) > -1
                    }, s, !0), c = [function(e, n, r) {
                        return !o && (r || n !== j) || ((t = n).nodeType ? u(e, n, r) : l(e, n, r))
                    }]; i > a; a++)
                    if (n = T.relative[e[a].type]) c = [d(h(c), n)];
                    else {
                        if (n = T.filter[e[a].type].apply(null, e[a].matches), n[W]) {
                            for (r = ++a; i > r && !T.relative[e[r].type]; r++);
                            return v(a > 1 && h(c), a > 1 && p(e.slice(0, a - 1).concat({
                                value: " " === e[a - 2].type ? "*" : ""
                            })).replace(ue, "$1"), n, r > a && y(e.slice(a, r)), i > r && y(e = e.slice(r)), i > r && p(e))
                        }
                        c.push(n)
                    }
                return h(c)
            }

            function x(e, n) {
                var i = n.length > 0,
                    o = e.length > 0,
                    s = function(r, s, a, u, l) {
                        var c, f, p, d = 0,
                            h = "0",
                            g = r && [],
                            v = [],
                            y = j,
                            x = r || o && T.find.TAG("*", l),
                            b = I += null == y ? 1 : Math.random() || .1,
                            w = x.length;
                        for (l && (j = s !== q && s); h !== w && null != (c = x[h]); h++) {
                            if (o && c) {
                                for (f = 0; p = e[f++];)
                                    if (p(c, s, a)) {
                                        u.push(c);
                                        break
                                    }
                                l && (I = b)
                            }
                            i && ((c = !p && c) && d--, r && g.push(c))
                        }
                        if (d += h, i && h !== d) {
                            for (f = 0; p = n[f++];) p(g, v, s, a);
                            if (r) {
                                if (d > 0)
                                    for (; h--;) g[h] || v[h] || (v[h] = J.call(u));
                                v = m(v)
                            }
                            Z.apply(u, v), l && !r && v.length > 0 && d + n.length > 1 && t.uniqueSort(u)
                        }
                        return l && (I = b, j = y), g
                    };
                return i ? r(s) : s
            }
            var b, w, T, C, N, E, k, S, j, D, A, L, q, H, O, M, F, P, R, W = "sizzle" + -new Date,
                $ = e.document,
                I = 0,
                B = 0,
                _ = n(),
                X = n(),
                z = n(),
                U = function(e, t) {
                    return e === t && (A = !0), 0
                },
                Y = "undefined",
                V = 1 << 31,
                G = {}.hasOwnProperty,
                Q = [],
                J = Q.pop,
                K = Q.push,
                Z = Q.push,
                ee = Q.slice,
                te = Q.indexOf || function(e) {
                    for (var t = 0, n = this.length; n > t; t++)
                        if (this[t] === e) return t;
                    return -1
                },
                ne = "checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",
                re = "[\\x20\\t\\r\\n\\f]",
                ie = "(?:\\\\.|[\\w-]|[^\\x00-\\xa0])+",
                oe = ie.replace("w", "w#"),
                se = "\\[" + re + "*(" + ie + ")(?:" + re + "*([*^$|!~]?=)" + re + "*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|(" + oe + "))|)" + re + "*\\]",
                ae = ":(" + ie + ")(?:\\((('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|((?:\\\\.|[^\\\\()[\\]]|" + se + ")*)|.*)\\)|)",
                ue = new RegExp("^" + re + "+|((?:^|[^\\\\])(?:\\\\.)*)" + re + "+$", "g"),
                le = new RegExp("^" + re + "*," + re + "*"),
                ce = new RegExp("^" + re + "*([>+~]|" + re + ")" + re + "*"),
                fe = new RegExp("=" + re + "*([^\\]'\"]*?)" + re + "*\\]", "g"),
                pe = new RegExp(ae),
                de = new RegExp("^" + oe + "$"),
                he = {
                    ID: new RegExp("^#(" + ie + ")"),
                    CLASS: new RegExp("^\\.(" + ie + ")"),
                    TAG: new RegExp("^(" + ie.replace("w", "w*") + ")"),
                    ATTR: new RegExp("^" + se),
                    PSEUDO: new RegExp("^" + ae),
                    CHILD: new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\(" + re + "*(even|odd|(([+-]|)(\\d*)n|)" + re + "*(?:([+-]|)" + re + "*(\\d+)|))" + re + "*\\)|)", "i"),
                    bool: new RegExp("^(?:" + ne + ")$", "i"),
                    needsContext: new RegExp("^" + re + "*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + re + "*((?:-\\d)?\\d*)" + re + "*\\)|)(?=[^-]|$)", "i")
                },
                ge = /^(?:input|select|textarea|button)$/i,
                me = /^h\d$/i,
                ve = /^[^{]+\{\s*\[native \w/,
                ye = /^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,
                xe = /[+~]/,
                be = /'|\\/g,
                we = new RegExp("\\\\([\\da-f]{1,6}" + re + "?|(" + re + ")|.)", "ig"),
                Te = function(e, t, n) {
                    var r = "0x" + t - 65536;
                    return r !== r || n ? t : 0 > r ? String.fromCharCode(r + 65536) : String.fromCharCode(r >> 10 | 55296, 1023 & r | 56320)
                };
            try {
                Z.apply(Q = ee.call($.childNodes), $.childNodes), Q[$.childNodes.length].nodeType
            } catch (Ce) {
                Z = {
                    apply: Q.length ? function(e, t) {
                        K.apply(e, ee.call(t))
                    } : function(e, t) {
                        for (var n = e.length, r = 0; e[n++] = t[r++];);
                        e.length = n - 1
                    }
                }
            }
            w = t.support = {}, N = t.isXML = function(e) {
                var t = e && (e.ownerDocument || e).documentElement;
                return t ? "HTML" !== t.nodeName : !1
            }, L = t.setDocument = function(e) {
                var t, n = e ? e.ownerDocument || e : $,
                    r = n.defaultView;
                return n !== q && 9 === n.nodeType && n.documentElement ? (q = n, H = n.documentElement, O = !N(n), r && r !== r.top && (r.addEventListener ? r.addEventListener("unload", function() {
                    L()
                }, !1) : r.attachEvent && r.attachEvent("onunload", function() {
                    L()
                })), w.attributes = i(function(e) {
                    return e.className = "i", !e.getAttribute("className")
                }), w.getElementsByTagName = i(function(e) {
                    return e.appendChild(n.createComment("")), !e.getElementsByTagName("*").length
                }), w.getElementsByClassName = ve.test(n.getElementsByClassName) && i(function(e) {
                    return e.innerHTML = "<div class='a'></div><div class='a i'></div>", e.firstChild.className = "i", 2 === e.getElementsByClassName("i").length
                }), w.getById = i(function(e) {
                    return H.appendChild(e).id = W, !n.getElementsByName || !n.getElementsByName(W).length
                }), w.getById ? (T.find.ID = function(e, t) {
                    if (typeof t.getElementById !== Y && O) {
                        var n = t.getElementById(e);
                        return n && n.parentNode ? [n] : []
                    }
                }, T.filter.ID = function(e) {
                    var t = e.replace(we, Te);
                    return function(e) {
                        return e.getAttribute("id") === t
                    }
                }) : (delete T.find.ID, T.filter.ID = function(e) {
                    var t = e.replace(we, Te);
                    return function(e) {
                        var n = typeof e.getAttributeNode !== Y && e.getAttributeNode("id");
                        return n && n.value === t
                    }
                }), T.find.TAG = w.getElementsByTagName ? function(e, t) {
                    return typeof t.getElementsByTagName !== Y ? t.getElementsByTagName(e) : void 0
                } : function(e, t) {
                    var n, r = [],
                        i = 0,
                        o = t.getElementsByTagName(e);
                    if ("*" === e) {
                        for (; n = o[i++];) 1 === n.nodeType && r.push(n);
                        return r
                    }
                    return o
                }, T.find.CLASS = w.getElementsByClassName && function(e, t) {
                    return typeof t.getElementsByClassName !== Y && O ? t.getElementsByClassName(e) : void 0
                }, F = [], M = [], (w.qsa = ve.test(n.querySelectorAll)) && (i(function(e) {
                    e.innerHTML = "<select msallowclip=''><option selected=''></option></select>", e.querySelectorAll("[msallowclip^='']").length && M.push("[*^$]=" + re + "*(?:''|\"\")"), e.querySelectorAll("[selected]").length || M.push("\\[" + re + "*(?:value|" + ne + ")"), e.querySelectorAll(":checked").length || M.push(":checked")
                }), i(function(e) {
                    var t = n.createElement("input");
                    t.setAttribute("type", "hidden"), e.appendChild(t).setAttribute("name", "D"), e.querySelectorAll("[name=d]").length && M.push("name" + re + "*[*^$|!~]?="), e.querySelectorAll(":enabled").length || M.push(":enabled", ":disabled"), e.querySelectorAll("*,:x"), M.push(",.*:")
                })), (w.matchesSelector = ve.test(P = H.matches || H.webkitMatchesSelector || H.mozMatchesSelector || H.oMatchesSelector || H.msMatchesSelector)) && i(function(e) {
                    w.disconnectedMatch = P.call(e, "div"), P.call(e, "[s!='']:x"), F.push("!=", ae)
                }), M = M.length && new RegExp(M.join("|")), F = F.length && new RegExp(F.join("|")), t = ve.test(H.compareDocumentPosition), R = t || ve.test(H.contains) ? function(e, t) {
                    var n = 9 === e.nodeType ? e.documentElement : e,
                        r = t && t.parentNode;
                    return e === r || !(!r || 1 !== r.nodeType || !(n.contains ? n.contains(r) : e.compareDocumentPosition && 16 & e.compareDocumentPosition(r)))
                } : function(e, t) {
                    if (t)
                        for (; t = t.parentNode;)
                            if (t === e) return !0;
                    return !1
                }, U = t ? function(e, t) {
                    if (e === t) return A = !0, 0;
                    var r = !e.compareDocumentPosition - !t.compareDocumentPosition;
                    return r ? r : (r = (e.ownerDocument || e) === (t.ownerDocument || t) ? e.compareDocumentPosition(t) : 1, 1 & r || !w.sortDetached && t.compareDocumentPosition(e) === r ? e === n || e.ownerDocument === $ && R($, e) ? -1 : t === n || t.ownerDocument === $ && R($, t) ? 1 : D ? te.call(D, e) - te.call(D, t) : 0 : 4 & r ? -1 : 1)
                } : function(e, t) {
                    if (e === t) return A = !0, 0;
                    var r, i = 0,
                        o = e.parentNode,
                        a = t.parentNode,
                        u = [e],
                        l = [t];
                    if (!o || !a) return e === n ? -1 : t === n ? 1 : o ? -1 : a ? 1 : D ? te.call(D, e) - te.call(D, t) : 0;
                    if (o === a) return s(e, t);
                    for (r = e; r = r.parentNode;) u.unshift(r);
                    for (r = t; r = r.parentNode;) l.unshift(r);
                    for (; u[i] === l[i];) i++;
                    return i ? s(u[i], l[i]) : u[i] === $ ? -1 : l[i] === $ ? 1 : 0
                }, n) : q
            }, t.matches = function(e, n) {
                return t(e, null, null, n)
            }, t.matchesSelector = function(e, n) {
                if ((e.ownerDocument || e) !== q && L(e), n = n.replace(fe, "='$1']"), w.matchesSelector && O && (!F || !F.test(n)) && (!M || !M.test(n))) try {
                    var r = P.call(e, n);
                    if (r || w.disconnectedMatch || e.document && 11 !== e.document.nodeType) return r
                } catch (i) {}
                return t(n, q, null, [e]).length > 0
            }, t.contains = function(e, t) {
                return (e.ownerDocument || e) !== q && L(e), R(e, t)
            }, t.attr = function(e, t) {
                (e.ownerDocument || e) !== q && L(e);
                var n = T.attrHandle[t.toLowerCase()],
                    r = n && G.call(T.attrHandle, t.toLowerCase()) ? n(e, t, !O) : void 0;
                return void 0 !== r ? r : w.attributes || !O ? e.getAttribute(t) : (r = e.getAttributeNode(t)) && r.specified ? r.value : null
            }, t.error = function(e) {
                throw new Error("Syntax error, unrecognized expression: " + e)
            }, t.uniqueSort = function(e) {
                var t, n = [],
                    r = 0,
                    i = 0;
                if (A = !w.detectDuplicates, D = !w.sortStable && e.slice(0), e.sort(U), A) {
                    for (; t = e[i++];) t === e[i] && (r = n.push(i));
                    for (; r--;) e.splice(n[r], 1)
                }
                return D = null, e
            }, C = t.getText = function(e) {
                var t, n = "",
                    r = 0,
                    i = e.nodeType;
                if (i) {
                    if (1 === i || 9 === i || 11 === i) {
                        if ("string" == typeof e.textContent) return e.textContent;
                        for (e = e.firstChild; e; e = e.nextSibling) n += C(e)
                    } else if (3 === i || 4 === i) return e.nodeValue
                } else
                    for (; t = e[r++];) n += C(t);
                return n
            }, T = t.selectors = {
                cacheLength: 50,
                createPseudo: r,
                match: he,
                attrHandle: {},
                find: {},
                relative: {
                    ">": {
                        dir: "parentNode",
                        first: !0
                    },
                    " ": {
                        dir: "parentNode"
                    },
                    "+": {
                        dir: "previousSibling",
                        first: !0
                    },
                    "~": {
                        dir: "previousSibling"
                    }
                },
                preFilter: {
                    ATTR: function(e) {
                        return e[1] = e[1].replace(we, Te), e[3] = (e[3] || e[4] || e[5] || "").replace(we, Te), "~=" === e[2] && (e[3] = " " + e[3] + " "), e.slice(0, 4)
                    },
                    CHILD: function(e) {
                        return e[1] = e[1].toLowerCase(), "nth" === e[1].slice(0, 3) ? (e[3] || t.error(e[0]), e[4] = +(e[4] ? e[5] + (e[6] || 1) : 2 * ("even" === e[3] || "odd" === e[3])), e[5] = +(e[7] + e[8] || "odd" === e[3])) : e[3] && t.error(e[0]), e
                    },
                    PSEUDO: function(e) {
                        var t, n = !e[6] && e[2];
                        return he.CHILD.test(e[0]) ? null : (e[3] ? e[2] = e[4] || e[5] || "" : n && pe.test(n) && (t = E(n, !0)) && (t = n.indexOf(")", n.length - t) - n.length) && (e[0] = e[0].slice(0, t), e[2] = n.slice(0, t)), e.slice(0, 3))
                    }
                },
                filter: {
                    TAG: function(e) {
                        var t = e.replace(we, Te).toLowerCase();
                        return "*" === e ? function() {
                            return !0
                        } : function(e) {
                            return e.nodeName && e.nodeName.toLowerCase() === t
                        }
                    },
                    CLASS: function(e) {
                        var t = _[e + " "];
                        return t || (t = new RegExp("(^|" + re + ")" + e + "(" + re + "|$)")) && _(e, function(e) {
                            return t.test("string" == typeof e.className && e.className || typeof e.getAttribute !== Y && e.getAttribute("class") || "")
                        })
                    },
                    ATTR: function(e, n, r) {
                        return function(i) {
                            var o = t.attr(i, e);
                            return null == o ? "!=" === n : n ? (o += "", "=" === n ? o === r : "!=" === n ? o !== r : "^=" === n ? r && 0 === o.indexOf(r) : "*=" === n ? r && o.indexOf(r) > -1 : "$=" === n ? r && o.slice(-r.length) === r : "~=" === n ? (" " + o + " ").indexOf(r) > -1 : "|=" === n ? o === r || o.slice(0, r.length + 1) === r + "-" : !1) : !0
                        }
                    },
                    CHILD: function(e, t, n, r, i) {
                        var o = "nth" !== e.slice(0, 3),
                            s = "last" !== e.slice(-4),
                            a = "of-type" === t;
                        return 1 === r && 0 === i ? function(e) {
                            return !!e.parentNode
                        } : function(t, n, u) {
                            var l, c, f, p, d, h, g = o !== s ? "nextSibling" : "previousSibling",
                                m = t.parentNode,
                                v = a && t.nodeName.toLowerCase(),
                                y = !u && !a;
                            if (m) {
                                if (o) {
                                    for (; g;) {
                                        for (f = t; f = f[g];)
                                            if (a ? f.nodeName.toLowerCase() === v : 1 === f.nodeType) return !1;
                                        h = g = "only" === e && !h && "nextSibling"
                                    }
                                    return !0
                                }
                                if (h = [s ? m.firstChild : m.lastChild], s && y) {
                                    for (c = m[W] || (m[W] = {}), l = c[e] || [], d = l[0] === I && l[1], p = l[0] === I && l[2], f = d && m.childNodes[d]; f = ++d && f && f[g] || (p = d = 0) || h.pop();)
                                        if (1 === f.nodeType && ++p && f === t) {
                                            c[e] = [I, d, p];
                                            break
                                        }
                                } else if (y && (l = (t[W] || (t[W] = {}))[e]) && l[0] === I) p = l[1];
                                else
                                    for (;
                                        (f = ++d && f && f[g] || (p = d = 0) || h.pop()) && ((a ? f.nodeName.toLowerCase() !== v : 1 !== f.nodeType) || !++p || (y && ((f[W] || (f[W] = {}))[e] = [I, p]), f !== t)););
                                return p -= i, p === r || p % r === 0 && p / r >= 0
                            }
                        }
                    },
                    PSEUDO: function(e, n) {
                        var i, o = T.pseudos[e] || T.setFilters[e.toLowerCase()] || t.error("unsupported pseudo: " + e);
                        return o[W] ? o(n) : o.length > 1 ? (i = [e, e, "", n], T.setFilters.hasOwnProperty(e.toLowerCase()) ? r(function(e, t) {
                            for (var r, i = o(e, n), s = i.length; s--;) r = te.call(e, i[s]), e[r] = !(t[r] = i[s])
                        }) : function(e) {
                            return o(e, 0, i)
                        }) : o
                    }
                },
                pseudos: {
                    not: r(function(e) {
                        var t = [],
                            n = [],
                            i = k(e.replace(ue, "$1"));
                        return i[W] ? r(function(e, t, n, r) {
                            for (var o, s = i(e, null, r, []), a = e.length; a--;)(o = s[a]) && (e[a] = !(t[a] = o))
                        }) : function(e, r, o) {
                            return t[0] = e, i(t, null, o, n), !n.pop()
                        }
                    }),
                    has: r(function(e) {
                        return function(n) {
                            return t(e, n).length > 0
                        }
                    }),
                    contains: r(function(e) {
                        return function(t) {
                            return (t.textContent || t.innerText || C(t)).indexOf(e) > -1
                        }
                    }),
                    lang: r(function(e) {
                        return de.test(e || "") || t.error("unsupported lang: " + e), e = e.replace(we, Te).toLowerCase(),
                            function(t) {
                                var n;
                                do
                                    if (n = O ? t.lang : t.getAttribute("xml:lang") || t.getAttribute("lang")) return n = n.toLowerCase(), n === e || 0 === n.indexOf(e + "-"); while ((t = t.parentNode) && 1 === t.nodeType);
                                return !1
                            }
                    }),
                    target: function(t) {
                        var n = e.location && e.location.hash;
                        return n && n.slice(1) === t.id
                    },
                    root: function(e) {
                        return e === H
                    },
                    focus: function(e) {
                        return e === q.activeElement && (!q.hasFocus || q.hasFocus()) && !!(e.type || e.href || ~e.tabIndex)
                    },
                    enabled: function(e) {
                        return e.disabled === !1
                    },
                    disabled: function(e) {
                        return e.disabled === !0
                    },
                    checked: function(e) {
                        var t = e.nodeName.toLowerCase();
                        return "input" === t && !!e.checked || "option" === t && !!e.selected
                    },
                    selected: function(e) {
                        return e.parentNode && e.parentNode.selectedIndex, e.selected === !0
                    },
                    empty: function(e) {
                        for (e = e.firstChild; e; e = e.nextSibling)
                            if (e.nodeType < 6) return !1;
                        return !0
                    },
                    parent: function(e) {
                        return !T.pseudos.empty(e)
                    },
                    header: function(e) {
                        return me.test(e.nodeName)
                    },
                    input: function(e) {
                        return ge.test(e.nodeName)
                    },
                    button: function(e) {
                        var t = e.nodeName.toLowerCase();
                        return "input" === t && "button" === e.type || "button" === t
                    },
                    text: function(e) {
                        var t;
                        return "input" === e.nodeName.toLowerCase() && "text" === e.type && (null == (t = e.getAttribute("type")) || "text" === t.toLowerCase())
                    },
                    first: l(function() {
                        return [0]
                    }),
                    last: l(function(e, t) {
                        return [t - 1]
                    }),
                    eq: l(function(e, t, n) {
                        return [0 > n ? n + t : n]
                    }),
                    even: l(function(e, t) {
                        for (var n = 0; t > n; n += 2) e.push(n);
                        return e
                    }),
                    odd: l(function(e, t) {
                        for (var n = 1; t > n; n += 2) e.push(n);
                        return e
                    }),
                    lt: l(function(e, t, n) {
                        for (var r = 0 > n ? n + t : n; --r >= 0;) e.push(r);
                        return e
                    }),
                    gt: l(function(e, t, n) {
                        for (var r = 0 > n ? n + t : n; ++r < t;) e.push(r);
                        return e
                    })
                }
            }, T.pseudos.nth = T.pseudos.eq;
            for (b in {
                    radio: !0,
                    checkbox: !0,
                    file: !0,
                    password: !0,
                    image: !0
                }) T.pseudos[b] = a(b);
            for (b in {
                    submit: !0,
                    reset: !0
                }) T.pseudos[b] = u(b);
            return f.prototype = T.filters = T.pseudos, T.setFilters = new f, E = t.tokenize = function(e, n) {
                var r, i, o, s, a, u, l, c = X[e + " "];
                if (c) return n ? 0 : c.slice(0);
                for (a = e, u = [], l = T.preFilter; a;) {
                    (!r || (i = le.exec(a))) && (i && (a = a.slice(i[0].length) || a), u.push(o = [])), r = !1, (i = ce.exec(a)) && (r = i.shift(), o.push({
                        value: r,
                        type: i[0].replace(ue, " ")
                    }), a = a.slice(r.length));
                    for (s in T.filter) !(i = he[s].exec(a)) || l[s] && !(i = l[s](i)) || (r = i.shift(), o.push({
                        value: r,
                        type: s,
                        matches: i
                    }), a = a.slice(r.length));
                    if (!r) break
                }
                return n ? a.length : a ? t.error(e) : X(e, u).slice(0)
            }, k = t.compile = function(e, t) {
                var n, r = [],
                    i = [],
                    o = z[e + " "];
                if (!o) {
                    for (t || (t = E(e)), n = t.length; n--;) o = y(t[n]), o[W] ? r.push(o) : i.push(o);
                    o = z(e, x(i, r)), o.selector = e
                }
                return o
            }, S = t.select = function(e, t, n, r) {
                var i, o, s, a, u, l = "function" == typeof e && e,
                    f = !r && E(e = l.selector || e);
                if (n = n || [], 1 === f.length) {
                    if (o = f[0] = f[0].slice(0), o.length > 2 && "ID" === (s = o[0]).type && w.getById && 9 === t.nodeType && O && T.relative[o[1].type]) {
                        if (t = (T.find.ID(s.matches[0].replace(we, Te), t) || [])[0], !t) return n;
                        l && (t = t.parentNode), e = e.slice(o.shift().value.length)
                    }
                    for (i = he.needsContext.test(e) ? 0 : o.length; i-- && (s = o[i], !T.relative[a = s.type]);)
                        if ((u = T.find[a]) && (r = u(s.matches[0].replace(we, Te), xe.test(o[0].type) && c(t.parentNode) || t))) {
                            if (o.splice(i, 1), e = r.length && p(o), !e) return Z.apply(n, r), n;
                            break
                        }
                }
                return (l || k(e, f))(r, t, !O, n, xe.test(e) && c(t.parentNode) || t), n
            }, w.sortStable = W.split("").sort(U).join("") === W, w.detectDuplicates = !!A, L(), w.sortDetached = i(function(e) {
                return 1 & e.compareDocumentPosition(q.createElement("div"))
            }), i(function(e) {
                return e.innerHTML = "<a href='#'></a>", "#" === e.firstChild.getAttribute("href")
            }) || o("type|href|height|width", function(e, t, n) {
                return n ? void 0 : e.getAttribute(t, "type" === t.toLowerCase() ? 1 : 2)
            }), w.attributes && i(function(e) {
                return e.innerHTML = "<input/>", e.firstChild.setAttribute("value", ""), "" === e.firstChild.getAttribute("value")
            }) || o("value", function(e, t, n) {
                return n || "input" !== e.nodeName.toLowerCase() ? void 0 : e.defaultValue
            }), i(function(e) {
                return null == e.getAttribute("disabled")
            }) || o(ne, function(e, t, n) {
                var r;
                return n ? void 0 : e[t] === !0 ? t.toLowerCase() : (r = e.getAttributeNode(t)) && r.specified ? r.value : null
            }), t
        }(e);
        Z.find = ie, Z.expr = ie.selectors, Z.expr[":"] = Z.expr.pseudos, Z.unique = ie.uniqueSort, Z.text = ie.getText, Z.isXMLDoc = ie.isXML, Z.contains = ie.contains;
        var oe = Z.expr.match.needsContext,
            se = /^<(\w+)\s*\/?>(?:<\/\1>|)$/,
            ae = /^.[^:#\[\.,]*$/;
        Z.filter = function(e, t, n) {
            var r = t[0];
            return n && (e = ":not(" + e + ")"), 1 === t.length && 1 === r.nodeType ? Z.find.matchesSelector(r, e) ? [r] : [] : Z.find.matches(e, Z.grep(t, function(e) {
                return 1 === e.nodeType
            }))
        }, Z.fn.extend({
            find: function(e) {
                var t, n = this.length,
                    r = [],
                    i = this;
                if ("string" != typeof e) return this.pushStack(Z(e).filter(function() {
                    for (t = 0; n > t; t++)
                        if (Z.contains(i[t], this)) return !0
                }));
                for (t = 0; n > t; t++) Z.find(e, i[t], r);
                return r = this.pushStack(n > 1 ? Z.unique(r) : r), r.selector = this.selector ? this.selector + " " + e : e, r
            },
            filter: function(e) {
                return this.pushStack(r(this, e || [], !1))
            },
            not: function(e) {
                return this.pushStack(r(this, e || [], !0))
            },
            is: function(e) {
                return !!r(this, "string" == typeof e && oe.test(e) ? Z(e) : e || [], !1).length
            }
        });
        var ue, le = /^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]*))$/,
            ce = Z.fn.init = function(e, t) {
                var n, r;
                if (!e) return this;
                if ("string" == typeof e) {
                    if (n = "<" === e[0] && ">" === e[e.length - 1] && e.length >= 3 ? [null, e, null] : le.exec(e), !n || !n[1] && t) return !t || t.jquery ? (t || ue).find(e) : this.constructor(t).find(e);
                    if (n[1]) {
                        if (t = t instanceof Z ? t[0] : t, Z.merge(this, Z.parseHTML(n[1], t && t.nodeType ? t.ownerDocument || t : J, !0)), se.test(n[1]) && Z.isPlainObject(t))
                            for (n in t) Z.isFunction(this[n]) ? this[n](t[n]) : this.attr(n, t[n]);
                        return this
                    }
                    return r = J.getElementById(n[2]), r && r.parentNode && (this.length = 1, this[0] = r), this.context = J, this.selector = e, this
                }
                return e.nodeType ? (this.context = this[0] = e, this.length = 1, this) : Z.isFunction(e) ? "undefined" != typeof ue.ready ? ue.ready(e) : e(Z) : (void 0 !== e.selector && (this.selector = e.selector, this.context = e.context), Z.makeArray(e, this))
            };
        ce.prototype = Z.fn, ue = Z(J);
        var fe = /^(?:parents|prev(?:Until|All))/,
            pe = {
                children: !0,
                contents: !0,
                next: !0,
                prev: !0
            };
        Z.extend({
            dir: function(e, t, n) {
                for (var r = [], i = void 0 !== n;
                    (e = e[t]) && 9 !== e.nodeType;)
                    if (1 === e.nodeType) {
                        if (i && Z(e).is(n)) break;
                        r.push(e)
                    }
                return r
            },
            sibling: function(e, t) {
                for (var n = []; e; e = e.nextSibling) 1 === e.nodeType && e !== t && n.push(e);
                return n
            }
        }), Z.fn.extend({
            has: function(e) {
                var t = Z(e, this),
                    n = t.length;
                return this.filter(function() {
                    for (var e = 0; n > e; e++)
                        if (Z.contains(this, t[e])) return !0
                })
            },
            closest: function(e, t) {
                for (var n, r = 0, i = this.length, o = [], s = oe.test(e) || "string" != typeof e ? Z(e, t || this.context) : 0; i > r; r++)
                    for (n = this[r]; n && n !== t; n = n.parentNode)
                        if (n.nodeType < 11 && (s ? s.index(n) > -1 : 1 === n.nodeType && Z.find.matchesSelector(n, e))) {
                            o.push(n);
                            break
                        }
                return this.pushStack(o.length > 1 ? Z.unique(o) : o)
            },
            index: function(e) {
                return e ? "string" == typeof e ? U.call(Z(e), this[0]) : U.call(this, e.jquery ? e[0] : e) : this[0] && this[0].parentNode ? this.first().prevAll().length : -1
            },
            add: function(e, t) {
                return this.pushStack(Z.unique(Z.merge(this.get(), Z(e, t))))
            },
            addBack: function(e) {
                return this.add(null == e ? this.prevObject : this.prevObject.filter(e))
            }
        }), Z.each({
            parent: function(e) {
                var t = e.parentNode;
                return t && 11 !== t.nodeType ? t : null
            },
            parents: function(e) {
                return Z.dir(e, "parentNode")
            },
            parentsUntil: function(e, t, n) {
                return Z.dir(e, "parentNode", n)
            },
            next: function(e) {
                return i(e, "nextSibling")
            },
            prev: function(e) {
                return i(e, "previousSibling")
            },
            nextAll: function(e) {
                return Z.dir(e, "nextSibling")
            },
            prevAll: function(e) {
                return Z.dir(e, "previousSibling")
            },
            nextUntil: function(e, t, n) {
                return Z.dir(e, "nextSibling", n)
            },
            prevUntil: function(e, t, n) {
                return Z.dir(e, "previousSibling", n)
            },
            siblings: function(e) {
                return Z.sibling((e.parentNode || {}).firstChild, e)
            },
            children: function(e) {
                return Z.sibling(e.firstChild)
            },
            contents: function(e) {
                return e.contentDocument || Z.merge([], e.childNodes)
            }
        }, function(e, t) {
            Z.fn[e] = function(n, r) {
                var i = Z.map(this, t, n);
                return "Until" !== e.slice(-5) && (r = n), r && "string" == typeof r && (i = Z.filter(r, i)), this.length > 1 && (pe[e] || Z.unique(i), fe.test(e) && i.reverse()), this.pushStack(i)
            }
        });
        var de = /\S+/g,
            he = {};
        Z.Callbacks = function(e) {
            e = "string" == typeof e ? he[e] || o(e) : Z.extend({}, e);
            var t, n, r, i, s, a, u = [],
                l = !e.once && [],
                c = function(o) {
                    for (t = e.memory && o, n = !0, a = i || 0, i = 0, s = u.length, r = !0; u && s > a; a++)
                        if (u[a].apply(o[0], o[1]) === !1 && e.stopOnFalse) {
                            t = !1;
                            break
                        }
                    r = !1, u && (l ? l.length && c(l.shift()) : t ? u = [] : f.disable())
                },
                f = {
                    add: function() {
                        if (u) {
                            var n = u.length;
                            ! function o(t) {
                                Z.each(t, function(t, n) {
                                    var r = Z.type(n);
                                    "function" === r ? e.unique && f.has(n) || u.push(n) : n && n.length && "string" !== r && o(n)
                                })
                            }(arguments), r ? s = u.length : t && (i = n, c(t))
                        }
                        return this
                    },
                    remove: function() {
                        return u && Z.each(arguments, function(e, t) {
                            for (var n;
                                (n = Z.inArray(t, u, n)) > -1;) u.splice(n, 1), r && (s >= n && s--, a >= n && a--)
                        }), this
                    },
                    has: function(e) {
                        return e ? Z.inArray(e, u) > -1 : !(!u || !u.length)
                    },
                    empty: function() {
                        return u = [], s = 0, this
                    },
                    disable: function() {
                        return u = l = t = void 0, this
                    },
                    disabled: function() {
                        return !u
                    },
                    lock: function() {
                        return l = void 0, t || f.disable(), this
                    },
                    locked: function() {
                        return !l
                    },
                    fireWith: function(e, t) {
                        return !u || n && !l || (t = t || [], t = [e, t.slice ? t.slice() : t], r ? l.push(t) : c(t)), this
                    },
                    fire: function() {
                        return f.fireWith(this, arguments), this
                    },
                    fired: function() {
                        return !!n
                    }
                };
            return f
        }, Z.extend({
            Deferred: function(e) {
                var t = [
                        ["resolve", "done", Z.Callbacks("once memory"), "resolved"],
                        ["reject", "fail", Z.Callbacks("once memory"), "rejected"],
                        ["notify", "progress", Z.Callbacks("memory")]
                    ],
                    n = "pending",
                    r = {
                        state: function() {
                            return n
                        },
                        always: function() {
                            return i.done(arguments).fail(arguments), this
                        },
                        then: function() {
                            var e = arguments;
                            return Z.Deferred(function(n) {
                                Z.each(t, function(t, o) {
                                    var s = Z.isFunction(e[t]) && e[t];
                                    i[o[1]](function() {
                                        var e = s && s.apply(this, arguments);
                                        e && Z.isFunction(e.promise) ? e.promise().done(n.resolve).fail(n.reject).progress(n.notify) : n[o[0] + "With"](this === r ? n.promise() : this, s ? [e] : arguments)
                                    })
                                }), e = null
                            }).promise()
                        },
                        promise: function(e) {
                            return null != e ? Z.extend(e, r) : r
                        }
                    },
                    i = {};
                return r.pipe = r.then, Z.each(t, function(e, o) {
                    var s = o[2],
                        a = o[3];
                    r[o[1]] = s.add, a && s.add(function() {
                        n = a
                    }, t[1 ^ e][2].disable, t[2][2].lock), i[o[0]] = function() {
                        return i[o[0] + "With"](this === i ? r : this, arguments), this
                    }, i[o[0] + "With"] = s.fireWith
                }), r.promise(i), e && e.call(i, i), i
            },
            when: function(e) {
                var t, n, r, i = 0,
                    o = _.call(arguments),
                    s = o.length,
                    a = 1 !== s || e && Z.isFunction(e.promise) ? s : 0,
                    u = 1 === a ? e : Z.Deferred(),
                    l = function(e, n, r) {
                        return function(i) {
                            n[e] = this, r[e] = arguments.length > 1 ? _.call(arguments) : i, r === t ? u.notifyWith(n, r) : --a || u.resolveWith(n, r)
                        }
                    };
                if (s > 1)
                    for (t = new Array(s), n = new Array(s), r = new Array(s); s > i; i++) o[i] && Z.isFunction(o[i].promise) ? o[i].promise().done(l(i, r, o)).fail(u.reject).progress(l(i, n, t)) : --a;
                return a || u.resolveWith(r, o), u.promise()
            }
        });
        var ge;
        Z.fn.ready = function(e) {
            return Z.ready.promise().done(e), this
        }, Z.extend({
            isReady: !1,
            readyWait: 1,
            holdReady: function(e) {
                e ? Z.readyWait++ : Z.ready(!0)
            },
            ready: function(e) {
                (e === !0 ? --Z.readyWait : Z.isReady) || (Z.isReady = !0, e !== !0 && --Z.readyWait > 0 || (ge.resolveWith(J, [Z]), Z.fn.triggerHandler && (Z(J).triggerHandler("ready"), Z(J).off("ready"))))
            }
        }), Z.ready.promise = function(t) {
            return ge || (ge = Z.Deferred(), "complete" === J.readyState ? setTimeout(Z.ready) : (J.addEventListener("DOMContentLoaded", s, !1), e.addEventListener("load", s, !1))), ge.promise(t)
        }, Z.ready.promise();
        var me = Z.access = function(e, t, n, r, i, o, s) {
            var a = 0,
                u = e.length,
                l = null == n;
            if ("object" === Z.type(n)) {
                i = !0;
                for (a in n) Z.access(e, t, a, n[a], !0, o, s)
            } else if (void 0 !== r && (i = !0, Z.isFunction(r) || (s = !0), l && (s ? (t.call(e, r), t = null) : (l = t, t = function(e, t, n) {
                    return l.call(Z(e), n)
                })), t))
                for (; u > a; a++) t(e[a], n, s ? r : r.call(e[a], a, t(e[a], n)));
            return i ? e : l ? t.call(e) : u ? t(e[0], n) : o
        };
        Z.acceptData = function(e) {
            return 1 === e.nodeType || 9 === e.nodeType || !+e.nodeType
        }, a.uid = 1, a.accepts = Z.acceptData, a.prototype = {
            key: function(e) {
                if (!a.accepts(e)) return 0;
                var t = {},
                    n = e[this.expando];
                if (!n) {
                    n = a.uid++;
                    try {
                        t[this.expando] = {
                            value: n
                        }, Object.defineProperties(e, t)
                    } catch (r) {
                        t[this.expando] = n, Z.extend(e, t)
                    }
                }
                return this.cache[n] || (this.cache[n] = {}), n
            },
            set: function(e, t, n) {
                var r, i = this.key(e),
                    o = this.cache[i];
                if ("string" == typeof t) o[t] = n;
                else if (Z.isEmptyObject(o)) Z.extend(this.cache[i], t);
                else
                    for (r in t) o[r] = t[r];
                return o
            },
            get: function(e, t) {
                var n = this.cache[this.key(e)];
                return void 0 === t ? n : n[t]
            },
            access: function(e, t, n) {
                var r;
                return void 0 === t || t && "string" == typeof t && void 0 === n ? (r = this.get(e, t), void 0 !== r ? r : this.get(e, Z.camelCase(t))) : (this.set(e, t, n), void 0 !== n ? n : t)
            },
            remove: function(e, t) {
                var n, r, i, o = this.key(e),
                    s = this.cache[o];
                if (void 0 === t) this.cache[o] = {};
                else {
                    Z.isArray(t) ? r = t.concat(t.map(Z.camelCase)) : (i = Z.camelCase(t), t in s ? r = [t, i] : (r = i, r = r in s ? [r] : r.match(de) || [])), n = r.length;
                    for (; n--;) delete s[r[n]]
                }
            },
            hasData: function(e) {
                return !Z.isEmptyObject(this.cache[e[this.expando]] || {})
            },
            discard: function(e) {
                e[this.expando] && delete this.cache[e[this.expando]]
            }
        };
        var ve = new a,
            ye = new a,
            xe = /^(?:\{[\w\W]*\}|\[[\w\W]*\])$/,
            be = /([A-Z])/g;
        Z.extend({
            hasData: function(e) {
                return ye.hasData(e) || ve.hasData(e)
            },
            data: function(e, t, n) {
                return ye.access(e, t, n)
            },
            removeData: function(e, t) {
                ye.remove(e, t)
            },
            _data: function(e, t, n) {
                return ve.access(e, t, n)
            },
            _removeData: function(e, t) {
                ve.remove(e, t)
            }
        }), Z.fn.extend({
            data: function(e, t) {
                var n, r, i, o = this[0],
                    s = o && o.attributes;
                if (void 0 === e) {
                    if (this.length && (i = ye.get(o), 1 === o.nodeType && !ve.get(o, "hasDataAttrs"))) {
                        for (n = s.length; n--;) s[n] && (r = s[n].name, 0 === r.indexOf("data-") && (r = Z.camelCase(r.slice(5)), u(o, r, i[r])));
                        ve.set(o, "hasDataAttrs", !0)
                    }
                    return i
                }
                return "object" == typeof e ? this.each(function() {
                    ye.set(this, e)
                }) : me(this, function(t) {
                    var n, r = Z.camelCase(e);
                    if (o && void 0 === t) {
                        if (n = ye.get(o, e), void 0 !== n) return n;
                        if (n = ye.get(o, r), void 0 !== n) return n;
                        if (n = u(o, r, void 0), void 0 !== n) return n
                    } else this.each(function() {
                        var n = ye.get(this, r);
                        ye.set(this, r, t), -1 !== e.indexOf("-") && void 0 !== n && ye.set(this, e, t)
                    })
                }, null, t, arguments.length > 1, null, !0)
            },
            removeData: function(e) {
                return this.each(function() {
                    ye.remove(this, e)
                })
            }
        }), Z.extend({
            queue: function(e, t, n) {
                var r;
                return e ? (t = (t || "fx") + "queue", r = ve.get(e, t), n && (!r || Z.isArray(n) ? r = ve.access(e, t, Z.makeArray(n)) : r.push(n)), r || []) : void 0
            },
            dequeue: function(e, t) {
                t = t || "fx";
                var n = Z.queue(e, t),
                    r = n.length,
                    i = n.shift(),
                    o = Z._queueHooks(e, t),
                    s = function() {
                        Z.dequeue(e, t)
                    };
                "inprogress" === i && (i = n.shift(), r--), i && ("fx" === t && n.unshift("inprogress"), delete o.stop, i.call(e, s, o)), !r && o && o.empty.fire()
            },
            _queueHooks: function(e, t) {
                var n = t + "queueHooks";
                return ve.get(e, n) || ve.access(e, n, {
                    empty: Z.Callbacks("once memory").add(function() {
                        ve.remove(e, [t + "queue", n])
                    })
                })
            }
        }), Z.fn.extend({
            queue: function(e, t) {
                var n = 2;
                return "string" != typeof e && (t = e, e = "fx", n--), arguments.length < n ? Z.queue(this[0], e) : void 0 === t ? this : this.each(function() {
                    var n = Z.queue(this, e, t);
                    Z._queueHooks(this, e), "fx" === e && "inprogress" !== n[0] && Z.dequeue(this, e)
                })
            },
            dequeue: function(e) {
                return this.each(function() {
                    Z.dequeue(this, e)
                })
            },
            clearQueue: function(e) {
                return this.queue(e || "fx", [])
            },
            promise: function(e, t) {
                var n, r = 1,
                    i = Z.Deferred(),
                    o = this,
                    s = this.length,
                    a = function() {
                        --r || i.resolveWith(o, [o])
                    };
                for ("string" != typeof e && (t = e, e = void 0), e = e || "fx"; s--;) n = ve.get(o[s], e + "queueHooks"), n && n.empty && (r++, n.empty.add(a));
                return a(), i.promise(t)
            }
        });
        var we = /[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source,
            Te = ["Top", "Right", "Bottom", "Left"],
            Ce = function(e, t) {
                return e = t || e, "none" === Z.css(e, "display") || !Z.contains(e.ownerDocument, e)
            },
            Ne = /^(?:checkbox|radio)$/i;
        ! function() {
            var e = J.createDocumentFragment(),
                t = e.appendChild(J.createElement("div")),
                n = J.createElement("input");
            n.setAttribute("type", "radio"), n.setAttribute("checked", "checked"), n.setAttribute("name", "t"), t.appendChild(n), Q.checkClone = t.cloneNode(!0).cloneNode(!0).lastChild.checked, t.innerHTML = "<textarea>x</textarea>", Q.noCloneChecked = !!t.cloneNode(!0).lastChild.defaultValue
        }();
        var Ee = "undefined";
        Q.focusinBubbles = "onfocusin" in e;
        var ke = /^key/,
            Se = /^(?:mouse|pointer|contextmenu)|click/,
            je = /^(?:focusinfocus|focusoutblur)$/,
            De = /^([^.]*)(?:\.(.+)|)$/;
        Z.event = {
            global: {},
            add: function(e, t, n, r, i) {
                var o, s, a, u, l, c, f, p, d, h, g, m = ve.get(e);
                if (m)
                    for (n.handler && (o = n, n = o.handler, i = o.selector), n.guid || (n.guid = Z.guid++), (u = m.events) || (u = m.events = {}), (s = m.handle) || (s = m.handle = function(t) {
                            return typeof Z !== Ee && Z.event.triggered !== t.type ? Z.event.dispatch.apply(e, arguments) : void 0
                        }), t = (t || "").match(de) || [""], l = t.length; l--;) a = De.exec(t[l]) || [], d = g = a[1], h = (a[2] || "").split(".").sort(), d && (f = Z.event.special[d] || {}, d = (i ? f.delegateType : f.bindType) || d, f = Z.event.special[d] || {}, c = Z.extend({
                        type: d,
                        origType: g,
                        data: r,
                        handler: n,
                        guid: n.guid,
                        selector: i,
                        needsContext: i && Z.expr.match.needsContext.test(i),
                        namespace: h.join(".")
                    }, o), (p = u[d]) || (p = u[d] = [], p.delegateCount = 0, f.setup && f.setup.call(e, r, h, s) !== !1 || e.addEventListener && e.addEventListener(d, s, !1)), f.add && (f.add.call(e, c), c.handler.guid || (c.handler.guid = n.guid)), i ? p.splice(p.delegateCount++, 0, c) : p.push(c), Z.event.global[d] = !0)
            },
            remove: function(e, t, n, r, i) {
                var o, s, a, u, l, c, f, p, d, h, g, m = ve.hasData(e) && ve.get(e);
                if (m && (u = m.events)) {
                    for (t = (t || "").match(de) || [""], l = t.length; l--;)
                        if (a = De.exec(t[l]) || [], d = g = a[1], h = (a[2] || "").split(".").sort(), d) {
                            for (f = Z.event.special[d] || {}, d = (r ? f.delegateType : f.bindType) || d, p = u[d] || [], a = a[2] && new RegExp("(^|\\.)" + h.join("\\.(?:.*\\.|)") + "(\\.|$)"), s = o = p.length; o--;) c = p[o], !i && g !== c.origType || n && n.guid !== c.guid || a && !a.test(c.namespace) || r && r !== c.selector && ("**" !== r || !c.selector) || (p.splice(o, 1), c.selector && p.delegateCount--, f.remove && f.remove.call(e, c));
                            s && !p.length && (f.teardown && f.teardown.call(e, h, m.handle) !== !1 || Z.removeEvent(e, d, m.handle), delete u[d])
                        } else
                            for (d in u) Z.event.remove(e, d + t[l], n, r, !0);
                    Z.isEmptyObject(u) && (delete m.handle, ve.remove(e, "events"))
                }
            },
            trigger: function(t, n, r, i) {
                var o, s, a, u, l, c, f, p = [r || J],
                    d = G.call(t, "type") ? t.type : t,
                    h = G.call(t, "namespace") ? t.namespace.split(".") : [];
                if (s = a = r = r || J, 3 !== r.nodeType && 8 !== r.nodeType && !je.test(d + Z.event.triggered) && (d.indexOf(".") >= 0 && (h = d.split("."), d = h.shift(), h.sort()), l = d.indexOf(":") < 0 && "on" + d, t = t[Z.expando] ? t : new Z.Event(d, "object" == typeof t && t), t.isTrigger = i ? 2 : 3, t.namespace = h.join("."), t.namespace_re = t.namespace ? new RegExp("(^|\\.)" + h.join("\\.(?:.*\\.|)") + "(\\.|$)") : null, t.result = void 0, t.target || (t.target = r), n = null == n ? [t] : Z.makeArray(n, [t]), f = Z.event.special[d] || {}, i || !f.trigger || f.trigger.apply(r, n) !== !1)) {
                    if (!i && !f.noBubble && !Z.isWindow(r)) {
                        for (u = f.delegateType || d, je.test(u + d) || (s = s.parentNode); s; s = s.parentNode) p.push(s), a = s;
                        a === (r.ownerDocument || J) && p.push(a.defaultView || a.parentWindow || e)
                    }
                    for (o = 0;
                        (s = p[o++]) && !t.isPropagationStopped();) t.type = o > 1 ? u : f.bindType || d, c = (ve.get(s, "events") || {})[t.type] && ve.get(s, "handle"), c && c.apply(s, n), c = l && s[l], c && c.apply && Z.acceptData(s) && (t.result = c.apply(s, n), t.result === !1 && t.preventDefault());
                    return t.type = d, i || t.isDefaultPrevented() || f._default && f._default.apply(p.pop(), n) !== !1 || !Z.acceptData(r) || l && Z.isFunction(r[d]) && !Z.isWindow(r) && (a = r[l], a && (r[l] = null), Z.event.triggered = d, r[d](), Z.event.triggered = void 0, a && (r[l] = a)), t.result
                }
            },
            dispatch: function(e) {
                e = Z.event.fix(e);
                var t, n, r, i, o, s = [],
                    a = _.call(arguments),
                    u = (ve.get(this, "events") || {})[e.type] || [],
                    l = Z.event.special[e.type] || {};
                if (a[0] = e, e.delegateTarget = this, !l.preDispatch || l.preDispatch.call(this, e) !== !1) {
                    for (s = Z.event.handlers.call(this, e, u), t = 0;
                        (i = s[t++]) && !e.isPropagationStopped();)
                        for (e.currentTarget = i.elem, n = 0;
                            (o = i.handlers[n++]) && !e.isImmediatePropagationStopped();)(!e.namespace_re || e.namespace_re.test(o.namespace)) && (e.handleObj = o, e.data = o.data, r = ((Z.event.special[o.origType] || {}).handle || o.handler).apply(i.elem, a), void 0 !== r && (e.result = r) === !1 && (e.preventDefault(), e.stopPropagation()));
                    return l.postDispatch && l.postDispatch.call(this, e), e.result
                }
            },
            handlers: function(e, t) {
                var n, r, i, o, s = [],
                    a = t.delegateCount,
                    u = e.target;
                if (a && u.nodeType && (!e.button || "click" !== e.type))
                    for (; u !== this; u = u.parentNode || this)
                        if (u.disabled !== !0 || "click" !== e.type) {
                            for (r = [], n = 0; a > n; n++) o = t[n], i = o.selector + " ", void 0 === r[i] && (r[i] = o.needsContext ? Z(i, this).index(u) >= 0 : Z.find(i, this, null, [u]).length), r[i] && r.push(o);
                            r.length && s.push({
                                elem: u,
                                handlers: r
                            })
                        }
                return a < t.length && s.push({
                    elem: this,
                    handlers: t.slice(a)
                }), s
            },
            props: "altKey bubbles cancelable ctrlKey currentTarget eventPhase metaKey relatedTarget shiftKey target timeStamp view which".split(" "),
            fixHooks: {},
            keyHooks: {
                props: "char charCode key keyCode".split(" "),
                filter: function(e, t) {
                    return null == e.which && (e.which = null != t.charCode ? t.charCode : t.keyCode), e
                }
            },
            mouseHooks: {
                props: "button buttons clientX clientY offsetX offsetY pageX pageY screenX screenY toElement".split(" "),
                filter: function(e, t) {
                    var n, r, i, o = t.button;
                    return null == e.pageX && null != t.clientX && (n = e.target.ownerDocument || J, r = n.documentElement, i = n.body, e.pageX = t.clientX + (r && r.scrollLeft || i && i.scrollLeft || 0) - (r && r.clientLeft || i && i.clientLeft || 0), e.pageY = t.clientY + (r && r.scrollTop || i && i.scrollTop || 0) - (r && r.clientTop || i && i.clientTop || 0)), e.which || void 0 === o || (e.which = 1 & o ? 1 : 2 & o ? 3 : 4 & o ? 2 : 0), e
                }
            },
            fix: function(e) {
                if (e[Z.expando]) return e;
                var t, n, r, i = e.type,
                    o = e,
                    s = this.fixHooks[i];
                for (s || (this.fixHooks[i] = s = Se.test(i) ? this.mouseHooks : ke.test(i) ? this.keyHooks : {}), r = s.props ? this.props.concat(s.props) : this.props, e = new Z.Event(o), t = r.length; t--;) n = r[t], e[n] = o[n];
                return e.target || (e.target = J), 3 === e.target.nodeType && (e.target = e.target.parentNode), s.filter ? s.filter(e, o) : e
            },
            special: {
                load: {
                    noBubble: !0
                },
                focus: {
                    trigger: function() {
                        return this !== f() && this.focus ? (this.focus(), !1) : void 0
                    },
                    delegateType: "focusin"
                },
                blur: {
                    trigger: function() {
                        return this === f() && this.blur ? (this.blur(), !1) : void 0
                    },
                    delegateType: "focusout"
                },
                click: {
                    trigger: function() {
                        return "checkbox" === this.type && this.click && Z.nodeName(this, "input") ? (this.click(), !1) : void 0
                    },
                    _default: function(e) {
                        return Z.nodeName(e.target, "a")
                    }
                },
                beforeunload: {
                    postDispatch: function(e) {
                        void 0 !== e.result && e.originalEvent && (e.originalEvent.returnValue = e.result)
                    }
                }
            },
            simulate: function(e, t, n, r) {
                var i = Z.extend(new Z.Event, n, {
                    type: e,
                    isSimulated: !0,
                    originalEvent: {}
                });
                r ? Z.event.trigger(i, null, t) : Z.event.dispatch.call(t, i), i.isDefaultPrevented() && n.preventDefault()
            }
        }, Z.removeEvent = function(e, t, n) {
            e.removeEventListener && e.removeEventListener(t, n, !1)
        }, Z.Event = function(e, t) {
            return this instanceof Z.Event ? (e && e.type ? (this.originalEvent = e, this.type = e.type, this.isDefaultPrevented = e.defaultPrevented || void 0 === e.defaultPrevented && e.returnValue === !1 ? l : c) : this.type = e, t && Z.extend(this, t), this.timeStamp = e && e.timeStamp || Z.now(), void(this[Z.expando] = !0)) : new Z.Event(e, t)
        }, Z.Event.prototype = {
            isDefaultPrevented: c,
            isPropagationStopped: c,
            isImmediatePropagationStopped: c,
            preventDefault: function() {
                var e = this.originalEvent;
                this.isDefaultPrevented = l, e && e.preventDefault && e.preventDefault()
            },
            stopPropagation: function() {
                var e = this.originalEvent;
                this.isPropagationStopped = l, e && e.stopPropagation && e.stopPropagation()
            },
            stopImmediatePropagation: function() {
                var e = this.originalEvent;
                this.isImmediatePropagationStopped = l, e && e.stopImmediatePropagation && e.stopImmediatePropagation(), this.stopPropagation()
            }
        }, Z.each({
            mouseenter: "mouseover",
            mouseleave: "mouseout",
            pointerenter: "pointerover",
            pointerleave: "pointerout"
        }, function(e, t) {
            Z.event.special[e] = {
                delegateType: t,
                bindType: t,
                handle: function(e) {
                    var n, r = this,
                        i = e.relatedTarget,
                        o = e.handleObj;
                    return (!i || i !== r && !Z.contains(r, i)) && (e.type = o.origType, n = o.handler.apply(this, arguments), e.type = t), n
                }
            }
        }), Q.focusinBubbles || Z.each({
            focus: "focusin",
            blur: "focusout"
        }, function(e, t) {
            var n = function(e) {
                Z.event.simulate(t, e.target, Z.event.fix(e), !0)
            };
            Z.event.special[t] = {
                setup: function() {
                    var r = this.ownerDocument || this,
                        i = ve.access(r, t);
                    i || r.addEventListener(e, n, !0), ve.access(r, t, (i || 0) + 1)
                },
                teardown: function() {
                    var r = this.ownerDocument || this,
                        i = ve.access(r, t) - 1;
                    i ? ve.access(r, t, i) : (r.removeEventListener(e, n, !0), ve.remove(r, t))
                }
            }
        }), Z.fn.extend({
            on: function(e, t, n, r, i) {
                var o, s;
                if ("object" == typeof e) {
                    "string" != typeof t && (n = n || t, t = void 0);
                    for (s in e) this.on(s, t, n, e[s], i);
                    return this
                }
                if (null == n && null == r ? (r = t, n = t = void 0) : null == r && ("string" == typeof t ? (r = n, n = void 0) : (r = n, n = t, t = void 0)), r === !1) r = c;
                else if (!r) return this;
                return 1 === i && (o = r, r = function(e) {
                    return Z().off(e), o.apply(this, arguments)
                }, r.guid = o.guid || (o.guid = Z.guid++)), this.each(function() {
                    Z.event.add(this, e, r, n, t)
                })
            },
            one: function(e, t, n, r) {
                return this.on(e, t, n, r, 1)
            },
            off: function(e, t, n) {
                var r, i;
                if (e && e.preventDefault && e.handleObj) return r = e.handleObj, Z(e.delegateTarget).off(r.namespace ? r.origType + "." + r.namespace : r.origType, r.selector, r.handler), this;
                if ("object" == typeof e) {
                    for (i in e) this.off(i, t, e[i]);
                    return this
                }
                return (t === !1 || "function" == typeof t) && (n = t, t = void 0), n === !1 && (n = c), this.each(function() {
                    Z.event.remove(this, e, n, t)
                })
            },
            trigger: function(e, t) {
                return this.each(function() {
                    Z.event.trigger(e, t, this)
                })
            },
            triggerHandler: function(e, t) {
                var n = this[0];
                return n ? Z.event.trigger(e, t, n, !0) : void 0
            }
        });
        var Ae = /<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi,
            Le = /<([\w:]+)/,
            qe = /<|&#?\w+;/,
            He = /<(?:script|style|link)/i,
            Oe = /checked\s*(?:[^=]|=\s*.checked.)/i,
            Me = /^$|\/(?:java|ecma)script/i,
            Fe = /^true\/(.*)/,
            Pe = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g,
            Re = {
                option: [1, "<select multiple='multiple'>", "</select>"],
                thead: [1, "<table>", "</table>"],
                col: [2, "<table><colgroup>", "</colgroup></table>"],
                tr: [2, "<table><tbody>", "</tbody></table>"],
                td: [3, "<table><tbody><tr>", "</tr></tbody></table>"],
                _default: [0, "", ""]
            };
        Re.optgroup = Re.option, Re.tbody = Re.tfoot = Re.colgroup = Re.caption = Re.thead, Re.th = Re.td, Z.extend({
            clone: function(e, t, n) {
                var r, i, o, s, a = e.cloneNode(!0),
                    u = Z.contains(e.ownerDocument, e);
                if (!(Q.noCloneChecked || 1 !== e.nodeType && 11 !== e.nodeType || Z.isXMLDoc(e)))
                    for (s = v(a), o = v(e), r = 0, i = o.length; i > r; r++) y(o[r], s[r]);
                if (t)
                    if (n)
                        for (o = o || v(e), s = s || v(a), r = 0, i = o.length; i > r; r++) m(o[r], s[r]);
                    else m(e, a);
                return s = v(a, "script"), s.length > 0 && g(s, !u && v(e, "script")), a
            },
            buildFragment: function(e, t, n, r) {
                for (var i, o, s, a, u, l, c = t.createDocumentFragment(), f = [], p = 0, d = e.length; d > p; p++)
                    if (i = e[p], i || 0 === i)
                        if ("object" === Z.type(i)) Z.merge(f, i.nodeType ? [i] : i);
                        else if (qe.test(i)) {
                    for (o = o || c.appendChild(t.createElement("div")), s = (Le.exec(i) || ["", ""])[1].toLowerCase(), a = Re[s] || Re._default, o.innerHTML = a[1] + i.replace(Ae, "<$1></$2>") + a[2], l = a[0]; l--;) o = o.lastChild;
                    Z.merge(f, o.childNodes), o = c.firstChild, o.textContent = ""
                } else f.push(t.createTextNode(i));
                for (c.textContent = "", p = 0; i = f[p++];)
                    if ((!r || -1 === Z.inArray(i, r)) && (u = Z.contains(i.ownerDocument, i), o = v(c.appendChild(i), "script"), u && g(o), n))
                        for (l = 0; i = o[l++];) Me.test(i.type || "") && n.push(i);
                return c
            },
            cleanData: function(e) {
                for (var t, n, r, i, o = Z.event.special, s = 0; void 0 !== (n = e[s]); s++) {
                    if (Z.acceptData(n) && (i = n[ve.expando], i && (t = ve.cache[i]))) {
                        if (t.events)
                            for (r in t.events) o[r] ? Z.event.remove(n, r) : Z.removeEvent(n, r, t.handle);
                        ve.cache[i] && delete ve.cache[i]
                    }
                    delete ye.cache[n[ye.expando]]
                }
            }
        }), Z.fn.extend({
            text: function(e) {
                return me(this, function(e) {
                    return void 0 === e ? Z.text(this) : this.empty().each(function() {
                        (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) && (this.textContent = e)
                    })
                }, null, e, arguments.length)
            },
            append: function() {
                return this.domManip(arguments, function(e) {
                    if (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) {
                        var t = p(this, e);
                        t.appendChild(e)
                    }
                })
            },
            prepend: function() {
                return this.domManip(arguments, function(e) {
                    if (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) {
                        var t = p(this, e);
                        t.insertBefore(e, t.firstChild)
                    }
                })
            },
            before: function() {
                return this.domManip(arguments, function(e) {
                    this.parentNode && this.parentNode.insertBefore(e, this)
                })
            },
            after: function() {
                return this.domManip(arguments, function(e) {
                    this.parentNode && this.parentNode.insertBefore(e, this.nextSibling)
                })
            },
            remove: function(e, t) {
                for (var n, r = e ? Z.filter(e, this) : this, i = 0; null != (n = r[i]); i++) t || 1 !== n.nodeType || Z.cleanData(v(n)), n.parentNode && (t && Z.contains(n.ownerDocument, n) && g(v(n, "script")), n.parentNode.removeChild(n));
                return this
            },
            empty: function() {
                for (var e, t = 0; null != (e = this[t]); t++) 1 === e.nodeType && (Z.cleanData(v(e, !1)), e.textContent = "");
                return this
            },
            clone: function(e, t) {
                return e = null == e ? !1 : e, t = null == t ? e : t, this.map(function() {
                    return Z.clone(this, e, t)
                })
            },
            html: function(e) {
                return me(this, function(e) {
                    var t = this[0] || {},
                        n = 0,
                        r = this.length;
                    if (void 0 === e && 1 === t.nodeType) return t.innerHTML;
                    if ("string" == typeof e && !He.test(e) && !Re[(Le.exec(e) || ["", ""])[1].toLowerCase()]) {
                        e = e.replace(Ae, "<$1></$2>");
                        try {
                            for (; r > n; n++) t = this[n] || {}, 1 === t.nodeType && (Z.cleanData(v(t, !1)), t.innerHTML = e);
                            t = 0
                        } catch (i) {}
                    }
                    t && this.empty().append(e)
                }, null, e, arguments.length)
            },
            replaceWith: function() {
                var e = arguments[0];
                return this.domManip(arguments, function(t) {
                    e = this.parentNode, Z.cleanData(v(this)), e && e.replaceChild(t, this)
                }), e && (e.length || e.nodeType) ? this : this.remove()
            },
            detach: function(e) {
                return this.remove(e, !0)
            },
            domManip: function(e, t) {
                e = X.apply([], e);
                var n, r, i, o, s, a, u = 0,
                    l = this.length,
                    c = this,
                    f = l - 1,
                    p = e[0],
                    g = Z.isFunction(p);
                if (g || l > 1 && "string" == typeof p && !Q.checkClone && Oe.test(p)) return this.each(function(n) {
                    var r = c.eq(n);
                    g && (e[0] = p.call(this, n, r.html())), r.domManip(e, t)
                });
                if (l && (n = Z.buildFragment(e, this[0].ownerDocument, !1, this), r = n.firstChild, 1 === n.childNodes.length && (n = r), r)) {
                    for (i = Z.map(v(n, "script"), d), o = i.length; l > u; u++) s = n, u !== f && (s = Z.clone(s, !0, !0), o && Z.merge(i, v(s, "script"))), t.call(this[u], s, u);
                    if (o)
                        for (a = i[i.length - 1].ownerDocument, Z.map(i, h), u = 0; o > u; u++) s = i[u], Me.test(s.type || "") && !ve.access(s, "globalEval") && Z.contains(a, s) && (s.src ? Z._evalUrl && Z._evalUrl(s.src) : Z.globalEval(s.textContent.replace(Pe, "")))
                }
                return this
            }
        }), Z.each({
            appendTo: "append",
            prependTo: "prepend",
            insertBefore: "before",
            insertAfter: "after",
            replaceAll: "replaceWith"
        }, function(e, t) {
            Z.fn[e] = function(e) {
                for (var n, r = [], i = Z(e), o = i.length - 1, s = 0; o >= s; s++) n = s === o ? this : this.clone(!0), Z(i[s])[t](n), z.apply(r, n.get());
                return this.pushStack(r)
            }
        });
        var We, $e = {},
            Ie = /^margin/,
            Be = new RegExp("^(" + we + ")(?!px)[a-z%]+$", "i"),
            _e = function(e) {
                return e.ownerDocument.defaultView.getComputedStyle(e, null)
            };
        ! function() {
            function t() {
                s.style.cssText = "-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;display:block;margin-top:1%;top:1%;border:1px;padding:1px;width:4px;position:absolute", s.innerHTML = "", i.appendChild(o);
                var t = e.getComputedStyle(s, null);
                n = "1%" !== t.top, r = "4px" === t.width, i.removeChild(o)
            }
            var n, r, i = J.documentElement,
                o = J.createElement("div"),
                s = J.createElement("div");
            s.style && (s.style.backgroundClip = "content-box", s.cloneNode(!0).style.backgroundClip = "", Q.clearCloneStyle = "content-box" === s.style.backgroundClip, o.style.cssText = "border:0;width:0;height:0;top:0;left:-9999px;margin-top:1px;position:absolute", o.appendChild(s), e.getComputedStyle && Z.extend(Q, {
                pixelPosition: function() {
                    return t(), n
                },
                boxSizingReliable: function() {
                    return null == r && t(), r
                },
                reliableMarginRight: function() {
                    var t, n = s.appendChild(J.createElement("div"));
                    return n.style.cssText = s.style.cssText = "-webkit-box-sizing:content-box;-moz-box-sizing:content-box;box-sizing:content-box;display:block;margin:0;border:0;padding:0", n.style.marginRight = n.style.width = "0", s.style.width = "1px", i.appendChild(o), t = !parseFloat(e.getComputedStyle(n, null).marginRight), i.removeChild(o), t
                }
            }))
        }(), Z.swap = function(e, t, n, r) {
            var i, o, s = {};
            for (o in t) s[o] = e.style[o], e.style[o] = t[o];
            i = n.apply(e, r || []);
            for (o in t) e.style[o] = s[o];
            return i
        };
        var Xe = /^(none|table(?!-c[ea]).+)/,
            ze = new RegExp("^(" + we + ")(.*)$", "i"),
            Ue = new RegExp("^([+-])=(" + we + ")", "i"),
            Ye = {
                position: "absolute",
                visibility: "hidden",
                display: "block"
            },
            Ve = {
                letterSpacing: "0",
                fontWeight: "400"
            },
            Ge = ["Webkit", "O", "Moz", "ms"];
        Z.extend({
            cssHooks: {
                opacity: {
                    get: function(e, t) {
                        if (t) {
                            var n = w(e, "opacity");
                            return "" === n ? "1" : n
                        }
                    }
                }
            },
            cssNumber: {
                columnCount: !0,
                fillOpacity: !0,
                flexGrow: !0,
                flexShrink: !0,
                fontWeight: !0,
                lineHeight: !0,
                opacity: !0,
                order: !0,
                orphans: !0,
                widows: !0,
                zIndex: !0,
                zoom: !0
            },
            cssProps: {
                "float": "cssFloat"
            },
            style: function(e, t, n, r) {
                if (e && 3 !== e.nodeType && 8 !== e.nodeType && e.style) {
                    var i, o, s, a = Z.camelCase(t),
                        u = e.style;
                    return t = Z.cssProps[a] || (Z.cssProps[a] = C(u, a)), s = Z.cssHooks[t] || Z.cssHooks[a], void 0 === n ? s && "get" in s && void 0 !== (i = s.get(e, !1, r)) ? i : u[t] : (o = typeof n, "string" === o && (i = Ue.exec(n)) && (n = (i[1] + 1) * i[2] + parseFloat(Z.css(e, t)), o = "number"), null != n && n === n && ("number" !== o || Z.cssNumber[a] || (n += "px"), Q.clearCloneStyle || "" !== n || 0 !== t.indexOf("background") || (u[t] = "inherit"), s && "set" in s && void 0 === (n = s.set(e, n, r)) || (u[t] = n)), void 0)
                }
            },
            css: function(e, t, n, r) {
                var i, o, s, a = Z.camelCase(t);
                return t = Z.cssProps[a] || (Z.cssProps[a] = C(e.style, a)), s = Z.cssHooks[t] || Z.cssHooks[a], s && "get" in s && (i = s.get(e, !0, n)), void 0 === i && (i = w(e, t, r)), "normal" === i && t in Ve && (i = Ve[t]), "" === n || n ? (o = parseFloat(i), n === !0 || Z.isNumeric(o) ? o || 0 : i) : i
            }
        }), Z.each(["height", "width"], function(e, t) {
            Z.cssHooks[t] = {
                get: function(e, n, r) {
                    return n ? Xe.test(Z.css(e, "display")) && 0 === e.offsetWidth ? Z.swap(e, Ye, function() {
                        return k(e, t, r)
                    }) : k(e, t, r) : void 0
                },
                set: function(e, n, r) {
                    var i = r && _e(e);
                    return N(e, n, r ? E(e, t, r, "border-box" === Z.css(e, "boxSizing", !1, i), i) : 0)
                }
            }
        }), Z.cssHooks.marginRight = T(Q.reliableMarginRight, function(e, t) {
            return t ? Z.swap(e, {
                display: "inline-block"
            }, w, [e, "marginRight"]) : void 0
        }), Z.each({
            margin: "",
            padding: "",
            border: "Width"
        }, function(e, t) {
            Z.cssHooks[e + t] = {
                expand: function(n) {
                    for (var r = 0, i = {}, o = "string" == typeof n ? n.split(" ") : [n]; 4 > r; r++) i[e + Te[r] + t] = o[r] || o[r - 2] || o[0];
                    return i
                }
            }, Ie.test(e) || (Z.cssHooks[e + t].set = N)
        }), Z.fn.extend({
            css: function(e, t) {
                return me(this, function(e, t, n) {
                    var r, i, o = {},
                        s = 0;
                    if (Z.isArray(t)) {
                        for (r = _e(e), i = t.length; i > s; s++) o[t[s]] = Z.css(e, t[s], !1, r);
                        return o
                    }
                    return void 0 !== n ? Z.style(e, t, n) : Z.css(e, t)
                }, e, t, arguments.length > 1)
            },
            show: function() {
                return S(this, !0)
            },
            hide: function() {
                return S(this)
            },
            toggle: function(e) {
                return "boolean" == typeof e ? e ? this.show() : this.hide() : this.each(function() {
                    Ce(this) ? Z(this).show() : Z(this).hide()
                })
            }
        }), Z.Tween = j, j.prototype = {
            constructor: j,
            init: function(e, t, n, r, i, o) {
                this.elem = e, this.prop = n, this.easing = i || "swing", this.options = t, this.start = this.now = this.cur(), this.end = r, this.unit = o || (Z.cssNumber[n] ? "" : "px")
            },
            cur: function() {
                var e = j.propHooks[this.prop];
                return e && e.get ? e.get(this) : j.propHooks._default.get(this)
            },
            run: function(e) {
                var t, n = j.propHooks[this.prop];
                return this.options.duration ? this.pos = t = Z.easing[this.easing](e, this.options.duration * e, 0, 1, this.options.duration) : this.pos = t = e, this.now = (this.end - this.start) * t + this.start, this.options.step && this.options.step.call(this.elem, this.now, this), n && n.set ? n.set(this) : j.propHooks._default.set(this), this
            }
        }, j.prototype.init.prototype = j.prototype, j.propHooks = {
            _default: {
                get: function(e) {
                    var t;
                    return null == e.elem[e.prop] || e.elem.style && null != e.elem.style[e.prop] ? (t = Z.css(e.elem, e.prop, ""), t && "auto" !== t ? t : 0) : e.elem[e.prop]
                },
                set: function(e) {
                    Z.fx.step[e.prop] ? Z.fx.step[e.prop](e) : e.elem.style && (null != e.elem.style[Z.cssProps[e.prop]] || Z.cssHooks[e.prop]) ? Z.style(e.elem, e.prop, e.now + e.unit) : e.elem[e.prop] = e.now
                }
            }
        }, j.propHooks.scrollTop = j.propHooks.scrollLeft = {
            set: function(e) {
                e.elem.nodeType && e.elem.parentNode && (e.elem[e.prop] = e.now)
            }
        }, Z.easing = {
            linear: function(e) {
                return e
            },
            swing: function(e) {
                return .5 - Math.cos(e * Math.PI) / 2
            }
        }, Z.fx = j.prototype.init, Z.fx.step = {};
        var Qe, Je, Ke = /^(?:toggle|show|hide)$/,
            Ze = new RegExp("^(?:([+-])=|)(" + we + ")([a-z%]*)$", "i"),
            et = /queueHooks$/,
            tt = [q],
            nt = {
                "*": [function(e, t) {
                    var n = this.createTween(e, t),
                        r = n.cur(),
                        i = Ze.exec(t),
                        o = i && i[3] || (Z.cssNumber[e] ? "" : "px"),
                        s = (Z.cssNumber[e] || "px" !== o && +r) && Ze.exec(Z.css(n.elem, e)),
                        a = 1,
                        u = 20;
                    if (s && s[3] !== o) {
                        o = o || s[3], i = i || [], s = +r || 1;
                        do a = a || ".5", s /= a, Z.style(n.elem, e, s + o); while (a !== (a = n.cur() / r) && 1 !== a && --u)
                    }
                    return i && (s = n.start = +s || +r || 0, n.unit = o, n.end = i[1] ? s + (i[1] + 1) * i[2] : +i[2]), n
                }]
            };
        Z.Animation = Z.extend(O, {
                tweener: function(e, t) {
                    Z.isFunction(e) ? (t = e, e = ["*"]) : e = e.split(" ");
                    for (var n, r = 0, i = e.length; i > r; r++) n = e[r], nt[n] = nt[n] || [], nt[n].unshift(t)
                },
                prefilter: function(e, t) {
                    t ? tt.unshift(e) : tt.push(e)
                }
            }), Z.speed = function(e, t, n) {
                var r = e && "object" == typeof e ? Z.extend({}, e) : {
                    complete: n || !n && t || Z.isFunction(e) && e,
                    duration: e,
                    easing: n && t || t && !Z.isFunction(t) && t
                };
                return r.duration = Z.fx.off ? 0 : "number" == typeof r.duration ? r.duration : r.duration in Z.fx.speeds ? Z.fx.speeds[r.duration] : Z.fx.speeds._default, (null == r.queue || r.queue === !0) && (r.queue = "fx"), r.old = r.complete, r.complete = function() {
                    Z.isFunction(r.old) && r.old.call(this), r.queue && Z.dequeue(this, r.queue)
                }, r
            }, Z.fn.extend({
                fadeTo: function(e, t, n, r) {
                    return this.filter(Ce).css("opacity", 0).show().end().animate({
                        opacity: t
                    }, e, n, r)
                },
                animate: function(e, t, n, r) {
                    var i = Z.isEmptyObject(e),
                        o = Z.speed(t, n, r),
                        s = function() {
                            var t = O(this, Z.extend({}, e), o);
                            (i || ve.get(this, "finish")) && t.stop(!0)
                        };
                    return s.finish = s, i || o.queue === !1 ? this.each(s) : this.queue(o.queue, s)
                },
                stop: function(e, t, n) {
                    var r = function(e) {
                        var t = e.stop;
                        delete e.stop, t(n)
                    };
                    return "string" != typeof e && (n = t, t = e, e = void 0), t && e !== !1 && this.queue(e || "fx", []), this.each(function() {
                        var t = !0,
                            i = null != e && e + "queueHooks",
                            o = Z.timers,
                            s = ve.get(this);
                        if (i) s[i] && s[i].stop && r(s[i]);
                        else
                            for (i in s) s[i] && s[i].stop && et.test(i) && r(s[i]);
                        for (i = o.length; i--;) o[i].elem !== this || null != e && o[i].queue !== e || (o[i].anim.stop(n), t = !1, o.splice(i, 1));
                        (t || !n) && Z.dequeue(this, e)
                    })
                },
                finish: function(e) {
                    return e !== !1 && (e = e || "fx"), this.each(function() {
                        var t, n = ve.get(this),
                            r = n[e + "queue"],
                            i = n[e + "queueHooks"],
                            o = Z.timers,
                            s = r ? r.length : 0;
                        for (n.finish = !0, Z.queue(this, e, []), i && i.stop && i.stop.call(this, !0), t = o.length; t--;) o[t].elem === this && o[t].queue === e && (o[t].anim.stop(!0), o.splice(t, 1));
                        for (t = 0; s > t; t++) r[t] && r[t].finish && r[t].finish.call(this);
                        delete n.finish
                    })
                }
            }), Z.each(["toggle", "show", "hide"], function(e, t) {
                var n = Z.fn[t];
                Z.fn[t] = function(e, r, i) {
                    return null == e || "boolean" == typeof e ? n.apply(this, arguments) : this.animate(A(t, !0), e, r, i)
                }
            }), Z.each({
                slideDown: A("show"),
                slideUp: A("hide"),
                slideToggle: A("toggle"),
                fadeIn: {
                    opacity: "show"
                },
                fadeOut: {
                    opacity: "hide"
                },
                fadeToggle: {
                    opacity: "toggle"
                }
            }, function(e, t) {
                Z.fn[e] = function(e, n, r) {
                    return this.animate(t, e, n, r)
                }
            }), Z.timers = [], Z.fx.tick = function() {
                var e, t = 0,
                    n = Z.timers;
                for (Qe = Z.now(); t < n.length; t++) e = n[t], e() || n[t] !== e || n.splice(t--, 1);
                n.length || Z.fx.stop(), Qe = void 0
            }, Z.fx.timer = function(e) {
                Z.timers.push(e), e() ? Z.fx.start() : Z.timers.pop()
            }, Z.fx.interval = 13, Z.fx.start = function() {
                Je || (Je = setInterval(Z.fx.tick, Z.fx.interval))
            }, Z.fx.stop = function() {
                clearInterval(Je), Je = null
            }, Z.fx.speeds = {
                slow: 600,
                fast: 200,
                _default: 400
            }, Z.fn.delay = function(e, t) {
                return e = Z.fx ? Z.fx.speeds[e] || e : e, t = t || "fx", this.queue(t, function(t, n) {
                    var r = setTimeout(t, e);
                    n.stop = function() {
                        clearTimeout(r)
                    }
                })
            },
            function() {
                var e = J.createElement("input"),
                    t = J.createElement("select"),
                    n = t.appendChild(J.createElement("option"));
                e.type = "checkbox", Q.checkOn = "" !== e.value, Q.optSelected = n.selected, t.disabled = !0, Q.optDisabled = !n.disabled, e = J.createElement("input"), e.value = "t", e.type = "radio", Q.radioValue = "t" === e.value
            }();
        var rt, it, ot = Z.expr.attrHandle;
        Z.fn.extend({
            attr: function(e, t) {
                return me(this, Z.attr, e, t, arguments.length > 1)
            },
            removeAttr: function(e) {
                return this.each(function() {
                    Z.removeAttr(this, e)
                })
            }
        }), Z.extend({
            attr: function(e, t, n) {
                var r, i, o = e.nodeType;
                if (e && 3 !== o && 8 !== o && 2 !== o) return typeof e.getAttribute === Ee ? Z.prop(e, t, n) : (1 === o && Z.isXMLDoc(e) || (t = t.toLowerCase(), r = Z.attrHooks[t] || (Z.expr.match.bool.test(t) ? it : rt)), void 0 === n ? r && "get" in r && null !== (i = r.get(e, t)) ? i : (i = Z.find.attr(e, t), null == i ? void 0 : i) : null !== n ? r && "set" in r && void 0 !== (i = r.set(e, n, t)) ? i : (e.setAttribute(t, n + ""), n) : void Z.removeAttr(e, t))
            },
            removeAttr: function(e, t) {
                var n, r, i = 0,
                    o = t && t.match(de);
                if (o && 1 === e.nodeType)
                    for (; n = o[i++];) r = Z.propFix[n] || n, Z.expr.match.bool.test(n) && (e[r] = !1), e.removeAttribute(n)
            },
            attrHooks: {
                type: {
                    set: function(e, t) {
                        if (!Q.radioValue && "radio" === t && Z.nodeName(e, "input")) {
                            var n = e.value;
                            return e.setAttribute("type", t), n && (e.value = n), t
                        }
                    }
                }
            }
        }), it = {
            set: function(e, t, n) {
                return t === !1 ? Z.removeAttr(e, n) : e.setAttribute(n, n), n
            }
        }, Z.each(Z.expr.match.bool.source.match(/\w+/g), function(e, t) {
            var n = ot[t] || Z.find.attr;
            ot[t] = function(e, t, r) {
                var i, o;
                return r || (o = ot[t], ot[t] = i, i = null != n(e, t, r) ? t.toLowerCase() : null, ot[t] = o), i
            }
        });
        var st = /^(?:input|select|textarea|button)$/i;
        Z.fn.extend({
            prop: function(e, t) {
                return me(this, Z.prop, e, t, arguments.length > 1)
            },
            removeProp: function(e) {
                return this.each(function() {
                    delete this[Z.propFix[e] || e]
                })
            }
        }), Z.extend({
            propFix: {
                "for": "htmlFor",
                "class": "className"
            },
            prop: function(e, t, n) {
                var r, i, o, s = e.nodeType;
                if (e && 3 !== s && 8 !== s && 2 !== s) return o = 1 !== s || !Z.isXMLDoc(e), o && (t = Z.propFix[t] || t, i = Z.propHooks[t]), void 0 !== n ? i && "set" in i && void 0 !== (r = i.set(e, n, t)) ? r : e[t] = n : i && "get" in i && null !== (r = i.get(e, t)) ? r : e[t]
            },
            propHooks: {
                tabIndex: {
                    get: function(e) {
                        return e.hasAttribute("tabindex") || st.test(e.nodeName) || e.href ? e.tabIndex : -1
                    }
                }
            }
        }), Q.optSelected || (Z.propHooks.selected = {
            get: function(e) {
                var t = e.parentNode;
                return t && t.parentNode && t.parentNode.selectedIndex, null
            }
        }), Z.each(["tabIndex", "readOnly", "maxLength", "cellSpacing", "cellPadding", "rowSpan", "colSpan", "useMap", "frameBorder", "contentEditable"], function() {
            Z.propFix[this.toLowerCase()] = this
        });
        var at = /[\t\r\n\f]/g;
        Z.fn.extend({
            addClass: function(e) {
                var t, n, r, i, o, s, a = "string" == typeof e && e,
                    u = 0,
                    l = this.length;
                if (Z.isFunction(e)) return this.each(function(t) {
                    Z(this).addClass(e.call(this, t, this.className))
                });
                if (a)
                    for (t = (e || "").match(de) || []; l > u; u++)
                        if (n = this[u], r = 1 === n.nodeType && (n.className ? (" " + n.className + " ").replace(at, " ") : " ")) {
                            for (o = 0; i = t[o++];) r.indexOf(" " + i + " ") < 0 && (r += i + " ");
                            s = Z.trim(r), n.className !== s && (n.className = s)
                        }
                return this
            },
            removeClass: function(e) {
                var t, n, r, i, o, s, a = 0 === arguments.length || "string" == typeof e && e,
                    u = 0,
                    l = this.length;
                if (Z.isFunction(e)) return this.each(function(t) {
                    Z(this).removeClass(e.call(this, t, this.className))
                });
                if (a)
                    for (t = (e || "").match(de) || []; l > u; u++)
                        if (n = this[u], r = 1 === n.nodeType && (n.className ? (" " + n.className + " ").replace(at, " ") : "")) {
                            for (o = 0; i = t[o++];)
                                for (; r.indexOf(" " + i + " ") >= 0;) r = r.replace(" " + i + " ", " ");
                            s = e ? Z.trim(r) : "", n.className !== s && (n.className = s)
                        }
                return this
            },
            toggleClass: function(e, t) {
                var n = typeof e;
                return "boolean" == typeof t && "string" === n ? t ? this.addClass(e) : this.removeClass(e) : Z.isFunction(e) ? this.each(function(n) {
                    Z(this).toggleClass(e.call(this, n, this.className, t), t)
                }) : this.each(function() {
                    if ("string" === n)
                        for (var t, r = 0, i = Z(this), o = e.match(de) || []; t = o[r++];) i.hasClass(t) ? i.removeClass(t) : i.addClass(t);
                    else(n === Ee || "boolean" === n) && (this.className && ve.set(this, "__className__", this.className), this.className = this.className || e === !1 ? "" : ve.get(this, "__className__") || "")
                })
            },
            hasClass: function(e) {
                for (var t = " " + e + " ", n = 0, r = this.length; r > n; n++)
                    if (1 === this[n].nodeType && (" " + this[n].className + " ").replace(at, " ").indexOf(t) >= 0) return !0;
                return !1
            }
        });
        var ut = /\r/g;
        Z.fn.extend({
            val: function(e) {
                var t, n, r, i = this[0]; {
                    if (arguments.length) return r = Z.isFunction(e), this.each(function(n) {
                        var i;
                        1 === this.nodeType && (i = r ? e.call(this, n, Z(this).val()) : e, null == i ? i = "" : "number" == typeof i ? i += "" : Z.isArray(i) && (i = Z.map(i, function(e) {
                            return null == e ? "" : e + ""
                        })), t = Z.valHooks[this.type] || Z.valHooks[this.nodeName.toLowerCase()], t && "set" in t && void 0 !== t.set(this, i, "value") || (this.value = i))
                    });
                    if (i) return t = Z.valHooks[i.type] || Z.valHooks[i.nodeName.toLowerCase()], t && "get" in t && void 0 !== (n = t.get(i, "value")) ? n : (n = i.value, "string" == typeof n ? n.replace(ut, "") : null == n ? "" : n)
                }
            }
        }), Z.extend({
            valHooks: {
                option: {
                    get: function(e) {
                        var t = Z.find.attr(e, "value");
                        return null != t ? t : Z.trim(Z.text(e))
                    }
                },
                select: {
                    get: function(e) {
                        for (var t, n, r = e.options, i = e.selectedIndex, o = "select-one" === e.type || 0 > i, s = o ? null : [], a = o ? i + 1 : r.length, u = 0 > i ? a : o ? i : 0; a > u; u++)
                            if (n = r[u], (n.selected || u === i) && (Q.optDisabled ? !n.disabled : null === n.getAttribute("disabled")) && (!n.parentNode.disabled || !Z.nodeName(n.parentNode, "optgroup"))) {
                                if (t = Z(n).val(), o) return t;
                                s.push(t)
                            }
                        return s
                    },
                    set: function(e, t) {
                        for (var n, r, i = e.options, o = Z.makeArray(t), s = i.length; s--;) r = i[s], (r.selected = Z.inArray(r.value, o) >= 0) && (n = !0);
                        return n || (e.selectedIndex = -1), o
                    }
                }
            }
        }), Z.each(["radio", "checkbox"], function() {
            Z.valHooks[this] = {
                set: function(e, t) {
                    return Z.isArray(t) ? e.checked = Z.inArray(Z(e).val(), t) >= 0 : void 0
                }
            }, Q.checkOn || (Z.valHooks[this].get = function(e) {
                return null === e.getAttribute("value") ? "on" : e.value
            })
        }), Z.each("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error contextmenu".split(" "), function(e, t) {
            Z.fn[t] = function(e, n) {
                return arguments.length > 0 ? this.on(t, null, e, n) : this.trigger(t)
            }
        }), Z.fn.extend({
            hover: function(e, t) {
                return this.mouseenter(e).mouseleave(t || e)
            },
            bind: function(e, t, n) {
                return this.on(e, null, t, n)
            },
            unbind: function(e, t) {
                return this.off(e, null, t)
            },
            delegate: function(e, t, n, r) {
                return this.on(t, e, n, r)
            },
            undelegate: function(e, t, n) {
                return 1 === arguments.length ? this.off(e, "**") : this.off(t, e || "**", n)
            }
        });
        var lt = Z.now(),
            ct = /\?/;
        Z.parseJSON = function(e) {
            return JSON.parse(e + "")
        }, Z.parseXML = function(e) {
            var t, n;
            if (!e || "string" != typeof e) return null;
            try {
                n = new DOMParser, t = n.parseFromString(e, "text/xml")
            } catch (r) {
                t = void 0
            }
            return (!t || t.getElementsByTagName("parsererror").length) && Z.error("Invalid XML: " + e), t
        };
        var ft, pt, dt = /#.*$/,
            ht = /([?&])_=[^&]*/,
            gt = /^(.*?):[ \t]*([^\r\n]*)$/gm,
            mt = /^(?:about|app|app-storage|.+-extension|file|res|widget):$/,
            vt = /^(?:GET|HEAD)$/,
            yt = /^\/\//,
            xt = /^([\w.+-]+:)(?:\/\/(?:[^\/?#]*@|)([^\/?#:]*)(?::(\d+)|)|)/,
            bt = {},
            wt = {},
            Tt = "*/".concat("*");
        try {
            pt = location.href
        } catch (Ct) {
            pt = J.createElement("a"), pt.href = "", pt = pt.href
        }
        ft = xt.exec(pt.toLowerCase()) || [], Z.extend({
            active: 0,
            lastModified: {},
            etag: {},
            ajaxSettings: {
                url: pt,
                type: "GET",
                isLocal: mt.test(ft[1]),
                global: !0,
                processData: !0,
                async: !0,
                contentType: "application/x-www-form-urlencoded; charset=UTF-8",
                accepts: {
                    "*": Tt,
                    text: "text/plain",
                    html: "text/html",
                    xml: "application/xml, text/xml",
                    json: "application/json, text/javascript"
                },
                contents: {
                    xml: /xml/,
                    html: /html/,
                    json: /json/
                },
                responseFields: {
                    xml: "responseXML",
                    text: "responseText",
                    json: "responseJSON"
                },
                converters: {
                    "* text": String,
                    "text html": !0,
                    "text json": Z.parseJSON,
                    "text xml": Z.parseXML
                },
                flatOptions: {
                    url: !0,
                    context: !0
                }
            },
            ajaxSetup: function(e, t) {
                return t ? P(P(e, Z.ajaxSettings), t) : P(Z.ajaxSettings, e)
            },
            ajaxPrefilter: M(bt),
            ajaxTransport: M(wt),
            ajax: function(e, t) {
                function n(e, t, n, s) {
                    var u, c, v, y, b, T = t;
                    2 !== x && (x = 2, a && clearTimeout(a), r = void 0, o = s || "", w.readyState = e > 0 ? 4 : 0, u = e >= 200 && 300 > e || 304 === e, n && (y = R(f, w, n)), y = W(f, y, w, u), u ? (f.ifModified && (b = w.getResponseHeader("Last-Modified"), b && (Z.lastModified[i] = b), b = w.getResponseHeader("etag"), b && (Z.etag[i] = b)), 204 === e || "HEAD" === f.type ? T = "nocontent" : 304 === e ? T = "notmodified" : (T = y.state, c = y.data, v = y.error, u = !v)) : (v = T, (e || !T) && (T = "error", 0 > e && (e = 0))), w.status = e, w.statusText = (t || T) + "", u ? h.resolveWith(p, [c, T, w]) : h.rejectWith(p, [w, T, v]), w.statusCode(m), m = void 0, l && d.trigger(u ? "ajaxSuccess" : "ajaxError", [w, f, u ? c : v]), g.fireWith(p, [w, T]), l && (d.trigger("ajaxComplete", [w, f]), --Z.active || Z.event.trigger("ajaxStop")))
                }
                "object" == typeof e && (t = e, e = void 0), t = t || {};
                var r, i, o, s, a, u, l, c, f = Z.ajaxSetup({}, t),
                    p = f.context || f,
                    d = f.context && (p.nodeType || p.jquery) ? Z(p) : Z.event,
                    h = Z.Deferred(),
                    g = Z.Callbacks("once memory"),
                    m = f.statusCode || {},
                    v = {},
                    y = {},
                    x = 0,
                    b = "canceled",
                    w = {
                        readyState: 0,
                        getResponseHeader: function(e) {
                            var t;
                            if (2 === x) {
                                if (!s)
                                    for (s = {}; t = gt.exec(o);) s[t[1].toLowerCase()] = t[2];
                                t = s[e.toLowerCase()]
                            }
                            return null == t ? null : t
                        },
                        getAllResponseHeaders: function() {
                            return 2 === x ? o : null
                        },
                        setRequestHeader: function(e, t) {
                            var n = e.toLowerCase();
                            return x || (e = y[n] = y[n] || e, v[e] = t), this
                        },
                        overrideMimeType: function(e) {
                            return x || (f.mimeType = e), this
                        },
                        statusCode: function(e) {
                            var t;
                            if (e)
                                if (2 > x)
                                    for (t in e) m[t] = [m[t], e[t]];
                                else w.always(e[w.status]);
                            return this
                        },
                        abort: function(e) {
                            var t = e || b;
                            return r && r.abort(t), n(0, t), this
                        }
                    };
                if (h.promise(w).complete = g.add, w.success = w.done, w.error = w.fail, f.url = ((e || f.url || pt) + "").replace(dt, "").replace(yt, ft[1] + "//"), f.type = t.method || t.type || f.method || f.type, f.dataTypes = Z.trim(f.dataType || "*").toLowerCase().match(de) || [""], null == f.crossDomain && (u = xt.exec(f.url.toLowerCase()), f.crossDomain = !(!u || u[1] === ft[1] && u[2] === ft[2] && (u[3] || ("http:" === u[1] ? "80" : "443")) === (ft[3] || ("http:" === ft[1] ? "80" : "443")))), f.data && f.processData && "string" != typeof f.data && (f.data = Z.param(f.data, f.traditional)), F(bt, f, t, w), 2 === x) return w;
                l = f.global, l && 0 === Z.active++ && Z.event.trigger("ajaxStart"), f.type = f.type.toUpperCase(), f.hasContent = !vt.test(f.type), i = f.url, f.hasContent || (f.data && (i = f.url += (ct.test(i) ? "&" : "?") + f.data, delete f.data), f.cache === !1 && (f.url = ht.test(i) ? i.replace(ht, "$1_=" + lt++) : i + (ct.test(i) ? "&" : "?") + "_=" + lt++)), f.ifModified && (Z.lastModified[i] && w.setRequestHeader("If-Modified-Since", Z.lastModified[i]), Z.etag[i] && w.setRequestHeader("If-None-Match", Z.etag[i])), (f.data && f.hasContent && f.contentType !== !1 || t.contentType) && w.setRequestHeader("Content-Type", f.contentType), w.setRequestHeader("Accept", f.dataTypes[0] && f.accepts[f.dataTypes[0]] ? f.accepts[f.dataTypes[0]] + ("*" !== f.dataTypes[0] ? ", " + Tt + "; q=0.01" : "") : f.accepts["*"]);
                for (c in f.headers) w.setRequestHeader(c, f.headers[c]);
                if (f.beforeSend && (f.beforeSend.call(p, w, f) === !1 || 2 === x)) return w.abort();
                b = "abort";
                for (c in {
                        success: 1,
                        error: 1,
                        complete: 1
                    }) w[c](f[c]);
                if (r = F(wt, f, t, w)) {
                    w.readyState = 1, l && d.trigger("ajaxSend", [w, f]), f.async && f.timeout > 0 && (a = setTimeout(function() {
                        w.abort("timeout")
                    }, f.timeout));
                    try {
                        x = 1, r.send(v, n)
                    } catch (T) {
                        if (!(2 > x)) throw T;
                        n(-1, T)
                    }
                } else n(-1, "No Transport");
                return w
            },
            getJSON: function(e, t, n) {
                return Z.get(e, t, n, "json")
            },
            getScript: function(e, t) {
                return Z.get(e, void 0, t, "script")
            }
        }), Z.each(["get", "post"], function(e, t) {
            Z[t] = function(e, n, r, i) {
                return Z.isFunction(n) && (i = i || r, r = n, n = void 0), Z.ajax({
                    url: e,
                    type: t,
                    dataType: i,
                    data: n,
                    success: r
                })
            }
        }), Z.each(["ajaxStart", "ajaxStop", "ajaxComplete", "ajaxError", "ajaxSuccess", "ajaxSend"], function(e, t) {
            Z.fn[t] = function(e) {
                return this.on(t, e)
            }
        }), Z._evalUrl = function(e) {
            return Z.ajax({
                url: e,
                type: "GET",
                dataType: "script",
                async: !1,
                global: !1,
                "throws": !0
            })
        }, Z.fn.extend({
            wrapAll: function(e) {
                var t;
                return Z.isFunction(e) ? this.each(function(t) {
                    Z(this).wrapAll(e.call(this, t))
                }) : (this[0] && (t = Z(e, this[0].ownerDocument).eq(0).clone(!0), this[0].parentNode && t.insertBefore(this[0]), t.map(function() {
                    for (var e = this; e.firstElementChild;) e = e.firstElementChild;
                    return e
                }).append(this)), this)
            },
            wrapInner: function(e) {
                return Z.isFunction(e) ? this.each(function(t) {
                    Z(this).wrapInner(e.call(this, t))
                }) : this.each(function() {
                    var t = Z(this),
                        n = t.contents();
                    n.length ? n.wrapAll(e) : t.append(e)
                })
            },
            wrap: function(e) {
                var t = Z.isFunction(e);
                return this.each(function(n) {
                    Z(this).wrapAll(t ? e.call(this, n) : e)
                })
            },
            unwrap: function() {
                return this.parent().each(function() {
                    Z.nodeName(this, "body") || Z(this).replaceWith(this.childNodes)
                }).end()
            }
        }), Z.expr.filters.hidden = function(e) {
            return e.offsetWidth <= 0 && e.offsetHeight <= 0
        }, Z.expr.filters.visible = function(e) {
            return !Z.expr.filters.hidden(e)
        };
        var Nt = /%20/g,
            Et = /\[\]$/,
            kt = /\r?\n/g,
            St = /^(?:submit|button|image|reset|file)$/i,
            jt = /^(?:input|select|textarea|keygen)/i;
        Z.param = function(e, t) {
            var n, r = [],
                i = function(e, t) {
                    t = Z.isFunction(t) ? t() : null == t ? "" : t, r[r.length] = encodeURIComponent(e) + "=" + encodeURIComponent(t)
                };
            if (void 0 === t && (t = Z.ajaxSettings && Z.ajaxSettings.traditional), Z.isArray(e) || e.jquery && !Z.isPlainObject(e)) Z.each(e, function() {
                i(this.name, this.value)
            });
            else
                for (n in e) $(n, e[n], t, i);
            return r.join("&").replace(Nt, "+")
        }, Z.fn.extend({
            serialize: function() {
                return Z.param(this.serializeArray())
            },
            serializeArray: function() {
                return this.map(function() {
                    var e = Z.prop(this, "elements");
                    return e ? Z.makeArray(e) : this
                }).filter(function() {
                    var e = this.type;
                    return this.name && !Z(this).is(":disabled") && jt.test(this.nodeName) && !St.test(e) && (this.checked || !Ne.test(e))
                }).map(function(e, t) {
                    var n = Z(this).val();
                    return null == n ? null : Z.isArray(n) ? Z.map(n, function(e) {
                        return {
                            name: t.name,
                            value: e.replace(kt, "\r\n")
                        }
                    }) : {
                        name: t.name,
                        value: n.replace(kt, "\r\n")
                    }
                }).get()
            }
        }), Z.ajaxSettings.xhr = function() {
            try {
                return new XMLHttpRequest
            } catch (e) {}
        };
        var Dt = 0,
            At = {},
            Lt = {
                0: 200,
                1223: 204
            },
            qt = Z.ajaxSettings.xhr();
        e.ActiveXObject && Z(e).on("unload", function() {
            for (var e in At) At[e]()
        }), Q.cors = !!qt && "withCredentials" in qt, Q.ajax = qt = !!qt, Z.ajaxTransport(function(e) {
            var t;
            return Q.cors || qt && !e.crossDomain ? {
                send: function(n, r) {
                    var i, o = e.xhr(),
                        s = ++Dt;
                    if (o.open(e.type, e.url, e.async, e.username, e.password), e.xhrFields)
                        for (i in e.xhrFields) o[i] = e.xhrFields[i];
                    e.mimeType && o.overrideMimeType && o.overrideMimeType(e.mimeType), e.crossDomain || n["X-Requested-With"] || (n["X-Requested-With"] = "XMLHttpRequest");
                    for (i in n) o.setRequestHeader(i, n[i]);
                    t = function(e) {
                        return function() {
                            t && (delete At[s], t = o.onload = o.onerror = null, "abort" === e ? o.abort() : "error" === e ? r(o.status, o.statusText) : r(Lt[o.status] || o.status, o.statusText, "string" == typeof o.responseText ? {
                                text: o.responseText
                            } : void 0, o.getAllResponseHeaders()))
                        }
                    }, o.onload = t(), o.onerror = t("error"), t = At[s] = t("abort");
                    try {
                        o.send(e.hasContent && e.data || null)
                    } catch (a) {
                        if (t) throw a
                    }
                },
                abort: function() {
                    t && t()
                }
            } : void 0
        }), Z.ajaxSetup({
            accepts: {
                script: "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"
            },
            contents: {
                script: /(?:java|ecma)script/
            },
            converters: {
                "text script": function(e) {
                    return Z.globalEval(e), e
                }
            }
        }), Z.ajaxPrefilter("script", function(e) {
            void 0 === e.cache && (e.cache = !1), e.crossDomain && (e.type = "GET")
        }), Z.ajaxTransport("script", function(e) {
            if (e.crossDomain) {
                var t, n;
                return {
                    send: function(r, i) {
                        t = Z("<script>").prop({
                            async: !0,
                            charset: e.scriptCharset,
                            src: e.url
                        }).on("load error", n = function(e) {
                            t.remove(), n = null, e && i("error" === e.type ? 404 : 200, e.type)
                        }), J.head.appendChild(t[0])
                    },
                    abort: function() {
                        n && n()
                    }
                }
            }
        });
        var Ht = [],
            Ot = /(=)\?(?=&|$)|\?\?/;
        Z.ajaxSetup({
            jsonp: "callback",
            jsonpCallback: function() {
                var e = Ht.pop() || Z.expando + "_" + lt++;
                return this[e] = !0, e
            }
        }), Z.ajaxPrefilter("json jsonp", function(t, n, r) {
            var i, o, s, a = t.jsonp !== !1 && (Ot.test(t.url) ? "url" : "string" == typeof t.data && !(t.contentType || "").indexOf("application/x-www-form-urlencoded") && Ot.test(t.data) && "data");
            return a || "jsonp" === t.dataTypes[0] ? (i = t.jsonpCallback = Z.isFunction(t.jsonpCallback) ? t.jsonpCallback() : t.jsonpCallback, a ? t[a] = t[a].replace(Ot, "$1" + i) : t.jsonp !== !1 && (t.url += (ct.test(t.url) ? "&" : "?") + t.jsonp + "=" + i), t.converters["script json"] = function() {
                return s || Z.error(i + " was not called"), s[0]
            }, t.dataTypes[0] = "json", o = e[i], e[i] = function() {
                s = arguments
            }, r.always(function() {
                e[i] = o, t[i] && (t.jsonpCallback = n.jsonpCallback, Ht.push(i)), s && Z.isFunction(o) && o(s[0]), s = o = void 0
            }), "script") : void 0
        }), Z.parseHTML = function(e, t, n) {
            if (!e || "string" != typeof e) return null;
            "boolean" == typeof t && (n = t, t = !1), t = t || J;
            var r = se.exec(e),
                i = !n && [];
            return r ? [t.createElement(r[1])] : (r = Z.buildFragment([e], t, i), i && i.length && Z(i).remove(), Z.merge([], r.childNodes))
        };
        var Mt = Z.fn.load;
        Z.fn.load = function(e, t, n) {
            if ("string" != typeof e && Mt) return Mt.apply(this, arguments);
            var r, i, o, s = this,
                a = e.indexOf(" ");
            return a >= 0 && (r = Z.trim(e.slice(a)), e = e.slice(0, a)), Z.isFunction(t) ? (n = t, t = void 0) : t && "object" == typeof t && (i = "POST"), s.length > 0 && Z.ajax({
                url: e,
                type: i,
                dataType: "html",
                data: t
            }).done(function(e) {
                o = arguments, s.html(r ? Z("<div>").append(Z.parseHTML(e)).find(r) : e)
            }).complete(n && function(e, t) {
                s.each(n, o || [e.responseText, t, e])
            }), this
        }, Z.expr.filters.animated = function(e) {
            return Z.grep(Z.timers, function(t) {
                return e === t.elem
            }).length
        };
        var Ft = e.document.documentElement;
        Z.offset = {
            setOffset: function(e, t, n) {
                var r, i, o, s, a, u, l, c = Z.css(e, "position"),
                    f = Z(e),
                    p = {};
                "static" === c && (e.style.position = "relative"), a = f.offset(), o = Z.css(e, "top"), u = Z.css(e, "left"), l = ("absolute" === c || "fixed" === c) && (o + u).indexOf("auto") > -1, l ? (r = f.position(), s = r.top, i = r.left) : (s = parseFloat(o) || 0, i = parseFloat(u) || 0), Z.isFunction(t) && (t = t.call(e, n, a)), null != t.top && (p.top = t.top - a.top + s), null != t.left && (p.left = t.left - a.left + i), "using" in t ? t.using.call(e, p) : f.css(p)
            }
        }, Z.fn.extend({
            offset: function(e) {
                if (arguments.length) return void 0 === e ? this : this.each(function(t) {
                    Z.offset.setOffset(this, e, t)
                });
                var t, n, r = this[0],
                    i = {
                        top: 0,
                        left: 0
                    },
                    o = r && r.ownerDocument;
                if (o) return t = o.documentElement, Z.contains(t, r) ? (typeof r.getBoundingClientRect !== Ee && (i = r.getBoundingClientRect()), n = I(o), {
                    top: i.top + n.pageYOffset - t.clientTop,
                    left: i.left + n.pageXOffset - t.clientLeft
                }) : i
            },
            position: function() {
                if (this[0]) {
                    var e, t, n = this[0],
                        r = {
                            top: 0,
                            left: 0
                        };
                    return "fixed" === Z.css(n, "position") ? t = n.getBoundingClientRect() : (e = this.offsetParent(), t = this.offset(), Z.nodeName(e[0], "html") || (r = e.offset()), r.top += Z.css(e[0], "borderTopWidth", !0), r.left += Z.css(e[0], "borderLeftWidth", !0)), {
                        top: t.top - r.top - Z.css(n, "marginTop", !0),
                        left: t.left - r.left - Z.css(n, "marginLeft", !0)
                    }
                }
            },
            offsetParent: function() {
                return this.map(function() {
                    for (var e = this.offsetParent || Ft; e && !Z.nodeName(e, "html") && "static" === Z.css(e, "position");) e = e.offsetParent;
                    return e || Ft
                })
            }
        }), Z.each({
            scrollLeft: "pageXOffset",
            scrollTop: "pageYOffset"
        }, function(t, n) {
            var r = "pageYOffset" === n;
            Z.fn[t] = function(i) {
                return me(this, function(t, i, o) {
                    var s = I(t);
                    return void 0 === o ? s ? s[n] : t[i] : void(s ? s.scrollTo(r ? e.pageXOffset : o, r ? o : e.pageYOffset) : t[i] = o)
                }, t, i, arguments.length, null)
            }
        }), Z.each(["top", "left"], function(e, t) {
            Z.cssHooks[t] = T(Q.pixelPosition, function(e, n) {
                return n ? (n = w(e, t), Be.test(n) ? Z(e).position()[t] + "px" : n) : void 0
            })
        }), Z.each({
            Height: "height",
            Width: "width"
        }, function(e, t) {
            Z.each({
                padding: "inner" + e,
                content: t,
                "": "outer" + e
            }, function(n, r) {
                Z.fn[r] = function(r, i) {
                    var o = arguments.length && (n || "boolean" != typeof r),
                        s = n || (r === !0 || i === !0 ? "margin" : "border");
                    return me(this, function(t, n, r) {
                        var i;
                        return Z.isWindow(t) ? t.document.documentElement["client" + e] : 9 === t.nodeType ? (i = t.documentElement, Math.max(t.body["scroll" + e], i["scroll" + e], t.body["offset" + e], i["offset" + e], i["client" + e])) : void 0 === r ? Z.css(t, n, s) : Z.style(t, n, r, s)
                    }, t, o ? r : void 0, o, null)
                }
            })
        }), Z.fn.size = function() {
            return this.length
        }, Z.fn.andSelf = Z.fn.addBack, "function" == typeof define && define.amd && define("jquery", [], function() {
            return Z
        });
        var Pt = e.jQuery,
            Rt = e.$;
        return Z.noConflict = function(t) {
            return e.$ === Z && (e.$ = Rt), t && e.jQuery === Z && (e.jQuery = Pt), Z
        }, typeof t === Ee && (e.jQuery = e.$ = Z), Z
    }),
    function(e) {
        "use strict";

        function t(e, t, n, r) {
            return Math.abs(e - t) >= Math.abs(n - r) ? e - t > 0 ? "Left" : "Right" : n - r > 0 ? "Up" : "Down"
        }

        function n() {
            c = null, p.last && (p.el.trigger("longTap"), p = {})
        }

        function r() {
            c && clearTimeout(c), c = null
        }

        function i() {
            a && clearTimeout(a), u && clearTimeout(u), l && clearTimeout(l), c && clearTimeout(c), a = u = l = c = null, p = {}
        }

        function o(e) {
            return e = e.originalEvent || e, ("touch" == e.pointerType || e.pointerType == e.MSPOINTER_TYPE_TOUCH) && e.isPrimary
        }

        function s(e, t) {
            return e = e.originalEvent || e, e.type == "pointer" + t || e.type.toLowerCase() == "mspointer" + t
        }
        var a, u, l, c, f, p = {},
            d = 750;
        e(document).ready(function() {
            var h, g, m, v, y = 0,
                x = 0;
            "MSGesture" in window && (f = new MSGesture, f.target = document.body), e(document).bind("MSGestureEnd", function(e) {
                var e = e.originalEvent || e,
                    t = e.velocityX > 1 ? "Right" : e.velocityX < -1 ? "Left" : e.velocityY > 1 ? "Down" : e.velocityY < -1 ? "Up" : null;
                t && (p.el.trigger("swipe"), p.el.trigger("swipe" + t))
            }).on("touchstart MSPointerDown pointerdown", function(t) {
                t = t.originalEvent || t, (!(v = s(t, "down")) || o(t)) && (m = v ? t : t.touches[0], t.touches && 1 === t.touches.length && p.x2 && (p.x2 = void 0, p.y2 = void 0), h = Date.now(), g = h - (p.last || h), p.el = e("tagName" in m.target ? m.target : m.target.parentNode), a && clearTimeout(a), p.x1 = m.pageX, p.y1 = m.pageY, g > 0 && 250 >= g && (p.isDoubleTap = !0), p.last = h, c = setTimeout(n, d), f && v && f.addPointer(t.pointerId))
            }).on("touchmove MSPointerMove pointermove", function(e) {
                e = e.originalEvent || e, (!(v = s(e, "move")) || o(e)) && (m = v ? e : e.touches[0], r(), p.x2 = m.pageX, p.y2 = m.pageY, y += Math.abs(p.x1 - p.x2), x += Math.abs(p.y1 - p.y2))
            }).on("touchend MSPointerUp pointerup", function(n) {
                n = n.originalEvent || n, (!(v = s(n, "up")) || o(n)) && (r(), p.x2 && Math.abs(p.x1 - p.x2) > 30 || p.y2 && Math.abs(p.y1 - p.y2) > 30 ? l = setTimeout(function() {
                    p.el.trigger("swipe"), p.el.trigger("swipe" + t(p.x1, p.x2, p.y1, p.y2)), p = {}
                }, 0) : "last" in p && (30 > y && 30 > x ? u = setTimeout(function() {
                    var t = e.Event("tap");
                    t.cancelTouch = i, p.el.trigger(t), p.isDoubleTap ? (p.el && p.el.trigger("doubleTap"), p = {}) : a = setTimeout(function() {
                        a = null, p.el && p.el.trigger("singleTap"), p = {}
                    }, 250)
                }, 0) : p = {}), y = x = 0)
            }).on("touchcancel MSPointerCancel pointercancel", i), e(window).on("scroll", i)
        }), ["swipe", "swipeLeft", "swipeRight", "swipeUp", "swipeDown", "doubleTap", "tap", "singleTap", "longTap"].forEach(function(t) {
            e.fn[t] = function(e) {
                return this.on(t, e)
            }
        })
    }(jQuery), window.lofty && (jQuery.noConflict(), define("gallery/jquery/jquery-latest", function() {
        return jQuery
    }), lofty.config({
        alias: {
            jquery: "gallery/jquery/jquery-latest"
        }
    }));

function aliclick(e, t) {
    var n = "http://stat.1688.com/tracelog/click.html";
    return baseClick(n, t)
}

function etcclick(e, t) {
    var n = "http://stat.1688.com/etclistquery.html";
    return baseClick(n, t)
}

function eeclick(e, t) {
    var n = "http://stat.1688.com/ee.html";
    return baseClick(n, t)
}

function aliclickType(e, t) {
    var n = window.location.href;
    if (n) var i = n.substring(n.lastIndexOf("/") + 1, n.lastIndexOf("."));
    aliclick(e, t + "_" + i)
}

function baseClick(e, t) {
    var n = new Date;
    if (document.images) {
        var i = "//gm.mmstat.com" + aliClickMap[e];
        (new Image).src = i + "?gmkey=CLK&gokey=" + encodeURIComponent(t) + "&time=" + n.getTime()
    }
    return !0
}! function(e) {
    function t(t) {
        if (a.test(t)) {
            var n = e.Wing.navigator.getProductRoot("butterfly");
            return u.test(t) || (t += ".js"), n + "/vendor/" + t
        }
    }

    function n(e) {
        for (var t = 0, n = e.length; n > t; t++)
            if (!l.test(e[t])) return !1;
        return !0
    }

    function i(e, t) {
        if ("undefined" != typeof butterfly) return butterfly.require(e, t);
        var n = jQuery,
            i = [];
        n.each(e, function(e, t) {
            var o = n.Deferred(),
                a = u.test(t) ? "loadCss" : "loadJs";
            r[a](t, {
                success: o.resolve,
                error: o.resolve
            }), i.push(o)
        }), n.when.apply(n, i).done(function() {
            t()
        })
    }
    if (e.wingloader) throw new Error("wingloader already defined");
    var r = e.wingloader = {},
        o = !1;
    r.require = function(e, r) {
        "string" == typeof e && (e = [e]);
        var a = "undefined" != typeof lofty && "function" == typeof lofty.define,
            u = "undefined" != typeof butterfly;
        if (o || (o = !0, a ? lofty.config({
                resolve: function(e) {
                    return t(e, !0)
                }
            }) : u && butterfly.config("resolve", function(e) {
                return t(e)
            })), a) {
            if (n(e)) return i(e, r);
            var l = null;
            return lofty.define(e, function() {
                l = arguments[0], r && r.apply(null, arguments)
            }), l
        }
        if (u) return butterfly.require(e, r);
        throw new Error("no loader found")
    };
    var a = /^(wing-jsbridge|wingx)\//,
        u = /\.css(\?.*)?$/,
        l = /(^\w*:\/\/)|(^[.\/])/
}(window),
function(e) {
    function t(e, t) {
        var n = !1;
        setTimeout(function() {
            n || (n = !0, t.error && t.error())
        }, t.timeout || 1e4);
        var i = function() {
            var r = !1;
            try {
                r = !!e.sheet
            } catch (o) {
                r = d.test(o.message)
            }
            n || (r ? (n = !0, t.success && t.success()) : setTimeout(i, 20))
        };
        i()
    }

    function n(e, t, n, i, r) {
        e.onload = e.onreadystatechange = function(t) {
            t = t || window.event || {}, ("load" === t.type || f.test("" + e.readyState)) && (e.onload = e.onreadystatechange = e.onerror = null, n && p.removeChild(e), r && r(), i.success && i.success())
        }, e.onerror = function() {
            e.onload = e.onreadystatechange = e.onerror = null, i.error && i.error()
        }
    }

    function i(e) {
        h ? p.insertBefore(e, h) : p.appendChild(e)
    }
    var r = e.wingloader;
    r.loadJs = function(e, t) {
        t = t || {};
        var r = g.createElement("script");
        n(r, e, !0, t), r.async = "async", r.src = e, i(r)
    };
    var o = /.*webkit\/?(\d+)\..*/,
        a = /mobile/,
        u = window.navigator.userAgent.toLowerCase(),
        l = o.exec(u),
        s = l ? 1 * l[1] < 536 : !1,
        c = s || !l && a.test(u);
    r.loadCss = function(e, r) {
        r = r || {};
        var o = g.createElement("link");
        o.rel = "stylesheet", o.href = e, "onload" in o && !c ? n(o, e, !1, r) : setTimeout(function() {
            t(o, r)
        }, 1), i(o)
    };
    var d = /security|denied/i,
        f = /loaded|complete|undefined/,
        g = document,
        p = g.head || g.getElementsByTagName("head")[0] || g.documentElement,
        h = g.getElementsByTagName("base")[0]
}(window),
function(e) {
    var t = e.Wing || (e.Wing = {});
    if (t.lib) throw new Error("Wing.lib already defined");
    t.lib = {}, "undefined" != typeof e.wingloader ? t.lib.require = e.wingloader.require : console.warn("wingloader not specified"), t.navigator = t.navigator || {}, t.navigator.util = t.navigator.util || {}
}(window),
function(e) {
    var t = e.Wing.lib.lang = {},
        n = Object.prototype.toString;
    t.isObject = function(e) {
        return "[object Object]" === n.apply(e)
    }, t.extend = function() {
        for (var e = arguments, t = e[0], n = 1, i = e.length; i > n; n++) {
            var r = e[n];
            if (r)
                for (var o in r) {
                    var a = r[o];
                    void 0 !== a && (t[o] = a)
                }
        }
        return t
    }, t.param = function(e) {
        var t = [];
        for (var n in e) {
            var i = e[n];
            null !== i && void 0 !== i && t.push(n + "=" + encodeURIComponent(i))
        }
        return t.join("&")
    }, t.unserialize = function(e) {
        for (var t = {}, n = e.split("&"), i = 0, o = n.length; o > i; i++) r(t, n[i]);
        return t
    };
    var i = /^(?:([-\w]+)(\[([-\w]*)\])?)(?:=(.*))?$/,
        r = function(e, t) {
            var n = i.exec(t);
            if (n) {
                var r = n[1],
                    o = n[2],
                    a = n[3],
                    u = decodeURIComponent(n[4]);
                return o ? void(a ? (e[r] = e[r] || {}, e[r][a] = u) : (e[r] = e[r] || [], e[r].push(u))) : void(e[r] = u)
            }
        };
    t.formatUrl = function(e, n) {
        return n && (n = "string" == typeof n ? n : t.param(n), n && (e = e + (-1 === e.indexOf("?") ? "?" : "&") + n)), e
    }, t.format = function(e, t) {
        return e.replace(/\{(\w+)\}/g, function(e, n) {
            return void 0 !== t[n] ? t[n] : "{" + n + "}"
        })
    }, t.Class = function(e) {
        var n = function() {
            var e = this.initialize || this.init;
            return e && e.apply(this, arguments)
        };
        return t.extend(n.prototype, e), n
    }
}(window),
function(e) {
    function t(e, t) {
        var n = i.require("jquery"),
            r = [];
        n.each(t.js, function(e, t) {
            t.options && t.options.reload ? n.ajax({
                url: t.path,
                dataType: "script",
                crossDomain: !0
            }) : r.push(t.path)
        }), i.require(r, function() {
            n("body").trigger("wing-context-ready", e)
        })
    }
    var n = e.Wing;
    if (!n.config) throw new Error("Wing.config required");
    var i = n.lib,
        r = i.util = {};
    i.core = r, r.renderWingView = function(e, n, r) {
        var o = n.body || "",
            a = n.assets,
            u = a.css.map(function(e) {
                return e.path
            });
        i.require(u, function() {
            o && e.html(o), e.trigger("wing-content-change"), t(e, a), r && r()
        })
    }, r.antiShake = function(e, t) {
        var n = null;
        return function() {
            n || (n = setTimeout(function() {
                n = null
            }, t || 500), e.apply(this, arguments))
        }
    };
    var o = /(^\w*:\/\/)|(^[.\/])/,
        a = /^(?:([-\w]+)[:\/])?(page|module)s\/([-\w]+)\/([-\w]+)$/;
    r.regularProductUrl = function(e) {
        if (o.test(e)) return e;
        var t = a.exec(e);
        if (!t) throw new Error("invalid product url: " + e);
        var i = t[1] || n.config.productName,
            u = t[2],
            l = t[3],
            s = t[4];
        if (e = r.getProductUrl(i), !e) throw new Error("can not find product: [" + i + "]");
        return e = e + "/" + u + "/" + l, "view" !== s && (e += "/" + s), e + ".html"
    }
}(window),
function(e) {
    var t = e.Wing,
        n = t.lib.core,
        i = t.config.meta.server,
        r = t.config.meta.products;
    n.getAssetsRoot = function(e) {
        var t = r[e];
        return t && t.assetsRoot
    }, n.getProductUrl = function(e) {
        var t = r[e];
        if (!t) return null;
        if (t.productUrl) return t.productUrl;
        var n = t.domain;
        return i.port && "" + i.port != "80" && (n = n + ":" + i.port), "http://" + n
    }
}(window),
function(e) {
    function t(e, t) {
        if ("action" === e) {
            var n = t.data && t.data.__navigate__;
            if (n && "login" === n.type) {
                var i = Wing.navigator.getProductUrl("wap") + "/page/login.html?done=" + encodeURIComponent(window.location.href);
                return window.location.href = i, !0
            }
        }
    }

    function n(e) {
        var t = /complete|loaded|interactive/;
        return t.test(document.readyState) ? e() : document.addEventListener("DOMContentLoaded", e, !1)
    }
    var i = e.Wing.lib,
        r = i.lang,
        o = i.core,
        a = Wing.config;
    Wing.app = {};
    var u = Wing.app.productInfo = {
        name: a.productName,
        config: a.meta.config
    };
    Wing.app.view = function(e, t) {
        return c("view", s(e), t, function(e, t) {
            t.resolve(e.body, e)
        })
    }, Wing.app.render = function(e, t) {
        return c("render", s(e), t, function(e, t) {
            t.resolve(e.body, e)
        })
    }, Wing.app.action = function(e, t) {
        return c("action", s(e), t, function(e, t) {
            t.resolve(e.data)
        })
    }, Wing.app.url = function(e, t) {
        e = e && "/" !== e.charAt(0) ? "/" + e : e || "";
        var n = o.getProductUrl(u.name);
        return n + r.formatUrl(e, t)
    }, Wing.app.path = function(e) {
        return e = e && "/" !== e.charAt(0) ? "/" + e : e || "", o.getAssetsRoot(u.name) + e
    }, Wing.remote = {}, Wing.remote.view = function(e, t) {
        return c("view", e, t, function(e, t) {
            t.resolve(e.body, e)
        }, !0)
    }, Wing.remote.render = function(e, t) {
        return c("render", e, t, function(e, t) {
            t.resolve(e.body, e)
        }, !0)
    }, Wing.remote.action = function(e, t) {
        return c("action", e, t, function(e, t) {
            t.resolve(e.data)
        }, !0)
    }, Wing.app.redirect = function(e, t, n) {
        t === !0 && (n = !0, t = null);
        var i = /^(\w*:\/\/|\/)/;
        i.test(e) || (e = o.getProductUrl(u.name) + "/" + e), window.location.href = r.formatUrl(e, t)
    };
    var l = /^(?:\/?(pages|modules)[.\/])?([^.\/]+)(?:[.\/](.+))?$/,
        s = function(e) {
            if ("string" == typeof e) {
                var t = l.exec(e);
                if (!t) return null;
                e = {
                    "package": t[1],
                    module: t[2],
                    action: t[3]
                }
            }
            return e["package"] = e["package"] || "modules", e.action = e.action || "view", u.name + ":" + e["package"] + "/" + e.module + "/" + e.action
        },
        c = function(n, i, o, u, l) {
            var s = e.jQuery,
                c = s.Deferred();
            o = o || {};
            var d = o.data;
            "view" !== n || l || (d = r.extend({}, Wing.config.query, d));
            var f = {
                    data: d,
                    viewData: o.viewData
                },
                g = {
                    _csrf: a.meta.csrf,
                    __wing_navigate_type: n,
                    __wing_navigate_url: i,
                    __wing_navigate_options: JSON.stringify(f)
                };
            l && (g.__wing_navigate_remote = l);
            var p = window.location.href.replace(/\?.*$/, "");
            return s.ajax(p, {
                type: "view" === n ? "get" : "post",
                dataType: "json",
                cache: !1,
                data: g,
                success: function(e) {
                    if (e && "error" === e.type) c.reject(e);
                    else {
                        if (t(n, e)) return;
                        u(e, c)
                    }
                },
                error: function(e, t, n) {
                    var i = new Error(n);
                    i.status = e.status, i.statusText = t, i.errorThrown = n, i.responseText = e.responseText, c.reject(i)
                }
            }), c
        };
    Wing.ready = function(t) {
        var i = e.jQuery || e.af || n;
        i(function() {
            t(Wing.app)
        })
    }
}(window),
function(e) {
    var t = e.Wing,
        n = t.lib.core,
        i = t.navigator = {},
        r = /^https:/.test(location.href),
        o = /^(\w+)\/(.*)$/;
    i.getRealURL = function(e) {
        var t = o.exec(e);
        if (!t) throw new Error("invalid url paramter for getRealURL: " + e);
        var i = n.getAssetsRoot(t[1]);
        return i && i + "/" + t[2]
    }, i.getAssetsRoot = function(e) {
        return n.getAssetsRoot(e)
    }, i.getProductUrl = function(e) {
        return n.getProductUrl(e)
    }, i.rewrite = function(e, t) {
        return "URL" === e || "load" === e ? void(window.location.href = t) : "reload" === e ? void window.location.reload() : void 0
    }, i.post = function(e, i) {
        e = n.regularProductUrl(e), r && (e = e.replace(/^http:/, "https:").replace(/^\/\//, "https://"));
        var o = function(e) {
                return document.createElement(e)
            },
            a = o("form");
        document.getElementsByTagName("body")[0].appendChild(a), a.method = "post", a.action = e;
        var u = {
            _csrf: t.config.meta.csrf,
            __wing_navigate_post: JSON.stringify(i)
        };
        for (var l in u) {
            var s = o("input");
            s.type = "hidden", s.name = l, s.value = u[l], a.appendChild(s)
        }
        a.submit(), a.remove()
    }, i.tooltip = function(e) {
        var t = 3e3,
            n = null;
        define(["lofty/ui/popup/1.0/popup"], function(i) {
            n = new i({
                tpl: '<p id="toast_for_wap" style="display: block; background-color: #888;color: white;padding: 4px 10px;font-size: 12px;">' + e + "</p>",
                isModal: !1,
                y: document.documentElement.clientHeight - 100
            }), n.show(), setTimeout(function() {
                n.hide()
            }, t)
        })
    }
}(window),
function(e) {
    e.album = {
        photoPicker: function(e, t) {
            throw new Error("NotSupportError")
        },
        uploadWithDataImage: function(e) {
            if (e = e || {}, !e.memberId || !e.imageData) throw new Error("memberId and imageData required");
            var t = Wing.remote.action("loftyui:pages/album/upload", {
                    data: {
                        memberId: e.memberId,
                        imageData: e.imageData
                    }
                }),
                n = function(t) {
                    t = t || {};
                    var n = t.message || "ç½‘ç»œç¹å¿™, è¯·ç¨åŽé‡è¯•",
                        i = t.code || "service_error";
                    e.error && e.error({
                        message: n,
                        code: i
                    })
                };
            t.done(function(t) {
                t && t.success ? e.success && e.success(t.data) : n(t)
            }), t.fail(n)
        }
    }
}(Wing.navigator),
function(e) {
    var t = e.back = {},
        n = [],
        i = 0;
    t.listener = function(e) {
        n.push(e)
    }, t.go = function() {
        var e = n[i++];
        e ? e() : window.history.back()
    }, t.triggerBackListener = function() {
        i = 0, t.go()
    }, document.addEventListener("keydown", function(e) {
        e.ctrlKey && 188 === e.keyCode && t.triggerBackListener()
    }, !1)
}(Wing.navigator),
function(e) {
    function t() {
        e.back.listener(function() {
            History.back()
        }), History.Adapter.bind(window, "hashchange", function(e) {
            var t = e.oldURL;
            t && -1 !== t.indexOf("#wing") && o.trigger()
        })
    }
    var n = {},
        i = [],
        r = !1,
        o = e.history = {};
    o.push = function(e, o) {
        if (void 0 === n[e]) {
            r || (t(), r = !0), n[e] = i.length, i.push({
                name: e,
                fn: o
            });
            var a = "#wing" + (new Date).getTime();
            History.pushState(null, null, a)
        }
    }, o.remove = function(e) {
        void 0 !== n[e] && (i.splice(n[e], 1), delete n[e], History.back())
    }, o.trigger = function() {
        if (i.length) {
            var t = i.pop();
            delete n[t.name], t.fn()
        } else e.back.go()
    }
}(Wing.navigator),
function(e) {
    e.login = {
        getLoginInfo: function() {
            var e = Wing.config.meta.login;
            return {
                data: {
                    islogin: e.isLogin ? "true" : "false"
                }
            }
        }
    }
}(Wing.navigator),
function(e) {
    e.loginhelper = {
        doLogin: function() {
            var t = e.getProductUrl("wap") + "/page/login.html?done=" + encodeURIComponent(window.location.href);
            window.location.href = t
        }
    }
}(Wing.navigator),
function(e) {
    e.keyboard = {
        enter: function() {
            console.log("keyboard.enter()")
        }
    }
}(Wing.navigator),
function(e) {
    function t() {
        if (!s) {
            s = !0;
            var e = /#(native-ui-page-\d+)/;
            l.Adapter.bind(window, "hashchange", function(t) {
                var n = t.oldURL,
                    i = e.exec(n);
                if (i) {
                    var r = i[1];
                    a[r]("cancel"), l.busy(!1)
                }
            })
        }
    }
    var n = Wing.lib.lang,
        i = Wing.lib.core,
        r = function() {
            console.log.apply(console, arguments)
        };
    e.ui = {
        callback: function(e, t, n) {
            r("navigator.ui.callback", e, t, n)
        },
        open: function(e, t, n, r) {
            e = i.regularProductUrl(e);
            var o = new u(e, {
                query: t,
                finish: n,
                cancel: r
            });
            o.open()
        },
        finish: function(e) {
            this._complete("finish", e)
        },
        cancel: function() {
            this._complete("cancel")
        },
        _complete: function(e, t) {
            var n = window.parent.nativeUiPage;
            n && n[window.name] ? n[window.name](e, t) : alert(e)
        },
        setCloseAfterNewPage: function(e) {
            r("navigator.ui.setCloseAfterNewPage", e)
        }
    };
    var o = (new Date).getTime(),
        a = window.nativeUiPage = {},
        u = function(e, t) {
            this.url = e, this.options = t
        },
        l = window.History;
    u.prototype = {
        layout: function() {
            if (this.node && this.frame) {
                var e = window.jQuery,
                    t = e(window),
                    n = t.height(),
                    i = t.width();
                this.node.height(n).width(i), this.frame.height(n).width(i)
            }
        },
        open: function() {
            var e = window.jQuery,
                i = this,
                r = this.options || {},
                u = r.query,
                s = "native-ui-page-" + o++,
                c = u ? this.url + "?" + n.param(u) : this.url;
            e("body").append(n.format(this._tpl, {
                id: s,
                src: c
            }));
            var d = e("#wing-page-content");
            d.hide();
            var f = e("#" + s),
                g = e("iframe", f);
            this.node = f, this.frame = g, g[0].contentWindow.name = s, this.layout();
            var p = function() {
                i.layout()
            };
            e(window).on("resize", p), a[s] = function(t, n) {
                r[t] && r[t](n), e(window).off("resize", p), f.remove(), delete i.node, delete i.frame, delete a[s], d.show()
            }, l && (t(), l.pushState(null, null, "#" + s))
        },
        _tpl: '<div id="{id}" class="wing-native-mock-ui-page" style="position: fixed; left: 0; top: 0; width: 100%; height: 100%; z-index: 10000; background: #fff;"><iframe src="{src}" frameborder="0" scrolling="no" style="width: 100%; height: 100%;"></iframe></div>'
    };
    var s = !1;
    ! function() {
        var e = window.history;
        e.go;
        e.go = function() {}
    }(),
    function() {
        var t = /AlipayClient/.test(navigator.userAgent);
        if (t) {
            var i = e.ui;
            i.open = function(e, t, i, r) {
                e = t ? n.formatUrl(e, t) : e, window.location.href = e
            }, i.finish = function() {
                window.history.back()
            }, i.cancel = function() {
                window.history.back()
            }
        }
    }()
}(Wing.navigator),
function(e) {
    function t(e) {
        "function" == typeof aliclick && aliclick(null, "tracelog=" + encodeURIComponent(e))
    }
    e.uthandler = {
        pageProperties: function() {
            console.log("Wing.navigator.uthandler.pageProperties")
        },
        pageButtonClick: function(e, n, i) {
            t(e)
        },
        pageButtonClickExt: function(e, n) {
            t(e)
        }
    }
}(Wing.navigator),
function(e) {
    e.v5hole = {
        show: function() {
            console.log("Wing.navigator.v5hole.show")
        }
    }
}(Wing.navigator),
function(e) {
    e.v5share = {
        share: function() {
            var e, t = /\/offer\/(\d+)\.html?$/,
                n = /\/winport\/([-\w]+)\.html?$/,
                i = window.location,
                r = i.pathname;
            null !== (e = r.match(t)) ? i.href = "http://wap.m.1688.com/page/share.html?offerId=" + e[1] : null !== (e = r.match(n)) ? i.href = "http://wap.m.1688.com/page/share.html?memberId=" + e[1] : i.href = "http://wap.m.1688.com/page/share.html"
        }
    }
}(Wing.navigator),
function(e) {
    e.v5tool = {
        getUserID: function() {
            return Wing.config.meta.login.isLogin ? {
                data: {
                    userid: Wing.config.meta.login.userId
                }
            } : ""
        },
        getDeviceID: function() {
            return ""
        },
        createShortCut: function() {
            console.log("createShortCut")
        },
        saveContactInfo: function(e) {
            console.log("saveContactInfo", e)
        }
    }
}(Wing.navigator),
function(e) {
    e.view = {
        loadURL: function(e) {
            window.location = e
        }
    }
}(Wing.navigator),
function(e) {
    e.wangwang = {
        openWW: function() {
            var e, t = window.Wing.navigator.getProductUrl("wap") + "/page/wangwang.html",
                n = /\/offer\/(\d+)\.html?$/,
                i = /\/winport\/([-\w]+)\.html?$/,
                r = window.location,
                o = r.pathname;
            null !== (e = o.match(n)) ? r.href = t + "?offerId=" + e[1] : null !== (e = o.match(i)) ? r.href = t + "?memberId=" + e[1] : r.href = t
        },
        isUserLogin: function(e, t) {
            t({
                data: {
                    loginstatus: 1
                }
            })
        }
    }
}(Wing.navigator),
function(e) {
    e.device = {
        platform: "Wap"
    };
    var t = window.screen;
    e.device.screen = {
        width: t.width,
        height: t.height
    }
}(Wing.navigator),
function() {
    function e() {
        Wing.app.view = t(Wing.app.view), Wing.app.render = t(Wing.app.render), Wing.remote.view = t(Wing.remote.view), Wing.remote.render = t(Wing.remote.render)
    }

    function t(e) {
        return function(t, i) {
            i = i || {};
            var r = e(t, i);
            return i.container ? (r.done(function(e, t) {
                var r = n.require("jquery"),
                    o = r(i.container);
                n.core.renderWingView(o, t)
            }), r) : r
        }
    }
    var n = Wing.lib;
    Wing.ready(e)
}(),
function() {
    function e() {
        c || (c = !0, window.addEventListener("message", t))
    }

    function t(e) {
        var t = n(e.data);
        if (t) {
            var i = t.content;
            t.type === o ? u[i.name] && window._wingNativeEventOnHandler(i.name, i.dataString) : t.type === a && l[i.name] && window._wingNativeEventRequestHandler(i.name, i.dataString, i.reqid)
        }
    }

    function n(e) {
        if (e) try {
            var t = JSON.parse(e);
            if (t && t.wingnative && t.wingtoken !== s) return t
        } catch (n) {}
    }

    function i(e, t) {
        var n = {
            type: e,
            content: t,
            wingnative: !0,
            wingtoken: s
        };
        window.postMessage(JSON.stringify(n), "*")
    }
    var r = window._wingNative || (window._wingNative = {});
    if (!r.on || !r.trigger) {
        var o = "wingNativeOnEvent",
            a = "wingNativeResponseEvent",
            u = {},
            l = {},
            s = "wingtoken" + (new Date).getTime() + Math.floor(1e3 * Math.random());
        r.on = function() {
            u[name] = !0, e()
        };
        var c = !1;
        r.off = function(e) {
            delete u[e]
        }, r.trigger = function(e, t) {
            i(o, {
                name: e,
                dataString: t
            })
        }, r.request = function(t, n, r) {
            u[r] = !0, e();
            var o = {
                name: t,
                dataString: n,
                reqid: r
            };
            i(a, o)
        }, r.response = function(t) {
            l[t] = !0, e()
        }
    }
}(),
function() {
    function e(e) {
        if (void 0 !== e) {
            var t = JSON.stringify(e);
            return t = t.replace(/\\/g, "\\\\")
        }
    }

    function t(e) {
        return e + "|" + m++
    }

    function n(e, t) {
        return r(p, e, t)
    }

    function i(e, t) {
        return r(h, e, t)
    }

    function r(e, t, n) {
        for (var i = e[t] || (e[t] = []), r = 0, o = i.length; o > r; r++)
            if (i[r] === n) return;
        i.push(n);
        var a = v[t];
        return a && c(a.bus, a.name, a.params, !0), !0
    }

    function o(e, t) {
        n(e, t), w.on(e)
    }

    function a(e, t) {
        var n = p[e];
        if (!n) return !1;
        var i = !1;
        if (t) {
            for (var r = 0, o = n.length; o > r; r++)
                if (n[r] === t) {
                    n.splice(r, 1), i = !0;
                    break
                }
            0 === n.length && delete p[e]
        } else i = !0, delete p[e];
        return p[e] || w.off(e), i
    }

    function u(t, n) {
        n = void 0 === n ? {} : n, l(t, n), w.trigger(t, e(n))
    }

    function l(e, t) {
        c(p, e, [{
            data: t
        }])
    }

    function s(e, t, n) {
        c(h, e, [e, t, n])
    }

    function c(e, t, n, i) {
        i || (v[t] = {
            bus: e,
            name: t,
            params: n
        }, setTimeout(function() {
            delete v[t]
        }, 5e3));
        var r = e[t];
        if (r)
            for (var o = 0, a = r.length; a > o; o++) {
                var u = r[o].apply(null, n);
                if (u === !1) break
            }
    }

    function d(i, r) {
        r = r || {};
        var o = r.data,
            a = e(o),
            u = function(e) {
                r.success && r.success(e.data)
            },
            l = t(i);
        n(l, u), s(i, o, l), w.request(i, a, l)
    }

    function f(t, n) {
        var r = function(t, i, r) {
            var o = {
                    data: i
                },
                a = {
                    send: function(t) {
                        l(r, t), w.trigger(r, e(t))
                    }
                };
            n(o, a)
        };
        i(t, r), w.response(t)
    }
    var g = Wing.navigator,
        p = {},
        h = {},
        v = {},
        w = window._wingNative;
    window._wingNativeEventOnHandler = function(e, t) {
        try {
            t = JSON.parse(t || "{}")
        } catch (n) {
            return void console.error("call _wingNativeEventOnHandler param is invalid json: " + t)
        }
        l(e, t)
    }, window._wingNativeEventRequestHandler = function(e, t, n) {
        s(e, JSON.parse(t), n)
    };
    var m = 1;
    g.event = {
        on: o,
        off: a,
        trigger: u,
        request: d,
        response: f
    }
}(),
function(e) {
    function t(e) {
        var t = f("<div>", {
                id: r(e.id),
                "class": "wing-layout-layer-item",
                height: "100%"
            }),
            i = d.util.regularProductUrl(e.url),
            o = e.data || {};
        o._wingLayerId = e.id, i += "?" + d.lang.param(o);
        var a = n(i);
        t.append(a), u(t, e)
    }

    function n(e) {
        var t = f("<iframe>", {
            src: e,
            onload: "Wing.navigator.layouttemplate.layoutframe(this)",
            scrolling: "no",
            frameborder: "0",
            width: "100%",
            height: "100%"
        });
        return t
    }

    function i(e) {
        var t = Wing.app.view(e.url, {
            data: e.data
        });
        t.done(function(t, n) {
            var i = f("<div>", {
                id: r(e.id),
                "class": "wing-layout-layer-item"
            });
            d.core.renderWingView(i, n, function() {
                u(i, e)
            })
        })
    }

    function r(e) {
        return "wing-layout-layer-" + e.replace(/[^\w]/g, "-")
    }

    function o() {
        f = d.require("jquery");
        var e = f("div.wing-layout-layer"),
            t = f("div.wing-layout-layer-item", e);
        t.each(function() {
            var e = f(this),
                t = e.data("url");
            a(e, t, Wing.config.query)
        }), t.on("close", function() {
            e.append(f(this))
        })
    }

    function a(e, t, n) {
        var i = Wing.app.view(t, {
            data: n
        });
        i.done(function(t, n) {
            d.core.renderWingView(e, n)
        })
    }

    function u(e, t) {
        d.require(["lofty/ui/popup/1.0/popup"], function(n) {
            var i = new n({
                tpl: e,
                isModal: t.needMask,
                isMaskTouchHide: t.hideOnTouch
            });
            i.position = function() {
                s(i, t)
            };
            var r = i.hide;
            i.hide = function() {
                r.call(this), l(this)
            }, e.data("popup", i), i.show(), c(i)
        })
    }

    function l(t) {
        t.get("el").trigger("close"), t.get("contentLyr").remove();
        var n = t.get("maskElment");
        n && n.remove(), e.history.remove("showlayer")
    }

    function s(e, t) {
        var n = e.get("contentLyr"),
            i = t.width,
            r = t.height,
            o = "percent" === t.unit,
            a = f(window),
            u = {};
        u.left = 0, i ? (i = o ? Math.round(a.width() * i / 100) : i, u.width = i + "px") : u.width = "100%", !t.autoheight && r && (r = o ? Math.round(a.height() * r / 100) : r, u.height = r + "px");
        var l = t.align;
        if (n.addClass("wing-layer-popup wing-layer-popup-" + l), "top" === l) u.top = "0", u.bottom = "auto";
        else if ("bottom" === l) u.top = "auto", u.bottom = "0";
        else {
            var s = parseInt(u.height, 10) || e.get("el").height();
            u.top = (a.height() - s) / 2
        }
        n.css(u)
    }

    function c(t) {
        var n = t.get("contentLyr");
        f("body").trigger("wing-layout-ready", {
            container: n,
            height: n.height()
        }), "Wap" === e.device.platform || e.history.push("showlayer", function() {
            t.hide()
        })
    }
    if (!e.ui || !e.ui.layer) {
        var d = Wing.lib,
            f = null;
        Wing.ready(o), e.ui.layer = {
            mock: !0,
            open: function(e) {
                if (e.url) return e.frame ? t(e) : i(e);
                if (e.id) {
                    var n = f("#" + r(e.id));
                    return void(n.length && u(n, e))
                }
                throw new Error("options.id or options.url is required")
            },
            close: function(e) {
                if (!e) throw new Error("id required");
                if (window !== window.parent) return window.parent.Wing.navigator.ui.layer.close(e);
                var t = f("#" + r(e)),
                    n = t.data("popup");
                n && n.hide()
            },
            reposition: function(e) {
                var t = f("#" + r(e)),
                    n = t.data("popup");
                n && n.position()
            }
        }
    }
}(Wing.navigator),
function(e) {
    function t(t) {
        t.url && (t.id = "wing-dialog-" + s++), c = t.id;
        var n = !t.url;
        if (n && e.event.trigger("wing-layer-open." + t.id, t), t.onClose || t.onFinish || t.onCancel) {
            var i = "wing-layer-close." + t.id;
            e.event.off(i), e.event.on(i, function(n) {
                e.event.off(i);
                var r = n.data,
                    o = t[l[r.type]];
                o && o(r.data)
            })
        }
        if (!u && t.autoheight && !t.url) return void e.event.trigger("wing-layer-open-do." + t.id, t);
        if (u && t.autoheight && (t.height = null), !u && t.url) {
            var r = t.data || {};
            t.url += "?" + a.param(r), delete t.data
        }
        e.ui.layer.open(t)
    }

    function n(t) {
        return function(n, i) {
            if (a.isObject(n) && (i = n, n = null), !n && (n = Wing.config.query._wingLayerId || u && c, !n)) throw new Error("dialog id is required for close");
            var r = {
                type: t,
                data: i
            };
            e.ui.layer.close(n), setTimeout(function() {
                e.event.trigger("wing-layer-close." + n, r)
            }, 300)
        }
    }

    function i() {
        var t = u ? c : Wing.config.query._wingLayerId;
        e.ui.layer.reposition(t)
    }

    function r() {
        if (!u) {
            var t = Wing.config.query._wingLayerId;
            if (t && "default" !== t) {
                var n = o.require("jquery"),
                    i = "wing-layer-open-do." + t;
                e.event.on(i, function(t) {
                    var i = t.data;
                    i.autoheight && (i.height = n("#wing-page-content").height(), i.unit = null), e.ui.layer.open(i)
                })
            }
        }
    }
    var o = Wing.lib,
        a = Wing.lib.lang,
        u = e.ui.layer.mock;
    e.ui.dialog = {
        open: function(e) {
            var n = a.extend({
                needMask: !0,
                hideOnTouch: !0,
                align: "bottom",
                height: 300
            }, e);
            t(n)
        },
        reposition: function() {
            i()
        },
        close: n("close"),
        finish: n("finish"),
        cancel: n("cancel")
    }, e.ui.menu = {
        open: function(e) {
            var n = a.extend({
                y: e.top,
                x: e.left,
                needMask: !1,
                align: "position"
            }, e);
            t(n)
        },
        close: e.ui.dialog.close,
        finish: e.ui.dialog.finish,
        cancel: e.ui.dialog.cancel
    };
    var l = {
            close: "onClose",
            finish: "onFinish",
            cancel: "onCancel"
        },
        s = 1,
        c = null;
    t = o.util.antiShake(t, 2e3), Wing.ready(r)
}(Wing.navigator);
var aliClickMap = {
    "http://stat.1688.com/tracelog/click.html": "/btob.6",
    "http://stat.1688.com/etclistquery.html": "/btob.2",
    "http://stat.1688.com/ee.html": "/btob.17"
};
! function(e, t) {
    "use strict";
    var n = e.console || t,
        i = e.document,
        r = e.navigator,
        o = !1,
        a = e.setTimeout,
        u = e.clearTimeout,
        l = e.setInterval,
        s = e.clearInterval,
        c = e.JSON,
        d = e.alert,
        f = e.History = e.History || {},
        g = e.history;
    try {
        o = e.sessionStorage, o.setItem("TEST", "1"), o.removeItem("TEST")
    } catch (p) {
        o = !1
    }
    if (c.stringify = c.stringify || c.encode, c.parse = c.parse || c.decode, "undefined" != typeof f.init) throw new Error("History.js Core has already been loaded...");
    f.init = function(e) {
        return "undefined" == typeof f.Adapter ? !1 : ("undefined" != typeof f.initCore && f.initCore(), "undefined" != typeof f.initHtml4 && f.initHtml4(), !0)
    }, f.initCore = function(p) {
        if ("undefined" != typeof f.initCore.initialized) return !1;
        if (f.initCore.initialized = !0, f.options = f.options || {}, f.options.hashChangeInterval = f.options.hashChangeInterval || 100, f.options.safariPollInterval = f.options.safariPollInterval || 500, f.options.doubleCheckInterval = f.options.doubleCheckInterval || 500, f.options.disableSuid = f.options.disableSuid || !1, f.options.storeInterval = f.options.storeInterval || 1e3, f.options.busyDelay = f.options.busyDelay || 250, f.options.debug = f.options.debug || !1, f.options.initialTitle = f.options.initialTitle || i.title, f.options.html4Mode = f.options.html4Mode || !1, f.options.delayInit = f.options.delayInit || !1, f.intervalList = [], f.clearAllIntervals = function() {
                var e, t = f.intervalList;
                if ("undefined" != typeof t && null !== t) {
                    for (e = 0; e < t.length; e++) s(t[e]);
                    f.intervalList = null
                }
            }, f.debug = function() {
                f.options.debug && f.log.apply(f, arguments)
            }, f.log = function() {
                var e, t, r, o, a, u = !("undefined" == typeof n || "undefined" == typeof n.log || "undefined" == typeof n.log.apply),
                    l = i.getElementById("log");
                for (u ? (o = Array.prototype.slice.call(arguments), e = o.shift(), "undefined" != typeof n.debug ? n.debug.apply(n, [e, o]) : n.log.apply(n, [e, o])) : e = "\n" + arguments[0] + "\n", t = 1, r = arguments.length; r > t; ++t) {
                    if (a = arguments[t], "object" == typeof a && "undefined" != typeof c) try {
                        a = c.stringify(a)
                    } catch (s) {}
                    e += "\n" + a + "\n"
                }
                return l ? (l.value += e + "\n-----\n", l.scrollTop = l.scrollHeight - l.clientHeight) : u || d(e), !0
            }, f.getInternetExplorerMajorVersion = function() {
                var e = f.getInternetExplorerMajorVersion.cached = "undefined" != typeof f.getInternetExplorerMajorVersion.cached ? f.getInternetExplorerMajorVersion.cached : function() {
                    for (var e = 3, t = i.createElement("div"), n = t.getElementsByTagName("i");
                        (t.innerHTML = "<!--[if gt IE " + ++e + "]><i></i><![endif]-->") && n[0];);
                    return e > 4 ? e : !1
                }();
                return e
            }, f.isInternetExplorer = function() {
                var e = f.isInternetExplorer.cached = "undefined" != typeof f.isInternetExplorer.cached ? f.isInternetExplorer.cached : Boolean(f.getInternetExplorerMajorVersion());
                return e
            }, f.options.html4Mode ? f.emulated = {
                pushState: !0,
                hashChange: !0
            } : f.emulated = {
                pushState: !Boolean(e.history && e.history.pushState && e.history.replaceState && !(/ Mobile\/([1-7][a-z]|(8([abcde]|f(1[0-8]))))/i.test(r.userAgent) || /AppleWebKit\/5([0-2]|3[0-2])/i.test(r.userAgent))),
                hashChange: Boolean(!("onhashchange" in e || "onhashchange" in i) || f.isInternetExplorer() && f.getInternetExplorerMajorVersion() < 8)
            }, f.enabled = !f.emulated.pushState, f.bugs = {
                setHash: Boolean(!f.emulated.pushState && "Apple Computer, Inc." === r.vendor && /AppleWebKit\/5([0-2]|3[0-3])/.test(r.userAgent)),
                safariPoll: Boolean(!f.emulated.pushState && "Apple Computer, Inc." === r.vendor && /AppleWebKit\/5([0-2]|3[0-3])/.test(r.userAgent)),
                ieDoubleCheck: Boolean(f.isInternetExplorer() && f.getInternetExplorerMajorVersion() < 8),
                hashEscape: Boolean(f.isInternetExplorer() && f.getInternetExplorerMajorVersion() < 7)
            }, f.isEmptyObject = function(e) {
                for (var t in e)
                    if (e.hasOwnProperty(t)) return !1;
                return !0
            }, f.cloneObject = function(e) {
                var t, n;
                return e ? (t = c.stringify(e), n = c.parse(t)) : n = {}, n
            }, f.getRootUrl = function() {
                var e = i.location.protocol + "//" + (i.location.hostname || i.location.host);
                return i.location.port && (e += ":" + i.location.port), e += "/"
            }, f.getBaseHref = function() {
                var e = i.getElementsByTagName("base"),
                    t = null,
                    n = "";
                return 1 === e.length && (t = e[0], n = t.href.replace(/[^\/]+$/, "")), n = n.replace(/\/+$/, ""), n && (n += "/"), n
            }, f.getBaseUrl = function() {
                var e = f.getBaseHref() || f.getBasePageUrl() || f.getRootUrl();
                return e
            }, f.getPageUrl = function() {
                var e, t = f.getState(!1, !1),
                    n = (t || {}).url || f.getLocationHref();
                return e = n.replace(/\/+$/, "").replace(/[^\/]+$/, function(e, t, n) {
                    return /\./.test(e) ? e : e + "/"
                })
            }, f.getBasePageUrl = function() {
                var e = f.getLocationHref().replace(/[#\?].*/, "").replace(/[^\/]+$/, function(e, t, n) {
                    return /[^\/]$/.test(e) ? "" : e
                }).replace(/\/+$/, "") + "/";
                return e
            }, f.getFullUrl = function(e, t) {
                var n = e,
                    i = e.substring(0, 1);
                return t = "undefined" == typeof t ? !0 : t, /[a-z]+\:\/\//.test(e) || (n = "/" === i ? f.getRootUrl() + e.replace(/^\/+/, "") : "#" === i ? f.getPageUrl().replace(/#.*/, "") + e : "?" === i ? f.getPageUrl().replace(/[\?#].*/, "") + e : t ? f.getBaseUrl() + e.replace(/^(\.\/)+/, "") : f.getBasePageUrl() + e.replace(/^(\.\/)+/, "")), n.replace(/\#$/, "")
            }, f.getShortUrl = function(e) {
                var t = e,
                    n = f.getBaseUrl(),
                    i = f.getRootUrl();
                return f.emulated.pushState && (t = t.replace(n, "")), t = t.replace(i, "/"), f.isTraditionalAnchor(t) && (t = "./" + t), t = t.replace(/^(\.\/)+/g, "./").replace(/\#$/, "")
            }, f.getLocationHref = function(e) {
                return e = e || i, e.URL === e.location.href ? e.location.href : e.location.href === decodeURIComponent(e.URL) ? e.URL : e.location.hash && decodeURIComponent(e.location.href.replace(/^[^#]+/, "")) === e.location.hash ? e.location.href : -1 == e.URL.indexOf("#") && -1 != e.location.href.indexOf("#") ? e.location.href : e.URL || e.location.href
            }, f.store = {}, f.idToState = f.idToState || {}, f.stateToId = f.stateToId || {}, f.urlToId = f.urlToId || {}, f.storedStates = f.storedStates || [], f.savedStates = f.savedStates || [], f.normalizeStore = function() {
                f.store.idToState = f.store.idToState || {}, f.store.urlToId = f.store.urlToId || {}, f.store.stateToId = f.store.stateToId || {}
            }, f.getState = function(e, t) {
                "undefined" == typeof e && (e = !0), "undefined" == typeof t && (t = !0);
                var n = f.getLastSavedState();
                return !n && t && (n = f.createStateObject()), e && (n = f.cloneObject(n), n.url = n.cleanUrl || n.url), n
            }, f.getIdByState = function(e) {
                var t, n = f.extractId(e.url);
                if (!n)
                    if (t = f.getStateString(e), "undefined" != typeof f.stateToId[t]) n = f.stateToId[t];
                    else if ("undefined" != typeof f.store.stateToId[t]) n = f.store.stateToId[t];
                else {
                    for (;;)
                        if (n = (new Date).getTime() + String(Math.random()).replace(/\D/g, ""), "undefined" == typeof f.idToState[n] && "undefined" == typeof f.store.idToState[n]) break;
                    f.stateToId[t] = n, f.idToState[n] = e
                }
                return n
            }, f.normalizeState = function(e) {
                var t, n;
                return e && "object" == typeof e || (e = {}), "undefined" != typeof e.normalized ? e : (e.data && "object" == typeof e.data || (e.data = {}), t = {}, t.normalized = !0, t.title = e.title || "", t.url = f.getFullUrl(e.url ? e.url : f.getLocationHref()), t.hash = f.getShortUrl(t.url), t.data = f.cloneObject(e.data), t.id = f.getIdByState(t), t.cleanUrl = t.url.replace(/\??\&_suid.*/, ""), t.url = t.cleanUrl, n = !f.isEmptyObject(t.data), (t.title || n) && f.options.disableSuid !== !0 && (t.hash = f.getShortUrl(t.url).replace(/\??\&_suid.*/, ""), /\?/.test(t.hash) || (t.hash += "?"), t.hash += "&_suid=" + t.id), t.hashedUrl = f.getFullUrl(t.hash), (f.emulated.pushState || f.bugs.safariPoll) && f.hasUrlDuplicate(t) && (t.url = t.hashedUrl), t)
            }, f.createStateObject = function(e, t, n) {
                var i = {
                    data: e,
                    title: t,
                    url: n
                };
                return i = f.normalizeState(i)
            }, f.getStateById = function(e) {
                e = String(e);
                var n = f.idToState[e] || f.store.idToState[e] || t;
                return n
            }, f.getStateString = function(e) {
                var t, n, i;
                return t = f.normalizeState(e), n = {
                    data: t.data,
                    title: e.title,
                    url: e.url
                }, i = c.stringify(n)
            }, f.getStateId = function(e) {
                var t, n;
                return t = f.normalizeState(e), n = t.id
            }, f.getHashByState = function(e) {
                var t, n;
                return t = f.normalizeState(e), n = t.hash
            }, f.extractId = function(e) {
                var t, n, i, r;
                return r = -1 != e.indexOf("#") ? e.split("#")[0] : e, n = /(.*)\&_suid=([0-9]+)$/.exec(r), i = n ? n[1] || e : e, t = n ? String(n[2] || "") : "", t || !1
            }, f.isTraditionalAnchor = function(e) {
                var t = !/[\/\?\.]/.test(e);
                return t
            }, f.extractState = function(e, t) {
                var n, i, r = null;
                return t = t || !1, n = f.extractId(e), n && (r = f.getStateById(n)), r || (i = f.getFullUrl(e), n = f.getIdByUrl(i) || !1, n && (r = f.getStateById(n)), r || !t || f.isTraditionalAnchor(e) || (r = f.createStateObject(null, null, i))), r
            }, f.getIdByUrl = function(e) {
                var n = f.urlToId[e] || f.store.urlToId[e] || t;
                return n
            }, f.getLastSavedState = function() {
                return f.savedStates[f.savedStates.length - 1] || t
            }, f.getLastStoredState = function() {
                return f.storedStates[f.storedStates.length - 1] || t
            }, f.hasUrlDuplicate = function(e) {
                var t, n = !1;
                return t = f.extractState(e.url), n = t && t.id !== e.id
            }, f.storeState = function(e) {
                return f.urlToId[e.url] = e.id, f.storedStates.push(f.cloneObject(e)), e
            }, f.isLastSavedState = function(e) {
                var t, n, i, r = !1;
                return f.savedStates.length && (t = e.id, n = f.getLastSavedState(), i = n.id, r = t === i), r
            }, f.saveState = function(e) {
                return f.isLastSavedState(e) ? !1 : (f.savedStates.push(f.cloneObject(e)), !0)
            }, f.getStateByIndex = function(e) {
                var t = null;
                return t = "undefined" == typeof e ? f.savedStates[f.savedStates.length - 1] : 0 > e ? f.savedStates[f.savedStates.length + e] : f.savedStates[e]
            }, f.getCurrentIndex = function() {
                var e = null;
                return e = f.savedStates.length < 1 ? 0 : f.savedStates.length - 1
            }, f.getHash = function(e) {
                var t, n = f.getLocationHref(e);
                return t = f.getHashByUrl(n)
            }, f.unescapeHash = function(e) {
                var t = f.normalizeHash(e);
                return t = decodeURIComponent(t)
            }, f.normalizeHash = function(e) {
                var t = e.replace(/[^#]*#/, "").replace(/#.*/, "");
                return t
            }, f.setHash = function(e, t) {
                var n, r;
                return t !== !1 && f.busy() ? (f.pushQueue({
                    scope: f,
                    callback: f.setHash,
                    args: arguments,
                    queue: t
                }), !1) : (f.busy(!0), n = f.extractState(e, !0), n && !f.emulated.pushState ? f.pushState(n.data, n.title, n.url, !1) : f.getHash() !== e && (f.bugs.setHash ? (r = f.getPageUrl(), f.pushState(null, null, r + "#" + e, !1)) : i.location.hash = e), f)
            }, f.escapeHash = function(t) {
                var n = f.normalizeHash(t);
                return n = e.encodeURIComponent(n), f.bugs.hashEscape || (n = n.replace(/\%21/g, "!").replace(/\%26/g, "&").replace(/\%3D/g, "=").replace(/\%3F/g, "?")), n
            }, f.getHashByUrl = function(e) {
                var t = String(e).replace(/([^#]*)#?([^#]*)#?(.*)/, "$2");
                return t = f.unescapeHash(t)
            }, f.setTitle = function(e) {
                var t, n = e.title;
                n || (t = f.getStateByIndex(0), t && t.url === e.url && (n = t.title || f.options.initialTitle));
                try {
                    i.getElementsByTagName("title")[0].innerHTML = n.replace("<", "&lt;").replace(">", "&gt;").replace(" & ", " &amp; ");
                } catch (r) {}
                return i.title = n, f
            }, f.queues = [], f.busy = function(e) {
                if ("undefined" != typeof e ? f.busy.flag = e : "undefined" == typeof f.busy.flag && (f.busy.flag = !1), !f.busy.flag) {
                    u(f.busy.timeout);
                    var t = function() {
                        var e, n, i;
                        if (!f.busy.flag)
                            for (e = f.queues.length - 1; e >= 0; --e) n = f.queues[e], 0 !== n.length && (i = n.shift(), f.fireQueueItem(i), f.busy.timeout = a(t, f.options.busyDelay))
                    };
                    f.busy.timeout = a(t, f.options.busyDelay)
                }
                return f.busy.flag
            }, f.busy.flag = !1, f.fireQueueItem = function(e) {
                return e.callback.apply(e.scope || f, e.args || [])
            }, f.pushQueue = function(e) {
                return f.queues[e.queue || 0] = f.queues[e.queue || 0] || [], f.queues[e.queue || 0].push(e), f
            }, f.queue = function(e, t) {
                return "function" == typeof e && (e = {
                    callback: e
                }), "undefined" != typeof t && (e.queue = t), f.busy() ? f.pushQueue(e) : f.fireQueueItem(e), f
            }, f.clearQueue = function() {
                return f.busy.flag = !1, f.queues = [], f
            }, f.stateChanged = !1, f.doubleChecker = !1, f.doubleCheckComplete = function() {
                return f.stateChanged = !0, f.doubleCheckClear(), f
            }, f.doubleCheckClear = function() {
                return f.doubleChecker && (u(f.doubleChecker), f.doubleChecker = !1), f
            }, f.doubleCheck = function(e) {
                return f.stateChanged = !1, f.doubleCheckClear(), f.bugs.ieDoubleCheck && (f.doubleChecker = a(function() {
                    return f.doubleCheckClear(), f.stateChanged || e(), !0
                }, f.options.doubleCheckInterval)), f
            }, f.safariStatePoll = function() {
                var t, n = f.extractState(f.getLocationHref());
                if (!f.isLastSavedState(n)) return t = n, t || (t = f.createStateObject()), f.Adapter.trigger(e, "popstate"), f
            }, f.back = function(e) {
                return e !== !1 && f.busy() ? (f.pushQueue({
                    scope: f,
                    callback: f.back,
                    args: arguments,
                    queue: e
                }), !1) : (f.busy(!0), f.doubleCheck(function() {
                    f.back(!1)
                }), g.go(-1), !0)
            }, f.forward = function(e) {
                return e !== !1 && f.busy() ? (f.pushQueue({
                    scope: f,
                    callback: f.forward,
                    args: arguments,
                    queue: e
                }), !1) : (f.busy(!0), f.doubleCheck(function() {
                    f.forward(!1)
                }), g.go(1), !0)
            }, f.go = function(e, t) {
                var n;
                if (e > 0)
                    for (n = 1; e >= n; ++n) f.forward(t);
                else {
                    if (!(0 > e)) throw new Error("History.go: History.go requires a positive or negative integer passed.");
                    for (n = -1; n >= e; --n) f.back(t)
                }
                return f
            }, f.emulated.pushState) {
            var h = function() {};
            f.pushState = f.pushState || h, f.replaceState = f.replaceState || h
        } else f.onPopState = function(t, n) {
            var i, r, o = !1,
                a = !1;
            return f.doubleCheckComplete(), (i = f.getHash()) ? (r = f.extractState(i || f.getLocationHref(), !0), r ? f.replaceState(r.data, r.title, r.url, !1) : (f.Adapter.trigger(e, "anchorchange"), f.busy(!1)), f.expectedStateId = !1, !1) : (o = f.Adapter.extractEventData("state", t, n) || !1, a = o ? f.getStateById(o) : f.expectedStateId ? f.getStateById(f.expectedStateId) : f.extractState(f.getLocationHref()), a || (a = f.createStateObject(null, null, f.getLocationHref())), f.expectedStateId = !1, f.isLastSavedState(a) ? (f.busy(!1), !1) : (f.storeState(a), f.saveState(a), f.setTitle(a), f.Adapter.trigger(e, "statechange"), f.busy(!1), !0))
        }, f.Adapter.bind(e, "popstate", f.onPopState), f.pushState = function(t, n, i, r) {
            if (f.getHashByUrl(i) && f.emulated.pushState) throw new Error("History.js does not support states with fragement-identifiers (hashes/anchors).");
            if (r !== !1 && f.busy()) return f.pushQueue({
                scope: f,
                callback: f.pushState,
                args: arguments,
                queue: r
            }), !1;
            f.busy(!0);
            var o = f.createStateObject(t, n, i);
            return f.isLastSavedState(o) ? f.busy(!1) : (f.storeState(o), f.expectedStateId = o.id, g.pushState(o.id, o.title, o.url), f.Adapter.trigger(e, "popstate")), !0
        }, f.replaceState = function(t, n, i, r) {
            if (f.getHashByUrl(i) && f.emulated.pushState) throw new Error("History.js does not support states with fragement-identifiers (hashes/anchors).");
            if (r !== !1 && f.busy()) return f.pushQueue({
                scope: f,
                callback: f.replaceState,
                args: arguments,
                queue: r
            }), !1;
            f.busy(!0);
            var o = f.createStateObject(t, n, i);
            return f.isLastSavedState(o) ? f.busy(!1) : (f.storeState(o), f.expectedStateId = o.id, g.replaceState(o.id, o.title, o.url), f.Adapter.trigger(e, "popstate")), !0
        };
        if (o) {
            try {
                f.store = c.parse(o.getItem("History.store")) || {}
            } catch (v) {
                f.store = {}
            }
            f.normalizeStore()
        } else f.store = {}, f.normalizeStore();
        f.Adapter.bind(e, "unload", f.clearAllIntervals), f.saveState(f.storeState(f.extractState(f.getLocationHref(), !0))), o && (f.onUnload = function() {
            var e, t, n;
            try {
                e = c.parse(o.getItem("History.store")) || {}
            } catch (i) {
                e = {}
            }
            e.idToState = e.idToState || {}, e.urlToId = e.urlToId || {}, e.stateToId = e.stateToId || {};
            for (t in f.idToState) f.idToState.hasOwnProperty(t) && (e.idToState[t] = f.idToState[t]);
            for (t in f.urlToId) f.urlToId.hasOwnProperty(t) && (e.urlToId[t] = f.urlToId[t]);
            for (t in f.stateToId) f.stateToId.hasOwnProperty(t) && (e.stateToId[t] = f.stateToId[t]);
            f.store = e, f.normalizeStore(), n = c.stringify(e);
            try {
                o.setItem("History.store", n)
            } catch (r) {
                if (r.code !== DOMException.QUOTA_EXCEEDED_ERR) throw r;
                o.length && (o.removeItem("History.store"), o.setItem("History.store", n))
            }
        }, f.intervalList.push(l(f.onUnload, f.options.storeInterval)), f.Adapter.bind(e, "beforeunload", f.onUnload), f.Adapter.bind(e, "unload", f.onUnload)), f.emulated.pushState || (f.bugs.safariPoll && f.intervalList.push(l(f.safariStatePoll, f.options.safariPollInterval)), ("Apple Computer, Inc." === r.vendor || "Mozilla" === (r.appCodeName || "")) && (f.Adapter.bind(e, "hashchange", function() {
            f.Adapter.trigger(e, "popstate")
        }), f.getHash() && f.Adapter.onDomLoad(function() {
            f.Adapter.trigger(e, "hashchange")
        })))
    }, f.options && f.options.delayInit || f.init()
}(window),
function(e, t) {
    "use strict";
    var n = e.History = e.History || {};
    if ("undefined" != typeof n.Adapter) throw new Error("History.js Adapter has already been loaded...");
    n.Adapter = {
        handlers: {},
        _uid: 1,
        uid: function(e) {
            return e._uid || (e._uid = n.Adapter._uid++)
        },
        bind: function(e, t, i) {
            var r = n.Adapter.uid(e);
            n.Adapter.handlers[r] = n.Adapter.handlers[r] || {}, n.Adapter.handlers[r][t] = n.Adapter.handlers[r][t] || [], n.Adapter.handlers[r][t].push(i), e["on" + t] = function(e, t) {
                return function(i) {
                    n.Adapter.trigger(e, t, i)
                }
            }(e, t)
        },
        trigger: function(e, t, i) {
            i = i || {};
            var r, o, a = n.Adapter.uid(e);
            for (n.Adapter.handlers[a] = n.Adapter.handlers[a] || {}, n.Adapter.handlers[a][t] = n.Adapter.handlers[a][t] || [], r = 0, o = n.Adapter.handlers[a][t].length; o > r; ++r) n.Adapter.handlers[a][t][r].apply(this, [i])
        },
        extractEventData: function(e, n) {
            var i = n && n[e] || t;
            return i
        },
        onDomLoad: function(t) {
            var n = e.setTimeout(function() {
                t()
            }, 2e3);
            e.onload = function() {
                clearTimeout(n), t()
            }
        }
    }, "undefined" != typeof n.init && n.init()
}(window);
var xloader = function(e) {
    function t(i) {
        if (n[i]) return n[i].exports;
        var r = n[i] = {
            exports: {},
            id: i,
            loaded: !1
        };
        return e[i].call(r.exports, r, r.exports, t), r.loaded = !0, r.exports
    }
    var n = {};
    return t.m = e, t.c = n, t.p = "", t(0)
}([function(e, t, n) {
    (function(t, i) {
        "use strict";
        var r = n(2),
            o = n(5),
            a = n(19),
            u = e.exports = {};
        u["new"] = function(e, t) {
            return new a(e, t)
        }, u.log = o;
        var l = u["new"]("x", {
                autoloadAnonymous: !0
            }),
            s = ["config", "on", "off", "define", "require", "hasDefine", "getModules", "resolve", "undefine"];
        r.each(s, function(e, t) {
            u[t] = l[t]
        }), l.define("global", function() {
            return t
        }), i.browser && ! function() {
            var e = t.define,
                i = t.require,
                r = t.xloader;
            u.noConflict = function(n) {
                return t.define = e, t.require = i, n && (t.xloader = r), u
            }, u.assets = n(17), t.xloader = u, t.define = u.define, t.require = u.require
        }()
    }).call(t, function() {
        return this
    }(), n(6))
}, , function(e, t) {
    "use strict";

    function n(e) {
        return "[object Array]" === i.call(e)
    }
    var i = Object.prototype.toString,
        r = 1;
    t.isArray = Array.isArray ? Array.isArray : n, t.__test = {
        isArray: n
    }, t.extend = function(e, t) {
        for (var n in t) {
            var i = t[n];
            null !== i && void 0 !== i && (e[n] = i)
        }
        return e
    }, t.each = function(e, t) {
        var n = e.length,
            i = 0 === n || "number" == typeof n && n > 0 && n - 1 in e;
        if (i)
            for (var r = 0; n > r; r++) t(r, e[r]);
        else
            for (var o in e) t(o, e[o])
    }, t.map = function(e, t) {
        for (var n = [], i = 0, r = e.length; r > i; i++) {
            var o = t(i, e[i]);
            void 0 !== o && n.push(o)
        }
        return n
    }, t.proxy = function(e, t) {
        var n = e[t];
        return function() {
            return n.apply(e, arguments)
        }
    }, t.assert = function(e, t) {
        if (!e) throw new Error("AssertFailError: " + t)
    }, t.guid = function() {
        return r++
    };
    var o = /([-\w]+\/\.\.\/)/g,
        a = /([^.])\.\//g;
    t.join = function(e, t) {
        for (t = e ? e + "/" + t : t, t = t.replace(a, "$1"); o.test(t);) t = t.replace(o, "");
        return t
    };
    var u = /\/$/;
    t.dirname = function(e) {
        e = e.replace(u, "");
        var t = e.lastIndexOf("/");
        return -1 === t ? "" : e.substr(0, t)
    }
}, , , function(e, t, n) {
    (function(t) {
        "use strict";
        var i = n(2),
            r = {
                none: 0,
                error: 1,
                warn: 2,
                info: 3,
                debug: 4
            },
            o = [].slice,
            a = e.exports = {};
        a.level = "warn", a.filter = !1, a.isEnabled = function(e) {
            return r[e] <= r[a.level]
        }, i.each(r, function(e) {
            a[e] = function() {
                if (a.isEnabled(e)) {
                    var t = o.call(arguments, 0);
                    (!a.filter || a.filter(t[0])) && (t[0] = "[loader] " + t[0], a.handler(e, t))
                }
            }
        }), a.handler = "undefined" != typeof console ? function(e, t) {
            console[e] && console[e].apply(console, t)
        } : function() {};
        var u = t.env.XLOADER_LOG;
        if (t.browser) {
            var l = /\bxloader\.log=([^&]+)/,
                s = l.exec(window.location.search);
            u = s && s[1]
        }
        u && ! function() {
            a.level = "debug", u = u.replace(/([.\[\]\(\)\{\}^$\\?+])/g, "\\$1").replace(/\*/g, ".*");
            var e = new RegExp("^" + u + "$");
            a.filter = function(t) {
                return e.test(t)
            }
        }()
    }).call(t, n(6))
}, function(e, t) {
    function n() {
        s = !1, a.length ? l = a.concat(l) : c = -1, l.length && i()
    }

    function i() {
        if (!s) {
            var e = setTimeout(n);
            s = !0;
            for (var t = l.length; t;) {
                for (a = l, l = []; ++c < t;) a && a[c].run();
                c = -1, t = l.length
            }
            a = null, s = !1, clearTimeout(e)
        }
    }

    function r(e, t) {
        this.fun = e, this.array = t
    }

    function o() {}
    var a, u = e.exports = {},
        l = [],
        s = !1,
        c = -1;
    u.nextTick = function(e) {
        var t = new Array(arguments.length - 1);
        if (arguments.length > 1)
            for (var n = 1; n < arguments.length; n++) t[n - 1] = arguments[n];
        l.push(new r(e, t)), 1 !== l.length || s || setTimeout(i, 0)
    }, r.prototype.run = function() {
        this.fun.apply(null, this.array)
    }, u.title = "browser", u.browser = !0, u.env = {}, u.argv = [], u.version = "", u.versions = {}, u.on = o, u.addListener = o, u.once = o, u.off = o, u.removeListener = o, u.removeAllListeners = o, u.emit = o, u.binding = function(e) {
        throw new Error("process.binding is not supported")
    }, u.cwd = function() {
        return "/"
    }, u.chdir = function(e) {
        throw new Error("process.chdir is not supported")
    }, u.umask = function() {
        return 0
    }
}, , function(e, t, n) {
    "use strict";
    var i = n(5),
        r = [].slice;
    e.exports = function(e) {
        var t = {};
        return e = e || {}, e.on = function(e, n) {
            i.debug("event.on: " + e, n);
            var r = t[e] || (t[e] = []);
            r.push(n)
        }, e.trigger = function(n) {
            var o = t[n];
            if (o) {
                var a = arguments.length > 1 ? r.call(arguments, 1) : [];
                i.debug("event.trigger: " + n, a);
                for (var u = 0, l = o.length; l > u; u++) {
                    var s = o[u].apply(e, a);
                    if (null !== s && void 0 !== s) return s
                }
            }
        }, e.off = function(e, n) {
            i.debug("event.off: " + e, n);
            var r = t[e];
            if (r) {
                for (var o = r.length - 1; o >= 0; o--) r[o] === n && r.splice(o, 1);
                r.length || delete t[e]
            }
        }, e
    }
}, , function(e, t, n) {
    "use strict";
    var i = n(11),
        r = n(5),
        o = {
            alias: !0,
            resolve: !0
        };
    e.exports = i({
        init: function() {
            this.cache = {}
        },
        get: function(e) {
            var t = this.cache;
            return o[e] ? t[e] || [] : t[e]
        },
        set: function(e, t) {
            r.debug("set config: " + e, t);
            var n = this.cache;
            o[e] ? (n[e] = n[e] || [], n[e].push(t)) : n[e] = t
        }
    })
}, function(e, t, n) {
    "use strict";
    var i = n(2);
    e.exports = function(e) {
        var t = function() {
            var e = this.init;
            return e && e.apply(this, arguments)
        };
        return e && i.extend(t.prototype, e), t
    }
}, , function(e, t, n) {
    "use strict";

    function i(e, t, n) {
        void 0 !== n || l(t) || (n = t, t = s), "function" == typeof e ? (n = e, t = s, e = null) : l(e) && (t = e, e = null), u(l(t), "arguments error, depends should be an array");
        var i = !e;
        return e = e || "____anonymous" + r.guid(), {
            id: e,
            depends: t,
            factory: n,
            anonymous: i
        }
    }
    var r = n(2),
        o = n(5),
        a = n(11);
    e.exports = a({
        init: function(e) {
            this.loader = e
        },
        define: function(e, t, n) {
            var r = this.loader,
                a = r.modules,
                u = i(e, t, n);
            return e = u.id, a[e] ? (o.warn("module already defined, ignore: " + e), a[e]) : (o.debug("define module: " + e, u), a[e] = u, r.trigger("define", u), u)
        }
    });
    var u = r.assert,
        l = r.isArray,
        s = []
}, , function(e, t, n) {
    "use strict";

    function i(e, t, n) {
        if (s.debug("init module: " + t.id), t.loadtimes > 0) return t.loadtimes++, s.debug(t.id + " is loaded", t.exports), void n();
        var i = t.loadlist || (t.loadlist = []);
        return i.push(n), i.length > 1 ? void s.debug("module is in loading: " + t.id) : void r(e, t, function() {
            o(e, t, function() {
                s.debug(t.id + " is loaded", t.exports), t.loadtimes = i.length, delete t.loadlist, l.each(i, function(e, t) {
                    t()
                })
            })
        })
    }

    function r(e, t, n) {
        var r = e.loader,
            o = r.modules,
            u = t.depends;
        if (0 === u.length) return n();
        var c = t.adepends = [],
            f = l.dirname(t.id);
        l.each(u, function(e, t) {
            c[e] = d.test(t) ? l.join(f, t) : t
        }), s.debug("try load depends for: " + t.id, c);
        var g = c.length,
            p = 0,
            h = e.aliasCache;
        l.each(c, function(t, u) {
            var l = h[u] || r.trigger("alias", u);
            l && u !== l && (s.debug("alias " + u + " -> " + l), u = l, h[u] = u, c[t] = u);
            var d = !1,
                f = function() {
                    return d ? void s.error("depend already loaded: " + u) : (d = !0, p++, void(p >= g && n()))
                },
                v = o[u];
            return v ? void i(e, v, f) : void a(e, u, function(t) {
                i(e, t, f)
            })
        })
    }

    function o(e, t, n) {
        var i = e.loader,
            r = i.modules;
        i.trigger("compile", t);
        var o = t.factory;
        "function" == typeof o && ! function() {
            var e = t.adepends,
                n = {
                    id: t.id,
                    exports: {}
                },
                a = [];
            e && e.length && l.each(e, function(e, i) {
                var o = r[i];
                c(o && "exports" in o, "module should already loaded: " + i), o.exports && "function" == typeof o.exports.$compile ? a[e] = o.exports.$compile(n, t) : a[e] = o.exports
            });
            try {
                s.debug("compile " + t.id, t), o = o.apply(null, a), void 0 === o && (o = n.exports)
            } catch (u) {
                o = null, i.trigger("error", u)
            }
        }(), t.exports = o, n()
    }

    function a(e, t, n) {
        var i = e.loader,
            r = i.modules,
            o = i.trigger("resolve", t);
        if (!o) return void i.trigger("error", new Error("can not resolve module: " + t));
        s.debug("resolve " + t + " -> " + o);
        var a = f[t] || (f[t] = []),
            u = function() {
                var e = r[t];
                return e ? (e.async = !0, e.url = o, void n(e)) : void i.trigger("error", new Error("can not find module: " + t))
            };
        if (a.push(u), !(a.length > 1)) {
            var c = {
                id: t,
                url: o,
                namespace: i.namespace
            };
            s.debug("try request: " + o), i.trigger("request", c, function() {
                delete f[t], l.each(a, function(e, t) {
                    t()
                })
            })
        }
    }
    var u = n(11),
        l = n(2),
        s = n(5),
        c = l.assert;
    e.exports = u({
        init: function(e) {
            this.loader = e, this.aliasCache = {}
        },
        require: function(e, t) {
            e = l.isArray(e) ? e : [e];
            var n = {
                proxy: !0,
                id: "____require" + l.guid(),
                depends: e,
                factory: function() {
                    return arguments
                }
            };
            return i(this, n, function() {
                t && t.apply(null, n.exports)
            }), n.exports && n.exports[0]
        }
    });
    var d = /^\.\.?\//,
        f = {}
}, , function(e, t, n) {
    "use strict";

    function i(e, t) {
        var n = !1;
        setTimeout(function() {
            n || (n = !0, t.error && t.error(new Error("poll request css timeout")))
        }, t.timeout || 1e4);
        var i = function r() {
            var i = !1;
            try {
                i = !!e.sheet
            } catch (o) {
                i = h.test(o.message)
            }
            n || (i ? (n = !0, t.success && t.success()) : setTimeout(r, 20))
        };
        i()
    }

    function r(e, t, n, i, r) {
        e.onload = e.onreadystatechange = function(t) {
            t = t || window.event || {}, ("load" === t.type || v.test("" + e.readyState)) && (e.onload = e.onreadystatechange = e.onerror = null, n && m.removeChild(e), r && r(), i.success && i.success())
        }, e.onerror = function() {
            e.onload = e.onreadystatechange = e.onerror = null;
            var n = new Error("load assets error: " + t);
            i.error && i.error(n)
        }
    }

    function o(e) {
        y ? m.insertBefore(e, y) : m.appendChild(e)
    }
    var a = n(5),
        u = /\.css(\?|$)/;
    t.postLoadScript = null, t.load = function(e, n) {
        var i = u.test(e) ? "css" : "script";
        return t[i](e, n)
    };
    var l = void 0;
    t.script = function(e, n) {
        n = n || {};
        var i = w.createElement("script"),
            u = !a.isEnabled("debug");
        r(i, e, u, n, function() {
            t.postLoadScript && (t.postLoadScript(e, n), t.postLoadScript = null)
        }), i.async = "async", n.namespace && i.setAttribute("data-namespace", n.namespace), i.src = e, n.charset && (i.charset = n.charset), l = i, o(i), l = null
    };
    var s = /.*webkit\/?(\d+)\..*/,
        c = /mobile/,
        d = window.navigator.userAgent.toLowerCase(),
        f = s.exec(d),
        g = f ? 1 * f[1] < 536 : !1,
        p = g || !f && c.test(d);
    t.css = function(e, t) {
        t = t || {};
        var n = w.createElement("link");
        n.rel = "stylesheet", n.href = e, t.charset && (n.charset = t.charset), "onload" in n && !p ? r(n, e, !1, t) : setTimeout(function() {
            i(n, t)
        }, 1), o(n)
    };
    var h = /security|denied/i,
        v = /loaded|complete|undefined/,
        w = document,
        m = w.head || w.getElementsByTagName("head")[0] || w.documentElement,
        y = w.getElementsByTagName("base")[0],
        b = void 0;
    t.getCurrentScript = function() {
        if (l) return l;
        if (b && "interactive" === b.readyState) return b;
        for (var e = m.getElementsByTagName("script"), t = e.length - 1; t >= 0; t--) {
            var n = e[t];
            if ("interactive" === n.readyState) return b = n
        }
    }
}, , function(e, t, n) {
    "use strict";

    function i(e) {
        var t = e.modules = {};
        new p(e);
        var n = new h,
            i = new v(e),
            r = new w(e);
        f.isEnabled("debug") && (e._config = n, e._define = i, e._require = r), e.config = function(e, t) {
            return void 0 === t ? n.get(e) : n.set(e, t)
        }, e.define = d.proxy(i, "define"), e.require = d.proxy(r, "require"), e.hasDefine = function(e) {
            return !!t[e]
        }, e.getModules = function() {
            return t
        }, e.resolve = function(t) {
            return e.trigger("resolve", t)
        }, e.undefine = function(e) {
            delete t[e]
        }
    }

    function r(e) {
        e.on("error", function(e) {
            f.error(e.stack)
        })
    }

    function o(e) {
        e.on("alias", function(t) {
            return c(e.config("alias"), function(e, n) {
                return "function" == typeof n ? n(t) : n[t]
            })
        })
    }

    function a(e) {
        e.on("resolve", function(t) {
            var n = c(e.config("resolve"), function(e, n) {
                return n(t)
            });
            return !n && y.test(t) && (n = t), n
        })
    }

    function u(e) {
        var t = new m(e);
        e.on("request", function(e, n) {
            t.handle(e, n)
        })
    }

    function l(e) {
        e.define("require", function() {
            return e.require
        }), e.define("module", function() {
            return {
                $compile: function(e) {
                    return e
                }
            }
        }), e.define("exports", function() {
            return {
                $compile: function(e) {
                    return e.exports
                }
            }
        })
    }

    function s(e) {
        e.on("define", function(t) {
            t.anonymous && (f.debug("require anonymous module: " + t.id), e.require(t.id))
        })
    }

    function c(e, t) {
        if (!e || 0 === e.length) return null;
        for (var n = 0, i = e.length; i > n; n++) {
            var r = t(n, e[n]);
            if (r) return r
        }
    }
    var d = n(2),
        f = n(5),
        g = n(11),
        p = n(8),
        h = n(10),
        v = n(13),
        w = n(15),
        m = n(20);
    e.exports = g({
        init: function(e, t) {
            var n = e,
                c = t || {};
            this.namespace = n, this.options = c, i(this), r(this), o(this), a(this), u(this), l(this), c.autoloadAnonymous && s(this)
        }
    });
    var y = /(^(\w+:)?\/\/)|(^\/)/
}, function(e, t, n) {
    (function(t) {
        "use strict";
        var i = n(11),
            r = n(2),
            o = n(5),
            a = /\.\w+(\?|$)/;
        e.exports = i({
            init: function(e) {
                this.loader = e
            },
            handle: function(e, i) {
                var u = this.loader,
                    l = u.config("requestHandler");
                if (l) return l.call(u, e, i);
                if (!t.browser) throw new Error("requestHandler not exists");
                var s = u.modules,
                    c = e.id,
                    d = e.url,
                    f = u.config("requestOptions");
                f = "function" == typeof f ? f(e) : f, f = r.extend({
                    id: c,
                    namespace: e.namespace
                }, f), f.success = function() {
                    o.debug("request assets success: " + d, e), !s[c] && a.test(c) && (u.define(c), s[c].file = !0), i()
                }, f.error = function(t) {
                    o.debug("request assets error: " + d, t), u.trigger("error", t, e)
                }, o.debug("request assets: " + d, e);
                var g = n(17);
                g.load(d, f)
            }
        })
    }).call(t, n(6))
}]);
! function(e) {
    var t = null,
        n = /(^\w*:\/\/)|(^[\/])/,
        i = /^(util|ui|vendor|butterfly)\./,
        r = /^ui\/([-\w]+)$/,
        o = /^butterfly\/lib\//;
    e.butterfly = e.xloader, e.butterfly._modules = {
        butterfly: e.xloader.getModules()
    }, butterfly.config("resolve", function(e) {
        if (t = t || (butterfly.config("butterflyRoot") || "").replace(/\/$/, ""), n.test(e)) return e;
        if (i.test(e)) {
            e = e.replace(/\./g, "/").replace(/([a-z])([A-Z])/g, function(e, t, n) {
                return t + "-" + n
            }).toLowerCase(), e = e.replace(o, "");
            var a = r.exec(e);
            a && (e = e + "/" + a[1]);
            var u = /^vendor\//.test(e) ? "" : "lib/";
            return t + "/" + u + e + ".js"
        }
    });
    var a = /^butterfly\//;
    butterfly.config("resolve", function(e) {
        return t = t || (butterfly.config("butterflyRoot") || "").replace(/\/$/, ""), a.test(e) ? t + "/" + e.replace(a, "") : void 0
    })
}(this),
function() {
    butterfly.define("loader", function() {
        return butterfly
    }), butterfly.config("alias", {
        "lang.Lang": "@ali/wing-lib-lang/lib/lang",
        "lang.Class": "@ali/wing-lib-lang/lib/class",
        "lang.Log": "@ali/wing-lib-lang/lib/log",
        "lang.Event": "@ali/wing-lib-lang/lib/event",
        "lang.Deferred": "@ali/wing-lib-lang/lib/deferred",
        "lang.Timestamp": "@ali/wing-lib-lang/lib/timestamp",
        "lang.Executor": "@ali/wing-lib-lang/lib/executor",
        "wing.render.Art": "@ali/wing-render/lib/render/art",
        "wingx.ViewModule": "@ali/wing-render/lib/extend/view-module",
        "context.Application": "wingx/lib/context/application",
        "context.Autowire": "wingx/lib/context/autowire",
        "context.wing.Back": "wingx/lib/wingx/back",
        "context.wing.Module": "wingx/lib/wingx/module",
        "context.wing.QuickPage": "wingx/lib/wingx/quick-page",
        "wing.core.Native": "wingx/lib/wingx/native-bridge",
        "wingx.Application": "wingx/lib/wingx/application",
        "wingx.NativeBridge": "wingx/lib/wingx/native-bridge",
        "wingx.Back": "wingx/lib/wingx/back",
        "wingx.Module": "wingx/lib/wingx/module",
        "wingx.QuickPage": "wingx/lib/wingx/quick-page",
        jQuery: "lang.Jquery",
        Class: "@ali/wing-lib-lang/lib/class"
    }), butterfly.config("alias", function(e) {
        var t = "wingc.ui.";
        if (0 === e.indexOf(t)) return e = e.replace(t, ""), "butterfly.lib.ui." + e + ".views." + e
    })
}(),
function() {
    function e(e, n, i, r) {
        var o = l[e];
        o || (o = l[e] = [], setTimeout(function() {
            l[e] = null, t(e, o)
        }, 0)), o.push({
            type: e,
            url: n,
            success: i,
            error: r
        })
    }

    function t(e, t) {
        var i = t.map(function(e) {
            return e.url.replace(s, "")
        }).join(",");
        i = n + "??" + i, i += "?_" + c;
        var r = {};
        r.success = function() {
            t.forEach(function(e) {
                e.success()
            })
        }, r.error = function() {
            t.forEach(function(e) {
                e.error()
            })
        }, o[e](i, r)
    }
    var n = "//astyle.alicdn.com",
        i = /^(?:https?:)?\/\/(?:(?:style\.c\.aliimg\.com)|(?:astyle-src\.alicdn\.com))\/(.*)$/,
        r = /\.\w+(\?|$)/,
        o = butterfly.assets,
        a = butterfly.log,
        u = /\.css(\?|$)/;
    butterfly.config("requestHandler", function(t, n) {
        var l = this,
            s = l.modules,
            c = t.id,
            d = t.url,
            f = function() {
                a.debug("request assets success: " + c), !s[c] && r.test(c) && (l.define(c), s[c].file = !0), n()
            },
            g = function(e) {
                a.debug("request assets error: " + c), l.trigger("error", e, t)
            },
            p = u.test(d),
            h = p ? "css" : "script",
            v = i.exec(d);
        return v ? void e(h, v[1], f, g) : void o[h](d, {
            success: f,
            error: g
        })
    });
    var l = {
            script: null,
            css: null
        },
        s = /\?.*$/,
        c = (new Date).getTime()
}(), define("@ali/wing-lib-lang/lib/lang", ["require", "module", "exports"], function(e, t, n) {
    var i = this,
        r = Object.prototype.toString,
        o = Array.isArray;
    n.isArray = o || function(e) {
        return "[object Array]" === r.call(e)
    }, n.isObject = function(e) {
        return "[object Object]" === r.apply(e)
    }, n.extend = function() {
        return a(arguments, !1)
    };
    var a = function(e, t) {
        for (var n = e[0], i = 1, r = e.length; r > i; i++) {
            var o = e[i];
            if (o)
                for (var a in o) {
                    var u = o[a],
                        l = n[a];
                    t && void 0 !== l || void 0 !== u && (n[a] = u)
                }
        }
        return n
    };
    n.each = function(e, t) {
        var n = e.length,
            i = 0 === n || "number" == typeof n && n > 0 && n - 1 in e;
        if (i)
            for (var r = 0, o = n; o > r && t(r, e[r]) !== !1; r++);
        else
            for (var a in e)
                if (t(a, e[a]) === !1) break
    }, n.filter = function(e, t) {
        var i = [];
        return n.each(e, function(e, n) {
            t(e, n) && i.push(n)
        }), i
    }, n.map = function(e, t) {
        var i = [];
        return n.each(e, function(e, n) {
            var r = t(e, n);
            void 0 !== r && i.push(r)
        }), i
    };
    var u = [].slice;
    n.proxy = function(e, t) {
        var n, r;
        if ("function" == typeof e ? (n = e, e = i, r = 1) : (n = e[t], r = 2), "function" != typeof n) throw new TypeError(t + " is not a function");
        var o = arguments.length > r ? u.call(arguments, r) : null;
        return function() {
            var t = arguments;
            return o && (t = o.slice(0), t.push.apply(t, arguments)), n.apply(e, t)
        }
    }, n.param = function(e) {
        var t = [];
        for (var n in e) {
            var i = e[n];
            null !== i && void 0 !== i && t.push(n + "=" + encodeURIComponent(i))
        }
        return t.join("&")
    }, n.unparam = function(e) {
        var t = {},
            i = /^([^=]+)=(.*)$/,
            r = e.split("&");
        return n.each(r, function(e, n) {
            var r = i.exec(n);
            if (r) try {
                t[r[1]] = decodeURIComponent(r[2])
            } catch (o) {
                t[r[1]] = r[2]
            }
        }), t
    }, n.format = function(e, t) {
        return e.replace(/\{(\w+)\}/g, function(e, n) {
            return void 0 !== t[n] ? t[n] : "{" + n + "}"
        })
    };
    var l = /-([\da-z])/gi,
        s = /^[a-z]/;
    n.camelCase = function(e) {
        return e.replace(l, function(e, t) {
            return t.toUpperCase()
        })
    }, n.pascalCase = function(e) {
        return n.camelCase(e).replace(s, function(e) {
            return e.toUpperCase()
        })
    };
    var c = function() {};
    n.createObject = function(e, t) {
        c.prototype = e;
        var i = new c;
        return t ? n.extend(i, t) : i
    }
}), define("@ali/wing-lib-lang/lib/class", ["@ali/wing-lib-lang/lib/lang", "require", "module", "exports"], function(e, t, n, i) {
    var r = 1,
        o = function() {},
        a = n.exports = function(t, n) {
            n || (n = t, t = null);
            var i = function() {
                    var e = this.initialize || this.init;
                    return e && e.apply(this, arguments)
                },
                a = null;
            if (i.guid = r++, t) {
                if ("function" != typeof t) throw new TypeError("parent should be a function");
                i.superclass = t, o.prototype = t.prototype, a = new o
            } else a = {};
            var l = n.Mixin;
            return l && (u(a, l), delete n.Mixin), a.constructor = i, i.prototype = e.extend(a, n), i
        },
        u = function(t, n) {
            return n = e.isArray(n) ? n : [n], e.each(n, function(n, i) {
                i = "function" == typeof i ? i.prototype : i, e.extend(t, i)
            }), t
        };
    a.mixin = function(e, t) {
        if ("function" != typeof e) throw new TypeError("invalid class, should be a function:" + e);
        return u(e.prototype, t), e
    }
}), define("@ali/wing-lib-lang/lib/log", ["@ali/wing-lib-lang/lib/lang", "require", "module", "exports"], function(e, t, n, i) {
    var r = o,
        o = "undefined" != typeof r ? r : "undefined" != typeof window ? window : {},
        a = {
            none: 0,
            error: 1,
            warn: 2,
            info: 3,
            debug: 4
        },
        u = o.location ? o.location.search : "",
        l = (/\bdebug-log-level=(\w+)/.exec(u) || [])[1] || o.debugLogLevel || "error",
        s = n.exports = function(e) {
            return this instanceof s ? void(this.name = e || "Anonymous") : new s(e)
        };
    s.handler = o.console ? function(e, t, n) {
        var i = o.console,
            r = i[t] ? i[t] : i.log ? i.log : function() {};
        n.unshift("[" + e + "]"), r.apply(i, n)
    } : function() {};
    var c = s.prototype = {
            LEVEL: a,
            level: l,
            isEnabled: function(e) {
                return e = "string" == typeof e ? a[e] : e, e <= a[this.level]
            }
        },
        d = [].slice,
        f = function(e, t, n) {
            return e.isEnabled(t) && (n = d.call(n, 0), s.handler(e.name, t, n)), e
        };
    e.each(a, function(e) {
        c[e] = function() {
            return f(this, e, arguments)
        }
    }), s.setLevel = function(e) {
        c.level = e
    }
}), define("@ali/wing-lib-lang/lib/event", ["@ali/wing-lib-lang/lib/lang", "@ali/wing-lib-lang/lib/log", "require", "module", "exports"], function(e, t, n, i, r) {
    function o(t, n, i) {
        e.each(t._lazyList, function(e, r) {
            r.type === n && (l.info("lazy trigger: ", n), i.apply(t.target, r.args))
        })
    }

    function a(e) {
        var t = e.split(".");
        return {
            type: t[0],
            namespace: t.slice(1).join(".")
        }
    }

    function u(e, t) {
        return t ? 0 === e.indexOf(t) : !0
    }
    var l = new t("lang/event"),
        s = i.exports = function(e) {
            this.target = e, this.isLazy = !1, this._cache = {}, this._lazyList = []
        };
    s.prototype = {
        on: function(e, t) {
            l.info("on", e);
            var n = a(e),
                i = this._cache[n.type] || (this._cache[n.type] = []);
            return i.push({
                namespace: n.namespace,
                fn: t
            }), this.isLazy && o(this, e, t), this
        },
        off: function(e, t) {
            l.info("off", e);
            var n = a(e),
                i = this._cache[n.type];
            if (i) {
                for (var r = i.length - 1; r >= 0; r--) {
                    var o = i[r];
                    u(o.namespace, n.namespace) && (t ? o.fn === t : !0) && i.splice(r, 1)
                }
                return 0 === i.length && delete this._cache[n.type], this
            }
        },
        trigger: function(e) {
            l.debug("trigger", e), this.isLazy && this._lazyList.push({
                type: e,
                args: arguments
            });
            var t = a(e),
                n = this._cache[t.type];
            if (n && 0 !== n.length)
                for (var i = [].slice.call(arguments, 1), r = 0, o = n.length; o > r; r++) {
                    var s = n[r];
                    if (u(s.namespace, t.namespace)) {
                        var c = s.fn.apply(this.target, i);
                        if (void 0 !== c && null !== c) return c
                    }
                }
        },
        once: function(e, t) {
            var n = this,
                i = function() {
                    t.apply(this, arguments), n.off(e, i)
                };
            this.on(e, i)
        },
        mixto: function(t) {
            var n = this;
            return e.each(["on", "off", "trigger", "once"], function(i, r) {
                t[r] = t[r] || e.proxy(n, r)
            }), this
        },
        setTarget: function(e) {
            this.target = e
        },
        setLazy: function(e) {
            this.isLazy = e, this._lazyList.length = 0
        }
    }
}), define("@ali/wing-lib-lang/lib/deferred", ["@ali/wing-lib-lang/lib/lang", "require", "module", "exports"], function(e, t, n, i) {
    var r = n.exports = function(t) {
            var n = [],
                i = [],
                u = [],
                l = null,
                s = null,
                c = "pending",
                d = !1,
                f = {
                    state: function() {
                        return c
                    },
                    done: function() {
                        return d ? "resolved" === c && a(arguments, l) : o(n, arguments), f
                    },
                    fail: function() {
                        return d ? "rejected" === c && a(arguments, s) : o(i, arguments), f
                    },
                    always: function() {
                        return f.done.apply(f, arguments), f.fail.apply(f, arguments), f
                    },
                    progress: function() {
                        return d || o(u, arguments), f
                    },
                    resolve: function() {
                        return d || (c = "resolved", d = !0, l = arguments, a(n, l), n.length = i.length = u.length = 0), f
                    },
                    reject: function() {
                        return d || (c = "rejected", d = !0, s = arguments, a(i, s), n.length = i.length = u.length = 0), f
                    },
                    notify: function() {
                        return d || a(u, arguments), f
                    },
                    promise: function(t) {
                        return t ? e.extend(t, f) : f
                    },
                    then: function(e) {
                        return r(function(t) {
                            f.done(function() {
                                try {
                                    var n = e.apply(null, arguments);
                                    n && "function" == typeof n.promise ? n.promise().done(t.resolve).fail(t.reject) : t.resolve(n)
                                } catch (i) {
                                    return void t.reject(i)
                                }
                            }), f.fail(t.reject)
                        })
                    },
                    pipe: function(e) {
                        return f.done(e.resolve).fail(e.reject)
                    }
                };
            return t && t.call(f, f), f
        },
        o = function(e, t) {
            for (var n = 0, i = t.length; i > n; n++) e.push(t[n])
        },
        a = function(e, t, n) {
            for (var i = 0, r = e.length; r > i; i++) e[i].apply(n, t)
        },
        u = [].slice;
    r.when = function() {
        var t = arguments[0];
        t = e.isArray(t) ? t : arguments;
        var n = r(),
            i = t.length,
            o = 0,
            a = [];
        if (0 === i) return n.resolve();
        for (var l = function(e) {
                return function() {
                    a[e] = u.call(arguments, 0), o++, o >= i && n.resolve.apply(n, a)
                }
            }, s = 0, c = i; c > s; s++) {
            var d = t[s];
            d.done(l(s)), d.fail(n.reject)
        }
        return n
    }, r.then = function() {
        var t = arguments[0];
        t = e.isArray(t) ? t : arguments;
        for (var n = r(), i = n, o = 0, a = t.length; a > o; o++) i = i.then(t[o]);
        return n.resolve(), i
    }
}), define("@ali/wing-lib-lang/lib/timing", ["@ali/wing-lib-lang/lib/log", "require", "module", "exports"], function(e, t, n, i) {
    var r = new e("lang/timing"),
        o = n.exports = function() {
            this.cache = {}, this.stamps = []
        };
    o.prototype.mark = function(e, t) {
        var n = this.cache,
            i = this.stamps,
            o = t || (new Date).getTime(),
            a = n[e];
        if (a) {
            var u = o - a;
            i.push({
                name: e,
                time: a,
                cost: u
            }), delete n[e], r[u > 100 ? "warn" : "info"]("[" + e + "] cost " + u + " ms")
        } else n[e] = o, r.info("[" + e + "] start")
    }, o.prototype.reset = function() {
        this.cache = {}, this.stamps = []
    }, o.prototype.report = function(e) {
        var t = this.stamps.filter(function(e) {
            return e.cost > 0
        });
        return t.sort(function(e, t) {
            return e.time - t.time
        }), "function" == typeof e ? e(t) : (e = a[e || "default"] || a["default"], void e(t))
    };
    var a = o.Reporter = {};
    a["default"] = function(e) {
        console && console.table && console.table(e)
    }
}), define("@ali/wing-lib-lang/lib/timestamp", ["require", "module", "exports"], function(e, t, n) {
    n.mark = function() {}, n.report = function() {}
}), define("@ali/wing-lib-lang/lib/executor", ["@ali/wing-lib-lang/lib/log", "@ali/wing-lib-lang/lib/timing", "require", "module", "exports"], function(e, t, n, i, r) {
    function o(e) {
        if (u.isEnabled("info")) throw e;
        u.error(e.stack || e)
    }

    function a(e, t) {
        try {
            return "function" == typeof t ? t() : t
        } catch (n) {
            e.error(n)
        }
    }
    var u = new e("lang/executor"),
        l = i.exports = function(e) {
            e = e || {}, this.error = e.error || o, l.enableTiming && (this.timing = new t)
        };
    l.prototype.execute = function(e, t) {
        var n = this.timing;
        if (!n) return t && a(this, t);
        if (n.mark(e), t) {
            var i = a(this, t),
                r = function() {
                    n.mark(e)
                };
            return i && "function" == typeof i.then ? i.done(r) : r(), i
        }
    }, l.prototype.mark = l.prototype.execute, l.prototype.report = function(e) {
        this.timing && this.timing.report(e)
    }
}), define("@ali/apm-wing-helper/apm", ["require", "module", "exports"], function(e, t, n) {
    "use strict";

    function i(e, t, n) {
        return '<link rel="stylesheet" href="' + r(e, t, n) + '"/>'
    }

    function r(e, t, n) {
        var i, r, l, s, c;
        return (r = u.exec(t)) && (i = r[1]), (l = n[i]) ? (s = l.version, c = i === t ? l.mainCss : t.replace(new RegExp("^" + i + "/"), ""), a.test(c) && (c = c.replace(".less", ".css")), o.test(c) || (c += ".css"), e + "/spm_modules/" + i + "/" + s + "/" + c) : ""
    }
    var o = /\.css$/,
        a = /\.less$/,
        u = /([\w-]+)\/?/;
    t.exports = {
        assetsRoot: "",
        meta: {},
        init: function(e, t) {
            this.assetsRoot = e, this.meta = t
        },
        css: function(e) {
            return i(this.assetsRoot, e, this.meta)
        },
        href: function(e) {
            return r(this.assetsRoot, e, this.meta)
        }
    }
}), define("lang.Jquery", function() {
    var e = window.jQuery || window.af || window.Zepto;
    return window.af && ! function() {
            var t = e.ajax;
            e.ajax = function(n, i) {
                return i = e.extend({}, i), i.url = n, t(i)
            }
        }(),
        function() {
            var t = e.fn.on,
                n = window.DocumentTouch && document instanceof window.DocumentTouch || "ontouchstart" in window;
            e.fn.on = n ? t : function(e, n, i) {
                return "tap" === e ? t.call(this, "click", n, i) : t.apply(this, arguments)
            }
        }(), window.jQuery && ! function() {
            var t = e.cleanData;
            e.cleanData = function(n) {
                return e(n).trigger("cleandata"), t.apply(e, arguments)
            }
        }(), e
}), define("wingx/lib/context/application", ["loader", "jquery", "@ali/wing-lib-lang/lib/lang", "@ali/wing-lib-lang/lib/class", "@ali/wing-lib-lang/lib/log", "@ali/wing-lib-lang/lib/event", "@ali/wing-lib-lang/lib/executor", "wingx/lib/context/view-context", "wingx/lib/context/autowire", "require", "module", "exports"], function(e, t, n, i, r, o, a, u, l, s, c, d) {
    var f = new r("context/application");
    c.exports = i({
        init: function(e) {
            this.config = e || {}, this.name = e.name, this.namespace = e.name.toLowerCase() + ".core", f.info("init application: " + this.name), this._initEvent(), this._initExecutor(), this._initViewContext()
        },
        start: function(e) {
            var t = this;
            f.info("application start", e), this.executor.execute("application start", function() {
                t.viewContext.start(e), t._startAutowire(e)
            }), this.event.setLazy(!1), this._report()
        },
        _initEvent: function() {
            var t = this.event = new o(this);
            t.mixto(this), t.setLazy(!0), e.define(this.namespace + ".Event", function() {
                return t
            })
        },
        _initExecutor: function() {
            var t = new a({
                error: n.proxy(this, "_error")
            });
            this.executor = t, e.define(this.namespace + ".Executor", function() {
                return t
            })
        },
        _error: function(e) {
            if (f.isEnabled("info")) throw e;
            f.error(e), this.event.trigger("error", e)
        },
        _initViewContext: function() {
            var e = n.extend({
                event: this.event,
                executor: this.executor
            }, this.config.viewContext);
            this.viewContext = new u(e)
        },
        _startAutowire: function(e) {
            new l(e || t("body"), {
                executor: this.executor
            })
        },
        _report: function() {
            var e = this;
            setTimeout(function() {
                e.executor.report()
            }, 3e3)
        }
    })
}), define("wingx/lib/context/autowire", ["jquery", "@ali/wing-lib-lang/lib/lang", "@ali/wing-lib-lang/lib/class", "@ali/wing-lib-lang/lib/log", "require", "module", "exports"], function(e, t, n, i, r, o, a) {
    var u = new i("context/autowire");
    o.exports = n({
        init: function(t, n) {
            if (t = e(t), n = n || {}, !t.length) return void u.error("please specify parent element for autowire");
            this.executor = n.executor, u.info("auto wire for:", t);
            var i = this,
                r = e("[data-wing-ui]", t);
            r.length && r.each(function() {
                i.handle(e(this))
            })
        },
        handle: function(e) {
            var t = e.data("wing-ui"),
                n = this.getConfig(e);
            this.process(e, t, n)
        },
        process: function(e, t, n) {
            var i = this;
            e.data("__autowired") || (e.data("__autowired", !0), r([t], function(r) {
                u.info("init widget, element:", e, " type:", t), i.executor.execute("autowire [" + t + "]", function() {
                    e.data("wingui", new r(e, n))
                })
            }))
        },
        getConfig: function(e) {
            for (var n = {}, i = /^data-(.+)$/, r = e[0].attributes, o = 0, a = r.length; a > o; o++) {
                var u = r[o],
                    l = i.exec(u.name);
                l && "wing-ui" !== l[1] && (n[t.camelCase(l[1])] = e.data(l[1]))
            }
            return n
        }
    })
}), define("wingx/lib/context/view-context", ["jquery", "@ali/wing-lib-lang/lib/class", "@ali/wing-lib-lang/lib/log", "require", "module", "exports"], function(e, t, n, i, r, o) {
    var a = new n("context/view-context");
    r.exports = t({
        init: function(e) {
            this.event = e.event, this.executor = e.executor, this.execute = e.execute
        },
        start: function(t) {
            a.info("startting");
            var n = this,
                i = this.event,
                r = "div[data-wing-view]";
            i.on("wing-view-ready", function(t, i) {
                1 === t.length ? n._bind(t, i) : t.each(function() {
                    n._bind(e(this), i)
                })
            }), e("body").on("wing-context-ready", function(t, n) {
                i.trigger("wing-view-ready", e(r, n))
            }), t = e(t || "body"), i.trigger("wing-view-ready", e(r, t)), i.trigger("wing-view-all-ready")
        },
        _bind: function(e, t) {
            a.info("bind", e);
            var n = this,
                r = e.data("wing-view");
            r && i([r], function(i) {
                a.info("init view: " + r), n.executor.execute("init view [" + r + "]", function() {
                    n.execute(i, e, t)
                }), e.trigger("wing-view-init")
            })
        }
    })
}), define("wingx/lib/wingx/native-bridge", ["require", "module", "exports"], function(e, t, n) {
    var i = window.Wing,
        r = i.navigator;
    n.getAssetsRoot = function(e) {
        return r.getAssetsRoot(e)
    }, n.getProductUrl = function(e) {
        return r.getProductUrl(e)
    }, n.getProductRoot = function(e) {
        return r.getProductRoot(e)
    }, n.redirect = function(e) {
        i.navigator.rewrite("URL", e)
    }, n.post = function(e, t) {
        i.navigator.post(e, t)
    }, n.invokeWebview = function(e, t, n) {
        i.navigator.ui.callback(e, t, n)
    }
}), define("wingx/lib/wingx/application", ["loader", "jquery", "@ali/wing-lib-lang/lib/lang", "@ali/wing-lib-lang/lib/log", "@ali/wing-lib-lang/lib/class", "@ali/wing-lib-lang/lib/deferred", "wingx/lib/context/application", "wingx/lib/context/autowire", "wingx/lib/wingx/native-bridge", "require", "module", "exports"], function(e, t, n, i, r, o, a, u, l, s, c, d) {
    var f = new i("wingx/application"),
        g = c.exports = r(a, {
            init: function(t) {
                var i = this,
                    r = {
                        name: t.productInfo.name,
                        viewContext: {
                            execute: n.proxy(this, "_execute")
                        }
                    };
                a.prototype.init.call(this, r), this._handleReadyEvent(t), this.wing = this._createGlobalWing(t), e.define(this.namespace + ".ProductInfo", t.productInfo), e.define(this.namespace + ".Wing", this.wing), e.define(this.namespace + ".RemoteWing", function() {
                    return i._createRemoteWing(window.Wing.remote)
                }), this._handleBack(), this._handleRemoteEvent()
            },
            start: function(e) {
                var t = this,
                    n = this._loadAsyncViews(e);
                n.done(function() {
                    a.prototype.start.call(t, e)
                })
            },
            _loadAsyncViews: function(e) {
                var n = this,
                    i = [],
                    r = t("div.wing-async-view", e);
                return r.each(function() {
                    var e = o(),
                        r = t(this),
                        a = r.data("async-info");
                    n.wing.view(a).done(function(i, o) {
                        var a = n._loadAssets(o, !0);
                        a.done(function() {
                            var n = t(i);
                            r.replaceWith(n), n.addClass("wing-async-view-ready"), e.resolve()
                        })
                    }), i.push(e)
                }), o.when(i)
            },
            _execute: function(e, t) {
                var i = +t.data("wing-guid"),
                    r = window.wingxViewData,
                    o = r[i];
                if ("function" == typeof e) {
                    var a = this._createScopeWing(t, o.info),
                        u = n.extend({}, r[0], o.context);
                    f.info("execute", t, u, a), new e(t, u, a)
                }
            },
            _handleReadyEvent: function(e) {
                this.event.mixto(e), this.event.on("wing-ready", n.proxy(this, "start"))
            },
            _createGlobalWing: function(e) {
                var i = this;
                return e = n.createObject(e), e.load = function(t, r) {
                    var a = o(),
                        u = n.extend({}, r);
                    return delete u.container, e.view(t, u).done(function(e, t) {
                        i._initWingView(t, r, a)
                    }), a
                }, e.reload = function(t, n) {
                    var i = t.data("wing-action-info");
                    return i ? e.load(i, n).then(function(e, n) {
                        e.insertBefore(t), t.remove(), n()
                    }) : void f.error("invalid wing view element", t)
                }, e.post = function(e, n) {
                    if ("string" != typeof e) {
                        var r = t(e);
                        e = r.attr("action"), n = r.serialize()
                    }
                    var o = /^(?:([-\w+]+):)?(.*)$/.exec(e),
                        a = o[1] || i.wing.productInfo.name,
                        u = a + "/" + o[2];
                    f.info("post", u, n);
                    try {
                        l.post(u, n)
                    } catch (s) {
                        f.error("post error", s)
                    }
                }, e.navigator = window.Wing.navigator, e
            },
            _createRemoteWing: function(e) {
                return e = n.createObject(e), e.load = function(i, r) {
                    var a = o(),
                        u = n.extend({}, r);
                    return delete u.container, e.view(i, u).done(function(e, n) {
                        var i = t('<div class="wing-remote-box">' + e + "</div>"),
                            o = function() {
                                var e = new g(n);
                                e.start(i)
                            };
                        r && r.container && (t(r.container).empty().append(i), o()), a.resolve(i, o)
                    }), a
                }, e
            },
            _initWingView: function(e, n, i) {
                var r = this,
                    o = t(e.body),
                    a = function() {
                        var e = "div[data-wing-view]",
                            n = t(e, o);
                        o.is(e) && r.event.trigger("wing-view-ready", o), n.length && r.event.trigger("wing-view-ready", n), new u(o, {
                            executor: r.executor
                        })
                    },
                    l = this._loadAssets(e);
                l.done(function() {
                    n && n.container && (t(n.container).empty().append(o), a()), i.resolve(o, a)
                })
            },
            _loadAssets: function(e, t) {
                var i = o(),
                    r = e.assets || {},
                    a = null;
                return r.css && r.css.length ? (a = n.map(r.css, function(e, t) {
                    return t.path
                }), s(a, i.resolve)) : i.resolve(), t && r.js && r.js.length && (a = n.map(r.js, function(e, t) {
                    return t.path
                }), s(a)), i
            },
            _createScopeWing: function(e, t) {
                var i = this,
                    r = function(e) {
                        return function(n, r) {
                            return "string" == typeof n && /^[-\w]+$/.test(n) && (n = {
                                "package": t["package"],
                                module: t.module,
                                action: n
                            }), i.wing[e](n, r)
                        }
                    },
                    o = n.createObject(this.wing);
                return o.view = r("view"), o.action = r("action"), o.navigate = r("navigate"), o.load = r("load"), o.reload = function(t, r) {
                    return n.isPlainObject(t) && (r = t, t = e), i.wing.reload(t, r)
                }, o
            },
            _handleBack: function() {
                var e = this.event,
                    t = e.on;
                e.on = function(n, i) {
                    return "back" !== n ? t.apply(e, arguments) : (f.warn("back event is deprecated, use wingx.Back instead"), void window.Wing.navigator.back.listener(function() {
                        i() !== !1 && window.Wing.navigator.back.go()
                    }))
                }
            },
            _handleRemoteEvent: function() {
                var e = this.event;
                e.on("remote", function() {
                    var e = [].slice.call(arguments, 0),
                        t = JSON.stringify(e),
                        n = function(e) {
                            l.invokeWebview(e, "wingUiCallback", t)
                        };
                    n("header"), n("footer")
                }), window.wingUiCallback = function(t) {
                    e.trigger.apply(e, JSON.parse(t))
                }
            }
        })
}), define("wingx/lib/wingx/util", ["@ali/wing-lib-lang/lib/lang", "require", "module", "exports"], function(e, t, n, i) {
    var r = /^(?:http:\/\/(\w+)(?:\.[^\/]+)?)?((?:\/[^.\/]+)+)\.html(?:\?([^#]*))?/,
        o = /^(?:(\w+):)?((?:\/[^.\/]+)+)/,
        a = window.Wing.navigator.device,
        u = a && a.mock,
        l = window.Wing.app.productInfo.name;
    i.parseUrl = function(t) {
        var n = r.exec(t),
            i = null,
            a = null;
        if (n) i = n[2].split("/"), i.shift(), u || i.unshift(n[1]), i[1] = i[1] + "s", n[3] && (a = e.unparam(n[3]));
        else {
            if (n = o.exec(t), !n) return null;
            i = n[2].split("/"), i[0] = n[1] || l
        }
        return {
            product: i[0],
            "package": i[1],
            module: i[2],
            action: i[3] || "view",
            query: a
        }
    }
}), define("wingx/lib/wingx/resolver", ["require", "module", "exports"], function(e, t, n) {
    var i = /^([^\/]+)\/([^\/]+)\/([^\/]+)(.*)\/([^\/]*)$/,
        r = /\.\w+$/;
    t.exports = function(e, t) {
        return function(n) {
            if (0 === n.indexOf(e + "/")) {
                var o = t + n.replace(e, "");
                return r.test(n) || (o += ".js"), o
            }
            if (0 === n.indexOf(e + ".")) return n = n.replace(/\./g, "/"), n = n.replace(i, function(e, t, n, i, r, o) {
                return r || "Module" === o || "module" === o || (r = "/js"), t + "/" + n + "/" + i + r + "/" + o
            }), n = n.replace(/\/([A-Z])([^\/]*)$/, function(e, t, n) {
                return "/" + t.toLowerCase() + n
            }), t + n.replace(e, "") + ".js"
        }
    }
}), define("wingx/lib/wingx/back", ["require", "module", "exports"], function(e, t, n) {
    t.exports = Wing.navigator.history
}), define("wingx/lib/wingx/module", ["@ali/wing-lib-lang/lib/log", "@ali/wing-render/lib/extend/view-module", "require", "module", "exports"], function(e, t, n, i, r) {
    var o = new e("wingx.Module");
    o.warn("wingx/module is deprecated, use @ali/wing-render/lib/extend/view-module instead");
    var a = new t;
    r.init = function() {
        a.init.apply(a, arguments)
    }, r.setup = function(e) {
        this.app = e
    }, r.afterRender = function() {
        return a.afterRender.apply(a, arguments)
    }
}), define("wingx/lib/wingx/quick-page", ["jquery", "@ali/wing-lib-lang/lib/class", "@ali/wing-lib-lang/lib/log", "@ali/wing-lib-lang/lib/deferred", "wingx/lib/wingx/util", "wingx/lib/wingx/back", "require", "module", "exports"], function(e, t, n, i, r, o, a, u, l) {
    var s = new n("wingx/quick-page"),
        c = 1;
    u.exports = t({
        init: function(e, t) {
            this.url = e, this.options = t || {}, this.options.preload && this.load()
        },
        load: function() {
            if (this._loadDefer) return this._loadDefer;
            var e = this.url,
                t = this.options;
            s.info("load page", e, t);
            var n = r.parseUrl(e);
            return n ? this._load(n, t) : void s.error("invalid url", e)
        },
        _load: function(t, n) {
            var r = this,
                o = this._loadDefer = i(),
                u = window.Wing.app.productInfo.name,
                l = t.product + (t.product === u ? ".core.Wing" : ".core.RemoteWing");
            return a([l], function(a) {
                var u = e.extend({}, t.query || n.data);
                u.wingQuickPage = !0, a.load(t, {
                    data: u
                }).done(function(t, a) {
                    r._node = t, r._page = e(r._tpl), r._page.append(t), e("body").append(r._page), r.options.effect && "slide" === r.options.effect.type && (document.body.style.overflowX = "hidden", r._page.addClass("effect-slide"), r._page.css("visibility", "hidden"), r._page.css("WebkitTransform", "translate3d(" + document.body.clientWidth + "px, 0, 0)"), r.options.loadFn && r.options.loadFn(r)), r._initDefer = i(), t.on("wing-view-init", r._initDefer.resolve), t.on("quickpage-close", e.proxy(r, "close")), n.preload ? a() : r._next = a, o.resolve()
                }).fail(o.reject)
            }), o
        },
        _tpl: '<div class="wing-quick-page ihidden"></div>',
        open: function(t) {
            return this.load().done(e.proxy(this, "show", t))
        },
        show: function(t) {
            function n(t) {
                t.options.effect && "slide" === t.options.effect.type ? (u.each(function() {
                    var t = e(this);
                    t.addClass("slide-out-right")
                }), t._page.removeClass("ihidden"), t._page.css("visibility", "visible"), t._page.css("WebkitTransform", "translate3d(0, 0, 0)"), t.effectEndFn || (t.effectEndFn = function() {
                    t._page.hasClass("ihidden") ? t._page.css("visibility", "hidden") : i()
                }, t._page[0].addEventListener("webkitTransitionEnd", t.effectEndFn))) : (t._page.removeClass("ihidden"), i())
            }

            function i() {
                e(document.body).scrollTop(0), u.each(function() {
                    var t = e(this);
                    t[0] !== a._page[0] && (t.data("originalDisplay") || t.data("originalDisplay", t.css("display")), t.css("display", "none"))
                }), a._next && (a._next(), a._next = null), a._initDefer.done(function() {
                    a._node.trigger("wing-view-show", t)
                }), o.push("quick-page-" + c++, function() {
                    a.options.preload ? a.hide() : a.close()
                }), a.options.afterShowFn && a.options.afterShowFn(a)
            }
            if (!this._page) return void s.error("should load page first, use open() instead");
            if (!this._hideHandler) {
                var r, a = this,
                    u = e("body>div");
                r = e(document.body).scrollTop(), a.options.beforeShowFn ? a.options.beforeShowFn(a).done(function() {
                    n(a)
                }) : n(a), this._hideHandler = function() {
                    u.each(function() {
                        var t = e(this);
                        t.css("display", t.data("originalDisplay"))
                    }), e(document.body).scrollTop(r), a._page.addClass("ihidden"), a.options.effect && "slide" === a.options.effect.type && setTimeout(function() {
                        a._page.css("WebkitTransform", "translate3d(" + document.body.clientWidth + "px, 0, 0)")
                    }, 100)
                }
            }
        },
        close: function() {
            return this._page ? (this.hide(), this._node.trigger("wing-view-beforeclose"), this._page.remove(), void(this._page = this._node = this._loadDefer = null)) : void s.warn("page is not loaded")
        },
        hide: function() {
            this._hideHandler && (this._hideHandler(), this._hideHandler = null)
        }
    })
}), define("wingx/lib/wingx/boot", ["loader", "@ali/wing-lib-lang/lib/executor", "require", "module", "exports"], function(e, t, n, i, r) {
    var o = window.Wing;
    e.config("butterflyRoot", o.navigator.getAssetsRoot("butterfly")), e.config("loftyRoot", o.navigator.getAssetsRoot("lofty")), e.config("alias", {
        jquery: "lang.Jquery"
    }), o.ready(function(i) {
        var r = n("wingx/lib/wingx/resolver"),
            a = n("wingx/lib/wingx/application"),
            u = o.config,
            l = u.productName,
            s = u.query["debug-timing"];
        void 0 !== s && (t.enableTiming = !0);
        var c = o.navigator.getAssetsRoot(l);
        e.config("resolve", r(l, c));
        var d = function() {
                var e = new a(i);
                e.start()
            },
            f = o.navigator.device.platform;
        if ("Wap" === f) {
            var g = window.jQuery;
            g(window).on("load", d)
        } else d()
    })
}), butterfly.require("wingx/lib/wingx/boot");
! function(t) {
    var r = butterfly.require;
    r.use = function() {
        return r.apply(butterfly, arguments)
    };
    var e = /^(lofty|fui|alicn|util)\/([-\w]+)(?:\/([.\d]+))?$/,
        n = {
            lofty: "lang",
            fui: "ui"
        };
    butterfly.config("alias", function(t) {
        var r = e.exec(t);
        if (r) {
            var i = n[r[1]] || r[1];
            return t = "lofty/" + i + "/" + r[2], r[3] && (t = t + "/" + r[3] + "/" + r[2]), t
        }
    }), butterfly.config("alias", function(t) {
        if (0 === t.indexOf("lofty.")) {
            t = t.replace(/\./g, "/").replace(/([a-z])([A-Z])/g, function(t, r, e) {
                return r + "-" + e
            }).toLowerCase();
            var r = /^lofty\/(?:ui|util|alicn)\/([-\w]+)$/.exec(t);
            return r && (t = t + "/1.0/" + r[1]), t
        }
    });
    var i = {
            lofty: Wing.navigator.getAssetsRoot("lofty"),
            proton: Wing.navigator.getAssetsRoot("proton")
        },
        o = /\.css$/;
    butterfly.config("resolve", function(t) {
        for (var r in i)
            if (0 === t.indexOf(r + "/")) {
                var e = i[r].replace(/\/$/, "");
                return o.test(t) || (t += ".js"), e + t.substr(r.length)
            }
    })
}(this);
define("lofty/ui/widget/1.0/widget", ["lofty/lang/class", "lofty/lang/base", "jquery", "require", "module", "exports"], function(t, n, e, i, o, r) {
    "use strict";

    function s() {
        return "fui_widget_" + g++
    }

    function a(t, n, e) {
        if ("document" === e) d(document).off(n);
        else if ("window" === e) d(window).off(n);
        else {
            var i = t.get("el");
            i.off(n, e)
        }
    }

    function l(t) {
        var n = document.documentElement;
        return d.contains ? d.contains(n, t) : !!(16 & n.compareDocumentPosition(t))
    }

    function u(t, n) {
        return t.replace(/{([^}]+)}/g, function(t, e) {
            for (var i, o = e.split("."), r = n; i = o.shift();) r = r === n.options ? n.get(i) : r[i];
            return p(r) ? r : ""
        })
    }
    var h = t,
        c = n,
        d = e,
        f = (o.exports = h(c, {
            options: {
                tpl: "<div></div>",
                extendTplData: null,
                container: {
                    value: "body",
                    getter: function(t) {
                        return p(t) && (t = d(t)), t
                    }
                },
                el: {
                    getter: function(t) {
                        return p(t) && (t = d(t)), t
                    }
                }
            },
            events: null,
            init: function(t) {
                this.mixOptions(["tpl", "events"]), c.prototype.init.call(this, t || {}), this.buildElement(), this.bindEvent(), this._create()
            },
            destroy: function() {
                this.unbindEvent(), c.prototype.destroy.call(this)
            },
            _create: function(t) {},
            render: function(t) {
                t && this.set("container", t);
                var n = this.get("el"),
                    e = this.get("container");
                return e && !l(n[0]) && n.appendTo(e), this
            },
            bindEvent: function(t) {
                t = t || this.get("events");
                for (var n in t) {
                    var e = t[n];
                    for (var i in e) {
                        var n = u(n, this),
                            o = u(i, this) + ".events-" + this.wId;
                        ! function(t, e) {
                            var i = function(n) {
                                    v(t) ? t.call(e, n) : e[t](n)
                                },
                                r = e.get("el");
                            "" === n ? r.on(o, i) : "document" === n ? d(document).on(o, i) : "window" === n ? d(window).on(o, i) : r.on(o, n, i)
                        }(e[i], this)
                    }
                }
                return this
            },
            unbindEvent: function(t) {
                if (t)
                    for (var n in t) {
                        var e = t[n],
                            n = u(n, this);
                        for (var i in e) {
                            var o = u(i, this) + ".events-" + this.wId;
                            a(this, o, n)
                        }
                    } else {
                        var o = ".events-" + this.wId;
                        a(this, o)
                    }
                return this
            },
            buildElement: function() {
                var t, n = "dynamic",
                    e = this.get("tpl");
                if (this.wId = s(), p(e) ? ("." === e.charAt(0) || "#" === e.charAt(0) || "body" === e) && (t = d(e)) : t = e, t && t.length > 0 && ("SCRIPT" == t[0].nodeName.toUpperCase() ? (e = t.html(), this.set("tpl", e)) : n = "static"), this.set("renderType", n), "static" === n) this.set("el", t);
                else {
                    var i = d(this.get("el"));
                    if (this.handleTpl(), i && 0 !== i.length) {
                        var o = this.get("container");
                        o.append(d(this.get("tpl")))
                    } else {
                        var r = this.wId,
                            e = d(this.get("tpl"));
                        e.length > 1 ? e = d('<div id="' + r + '"></div>').append(e) : (r = e.attr("id") || this.wId, e.attr("id", r)), this.set("el", e)
                    }
                }
                if (!this.get("el")) throw new Error("element is empty!")
            },
            mixOptions: function(t) {
                for (var n in t) {
                    var e = t[n];
                    this[e] && this.options && (this.options[e] = this[e])
                }
            },
            handleTpl: function() {}
        }), {}.toString),
        v = function(t) {
            return "[object Function]" === f.call(t)
        },
        p = function(t) {
            return "string" == typeof t
        },
        g = 0
});
define(["jquery", "require"], function(a, e) {
    var n = /AliApp\(AP.*\)/,
        o = window.navigator.userAgent;
    if (!window.JumpUtil && n.test(o)) {
        var i = function() {
                var a;
                if (a) return a;
                var e = /AliApp\(1688.*\)/,
                    n = /AliApp\(QN.*\)/,
                    o = /AliApp\(AP.*\)/,
                    i = /MicroMessenger/,
                    t = window.navigator.userAgent;
                return a = e.test(t) ? "1688" : n.test(t) ? "qianniu" : o.test(t) ? "alipay" : i.test(t) ? "weixin" : "wap"
            }(),
            t = function(a, e) {
                var n = a[0],
                    o = [];
                if ("yundetail" === n) {
                    o.push("//jinhuobao.1688.com");
                    for (var i = 0, t = a.length; t > i; i++) o.push("/"), o.push(a[i])
                } else {
                    o.push("//" + n + ".m.1688.com");
                    for (var i = 1, t = a.length; t > i; i++) o.push("/"), o.push(a[i])
                }
                return o.push(".html"), e && (o.push("?"), o.push(e)), o.join("")
            },
            r = function(a, e) {
                window.Wing ? e ? Wing.navigator.rewrite("load", a) : Wing.navigator.rewrite("URL", a) : window.location.href = a
            },
            p = function(a, e) {
                if (!window.Wing) return t(a, e);
                var n = a.shift();
                "yundetail" === n && (n = "detail");
                var o = "//" + n + ".m.1688.com",
                    i = o + "/" + a.join("/") + ".html";
                return e && (i = i + "?" + e), i
            },
            l = function(a, e) {
                -1 !== a.indexOf("20000522.h5app.m.taobao.com") || -1 !== a.indexOf("20000522.h5app.waptest.taobao.com") ? ant.ready(function() {
                    window.AlipayJSBridge && window.AlipayJSBridge.startupParams && "20000522" == window.AlipayJSBridge.startupParams.appId ? e ? window.location.href = a : ant.pushWindow({
                        url: a,
                        param: {
                            readTitle: !1,
                            pullRefresh: !1,
                            canPullDown: !1,
                            showLoading: !0
                        }
                    }) : ant.startApp({
                        appId: "20000522",
                        param: {
                            url: a.replace(/^https?:\/\/.*?\//, "/"),
                            ssoEnabled: !0,
                            showLoading: !0,
                            readTitle: !1,
                            pullRefresh: !1
                        },
                        closeCurrentApp: !1
                    }, function(a) {})
                }) : e ? window.location.href = a : ant.pushWindow({
                    url: a,
                    param: {
                        readTitle: !1,
                        pullRefresh: !1,
                        canPullDown: !1,
                        showLoading: !0
                    }
                })
            },
            u = function(a, e) {
                var n = window.yunOfflineConfig,
                    o = window.yunOfflineOrigin;
                if (n[a[0]]) {
                    var i = o + "/yuncore/lib/port/index.html?path=" + a.join("/");
                    return e && (i += "&" + e), i
                }
                return t(a, e)
            },
            s = function(a) {
                window.location.href = a
            },
            d = function(a, e) {
                return t(a, e)
            },
            c = function(a) {
                var e = /^https?:\/\/(.*)\.m\.1688\.com\/.*?/,
                    n = a.match(e);
                n && n.length && (a = n[1] + "/" + a.replace(e, ""));
                var o = /^https?:\/\/.*?\//;
                a = a.replace(o, "");
                var i, t, r = a.split("?");
                r[0] && (i = r[0]), r[1] && (t = r[1]);
                for (var p = i.split("/"), l = [], u = 0, s = p.length; s > u; u++) p[u] && l.push(p[u]);
                var d = l.length;
                return 3 > d ? void 0 : (l[d - 1] = l[d - 1].replace(/\.html$/, ""), 3 == d && l.push("view"), {
                    route: l,
                    param: t
                })
            };
        window.JumpUtil = {}, JumpUtil.redirect = function(a, e) {
            var n = !1,
                o = !1;
            if (e && ("boolean" == typeof e ? n = e : "object" == typeof e && (e.noProcess && (n = e.noProcess), e.isRewrite && (o = e.isRewrite))), n) return void("1688" == i ? r(a, o) : "alipay" == i ? l(a, o) : s(a, o));
            var t = c(a);
            if (!t) return void("1688" == i ? r(a, o) : "alipay" == i ? l(a, o) : s(a, o));
            if ("1688" == i) {
                var a = p(t.route, t.param);
                r(a, o)
            } else if ("alipay" == i) {
                var a = u(t.route, t.param);
                l(a, o)
            } else {
                var a = d(t.route, t.param);
                s(a, o)
            }
        }, JumpUtil.getAbsoluteUrl = function(a) {
            var e = c(a);
            return e ? "1688" == i ? p(e.route, e.param) : "alipay" == i ? u(e.route, e.param) : d(e.route, e.param) : a
        };
        var m = window.location.href;
        if ("1688" == i) {
            if (-1 !== m.indexOf("//jinhuobao.1688.com/")) {
                var w = JumpUtil.getAbsoluteUrl(m);
                m !== w && (Wing = null, navigator.userAgent.indexOf("iPhone") > 0 ? e.use(["//astyle-src.alicdn.com/m/lofty/alicn/native/5.0/wing.ios.js"], function() {
                    Wing.navigator.rewrite("load", w)
                }) : e.use(["//astyle-src.alicdn.com/m/lofty/alicn/native/5.0/wing.android.js"], function() {
                    Wing.navigator.rewrite("load", w)
                }))
            }
        } else "weixin" == i ? a(function() {
            var e = window.navigator.userAgent;
            e.match(/(Android)\s+([\d.]+)/) || e.match(/Silk-Accelerated/) ? a("body").append('<div style="height:100%;width:100%;background-color:#000;position:absolute;z-index:9999;top:0;background-image: url(//cbu01.alicdn.com/cms/upload/2015/375/394/2493573_1805353437.png);background-size: cover;"></div>') : a("body").append('<div style="height:100%;width:100%;background-color:#000;position:absolute;z-index:9999;top:0;background-image: url(//cbu01.alicdn.com/cms/upload/2015/305/694/2496503_1805353437.png);background-size: cover;"></div>')
        }) : "wap" == i && a(function() {
            window.localStorage.getItem("_yun_market_open_alipay_false") || (a("body").append('<div class="open_alipay" style="height:4.0625rem;width:100%;background-color:rgba(0,0,0,0.9);position:fixed;z-index:9999;bottom:0;background-image: url(//cbu01.alicdn.com/cms/upload/2015/697/784/2487796_1805353437.png);background-size: cover;"><span class="close" style="position:absolute;top:0;left:0;width:2rem;height:4.0625rem;display:block;"></span><span class="open" style="position:absolute;top:0;right:0;width:7rem;height:4.0625rem;display:block;"></span></div>'), a("body").on("tap", ".open_alipay .close", function(e) {
                window.localStorage.setItem("_yun_market_open_alipay_false", "1"), a(".open_alipay").remove()
            }), a("body").on("tap", ".open_alipay .open", function(a) {
                var e = "alipays://platformapi/startapp?appId=20000067&ssoEnabled=YES&url=" + encodeURIComponent(window.location.href);
                window.location.href = "//ds.alipay.com/?scheme=" + encodeURIComponent(e)
            }))
        });
        "alipay" == i && (window.ant && window.ant.remoteLog ? ant.remoteLog({
            type: "monitor",
            seedId: "H5_20000522_MONITOR",
            param1: "page_load_pv",
            param2: m,
            param3: window.document.referrer
        }) : e.use(["//static.alipayobjects.com/publichome-static/antBridge/antBridge.min.js"], function() {
            ant.remoteLog({
                type: "monitor",
                seedId: "H5_20000522_MONITOR",
                param1: "page_load_pv",
                param2: m,
                param3: window.document.referrer
            })
        })), ant && (ant.showOptionMenu(), ant.setOptionMenu({
            title: "è¿›è´§å•"
        }), ant.on("optionMenu", function() {
            JumpUtil.redirect("https://m.1688.com/page/cart.html")
        }), ant.on("back", function() {
            ant.setOptionMenu({
                reset: !0
            }), a("title").eq(0).text("")
        }))
    }
});
! function(n) {
    var e = {
            yuncore: !0,
            proton: !0,
            favorite: !1,
            yun: !0
        },
        t = "//20000522.h5app.m.taobao.com";
    if ("undefined" != typeof exports && n === exports) {
        if ("yunOfflineConfig" in exports) return;
        exports.yunOfflineConfig = e, exports.yunOfflineOrigin = t
    } else {
        if ("yunOfflineConfig" in n) return;
        n.yunOfflineConfig = e, n.yunOfflineOrigin = t
    }
}(this),
function(n) {
    var e = /AliApp\(1688.*\)/,
        t = window.navigator.userAgent;
    e.test(t) && (Wing.app = Wing.app || {}, Wing.app.yunShare = function(n, e) {
        var t = {};
        "dangkou" === n ? (t.shareTitle = "æ±‡èšæ‰¹å‘å¸‚åœºå¥½è´§æº", t.shareContent = "æŽ¨èä½ " + e.marketName + "çš„" + e.dangkouNum + 'æ¡£å£"' + e.dangkouName + '"\nå¿«æ¥çœ‹çœ‹å§!') : "offer" === n ? (t.shareTitle = "", t.shareContent = "æŽ¨èä½ " + e.marketName + "çš„" + e.dangkouNum + 'æ¡£å£"' + e.dangkouName + '"å¥½è´§æº!\n' + e.offerTitle) : "detail" === n && (t.content = e.shareContent), t.sharePicUrl = e.shareImg, t.shareUrl = e.shareUrl, Wing.navigator.v5share.share("yunmarket", t)
    }, Wing.app.openWW = function(n) {
        var e = new Object;
        e.id = "", e.clientID = n, e.siteID = "cnalichn", Wing.navigator.wangwang.openWW(e)
    }, Wing.navigator.back.listener(function() {
        Wing.navigator.keyboard.hide(), Wing.navigator.back.go()
    }))
}(Wing.navigator),
function(n) {
    var e = /AliApp\(AP.*\)/,
        t = window.navigator.userAgent;
    if (e.test(t)) {
        var a, i, r = window.yunOfflineConfig,
            o = window.yunOfflineOrigin,
            l = window.location.href,
            u = -1 !== l.indexOf(o);
        u || (i = Wing.config.meta.products, a = Wing.config.meta.server), n.getRealURL = function(n) {
            if (-1 != n.indexOf("/")) {
                var e = n.split("/"),
                    t = e.shift();
                if (u) {
                    if (r[t]) return "/" + n
                } else {
                    var a = i[t];
                    if (a && a.assetsRoot) {
                        var o = a.assetsRoot;
                        return o + "/" + e.join("/")
                    }
                }
            }
        };
        var g, p = n.back = {};
        p.listener = function(n) {
            g = n
        }, p.go = function(n) {
            ant.popWindow()
        }, p.triggerBackListener = function() {
            p.go()
        }, ant.on("back", function(n) {
            g && (n.preventDefault(), g())
        });
        var c = {},
            s = [],
            f = !1,
            h = n.history = {};
        h.push = function(e, t) {
            void 0 === c[e] && (f || (n.back.listener(h.trigger), f = !0), c[e] = s.length, s.push({
                name: e,
                fn: t
            }))
        }, h.remove = function(n) {
            void 0 !== c[n] && (s.splice(c[n], 1), delete c[n])
        }, h.trigger = function() {
            if (s.length) {
                var e = s.pop();
                delete c[e.name], e.fn()
            } else n.back.go()
        }, n.tooltip = function(n) {
            var e = 3e3,
                t = null;
            define(["lofty/ui/popup/1.0/popup"], function(a) {
                t = new a({
                    tpl: '<p id="toast_for_wap" style="display: block; background-color: #888;color: white;padding: 4px 10px;font-size: 12px;">' + n + "</p>",
                    isModal: !1,
                    y: document.documentElement.clientHeight - 100
                }), t.show(), setTimeout(function() {
                    t.hide()
                }, e)
            })
        }, n.getProductRoot = function(n) {
            return "/" + n
        }, n.setTitle = function(n) {
            ant.setTitle(n)
        };
        var d = !1;
        n.setRightNav = function(n) {
            d || (ant.showOptionMenu(), d = !0);
            var e = {
                redDot: -1
            };
            n.title ? e.title = n.title : n.icon && (e.icon = n.icon), ant.setOptionMenu(e), ant.on("optionMenu", function() {
                n.callback && n.callback()
            })
        }, n.setMenuList = function(n) {
            d || (ant.showOptionMenu(), d = !0);
            for (var e = {}, t = [], a = "key", i = 0, r = n.length; r > i; i++) {
                var o = a + i;
                t.push({
                    name: n[i].title,
                    tag: o
                }), n[i].callback && (e[o] = n[i].callback)
            }
            ant.setToolbarMenu({
                menus: t
            }), ant.on("toolbarMenuClick", function(n) {
                var t = n.data.tag;
                e[t]()
            })
        }, Wing.app = Wing.app || {}, Wing.app.redirect = function(n) {
            JumpUtil.redirect(n)
        }, Wing.app.openWW = function(n) {
            var e = encodeURIComponent("cnalichn" + n),
                t = "//20000522.h5app.m.taobao.com",
                a = "/ww/alipaylaunch.html?__alipay_wing_route__=/ww/page/chat/view&touid=" + e;
            ant.ready(function() {
                window.AlipayJSBridge && window.AlipayJSBridge.startupParams && "20000522" == window.AlipayJSBridge.startupParams.appId ? ant.pushWindow({
                    url: t + a,
                    param: {
                        readTitle: !1,
                        pullRefresh: !1,
                        canPullDown: !1,
                        showLoading: !1
                    }
                }) : ant.startApp({
                    appId: "20000522",
                    param: {
                        url: a,
                        ssoEnabled: !0,
                        showLoading: !1,
                        readTitle: !1,
                        pullRefresh: !1
                    },
                    closeCurrentApp: !1
                }, function(n) {})
            })
        }, n.wangwang = n.wangwang || {}, n.wangwang.openWW = function(n) {
            var e = n.clientID;
            Wing.app.openWW(e)
        }, n.v5share = n.v5share || {};
        var m = function(n) {
            ant.share({
                channels: [{
                    name: "Weibo",
                    param: {
                        title: n.title,
                        content: n.content,
                        imageUrl: n.shareImg,
                        url: n.targetUrl
                    }
                }, {
                    name: "LaiwangContacts",
                    param: {
                        title: n.title,
                        content: n.content,
                        imageUrl: n.shareImg,
                        url: n.targetUrl
                    }
                }, {
                    name: "LaiwangTimeline",
                    param: {
                        title: n.title,
                        content: n.content,
                        imageUrl: n.shareImg,
                        url: n.targetUrl
                    }
                }, {
                    name: "Weixin",
                    param: {
                        title: n.title,
                        content: n.content,
                        imageUrl: n.shareImg,
                        url: n.targetUrl
                    }
                }, {
                    name: "WeixinTimeLine",
                    param: {
                        title: n.title,
                        content: n.content,
                        imageUrl: n.shareImg,
                        url: n.targetUrl
                    }
                }, {
                    name: "CopyLink",
                    param: {
                        url: n.targetUrl
                    }
                }]
            }, function(n) {})
        };
        n.v5share.share = function(n, e) {
            m({
                title: e.shareTitle,
                content: e.shareContent,
                shareImg: e.sharePicUrl,
                targetUrl: e.shareUrl
            })
        }, Wing.app.yunShare = function(n, e) {
            var t = {};
            "dangkou" === n ? (t.title = "æ±‡èšæ‰¹å‘å¸‚åœºå¥½è´§æº", t.content = "æŽ¨èä½ " + e.marketName + "çš„" + e.dangkouNum + 'æ¡£å£"' + e.dangkouName + '"\nå¿«æ¥çœ‹çœ‹å§!') : "offer" === n ? t.content = "æŽ¨èä½ " + e.marketName + "çš„" + e.dangkouNum + 'æ¡£å£"' + e.dangkouName + '"å¥½è´§æº!\n' + e.offerTitle : "detail" === n && (t.content = e.shareContent), t.shareImg = e.shareImg, t.targetUrl = e.shareUrl, m(t)
        }, n.uthandler = n.uthandler || {};
        var v = window.location.href,
            w = window.document.referrer;
        n.uthandler.pageButtonClick = function(n) {
            ant.remoteLog({
                type: "monitor",
                seedId: "H5_20000522_MONITOR",
                param1: n,
                param2: v,
                param3: w
            })
        }
    }
}(Wing.navigator),
function(n) {
    var e = /AliApp\(QN.*\)/,
        t = window.navigator.userAgent;
    if (e.test(t)) {
        n.setTitle = function(n) {
            TOP.mobile.vpage.title(n)
        }, n.setRightNav = function(n) {
            var e = {};
            n.title ? e.text = n.title : n.icon && (e.iconBase64 = n.icon), Ali.qn.register("navRightItem", e, function() {
                n.callback && n.callback()
            })
        }, n.setMenuList = function(n) {}, Wing.app = Wing.app || {};
        var a = Wing.app.redirect;
        Wing.app.redirect = function(n, e, t) {
            "boolean" == typeof e && (t = e, e = {}), e = e || {}, a(n, e, t)
        }, n.v5share = n.v5share || {}, n.v5share.share = function(n, e) {
            TOP.mobile.application.request({
                event: "openShareComponent",
                biz: {
                    title: e.shareTitle,
                    textContent: e.shareContent,
                    mediaContent: e.sharePicUrl,
                    targetUrl: e.shareUrl
                },
                success: function() {},
                error: function() {}
            })
        }, Wing.app.yunShare = function(n, e) {
            var t = {};
            "dangkou" === n ? (t.title = "æ±‡èšæ‰¹å‘å¸‚åœºå¥½è´§æº", t.textContent = "æŽ¨èä½ " + e.marketName + "çš„" + e.dangkouNum + 'æ¡£å£"' + e.dangkouName + '"\nå¿«æ¥çœ‹çœ‹å§!') : "offer" === n ? t.textContent = "æŽ¨èä½ " + e.marketName + "çš„" + e.dangkouNum + 'æ¡£å£"' + e.dangkouName + '"å¥½è´§æº!\n' + e.offerTitle : "detail" === n && (t.content = e.shareContent), t.mediaContent = e.shareImg, t.targetUrl = e.shareUrl, TOP.mobile.application.request({
                event: "openShareComponent",
                biz: t,
                success: function() {},
                error: function() {}
            })
        }, Wing.app.openWW = function(n) {
            var e = TOP.mobile.ww;
            e.chat({
                chatNick: n
            })
        }
    }
}(Wing.navigator),
function(n) {
    Wing.app = Wing.app || {}, Wing.app.header = {}, Wing.app.header.setTitle = function(e) {
        return n.setTitle ? void n.setTitle(e) : (n.headerObj = n.headerObj || {}, void(n.headerObj.title = e))
    }, Wing.app.header.setRightNav = function(e) {
        return n.setRightNav ? void n.setRightNav(e) : (n.headerObj = n.headerObj || {}, void(n.headerObj.rightNavOpts = e))
    }, Wing.app.header.setMenuList = function(e) {
        return n.setMenuList ? void(n.setMenuList && n.setMenuList(e)) : (n.headerObj = n.headerObj || {}, void(n.headerObj.menuListOpts = e))
    }
}(Wing.navigator);
/*!
 * Vue.js v1.0.21
 * (c) 2016 Evan You
 * Released under the MIT License.
 */

/*!!cmd:uglify=false*/

! function(t, e) {
    "object" == typeof exports && "undefined" != typeof module ? module.exports = e() : "function" == typeof define && define.amd ? define(e) : t.Vue = e()
}(this, function() {
    "use strict";

    function t(e, n, r) {
        if (i(e, n)) return void(e[n] = r);
        if (e._isVue) return void t(e._data, n, r);
        var s = e.__ob__;
        if (!s) return void(e[n] = r);
        if (s.convert(n, r), s.dep.notify(), s.vms)
            for (var o = s.vms.length; o--;) {
                var a = s.vms[o];
                a._proxy(n), a._digest()
            }
        return r
    }

    function e(t, e) {
        if (i(t, e)) {
            delete t[e];
            var n = t.__ob__;
            if (n && (n.dep.notify(), n.vms))
                for (var r = n.vms.length; r--;) {
                    var s = n.vms[r];
                    s._unproxy(e), s._digest()
                }
        }
    }

    function i(t, e) {
        return xi.call(t, e)
    }

    function n(t) {
        return Ai.test(t)
    }

    function r(t) {
        var e = (t + "").charCodeAt(0);
        return 36 === e || 95 === e
    }

    function s(t) {
        return null == t ? "" : t.toString()
    }

    function o(t) {
        if ("string" != typeof t) return t;
        var e = Number(t);
        return isNaN(e) ? t : e
    }

    function a(t) {
        return "true" === t ? !0 : "false" === t ? !1 : t
    }

    function h(t) {
        var e = t.charCodeAt(0),
            i = t.charCodeAt(t.length - 1);
        return e !== i || 34 !== e && 39 !== e ? t : t.slice(1, -1)
    }

    function l(t) {
        return t.replace(Oi, c)
    }

    function c(t, e) {
        return e ? e.toUpperCase() : ""
    }

    function u(t) {
        return t.replace(Ti, "$1-$2").toLowerCase()
    }

    function f(t) {
        return t.replace(Ni, c)
    }

    function p(t, e) {
        return function(i) {
            var n = arguments.length;
            return n ? n > 1 ? t.apply(e, arguments) : t.call(e, i) : t.call(e)
        }
    }

    function d(t, e) {
        e = e || 0;
        for (var i = t.length - e, n = new Array(i); i--;) n[i] = t[i + e];
        return n
    }

    function v(t, e) {
        for (var i = Object.keys(e), n = i.length; n--;) t[i[n]] = e[i[n]];
        return t
    }

    function m(t) {
        return null !== t && "object" == typeof t
    }

    function g(t) {
        return ji.call(t) === Ei
    }

    function _(t, e, i, n) {
        Object.defineProperty(t, e, {
            value: i,
            enumerable: !!n,
            writable: !0,
            configurable: !0
        })
    }

    function y(t, e) {
        var i, n, r, s, o, a = function h() {
            var a = Date.now() - s;
            e > a && a >= 0 ? i = setTimeout(h, e - a) : (i = null, o = t.apply(r, n), i || (r = n = null))
        };
        return function() {
            return r = this, n = arguments, s = Date.now(), i || (i = setTimeout(a, e)), o
        }
    }

    function b(t, e) {
        for (var i = t.length; i--;)
            if (t[i] === e) return i;
        return -1
    }

    function w(t) {
        var e = function i() {
            return i.cancelled ? void 0 : t.apply(this, arguments)
        };
        return e.cancel = function() {
            e.cancelled = !0
        }, e
    }

    function C(t, e) {
        return t == e || (m(t) && m(e) ? JSON.stringify(t) === JSON.stringify(e) : !1)
    }

    function $(t) {
        this.size = 0, this.limit = t, this.head = this.tail = void 0, this._keymap = Object.create(null)
    }

    function k() {
        var t, e = qi.slice(Yi, Zi).trim();
        if (e) {
            t = {};
            var i = e.match(an);
            t.name = i[0], i.length > 1 && (t.args = i.slice(1).map(x))
        }
        t && (Qi.filters = Qi.filters || []).push(t), Yi = Zi + 1
    }

    function x(t) {
        if (hn.test(t)) return {
            value: o(t),
            dynamic: !1
        };
        var e = h(t),
            i = e === t;
        return {
            value: i ? t : e,
            dynamic: i
        }
    }

    function A(t) {
        var e = on.get(t);
        if (e) return e;
        for (qi = t, tn = en = !1, nn = rn = sn = 0, Yi = 0, Qi = {}, Zi = 0, Xi = qi.length; Xi > Zi; Zi++)
            if (Ki = Gi, Gi = qi.charCodeAt(Zi), tn) 39 === Gi && 92 !== Ki && (tn = !tn);
            else if (en) 34 === Gi && 92 !== Ki && (en = !en);
        else if (124 === Gi && 124 !== qi.charCodeAt(Zi + 1) && 124 !== qi.charCodeAt(Zi - 1)) null == Qi.expression ? (Yi = Zi + 1, Qi.expression = qi.slice(0, Zi).trim()) : k();
        else switch (Gi) {
            case 34:
                en = !0;
                break;
            case 39:
                tn = !0;
                break;
            case 40:
                sn++;
                break;
            case 41:
                sn--;
                break;
            case 91:
                rn++;
                break;
            case 93:
                rn--;
                break;
            case 123:
                nn++;
                break;
            case 125:
                nn--
        }
        return null == Qi.expression ? Qi.expression = qi.slice(0, Zi).trim() : 0 !== Yi && k(), on.put(t, Qi), Qi
    }

    function O(t) {
        return t.replace(cn, "\\$&")
    }

    function T() {
        var t = O(_n.delimiters[0]),
            e = O(_n.delimiters[1]),
            i = O(_n.unsafeDelimiters[0]),
            n = O(_n.unsafeDelimiters[1]);
        fn = new RegExp(i + "((?:.|\\n)+?)" + n + "|" + t + "((?:.|\\n)+?)" + e, "g"), pn = new RegExp("^" + i + ".*" + n + "$"), un = new $(1e3)
    }

    function N(t) {
        un || T();
        var e = un.get(t);
        if (e) return e;
        if (!fn.test(t)) return null;
        for (var i, n, r, s, o, a, h = [], l = fn.lastIndex = 0; i = fn.exec(t);) n = i.index, n > l && h.push({
            value: t.slice(l, n)
        }), r = pn.test(i[0]), s = r ? i[1] : i[2], o = s.charCodeAt(0), a = 42 === o, s = a ? s.slice(1) : s, h.push({
            tag: !0,
            value: s.trim(),
            html: r,
            oneTime: a
        }), l = n + i[0].length;
        return l < t.length && h.push({
            value: t.slice(l)
        }), un.put(t, h), h
    }

    function j(t, e) {
        return t.length > 1 ? t.map(function(t) {
            return E(t, e)
        }).join("+") : E(t[0], e, !0)
    }

    function E(t, e, i) {
        return t.tag ? t.oneTime && e ? '"' + e.$eval(t.value) + '"' : F(t.value, i) : '"' + t.value + '"'
    }

    function F(t, e) {
        if (dn.test(t)) {
            var i = A(t);
            return i.filters ? "this._applyFilters(" + i.expression + ",null," + JSON.stringify(i.filters) + ",false)" : "(" + t + ")"
        }
        return e ? t : "(" + t + ")"
    }

    function S(t, e, i, n) {
        R(t, 1, function() {
            e.appendChild(t)
        }, i, n)
    }

    function D(t, e, i, n) {
        R(t, 1, function() {
            B(t, e)
        }, i, n)
    }

    function P(t, e, i) {
        R(t, -1, function() {
            z(t)
        }, e, i)
    }

    function R(t, e, i, n, r) {
        var s = t.__v_trans;
        if (!s || !s.hooks && !Wi || !n._isCompiled || n.$parent && !n.$parent._isCompiled) return i(), void(r && r());
        var o = e > 0 ? "enter" : "leave";
        s[o](i, r)
    }

    function L(t) {
        if ("string" == typeof t) {
            t = document.querySelector(t)
        }
        return t
    }

    function H(t) {
        var e = document.documentElement,
            i = t && t.parentNode;
        return e === t || e === i || !(!i || 1 !== i.nodeType || !e.contains(i))
    }

    function M(t, e) {
        var i = t.getAttribute(e);
        return null !== i && t.removeAttribute(e), i
    }

    function W(t, e) {
        var i = M(t, ":" + e);
        return null === i && (i = M(t, "v-bind:" + e)), i
    }

    function I(t, e) {
        return t.hasAttribute(e) || t.hasAttribute(":" + e) || t.hasAttribute("v-bind:" + e)
    }

    function B(t, e) {
        e.parentNode.insertBefore(t, e)
    }

    function V(t, e) {
        e.nextSibling ? B(t, e.nextSibling) : e.parentNode.appendChild(t)
    }

    function z(t) {
        t.parentNode.removeChild(t)
    }

    function U(t, e) {
        e.firstChild ? B(t, e.firstChild) : e.appendChild(t)
    }

    function J(t, e) {
        var i = t.parentNode;
        i && i.replaceChild(e, t)
    }

    function q(t, e, i, n) {
        t.addEventListener(e, i, n)
    }

    function Q(t, e, i) {
        t.removeEventListener(e, i)
    }

    function G(t) {
        var e = t.className;
        return "object" == typeof e && (e = e.baseVal || ""), e
    }

    function K(t, e) {
        Li && !/svg$/.test(t.namespaceURI) ? t.className = e : t.setAttribute("class", e)
    }

    function Z(t, e) {
        if (t.classList) t.classList.add(e);
        else {
            var i = " " + G(t) + " ";
            i.indexOf(" " + e + " ") < 0 && K(t, (i + e).trim())
        }
    }

    function X(t, e) {
        if (t.classList) t.classList.remove(e);
        else {
            for (var i = " " + G(t) + " ", n = " " + e + " "; i.indexOf(n) >= 0;) i = i.replace(n, " ");
            K(t, i.trim())
        }
        t.className || t.removeAttribute("class")
    }

    function Y(t, e) {
        var i, n;
        if (it(t) && at(t.content) && (t = t.content), t.hasChildNodes())
            for (tt(t), n = e ? document.createDocumentFragment() : document.createElement("div"); i = t.firstChild;) n.appendChild(i);
        return n
    }

    function tt(t) {
        for (var e; e = t.firstChild, et(e);) t.removeChild(e);
        for (; e = t.lastChild, et(e);) t.removeChild(e)
    }

    function et(t) {
        return t && (3 === t.nodeType && !t.data.trim() || 8 === t.nodeType)
    }

    function it(t) {
        return t.tagName && "template" === t.tagName.toLowerCase()
    }

    function nt(t, e) {
        var i = _n.debug ? document.createComment(t) : document.createTextNode(e ? " " : "");
        return i.__v_anchor = !0, i
    }

    function rt(t) {
        if (t.hasAttributes())
            for (var e = t.attributes, i = 0, n = e.length; n > i; i++) {
                var r = e[i].name;
                if (wn.test(r)) return l(r.replace(wn, ""))
            }
    }

    function st(t, e, i) {
        for (var n; t !== e;) n = t.nextSibling, i(t), t = n;
        i(e)
    }

    function ot(t, e, i, n, r) {
        function s() {
            if (a++, o && a >= h.length) {
                for (var t = 0; t < h.length; t++) n.appendChild(h[t]);
                r && r()
            }
        }
        var o = !1,
            a = 0,
            h = [];
        st(t, e, function(t) {
            t === e && (o = !0), h.push(t), P(t, i, s)
        })
    }

    function at(t) {
        return t && 11 === t.nodeType
    }

    function ht(t) {
        if (t.outerHTML) return t.outerHTML;
        var e = document.createElement("div");
        return e.appendChild(t.cloneNode(!0)), e.innerHTML
    }

    function lt(t, e) {
        var i = t.tagName.toLowerCase(),
            n = t.hasAttributes();
        if (Cn.test(i) || $n.test(i)) {
            if (n) return ct(t)
        } else {
            if (gt(e, "components", i)) return {
                id: i
            };
            var r = n && ct(t);
            if (r) return r
        }
    }

    function ct(t) {
        var e = M(t, "is");
        return null != e ? {
            id: e
        } : (e = W(t, "is"), null != e ? {
            id: e,
            dynamic: !0
        } : void 0)
    }

    function ut(e, n) {
        var r, s, o;
        for (r in n) s = e[r], o = n[r], i(e, r) ? m(s) && m(o) && ut(s, o) : t(e, r, o);
        return e
    }

    function ft(t, e) {
        var i = Object.create(t);
        return e ? v(i, vt(e)) : i
    }

    function pt(t) {
        if (t.components)
            for (var e, i = t.components = vt(t.components), n = Object.keys(i), r = 0, s = n.length; s > r; r++) {
                var o = n[r];
                Cn.test(o) || $n.test(o) || (e = i[o], g(e) && (i[o] = yi.extend(e)))
            }
    }

    function dt(t) {
        var e, i, n = t.props;
        if (Fi(n))
            for (t.props = {}, e = n.length; e--;) i = n[e], "string" == typeof i ? t.props[i] = null : i.name && (t.props[i.name] = i);
        else if (g(n)) {
            var r = Object.keys(n);
            for (e = r.length; e--;) i = n[r[e]], "function" == typeof i && (n[r[e]] = {
                type: i
            })
        }
    }

    function vt(t) {
        if (Fi(t)) {
            for (var e, i = {}, n = t.length; n--;) {
                e = t[n];
                var r = "function" == typeof e ? e.options && e.options.name || e.id : e.name || e.id;
                r && (i[r] = e)
            }
            return i
        }
        return t
    }

    function mt(t, e, n) {
        function r(i) {
            var r = kn[i] || xn;
            o[i] = r(t[i], e[i], n, i)
        }
        pt(e), dt(e);
        var s, o = {};
        if (e.mixins)
            for (var a = 0, h = e.mixins.length; h > a; a++) t = mt(t, e.mixins[a], n);
        for (s in t) r(s);
        for (s in e) i(t, s) || r(s);
        return o
    }

    function gt(t, e, i, n) {
        if ("string" == typeof i) {
            var r, s = t[e],
                o = s[i] || s[r = l(i)] || s[r.charAt(0).toUpperCase() + r.slice(1)];
            return o
        }
    }

    function _t() {
        this.id = An++, this.subs = []
    }

    function yt(t) {
        jn = !1, t(), jn = !0
    }

    function bt(t) {
        if (this.value = t, this.dep = new _t, _(t, "__ob__", this), Fi(t)) {
            var e = Si ? wt : Ct;
            e(t, Tn, Nn), this.observeArray(t)
        } else this.walk(t)
    }

    function wt(t, e) {
        t.__proto__ = e
    }

    function Ct(t, e, i) {
        for (var n = 0, r = i.length; r > n; n++) {
            var s = i[n];
            _(t, s, e[s])
        }
    }

    function $t(t, e) {
        if (t && "object" == typeof t) {
            var n;
            return i(t, "__ob__") && t.__ob__ instanceof bt ? n = t.__ob__ : jn && (Fi(t) || g(t)) && Object.isExtensible(t) && !t._isVue && (n = new bt(t)), n && e && n.addVm(e), n
        }
    }

    function kt(t, e, i) {
        var n = new _t,
            r = Object.getOwnPropertyDescriptor(t, e);
        if (!r || r.configurable !== !1) {
            var s = r && r.get,
                o = r && r.set,
                a = $t(i);
            Object.defineProperty(t, e, {
                enumerable: !0,
                configurable: !0,
                get: function() {
                    var e = s ? s.call(t) : i;
                    if (_t.target && (n.depend(), a && a.dep.depend(), Fi(e)))
                        for (var r, o = 0, h = e.length; h > o; o++) r = e[o], r && r.__ob__ && r.__ob__.dep.depend();
                    return e
                },
                set: function(e) {
                    var r = s ? s.call(t) : i;
                    e !== r && (o ? o.call(t, e) : i = e, a = $t(e), n.notify())
                }
            })
        }
    }

    function xt(t) {
        t.prototype._init = function(t) {
            t = t || {}, this.$el = null, this.$parent = t.parent, this.$root = this.$parent ? this.$parent.$root : this, this.$children = [], this.$refs = {}, this.$els = {}, this._watchers = [], this._directives = [], this._uid = Fn++, this._isVue = !0, this._events = {}, this._eventsCount = {}, this._isFragment = !1, this._fragment = this._fragmentStart = this._fragmentEnd = null, this._isCompiled = this._isDestroyed = this._isReady = this._isAttached = this._isBeingDestroyed = this._vForRemoving = !1, this._unlinkFn = null, this._context = t._context || this.$parent, this._scope = t._scope, this._frag = t._frag, this._frag && this._frag.children.push(this), this.$parent && this.$parent.$children.push(this), t = this.$options = mt(this.constructor.options, t, this), this._updateRef(), this._data = {}, this._runtimeData = t.data, this._callHook("init"), this._initState(), this._initEvents(), this._callHook("created"), t.el && this.$mount(t.el)
        }
    }

    function At(t) {
        if (void 0 === t) return "eof";
        var e = t.charCodeAt(0);
        switch (e) {
            case 91:
            case 93:
            case 46:
            case 34:
            case 39:
            case 48:
                return t;
            case 95:
            case 36:
                return "ident";
            case 32:
            case 9:
            case 10:
            case 13:
            case 160:
            case 65279:
            case 8232:
            case 8233:
                return "ws"
        }
        return e >= 97 && 122 >= e || e >= 65 && 90 >= e ? "ident" : e >= 49 && 57 >= e ? "number" : "else"
    }

    function Ot(t) {
        var e = t.trim();
        return "0" === t.charAt(0) && isNaN(t) ? !1 : n(e) ? h(e) : "*" + e
    }

    function Tt(t) {
        function e() {
            var e = t[c + 1];
            return u === Vn && "'" === e || u === zn && '"' === e ? (c++, n = "\\" + e, p[Dn](), !0) : void 0
        }
        var i, n, r, s, o, a, h, l = [],
            c = -1,
            u = Hn,
            f = 0,
            p = [];
        for (p[Pn] = function() {
                void 0 !== r && (l.push(r), r = void 0)
            }, p[Dn] = function() {
                void 0 === r ? r = n : r += n
            }, p[Rn] = function() {
                p[Dn](), f++
            }, p[Ln] = function() {
                if (f > 0) f--, u = Bn, p[Dn]();
                else {
                    if (f = 0, r = Ot(r), r === !1) return !1;
                    p[Pn]()
                }
            }; null != u;)
            if (c++, i = t[c], "\\" !== i || !e()) {
                if (s = At(i), h = qn[u], o = h[s] || h["else"] || Jn, o === Jn) return;
                if (u = o[0], a = p[o[1]], a && (n = o[2], n = void 0 === n ? i : n, a() === !1)) return;
                if (u === Un) return l.raw = t, l
            }
    }

    function Nt(t) {
        var e = Sn.get(t);
        return e || (e = Tt(t), e && Sn.put(t, e)), e
    }

    function jt(t, e) {
        return Ht(e).get(t)
    }

    function Et(e, i, n) {
        var r = e;
        if ("string" == typeof i && (i = Tt(i)), !i || !m(e)) return !1;
        for (var s, o, a = 0, h = i.length; h > a; a++) s = e, o = i[a], "*" === o.charAt(0) && (o = Ht(o.slice(1)).get.call(r, r)), h - 1 > a ? (e = e[o], m(e) || (e = {}, t(s, o, e))) : Fi(e) ? e.$set(o, n) : o in e ? e[o] = n : t(e, o, n);
        return !0
    }

    function Ft(t, e) {
        var i = hr.length;
        return hr[i] = e ? t.replace(ir, "\\n") : t, '"' + i + '"'
    }

    function St(t) {
        var e = t.charAt(0),
            i = t.slice(1);
        return Xn.test(i) ? t : (i = i.indexOf('"') > -1 ? i.replace(rr, Dt) : i, e + "scope." + i)
    }

    function Dt(t, e) {
        return hr[e]
    }

    function Pt(t) {
        tr.test(t), hr.length = 0;
        var e = t.replace(nr, Ft).replace(er, "");
        return e = (" " + e).replace(or, St).replace(rr, Dt), Rt(e)
    }

    function Rt(t) {
        try {
            return new Function("scope", "return " + t + ";")
        } catch (e) {}
    }

    function Lt(t) {
        var e = Nt(t);
        return e ? function(t, i) {
            Et(t, e, i)
        } : void 0
    }

    function Ht(t, e) {
        t = t.trim();
        var i = Kn.get(t);
        if (i) return e && !i.set && (i.set = Lt(i.exp)), i;
        var n = {
            exp: t
        };
        return n.get = Mt(t) && t.indexOf("[") < 0 ? Rt("scope." + t) : Pt(t), e && (n.set = Lt(t)), Kn.put(t, n), n
    }

    function Mt(t) {
        return sr.test(t) && !ar.test(t) && "Math." !== t.slice(0, 5)
    }

    function Wt() {
        cr = [], ur = [], fr = {}, pr = {}, dr = vr = !1
    }

    function It() {
        Bt(cr), vr = !0, Bt(ur), Pi && _n.devtools && Pi.emit("flush"), Wt()
    }

    function Bt(t) {
        for (Qn = 0; Qn < t.length; Qn++) {
            var e = t[Qn],
                i = e.id;
            fr[i] = null, e.run()
        }
    }

    function Vt(t) {
        var e = t.id;
        if (null == fr[e])
            if (vr && !t.user) ur.splice(Qn + 1, 0, t);
            else {
                var i = t.user ? ur : cr;
                fr[e] = i.length, i.push(t), dr || (dr = !0, Ui(It))
            }
    }

    function zt(t, e, i, n) {
        n && v(this, n);
        var r = "function" == typeof e;
        if (this.vm = t, t._watchers.push(this), this.expression = e, this.cb = i, this.id = ++mr, this.active = !0, this.dirty = this.lazy, this.deps = [], this.newDeps = [], this.depIds = Object.create(null), this.newDepIds = null, this.prevError = null, r) this.getter = e, this.setter = void 0;
        else {
            var s = Ht(e, this.twoWay);
            this.getter = s.get, this.setter = s.set
        }
        this.value = this.lazy ? void 0 : this.get(), this.queued = this.shallow = !1
    }

    function Ut(t) {
        var e, i;
        if (Fi(t))
            for (e = t.length; e--;) Ut(t[e]);
        else if (m(t))
            for (i = Object.keys(t), e = i.length; e--;) Ut(t[i[e]])
    }

    function Jt(t) {
        return it(t) && at(t.content)
    }

    function qt(t, e) {
        var i = e ? t : t.trim(),
            n = _r.get(i);
        if (n) return n;
        var r = document.createDocumentFragment(),
            s = t.match(wr),
            o = Cr.test(t);
        if (s || o) {
            var a = s && s[1],
                h = br[a] || br.efault,
                l = h[0],
                c = h[1],
                u = h[2],
                f = document.createElement("div");
            for (f.innerHTML = c + t + u; l--;) f = f.lastChild;
            for (var p; p = f.firstChild;) r.appendChild(p)
        } else r.appendChild(document.createTextNode(t));
        return e || tt(r), _r.put(i, r), r
    }

    function Qt(t) {
        if (Jt(t)) return tt(t.content), t.content;
        if ("SCRIPT" === t.tagName) return qt(t.textContent);
        for (var e, i = Gt(t), n = document.createDocumentFragment(); e = i.firstChild;) n.appendChild(e);
        return tt(n), n
    }

    function Gt(t) {
        if (!t.querySelectorAll) return t.cloneNode();
        var e, i, n, r = t.cloneNode(!0);
        if ($r) {
            var s = r;
            if (Jt(t) && (t = t.content, s = r.content), i = t.querySelectorAll("template"), i.length)
                for (n = s.querySelectorAll("template"), e = n.length; e--;) n[e].parentNode.replaceChild(Gt(i[e]), n[e])
        }
        if (kr)
            if ("TEXTAREA" === t.tagName) r.value = t.value;
            else if (i = t.querySelectorAll("textarea"), i.length)
            for (n = r.querySelectorAll("textarea"), e = n.length; e--;) n[e].value = i[e].value;
        return r
    }

    function Kt(t, e, i) {
        var n, r;
        return at(t) ? (tt(t), e ? Gt(t) : t) : ("string" == typeof t ? i || "#" !== t.charAt(0) ? r = qt(t, i) : (r = yr.get(t), r || (n = document.getElementById(t.slice(1)), n && (r = Qt(n), yr.put(t, r)))) : t.nodeType && (r = Qt(t)), r && e ? Gt(r) : r)
    }

    function Zt(t, e, i, n, r, s) {
        this.children = [], this.childFrags = [], this.vm = e, this.scope = r, this.inserted = !1, this.parentFrag = s, s && s.childFrags.push(this), this.unlink = t(e, i, n, r, this);
        var o = this.single = 1 === i.childNodes.length && !i.childNodes[0].__v_anchor;
        o ? (this.node = i.childNodes[0], this.before = Xt, this.remove = Yt) : (this.node = nt("fragment-start"), this.end = nt("fragment-end"), this.frag = i, U(this.node, i), i.appendChild(this.end), this.before = te, this.remove = ee), this.node.__v_frag = this
    }

    function Xt(t, e) {
        this.inserted = !0;
        var i = e !== !1 ? D : B;
        i(this.node, t, this.vm), H(this.node) && this.callHook(ie)
    }

    function Yt() {
        this.inserted = !1;
        var t = H(this.node),
            e = this;
        this.beforeRemove(), P(this.node, this.vm, function() {
            t && e.callHook(ne), e.destroy()
        })
    }

    function te(t, e) {
        this.inserted = !0;
        var i = this.vm,
            n = e !== !1 ? D : B;
        st(this.node, this.end, function(e) {
            n(e, t, i)
        }), H(this.node) && this.callHook(ie)
    }

    function ee() {
        this.inserted = !1;
        var t = this,
            e = H(this.node);
        this.beforeRemove(), ot(this.node, this.end, this.vm, this.frag, function() {
            e && t.callHook(ne), t.destroy()
        })
    }

    function ie(t) {
        !t._isAttached && H(t.$el) && t._callHook("attached")
    }

    function ne(t) {
        t._isAttached && !H(t.$el) && t._callHook("detached")
    }

    function re(t, e) {
        this.vm = t;
        var i, n = "string" == typeof e;
        n || it(e) ? i = Kt(e, !0) : (i = document.createDocumentFragment(), i.appendChild(e)), this.template = i;
        var r, s = t.constructor.cid;
        if (s > 0) {
            var o = s + (n ? e : ht(e));
            r = Or.get(o), r || (r = Se(i, t.$options, !0), Or.put(o, r))
        } else r = Se(i, t.$options, !0);
        this.linker = r
    }

    function se(t, e, i) {
        var n = t.node.previousSibling;
        if (n) {
            for (t = n.__v_frag; !(t && t.forId === i && t.inserted || n === e);) {
                if (n = n.previousSibling, !n) return;
                t = n.__v_frag
            }
            return t
        }
    }

    function oe(t) {
        var e = t.node;
        if (t.end)
            for (; !e.__vue__ && e !== t.end && e.nextSibling;) e = e.nextSibling;
        return e.__vue__
    }

    function ae(t) {
        for (var e = -1, i = new Array(Math.floor(t)); ++e < t;) i[e] = e;
        return i
    }

    function he(t, e, i) {
        for (var n, r, s, o = e ? [] : null, a = 0, h = t.options.length; h > a; a++)
            if (n = t.options[a], s = i ? n.hasAttribute("selected") : n.selected) {
                if (r = n.hasOwnProperty("_value") ? n._value : n.value, !e) return r;
                o.push(r)
            }
        return o
    }

    function le(t, e) {
        for (var i = t.length; i--;)
            if (C(t[i], e)) return i;
        return -1
    }

    function ce(t, e) {
        var i = e.map(function(t) {
            var e = t.charCodeAt(0);
            return e > 47 && 58 > e ? parseInt(t, 10) : 1 === t.length && (e = t.toUpperCase().charCodeAt(0), e > 64 && 91 > e) ? e : Qr[t]
        });
        return i = [].concat.apply([], i),
            function(e) {
                return i.indexOf(e.keyCode) > -1 ? t.call(this, e) : void 0
            }
    }

    function ue(t) {
        return function(e) {
            return e.stopPropagation(), t.call(this, e)
        }
    }

    function fe(t) {
        return function(e) {
            return e.preventDefault(), t.call(this, e)
        }
    }

    function pe(t) {
        return function(e) {
            return e.target === e.currentTarget ? t.call(this, e) : void 0
        }
    }

    function de(t) {
        if (Yr[t]) return Yr[t];
        var e = ve(t);
        return Yr[t] = Yr[e] = e, e
    }

    function ve(t) {
        t = u(t);
        var e = l(t),
            i = e.charAt(0).toUpperCase() + e.slice(1);
        ts || (ts = document.createElement("div"));
        for (var n, r = Kr.length; r--;)
            if (n = Zr[r] + i, n in ts.style) return {
                kebab: Kr[r] + t,
                camel: n
            };
        return e in ts.style ? {
            kebab: t,
            camel: e
        } : void 0
    }

    function me(t, e) {
        for (var i = Object.keys(e), n = 0, r = i.length; r > n; n++) {
            var s = i[n];
            e[s] && _e(t, s, Z)
        }
    }

    function ge(t) {
        for (var e = {}, i = t.trim().split(/\s+/), n = 0, r = i.length; r > n; n++) e[i[n]] = !0;
        return e
    }

    function _e(t, e, i) {
        if (e = e.trim(), -1 === e.indexOf(" ")) return void i(t, e);
        for (var n = e.split(/\s+/), r = 0, s = n.length; s > r; r++) i(t, n[r])
    }

    function ye(t, e, i) {
        function n() {
            ++s >= r ? i() : t[s].call(e, n)
        }
        var r = t.length,
            s = 0;
        t[0].call(e, n)
    }

    function be(t, e, i) {
        for (var r, s, o, a, h, c, f, p = [], d = Object.keys(e), v = d.length; v--;) s = d[v], r = e[s] || ms, h = l(s), gs.test(h) && (f = {
            name: s,
            path: h,
            options: r,
            mode: vs.ONE_WAY,
            raw: null
        }, o = u(s), null === (a = W(t, o)) && (null !== (a = W(t, o + ".sync")) ? f.mode = vs.TWO_WAY : null !== (a = W(t, o + ".once")) && (f.mode = vs.ONE_TIME)), null !== a ? (f.raw = a, c = A(a), a = c.expression, f.filters = c.filters, n(a) && !c.filters ? f.optimizedLiteral = !0 : f.dynamic = !0, f.parentPath = a) : null !== (a = M(t, o)) && (f.raw = a), p.push(f));
        return we(p)
    }

    function we(t) {
        return function(e, i) {
            e._props = {};
            for (var n, r, s, l, c, f = t.length; f--;)
                if (n = t[f], c = n.raw, r = n.path, s = n.options, e._props[r] = n, null === c) $e(e, n, void 0);
                else if (n.dynamic) n.mode === vs.ONE_TIME ? (l = (i || e._context || e).$get(n.parentPath), $e(e, n, l)) : e._context ? e._bindDir({
                name: "prop",
                def: ys,
                prop: n
            }, null, null, i) : $e(e, n, e.$get(n.parentPath));
            else if (n.optimizedLiteral) {
                var p = h(c);
                l = p === c ? a(o(c)) : p, $e(e, n, l)
            } else l = s.type !== Boolean || "" !== c && c !== u(n.name) ? c : !0, $e(e, n, l)
        }
    }

    function Ce(t, e, i, n) {
        var r = e.dynamic && Mt(e.parentPath),
            s = i;
        void 0 === s && (s = xe(t, e)), s = Oe(e, s);
        var o = s !== i;
        Ae(e, s, t) || (s = void 0), r && !o ? yt(function() {
            n(s)
        }) : n(s)
    }

    function $e(t, e, i) {
        Ce(t, e, i, function(i) {
            kt(t, e.path, i)
        })
    }

    function ke(t, e, i) {
        Ce(t, e, i, function(i) {
            t[e.path] = i
        })
    }

    function xe(t, e) {
        var n = e.options;
        if (!i(n, "default")) return n.type === Boolean ? !1 : void 0;
        var r = n["default"];
        return m(r), "function" == typeof r && n.type !== Function ? r.call(t) : r
    }

    function Ae(t, e, i) {
        if (!t.options.required && (null === t.raw || null == e)) return !0;
        var n = t.options,
            r = n.type,
            s = !r,
            o = [];
        if (r) {
            Fi(r) || (r = [r]);
            for (var a = 0; a < r.length && !s; a++) {
                var h = Te(e, r[a]);
                o.push(h.expectedType), s = h.valid
            }
        }
        if (!s) return !1;
        var l = n.validator;
        return !l || l(e)
    }

    function Oe(t, e) {
        var i = t.options.coerce;
        return i ? i(e) : e
    }

    function Te(t, e) {
        var i, n;
        return e === String ? (n = "string", i = typeof t === n) : e === Number ? (n = "number", i = typeof t === n) : e === Boolean ? (n = "boolean", i = typeof t === n) : e === Function ? (n = "function", i = typeof t === n) : e === Object ? (n = "object", i = g(t)) : e === Array ? (n = "array", i = Fi(t)) : i = t instanceof e, {
            valid: i,
            expectedType: n
        }
    }

    function Ne(t) {
        bs.push(t), ws || (ws = !0, Ui(je))
    }

    function je() {
        for (var t = document.documentElement.offsetHeight, e = 0; e < bs.length; e++) bs[e]();
        return bs = [], ws = !1, t
    }

    function Ee(t, e, i, n) {
        this.id = e, this.el = t, this.enterClass = i && i.enterClass || e + "-enter", this.leaveClass = i && i.leaveClass || e + "-leave", this.hooks = i, this.vm = n, this.pendingCssEvent = this.pendingCssCb = this.cancel = this.pendingJsCb = this.op = this.cb = null, this.justEntered = !1, this.entered = this.left = !1, this.typeCache = {}, this.type = i && i.type;
        var r = this;
        ["enterNextTick", "enterDone", "leaveNextTick", "leaveDone"].forEach(function(t) {
            r[t] = p(r[t], r)
        })
    }

    function Fe(t) {
        if (/svg$/.test(t.namespaceURI)) {
            var e = t.getBoundingClientRect();
            return !(e.width || e.height)
        }
        return !(t.offsetWidth || t.offsetHeight || t.getClientRects().length)
    }

    function Se(t, e, i) {
        var n = i || !e._asComponent ? We(t, e) : null,
            r = n && n.terminal || "SCRIPT" === t.tagName || !t.hasChildNodes() ? null : Je(t.childNodes, e);
        return function(t, e, i, s, o) {
            var a = d(e.childNodes),
                h = De(function() {
                    n && n(t, e, i, s, o), r && r(t, a, i, s, o)
                }, t);
            return Re(t, h)
        }
    }

    function De(t, e) {
        e._directives = [];
        var i = e._directives.length;
        t();
        var n = e._directives.slice(i);
        n.sort(Pe);
        for (var r = 0, s = n.length; s > r; r++) n[r]._bind();
        return n
    }

    function Pe(t, e) {
        return t = t.descriptor.def.priority || Rs, e = e.descriptor.def.priority || Rs, t > e ? -1 : t === e ? 0 : 1
    }

    function Re(t, e, i, n) {
        function r(r) {
            Le(t, e, r), i && n && Le(i, n)
        }
        return r.dirs = e, r
    }

    function Le(t, e, i) {
        for (var n = e.length; n--;) e[n]._teardown()
    }

    function He(t, e, i, n) {
        var r = be(e, i, t),
            s = De(function() {
                r(t, n)
            }, t);
        return Re(t, s)
    }

    function Me(t, e, i) {
        var n, r, s = e._containerAttrs,
            o = e._replacerAttrs;
        return 11 !== t.nodeType && (e._asComponent ? (s && i && (n = Ye(s, i)), o && (r = Ye(o, e))) : r = Ye(t.attributes, e)), e._containerAttrs = e._replacerAttrs = null,
            function(t, e, i) {
                var s, o = t._context;
                o && n && (s = De(function() {
                    n(o, e, null, i)
                }, o));
                var a = De(function() {
                    r && r(t, e)
                }, t);
                return Re(t, a, o, s)
            }
    }

    function We(t, e) {
        var i = t.nodeType;
        return 1 === i && "SCRIPT" !== t.tagName ? Ie(t, e) : 3 === i && t.data.trim() ? Be(t, e) : null
    }

    function Ie(t, e) {
        if ("TEXTAREA" === t.tagName) {
            var i = N(t.value);
            i && (t.setAttribute(":value", j(i)), t.value = "")
        }
        var n, r = t.hasAttributes(),
            s = r && d(t.attributes);
        return r && (n = Ke(t, s, e)), n || (n = Qe(t, e)), n || (n = Ge(t, e)), !n && r && (n = Ye(s, e)), n
    }

    function Be(t, e) {
        if (t._skip) return Ve;
        var i = N(t.wholeText);
        if (!i) return null;
        for (var n = t.nextSibling; n && 3 === n.nodeType;) n._skip = !0, n = n.nextSibling;
        for (var r, s, o = document.createDocumentFragment(), a = 0, h = i.length; h > a; a++) s = i[a], r = s.tag ? ze(s, e) : document.createTextNode(s.value), o.appendChild(r);
        return Ue(i, o, e)
    }

    function Ve(t, e) {
        z(e)
    }

    function ze(t, e) {
        function i(e) {
            if (!t.descriptor) {
                var i = A(t.value);
                t.descriptor = {
                    name: e,
                    def: fs[e],
                    expression: i.expression,
                    filters: i.filters
                }
            }
        }
        var n;
        return t.oneTime ? n = document.createTextNode(t.value) : t.html ? (n = document.createComment("v-html"), i("html")) : (n = document.createTextNode(" "), i("text")), n
    }

    function Ue(t, e) {
        return function(i, n, r, s) {
            for (var o, a, h, l = e.cloneNode(!0), c = d(l.childNodes), u = 0, f = t.length; f > u; u++) o = t[u], a = o.value, o.tag && (h = c[u], o.oneTime ? (a = (s || i).$eval(a), o.html ? J(h, Kt(a, !0)) : h.data = a) : i._bindDir(o.descriptor, h, r, s));
            J(n, l)
        }
    }

    function Je(t, e) {
        for (var i, n, r, s = [], o = 0, a = t.length; a > o; o++) r = t[o], i = We(r, e), n = i && i.terminal || "SCRIPT" === r.tagName || !r.hasChildNodes() ? null : Je(r.childNodes, e), s.push(i, n);
        return s.length ? qe(s) : null
    }

    function qe(t) {
        return function(e, i, n, r, s) {
            for (var o, a, h, l = 0, c = 0, u = t.length; u > l; c++) {
                o = i[c], a = t[l++], h = t[l++];
                var f = d(o.childNodes);
                a && a(e, o, n, r, s), h && h(e, f, n, r, s)
            }
        }
    }

    function Qe(t, e) {
        var i = t.tagName.toLowerCase();
        if (!Cn.test(i)) {
            var n = gt(e, "elementDirectives", i);
            return n ? Xe(t, i, "", e, n) : void 0
        }
    }

    function Ge(t, e) {
        var i = lt(t, e);
        if (i) {
            var n = rt(t),
                r = {
                    name: "component",
                    ref: n,
                    expression: i.id,
                    def: js.component,
                    modifiers: {
                        literal: !i.dynamic
                    }
                },
                s = function(t, e, i, s, o) {
                    n && kt((s || t).$refs, n, null), t._bindDir(r, e, i, s, o)
                };
            return s.terminal = !0, s
        }
    }

    function Ke(t, e, i) {
        if (null !== M(t, "v-pre")) return Ze;
        if (t.hasAttribute("v-else")) {
            var n = t.previousElementSibling;
            if (n && n.hasAttribute("v-if")) return Ze
        }
        for (var r, s, o, a, h, l, c, u, f, p, d = 0, v = e.length; v > d; d++) r = e[d], a = ti(r.name), s = r.name.replace(Ds, ""), (h = s.match(Ss)) && (f = gt(i, "directives", h[1]), f && f.terminal && (!p || (f.priority || Ls) > p.priority) && (p = f, c = r.name, o = r.value, l = h[1], u = h[2]));
        return p ? Xe(t, l, o, i, p, c, u, a) : void 0
    }

    function Ze() {}

    function Xe(t, e, i, n, r, s, o, a) {
        var h = A(i),
            l = {
                name: e,
                arg: o,
                expression: h.expression,
                filters: h.filters,
                raw: i,
                attr: s,
                modifiers: a,
                def: r
            };
        "for" !== e && "router-view" !== e || (l.ref = rt(t));
        var c = function(t, e, i, n, r) {
            l.ref && kt((n || t).$refs, l.ref, null), t._bindDir(l, e, i, n, r)
        };
        return c.terminal = !0, c
    }

    function Ye(t, e) {
        function i(t, e, i) {
            var n = i && ii(i),
                r = !n && A(s);
            v.push({
                name: t,
                attr: o,
                raw: a,
                def: e,
                arg: l,
                modifiers: c,
                expression: r && r.expression,
                filters: r && r.filters,
                interp: i,
                hasOneTime: n
            })
        }
        for (var n, r, s, o, a, h, l, c, u, f, p, d = t.length, v = []; d--;)
            if (n = t[d], r = o = n.name, s = a = n.value, f = N(s), l = null, c = ti(r), r = r.replace(Ds, ""), f) s = j(f), l = r, i("bind", fs.bind, f);
            else if (Ps.test(r)) c.literal = !Es.test(r), i("transition", js.transition);
        else if (Fs.test(r)) l = r.replace(Fs, ""), i("on", fs.on);
        else if (Es.test(r)) h = r.replace(Es, ""), "style" === h || "class" === h ? i(h, js[h]) : (l = h, i("bind", fs.bind));
        else if (p = r.match(Ss)) {
            if (h = p[1], l = p[2], "else" === h) continue;
            u = gt(e, "directives", h, !0), u && i(h, u)
        }
        return v.length ? ei(v) : void 0
    }

    function ti(t) {
        var e = Object.create(null),
            i = t.match(Ds);
        if (i)
            for (var n = i.length; n--;) e[i[n].slice(1)] = !0;
        return e
    }

    function ei(t) {
        return function(e, i, n, r, s) {
            for (var o = t.length; o--;) e._bindDir(t[o], i, n, r, s)
        }
    }

    function ii(t) {
        for (var e = t.length; e--;)
            if (t[e].oneTime) return !0
    }

    function ni(t, e) {
        return e && (e._containerAttrs = si(t)), it(t) && (t = Kt(t)), e && (e._asComponent && !e.template && (e.template = "<slot></slot>"), e.template && (e._content = Y(t), t = ri(t, e))), at(t) && (U(nt("v-start", !0), t), t.appendChild(nt("v-end", !0))), t
    }

    function ri(t, e) {
        var i = e.template,
            n = Kt(i, !0);
        if (n) {
            var r = n.firstChild,
                s = r.tagName && r.tagName.toLowerCase();
            return e.replace ? (t === document.body, n.childNodes.length > 1 || 1 !== r.nodeType || "component" === s || gt(e, "components", s) || I(r, "is") || gt(e, "elementDirectives", s) || r.hasAttribute("v-for") || r.hasAttribute("v-if") ? n : (e._replacerAttrs = si(r), oi(t, r), r)) : (t.appendChild(n), t)
        }
    }

    function si(t) {
        return 1 === t.nodeType && t.hasAttributes() ? d(t.attributes) : void 0
    }

    function oi(t, e) {
        for (var i, n, r = t.attributes, s = r.length; s--;) i = r[s].name, n = r[s].value, e.hasAttribute(i) || Hs.test(i) ? "class" !== i || N(n) || n.trim().split(/\s+/).forEach(function(t) {
            Z(e, t)
        }) : e.setAttribute(i, n)
    }

    function ai(t, e) {
        if (e) {
            for (var i, n, r = t._slotContents = Object.create(null), s = 0, o = e.children.length; o > s; s++) i = e.children[s], (n = i.getAttribute("slot")) && (r[n] || (r[n] = [])).push(i);
            for (n in r) r[n] = hi(r[n], e);
            e.hasChildNodes() && (r["default"] = hi(e.childNodes, e))
        }
    }

    function hi(t, e) {
        var i = document.createDocumentFragment();
        t = d(t);
        for (var n = 0, r = t.length; r > n; n++) {
            var s = t[n];
            !it(s) || s.hasAttribute("v-if") || s.hasAttribute("v-for") || (e.removeChild(s), s = Kt(s)), i.appendChild(s)
        }
        return i
    }

    function li(t) {
        function e() {}

        function n(t, e) {
            var i = new zt(e, t, null, {
                lazy: !0
            });
            return function() {
                return i.dirty && i.evaluate(), _t.target && i.depend(), i.value
            }
        }
        Object.defineProperty(t.prototype, "$data", {
            get: function() {
                return this._data
            },
            set: function(t) {
                t !== this._data && this._setData(t)
            }
        }), t.prototype._initState = function() {
            this._initProps(), this._initMeta(), this._initMethods(), this._initData(), this._initComputed()
        }, t.prototype._initProps = function() {
            var t = this.$options,
                e = t.el,
                i = t.props;
            e = t.el = L(e), this._propsUnlinkFn = e && 1 === e.nodeType && i ? He(this, e, i, this._scope) : null
        }, t.prototype._initData = function() {
            var t = this.$options.data,
                e = this._data = t ? t() : {};
            g(e) || (e = {});
            var n, r, s = this._props,
                o = this._runtimeData ? "function" == typeof this._runtimeData ? this._runtimeData() : this._runtimeData : null,
                a = Object.keys(e);
            for (n = a.length; n--;) r = a[n], (!s || !i(s, r) || o && i(o, r) && null === s[r].raw) && this._proxy(r);
            $t(e, this)
        }, t.prototype._setData = function(t) {
            t = t || {};
            var e = this._data;
            this._data = t;
            var n, r, s;
            for (n = Object.keys(e), s = n.length; s--;) r = n[s], r in t || this._unproxy(r);
            for (n = Object.keys(t), s = n.length; s--;) r = n[s], i(this, r) || this._proxy(r);
            e.__ob__.removeVm(this), $t(t, this), this._digest()
        }, t.prototype._proxy = function(t) {
            if (!r(t)) {
                var e = this;
                Object.defineProperty(e, t, {
                    configurable: !0,
                    enumerable: !0,
                    get: function() {
                        return e._data[t]
                    },
                    set: function(i) {
                        e._data[t] = i
                    }
                })
            }
        }, t.prototype._unproxy = function(t) {
            r(t) || delete this[t]
        }, t.prototype._digest = function() {
            for (var t = 0, e = this._watchers.length; e > t; t++) this._watchers[t].update(!0)
        }, t.prototype._initComputed = function() {
            var t = this.$options.computed;
            if (t)
                for (var i in t) {
                    var r = t[i],
                        s = {
                            enumerable: !0,
                            configurable: !0
                        };
                    "function" == typeof r ? (s.get = n(r, this), s.set = e) : (s.get = r.get ? r.cache !== !1 ? n(r.get, this) : p(r.get, this) : e, s.set = r.set ? p(r.set, this) : e), Object.defineProperty(this, i, s)
                }
        }, t.prototype._initMethods = function() {
            var t = this.$options.methods;
            if (t)
                for (var e in t) this[e] = p(t[e], this)
        }, t.prototype._initMeta = function() {
            var t = this.$options._meta;
            if (t)
                for (var e in t) kt(this, e, t[e])
        }
    }

    function ci(t) {
        function e(t, e) {
            for (var i, n, r = e.attributes, s = 0, o = r.length; o > s; s++) i = r[s].name, Ws.test(i) && (i = i.replace(Ws, ""), n = (t._scope || t._context).$eval(r[s].value, !0), "function" == typeof n && (n._fromParent = !0, t.$on(i.replace(Ws), n)))
        }

        function i(t, e, i) {
            if (i) {
                var r, s, o, a;
                for (s in i)
                    if (r = i[s], Fi(r))
                        for (o = 0, a = r.length; a > o; o++) n(t, e, s, r[o]);
                    else n(t, e, s, r)
            }
        }

        function n(t, e, i, r, s) {
            var o = typeof r;
            if ("function" === o) t[e](i, r, s);
            else if ("string" === o) {
                var a = t.$options.methods,
                    h = a && a[r];
                h && t[e](i, h, s)
            } else r && "object" === o && n(t, e, i, r.handler, r)
        }

        function r() {
            this._isAttached || (this._isAttached = !0, this.$children.forEach(s))
        }

        function s(t) {
            !t._isAttached && H(t.$el) && t._callHook("attached")
        }

        function o() {
            this._isAttached && (this._isAttached = !1, this.$children.forEach(a))
        }

        function a(t) {
            t._isAttached && !H(t.$el) && t._callHook("detached")
        }
        t.prototype._initEvents = function() {
            var t = this.$options;
            t._asComponent && e(this, t.el), i(this, "$on", t.events), i(this, "$watch", t.watch)
        }, t.prototype._initDOMHooks = function() {
            this.$on("hook:attached", r), this.$on("hook:detached", o)
        }, t.prototype._callHook = function(t) {
            this.$emit("pre-hook:" + t);
            var e = this.$options[t];
            if (e)
                for (var i = 0, n = e.length; n > i; i++) e[i].call(this);
            this.$emit("hook:" + t)
        }
    }

    function ui() {}

    function fi(t, e, i, n, r, s) {
        this.vm = e, this.el = i, this.descriptor = t, this.name = t.name, this.expression = t.expression, this.arg = t.arg, this.modifiers = t.modifiers, this.filters = t.filters, this.literal = this.modifiers && this.modifiers.literal, this._locked = !1, this._bound = !1, this._listeners = null, this._host = n, this._scope = r, this._frag = s
    }

    function pi(t) {
        t.prototype._updateRef = function(t) {
            var e = this.$options._ref;
            if (e) {
                var i = (this._scope || this._context).$refs;
                t ? i[e] === this && (i[e] = null) : i[e] = this
            }
        }, t.prototype._compile = function(t) {
            var e = this.$options,
                i = t;
            if (t = ni(t, e), this._initElement(t), 1 !== t.nodeType || null === M(t, "v-pre")) {
                var n = this._context && this._context.$options,
                    r = Me(t, e, n);
                ai(this, e._content);
                var s, o = this.constructor;
                e._linkerCachable && (s = o.linker, s || (s = o.linker = Se(t, e)));
                var a = r(this, t, this._scope),
                    h = s ? s(this, t) : Se(t, e)(this, t);
                this._unlinkFn = function() {
                    a(), h(!0)
                }, e.replace && J(i, t), this._isCompiled = !0, this._callHook("compiled")
            }
        }, t.prototype._initElement = function(t) {
            at(t) ? (this._isFragment = !0, this.$el = this._fragmentStart = t.firstChild, this._fragmentEnd = t.lastChild, 3 === this._fragmentStart.nodeType && (this._fragmentStart.data = this._fragmentEnd.data = ""), this._fragment = t) : this.$el = t, this.$el.__vue__ = this, this._callHook("beforeCompile")
        }, t.prototype._bindDir = function(t, e, i, n, r) {
            this._directives.push(new fi(t, this, e, i, n, r))
        }, t.prototype._destroy = function(t, e) {
            if (this._isBeingDestroyed) return void(e || this._cleanup());
            var i, n, r = this,
                s = function() {
                    !i || n || e || r._cleanup()
                };
            t && this.$el && (n = !0, this.$remove(function() {
                n = !1, s()
            })), this._callHook("beforeDestroy"), this._isBeingDestroyed = !0;
            var o, a = this.$parent;
            for (a && !a._isBeingDestroyed && (a.$children.$remove(this), this._updateRef(!0)), o = this.$children.length; o--;) this.$children[o].$destroy();
            for (this._propsUnlinkFn && this._propsUnlinkFn(), this._unlinkFn && this._unlinkFn(), o = this._watchers.length; o--;) this._watchers[o].teardown();
            this.$el && (this.$el.__vue__ = null), i = !0, s()
        }, t.prototype._cleanup = function() {
            this._isDestroyed || (this._frag && this._frag.children.$remove(this), this._data.__ob__ && this._data.__ob__.removeVm(this), this.$el = this.$parent = this.$root = this.$children = this._watchers = this._context = this._scope = this._directives = null, this._isDestroyed = !0, this._callHook("destroyed"), this.$off())
        }
    }

    function di(t) {
        t.prototype._applyFilters = function(t, e, i, n) {
            var r, s, o, a, h, l, c, u, f;
            for (l = 0, c = i.length; c > l; l++)
                if (r = i[n ? c - l - 1 : l], s = gt(this.$options, "filters", r.name, !0), s && (s = n ? s.write : s.read || s, "function" == typeof s)) {
                    if (o = n ? [t, e] : [t], h = n ? 2 : 1, r.args)
                        for (u = 0, f = r.args.length; f > u; u++) a = r.args[u], o[u + h] = a.dynamic ? this.$get(a.value) : a.value;
                    t = s.apply(this, o)
                }
            return t
        }, t.prototype._resolveComponent = function(e, i) {
            var n;
            if (n = "function" == typeof e ? e : gt(this.$options, "components", e, !0))
                if (n.options) i(n);
                else if (n.resolved) i(n.resolved);
            else if (n.requested) n.pendingCallbacks.push(i);
            else {
                n.requested = !0;
                var r = n.pendingCallbacks = [i];
                n.call(this, function(e) {
                    g(e) && (e = t.extend(e)), n.resolved = e;
                    for (var i = 0, s = r.length; s > i; i++) r[i](e)
                }, function(t) {})
            }
        }
    }

    function vi(t) {
        function i(t) {
            return JSON.parse(JSON.stringify(t))
        }
        t.prototype.$get = function(t, e) {
            var i = Ht(t);
            if (i) {
                if (e && !Mt(t)) {
                    var n = this;
                    return function() {
                        n.$arguments = d(arguments);
                        var t = i.get.call(n, n);
                        return n.$arguments = null, t
                    }
                }
                try {
                    return i.get.call(this, this)
                } catch (r) {}
            }
        }, t.prototype.$set = function(t, e) {
            var i = Ht(t, !0);
            i && i.set && i.set.call(this, this, e)
        }, t.prototype.$delete = function(t) {
            e(this._data, t)
        }, t.prototype.$watch = function(t, e, i) {
            var n, r = this;
            "string" == typeof t && (n = A(t), t = n.expression);
            var s = new zt(r, t, e, {
                deep: i && i.deep,
                sync: i && i.sync,
                filters: n && n.filters,
                user: !i || i.user !== !1
            });
            return i && i.immediate && e.call(r, s.value),
                function() {
                    s.teardown()
                }
        }, t.prototype.$eval = function(t, e) {
            if (Is.test(t)) {
                var i = A(t),
                    n = this.$get(i.expression, e);
                return i.filters ? this._applyFilters(n, null, i.filters) : n
            }
            return this.$get(t, e)
        }, t.prototype.$interpolate = function(t) {
            var e = N(t),
                i = this;
            return e ? 1 === e.length ? i.$eval(e[0].value) + "" : e.map(function(t) {
                return t.tag ? i.$eval(t.value) : t.value
            }).join("") : t
        }, t.prototype.$log = function(t) {
            var e = t ? jt(this._data, t) : this._data;
            if (e && (e = i(e)), !t) {
                var n;
                for (n in this.$options.computed) e[n] = i(this[n]);
                if (this._props)
                    for (n in this._props) e[n] = i(this[n])
            }
            console.log(e)
        }
    }

    function mi(t) {
        function e(t, e, n, r, s, o) {
            e = i(e);
            var a = !H(e),
                h = r === !1 || a ? s : o,
                l = !a && !t._isAttached && !H(t.$el);
            return t._isFragment ? (st(t._fragmentStart, t._fragmentEnd, function(i) {
                h(i, e, t)
            }), n && n()) : h(t.$el, e, t, n), l && t._callHook("attached"), t
        }

        function i(t) {
            return "string" == typeof t ? document.querySelector(t) : t
        }

        function n(t, e, i, n) {
            e.appendChild(t), n && n()
        }

        function r(t, e, i, n) {
            B(t, e), n && n()
        }

        function s(t, e, i) {
            z(t), i && i()
        }
        t.prototype.$nextTick = function(t) {
            Ui(t, this)
        }, t.prototype.$appendTo = function(t, i, r) {
            return e(this, t, i, r, n, S)
        }, t.prototype.$prependTo = function(t, e, n) {
            return t = i(t), t.hasChildNodes() ? this.$before(t.firstChild, e, n) : this.$appendTo(t, e, n), this
        }, t.prototype.$before = function(t, i, n) {
            return e(this, t, i, n, r, D)
        }, t.prototype.$after = function(t, e, n) {
            return t = i(t), t.nextSibling ? this.$before(t.nextSibling, e, n) : this.$appendTo(t.parentNode, e, n), this
        }, t.prototype.$remove = function(t, e) {
            if (!this.$el.parentNode) return t && t();
            var i = this._isAttached && H(this.$el);
            i || (e = !1);
            var n = this,
                r = function() {
                    i && n._callHook("detached"), t && t()
                };
            if (this._isFragment) ot(this._fragmentStart, this._fragmentEnd, this, this._fragment, r);
            else {
                var o = e === !1 ? s : P;
                o(this.$el, this, r)
            }
            return this
        }
    }

    function gi(t) {
        function e(t, e, n) {
            var r = t.$parent;
            if (r && n && !i.test(e))
                for (; r;) r._eventsCount[e] = (r._eventsCount[e] || 0) + n, r = r.$parent
        }
        t.prototype.$on = function(t, i) {
            return (this._events[t] || (this._events[t] = [])).push(i), e(this, t, 1), this
        }, t.prototype.$once = function(t, e) {
            function i() {
                n.$off(t, i), e.apply(this, arguments)
            }
            var n = this;
            return i.fn = e, this.$on(t, i), this
        }, t.prototype.$off = function(t, i) {
            var n;
            if (!arguments.length) {
                if (this.$parent)
                    for (t in this._events) n = this._events[t], n && e(this, t, -n.length);
                return this._events = {}, this
            }
            if (n = this._events[t], !n) return this;
            if (1 === arguments.length) return e(this, t, -n.length), this._events[t] = null, this;
            for (var r, s = n.length; s--;)
                if (r = n[s], r === i || r.fn === i) {
                    e(this, t, -1), n.splice(s, 1);
                    break
                }
            return this
        }, t.prototype.$emit = function(t) {
            var e = "string" == typeof t;
            t = e ? t : t.name;
            var i = this._events[t],
                n = e || !i;
            if (i) {
                i = i.length > 1 ? d(i) : i;
                var r = e && i.some(function(t) {
                    return t._fromParent
                });
                r && (n = !1);
                for (var s = d(arguments, 1), o = 0, a = i.length; a > o; o++) {
                    var h = i[o],
                        l = h.apply(this, s);
                    l !== !0 || r && !h._fromParent || (n = !0)
                }
            }
            return n
        }, t.prototype.$broadcast = function(t) {
            var e = "string" == typeof t;
            if (t = e ? t : t.name, this._eventsCount[t]) {
                var i = this.$children,
                    n = d(arguments);
                e && (n[0] = {
                    name: t,
                    source: this
                });
                for (var r = 0, s = i.length; s > r; r++) {
                    var o = i[r],
                        a = o.$emit.apply(o, n);
                    a && o.$broadcast.apply(o, n)
                }
                return this
            }
        }, t.prototype.$dispatch = function(t) {
            var e = this.$emit.apply(this, arguments);
            if (e) {
                var i = this.$parent,
                    n = d(arguments);
                for (n[0] = {
                        name: t,
                        source: this
                    }; i;) e = i.$emit.apply(i, n), i = e ? i.$parent : null;
                return this
            }
        };
        var i = /^hook:/
    }

    function _i(t) {
        function e() {
            this._isAttached = !0, this._isReady = !0, this._callHook("ready")
        }
        t.prototype.$mount = function(t) {
            return this._isCompiled ? void 0 : (t = L(t), t || (t = document.createElement("div")), this._compile(t), this._initDOMHooks(), H(this.$el) ? (this._callHook("attached"), e.call(this)) : this.$once("hook:attached", e), this)
        }, t.prototype.$destroy = function(t, e) {
            this._destroy(t, e)
        }, t.prototype.$compile = function(t, e, i, n) {
            return Se(t, this.$options, !0)(this, t, e, i, n)
        }
    }

    function yi(t) {
        this._init(t)
    }

    function bi(t, e, i) {
        return i = i ? parseInt(i, 10) : 0, e = o(e), "number" == typeof e ? t.slice(i, i + e) : t
    }

    function wi(t, e, i) {
        if (t = Us(t), null == e) return t;
        if ("function" == typeof e) return t.filter(e);
        e = ("" + e).toLowerCase();
        for (var n, r, s, o, a = "in" === i ? 3 : 2, h = Array.prototype.concat.apply([], d(arguments, a)), l = [], c = 0, u = t.length; u > c; c++)
            if (n = t[c], s = n && n.$value || n, o = h.length) {
                for (; o--;)
                    if (r = h[o], "$key" === r && $i(n.$key, e) || $i(jt(s, r), e)) {
                        l.push(n);
                        break
                    }
            } else $i(n, e) && l.push(n);
        return l
    }

    function Ci(t) {
        function e(t, e, i) {
            var r = n[i];
            return r && ("$key" !== r && (m(t) && "$value" in t && (t = t.$value), m(e) && "$value" in e && (e = e.$value)), t = m(t) ? jt(t, r) : t, e = m(e) ? jt(e, r) : e), t === e ? 0 : t > e ? s : -s
        }
        var i = null,
            n = void 0;
        t = Us(t);
        var r = d(arguments, 1),
            s = r[r.length - 1];
        "number" == typeof s ? (s = 0 > s ? -1 : 1, r = r.length > 1 ? r.slice(0, -1) : r) : s = 1;
        var o = r[0];
        return o ? ("function" == typeof o ? i = function(t, e) {
            return o(t, e) * s
        } : (n = Array.prototype.concat.apply([], r), i = function(t, r, s) {
            return s = s || 0, s >= n.length - 1 ? e(t, r, s) : e(t, r, s) || i(t, r, s + 1)
        }), t.slice().sort(i)) : t
    }

    function $i(t, e) {
        var i;
        if (g(t)) {
            var n = Object.keys(t);
            for (i = n.length; i--;)
                if ($i(t[n[i]], e)) return !0
        } else if (Fi(t)) {
            for (i = t.length; i--;)
                if ($i(t[i], e)) return !0
        } else if (null != t) return t.toString().toLowerCase().indexOf(e) > -1
    }

    function ki(i) {
        function n(t) {
            return new Function("return function " + f(t) + " (options) { this._init(options) }")()
        }
        i.options = {
            directives: fs,
            elementDirectives: zs,
            filters: qs,
            transitions: {},
            components: {},
            partials: {},
            replace: !0
        }, i.util = En, i.config = _n, i.set = t, i["delete"] = e, i.nextTick = Ui, i.compiler = Ms, i.FragmentFactory = re, i.internalDirectives = js, i.parsers = {
            path: Gn,
            text: vn,
            template: xr,
            directive: ln,
            expression: lr
        }, i.cid = 0;
        var r = 1;
        i.extend = function(t) {
            t = t || {};
            var e = this,
                i = 0 === e.cid;
            if (i && t._Ctor) return t._Ctor;
            var s = t.name || e.options.name,
                o = n(s || "VueComponent");
            return o.prototype = Object.create(e.prototype), o.prototype.constructor = o, o.cid = r++, o.options = mt(e.options, t), o["super"] = e, o.extend = e.extend, _n._assetTypes.forEach(function(t) {
                o[t] = e[t]
            }), s && (o.options.components[s] = o), i && (t._Ctor = o), o
        }, i.use = function(t) {
            if (!t.installed) {
                var e = d(arguments, 1);
                return e.unshift(this), "function" == typeof t.install ? t.install.apply(t, e) : t.apply(null, e), t.installed = !0, this
            }
        }, i.mixin = function(t) {
            i.options = mt(i.options, t)
        }, _n._assetTypes.forEach(function(t) {
            i[t] = function(e, n) {
                return n ? ("component" === t && g(n) && (n.name = e, n = i.extend(n)), this.options[t + "s"][e] = n, n) : this.options[t + "s"][e]
            }
        }), v(i.transition, bn)
    }
    var xi = Object.prototype.hasOwnProperty,
        Ai = /^\s?(true|false|-?[\d\.]+|'[^']*'|"[^"]*")\s?$/,
        Oi = /-(\w)/g,
        Ti = /([a-z\d])([A-Z])/g,
        Ni = /(?:^|[-_\/])(\w)/g,
        ji = Object.prototype.toString,
        Ei = "[object Object]",
        Fi = Array.isArray,
        Si = "__proto__" in {},
        Di = "undefined" != typeof window && "[object Object]" !== Object.prototype.toString.call(window),
        Pi = Di && window.__VUE_DEVTOOLS_GLOBAL_HOOK__,
        Ri = Di && window.navigator.userAgent.toLowerCase(),
        Li = Ri && Ri.indexOf("msie 9.0") > 0,
        Hi = Ri && Ri.indexOf("android") > 0,
        Mi = void 0,
        Wi = void 0,
        Ii = void 0,
        Bi = void 0;
    if (Di && !Li) {
        var Vi = void 0 === window.ontransitionend && void 0 !== window.onwebkittransitionend,
            zi = void 0 === window.onanimationend && void 0 !== window.onwebkitanimationend;
        Mi = Vi ? "WebkitTransition" : "transition", Wi = Vi ? "webkitTransitionEnd" : "transitionend", Ii = zi ? "WebkitAnimation" : "animation", Bi = zi ? "webkitAnimationEnd" : "animationend"
    }
    var Ui = function() {
            function t() {
                n = !1;
                var t = i.slice(0);
                i = [];
                for (var e = 0; e < t.length; e++) t[e]()
            }
            var e, i = [],
                n = !1;
            if ("undefined" != typeof MutationObserver) {
                var r = 1,
                    s = new MutationObserver(t),
                    o = document.createTextNode(r);
                s.observe(o, {
                    characterData: !0
                }), e = function() {
                    r = (r + 1) % 2, o.data = r
                }
            } else {
                var a = Di ? window : "undefined" != typeof global ? global : {};
                e = a.setImmediate || setTimeout
            }
            return function(r, s) {
                var o = s ? function() {
                    r.call(s)
                } : r;
                i.push(o), n || (n = !0, e(t, 0))
            }
        }(),
        Ji = $.prototype;
    Ji.put = function(t, e) {
        var i;
        this.size === this.limit && (i = this.shift());
        var n = this.get(t, !0);
        return n || (n = {
            key: t
        }, this._keymap[t] = n, this.tail ? (this.tail.newer = n, n.older = this.tail) : this.head = n, this.tail = n, this.size++), n.value = e, i
    }, Ji.shift = function() {
        var t = this.head;
        return t && (this.head = this.head.newer, this.head.older = void 0, t.newer = t.older = void 0, this._keymap[t.key] = void 0, this.size--), t
    }, Ji.get = function(t, e) {
        var i = this._keymap[t];
        if (void 0 !== i) return i === this.tail ? e ? i : i.value : (i.newer && (i === this.head && (this.head = i.newer), i.newer.older = i.older), i.older && (i.older.newer = i.newer), i.newer = void 0, i.older = this.tail, this.tail && (this.tail.newer = i), this.tail = i, e ? i : i.value)
    };
    var qi, Qi, Gi, Ki, Zi, Xi, Yi, tn, en, nn, rn, sn, on = new $(1e3),
        an = /[^\s'"]+|'[^']*'|"[^"]*"/g,
        hn = /^in$|^-?\d+/,
        ln = Object.freeze({
            parseDirective: A
        }),
        cn = /[-.*+?^${}()|[\]\/\\]/g,
        un = void 0,
        fn = void 0,
        pn = void 0,
        dn = /[^|]\|[^|]/,
        vn = Object.freeze({
            compileRegex: T,
            parseText: N,
            tokensToExp: j
        }),
        mn = ["{{", "}}"],
        gn = ["{{{", "}}}"],
        _n = Object.defineProperties({
            debug: !1,
            silent: !1,
            async: !0,
            warnExpressionErrors: !0,
            devtools: !1,
            _delimitersChanged: !0,
            _assetTypes: ["component", "directive", "elementDirective", "filter", "transition", "partial"],
            _propBindingModes: {
                ONE_WAY: 0,
                TWO_WAY: 1,
                ONE_TIME: 2
            },
            _maxUpdateCount: 100
        }, {
            delimiters: {
                get: function() {
                    return mn
                },
                set: function(t) {
                    mn = t, T()
                },
                configurable: !0,
                enumerable: !0
            },
            unsafeDelimiters: {
                get: function() {
                    return gn
                },
                set: function(t) {
                    gn = t, T()
                },
                configurable: !0,
                enumerable: !0
            }
        }),
        yn = void 0,
        bn = Object.freeze({
            appendWithTransition: S,
            beforeWithTransition: D,
            removeWithTransition: P,
            applyTransition: R
        }),
        wn = /^v-ref:/,
        Cn = /^(div|p|span|img|a|b|i|br|ul|ol|li|h1|h2|h3|h4|h5|h6|code|pre|table|th|td|tr|form|label|input|select|option|nav|article|section|header|footer)$/i,
        $n = /^(slot|partial|component)$/i,
        kn = _n.optionMergeStrategies = Object.create(null);
    kn.data = function(t, e, i) {
        return i ? t || e ? function() {
            var n = "function" == typeof e ? e.call(i) : e,
                r = "function" == typeof t ? t.call(i) : void 0;
            return n ? ut(n, r) : r
        } : void 0 : e ? "function" != typeof e ? t : t ? function() {
            return ut(e.call(this), t.call(this))
        } : e : t
    }, kn.el = function(t, e, i) {
        if (i || !e || "function" == typeof e) {
            var n = e || t;
            return i && "function" == typeof n ? n.call(i) : n
        }
    }, kn.init = kn.created = kn.ready = kn.attached = kn.detached = kn.beforeCompile = kn.compiled = kn.beforeDestroy = kn.destroyed = kn.activate = function(t, e) {
        return e ? t ? t.concat(e) : Fi(e) ? e : [e] : t
    }, _n._assetTypes.forEach(function(t) {
        kn[t + "s"] = ft
    }), kn.watch = kn.events = function(t, e) {
        if (!e) return t;
        if (!t) return e;
        var i = {};
        v(i, t);
        for (var n in e) {
            var r = i[n],
                s = e[n];
            r && !Fi(r) && (r = [r]), i[n] = r ? r.concat(s) : [s]
        }
        return i
    }, kn.props = kn.methods = kn.computed = function(t, e) {
        if (!e) return t;
        if (!t) return e;
        var i = Object.create(null);
        return v(i, t), v(i, e), i
    };
    var xn = function(t, e) {
            return void 0 === e ? t : e
        },
        An = 0;
    _t.target = null, _t.prototype.addSub = function(t) {
        this.subs.push(t)
    }, _t.prototype.removeSub = function(t) {
        this.subs.$remove(t)
    }, _t.prototype.depend = function() {
        _t.target.addDep(this)
    }, _t.prototype.notify = function() {
        for (var t = d(this.subs), e = 0, i = t.length; i > e; e++) t[e].update()
    };
    var On = Array.prototype,
        Tn = Object.create(On);
    ["push", "pop", "shift", "unshift", "splice", "sort", "reverse"].forEach(function(t) {
        var e = On[t];
        _(Tn, t, function() {
            for (var i = arguments.length, n = new Array(i); i--;) n[i] = arguments[i];
            var r, s = e.apply(this, n),
                o = this.__ob__;
            switch (t) {
                case "push":
                    r = n;
                    break;
                case "unshift":
                    r = n;
                    break;
                case "splice":
                    r = n.slice(2)
            }
            return r && o.observeArray(r), o.dep.notify(), s
        })
    }), _(On, "$set", function(t, e) {
        return t >= this.length && (this.length = Number(t) + 1), this.splice(t, 1, e)[0]
    }), _(On, "$remove", function(t) {
        if (this.length) {
            var e = b(this, t);
            return e > -1 ? this.splice(e, 1) : void 0
        }
    });
    var Nn = Object.getOwnPropertyNames(Tn),
        jn = !0;
    bt.prototype.walk = function(t) {
        for (var e = Object.keys(t), i = 0, n = e.length; n > i; i++) this.convert(e[i], t[e[i]])
    }, bt.prototype.observeArray = function(t) {
        for (var e = 0, i = t.length; i > e; e++) $t(t[e])
    }, bt.prototype.convert = function(t, e) {
        kt(this.value, t, e)
    }, bt.prototype.addVm = function(t) {
        (this.vms || (this.vms = [])).push(t)
    }, bt.prototype.removeVm = function(t) {
        this.vms.$remove(t)
    };
    var En = Object.freeze({
            defineReactive: kt,
            set: t,
            del: e,
            hasOwn: i,
            isLiteral: n,
            isReserved: r,
            _toString: s,
            toNumber: o,
            toBoolean: a,
            stripQuotes: h,
            camelize: l,
            hyphenate: u,
            classify: f,
            bind: p,
            toArray: d,
            extend: v,
            isObject: m,
            isPlainObject: g,
            def: _,
            debounce: y,
            indexOf: b,
            cancellable: w,
            looseEqual: C,
            isArray: Fi,
            hasProto: Si,
            inBrowser: Di,
            devtools: Pi,
            isIE9: Li,
            isAndroid: Hi,
            get transitionProp() {
                return Mi
            },
            get transitionEndEvent() {
                return Wi
            },
            get animationProp() {
                return Ii
            },
            get animationEndEvent() {
                return Bi
            },
            nextTick: Ui,
            query: L,
            inDoc: H,
            getAttr: M,
            getBindAttr: W,
            hasBindAttr: I,
            before: B,
            after: V,
            remove: z,
            prepend: U,
            replace: J,
            on: q,
            off: Q,
            setClass: K,
            addClass: Z,
            removeClass: X,
            extractContent: Y,
            trimNode: tt,
            isTemplate: it,
            createAnchor: nt,
            findRef: rt,
            mapNodeRange: st,
            removeNodeRange: ot,
            isFragment: at,
            getOuterHTML: ht,
            mergeOptions: mt,
            resolveAsset: gt,
            checkComponentAttr: lt,
            commonTagRE: Cn,
            reservedTagRE: $n,
            warn: yn
        }),
        Fn = 0,
        Sn = new $(1e3),
        Dn = 0,
        Pn = 1,
        Rn = 2,
        Ln = 3,
        Hn = 0,
        Mn = 1,
        Wn = 2,
        In = 3,
        Bn = 4,
        Vn = 5,
        zn = 6,
        Un = 7,
        Jn = 8,
        qn = [];
    qn[Hn] = {
        ws: [Hn],
        ident: [In, Dn],
        "[": [Bn],
        eof: [Un]
    }, qn[Mn] = {
        ws: [Mn],
        ".": [Wn],
        "[": [Bn],
        eof: [Un]
    }, qn[Wn] = {
        ws: [Wn],
        ident: [In, Dn]
    }, qn[In] = {
        ident: [In, Dn],
        0: [In, Dn],
        number: [In, Dn],
        ws: [Mn, Pn],
        ".": [Wn, Pn],
        "[": [Bn, Pn],
        eof: [Un, Pn]
    }, qn[Bn] = {
        "'": [Vn, Dn],
        '"': [zn, Dn],
        "[": [Bn, Rn],
        "]": [Mn, Ln],
        eof: Jn,
        "else": [Bn, Dn]
    }, qn[Vn] = {
        "'": [Bn, Dn],
        eof: Jn,
        "else": [Vn, Dn]
    }, qn[zn] = {
        '"': [Bn, Dn],
        eof: Jn,
        "else": [zn, Dn]
    };
    var Qn, Gn = Object.freeze({
            parsePath: Nt,
            getPath: jt,
            setPath: Et
        }),
        Kn = new $(1e3),
        Zn = "Math,Date,this,true,false,null,undefined,Infinity,NaN,isNaN,isFinite,decodeURI,decodeURIComponent,encodeURI,encodeURIComponent,parseInt,parseFloat",
        Xn = new RegExp("^(" + Zn.replace(/,/g, "\\b|") + "\\b)"),
        Yn = "break,case,class,catch,const,continue,debugger,default,delete,do,else,export,extends,finally,for,function,if,import,in,instanceof,let,return,super,switch,throw,try,var,while,with,yield,enum,await,implements,package,protected,static,interface,private,public",
        tr = new RegExp("^(" + Yn.replace(/,/g, "\\b|") + "\\b)"),
        er = /\s/g,
        ir = /\n/g,
        nr = /[\{,]\s*[\w\$_]+\s*:|('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|`(?:[^`\\]|\\.)*\$\{|\}(?:[^`\\]|\\.)*`|`(?:[^`\\]|\\.)*`)|new |typeof |void /g,
        rr = /"(\d+)"/g,
        sr = /^[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*|\['.*?'\]|\[".*?"\]|\[\d+\]|\[[A-Za-z_$][\w$]*\])*$/,
        or = /[^\w$\.](?:[A-Za-z_$][\w$]*)/g,
        ar = /^(?:true|false)$/,
        hr = [],
        lr = Object.freeze({
            parseExpression: Ht,
            isSimplePath: Mt
        }),
        cr = [],
        ur = [],
        fr = {},
        pr = {},
        dr = !1,
        vr = !1,
        mr = 0;
    zt.prototype.get = function() {
        this.beforeGet();
        var t, e = this.scope || this.vm;
        try {
            t = this.getter.call(e, e)
        } catch (i) {}
        return this.deep && Ut(t), this.preProcess && (t = this.preProcess(t)), this.filters && (t = e._applyFilters(t, null, this.filters, !1)), this.postProcess && (t = this.postProcess(t)), this.afterGet(), t
    }, zt.prototype.set = function(t) {
        var e = this.scope || this.vm;
        this.filters && (t = e._applyFilters(t, this.value, this.filters, !0));
        try {
            this.setter.call(e, e, t)
        } catch (i) {}
        var n = e.$forContext;
        if (n && n.alias === this.expression) {
            if (n.filters) return;
            n._withLock(function() {
                e.$key ? n.rawValue[e.$key] = t : n.rawValue.$set(e.$index, t)
            })
        }
    }, zt.prototype.beforeGet = function() {
        _t.target = this, this.newDepIds = Object.create(null), this.newDeps.length = 0
    }, zt.prototype.addDep = function(t) {
        var e = t.id;
        this.newDepIds[e] || (this.newDepIds[e] = !0, this.newDeps.push(t), this.depIds[e] || t.addSub(this))
    }, zt.prototype.afterGet = function() {
        _t.target = null;
        for (var t = this.deps.length; t--;) {
            var e = this.deps[t];
            this.newDepIds[e.id] || e.removeSub(this)
        }
        this.depIds = this.newDepIds;
        var i = this.deps;
        this.deps = this.newDeps, this.newDeps = i
    }, zt.prototype.update = function(t) {
        this.lazy ? this.dirty = !0 : this.sync || !_n.async ? this.run() : (this.shallow = this.queued ? t ? this.shallow : !1 : !!t, this.queued = !0, Vt(this))
    }, zt.prototype.run = function() {
        if (this.active) {
            var t = this.get();
            if (t !== this.value || (m(t) || this.deep) && !this.shallow) {
                var e = this.value;
                this.value = t;
                this.prevError;
                this.cb.call(this.vm, t, e)
            }
            this.queued = this.shallow = !1
        }
    }, zt.prototype.evaluate = function() {
        var t = _t.target;
        this.value = this.get(), this.dirty = !1, _t.target = t
    }, zt.prototype.depend = function() {
        for (var t = this.deps.length; t--;) this.deps[t].depend()
    }, zt.prototype.teardown = function() {
        if (this.active) {
            this.vm._isBeingDestroyed || this.vm._vForRemoving || this.vm._watchers.$remove(this);
            for (var t = this.deps.length; t--;) this.deps[t].removeSub(this);
            this.active = !1, this.vm = this.cb = this.value = null
        }
    };
    var gr = {
            bind: function() {
                this.attr = 3 === this.el.nodeType ? "data" : "textContent"
            },
            update: function(t) {
                this.el[this.attr] = s(t)
            }
        },
        _r = new $(1e3),
        yr = new $(1e3),
        br = {
            efault: [0, "", ""],
            legend: [1, "<fieldset>", "</fieldset>"],
            tr: [2, "<table><tbody>", "</tbody></table>"],
            col: [2, "<table><tbody></tbody><colgroup>", "</colgroup></table>"]
        };
    br.td = br.th = [3, "<table><tbody><tr>", "</tr></tbody></table>"], br.option = br.optgroup = [1, '<select multiple="multiple">', "</select>"], br.thead = br.tbody = br.colgroup = br.caption = br.tfoot = [1, "<table>", "</table>"], br.g = br.defs = br.symbol = br.use = br.image = br.text = br.circle = br.ellipse = br.line = br.path = br.polygon = br.polyline = br.rect = [1, '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ev="http://www.w3.org/2001/xml-events"version="1.1">', "</svg>"];
    var wr = /<([\w:-]+)/,
        Cr = /&#?\w+?;/,
        $r = function() {
            if (Di) {
                var t = document.createElement("div");
                return t.innerHTML = "<template>1</template>", !t.cloneNode(!0).firstChild.innerHTML
            }
            return !1
        }(),
        kr = function() {
            if (Di) {
                var t = document.createElement("textarea");
                return t.placeholder = "t", "t" === t.cloneNode(!0).value
            }
            return !1
        }(),
        xr = Object.freeze({
            cloneNode: Gt,
            parseTemplate: Kt
        }),
        Ar = {
            bind: function() {
                8 === this.el.nodeType && (this.nodes = [], this.anchor = nt("v-html"), J(this.el, this.anchor))
            },
            update: function(t) {
                t = s(t), this.nodes ? this.swap(t) : this.el.innerHTML = t
            },
            swap: function(t) {
                for (var e = this.nodes.length; e--;) z(this.nodes[e]);
                var i = Kt(t, !0, !0);
                this.nodes = d(i.childNodes), B(i, this.anchor)
            }
        };
    Zt.prototype.callHook = function(t) {
        var e, i;
        for (e = 0, i = this.childFrags.length; i > e; e++) this.childFrags[e].callHook(t);
        for (e = 0, i = this.children.length; i > e; e++) t(this.children[e])
    }, Zt.prototype.beforeRemove = function() {
        var t, e;
        for (t = 0, e = this.childFrags.length; e > t; t++) this.childFrags[t].beforeRemove(!1);
        for (t = 0, e = this.children.length; e > t; t++) this.children[t].$destroy(!1, !0);
        var i = this.unlink.dirs;
        for (t = 0, e = i.length; e > t; t++) i[t]._watcher && i[t]._watcher.teardown()
    }, Zt.prototype.destroy = function() {
        this.parentFrag && this.parentFrag.childFrags.$remove(this), this.node.__v_frag = null, this.unlink()
    };
    var Or = new $(5e3);
    re.prototype.create = function(t, e, i) {
        var n = Gt(this.template);
        return new Zt(this.linker, this.vm, n, t, e, i)
    };
    var Tr = 700,
        Nr = 800,
        jr = 850,
        Er = 1100,
        Fr = 1500,
        Sr = 1500,
        Dr = 1750,
        Pr = 2100,
        Rr = 2200,
        Lr = 2300,
        Hr = 0,
        Mr = {
            priority: Rr,
            terminal: !0,
            params: ["track-by", "stagger", "enter-stagger", "leave-stagger"],
            bind: function() {
                var t = this.expression.match(/(.*) (?:in|of) (.*)/);
                if (t) {
                    var e = t[1].match(/\((.*),(.*)\)/);
                    e ? (this.iterator = e[1].trim(), this.alias = e[2].trim()) : this.alias = t[1].trim(), this.expression = t[2]
                }
                if (this.alias) {
                    this.id = "__v-for__" + ++Hr;
                    var i = this.el.tagName;
                    this.isOption = ("OPTION" === i || "OPTGROUP" === i) && "SELECT" === this.el.parentNode.tagName, this.start = nt("v-for-start"), this.end = nt("v-for-end"), J(this.el, this.end), B(this.start, this.end), this.cache = Object.create(null), this.factory = new re(this.vm, this.el)
                }
            },
            update: function(t) {
                this.diff(t), this.updateRef(), this.updateModel()
            },
            diff: function(t) {
                var e, n, r, s, o, a, h = t[0],
                    l = this.fromObject = m(h) && i(h, "$key") && i(h, "$value"),
                    c = this.params.trackBy,
                    u = this.frags,
                    f = this.frags = new Array(t.length),
                    p = this.alias,
                    d = this.iterator,
                    v = this.start,
                    g = this.end,
                    _ = H(v),
                    y = !u;
                for (e = 0, n = t.length; n > e; e++) h = t[e], s = l ? h.$key : null, o = l ? h.$value : h, a = !m(o), r = !y && this.getCachedFrag(o, e, s), r ? (r.reused = !0, r.scope.$index = e, s && (r.scope.$key = s), d && (r.scope[d] = null !== s ? s : e), (c || l || a) && yt(function() {
                    r.scope[p] = o
                })) : (r = this.create(o, p, e, s), r.fresh = !y), f[e] = r, y && r.before(g);
                if (!y) {
                    var b = 0,
                        w = u.length - f.length;
                    for (this.vm._vForRemoving = !0, e = 0, n = u.length; n > e; e++) r = u[e], r.reused || (this.deleteCachedFrag(r), this.remove(r, b++, w, _));
                    this.vm._vForRemoving = !1, b && (this.vm._watchers = this.vm._watchers.filter(function(t) {
                        return t.active
                    }));
                    var C, $, k, x = 0;
                    for (e = 0, n = f.length; n > e; e++) r = f[e], C = f[e - 1], $ = C ? C.staggerCb ? C.staggerAnchor : C.end || C.node : v, r.reused && !r.staggerCb ? (k = se(r, v, this.id), k === C || k && se(k, v, this.id) === C || this.move(r, $)) : this.insert(r, x++, $, _), r.reused = r.fresh = !1
                }
            },
            create: function(t, e, i, n) {
                var r = this._host,
                    s = this._scope || this.vm,
                    o = Object.create(s);
                o.$refs = Object.create(s.$refs), o.$els = Object.create(s.$els), o.$parent = s, o.$forContext = this, yt(function() {
                    kt(o, e, t)
                }), kt(o, "$index", i), n ? kt(o, "$key", n) : o.$key && _(o, "$key", null), this.iterator && kt(o, this.iterator, null !== n ? n : i);
                var a = this.factory.create(r, o, this._frag);
                return a.forId = this.id, this.cacheFrag(t, a, i, n), a
            },
            updateRef: function() {
                var t = this.descriptor.ref;
                if (t) {
                    var e, i = (this._scope || this.vm).$refs;
                    this.fromObject ? (e = {}, this.frags.forEach(function(t) {
                        e[t.scope.$key] = oe(t)
                    })) : e = this.frags.map(oe), i[t] = e
                }
            },
            updateModel: function() {
                if (this.isOption) {
                    var t = this.start.parentNode,
                        e = t && t.__v_model;
                    e && e.forceUpdate()
                }
            },
            insert: function(t, e, i, n) {
                t.staggerCb && (t.staggerCb.cancel(), t.staggerCb = null);
                var r = this.getStagger(t, e, null, "enter");
                if (n && r) {
                    var s = t.staggerAnchor;
                    s || (s = t.staggerAnchor = nt("stagger-anchor"), s.__v_frag = t), V(s, i);
                    var o = t.staggerCb = w(function() {
                        t.staggerCb = null, t.before(s), z(s)
                    });
                    setTimeout(o, r)
                } else t.before(i.nextSibling)
            },
            remove: function(t, e, i, n) {
                if (t.staggerCb) return t.staggerCb.cancel(), void(t.staggerCb = null);
                var r = this.getStagger(t, e, i, "leave");
                if (n && r) {
                    var s = t.staggerCb = w(function() {
                        t.staggerCb = null, t.remove()
                    });
                    setTimeout(s, r)
                } else t.remove()
            },
            move: function(t, e) {
                e.nextSibling || this.end.parentNode.appendChild(this.end), t.before(e.nextSibling, !1)
            },
            cacheFrag: function(t, e, n, r) {
                var s, o = this.params.trackBy,
                    a = this.cache,
                    h = !m(t);
                r || o || h ? (s = o ? "$index" === o ? n : jt(t, o) : r || t, a[s] || (a[s] = e)) : (s = this.id, i(t, s) ? null === t[s] && (t[s] = e) : _(t, s, e)), e.raw = t
            },
            getCachedFrag: function(t, e, i) {
                var n, r = this.params.trackBy,
                    s = !m(t);
                if (i || r || s) {
                    var o = r ? "$index" === r ? e : jt(t, r) : i || t;
                    n = this.cache[o]
                } else n = t[this.id];
                return n && (n.reused || n.fresh), n
            },
            deleteCachedFrag: function(t) {
                var e = t.raw,
                    n = this.params.trackBy,
                    r = t.scope,
                    s = r.$index,
                    o = i(r, "$key") && r.$key,
                    a = !m(e);
                if (n || o || a) {
                    var h = n ? "$index" === n ? s : jt(e, n) : o || e;
                    this.cache[h] = null
                } else e[this.id] = null, t.raw = null
            },
            getStagger: function(t, e, i, n) {
                n += "Stagger";
                var r = t.node.__v_trans,
                    s = r && r.hooks,
                    o = s && (s[n] || s.stagger);
                return o ? o.call(t, e, i) : e * parseInt(this.params[n] || this.params.stagger, 10)
            },
            _preProcess: function(t) {
                return this.rawValue = t, t
            },
            _postProcess: function(t) {
                if (Fi(t)) return t;
                if (g(t)) {
                    for (var e, i = Object.keys(t), n = i.length, r = new Array(n); n--;) e = i[n], r[n] = {
                        $key: e,
                        $value: t[e]
                    };
                    return r
                }
                return "number" != typeof t || isNaN(t) || (t = ae(t)), t || []
            },
            unbind: function() {
                if (this.descriptor.ref && ((this._scope || this.vm).$refs[this.descriptor.ref] = null), this.frags)
                    for (var t, e = this.frags.length; e--;) t = this.frags[e], this.deleteCachedFrag(t), t.destroy()
            }
        },
        Wr = {
            priority: Pr,
            terminal: !0,
            bind: function() {
                var t = this.el;
                if (t.__vue__) this.invalid = !0;
                else {
                    var e = t.nextElementSibling;
                    e && null !== M(e, "v-else") && (z(e), this.elseEl = e), this.anchor = nt("v-if"), J(t, this.anchor)
                }
            },
            update: function(t) {
                this.invalid || (t ? this.frag || this.insert() : this.remove())
            },
            insert: function() {
                this.elseFrag && (this.elseFrag.remove(), this.elseFrag = null), this.factory || (this.factory = new re(this.vm, this.el)), this.frag = this.factory.create(this._host, this._scope, this._frag), this.frag.before(this.anchor)
            },
            remove: function() {
                this.frag && (this.frag.remove(), this.frag = null), this.elseEl && !this.elseFrag && (this.elseFactory || (this.elseFactory = new re(this.elseEl._context || this.vm, this.elseEl)), this.elseFrag = this.elseFactory.create(this._host, this._scope, this._frag), this.elseFrag.before(this.anchor))
            },
            unbind: function() {
                this.frag && this.frag.destroy(), this.elseFrag && this.elseFrag.destroy()
            }
        },
        Ir = {
            bind: function() {
                var t = this.el.nextElementSibling;
                t && null !== M(t, "v-else") && (this.elseEl = t)
            },
            update: function(t) {
                this.apply(this.el, t), this.elseEl && this.apply(this.elseEl, !t)
            },
            apply: function(t, e) {
                function i() {
                    t.style.display = e ? "" : "none"
                }
                H(t) ? R(t, e ? 1 : -1, i, this.vm) : i()
            }
        },
        Br = {
            bind: function() {
                var t = this,
                    e = this.el,
                    i = "range" === e.type,
                    n = this.params.lazy,
                    r = this.params.number,
                    s = this.params.debounce,
                    a = !1;
                if (Hi || i || (this.on("compositionstart", function() {
                        a = !0
                    }), this.on("compositionend", function() {
                        a = !1, n || t.listener()
                    })), this.focused = !1, i || n || (this.on("focus", function() {
                        t.focused = !0
                    }), this.on("blur", function() {
                        t.focused = !1, t._frag && !t._frag.inserted || t.rawListener()
                    })), this.listener = this.rawListener = function() {
                        if (!a && t._bound) {
                            var n = r || i ? o(e.value) : e.value;
                            t.set(n), Ui(function() {
                                t._bound && !t.focused && t.update(t._watcher.value)
                            })
                        }
                    }, s && (this.listener = y(this.listener, s)), this.hasjQuery = "function" == typeof jQuery, this.hasjQuery) {
                    var h = jQuery.fn.on ? "on" : "bind";
                    jQuery(e)[h]("change", this.rawListener), n || jQuery(e)[h]("input", this.listener)
                } else this.on("change", this.rawListener), n || this.on("input", this.listener);
                !n && Li && (this.on("cut", function() {
                    Ui(t.listener)
                }), this.on("keyup", function(e) {
                    46 !== e.keyCode && 8 !== e.keyCode || t.listener()
                })), (e.hasAttribute("value") || "TEXTAREA" === e.tagName && e.value.trim()) && (this.afterBind = this.listener)
            },
            update: function(t) {
                this.el.value = s(t)
            },
            unbind: function() {
                var t = this.el;
                if (this.hasjQuery) {
                    var e = jQuery.fn.off ? "off" : "unbind";
                    jQuery(t)[e]("change", this.listener), jQuery(t)[e]("input", this.listener)
                }
            }
        },
        Vr = {
            bind: function() {
                var t = this,
                    e = this.el;
                this.getValue = function() {
                    if (e.hasOwnProperty("_value")) return e._value;
                    var i = e.value;
                    return t.params.number && (i = o(i)), i
                }, this.listener = function() {
                    t.set(t.getValue())
                }, this.on("change", this.listener), e.hasAttribute("checked") && (this.afterBind = this.listener)
            },
            update: function(t) {
                this.el.checked = C(t, this.getValue())
            }
        },
        zr = {
            bind: function() {
                var t = this,
                    e = this.el;
                this.forceUpdate = function() {
                    t._watcher && t.update(t._watcher.get())
                };
                var i = this.multiple = e.hasAttribute("multiple");
                this.listener = function() {
                    var n = he(e, i);
                    n = t.params.number ? Fi(n) ? n.map(o) : o(n) : n, t.set(n)
                }, this.on("change", this.listener);
                var n = he(e, i, !0);
                (i && n.length || !i && null !== n) && (this.afterBind = this.listener), this.vm.$on("hook:attached", this.forceUpdate)
            },
            update: function(t) {
                var e = this.el;
                e.selectedIndex = -1;
                for (var i, n, r = this.multiple && Fi(t), s = e.options, o = s.length; o--;) i = s[o], n = i.hasOwnProperty("_value") ? i._value : i.value, i.selected = r ? le(t, n) > -1 : C(t, n)
            },
            unbind: function() {
                this.vm.$off("hook:attached", this.forceUpdate)
            }
        },
        Ur = {
            bind: function() {
                function t() {
                    var t = i.checked;
                    return t && i.hasOwnProperty("_trueValue") ? i._trueValue : !t && i.hasOwnProperty("_falseValue") ? i._falseValue : t
                }
                var e = this,
                    i = this.el;
                this.getValue = function() {
                    return i.hasOwnProperty("_value") ? i._value : e.params.number ? o(i.value) : i.value
                }, this.listener = function() {
                    var n = e._watcher.value;
                    if (Fi(n)) {
                        var r = e.getValue();
                        i.checked ? b(n, r) < 0 && n.push(r) : n.$remove(r)
                    } else e.set(t())
                }, this.on("change", this.listener), i.hasAttribute("checked") && (this.afterBind = this.listener)
            },
            update: function(t) {
                var e = this.el;
                Fi(t) ? e.checked = b(t, this.getValue()) > -1 : e.hasOwnProperty("_trueValue") ? e.checked = C(t, e._trueValue) : e.checked = !!t
            }
        },
        Jr = {
            text: Br,
            radio: Vr,
            select: zr,
            checkbox: Ur
        },
        qr = {
            priority: Nr,
            twoWay: !0,
            handlers: Jr,
            params: ["lazy", "number", "debounce"],
            bind: function() {
                this.checkFilters(), this.hasRead && !this.hasWrite;
                var t, e = this.el,
                    i = e.tagName;
                if ("INPUT" === i) t = Jr[e.type] || Jr.text;
                else if ("SELECT" === i) t = Jr.select;
                else {
                    if ("TEXTAREA" !== i) return;
                    t = Jr.text
                }
                e.__v_model = this, t.bind.call(this), this.update = t.update, this._unbind = t.unbind
            },
            checkFilters: function() {
                var t = this.filters;
                if (t)
                    for (var e = t.length; e--;) {
                        var i = gt(this.vm.$options, "filters", t[e].name);
                        ("function" == typeof i || i.read) && (this.hasRead = !0), i.write && (this.hasWrite = !0)
                    }
            },
            unbind: function() {
                this.el.__v_model = null, this._unbind && this._unbind()
            }
        },
        Qr = {
            esc: 27,
            tab: 9,
            enter: 13,
            space: 32,
            "delete": [8, 46],
            up: 38,
            left: 37,
            right: 39,
            down: 40
        },
        Gr = {
            priority: Tr,
            acceptStatement: !0,
            keyCodes: Qr,
            bind: function() {
                if ("IFRAME" === this.el.tagName && "load" !== this.arg) {
                    var t = this;
                    this.iframeBind = function() {
                        q(t.el.contentWindow, t.arg, t.handler, t.modifiers.capture)
                    }, this.on("load", this.iframeBind)
                }
            },
            update: function(t) {
                if (this.descriptor.raw || (t = function() {}), "function" == typeof t) {
                    this.modifiers.stop && (t = ue(t)), this.modifiers.prevent && (t = fe(t)), this.modifiers.self && (t = pe(t));
                    var e = Object.keys(this.modifiers).filter(function(t) {
                        return "stop" !== t && "prevent" !== t && "self" !== t
                    });
                    e.length && (t = ce(t, e)), this.reset(), this.handler = t, this.iframeBind ? this.iframeBind() : q(this.el, this.arg, this.handler, this.modifiers.capture)
                }
            },
            reset: function() {
                var t = this.iframeBind ? this.el.contentWindow : this.el;
                this.handler && Q(t, this.arg, this.handler)
            },
            unbind: function() {
                this.reset()
            }
        },
        Kr = ["-webkit-", "-moz-", "-ms-"],
        Zr = ["Webkit", "Moz", "ms"],
        Xr = /!important;?$/,
        Yr = Object.create(null),
        ts = null,
        es = {
            deep: !0,
            update: function(t) {
                "string" == typeof t ? this.el.style.cssText = t : Fi(t) ? this.handleObject(t.reduce(v, {})) : this.handleObject(t || {})
            },
            handleObject: function(t) {
                var e, i, n = this.cache || (this.cache = {});
                for (e in n) e in t || (this.handleSingle(e, null), delete n[e]);
                for (e in t) i = t[e], i !== n[e] && (n[e] = i, this.handleSingle(e, i))
            },
            handleSingle: function(t, e) {
                if (t = de(t))
                    if (null != e && (e += ""), e) {
                        var i = Xr.test(e) ? "important" : "";
                        i ? (e = e.replace(Xr, "").trim(), this.el.style.setProperty(t.kebab, e, i)) : this.el.style[t.camel] = e
                    } else this.el.style[t.camel] = ""
            }
        },
        is = "http://www.w3.org/1999/xlink",
        ns = /^xlink:/,
        rs = /^v-|^:|^@|^(?:is|transition|transition-mode|debounce|track-by|stagger|enter-stagger|leave-stagger)$/,
        ss = /^(?:value|checked|selected|muted)$/,
        os = /^(?:draggable|contenteditable|spellcheck)$/,
        as = {
            value: "_value",
            "true-value": "_trueValue",
            "false-value": "_falseValue"
        },
        hs = {
            priority: jr,
            bind: function() {
                var t = this.arg,
                    e = this.el.tagName;
                t || (this.deep = !0);
                var i = this.descriptor,
                    n = i.interp;
                n && (i.hasOneTime && (this.expression = j(n, this._scope || this.vm)), (rs.test(t) || "name" === t && ("PARTIAL" === e || "SLOT" === e)) && (this.el.removeAttribute(t), this.invalid = !0))
            },
            update: function(t) {
                if (!this.invalid) {
                    var e = this.arg;
                    this.arg ? this.handleSingle(e, t) : this.handleObject(t || {})
                }
            },
            handleObject: es.handleObject,
            handleSingle: function(t, e) {
                var i = this.el,
                    n = this.descriptor.interp;
                this.modifiers.camel && (t = l(t)), !n && ss.test(t) && t in i && (i[t] = "value" === t && null == e ? "" : e);
                var r = as[t];
                if (!n && r) {
                    i[r] = e;
                    var s = i.__v_model;
                    s && s.listener()
                }
                return "value" === t && "TEXTAREA" === i.tagName ? void i.removeAttribute(t) : void(os.test(t) ? i.setAttribute(t, e ? "true" : "false") : null != e && e !== !1 ? "class" === t ? (i.__v_trans && (e += " " + i.__v_trans.id + "-transition"), K(i, e)) : ns.test(t) ? i.setAttributeNS(is, t, e === !0 ? "" : e) : i.setAttribute(t, e === !0 ? "" : e) : i.removeAttribute(t))
            }
        },
        ls = {
            priority: Fr,
            bind: function() {
                if (this.arg) {
                    var t = this.id = l(this.arg),
                        e = (this._scope || this.vm).$els;
                    i(e, t) ? e[t] = this.el : kt(e, t, this.el)
                }
            },
            unbind: function() {
                var t = (this._scope || this.vm).$els;
                t[this.id] === this.el && (t[this.id] = null)
            }
        },
        cs = {
            bind: function() {}
        },
        us = {
            bind: function() {
                var t = this.el;
                this.vm.$once("pre-hook:compiled", function() {
                    t.removeAttribute("v-cloak")
                })
            }
        },
        fs = {
            text: gr,
            html: Ar,
            "for": Mr,
            "if": Wr,
            show: Ir,
            model: qr,
            on: Gr,
            bind: hs,
            el: ls,
            ref: cs,
            cloak: us
        },
        ps = {
            deep: !0,
            update: function(t) {
                t && "string" == typeof t ? this.handleObject(ge(t)) : g(t) ? this.handleObject(t) : Fi(t) ? this.handleArray(t) : this.cleanup()
            },
            handleObject: function(t) {
                this.cleanup(t), this.prevKeys = Object.keys(t), me(this.el, t)
            },
            handleArray: function(t) {
                this.cleanup(t);
                for (var e = 0, i = t.length; i > e; e++) {
                    var n = t[e];
                    n && g(n) ? me(this.el, n) : n && "string" == typeof n && Z(this.el, n)
                }
                this.prevKeys = t.slice();
            },
            cleanup: function(t) {
                if (this.prevKeys)
                    for (var e = this.prevKeys.length; e--;) {
                        var i = this.prevKeys[e];
                        if (i)
                            for (var n = g(i) ? Object.keys(i) : [i], r = 0, s = n.length; s > r; r++) _e(this.el, n[r], X)
                    }
            }
        },
        ds = {
            priority: Sr,
            params: ["keep-alive", "transition-mode", "inline-template"],
            bind: function() {
                this.el.__vue__ || (this.keepAlive = this.params.keepAlive, this.keepAlive && (this.cache = {}), this.params.inlineTemplate && (this.inlineTemplate = Y(this.el, !0)), this.pendingComponentCb = this.Component = null, this.pendingRemovals = 0, this.pendingRemovalCb = null, this.anchor = nt("v-component"), J(this.el, this.anchor), this.el.removeAttribute("is"), this.descriptor.ref && this.el.removeAttribute("v-ref:" + u(this.descriptor.ref)), this.literal && this.setComponent(this.expression))
            },
            update: function(t) {
                this.literal || this.setComponent(t)
            },
            setComponent: function(t, e) {
                if (this.invalidatePending(), t) {
                    var i = this;
                    this.resolveComponent(t, function() {
                        i.mountComponent(e)
                    })
                } else this.unbuild(!0), this.remove(this.childVM, e), this.childVM = null
            },
            resolveComponent: function(t, e) {
                var i = this;
                this.pendingComponentCb = w(function(n) {
                    i.ComponentName = n.options.name || ("string" == typeof t ? t : null), i.Component = n, e()
                }), this.vm._resolveComponent(t, this.pendingComponentCb)
            },
            mountComponent: function(t) {
                this.unbuild(!0);
                var e = this,
                    i = this.Component.options.activate,
                    n = this.getCached(),
                    r = this.build();
                i && !n ? (this.waitingFor = r, ye(i, r, function() {
                    e.waitingFor === r && (e.waitingFor = null, e.transition(r, t))
                })) : (n && r._updateRef(), this.transition(r, t))
            },
            invalidatePending: function() {
                this.pendingComponentCb && (this.pendingComponentCb.cancel(), this.pendingComponentCb = null)
            },
            build: function(t) {
                var e = this.getCached();
                if (e) return e;
                if (this.Component) {
                    var i = {
                        name: this.ComponentName,
                        el: Gt(this.el),
                        template: this.inlineTemplate,
                        parent: this._host || this.vm,
                        _linkerCachable: !this.inlineTemplate,
                        _ref: this.descriptor.ref,
                        _asComponent: !0,
                        _isRouterView: this._isRouterView,
                        _context: this.vm,
                        _scope: this._scope,
                        _frag: this._frag
                    };
                    t && v(i, t);
                    var n = new this.Component(i);
                    return this.keepAlive && (this.cache[this.Component.cid] = n), n
                }
            },
            getCached: function() {
                return this.keepAlive && this.cache[this.Component.cid]
            },
            unbuild: function(t) {
                this.waitingFor && (this.keepAlive || this.waitingFor.$destroy(), this.waitingFor = null);
                var e = this.childVM;
                return !e || this.keepAlive ? void(e && (e._inactive = !0, e._updateRef(!0))) : void e.$destroy(!1, t)
            },
            remove: function(t, e) {
                var i = this.keepAlive;
                if (t) {
                    this.pendingRemovals++, this.pendingRemovalCb = e;
                    var n = this;
                    t.$remove(function() {
                        n.pendingRemovals--, i || t._cleanup(), !n.pendingRemovals && n.pendingRemovalCb && (n.pendingRemovalCb(), n.pendingRemovalCb = null)
                    })
                } else e && e()
            },
            transition: function(t, e) {
                var i = this,
                    n = this.childVM;
                switch (n && (n._inactive = !0), t._inactive = !1, this.childVM = t, i.params.transitionMode) {
                    case "in-out":
                        t.$before(i.anchor, function() {
                            i.remove(n, e)
                        });
                        break;
                    case "out-in":
                        i.remove(n, function() {
                            t.$before(i.anchor, e)
                        });
                        break;
                    default:
                        i.remove(n), t.$before(i.anchor, e)
                }
            },
            unbind: function() {
                if (this.invalidatePending(), this.unbuild(), this.cache) {
                    for (var t in this.cache) this.cache[t].$destroy();
                    this.cache = null
                }
            }
        },
        vs = _n._propBindingModes,
        ms = {},
        gs = /^[$_a-zA-Z]+[\w$]*$/,
        _s = _n._propBindingModes,
        ys = {
            bind: function() {
                var t = this.vm,
                    e = t._context,
                    i = this.descriptor.prop,
                    n = i.path,
                    r = i.parentPath,
                    s = i.mode === _s.TWO_WAY,
                    o = this.parentWatcher = new zt(e, r, function(e) {
                        ke(t, i, e)
                    }, {
                        twoWay: s,
                        filters: i.filters,
                        scope: this._scope
                    });
                if ($e(t, i, o.value), s) {
                    var a = this;
                    t.$once("pre-hook:created", function() {
                        a.childWatcher = new zt(t, n, function(t) {
                            o.set(t)
                        }, {
                            sync: !0
                        })
                    })
                }
            },
            unbind: function() {
                this.parentWatcher.teardown(), this.childWatcher && this.childWatcher.teardown()
            }
        },
        bs = [],
        ws = !1,
        Cs = "transition",
        $s = "animation",
        ks = Mi + "Duration",
        xs = Ii + "Duration",
        As = Di && window.requestAnimationFrame,
        Os = As ? function(t) {
            As(function() {
                As(t)
            })
        } : function(t) {
            setTimeout(t, 50)
        },
        Ts = Ee.prototype;
    Ts.enter = function(t, e) {
        this.cancelPending(), this.callHook("beforeEnter"), this.cb = e, Z(this.el, this.enterClass), t(), this.entered = !1, this.callHookWithCb("enter"), this.entered || (this.cancel = this.hooks && this.hooks.enterCancelled, Ne(this.enterNextTick))
    }, Ts.enterNextTick = function() {
        var t = this;
        this.justEntered = !0, Os(function() {
            t.justEntered = !1
        });
        var e = this.enterDone,
            i = this.getCssTransitionType(this.enterClass);
        this.pendingJsCb ? i === Cs && X(this.el, this.enterClass) : i === Cs ? (X(this.el, this.enterClass), this.setupCssCb(Wi, e)) : i === $s ? this.setupCssCb(Bi, e) : e()
    }, Ts.enterDone = function() {
        this.entered = !0, this.cancel = this.pendingJsCb = null, X(this.el, this.enterClass), this.callHook("afterEnter"), this.cb && this.cb()
    }, Ts.leave = function(t, e) {
        this.cancelPending(), this.callHook("beforeLeave"), this.op = t, this.cb = e, Z(this.el, this.leaveClass), this.left = !1, this.callHookWithCb("leave"), this.left || (this.cancel = this.hooks && this.hooks.leaveCancelled, this.op && !this.pendingJsCb && (this.justEntered ? this.leaveDone() : Ne(this.leaveNextTick)))
    }, Ts.leaveNextTick = function() {
        var t = this.getCssTransitionType(this.leaveClass);
        if (t) {
            var e = t === Cs ? Wi : Bi;
            this.setupCssCb(e, this.leaveDone)
        } else this.leaveDone()
    }, Ts.leaveDone = function() {
        this.left = !0, this.cancel = this.pendingJsCb = null, this.op(), X(this.el, this.leaveClass), this.callHook("afterLeave"), this.cb && this.cb(), this.op = null
    }, Ts.cancelPending = function() {
        this.op = this.cb = null;
        var t = !1;
        this.pendingCssCb && (t = !0, Q(this.el, this.pendingCssEvent, this.pendingCssCb), this.pendingCssEvent = this.pendingCssCb = null), this.pendingJsCb && (t = !0, this.pendingJsCb.cancel(), this.pendingJsCb = null), t && (X(this.el, this.enterClass), X(this.el, this.leaveClass)), this.cancel && (this.cancel.call(this.vm, this.el), this.cancel = null)
    }, Ts.callHook = function(t) {
        this.hooks && this.hooks[t] && this.hooks[t].call(this.vm, this.el)
    }, Ts.callHookWithCb = function(t) {
        var e = this.hooks && this.hooks[t];
        e && (e.length > 1 && (this.pendingJsCb = w(this[t + "Done"])), e.call(this.vm, this.el, this.pendingJsCb))
    }, Ts.getCssTransitionType = function(t) {
        if (!(!Wi || document.hidden || this.hooks && this.hooks.css === !1 || Fe(this.el))) {
            var e = this.type || this.typeCache[t];
            if (e) return e;
            var i = this.el.style,
                n = window.getComputedStyle(this.el),
                r = i[ks] || n[ks];
            if (r && "0s" !== r) e = Cs;
            else {
                var s = i[xs] || n[xs];
                s && "0s" !== s && (e = $s)
            }
            return e && (this.typeCache[t] = e), e
        }
    }, Ts.setupCssCb = function(t, e) {
        this.pendingCssEvent = t;
        var i = this,
            n = this.el,
            r = this.pendingCssCb = function(s) {
                s.target === n && (Q(n, t, r), i.pendingCssEvent = i.pendingCssCb = null, !i.pendingJsCb && e && e())
            };
        q(n, t, r)
    };
    var Ns = {
            priority: Er,
            update: function(t, e) {
                var i = this.el,
                    n = gt(this.vm.$options, "transitions", t);
                t = t || "v", i.__v_trans = new Ee(i, t, n, this.vm), e && X(i, e + "-transition"), Z(i, t + "-transition")
            }
        },
        js = {
            style: es,
            "class": ps,
            component: ds,
            prop: ys,
            transition: Ns
        },
        Es = /^v-bind:|^:/,
        Fs = /^v-on:|^@/,
        Ss = /^v-([^:]+)(?:$|:(.*)$)/,
        Ds = /\.[^\.]+/g,
        Ps = /^(v-bind:|:)?transition$/,
        Rs = 1e3,
        Ls = 2e3;
    Ze.terminal = !0;
    var Hs = /[^\w\-:\.]/,
        Ms = Object.freeze({
            compile: Se,
            compileAndLinkProps: He,
            compileRoot: Me,
            transclude: ni,
            resolveSlots: ai
        }),
        Ws = /^v-on:|^@/;
    fi.prototype._bind = function() {
        var t = this.name,
            e = this.descriptor;
        if (("cloak" !== t || this.vm._isCompiled) && this.el && this.el.removeAttribute) {
            var i = e.attr || "v-" + t;
            this.el.removeAttribute(i)
        }
        var n = e.def;
        if ("function" == typeof n ? this.update = n : v(this, n), this._setupParams(), this.bind && this.bind(), this._bound = !0, this.literal) this.update && this.update(e.raw);
        else if ((this.expression || this.modifiers) && (this.update || this.twoWay) && !this._checkStatement()) {
            var r = this;
            this.update ? this._update = function(t, e) {
                r._locked || r.update(t, e)
            } : this._update = ui;
            var s = this._preProcess ? p(this._preProcess, this) : null,
                o = this._postProcess ? p(this._postProcess, this) : null,
                a = this._watcher = new zt(this.vm, this.expression, this._update, {
                    filters: this.filters,
                    twoWay: this.twoWay,
                    deep: this.deep,
                    preProcess: s,
                    postProcess: o,
                    scope: this._scope
                });
            this.afterBind ? this.afterBind() : this.update && this.update(a.value)
        }
    }, fi.prototype._setupParams = function() {
        if (this.params) {
            var t = this.params;
            this.params = Object.create(null);
            for (var e, i, n, r = t.length; r--;) e = u(t[r]), n = l(e), i = W(this.el, e), null != i ? this._setupParamWatcher(n, i) : (i = M(this.el, e), null != i && (this.params[n] = "" === i ? !0 : i))
        }
    }, fi.prototype._setupParamWatcher = function(t, e) {
        var i = this,
            n = !1,
            r = (this._scope || this.vm).$watch(e, function(e, r) {
                if (i.params[t] = e, n) {
                    var s = i.paramWatchers && i.paramWatchers[t];
                    s && s.call(i, e, r)
                } else n = !0
            }, {
                immediate: !0,
                user: !1
            });
        (this._paramUnwatchFns || (this._paramUnwatchFns = [])).push(r)
    }, fi.prototype._checkStatement = function() {
        var t = this.expression;
        if (t && this.acceptStatement && !Mt(t)) {
            var e = Ht(t).get,
                i = this._scope || this.vm,
                n = function(t) {
                    i.$event = t, e.call(i, i), i.$event = null
                };
            return this.filters && (n = i._applyFilters(n, null, this.filters)), this.update(n), !0
        }
    }, fi.prototype.set = function(t) {
        this.twoWay && this._withLock(function() {
            this._watcher.set(t)
        })
    }, fi.prototype._withLock = function(t) {
        var e = this;
        e._locked = !0, t.call(e), Ui(function() {
            e._locked = !1
        })
    }, fi.prototype.on = function(t, e, i) {
        q(this.el, t, e, i), (this._listeners || (this._listeners = [])).push([t, e])
    }, fi.prototype._teardown = function() {
        if (this._bound) {
            this._bound = !1, this.unbind && this.unbind(), this._watcher && this._watcher.teardown();
            var t, e = this._listeners;
            if (e)
                for (t = e.length; t--;) Q(this.el, e[t][0], e[t][1]);
            var i = this._paramUnwatchFns;
            if (i)
                for (t = i.length; t--;) i[t]();
            this.vm = this.el = this._watcher = this._listeners = null
        }
    };
    var Is = /[^|]\|[^|]/;
    xt(yi), li(yi), ci(yi), pi(yi), di(yi), vi(yi), mi(yi), gi(yi), _i(yi);
    var Bs = {
            priority: Lr,
            params: ["name"],
            bind: function() {
                var t = this.params.name || "default",
                    e = this.vm._slotContents && this.vm._slotContents[t];
                e && e.hasChildNodes() ? this.compile(e.cloneNode(!0), this.vm._context, this.vm) : this.fallback()
            },
            compile: function(t, e, i) {
                if (t && e) {
                    if (this.el.hasChildNodes() && 1 === t.childNodes.length && 1 === t.childNodes[0].nodeType && t.childNodes[0].hasAttribute("v-if")) {
                        var n = document.createElement("template");
                        n.setAttribute("v-else", ""), n.innerHTML = this.el.innerHTML, n._context = this.vm, t.appendChild(n)
                    }
                    var r = i ? i._scope : this._scope;
                    this.unlink = e.$compile(t, i, r, this._frag)
                }
                t ? J(this.el, t) : z(this.el)
            },
            fallback: function() {
                this.compile(Y(this.el, !0), this.vm)
            },
            unbind: function() {
                this.unlink && this.unlink()
            }
        },
        Vs = {
            priority: Dr,
            params: ["name"],
            paramWatchers: {
                name: function(t) {
                    Wr.remove.call(this), t && this.insert(t)
                }
            },
            bind: function() {
                this.anchor = nt("v-partial"), J(this.el, this.anchor), this.insert(this.params.name)
            },
            insert: function(t) {
                var e = gt(this.vm.$options, "partials", t, !0);
                e && (this.factory = new re(this.vm, e), Wr.insert.call(this))
            },
            unbind: function() {
                this.frag && this.frag.destroy()
            }
        },
        zs = {
            slot: Bs,
            partial: Vs
        },
        Us = Mr._postProcess,
        Js = /(\d{3})(?=\d)/g,
        qs = {
            orderBy: Ci,
            filterBy: wi,
            limitBy: bi,
            json: {
                read: function(t, e) {
                    return "string" == typeof t ? t : JSON.stringify(t, null, Number(e) || 2)
                },
                write: function(t) {
                    try {
                        return JSON.parse(t)
                    } catch (e) {
                        return t
                    }
                }
            },
            capitalize: function(t) {
                return t || 0 === t ? (t = t.toString(), t.charAt(0).toUpperCase() + t.slice(1)) : ""
            },
            uppercase: function(t) {
                return t || 0 === t ? t.toString().toUpperCase() : ""
            },
            lowercase: function(t) {
                return t || 0 === t ? t.toString().toLowerCase() : ""
            },
            currency: function(t, e) {
                if (t = parseFloat(t), !isFinite(t) || !t && 0 !== t) return "";
                e = null != e ? e : "$";
                var i = Math.abs(t).toFixed(2),
                    n = i.slice(0, -3),
                    r = n.length % 3,
                    s = r > 0 ? n.slice(0, r) + (n.length > 3 ? "," : "") : "",
                    o = i.slice(-3),
                    a = 0 > t ? "-" : "";
                return a + e + s + n.slice(r).replace(Js, "$1,") + o
            },
            pluralize: function(t) {
                var e = d(arguments, 1);
                return e.length > 1 ? e[t % 10 - 1] || e[e.length - 1] : e[0] + (1 === t ? "" : "s")
            },
            debounce: function(t, e) {
                return t ? (e || (e = 300), y(t, e)) : void 0
            }
        };
    return ki(yi), yi.version = "1.0.21", setTimeout(function() {
        _n.devtools && Pi && Pi.emit("init", yi)
    }, 0), yi
});

define("detail.pages.offerRemark.View", ["jQuery", "Class", "detail.lib.page.Tracelog"], function(i, t, e) {
    return t({
        init: function(i, t) {
            this.onEvent = "tap", this.div = i, this.config = t, this._initTracelog()
        },
        _initTracelog: function() {
            new e(this.div, this.config)
        }
    })
});
! function(t) {
    function o() {
        var t = jQuery,
            o = t("body");
        o.on("wing-layout-ready", function(t, o) {
            e(o)
        }), o.trigger("wing-layout-ready", {
            container: o,
            height: t(window).height()
        })
    }

    function e(t) {
        var o = t.container;
        if (!o || !o.length) throw new Error("container required");
        var e = jQuery,
            i = e("div.wing-layout-top", o),
            r = e("div.wing-layout-bottom", o),
            a = e("div.wing-layout-center", o);
        if (a.length) {
            var g = i.height() || 0,
                h = r.height() || 0,
                l = {};
            i.length && (l["margin-top"] = g + "px"), r.length && (l["margin-bottom"] = h + "px"), n(a, "h5:page-scroll") || (l.height = t.height - g - h + "px"), n(a, "h5:overflow-scrolling-touch") && a.addClass("wing-layout-overflow-scrolling-touch"), a.css(l)
        }
    }

    function n(t, o) {
        for (var e = t.data("effects") || [], n = 0, i = e.length; i > n; n++) {
            var r = e[n];
            if (r.type === o) return r
        }
    }
    t.layouttemplate = {
        layoutframe: function(t) {
            if (!t.getAttribute("height")) {
                var o = function() {
                    var e = t.contentWindow;
                    if (e && e.document) try {
                        var n = e.document.body.scrollHeight,
                            i = e.document.documentElement.scrollHeight,
                            r = Math.max(n, i);
                        r && (t.height = r), setTimeout(o, 200)
                    } catch (a) {
                        console.error(a)
                    }
                };
                o()
            }
        }
    }, Wing.ready(o)
}(Wing.navigator);
define("detail.modules.subHeader.View", ["jQuery", "Class"], function(n, i) {
    return i({
        init: function(n, i) {
            this.onEvent = "tap", this.div = n, this.config = i, this.bindEvent()
        },
        bindEvent: function() {
            this.div.on("tap", ".back", function(n) {
                Wing.navigator.back.go()
            }).on("tap", ".icon-more", function() {
                Wing.navigator.nativemenu.show(48, [])
            })
        }
    })
});
define("detail.modules.offerRemark.View", ["jQuery", "Class", "detail.core.Wing", "detail.core.Event", "detail.modules.offerRemark.renderRemark"], function(e, i, t, n, a) {
    return i({
        init: function(e, i) {
            this.onEvent = "click", this.div = e, this.config = i, this.bindEvent(), this.getRemarkList(), this.initTabEvent();
            try {
                a.init(i.loginId)
            } catch (t) {
                console.log(t)
            }
        },
        bindEvent: function() {
            var i = this;
            this.div.on("click", "div.level-filter div.filter", function() {
                var t = e(this).data("level") - 0;
                e(this).parent().find("div.filter").removeClass("active"), e(this).addClass("active"), i.getRemarkList({
                    starLevel: t
                })
            })
        },
        getRemarkList: function(i) {
            var n = {
                    receiveUserId: this.config.userId - 0,
                    starLevel: 0,
                    itemId: this.config.offerId - 0,
                    bizType: "trade",
                    page: 1,
                    pageSize: 5
                },
                a = this;
            e.extend(n, i), t.load("offerRemarkList", {
                data: n
            }).done(function(i, t) {
                var n = i.find("div.remark-item");
                e("#remark-list-container").html("").append(i), (n.length < 5 || a.config.rateTotals < 6) && e("#pullUp").remove(), t()
            })
        },
        initTabEvent: function() {
            var i, t = e("div.detail-tab", this.div),
                n = t.offset().top,
                a = 0;
            e(window).on("scroll", function() {
                i = e(window).scrollTop(), t[i > n ? "addClass" : "removeClass"]("fixed"), a = i
            })
        },
        end: 0
    })
});
var SceneManage = {};
SceneManage.scene = null, SceneManage.$ = null, SceneManage.record = {};
var date = new Date;
SceneManage.startTime = date.getTime();
var verison = Math.round(date.getTime() / 1e3 / 86400);
SceneManage.version = verison,
    function(e) {
        var t = function() {
            var e = navigator.userAgent;
            return e && (e.indexOf("Baiduspider") > 0 || e.indexOf("Googlebot") > 0 || e.indexOf("MSNBot") > 0 || e.indexOf("YoudaoBot") > 0 || e.indexOf("Sogou") > 0 && e.indexOf("spider") > 0 || e.indexOf("JikeSpider") > 0 || e.indexOf("Sosospider") > 0 || e.indexOf("360Spider") > 0 || e.indexOf("HaoSouSpider") > 0 || e.indexOf("YisouSpider") > 0) ? !0 : !1
        };
        if (!t()) {
            var n = function() {
                    var e = document.referrer,
                        t = location.search,
                        n = !1;
                    if (e && e.indexOf("1688.com") > 0) n = !0;
                    else if (t)
                        for (var r = t.split("&"), o = 0; o < r.length; o++)
                            if (r[o].indexOf("spm=") >= 0) {
                                n = !0;
                                break
                            }
                    return n
                },
                r = function(e) {
                    SceneManage.$ = e, e(document).ready(function() {
                        var t = document.body.getAttribute("data-spm");
                        t || (t = window.location.origin + window.location.pathname), SceneManage.record.spmb = t;
                        var r = document.createElement("script");
                        r.setAttribute("async", !0);
                        var o = document.referrer,
                            a = location.search,
                            i = "",
                            c = "https://cui.m.1688.com/scene?spmb=" + encodeURIComponent(t) + "&referrer=" + encodeURIComponent(o);
                        if (a && "" != a) {
                            var d = a.substring(1),
                                s = d.split("&");
                            for (var f in s) {
                                var u = s[f].split("=");
                                2 == u.length && ("env" == u[0] ? (i = u[1], c = c + "&env=" + i) : "isGray" == u[0] && (c = c + "&isGray=" + u[1]))
                            }
                        }
                        var m = function() {
                                var e = /\/offer\/(\d+)\.html/g,
                                    t = null;
                                return e.test(location.href) && (t = RegExp.$1), t
                            },
                            p = e("#ws-page").attr("data-keywords"),
                            l = m();
                        if (p && "" !== p)
                            for (var s = e(".wsw-offer a"), g = s.size(), v = /\/offer\/(\d+)\.html/g, f = 0; g > f; f++) {
                                var w = s.get(f).getAttribute("href");
                                if (v.test(w)) {
                                    l = RegExp.$1;
                                    break
                                }
                            } else if (p = e("#searchKeywords").val(), p && "" !== p)
                                for (var s = e(".a"), g = s.size(), v = /\/offer\/(\d+)\.html/g, f = 0; g > f; f++) {
                                    var w = s.get(f).getAttribute("href");
                                    if (v.test(w)) {
                                        l = RegExp.$1;
                                        break
                                    }
                                }
                        l && "" !== l && (c += "&itemId=" + l), p && "" !== p && (c += "&keyword=" + encodeURIComponent(p)), c += "&serial=" + n(), r.src = c, r.onerror = function() {
                            setTimeout(function() {
                                r.src = c + "&time=" + (new Date).getTime()
                            }, 500)
                        }, document.body.appendChild(r);
                        var h = document.createElement("script");
                        h.setAttribute("async", !0);
                        var S = SceneManage.version;
                        try {
                            var b = window.localStorage.getItem("showScript");
                            b && "" != b && (S = b)
                        } catch (x) {}
                        h.src = "//astyle.alicdn.com/m/roc/wap/static/sceneshow.js?_v=20170728" + S + ".js", document.body.appendChild(h)
                    })
                };
            if (e) r(e);
            else {
                var o = document.createElement("script");
                o.src = "//g.alicdn.com/mtb/??zepto/1.1.3/zepto.js", o.setAttribute("async", !0), o.onload = function() {
                    r(window.Zepto)
                }, document.body.appendChild(o)
            }
        }
    }(window.jQuery || window.Zepto);
! function(e) {
    function t(e) {
        return "[object String]" == Object.prototype.toString.call(e)
    }
    if (!window.ImageControl) {
        var i = {},
            r = !1,
            e = e;
        i.defaultWidth = [16, 20, 24, 30, 32, 36, 40, 48, 50, 60, 64, 70, 72, 75, 80, 81, 88, 90, 100, 110, 115, 120, 121, 125, 128, 130, 140, 142, 145, 150, 160, 165, 170, 180, 190, 196, 200, 210, 220, 230, 240, 250, 264, 270, 280, 284, 288, 290, 292, 294, 300, 310, 315, 320, 336, 350, 360, 400, 420, 430, 440, 450, 460, 468, 480, 485, 490, 500, 540, 560, 570, 580, 600, 640, 660, 670, 720, 728, 760, 790, 960], i.defaultSize = {
            16: [16],
            20: [20],
            24: [24],
            30: [30],
            32: [32],
            36: [36],
            40: [40],
            48: [48],
            50: [50],
            60: [30, 60, 90],
            64: [64],
            70: [70],
            72: [72],
            75: [75, 100],
            80: [48, 60, 80],
            81: [65],
            88: [88],
            90: [45, 60, 90, 135],
            100: [50, 100, 150],
            110: [90, 110],
            115: [100],
            120: [60, 90, 120, 160],
            121: [75],
            125: [125],
            128: [128],
            130: [130],
            140: [70, 140],
            142: [142],
            145: [145],
            150: [150, 200],
            160: [80, 90, 160, 180, 240],
            165: [5e3],
            170: [120, 170],
            180: [90, 180, 230],
            190: [43, 190],
            196: [196],
            200: [100, 200],
            210: [140, 210],
            220: [220, 330],
            230: [87, 230],
            234: [234],
            240: [240],
            250: [225, 250],
            264: [100],
            270: [180, 270],
            280: [410],
            284: [284],
            288: [480],
            290: [290],
            292: [292],
            294: [430],
            300: [300, 1e3],
            310: [310],
            315: [315],
            320: [320, 480],
            336: [336],
            350: [350],
            360: [360],
            400: [152, 400],
            420: [280],
            430: [430],
            440: [440],
            450: [600],
            460: [460],
            468: [468],
            480: [420, 480],
            485: [175],
            490: [330, 490],
            500: [450, 1e3],
            540: [540],
            560: [370, 560, 840],
            570: [570],
            580: [580],
            600: [600],
            640: [480, 640],
            660: [440],
            670: [670],
            720: [720],
            728: [728],
            760: [760],
            790: [420],
            960: [960]
        }, i.cutSize = {
            "72x72": !0,
            "88x88": !0,
            "100x100": !0,
            "110x110": !0,
            "112x336": !0,
            "120x120": !0,
            "145x145": !0,
            "160x160": !0,
            "160x240": !0,
            "170x170": !0,
            "180x180": !0,
            "200x200": !0,
            "230x230": !0,
            "240x240": !0,
            "270x270": !0,
            "290x290": !0,
            "336x112": !0,
            "360x360": !0,
            "310x310": !0,
            "320x320": !0,
            "320x378": !0,
            "580x580": !0,
            "460x460": !0,
            "640x640": !0,
            "560x840": !0
        };
        var n = "q90",
            a = !1,
            o = !0,
            c = {},
            l = {},
            d = "data-lazyload-src",
            s = !1,
            p = function() {
                function e() {
                    for (var e = 0, t = {}; e < arguments.length; e++) {
                        var i = arguments[e];
                        for (var r in i) t[r] = i[r]
                    }
                    return t
                }

                function t(i) {
                    function r(t, n, a) {
                        var o;
                        if (arguments.length > 1) {
                            if (a = e({
                                    path: "/"
                                }, r.defaults, a), "number" == typeof a.expires) {
                                var c = new Date;
                                c.setMilliseconds(c.getMilliseconds() + 864e5 * a.expires), a.expires = c
                            }
                            try {
                                o = JSON.stringify(n), /^[\{\[]/.test(o) && (n = o)
                            } catch (l) {}
                            return n = i.write ? i.write(n, t) : encodeURIComponent(String(n)).replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g, decodeURIComponent), t = encodeURIComponent(String(t)), t = t.replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent), t = t.replace(/[\(\)]/g, escape), document.cookie = [t, "=", n, a.expires && "; expires=" + a.expires.toUTCString(), a.path && "; path=" + a.path, a.domain && "; domain=" + a.domain, a.secure ? "; secure" : ""].join("")
                        }
                        t || (o = {});
                        for (var d = document.cookie ? document.cookie.split("; ") : [], s = /(%[0-9A-Z]{2})+/g, p = 0; p < d.length; p++) {
                            var u = d[p].split("="),
                                f = u[0].replace(s, decodeURIComponent),
                                g = u.slice(1).join("=");
                            '"' === g.charAt(0) && (g = g.slice(1, -1));
                            try {
                                if (g = i.read ? i.read(g, f) : i(g, f) || g.replace(s, decodeURIComponent), this.json) try {
                                    g = JSON.parse(g)
                                } catch (l) {}
                                if (t === f) {
                                    o = g;
                                    break
                                }
                                t || (o[f] = g)
                            } catch (l) {}
                        }
                        return o
                    }
                    return r.get = r.set = r, r.getJSON = function() {
                        return r.apply({
                            json: !0
                        }, [].slice.call(arguments))
                    }, r.defaults = {}, r.remove = function(t, i) {
                        r(t, "", e(i, {
                            expires: -1
                        }))
                    }, r.withConverter = t, r
                }
                return t(function() {})
            }(),
            u = function() {
                if (p.set("webp", "0", {
                        expires: 7,
                        domain: ".1688.com",
                        path: "/"
                    }), window.localStorage) try {
                    var e = window.localStorage.getItem("needWebpJS"),
                        t = window.localStorage.getItem("webp");
                    if (e) {
                        r = !1;
                        var i = document.createElement("script");
                        i.type = "text/javascript";
                        var n = document.getElementsByTagName("head")[0];
                        return i.src = "//astyle.alicdn.com/m/roc/wap/static/webpjs-0.0.2.min.js", n.appendChild(i), i.onload = function() {
                            r = !0
                        }, void p.set("webp", "0", {
                            expires: 7,
                            domain: ".1688.com",
                            path: "/"
                        })
                    }
                    if (t && "true" == t) return r = !0, void p.set("webp", "1", {
                        expires: 7,
                        domain: ".1688.com",
                        path: "/"
                    })
                } catch (a) {
                    t = p.get("webp"), t && "1" == t && (r = !0)
                }
                var o = new Image;
                new Date;
                o.src = "data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA", o.onload = o.onerror = function() {
                    if (2 != o.height) {
                        r = !1, p.set("webp", "0", {
                            expires: 7,
                            domain: ".1688.com",
                            path: "/"
                        });
                        var e = document.createElement("script");
                        e.type = "text/javascript", e.async = !0;
                        var t = document.getElementsByTagName("script")[0];
                        e.src = "//astyle.alicdn.com/m/roc/wap/static/webpjs-0.0.2.min.js", e.onload = function() {
                            if (r = !0, p.set("webp", "0", {
                                    expires: 7,
                                    domain: ".1688.com",
                                    path: "/"
                                }), window.localStorage) try {
                                window.localStorage.setItem("webp", !0), window.localStorage.setItem("needWebpJS", !0)
                            } catch (e) {}
                        }, t.parentNode.insertBefore(e, t)
                    } else if (r = !0, p.set("webp", "1", {
                            expires: 7,
                            domain: ".1688.com",
                            path: "/"
                        }), window.localStorage) try {
                        window.localStorage.setItem("webp", !0)
                    } catch (i) {}
                }
            };
        u(), i.isSupportWebp = function() {
            return r
        }, i.getFillSize = function(e, t, a, c) {
            if (!e || "" == e) return e;
            (0 == t || t > document.documentElement.offsetWidth) && (t = document.documentElement.offsetWidth), window.devicePixelRatio && o && !c && (t * window.devicePixelRatio < 480 ? (t *= window.devicePixelRatio, a *= window.devicePixelRatio) : t = 480), e = e.replace(/_\d+x\d+xzq\d+\.jpg$/g, ""), e = e.replace(/\d+x\d+xzq\d+\.jpg$/g, "jpg"), e = e.replace(/\.\d+x\d+/g, "");
            var l = e.split("-"),
                d = 0,
                s = 0;
            if (e.toLowerCase().indexOf("_.webp") > 0 && (e = e.substring(0, e.indexOf("_.webp"))), e.indexOf("xz.jpg") > 0 && (e = e.replace("xz.jpg", ".jpg")), l.length > 1 && (d = parseInt(l[1]), 3 == l.length)) {
                var p = l[2];
                s = parseInt(p.substring(0, p.indexOf(".")))
            }
            if (0 == d && (d = t), 0 == s && (s = a), t > d || a > s) return n && "" != n && (e += "_" + n + ".jpg"), r ? e + "_.webp" : e;
            var u = i.getFixSize(t, a);
            if (!u) return n && "" != n && (e += "_" + n + ".jpg"), r ? e + "_.webp" : e;
            var f = u.width,
                g = u.height,
                m = "";
            if (g) {
                var w = f + "x" + g;
                i.cutSize[w] && d >= s && Math.round(d / s) < 2 && (w += "xz"), w += n, m = "_" + w + ".jpg"
            }
            return m ? (r ? e = e + m + "_.webp" : e += m, e) : e
        }, i.getFixSize = function(e, t) {
            var r = e / t;
            if (l[e + "x" + t]) return l[e + "x" + t];
            var n = e >= t ? e : t,
                a = null,
                o = i.defaultWidth,
                c = e;
            if (t > 0 && t > e && (c = t), o[0] >= c) n = o[0];
            else
                for (var d = 0, s = o.length; s > d; d++) {
                    if (d == s - 1) {
                        n = o[d];
                        break
                    }
                    if (o[d] >= c) {
                        var p = i.defaultSize[o[d]];
                        if (1 != p.length) {
                            n = o[d];
                            break
                        }
                        if (a = p[0], Math.abs(r - n / a) <= .5) {
                            n = o[d];
                            break
                        }
                    }
                }
            var u = i.defaultSize[n];
            if (!u) return null;
            if (1 == u.length) a = u[0], suffix = "_" + n + "x" + u[0] + ".jpg";
            else
                for (var d = 0, s = u.length; s > d; d++) {
                    if (d == s - 1) {
                        a = u[d];
                        break
                    }
                    if (n / u[d] <= r && n / u[d + 1] > r) {
                        a = u[d];
                        break
                    }
                }
            var p = {
                width: n,
                height: a
            };
            return l[e + "x" + t] = p, p
        };
        var f = function(e) {
            var t = e.attr("unable-fix");
            return t ? !1 : !0
        };
        i.enableResize = function(e, t) {
            if (!f(t)) return !1;
            var i = /\.gif$/i.test(e);
            return i ? !1 : /.+\.aliimg\.com/i.test(e) || /.+\.alicdn\.com/i.test(e) || /.+\.tbcdn\.com/i.test(e) ? !0 : !1
        };
        var g = [];
        i.on = function(e) {
                g.push(e)
            }, i.pause = function() {
                a = !1
            }, i.resume = function() {
                a = !0, i.autoShow()
            }, i.autoShow = function(t) {
                if (a)
                    for (var r = e("img[" + d + "]"), n = 0, o = r.length; o > n; n++) i.loadImage(r.get(n), t)
            }, i.isAutoLoad = function() {
                return s
            }, i.loadImage = function(t, n) {
                var a = document.documentElement.clientHeight,
                    o = window.scrollY,
                    l = e(t),
                    s = l.attr(d),
                    p = l.attr("load-finished");
                if (n || !p || "true" != p) {
                    var u = l.attr("loading");
                    if (!u && "true" != u && s) {
                        s = s.replace(/\s/g, ""), s.indexOf("?") > 0 && (s = s.substring(0, s.indexOf("?"))), s = s.replace(/img\.china\.alibaba\.com/, "cbu01.alicdn.com"), s = s.replace(/gtms[\d]{2}\.alicdn\.com/, "gw.alicdn.com"), s = s.replace(/cbu[\d]{2}\.alicdn\.com/, "cbu01.alicdn.com"), s = s.replace(/style\.c\.aliimg\.com/, "astyle.alicdn.com");
                        var f = l.height(),
                            m = l.parent();
                        m && 1 == m.children().length && (f = m.height());
                        var w = l.offset().top;
                        if (a + o >= w && w + f >= o) {
                            if (s && !i.enableResize(s, l)) return l.attr("src", s), void l.attr(d, null);
                            s = s.replace(/\.search\./, ".");
                            var h = l.width();
                            if (t.parentElement && "p" == t.parentElement.tagName.toLowerCase() && (h = t.parentElement.offsetWidth), m && 1 == m.children().length && (h = m.width()), 0 == h && (h = l.css("width"))) try {
                                h = parseInt(h)
                            } catch (x) {
                                h = 0
                            }
                            h > screen.width && (h = screen.width, l.css("width", h + "px"));
                            var v = new Date;
                            l.on("load", function() {
                                if (c[this.src] = (new Date).getTime() - v.getTime(), g)
                                    for (var e in g) g[e].call(this);
                                l.attr("load-finished", "true"), l.attr("loading", null), l.attr(d, null)
                            }), l.attr("onerror", "if(this.getAttribute('load-finished')){return;}this.src='" + s + "';this.setAttribute('load-finished',true)");
                            var b = r,
                                S = l.attr("no-webp");
                            S && (r = !1);
                            var A = i.getFillSize(s, h, f);
                            r = b, l.attr("src", A), l.attr("loading", !0)
                        }
                    }
                }
            }, window.ImageControl = i,
            function(e) {
                var e = e,
                    r = null;
                e(document).ready(function() {
                    var c = window.pageLength || e("#pagecontent_length").val(),
                        l = window.pageSpeedConfig || e("#pagespeed_config").val();
                    if (l && c) {
                        if (a = l.autoFixFlag ? l.autoFixFlag : !1, l.lazyAttr && (d = l.lazyAttr), window.performance) {
                            var s = window.performance.timing,
                                p = s.responseEnd - s.responseStart,
                                u = 1e3 * c / (1024 * p);
                            r = u;
                            var f = l;
                            t(f) && (f = JSON.parse(f));
                            var g = f.quality;
                            if (g)
                                for (var m = g.split(";"), w = 0, h = m.length; h > w; w++) {
                                    var x = m[w],
                                        g = x.split(":");
                                    if (u >= g[0]) {
                                        n = g[1];
                                        break
                                    }
                                }
                            var v = f.dpr;
                            v && (0 > u || u >= v) && (o = !0)
                        }
                        if (!l.globalSwitch) return
                    }
                    if (a)
                        for (var b = document.getElementsByTagName("img"), w = 0, S = b.length; S > w; w++) {
                            var A = b[w].getAttribute(d);
                            if (!A || "" == A) {
                                var y = b[w].getAttribute("onerror");
                                if (!y) {
                                    var j = b[w].getAttribute("src");
                                    j && i.enableResize(j, e(b[w])) && (j.indexOf("?") > 0 && (j = j.substring(0, j.indexOf("?"))), b[w].setAttribute(d, j), b[w].removeAttribute("src"))
                                }
                            }
                        }
                })
            }(e)
    }
}(window.jQuery || window.Zepto);