if(typeof define !== 'function'){
    var define = require('amdefine')(module);
}

'use strict';
define("taobaowpmod/shop_base_info/index.weex", ["rax", "rax-view", "rax-text", "rax-picture", "rax-touchable"], function(require, canCreateDiscussions, mixin) {
    try {
        var CreditCardList = require("rax");
    } catch (conv_reverse_sort) {
        if ("undefined" != typeof console) {
            console.log(conv_reverse_sort);
        }
    }
    try {
        var CreditCardList = require("rax-view");
    } catch (conv_reverse_sort) {
        if ("undefined" != typeof console) {
            console.log(conv_reverse_sort);
        }
    }
    try {
        var LightShader = require("rax-text");
    } catch (conv_reverse_sort) {
        if ("undefined" != typeof console) {
            console.log(conv_reverse_sort);
        }
    }
    try {
        var LightShader = require("rax-picture");
    } catch (conv_reverse_sort) {
        if ("undefined" != typeof console) {
            console.log(conv_reverse_sort);
        }
    }
    try {
        var CreditCardList = require("rax-touchable");
    } catch (conv_reverse_sort) {
        if ("undefined" != typeof console) {
            console.log(conv_reverse_sort);
        }
    }
    return mixin.exports = function(modules) {
        /**
         * @param {number} moduleId
         * @return {?}
         */
        function __webpack_require__(moduleId) {
            if (installedModules[moduleId]) {
                return installedModules[moduleId].exports;
            }
            var module = installedModules[moduleId] = {
                exports: {},
                id: moduleId,
                loaded: false
            };
            return modules[moduleId].call(module.exports, module, module.exports, __webpack_require__), module.loaded = true, module.exports;
        }
        var installedModules = {};
        return __webpack_require__.m = modules, __webpack_require__.c = installedModules, __webpack_require__.p = "", __webpack_require__(0);
    }([function(exports, e, __webpack_require__) {
        /**
         * @param {!Object} obj
         * @return {?}
         */
        function _interopRequireDefault(obj) {
            return obj && obj.__esModule ? obj : {
                default: obj
            };
        }
        /**
         * @param {!AudioNode} t
         * @param {!Function} e
         * @return {undefined}
         */
        function error(t, e) {
            if (!(t instanceof e)) {
                throw new TypeError("Cannot call a class as a function");
            }
        }
        /**
         * @param {string} fn
         * @param {string} t
         * @return {?}
         */
        function $(fn, t) {
            if (!fn) {
                throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            }
            return !t || "object" != typeof t && "function" != typeof t ? fn : t;
        }
        /**
         * @param {!Object} subClass
         * @param {!Object} superClass
         * @return {undefined}
         */
        function _inherits(subClass, superClass) {
            if ("function" != typeof superClass && null !== superClass) {
                throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
            }
            /** @type {!Object} */
            subClass.prototype = Object.create(superClass && superClass.prototype, {
                constructor: {
                    value: subClass,
                    enumerable: false,
                    writable: true,
                    configurable: true
                }
            });
            if (superClass) {
                if (Object.setPrototypeOf) {
                    Object.setPrototypeOf(subClass, superClass);
                } else {
                    /** @type {!Object} */
                    subClass.__proto__ = superClass;
                }
            }
        }
        Object.defineProperty(e, "__esModule", {
            value: true
        });
        var _createClass = function() {
            /**
             * @param {!Function} d
             * @param {string} props
             * @return {undefined}
             */
            function t(d, props) {
                /** @type {number} */
                var i = 0;
                for (; i < props.length; i++) {
                    var descriptor = props[i];
                    descriptor.enumerable = descriptor.enumerable || false;
                    /** @type {boolean} */
                    descriptor.configurable = true;
                    if ("value" in descriptor) {
                        /** @type {boolean} */
                        descriptor.writable = true;
                    }
                    Object.defineProperty(d, descriptor.key, descriptor);
                }
            }
            return function(p, n, a) {
                return n && t(p.prototype, n), a && t(p, a), p;
            };
        }();
        var _require = __webpack_require__(1);
        var _normalizeDataUri = __webpack_require__(2);
        var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
        var _UiIcon = __webpack_require__(3);
        var _UiIcon2 = _interopRequireDefault(_UiIcon);
        var _classlist = __webpack_require__(4);
        var _classlist2 = _interopRequireDefault(_classlist);
        var _helpers = __webpack_require__(5);
        var helpers = function(obj) {
            if (obj && obj.__esModule) {
                return obj;
            }
            var newObj = {};
            if (null != obj) {
                var key;
                for (key in obj) {
                    if (Object.prototype.hasOwnProperty.call(obj, key)) {
                        newObj[key] = obj[key];
                    }
                }
            }
            return newObj.default = obj, newObj;
        }(_helpers);
        var _prepareStyleProperties = __webpack_require__(6);
        var _this = _interopRequireDefault(_prepareStyleProperties);
        var _UiRippleInk = __webpack_require__(7);
        var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
        var newOrg = function(_EventEmitter) {
            /**
             * @param {?} attrs
             * @return {?}
             */
            function e(attrs) {
                error(this, e);
                var that = $(this, (e.__proto__ || Object.getPrototypeOf(e)).call(this, attrs));
                return that.state = {
                    showDataStatus: false,
                    showNoDataStatus: false
                }, that.updateShowData = function() {
                    var state = that.state;
                    var playerMask = state.gdc;
                    var self = state.mds;
                    var data = self.moduleData || {};
                    that.setState({
                        showDataStatus: data.ticket && Object.keys(data.ticket).length,
                        showNoDataStatus: !(1 != playerMask.preView && "true" != playerMask.preView || data.ticket && Object.keys(data.ticket).length)
                    });
                }, that.goTargetUrl = function(uri, method, protocol) {
                    var params = that.state.mds;
                    var where = {
                        url: uri,
                        protocol: protocol || "",
                        nid: method || 0,
                        widgetId: params.widgetId,
                        moduleName: params.moduleName
                    };
                    if (that.pageUtils.goTargetUrl) {
                        that.pageUtils.goTargetUrl(where);
                    }
                }, that.pageUtils = attrs.pageUtils, that.state = {
                    gdc: that.props.gdc || {},
                    mds: that.props.mds || {},
                    items: []
                }, that.xid = "", that;
            }
            return _inherits(e, _EventEmitter), _createClass(e, [{
                key: "createUTClickData",
                value: function(recB) {
                    return {
                        control: "Button-" + recB,
                        params: {
                            shop_id: this.shopId,
                            seller_id: this.sellerId
                        }
                    };
                }
            }, {
                key: "componentWillMount",
                value: function() {
                    var payload = this.state.mds;
                    var readyPorts = payload.moduleData || {};
                    if (payload.widgetId && Object.keys(readyPorts).length > 0) {
                        this.updateShowData();
                    }
                }
            }, {
                key: "shouldComponentUpdate",
                value: function(saveEvenIfSeemsUnchanged, optionalUrl) {
                    return !!this.shallowDiffers(this.props, saveEvenIfSeemsUnchanged) || !!this.shallowDiffers(this.state, optionalUrl);
                }
            }, {
                key: "shallowDiffers",
                value: function(f, e) {
                    var i;
                    for (i in f) {
                        if (!(i in e)) {
                            return true;
                        }
                    }
                    var j;
                    for (j in e) {
                        if (f[j] !== e[j]) {
                            return true;
                        }
                    }
                    return false;
                }
            }, {
                key: "componentDidMount",
                value: function() {
                    this.requestData();
                }
            }, {
                key: "requestData",
                value: function() {
                    var portalsData = this;
                    var result = this.props.gdc;
                    var userId = result.userId;
                    var courseSections = result.shopId;
                    var maindata3 = {
                        sellerId: userId,
                        shopId: courseSections
                    };
                    this.pageUtils.Mtop.request({
                        api: "mtop.taobao.shop.impression.intro.get",
                        v: "1.0",
                        type: "GET",
                        secType: 1,
                        data: maindata3,
                        ecode: 0,
                        timeout: 3e3
                    }, function(result) {
                        if ("SUCCESS" === result.ret[0].split("::")[0]) {
                            portalsData.parseShopData(result.data.result);
                            portalsData.checkTripLicense();
                        }
                    }, function(prop) {
                        prop.ret[0].split("::");
                    });
                }
            }, {
                key: "isEmpty",
                value: function(b) {
                    /** @type {function(this:Object, *): boolean} */
                    var hasOwnProperty = Object.prototype.hasOwnProperty;
                    if (null == b) {
                        return true;
                    }
                    if (b.length > 0) {
                        return false;
                    }
                    if (0 === b.length) {
                        return true;
                    }
                    var prop;
                    for (prop in b) {
                        if (hasOwnProperty.call(b, prop)) {
                            return false;
                        }
                    }
                    return true;
                }
            }, {
                key: "checkTripLicense",
                value: function() {
                    var that = this;
                    var options = {
                        api: "mtop.trip.tripsm.triplicense.check",
                        v: "1.0",
                        type: "GET",
                        data: {
                            xid: this.xid
                        }
                    };
                    /**
                     * @param {string} data
                     * @return {undefined}
                     */
                    var init = function(data) {
                        /** @type {string} */
                        var message = data;
                        if ("string" == typeof message) {
                            try {
                                /** @type {*} */
                                message = JSON.parse(data);
                            } catch (t) {}
                        }
                        if (message && !that.isEmpty(message.data)) {
                            var data = message.data.models;
                            if (data && ("true" == data.isVacationSeller || true === data.isVacationSeller)) {
                                var listBoxItems = that.state.items.slice();
                                that.state.items.map(function(res) {
                                    return "iconCell" === res.type && "license" === res.id && res.licenses.push({
                                        icon: "//img.alicdn.com/tfs/TB1roxSSVXXXXXEXXXXXXXXXXXX-32-32.png",
                                        link: data.link
                                    }), res;
                                });
                                that.setState({
                                    items: listBoxItems
                                });
                            }
                        }
                    };
                    /**
                     * @param {?} textPositions
                     * @return {undefined}
                     */
                    var check = function(textPositions) {};
                    this.pageUtils.Mtop.request(options, init, check);
                }
            }, {
                key: "parseShopData",
                value: function(options) {
                    this.xid = options.xid;
                    var userId = this.props.gdc.userId;
                    var urlPage = userId;
                    /** @type {!Array} */
                    var result = [];
                    var f = options.isMall;
                    var content = options.nick;
                    var target = options.wangwangLink;
                    var readOnlyFn = options.wangwangIcon;
                    result.push({
                        type: "info",
                        title: "\u638c\u67dc\u540d",
                        content: content || "",
                        targetUrl: target,
                        rightIconUrl: readOnlyFn,
                        clickUTData: this.createUTClickData("AliWangWang")
                    });
                    var name = options.phone;
                    var phoneIcon = options.phoneIcon;
                    if (name && name.length > 0) {
                        /** @type {string} */
                        var targetUrl = "tel:" + name;
                        result.push({
                            type: "info",
                            title: "\u670d\u52a1\u7535\u8bdd",
                            content: name,
                            rightIconUrl: phoneIcon,
                            targetUrl: targetUrl,
                            clickUTData: this.createUTClickData("TelPhone"),
                            targetType: "tel"
                        });
                    }
                    result.push(this.createSeparationData());
                    var location = options.city;
                    if (location) {
                        result.push({
                            type: "info",
                            title: "\u6240\u5728\u5730",
                            content: location
                        });
                    }
                    /** @type {boolean} */
                    var c = false;
                    var d = options.aptitude;
                    if (!f && d) {
                        result.push({
                            type: "info",
                            title: "\u8d44\u8d28",
                            content: d,
                            rightIconUrl: "//img.alicdn.com/tps/TB1pt9bJVXXXXX6XVXXXXXXXXXX-32-32.png"
                        });
                        /** @type {boolean} */
                        c = true;
                    }
                    var dataH = options.licenseUrl;
                    /** @type {!Array} */
                    var pipelets = ["//img.alicdn.com/tps/TB1kAR_JVXXXXblXVXXXXXXXXXX-32-32.png"];
                    if (dataH && dataH.length > 0) {
                        /** @type {!Array} */
                        var items = [];
                        pipelets.forEach(function(icoURL) {
                            return items.push({
                                icon: icoURL,
                                link: dataH
                            });
                        });
                        result.push({
                            id: "license",
                            type: "iconCell",
                            title: "\u4f01\u4e1a\u8d44\u8d28",
                            action: "link",
                            licenses: items,
                            clickUTData: this.createUTClickData("Gszz")
                        });
                        /** @type {boolean} */
                        c = true;
                    }
                    var url = options.industryLicenseUrl;
                    var col = options.industryLicenseIcon;
                    if (col && col.length > 0) {
                        var licenses = col.map(function(icoURL) {
                            return {
                                icon: icoURL,
                                link: url
                            };
                        });
                        if (url && url.length > 0 && col && col.length > 0) {
                            result.push({
                                type: "iconCell",
                                title: "\u884c\u4e1a\u8bc1\u7167",
                                licenses: licenses,
                                action: "link"
                            });
                            /** @type {boolean} */
                            c = true;
                        }
                    }
                    if (c && result.push(this.createSeparationData()), this.pageUtils && this.pageUtils.aliEnv && this.pageUtils.aliEnv.isTB) {
                        /** @type {string} */
                        var targetUrl = "//h5.m.taobao.com/weapp/view_page.htm?page=shop/card&userId=" + urlPage;
                        result.push({
                            type: "info",
                            title: "\u5e97\u94fa\u540d\u7247",
                            targetUrl: targetUrl,
                            action: "link",
                            clickUTData: this.createUTClickData("BarCode")
                        }, this.createSeparationData());
                    }
                    var value = options.starts;
                    if (value) {
                        result.push({
                            type: "info",
                            title: "\u5f00\u5e97\u65f6\u95f4",
                            content: helpers.formatDate(value)
                        });
                    }
                    this.setState({
                        items: result
                    });
                }
            }, {
                key: "createSeparationData",
                value: function() {
                    return {};
                }
            }, {
                key: "render",
                value: function() {
                    var page = this;
                    var thisState = this.state;
                    var self = (thisState.gdc, thisState.mds);
                    thisState.showDataStatus;
                    thisState.showNoDataStatus;
                    self.moduleData;
                    this.state.data;
                    return (0, _require.createElement)(_normalizeDataUri2.default, {
                        style: _this.default.wrapper,
                        "data-spmc": self.moduleName + "_" + self.widgetId
                    }, (0, _require.createElement)(_normalizeDataUri2.default, {
                        style: _this.default.titleWrapper
                    }, (0, _require.createElement)(_UiIcon2.default, {
                        style: _this.default.title
                    }, "\u57fa\u7840\u4fe1\u606f")), (0, _require.createElement)(_normalizeDataUri2.default, {
                        style: _this.default.body
                    }, this.state.items.map(function(data, top) {
                        /** @type {string} */
                        var addedPathkey = "";
                        if ("info" == data.type) {
                            addedPathkey = (0, _require.createElement)(_normalizeDataUri2.default, {
                                style: [_this.default.flexRow, {
                                    alignItems: "center"
                                }]
                            }, data.rightIconUrl ? (0, _require.createElement)(_classlist2.default, {
                                style: _this.default.icon,
                                source: {
                                    uri: data.rightIconUrl
                                }
                            }) : null, data.content ? (0, _require.createElement)(_UiIcon2.default, {
                                style: _this.default.infoText
                            }, data.content) : null);
                        } else {
                            if ("iconCell" != data.type) {
                                return (0, _require.createElement)(_normalizeDataUri2.default, null);
                            }
                            addedPathkey = (0, _require.createElement)(_normalizeDataUri2.default, {
                                style: _this.default.flexRow
                            }, data.licenses.map(function(options, inc) {
                                return (0, _require.createElement)(_normalizeDataUri2.default, {
                                    onClick: function() {
                                        page.goTargetUrl(options.link, top + "-" + inc);
                                    }
                                }, (0, _require.createElement)(_classlist2.default, {
                                    style: _this.default.icon,
                                    source: {
                                        uri: options.icon
                                    }
                                }));
                            }));
                        }
                        return (0, _require.createElement)(_UiRippleInk2.default, {
                            title: data.title,
                            type: "normal",
                            action: data.action,
                            onClick: function() {
                                if (data.targetUrl) {
                                    page.goTargetUrl(data.targetUrl, top, data.targetType);
                                }
                            },
                            "data-spmd": self.moduleName + "_" + self.widgetId + "_" + top
                        }, addedPathkey);
                    })));
                }
            }]), e;
        }(_require.Component);
        e.default = newOrg;
        exports.exports = e.default;
    }, function(module, canCreateDiscussions) {
        module.exports = CreditCardList;
    }, function(module, canCreateDiscussions) {
        module.exports = CreditCardList;
    }, function(module, canCreateDiscussions) {
        module.exports = LightShader;
    }, function(module, canCreateDiscussions) {
        module.exports = LightShader;
    }, function(canCreateDiscussions, d) {
        Object.defineProperty(d, "__esModule", {
            value: true
        });
        /** @type {function(number): ?} */
        var validateParameterPresence = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(p_or_v) {
            return typeof p_or_v;
        } : function(obj) {
            return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
        };
        /**
         * @param {number} value
         * @param {?} format
         * @return {?}
         */
        d.formatDate = function(value, format) {
            if ("object" === (void 0 === value ? "undefined" : validateParameterPresence(value))) {
                return value;
            }
            /** @type {!Date} */
            value = new Date(parseInt(value));
            console.log(value);
            if (void 0 === format) {
                /** @type {string} */
                format = "yyyy-MM-dd hh:mm:ss";
            }
            var obj = {
                "M+": value.getMonth() + 1,
                "d+": value.getDate(),
                "h+": value.getHours(),
                "m+": value.getMinutes(),
                "s+": value.getSeconds(),
                "q+": Math.floor((value.getMonth() + 3) / 3),
                S: value.getMilliseconds()
            };
            if (/(y+)/.test(format)) {
                format = format.replace(RegExp.$1, ("" + value.getFullYear()).substr(4 - RegExp.$1.length));
            }
            var i;
            for (i in obj) {
                if ((new RegExp("(" + i + ")")).test(format)) {
                    format = format.replace(RegExp.$1, 1 == RegExp.$1.length ? obj[i] : ("00" + obj[i]).substr(("" + obj[i]).length));
                }
            }
            return format;
        };
    }, function(module, canCreateDiscussions) {
        var defaults = {
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
        module.exports = defaults;
    }, function(exports, e, __webpack_require__) {
        /**
         * @param {!Object} obj
         * @return {?}
         */
        function _interopRequireDefault(obj) {
            return obj && obj.__esModule ? obj : {
                default: obj
            };
        }
        /**
         * @param {!AudioNode} instance
         * @param {!Function} Constructor
         * @return {undefined}
         */
        function _classCallCheck(instance, Constructor) {
            if (!(instance instanceof Constructor)) {
                throw new TypeError("Cannot call a class as a function");
            }
        }
        /**
         * @param {string} self
         * @param {string} call
         * @return {?}
         */
        function _possibleConstructorReturn(self, call) {
            if (!self) {
                throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            }
            return !call || "object" != typeof call && "function" != typeof call ? self : call;
        }
        /**
         * @param {!Object} subClass
         * @param {!Object} superClass
         * @return {undefined}
         */
        function _inherits(subClass, superClass) {
            if ("function" != typeof superClass && null !== superClass) {
                throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
            }
            /** @type {!Object} */
            subClass.prototype = Object.create(superClass && superClass.prototype, {
                constructor: {
                    value: subClass,
                    enumerable: false,
                    writable: true,
                    configurable: true
                }
            });
            if (superClass) {
                if (Object.setPrototypeOf) {
                    Object.setPrototypeOf(subClass, superClass);
                } else {
                    /** @type {!Object} */
                    subClass.__proto__ = superClass;
                }
            }
        }
        Object.defineProperty(e, "__esModule", {
            value: true
        });
        var _createClass = function() {
            /**
             * @param {!Function} d
             * @param {string} props
             * @return {undefined}
             */
            function t(d, props) {
                /** @type {number} */
                var i = 0;
                for (; i < props.length; i++) {
                    var descriptor = props[i];
                    descriptor.enumerable = descriptor.enumerable || false;
                    /** @type {boolean} */
                    descriptor.configurable = true;
                    if ("value" in descriptor) {
                        /** @type {boolean} */
                        descriptor.writable = true;
                    }
                    Object.defineProperty(d, descriptor.key, descriptor);
                }
            }
            return function(p, n, a) {
                return n && t(p.prototype, n), a && t(p, a), p;
            };
        }();
        var _require = __webpack_require__(1);
        var _normalizeDataUri = __webpack_require__(2);
        var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
        var _classlist = __webpack_require__(3);
        var _classlist2 = _interopRequireDefault(_classlist);
        var _UiRippleInk = __webpack_require__(4);
        var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
        var _UiIcon = __webpack_require__(8);
        var _prepareStyleProperties = (_interopRequireDefault(_UiIcon), __webpack_require__(9));
        var self = _interopRequireDefault(_prepareStyleProperties);
        var newOrg = function(_EventEmitter) {
            /**
             * @param {?} data
             * @return {?}
             */
            function Agent(data) {
                _classCallCheck(this, Agent);
                var _this = _possibleConstructorReturn(this, (Agent.__proto__ || Object.getPrototypeOf(Agent)).call(this, data));
                return _this.onClick = function() {
                    _this.props.onClick();
                }, _this;
            }
            return _inherits(Agent, _EventEmitter), _createClass(Agent, [{
                key: "render",
                value: function() {
                    return (0, _require.createElement)(_normalizeDataUri2.default, {
                        style: self.default.cell,
                        onClick: this.onClick
                    }, (0, _require.createElement)(_normalizeDataUri2.default, {
                        style: self.default.titleWrapper
                    }, (0, _require.createElement)(_classlist2.default, {
                        style: self.default.title,
                        numberOfLines: 1
                    }, this.props.title)), (0, _require.createElement)(_normalizeDataUri2.default, {
                        style: self.default.iconWrapper
                    }, this.props.children, "link" == this.props.action ? (0, _require.createElement)(_UiRippleInk2.default, {
                        style: self.default.linkIcon,
                        source: {
                            uri: "//gtms03.alicdn.com/tps/i3/T12T6uFJxbXXXCWhje-36-36.png"
                        }
                    }) : null));
                }
            }]), Agent;
        }(_require.Component);
        e.default = newOrg;
        exports.exports = e.default;
    }, function(module, canCreateDiscussions) {
        module.exports = CreditCardList;
    }, function(blob, canCreateDiscussions) {
        var data = {
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
        blob.exports = data;
    }]);
});

// 调用模块
require([], function (mod2){

    var mod = mod2();
    mod._inherits();

    console.log(mod.show());
});
