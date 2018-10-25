'use strict';
(window.webpackJsonp = window.webpackJsonp || []).push([
    [3],
    [, , , , , function(canCreateDiscussions, isSlidingUp, i) {}, function(canCreateDiscussions, exports, i) {
        Object.defineProperty(exports, "__esModule", {
            value: true
        });
        exports.default = {
            data: function() {
                return {};
            }
        };
    }, function(canCreateDiscussions, message, key) {
        key.r(message);
        var value = key(6);
        var data = key.n(value);
        var k;
        for (k in value) {
            if ("default" !== k) {
                (function(c) {
                    key.d(message, c, function() {
                        return value[c];
                    });
                })(k);
            }
        }
        message.default = data.a;
    }, function(canCreateDiscussions, isSlidingUp, i) {}, function(canCreateDiscussions, exports, floor) {
        Object.defineProperty(exports, "__esModule", {
            value: true
        });
        var startYNew = floor(18);
        exports.default = {
            props: {
                title: {
                    type: String,
                    default: ""
                },
                forceShow: {
                    type: Boolean,
                    default: true
                }
            },
            data: function() {
                var value = this.$props.forceShow;
                return value || (value = !(0, startYNew.isMFWIndepTravel)()), {
                    visible: value
                };
            },
            methods: {
                onBack: function() {
                    this.$emit("onback");
                }
            }
        };
    }, function(canCreateDiscussions, message, key) {
        key.r(message);
        var value = key(9);
        var data = key.n(value);
        var k;
        for (k in value) {
            if ("default" !== k) {
                (function(c) {
                    key.d(message, c, function() {
                        return value[c];
                    });
                })(k);
            }
        }
        message.default = data.a;
    }, , , function(canCreateDiscussions, __webpack_exports__, __webpack_require__) {
        /**
         * @return {?}
         */
        var render = function() {
            var _vm = this;
            var _h = _vm.$createElement;
            var _c = _vm._self._c || _h;
            return _c("div", {
                staticClass: "app-with-titlebar",
                class: {
                    fringeHack: _vm.visible
                }
            }, [_vm.visible ? _c("div", {
                staticClass: "app-title-bar-head"
            }, [_c("div", {
                staticClass: "inner"
            }, [_c("span", {
                staticClass: "app-title-bar-title"
            }, [_vm._v(_vm._s(_vm.title))]), _c("div", {
                staticClass: "btn-back",
                on: {
                    click: _vm.onBack
                }
            })])]) : _vm._e(), _c("div", {
                staticClass: "app-title-bar-body"
            }, [_c("div", {
                staticClass: "app-title-bar-body-inner"
            }, [_vm._t("default")], 2)]), _vm._t("dialog")], 2);
        };
        /** @type {!Array} */
        var n = [];
        /** @type {boolean} */
        render._withStripped = true;
        __webpack_require__.d(__webpack_exports__, "a", function() {
            return render;
        });
        __webpack_require__.d(__webpack_exports__, "b", function() {
            return n;
        });
    }, function(canCreateDiscussions, __webpack_exports__, __webpack_require__) {
        /**
         * @return {?}
         */
        var render = function() {
            var t = this.$createElement;
            this._self._c;
            return this._m(0);
        };
        /** @type {!Array} */
        var n = [function() {
            var _h = this.$createElement;
            var _c = this._self._c || _h;
            return _c("div", {
                staticClass: "mfwui-loading"
            }, [_c("div", {
                staticClass: "mfwui-loading-icon"
            })]);
        }];
        /** @type {boolean} */
        render._withStripped = true;
        __webpack_require__.d(__webpack_exports__, "a", function() {
            return render;
        });
        __webpack_require__.d(__webpack_exports__, "b", function() {
            return n;
        });
    }, , , , function(canCreateDiscussions, $scope, aggFn) {
        /**
         * @param {string} target
         * @return {?}
         */
        function text(target) {
            var config = window.MFWAPP;
            return config && config.sdk && config.sdk.has(target);
        }
        /**
         * @param {string} state
         * @return {undefined}
         */
        function toggle(state) {
            if (text("webview.setNavigationBarDisplay")) {
                window.MFWAPP.webview.setNavigationBarDisplay({
                    display: "hide"
                });
            }
        }
        /**
         * @param {!Object} t
         * @return {undefined}
         */
        function callback(t) {
            if (text("webview.setTitle")) {
                window.MFWAPP.webview.setTitle({
                    title: t
                });
            } else {
                /** @type {!Object} */
                document.title = t;
            }
        }
        Object.defineProperty($scope, "__esModule", {
            value: true
        });
        /** @type {function(string): ?} */
        $scope.support = text;
        /**
         * @return {?}
         */
        $scope.isMFWIndepTravel = function() {
            return window.MFWAPP && (window.MFWAPP.sdk.isMFWIndepTravel || window.MFWAPP.sdk.isMFWAPP);
        };
        /**
         * @param {string} theURL
         * @return {undefined}
         */
        $scope.openNewPage = function(theURL) {
            if (text("webview.openNewPage")) {
                window.MFWAPP.webview.openNewPage({
                    url: theURL
                });
            } else {
                /** @type {string} */
                window.location.href = theURL;
            }
        };
        /**
         * @return {undefined}
         */
        $scope.disableBounces = function() {
            if (text("webview.enableBounces")) {
                window.MFWAPP.webview.enableBounces({
                    enable: 0
                });
            }
        };
        /**
         * @return {undefined}
         */
        $scope.enableBounces = function() {
            if (text("webview.enableBounces")) {
                window.MFWAPP.webview.enableBounces({
                    enable: 1
                });
            }
        };
        /**
         * @return {undefined}
         */
        $scope.hideNavigationBar = function() {
            toggle("hide");
        };
        /**
         * @return {undefined}
         */
        $scope.showNavigationBar = function() {
            toggle("show");
        };
        /** @type {function(string): undefined} */
        $scope.setNavigationBarDisplay = toggle;
        /**
         * @return {undefined}
         */
        $scope.closeWebview = function() {
            if (text("webview.close")) {
                window.MFWAPP.webview.close();
            }
        };
        /**
         * @return {undefined}
         */
        $scope.hideShareButtonInNavigationBar = function() {
            if (text("share.hideShareButtonInNavigationBar")) {
                window.MFWAPP.share.hideShareButtonInNavigationBar({
                    hide: 1
                });
            }
        };
        /**
         * @return {undefined}
         */
        $scope.hideMoreButtonInNavigationBar = function() {
            if (text("webview.hideMoreButtonInNavigationBar")) {
                window.MFWAPP.webview.hideMoreButtonInNavigationBar({
                    hide: 0
                });
            }
        };
        /** @type {function(!Object): undefined} */
        $scope.setTitle = callback;
        /**
         * @param {!Object} title
         * @return {undefined}
         */
        $scope.setSubTitle = function(title) {
            if (text("webview.setSubTitle")) {
                window.MFWAPP.webview.setSubTitle({
                    title: title
                });
            }
        };
        /**
         * @param {?} isBgroundImg
         * @return {undefined}
         */
        $scope.setNavigationBarStyle = function(isBgroundImg) {
            if (text("webview.setNavigationBarStyle")) {
                window.MFWAPP.webview.setNavigationBarStyle(isBgroundImg);
            }
        };
        /**
         * @return {undefined}
         */
        $scope.setShouldLeavePageHooker = function() {
            var t = !(arguments.length > 0 && void 0 !== arguments[0]) || arguments[0];
            arguments[1];
            if (text("webview.setShouldLeavePageHooker")) {
                window.MFWAPP.webview.setShouldLeavePageHooker({
                    hooker: function f(i) {
                        return f && f(i), {
                            should: t ? 1 : 0
                        };
                    }
                });
            }
        };
        /**
         * @return {undefined}
         */
        $scope.listCalendar = function() {
            var header = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
            var type = header.departDate;
            var mode = void 0 === type ? "" : type;
            var key = header.departCode;
            var url = void 0 === key ? "" : key;
            var val = header.destCode;
            var json = void 0 === val ? "" : val;
            var loadPage = arguments[1];
            var value = arguments[2];
            if (text("flight.pickAirTicketDate")) {
                window.MFWAPP.flight.pickAirTicketDate({
                    begin: mode,
                    trip_type: "oneWay",
                    depart_code: url,
                    dest_code: json,
                    onSelect: function(elem) {
                        if ((0, v.isFunction)(loadPage)) {
                            loadPage(elem);
                        }
                    },
                    onCancel: function() {
                        if ((0, v.isFunction)(value)) {
                            value();
                        }
                    }
                });
            }
        };
        /**
         * @return {undefined}
         */
        $scope.showCalendarPicker = function() {
            var seg = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
            var type = seg.departDate;
            var mode = void 0 === type ? "" : type;
            var toggleAnimationClass = (seg.departCode, seg.destCode, arguments[1]);
            var value = arguments[2];
            if (text("sales.showCalendarPicker")) {
                window.MFWAPP.sales.showCalendarPicker({
                    startDate: mode,
                    businessId: "flight",
                    businessExt: '{"departCode":"BJS","destCode":"NKG"}',
                    onSelect: function(rightToLeft) {
                        if ((0, v.isFunction)(toggleAnimationClass)) {
                            toggleAnimationClass(rightToLeft);
                        }
                    },
                    onCancel: function() {
                        if ((0, v.isFunction)(value)) {
                            value();
                        }
                    }
                });
            }
        };
        /**
         * @param {string} loginUrl
         * @return {undefined}
         */
        $scope.navigateToNewPage = function(loginUrl) {
            /** @type {number} */
            document.body.style.opacity = 0;
            callback("");
            setTimeout(function() {
                /** @type {string} */
                location.href = loginUrl;
            }, 20);
        };
        /**
         * @return {undefined}
         */
        $scope.historyBack = function() {
            /** @type {number} */
            document.body.style.opacity = 0;
            callback("");
            setTimeout(function() {
                history.back();
            }, 20);
        };
        var v = aggFn(11);
    }, function(data, canCreateDiscussions) {
        data.exports = window.moment;
    }, , , , , , , , , , , function(module, canCreateDiscussions) {
        module.exports = window.Vue;
    }, function(canCreateDiscussions, d, saveNotifs) {
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
         * @param {undefined} event
         * @return {?}
         */
        function s(event) {
            return animationConfigs[event];
        }
        Object.defineProperty(d, "__esModule", {
            value: true
        });
        var _deepAssign2 = _interopRequireDefault(saveNotifs(97));
        /** @type {function(undefined): ?} */
        d.toChineseWeekDay = s;
        /**
         * @param {?} num
         * @return {?}
         */
        d.getChineseWeekDay = function(num) {
            if (!num) {
                return "";
            }
            return "\u5468" + s((0, _noframeworkWaypoints2.default)(num).locale("zh-cn").weekday());
        };
        /**
         * @param {number} resumeTime
         * @return {?}
         */
        d.toHourMinute = function(resumeTime) {
            return Math.floor(resumeTime / 60) + "\u5c0f\u65f6" + resumeTime % 60 + "\u5206";
        };
        /**
         * @param {number} t
         * @return {?}
         */
        d.toShortDate = function(t) {
            return t ? t.substr(5) : "";
        };
        /**
         * @param {?} dateIn
         * @return {?}
         */
        d.dateFormat = function(dateIn) {
            /** @type {!Date} */
            var dat = new Date(dateIn);
            /** @type {number} */
            var parentDir = dat.getFullYear();
            /** @type {(number|string)} */
            var file = dat.getMonth() + 1 < 10 ? "0" + (dat.getMonth() + 1) : dat.getMonth() + 1;
            /** @type {(number|string)} */
            var _transactionName = dat.getDate() < 10 ? "0" + dat.getDate() : dat.getDate();
            return parentDir + "-" + file + "-" + _transactionName;
        };
        /**
         * @param {string} text
         * @return {?}
         */
        d.setTime = function(text) {
            var regJsonFormat = text.split(":");
            var props = (0, _deepAssign2.default)(regJsonFormat, 2);
            var x = props[0];
            var increment = props[1];
            return (2 === x.length || 2 === increment.length) && (0, _noframeworkWaypoints2.default)({
                hour: x,
                minute: increment
            });
        };
        /**
         * @param {string} patternStartsWith
         * @return {?}
         */
        d.toMonth = function(patternStartsWith) {
            return patternStartsWith && patternStartsWith.substr(0, 2) + "\u6708" + patternStartsWith.substr(3) + "\u65e5";
        };
        /**
         * @param {?} start
         * @param {?} end
         * @return {?}
         */
        d.diffDays = function(start, end) {
            if (!start || !end) {
                return 0;
            }
            return (0, _noframeworkWaypoints2.default)(end).diff((0, _noframeworkWaypoints2.default)(start), "days");
        };
        /**
         * @param {?} _newCharWidth
         * @param {?} _newCharHeight
         * @return {?}
         */
        d.diffMinutes = function(_newCharWidth, _newCharHeight) {
            if (!_newCharWidth || !_newCharHeight) {
                return 0;
            }
            return (0, _noframeworkWaypoints2.default)(_newCharHeight).diff((0, _noframeworkWaypoints2.default)(_newCharWidth), "minutes");
        };
        var _noframeworkWaypoints2 = _interopRequireDefault(saveNotifs(19));
        /** @type {!Array} */
        var animationConfigs = ["\u65e5", "\u4e00", "\u4e8c", "\u4e09", "\u56db", "\u4e94", "\u516d"];
    }, , , , , , function(canCreateDiscussions, isSlidingUp, __webpack_require__) {
        var __WEBPACK_IMPORTED_MODULE_20_date_fns_min__ = __webpack_require__(5);
        __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_20_date_fns_min__).a;
    }, function(canCreateDiscussions, context, $) {
        $.r(context);
        var tParentMatrix = $(14);
        var a = $(7);
        var k;
        for (k in a) {
            if ("default" !== k) {
                (function(m) {
                    $.d(context, m, function() {
                        return a[m];
                    });
                })(k);
            }
        }
        $(37);
        var self = $(0);
        var module = Object(self.a)(a.default, tParentMatrix.a, tParentMatrix.b, false, null, null, null);
        /** @type {string} */
        module.options.__file = "src/common/components/loading.vue";
        context.default = module.exports;
    }, , function(canCreateDiscussions, isSlidingUp, __webpack_require__) {
        var __WEBPACK_IMPORTED_MODULE_20_date_fns_min__ = __webpack_require__(8);
        __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_20_date_fns_min__).a;
    }, function(canCreateDiscussions, context, $) {
        $.r(context);
        var tParentMatrix = $(13);
        var a = $(10);
        var k;
        for (k in a) {
            if ("default" !== k) {
                (function(m) {
                    $.d(context, m, function() {
                        return a[m];
                    });
                })(k);
            }
        }
        $(40);
        var self = $(0);
        var module = Object(self.a)(a.default, tParentMatrix.a, tParentMatrix.b, false, null, null, null);
        /** @type {string} */
        module.options.__file = "src/common/components/titlebar.vue";
        context.default = module.exports;
    }, function(canCreateDiscussions, BeautifulProperties, saveNotifs) {
        /**
         * @param {!Object} obj
         * @return {?}
         */
        function _interopRequireDefault(obj) {
            return obj && obj.__esModule ? obj : {
                default: obj
            };
        }
        Object.defineProperty(BeautifulProperties, "__esModule", {
            value: true
        });
        /**
         * @param {!Object} Vue
         * @return {undefined}
         */
        BeautifulProperties.installVue = function(Vue) {
            Vue.component("mfwui-title-bar", _VuetablePagination2.default);
            Vue.component("mfwui-dialog", _VuetablePaginationDropdown2.default);
        };
        var _VuetablePagination2 = _interopRequireDefault(saveNotifs(41));
        var _VuetablePaginationDropdown2 = _interopRequireDefault(saveNotifs(38));
    }, , , , , , , , , function(canCreateDiscussions, e, i) {
        Object.defineProperty(e, "__esModule", {
            value: true
        });
        var undefined = localStorage.getItem("trans_flight_chn_dev");
        /** @type {boolean} */
        var nullTerminated = "q" === undefined;
        /** @type {boolean} */
        var isDev = "d" === undefined;
        /** @type {boolean} */
        var isPre = "p" === undefined;
        var newOrg = {
            AJAX_BASEURL: "https://" + (nullTerminated ? "qa-fwl-traffic.mfwdev.com" : isDev ? "dev-fwl-traffic.mfwdev.com" : isPre ? "sim-fwl-traffic.mfwdev.com" : "searchwl-traffic.mafengwo.cn"),
            AJAX_BASEURL_PHP: "",
            isQa: nullTerminated,
            isDev: isDev,
            isPre: isPre
        };
        e.default = newOrg;
    }, function(canCreateDiscussions, e, require) {
        Object.defineProperty(e, "__esModule", {
            value: true
        });
        /**
         * @param {?} url
         * @return {?}
         */
        e.get = function(url) {
            var nominatimQuery = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
            return Request.get(url, {
                params: nominatimQuery
            });
        };
        /**
         * @param {?} url
         * @return {?}
         */
        e.post = function(url) {
            var params = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
            var headers = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {};
            return Request.post(url, params, headers);
        };
        var Request = require(90);
        /** @type {boolean} */
        Request.defaults.withCredentials = true;
    }, , , , , , , , , , , , , function(canCreateDiscussions, isSlidingUp, i) {}, function(canCreateDiscussions, isSlidingUp, i) {}, function(canCreateDiscussions, exports, i) {
        Object.defineProperty(exports, "__esModule", {
            value: true
        });
        exports.default = {
            props: {
                title: {
                    type: String,
                    default: ""
                }
            },
            methods: {
                onBack: function() {
                    this.$emit("onback");
                }
            }
        };
    }, function(canCreateDiscussions, message, key) {
        key.r(message);
        var value = key(67);
        var data = key.n(value);
        var k;
        for (k in value) {
            if ("default" !== k) {
                (function(c) {
                    key.d(message, c, function() {
                        return value[c];
                    });
                })(k);
            }
        }
        message.default = data.a;
    }, function(canCreateDiscussions, isSlidingUp, i) {}, function(canCreateDiscussions, exports, floor) {
        /**
         * @param {!Object} obj
         * @return {?}
         */
        function _interopRequireDefault(obj) {
            return obj && obj.__esModule ? obj : {
                default: obj
            };
        }
        Object.defineProperty(exports, "__esModule", {
            value: true
        });
        var _deepAssign2 = _interopRequireDefault(floor(32));
        var _noframeworkWaypoints2 = _interopRequireDefault(floor(50));
        var _custom2 = _interopRequireDefault(floor(29));
        var startYNew = floor(27);
        exports.default = {
            props: {
                startAirPortList: {
                    type: Array,
                    default: function() {
                        return [];
                    }
                },
                arrAirPortList: {
                    type: Array,
                    default: function() {
                        return [];
                    }
                },
                airlineCompanyList: {
                    type: Array,
                    default: function() {
                        return [];
                    }
                }
            },
            components: (0, _custom2.default)({}, (0, startYNew.mapComponents)(startYNew.BetterScroller)),
            data: function() {
                return {
                    selectShow: false,
                    selectedItem: {},
                    orgCondition: null,
                    currentCondition: {},
                    currentShowCondition: {},
                    currentConditionTemp: false,
                    directFlightSwitch: false,
                    sortShowTemp: false,
                    sortList: [{
                        type: 0,
                        typeName: "\u65f6\u95f4",
                        data: [{
                            id: 1,
                            text: "\u65e9\u2192\u665a"
                        }, {
                            id: 2,
                            text: "\u665a\u2192\u65e9"
                        }]
                    }, {
                        type: 1,
                        typeName: "\u4ef7\u683c",
                        data: [{
                            id: 3,
                            text: "\u4f4e\u2192\u9ad8"
                        }, {
                            id: 4,
                            text: "\u9ad8\u2192\u4f4e"
                        }]
                    }],
                    currentSort: {}
                };
            },
            computed: {
                allFilterConditions: function() {
                    return [{
                        id: 1,
                        name: "\u8d77\u98de\u65f6\u95f4",
                        data: ["\u4e0a\u5348(00:00-11:59)", "\u4e2d\u5348(12:00-13:59)", "\u4e0b\u5348(14:00-17:59)", "\u665a\u4e0a(18:00-23:59)"]
                    }, {
                        id: 2,
                        name: "\u51fa\u53d1\u673a\u573a",
                        data: this.startAirPortList
                    }, {
                        id: 3,
                        name: "\u5230\u8fbe\u673a\u573a",
                        data: this.arrAirPortList
                    }, {
                        id: 4,
                        name: "\u822a\u7a7a\u516c\u53f8",
                        data: this.airlineCompanyList
                    }, {
                        id: 5,
                        name: "\u673a\u578b",
                        data: ["\u5927\u578b\u673a", "\u4e2d\u578b\u673a", "\u5c0f\u578b\u673a"]
                    }];
                }
            },
            mounted: function() {
                this.filterReset("currentConditionReset");
                this.currentSortInit();
            },
            methods: {
                chooseCondition: function(name, i) {
                    if (this.currentShowCondition[name]) {
                        var e = this.currentShowCondition[name];
                        if (e.indexOf(i) >= 0) {
                            e.splice(e.indexOf(i), 1);
                        } else {
                            e.push(i);
                        }
                        this.currentShowCondition[name] = e;
                    }
                },
                filterReset: function(canCreateDiscussions) {
                    var clocklog = this;
                    if (!this.orgCondition) {
                        this.orgCondition = {};
                        this.allFilterConditions.forEach(function(sclock) {
                            if (sclock.id) {
                                /** @type {!Array} */
                                clocklog.orgCondition[sclock.id] = [];
                            }
                        });
                    }
                    if ("currentConditionReset" === canCreateDiscussions) {
                        this.currentCondition = this.objSetVal(this.orgCondition);
                    }
                    this.currentShowCondition = this.objSetVal(this.orgCondition);
                },
                objSetVal: function(value) {
                    var output = this;
                    if ("object" !== (void 0 === value ? "undefined" : (0, _noframeworkWaypoints2.default)(value))) {
                        return value;
                    }
                    /** @type {(Array|{})} */
                    var props = value instanceof Array ? [] : {};
                    return (0, _deepAssign2.default)(value).forEach(function(key) {
                        output.$set(props, key, output.objSetVal(value[key]));
                    }), props;
                },
                selectJudge: function(pos, real) {
                    var data = this.currentShowCondition[pos];
                    return data && data.indexOf(real) >= 0;
                },
                filterPartShow: function() {
                    this.currentShowCondition = this.objSetVal(this.currentCondition);
                    /** @type {boolean} */
                    this.selectShow = true;
                    var MotionChangeRecommendation = this.$refs["filter-scroller"];
                    if (MotionChangeRecommendation) {
                        MotionChangeRecommendation.refresh();
                    }
                },
                filterPartHide: function() {
                    if (this.selectShow = false, this.currentCondition) {
                        /** @type {boolean} */
                        var t = false;
                        var frozenIndex;
                        for (frozenIndex in this.currentCondition) {
                            if (this.currentCondition[frozenIndex].length) {
                                /** @type {boolean} */
                                this.currentConditionTemp = true;
                                /** @type {boolean} */
                                t = true;
                                break;
                            }
                        }
                        if (!t) {
                            /** @type {boolean} */
                            this.currentConditionTemp = false;
                        }
                    }
                },
                resultShow: function() {
                    this.currentCondition = this.objSetVal(this.currentShowCondition);
                    this.filterConditionEmit();
                    this.filterPartHide();
                },
                filterConditionEmit: function(canCreateDiscussions) {
                    this.$emit("filter-condition", (0, _custom2.default)({}, this.currentCondition));
                },
                currentSortInit: function() {
                    this.sortSelcet(this.sortList[1]);
                },
                sortSelcet: function(model) {
                    var vm = this;
                    if (model.select) {
                        /** @type {number} */
                        var n = 0;
                        model.data.forEach(function(eball, max_out) {
                            if (vm.currentSort.id === eball.id) {
                                /** @type {number} */
                                n = max_out;
                            }
                        });
                        var i = n + 1;
                        i = i >= model.data.length ? 0 : i;
                        this.currentSort = model.data[i];
                    } else {
                        this.sortList.forEach(function(source) {
                            /** @type {boolean} */
                            source.select = source.type === model.type;
                        });
                        this.currentSort = model.data[0];
                    }
                    this.$emit("current-sort", this.currentSort.id);
                },
                currentShowText: function(p) {
                    return p.select ? this.currentSort.text : p.typeName;
                }
            }
        };
    }, function(canCreateDiscussions, message, key) {
        key.r(message);
        var value = key(70);
        var data = key.n(value);
        var k;
        for (k in value) {
            if ("default" !== k) {
                (function(c) {
                    key.d(message, c, function() {
                        return value[c];
                    });
                })(k);
            }
        }
        message.default = data.a;
    }, function(canCreateDiscussions, isSlidingUp, i) {}, function(canCreateDiscussions, exports, require) {
        /**
         * @param {!Object} obj
         * @return {?}
         */
        function _interopRequireDefault(obj) {
            return obj && obj.__esModule ? obj : {
                default: obj
            };
        }
        Object.defineProperty(exports, "__esModule", {
            value: true
        });
        var _noframeworkWaypoints2 = _interopRequireDefault(require(29));
        var _deepAssign2 = _interopRequireDefault(require(51));
        var TagHourlyStat = require(27);
        var ecQuery = require(11);
        exports.default = {
            data: function() {
                return {
                    originflightList: [],
                    flightList: {},
                    UTIL: _deepAssign2.default,
                    betterScrollerOptions: {
                        probeType: 2
                    }
                };
            },
            components: (0, _noframeworkWaypoints2.default)({}, (0, TagHourlyStat.mapComponents)(TagHourlyStat.BetterScroller)),
            mounted: function() {
                var vm = this;
                vm.$nextTick(function() {
                    var obj = (0, ecQuery.deepQuery)(vm, "$refs", "flightListWrap");
                    if (obj) {
                        obj.on("scroll", function() {
                            var i = vm.flightList.length;
                            var patchLen = vm.originflightList.length;
                            var scroller = obj.$betterScroller;
                            if (i < patchLen) {
                                var content = (0, ecQuery.deepQuery)(vm, "$refs", "flightListItem", 0);
                                if (content) {
                                    if ((~~scroller.scrollerHeight - ~~scroller.wrapperHeight + ~~scroller.y) / ~~content.offsetHeight < 5) {
                                        vm.flightList = vm.flightList.concat(vm.originflightList.slice(i, i + 20));
                                        vm.BSRefresh();
                                    }
                                }
                            }
                            vm.$emit("listScroll");
                        });
                    }
                });
            },
            methods: {
                setFlightListData: function(pollProfileId, userId) {
                    /** @type {string} */
                    this.originflightList = pollProfileId;
                    var i = 1 === userId && this.flightList.length > 0 ? this.flightList.length : 20;
                    this.flightList = this.originflightList.slice(0, i);
                    this.BSRefresh();
                },
                BSRefresh: function() {
                    var MotionChangeRecommendation = (0, ecQuery.deepQuery)(this, "$refs", "flightListWrap");
                    if (MotionChangeRecommendation) {
                        MotionChangeRecommendation.refresh();
                    }
                },
                BSScrollTo: function() {
                    var groupPanelScrollable = (0, ecQuery.deepQuery)(this, "$refs", "flightListWrap");
                    if (groupPanelScrollable) {
                        groupPanelScrollable.scrollTo();
                    }
                }
            }
        };
    }, function(canCreateDiscussions, message, key) {
        key.r(message);
        var value = key(73);
        var data = key.n(value);
        var k;
        for (k in value) {
            if ("default" !== k) {
                (function(c) {
                    key.d(message, c, function() {
                        return value[c];
                    });
                })(k);
            }
        }
        message.default = data.a;
    }, function(canCreateDiscussions, isSlidingUp, i) {}, function(canCreateDiscussions, exports, floor) {
        Object.defineProperty(exports, "__esModule", {
            value: true
        });
        var startYNew = floor(18);
        exports.default = {
            props: {
                lowPriceList: {
                    type: Array,
                    default: function() {
                        return [];
                    }
                },
                scrollLeft: {
                    type: Number,
                    default: 0
                },
                departDate: {
                    type: String,
                    default: ""
                },
                departCode: {
                    type: String,
                    default: ""
                },
                destCode: {
                    type: String,
                    default: ""
                }
            },
            watch: {
                scrollLeft: function(value) {
                    var me = this;
                    this.$nextTick(function() {
                        if (me.lowPriceList.length > 0) {
                            /** @type {number} */
                            me.$refs.lowPriceWrap.scrollLeft = value * me.$refs.lowPriceItem[0].offsetWidth;
                        }
                    });
                }
            },
            mounted: function() {
                var me = this;
                this.$nextTick(function() {
                    if (me.lowPriceList.length > 0) {
                        /** @type {number} */
                        me.$refs.lowPriceWrap.scrollLeft = me.scrollLeft * me.$refs.lowPriceItem[0].offsetWidth;
                    }
                });
            },
            methods: {
                toggleDate: function(data, index) {
                    this.$emit("toggle-date", data, index);
                },
                calendarShow: function() {
                    var $scope = this;
                    (0, startYNew.listCalendar)({
                        departDate: this.departDate,
                        departCode: this.departCode,
                        destCode: this.destCode
                    }, function(options) {
                        var from = options.beginDate;
                        if (from) {
                            $scope.toggleDate({
                                formatDate: from
                            }, 2);
                        }
                    });
                    console.warn(this.departDate, this.departCode, this.destCode);
                }
            }
        };
    }, function(canCreateDiscussions, message, key) {
        key.r(message);
        var value = key(76);
        var data = key.n(value);
        var k;
        for (k in value) {
            if ("default" !== k) {
                (function(c) {
                    key.d(message, c, function() {
                        return value[c];
                    });
                })(k);
            }
        }
        message.default = data.a;
    }, function(canCreateDiscussions, exports, require) {
        /**
         * @param {!Object} obj
         * @return {?}
         */
        function _interopRequireDefault(obj) {
            return obj && obj.__esModule ? obj : {
                default: obj
            };
        }
        Object.defineProperty(exports, "__esModule", {
            value: true
        });
        var _noframeworkWaypoints2 = _interopRequireDefault(require(97));
        var _custom2 = _interopRequireDefault(require(221));
        var _UiIcon2 = _interopRequireDefault(require(216));
        var _readArchive2 = _interopRequireDefault(require(49));
        var _colorsList2 = _interopRequireDefault(require(131));
        var _validateUrl2 = _interopRequireDefault(require(29));
        var _aliapp2 = _interopRequireDefault(require(124));
        var _browser2 = _interopRequireDefault(require(32));
        var HttpManager = require(52);
        var _deepAssign2 = _interopRequireDefault(require(51));
        var now = require(31);
        var TagHourlyStat = require(89);
        var app = require(18);
        var _thirdapp2 = _interopRequireDefault(require(88));
        var _params2 = _interopRequireDefault(require(87));
        var _isSupported2 = _interopRequireDefault(require(84));
        var CheckDailyStat = require(83);
        var self = require(11);
        var App = require(27);
        var _buildElement2 = _interopRequireDefault(require(185));
        var _buildPageNumber2 = _interopRequireDefault(require(181));
        var _buildStyle2 = _interopRequireDefault(require(178));
        var _setStyles2 = _interopRequireDefault(require(175));
        (0, app.hideMoreButtonInNavigationBar)();
        (0, app.hideShareButtonInNavigationBar)();
        (0, app.setNavigationBarDisplay)();
        var Dropzone = {
            oneWay: 0,
            goTrip: 1,
            retTrip: 2
        };
        var animationConfigs = {
            oneWay: 0,
            roundWay: 1
        };
        /** @type {number} */
        var maxDist = 0;
        /** @type {null} */
        var _takingTooLongTimeout = null;
        exports.default = {
            props: {},
            components: (0, _validateUrl2.default)({
                lowPriceCalendar: _buildElement2.default,
                flightList: _buildPageNumber2.default,
                listFilter: _buildStyle2.default,
                listTitlebar: _setStyles2.default
            }, (0, App.mapComponents)(App.MaskLoading)),
            data: function() {
                return {
                    mfwLoading: true,
                    originLowPriceList: [],
                    lowPriceList: [],
                    urlParam: {},
                    calendarScrollLeft: 0,
                    originFlightList: [],
                    formatFlightList: [],
                    showFlightList: {},
                    startAirPortList: [],
                    arrAirPortList: [],
                    airlineCompanyList: [],
                    loadingMore: true,
                    currentSortId: 0,
                    curFlightListCacheKey: "",
                    goTripInfo: null,
                    tripType: {
                        oneWay: false,
                        goTrip: false,
                        retTrip: false
                    },
                    progressWidth: 0,
                    listTitlebarInfo: {}
                };
            },
            mounted: function() {
                var textStyles = this;
                this.urlParam = function(strRect) {
                    var r = {};
                    /** @type {(Array<string>|null)} */
                    var n = strRect.match(/[?&]([^=&#]+)=([^&#]*)/g);
                    return n && (0, _browser2.default)(n).forEach(function(index) {
                        /** @type {!Array<string>} */
                        var matches = n[index].split("=");
                        /** @type {string} */
                        var f = matches[0].substr(1);
                        /** @type {string} */
                        var v = decodeURIComponent(matches[1]);
                        /** @type {string} */
                        r[f] = v;
                    }), r;
                }(location.href);
                var event = (0, self.queryString)("type", "oneWay");
                if (void 0 === this.urlParam.status ? this.urlParam.status = animationConfigs[event] || 0 : this.urlParam.status = ~~this.urlParam.status, this.urlParam.adult_nums = ~~(0, self.queryString)("adult_nums", 1), this.urlParam.with_child = ~~this.urlParam.with_child, function(file) {
                        return !((0, _aliapp2.default)(Dropzone).indexOf(file.status) < 0 || file.status !== Dropzone.oneWay && !file.destDate) && file.departCity && file.departCode && file.destCity && file.destCode && file.departDate && file.adult_nums > 0;
                    }(this.urlParam)) {
                    /** @type {boolean} */
                    this.tripType.oneWay = this.urlParam.status === Dropzone.oneWay;
                    /** @type {boolean} */
                    this.tripType.goTrip = this.urlParam.status === Dropzone.goTrip;
                    /** @type {boolean} */
                    this.tripType.retTrip = this.urlParam.status === Dropzone.retTrip;
                    this.getOriginFlightList();
                    if (this.tripType.oneWay) {
                        this.getLowPriceList();
                    }
                    /** @type {!Array} */
                    var i = [this.urlParam.departCity, this.urlParam.destCity];
                    if (!this.tripType.goTrip) {
                        this.tripType.retTrip;
                    }
                    if (this.tripType.retTrip) {
                        i.reverse().join("-");
                    } else {
                        i.join("-");
                    }
                    /** @type {string} */
                    this.listTitlebarInfo.tripType = this.tripType.goTrip ? "\u53bb\u7a0b\uff1a" : this.tripType.retTrip ? "\u8fd4\u7a0b\uff1a" : "";
                    this.listTitlebarInfo.departCity = this.tripType.retTrip ? this.urlParam.destCity : this.urlParam.departCity;
                    this.listTitlebarInfo.destCity = this.tripType.retTrip ? this.urlParam.departCity : this.urlParam.destCity;
                    if (this.tripType.retTrip) {
                        this.goTripInfo = {
                            dateInfo: [this.urlParam.departDate, (0, now.getChineseWeekDay)(this.urlParam.departDate)].join(" "),
                            timeSlot: this.urlParam.timeSlot,
                            airlineCompanyName: this.urlParam.airlineCompanyName
                        };
                    }
                    _isSupported2.default.pageEvent("flight", "page", {
                        name: "\u5927\u4ea4\u901a\u9891\u9053-\u56fd\u5185\u822a\u73ed\u5217\u8868\u9875"
                    });
                    (0, app.setShouldLeavePageHooker)(true, function() {
                        if (textStyles.tripType.oneWay || textStyles.tripType.goTrip) {
                            (0, app.closeWebview)();
                        }
                    });
                    window.addEventListener("scroll", function() {
                        /** @type {number} */
                        var d = ~~window.scrollY;
                        if (d > maxDist) {
                            /** @type {number} */
                            maxDist = d;
                        }
                    });
                } else {
                    App.ErrorPage.show({
                        container: this.$refs["scroll-wrap"],
                        title: "\u67e5\u8be2\u6240\u9700\u6570\u636e\u8d70\u4e22\u4e86",
                        buttonText: ""
                    });
                }
            },
            methods: {
                onback: function() {
                    _isSupported2.default.pageEvent("flight", "flight_list_module_click", {
                        _tp: "\u5927\u4ea4\u901a\u9891\u9053-\u56fd\u5185\u822a\u73ed\u5217\u8868\u9875",
                        module_name: "\u9876\u90e8\u680f",
                        item_name: "\u8fd4\u56de",
                        item_info: "",
                        dept_airport_code: (0, self.queryString)("departCode"),
                        arr_airport_code: (0, self.queryString)("destCode")
                    });
                    if (this.tripType.oneWay || this.tripType.goTrip) {
                        (0, app.closeWebview)();
                    } else {
                        (0, app.historyBack)();
                    }
                },
                showLoading: function() {
                    /** @type {boolean} */
                    this.mfwLoading = true;
                    App.MaskLoading.show({
                        className: "loading-top"
                    });
                },
                hideLoading: function() {
                    /** @type {boolean} */
                    this.mfwLoading = false;
                    App.MaskLoading.hide();
                },
                getLowPriceList: function() {
                    var creationItem = this;
                    var varCatViewer = this;
                    var paymentChannel = {
                        departCode: this.urlParam.departCode,
                        destCode: this.urlParam.destCode,
                        signKey: (0, _thirdapp2.default)()
                    };
                    paymentChannel.sign = (0, _params2.default)(function(artistInfo) {
                        return [paymentChannel.departCode, paymentChannel.destCode, artistInfo].join("");
                    }(paymentChannel.signKey));
                    (0, HttpManager.post)(_deepAssign2.default.AJAX_BASEURL + "/fwl/lowprice/list", paymentChannel).then(function(settings) {
                        if (settings.data.success && settings.data.data && settings.data.data.length) {
                            varCatViewer.originLowPriceList = settings.data.data;
                        } else {
                            _isSupported2.default.pageEvent("default", "page_error", {
                                page_name: "\u56fd\u5185\u62a5\u4ef7\u9875",
                                project_name: "\u56fd\u5185\u673a\u7968",
                                message: "\u8bf7\u6c42\u6210\u529f\u4e14\u8fd4\u56de\u6210\u529f\u4f46\u6570\u636e\u4e3anull\uff0c\u6216\u8005\u957f\u5ea6\u4e3a0;\u6216\u8005\u8bf7\u6c42\u6210\u529f\u8fd4\u56defail\uff0c"
                            });
                        }
                        creationItem.lowPriceListDeal(creationItem.urlParam.departDate);
                    }).catch(function(canCreateDiscussions) {
                        _isSupported2.default.pageEvent("default", "page_error", {
                            page_name: "\u56fd\u5185\u62a5\u4ef7\u9875",
                            project_name: "\u56fd\u5185\u673a\u7968",
                            message: "\u8bf7\u6c42\u5931\u8d25"
                        });
                    });
                },
                toggleDate: function(type, date) {
                    _isSupported2.default.pageEvent("flight", "flight_list_module_click", {
                        _tp: "\u5927\u4ea4\u901a\u9891\u9053-\u56fd\u5185\u822a\u73ed\u5217\u8868\u9875",
                        module_name: "\u65f6\u95f4",
                        item_name: 1 === date ? "\u641c\u7d22\u5217\u8868\u65e5\u5386" : "\u4f4e\u4ef7\u65e5\u5386",
                        item_info: "",
                        dept_airport_code: (0, self.queryString)("departCode"),
                        arr_airport_code: (0, self.queryString)("destCode")
                    });
                    this.urlParam.departDate = type.formatDate;
                    (0, app.navigateToNewPage)(location.pathname + "?" + (0, self.stringifyQuery)(this.urlParam));
                },
                getLowerPriceText: function(other) {
                    /** @type {boolean} */
                    var _iteratorNormalCompletion3 = true;
                    /** @type {boolean} */
                    var i = false;
                    var r = void 0;
                    try {
                        var _step2;
                        var _iterator3 = (0, _colorsList2.default)(this.originLowPriceList);
                        for (; !(_iteratorNormalCompletion3 = (_step2 = _iterator3.next()).done); _iteratorNormalCompletion3 = true) {
                            var o = _step2.value;
                            if (o.date === (0, now.dateFormat)(other)) {
                                return o.price < 99999999 ? "\u00a5" + o.price : "\u67e5\u4ef7";
                            }
                        }
                    } catch (G__20648) {
                        /** @type {boolean} */
                        i = true;
                        r = G__20648;
                    } finally {
                        try {
                            if (!_iteratorNormalCompletion3 && _iterator3.return) {
                                _iterator3.return();
                            }
                        } finally {
                            if (i) {
                                throw r;
                            }
                        }
                    }
                    return "\u67e5\u4ef7";
                },
                lowPriceListDeal: function(s) {
                    /** @type {!Date} */
                    var r = new Date(s);
                    /** @type {!Date} */
                    var d = new Date((0, now.dateFormat)(new Date));
                    if (r - d >= 0) {
                        /** @type {number} */
                        var r = 0;
                        /** @type {number} */
                        var x = -7;
                        for (; x < 8; x++) {
                            /** @type {!Date} */
                            var c = new Date(s);
                            if (c.setDate(c.getDate() + x), c >= d) {
                                var item = {
                                    day: (0, now.getChineseWeekDay)((0, now.dateFormat)(c)),
                                    formatDate: (0, now.dateFormat)(c),
                                    date: c.getDate() > 9 ? c.getDate() : "0" + c.getDate(),
                                    month: c.getMonth() + 1 > 9 ? c.getMonth() + 1 : "0" + (c.getMonth() + 1),
                                    price: this.getLowerPriceText(c)
                                };
                                if (0 === x) {
                                    /** @type {boolean} */
                                    item.current = true;
                                }
                                if (x < 0) {
                                    r++;
                                }
                                this.lowPriceList.push(item);
                            }
                        }
                        /** @type {number} */
                        this.calendarScrollLeft = r > 2 ? r - 2 : 0;
                    }
                },
                lowPriceListSetCur: function(url) {
                    if (this.lowPriceList.length) {
                        /** @type {number} */
                        var s = 0;
                        var solidsLength = this.lowPriceList.length;
                        for (; s < solidsLength; s++) {
                            if (this.lowPriceList[s].formatDate === this.urlParam.departDate) {
                                /** @type {string} */
                                this.lowPriceList[s].price = "\u00a5" + url;
                                break;
                            }
                        }
                    }
                },
                getOriginFlightList: function() {
                    /**
                     * @param {!Function} func
                     * @return {undefined}
                     */
                    function post(func) {
                        setTimeout(function() {
                            func();
                        }, paymentChannel.queryTimes < 21 ? 500 : 1e3);
                    }
                    var self = this;
                    self.showLoading();
                    var paymentChannel = {
                        departCity: self.urlParam.departCity,
                        departCode: self.urlParam.departCode,
                        departDate: self.urlParam.departDate,
                        destCity: self.urlParam.destCity,
                        destCode: self.urlParam.destCode,
                        adultNums: self.urlParam.adult_nums,
                        hasChildren: !!self.urlParam.with_child,
                        trip: self.urlParam.status,
                        queryTimes: 0
                    };
                    if (this.tripType.goTrip) {
                        (0, _readArchive2.default)(paymentChannel, {
                            destDate: self.urlParam.destDate
                        });
                    }
                    if (this.tripType.retTrip) {
                        (0, _readArchive2.default)(paymentChannel, {
                            flightNo: self.urlParam.flightNo,
                            destDate: self.urlParam.destDate
                        });
                    }! function add() {
                        (0, TagHourlyStat.setLastSearchTime)();
                        paymentChannel.signKey = (0, _thirdapp2.default)();
                        paymentChannel.sign = (0, _params2.default)(function(sideLength) {
                            return [paymentChannel.departCode, paymentChannel.destCode, sideLength, paymentChannel.departDate, paymentChannel.destDate, sideLength].join("");
                        }(paymentChannel.signKey));
                        (0, HttpManager.post)(_deepAssign2.default.AJAX_BASEURL + "/fwl/flightList/search", paymentChannel).then(function(evtA) {
                            paymentChannel.queryTimes++;
                            var a = evtA.data;
                            if (a.success) {
                                var user = a.data;
                                var state = user ? user.flightList : void 0;
                                if (user && state && state.length && state[0].merchantId) {
                                    if (self.originFlightList.length < 50) {
                                        self.originFlightList = state;
                                        self.flightDataFormat();
                                        self.hideLoading();
                                        self.setProgress();
                                        self.curFlightListCacheKey = user.curFlightListCacheKey;
                                        if (user.needQueryMore && paymentChannel.queryTimes < 30) {
                                            post(add);
                                        } else {
                                            self.hideProgress();
                                        }
                                    } else {
                                        if (user.needQueryMore && paymentChannel.queryTimes < 30) {
                                            post(add);
                                        } else {
                                            self.originFlightList = state;
                                            self.flightDataFormat();
                                            self.hideProgress();
                                        }
                                    }
                                } else {
                                    if (user.needQueryMore && paymentChannel.queryTimes < 30) {
                                        post(add);
                                    } else {
                                        if (self.originFlightList.length) {
                                            self.hideProgress();
                                        } else {
                                            self.hideLoading();
                                            App.ErrorPage.show({
                                                container: self.$refs["scroll-wrap"],
                                                title: "\u6570\u636e\u8d70\u4e22\u4e86"
                                            });
                                        }
                                    }
                                }
                            } else {
                                if (404 == ~~a.code) {
                                    return self.hideLoading(), void App.ErrorPage.show({
                                        container: self.$refs["scroll-wrap"],
                                        title: a.message || "\u7cfb\u7edf\u7ef4\u62a4\u4e2d",
                                        buttonText: ""
                                    });
                                }
                                if (self.originFlightList.length) {
                                    self.hideProgress();
                                } else {
                                    self.hideLoading();
                                    App.ErrorPage.show({
                                        container: self.$refs["scroll-wrap"],
                                        title: "\u6570\u636e\u8d70\u4e22\u4e86"
                                    });
                                    _isSupported2.default.pageEvent("default", "page_error", {
                                        page_name: "\u56fd\u5185\u62a5\u4ef7\u9875",
                                        project_name: "\u56fd\u5185\u673a\u7968",
                                        message: "\u8bf7\u6c42\u6210\u529f\u4e14\u8fd4\u56de\u6210\u529f\uff0c\u4f46\u8f6e\u8be2\u6570\u636e\u4e3anull\uff0c\u6216\u8005\u957f\u5ea6\u4e3a0"
                                    });
                                }
                            }
                        }).catch(function(canCreateDiscussions) {
                            if (self.originFlightList.length) {
                                self.hideProgress();
                            } else {
                                self.hideLoading();
                                App.ErrorPage.show({
                                    container: self.$refs["scroll-wrap"],
                                    title: "\u6570\u636e\u8d70\u4e22\u4e86"
                                });
                            }
                            _isSupported2.default.pageEvent("default", "page_error", {
                                page_name: "\u56fd\u5185\u62a5\u4ef7\u9875",
                                project_name: "\u56fd\u5185\u673a\u7968",
                                message: "\u8bf7\u6c42\u5931\u8d25"
                            });
                        });
                    }();
                },
                getObjVal: function(options, index) {
                    var nested = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : "";
                    return options[index] ? options[index] : nested;
                },
                flightDataFormat: function() {
                    var textStyles = this;
                    var utils = this;
                    /** @type {!Array} */
                    var props = [];
                    var view = new _UiIcon2.default;
                    var o = new _UiIcon2.default;
                    var s = new _UiIcon2.default;
                    /** @type {number} */
                    var x = 99999999;
                    utils.originFlightList.forEach(function(settings) {
                        var env = (0, self.deepQuery)(settings, "goTrip", "segmentMOList");
                        var children = (0, self.deepQuery)(settings, "seat_infos");
                        if (env && env.length && children && children.length) {
                            var options = env[0];
                            var obj = children[0];
                            /** @type {!Array} */
                            var slashes = [];
                            if (options.stop_infos && options.stop_infos.length) {
                                options.stop_infos.forEach(function(loc) {
                                    slashes.push(loc.city_name);
                                });
                            }
                            var order = options.org_airport_name ? options.org_airport_name.replace("\u673a\u573a", "") : "";
                            var m = options.dst_airport_name ? options.dst_airport_name.replace("\u673a\u573a", "") : "";
                            var v = new _UiIcon2.default;
                            if (options.flight_share) {
                                v.add("\u5171\u4eab");
                            }
                            var timing = {
                                start: {
                                    time: options.dep_time,
                                    airport: order,
                                    terminal: options.org_airport_quay
                                },
                                arrive: {
                                    time: options.arr_time,
                                    airport: m,
                                    terminal: options.dst_airport_quay
                                },
                                duration: {
                                    text: options.fly_time ? options.fly_time.replace("\u949f", "") : ""
                                },
                                stopInfo: slashes,
                                addDay: options.arr_next_day > 0 ? "+" + options.arr_next_day + "\u5929" : "",
                                airlineCompany: {
                                    name: (0, self.deepQuery)(options, "airline_name"),
                                    logoUrl: "https://css.mafengwo.net/mobile/images/flight_int_logo/" + (options.flight_no ? options.flight_no.substr(0, 2) : "") + ".png"
                                },
                                flightNo: options.flight_no,
                                showFlightNo: options.flight_no,
                                other: [].concat((0, _custom2.default)(v)),
                                priceInfo: {
                                    price: obj.settle_price_coupon,
                                    chdPrice: utils.urlParam.with_child ? obj.settle_price_child : "",
                                    coupon: obj.settle_price - obj.settle_price_coupon
                                },
                                planeSize: utils.getPlaneSize(options.plane_size),
                                planeType: utils.getObjVal(options, "plane_name") + (utils.getPlaneSize(options.plane_size) ? "(" + utils.getPlaneSize(options.plane_size).replace("\u578b\u673a", "") + ")" : ""),
                                merchantId: settings.merchantId
                            };
                            if (props.push(timing), view.add(order), o.add(m), s.add(options.airline_name), textStyles.tripType.oneWay) {
                                /** @type {number} */
                                var y = ~~obj.settle_price_coupon;
                                if (0 !== y && y < x) {
                                    /** @type {number} */
                                    x = y;
                                }
                            }
                        }
                    });
                    /** @type {!Array<?>} */
                    this.formatFlightList = [].concat(props);
                    /** @type {!Array<?>} */
                    this.startAirPortList = [].concat((0, _custom2.default)(view));
                    /** @type {!Array<?>} */
                    this.arrAirPortList = [].concat((0, _custom2.default)(o));
                    /** @type {!Array<?>} */
                    this.airlineCompanyList = [].concat((0, _custom2.default)(s));
                    this.setShowFlightList([].concat(this.formatFlightList), 1);
                    if (this.currentSortId) {
                        this.sortDeal(this.currentSortId);
                    }
                    if (this.tripType.oneWay && 99999999 !== x && x > 0) {
                        this.lowPriceListSetCur(x);
                    }
                },
                getPlaneSize: function(width) {
                    switch (width) {
                        case "S":
                            return "\u5c0f\u578b\u673a";
                        case "M":
                            return "\u4e2d\u578b\u673a";
                        case "L":
                            return "\u5927\u578b\u673a";
                        default:
                            return "";
                    }
                },
                select: function(e, keepExisting) {
                    var $ = this;
                    if ((0, TagHourlyStat.isSearchTimeout)()) {
                        App.MessageBox.alert({
                            title: "\u62a5\u4ef7\u5df2\u8fc7\u671f",
                            content: "\u822a\u73ed\u4ef7\u683c\u53ef\u80fd\u53d8\u52a8\uff0c\u5c06\u4e3a\u60a8\u91cd\u65b0\u67e5\u8be2",
                            buttonText: "\u91cd\u65b0\u67e5\u8be2",
                            okButtonClick: function() {
                                if ($.tripType.retTrip) {
                                    /** @type {number} */
                                    $.urlParam.status = Dropzone.goTrip;
                                    if ($.urlParam.flightNo) {
                                        delete $.urlParam.flightNo;
                                    }
                                    (0, app.navigateToNewPage)("?" + (0, self.stringifyQuery)($.urlParam));
                                } else {
                                    (0, app.navigateToNewPage)(location.href);
                                }
                            }
                        });
                    } else {
                        _isSupported2.default.pageEvent("flight", "flight_list_module_click", {
                            _tp: "\u5927\u4ea4\u901a\u9891\u9053-\u56fd\u5185\u822a\u73ed\u5217\u8868\u9875",
                            module_name: "\u822a\u73ed\u73ed\u6b21",
                            item_name: e.airlineCompany.name + e.showFlightNo,
                            item_info: "",
                            dept_airport_code: (0, self.queryString)("departCode"),
                            arr_airport_code: (0, self.queryString)("destCode")
                        });
                        (0, self.deepQuery)(window, "screen", "height");
                        (0, self.deepQuery)(keepExisting, "currentTarget", "clientHeight");
                        if (this.urlParam.flightNo = e.flightNo, this.tripType.goTrip) {
                            this.urlParam.curFlightListCacheKey = this.curFlightListCacheKey;
                            this.urlParam.timeSlot = ((0, self.deepQuery)(e, "start", "time") || "") + "-" + ((0, self.deepQuery)(e, "arrive", "time") || "");
                            this.urlParam.airlineCompanyName = (0, self.deepQuery)(e, "airlineCompany", "name") || "";
                        } else {
                            if (this.urlParam.destDate && this.tripType.oneWay) {
                                delete this.urlParam.destDate;
                            }
                            var r = this.urlParam.curFlightListCacheKey;
                            this.urlParam.curFlightListCacheKey = r && this.tripType.retTrip ? r + "%" + this.curFlightListCacheKey : this.curFlightListCacheKey;
                        }
                        (0, app.navigateToNewPage)("seats" + ((0, CheckDailyStat.isInOldPHPProject)() ? "" : ".html") + "?" + (0, self.stringifyQuery)(this.urlParam));
                    }
                },
                filterCondition: function(item) {
                    this.filterDeal(item);
                    var e = (0, self.deepQuery)(this, "$refs", "flight-list");
                    if (e) {
                        e.BSScrollTo();
                    }
                    _isSupported2.default.pageEvent("flight", "flight_list_module_click", {
                        _tp: "\u5927\u4ea4\u901a\u9891\u9053-\u56fd\u5185\u822a\u73ed\u5217\u8868\u9875",
                        module_name: "\u5e95\u90e8\u7b5b\u9009\u680f",
                        item_name: "-",
                        item_info: "",
                        dept_airport_code: (0, self.queryString)("departCode"),
                        arr_airport_code: (0, self.queryString)("destCode")
                    });
                },
                filterDeal: function(t) {
                    var sample = this;
                    var $show = this.formatFlightList.concat();
                    var lastEndItem = t.directFlight;
                    var n = (0, self.deepQuery)(t, 1);
                    var label = (0, self.deepQuery)(t, 2);
                    var s = (0, self.deepQuery)(t, 3);
                    var options = (0, self.deepQuery)(t, 4);
                    var a = (0, self.deepQuery)(t, 5);
                    $show = $show.filter(function(self) {
                        return !(n && n.length && !sample.startTimeJudege(self.start.time, n)) && (!(lastEndItem && self.transfer.length > 0) && (!(label && label.length && label.indexOf(self.start.airport) < 0) && (!(s && s.length && s.indexOf(self.arrive.airport) < 0) && (!(options && options.length && options.indexOf(self.airlineCompany.name) < 0) && !(a && a.length && a.indexOf(self.planeSize) < 0)))));
                    });
                    this.setShowFlightList($show, 2);
                    this.sortDeal(this.currentSortId);
                },
                startTimeJudege: function(ast, args) {
                    /** @type {!RegExp} */
                    var _digitExpr = /\([^\)]*\)/g;
                    /** @type {number} */
                    var i = 0;
                    var arg_count = args.length;
                    for (; i < arg_count; i++) {
                        var index = args[i].match(_digitExpr)[0].replace(/[\(|\)]/g, "").split("-");
                        var conditions = (0, _noframeworkWaypoints2.default)(index, 2);
                        var conditionVariable = conditions[0];
                        var item = conditions[1];
                        if ((0, now.setTime)(ast) >= (0, now.setTime)(conditionVariable) && (0, now.setTime)(ast) <= (0, now.setTime)(item)) {
                            return true;
                        }
                    }
                    return false;
                },
                currentSort: function(url) {
                    /** @type {number} */
                    this.currentSortId = url;
                    this.sortDeal(url);
                    var e = (0, self.deepQuery)(this, "$refs", "flight-list");
                    if (e) {
                        e.BSScrollTo();
                    }
                    if (1 == url || 2 == url) {
                        _isSupported2.default.pageEvent("flight", "flight_list_module_click", {
                            _tp: "\u5927\u4ea4\u901a\u9891\u9053-\u56fd\u5185\u822a\u73ed\u5217\u8868\u9875",
                            module_name: 1 == url ? "\u4ece\u4f4e\u5230\u9ad8" : "\u4ece\u9ad8\u5230\u4f4e",
                            item_info: "",
                            dept_airport_code: (0, self.queryString)("departCode"),
                            arr_airport_code: (0, self.queryString)("destCode")
                        });
                    } else {
                        _isSupported2.default.pageEvent("flight", "flight_list_module_click", {
                            _tp: "\u5927\u4ea4\u901a\u9891\u9053-\u56fd\u5185\u822a\u73ed\u5217\u8868\u9875",
                            module_name: 3 == url ? "\u4ece\u65e9\u5230\u665a" : "\u4ece\u665a\u5230\u65e9",
                            item_info: "",
                            dept_airport_code: (0, self.queryString)("departCode"),
                            arr_airport_code: (0, self.queryString)("destCode")
                        });
                    }
                },
                sortDeal: function(unit) {
                    var e = this;
                    var $this = this.showFlightList.slice(0);
                    $this.sort(function(i, eid) {
                        return e.sortJudge(i, eid, unit);
                    });
                    this.setShowFlightList($this, 2);
                },
                sortJudge: function(p, item, count) {
                    switch (count) {
                        case 1:
                            return (0, now.setTime)(p.start.time) - (0, now.setTime)(item.start.time);
                        case 2:
                            return (0, now.setTime)(item.start.time) - (0, now.setTime)(p.start.time);
                        case 3:
                            return p.priceInfo.price - item.priceInfo.price;
                        case 4:
                            return item.priceInfo.price - p.priceInfo.price;
                        default:
                            return 0;
                    }
                },
                setShowFlightList: function($el, name) {
                    /** @type {string} */
                    this.showFlightList = $el;
                    var $mmaModSurveyOffline = (0, self.deepQuery)(this, "$refs", "flight-list");
                    if ($mmaModSurveyOffline) {
                        $mmaModSurveyOffline.setFlightListData(this.showFlightList, name);
                    }
                },
                setProgress: function() {
                    var self = this;
                    /** @type {number} */
                    _takingTooLongTimeout = setTimeout(function() {
                        if (self.progressWidth <= 90) {
                            self.progressWidth += self.progressWidth > 50 ? 10 : 1;
                            self.setProgress();
                        } else {
                            clearTimeout(_takingTooLongTimeout);
                        }
                    }, 100);
                },
                hideProgress: function() {
                    var scope = this;
                    if (_takingTooLongTimeout) {
                        clearTimeout(_takingTooLongTimeout);
                    }
                    /** @type {number} */
                    scope.progressWidth = 100;
                    setTimeout(function() {
                        /** @type {boolean} */
                        scope.loadingMore = false;
                    }, 500);
                },
                listScroll: function() {}
            }
        };
    }, function(canCreateDiscussions, message, key) {
        key.r(message);
        var value = key(78);
        var data = key.n(value);
        var k;
        for (k in value) {
            if ("default" !== k) {
                (function(c) {
                    key.d(message, c, function() {
                        return value[c];
                    });
                })(k);
            }
        }
        message.default = data.a;
    }, , , , function(canCreateDiscussions, self, i) {
        Object.defineProperty(self, "__esModule", {
            value: true
        });
        /**
         * @param {?} callback
         * @return {?}
         */
        self.deepQuery = function(callback) {
            /** @type {number} */
            var length = arguments.length;
            /** @type {!Array} */
            var args = Array(length > 1 ? length - 1 : 0);
            /** @type {number} */
            var i = 1;
            for (; i < length; i++) {
                args[i - 1] = arguments[i];
            }
            return args.reduce(function(obj, elementID) {
                return obj ? obj[elementID] : obj;
            }, callback);
        };
        /**
         * @return {?}
         */
        self.isInOldPHPProject = function() {
            return !("w.mafengwo.cn" === location.host || 0 === location.host.indexOf("localhost"));
        };
    }, function(canCreateDiscussions, exports, aggFn) {
        /**
         * @param {string} m
         * @param {string} n
         * @return {undefined}
         */
        function open(m, n) {
            var link_options = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {};
            if ((0, v.isFunction)(window.mfwPageEvent)) {
                window.mfwPageEvent(m, n, link_options);
            }
        }
        Object.defineProperty(exports, "__esModule", {
            value: true
        });
        /** @type {function(string, string): undefined} */
        exports.pageEvent = open;
        var v = aggFn(11);
        exports.default = {
            pageEvent: open
        };
    }, , , function(record, args, i) {
        /**
         * @param {number} a
         * @param {number} b
         * @return {?}
         */
        function $(a, b) {
            /** @type {number} */
            var i = (65535 & a) + (65535 & b);
            return (a >> 16) + (b >> 16) + (i >> 16) << 16 | 65535 & i;
        }
        /**
         * @param {number} t
         * @param {number} n
         * @param {number} d
         * @param {number} input
         * @param {number} id
         * @param {number} obj
         * @return {?}
         */
        function add(t, n, d, input, id, obj) {
            return $(function(n, s) {
                return n << s | n >>> 32 - s;
            }($($(n, t), $(input, obj)), id), d);
        }
        /**
         * @param {number} p
         * @param {number} d
         * @param {number} a
         * @param {number} b
         * @param {undefined} data
         * @param {number} n
         * @param {number} context
         * @return {?}
         */
        function cb(p, d, a, b, data, n, context) {
            return add(d & a | ~d & b, p, d, data, n, context);
        }
        /**
         * @param {number} x
         * @param {number} d
         * @param {number} a
         * @param {number} b
         * @param {undefined} out
         * @param {number} callback
         * @param {number} color
         * @return {?}
         */
        function debug(x, d, a, b, out, callback, color) {
            return add(d & b | a & ~b, x, d, out, callback, color);
        }
        /**
         * @param {number} t
         * @param {number} d
         * @param {number} a
         * @param {number} b
         * @param {undefined} n
         * @param {number} selector
         * @param {number} callback
         * @return {?}
         */
        function fn(t, d, a, b, n, selector, callback) {
            return add(d ^ a ^ b, t, d, n, selector, callback);
        }
        /**
         * @param {number} t
         * @param {number} d
         * @param {number} a
         * @param {number} b
         * @param {undefined} n
         * @param {number} selector
         * @param {number} capture
         * @return {?}
         */
        function callback(t, d, a, b, n, selector, capture) {
            return add(a ^ (d | ~b), t, d, n, selector, capture);
        }
        /**
         * @param {!Object} args
         * @param {number} delay
         * @return {?}
         */
        function next(args, delay) {
            var i;
            var element;
            var c;
            var block;
            var filename;
            args[delay >> 5] |= 128 << delay % 32;
            /** @type {number} */
            args[14 + (delay + 64 >>> 9 << 4)] = delay;
            /** @type {number} */
            var result = 1732584193;
            /** @type {number} */
            var value = -271733879;
            /** @type {number} */
            var res = -1732584194;
            /** @type {number} */
            var key = 271733878;
            /** @type {number} */
            i = 0;
            for (; i < args.length; i = i + 16) {
                element = result;
                c = value;
                block = res;
                filename = key;
                value = callback(value = callback(value = callback(value = callback(value = fn(value = fn(value = fn(value = fn(value = debug(value = debug(value = debug(value = debug(value = cb(value = cb(value = cb(value = cb(value, res = cb(res, key = cb(key, result = cb(result, value, res, key, args[i], 7, -680876936), value, res, args[i + 1], 12, -389564586), result, value, args[i + 2], 17, 606105819), key, result, args[i + 3], 22, -1044525330), res = cb(res, key = cb(key, result = cb(result, value, res,
                            key, args[i + 4], 7, -176418897), value, res, args[i + 5], 12, 1200080426), result, value, args[i + 6], 17, -1473231341), key, result, args[i + 7], 22, -45705983), res = cb(res, key = cb(key, result = cb(result, value, res, key, args[i + 8], 7, 1770035416), value, res, args[i + 9], 12, -1958414417), result, value, args[i + 10], 17, -42063), key, result, args[i + 11], 22, -1990404162), res = cb(res, key = cb(key, result = cb(result, value, res, key, args[i + 12], 7, 1804603682), value, res,
                            args[i + 13], 12, -40341101), result, value, args[i + 14], 17, -1502002290), key, result, args[i + 15], 22, 1236535329), res = debug(res, key = debug(key, result = debug(result, value, res, key, args[i + 1], 5, -165796510), value, res, args[i + 6], 9, -1069501632), result, value, args[i + 11], 14, 643717713), key, result, args[i], 20, -373897302), res = debug(res, key = debug(key, result = debug(result, value, res, key, args[i + 5], 5, -701558691), value, res, args[i + 10], 9, 38016083), result,
                            value, args[i + 15], 14, -660478335), key, result, args[i + 4], 20, -405537848), res = debug(res, key = debug(key, result = debug(result, value, res, key, args[i + 9], 5, 568446438), value, res, args[i + 14], 9, -1019803690), result, value, args[i + 3], 14, -187363961), key, result, args[i + 8], 20, 1163531501), res = debug(res, key = debug(key, result = debug(result, value, res, key, args[i + 13], 5, -1444681467), value, res, args[i + 2], 9, -51403784), result, value, args[i + 7], 14, 1735328473),
                        key, result, args[i + 12], 20, -1926607734), res = fn(res, key = fn(key, result = fn(result, value, res, key, args[i + 5], 4, -378558), value, res, args[i + 8], 11, -2022574463), result, value, args[i + 11], 16, 1839030562), key, result, args[i + 14], 23, -35309556), res = fn(res, key = fn(key, result = fn(result, value, res, key, args[i + 1], 4, -1530992060), value, res, args[i + 4], 11, 1272893353), result, value, args[i + 7], 16, -155497632), key, result, args[i + 10], 23, -1094730640),
                    res = fn(res, key = fn(key, result = fn(result, value, res, key, args[i + 13], 4, 681279174), value, res, args[i], 11, -358537222), result, value, args[i + 3], 16, -722521979), key, result, args[i + 6], 23, 76029189), res = fn(res, key = fn(key, result = fn(result, value, res, key, args[i + 9], 4, -640364487), value, res, args[i + 12], 11, -421815835), result, value, args[i + 15], 16, 530742520), key, result, args[i + 2], 23, -995338651), res = callback(res, key = callback(key, result = callback(result,
                    value, res, key, args[i], 6, -198630844), value, res, args[i + 7], 10, 1126891415), result, value, args[i + 14], 15, -1416354905), key, result, args[i + 5], 21, -57434055), res = callback(res, key = callback(key, result = callback(result, value, res, key, args[i + 12], 6, 1700485571), value, res, args[i + 3], 10, -1894986606), result, value, args[i + 10], 15, -1051523), key, result, args[i + 1], 21, -2054922799), res = callback(res, key = callback(key, result = callback(result, value, res,
                    key, args[i + 8], 6, 1873313359), value, res, args[i + 15], 10, -30611744), result, value, args[i + 6], 15, -1560198380), key, result, args[i + 13], 21, 1309151649), res = callback(res, key = callback(key, result = callback(result, value, res, key, args[i + 4], 6, -145523070), value, res, args[i + 11], 10, -1120210379), result, value, args[i + 2], 15, 718787259), key, result, args[i + 9], 21, -343485551);
                result = $(result, element);
                value = $(value, c);
                res = $(res, block);
                key = $(key, filename);
            }
            return [result, value, res, key];
        }
        /**
         * @param {!Object} bin
         * @return {?}
         */
        function fromCharCode(bin) {
            var i;
            /** @type {string} */
            var char = "";
            /** @type {number} */
            var inputsSize = 32 * bin.length;
            /** @type {number} */
            i = 0;
            for (; i < inputsSize; i = i + 8) {
                /** @type {string} */
                char = char + String.fromCharCode(bin[i >> 5] >>> i % 32 & 255);
            }
            return char;
        }
        /**
         * @param {string} e
         * @return {?}
         */
        function f(e) {
            var a;
            /** @type {!Array} */
            var b = [];
            b[(e.length >> 2) - 1] = void 0;
            /** @type {number} */
            a = 0;
            for (; a < b.length; a = a + 1) {
                /** @type {number} */
                b[a] = 0;
            }
            /** @type {number} */
            var Del = 8 * e.length;
            /** @type {number} */
            a = 0;
            for (; a < Del; a = a + 8) {
                b[a >> 5] |= (255 & e.charCodeAt(a / 8)) << a % 32;
            }
            return b;
        }
        /**
         * @param {string} s
         * @return {?}
         */
        function expect(s) {
            var a;
            var i;
            /** @type {string} */
            var chain = "";
            /** @type {number} */
            i = 0;
            for (; i < s.length; i = i + 1) {
                a = s.charCodeAt(i);
                /** @type {string} */
                chain = chain + ("0123456789abcdef".charAt(a >>> 4 & 15) + "0123456789abcdef".charAt(15 & a));
            }
            return chain;
        }
        /**
         * @param {?} message
         * @return {?}
         */
        function write(message) {
            return unescape(encodeURIComponent(message));
        }
        /**
         * @param {?} a
         * @return {?}
         */
        function g(a) {
            return function(value) {
                return fromCharCode(next(f(value), 8 * value.length));
            }(write(a));
        }
        /**
         * @param {?} e
         * @param {?} source
         * @return {?}
         */
        function bind(e, source) {
            return function(e, params) {
                var i;
                var result;
                var b = f(e);
                /** @type {!Array} */
                var parts = [];
                /** @type {!Array} */
                var ultimates = [];
                parts[15] = ultimates[15] = void 0;
                if (b.length > 16) {
                    b = next(b, 8 * e.length);
                }
                /** @type {number} */
                i = 0;
                for (; i < 16; i = i + 1) {
                    /** @type {number} */
                    parts[i] = 909522486 ^ b[i];
                    /** @type {number} */
                    ultimates[i] = 1549556828 ^ b[i];
                }
                return result = next(parts.concat(f(params)), 512 + 8 * params.length), fromCharCode(next(ultimates.concat(result), 640));
            }(write(e), write(source));
        }
        /**
         * @param {?} id
         * @param {?} name
         * @param {?} args
         * @return {?}
         */
        function init(id, name, args) {
            return name ? args ? bind(name, id) : function(t, b) {
                return expect(bind(t, b));
            }(name, id) : args ? g(id) : function(action) {
                return expect(g(action));
            }(id);
        }
        var result;
        Object.defineProperty(args, "__esModule", {
            value: true
        });
        ! function(exports) {
            if (exports) {
                exports.__esModule;
            }
        }(i(50));
        if (!(void 0 === (result = function() {
                return init;
            }.call(args, i, args, record)))) {
            record.exports = result;
        }
        /** @type {function(?, ?, ?): ?} */
        args.default = init;
    }, function(canCreateDiscussions, e, floor) {
        Object.defineProperty(e, "__esModule", {
            value: true
        });
        var startYNew = floor(11);
        /**
         * @return {?}
         */
        e.default = function() {
            return (0, startYNew.randomGuid)("");
        };
    }, function(canCreateDiscussions, BeautifulProperties, $) {
        Object.defineProperty(BeautifulProperties, "__esModule", {
            value: true
        });
        /**
         * @return {?}
         */
        BeautifulProperties.isSearchTimeout = function() {
            try {
                /** @type {number} */
                var t = +new Date(localStorage.getItem("last_search_time"));
                /** @type {number} */
                var c = +new Date - t;
                return c > 6e5;
            } catch (t) {
                return false;
            }
        };
        /**
         * @return {undefined}
         */
        BeautifulProperties.setLastSearchTime = function() {
            localStorage.setItem("last_search_time", new Date);
        };
        /**
         * @param {string} t
         * @param {!Object} data
         * @return {?}
         */
        BeautifulProperties.translateTripData = function(t, data) {
            var network = data && data[0];
            var doc = {
                type: t,
                displayFlightNo: network.mfwFlightNo || network.flight_no,
                flightNo: network.flight_no,
                departCityName: network.org_city_name,
                departDate: network.dep_date,
                departDateShort: (0, self.toMonth)((0, self.toShortDate)(network.dep_date)),
                destCityName: network.dst_city_name,
                weekDay: (0, self.getChineseWeekDay)(network.dep_date),
                duration: network.fly_time || "",
                durationStr: network.fly_time || "",
                transferNums: data.transfer_nums || "",
                transferTimes: data.transfer_times || "",
                crossDays: network.arr_next_day || "",
                departTime: network.dep_time,
                departAirportName: network.org_airport_name,
                departAirportQuay: network.org_airport_quay,
                destAirportName: network.dst_airport_name,
                destAirportQuay: network.dst_airport_quay,
                depAirport: network.org_airport,
                arrAirport: network.dst_airport,
                destTime: network.arr_time,
                airlineName: network.airline_name,
                allFlightNo: [],
                allAirport: [],
                segments: [],
                segmentsCopy: [],
                hasShareFlight: network.flight_share,
                needTransfer: false,
                hasStopPoints: false
            };
            return data.forEach(function(tok, canCreateDiscussions) {
                if (doc.allFlightNo.indexOf(tok.flight_no) < 0) {
                    doc.allFlightNo.push(tok.flight_no);
                }
                if (doc.allAirport.indexOf(tok.org_airport_code) < 0) {
                    doc.allAirport.push(tok.org_airport_code);
                }
                if (doc.allAirport.indexOf(tok.dst_airport_code) < 0) {
                    doc.allAirport.push(tok.dst_airport_code);
                }
                var breakToken = tok.flight_share;
                /** @type {!Array} */
                var slashes = [];
                if (breakToken) {
                    /** @type {boolean} */
                    doc.hasShareFlight = true;
                }
                if (tok.stop_num) {
                    /** @type {boolean} */
                    doc.hasStopPoints = true;
                    if (tok.stop_infos) {
                        tok.stop_infos.forEach(function(loc) {
                            slashes.push(loc.city_name);
                        });
                    }
                }
                doc.segments.push({
                    otaId: tok.ota_id,
                    departTime: tok.dep_time,
                    departAirportName: tok.org_airport_name,
                    departAirportQuay: tok.org_airport_quay,
                    destAirportName: tok.dst_airport_name,
                    destAirportQuay: tok.dst_airport_quay,
                    destTime: tok.arr_time || "",
                    airlineName: tok.airline_name,
                    flightNo: tok.flight_no,
                    displayFlightNo: tok.mfwFlightNo || tok.flight_no,
                    planeSize: tok.plane_size,
                    planeType: tok.plane_type,
                    stop: tok.stop_num,
                    stopNum: tok.stop_num,
                    meal: tok.meal,
                    correctness: tok.correctness,
                    isShareFlight: breakToken,
                    shareFlightNo: tok.operating_flight_no || "",
                    duration: tok.fly_time || "",
                    durationStr: tok.fly_time || "",
                    hasNext: false,
                    needTransfer: false,
                    transferTimeIsTight: true,
                    transferDuration: "",
                    crossDays: tok.arr_next_day || 0,
                    stopPoints: slashes,
                    depCrossDays: tok.depCrossDays || 0
                });
                if (doc.segments.length >= 1) {
                    /** @type {number} */
                    doc.segments.length = 1;
                }
            }), doc;
        };
        /**
         * @param {!Function} str
         * @return {?}
         */
        BeautifulProperties.filterNum = function(str) {
            return !!/\d+/.test(str) && str;
        };
        ! function(exports) {
            if (exports) {
                exports.__esModule;
            }
        }($(19));
        var self = $(31);
    }, function(module, canCreateDiscussions) {
        module.exports = window.axios;
    }, , , , , , , , function(module, canCreateDiscussions) {
        module.exports = window.BScroll;
    }, , , , , , , , , , , function(canCreateDiscussions, __webpack_exports__, __webpack_require__) {
        /**
         * @return {?}
         */
        var render = function() {
            var _vm = this;
            var currHeight = _vm.$createElement;
            var _h = _vm._self._c || currHeight;
            return _h("div", {
                staticClass: "v-list-com-titlebar"
            }, [_h("div", {
                staticClass: "v-list-com-titlebar-head"
            }, [_h("div", {
                staticClass: "v-list-com-titlebar-head-title"
            }, [_h("div", {
                staticClass: "btn-back",
                on: {
                    click: _vm.onBack
                }
            }), _vm._t("title", [_vm._v(_vm._s(_vm.title))])], 2), _h("div", {
                staticClass: "v-list-com-titlebar-head-content"
            }, [_vm._t("head-content")], 2)]), _h("div", {
                staticClass: "v-list-com-titlebar-body"
            }, [_vm._t("default")], 2), _vm._t("dialog")], 2);
        };
        /** @type {!Array} */
        var n = [];
        /** @type {boolean} */
        render._withStripped = true;
        __webpack_require__.d(__webpack_exports__, "a", function() {
            return render;
        });
        __webpack_require__.d(__webpack_exports__, "b", function() {
            return n;
        });
    }, function(canCreateDiscussions, __webpack_exports__, __webpack_require__) {
        /**
         * @return {?}
         */
        var render = function() {
            var _vm = this;
            var _h = _vm.$createElement;
            var _c = _vm._self._c || _h;
            return _c("div", {
                staticClass: "lowPrice-wrap"
            }, [_c("div", {
                ref: "lowPriceWrap",
                staticClass: "l"
            }, [_c("ul", _vm._l(_vm.lowPriceList, function(item, awsKey) {
                return _c("li", {
                    key: awsKey,
                    ref: "lowPriceItem",
                    refInFor: true,
                    class: {
                        current: item.current
                    },
                    on: {
                        click: function(val) {
                            _vm.toggleDate(item, 1);
                        }
                    }
                }, [_c("p", [_vm._v(_vm._s(item.day))]), _c("p", [_vm._v(_vm._s(item.current ? item.month + "\u6708" + item.date + "\u65e5" : item.date))]), _c("p", [_vm._v(_vm._s(item.price))])]);
            }))]), _c("div", {
                staticClass: "r",
                on: {
                    click: _vm.calendarShow
                }
            }, [_vm._m(0)])]);
        };
        /** @type {!Array} */
        var n = [function() {
            var canvasHeight = this.$createElement;
            var h = this._self._c || canvasHeight;
            return h("div", {
                staticClass: "r-c"
            }, [this._v("\n      \u4f4e\u4ef7"), h("br"), this._v("\n      \u65e5\u5386"), h("br"), h("img", {
                attrs: {
                    src: __webpack_require__(184)
                }
            })]);
        }];
        /** @type {boolean} */
        render._withStripped = true;
        __webpack_require__.d(__webpack_exports__, "a", function() {
            return render;
        });
        __webpack_require__.d(__webpack_exports__, "b", function() {
            return n;
        });
    }, function(canCreateDiscussions, __webpack_exports__, __webpack_require__) {
        /**
         * @return {?}
         */
        var render = function() {
            var _vm = this;
            var _h = _vm.$createElement;
            var h = _vm._self._c || _h;
            return h("div", {
                staticClass: "filter-wrap"
            }, [h("div", {
                staticClass: "filter-show"
            }, [h("div", {
                staticClass: "filter-show-c"
            }, [h("div", {
                staticClass: "one-item first",
                class: {
                    on: _vm.currentConditionTemp
                },
                on: {
                    click: _vm.filterPartShow
                }
            }, [_vm._m(0)]), _vm._l(_vm.sortList, function(item) {
                return h("div", {
                    key: item.id,
                    staticClass: "one-item second",
                    class: {
                        on: item.select,
                            second: 0 === item.type,
                            third: 1 === item.type
                    },
                    on: {
                        click: function(val) {
                            _vm.sortSelcet(item);
                        }
                    }
                }, [h("div", {
                    staticClass: "one-item-c"
                }, [h("span", [_vm._v(_vm._s(_vm.currentShowText(item)))])])]);
            })], 2)]), h("div", {
                directives: [{
                    name: "show",
                    rawName: "v-show",
                    value: _vm.selectShow,
                    expression: "selectShow"
                }],
                staticClass: "new-filter-wrap",
                on: {
                    touchmove: function(event) {
                        event.preventDefault();
                    }
                }
            }, [h("div", {
                staticClass: "filter-title"
            }, [h("span", {
                staticClass: "icon",
                on: {
                    click: _vm.filterPartHide
                }
            }, [h("i")]), h("p", [_vm._v("\u7b5b\u9009")])]), h("tui-better-scroller", {
                ref: "filter-scroller",
                staticClass: "filter-content"
            }, [h("div", _vm._l(_vm.allFilterConditions, function(item) {
                return h("div", {
                    key: item.id,
                    staticClass: "one-item-wrap"
                }, [h("p", {
                    staticClass: "one-item-title"
                }, [_vm._v(_vm._s(item.name))]), h("div", {
                    staticClass: "item-content"
                }, [h("ul", _vm._l(item.data, function(value, awsKey) {
                    return h("li", {
                        key: awsKey,
                        on: {
                            click: function(val) {
                                _vm.chooseCondition(item.id, value);
                            }
                        }
                    }, [h("span", {
                        staticClass: "select-icon",
                        class: {
                            select: _vm.selectJudge(item.id, value)
                        }
                    }), h("p", {
                        staticClass: "item-text"
                    }, [_vm._v(_vm._s(value))])]);
                }))])]);
            }))]), h("div", {
                staticClass: "filter-footer"
            }, [h("div", {
                staticClass: "reset-btn-wrap"
            }, [h("div", {
                staticClass: "reset-btn",
                on: {
                    click: _vm.filterReset
                }
            }, [_vm._v("\u91cd\u7f6e")])]), h("div", {
                staticClass: "confirm-btn-wrap"
            }, [h("div", {
                staticClass: "confirm-btn",
                on: {
                    click: _vm.resultShow
                }
            }, [_vm._v("\u786e\u5b9a")])])])], 1)]);
        };
        /** @type {!Array} */
        var n = [function() {
            var _h = this.$createElement;
            var _c = this._self._c || _h;
            return _c("div", {
                staticClass: "one-item-c"
            }, [_c("span", [this._v("\u7b5b\u9009")])]);
        }];
        /** @type {boolean} */
        render._withStripped = true;
        __webpack_require__.d(__webpack_exports__, "a", function() {
            return render;
        });
        __webpack_require__.d(__webpack_exports__, "b", function() {
            return n;
        });
    }, , , function(canCreateDiscussions, __webpack_exports__, __webpack_require__) {
        /**
         * @return {?}
         */
        var render = function() {
            var self = this;
            var _h = self.$createElement;
            var h = self._self._c || _h;
            return h("list-titlebar", {
                on: {
                    onback: self.onback
                }
            }, [h("template", {
                slot: "title"
            }, [self.listTitlebarInfo.departCity ? h("span", {
                staticClass: "titlebar-title"
            }, [h("span", [self._v(self._s(self.listTitlebarInfo.tripType))]), h("span", [self._v(self._s(self.listTitlebarInfo.departCity))]), h("img", {
                directives: [{
                    name: "show",
                    rawName: "v-show",
                    value: self.listTitlebarInfo.departCity,
                    expression: "listTitlebarInfo.departCity"
                }],
                attrs: {
                    src: __webpack_require__(233)
                }
            }), h("span", [self._v(self._s(self.listTitlebarInfo.destCity))])]) : h("span", [self._v("\u56fd\u5185\u673a\u7968\u5217\u8868")])]), h("template", {
                slot: "head-content"
            }, [self.tripType.oneWay && self.lowPriceList.length ? h("low-price-calendar", {
                attrs: {
                    lowPriceList: self.lowPriceList,
                    scrollLeft: self.calendarScrollLeft,
                    departDate: self.urlParam.departDate,
                    departCode: self.urlParam.departCode,
                    destCode: self.urlParam.destCode
                },
                on: {
                    "toggle-date": self.toggleDate
                }
            }) : self._e(), self.goTripInfo && self.tripType.retTrip && !self.mfwLoading ? h("div", {
                staticClass: "go-trip-info"
            }, [h("span", {
                staticClass: "name"
            }, [self._v("\u53bb")]), h("span", {
                staticClass: "info"
            }, [self._v(self._s(self.goTripInfo.dateInfo))]), h("span", {
                staticClass: "info"
            }, [self._v(self._s(self.goTripInfo.timeSlot))]), h("span", {
                staticClass: "info"
            }, [self._v(self._s(self.goTripInfo.airlineCompanyName))])]) : self._e()], 1), h("div", {
                ref: "scroll-wrap",
                staticClass: "scroll-wrap"
            }, [self.lowPriceList.length || self.formatFlightList.length ? h("div", {
                staticClass: "progress-wrap"
            }, [h("div", {
                staticClass: "progress",
                style: {
                    width: self.progressWidth + "%",
                    opacity: self.loadingMore ? 1 : 0,
                    display: self.tripType.retTrip ? "block" : self.loadingMore ? "block" : "none"
                }
            })]) : self._e(), h("flight-list", {
                ref: "flight-list",
                on: {
                    select: self.select,
                    listScroll: self.listScroll
                }
            })], 1), h("template", {
                slot: "dialog"
            }, [!self.formatFlightList.length || self.mfwLoading || self.loadingMore ? self._e() : h("list-filter", {
                attrs: {
                    startAirPortList: self.startAirPortList,
                    arrAirPortList: self.arrAirPortList,
                    airlineCompanyList: self.airlineCompanyList
                },
                on: {
                    "filter-condition": self.filterCondition,
                    "current-sort": self.currentSort
                }
            })], 1)], 2);
        };
        /** @type {!Array} */
        var n = [];
        /** @type {boolean} */
        render._withStripped = true;
        __webpack_require__.d(__webpack_exports__, "a", function() {
            return render;
        });
        __webpack_require__.d(__webpack_exports__, "b", function() {
            return n;
        });
    }, , function(canCreateDiscussions, __webpack_exports__, __webpack_require__) {
        /**
         * @return {?}
         */
        var render = function() {
            var self = this;
            var _h = self.$createElement;
            var _c = self._self._c || _h;
            return _c("tui-better-scroller", {
                ref: "flightListWrap",
                staticClass: "flight-list-wrap",
                attrs: {
                    options: self.betterScrollerOptions
                }
            }, [_c("div", {
                staticClass: "flight-list"
            }, [self.flightList.length ? _c("ul", {
                staticClass: "list-row-wrap"
            }, self._l(self.flightList, function(item) {
                return _c("li", {
                    key: item.flightNo,
                    ref: "flightListItem",
                    refInFor: true,
                    staticClass: "list-row",
                    on: {
                        click: function(evt) {
                            self.$emit("select", item, evt);
                        }
                    }
                }, [self.UTIL.isQa || self.UTIL.isDev || self.UTIL.isPre ? _c("p", {
                    staticStyle: {
                        position: "absolute",
                        left: "0",
                        top: "0"
                    }
                }, [self._v(self._s(item.merchantId))]) : self._e(), _c("div", {
                    staticClass: "flight-info"
                }, [_c("div", {
                    staticClass: "air-line-info"
                }, [_c("div", {
                    staticClass: "airpot-info from-info"
                }, [_c("p", {
                    staticClass: "time-font"
                }, [self._v(self._s(item.start.time))]), _c("p", {
                    staticClass: "airpot"
                }, [self._v(self._s(item.start.airport) + self._s(item.start.terminal))])]), _c("div", {
                    staticClass: "time-info",
                    class: {
                        "time-info-pb": !item.stopInfo.length
                    }
                }, [_c("p", {
                    staticClass: "howlong"
                }, [self._v(self._s(item.duration.text))]), _c("div", {
                    staticClass: "plane-info-wrap"
                }, [_c("div", {
                    staticClass: "plane-info"
                }, [item.stopInfo && item.stopInfo.length ? _c("span", {
                    staticClass: "line-icon"
                }, [self._v("\u7ecf\u505c")]) : self._e()])]), self._l(item.stopInfo, function(name, awsKey) {
                    return item.stopInfo.length && item.stopInfo.length < 2 ? _c("p", {
                        key: awsKey,
                        staticClass: "transfer-place"
                    }, [self._v(self._s(name))]) : self._e();
                }), item.stopInfo.length && item.stopInfo.length >= 2 ? _c("p", {
                    staticClass: "transfer-place"
                }, [self._v(self._s(item.stopInfo.length) + "\u6b21")]) : self._e()], 2), _c("div", {
                    staticClass: "airpot-info to-info"
                }, [_c("div", {
                    staticClass: "time-font-wrap"
                }, [_c("p", {
                    staticClass: "time-font"
                }, [self._v(self._s(item.arrive.time))]), item.addDay ? _c("span", {
                    staticClass: "add-day"
                }, [self._v(self._s(item.addDay))]) : self._e()]), _c("p", {
                    staticClass: "airpot"
                }, [self._v(self._s(item.arrive.airport) + self._s(item.arrive.terminal))])])]), _c("div", {
                    staticClass: "company-info"
                }, [item.airlineCompany.logoUrl ? _c("span", {
                    staticClass: "company-logo",
                    style: {
                        "background-image": "url(" + item.airlineCompany.logoUrl + ")"
                    }
                }) : self._e(), _c("span", {
                    staticClass: "company-name"
                }, [self._v(self._s(item.airlineCompany.name))]), _c("span", {
                    staticClass: "flight-no"
                }, [self._v(self._s(item.showFlightNo))]), self._l(item.other, function(name, awsKey) {
                    return _c("span", {
                        key: awsKey,
                        staticClass: "flight-share"
                    }, [self._v(self._s(name))]);
                }), _c("span", {
                    staticClass: "plane-type"
                }, [self._v(self._s(item.planeType))])], 2)]), _c("div", {
                    staticClass: "price-info"
                }, [_c("p", {
                    staticClass: "price"
                }, [_c("span", {
                    staticClass: "price-icon"
                }, [self._v("\u00a5")]), self._v(self._s(item.priceInfo.price))]), item.priceInfo.chdPrice ? _c("p", {
                    staticClass: "price-type"
                }, [_c("span", [self._v("\u513f\u7ae5")]), _c("span", {
                    staticClass: "price-icon"
                }, [self._v("\u00a5")]), self._v(self._s(item.priceInfo.chdPrice))]) : self._e(), item.priceInfo.coupon > 0 ? _c("p", {
                    staticClass: "coupon-price"
                }, [self._v("\u7acb\u51cf\u00a5" + self._s(item.priceInfo.coupon))]) : self._e()])]);
            })) : self._e(), self.flightList.length <= 0 ? _c("div", {
                staticClass: "no-data"
            }, [_c("div", {
                staticClass: "icon-wifi"
            }), _c("div", {
                staticClass: "text-tip"
            }, [self._v("\u6682\u65e0\u822a\u73ed\u6570\u636e")])]) : self._e()])]);
        };
        /** @type {!Array} */
        var n = [];
        /** @type {boolean} */
        render._withStripped = true;
        __webpack_require__.d(__webpack_exports__, "a", function() {
            return render;
        });
        __webpack_require__.d(__webpack_exports__, "b", function() {
            return n;
        });
    }, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , function(canCreateDiscussions, isSlidingUp, i) {}, , , , , , , , function(canCreateDiscussions, self, saveNotifs) {
        Object.defineProperty(self, "__esModule", {
            value: true
        });
        var _deepAssign2 = function(obj) {
            return obj && obj.__esModule ? obj : {
                default: obj
            };
        }(saveNotifs(121));
        /**
         * @param {string} url
         * @return {?}
         */
        self.loadJs = function(url) {
            var toggle = !(arguments.length > 1 && void 0 !== arguments[1]) || arguments[1];
            return new _deepAssign2.default(function(notify_success, down) {
                /** @type {!Element} */
                var node = document.createElement("script");
                /** @type {string} */
                node.type = "text/javascript";
                node.async = toggle;
                /** @type {function(): undefined} */
                node.onload = node.onreadystatechange = function() {
                    if (!(this.readyState && "loaded" !== this.readyState && "complete" !== this.readyState)) {
                        /** @type {null} */
                        node.onload = node.onreadystatechange = null;
                        notify_success();
                    }
                };
                /** @type {!Function} */
                node.onerror = down;
                /** @type {string} */
                node.src = url;
                document.getElementsByTagName("head")[0].appendChild(node);
            });
        };
    }, , , , , function(canCreateDiscussions, e, require) {
        /**
         * @param {!Object} obj
         * @return {?}
         */
        function _interopRequireDefault(obj) {
            return obj && obj.__esModule ? obj : {
                default: obj
            };
        }
        Object.defineProperty(e, "__esModule", {
            value: true
        });
        var _deepAssign2 = _interopRequireDefault(require(49));
        var _noframeworkWaypoints2 = _interopRequireDefault(require(32));
        var _custom2 = _interopRequireDefault(require(169));
        var _UiIcon2 = _interopRequireDefault(require(168));
        var util = require(11);
        var leadModel = require(52);
        var JSLoader = require(165);
        /** @type {!Array} */
        var jsApiList = ["checkJsApi", "onMenuShareTimeline", "onMenuShareAppMessage", "onMenuShareQQ", "onMenuShareWeibo", "hideMenuItems", "showMenuItems", "hideAllNonBaseMenuItem", "showAllNonBaseMenuItem", "translateVoice", "startRecord", "stopRecord", "onRecordEnd", "playVoice", "pauseVoice", "stopVoice", "uploadVoice", "downloadVoice", "chooseImage", "previewImage", "uploadImage", "downloadImage", "getNetworkType", "openLocation", "getLocation", "hideOptionMenu", "showOptionMenu", "closeWindow",
            "scanQRCode", "chooseWXPay", "openProductSpecificView", "addCard", "chooseCard", "openCard"
        ];
        var doc = window.document;
        var newOrg = new(function() {
            /**
             * @return {undefined}
             */
            function ready() {
                var self = this;
                (0, _custom2.default)(this, ready);
                /** @type {null} */
                this.weChatConfig = null;
                this.eventCache = {};
                this.shareInfo = {
                    title: "",
                    url: "",
                    image: "",
                    description: ""
                };
                /** @type {boolean} */
                this._ready = false;
                if ((0, util.isWeixin)()) {
                    if ("undefined" == typeof WeixinJSBridge) {
                        doc.addEventListener("WeixinJSBridgeReady", function() {
                            self._onReady();
                        }, false);
                    } else {
                        this._onReady();
                    }
                }
            }
            return (0, _UiIcon2.default)(ready, [{
                key: "_onReady",
                value: function() {
                    var _this = this;
                    if (!this._ready && "undefined" == typeof wx) {
                        return (0, JSLoader.loadJs)("//wpstatic.mafengwo.net/webpack/trans_static/js/jweixin-1.2.0.js").then(function() {
                            return _this._onReady();
                        });
                    }
                    this._queryConfig().then(function(data) {
                        /** @type {!Object} */
                        _this.weChatConfig = data;
                        var wx = window.wx;
                        wx.config({
                            debug: false,
                            appId: data.appId,
                            timestamp: parseInt(data.timestamp, 10),
                            nonceStr: data.nonceStr,
                            signature: data.signature,
                            jsApiList: jsApiList
                        });
                        wx.ready(function() {
                            _this._setShareInfo();
                        });
                    });
                    /** @type {boolean} */
                    this._ready = true;
                }
            }, {
                key: "_queryConfig",
                value: function() {
                    return (0, leadModel.get)("//m.mafengwo.cn/sales/activity/flightpromotion/ajax_data/WeiXinShare", {
                        url: location.href
                    }).then(function(storeCfg) {
                        return storeCfg.data.data;
                    });
                }
            }, {
                key: "_getMetaShareInfo",
                value: function() {
                    var options = {
                        title: "",
                        image: "",
                        description: "",
                        url: ""
                    };
                    return (0, _noframeworkWaypoints2.default)(options).forEach(function(i) {
                        var currMetaTag = doc.querySelector('meta[property="og:' + i + '"]');
                        if (currMetaTag) {
                            options[i] = currMetaTag.getAttribute("content") || "";
                        }
                    }), {
                        img_url: options.image || "https://wpstatic.mafengwo.net/webpack/trans_static/img/mfw-logo-new.png",
                        img_width: 150,
                        img_height: 150,
                        link: options.url || location.href,
                        desc: options.description || "",
                        title: options.title || doc.title || "\u9a6c\u8702\u7a9d"
                    };
                }
            }, {
                key: "_dispatchEvent",
                value: function(e) {
                    if ((0, util.isFunction)(doc.dispatchEvent) && (0, util.isFunction)(doc.createEvent)) {
                        var event = this.eventCache[e];
                        if (!event) {
                            (event = doc.createEvent("Event")).initEvent(e, true, true);
                            this.eventCache[e] = event;
                        }
                        doc.dispatchEvent(event);
                    }
                }
            }, {
                key: "_setShareInfo",
                value: function() {
                    var _this = this;
                    var data = this._getMetaShareInfo();
                    var $ = window.wx;
                    ["Timeline", "AppMessage", "QQ", "Weibo"].forEach(function(end) {
                        /** @type {string} */
                        var type = "onMenuShare" + end;
                        if (type in $) {
                            $[type]({
                                title: data.title,
                                desc: data.desc,
                                link: data.link,
                                imgUrl: data.img_url,
                                success: function() {
                                    /** @type {string} */
                                    var statement = "wx:onMenuShare" + end;
                                    _this._dispatchEvent(statement);
                                }
                            });
                        }
                    });
                }
            }, {
                key: "setShareInfo",
                value: function() {
                    var artistTrack = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
                    var e = this._getMetaShareInfo();
                    this.shareInfo = (0, _deepAssign2.default)(e, artistTrack);
                }
            }]), ready;
        }());
        e.default = newOrg;
    }, , function(canCreateDiscussions, isSlidingUp, __webpack_require__) {
        var __WEBPACK_IMPORTED_MODULE_20_date_fns_min__ = __webpack_require__(65);
        __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_20_date_fns_min__).a;
    }, , function(canCreateDiscussions, isSlidingUp, __webpack_require__) {
        var __WEBPACK_IMPORTED_MODULE_20_date_fns_min__ = __webpack_require__(66);
        __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_20_date_fns_min__).a;
    }, function(canCreateDiscussions, context, $) {
        $.r(context);
        var tParentMatrix = $(109);
        var a = $(68);
        var k;
        for (k in a) {
            if ("default" !== k) {
                (function(m) {
                    $.d(context, m, function() {
                        return a[m];
                    });
                })(k);
            }
        }
        $(174);
        var self = $(0);
        var module = Object(self.a)(a.default, tParentMatrix.a, tParentMatrix.b, false, null, null, null);
        /** @type {string} */
        module.options.__file = "src/pages/html/list/components/list-titlebar.vue";
        context.default = module.exports;
    }, , function(canCreateDiscussions, isSlidingUp, __webpack_require__) {
        var __WEBPACK_IMPORTED_MODULE_20_date_fns_min__ = __webpack_require__(69);
        __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_20_date_fns_min__).a;
    }, function(canCreateDiscussions, context, $) {
        $.r(context);
        var tParentMatrix = $(111);
        var a = $(71);
        var k;
        for (k in a) {
            if ("default" !== k) {
                (function(m) {
                    $.d(context, m, function() {
                        return a[m];
                    });
                })(k);
            }
        }
        $(177);
        var self = $(0);
        var module = Object(self.a)(a.default, tParentMatrix.a, tParentMatrix.b, false, null, null, null);
        /** @type {string} */
        module.options.__file = "src/pages/html/list/components/listFilter.vue";
        context.default = module.exports;
    }, , function(canCreateDiscussions, isSlidingUp, __webpack_require__) {
        var __WEBPACK_IMPORTED_MODULE_20_date_fns_min__ = __webpack_require__(72);
        __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_20_date_fns_min__).a;
    }, function(canCreateDiscussions, context, $) {
        $.r(context);
        var tParentMatrix = $(116);
        var a = $(74);
        var k;
        for (k in a) {
            if ("default" !== k) {
                (function(m) {
                    $.d(context, m, function() {
                        return a[m];
                    });
                })(k);
            }
        }
        $(180);
        var self = $(0);
        var module = Object(self.a)(a.default, tParentMatrix.a, tParentMatrix.b, false, null, null, null);
        /** @type {string} */
        module.options.__file = "src/pages/html/list/components/flightList.vue";
        context.default = module.exports;
    }, , function(canCreateDiscussions, isSlidingUp, __webpack_require__) {
        var __WEBPACK_IMPORTED_MODULE_20_date_fns_min__ = __webpack_require__(75);
        __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_20_date_fns_min__).a;
    }, function(mixin, canCreateDiscussions) {
        /** @type {string} */
        mixin.exports = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAMCAYAAAEVC61tAAAAAXNSR0IArs4c6QAAATJJREFUKBWdkr9OwzAQxu2QvkweIEsU2MvMCIKp6sKfxVG2jEmmikpUGRADr8ATIGXoS/AKLJAsacN3EWe5rqtG9WLfd7/7cmdHCHsppXpbEwLqz6CaaS2afFVVE5EkyYxFnN/4PCRMQSK47Pv+oyxLqSnjQDDyV1qCMDObIMDZCFekaToH0HGs96FTHR0+nAVB0EVR9F3X9drGsizzwjDcxnH87mEID8ACn7s3QYKaptlIKS/yPP/SkwLcAnxE4bMJFUXxSQYapIBgXMUTXBbkxBDl9hbBuJpzOyGRuEP1CxIKDksbOBb/t7mCx43v+/HQIj0KWluhmOIHmmeMUdu2r6i7BfsLwymNtDPzGGPqyGXEDewYsugyPmbEtU5DTlrGJOvRmDlpx398DfO9F3WZ/QHq47GluibAYQAAAABJRU5ErkJggg==";
    }, function(canCreateDiscussions, context, $) {
        $.r(context);
        var tParentMatrix = $(110);
        var a = $(77);
        var k;
        for (k in a) {
            if ("default" !== k) {
                (function(m) {
                    $.d(context, m, function() {
                        return a[m];
                    });
                })(k);
            }
        }
        $(183);
        var self = $(0);
        var module = Object(self.a)(a.default, tParentMatrix.a, tParentMatrix.b, false, null, null, null);
        /** @type {string} */
        module.options.__file = "src/pages/html/list/components/lowPriceCalendar.vue";
        context.default = module.exports;
    }, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , function(mixin, canCreateDiscussions) {
        /** @type {string} */
        mixin.exports = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAACU0lEQVRoQ+2Vy2sTYRTFz5mkDxoqFRR3JTHRlMamiG7Ev8C1gkupIAgVNxaXXRSkCqKIIK587ETcuxRUBJH6SoIxRjOVLHQhpcGqzeO7klbBSmkyufClhS/bufee8ztnyBBb/Mct7h8OoNsNugZcA8oE3CukDFC97hpQR6g84BoIEKAXGxm/RpEjgFyoLi3cK5fLPwPsrztqrYH46GjCNMIf/rioAbgbapiLxWL2owbCGsDu5L6DAu/FP2brAjwBvZN+/rXfKUQ3AVY9U4ow4WOlwqssgEZQkO4DrDr+QmDGLFdu+77/KwjE5gAQEYAVkNdL799MA5B2ITYHwBq3vI9q42yplP3aDoQ1gHgyddgg9LSVKRE0POKx52Gq+O7ty1bzVgBSqVTvj1r4CiiTrQw1n4uIIekbkTPzhczDjXZWAKLRaH+ob+iAEXNKPIxRMNSOULszBAYFsgNgwMDkO4hzAyFzJ5fLVdfT4650OhJZ5rSBTBKItGvK2pxgkeTNeq+59DmTWfhfl9G948dBuUVgwJqp4ELN9B8Jq6f9fH7NR4/RkfQzCg4Fv2l9QyB4LpAJv5DJ/1VnLJmuABi0bqdzwTwNZj5t63mAublaE6BJk+z8nv1NgXwDvct+fekqY3vSU/AwCyBs34pKsUbgPIeHx7aH+3lDiKMAelQn7S/Pr/wvJxL7d9ZD9QkQJyiMA+iz7yWgomBRyNmAH5aAIhbGHYCFkDeUcA24BpQJuFdIGaB63TWgjlB5wDWgDFC97hpQR6g84BpQBqhedw2oI1Qe+A2Op7OqWyXkOQAAAABJRU5ErkJggg==";
    }, function(canCreateDiscussions, context, $) {
        $.r(context);
        var tParentMatrix = $(114);
        var a = $(79);
        var k;
        for (k in a) {
            if ("default" !== k) {
                (function(m) {
                    $.d(context, m, function() {
                        return a[m];
                    });
                })(k);
            }
        }
        $(172);
        var self = $(0);
        var module = Object(self.a)(a.default, tParentMatrix.a, tParentMatrix.b, false, null, null, null);
        /** @type {string} */
        module.options.__file = "src/pages/html/list/App.vue";
        context.default = module.exports;
    }, function(canCreateDiscussions, isSlidingUp, floor) {
        /**
         * @param {!Object} obj
         * @return {?}
         */
        function _interopRequireDefault(obj) {
            return obj && obj.__esModule ? obj : {
                default: obj
            };
        }
        var _vue2 = _interopRequireDefault(floor(30));
        var startYNew = floor(42);
        var _store2 = _interopRequireDefault(floor(234));
        floor(170);
        floor(157);
        (0, startYNew.installVue)(_vue2.default);
        window._app = new _vue2.default({
            el: "#app",
            render: function(createElement) {
                return createElement(_store2.default);
            }
        });
    }],
    [
        [235, 0, 1]
    ]
]);