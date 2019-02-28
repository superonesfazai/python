if(typeof define !== 'function'){
    var define = require('amdefine')(module);
}

define("taobaowpmod/shop_base_info/index.weex", ["rax", "rax-view", "rax-text", "rax-picture", "rax-touchable"], function(require, t, e) {
    try {
        var n = require("rax")
    } catch (t) {
        "undefined" != typeof console && console.log(t)
    }
    try {
        var r = require("rax-view")
    } catch (t) {
        "undefined" != typeof console && console.log(t)
    }
    try {
        var o = require("rax-text")
    } catch (t) {
        "undefined" != typeof console && console.log(t)
    }
    try {
        var i = require("rax-picture")
    } catch (t) {
        "undefined" != typeof console && console.log(t)
    }
    try {
        var a = require("rax-touchable")
    } catch (t) {
        "undefined" != typeof console && console.log(t)
    }
    return e.exports = function(t) {
        function e(r) {
            if (n[r]) return n[r].exports;
            var o = n[r] = {
                exports: {},
                id: r,
                loaded: !1
            };
            return t[r].call(o.exports, o, o.exports, e), o.loaded = !0, o.exports
        }
        var n = {};
        return e.m = t, e.c = n, e.p = "", e(0)
    }([function(t, e, n) {
        "use strict";

        function r(t) {
            return t && t.__esModule ? t : {
                default: t
            }
        }

        function o(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function i(t, e) {
            if (!t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return !e || "object" != typeof e && "function" != typeof e ? t : e
        }

        function a(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function, not " + typeof e);
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    enumerable: !1,
                    writable: !0,
                    configurable: !0
                }
            }), e && (Object.setPrototypeOf ? Object.setPrototypeOf(t, e) : t.__proto__ = e)
        }
        Object.defineProperty(e, "__esModule", {
            value: !0
        });
        var l = function() {
                function t(t, e) {
                    for (var n = 0; n < e.length; n++) {
                        var r = e[n];
                        r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(t, r.key, r)
                    }
                }
                return function(e, n, r) {
                    return n && t(e.prototype, n), r && t(e, r), e
                }
            }(),
            c = n(1),
            s = n(2),
            u = r(s),
            p = n(3),
            f = r(p),
            d = n(4),
            h = r(d),
            g = n(5),
            y = function(t) {
                if (t && t.__esModule) return t;
                var e = {};
                if (null != t)
                    for (var n in t) Object.prototype.hasOwnProperty.call(t, n) && (e[n] = t[n]);
                return e.default = t, e
            }(g),
            m = n(6),
            v = r(m),
            b = n(7),
            w = r(b),
            x = function(t) {
                function e(t) {
                    o(this, e);
                    var n = i(this, (e.__proto__ || Object.getPrototypeOf(e)).call(this, t));
                    return n.state = {
                        showDataStatus: !1,
                        showNoDataStatus: !1
                    }, n.updateShowData = function() {
                        var t = n.state,
                            e = t.gdc,
                            r = t.mds,
                            o = r.moduleData || {};
                        n.setState({
                            showDataStatus: o.ticket && Object.keys(o.ticket).length,
                            showNoDataStatus: !(1 != e.preView && "true" != e.preView || o.ticket && Object.keys(o.ticket).length)
                        })
                    }, n.goTargetUrl = function(t, e, r) {
                        var o = n.state.mds,
                            i = {
                                url: t,
                                protocol: r || "",
                                nid: e || 0,
                                widgetId: o.widgetId,
                                moduleName: o.moduleName
                            };
                        n.pageUtils.goTargetUrl && n.pageUtils.goTargetUrl(i)
                    }, n.pageUtils = t.pageUtils, n.state = {
                        gdc: n.props.gdc || {},
                        mds: n.props.mds || {},
                        items: []
                    }, n.xid = "", n
                }
                return a(e, t), l(e, [{
                    key: "createUTClickData",
                    value: function(t) {
                        return {
                            control: "Button-" + t,
                            params: {
                                shop_id: this.shopId,
                                seller_id: this.sellerId
                            }
                        }
                    }
                }, {
                    key: "componentWillMount",
                    value: function() {
                        var t = this.state.mds,
                            e = t.moduleData || {};
                        t.widgetId && Object.keys(e).length > 0 && this.updateShowData()
                    }
                }, {
                    key: "shouldComponentUpdate",
                    value: function(t, e) {
                        return !!this.shallowDiffers(this.props, t) || !!this.shallowDiffers(this.state, e)
                    }
                }, {
                    key: "shallowDiffers",
                    value: function(t, e) {
                        for (var n in t)
                            if (!(n in e)) return !0;
                        for (var r in e)
                            if (t[r] !== e[r]) return !0;
                        return !1
                    }
                }, {
                    key: "componentDidMount",
                    value: function() {
                        this.requestData()
                    }
                }, {
                    key: "requestData",
                    value: function() {
                        var t = this,
                            e = this.props.gdc,
                            n = e.userId,
                            r = e.shopId,
                            o = {
                                sellerId: n,
                                shopId: r
                            };
                        this.pageUtils.Mtop.request({
                            api: "mtop.taobao.shop.impression.intro.get",
                            v: "1.0",
                            type: "GET",
                            secType: 1,
                            data: o,
                            ecode: 0,
                            timeout: 3e3
                        }, function(e) {
                            "SUCCESS" === e.ret[0].split("::")[0] && (t.parseShopData(e.data.result), t.checkTripLicense())
                        }, function(t) {
                            t.ret[0].split("::")
                        })
                    }
                }, {
                    key: "isEmpty",
                    value: function(t) {
                        var e = Object.prototype.hasOwnProperty;
                        if (null == t) return !0;
                        if (t.length > 0) return !1;
                        if (0 === t.length) return !0;
                        for (var n in t)
                            if (e.call(t, n)) return !1;
                        return !0
                    }
                }, {
                    key: "checkTripLicense",
                    value: function() {
                        var t = this,
                            e = {
                                api: "mtop.trip.tripsm.triplicense.check",
                                v: "1.0",
                                type: "GET",
                                data: {
                                    xid: this.xid
                                }
                            },
                            n = function(e) {
                                var n = e;
                                if ("string" == typeof n) try {
                                    n = JSON.parse(e)
                                } catch (t) {}
                                if (n && !t.isEmpty(n.data)) {
                                    var r = n.data.models;
                                    if (r && ("true" == r.isVacationSeller || !0 === r.isVacationSeller)) {
                                        var o = t.state.items.slice();
                                        t.state.items.map(function(t) {
                                            return "iconCell" === t.type && "license" === t.id && t.licenses.push({
                                                icon: "//img.alicdn.com/tfs/TB1roxSSVXXXXXEXXXXXXXXXXXX-32-32.png",
                                                link: r.link
                                            }), t
                                        });
                                        t.setState({
                                            items: o
                                        })
                                    }
                                }
                            },
                            r = function(t) {};
                        this.pageUtils.Mtop.request(e, n, r)
                    }
                }, {
                    key: "parseShopData",
                    value: function(t) {
                        this.xid = t.xid;
                        var e = this.props.gdc.userId,
                            n = e,
                            r = [],
                            o = t.isMall,
                            i = t.nick,
                            a = t.wangwangLink,
                            l = t.wangwangIcon;
                        r.push({
                            type: "info",
                            title: "掌柜名",
                            content: i || "",
                            targetUrl: a,
                            rightIconUrl: l,
                            clickUTData: this.createUTClickData("AliWangWang")
                        });
                        var c = t.phone,
                            s = t.phoneIcon;
                        if (c && c.length > 0) {
                            var u = "tel:" + c;
                            r.push({
                                type: "info",
                                title: "服务电话",
                                content: c,
                                rightIconUrl: s,
                                targetUrl: u,
                                clickUTData: this.createUTClickData("TelPhone"),
                                targetType: "tel"
                            })
                        }
                        r.push(this.createSeparationData());
                        var p = t.city;
                        p && r.push({
                            type: "info",
                            title: "所在地",
                            content: p
                        });
                        var f = !1,
                            d = t.aptitude;
                        !o && d && (r.push({
                            type: "info",
                            title: "资质",
                            content: d,
                            rightIconUrl: "//img.alicdn.com/tps/TB1pt9bJVXXXXX6XVXXXXXXXXXX-32-32.png"
                        }), f = !0);
                        var h = t.licenseUrl,
                            g = ["//img.alicdn.com/tps/TB1kAR_JVXXXXblXVXXXXXXXXXX-32-32.png"];
                        if (h && h.length > 0) {
                            var m = [];
                            g.forEach(function(t) {
                                return m.push({
                                    icon: t,
                                    link: h
                                })
                            }), r.push({
                                id: "license",
                                type: "iconCell",
                                title: "企业资质",
                                action: "link",
                                licenses: m,
                                clickUTData: this.createUTClickData("Gszz")
                            }), f = !0
                        }
                        var v = t.industryLicenseUrl,
                            b = t.industryLicenseIcon;
                        if (b && b.length > 0) {
                            var w = b.map(function(t) {
                                return {
                                    icon: t,
                                    link: v
                                }
                            });
                            v && v.length > 0 && b && b.length > 0 && (r.push({
                                type: "iconCell",
                                title: "行业证照",
                                licenses: w,
                                action: "link"
                            }), f = !0)
                        }
                        if (f && r.push(this.createSeparationData()), this.pageUtils && this.pageUtils.aliEnv && this.pageUtils.aliEnv.isTB) {
                            var x = "//h5.m.taobao.com/weapp/view_page.htm?page=shop/card&userId=" + n;
                            r.push({
                                type: "info",
                                title: "店铺名片",
                                targetUrl: x,
                                action: "link",
                                clickUTData: this.createUTClickData("BarCode")
                            }, this.createSeparationData())
                        }
                        var k = t.starts;
                        k && r.push({
                            type: "info",
                            title: "开店时间",
                            content: y.formatDate(k)
                        }), this.setState({
                            items: r
                        })
                    }
                }, {
                    key: "createSeparationData",
                    value: function() {
                        return {}
                    }
                }, {
                    key: "render",
                    value: function() {
                        var t = this,
                            e = this.state,
                            n = (e.gdc, e.mds);
                        e.showDataStatus, e.showNoDataStatus, n.moduleData, this.state.data;
                        return (0, c.createElement)(u.default, {
                            style: v.default.wrapper,
                            "data-spmc": n.moduleName + "_" + n.widgetId
                        }, (0, c.createElement)(u.default, {
                            style: v.default.titleWrapper
                        }, (0, c.createElement)(f.default, {
                            style: v.default.title
                        }, "基础信息")), (0, c.createElement)(u.default, {
                            style: v.default.body
                        }, this.state.items.map(function(e, r) {
                            var o = "";
                            if ("info" == e.type) o = (0, c.createElement)(u.default, {
                                style: [v.default.flexRow, {
                                    alignItems: "center"
                                }]
                            }, e.rightIconUrl ? (0, c.createElement)(h.default, {
                                style: v.default.icon,
                                source: {
                                    uri: e.rightIconUrl
                                }
                            }) : null, e.content ? (0, c.createElement)(f.default, {
                                style: v.default.infoText
                            }, e.content) : null);
                            else {
                                if ("iconCell" != e.type) return (0, c.createElement)(u.default, null);
                                o = (0, c.createElement)(u.default, {
                                    style: v.default.flexRow
                                }, e.licenses.map(function(e, n) {
                                    return (0, c.createElement)(u.default, {
                                        onClick: function() {
                                            t.goTargetUrl(e.link, r + "-" + n)
                                        }
                                    }, (0, c.createElement)(h.default, {
                                        style: v.default.icon,
                                        source: {
                                            uri: e.icon
                                        }
                                    }))
                                }))
                            }
                            return (0, c.createElement)(w.default, {
                                title: e.title,
                                type: "normal",
                                action: e.action,
                                onClick: function() {
                                    e.targetUrl && t.goTargetUrl(e.targetUrl, r, e.targetType)
                                },
                                "data-spmd": n.moduleName + "_" + n.widgetId + "_" + r
                            }, o)
                        })))
                    }
                }]), e
            }(c.Component);
        e.default = x, t.exports = e.default
    }, function(t, e) {
        t.exports = n
    }, function(t, e) {
        t.exports = r
    }, function(t, e) {
        t.exports = o
    }, function(t, e) {
        t.exports = i
    }, function(t, e) {
        "use strict";
        Object.defineProperty(e, "__esModule", {
            value: !0
        });
        var n = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
            return typeof t
        } : function(t) {
            return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
        };
        e.formatDate = function(t, e) {
            if ("object" === (void 0 === t ? "undefined" : n(t))) return t;
            t = new Date(parseInt(t)), console.log(t), void 0 === e && (e = "yyyy-MM-dd hh:mm:ss");
            var r = {
                "M+": t.getMonth() + 1,
                "d+": t.getDate(),
                "h+": t.getHours(),
                "m+": t.getMinutes(),
                "s+": t.getSeconds(),
                "q+": Math.floor((t.getMonth() + 3) / 3),
                S: t.getMilliseconds()
            };
            /(y+)/.test(e) && (e = e.replace(RegExp.$1, ("" + t.getFullYear()).substr(4 - RegExp.$1.length)));
            for (var o in r) new RegExp("(" + o + ")").test(e) && (e = e.replace(RegExp.$1, 1 == RegExp.$1.length ? r[o] : ("00" + r[o]).substr(("" + r[o]).length)));
            return e
        }
    }, function(t, e) {
        var n = {
            defaultImage: {
                width: 750,
                height: 400
            },
            wrapper: {
                width: 750,
                justifyContent: "space-between",
                backgroundColor: "rgb(255,255,255)",
                marginBottom: 30
            },
            titleWrapper: {
                height: 80,
                paddingLeft: 24,
                paddingRight: 24,
                justifyContent: "center"
            },
            title: {
                color: "rgb(153,153,153)",
                fontSize: 32
            },
            flexRow: {
                flexDirection: "row"
            },
            infoText: {
                fontSize: 24,
                color: "rgb(74,74,74)"
            },
            icon: {
                width: 40,
                height: 40,
                marginRight: 25
            }
        };
        t.exports = n
    }, function(t, e, n) {
        "use strict";

        function r(t) {
            return t && t.__esModule ? t : {
                default: t
            }
        }

        function o(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function i(t, e) {
            if (!t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return !e || "object" != typeof e && "function" != typeof e ? t : e
        }

        function a(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function, not " + typeof e);
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    enumerable: !1,
                    writable: !0,
                    configurable: !0
                }
            }), e && (Object.setPrototypeOf ? Object.setPrototypeOf(t, e) : t.__proto__ = e)
        }
        Object.defineProperty(e, "__esModule", {
            value: !0
        });
        var l = function() {
                function t(t, e) {
                    for (var n = 0; n < e.length; n++) {
                        var r = e[n];
                        r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(t, r.key, r)
                    }
                }
                return function(e, n, r) {
                    return n && t(e.prototype, n), r && t(e, r), e
                }
            }(),
            c = n(1),
            s = n(2),
            u = r(s),
            p = n(3),
            f = r(p),
            d = n(4),
            h = r(d),
            g = n(8),
            y = (r(g), n(9)),
            m = r(y),
            v = function(t) {
                function e(t) {
                    o(this, e);
                    var n = i(this, (e.__proto__ || Object.getPrototypeOf(e)).call(this, t));
                    return n.onClick = function() {
                        n.props.onClick()
                    }, n
                }
                return a(e, t), l(e, [{
                    key: "render",
                    value: function() {
                        return (0, c.createElement)(u.default, {
                            style: m.default.cell,
                            onClick: this.onClick
                        }, (0, c.createElement)(u.default, {
                            style: m.default.titleWrapper
                        }, (0, c.createElement)(f.default, {
                            style: m.default.title,
                            numberOfLines: 1
                        }, this.props.title)), (0, c.createElement)(u.default, {
                            style: m.default.iconWrapper
                        }, this.props.children, "link" == this.props.action ? (0, c.createElement)(h.default, {
                            style: m.default.linkIcon,
                            source: {
                                uri: "//gtms03.alicdn.com/tps/i3/T12T6uFJxbXXXCWhje-36-36.png"
                            }
                        }) : null))
                    }
                }]), e
            }(c.Component);
        e.default = v, t.exports = e.default
    }, function(t, e) {
        t.exports = a
    }, function(t, e) {
        var n = {
            cell: {
                width: 750,
                height: 80,
                paddingLeft: 24,
                paddingRight: 24,
                flexDirection: "row"
            },
            titleWrapper: {
                flex: 1,
                height: 80,
                justifyContent: "center"
            },
            title: {
                width: 200,
                fontSize: 28,
                color: "rgb(51,51,51)",
                justifyContent: "center",
                textOverflow: "ellipsis",
                lines: 1
            },
            iconWrapper: {
                flex: 1,
                height: 80,
                flexDirection: "row",
                justifyContent: "flex-end",
                alignItems: "center"
            },
            linkIcon: {
                width: 32,
                height: 32
            }
        };
        t.exports = n
    }])
});

require(["taobaowpmod/shop_base_info/index.weex"], function () {
   // alert("load finish")
});