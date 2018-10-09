/**
 * @license
 Browser bundle of nunjucks 3.1.2 (slim, only works with precompiled templates)  Copyright (c) 2016 Jed Watson.
  Licensed under the MIT License (MIT), see
  http://jedwatson.github.io/classnames
 @overview es6-promise - a tiny implementation of Promises/A+.
 @copyright Copyright (c) 2014 Yehuda Katz, Tom Dale, Stefan Penner and contributors (Conversion to ES6 API by Jake Archibald)
 @license   Licensed under MIT license
            See https://raw.githubusercontent.com/stefanpenner/es6-promise/master/LICENSE
 @version   v4.2.4+314e4831
*/
'use strict';
webpackJsonp([5], {
  "+2u5" : function(module, level, n) {
    var result;
    var a = n("gf5I");
    !function(exports) {
      if (exports) {
        exports.__esModule;
      }
    }(a);
    !function(canCreateDiscussions) {
      /**
       * @param {number} a
       * @param {number} b
       * @return {?}
       */
      function i(a, b) {
        /** @type {number} */
        var n = (65535 & a) + (65535 & b);
        return (a >> 16) + (b >> 16) + (n >> 16) << 16 | 65535 & n;
      }
      /**
       * @param {number} a
       * @param {number} b
       * @return {?}
       */
      function callback(a, b) {
        return a << b | a >>> 32 - b;
      }
      /**
       * @param {number} a
       * @param {number} c
       * @param {number} n
       * @param {number} e
       * @param {number} f
       * @param {number} s
       * @return {?}
       */
      function get(a, c, n, e, f, s) {
        return i(callback(i(i(c, a), i(e, s)), f), n);
      }
      /**
       * @param {number} m
       * @param {number} d
       * @param {number} a
       * @param {number} b
       * @param {undefined} c
       * @param {number} callback
       * @param {number} next
       * @return {?}
       */
      function fn(m, d, a, b, c, callback, next) {
        return get(d & a | ~d & b, m, d, c, callback, next);
      }
      /**
       * @param {number} a
       * @param {number} b
       * @param {number} c
       * @param {number} d
       * @param {undefined} s
       * @param {number} callback
       * @param {number} next
       * @return {?}
       */
      function md5_gg(a, b, c, d, s, callback, next) {
        return get(b & d | c & ~d, a, b, s, callback, next);
      }
      /**
       * @param {number} d
       * @param {number} x
       * @param {number} y
       * @param {number} z
       * @param {undefined} c
       * @param {number} callback
       * @param {number} arg1
       * @return {?}
       */
      function setTimeout(d, x, y, z, c, callback, arg1) {
        return get(x ^ y ^ z, d, x, c, callback, arg1);
      }
      /**
       * @param {number} y
       * @param {number} d
       * @param {number} a
       * @param {number} b
       * @param {undefined} c
       * @param {number} callback
       * @param {number} next
       * @return {?}
       */
      function p(y, d, a, b, c, callback, next) {
        return get(a ^ (d | ~b), y, d, c, callback, next);
      }
      /**
       * @param {!Object} args
       * @param {number} n
       * @return {?}
       */
      function f(args, n) {
        args[n >> 5] |= 128 << n % 32;
        /** @type {number} */
        args[14 + (n + 64 >>> 9 << 4)] = n;
        var index;
        var h;
        var q;
        var r;
        var m;
        /** @type {number} */
        var a = 1732584193;
        /** @type {number} */
        var b = -271733879;
        /** @type {number} */
        var c = -1732584194;
        /** @type {number} */
        var d = 271733878;
        /** @type {number} */
        index = 0;
        for (; index < args.length; index = index + 16) {
          h = a;
          q = b;
          r = c;
          m = d;
          a = fn(a, b, c, d, args[index], 7, -680876936);
          d = fn(d, a, b, c, args[index + 1], 12, -389564586);
          c = fn(c, d, a, b, args[index + 2], 17, 606105819);
          b = fn(b, c, d, a, args[index + 3], 22, -1044525330);
          a = fn(a, b, c, d, args[index + 4], 7, -176418897);
          d = fn(d, a, b, c, args[index + 5], 12, 1200080426);
          c = fn(c, d, a, b, args[index + 6], 17, -1473231341);
          b = fn(b, c, d, a, args[index + 7], 22, -45705983);
          a = fn(a, b, c, d, args[index + 8], 7, 1770035416);
          d = fn(d, a, b, c, args[index + 9], 12, -1958414417);
          c = fn(c, d, a, b, args[index + 10], 17, -42063);
          b = fn(b, c, d, a, args[index + 11], 22, -1990404162);
          a = fn(a, b, c, d, args[index + 12], 7, 1804603682);
          d = fn(d, a, b, c, args[index + 13], 12, -40341101);
          c = fn(c, d, a, b, args[index + 14], 17, -1502002290);
          b = fn(b, c, d, a, args[index + 15], 22, 1236535329);
          a = md5_gg(a, b, c, d, args[index + 1], 5, -165796510);
          d = md5_gg(d, a, b, c, args[index + 6], 9, -1069501632);
          c = md5_gg(c, d, a, b, args[index + 11], 14, 643717713);
          b = md5_gg(b, c, d, a, args[index], 20, -373897302);
          a = md5_gg(a, b, c, d, args[index + 5], 5, -701558691);
          d = md5_gg(d, a, b, c, args[index + 10], 9, 38016083);
          c = md5_gg(c, d, a, b, args[index + 15], 14, -660478335);
          b = md5_gg(b, c, d, a, args[index + 4], 20, -405537848);
          a = md5_gg(a, b, c, d, args[index + 9], 5, 568446438);
          d = md5_gg(d, a, b, c, args[index + 14], 9, -1019803690);
          c = md5_gg(c, d, a, b, args[index + 3], 14, -187363961);
          b = md5_gg(b, c, d, a, args[index + 8], 20, 1163531501);
          a = md5_gg(a, b, c, d, args[index + 13], 5, -1444681467);
          d = md5_gg(d, a, b, c, args[index + 2], 9, -51403784);
          c = md5_gg(c, d, a, b, args[index + 7], 14, 1735328473);
          b = md5_gg(b, c, d, a, args[index + 12], 20, -1926607734);
          a = setTimeout(a, b, c, d, args[index + 5], 4, -378558);
          d = setTimeout(d, a, b, c, args[index + 8], 11, -2022574463);
          c = setTimeout(c, d, a, b, args[index + 11], 16, 1839030562);
          b = setTimeout(b, c, d, a, args[index + 14], 23, -35309556);
          a = setTimeout(a, b, c, d, args[index + 1], 4, -1530992060);
          d = setTimeout(d, a, b, c, args[index + 4], 11, 1272893353);
          c = setTimeout(c, d, a, b, args[index + 7], 16, -155497632);
          b = setTimeout(b, c, d, a, args[index + 10], 23, -1094730640);
          a = setTimeout(a, b, c, d, args[index + 13], 4, 681279174);
          d = setTimeout(d, a, b, c, args[index], 11, -358537222);
          c = setTimeout(c, d, a, b, args[index + 3], 16, -722521979);
          b = setTimeout(b, c, d, a, args[index + 6], 23, 76029189);
          a = setTimeout(a, b, c, d, args[index + 9], 4, -640364487);
          d = setTimeout(d, a, b, c, args[index + 12], 11, -421815835);
          c = setTimeout(c, d, a, b, args[index + 15], 16, 530742520);
          b = setTimeout(b, c, d, a, args[index + 2], 23, -995338651);
          a = p(a, b, c, d, args[index], 6, -198630844);
          d = p(d, a, b, c, args[index + 7], 10, 1126891415);
          c = p(c, d, a, b, args[index + 14], 15, -1416354905);
          b = p(b, c, d, a, args[index + 5], 21, -57434055);
          a = p(a, b, c, d, args[index + 12], 6, 1700485571);
          d = p(d, a, b, c, args[index + 3], 10, -1894986606);
          c = p(c, d, a, b, args[index + 10], 15, -1051523);
          b = p(b, c, d, a, args[index + 1], 21, -2054922799);
          a = p(a, b, c, d, args[index + 8], 6, 1873313359);
          d = p(d, a, b, c, args[index + 15], 10, -30611744);
          c = p(c, d, a, b, args[index + 6], 15, -1560198380);
          b = p(b, c, d, a, args[index + 13], 21, 1309151649);
          a = p(a, b, c, d, args[index + 4], 6, -145523070);
          d = p(d, a, b, c, args[index + 11], 10, -1120210379);
          c = p(c, d, a, b, args[index + 2], 15, 718787259);
          b = p(b, c, d, a, args[index + 9], 21, -343485551);
          a = i(a, h);
          b = i(b, q);
          c = i(c, r);
          d = i(d, m);
        }
        return [a, b, c, d];
      }
      /**
       * @param {!Object} input
       * @return {?}
       */
      function u(input) {
        var i;
        /** @type {string} */
        var parameter = "";
        /** @type {number} */
        i = 0;
        for (; i < 32 * input.length; i = i + 8) {
          /** @type {string} */
          parameter = parameter + String.fromCharCode(input[i >> 5] >>> i % 32 & 255);
        }
        return parameter;
      }
      /**
       * @param {string} a
       * @return {?}
       */
      function $(a) {
        var b;
        /** @type {!Array} */
        var e = [];
        e[(a.length >> 2) - 1] = void 0;
        /** @type {number} */
        b = 0;
        for (; b < e.length; b = b + 1) {
          /** @type {number} */
          e[b] = 0;
        }
        /** @type {number} */
        b = 0;
        for (; b < 8 * a.length; b = b + 8) {
          e[b >> 5] |= (255 & a.charCodeAt(b / 8)) << b % 32;
        }
        return e;
      }
      /**
       * @param {string} a
       * @return {?}
       */
      function header(a) {
        return u(f($(a), 8 * a.length));
      }
      /**
       * @param {string} value
       * @param {string} context
       * @return {?}
       */
      function cb(value, context) {
        var i;
        var e;
        var message = $(value);
        /** @type {!Array} */
        var results = [];
        /** @type {!Array} */
        var val = [];
        results[15] = val[15] = void 0;
        if (message.length > 16) {
          message = f(message, 8 * value.length);
        }
        /** @type {number} */
        i = 0;
        for (; i < 16; i = i + 1) {
          /** @type {number} */
          results[i] = 909522486 ^ message[i];
          /** @type {number} */
          val[i] = 1549556828 ^ message[i];
        }
        return e = f(results.concat($(context)), 512 + 8 * context.length), u(f(val.concat(e), 640));
      }
      /**
       * @param {string} _color
       * @return {?}
       */
      function log(_color) {
        var a;
        var i;
        /** @type {string} */
        var s = "0123456789abcdef";
        /** @type {string} */
        var notifications = "";
        /** @type {number} */
        i = 0;
        for (; i < _color.length; i = i + 1) {
          a = _color.charCodeAt(i);
          /** @type {string} */
          notifications = notifications + (s.charAt(a >>> 4 & 15) + s.charAt(15 & a));
        }
        return notifications;
      }
      /**
       * @param {?} data
       * @return {?}
       */
      function clean(data) {
        return unescape(encodeURIComponent(data));
      }
      /**
       * @param {?} type
       * @return {?}
       */
      function test(type) {
        return header(clean(type));
      }
      /**
       * @param {?} type
       * @return {?}
       */
      function resolve(type) {
        return log(test(type));
      }
      /**
       * @param {?} content
       * @param {?} value
       * @return {?}
       */
      function update(content, value) {
        return cb(clean(content), clean(value));
      }
      /**
       * @param {?} name
       * @param {?} params
       * @return {?}
       */
      function defer(name, params) {
        return log(update(name, params));
      }
      /**
       * @param {?} value
       * @param {?} name
       * @param {?} fn
       * @return {?}
       */
      function init(value, name, fn) {
        return name ? fn ? update(name, value) : defer(name, value) : fn ? test(value) : resolve(value);
      }
      if (void 0 !== (result = function() {
        return init;
      }.call(level, n, level, module))) {
        module.exports = result;
      }
    }();
  },
  "+6Wo" : function(formatters, customFormatters) {
  },
  "+LfV" : function(preventPushState, id, require) {
    var r = require("Uyjf");
    var start = require("nmRV");
    require("Xb9Y")("keys", function() {
      return function(moduleId) {
        return start(r(moduleId));
      };
    });
  },
  "+YOn" : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    /**
     * @param {string} key
     * @param {string} action
     * @param {!Object} index
     * @param {number} name
     * @param {?} value
     * @return {undefined}
     */
    function o(key, action, index, name, value) {
      window.gaevent(key, action, index, name, value);
      window.baevent(key, action, index, name, value);
    }
    /**
     * @return {undefined}
     */
    function YM() {
      window.resendGA();
      window.resendBA();
    }
    /**
     * @return {undefined}
     */
    function resolve() {
      if ("m.ixigua.com" === location.host) {
        _normalizeDataUri2.default.init();
        _UiIcon2.default.init();
      } else {
        _prepareStyleProperties2.default.init();
        _UiIcon2.default.init();
      }
      /** @type {function(string, string, !Object, number, ?): undefined} */
      window.maevent = o;
      /** @type {function(): undefined} */
      window.resendMA = YM;
    }
    /**
     * @return {undefined}
     */
    function init() {
      resolve();
      _omiTransform2.default.init();
      if (2 === history.length && _deepAssign2.default.os.android && _deepAssign2.default.browser.weixin && location.href.indexOf("weixin_list=0") > -1) {
        history.back();
      }
    }
    var _prepareStyleProperties = __webpack_require__("yRjA");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _normalizeDataUri = __webpack_require__("AJa0");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("bChP");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _omiTransform = __webpack_require__("QVlm");
    var _omiTransform2 = _interopRequireDefault(_omiTransform);
    __webpack_require__("VPAO");
    var _deepAssign = __webpack_require__("gT+X");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    /** @type {function(): undefined} */
    module.exports = init;
  },
  "+mxV" : function(module, selector, convertToImages) {
    /**
     * @param {!Object} name
     * @return {?}
     */
    function Emitter(name) {
      if (name) {
        return assign(name);
      }
    }
    /**
     * @param {!Object} object
     * @return {?}
     */
    function assign(object) {
      var key;
      for (key in Emitter.prototype) {
        object[key] = Emitter.prototype[key];
      }
      return object;
    }
    /** @type {function(!Object): ?} */
    module.exports = Emitter;
    /** @type {function(string, !Function): ?} */
    Emitter.prototype.on = Emitter.prototype.addEventListener = function(name, event) {
      return this._callbacks = this._callbacks || {}, (this._callbacks["$" + name] = this._callbacks["$" + name] || []).push(event), this;
    };
    /**
     * @param {string} t
     * @param {!Function} e
     * @return {?}
     */
    Emitter.prototype.once = function(t, e) {
      /**
       * @return {undefined}
       */
      function n() {
        this.off(t, n);
        e.apply(this, arguments);
      }
      return n.fn = e, this.on(t, n), this;
    };
    /** @type {function(string, !Function): ?} */
    Emitter.prototype.off = Emitter.prototype.removeListener = Emitter.prototype.removeAllListeners = Emitter.prototype.removeEventListener = function(event, fn) {
      if (this._callbacks = this._callbacks || {}, 0 == arguments.length) {
        return this._callbacks = {}, this;
      }
      var callbacks = this._callbacks["$" + event];
      if (!callbacks) {
        return this;
      }
      if (1 == arguments.length) {
        return delete this._callbacks["$" + event], this;
      }
      var cb;
      /** @type {number} */
      var i = 0;
      for (; i < callbacks.length; i++) {
        if ((cb = callbacks[i]) === fn || cb.fn === fn) {
          callbacks.splice(i, 1);
          break;
        }
      }
      return this;
    };
    /**
     * @param {string} event
     * @return {?}
     */
    Emitter.prototype.emit = function(event) {
      this._callbacks = this._callbacks || {};
      /** @type {!Array<?>} */
      var cmd_args = [].slice.call(arguments, 1);
      var callbacks = this._callbacks["$" + event];
      if (callbacks) {
        callbacks = callbacks.slice(0);
        /** @type {number} */
        var len = 0;
        var i = callbacks.length;
        for (; len < i; ++len) {
          callbacks[len].apply(this, cmd_args);
        }
      }
      return this;
    };
    /**
     * @param {string} event
     * @return {?}
     */
    Emitter.prototype.listeners = function(event) {
      return this._callbacks = this._callbacks || {}, this._callbacks["$" + event] || [];
    };
    /**
     * @param {string} event
     * @return {?}
     */
    Emitter.prototype.hasListeners = function(event) {
      return !!this.listeners(event).length;
    };
  },
  "/BaA" : function(module, t, xgh2) {
    Object.defineProperty(t, "__esModule", {
      value : true
    });
    /** @type {boolean} */
    t.default = !("undefined" == typeof window || !window.document || !window.document.createElement);
    /** @type {boolean} */
    module.exports = t.default;
  },
  "/xZR" : function(formatters, customFormatters) {
  },
  "0vED" : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _UiRippleInk = __webpack_require__("mRYa");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _AboutPage = __webpack_require__("IJ1K");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _deepAssign = __webpack_require__("nhKt");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _AppDownload = __webpack_require__("J5EE");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var PercentageSymbol = function(leftFence) {
      /**
       * @param {?} props
       * @return {?}
       */
      function ReflexElement(props) {
        return (0, _UiIcon2.default)(this, ReflexElement), (0, _UiRippleInk2.default)(this, (ReflexElement.__proto__ || (0, _normalizeDataUri2.default)(ReflexElement)).call(this, props));
      }
      return (0, _AboutPage2.default)(ReflexElement, leftFence), (0, _classlist2.default)(ReflexElement, [{
        key : "handleClick",
        value : function(name) {
          window.maevent(name.ga.category, "click");
        }
      }, {
        key : "singleImage",
        value : function(value) {
          var thiz = this;
          return _prepareStyleProperties2.default.createElement("section", {
            "data-is-video" : "False",
            "data-hot-time" : "",
            className : "middle_mode has_action xpromt_item",
            "data-group-id" : "",
            "data-item-id" : "",
            "data-format" : "0"
          }, _prepareStyleProperties2.default.createElement("a", {
            href : value.url,
            className : "article_link clearfix ",
            onClick : function() {
              thiz.handleClick(value);
            },
            "data-action-label" : "click_xpromt_item"
          }, _prepareStyleProperties2.default.createElement("div", {
            className : "desc"
          }, _prepareStyleProperties2.default.createElement("h3", {
            className : "dotdot line3 image-margin-right"
          }, value.title), _prepareStyleProperties2.default.createElement("div", {
            className : "item_info"
          }, _prepareStyleProperties2.default.createElement("span", {
            className : "hot_label space"
          }, "\u70ed"), _prepareStyleProperties2.default.createElement("span", {
            className : "src space"
          }, value.src))), _prepareStyleProperties2.default.createElement("div", {
            className : "list_img_holder",
            style : {
              background : "none"
            }
          }, _prepareStyleProperties2.default.createElement(_AppDownload2.default, {
            src : "http://s3.pstatp.com/site/promotion/landing_page/img/" + value.pics[0]
          }))));
        }
      }, {
        key : "smallImage",
        value : function(value) {
          var thiz = this;
          return _prepareStyleProperties2.default.createElement("section", {
            "data-is-video" : "False",
            "data-hot-time" : "",
            className : "has_action xpromt_item",
            "data-group-id" : "",
            "data-item-id" : "",
            "data-format" : "0"
          }, _prepareStyleProperties2.default.createElement("a", {
            href : value.url,
            className : "article_link clearfix ",
            onClick : function() {
              thiz.handleClick(value);
            },
            "data-action-label" : "click_xpromt_item"
          }, _prepareStyleProperties2.default.createElement("h3", {
            className : "dotdot line3 "
          }, value.title), _prepareStyleProperties2.default.createElement("div", {
            className : "list_image"
          }, _prepareStyleProperties2.default.createElement("ul", {
            className : "clearfix"
          }, value.pics.map(function(result) {
            return _prepareStyleProperties2.default.createElement("li", {
              className : "list_img_holder",
              style : {
                background : "none"
              }
            }, _prepareStyleProperties2.default.createElement(_AppDownload2.default, {
              src : "http://s3.pstatp.com/site/promotion/landing_page/img/" + result,
              style : {
                opacity : 1
              }
            }));
          }))), _prepareStyleProperties2.default.createElement("div", {
            className : "item_info"
          }, _prepareStyleProperties2.default.createElement("span", {
            className : "hot_label space"
          }, "\u70ed"), _prepareStyleProperties2.default.createElement("span", {
            className : "src space"
          }, value.src))));
        }
      }, {
        key : "render",
        value : function() {
          var config = this.props.datum;
          return window.maevent(config.ga.category, "show"), 1 === config.pics.length ? this.singleImage(config) : this.smallImage(config);
        }
      }]), ReflexElement;
    }(_prepareStyleProperties.Component);
    PercentageSymbol.propTypes = {
      datum : _deepAssign2.default.object
    };
    mixin.exports = PercentageSymbol;
  },
  "0wW8" : function(record, deep, callback) {
    /**
     * @return {?}
     */
    function f() {
      /** @type {number} */
      var stdout = Math.floor((new Date).getTime() / 1E3);
      /** @type {string} */
      var scores = stdout.toString(16).toUpperCase();
      var elmObjsSorted = resolve(stdout).toString().toUpperCase();
      if (8 !== scores.length) {
        return {
          as : "479BB4B7254C150",
          cp : "7E0AC8874BB0985"
        };
      }
      var accumScores = elmObjsSorted.slice(0, 5);
      var tabw = elmObjsSorted.slice(-5);
      /** @type {string} */
      var pix_color = "";
      /** @type {number} */
      var docRef = 0;
      for (; docRef < 5; docRef++) {
        /** @type {string} */
        pix_color = pix_color + (accumScores[docRef] + scores[docRef]);
      }
      /** @type {string} */
      var summaryHtml = "";
      /** @type {number} */
      var i = 0;
      for (; i < 5; i++) {
        /** @type {string} */
        summaryHtml = summaryHtml + (scores[i + 3] + tabw[i]);
      }
      return {
        as : "A1" + pix_color + scores.slice(-3),
        cp : scores.slice(0, 3) + summaryHtml + "E1"
      };
    }
    var resolve = callback("+2u5");
    /** @type {function(): ?} */
    record.exports = f;
  },
  1 : function(module, object, instantiate) {
    module.exports = instantiate("Bbyf");
  },
  "1+Ds" : function(mixin, args, parseAsUTC) {
    mixin.exports = {
      nativeProxyServer : "http://[::1]:8192/",
      installNumber : "5.3",
      NETWORKTIPS : {
        RETRY : "\u7f51\u7edc\u5931\u8d25,\u70b9\u51fb\u91cd\u8bd5",
        COMMENTRETRY : "\u8bc4\u8bba\u52a0\u8f7d\u5931\u8d25,\u70b9\u51fb\u91cd\u8bd5",
        NETWORKERROR : "\u7f51\u7edc\u5931\u8d25",
        LOADING : "\u52a0\u8f7d\u4e2d...",
        WAITE : "\u52a0\u8f7d\u4e2d,\u8bf7\u7a0d\u540e",
        RECOMMENDING : "\u6b63\u5728\u63a8\u8350...",
        RECOMMENDCOUNT : "\u4e3a\u60a8\u63a8\u8350\u4e86#n#\u7bc7\u6587\u7ae0",
        RECOMMENDEMPTY : "\u6682\u65e0\u66f4\u65b0,\u8bf7\u4f11\u606f\u4e00\u4f1a\u513f",
        RECOMMENDDISLIKE : "\u5c06\u51cf\u5c11\u7c7b\u4f3c\u63a8\u8350",
        HASMORE : "\u67e5\u770b\u66f4\u591a",
        SENDING : "\u6b63\u5728\u63d0\u4ea4",
        SENDINGERROR : "\u53d1\u8868\u5931\u8d25",
        SENDINGSUCCESS : "\u53d1\u8868\u6210\u529f",
        GEOLOCATIONERROR : "\u83b7\u53d6\u5730\u7406\u4f4d\u7f6e\u5931\u8d25",
        NOSEARCHDATA : "\u6682\u65e0\u641c\u7d22\u7ed3\u679c",
        SERVERERROR : "\u670d\u52a1\u5f02\u5e38,\u8bf7\u7a0d\u540e\u91cd\u8bd5",
        LOCALSTORAGEERROE : "\u8bf7\u5728 \u8bbe\u7f6e->Safari->\u963b\u6b62Cookie \u4e2d\u52fe\u9009 '\u6765\u81ea\u7b2c\u4e09\u65b9\u548c\u5e7f\u544a\u5546',\u6216'\u6c38\u4e0d',\u4ee5\u514d\u5f71\u54cd\u5934\u6761\u7f51\u6b63\u5e38\u4f7f\u7528"
      }
    };
  },
  "1uVg" : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _AboutPage = __webpack_require__("mRYa");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _deepAssign = __webpack_require__("IJ1K");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _Types = __webpack_require__("nhKt");
    var _Types2 = _interopRequireDefault(_Types);
    var _AppDownload = __webpack_require__("Cqu5");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var _noframeworkWaypoints = __webpack_require__("lH70");
    var _noframeworkWaypoints2 = _interopRequireDefault(_noframeworkWaypoints);
    __webpack_require__("/xZR");
    var PercentageSymbol = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        (0, _UiIcon2.default)(this, Agent);
        var t = (0, _AboutPage2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).call(this));
        return t.createMarkup = t.createMarkup.bind(t), t;
      }
      return (0, _deepAssign2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "createMarkup",
        value : function(name) {
          return {
            __html : _noframeworkWaypoints2.default.render(name)
          };
        }
      }, {
        key : "render",
        value : function() {
          var item = this.props.datum;
          var langClass = (0, _AppDownload2.default)({
            middle_mode : item.middle_mode,
            taobaoAd : "taobao" === item.ad_type,
            has_action : true,
            "item-hidden" : item.honey
          });
          return _prepareStyleProperties2.default.createElement("section", {
            className : langClass,
            "data-hot-time" : item.behot_time,
            "data-group-id" : item.group_id,
            "data-item-id" : item.item_id,
            "data-format" : "0",
            dangerouslySetInnerHTML : this.createMarkup(item)
          });
        }
      }]), Agent;
    }(_prepareStyleProperties.Component);
    PercentageSymbol.propTypes = {
      datum : _Types2.default.object
    };
    mixin.exports = PercentageSymbol;
  },
  "2SGS" : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _UiIcon = __webpack_require__("iltz");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("fvPU");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _UiRippleInk = __webpack_require__("hJ6a");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _AboutPage = __webpack_require__("mRYa");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _AppDownload = __webpack_require__("IJ1K");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    var _deepAssign = __webpack_require__("YWnE");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _normalizeDataUri = __webpack_require__("Xamz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _toHyphenCase = __webpack_require__("ZD21");
    var _toHyphenCase2 = _interopRequireDefault(_toHyphenCase);
    __webpack_require__("Yyv+");
    var ExampleReactComponent = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _classlist2.default)(this, Agent), (0, _AboutPage2.default)(this, (Agent.__proto__ || (0, _UiIcon2.default)(Agent)).apply(this, arguments));
      }
      return (0, _AppDownload2.default)(Agent, _EventEmitter), (0, _UiRippleInk2.default)(Agent, [{
        key : "onRefreshBtnClick",
        value : function() {
          this.props.onRefreshBtnClick();
        }
      }, {
        key : "render",
        value : function() {
          var subgroupObj = this;
          var filterText = this.props.GTMValue.hideTopBar || this.props.hideTopBar;
          var n = this.props.GTMValue.hideMsgBox || this.props.hideMsgBox;
          return _prepareStyleProperties2.default.createElement("header", {
            id : "indexHeader",
            className : "index--toutiaoribao"
          }, filterText ? null : _prepareStyleProperties2.default.createElement("div", {
            className : "top_bar"
          }, _prepareStyleProperties2.default.createElement("div", {
            className : "abs_m"
          }, _prepareStyleProperties2.default.createElement("a", {
            href : "#",
            className : "refresh_title btn"
          }), _prepareStyleProperties2.default.createElement(_toHyphenCase2.default, {
            rotateRefreshBtn : this.props.rotateRefreshBtn,
            onRefreshClick : function() {
              return subgroupObj.onRefreshBtnClick();
            }
          })), this.props.showAuditInfo ? _prepareStyleProperties2.default.createElement("span", {
            className : "abs_l",
            onClick : function() {
              return subgroupObj.props.onClickShowAuditInfo();
            }
          }, "\u8fd4\u56de") : _prepareStyleProperties2.default.createElement("div", {
            className : "abs_l"
          }, !n && _prepareStyleProperties2.default.createElement(_normalizeDataUri2.default, null)), this.props.showAuditBtn ? _prepareStyleProperties2.default.createElement("span", {
            className : "abs_r",
            onClick : function() {
              return subgroupObj.props.onClickShowAuditInfo();
            }
          }, "\u8054\u7cfb\u6211\u4eec") : _prepareStyleProperties2.default.createElement("div", {
            className : "abs_r"
          }, _prepareStyleProperties2.default.createElement("a", {
            href : _deepAssign2.default.appendQuery("//m.toutiao.com/search/", "need_open_window=1"),
            className : "btn search"
          }))));
        }
      }]), Agent;
    }(_prepareStyleProperties.Component);
    ExampleReactComponent.propTypes = {
      GTMValue : _propTypes2.default.object,
      onRefreshBtnClick : _propTypes2.default.func,
      rotateRefreshBtn : _propTypes2.default.bool,
      hideTopBar : _propTypes2.default.bool,
      hideMsgBox : _propTypes2.default.bool,
      showAuditBtn : _propTypes2.default.bool,
      onClickShowAuditInfo : _propTypes2.default.func,
      showAuditInfo : _propTypes2.default.bool
    };
    ExampleReactComponent.defaultProps = {
      showAuditBtn : false,
      showAuditInfo : false
    };
    module.exports = ExampleReactComponent;
  },
  "3/fS" : function(record, array, n) {
    (function(code) {
      var s = n("QVlm");
      var m = n("UoBj");
      var helpers = n("SJPe");
      var ellipsis = function($, metaWindow) {
        /**
         * @param {number} n
         * @return {?}
         */
        function degToRad(n) {
          return n * (Math.PI / 180);
        }
        /**
         * @param {number} ow
         * @param {!Object} callback
         * @return {undefined}
         */
        function normal(ow, callback) {
          /** @type {!Array} */
          var xy = [0, 0];
          /** @type {!Array} */
          var responseGroup = [xy[0], xy[1] + ow];
          /** @type {!Array} */
          var sourceInfoParts = [xy[0] + ow / 2, xy[1] + ow / 2];
          /** @type {!Array} */
          var prop_values = [xy[0], xy[1] + ow / 2];
          /** @type {!Object} */
          var targetArray = callback;
          /** @type {!Array} */
          var cmds = [];
          cmds.push("M" + xy.join(","));
          cmds.push("L" + responseGroup.join(","));
          cmds.push("L" + sourceInfoParts.join(","));
          cmds.push("L" + xy.join(","));
          targetArray.find("path").attr("d", cmds.join(" "));
          targetArray[0].setAttribute("refX", prop_values[0]);
          targetArray[0].setAttribute("refY", prop_values[1]);
        }
        /**
         * @param {!Object} settings
         * @return {undefined}
         */
        function render(settings) {
          settings = $.extend({
            x : 0,
            y : 0,
            radius : 0,
            margin : 0,
            startDegree : 0,
            endDegree : 0,
            arrowSize : 0,
            arrowObj : $("#markerArrow"),
            pathObj : $("#svgPath"),
            color : "#ff0000"
          }, settings);
          var i = settings.radius;
          var j = settings.margin;
          var r = i + j + i * Math.sin(degToRad(settings.endDegree));
          /** @type {number} */
          var id = i + j - i * Math.cos(degToRad(settings.endDegree));
          var match = i + j + i * Math.sin(degToRad(settings.startDegree));
          /** @type {number} */
          var data = i + j - i * Math.cos(degToRad(settings.startDegree));
          match = s.px2px(match);
          data = s.px2px(data);
          i = s.px2px(i);
          r = s.px2px(r);
          id = s.px2px(id);
          /** @type {!Array} */
          var drilldownLevelLabels = [["M" + match, data].join(",")];
          drilldownLevelLabels.push([["A" + i, i].join(","), "0", [settings.endDegree - settings.startDegree > 180 ? "1" : "0", "1"].join(","), [r, id].join(",")].join(" "));
          /** @type {string} */
          var CONT_CLASS = drilldownLevelLabels.join(" ");
          $(settings.pathObj).attr("d", CONT_CLASS).css("stroke", settings.color);
          $(settings.arrowObj).find("path").css("fill", settings.color);
          normal(settings.arrowSize, $(settings.arrowObj));
        }
        return {
          drawArc : render
        };
      }(window.jQuery || window.Zepto, window);
      var func = function($, me) {
        var DOM = me.document;
        var getTime = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || function(key) {
          window.setTimeout(key, 1E3 / 60);
        };
        var defaultOptions = {
          con : "",
          minDistance : 4
        };
        /** @type {!Array} */
        var l = ["onPullStart", "onMove", "onRelease", "needRefresh", "doRefresh", "noop"];
        /** @type {number} */
        var c = 30;
        /** @type {number} */
        var gw = 300;
        /**
         * @return {?}
         */
        var getZero = function() {
          return 85 * ((s || {
            dpr : 1
          }).dpr || 1);
        };
        /** @type {number} */
        var v = 10;
        /**
         * @param {number} type
         * @return {?}
         */
        var createEvent = function(type) {
          return 5 * type / 12;
        };
        var enable_keys = function() {
          /** @type {!Element} */
          var textedCanvas = document.createElement("canvas");
          /** @type {boolean} */
          var t = !(!textedCanvas.getContext || !textedCanvas.getContext("2d"));
          /** @type {string} */
          var searcher_name = navigator.userAgent.toLowerCase();
          /** @type {(Array<string>|null)} */
          var resize = (searcher_name.match(/chrome\/([\d.]+)/), searcher_name.match(/version\/([\d.]+).*safari/));
          /** @type {(Array<string>|null)} */
          var l = (searcher_name.match(/firefox\/([\d.]+)/), searcher_name.match(/mx[\d.]+/));
          /** @type {boolean} */
          var fallback = false;
          return l && resize && (fallback = true), !t && fallback;
        }();
        /**
         * @param {!Object} options
         * @return {undefined}
         */
        var init = function(options) {
          if ("string" == typeof options.con) {
            options.con = DOM.querySelector(options.con);
          }
          var opts = {};
          var obj = this;
          $.each(l, function(canCreateDiscussions, name) {
            opts[name] = obj["_" + name].bind(obj);
          });
          this.options = $.extend({}, defaultOptions, opts, options);
          /** @type {boolean} */
          this.shouldRefresh = false;
          /** @type {boolean} */
          this.isRefreshing = false;
          /** @type {null} */
          this.$pullTip = null;
          opts.onPullEnd = this._onPullEnd.bind(this);
          options = $.extend({}, opts, options);
          this.touchPull = m.init(options);
          /** @type {number} */
          this.refreshTimes = 0;
        };
        return init.prototype = {
          _onPullStart : function(event, tempalte) {
            if (!this.isRefreshing) {
              event.preventDefault();
              this.addPullTip(this.options.con);
            }
          },
          _onMove : function(e, event) {
            if (!this.isRefreshing) {
              e.preventDefault();
              var evt = createEvent(event);
              evt = this.isRefreshing ? evt + this.minRefreshDistance : evt;
              this.movePullTip(evt);
              this.changePullTip(evt, this.options.con);
            }
          },
          _onPullEnd : function(size, deprecatedHeight, deprecatedGrow) {
            if (!this.isRefreshing) {
              var self = this;
              this.options.needRefresh(deprecatedHeight);
              this.options.onRelease().then(function() {
                if (self.options.needRefresh()) {
                  me._vis_opt_queue = me._vis_opt_queue || [];
                  me._vis_opt_queue.push(function() {
                    _vis_opt_goal_conversion(13359);
                  });
                  /** @type {boolean} */
                  self.isRefreshing = true;
                  self.refreshTimes += 1;
                  self.options.doRefresh().always(function() {
                    self.reset();
                  });
                } else {
                  self.reset();
                  self.options.noop();
                }
              });
            }
          },
          transitionDefer : null,
          onTransitionEnd : function() {
            var $rootScope = this;
            if ($rootScope.shouldRefresh) {
              $rootScope.canvasObj.startAuto();
            } else {
              $rootScope.reset();
            }
            setTimeout(function() {
              $rootScope.transitionDefer.resolve();
            }, false);
          },
          _onRelease : function() {
            if (this.transitionDefer = $.Deferred(), this.pullTipExist()) {
              this.$pullTip[0].addEventListener("webkitTransitionEnd", this.onTransitionEnd.bind(this), false);
              var uboard = this.shouldRefresh ? this.minRefreshDistance : 0;
              this.movePullTip(uboard, "all " + gw + "ms linear", true);
            } else {
              this.transitionDefer.resolve();
            }
            return this.transitionDefer;
          },
          _doRefresh : function() {
            var extensionResolver = $.Deferred();
            return extensionResolver.resolve(), extensionResolver;
          },
          _noop : function() {
          },
          _needRefresh : function(type) {
            return type = createEvent(type), !this.shouldRefresh && type >= this.minRefreshDistance && (this.shouldRefresh = true), this.shouldRefresh;
          },
          pullTipExist : function() {
            return this.$pullTip && this.$pullTip[0];
          },
          reset : function() {
            var clojIsReversed = this.isRefreshing;
            /** @type {boolean} */
            this.isRefreshing = false;
            /** @type {boolean} */
            this.shouldRefresh = false;
            this.removePullTip(clojIsReversed);
          },
          canvasObj : function() {
            /**
             * @return {?}
             */
            function find_eol() {
              /** @type {number} */
              var contactCapacity = (i + 1) % colors.length;
              return i = contactCapacity, contactCapacity;
            }
            /**
             * @param {number} status
             * @return {?}
             */
            function proxy(status) {
              return 360 + status - arc;
            }
            /**
             * @return {undefined}
             */
            function getMustache() {
              if (!isVisible) {
                ctx.clearRect(0, 0, 2 * w, 2 * h);
              }
            }
            /**
             * @param {!Object} options
             * @return {undefined}
             */
            function clear(options) {
              if (!enable_keys) {
                var i = options.start;
                var x = options.end;
                var lineWidth = options.lineWidth;
                var lineColor = options.color;
                var direction = options.counterClockwise;
                var fallback = options.co;
                if (options.clearRect) {
                  getMustache();
                }
                ctx.save();
                ctx.globalCompositeOperation = fallback;
                ctx.beginPath();
                ctx.arc(w, h, r, normalize(i), normalize(x), direction);
                ctx.lineWidth = lineWidth;
                ctx.strokeStyle = lineColor;
                ctx.stroke();
                ctx.restore();
              }
            }
            /**
             * @return {undefined}
             */
            function initialize() {
              if (!enable_keys) {
                var interval = options.speed;
                var startAngle = options.startAngle;
                var t = start;
                var colorize = options.color;
                var lineWidth = options.lineWidth;
                var val = options.counterClockwise;
                var mult = options.globalCompositeOperation;
                var y2 = triples || +new Date;
                /** @type {number} */
                t = +new Date;
                /** @type {number} */
                interval = 360 / duration * (t - y2);
                /** @type {number} */
                triples = t;
                start = start + interval;
                /** @type {number} */
                t = Math.min(b, start);
                /** @type {boolean} */
                var clearRect = "draw" === tool;
                if (!isVisible && (clear({
                  start : startAngle,
                  end : t,
                  color : colorize,
                  lineWidth : lineWidth,
                  counterClockwise : val,
                  co : mult,
                  clearRect : clearRect
                }), start >= b)) {
                  if (ctx.closePath(), options = "erase" !== tool ? defaultOptions : opts, "draw" === (tool = "erase" !== tool ? "erase" : "draw")) {
                    c = options.color;
                    var i = find_eol(c);
                    options.color = colors[i];
                    /** @type {number} */
                    options.startAngle = (options.startAngle - arc) % 360;
                    /** @type {number} */
                    start = options.startAngle;
                    b = proxy(start);
                  } else {
                    /** @type {number} */
                    start = options.startAngle = opts.startAngle;
                  }
                }
              }
            }
            /**
             * @param {number} s
             * @return {undefined}
             */
            function tick(s) {
              if (!enable_keys) {
                /** @type {number} */
                var PI2 = opts.speed;
                /** @type {number} */
                var startAngle = opts.startAngle;
                /** @type {number} */
                var endAngle = opts.startAngle;
                var c = colors[0];
                if (!isNaN(s)) {
                  /** @type {number} */
                  s = Math.min(a.minRefreshDistance - c, s);
                  /** @type {number} */
                  var r = s / (a.minRefreshDistance - c);
                  /** @type {number} */
                  PI2 = (b - v) * r - opts.startAngle;
                }
                /** @type {number} */
                endAngle = endAngle + PI2;
                /** @type {number} */
                len = endAngle;
                render({
                  start : startAngle,
                  end : endAngle,
                  color : c,
                  distance : s
                });
              }
            }
            /**
             * @return {?}
             */
            function _getUpdateInformation() {
              /** @type {number} */
              var t = a.minRefreshDistance - c;
              /** @type {number} */
              var h = t / duration * 1.3;
              var c1 = colors[0];
              /** @type {number} */
              var s = t;
              /** @type {number} */
              var rate = +new Date;
              var postdefer = $.Deferred();
              return getTime(function start() {
                if (s >= 0) {
                  /** @type {number} */
                  var newRate = +new Date;
                  /** @type {number} */
                  s = s - h * (newRate - rate);
                  /** @type {number} */
                  rate = newRate;
                  /** @type {number} */
                  var r = s / (a.minRefreshDistance - c);
                  /** @type {number} */
                  var width = (b - v) * r - opts.startAngle;
                  /** @type {number} */
                  var pos = len - width;
                  /** @type {number} */
                  pos = Math.min(pos, len);
                  render({
                    start : pos,
                    end : len,
                    color : c1,
                    distance : s
                  });
                  getTime(start);
                } else {
                  postdefer.resolve();
                }
              }), postdefer;
            }
            /**
             * @param {!Object} options
             * @return {undefined}
             */
            function render(options) {
              var d = options.distance;
              /** @type {number} */
              var v = isVisible ? 10 : 25;
              /** @type {number} */
              var plane_h = lineWidth;
              /** @type {number} */
              var scale = d / (a.minRefreshDistance - c);
              if (!isNaN(d)) {
                /** @type {number} */
                v = v * scale;
                /** @type {number} */
                plane_h = lineWidth * scale;
              }
              getMustache();
              if (isVisible) {
                ellipsis.drawArc({
                  x : w,
                  y : h,
                  radius : r,
                  margin : str,
                  startDegree : options.start,
                  endDegree : options.end,
                  arrowSize : v,
                  arrowObj : $(elem).find("#markerArrow"),
                  pathObj : $(elem).find("#svgPath"),
                  color : options.color
                });
              } else {
                ctx.strokeStyle = options.color;
                ctx.fillStyle = options.color;
                helpers.drawArcedArrow(ctx, w, h, r, normalize(options.start), normalize(options.end), false, 1, 2, normalize(45), v, lineWidth, plane_h);
              }
            }
            /**
             * @param {string} string
             * @return {?}
             */
            function parseTransform(string) {
              /** @type {number} */
              var values = 0;
              if (string) {
                string = string.replace("matrix(", "").replace(")", "");
                string = string.replace(/\s+/gi, "");
                values = string.split(",")[5] || 0;
              }
              return values;
            }
            /**
             * @return {undefined}
             */
            function translate() {
              var r = parseTransform(a.$pullTip.css("transform"));
              if (!(r < c)) {
                /** @type {number} */
                var w = gw;
                /** @type {number} */
                var h = r / w;
                var t = r;
                /** @type {number} */
                var minValue = +new Date;
                getTime(function onComplete() {
                  if (t > c && a.$pullTip) {
                    /** @type {number} */
                    var v = +new Date;
                    /** @type {number} */
                    t = t - h * (v - minValue);
                    show(t - c);
                    tick(t - c);
                    resetPosition(t - c);
                    /** @type {number} */
                    minValue = v;
                    getTime(onComplete);
                  }
                });
              }
            }
            /**
             * @param {number} width
             * @return {undefined}
             */
            function resetPosition(width) {
              /** @type {number} */
              var meterPos = 1 * width / (a.minRefreshDistance - c);
              $(elem).css("opacity", meterPos);
            }
            /**
             * @param {?} name
             * @param {string} type
             * @return {undefined}
             */
            function show(name, type) {
              var moduleEntryFile = name;
              if (!type) {
                /** @type {number} */
                moduleEntryFile = Math.max(0, (name - c) / a.minRefreshDistance * 360);
              }
              /** @type {string} */
              elem.style.webkitTransition = "none";
              /** @type {string} */
              elem.style.webkitTransform = "rotate(" + moduleEntryFile + "deg)";
            }
            /**
             * @param {number} opt_length
             * @return {?}
             */
            function normalize(opt_length) {
              return opt_length * (Math.PI / 180);
            }
            /**
             * @param {number} fadeTime
             * @return {undefined}
             */
            function stop(fadeTime) {
              clearTimeout(_takingTooLongTimeout);
              fadeTime = fadeTime || 8E3;
              /** @type {number} */
              _takingTooLongTimeout = setTimeout(function() {
                a.reset();
              }, fadeTime);
            }
            /** @type {null} */
            var a = null;
            /** @type {null} */
            var elem = null;
            /** @type {null} */
            var ctx = null;
            /** @type {boolean} */
            var isVisible = false;
            /** @type {number} */
            var w = 100;
            /** @type {number} */
            var h = 100;
            /** @type {number} */
            var r = 50;
            /** @type {number} */
            var str = 0;
            /** @type {number} */
            var lineWidth = 15;
            /** @type {boolean} */
            var L = false;
            /** @type {number} */
            var duration = 1E3;
            /** @type {!Array} */
            var colors = ["green", "red", "blue", "#f3b000"];
            var c = colors[0];
            /** @type {number} */
            var i = 1;
            var opts = {
              startAngle : 0,
              speed : 5,
              color : colors[0],
              counterClockwise : false,
              globalCompositeOperation : "source-out",
              lineWidth : lineWidth
            };
            var defaultOptions = {
              startAngle : 0,
              speed : 5,
              color : "white",
              counterClockwise : false,
              globalCompositeOperation : "destination-out",
              lineWidth : lineWidth + 40
            };
            /** @type {number} */
            var start = 0;
            /** @type {number} */
            var len = 0;
            var options = opts;
            /** @type {string} */
            var tool = "draw";
            /** @type {number} */
            var arc = 50;
            /** @type {number} */
            var b = 0;
            /** @type {number} */
            var triples = 0;
            /** @type {number} */
            var _takingTooLongTimeout = -1;
            return {
              init : function(_, value) {
                this.reset();
                /** @type {number} */
                triples = 0;
                /** @type {boolean} */
                L = false;
                elem = _.find("#load-tip-svg")[0] || _.find("#load-tip-canvas")[0];
                ctx = elem.getContext ? elem.getContext("2d") : elem;
                /** @type {boolean} */
                isVisible = !elem.getContext;
                /** @type {number} */
                len = start = 0;
                /** @type {number} */
                opts.startAngle = defaultOptions.startAngle = 0;
                b = proxy(start);
                /** @type {number} */
                i = 1;
                opts.color = colors[i];
                /** @type {string} */
                tool = "draw";
                options = opts;
                /** @type {!Object} */
                a = value;
                if (isVisible) {
                  /** @type {number} */
                  str = 9;
                  /** @type {number} */
                  w = h = r = (40 - 2 * str) / 2;
                } else {
                  /** @type {number} */
                  w = h = 100;
                  /** @type {number} */
                  str = 0;
                  /** @type {number} */
                  r = 50;
                }
              },
              reset : function() {
                /** @type {null} */
                elem = null;
                /** @type {null} */
                ctx = null;
              },
              drawArrowedArcByDis : function(data) {
                tick(data);
              },
              drawArc : function(x1) {
                if (enable_keys) {
                  console.log("not support");
                } else {
                  initialize();
                }
              },
              clearCurrent : function() {
                if (enable_keys) {
                  console.log("not support");
                } else {
                  translate();
                }
              },
              rotate : show,
              changeOpacity : resetPosition,
              autoRotate : function() {
                var e = elem.style.webkitTransform;
                e = e.replace("rotate(", "").replace("deg", "").replace(")", "");
                /** @type {number} */
                var x = parseFloat(e);
                var interpolate = this;
                /** @type {number} */
                var i = +new Date;
                getTime(function duration() {
                  if (L) {
                    /** @type {number} */
                    var varend = +new Date;
                    var x1 = x + .24 * (varend - i);
                    /** @type {number} */
                    i = varend;
                    interpolate.rotate(x1, true);
                    x = x1;
                    getTime(duration);
                  }
                });
              },
              autoDraw : function() {
                if (!enable_keys) {
                  /**
                   * @return {undefined}
                   */
                  var duration = function render() {
                    if (L) {
                      if (isVisible) {
                        /** @type {boolean} */
                        L = false;
                        $(ctx).attr("class", "spinner");
                      } else {
                        initialize();
                        getTime(render);
                      }
                    }
                  };
                  _getUpdateInformation().done(function() {
                    getTime(duration);
                  });
                }
              },
              startAuto : function() {
                /** @type {boolean} */
                L = true;
                a.touchPull.detachEvent();
                this.autoDraw();
                this.autoRotate();
                stop();
              },
              stopAuto : function() {
                /** @type {boolean} */
                L = false;
                a.touchPull.initEvent();
                clearTimeout(_takingTooLongTimeout);
              }
            };
          }(),
          initCanvas : function() {
            this.canvasObj.init(this.$pullTip, this);
          },
          addPullTip : function(c) {
            this.removePullTip();
            c = this.options.con;
            var model = this.$pullTip;
            if (!model) {
              /** @type {!Array} */
              var outChance = [];
              outChance.push("<div class='list_top'>");
              outChance.push("<div class='list_top_con v2'>");
              outChance.push("<canvas                             id='load-tip-canvas'                             width='200'                             height='200'                             class='" + (enable_keys ? "not-support" : "") + "'></canvas>");
              outChance.push("</div></div>");
              this.$pullTip = $(outChance.join("")).insertAfter("body");
              model = this.$pullTip;
              this.minRefreshDistance = model.outerHeight();
              var loading = model[0];
              /** @type {string} */
              loading.style.webkitTransition = "none";
              /** @type {string} */
              loading.style.webkitTransform = "translate3d(0,10px,0)";
              /** @type {string} */
              loading.style.top = c.getBoundingClientRect().top - this.minRefreshDistance + "px";
              this.initCanvas();
            }
          },
          movePullTip : function(e, value, _flexdatalist) {
            if (this.pullTipExist()) {
              /** @type {number} */
              var $retHtml = Math.min(getZero(), e);
              this.$pullTip[0].style.webkitTransition = value || "none";
              /** @type {string} */
              this.$pullTip[0].style.webkitTransform = "translate3d(0," + $retHtml + "px,0)";
              if (0 === e) {
                this.canvasObj.clearCurrent();
              } else {
                if (e > c) {
                  if (this.shouldRefresh) {
                    if (!(this.isRefreshing || true === _flexdatalist)) {
                      this.canvasObj.rotate(e);
                    }
                  } else {
                    if (e <= getZero() - 5) {
                      this.canvasObj.rotate(e);
                    }
                    this.canvasObj.drawArrowedArcByDis(e - c);
                    this.canvasObj.changeOpacity(e - c);
                  }
                }
              }
            }
          },
          changePullTip : function(e, islongclick) {
            this.pullTipExist();
          },
          removePullTip : function(isSlidingUp) {
            if (this.pullTipExist()) {
              if (isSlidingUp) {
                var config = this;
                config.canvasObj.stopAuto();
                /** @type {string} */
                config.$pullTip[0].style.webkitTransition = "all 100ms linear";
                config.$pullTip.css("opacity", .1);
                config.$pullTip[0].style.webkitTransform += " scale(0.1)";
              } else {
                this.$pullTip[0].removeEventListener("webkitTransitionEnd", this.onTransitionEnd, false);
                this.$pullTip.remove();
                /** @type {null} */
                this.$pullTip = null;
                $(window).trigger("pullrefresh_pulltip_removed");
              }
            }
          }
        }, {
          init : function(selector) {
            return new init(selector);
          }
        };
      }(code, window);
      record.exports = func;
    }).call(array, n("gXQ3"));
  },
  "3Cyt" : function(module, exports, __webpack_require__) {
    (function(setImmediate, obj) {
      !function(canCreateDiscussions, factory) {
        module.exports = factory();
      }("undefined" != typeof self && self, function() {
        return function(e) {
          /**
           * @param {number} i
           * @return {?}
           */
          function t(i) {
            if (n[i]) {
              return n[i].exports;
            }
            var module = n[i] = {
              i : i,
              l : false,
              exports : {}
            };
            return e[i].call(module.exports, module, module.exports, t), module.l = true, module.exports;
          }
          var n = {};
          return t.m = e, t.c = n, t.d = function(name, o, n) {
            if (!t.o(name, o)) {
              Object.defineProperty(name, o, {
                configurable : false,
                enumerable : true,
                get : n
              });
            }
          }, t.n = function(module) {
            /** @type {function(): ?} */
            var n = module && module.__esModule ? function() {
              return module.default;
            } : function() {
              return module;
            };
            return t.d(n, "a", n), n;
          }, t.o = function(t, object) {
            return Object.prototype.hasOwnProperty.call(t, object);
          }, t.p = "", t(t.s = 6);
        }([function(canCreateDiscussions, isSlidingUp) {
        }, function(mixin, exports, n) {
          /**
           * @param {!Object} value
           * @param {string} count
           * @return {?}
           */
          function bind(value, count) {
            return ObjP.hasOwnProperty.call(value, count);
          }
          /**
           * @param {?} trait
           * @return {?}
           */
          function from(trait) {
            return traitsChosen[trait];
          }
          /**
           * @param {string} delta
           * @param {?} notify
           * @param {!Error} msg
           * @return {?}
           */
          function render(delta, notify, msg) {
            if (msg.Update || (msg = new exports.TemplateError(msg)), msg.Update(delta), !notify) {
              /** @type {!Error} */
              var data = msg;
              /** @type {!Error} */
              msg = new Error(data.message);
              msg.name = data.name;
            }
            return msg;
          }
          /**
           * @param {!Object} name
           * @param {number} type
           * @param {(number|string)} i
           * @return {?}
           */
          function init(name, type, i) {
            var e;
            var object;
            var err = this;
            if (name instanceof Error) {
              /** @type {!Object} */
              object = name;
              /** @type {string} */
              name = object.name + ": " + object.message;
            }
            if (Object.setPrototypeOf) {
              /** @type {!Error} */
              e = new Error(name);
              Object.setPrototypeOf(e, init.prototype);
            } else {
              e = this;
              Object.defineProperty(e, "message", {
                enumerable : false,
                writable : true,
                value : name
              });
            }
            Object.defineProperty(e, "name", {
              value : "Template render error"
            });
            if (Error.captureStackTrace) {
              Error.captureStackTrace(e, this.constructor);
            }
            var format;
            if (object) {
              /** @type {(ObjectPropertyDescriptor<Error>|undefined)} */
              var item = Object.getOwnPropertyDescriptor(object, "stack");
              /** @type {(!Function|undefined)} */
              format = item && (item.get || function() {
                return item.value;
              });
              if (!format) {
                /**
                 * @return {?}
                 */
                format = function() {
                  return object.stack;
                };
              }
            } else {
              /** @type {string} */
              var err = (new Error(name)).stack;
              /**
               * @return {?}
               */
              format = function() {
                return err;
              };
            }
            return Object.defineProperty(e, "stack", {
              get : function() {
                return format.call(err);
              }
            }), Object.defineProperty(e, "cause", {
              value : object
            }), e.lineno = type, e.colno = i, e.firstUpdate = true, e.Update = function(delta) {
              /** @type {string} */
              var msg = "(" + (delta || "unknown path") + ")";
              return err.firstUpdate && (err.lineno && err.colno ? msg = msg + (" [Line " + err.lineno + ", Column " + err.colno + "]") : err.lineno && (msg = msg + (" [Line " + err.lineno + "]"))), msg = msg + "\n ", err.firstUpdate && (msg = msg + " "), err.message = msg + (err.message || ""), err.firstUpdate = false, err;
            }, e;
          }
          /**
           * @param {string} string
           * @return {?}
           */
          function escapeHtml(string) {
            return string.replace(regSpaceAll, from);
          }
          /**
           * @param {!Object} obj
           * @return {?}
           */
          function isFunction(obj) {
            return "[object Function]" === ObjP.toString.call(obj);
          }
          /**
           * @param {!Object} obj
           * @return {?}
           */
          function isArray(obj) {
            return "[object Array]" === ObjP.toString.call(obj);
          }
          /**
           * @param {!Object} str
           * @return {?}
           */
          function isString(str) {
            return "[object String]" === ObjP.toString.call(str);
          }
          /**
           * @param {!Object} obj
           * @return {?}
           */
          function isUndefined(obj) {
            return "[object Object]" === ObjP.toString.call(obj);
          }
          /**
           * @param {!NodeList} array
           * @param {?} value
           * @return {?}
           */
          function write(array, value) {
            var length = {};
            var val = isFunction(value) ? value : function(type) {
              return type[value];
            };
            /** @type {number} */
            var i = 0;
            for (; i < array.length; i++) {
              var min = array[i];
              var a = val(min, i);
              (length[a] || (length[a] = [])).push(min);
            }
            return length;
          }
          /**
           * @param {!Array} arrLike
           * @return {?}
           */
          function toArray(arrLike) {
            return Array.prototype.slice.call(arrLike);
          }
          /**
           * @param {!NodeList} array
           * @return {?}
           */
          function without(array) {
            /** @type {!Array} */
            var result = [];
            if (!array) {
              return result;
            }
            var length = array.length;
            var standardInjects = toArray(arguments).slice(1);
            /** @type {number} */
            var i = -1;
            for (; ++i < length;) {
              if (-1 === indexOf(standardInjects, array[i])) {
                result.push(array[i]);
              }
            }
            return result;
          }
          /**
           * @param {string} i
           * @param {number} t
           * @return {?}
           */
          function repeat(i, t) {
            /** @type {string} */
            var s = "";
            /** @type {number} */
            var offset = 0;
            for (; offset < t; offset++) {
              /** @type {string} */
              s = s + i;
            }
            return s;
          }
          /**
           * @param {!Object} obj
           * @param {!Function} iterator
           * @param {?} context
           * @return {undefined}
           */
          function forEach(obj, iterator, context) {
            if (null != obj) {
              if (ArrayProto.forEach && obj.forEach === ArrayProto.forEach) {
                obj.forEach(iterator, context);
              } else {
                if (obj.length === +obj.length) {
                  /** @type {number} */
                  var i = 0;
                  var originalLength = obj.length;
                  for (; i < originalLength; i++) {
                    iterator.call(context, obj[i], i, obj);
                  }
                }
              }
            }
          }
          /**
           * @param {string} obj
           * @param {!Function} f
           * @return {?}
           */
          function map(obj, f) {
            /** @type {!Array} */
            var r = [];
            if (null == obj) {
              return r;
            }
            if (ArrayProto.map && obj.map === ArrayProto.map) {
              return obj.map(f);
            }
            /** @type {number} */
            var i = 0;
            for (; i < obj.length; i++) {
              r[r.length] = f(obj[i], i);
            }
            return obj.length === +obj.length && (r.length = obj.length), r;
          }
          /**
           * @param {!Object} results
           * @param {!Function} callback
           * @param {!Function} done
           * @return {undefined}
           */
          function onConnect(results, callback, done) {
            /**
             * @return {undefined}
             */
            function end() {
              i++;
              if (i < results.length) {
                callback(results[i], i, end, done);
              } else {
                done();
              }
            }
            /** @type {number} */
            var i = -1;
            end();
          }
          /**
           * @param {!Object} el
           * @param {!Function} filter
           * @param {!Function} cb
           * @return {undefined}
           */
          function constructor(el, filter, cb) {
            /**
             * @return {undefined}
             */
            function callback() {
              i++;
              var key = row[i];
              if (i < columns) {
                filter(key, el[key], i, columns, callback);
              } else {
                cb();
              }
            }
            var row = $(el || {});
            var columns = row.length;
            /** @type {number} */
            var i = -1;
            callback();
          }
          /**
           * @param {string} arr
           * @param {number} val
           * @param {?} byteOffset
           * @return {?}
           */
          function indexOf(arr, val, byteOffset) {
            return Array.prototype.indexOf.call(arr || [], val, byteOffset);
          }
          /**
           * @param {!Object} name
           * @return {?}
           */
          function $(name) {
            /** @type {!Array} */
            var rv = [];
            var n;
            for (n in name) {
              if (bind(name, n)) {
                rv.push(n);
              }
            }
            return rv;
          }
          /**
           * @param {undefined} obj
           * @return {?}
           */
          function entries(obj) {
            return $(obj).map(function(sourcePropKey) {
              return [sourcePropKey, obj[sourcePropKey]];
            });
          }
          /**
           * @param {undefined} p
           * @return {?}
           */
          function value(p) {
            return $(p).map(function(inType) {
              return p[inType];
            });
          }
          /**
           * @param {string} data
           * @param {!Object} value
           * @return {?}
           */
          function Set(data, value) {
            return data = data || {}, $(value).forEach(function(k) {
              data[k] = value[k];
            }), data;
          }
          /**
           * @param {string} y
           * @param {!Object} x
           * @return {?}
           */
          function T(y, x) {
            if (isArray(x) || isString(x)) {
              return -1 !== x.indexOf(y);
            }
            if (isUndefined(x)) {
              return y in x;
            }
            throw new Error('Cannot use "in" operator to search for "' + y + '" in unexpected types.');
          }
          var ArrayProto = Array.prototype;
          var ObjP = Object.prototype;
          var traitsChosen = {
            "&" : "&amp;",
            '"' : "&quot;",
            "'" : "&#39;",
            "<" : "&lt;",
            ">" : "&gt;"
          };
          /** @type {!RegExp} */
          var regSpaceAll = /[&"'<>]/g;
          exports = mixin.exports = {};
          /** @type {function(!Object, string): ?} */
          exports.hasOwnProp = bind;
          /** @type {function(string, ?, !Error): ?} */
          exports._prettifyError = render;
          if (Object.setPrototypeOf) {
            Object.setPrototypeOf(init.prototype, Error.prototype);
          } else {
            /** @type {!Object} */
            init.prototype = Object.create(Error.prototype, {
              constructor : {
                value : init
              }
            });
          }
          /** @type {function(!Object, number, (number|string)): ?} */
          exports.TemplateError = init;
          /** @type {function(string): ?} */
          exports.escape = escapeHtml;
          /** @type {function(!Object): ?} */
          exports.isFunction = isFunction;
          /** @type {function(!Object): ?} */
          exports.isArray = isArray;
          /** @type {function(!Object): ?} */
          exports.isString = isString;
          /** @type {function(!Object): ?} */
          exports.isObject = isUndefined;
          /** @type {function(!NodeList, ?): ?} */
          exports.groupBy = write;
          /** @type {function(!Array): ?} */
          exports.toArray = toArray;
          /** @type {function(!NodeList): ?} */
          exports.without = without;
          /** @type {function(string, number): ?} */
          exports.repeat = repeat;
          /** @type {function(!Object, !Function, ?): undefined} */
          exports.each = forEach;
          /** @type {function(string, !Function): ?} */
          exports.map = map;
          /** @type {function(!Object, !Function, !Function): undefined} */
          exports.asyncIter = onConnect;
          /** @type {function(!Object, !Function, !Function): undefined} */
          exports.asyncFor = constructor;
          /** @type {function(string, number, ?): ?} */
          exports.indexOf = indexOf;
          /** @type {function(!Object): ?} */
          exports.keys = $;
          /** @type {function(undefined): ?} */
          exports._entries = entries;
          /** @type {function(undefined): ?} */
          exports._values = value;
          /** @type {function(string, !Object): ?} */
          exports._assign = exports.extend = Set;
          /** @type {function(string, !Object): ?} */
          exports.inOperator = T;
        }, function(module, canCreateDiscussions, load) {
          /**
           * @param {!Array} args
           * @param {!Array} obj
           * @param {!Function} runner
           * @return {?}
           */
          function exports(args, obj, runner) {
            var topic = this;
            return function() {
              /** @type {number} */
              var n = arguments.length;
              /** @type {!Array} */
              var m = new Array(n);
              /** @type {number} */
              var j = 0;
              for (; j < n; j++) {
                m[j] = arguments[j];
              }
              var r;
              var i = push(m);
              var f = a(m);
              if (i > args.length) {
                /** @type {!Array<?>} */
                r = m.slice(0, args.length);
                m.slice(r.length, i).forEach(function(elem, i) {
                  if (i < obj.length) {
                    f[obj[i]] = elem;
                  }
                });
                r.push(f);
              } else {
                if (i < args.length) {
                  /** @type {!Array<?>} */
                  r = m.slice(0, i);
                  var index = i;
                  for (; index < args.length; index++) {
                    var a = args[index];
                    r.push(f[a]);
                    delete f[a];
                  }
                  r.push(f);
                } else {
                  /** @type {!Array} */
                  r = m;
                }
              }
              return runner.apply(topic, r);
            };
          }
          /**
           * @param {?} obj
           * @return {?}
           */
          function makeKeywordArgs(obj) {
            return obj.__keywords = true, obj;
          }
          /**
           * @param {boolean} o
           * @return {?}
           */
          function inspect(o) {
            return o && Object.prototype.hasOwnProperty.call(o, "__keywords");
          }
          /**
           * @param {!Array} t
           * @return {?}
           */
          function a(t) {
            var tlen = t.length;
            if (tlen) {
              var n = t[tlen - 1];
              if (inspect(n)) {
                return n;
              }
            }
            return {};
          }
          /**
           * @param {!Array} values
           * @return {?}
           */
          function push(values) {
            var nbindividuals = values.length;
            return 0 === nbindividuals ? 0 : inspect(values[nbindividuals - 1]) ? nbindividuals - 1 : nbindividuals;
          }
          /**
           * @param {string} val
           * @return {?}
           */
          function SafeString(val) {
            if ("string" != typeof val) {
              return val;
            }
            /** @type {string} */
            this.val = val;
            /** @type {number} */
            this.length = val.length;
          }
          /**
           * @param {!Object} val
           * @param {!Object} str
           * @return {?}
           */
          function safe(val, str) {
            return val instanceof SafeString ? new SafeString(str) : str.toString();
          }
          /**
           * @param {!Function} val
           * @return {?}
           */
          function markSafe(val) {
            /** @type {string} */
            var type = typeof val;
            return "string" === type ? new SafeString(val) : "function" !== type ? val : function(canCreateDiscussions) {
              var re = val.apply(this, arguments);
              return "string" == typeof re ? new SafeString(re) : re;
            };
          }
          /**
           * @param {?} val
           * @param {?} opt_validate
           * @return {?}
           */
          function set(val, opt_validate) {
            return val = void 0 !== val && null !== val ? val : "", !opt_validate || val instanceof SafeString || (val = lib.escape(val.toString())), val;
          }
          /**
           * @param {!Array} val
           * @param {number} lineno
           * @param {number} colno
           * @return {?}
           */
          function ensureDefined(val, lineno, colno) {
            if (null === val || void 0 === val) {
              throw new lib.TemplateError("attempted to output null or undefined value", lineno + 1, colno + 1);
            }
            return val;
          }
          /**
           * @param {?} v
           * @param {string} key
           * @return {?}
           */
          function p(v, key) {
            if (void 0 !== v && null !== v) {
              return "function" == typeof v[key] ? function() {
                /** @type {number} */
                var arglen = arguments.length;
                /** @type {!Array} */
                var args = new Array(arglen);
                /** @type {number} */
                var i = 0;
                for (; i < arglen; i++) {
                  args[i] = arguments[i];
                }
                return v[key].apply(v, args);
              } : v[key];
            }
          }
          /**
           * @param {!Function} callback
           * @param {string} name
           * @param {?} context
           * @param {?} args
           * @return {?}
           */
          function callWrap(callback, name, context, args) {
            if (!callback) {
              throw new Error("Unable to call `" + name + "`, which is undefined or falsey");
            }
            if ("function" != typeof callback) {
              throw new Error("Unable to call `" + name + "`, which is not a function");
            }
            return callback.apply(context, args);
          }
          /**
           * @param {!Object} context
           * @param {!Object} frame
           * @param {string} name
           * @return {?}
           */
          function contextOrFrameLookup(context, frame, name) {
            var versionByName = frame.lookup(name);
            return void 0 !== versionByName ? versionByName : context.lookup(name);
          }
          /**
           * @param {!Object} error
           * @param {string} lineno
           * @param {!Object} colno
           * @return {?}
           */
          function handleError(error, lineno, colno) {
            return error.lineno ? error : new lib.TemplateError(error, lineno, colno);
          }
          /**
           * @param {!Object} arr
           * @param {?} list
           * @param {!Function} iter
           * @param {!Function} cb
           * @return {undefined}
           */
          function asyncEach(arr, list, iter, cb) {
            if (lib.isArray(arr)) {
              var len = arr.length;
              lib.asyncIter(arr, function(item, i, next) {
                switch(list) {
                  case 1:
                    iter(item, i, len, next);
                    break;
                  case 2:
                    iter(item[0], item[1], i, len, next);
                    break;
                  case 3:
                    iter(item[0], item[1], item[2], i, len, next);
                    break;
                  default:
                    item.push(i, len, next);
                    iter.apply(this, item);
                }
              }, cb);
            } else {
              lib.asyncFor(arr, function(extra, data, key, i, next) {
                iter(extra, data, key, i, next);
              }, cb);
            }
          }
          /**
           * @param {!Object} options
           * @param {?} func
           * @param {!Function} cb
           * @param {?} next
           * @return {undefined}
           */
          function asyncAll(options, func, cb, next) {
            /**
             * @param {?} i
             * @param {?} p
             * @return {undefined}
             */
            function next(i, p) {
              elToFocus++;
              c[i] = p;
              if (elToFocus === value) {
                next(null, c.join(""));
              }
            }
            var value;
            var c;
            /** @type {number} */
            var elToFocus = 0;
            if (lib.isArray(options)) {
              if (value = options.length, c = new Array(value), 0 === value) {
                next(null, "");
              } else {
                /** @type {number} */
                var x = 0;
                for (; x < options.length; x++) {
                  var m = options[x];
                  switch(func) {
                    case 1:
                      cb(m, x, value, next);
                      break;
                    case 2:
                      cb(m[0], m[1], x, value, next);
                      break;
                    case 3:
                      cb(m[0], m[1], m[2], x, value, next);
                      break;
                    default:
                      m.push(x, value, next);
                      cb.apply(this, m);
                  }
                }
              }
            } else {
              var args = lib.keys(options || {});
              if (value = args.length, c = new Array(value), 0 === value) {
                next(null, "");
              } else {
                /** @type {number} */
                var index = 0;
                for (; index < args.length; index++) {
                  var url = args[index];
                  cb(url, options[url], index, value, next);
                }
              }
            }
          }
          /**
           * @param {!Object} value
           * @return {?}
           */
          function isIndexMatchable(value) {
            return "object" != typeof value || null === value || lib.isArray(value) ? value : boundTag && Symbol.iterator in value ? isArray(value) : value;
          }
          var lib = load(1);
          /** @type {function((IArrayLike<T>|Iterable<T>|string), function(this:S, (T|string), number): R=, S=): !Array<R>} */
          var isArray = Array.from;
          var boundTag = "function" == typeof Symbol && Symbol.iterator && "function" == typeof isArray;
          var Frame = function() {
            /**
             * @param {?} parentContext
             * @param {string} expression
             * @return {undefined}
             */
            function Context(parentContext, expression) {
              this.variables = {};
              this.parent = parentContext;
              /** @type {boolean} */
              this.topLevel = false;
              /** @type {string} */
              this.isolateWrites = expression;
            }
            var context = Context.prototype;
            return context.set = function(name, value, dir) {
              var values = name.split(".");
              var map = this.variables;
              var path = this;
              if (dir && (path = this.resolve(values[0], true))) {
                return void path.set(name, value);
              }
              /** @type {number} */
              var i = 0;
              for (; i < values.length - 1; i++) {
                var type = values[i];
                if (!map[type]) {
                  map[type] = {};
                }
                map = map[type];
              }
              /** @type {string} */
              map[values[values.length - 1]] = value;
            }, context.get = function(name) {
              var r = this.variables[name];
              return void 0 !== r ? r : null;
            }, context.lookup = function(name) {
              var p = this.parent;
              var r = this.variables[name];
              return void 0 !== r ? r : p && p.lookup(name);
            }, context.resolve = function(name, forWrite) {
              var p = forWrite && this.isolateWrites ? void 0 : this.parent;
              return void 0 !== this.variables[name] ? this : p && p.resolve(name);
            }, context.push = function(type) {
              return new Context(this, type);
            }, context.pop = function() {
              return this.parent;
            }, Context;
          }();
          /** @type {!Object} */
          SafeString.prototype = Object.create(String.prototype, {
            length : {
              writable : true,
              configurable : true,
              value : 0
            }
          });
          /**
           * @return {?}
           */
          SafeString.prototype.valueOf = function() {
            return this.val;
          };
          /**
           * @return {?}
           */
          SafeString.prototype.toString = function() {
            return this.val;
          };
          module.exports = {
            Frame : Frame,
            makeMacro : exports,
            makeKeywordArgs : makeKeywordArgs,
            numArgs : push,
            suppressValue : set,
            ensureDefined : ensureDefined,
            memberLookup : p,
            contextOrFrameLookup : contextOrFrameLookup,
            callWrap : callWrap,
            handleError : handleError,
            isArray : lib.isArray,
            keys : lib.keys,
            SafeString : SafeString,
            copySafeness : safe,
            markSafe : markSafe,
            asyncEach : asyncEach,
            asyncAll : asyncAll,
            inOperator : lib.inOperator,
            fromIterator : isIndexMatchable
          };
        }, function(mixin, canCreateDiscussions, parseInt) {
          /**
           * @param {?} target
           * @param {!Object} src
           * @return {undefined}
           */
          function isArray(target, src) {
            /** @type {!Object} */
            target.prototype = Object.create(src.prototype);
            target.prototype.constructor = target;
            /** @type {!Object} */
            target.__proto__ = src;
          }
          var individual = parseInt(4);
          var indContent = function(klass) {
            /**
             * @param {number} value
             * @return {?}
             */
            function tr(value) {
              var me;
              return me = klass.call(this) || this, me.precompiled = value || {}, me;
            }
            return isArray(tr, klass), tr.prototype.getSource = function(name) {
              return this.precompiled[name] ? {
                src : {
                  type : "code",
                  obj : this.precompiled[name]
                },
                path : name
              } : null;
            }, tr;
          }(individual);
          mixin.exports = {
            PrecompiledLoader : indContent
          };
        }, function(module, canCreateDiscussions, n) {
          /**
           * @param {?} a
           * @param {!Object} b
           * @return {undefined}
           */
          function merge(a, b) {
            /** @type {!Object} */
            a.prototype = Object.create(b.prototype);
            a.prototype.constructor = a;
            /** @type {!Object} */
            a.__proto__ = b;
          }
          var p = n(0);
          var name = n(5);
          module.exports = function(hash) {
            /**
             * @return {?}
             */
            function _() {
              return hash.apply(this, arguments) || this;
            }
            merge(_, hash);
            var r = _.prototype;
            return r.on = function(type, name) {
              this.listeners = this.listeners || {};
              this.listeners[type] = this.listeners[type] || [];
              this.listeners[type].push(name);
            }, r.emit = function(name) {
              /** @type {number} */
              var length = arguments.length;
              /** @type {!Array} */
              var args = new Array(length > 1 ? length - 1 : 0);
              /** @type {number} */
              var i = 1;
              for (; i < length; i++) {
                args[i - 1] = arguments[i];
              }
              if (this.listeners && this.listeners[name]) {
                this.listeners[name].forEach(function(fToRetry) {
                  fToRetry.apply(void 0, args);
                });
              }
            }, r.resolve = function(value, to) {
              return p.resolve(p.dirname(value), to);
            }, r.isRelative = function(str) {
              return 0 === str.indexOf("./") || 0 === str.indexOf("../");
            }, _;
          }(name);
        }, function(module, canCreateDiscussions, convertSchema) {
          /**
           * @param {!Function} y
           * @param {string} props
           * @return {undefined}
           */
          function t(y, props) {
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
              Object.defineProperty(y, descriptor.key, descriptor);
            }
          }
          /**
           * @param {!Function} x
           * @param {!Function} n
           * @param {!Function} a
           * @return {?}
           */
          function is(x, n, a) {
            return n && t(x.prototype, n), a && t(x, a), x;
          }
          /**
           * @param {?} b
           * @param {!Object} t
           * @return {undefined}
           */
          function _inherits(b, t) {
            /** @type {!Object} */
            b.prototype = Object.create(t.prototype);
            b.prototype.constructor = b;
            /** @type {!Object} */
            b.__proto__ = t;
          }
          /**
           * @param {?} o
           * @param {!Function} fn
           * @return {?}
           */
          function check(o, fn) {
            return "function" != typeof o || "function" != typeof fn ? fn : function() {
              var p = this.parent;
              this.parent = o;
              var match = fn.apply(this, arguments);
              return this.parent = p, match;
            };
          }
          /**
           * @param {!Function} error
           * @param {string} t
           * @param {!Object} options
           * @return {?}
           */
          function extend(error, t, options) {
            options = options || {};
            meta.keys(options).forEach(function(key) {
              options[key] = check(error.prototype[key], options[key]);
            });
            var a = function(e) {
              /**
               * @return {?}
               */
              function t() {
                return e.apply(this, arguments) || this;
              }
              return _inherits(t, e), is(t, [{
                key : "typename",
                get : function() {
                  return t;
                }
              }]), t;
            }(error);
            return meta._assign(a.prototype, options), a;
          }
          var meta = convertSchema(1);
          var storeMixin = function() {
            /**
             * @return {undefined}
             */
            function result() {
              this.init.apply(this, arguments);
            }
            return result.prototype.init = function() {
            }, result.extend = function(value, options) {
              return "object" == typeof value && (options = value, value = "anonymous"), extend(this, value, options);
            }, is(result, [{
              key : "typename",
              get : function() {
                return this.constructor.name;
              }
            }]), result;
          }();
          module.exports = storeMixin;
        }, function(module, canCreateDiscussions, require) {
          /**
           * @param {!Object} templatesPath
           * @param {!Object} opts
           * @return {?}
           */
          function init(templatesPath, opts) {
            opts = opts || {};
            if (lib.isObject(templatesPath)) {
              /** @type {!Object} */
              opts = templatesPath;
              /** @type {null} */
              templatesPath = null;
            }
            var args;
            return loaders.FileSystemLoader ? args = new loaders.FileSystemLoader(templatesPath, {
              watch : opts.watch,
              noCache : opts.noCache
            }) : loaders.WebLoader && (args = new loaders.WebLoader(templatesPath, {
              useCache : opts.web && opts.web.useCache,
              async : opts.web && opts.web.async
            })), self = new Environment(args, opts), opts && opts.express && self.express(opts.express), self;
          }
          var self;
          var lib = require(1);
          var template = require(7);
          var Environment = template.Environment;
          var Template = template.Template;
          var Loader = require(4);
          var loaders = require(3);
          var precompile = require(0);
          var version = require(0);
          var html5 = require(0);
          var lexer = require(0);
          var ViewUtils = require(2);
          var ctrls = require(0);
          var renderAssign = require(16);
          module.exports = {
            Environment : Environment,
            Template : Template,
            Loader : Loader,
            FileSystemLoader : loaders.FileSystemLoader,
            PrecompiledLoader : loaders.PrecompiledLoader,
            WebLoader : loaders.WebLoader,
            compiler : version,
            parser : html5,
            lexer : lexer,
            runtime : ViewUtils,
            lib : lib,
            nodes : ctrls,
            installJinjaCompat : renderAssign,
            configure : init,
            reset : function() {
              self = void 0;
            },
            compile : function(parent, path, view, target) {
              return self || init(), new Template(parent, path, view, target);
            },
            render : function(expr, x, target) {
              return self || init(), self.render(expr, x, target);
            },
            renderString : function(template, data, module) {
              return self || init(), self.renderString(template, data, module);
            },
            precompile : precompile ? precompile.precompile : void 0,
            precompileString : precompile ? precompile.precompileString : void 0
          };
        }, function(module, canCreateDiscussions, require) {
          /**
           * @param {?} o
           * @param {!Function} parent
           * @return {undefined}
           */
          function callback(o, parent) {
            /** @type {!Object} */
            o.prototype = Object.create(parent.prototype);
            o.prototype.constructor = o;
            /** @type {!Function} */
            o.__proto__ = parent;
          }
          /**
           * @param {!Object} f
           * @param {?} data
           * @param {!Object} end
           * @return {undefined}
           */
          function next(f, data, end) {
            loseSlide(function() {
              f(data, end);
            });
          }
          var loseSlide = require(8);
          var cb = require(11);
          var lib = require(1);
          var compiler = require(0);
          var o = require(12);
          var loaders = require(3);
          var GroupingView = loaders.FileSystemLoader;
          var Composite_ = loaders.WebLoader;
          var RiftSandbox = loaders.PrecompiledLoader;
          var langLocaleMap = require(13);
          var globals = require(14);
          var template = require(5);
          var runtime = require(2);
          var handleError = runtime.handleError;
          var Frame = runtime.Frame;
          var send = require(15);
          var a = {
            type : "code",
            obj : {
              root : function(context, data, scope, name, cb) {
                try {
                  cb(null, "");
                } catch (e) {
                  cb(handleError(e, null, null));
                }
              }
            }
          };
          var Environment = function(View) {
            /**
             * @return {?}
             */
            function d() {
              return View.apply(this, arguments) || this;
            }
            callback(d, View);
            var self = d.prototype;
            return self.init = function(loaders, opts) {
              var self = this;
              opts = this.opts = opts || {};
              /** @type {boolean} */
              this.opts.dev = !!opts.dev;
              this.opts.autoescape = null == opts.autoescape || opts.autoescape;
              /** @type {boolean} */
              this.opts.throwOnUndefined = !!opts.throwOnUndefined;
              /** @type {boolean} */
              this.opts.trimBlocks = !!opts.trimBlocks;
              /** @type {boolean} */
              this.opts.lstripBlocks = !!opts.lstripBlocks;
              /** @type {!Array} */
              this.loaders = [];
              if (loaders) {
                this.loaders = lib.isArray(loaders) ? loaders : [loaders];
              } else {
                if (GroupingView) {
                  /** @type {!Array} */
                  this.loaders = [new GroupingView("views")];
                } else {
                  if (Composite_) {
                    /** @type {!Array} */
                    this.loaders = [new Composite_("/views")];
                  }
                }
              }
              if ("undefined" != typeof window && window.nunjucksPrecompiled) {
                this.loaders.unshift(new RiftSandbox(window.nunjucksPrecompiled));
              }
              this.initCache();
              this.globals = globals();
              this.filters = {};
              this.tests = {};
              /** @type {!Array} */
              this.asyncFilters = [];
              this.extensions = {};
              /** @type {!Array} */
              this.extensionsList = [];
              lib._entries(o).forEach(function(args) {
                var name = args[0];
                var value = args[1];
                return self.addFilter(name, value);
              });
              lib._entries(langLocaleMap).forEach(function(results) {
                var msg = results[0];
                var test = results[1];
                return self.addTest(msg, test);
              });
            }, self.initCache = function() {
              this.loaders.forEach(function(require) {
                require.cache = {};
                if ("function" == typeof require.on) {
                  require.on("update", function(plugPath) {
                    /** @type {null} */
                    require.cache[plugPath] = null;
                  });
                }
              });
            }, self.addExtension = function(name, extension) {
              return extension.__name = name, this.extensions[name] = extension, this.extensionsList.push(extension), this;
            }, self.removeExtension = function(name) {
              var extension = this.getExtension(name);
              if (extension) {
                this.extensionsList = lib.without(this.extensionsList, extension);
                delete this.extensions[name];
              }
            }, self.getExtension = function(name) {
              return this.extensions[name];
            }, self.hasExtension = function(name) {
              return !!this.extensions[name];
            }, self.addGlobal = function(name, value) {
              return this.globals[name] = value, this;
            }, self.getGlobal = function(name) {
              if (void 0 === this.globals[name]) {
                throw new Error("global not found: " + name);
              }
              return this.globals[name];
            }, self.addFilter = function(name, value, handler) {
              /** @type {!Function} */
              var wrapped = value;
              return handler && this.asyncFilters.push(name), this.filters[name] = wrapped, this;
            }, self.getFilter = function(name) {
              if (!this.filters[name]) {
                throw new Error("filter not found: " + name);
              }
              return this.filters[name];
            }, self.addTest = function(name, func) {
              return this.tests[name] = func, this;
            }, self.getTest = function(name) {
              if (!this.tests[name]) {
                throw new Error("test not found: " + name);
              }
              return this.tests[name];
            }, self.resolveTemplate = function(loader, parentName, filename) {
              return !(loader.isRelative && parentName && loader.isRelative(filename) && loader.resolve) ? filename : loader.resolve(parentName, filename);
            }, self.getTemplate = function(name, eagerCompile, parentName, filename, cb) {
              var _this = this;
              var that = this;
              /** @type {null} */
              var p = null;
              if (name && name.raw && (name = name.raw), lib.isFunction(parentName) && (cb = parentName, parentName = null, eagerCompile = eagerCompile || false), lib.isFunction(eagerCompile) && (cb = eagerCompile, eagerCompile = false), name instanceof Template) {
                p = name;
              } else {
                if ("string" != typeof name) {
                  throw new Error("template names must be a string: " + name);
                }
                /** @type {number} */
                var i = 0;
                for (; i < this.loaders.length; i++) {
                  var element = this.loaders[i];
                  if (p = element.cache[this.resolveTemplate(element, parentName, name)]) {
                    break;
                  }
                }
              }
              if (p) {
                return eagerCompile && p.compile(), cb ? void cb(null, p) : p;
              }
              var stroke;
              /**
               * @param {!Object} err
               * @param {!Object} data
               * @return {?}
               */
              var createTemplate = function(err, data) {
                if (data || err || filename || (err = new Error("template not found: " + name)), err) {
                  if (cb) {
                    return void cb(err);
                  }
                  throw err;
                }
                var tmpl;
                if (data) {
                  tmpl = new Template(data.src, _this, data.path, eagerCompile);
                  if (!data.noCache) {
                    data.loader.cache[name] = tmpl;
                  }
                } else {
                  tmpl = new Template(a, _this, "", eagerCompile);
                }
                if (cb) {
                  cb(null, tmpl);
                } else {
                  stroke = tmpl;
                }
              };
              return lib.asyncIter(this.loaders, function(loader, canCreateDiscussions, getLeaklessArgs, action) {
                /**
                 * @param {!Object} ctx
                 * @param {!Object} evt
                 * @return {undefined}
                 */
                function handle(ctx, evt) {
                  if (ctx) {
                    action(ctx);
                  } else {
                    if (evt) {
                      /** @type {!Object} */
                      evt.loader = loader;
                      action(null, evt);
                    } else {
                      getLeaklessArgs();
                    }
                  }
                }
                name = that.resolveTemplate(loader, parentName, name);
                if (loader.async) {
                  loader.getSource(name, handle);
                } else {
                  handle(null, loader.getSource(name));
                }
              }, createTemplate), stroke;
            }, self.express = function(payload) {
              return send(this, payload);
            }, self.render = function(name, e, s) {
              if (lib.isFunction(e)) {
                /** @type {!Object} */
                s = e;
                /** @type {null} */
                e = null;
              }
              /** @type {null} */
              var value = null;
              return this.getTemplate(name, function(b, target) {
                if (b && s) {
                  next(s, b);
                } else {
                  if (b) {
                    throw b;
                  }
                  value = target.render(e, s);
                }
              }), value;
            }, self.renderString = function(tpl, obj, opts, data) {
              return lib.isFunction(opts) && (data = opts, opts = {}), opts = opts || {}, (new Template(tpl, this, opts.path)).render(obj, data);
            }, self.waterfall = function(val, err, init) {
              return cb(val, err, init);
            }, d;
          }(template);
          var Context = function(View) {
            /**
             * @return {?}
             */
            function init() {
              return View.apply(this, arguments) || this;
            }
            callback(init, View);
            var context = init.prototype;
            return context.init = function(container, params, env) {
              var self = this;
              this.env = env || new Environment;
              this.ctx = lib.extend({}, container);
              this.blocks = {};
              /** @type {!Array} */
              this.exported = [];
              lib.keys(params).forEach(function(name) {
                self.addBlock(name, params[name]);
              });
            }, context.lookup = function(name) {
              return name in this.env.globals && !(name in this.ctx) ? this.env.globals[name] : this.ctx[name];
            }, context.setVariable = function(name, value) {
              this.ctx[name] = value;
            }, context.getVariables = function() {
              return this.ctx;
            }, context.addBlock = function(name, block) {
              return this.blocks[name] = this.blocks[name] || [], this.blocks[name].push(block), this;
            }, context.getBlock = function(name) {
              if (!this.blocks[name]) {
                throw new Error('unknown block "' + name + '"');
              }
              return this.blocks[name][0];
            }, context.getSuper = function(env, name, block, frame, runtime, cb) {
              var idx = lib.indexOf(this.blocks[name] || [], block);
              var blk = this.blocks[name][idx + 1];
              var context = this;
              if (-1 === idx || !blk) {
                throw new Error('no super block available for "' + name + '"');
              }
              blk(env, context, frame, runtime, cb);
            }, context.addExport = function(name) {
              this.exported.push(name);
            }, context.getExported = function() {
              var modelInstance = this;
              var processedOptions = {};
              return this.exported.forEach(function(name) {
                processedOptions[name] = modelInstance.ctx[name];
              }), processedOptions;
            }, init;
          }(template);
          var Template = function(View) {
            /**
             * @return {?}
             */
            function t() {
              return View.apply(this, arguments) || this;
            }
            callback(t, View);
            var p = t.prototype;
            return p.init = function(src, env, id, o) {
              if (this.env = env || new Environment, lib.isObject(src)) {
                switch(src.type) {
                  case "code":
                    this.tmplProps = src.obj;
                    break;
                  case "string":
                    this.tmplStr = src.obj;
                    break;
                  default:
                    throw new Error("Unexpected template object type " + src.type + "; expected 'code', or 'string'");
                }
              } else {
                if (!lib.isString(src)) {
                  throw new Error("src must be a string or an object describing the source");
                }
                /** @type {!Object} */
                this.tmplStr = src;
              }
              if (this.path = id, o) {
                try {
                  this._compile();
                } catch (i) {
                  throw lib._prettifyError(this.path, this.env.opts.dev, i);
                }
              } else {
                /** @type {boolean} */
                this.compiled = false;
              }
            }, p.render = function(o, a, f) {
              var self = this;
              if ("function" == typeof o) {
                /** @type {!Object} */
                f = o;
                o = {};
              } else {
                if ("function" == typeof a) {
                  /** @type {!Object} */
                  f = a;
                  /** @type {null} */
                  a = null;
                }
              }
              /** @type {boolean} */
              var booA = !a;
              try {
                this.compile();
              } catch (i) {
                var value = lib._prettifyError(this.path, this.env.opts.dev, i);
                if (f) {
                  return next(f, value);
                }
                throw value;
              }
              var context = new Context(o || {}, this.blocks, this.env);
              var frame = a ? a.push(true) : new Frame;
              /** @type {boolean} */
              frame.topLevel = true;
              /** @type {null} */
              var historystate = null;
              /** @type {boolean} */
              var j = false;
              return this.rootRenderFunc(this.env, context, frame, runtime, function(i, undefined) {
                if (!j) {
                  if (i && (i = lib._prettifyError(self.path, self.env.opts.dev, i), j = true), f) {
                    if (booA) {
                      next(f, i, undefined);
                    } else {
                      f(i, undefined);
                    }
                  } else {
                    if (i) {
                      throw i;
                    }
                    /** @type {!Object} */
                    historystate = undefined;
                  }
                }
              }), historystate;
            }, p.getExported = function(ctx, value, cb) {
              if ("function" == typeof ctx) {
                /** @type {!Object} */
                cb = ctx;
                ctx = {};
              }
              if ("function" == typeof value) {
                /** @type {!Object} */
                cb = value;
                /** @type {null} */
                value = null;
              }
              try {
                this.compile();
              } catch (mutationsMap) {
                if (cb) {
                  return cb(mutationsMap);
                }
                throw mutationsMap;
              }
              var frame = value ? value.push() : new Frame;
              /** @type {boolean} */
              frame.topLevel = true;
              var context = new Context(ctx || {}, this.blocks, this.env);
              this.rootRenderFunc(this.env, context, frame, runtime, function(fallbackReleases) {
                if (fallbackReleases) {
                  cb(fallbackReleases, null);
                } else {
                  cb(null, context.getExported());
                }
              });
            }, p.compile = function() {
              if (!this.compiled) {
                this._compile();
              }
            }, p._compile = function() {
              var props;
              if (this.tmplProps) {
                props = this.tmplProps;
              } else {
                var source = compiler.compile(this.tmplStr, this.env.asyncFilters, this.env.extensionsList, this.path, this.env.opts);
                props = (new Function(source))();
              }
              this.blocks = this._getBlocks(props);
              this.rootRenderFunc = props.root;
              /** @type {boolean} */
              this.compiled = true;
            }, p._getBlocks = function(a) {
              var aObj = {};
              return lib.keys(a).forEach(function(p) {
                if ("b_" === p.slice(0, 2)) {
                  aObj[p.slice(2)] = a[p];
                }
              }), aObj;
            }, t;
          }(template);
          module.exports = {
            Environment : Environment,
            Template : Template
          };
        }, function(module, canCreateDiscussions, __webpack_require__) {
          /**
           * @return {undefined}
           */
          function throwFirstError() {
            if (u.length) {
              throw u.shift();
            }
          }
          /**
           * @param {!Object} name
           * @return {undefined}
           */
          function asap(name) {
            var rawTask;
            rawTask = modes.length ? modes.pop() : new RawTask;
            /** @type {!Object} */
            rawTask.task = name;
            rawAsap(rawTask);
          }
          /**
           * @return {undefined}
           */
          function RawTask() {
            /** @type {null} */
            this.task = null;
          }
          var rawAsap = __webpack_require__(9);
          /** @type {!Array} */
          var modes = [];
          /** @type {!Array} */
          var u = [];
          var requestErrorThrow = rawAsap.makeRequestCallFromTimer(throwFirstError);
          /** @type {function(!Object): undefined} */
          module.exports = asap;
          /**
           * @return {undefined}
           */
          RawTask.prototype.call = function() {
            try {
              this.task.call();
            } catch (error) {
              if (asap.onerror) {
                asap.onerror(error);
              } else {
                u.push(error);
                requestErrorThrow();
              }
            } finally {
              /** @type {null} */
              this.task = null;
              modes[modes.length] = this;
            }
          };
        }, function(module, gen34_options, moment) {
          (function(global) {
            /**
             * @param {!Object} name
             * @return {undefined}
             */
            function rawAsap(name) {
              if (!a.length) {
                requestFlush();
                /** @type {boolean} */
                s = true;
              }
              /** @type {!Object} */
              a[a.length] = name;
            }
            /**
             * @return {undefined}
             */
            function err() {
              for (; b < a.length;) {
                var name = b;
                if (b = b + 1, a[name].call(), b > thresh) {
                  /** @type {number} */
                  var j = 0;
                  /** @type {number} */
                  var z = a.length - b;
                  for (; j < z; j++) {
                    a[j] = a[j + b];
                  }
                  a.length -= b;
                  /** @type {number} */
                  b = 0;
                }
              }
              /** @type {number} */
              a.length = 0;
              /** @type {number} */
              b = 0;
              /** @type {boolean} */
              s = false;
            }
            /**
             * @param {!Function} callback
             * @return {?}
             */
            function makeRequestCallFromTimer(callback) {
              return function() {
                /**
                 * @return {undefined}
                 */
                function handleTimer() {
                  clearTimeout(timeoutHandle);
                  clearInterval(intervalHandle);
                  callback();
                }
                /** @type {number} */
                var timeoutHandle = setTimeout(handleTimer, 0);
                /** @type {number} */
                var intervalHandle = setInterval(handleTimer, 50);
              };
            }
            /** @type {function(!Object): undefined} */
            module.exports = rawAsap;
            var requestFlush;
            /** @type {!Array} */
            var a = [];
            /** @type {boolean} */
            var s = false;
            /** @type {number} */
            var b = 0;
            /** @type {number} */
            var thresh = 1024;
            var scope = void 0 !== global ? global : self;
            var RectObj = scope.MutationObserver || scope.WebKitMutationObserver;
            requestFlush = "function" == typeof RectObj ? function(obj) {
              /** @type {number} */
              var q = 1;
              var o = new RectObj(obj);
              /** @type {!Text} */
              var item = document.createTextNode("");
              return o.observe(item, {
                characterData : true
              }), function() {
                /** @type {number} */
                q = -q;
                /** @type {number} */
                item.data = q;
              };
            }(err) : makeRequestCallFromTimer(err);
            rawAsap.requestFlush = requestFlush;
            /** @type {function(!Function): ?} */
            rawAsap.makeRequestCallFromTimer = makeRequestCallFromTimer;
          }).call(gen34_options, moment(10));
        }, function(module, canCreateDiscussions) {
          var g;
          g = function() {
            return this;
          }();
          try {
            g = g || Function("return this")() || (0, eval)("this");
          } catch (e) {
            if ("object" == typeof window) {
              /** @type {!Window} */
              g = window;
            }
          }
          module.exports = g;
        }, function(mixin, r, canCreateDiscussions) {
          var word;
          var m;
          !function(canCreateDiscussions) {
            /**
             * @return {undefined}
             */
            var hide = function() {
              /** @type {!Array<?>} */
              var e = Array.prototype.slice.call(arguments);
              if ("function" == typeof e[0]) {
                e[0].apply(null, e.splice(1));
              }
            };
            /**
             * @param {!Function} fn
             * @return {undefined}
             */
            var _nextTick = function(fn) {
              if ("function" == typeof setImmediate) {
                setImmediate(fn);
              } else {
                if (void 0 !== obj && obj.nextTick) {
                  obj.nextTick(fn);
                } else {
                  setTimeout(fn, 0);
                }
              }
            };
            /**
             * @param {!Object} source
             * @return {?}
             */
            var merge = function(source) {
              /**
               * @param {number} key
               * @return {?}
               */
              var callback = function(key) {
                /**
                 * @return {?}
                 */
                var end = function() {
                  return source.length && source[key].apply(null, arguments), end.next();
                };
                return end.next = function() {
                  return key < source.length - 1 ? callback(key + 1) : null;
                }, end;
              };
              return callback(0);
            };
            /** @type {function(*): boolean} */
            var pvFactor = Array.isArray || function(obj) {
              return "[object Array]" === Object.prototype.toString.call(obj);
            };
            /**
             * @param {!Object} key
             * @param {!Object} callback
             * @param {string} val
             * @return {?}
             */
            var f = function(key, callback, val) {
              /** @type {!Function} */
              var func = val ? _nextTick : hide;
              if (callback = callback || function() {
              }, !pvFactor(key)) {
                /** @type {!Error} */
                var unsupportedError = new Error("First argument to waterfall must be an array of functions");
                return callback(unsupportedError);
              }
              if (!key.length) {
                return callback();
              }
              /**
               * @param {!Function} node
               * @return {?}
               */
              var fn = function(node) {
                return function(n) {
                  if (n) {
                    callback.apply(null, arguments);
                    /**
                     * @return {undefined}
                     */
                    callback = function() {
                    };
                  } else {
                    /** @type {!Array<?>} */
                    var list = Array.prototype.slice.call(arguments, 1);
                    var id = node.next();
                    if (id) {
                      list.push(fn(id));
                    } else {
                      list.push(callback);
                    }
                    func(function() {
                      node.apply(null, list);
                    });
                  }
                };
              };
              fn(merge(key))();
            };
            /** @type {!Array} */
            word = [];
            if (void 0 !== (m = function() {
              return f;
            }.apply(r, word))) {
              mixin.exports = m;
            }
          }();
        }, function($module, exports, require) {
          /**
           * @param {number} str
           * @param {!Object} tok
           * @return {?}
           */
          function $(str, tok) {
            return null === str || void 0 === str || false === str ? tok : str;
          }
          /**
           * @param {number} val
           * @return {?}
           */
          function isNaN(val) {
            return val !== val;
          }
          /**
           * @param {!Array} data
           * @param {number} batchSize
           * @param {!Object} callback
           * @return {?}
           */
          function init(data, batchSize, callback) {
            var i;
            /** @type {!Array} */
            var ret = [];
            /** @type {!Array} */
            var source = [];
            /** @type {number} */
            i = 0;
            for (; i < data.length; i++) {
              if (i % batchSize == 0 && source.length) {
                ret.push(source);
                /** @type {!Array} */
                source = [];
              }
              source.push(data[i]);
            }
            if (source.length) {
              if (callback) {
                /** @type {number} */
                i = source.length;
                for (; i < batchSize; i++) {
                  source.push(callback);
                }
              }
              ret.push(source);
            }
            return ret;
          }
          /**
           * @param {?} str
           * @return {?}
           */
          function capitalize(str) {
            str = $(str, "");
            var zval = str.toLowerCase();
            return r.copySafeness(str, zval.charAt(0).toUpperCase() + zval.slice(1));
          }
          /**
           * @param {!Array} str
           * @param {number} length
           * @return {?}
           */
          function center(str, length) {
            if (str = $(str, ""), length = length || 80, str.length >= length) {
              return str;
            }
            /** @type {number} */
            var spaces = length - str.length;
            var pre = _.repeat(" ", spaces / 2 - spaces % 2);
            var post = _.repeat(" ", spaces / 2);
            return r.copySafeness(str, pre + str + post);
          }
          /**
           * @param {?} name
           * @param {string} type
           * @param {!Function} i
           * @return {?}
           */
          function mixin(name, type, i) {
            return i ? name || type : void 0 !== name ? name : type;
          }
          /**
           * @param {!Object} name
           * @param {?} index
           * @param {?} count
           * @return {?}
           */
          function render(name, index, count) {
            if (!_.isObject(name)) {
              throw new _.TemplateError("dictsort filter: val must be an object");
            }
            /** @type {!Array} */
            var linesForKeySorted = [];
            var k;
            for (k in name) {
              linesForKeySorted.push([k, name[k]]);
            }
            var i;
            if (void 0 === count || "key" === count) {
              /** @type {number} */
              i = 0;
            } else {
              if ("value" !== count) {
                throw new _.TemplateError("dictsort filter: You can only sort by either key or value");
              }
              /** @type {number} */
              i = 1;
            }
            return linesForKeySorted.sort(function(scriptIds, requireOptionKeys) {
              var id = scriptIds[i];
              var key = requireOptionKeys[i];
              return index || (_.isString(id) && (id = id.toUpperCase()), _.isString(key) && (key = key.toUpperCase())), id > key ? 1 : id === key ? 0 : -1;
            }), linesForKeySorted;
          }
          /**
           * @param {!Function} e
           * @param {?} space
           * @return {?}
           */
          function dump(e, space) {
            return JSON.stringify(e, null, space);
          }
          /**
           * @param {number} value
           * @return {?}
           */
          function stringify(value) {
            return value instanceof r.SafeString ? value : (value = null === value || void 0 === value ? "" : value, r.markSafe(_.escape(value.toString())));
          }
          /**
           * @param {number} str
           * @return {?}
           */
          function create(str) {
            return str instanceof r.SafeString ? str : (str = null === str || void 0 === str ? "" : str, r.markSafe(str.toString()));
          }
          /**
           * @param {!Object} keywordGetter
           * @return {?}
           */
          function head(keywordGetter) {
            return keywordGetter[0];
          }
          /**
           * @param {(Node|NodeList|string)} properties
           * @param {?} key
           * @return {?}
           */
          function group(properties, key) {
            return _.groupBy(properties, key);
          }
          /**
           * @param {?} str
           * @param {number} add
           * @param {boolean} editable
           * @return {?}
           */
          function indent(str, add, editable) {
            if ("" === (str = $(str, ""))) {
              return "";
            }
            add = add || 4;
            var navLinksArr = str.split("\n");
            var construct = _.repeat(" ", add);
            var input = navLinksArr.map(function(extension, size) {
              return 0 !== size || editable ? "" + construct + extension + "\n" : extension + "\n";
            }).join("");
            return r.copySafeness(str, input);
          }
          /**
           * @param {string} data
           * @param {!Object} type
           * @param {string} key
           * @return {?}
           */
          function join(data, type, key) {
            return type = type || "", key && (data = _.map(data, function(translationJSON) {
              return translationJSON[key];
            })), data.join(type);
          }
          /**
           * @param {!Object} require
           * @return {?}
           */
          function n(require) {
            return require[require.length - 1];
          }
          /**
           * @param {number} address
           * @return {?}
           */
          function bind(address) {
            var value = $(address, "");
            return void 0 !== value ? "function" == typeof Map && value instanceof Map || "function" == typeof Set && value instanceof Set ? value.size : !_.isObject(value) || value instanceof r.SafeString ? value.length : _.keys(value).length : 0;
          }
          /**
           * @param {!Object} name
           * @return {?}
           */
          function get(name) {
            if (_.isString(name)) {
              return name.split("");
            }
            if (_.isObject(name)) {
              return _._entries(name || {}).map(function(fieldMaster) {
                return {
                  key : fieldMaster[0],
                  value : fieldMaster[1]
                };
              });
            }
            if (_.isArray(name)) {
              return name;
            }
            throw new _.TemplateError("list filter: type not iterable");
          }
          /**
           * @param {(number|string)} e
           * @return {?}
           */
          function position(e) {
            return e = $(e, ""), e.toLowerCase();
          }
          /**
           * @param {?} val
           * @return {?}
           */
          function b(val) {
            return null === val || void 0 === val ? "" : r.copySafeness(val, val.replace(/\r\n|\n/g, "<br />\n"));
          }
          /**
           * @param {!Object} bytes
           * @return {?}
           */
          function random(bytes) {
            return bytes[Math.floor(Math.random() * bytes.length)];
          }
          /**
           * @param {!Array} selector
           * @param {number} event
           * @return {?}
           */
          function findSelect2Entry(selector, event) {
            return selector.filter(function(chartConfig) {
              return !chartConfig[event];
            });
          }
          /**
           * @param {!Array} data
           * @param {number} n
           * @return {?}
           */
          function everyNth(data, n) {
            return data.filter(function(aomask) {
              return !!aomask[n];
            });
          }
          /**
           * @param {!Object} str
           * @param {string} value
           * @param {string} i
           * @param {number} position
           * @return {?}
           */
          function replace(str, value, i, position) {
            /** @type {!Object} */
            var val = str;
            if (value instanceof RegExp) {
              return str.replace(value, i);
            }
            if (void 0 === position) {
              /** @type {number} */
              position = -1;
            }
            /** @type {string} */
            var prefix = "";
            if ("number" == typeof value) {
              /** @type {string} */
              value = "" + value;
            } else {
              if ("string" != typeof value) {
                return str;
              }
            }
            if ("number" == typeof str && (str = "" + str), "string" != typeof str && !(str instanceof r.SafeString)) {
              return str;
            }
            if ("" === value) {
              return prefix = i + str.split("").join(i) + i, r.copySafeness(str, prefix);
            }
            var index = str.indexOf(value);
            if (0 === position || -1 === index) {
              return str;
            }
            /** @type {number} */
            var j = 0;
            /** @type {number} */
            var current_index = 0;
            for (; index > -1 && (-1 === position || current_index < position);) {
              /** @type {string} */
              prefix = prefix + (str.substring(j, index) + i);
              j = index + value.length;
              current_index++;
              index = str.indexOf(value, j);
            }
            return j < str.length && (prefix = prefix + str.substring(j)), r.copySafeness(val, prefix);
          }
          /**
           * @param {undefined} input
           * @return {?}
           */
          function reverse(input) {
            var result;
            return result = _.isString(input) ? get(input) : _.map(input, function(all) {
              return all;
            }), result.reverse(), _.isString(input) ? r.copySafeness(input, result.join("")) : result;
          }
          /**
           * @param {number} x
           * @param {number} n
           * @param {string} p
           * @return {?}
           */
          function round(x, n, p) {
            n = n || 0;
            /** @type {number} */
            var sigma = Math.pow(10, n);
            return ("ceil" === p ? Math.ceil : "floor" === p ? Math.floor : Math.round)(x * sigma) / sigma;
          }
          /**
           * @param {?} array
           * @param {number} n
           * @param {!Object} val
           * @return {?}
           */
          function slice(array, n, val) {
            /** @type {number} */
            var factor = Math.floor(array.length / n);
            /** @type {number} */
            var start = array.length % n;
            /** @type {!Array} */
            var parts = [];
            /** @type {number} */
            var a = 0;
            /** @type {number} */
            var x = 0;
            for (; x < n; x++) {
              /** @type {number} */
              var value = a + x * factor;
              if (x < start) {
                a++;
              }
              /** @type {number} */
              var mid = a + (x + 1) * factor;
              var str = array.slice(value, mid);
              if (val && x >= start) {
                str.push(val);
              }
              parts.push(str);
            }
            return parts;
          }
          /**
           * @param {!Array} e
           * @param {string} c
           * @param {number} mat
           * @return {?}
           */
          function sum(e, c, mat) {
            return void 0 === mat && (mat = 0), c && (e = _.map(e, function(cellids) {
              return cellids[c];
            })), mat + e.reduce(function(buckets, name) {
              return buckets + name;
            }, 0);
          }
          /**
           * @param {!Object} name
           * @return {?}
           */
          function time(name) {
            return r.copySafeness(name, name);
          }
          /**
           * @param {?} input
           * @param {(!Function|boolean)} key
           * @return {?}
           */
          function L(input, key) {
            input = $(input, "");
            /** @type {!RegExp} */
            var rx = /<\/?([a-z][a-z0-9]*)\b[^>]*>|\x3c!--[\s\S]*?--\x3e/gi;
            var example = trim(input.replace(rx, ""));
            /** @type {string} */
            var res = "";
            return res = key ? example.replace(/^ +| +$/gm, "").replace(/ +/g, " ").replace(/(\r\n)/g, "\n").replace(/\n\n\n+/g, "\n\n") : example.replace(/\s+/gi, " "), r.copySafeness(input, res);
          }
          /**
           * @param {?} str
           * @return {?}
           */
          function camelCase(str) {
            str = $(str, "");
            var drilldownLevelLabels = str.split(" ").map(function(part) {
              return capitalize(part);
            });
            return r.copySafeness(str, drilldownLevelLabels.join(" "));
          }
          /**
           * @param {string} val
           * @return {?}
           */
          function trim(val) {
            return r.copySafeness(val, val.replace(/^\s*|\s*$/g, ""));
          }
          /**
           * @param {string} text
           * @param {number} length
           * @param {?} type
           * @param {number} s
           * @return {?}
           */
          function truncate(text, length, type, s) {
            /** @type {string} */
            var val = text;
            if (text = $(text, ""), length = length || 255, text.length <= length) {
              return text;
            }
            if (type) {
              text = text.substring(0, length);
            } else {
              var index = text.lastIndexOf(" ", length);
              if (-1 === index) {
                /** @type {number} */
                index = length;
              }
              text = text.substring(0, index);
            }
            return text = text + (void 0 !== s && null !== s ? s : "..."), r.copySafeness(val, text);
          }
          /**
           * @param {number} e
           * @return {?}
           */
          function key(e) {
            return e = $(e, ""), e.toUpperCase();
          }
          /**
           * @param {number} data
           * @return {?}
           */
          function send(data) {
            /** @type {function(string): string} */
            var encode = encodeURIComponent;
            return _.isString(data) ? encode(data) : (_.isArray(data) ? data : _._entries(data)).map(function(val) {
              var value = val[0];
              var val2 = val[1];
              return encode(value) + "=" + encode(val2);
            }).join("&");
          }
          /**
           * @param {string} imgFileName
           * @param {number} x
           * @param {(number|string)} n
           * @return {?}
           */
          function loadFiltersFromUrl(imgFileName, x, n) {
            if (isNaN(x)) {
              /** @type {number} */
              x = 1 / 0;
            }
            /** @type {string} */
            var opt_by = true === n ? ' rel="nofollow"' : "";
            return imgFileName.split(/(\s+)/).filter(function(connectionConfigs) {
              return connectionConfigs && connectionConfigs.length;
            }).map(function(a) {
              var e = a.match(W);
              var m = e ? e[1] : a;
              var pivot_angle = m.substr(0, x);
              return _updateShellBoundsAndConformDims.test(m) ? '<a href="' + m + '"' + opt_by + ">" + pivot_angle + "</a>" : timeBack.test(m) ? '<a href="http://' + m + '"' + opt_by + ">" + pivot_angle + "</a>" : attReg.test(m) ? '<a href="mailto:' + m + '">' + m + "</a>" : extIds.test(m) ? '<a href="http://' + m + '"' + opt_by + ">" + pivot_angle + "</a>" : a;
            }).join("");
          }
          /**
           * @param {number} s
           * @return {?}
           */
          function h(s) {
            s = $(s, "");
            var step = s ? s.match(/\w+/g) : null;
            return step ? step.length : null;
          }
          /**
           * @param {?} e
           * @param {number} t
           * @return {?}
           */
          function value(e, t) {
            /** @type {number} */
            var x = parseFloat(e);
            return isNaN(x) ? t : x;
          }
          /**
           * @param {?} name
           * @param {number} value
           * @return {?}
           */
          function int(name, value) {
            /** @type {number} */
            var num = parseInt(name, 10);
            return isNaN(num) ? value : num;
          }
          var _ = require(1);
          var r = require(2);
          exports = $module.exports = {};
          /** @type {function(?): number} */
          exports.abs = Math.abs;
          /** @type {function(!Array, number, !Object): ?} */
          exports.batch = init;
          /** @type {function(?): ?} */
          exports.capitalize = capitalize;
          /** @type {function(!Array, number): ?} */
          exports.center = center;
          /** @type {function(?, string, !Function): ?} */
          exports.default = mixin;
          /** @type {function(!Object, ?, ?): ?} */
          exports.dictsort = render;
          /** @type {function(!Function, ?): ?} */
          exports.dump = dump;
          /** @type {function(number): ?} */
          exports.escape = stringify;
          /** @type {function(number): ?} */
          exports.safe = create;
          /** @type {function(!Object): ?} */
          exports.first = head;
          /** @type {function((Node|NodeList|string), ?): ?} */
          exports.groupby = group;
          /** @type {function(?, number, boolean): ?} */
          exports.indent = indent;
          /** @type {function(string, !Object, string): ?} */
          exports.join = join;
          /** @type {function(!Object): ?} */
          exports.last = n;
          /** @type {function(number): ?} */
          exports.length = bind;
          /** @type {function(!Object): ?} */
          exports.list = get;
          /** @type {function((number|string)): ?} */
          exports.lower = position;
          /** @type {function(?): ?} */
          exports.nl2br = b;
          /** @type {function(!Object): ?} */
          exports.random = random;
          /** @type {function(!Array, number): ?} */
          exports.rejectattr = findSelect2Entry;
          /** @type {function(!Array, number): ?} */
          exports.selectattr = everyNth;
          /** @type {function(!Object, string, string, number): ?} */
          exports.replace = replace;
          /** @type {function(undefined): ?} */
          exports.reverse = reverse;
          /** @type {function(number, number, string): ?} */
          exports.round = round;
          /** @type {function(?, number, !Object): ?} */
          exports.slice = slice;
          /** @type {function(!Array, string, number): ?} */
          exports.sum = sum;
          exports.sort = r.makeMacro(["value", "reverse", "case_sensitive", "attribute"], [], function(sockets, inverse, _noMismatch, key) {
            var keys = _.map(sockets, function(canCreateDiscussions) {
              return canCreateDiscussions;
            });
            return keys.sort(function(value, res) {
              var val = key ? value[key] : value;
              var result = key ? res[key] : res;
              return !_noMismatch && _.isString(val) && _.isString(result) && (val = val.toLowerCase(), result = result.toLowerCase()), val < result ? inverse ? 1 : -1 : val > result ? inverse ? -1 : 1 : 0;
            }), keys;
          });
          /** @type {function(!Object): ?} */
          exports.string = time;
          /** @type {function(?, (!Function|boolean)): ?} */
          exports.striptags = L;
          /** @type {function(?): ?} */
          exports.title = camelCase;
          /** @type {function(string): ?} */
          exports.trim = trim;
          /** @type {function(string, number, ?, number): ?} */
          exports.truncate = truncate;
          /** @type {function(number): ?} */
          exports.upper = key;
          /** @type {function(number): ?} */
          exports.urlencode = send;
          /** @type {!RegExp} */
          var W = /^(?:\(|<|&lt;)?(.*?)(?:\.|,|\)|\n|&gt;)?$/;
          /** @type {!RegExp} */
          var attReg = /^[\w.!#$%&'*+\-\/=?\^`{|}~]+@[a-z\d\-]+(\.[a-z\d\-]+)+$/i;
          /** @type {!RegExp} */
          var _updateShellBoundsAndConformDims = /^https?:\/\/.*$/;
          /** @type {!RegExp} */
          var timeBack = /^www\./;
          /** @type {!RegExp} */
          var extIds = /\.(?:org|net|com)(?::|\/|$)/;
          /** @type {function(string, number, (number|string)): ?} */
          exports.urlize = loadFiltersFromUrl;
          /** @type {function(number): ?} */
          exports.wordcount = h;
          /** @type {function(?, number): ?} */
          exports.float = value;
          /** @type {function(?, number): ?} */
          exports.int = int;
          /** @type {function(?, string, !Function): ?} */
          exports.d = exports.default;
          /** @type {function(number): ?} */
          exports.e = exports.escape;
        }, function(canCreateDiscussions, options, saveNotifs) {
          /**
           * @param {?} fn
           * @return {?}
           */
          function callable(fn) {
            return "function" == typeof fn;
          }
          /**
           * @param {number} callback
           * @return {?}
           */
          function extractPresetLocal(callback) {
            return void 0 !== callback;
          }
          /**
           * @param {(boolean|number|string)} n
           * @param {(boolean|number|string)} i
           * @return {?}
           */
          function i(n, i) {
            return n % i == 0;
          }
          /**
           * @param {?} str
           * @return {?}
           */
          function escaped(str) {
            return str instanceof SafeString;
          }
          /**
           * @param {?} val
           * @param {?} start
           * @return {?}
           */
          function s(val, start) {
            return val === start;
          }
          /**
           * @param {number} i
           * @return {?}
           */
          function even(i) {
            return i % 2 == 0;
          }
          /**
           * @param {?} insertedIndex
           * @return {?}
           */
          function l(insertedIndex) {
            return !insertedIndex;
          }
          /**
           * @param {(boolean|number|string)} nTilesLoaded
           * @param {(boolean|number|string)} nTilesToLoad
           * @return {?}
           */
          function refreshLoadBar(nTilesLoaded, nTilesToLoad) {
            return nTilesLoaded >= nTilesToLoad;
          }
          /**
           * @param {(Date|number)} _num1
           * @param {!Date} _num2
           * @return {?}
           */
          function getRatio(_num1, _num2) {
            return _num1 > _num2;
          }
          /**
           * @param {(boolean|number|string)} mid_OR_high
           * @param {(boolean|number|string)} high_OR_null
           * @return {?}
           */
          function inRange(mid_OR_high, high_OR_null) {
            return mid_OR_high <= high_OR_null;
          }
          /**
           * @param {(boolean|number|string)} p
           * @param {(boolean|number|string)} s
           * @return {?}
           */
          function p(p, s) {
            return p < s;
          }
          /**
           * @param {string} n
           * @return {?}
           */
          function lower(n) {
            return n.toLowerCase() === n;
          }
          /**
           * @param {?} position
           * @param {?} index
           * @return {?}
           */
          function idx(position, index) {
            return position !== index;
          }
          /**
           * @param {!Object} lookHarder
           * @return {?}
           */
          function list(lookHarder) {
            return null === lookHarder;
          }
          /**
           * @param {!Object} name
           * @return {?}
           */
          function index(name) {
            return "number" == typeof name;
          }
          /**
           * @param {number} callback
           * @return {?}
           */
          function y(callback) {
            return callback % 2 == 1;
          }
          /**
           * @param {!Object} name
           * @return {?}
           */
          function css(name) {
            return "string" == typeof name;
          }
          /**
           * @param {?} val
           * @return {?}
           */
          function _truthy(val) {
            return !!val;
          }
          /**
           * @param {!Array} selector
           * @return {?}
           */
          function clickWithWebdriver(selector) {
            return void 0 === selector;
          }
          /**
           * @param {string} s
           * @return {?}
           */
          function upper(s) {
            return s.toUpperCase() === s;
          }
          /**
           * @param {!Object} data
           * @return {?}
           */
          function config(data) {
            return "undefined" != typeof Symbol ? !!data[Symbol.iterator] : Array.isArray(data) || "string" == typeof data;
          }
          /**
           * @param {?} value
           * @return {?}
           */
          function m(value) {
            /** @type {boolean} */
            var undefined = null !== value && void 0 !== value && "object" == typeof value && !Array.isArray(value);
            return Set ? undefined && !(value instanceof Set) : undefined;
          }
          var SafeString = saveNotifs(2).SafeString;
          /** @type {function(?): ?} */
          options.callable = callable;
          /** @type {function(number): ?} */
          options.defined = extractPresetLocal;
          /** @type {function((boolean|number|string), (boolean|number|string)): ?} */
          options.divisibleby = i;
          /** @type {function(?): ?} */
          options.escaped = escaped;
          /** @type {function(?, ?): ?} */
          options.equalto = s;
          /** @type {function(?, ?): ?} */
          options.eq = options.equalto;
          /** @type {function(?, ?): ?} */
          options.sameas = options.equalto;
          /** @type {function(number): ?} */
          options.even = even;
          /** @type {function(?): ?} */
          options.falsy = l;
          /** @type {function((boolean|number|string), (boolean|number|string)): ?} */
          options.ge = refreshLoadBar;
          /** @type {function((Date|number), !Date): ?} */
          options.greaterthan = getRatio;
          /** @type {function((Date|number), !Date): ?} */
          options.gt = options.greaterthan;
          /** @type {function((boolean|number|string), (boolean|number|string)): ?} */
          options.le = inRange;
          /** @type {function((boolean|number|string), (boolean|number|string)): ?} */
          options.lessthan = p;
          /** @type {function((boolean|number|string), (boolean|number|string)): ?} */
          options.lt = options.lessthan;
          /** @type {function(string): ?} */
          options.lower = lower;
          /** @type {function(?, ?): ?} */
          options.ne = idx;
          /** @type {function(!Object): ?} */
          options.null = list;
          /** @type {function(!Object): ?} */
          options.number = index;
          /** @type {function(number): ?} */
          options.odd = y;
          /** @type {function(!Object): ?} */
          options.string = css;
          /** @type {function(?): ?} */
          options.truthy = _truthy;
          /** @type {function(!Array): ?} */
          options.undefined = clickWithWebdriver;
          /** @type {function(string): ?} */
          options.upper = upper;
          /** @type {function(!Object): ?} */
          options.iterable = config;
          /** @type {function(?): ?} */
          options.mapping = m;
        }, function(module, canCreateDiscussions, n) {
          /**
           * @param {!NodeList} items
           * @return {?}
           */
          function cycler(items) {
            /** @type {number} */
            var index = -1;
            return {
              current : null,
              reset : function() {
                /** @type {number} */
                index = -1;
                /** @type {null} */
                this.current = null;
              },
              next : function() {
                return index++, index >= items.length && (index = 0), this.current = items[index], this.current;
              }
            };
          }
          /**
           * @param {!Object} values
           * @return {?}
           */
          function joiner(values) {
            values = values || ",";
            /** @type {boolean} */
            var decoder = true;
            return function() {
              var string = decoder ? "" : values;
              return decoder = false, string;
            };
          }
          /**
           * @return {?}
           */
          function globals() {
            return {
              range : function(c, p, step) {
                if (void 0 === p) {
                  /** @type {number} */
                  p = c;
                  /** @type {number} */
                  c = 0;
                  /** @type {number} */
                  step = 1;
                } else {
                  if (!step) {
                    /** @type {number} */
                    step = 1;
                  }
                }
                /** @type {!Array} */
                var startToEnd = [];
                if (step > 0) {
                  /** @type {number} */
                  var i = c;
                  for (; i < p; i = i + step) {
                    startToEnd.push(i);
                  }
                } else {
                  /** @type {number} */
                  var i = c;
                  for (; i > p; i = i + step) {
                    startToEnd.push(i);
                  }
                }
                return startToEnd;
              },
              cycler : function() {
                return cycler(Array.prototype.slice.call(arguments));
              },
              joiner : function(strings) {
                return joiner(strings);
              }
            };
          }
          /** @type {function(): ?} */
          module.exports = globals;
        }, function(mixin, canCreateDiscussions, __webpack_require__) {
          var API = __webpack_require__(0);
          /**
           * @param {!Object} name
           * @param {string} value
           * @return {?}
           */
          mixin.exports = function(name, value) {
            /**
             * @param {string} path
             * @param {!Object} opts
             * @return {undefined}
             */
            function page(path, opts) {
              if (this.name = path, this.path = path, this.defaultEngine = opts.defaultEngine, this.ext = API.extname(path), !this.ext && !this.defaultEngine) {
                throw new Error("No default engine was specified and no extension was provided.");
              }
              if (!this.ext) {
                this.name += this.ext = ("." !== this.defaultEngine[0] ? "." : "") + this.defaultEngine;
              }
            }
            return page.prototype.render = function(c, t) {
              name.render(this.name, c, t);
            }, value.set("view", page), value.set("nunjucksEnv", name), name;
          };
        }, function(module, canCreateDiscussions, n) {
          /**
           * @return {?}
           */
          function installCompat() {
            /**
             * @return {undefined}
             */
            function installCompat() {
              runtime.contextOrFrameLookup = load;
              runtime.memberLookup = orig_memberLookup;
              if (Compiler) {
                Compiler.prototype.assertType = r;
              }
              if (Parser) {
                Parser.prototype.parseAggregate = o;
              }
            }
            /**
             * @param {!Array} data
             * @param {number} offset
             * @param {number} to
             * @param {number} i
             * @return {?}
             */
            function append(data, offset, to, i) {
              data = data || [];
              if (null === offset) {
                /** @type {number} */
                offset = i < 0 ? data.length - 1 : 0;
              }
              if (null === to) {
                to = i < 0 ? -1 : data.length;
              } else {
                if (to < 0) {
                  to = to + data.length;
                }
              }
              if (offset < 0) {
                offset = offset + data.length;
              }
              /** @type {!Array} */
              var row = [];
              /** @type {number} */
              var j = offset;
              for (; !(j < 0 || j > data.length) && !(i > 0 && j >= to) && !(i < 0 && j <= to); j = j + i) {
                row.push(runtime.memberLookup(data, j));
              }
              return row;
            }
            /**
             * @param {?} source
             * @param {string} keys
             * @return {?}
             */
            function get(source, keys) {
              return Object.prototype.hasOwnProperty.call(source, keys);
            }
            var r;
            var o;
            var runtime = this.runtime;
            var utils = this.lib;
            var Compiler = this.compiler.Compiler;
            var Parser = this.parser.Parser;
            var load = (this.nodes, this.lexer, runtime.contextOrFrameLookup);
            var orig_memberLookup = runtime.memberLookup;
            if (Compiler) {
              r = Compiler.prototype.assertType;
            }
            if (Parser) {
              o = Parser.prototype.parseAggregate;
            }
            /**
             * @param {!Object} context
             * @param {!Object} frame
             * @param {string} key
             * @return {?}
             */
            runtime.contextOrFrameLookup = function(context, frame, key) {
              var val = load.apply(this, arguments);
              if (void 0 !== val) {
                return val;
              }
              switch(key) {
                case "True":
                  return true;
                case "False":
                  return false;
                case "None":
                  return null;
                default:
                  return;
              }
            };
            var options = {
              pop : function(index) {
                if (void 0 === index) {
                  return this.pop();
                }
                if (index >= this.length || index < 0) {
                  throw new Error("KeyError");
                }
                return this.splice(index, 1);
              },
              append : function(event) {
                return this.push(event);
              },
              remove : function(o) {
                /** @type {number} */
                var i = 0;
                for (; i < this.length; i++) {
                  if (this[i] === o) {
                    return this.splice(i, 1);
                  }
                }
                throw new Error("ValueError");
              },
              count : function(letter) {
                /** @type {number} */
                var element_count = 0;
                /** @type {number} */
                var i = 0;
                for (; i < this.length; i++) {
                  if (this[i] === letter) {
                    element_count++;
                  }
                }
                return element_count;
              },
              index : function(value) {
                var index;
                if (-1 === (index = this.indexOf(value))) {
                  throw new Error("ValueError");
                }
                return index;
              },
              find : function(value) {
                return this.indexOf(value);
              },
              insert : function(prop, obj) {
                return this.splice(prop, 0, obj);
              }
            };
            var OBJECT_MEMBERS = {
              items : function() {
                return utils._entries(this);
              },
              values : function() {
                return utils._values(this);
              },
              keys : function() {
                return utils.keys(this);
              },
              get : function(name, jpath) {
                var options = this[name];
                return void 0 === options && (options = jpath), options;
              },
              has_key : function(key) {
                return get(this, key);
              },
              pop : function(index, array) {
                var element = this[index];
                if (void 0 === element && void 0 !== array) {
                  /** @type {number} */
                  element = array;
                } else {
                  if (void 0 === element) {
                    throw new Error("KeyError");
                  }
                  delete this[index];
                }
                return element;
              },
              popitem : function() {
                var tilesToCheck = utils.keys(this);
                if (!tilesToCheck.length) {
                  throw new Error("KeyError");
                }
                var t = tilesToCheck[0];
                var PL$41 = this[t];
                return delete this[t], [t, PL$41];
              },
              setdefault : function(aAttr, aDefault) {
                return void 0 === aDefault && (aDefault = null), aAttr in this || (this[aAttr] = aDefault), this[aAttr];
              },
              update : function(info) {
                return utils._assign(this, info), null;
              }
            };
            return OBJECT_MEMBERS.iteritems = OBJECT_MEMBERS.items, OBJECT_MEMBERS.itervalues = OBJECT_MEMBERS.values, OBJECT_MEMBERS.iterkeys = OBJECT_MEMBERS.keys, runtime.memberLookup = function(model, val, autoescape) {
              return 4 === arguments.length ? append.apply(this, arguments) : (model = model || {}, utils.isArray(model) && get(options, val) ? options[val].bind(model) : utils.isObject(model) && get(OBJECT_MEMBERS, val) ? OBJECT_MEMBERS[val].bind(model) : orig_memberLookup.apply(this, arguments));
            }, installCompat;
          }
          /** @type {function(): ?} */
          module.exports = installCompat;
        }]);
      });
    }).call(exports, __webpack_require__("K3Oa").setImmediate, __webpack_require__("RxL3"));
  },
  "3QbQ" : function(mixin, doPost) {
    /**
     * @return {?}
     */
    mixin.exports = function() {
      /** @type {number} */
      var argl = arguments.length;
      /** @type {!Array} */
      var newItems = [];
      /** @type {number} */
      var i = 0;
      for (; i < argl; i++) {
        newItems[i] = arguments[i];
      }
      if (newItems = newItems.filter(function(canCreateDiscussions) {
        return null != canCreateDiscussions;
      }), 0 !== newItems.length) {
        return 1 === newItems.length ? newItems[0] : newItems.reduce(function(CropAreaRectangle, prevModFn) {
          return function() {
            CropAreaRectangle.apply(this, arguments);
            prevModFn.apply(this, arguments);
          };
        });
      }
    };
  },
  "4/IU" : function(mixin, args, n) {
    (function($) {
      var o = n("gT+X");
      var f = n("bVOP");
      var graph = n("YWnE");
      /**
       * @param {string} do_not_create
       * @return {undefined}
       */
      var get = function(do_not_create) {
        $("#app_iframe").remove();
        $("body").append("<iframe id='app_iframe' src='" + do_not_create + "' style='display:none'></iframe>");
      };
      /**
       * @param {!Object} options
       * @return {undefined}
       */
      var success = function(options) {
        if (["home", "detail", "mediaProfile"].indexOf(options.type || "home") > -1) {
          f.androidLocalServer(options).then(function(canCreateDiscussions) {
          }, function(canCreateDiscussions) {
            get(options.nativeLink);
          });
        } else {
          get(options.nativeLink);
        }
      };
      /**
       * @param {!Object} data
       * @return {undefined}
       */
      var init = function(data) {
        /** @type {string} */
        var href = location.href;
        var pversion = o.os.version;
        if (pversion >= 9 && !o.browser.qqbrowser) {
          /** @type {string} */
          var url = "//toutiao.com/m/detail/?";
          /** @type {string} */
          var m = "click_" + (o.browser.weixin ? "weixin" : "wap") + "_ios_deeplink";
          var param = data.nativeLink.replace(/gd_label=(\w+)/, "gd_label=" + m);
          if (-1 === param.indexOf("gd_label")) {
            /** @type {string} */
            param = param + ("&gd_label=" + m);
          }
          var p = {
            group_id : "",
            item_id : "",
            scheme : encodeURIComponent(param)
          };
          url = url + graph.toQuery(p);
          setTimeout(function() {
            location.href = data.universalLink || url;
          }, 300);
        } else {
          if (pversion >= 9) {
            var sf = o.browser.safari;
            /** @type {number} */
            var ngiScroll_timeout = sf ? 2E3 : 1300;
            setTimeout(function() {
              location.href = data.nativeLink;
              setTimeout(function() {
                if ("hidden" === graph.pageVisible()) {
                  /** @type {string} */
                  location.href = href;
                }
              }, ngiScroll_timeout);
            }, 10);
          } else {
            get(data.nativeLink);
          }
        }
      };
      /**
       * @param {!Object} data
       * @return {?}
       */
      var callback = function(data) {
        if ("m.toutiaoribao.cn" === location.host) {
          return void get(data.nativeLink);
        }
        if (o.os.ios) {
          o.os.version;
        }
        o.browser.weixin;
        if (o.os.ios) {
          init(data);
        } else {
          success(data);
        }
      };
      mixin.exports = {
        jumpToNativeapp : callback
      };
    }).call(args, n("gXQ3"));
  },
  "6+Kz" : function(cond, t, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    Object.defineProperty(t, "__esModule", {
      value : true
    });
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _deepAssign = __webpack_require__("mRYa");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _UiRippleInk = __webpack_require__("IJ1K");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    __webpack_require__("6AHJ");
    var offsetFromCenter = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _UiIcon2.default)(this, Agent), (0, _deepAssign2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).apply(this, arguments));
      }
      return (0, _UiRippleInk2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "render",
        value : function() {
          return _prepareStyleProperties2.default.createElement("div", {
            className : "audit-container"
          }, _prepareStyleProperties2.default.createElement("p", null, "Copyright \u00a9 2017 \u5934\u6761\u65e5\u62a5 \u7248\u6743\u6240\u6709 \u4eacICP\u590717027596 "), _prepareStyleProperties2.default.createElement("p", null, "\u5317\u4eac\u6296\u52a8\u9752\u6625\u79d1\u6280\u6709\u9650\u516c\u53f8"), _prepareStyleProperties2.default.createElement("p", null, "\u5317\u4eac\u5e02\u6d77\u6dc0\u533a\u4fe1\u606f\u8def\u753228\u53f7C\u5ea7\uff08\u4e8c\u5c42\uff0902A\u5ba4-345\u53f7"), _prepareStyleProperties2.default.createElement("p",
          null, "010-58341810"));
        }
      }]), Agent;
    }(_prepareStyleProperties.Component);
    t.default = offsetFromCenter;
  },
  "6AHJ" : function(formatters, customFormatters) {
  },
  "6isv" : function(module, exports, __webpack_require__) {
    __webpack_require__("Pj6p");
    module.exports = __webpack_require__("qGgm").Object.setPrototypeOf;
  },
  "6uqe" : function(module, exports, __weex_require__) {
    /** @type {function(this:Object, *): boolean} */
    var has = Object.prototype.hasOwnProperty;
    var w = function() {
      /** @type {!Array} */
      var newNodeLists = [];
      /** @type {number} */
      var alpha255 = 0;
      for (; alpha255 < 256; ++alpha255) {
        newNodeLists.push("%" + ((alpha255 < 16 ? "0" : "") + alpha255.toString(16)).toUpperCase());
      }
      return newNodeLists;
    }();
    /**
     * @param {!Array} array
     * @return {?}
     */
    var transform = function(array) {
      var i;
      for (; array.length;) {
        var subj = array.pop();
        if (i = subj.obj[subj.prop], Array.isArray(i)) {
          /** @type {!Array} */
          var replacement = [];
          /** @type {number} */
          var i1 = 0;
          for (; i1 < i.length; ++i1) {
            if (void 0 !== i[i1]) {
              replacement.push(i[i1]);
            }
          }
          /** @type {!Array} */
          subj.obj[subj.prop] = replacement;
        }
      }
      return i;
    };
    /**
     * @param {!Object} arr
     * @param {boolean} options
     * @return {?}
     */
    exports.arrayToObject = function(arr, options) {
      /** @type {!Object} */
      var ret = options && options.plainObjects ? Object.create(null) : {};
      /** @type {number} */
      var i = 0;
      for (; i < arr.length; ++i) {
        if (void 0 !== arr[i]) {
          ret[i] = arr[i];
        }
      }
      return ret;
    };
    /**
     * @param {!Object} obj
     * @param {!Object} o
     * @param {boolean} options
     * @return {?}
     */
    exports.merge = function(obj, o, options) {
      if (!o) {
        return obj;
      }
      if ("object" != typeof o) {
        if (Array.isArray(obj)) {
          obj.push(o);
        } else {
          if ("object" != typeof obj) {
            return [obj, o];
          }
          if (options.plainObjects || options.allowPrototypes || !has.call(Object.prototype, o)) {
            /** @type {boolean} */
            obj[o] = true;
          }
        }
        return obj;
      }
      if ("object" != typeof obj) {
        return [obj].concat(o);
      }
      /** @type {!Object} */
      var request = obj;
      return Array.isArray(obj) && !Array.isArray(o) && (request = exports.arrayToObject(obj, options)), Array.isArray(obj) && Array.isArray(o) ? (o.forEach(function(val, key) {
        if (has.call(obj, key)) {
          if (obj[key] && "object" == typeof obj[key]) {
            obj[key] = exports.merge(obj[key], val, options);
          } else {
            obj.push(val);
          }
        } else {
          /** @type {!Object} */
          obj[key] = val;
        }
      }), obj) : Object.keys(o).reduce(function(obj, key) {
        var val = o[key];
        return has.call(obj, key) ? obj[key] = exports.merge(obj[key], val, options) : obj[key] = val, obj;
      }, request);
    };
    /**
     * @param {!Object} name
     * @param {!Object} value
     * @return {?}
     */
    exports.assign = function(name, value) {
      return Object.keys(value).reduce(function(section, k) {
        return section[k] = value[k], section;
      }, name);
    };
    /**
     * @param {string} str
     * @return {?}
     */
    exports.decode = function(str) {
      try {
        return decodeURIComponent(str.replace(/\+/g, " "));
      } catch (t) {
        return str;
      }
    };
    /**
     * @param {string} string
     * @return {?}
     */
    exports.encode = function(string) {
      if (0 === string.length) {
        return string;
      }
      /** @type {string} */
      var t = "string" == typeof string ? string : String(string);
      /** @type {string} */
      var s = "";
      /** @type {number} */
      var i = 0;
      for (; i < t.length; ++i) {
        /** @type {number} */
        var j = t.charCodeAt(i);
        if (45 === j || 46 === j || 95 === j || 126 === j || j >= 48 && j <= 57 || j >= 65 && j <= 90 || j >= 97 && j <= 122) {
          /** @type {string} */
          s = s + t.charAt(i);
        } else {
          if (j < 128) {
            s = s + w[j];
          } else {
            if (j < 2048) {
              /** @type {string} */
              s = s + (w[192 | j >> 6] + w[128 | 63 & j]);
            } else {
              if (j < 55296 || j >= 57344) {
                /** @type {string} */
                s = s + (w[224 | j >> 12] + w[128 | j >> 6 & 63] + w[128 | 63 & j]);
              } else {
                /** @type {number} */
                i = i + 1;
                /** @type {number} */
                j = 65536 + ((1023 & j) << 10 | 1023 & t.charCodeAt(i));
                /** @type {string} */
                s = s + (w[240 | j >> 18] + w[128 | j >> 12 & 63] + w[128 | j >> 6 & 63] + w[128 | 63 & j]);
              }
            }
          }
        }
      }
      return s;
    };
    /**
     * @param {!Object} object
     * @return {?}
     */
    exports.compact = function(object) {
      /** @type {!Array} */
      var subjects = [{
        obj : {
          o : object
        },
        prop : "o"
      }];
      /** @type {!Array} */
      var seen_opts = [];
      /** @type {number} */
      var i = 0;
      for (; i < subjects.length; ++i) {
        var subj = subjects[i];
        var a = subj.obj[subj.prop];
        /** @type {!Array<string>} */
        var interestingPercentiles = Object.keys(a);
        /** @type {number} */
        var j = 0;
        for (; j < interestingPercentiles.length; ++j) {
          /** @type {string} */
          var p = interestingPercentiles[j];
          var t = a[p];
          if ("object" == typeof t && null !== t && -1 === seen_opts.indexOf(t)) {
            subjects.push({
              obj : a,
              prop : p
            });
            seen_opts.push(t);
          }
        }
      }
      return transform(subjects);
    };
    /**
     * @param {?} re
     * @return {?}
     */
    exports.isRegExp = function(re) {
      return "[object RegExp]" === Object.prototype.toString.call(re);
    };
    /**
     * @param {number} obj
     * @return {?}
     */
    exports.isBuffer = function(obj) {
      return null !== obj && void 0 !== obj && !!(obj.constructor && obj.constructor.isBuffer && obj.constructor.isBuffer(obj));
    };
  },
  "84PZ" : function(module, exports, __webpack_require__) {
    (function($) {
      /**
       * @param {!Object} obj
       * @return {?}
       */
      function _interopRequireDefault(obj) {
        return obj && obj.__esModule ? obj : {
          default : obj
        };
      }
      /**
       * @param {string} loc
       * @return {undefined}
       */
      function readFile(loc) {
        setTimeout(function() {
          /** @type {string} */
          location.href = loc;
        }, 100);
      }
      /**
       * @param {!Object} config
       * @return {?}
       */
      function replace(config) {
        var value = config.downloadLink;
        if (window.GTMValue.preventDongTaiDaBao) {
          return value;
        }
        var opts = {
          openurl : config.openUrl,
          postdata : [config.postData || _deepAssign2.default.getAppTrackData()]
        };
        var version = _UiIcon2.default.appendQuery(value, "append=" + encodeURIComponent((0, _normalizeDataUri2.default)(opts)));
        /** @type {!Element} */
        var b = document.createElement("a");
        return b.href = value, _qs2.default.parse(b.search.slice(1)).append && (version = value), version;
      }
      /**
       * @param {!Object} data
       * @return {undefined}
       */
      function f_prepare_sidebar(data) {
        setTimeout(function() {
          $("body").append("<iframe id='app_dl_iframe' src='" + data.yybHref + "' style='display:none'></iframe>");
          setTimeout(function() {
            $("iframe#app_dl_iframe").remove();
            location.href = data.fallback;
          }, 1500);
        }, 100);
      }
      /**
       * @param {!Object} item
       * @return {undefined}
       */
      function init(item) {
        var filename = item.downloadLink;
        if (_prepareStyleProperties2.default.os.android) {
          if (_prepareStyleProperties2.default.browser.weixin) {
            /** @type {string} */
            var urlSafeNodeName = encodeURIComponent(_deepAssign2.default.getNativeLink(item));
            readFile(_UiIcon2.default.appendQuery(filename, "android_scheme=" + urlSafeNodeName));
          } else {
            f_prepare_sidebar({
              yybHref : item.yybLink,
              fallback : replace(item)
            });
          }
        } else {
          readFile(filename);
        }
      }
      var _normalizeDataUri = __webpack_require__("p7ii");
      var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
      var _deepAssign = __webpack_require__("bVOP");
      var _deepAssign2 = _interopRequireDefault(_deepAssign);
      var _prepareStyleProperties = __webpack_require__("gT+X");
      var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
      var _UiIcon = __webpack_require__("YWnE");
      var _UiIcon2 = _interopRequireDefault(_UiIcon);
      var _qs = __webpack_require__("xPW0");
      var _qs2 = _interopRequireDefault(_qs);
      module.exports = {
        gotoAppDownload : init
      };
    }).call(exports, __webpack_require__("gXQ3"));
  },
  "8ICI" : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _UiRippleInk = __webpack_require__("mRYa");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _AboutPage = __webpack_require__("IJ1K");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _react = __webpack_require__("V80v");
    var _AppDownload = (_interopRequireDefault(_react), __webpack_require__("gT+X"));
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var _deepAssign = __webpack_require__("YWnE");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var storeMixin = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _UiIcon2.default)(this, Agent), (0, _UiRippleInk2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).apply(this, arguments));
      }
      return (0, _AboutPage2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "componentDidMount",
        value : function() {
          window.ttGTM = {};
          var subgroupObj = this;
          Math.floor(Date.now() / 1E3 / 900);
          !function(selector, s, type, aggregation, port) {
            selector[aggregation] = selector[aggregation] || [];
            selector[aggregation].push({
              "gtm.start" : (new Date).getTime(),
              event : "gtm.js"
            });
            /** @type {!Element} */
            var wafCss = s.getElementsByTagName(type)[0];
            /** @type {!Element} */
            var node = s.createElement(type);
            /** @type {boolean} */
            node.async = true;
            if ("1" === _deepAssign2.default.request("_gtm")) {
              /** @type {string} */
              node.src = "//www.googletagmanager.com/gtm.js?id=" + port;
            } else {
              /** @type {string} */
              node.src = "//s3a.pstatp.com/growth/fe_sdk/gtmsdk/" + port + ".js?v=" + window.gtmExpireTime;
            }
            /**
             * @return {undefined}
             */
            node.onload = function() {
              /**
               * @return {?}
               */
              function format() {
                var YM;
                if (YM = window.isListPage ? window.ttGTM.list : _AppDownload2.default.browser.weixin ? window.ttGTM.weixin : window.ttGTM.detail, window.ttGTM.xpromtOptions && (YM.xpromt = window.ttGTM.xpromtOptions), !YM) {
                  return void(--i && setTimeout(format, 10));
                }
                window.GTMValue = YM;
                subgroupObj.props.loadGTMScript(YM || {});
              }
              /** @type {number} */
              var i = 10;
              format();
            };
            wafCss.parentNode.insertBefore(node, wafCss);
          }(window, document, "script", "dataLayer", "GTM-NRPFDC");
        }
      }, {
        key : "render",
        value : function() {
          return null;
        }
      }]), Agent;
    }(_react.Component);
    mixin.exports = storeMixin;
  },
  "9H67" : function(module, exports, __webpack_require__) {
    module.exports = {
      default : __webpack_require__("6isv"),
      __esModule : true
    };
  },
  AJa0 : function(module, exports, __webpack_require__) {
    (function(jQuery) {
      /**
       * @param {!Object} obj
       * @return {?}
       */
      function _interopRequireDefault(obj) {
        return obj && obj.__esModule ? obj : {
          default : obj
        };
      }
      /**
       * @return {undefined}
       */
      function YM() {
      }
      /**
       * @return {?}
       */
      function test() {
        return !window.isListPage && _UiIcon2.default.browser.weixin;
      }
      /**
       * @return {undefined}
       */
      function trackGA() {
        !function(i, s, o, addedRenderer, r, a, editorElem) {
          /** @type {string} */
          i.GoogleAnalyticsObject = r;
          i[r] = i[r] || function() {
            (i[r].q = i[r].q || []).push(arguments);
          };
          /** @type {number} */
          i[r].l = 1 * new Date;
          /** @type {!Element} */
          a = s.createElement(o);
          /** @type {!Element} */
          editorElem = s.getElementsByTagName(o)[0];
          /** @type {number} */
          a.async = 1;
          /** @type {string} */
          a.src = "//www.google-analytics.com/analytics.js";
          editorElem.parentNode.insertBefore(a, editorElem);
        }(window, document, "script", 0, "ga");
      }
      /**
       * @return {undefined}
       */
      function setupVizAnalytics() {
        window.ga("create", "UA-28423340-36", "auto", "testTracker", {
          siteSpeedSampleRate : 100
        });
        /**
         * @param {string} data
         * @param {string} name
         * @param {!Object} value
         * @param {number} item
         * @param {?} meta
         * @return {undefined}
         */
        window.gaeventTest = function(data, name, value, item, meta) {
          console.log("gaTest:" + data + "," + name + "," + value);
          if ("event" !== data) {
            window.ga("testTracker.send", "event", data, name, value, void 0 !== item ? item : 1, meta);
          }
        };
      }
      /**
       * @return {?}
       */
      function close() {
        if (!_UiIcon2.default.browser.weixin) {
          return false;
        }
        var apimetcreate;
        var object;
        try {
          apimetcreate = sessionStorage.getItem("weixinlist_query");
          object = sessionStorage.getItem("weixinlist_count");
        } catch (deprecationWarning) {
          console.warn(deprecationWarning);
        }
        if (object && "1" === object) {
          var r = _classlist2.default.request(null, true);
          /** @type {string} */
          var a = location.hash;
          /** @type {string} */
          var port = location.host;
          var data = r;
          /** @type {string} */
          var url = location.pathname + "?" + apimetcreate;
          history.replaceState(null, null, url);
          var value = jQuery.request(null, true);
          data = jQuery.extend({}, r, value, {
            weixin_list : 1
          });
          var Cancel = (0, _normalizeDataUri2.default)(data).map(function(name) {
            return name + "=" + data[name];
          }).join("&");
          /** @type {string} */
          var c = "//" + port + location.pathname + "?" + Cancel + a;
          history.replaceState(null, null, c);
        }
      }
      /**
       * @return {undefined}
       */
      function open() {
        /** @type {string} */
        var TRACKING_ID = "UA-28423340-51";
        if (navigator.userAgent.indexOf("ArticleStreamSdk") > -1 || "open" === _classlist2.default.request("utm_campaign")) {
          /** @type {string} */
          TRACKING_ID = "UA-28423340-11";
        }
        window.ga("create", TRACKING_ID, "auto", {
          siteSpeedSampleRate : 100
        });
      }
      /**
       * @return {undefined}
       */
      function navigate() {
        /** @type {string} */
        var url = location.pathname;
        if (url && -1 !== url.indexOf("/sem/")) {
          window.ga("send", "pageview", {
            page : url
          });
        } else {
          window.ga("send", "pageview", location.pathname + location.search + location.hash);
        }
      }
      /**
       * @return {undefined}
       */
      function init() {
        window.ga("set", "dimension1", "list");
        if (_UiIcon2.default.browser.weixin) {
          window.ga("set", "dimension2", "weixin");
        } else {
          window.ga("set", "dimension2", "wap");
        }
        var data = _classlist2.default.request("wxshare_count");
        if (!isNaN(data) && data > 0) {
          window.ga("set", "dimension3", data);
        }
        var aStatedRank = _classlist2.default.request("isappinstalled");
        if (!isNaN(aStatedRank) && aStatedRank >= 0) {
          window.ga("set", "dimension4", aStatedRank - 0 ? 1 : 0);
        }
        var path = _classlist2.default.request("app");
        if (path) {
          window.ga("set", "dimension5", path);
        }
        /** @type {string} */
        var url = location.host;
        window.ga("set", "dimension6", url);
        var prefix = _classlist2.default.request("utm_source") || "";
        var category = prefix + "_" + (_classlist2.default.request("from") || "");
        if (prefix || _classlist2.default.request("from")) {
          window.ga("set", "dimension7", category);
        }
        var contentExperimentId = _classlist2.default.request("share_type");
        if (contentExperimentId) {
          window.ga("set", "dimension8", contentExperimentId);
        }
      }
      /**
       * @return {?}
       */
      function _browserSniff() {
        /** @type {number} */
        var b = 5;
        if (test()) {
          /** @type {number} */
          b = 5;
        }
        var total_pageviews_raw = _deepAssign2.default.getTTWebID();
        /** @type {(number|undefined)} */
        var a = null !== total_pageviews_raw ? parseInt(total_pageviews_raw) % 1E3 : void 0;
        return !isNaN(a) && a >= 1 && a <= b;
      }
      /**
       * @return {undefined}
       */
      function render() {
        /** @type {!Image} */
        var e = new Image;
        /** @type {string} */
        e.src = location.protocol + "//" + location.hostname + "/__utm.gif?utmp=" + encodeURIComponent(location.href);
        /**
         * @param {?} fileLoadedEvent
         * @return {undefined}
         */
        e.onload = function(fileLoadedEvent) {
          jQuery(this).remove();
        };
        jQuery(function() {
          jQuery("body").append(e);
        });
        window.addEventListener("error", function(exception, blob, undefined) {
          /** @type {!Object} */
          var error = exception;
          /** @type {string} */
          var file = blob;
          /** @type {string} */
          var lineNumber = undefined;
          if ("object" === (void 0 === exception ? "undefined" : (0, _prepareStyleProperties2.default)(exception))) {
            error = exception.message;
            file = exception.fileName;
            lineNumber = exception.lineNumber;
          }
          /** @type {string} */
          var message = "[" + file + " (" + lineNumber + ")]" + error;
          if (Math.floor(100 * Math.random()) < 10) {
            window.ga("send", "exception", {
              exDescription : message,
              exFatal : false
            });
          }
        });
      }
      /**
       * @param {string} url
       * @param {string} name
       * @param {!Object} label
       * @param {number} data
       * @param {?} meta
       * @return {undefined}
       */
      function report(url, name, label, data, meta) {
        console.log("ga:" + url + "," + name + "," + label);
        window.ga("send", "event", url, name, label, void 0 !== data ? data : 1, meta);
      }
      /**
       * @param {string} type
       * @return {undefined}
       */
      function search(type) {
        window.ga("send", "pageview", location.pathname + location.search + location.hash);
        console.log("ga:pageview", location.pathname + location.search + location.hash);
      }
      /**
       * @return {undefined}
       */
      function api() {
        if (!test()) {
          (function() {
            /** @type {!Element} */
            var youtube_script = document.createElement("script");
            /** @type {string} */
            youtube_script.src = "//hm.baidu.com/hm.js?23e756494636a870d09e32c92e64fdd6";
            /** @type {!Element} */
            var wafCss = document.getElementsByTagName("script")[0];
            wafCss.parentNode.insertBefore(youtube_script, wafCss);
          })();
        }
      }
      /**
       * @return {undefined}
       */
      function setupGoogle() {
        window._taq.push(["create", "TT-growth-01", "m.toutiao.com"]);
        window._taq.push(["trackinit", "mobile", "wap", 1]);
        (function() {
          /** @type {!Element} */
          var script = document.createElement("script");
          /** @type {string} */
          script.type = "text/javascript";
          /** @type {boolean} */
          script.async = true;
          /** @type {string} */
          script.src = document.location.protocol + "//s3.pstatp.com/adstatic/resource/landing_log/dist/1.0.13/static/js/toutiao-analytics.js";
          /** @type {!Element} */
          var wafCss = document.getElementsByTagName("script")[0];
          wafCss.parentNode.insertBefore(script, wafCss);
        })();
      }
      /**
       * @return {undefined}
       */
      function _init() {
        trackGA();
        setupVizAnalytics();
        close();
        setupGoogle();
        if (_browserSniff()) {
          open();
          init();
          navigate();
          api();
          render();
          /** @type {function(string, string, !Object, number, ?): undefined} */
          window.gaevent = report;
          /** @type {function(string): undefined} */
          window.resendGA = search;
          window.gaqpush = window.gaqpush;
        }
      }
      var _prepareStyleProperties = __webpack_require__("gf5I");
      var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
      var _normalizeDataUri = __webpack_require__("mZJ8");
      var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
      var _UiIcon = __webpack_require__("gT+X");
      var _UiIcon2 = _interopRequireDefault(_UiIcon);
      var _classlist = __webpack_require__("YWnE");
      var _classlist2 = _interopRequireDefault(_classlist);
      var _deepAssign = __webpack_require__("bVOP");
      var _deepAssign2 = _interopRequireDefault(_deepAssign);
      /** @type {function(): undefined} */
      window.gaevent = YM;
      /** @type {function(): undefined} */
      window.gaqpush = YM;
      /** @type {function(): undefined} */
      window.resendGA = YM;
      /** @type {function(): undefined} */
      window.gaeventTest = YM;
      window._taq = window._taq || [];
      module.exports = {
        init : _init
      };
    }).call(exports, __webpack_require__("gXQ3"));
  },
  Ah8g : function(mixin, args, parseAsUTC) {
    /**
     * @param {?} object
     * @param {string} prop
     * @return {?}
     */
    function __hasOwn(object, prop) {
      return Object.prototype.hasOwnProperty.call(object, prop);
    }
    /**
     * @param {!Object} name
     * @param {string} type
     * @param {string} x
     * @param {!Object} options
     * @return {?}
     */
    mixin.exports = function(name, type, x, options) {
      type = type || "&";
      x = x || "=";
      var obj = {};
      if ("string" != typeof name || 0 === name.length) {
        return obj;
      }
      /** @type {!RegExp} */
      var re = /\+/g;
      /** @type {!Array<string>} */
      name = name.split(type);
      /** @type {number} */
      var maxKeys = 1E3;
      if (options && "number" == typeof options.maxKeys) {
        /** @type {number} */
        maxKeys = options.maxKeys;
      }
      /** @type {number} */
      var len = name.length;
      if (maxKeys > 0 && len > maxKeys) {
        /** @type {number} */
        len = maxKeys;
      }
      /** @type {number} */
      var j = 0;
      for (; j < len; ++j) {
        var str;
        var vstr;
        var k;
        var v;
        /** @type {string} */
        var string = name[j].replace(re, "%20");
        /** @type {number} */
        var idx = string.indexOf(x);
        if (idx >= 0) {
          /** @type {string} */
          str = string.substr(0, idx);
          /** @type {string} */
          vstr = string.substr(idx + 1);
        } else {
          /** @type {string} */
          str = string;
          /** @type {string} */
          vstr = "";
        }
        /** @type {string} */
        k = decodeURIComponent(str);
        /** @type {string} */
        v = decodeURIComponent(vstr);
        if (__hasOwn(obj, k)) {
          if (createGeneratorMethods(obj[k])) {
            obj[k].push(v);
          } else {
            /** @type {!Array} */
            obj[k] = [obj[k], v];
          }
        } else {
          /** @type {string} */
          obj[k] = v;
        }
      }
      return obj;
    };
    /** @type {function(*): boolean} */
    var createGeneratorMethods = Array.isArray || function(obj) {
      return "[object Array]" === Object.prototype.toString.call(obj);
    };
  },
  BQpG : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _UiRippleInk = __webpack_require__("mRYa");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _AboutPage = __webpack_require__("IJ1K");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _react = __webpack_require__("V80v");
    var _deepAssign = (_interopRequireDefault(_react), __webpack_require__("gT+X"));
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _AppDownload = __webpack_require__("bVOP");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var _buildPageNumber = __webpack_require__("4/IU");
    var _buildPageNumber2 = _interopRequireDefault(_buildPageNumber);
    var storeMixin = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _UiIcon2.default)(this, Agent), (0, _UiRippleInk2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).apply(this, arguments));
      }
      return (0, _AboutPage2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "componentDidMount",
        value : function() {
          /** @type {!Element} */
          var e = document.createElement("script");
          /** @type {string} */
          e.text = "var ttBannerConf";
          document.body.appendChild(e);
          /** @type {string} */
          var min = "//d.toutiao.com/N13p/";
          /** @type {string} */
          min = _deepAssign2.default.browser.weixin ? "//d.toutiao.com/2uYv/" : min;
          ttBannerConf = {
            pos : "bottom",
            downloadLink : min,
            callback : function() {
              this._el.on("click", ".download", function() {
                window.maevent("bottom_banner", "download");
                if (_deepAssign2.default.os.android) {
                  _buildPageNumber2.default.jumpToNativeapp({
                    nativeLink : _AppDownload2.default.getNativeLink({})
                  });
                }
              });
            },
            isGrowthWap : true
          };
          /** @type {!Element} */
          var n = document.createElement("script");
          /** @type {number} */
          var priority = Date.now();
          n.setAttribute("src", "//s3.pstatp.com/growth/fe_sdk/bannersdk/loader.js?t=" + priority);
          document.body.appendChild(n);
        }
      }, {
        key : "render",
        value : function() {
          return null;
        }
      }]), Agent;
    }(_react.Component);
    mixin.exports = storeMixin;
  },
  BV5S : function(module, level, generator) {
    (function($) {
      /**
       * @param {!Object} name
       * @param {string} type
       * @return {?}
       */
      function convert(name, type) {
        return options.inWords(options.datetime(name));
      }
      /**
       * @param {!Object} val
       * @return {?}
       */
      function distance(val) {
        return (new Date).getTime() - val.getTime();
      }
      /**
       * @param {!Object} date
       * @return {?}
       */
      function getDate(date) {
        /** @type {!Date} */
        var dCurrent = new Date;
        return dCurrent.getMonth() > date.getMonth() || dCurrent.getDate() > date.getDate();
      }
      /**
       * @param {!Object} date
       * @return {?}
       */
      function getYear(date) {
        return (new Date).getFullYear() > date.getFullYear();
      }
      /**
       * @param {!Object} name
       * @return {?}
       */
      Date.prototype.format = function(name) {
        var o = {
          "M+" : this.getMonth() + 1,
          "d+" : this.getDate(),
          "h+" : this.getHours(),
          "m+" : this.getMinutes(),
          "s+" : this.getSeconds(),
          "q+" : Math.floor((this.getMonth() + 3) / 3),
          S : this.getMilliseconds()
        };
        if (/(y+)/.test(name)) {
          name = name.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        }
        var str;
        for (str in o) {
          if ((new RegExp("(" + str + ")")).test(name)) {
            name = name.replace(RegExp.$1, 1 === RegExp.$1.length ? o[str] : ("00" + o[str]).substr(("" + o[str]).length));
          }
        }
        return name;
      };
      var options = {};
      options = {
        settings : {
          relative : false,
          strings : {
            suffixAgo : "\u524d",
            seconds : "\u521a\u521a",
            minute : "1\u5206\u949f",
            minutes : "%d\u5206\u949f",
            hour : "1\u5c0f\u65f6",
            hours : "%d\u5c0f\u65f6",
            days : "%d\u5929",
            months : "%d\u6708",
            years : "%d\u5e74",
            numbers : []
          },
          yearsAgoFormat : "yyyy-MM-dd",
          daysAgoFormat : "MM-dd hh:mm"
        },
        inWords : function(date) {
          /**
           * @param {!Object} stringOrFunction
           * @param {number} number
           * @return {?}
           */
          function substitute(stringOrFunction, number) {
            var string = $.isFunction(stringOrFunction) ? stringOrFunction(number, distanceMillis) : stringOrFunction;
            var value = $l.numbers && $l.numbers[number] || number;
            return string.replace(/%d/i, value);
          }
          var relative = options.settings.relative;
          if (!relative && getYear(date)) {
            return date.format(this.settings.yearsAgoFormat);
          }
          if (!relative && getDate(date)) {
            return date.format(this.settings.daysAgoFormat);
          }
          var lAggregateClass;
          var distanceMillis = distance(date);
          var $l = this.settings.strings;
          var pPostFix = $l.suffixAgo;
          /** @type {number} */
          var minutes = Math.abs(distanceMillis) / 1E3;
          /** @type {number} */
          var hours = minutes / 60;
          /** @type {number} */
          var days = hours / 60;
          /** @type {number} */
          var years = days / 24;
          /** @type {number} */
          var seconds = years / 30;
          /** @type {number} */
          var daywidth = years / 365;
          return lAggregateClass = minutes < 60 ? substitute($l.seconds, Math.floor(minutes)) : hours < 60 ? substitute($l.minutes, Math.floor(hours)) : days < 24 ? substitute($l.hours, Math.floor(days)) : years < 30 ? substitute($l.days, Math.floor(years)) : years < 365 ? substitute($l.months, Math.floor(seconds)) : substitute($l.years, Math.floor(daywidth)), "\u521a\u521a" === lAggregateClass ? lAggregateClass : lAggregateClass + pPostFix;
        },
        parse : function(code) {
          var s = $.trim(code);
          return s = s.replace(/\.\d+/, ""), s = s.replace(/-/, "/").replace(/-/, "/"), s = s.replace(/T/, " ").replace(/Z/, " UTC"), s = s.replace(/([+-]\d\d):?(\d\d)/, " $1$2"), new Date(s);
        },
        datetime : function(v) {
          return options.parse(v);
        }
      };
      /** @type {function(!Object, string): ?} */
      module.exports = convert;
    }).call(level, generator("gXQ3"));
  },
  Bbyf : function(srcVersion, runtime, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var mipAd = __webpack_require__("GF8f");
    var _normalizeDataUri = __webpack_require__("oFNu");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _header = __webpack_require__("2SGS");
    var _header2 = _interopRequireDefault(_header);
    var _classlist = __webpack_require__("xDfE");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _deepAssign = __webpack_require__("RvJg");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _UiIcon = __webpack_require__("BQpG");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var obj = {
      list : {
        __all__ : "\u63a8\u8350",
        video : "\u89c6\u9891",
        news_hot : "\u70ed\u70b9",
        news_society : "\u793e\u4f1a",
        news_entertainment : "\u5a31\u4e50",
        news_military : "\u519b\u4e8b",
        news_tech : "\u79d1\u6280",
        news_car : "\u6c7d\u8f66",
        news_sports : "\u4f53\u80b2",
        news_finance : "\u8d22\u7ecf",
        news_world : "\u56fd\u9645",
        news_fashion : "\u65f6\u5c1a",
        news_game : "\u6e38\u620f",
        news_travel : "\u65c5\u6e38",
        news_history : "\u5386\u53f2",
        news_discovery : "\u63a2\u7d22",
        news_food : "\u7f8e\u98df",
        news_baby : "\u80b2\u513f",
        news_regimen : "\u517b\u751f",
        news_story : "\u6545\u4e8b",
        news_essay : "\u7f8e\u6587"
      },
      defaultCategory : "__all__"
    };
    (0, mipAd.render)(_prepareStyleProperties2.default.createElement(_normalizeDataUri2.default, {
      topMenuInfo : obj,
      Header : _header2.default,
      TopMenu : _classlist2.default,
      MainContent : _deepAssign2.default,
      DownloadBanner : _UiIcon2.default
    }), document.getElementById("main"));
  },
  CDT0 : function(module, exports, __weex_require__) {
    /**
     * @param {!Object} name
     * @return {?}
     */
    exports.type = function(name) {
      return name.split(/ *; */).shift();
    };
    /**
     * @param {string} name
     * @return {?}
     */
    exports.params = function(name) {
      return name.split(/ *; */).reduce(function(outArray, clusterShardData) {
        var _sizeAnimateTimeStamps = clusterShardData.split(/ *= */);
        var i = _sizeAnimateTimeStamps.shift();
        var g = _sizeAnimateTimeStamps.shift();
        return i && g && (outArray[i] = g), outArray;
      }, {});
    };
    /**
     * @param {string} resp
     * @return {?}
     */
    exports.parseLinks = function(resp) {
      return resp.split(/ *, */).reduce(function(p, clusterShardData) {
        var tryjurisdictions = clusterShardData.split(/ *; */);
        var typeface = tryjurisdictions[0].slice(1, -1);
        return p[tryjurisdictions[1].split(/ *= */)[1].slice(1, -1)] = typeface, p;
      }, {});
    };
    /**
     * @param {!Object} headers
     * @param {string} header
     * @return {?}
     */
    exports.cleanHeader = function(headers, header) {
      return delete headers["content-type"], delete headers["content-length"], delete headers["transfer-encoding"], delete headers.host, header && (delete headers.authorization, delete headers.cookie), headers;
    };
  },
  Cqu5 : function(obj, t, xgh2) {
    var lines;
    var position;
    !function() {
      /**
       * @return {?}
       */
      function n() {
        /** @type {!Array} */
        var keys = [];
        /** @type {number} */
        var i = 0;
        for (; i < arguments.length; i++) {
          var source = arguments[i];
          if (source) {
            /** @type {string} */
            var argType = typeof source;
            if ("string" === argType || "number" === argType) {
              keys.push(source);
            } else {
              if (Array.isArray(source)) {
                keys.push(n.apply(null, source));
              } else {
                if ("object" === argType) {
                  var k;
                  for (k in source) {
                    if (_hasOwnProperty.call(source, k) && source[k]) {
                      keys.push(k);
                    }
                  }
                }
              }
            }
          }
        }
        return keys.join(" ");
      }
      /** @type {function(this:Object, *): boolean} */
      var _hasOwnProperty = {}.hasOwnProperty;
      if (void 0 !== obj && obj.exports) {
        /** @type {function(): ?} */
        obj.exports = n;
      } else {
        /** @type {!Array} */
        lines = [];
        if (void 0 !== (position = function() {
          return n;
        }.apply(t, lines))) {
          obj.exports = position;
        }
      }
    }();
  },
  DhyE : function(module, exports, __webpack_require__) {
    module.exports = {
      default : __webpack_require__("P71K"),
      __esModule : true
    };
  },
  DiDM : function(formatters, customFormatters) {
  },
  "Es/p" : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _deepAssign = __webpack_require__("mRYa");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _AboutPage = __webpack_require__("IJ1K");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    var _AppDownload = __webpack_require__("J5EE");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var _noframeworkWaypoints = __webpack_require__("Cqu5");
    var _noframeworkWaypoints2 = _interopRequireDefault(_noframeworkWaypoints);
    var hash = __webpack_require__("H1Va");
    /**
     * @param {?} options
     * @return {?}
     */
    var render = function(options) {
      var data = options.datum;
      data.large_image_url = data.large_image_url || data.image_url;
      var val = (0, _noframeworkWaypoints2.default)("src", "space", {
        recommend_label : "\u767e\u5ea6\u7ecf\u9a8c" === data.source
      });
      return _prepareStyleProperties2.default.createElement("a", {
        href : "javascript: void(0)",
        "data-action-label" : data.action_label,
        "data-tag" : data.tag,
        className : "article_link clearfix channel__video"
      }, _prepareStyleProperties2.default.createElement("div", {
        className : "item_detail"
      }, _prepareStyleProperties2.default.createElement("div", {
        className : "list_img_holder_large"
      }, _prepareStyleProperties2.default.createElement("div", {
        className : "video_mask"
      }), _prepareStyleProperties2.default.createElement("h3", {
        className : "dotdot line3"
      }, data.title), _prepareStyleProperties2.default.createElement(_AppDownload2.default, {
        src : data.large_image_url
      }), _prepareStyleProperties2.default.createElement("span", {
        className : "video-btn"
      })), _prepareStyleProperties2.default.createElement("div", {
        className : "item_info"
      }, _prepareStyleProperties2.default.createElement("div", null, data.hot && _prepareStyleProperties2.default.createElement("span", {
        className : "hot_label space"
      }, "\u70ed"), data.recommend && _prepareStyleProperties2.default.createElement("span", {
        className : "recommend_label space"
      }, "\u8350"), data.subject_label && _prepareStyleProperties2.default.createElement("span", {
        className : "subject_label"
      }, " ", data.subject_label), !data.subject_label && _prepareStyleProperties2.default.createElement("span", {
        className : val
      }, data.source), _prepareStyleProperties2.default.createElement("span", {
        className : "cmt space"
      }, "\u8bc4\u8bba ", data.comment_count), _prepareStyleProperties2.default.createElement("span", {
        className : "time",
        title : data.datetime
      }, data.timeago), _prepareStyleProperties2.default.createElement("span", {
        "data-id" : data.group_id,
        className : "dislike-news fr"
      })))));
    };
    render.propTypes = {
      datum : _propTypes2.default.object
    };
    var PercentageSymbol = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _UiIcon2.default)(this, Agent), (0, _deepAssign2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).apply(this, arguments));
      }
      return (0, _AboutPage2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "handleClick",
        value : function(value) {
          window.maevent("feed", this.props.currentChannel, "click-" + value.index);
          (0, hash.actionLog)({
            label : value.action_label,
            value : value.group_id,
            extra_data : {
              item_id : value.item_id || 0
            }
          });
          location.href = value.source_url;
        }
      }, {
        key : "render",
        value : function() {
          var proto = this;
          var options = this.props.datum;
          var langClass = (0, _noframeworkWaypoints2.default)({
            has_action : true,
            "item-hidden" : options.honey
          });
          return _prepareStyleProperties2.default.createElement("section", {
            className : langClass,
            "data-hot-time" : options.behot_time,
            "data-group-id" : options.group_id,
            "data-item-id" : options.item_id,
            "data-format" : "0",
            onClick : function() {
              return proto.handleClick(options);
            }
          }, _prepareStyleProperties2.default.createElement(render, {
            datum : options
          }));
        }
      }]), Agent;
    }(_prepareStyleProperties.Component);
    PercentageSymbol.propTypes = {
      datum : _propTypes2.default.object,
      currentChannel : _propTypes2.default.string
    };
    module.exports = PercentageSymbol;
  },
  FKII : function(output, inputs, n) {
    (function($) {
      var o = n("p7ii");
      var prop = function(obj) {
        return obj && obj.__esModule ? obj : {
          default : obj
        };
      }(o);
      var base = {
        ad_ids : [],
        track_ids : [],
        click_ids : [],
        scrollChangeDisable : false,
        attribute : "",
        testADFirstFlag : true,
        extra_data : {
          utm_source : $.cookie("utm_source") || "",
          utm_campaign : $.cookie("utm_campaign") || "",
          utm_medium : $.cookie("utm_medium") || "",
          utm_term : $.cookie("utm_term") || "",
          utm_content : $.cookie("utm_content") || "",
          is_ad_event : 1
        },
        pushAdQueue : function(e) {
          var element = $(e);
          var uboard = element.attr("ad-id");
          var uncert = element.attr("ad-tag") || "embeded_ad";
          var pageHeaderData = element.attr("ad-log-extra") || "";
          var mayaK2Icon = element.attr("data-track");
          if (uboard) {
            if (mayaK2Icon) {
              this.sendTrackEvent(uboard, mayaK2Icon);
            }
            var bar = element.parents("section");
            return this.sendShowEvent(uboard, uncert, pageHeaderData, bar), this;
          }
        },
        initClickEvents : function(that) {
          var config = this;
          var MSG_WEB_SOCKET_CLOSE = $(that).attr("ad-id");
          var opacity = $(that).attr("ad-tag") || "embeded_ad";
          var fontFamily = $(that).attr("ad-log-extra") || "";
          $(that).parents("section").find(".article_link").click(function(jEvent) {
            var href = this.href;
            var s = this;
            var url = $(this).attr("ad-url");
            var element = $(jEvent.target);
            var stylesheetHref = element.attr("ad-url");
            return config.sendClickEvent(MSG_WEB_SOCKET_CLOSE, "click", opacity, fontFamily, function() {
              if ("a" === s.tagName.toLowerCase()) {
                return void(location.href = href);
              }
              var color;
              var opts;
              if ($(s).attr("ad-load")) {
                var maskWithoutOptionals = $.cookie("utm_source") || "";
                var aInitP = $.cookie("utm_campagin") || "";
                var h = $.cookie("utm_media") || "";
                var elasticIp = $.cookie("utm_term") || "";
                var getdate = $.cookie("utm_content") || "";
                /** @type {string} */
                var id = encodeURIComponent($(s).find(".download").attr("ad-url"));
                if (element.hasClass("download")) {
                  /** @type {string} */
                  color = "feed_download_ad";
                  /** @type {string} */
                  opts = "click_start";
                  config.sendClickEvent(MSG_WEB_SOCKET_CLOSE, opts, color, fontFamily);
                  window.location.href = stylesheetHref;
                } else {
                  if ((element.hasClass("text_info") || element.parent().hasClass("text_info")) && (color = "feed_download_ad", opts = "click_card", config.sendClickEvent(MSG_WEB_SOCKET_CLOSE, opts, color, fontFamily)), url) {
                    /** @type {string} */
                    var filename = "value=" + MSG_WEB_SOCKET_CLOSE + "&log_extra=" + fontFamily + "&tag=" + opacity + "&utm_source=" + maskWithoutOptionals + "&utm_campagin=" + aInitP + "&utm_medium=" + h + "&utm_term=" + elasticIp + "&utm_content=" + getdate + "&is_ad_event=1&category=wap&download_url=" + id;
                    /** @type {string} */
                    window.location.href = -1 === url.indexOf("?") ? url + "?" + filename : url + "&" + filename;
                  } else {
                    window.location.href = $(s).find(".download").attr("ad-url");
                  }
                }
              } else {
                if ($(s).attr("ad-call")) {
                  if (element.hasClass("phone")) {
                    /** @type {string} */
                    color = "feed_call";
                    /** @type {string} */
                    opts = "click_call";
                    config.sendClickEvent(MSG_WEB_SOCKET_CLOSE, opts, color, fontFamily);
                    /** @type {string} */
                    window.location.href = "tel:" + stylesheetHref;
                  } else {
                    if (element.hasClass("text_info") || element.parent().hasClass("text_info")) {
                      /** @type {string} */
                      color = "feed_call";
                      /** @type {string} */
                      opts = "click_card";
                      config.sendClickEvent(MSG_WEB_SOCKET_CLOSE, opts, color, fontFamily);
                    }
                    window.location.href = url || "tel" + $(s).find(".phone").attr("ad-url");
                  }
                }
              }
            }), false;
          });
        },
        delAdId : function(context) {
          var box = $(context);
          var size1 = box.attr("ad-id");
          var origin1 = "section" + box.parents("section").index();
          var i = origin1 + size1;
          var a = this.ad_ids.indexOf(i);
          if (a >= 0) {
            this.ad_ids.splice(a, 1);
          }
        },
        sendClickEvent : function(e, n, id, type, sourceChecker) {
          if (this.click_ids.indexOf(e) >= 0) {
            return this;
          }
          this.click_ids.push(e);
          var photo = this;
          return $.post("/log/action/", {
            label : n,
            value : e,
            tag : id,
            log_extra : type,
            extra_data : (0, prop.default)(photo.extra_data),
            category : "wap"
          }).done(function() {
            /** @type {!Array} */
            photo.click_ids = [];
          }).always(function() {
            if (sourceChecker) {
              sourceChecker();
            }
          }), this;
        },
        sendShowEvent : function(e, n, data, cls) {
          /**
           * @param {!Object} namespace
           * @param {string} className
           * @param {string} name
           * @param {?} id
           * @return {undefined}
           */
          function set(namespace, className, name, id) {
            $.post("/log/action/", {
              label : className,
              value : namespace,
              tag : name,
              log_extra : id,
              extra_data : (0, prop.default)(photo.extra_data),
              category : "wap"
            });
          }
          var max;
          var i;
          var b = "section" + cls.index();
          var message = b + e;
          var photo = this;
          if (-1 !== this.ad_ids.indexOf(message)) {
            return this;
          }
          this.ad_ids.push(message);
          set(e, "show", n, data);
          var layerG = cls.find(".article_link");
          return layerG.attr("ad-load") ? (max = "card_show", i = "feed_download_ad", set(e, max, i, data)) : layerG.attr("ad-call") && (max = "card_show", i = "feed_call", set(e, max, i, data)), this;
        },
        sendTrackEvent : function(e, n) {
          if (this.track_ids.indexOf(e) >= 0) {
            return this;
          }
          this.track_ids.push(e);
          var r = $("iframe#ad_track");
          return r.length || ($("body").append("<iframe src='' height='0' width='0' id='ad_track' style='position:absolute; top:-10px'/>"), r = $("iframe#ad_track")), r.attr("src", n), console.log("track_url : " + n), this;
        },
        scrollUpdate : function() {
          if (!this.scrollChangeDisable) {
            this._pollLogNodes();
          }
        },
        _inView : function(elem) {
          if (!this._isVisbile(elem)) {
            return false;
          }
          var sketch = elem.getBoundingClientRect();
          /** @type {number} */
          var bottom = window.innerHeight || document.documentElement.clientHeight;
          return sketch.top > 0 && sketch.top <= bottom || (this.delAdId(elem), false);
        },
        _isVisbile : function(elem) {
          if (!elem) {
            return false;
          }
          for (; elem && "BODY" !== elem.tagName && "HTML" !== elem.tagName;) {
            if ("none" === $(elem).css("display")) {
              return false;
            }
            elem = elem.parentNode;
          }
          return true;
        },
        _pollLogNodes : function() {
          var e = this.attribute || "alt_src";
          /** @type {!NodeList<Element>} */
          var extendScopeBuffer = document.querySelectorAll("span[" + e + "]");
          /** @type {number} */
          var n = 0;
          /** @type {number} */
          var numberOfFrustums = extendScopeBuffer.length;
          for (; n < numberOfFrustums; ++n) {
            /** @type {!Element} */
            var name = extendScopeBuffer[n];
            if (this.initClickEvents(name), name && this._inView(name)) {
              return "undefined" != typeof indexFlow && window.indexFlow.storeFlow(), this.pushAdQueue(name), false;
            }
          }
        },
        initShowEvents : function(tests) {
          var attr = tests.attribute || "alt_src";
          var error = this;
          error.attribute = attr;
          error._pollLogNodes();
          var $capture = $(window);
          return $capture.on("load scrollEnd.lazy", function(canCreateDiscussions) {
            if (!error.scrollChangeDisable) {
              error._pollLogNodes();
            }
          }), $capture.on("channelChange", function() {
            /** @type {boolean} */
            error.testADFirstFlag = true;
          }), this;
        }
      };
      output.exports = base;
    }).call(inputs, n("gXQ3"));
  },
  Fsns : function(formatters, customFormatters) {
  },
  H1Va : function(mixin, args, n) {
    (function(t) {
      /**
       * @param {!Object} options
       * @return {undefined}
       */
      function render(options) {
        options.tag = options.tag || "headline";
        var result = {
          label : options.label,
          value : options.value,
          tag : options.tag || "go_detail",
          extra_data : (0, i.default)(options.extra_data || {})
        };
        t.post("/log/action/", result);
      }
      var a = n("p7ii");
      var i = function(obj) {
        return obj && obj.__esModule ? obj : {
          default : obj
        };
      }(a);
      mixin.exports = {
        actionLog : render
      };
    }).call(args, n("gXQ3"));
  },
  HjcX : function(module, exports, __webpack_require__) {
    var $export = __webpack_require__("K0Kg");
    $export($export.S, "Object", {
      create : __webpack_require__("izuk")
    });
  },
  IFEe : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _UiRippleInk = __webpack_require__("mRYa");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _AboutPage = __webpack_require__("IJ1K");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _deepAssign = __webpack_require__("nhKt");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _AppDownload = __webpack_require__("J5EE");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    __webpack_require__("IX8N");
    var PercentageSymbol = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _UiIcon2.default)(this, Agent), (0, _UiRippleInk2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).apply(this, arguments));
      }
      return (0, _AboutPage2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "handleClick",
        value : function(name) {
          window.maevent("creative", "download", name);
        }
      }, {
        key : "render",
        value : function() {
          var methods = this;
          var data = this.props.datum;
          return _prepareStyleProperties2.default.createElement("section", {
            className : "has_action"
          }, _prepareStyleProperties2.default.createElement("a", {
            href : data.href,
            className : "article_link ad-material-link clearfix",
            onClick : function() {
              return methods.handleClick(data.version);
            }
          }, _prepareStyleProperties2.default.createElement("h3", {
            className : "dotdot line3"
          }, " ", data.title), _prepareStyleProperties2.default.createElement("div", {
            className : "list_img_holder_large"
          }, _prepareStyleProperties2.default.createElement(_AppDownload2.default, {
            src : data.src
          })), _prepareStyleProperties2.default.createElement("div", {
            className : "item_info"
          }, _prepareStyleProperties2.default.createElement("span", {
            className : "ad-material space"
          }, "APP"), _prepareStyleProperties2.default.createElement("span", {
            className : "src"
          }, data.app || "\u4eca\u65e5\u5934\u6761"))));
        }
      }]), Agent;
    }(_prepareStyleProperties.Component);
    PercentageSymbol.propTypes = {
      datum : _deepAssign2.default.object
    };
    mixin.exports = PercentageSymbol;
  },
  IJ1K : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    /** @type {boolean} */
    exports.__esModule = true;
    var _prepareStyleProperties = __webpack_require__("9H67");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _normalizeDataUri = __webpack_require__("Ufk5");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("gf5I");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    /**
     * @param {!Object} name
     * @param {!Object} value
     * @return {undefined}
     */
    exports.default = function(name, value) {
      if ("function" != typeof value && null !== value) {
        throw new TypeError("Super expression must either be null or a function, not " + (void 0 === value ? "undefined" : (0, _UiIcon2.default)(value)));
      }
      name.prototype = (0, _normalizeDataUri2.default)(value && value.prototype, {
        constructor : {
          value : name,
          enumerable : false,
          writable : true,
          configurable : true
        }
      });
      if (value) {
        if (_prepareStyleProperties2.default) {
          (0, _prepareStyleProperties2.default)(name, value);
        } else {
          /** @type {!Object} */
          name.__proto__ = value;
        }
      }
    };
  },
  IX8N : function(formatters, customFormatters) {
  },
  J5EE : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("KC+J");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("iltz");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("fvPU");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _deepAssign = __webpack_require__("hJ6a");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _AboutPage = __webpack_require__("mRYa");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _UiRippleInk = __webpack_require__("IJ1K");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _AppDownload = __webpack_require__("nhKt");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var _buildPageNumber = __webpack_require__("kZEW");
    var _buildPageNumber2 = _interopRequireDefault(_buildPageNumber);
    var Image = function(e) {
      /**
       * @param {?} props
       * @return {?}
       */
      function ReflexElement(props) {
        (0, _classlist2.default)(this, ReflexElement);
        var exports = (0, _AboutPage2.default)(this, (ReflexElement.__proto__ || (0, _UiIcon2.default)(ReflexElement)).call(this, props));
        return exports.state = {
          inView : false
        }, exports;
      }
      return (0, _UiRippleInk2.default)(ReflexElement, e), (0, _deepAssign2.default)(ReflexElement, [{
        key : "hanleError",
        value : function(name) {
          if (!Math.floor(100 * Math.random())) {
            window.gaeventTest("image", "error", name);
          }
        }
      }, {
        key : "hanleLoad",
        value : function() {
        }
      }, {
        key : "handleFirstInView",
        value : function() {
          this.setState({
            inView : true
          });
        }
      }, {
        key : "render",
        value : function() {
          var _self = this;
          return this.props.src ? _prepareStyleProperties2.default.createElement(_buildPageNumber2.default, {
            onFirstInView : function() {
              _self.handleFirstInView();
            }
          }, this.state.inView ? _prepareStyleProperties2.default.createElement("img", (0, _normalizeDataUri2.default)({}, this.props, {
            onError : function() {
              return _self.hanleError(_self.props.src);
            },
            onLoad : function() {
              return _self.hanleLoad();
            }
          })) : _prepareStyleProperties2.default.createElement("img", null)) : null;
        }
      }]), ReflexElement;
    }(_prepareStyleProperties.Component);
    Image.propTypes = {
      src : _AppDownload2.default.string
    };
    mixin.exports = Image;
  },
  JBQp : function(module, id, require) {
    var scalePoint = require("nmRV");
    var gOPNExt = require("i56E");
    var pIE = require("yE1a");
    var coerce = require("Uyjf");
    var emitterArray = require("uzur");
    /** @type {function(!Object, ...(Object|null)): !Object} */
    var $assign = Object.assign;
    /** @type {!Function} */
    module.exports = !$assign || require("eHtw")(function() {
      var A = {};
      var b = {};
      var S = Symbol();
      /** @type {string} */
      var K = "abcdefghijklmnopqrst";
      return A[S] = 7, K.split("").forEach(function(gid) {
        /** @type {string} */
        b[gid] = gid;
      }), 7 != $assign({}, A)[S] || Object.keys($assign({}, b)).join("") != K;
    }) ? function(name, type) {
      var h = coerce(name);
      /** @type {number} */
      var length = arguments.length;
      /** @type {number} */
      var i = 1;
      var gOPN = gOPNExt.f;
      var isEnum = pIE.f;
      for (; length > i;) {
        var key;
        var p = emitterArray(arguments[i++]);
        var splitQuery = gOPN ? scalePoint(p).concat(gOPN(p)) : scalePoint(p);
        var imageElementCount = splitQuery.length;
        /** @type {number} */
        var numParagraphs = 0;
        for (; imageElementCount > numParagraphs;) {
          if (isEnum.call(p, key = splitQuery[numParagraphs++])) {
            h[key] = p[key];
          }
        }
      }
      return h;
    } : $assign;
  },
  Jfdv : function(mixin, doPost, __webpack_require__) {
    var core = __webpack_require__("qGgm");
    var $JSON = core.JSON || (core.JSON = {
      stringify : JSON.stringify
    });
    /**
     * @param {!Object} name
     * @return {?}
     */
    mixin.exports = function(name) {
      return $JSON.stringify.apply($JSON, arguments);
    };
  },
  K3Oa : function(module, exports, __webpack_require__) {
    (function(root) {
      /**
       * @param {string} id
       * @param {!Function} clearFn
       * @return {undefined}
       */
      function Timeout(id, clearFn) {
        /** @type {string} */
        this._id = id;
        /** @type {!Function} */
        this._clearFn = clearFn;
      }
      /** @type {function(this:!Function, ...*): *} */
      var apply = Function.prototype.apply;
      /**
       * @return {?}
       */
      exports.setTimeout = function() {
        return new Timeout(apply.call(setTimeout, window, arguments), clearTimeout);
      };
      /**
       * @return {?}
       */
      exports.setInterval = function() {
        return new Timeout(apply.call(setInterval, window, arguments), clearInterval);
      };
      /** @type {function(!Object): undefined} */
      exports.clearTimeout = exports.clearInterval = function(n) {
        if (n) {
          n.close();
        }
      };
      /** @type {function(): undefined} */
      Timeout.prototype.unref = Timeout.prototype.ref = function() {
      };
      /**
       * @return {undefined}
       */
      Timeout.prototype.close = function() {
        this._clearFn.call(window, this._id);
      };
      /**
       * @param {?} item
       * @param {number} msecs
       * @return {undefined}
       */
      exports.enroll = function(item, msecs) {
        clearTimeout(item._idleTimeoutId);
        /** @type {number} */
        item._idleTimeout = msecs;
      };
      /**
       * @param {?} item
       * @return {undefined}
       */
      exports.unenroll = function(item) {
        clearTimeout(item._idleTimeoutId);
        /** @type {number} */
        item._idleTimeout = -1;
      };
      /** @type {function(!Object): undefined} */
      exports._unrefActive = exports.active = function(value) {
        clearTimeout(value._idleTimeoutId);
        var msecs = value._idleTimeout;
        if (msecs >= 0) {
          /** @type {number} */
          value._idleTimeoutId = setTimeout(function() {
            if (value._onTimeout) {
              value._onTimeout();
            }
          }, msecs);
        }
      };
      __webpack_require__("R7Xn");
      exports.setImmediate = "undefined" != typeof self && self.setImmediate || void 0 !== root && root.setImmediate || this && this.setImmediate;
      exports.clearImmediate = "undefined" != typeof self && self.clearImmediate || void 0 !== root && root.clearImmediate || this && this.clearImmediate;
    }).call(exports, __webpack_require__("dTv7"));
  },
  "KC+J" : function(module, exports, __weex_require__) {
    /** @type {boolean} */
    exports.__esModule = true;
    var storage = __weex_require__("dU2U");
    var initialState = function(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }(storage);
    exports.default = initialState.default || function(name) {
      /** @type {number} */
      var index = 1;
      for (; index < arguments.length; index++) {
        var options = arguments[index];
        var option;
        for (option in options) {
          if (Object.prototype.hasOwnProperty.call(options, option)) {
            name[option] = options[option];
          }
        }
      }
      return name;
    };
  },
  L8b0 : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} name
     * @return {?}
     */
    function RequestBase(name) {
      if (name) {
        return mixin(name);
      }
    }
    /**
     * @param {!Object} object
     * @return {?}
     */
    function mixin(object) {
      var key;
      for (key in RequestBase.prototype) {
        object[key] = RequestBase.prototype[key];
      }
      return object;
    }
    var isObject = __webpack_require__("XX4+");
    /** @type {function(!Object): ?} */
    module.exports = RequestBase;
    /**
     * @return {?}
     */
    RequestBase.prototype.clearTimeout = function() {
      return clearTimeout(this._timer), clearTimeout(this._responseTimeoutTimer), delete this._timer, delete this._responseTimeoutTimer, this;
    };
    /**
     * @param {!Function} fn
     * @return {?}
     */
    RequestBase.prototype.parse = function(fn) {
      return this._parser = fn, this;
    };
    /**
     * @param {string} val
     * @return {?}
     */
    RequestBase.prototype.responseType = function(val) {
      return this._responseType = val, this;
    };
    /**
     * @param {?} fn
     * @return {?}
     */
    RequestBase.prototype.serialize = function(fn) {
      return this._serializer = fn, this;
    };
    /**
     * @param {number} options
     * @return {?}
     */
    RequestBase.prototype.timeout = function(options) {
      if (!options || "object" != typeof options) {
        return this._timeout = options, this._responseTimeout = 0, this;
      }
      var option;
      for (option in options) {
        switch(option) {
          case "deadline":
            this._timeout = options.deadline;
            break;
          case "response":
            this._responseTimeout = options.response;
            break;
          default:
            console.warn("Unknown timeout option", option);
        }
      }
      return this;
    };
    /**
     * @param {number} count
     * @param {?} num
     * @return {?}
     */
    RequestBase.prototype.retry = function(count, num) {
      return 0 !== arguments.length && true !== count || (count = 1), count <= 0 && (count = 0), this._maxRetries = count, this._retries = 0, this._retryCallback = num, this;
    };
    /** @type {!Array} */
    var ERROR_CODES = ["ECONNRESET", "ETIMEDOUT", "EADDRINFO", "ESOCKETTIMEDOUT"];
    /**
     * @param {!Object} err
     * @param {!Object} error
     * @return {?}
     */
    RequestBase.prototype._shouldRetry = function(err, error) {
      if (!this._maxRetries || this._retries++ >= this._maxRetries) {
        return false;
      }
      if (this._retryCallback) {
        try {
          var stack = this._retryCallback(err, error);
          if (true === stack) {
            return true;
          }
          if (false === stack) {
            return false;
          }
        } catch (logValues) {
          console.error(logValues);
        }
      }
      if (error && error.status && error.status >= 500 && 501 != error.status) {
        return true;
      }
      if (err) {
        if (err.code && ~ERROR_CODES.indexOf(err.code)) {
          return true;
        }
        if (err.timeout && "ECONNABORTED" == err.code) {
          return true;
        }
        if (err.crossDomain) {
          return true;
        }
      }
      return false;
    };
    /**
     * @return {?}
     */
    RequestBase.prototype._retry = function() {
      return this.clearTimeout(), this.req && (this.req = null, this.req = this.request()), this._aborted = false, this.timedout = false, this._end();
    };
    /**
     * @param {!Function} resolve
     * @param {!Function} reject
     * @return {?}
     */
    RequestBase.prototype.then = function(resolve, reject) {
      if (!this._fullfilledPromise) {
        var endOfType = this;
        if (this._endCalled) {
          console.warn("Warning: superagent request was sent twice, because both .end() and .then() were called. Never call .end() if you use promises");
        }
        /** @type {!Promise} */
        this._fullfilledPromise = new Promise(function(saveNotifs, obtainGETData) {
          endOfType.end(function(val, notifications) {
            if (val) {
              obtainGETData(val);
            } else {
              saveNotifs(notifications);
            }
          });
        });
      }
      return this._fullfilledPromise.then(resolve, reject);
    };
    /**
     * @param {!Function} reject
     * @return {?}
     */
    RequestBase.prototype.catch = function(reject) {
      return this.then(void 0, reject);
    };
    /**
     * @param {?} create_content
     * @return {?}
     */
    RequestBase.prototype.use = function(create_content) {
      return create_content(this), this;
    };
    /**
     * @param {!Function} cb
     * @return {?}
     */
    RequestBase.prototype.ok = function(cb) {
      if ("function" != typeof cb) {
        throw Error("Callback required");
      }
      return this._okCallback = cb, this;
    };
    /**
     * @param {!Object} res
     * @return {?}
     */
    RequestBase.prototype._isResponseOK = function(res) {
      return !!res && (this._okCallback ? this._okCallback(res) : res.status >= 200 && res.status < 300);
    };
    /**
     * @param {string} name
     * @return {?}
     */
    RequestBase.prototype.get = function(name) {
      return this._header[name.toLowerCase()];
    };
    /** @type {function(string): ?} */
    RequestBase.prototype.getHeader = RequestBase.prototype.get;
    /**
     * @param {!Object} name
     * @param {string} value
     * @return {?}
     */
    RequestBase.prototype.set = function(name, value) {
      if (isObject(name)) {
        var key;
        for (key in name) {
          this.set(key, name[key]);
        }
        return this;
      }
      return this._header[name.toLowerCase()] = value, this.header[name] = value, this;
    };
    /**
     * @param {string} field
     * @return {?}
     */
    RequestBase.prototype.unset = function(field) {
      return delete this._header[field.toLowerCase()], delete this.header[field], this;
    };
    /**
     * @param {?} name
     * @param {?} val
     * @return {?}
     */
    RequestBase.prototype.field = function(name, val) {
      if (null === name || void 0 === name) {
        throw new Error(".field(name, val) name can not be empty");
      }
      if (this._data && console.error(".field() can't be used if .send() is used. Please use only .send() or only .field() & .attach()"), isObject(name)) {
        var key;
        for (key in name) {
          this.field(key, name[key]);
        }
        return this;
      }
      if (Array.isArray(val)) {
        var i;
        for (i in val) {
          this.field(name, val[i]);
        }
        return this;
      }
      if (null === val || void 0 === val) {
        throw new Error(".field(name, val) val can not be empty");
      }
      return "boolean" == typeof val && (val = "" + val), this._getFormData().append(name, val), this;
    };
    /**
     * @return {?}
     */
    RequestBase.prototype.abort = function() {
      return this._aborted ? this : (this._aborted = true, this.xhr && this.xhr.abort(), this.req && this.req.abort(), this.clearTimeout(), this.emit("abort"), this);
    };
    /**
     * @param {string} user
     * @param {string} password
     * @param {!Object} options
     * @param {!Function} next
     * @return {?}
     */
    RequestBase.prototype._auth = function(user, password, options, next) {
      switch(options.type) {
        case "basic":
          this.set("Authorization", "Basic " + next(user + ":" + password));
          break;
        case "auto":
          /** @type {string} */
          this.username = user;
          /** @type {string} */
          this.password = password;
          break;
        case "bearer":
          this.set("Authorization", "Bearer " + user);
      }
      return this;
    };
    /**
     * @param {number} value
     * @return {?}
     */
    RequestBase.prototype.withCredentials = function(value) {
      return void 0 == value && (value = true), this._withCredentials = value, this;
    };
    /**
     * @param {number} n
     * @return {?}
     */
    RequestBase.prototype.redirects = function(n) {
      return this._maxRedirects = n, this;
    };
    /**
     * @param {number} deepIndicator
     * @return {?}
     */
    RequestBase.prototype.maxResponseSize = function(deepIndicator) {
      if ("number" != typeof deepIndicator) {
        throw TypeError("Invalid argument");
      }
      return this._maxResponseSize = deepIndicator, this;
    };
    /**
     * @return {?}
     */
    RequestBase.prototype.toJSON = function() {
      return {
        method : this.method,
        url : this.url,
        data : this._data,
        headers : this._header
      };
    };
    /**
     * @param {string} data
     * @return {?}
     */
    RequestBase.prototype.send = function(data) {
      var isObj = isObject(data);
      var type = this._header["content-type"];
      if (this._formData && console.error(".send() can't be used if .attach() or .field() is used. Please use only .send() or only .field() & .attach()"), isObj && !this._data) {
        if (Array.isArray(data)) {
          /** @type {!Array} */
          this._data = [];
        } else {
          if (!this._isHost(data)) {
            this._data = {};
          }
        }
      } else {
        if (data && this._data && this._isHost(this._data)) {
          throw Error("Can't merge these send calls");
        }
      }
      if (isObj && isObject(this._data)) {
        var i;
        for (i in data) {
          this._data[i] = data[i];
        }
      } else {
        if ("string" == typeof data) {
          if (!type) {
            this.type("form");
          }
          type = this._header["content-type"];
          /** @type {string} */
          this._data = "application/x-www-form-urlencoded" == type ? this._data ? this._data + "&" + data : data : (this._data || "") + data;
        } else {
          /** @type {string} */
          this._data = data;
        }
      }
      return !isObj || this._isHost(data) ? this : (type || this.type("json"), this);
    };
    /**
     * @param {?} sort
     * @return {?}
     */
    RequestBase.prototype.sortQuery = function(sort) {
      return this._sort = void 0 === sort || sort, this;
    };
    /**
     * @return {undefined}
     */
    RequestBase.prototype._finalizeQueryString = function() {
      var params = this._query.join("&");
      if (params && (this.url += (this.url.indexOf("?") >= 0 ? "&" : "?") + params), this._query.length = 0, this._sort) {
        var index = this.url.indexOf("?");
        if (index >= 0) {
          var queryArr = this.url.substring(index + 1).split("&");
          if ("function" == typeof this._sort) {
            queryArr.sort(this._sort);
          } else {
            queryArr.sort();
          }
          /** @type {string} */
          this.url = this.url.substring(0, index) + "?" + queryArr.join("&");
        }
      }
    };
    /**
     * @return {undefined}
     */
    RequestBase.prototype._appendQueryString = function() {
      console.trace("Unsupported");
    };
    /**
     * @param {string} reason
     * @param {number} timeout
     * @param {string} errno
     * @return {undefined}
     */
    RequestBase.prototype._timeoutError = function(reason, timeout, errno) {
      if (!this._aborted) {
        /** @type {!Error} */
        var err = new Error(reason + timeout + "ms exceeded");
        /** @type {number} */
        err.timeout = timeout;
        /** @type {string} */
        err.code = "ECONNABORTED";
        /** @type {string} */
        err.errno = errno;
        /** @type {boolean} */
        this.timedout = true;
        this.abort();
        this.callback(err);
      }
    };
    /**
     * @return {undefined}
     */
    RequestBase.prototype._setTimeouts = function() {
      var self = this;
      if (this._timeout && !this._timer) {
        /** @type {number} */
        this._timer = setTimeout(function() {
          self._timeoutError("Timeout of ", self._timeout, "ETIME");
        }, this._timeout);
      }
      if (this._responseTimeout && !this._responseTimeoutTimer) {
        /** @type {number} */
        this._responseTimeoutTimer = setTimeout(function() {
          self._timeoutError("Response timeout of ", self._responseTimeout, "ETIMEDOUT");
        }, this._responseTimeout);
      }
    };
  },
  LC85 : function(module, exports, require) {
    /**
     * @return {undefined}
     */
    function noop() {
    }
    /**
     * @param {string} obj
     * @return {?}
     */
    function serialize(obj) {
      if (!setElementTransformProperty(obj)) {
        return obj;
      }
      /** @type {!Array} */
      var showIcon = [];
      var prop;
      for (prop in obj) {
        set(showIcon, prop, obj[prop]);
      }
      return showIcon.join("&");
    }
    /**
     * @param {!Array} file
     * @param {string} id
     * @param {!Object} e
     * @return {undefined}
     */
    function set(file, id, e) {
      if (null != e) {
        if (Array.isArray(e)) {
          e.forEach(function(options) {
            set(file, id, options);
          });
        } else {
          if (setElementTransformProperty(e)) {
            var i;
            for (i in e) {
              set(file, id + "[" + i + "]", e[i]);
            }
          } else {
            file.push(encodeURIComponent(id) + "=" + encodeURIComponent(e));
          }
        }
      } else {
        if (null === e) {
          file.push(encodeURIComponent(id));
        }
      }
    }
    /**
     * @param {string} s
     * @return {?}
     */
    function parseString(s) {
      var t;
      var i;
      var d = {};
      var res = s.split("&");
      /** @type {number} */
      var _p = 0;
      var _len6 = res.length;
      for (; _p < _len6; ++_p) {
        t = res[_p];
        i = t.indexOf("=");
        if (-1 == i) {
          /** @type {string} */
          d[decodeURIComponent(t)] = "";
        } else {
          /** @type {string} */
          d[decodeURIComponent(t.slice(0, i))] = decodeURIComponent(t.slice(i + 1));
        }
      }
      return d;
    }
    /**
     * @param {string} headerStr
     * @return {?}
     */
    function parseHeader(headerStr) {
      var i;
      var k;
      var $orderCol;
      var pivot1;
      var rules = headerStr.split(/\r?\n/);
      var a = {};
      /** @type {number} */
      var j = 0;
      var ruleCount = rules.length;
      for (; j < ruleCount; ++j) {
        k = rules[j];
        if (-1 !== (i = k.indexOf(":"))) {
          $orderCol = k.slice(0, i).toLowerCase();
          pivot1 = readAttributeTypes(k.slice(i + 1));
          a[$orderCol] = pivot1;
        }
      }
      return a;
    }
    /**
     * @param {?} mime
     * @return {?}
     */
    function isJSON(mime) {
      return /[\/+]json($|[^-\w])/.test(mime);
    }
    /**
     * @param {!Object} req
     * @return {undefined}
     */
    function Response(req) {
      /** @type {!Object} */
      this.req = req;
      this.xhr = this.req.xhr;
      this.text = "HEAD" != this.req.method && ("" === this.xhr.responseType || "text" === this.xhr.responseType) || void 0 === this.xhr.responseType ? this.xhr.responseText : null;
      this.statusText = this.req.xhr.statusText;
      var status = this.xhr.status;
      if (1223 === status) {
        /** @type {number} */
        status = 204;
      }
      this._setStatusProperties(status);
      this.header = this.headers = parseHeader(this.xhr.getAllResponseHeaders());
      this.header["content-type"] = this.xhr.getResponseHeader("content-type");
      this._setHeaderProperties(this.header);
      if (null === this.text && req._responseType) {
        this.body = this.xhr.response;
      } else {
        this.body = "HEAD" != this.req.method ? this._parseBody(this.text ? this.text : this.xhr.response) : null;
      }
    }
    /**
     * @param {string} method
     * @param {string} url
     * @return {undefined}
     */
    function Request(method, url) {
      var self = this;
      this._query = this._query || [];
      /** @type {string} */
      this.method = method;
      /** @type {string} */
      this.url = url;
      this.header = {};
      this._header = {};
      this.on("end", function() {
        /** @type {null} */
        var err = null;
        /** @type {null} */
        var res = null;
        try {
          res = new Response(self);
        } catch (str) {
          return err = new Error("Parser is unable to parse the response"), err.parse = true, err.original = str, self.xhr ? (err.rawResponse = void 0 === self.xhr.responseType ? self.xhr.responseText : self.xhr.response, err.status = self.xhr.status ? self.xhr.status : null, err.statusCode = err.status) : (err.rawResponse = null, err.status = null), self.callback(err);
        }
        self.emit("response", res);
        var error;
        try {
          if (!self._isResponseOK(res)) {
            /** @type {!Error} */
            error = new Error(res.statusText || "Unsuccessful HTTP response");
          }
        } catch (callback) {
          error = callback;
        }
        if (error) {
          error.original = err;
          error.response = res;
          error.status = res.status;
          self.callback(error, res);
        } else {
          self.callback(null, res);
        }
      });
    }
    /**
     * @param {string} url
     * @param {string} n
     * @param {string} t
     * @return {?}
     */
    function del(url, n, t) {
      var res = request("DELETE", url);
      return "function" == typeof n && (t = n, n = null), n && res.send(n), t && res.end(t), res;
    }
    var root;
    if ("undefined" != typeof window) {
      /** @type {!Window} */
      root = window;
    } else {
      if ("undefined" != typeof self) {
        /** @type {!Window} */
        root = self;
      } else {
        console.warn("Using browser-only version of superagent in non-browser environment");
        root = this;
      }
    }
    var Emitter = require("+mxV");
    var expect = require("L8b0");
    var setElementTransformProperty = require("XX4+");
    var ResponseBase = require("pcGs");
    var Adapter = require("onnB");
    /** @type {function(string, string): ?} */
    var request = exports = module.exports = function(name, options) {
      return "function" == typeof options ? (new exports.Request("GET", name)).end(options) : 1 == arguments.length ? new exports.Request("GET", name) : new exports.Request(name, options);
    };
    /** @type {function(string, string): undefined} */
    exports.Request = Request;
    /**
     * @return {?}
     */
    request.getXHR = function() {
      if (!(!root.XMLHttpRequest || root.location && "file:" == root.location.protocol && root.ActiveXObject)) {
        return new XMLHttpRequest;
      }
      try {
        return new ActiveXObject("Microsoft.XMLHTTP");
      } catch (e) {
      }
      try {
        return new ActiveXObject("Msxml2.XMLHTTP.6.0");
      } catch (e) {
      }
      try {
        return new ActiveXObject("Msxml2.XMLHTTP.3.0");
      } catch (e) {
      }
      try {
        return new ActiveXObject("Msxml2.XMLHTTP");
      } catch (e) {
      }
      throw Error("Browser-only version of superagent could not find XHR");
    };
    /** @type {function(!Object): ?} */
    var readAttributeTypes = "".trim ? function(commentToCheck) {
      return commentToCheck.trim();
    } : function(aShortcut) {
      return aShortcut.replace(/(^\s*|\s*$)/g, "");
    };
    /** @type {function(string): ?} */
    request.serializeObject = serialize;
    /** @type {function(string): ?} */
    request.parseString = parseString;
    request.types = {
      html : "text/html",
      json : "application/json",
      xml : "text/xml",
      urlencoded : "application/x-www-form-urlencoded",
      form : "application/x-www-form-urlencoded",
      "form-data" : "application/x-www-form-urlencoded"
    };
    request.serialize = {
      "application/x-www-form-urlencoded" : serialize,
      "application/json" : JSON.stringify
    };
    request.parse = {
      "application/x-www-form-urlencoded" : parseString,
      "application/json" : JSON.parse
    };
    ResponseBase(Response.prototype);
    /**
     * @param {number} str
     * @return {?}
     */
    Response.prototype._parseBody = function(str) {
      var parse = request.parse[this.type];
      return this.req._parser ? this.req._parser(this, str) : (!parse && isJSON(this.type) && (parse = request.parse["application/json"]), parse && str && (str.length || str instanceof Object) ? parse(str) : null);
    };
    /**
     * @return {?}
     */
    Response.prototype.toError = function() {
      var req = this.req;
      var method = req.method;
      var url = req.url;
      /** @type {string} */
      var errMsg = "cannot " + method + " " + url + " (" + this.status + ")";
      /** @type {!Error} */
      var err = new Error(errMsg);
      return err.status = this.status, err.method = method, err.url = url, err;
    };
    /** @type {function(!Object): undefined} */
    request.Response = Response;
    Emitter(Request.prototype);
    expect(Request.prototype);
    /**
     * @param {!Object} name
     * @return {?}
     */
    Request.prototype.type = function(name) {
      return this.set("Content-Type", request.types[name] || name), this;
    };
    /**
     * @param {?} type
     * @return {?}
     */
    Request.prototype.accept = function(type) {
      return this.set("Accept", request.types[type] || type), this;
    };
    /**
     * @param {string} data
     * @param {string} value
     * @param {!Object} cfg
     * @return {?}
     */
    Request.prototype.auth = function(data, value, cfg) {
      if (1 === arguments.length) {
        /** @type {string} */
        value = "";
      }
      if ("object" == typeof value && null !== value) {
        /** @type {string} */
        cfg = value;
        /** @type {string} */
        value = "";
      }
      if (!cfg) {
        cfg = {
          type : "function" == typeof btoa ? "basic" : "auto"
        };
      }
      /**
       * @param {?} payload
       * @return {?}
       */
      var onError = function(payload) {
        if ("function" == typeof btoa) {
          return btoa(payload);
        }
        throw new Error("Cannot use basic auth, btoa is not a function");
      };
      return this._auth(data, value, cfg, onError);
    };
    /**
     * @param {string} val
     * @return {?}
     */
    Request.prototype.query = function(val) {
      return "string" != typeof val && (val = serialize(val)), val && this._query.push(val), this;
    };
    /**
     * @param {!Object} event
     * @param {!Object} file
     * @param {!Function} filename
     * @return {?}
     */
    Request.prototype.attach = function(event, file, filename) {
      if (file) {
        if (this._data) {
          throw Error("superagent can't mix .send() and .attach()");
        }
        this._getFormData().append(event, file, filename || file.name);
      }
      return this;
    };
    /**
     * @return {?}
     */
    Request.prototype._getFormData = function() {
      return this._formData || (this._formData = new root.FormData), this._formData;
    };
    /**
     * @param {!Error} err
     * @param {!Object} error
     * @return {?}
     */
    Request.prototype.callback = function(err, error) {
      if (this._shouldRetry(err, error)) {
        return this._retry();
      }
      var fn = this._callback;
      this.clearTimeout();
      if (err) {
        if (this._maxRetries) {
          /** @type {number} */
          err.retries = this._retries - 1;
        }
        this.emit("error", err);
      }
      fn(err, error);
    };
    /**
     * @return {undefined}
     */
    Request.prototype.crossDomainError = function() {
      /** @type {!Error} */
      var err = new Error("Request has been terminated\nPossible causes: the network is offline, Origin is not allowed by Access-Control-Allow-Origin, the page is being unloaded, etc.");
      /** @type {boolean} */
      err.crossDomain = true;
      err.status = this.status;
      err.method = this.method;
      err.url = this.url;
      this.callback(err);
    };
    /** @type {function(): ?} */
    Request.prototype.buffer = Request.prototype.ca = Request.prototype.agent = function() {
      return console.warn("This is not supported in browser version of superagent"), this;
    };
    /** @type {function(): ?} */
    Request.prototype.pipe = Request.prototype.write = function() {
      throw Error("Streaming is not supported in browser version of superagent");
    };
    /**
     * @param {!Object} obj
     * @return {?}
     */
    Request.prototype._isHost = function(obj) {
      return obj && "object" == typeof obj && !Array.isArray(obj) && "[object Object]" !== Object.prototype.toString.call(obj);
    };
    /**
     * @param {!Function} fn
     * @return {?}
     */
    Request.prototype.end = function(fn) {
      return this._endCalled && console.warn("Warning: .end() was called twice. This is not supported in superagent"), this._endCalled = true, this._callback = fn || noop, this._finalizeQueryString(), this._end();
    };
    /**
     * @return {?}
     */
    Request.prototype._end = function() {
      var self = this;
      var xhr = this.xhr = request.getXHR();
      var data = this._formData || this._data;
      this._setTimeouts();
      /**
       * @return {?}
       */
      xhr.onreadystatechange = function() {
        var readyState = xhr.readyState;
        if (readyState >= 2 && self._responseTimeoutTimer && clearTimeout(self._responseTimeoutTimer), 4 == readyState) {
          var ref;
          try {
            ref = xhr.status;
          } catch (e) {
            /** @type {number} */
            ref = 0;
          }
          if (!ref) {
            if (self.timedout || self._aborted) {
              return;
            }
            return self.crossDomainError();
          }
          self.emit("end");
        }
      };
      /**
       * @param {string} direction
       * @param {!Object} e
       * @return {undefined}
       */
      var handleProgress = function(direction, e) {
        if (e.total > 0) {
          /** @type {number} */
          e.percent = e.loaded / e.total * 100;
        }
        /** @type {string} */
        e.direction = direction;
        self.emit("progress", e);
      };
      if (this.hasListeners("progress")) {
        try {
          xhr.onprogress = handleProgress.bind(null, "download");
          if (xhr.upload) {
            xhr.upload.onprogress = handleProgress.bind(null, "upload");
          }
        } catch (e) {
        }
      }
      try {
        if (this.username && this.password) {
          xhr.open(this.method, this.url, true, this.username, this.password);
        } else {
          xhr.open(this.method, this.url, true);
        }
      } catch (err) {
        return this.callback(err);
      }
      if (this._withCredentials && (xhr.withCredentials = true), !this._formData && "GET" != this.method && "HEAD" != this.method && "string" != typeof data && !this._isHost(data)) {
        var contentType = this._header["content-type"];
        var serialize = this._serializer || request.serialize[contentType ? contentType.split(";")[0] : ""];
        if (!serialize && isJSON(contentType)) {
          serialize = request.serialize["application/json"];
        }
        if (serialize) {
          data = serialize(data);
        }
      }
      var key;
      for (key in this.header) {
        if (null != this.header[key] && this.header.hasOwnProperty(key)) {
          xhr.setRequestHeader(key, this.header[key]);
        }
      }
      return this._responseType && (xhr.responseType = this._responseType), this.emit("request", this), xhr.send(void 0 !== data ? data : null), this;
    };
    /**
     * @return {?}
     */
    request.agent = function() {
      return new Adapter;
    };
    ["GET", "POST", "OPTIONS", "PATCH", "PUT", "DELETE"].forEach(function(method) {
      /**
       * @param {(!Function|RegExp|string)} url
       * @param {!Function} fn
       * @return {?}
       */
      Adapter.prototype[method.toLowerCase()] = function(url, fn) {
        var req = new request.Request(method, url);
        return this._setDefaults(req), fn && req.end(fn), req;
      };
    });
    Adapter.prototype.del = Adapter.prototype.delete;
    /**
     * @param {string} url
     * @param {string} n
     * @param {string} t
     * @return {?}
     */
    request.get = function(url, n, t) {
      var req = request("GET", url);
      return "function" == typeof n && (t = n, n = null), n && req.query(n), t && req.end(t), req;
    };
    /**
     * @param {string} cb
     * @param {string} n
     * @param {string} t
     * @return {?}
     */
    request.head = function(cb, n, t) {
      var req = request("HEAD", cb);
      return "function" == typeof n && (t = n, n = null), n && req.query(n), t && req.end(t), req;
    };
    /**
     * @param {string} url
     * @param {string} n
     * @param {string} t
     * @return {?}
     */
    request.options = function(url, n, t) {
      var req = request("OPTIONS", url);
      return "function" == typeof n && (t = n, n = null), n && req.send(n), t && req.end(t), req;
    };
    /** @type {function(string, string, string): ?} */
    request.del = del;
    /** @type {function(string, string, string): ?} */
    request.delete = del;
    /**
     * @param {string} fn
     * @param {string} n
     * @param {string} t
     * @return {?}
     */
    request.patch = function(fn, n, t) {
      var res = request("PATCH", fn);
      return "function" == typeof n && (t = n, n = null), n && res.send(n), t && res.end(t), res;
    };
    /**
     * @param {string} type
     * @param {string} n
     * @param {string} t
     * @return {?}
     */
    request.post = function(type, n, t) {
      var result = request("POST", type);
      return "function" == typeof n && (t = n, n = null), n && result.send(n), t && result.end(t), result;
    };
    /**
     * @param {string} done
     * @param {string} s
     * @param {string} i
     * @return {?}
     */
    request.put = function(done, s, i) {
      var req = request("PUT", done);
      return "function" == typeof s && (i = s, s = null), s && req.send(s), i && req.end(i), req;
    };
  },
  LHhu : function(__weex_module__, __weex_exports__, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
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
     * @param {!Object} a
     * @param {!Object} t
     * @return {undefined}
     */
    function i(a, t) {
      if ("function" != typeof t && null !== t) {
        throw new TypeError("Super expression must either be null or a function, not " + typeof t);
      }
      /** @type {!Object} */
      a.prototype = Object.create(t && t.prototype, {
        constructor : {
          value : a,
          enumerable : false,
          writable : true,
          configurable : true
        }
      });
      if (t) {
        if (Object.setPrototypeOf) {
          Object.setPrototypeOf(a, t);
        } else {
          /** @type {!Object} */
          a.__proto__ = t;
        }
      }
    }
    /** @type {boolean} */
    __weex_exports__.__esModule = true;
    /** @type {function(!Object, ...(Object|null)): !Object} */
    var extend = Object.assign || function(name) {
      /** @type {number} */
      var index = 1;
      for (; index < arguments.length; index++) {
        var options = arguments[index];
        var option;
        for (option in options) {
          if (Object.prototype.hasOwnProperty.call(options, option)) {
            name[option] = options[option];
          }
        }
      }
      return name;
    };
    var _normalizeDataUri = __webpack_require__("3QbQ");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _react = __webpack_require__("V80v");
    var _react2 = _interopRequireDefault(_react);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    var _prepareStyleProperties = __webpack_require__("mSCD");
    var exports = (_interopRequireDefault(_prepareStyleProperties), __webpack_require__("QuDk"));
    var defaultProps = (_propTypes2.default.any, _propTypes2.default.func, _propTypes2.default.node, {
      component : "span",
      childFactory : function(child) {
        return child;
      }
    });
    var TransitionGroup = function($) {
      /**
       * @param {!Object} props
       * @param {?} context
       * @return {?}
       */
      function TransitionGroup(props, context) {
        _classCallCheck(this, TransitionGroup);
        var _this = _possibleConstructorReturn(this, $.call(this, props, context));
        return _this.performAppear = function(key, promise) {
          /** @type {boolean} */
          _this.currentlyTransitioningKeys[key] = true;
          if (promise.componentWillAppear) {
            promise.componentWillAppear(_this._handleDoneAppearing.bind(_this, key, promise));
          } else {
            _this._handleDoneAppearing(key, promise);
          }
        }, _this._handleDoneAppearing = function(key, obj) {
          if (obj.componentDidAppear) {
            obj.componentDidAppear();
          }
          delete _this.currentlyTransitioningKeys[key];
          var prevChildMapping = (0, exports.getChildMapping)(_this.props.children);
          if (!(prevChildMapping && prevChildMapping.hasOwnProperty(key))) {
            _this.performLeave(key, obj);
          }
        }, _this.performEnter = function(key, promise) {
          /** @type {boolean} */
          _this.currentlyTransitioningKeys[key] = true;
          if (promise.componentWillEnter) {
            promise.componentWillEnter(_this._handleDoneEntering.bind(_this, key, promise));
          } else {
            _this._handleDoneEntering(key, promise);
          }
        }, _this._handleDoneEntering = function(key, obj) {
          if (obj.componentDidEnter) {
            obj.componentDidEnter();
          }
          delete _this.currentlyTransitioningKeys[key];
          var prevChildMapping = (0, exports.getChildMapping)(_this.props.children);
          if (!(prevChildMapping && prevChildMapping.hasOwnProperty(key))) {
            _this.performLeave(key, obj);
          }
        }, _this.performLeave = function(key, component) {
          /** @type {boolean} */
          _this.currentlyTransitioningKeys[key] = true;
          if (component.componentWillLeave) {
            component.componentWillLeave(_this._handleDoneLeaving.bind(_this, key, component));
          } else {
            _this._handleDoneLeaving(key, component);
          }
        }, _this._handleDoneLeaving = function(key, component) {
          if (component.componentDidLeave) {
            component.componentDidLeave();
          }
          delete _this.currentlyTransitioningKeys[key];
          var prevChildMapping = (0, exports.getChildMapping)(_this.props.children);
          if (prevChildMapping && prevChildMapping.hasOwnProperty(key)) {
            _this.keysToEnter.push(key);
          } else {
            _this.setState(function(parentModule) {
              /** @type {!Object} */
              var globalDependencies = extend({}, parentModule.children);
              return delete globalDependencies[key], {
                children : globalDependencies
              };
            });
          }
        }, _this.childRefs = Object.create(null), _this.state = {
          children : (0, exports.getChildMapping)(props.children)
        }, _this;
      }
      return i(TransitionGroup, $), TransitionGroup.prototype.componentWillMount = function() {
        this.currentlyTransitioningKeys = {};
        /** @type {!Array} */
        this.keysToEnter = [];
        /** @type {!Array} */
        this.keysToLeave = [];
      }, TransitionGroup.prototype.componentDidMount = function() {
        var grandchildren = this.state.children;
        var key;
        for (key in grandchildren) {
          if (grandchildren[key]) {
            this.performAppear(key, this.childRefs[key]);
          }
        }
      }, TransitionGroup.prototype.componentWillReceiveProps = function(newProps) {
        var result = (0, exports.getChildMapping)(newProps.children);
        var data = this.state.children;
        this.setState({
          children : (0, exports.mergeChildMappings)(data, result)
        });
        var key;
        for (key in result) {
          var envVar = data && data.hasOwnProperty(key);
          if (!(!result[key] || envVar || this.currentlyTransitioningKeys[key])) {
            this.keysToEnter.push(key);
          }
        }
        var prop;
        for (prop in data) {
          var remoteVersion = result && result.hasOwnProperty(prop);
          if (!(!data[prop] || remoteVersion || this.currentlyTransitioningKeys[prop])) {
            this.keysToLeave.push(prop);
          }
        }
      }, TransitionGroup.prototype.componentDidUpdate = function() {
        var _this = this;
        var keysToEnter = this.keysToEnter;
        /** @type {!Array} */
        this.keysToEnter = [];
        keysToEnter.forEach(function(key) {
          return _this.performEnter(key, _this.childRefs[key]);
        });
        var keysToLeave = this.keysToLeave;
        /** @type {!Array} */
        this.keysToLeave = [];
        keysToLeave.forEach(function(key) {
          return _this.performLeave(key, _this.childRefs[key]);
        });
      }, TransitionGroup.prototype.render = function() {
        var _this2 = this;
        /** @type {!Array} */
        var tasks = [];
        var key;
        for (key in this.state.children) {
          !function(key) {
            var child = _this2.state.children[key];
            if (child) {
              /** @type {boolean} */
              var showWeeks = "string" != typeof child.ref;
              var mode = _this2.props.childFactory(child);
              /**
               * @param {?} instance
               * @return {undefined}
               */
              var ref = function(instance) {
                _this2.childRefs[key] = instance;
              };
              if (mode === child && showWeeks) {
                ref = (0, _normalizeDataUri2.default)(child.ref, ref);
              }
              tasks.push(_react2.default.cloneElement(mode, {
                key : key,
                ref : ref
              }));
            }
          }(key);
        }
        /** @type {!Object} */
        var props = extend({}, this.props);
        return delete props.transitionLeave, delete props.transitionName, delete props.transitionAppear, delete props.transitionEnter, delete props.childFactory, delete props.transitionLeaveTimeout, delete props.transitionEnterTimeout, delete props.transitionAppearTimeout, delete props.component, _react2.default.createElement(this.props.component, props, tasks);
      }, TransitionGroup;
    }(_react2.default.Component);
    /** @type {string} */
    TransitionGroup.displayName = "TransitionGroup";
    TransitionGroup.propTypes = {};
    TransitionGroup.defaultProps = defaultProps;
    __weex_exports__.default = TransitionGroup;
    __weex_module__.exports = __weex_exports__.default;
  },
  MKUs : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    /**
     * @param {string} transitionType
     * @return {?}
     */
    function transitionTimeout(transitionType) {
      /** @type {string} */
      var timeoutPropName = "transition" + transitionType + "Timeout";
      /** @type {string} */
      var enabledPropName = "transition" + transitionType;
      return function(props) {
        if (props[enabledPropName]) {
          if (null == props[timeoutPropName]) {
            return new Error(timeoutPropName + " wasn't supplied to CSSTransitionGroup: this can cause unreliable animations and won't be supported in a future version of React. See https://fb.me/react-animation-transition-group-timeout for more information.");
          }
          if ("number" != typeof props[timeoutPropName]) {
            return new Error(timeoutPropName + " must be a number (in milliseconds)");
          }
        }
        return null;
      };
    }
    /** @type {boolean} */
    exports.__esModule = true;
    exports.nameShape = void 0;
    /** @type {function(string): ?} */
    exports.transitionTimeout = transitionTimeout;
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _propTypes = (_interopRequireDefault(_prepareStyleProperties), __webpack_require__("nhKt"));
    var _propTypes2 = _interopRequireDefault(_propTypes);
    exports.nameShape = _propTypes2.default.oneOfType([_propTypes2.default.string, _propTypes2.default.shape({
      enter : _propTypes2.default.string,
      leave : _propTypes2.default.string,
      active : _propTypes2.default.string
    }), _propTypes2.default.shape({
      enter : _propTypes2.default.string,
      enterActive : _propTypes2.default.string,
      leave : _propTypes2.default.string,
      leaveActive : _propTypes2.default.string,
      appear : _propTypes2.default.string,
      appearActive : _propTypes2.default.string
    })]);
  },
  "MWb/" : function(blob, id, require) {
    var utils = require("6uqe");
    /** @type {function(this:Object, *): boolean} */
    var has = Object.prototype.hasOwnProperty;
    var defaults = {
      allowDots : false,
      allowPrototypes : false,
      arrayLimit : 20,
      decoder : utils.decode,
      delimiter : "&",
      depth : 5,
      parameterLimit : 1E3,
      plainObjects : false,
      strictNullHandling : false
    };
    /**
     * @param {!Object} data
     * @param {!Object} options
     * @return {?}
     */
    var parseValues = function(data, options) {
      var obj = {};
      var value = options.ignoreQueryPrefix ? data.replace(/^\?/, "") : data;
      var offset = options.parameterLimit === 1 / 0 ? void 0 : options.parameterLimit;
      var parts = value.split(options.delimiter, offset);
      /** @type {number} */
      var i = 0;
      for (; i < parts.length; ++i) {
        var key;
        var currentValue;
        var part = parts[i];
        var d = part.indexOf("]=");
        var pos = -1 === d ? part.indexOf("=") : d + 1;
        if (-1 === pos) {
          key = options.decoder(part, defaults.decoder);
          /** @type {(null|string)} */
          currentValue = options.strictNullHandling ? null : "";
        } else {
          key = options.decoder(part.slice(0, pos), defaults.decoder);
          currentValue = options.decoder(part.slice(pos + 1), defaults.decoder);
        }
        if (has.call(obj, key)) {
          /** @type {!Array<?>} */
          obj[key] = [].concat(obj[key]).concat(currentValue);
        } else {
          obj[key] = currentValue;
        }
      }
      return obj;
    };
    /**
     * @param {!Array} object
     * @param {string} string
     * @param {!Object} options
     * @return {?}
     */
    var parseObject = function(object, string, options) {
      /** @type {string} */
      var result = string;
      /** @type {number} */
      var property = object.length - 1;
      for (; property >= 0; --property) {
        var results;
        var value = object[property];
        if ("[]" === value) {
          /** @type {!Array} */
          results = [];
          /** @type {!Array<?>} */
          results = results.concat(result);
        } else {
          /** @type {!Object} */
          results = options.plainObjects ? Object.create(null) : {};
          var id = "[" === value.charAt(0) && "]" === value.charAt(value.length - 1) ? value.slice(1, -1) : value;
          /** @type {number} */
          var index = parseInt(id, 10);
          if (!isNaN(index) && value !== id && String(index) === id && index >= 0 && options.parseArrays && index <= options.arrayLimit) {
            /** @type {!Array} */
            results = [];
            results[index] = result;
          } else {
            results[id] = result;
          }
        }
        /** @type {!Object} */
        result = results;
      }
      return result;
    };
    /**
     * @param {string} givenKey
     * @param {string} val
     * @param {!Object} options
     * @return {?}
     */
    var parseKeys = function(givenKey, val, options) {
      if (givenKey) {
        var p = options.allowDots ? givenKey.replace(/\.([^.[]+)/g, "[$1]") : givenKey;
        /** @type {!RegExp} */
        var i = /(\[[^[\]]*])/;
        /** @type {!RegExp} */
        var a = /(\[[^[\]]*])/g;
        /** @type {(Array<string>|null)} */
        var s = i.exec(p);
        var name = s ? p.slice(0, s.index) : p;
        /** @type {!Array} */
        var m = [];
        if (name) {
          if (!options.plainObjects && has.call(Object.prototype, name) && !options.allowPrototypes) {
            return;
          }
          m.push(name);
        }
        /** @type {number} */
        var level = 0;
        for (; null !== (s = a.exec(p)) && level < options.depth;) {
          if (level = level + 1, !options.plainObjects && has.call(Object.prototype, s[1].slice(1, -1)) && !options.allowPrototypes) {
            return;
          }
          m.push(s[1]);
        }
        return s && m.push("[" + p.slice(s.index) + "]"), parseObject(m, val, options);
      }
    };
    /**
     * @param {?} value
     * @param {string} name
     * @return {?}
     */
    blob.exports = function(value, name) {
      var options = name ? utils.assign({}, name) : {};
      if (null !== options.decoder && void 0 !== options.decoder && "function" != typeof options.decoder) {
        throw new TypeError("Decoder has to be a function.");
      }
      if (options.ignoreQueryPrefix = true === options.ignoreQueryPrefix, options.delimiter = "string" == typeof options.delimiter || utils.isRegExp(options.delimiter) ? options.delimiter : defaults.delimiter, options.depth = "number" == typeof options.depth ? options.depth : defaults.depth, options.arrayLimit = "number" == typeof options.arrayLimit ? options.arrayLimit : defaults.arrayLimit, options.parseArrays = false !== options.parseArrays, options.decoder = "function" == typeof options.decoder ?
      options.decoder : defaults.decoder, options.allowDots = "boolean" == typeof options.allowDots ? options.allowDots : defaults.allowDots, options.plainObjects = "boolean" == typeof options.plainObjects ? options.plainObjects : defaults.plainObjects, options.allowPrototypes = "boolean" == typeof options.allowPrototypes ? options.allowPrototypes : defaults.allowPrototypes, options.parameterLimit = "number" == typeof options.parameterLimit ? options.parameterLimit : defaults.parameterLimit, options.strictNullHandling =
      "boolean" == typeof options.strictNullHandling ? options.strictNullHandling : defaults.strictNullHandling, "" === value || null === value || void 0 === value) {
        return options.plainObjects ? Object.create(null) : {};
      }
      var display = "string" == typeof value ? parseValues(value, options) : value;
      /** @type {!Object} */
      var obj = options.plainObjects ? Object.create(null) : {};
      /** @type {!Array<string>} */
      var s = Object.keys(display);
      /** @type {number} */
      var i = 0;
      for (; i < s.length; ++i) {
        /** @type {string} */
        var key = s[i];
        var newObj = parseKeys(key, display[key], options);
        obj = utils.merge(obj, newObj, options);
      }
      return utils.compact(obj);
    };
  },
  MyTs : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _UiRippleInk = __webpack_require__("mRYa");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _AboutPage = __webpack_require__("IJ1K");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _react = __webpack_require__("V80v");
    var _deepAssign = (_interopRequireDefault(_react), __webpack_require__("3/fS"));
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    __webpack_require__("xsko");
    var storeMixin = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _UiIcon2.default)(this, Agent), (0, _UiRippleInk2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).apply(this, arguments));
      }
      return (0, _AboutPage2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "componentDidMount",
        value : function() {
          _deepAssign2.default.init({
            con : "div[data-pull-fresh]",
            minDistance : 4
          });
        }
      }, {
        key : "render",
        value : function() {
          return null;
        }
      }]), Agent;
    }(_react.Component);
    mixin.exports = storeMixin;
  },
  "N/n7" : function(mixin, args, parseAsUTC) {
    /**
     * @param {string} t
     * @param {string} str
     * @return {?}
     */
    function trim(t, str) {
      return t.replace(new RegExp("(^|\\s)" + str + "(?:\\s|$)", "g"), "$1").replace(/\s+/g, " ").replace(/^\s*|\s*$/g, "");
    }
    /**
     * @param {!Object} name
     * @param {string} value
     * @return {undefined}
     */
    mixin.exports = function(name, value) {
      if (name.classList) {
        name.classList.remove(value);
      } else {
        if ("string" == typeof name.className) {
          name.className = trim(name.className, value);
        } else {
          name.setAttribute("class", trim(name.className && name.className.baseVal || "", value));
        }
      }
    };
  },
  P71K : function(mixin, doPost, __webpack_require__) {
    __webpack_require__("bF+g");
    var Object = __webpack_require__("qGgm").Object;
    /**
     * @param {!Object} name
     * @param {string} type
     * @param {!Function} n
     * @return {?}
     */
    mixin.exports = function(name, type, n) {
      return Object.defineProperty(name, type, n);
    };
  },
  Pekt : function(module, cb, bind) {
    var toString = bind("XMdZ");
    var fn = bind("MWb/");
    var v = bind("tF0L");
    module.exports = {
      formats : v,
      parse : fn,
      stringify : toString
    };
  },
  Pj6p : function(srcVersion, runtime, __webpack_require__) {
    var $export = __webpack_require__("K0Kg");
    $export($export.S, "Object", {
      setPrototypeOf : __webpack_require__("wYmI").set
    });
  },
  QLF1 : function(formatters, customFormatters) {
  },
  QVlm : function(module, selector, convertToImages) {
    module.exports = function(win, t) {
      /**
       * @return {undefined}
       */
      function setViewport() {
        if (!elem) {
          /** @type {string} */
          var label = 1 == t.scale ? "width=device-width, " : "";
          if (elem = doc.createElement("meta"), elem.setAttribute("name", "viewport"), elem.setAttribute("content", label + "initial-scale=" + t.scale + ", maximum-scale=" + t.scale + ", minimum-scale=" + t.scale + ", user-scalable=no"), docEl.firstElementChild) {
            docEl.firstElementChild.appendChild(elem);
          } else {
            var wrap = doc.createElement("div");
            wrap.appendChild(elem);
            doc.write(wrap.innerHTML);
          }
        }
      }
      var doc = win.document;
      var docEl = doc.documentElement;
      var elem = doc.querySelector("meta[name='viewport']");
      var currMetaTag = doc.querySelector("meta[name='responsive']");
      /** @type {number} */
      var event = Math.floor(win.devicePixelRatio) || 1;
      /** @type {!Array} */
      var linkEnv = [1, 2, 3];
      /** @type {number} */
      var gutterLine = 1;
      /** @type {number} */
      var _takingTooLongTimeout = 0;
      /** @type {boolean} */
      var isDescending = false;
      if (t.init = function(Materialize) {
        return window.noScaling = Materialize, t.isScalable = isDescending = function() {
          if (Materialize) {
            return false;
          }
          /** @type {(Array<string>|null)} */
          var t = win.navigator.appVersion.match(/iphone/gi);
          /** @type {(Array<string>|null)} */
          var r = win.navigator.appVersion.match(/android/gi);
          /** @type {boolean} */
          var checkLowerCase = !!win.chrome;
          /** @type {string} */
          var ua = win.navigator.userAgent;
          /** @type {(Array<string>|null)} */
          var name = ua.match(/MicroMessenger\/([\d\.]+)/i);
          if (t) {
            /** @type {(Array<string>|null)} */
            var s = ua.match(/(iPhone\sOS)\s([\d_]+)/);
            return !(parseFloat(s[2]) < 7);
          }
          if (r) {
            /** @type {(Array<string>|null)} */
            var chunks = ua.match(/AppleWebKit\/([\d\.]+)/i);
            /** @type {(Array<string>|null)} */
            var startExtentParams = ua.match(/UCBrowser\/([\d\.]+)/i);
            /** @type {(Array<string>|null)} */
            var v = (ua.match(/MQQBrowser\/([\d\.]+)/i), ua.match(/Chrome\/([\d\.]+)/i));
            /** @type {(Array<string>|null)} */
            var hasUartService = ua.match(/MiuiBrowser/i);
            return !!(chunks && parseFloat(chunks[1]) >= 537.36 && (hasUartService || name && parseFloat(name[1]) >= 6.1)) || (!!(startExtentParams && parseFloat(startExtentParams[1]) >= 9.6) || !!(v && parseFloat(v[1]) >= 30 && checkLowerCase));
          }
          return false;
        }(), t.changeScale(), this;
      }, currMetaTag && isDescending && (content = currMetaTag.getAttribute("content"), content)) {
        var v2Destination = content.match(/initial\-dpr=([\d\.]+)/);
        if (v2Destination) {
          /** @type {number} */
          gutterLine = Math.floor(v2Destination[1]);
        }
      }
      return t.scaleLock = false, t.changeScale = function(e, scale) {
        if (!this.scaleLock) {
          if (this.isScalable) {
            /** @type {number} */
            e = Math.floor(e) || event;
            /** @type {number} */
            this.dpr = linkEnv.indexOf(e) > -1 ? e : 3;
          } else {
            /** @type {number} */
            this.dpr = 1;
          }
          /** @type {number} */
          this.scale = 1 / this.dpr;
          if (elem) {
            elem.parentNode.removeChild(elem);
            /** @type {null} */
            elem = null;
          }
          setViewport();
        }
        if (scale && (this.scaleLock = scale), docEl.getBoundingClientRect().width > win.innerWidth) {
          /** @type {(number|string)} */
          var a = 1 == this.scale ? "device-width" : win.innerWidth;
          elem.setAttribute("content", "width=" + a + ",initial-scale=" + this.scale + ", maximum-scale=" + this.scale + ", minimum-scale=" + this.scale + ", user-scalable=no");
        }
        /** @type {number} */
        this.baseFontSize = docEl.getBoundingClientRect().width / 10;
        /** @type {number} */
        this.baseFontSize = Math.max(this.baseFontSize, 32);
        /** @type {string} */
        docEl.style.fontSize = this.baseFontSize + "px";
        docEl.setAttribute("data-dpr", this.dpr);
      }, doc.addEventListener("DOMContentLoaded", function(canCreateDiscussions) {
        /** @type {string} */
        doc.body.style.fontSize = 12 * gutterLine + "px";
      }, false), win.addEventListener("orientationchange", function(canCreateDiscussions) {
        clearTimeout(_takingTooLongTimeout);
        /** @type {number} */
        _takingTooLongTimeout = setTimeout(t.changeScale.bind(t), 300);
      }, false), win.addEventListener("pageshow", function(state) {
        if (state.persisted) {
          clearTimeout(_takingTooLongTimeout);
          if (!window.noScaling) {
            /** @type {number} */
            _takingTooLongTimeout = setTimeout(t.changeScale.bind(t), 300);
          }
        }
      }, false), t.rem2px = function(d) {
        /** @type {number} */
        var szX = parseFloat(d) * this.dpr * this.baseFontSize;
        return "string" == typeof d && d.match(/rem$/) && (szX = szX + "px"), szX;
      }, t.px2rem = function(value) {
        /** @type {number} */
        var val = parseFloat(value) * this.dpr / this.baseFontSize;
        return "string" == typeof value && value.match(/px$/) && (val = val + "rem"), val;
      }, t.px2px = function(s) {
        /** @type {number} */
        var szX = parseFloat(s) * this.dpr;
        return "string" == typeof s && s.match(/px$/) && (szX = szX + "px"), szX;
      }, t;
    }(window, window.responsive || (window.responsive = {
      dpr : 1
    }));
  },
  Qsus : function(module, t, analyzer) {
    /**
     * @param {!Object} s
     * @return {?}
     */
    function fn(s) {
      /** @type {number} */
      var t = (new Date).getTime();
      /** @type {number} */
      var p = Math.max(0, 16 - (t - timeOfLastPatch));
      /** @type {number} */
      var n = setTimeout(s, p);
      return timeOfLastPatch = t, n;
    }
    Object.defineProperty(t, "__esModule", {
      value : true
    });
    var a = analyzer("/BaA");
    var i = function(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }(a);
    /** @type {!Array} */
    var prefixes = ["", "webkit", "moz", "o", "ms"];
    /** @type {string} */
    var cancel = "clearTimeout";
    /** @type {function(!Object): ?} */
    var listener = fn;
    var l = void 0;
    /**
     * @param {string} path
     * @param {string} id
     * @return {?}
     */
    var getKey = function(path, id) {
      return path + (path ? id[0].toUpperCase() + id.substr(1) : id) + "AnimationFrame";
    };
    if (i.default) {
      prefixes.some(function(vendor) {
        var rafKey = getKey(vendor, "request");
        if (rafKey in window) {
          return cancel = getKey(vendor, "cancel"), listener = function(value) {
            return window[rafKey](value);
          };
        }
      });
    }
    /** @type {number} */
    var timeOfLastPatch = (new Date).getTime();
    /**
     * @param {!Object} name
     * @return {?}
     */
    l = function(name) {
      return listener(name);
    };
    /**
     * @param {?} id
     * @return {undefined}
     */
    l.cancel = function(id) {
      if (window[cancel] && "function" == typeof window[cancel]) {
        window[cancel](id);
      }
    };
    /** @type {function(!Object): ?} */
    t.default = l;
    /** @type {function(!Object): ?} */
    module.exports = t.default;
  },
  QuDk : function(module, exports, __webpack_require__) {
    /**
     * @param {string} children
     * @return {?}
     */
    function getChildMapping(children) {
      if (!children) {
        return children;
      }
      var settings = {};
      return _react.Children.map(children, function(child) {
        return child;
      }).forEach(function(prefData) {
        /** @type {!Object} */
        settings[prefData.key] = prefData;
      }), settings;
    }
    /**
     * @param {number} prev
     * @param {!Object} next
     * @return {?}
     */
    function mergeChildMappings(prev, next) {
      /**
       * @param {string} key
       * @return {?}
       */
      function getValueForKey(key) {
        return next.hasOwnProperty(key) ? next[key] : prev[key];
      }
      prev = prev || {};
      next = next || {};
      var nextKeysPending = {};
      /** @type {!Array} */
      var pendingKeys = [];
      var prevKey;
      for (prevKey in prev) {
        if (next.hasOwnProperty(prevKey)) {
          if (pendingKeys.length) {
            /** @type {!Array} */
            nextKeysPending[prevKey] = pendingKeys;
            /** @type {!Array} */
            pendingKeys = [];
          }
        } else {
          pendingKeys.push(prevKey);
        }
      }
      var i = void 0;
      var childMapping = {};
      var nextKey;
      for (nextKey in next) {
        if (nextKeysPending.hasOwnProperty(nextKey)) {
          /** @type {number} */
          i = 0;
          for (; i < nextKeysPending[nextKey].length; i++) {
            var pendingNextKey = nextKeysPending[nextKey][i];
            childMapping[nextKeysPending[nextKey][i]] = getValueForKey(pendingNextKey);
          }
        }
        childMapping[nextKey] = getValueForKey(nextKey);
      }
      /** @type {number} */
      i = 0;
      for (; i < pendingKeys.length; i++) {
        childMapping[pendingKeys[i]] = getValueForKey(pendingKeys[i]);
      }
      return childMapping;
    }
    /** @type {boolean} */
    exports.__esModule = true;
    /** @type {function(string): ?} */
    exports.getChildMapping = getChildMapping;
    /** @type {function(number, !Object): ?} */
    exports.mergeChildMappings = mergeChildMappings;
    var _react = __webpack_require__("V80v");
  },
  R7Xn : function(module, exports, __webpack_require__) {
    (function(canCreateDiscussions, $process) {
      !function(global, elem) {
        /**
         * @param {!Object} value
         * @return {?}
         */
        function fn(value) {
          if ("function" != typeof value) {
            /** @type {!Function} */
            value = new Function("" + value);
          }
          /** @type {!Array} */
          var args = new Array(arguments.length - 1);
          /** @type {number} */
          var i = 0;
          for (; i < args.length; i++) {
            args[i] = arguments[i + 1];
          }
          var listener = {
            callback : value,
            args : args
          };
          return data[type] = listener, setImmediate(type), type++;
        }
        /**
         * @param {!Object} name
         * @return {undefined}
         */
        function clear(name) {
          delete data[name];
        }
        /**
         * @param {!Object} d
         * @return {undefined}
         */
        function success(d) {
          var fn = d.callback;
          var a = d.args;
          switch(a.length) {
            case 0:
              fn();
              break;
            case 1:
              fn(a[0]);
              break;
            case 2:
              fn(a[0], a[1]);
              break;
            case 3:
              fn(a[0], a[1], a[2]);
              break;
            default:
              fn.apply(elem, a);
          }
        }
        /**
         * @param {!Object} key
         * @return {undefined}
         */
        function resolve(key) {
          if (c) {
            setTimeout(resolve, 0, key);
          } else {
            var imageData = data[key];
            if (imageData) {
              /** @type {boolean} */
              c = true;
              try {
                success(imageData);
              } finally {
                clear(key);
                /** @type {boolean} */
                c = false;
              }
            }
          }
        }
        if (!global.setImmediate) {
          var setImmediate;
          /** @type {number} */
          var type = 1;
          var data = {};
          /** @type {boolean} */
          var c = false;
          var document = global.document;
          /** @type {(Object|null)} */
          var attachTo = Object.getPrototypeOf && Object.getPrototypeOf(global);
          attachTo = attachTo && attachTo.setTimeout ? attachTo : global;
          if ("[object process]" === {}.toString.call(global.process)) {
            (function() {
              /**
               * @param {?} data
               * @return {undefined}
               */
              setImmediate = function(data) {
                $process.nextTick(function() {
                  resolve(data);
                });
              };
            })();
          } else {
            if (function() {
              if (global.postMessage && !global.importScripts) {
                /** @type {boolean} */
                var t = true;
                var oldOnMessage = global.onmessage;
                return global.onmessage = function() {
                  /** @type {boolean} */
                  t = false;
                }, global.postMessage("", "*"), global.onmessage = oldOnMessage, t;
              }
            }()) {
              (function() {
                /** @type {string} */
                var prefix = "setImmediate$" + Math.random() + "$";
                /**
                 * @param {!Object} event
                 * @return {undefined}
                 */
                var onMessage = function(event) {
                  if (event.source === global && "string" == typeof event.data && 0 === event.data.indexOf(prefix)) {
                    resolve(+event.data.slice(prefix.length));
                  }
                };
                if (global.addEventListener) {
                  global.addEventListener("message", onMessage, false);
                } else {
                  global.attachEvent("onmessage", onMessage);
                }
                /**
                 * @param {number} name
                 * @return {undefined}
                 */
                setImmediate = function(name) {
                  global.postMessage(prefix + name, "*");
                };
              })();
            } else {
              if (global.MessageChannel) {
                (function() {
                  /** @type {!MessageChannel} */
                  var channel = new MessageChannel;
                  /**
                   * @param {!Object} event
                   * @return {undefined}
                   */
                  channel.port1.onmessage = function(event) {
                    resolve(event.data);
                  };
                  /**
                   * @param {number} data
                   * @return {undefined}
                   */
                  setImmediate = function(data) {
                    channel.port2.postMessage(data);
                  };
                })();
              } else {
                if (document && "onreadystatechange" in document.createElement("script")) {
                  (function() {
                    var root = document.documentElement;
                    /**
                     * @param {?} data
                     * @return {undefined}
                     */
                    setImmediate = function(data) {
                      var script = document.createElement("script");
                      /**
                       * @return {undefined}
                       */
                      script.onreadystatechange = function() {
                        resolve(data);
                        /** @type {null} */
                        script.onreadystatechange = null;
                        root.removeChild(script);
                        /** @type {null} */
                        script = null;
                      };
                      root.appendChild(script);
                    };
                  })();
                } else {
                  (function() {
                    /**
                     * @param {number} fn
                     * @return {undefined}
                     */
                    setImmediate = function(fn) {
                      setTimeout(resolve, 0, fn);
                    };
                  })();
                }
              }
            }
          }
          /** @type {function(!Object): ?} */
          attachTo.setImmediate = fn;
          /** @type {function(!Object): undefined} */
          attachTo.clearImmediate = clear;
        }
      }("undefined" == typeof self ? void 0 === canCreateDiscussions ? this : canCreateDiscussions : self);
    }).call(exports, __webpack_require__("dTv7"), __webpack_require__("RxL3"));
  },
  RIBO : function(formatters, customFormatters) {
  },
  RIhk : function(module, exports, __webpack_require__) {
    __webpack_require__("XgqU");
    module.exports = __webpack_require__("qGgm").Object.assign;
  },
  RfGB : function(formatters, customFormatters) {
  },
  RvJg : function(module, id, require) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function $(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var sources = require("gf5I");
    var file = $(sources);
    var _UiIcon = require("mZJ8");
    var _UiIcon2 = $(_UiIcon);
    var permissions = require("p7ii");
    var res = $(permissions);
    var d = require("iltz");
    var f = $(d);
    var h = require("fvPU");
    var el = $(h);
    var E = require("hJ6a");
    var chars = $(E);
    var layer = require("mRYa");
    var tags = $(layer);
    var y = require("IJ1K");
    var $origin = $(y);
    var Path = require("V80v");
    var p = $(Path);
    var _propTypes = require("nhKt");
    var _propTypes2 = $(_propTypes);
    var _CalendarDay = require("afpQ");
    var _CalendarDay2 = $(_CalendarDay);
    var button2 = require("1uVg");
    var button = $(button2);
    var _DraggableCore = require("Es/p");
    var _DraggableCore2 = $(_DraggableCore);
    var S = require("0vED");
    var t = $(S);
    var document = require("IFEe");
    var ShapeMaker_1 = $(document);
    var date = require("MyTs");
    var ShapeViewer_1 = $(date);
    var c = require("YWnE");
    var root = $(c);
    var srvc = require("BV5S");
    var item = $(srvc);
    var _deepAssign = require("FKII");
    var _deepAssign2 = $(_deepAssign);
    var window = require("bVOP");
    var wrappedWindow = $(window);
    var path = require("gT+X");
    var report = $(path);
    require("RIBO");
    wrappedWindow.default.initScrollEvents();
    var PercentageSymbol = function(e) {
      /**
       * @return {?}
       */
      function Sankey() {
        var _Object$getPrototypeO;
        var local_mobile_core_user_remove_user_device;
        var scope;
        var wsFunction;
        (0, el.default)(this, Sankey);
        /** @type {number} */
        var _len = arguments.length;
        /** @type {!Array} */
        var args = Array(_len);
        /** @type {number} */
        var _key = 0;
        for (; _key < _len; _key++) {
          args[_key] = arguments[_key];
        }
        return local_mobile_core_user_remove_user_device = scope = (0, tags.default)(this, (_Object$getPrototypeO = Sankey.__proto__ || (0, f.default)(Sankey)).call.apply(_Object$getPrototypeO, [this].concat(args))), scope.state = {
          listData : scope.props.listData
        }, wsFunction = local_mobile_core_user_remove_user_device, (0, tags.default)(scope, wsFunction);
      }
      return (0, $origin.default)(Sankey, e), (0, chars.default)(Sankey, [{
        key : "componentWillReceiveProps",
        value : function(name) {
          if (0 !== name.listData.length && 0 === this.props.listData.length && this.showMaterial()) {
            var received = this.props.GTMValue.adMaterialOptions;
            /** @type {*} */
            var n = JSON.parse(root.default.getCookieForLocal("ad_material_options")) || {};
            /** @type {number} */
            var r = (new Date).getTime() - received.adMaterialUpateTime;
            if (r >= 0) {
              if (n.adMaterialChannels) {
                root.default.setCookieForLocal("ad_material_options", (0, res.default)(received), 864E5 - r);
              }
            } else {
              /** @type {*} */
              received = n;
            }
            var spotPos = received.adMaterialPos || 3;
            /** @type {number} */
            var i = Math.floor(Math.random() * received.adMaterials.length);
            var a = received.adMaterials[i];
            /** @type {number} */
            a.version = i;
            this.props.addADMaterial({
              adMaterial : a,
              pos : spotPos
            });
            window.maevent("creative", "show", i, 1, {
              nonInteraction : true
            });
          }
          this.updateTimeAgo(name.listData);
          this.updateXpromt(name);
        }
      }, {
        key : "updateXpromt",
        value : function(name) {
          var n = name.currentChannel;
          var get = name.GTMValue;
          var src = name.listData;
          var data = get.xpromt || {};
          var j = (0, _UiIcon2.default)(data);
          var map = root.default.cloneDeep(src);
          if (-1 === j.indexOf(n)) {
            return false;
          }
          data[n].forEach(function(left, canCreateDiscussions) {
            /** @type {boolean} */
            left.xpromt = true;
            map.splice(left.position - 1, 0, left);
          });
          this.setState({
            listData : map
          });
        }
      }, {
        key : "componentDidMount",
        value : function() {
          var columns = this;
          columns.updateTimeAgo(this.props.listData);
          setInterval(function() {
            return columns.updateTimeAgo(columns.props.listData);
          }, 6E4);
          if ("object" === (void 0 === _deepAssign2.default ? "undefined" : (0, file.default)(_deepAssign2.default))) {
            _deepAssign2.default.initShowEvents({
              attribute : "data-show"
            });
          }
        }
      }, {
        key : "componentDidUpdate",
        value : function() {
          /** @type {boolean} */
          _deepAssign2.default.scrollChangeDisable = false;
          _deepAssign2.default.scrollUpdate();
        }
      }, {
        key : "updateTimeAgo",
        value : function(value) {
          var docs = root.default.cloneDeep(value);
          docs.forEach(function(scope) {
            var timeAgo = (0, item.default)(scope.datetime, {
              daysAgoFormat : "MM-dd"
            });
            scope.timeago = timeAgo;
          });
          this.setState({
            listData : docs
          });
        }
      }, {
        key : "showMaterial",
        value : function() {
          var LocaTable = this.props.GTMValue.adMaterialOptions;
          return !(!LocaTable || !LocaTable.adMaterialChannels) && (-1 !== LocaTable.adMaterialChannels.indexOf(root.default.hash("channel")) && !!LocaTable.adMaterials);
        }
      }, {
        key : "render",
        value : function() {
          var self = this;
          return p.default.createElement("content", {
            id : "pageletListContent",
            className : "feed-list-container"
          }, p.default.createElement(ShapeViewer_1.default, null), p.default.createElement("div", {
            className : "list_content",
            "data-pull-fresh" : "1"
          }, this.state.listData.map(function(data, index) {
            data.index = index + 1;
            var r = data.index;
            return data.action_label = "click_" + ("__all__" === self.props.currentChannel ? "headline" : self.props.currentChannel), report.default.browser.liteh5 && report.default.os.ios && (data.source_url && (data.source_url = root.default.appendQuery(data.source_url, "need_open_window=1")), data.url && (data.url = root.default.appendQuery(data.url, "need_open_window=1"))), data.showAdMaterial ? p.default.createElement(ShapeMaker_1.default, {
              key : r,
              datum : data.adMaterial
            }) : data.ad_id ? p.default.createElement(button.default, {
              key : r,
              datum : data
            }) : "video" === self.props.currentChannel || true === window.isVideoListPage ? p.default.createElement(_DraggableCore2.default, {
              key : r,
              datum : data,
              currentChannel : self.props.currentChannel
            }) : data.xpromt ? p.default.createElement(t.default, {
              key : r,
              datum : data
            }) : p.default.createElement(_CalendarDay2.default, {
              key : r,
              datum : data,
              currentChannel : self.props.currentChannel
            });
          })), p.default.createElement("div", {
            className : "list_bottom"
          }, p.default.createElement("section", {
            className : "loadmoretip"
          }, p.default.createElement("a", {
            href : "#"
          }, this.props.tips))));
        }
      }]), Sankey;
    }(Path.Component);
    PercentageSymbol.propTypes = {
      GTMValue : _propTypes2.default.object,
      listData : _propTypes2.default.array,
      dispatch : _propTypes2.default.func,
      currentChannel : _propTypes2.default.string,
      tips : _propTypes2.default.string,
      props : _propTypes2.default.object,
      addADMaterial : _propTypes2.default.func
    };
    module.exports = PercentageSymbol;
  },
  SJPe : function(mixin, args, parseAsUTC) {
    var storeMixin = function() {
      /**
       * @param {!CanvasRenderingContext2D} ctx
       * @param {number} c
       * @param {number} d
       * @param {number} r
       * @param {number} t
       * @param {number} a
       * @param {number} b
       * @param {number} callback
       * @return {undefined}
       */
      var render = function(ctx, c, d, r, t, a, b, callback) {
        if ("string" == typeof c) {
          /** @type {number} */
          c = parseFloat(c);
        }
        if ("string" == typeof d) {
          /** @type {number} */
          d = parseFloat(d);
        }
        if ("string" == typeof r) {
          /** @type {number} */
          r = parseFloat(r);
        }
        if ("string" == typeof t) {
          /** @type {number} */
          t = parseFloat(t);
        }
        if ("string" == typeof a) {
          /** @type {number} */
          a = parseFloat(a);
        }
        if ("string" == typeof b) {
          /** @type {number} */
          b = parseFloat(b);
        }
        Math.PI;
        switch(ctx.save(), ctx.beginPath(), ctx.moveTo(c, d), ctx.lineTo(r, t), ctx.lineTo(a, b), callback) {
          case 0:
            /** @type {number} */
            var h = Math.sqrt((a - c) * (a - c) + (b - d) * (b - d));
            ctx.arcTo(r, t, c, d, .55 * h);
            ctx.fill();
            break;
          case 1:
            ctx.beginPath();
            ctx.moveTo(c, d);
            ctx.lineTo(r, t);
            ctx.lineTo(a, b);
            ctx.lineTo(c, d);
            ctx.fill();
            break;
          case 2:
            ctx.stroke();
            break;
          case 3:
            /** @type {number} */
            var rx = (c + r + a) / 3;
            /** @type {number} */
            var yip = (d + t + b) / 3;
            ctx.quadraticCurveTo(rx, yip, c, d);
            ctx.fill();
            break;
          case 4:
            var w;
            var y2;
            var x;
            var y;
            if (a == c) {
              /** @type {number} */
              h = b - d;
              /** @type {number} */
              w = (r + c) / 2;
              /** @type {number} */
              x = (r + c) / 2;
              y2 = t + h / 5;
              /** @type {number} */
              y = t - h / 5;
            } else {
              /** @type {number} */
              h = Math.sqrt((a - c) * (a - c) + (b - d) * (b - d));
              /** @type {number} */
              var footerSpace_ = (c + a) / 2;
              /** @type {number} */
              var p_ = (d + b) / 2;
              /** @type {number} */
              var left = (footerSpace_ + r) / 2;
              /** @type {number} */
              var height = (p_ + t) / 2;
              /** @type {number} */
              var n = (b - d) / (a - c);
              /** @type {number} */
              var width = h / (2 * Math.sqrt(n * n + 1)) / 5;
              /** @type {number} */
              var offset = n * width;
              /** @type {number} */
              w = left - width;
              /** @type {number} */
              y2 = height - offset;
              /** @type {number} */
              x = left + width;
              /** @type {number} */
              y = height + offset;
            }
            ctx.bezierCurveTo(w, y2, x, y, c, d);
            ctx.fill();
        }
        ctx.restore();
      };
      /**
       * @param {!CanvasRenderingContext2D} ctx
       * @param {number} x
       * @param {number} y
       * @param {number} r
       * @param {?} startangle
       * @param {?} endangle
       * @param {boolean} anticlockwise
       * @param {number} style
       * @param {number} size
       * @param {number} angle
       * @param {number} d
       * @param {number} lineWidth
       * @param {number} lineRatio
       * @return {undefined}
       */
      var drawArcedArrow = function(ctx, x, y, r, startangle, endangle, anticlockwise, style, size, angle, d, lineWidth, lineRatio) {
        style = void 0 !== style ? style : 3;
        size = void 0 !== size ? size : 1;
        angle = void 0 !== angle ? angle : Math.PI / 8;
        d = void 0 !== d ? d : 10;
        lineWidth = void 0 !== lineWidth ? lineWidth : 1;
        ctx.save();
        /** @type {number} */
        ctx.lineWidth = lineWidth;
        ctx.beginPath();
        ctx.arc(x, y, r, startangle, endangle, anticlockwise);
        ctx.stroke();
        var sx;
        var sy;
        var bearingRad;
        var destx;
        var desty;
        if (1 & size && (sx = Math.cos(startangle) * r + x, sy = Math.sin(startangle) * r + y, bearingRad = Math.atan2(x - sx, sy - y), anticlockwise ? (destx = sx + 10 * Math.cos(bearingRad), desty = sy + 10 * Math.sin(bearingRad)) : (destx = sx - 10 * Math.cos(bearingRad), desty = sy - 10 * Math.sin(bearingRad)), drawArrow(ctx, sx, sy, destx, desty, style, 2, angle, d)), 2 & size) {
          sx = Math.cos(endangle) * r + x;
          sy = Math.sin(endangle) * r + y;
          /** @type {number} */
          bearingRad = Math.atan2(x - sx, sy - y);
          if (anticlockwise) {
            /** @type {number} */
            destx = sx - 10 * Math.cos(bearingRad);
            /** @type {number} */
            desty = sy - 10 * Math.sin(bearingRad);
          } else {
            destx = sx + 10 * Math.cos(bearingRad);
            desty = sy + 10 * Math.sin(bearingRad);
          }
          drawArrow(ctx, sx - lineRatio * Math.sin(endangle), sy + lineRatio * Math.cos(endangle), destx - lineRatio * Math.sin(endangle), desty + lineRatio * Math.cos(endangle), style, 2, angle, d);
        }
        ctx.restore();
      };
      /**
       * @param {!CanvasRenderingContext2D} ctx
       * @param {number} x
       * @param {number} y
       * @param {number} x2
       * @param {number} y2
       * @param {number} fn
       * @param {number} size
       * @param {number} c
       * @param {number} d
       * @return {undefined}
       */
      var drawArrow = function(ctx, x, y, x2, y2, fn, size, c, d) {
        if ("string" == typeof x) {
          /** @type {number} */
          x = parseFloat(x);
        }
        if ("string" == typeof y) {
          /** @type {number} */
          y = parseFloat(y);
        }
        if ("string" == typeof x2) {
          /** @type {number} */
          x2 = parseFloat(x2);
        }
        if ("string" == typeof y2) {
          /** @type {number} */
          y2 = parseFloat(y2);
        }
        fn = void 0 !== fn ? fn : 3;
        size = void 0 !== size ? size : 1;
        c = void 0 !== c ? c : Math.PI / 8;
        d = void 0 !== d ? d : 10;
        var tox;
        var toy;
        var right;
        var bottom;
        /** @type {!Function} */
        var callback = "function" != typeof fn ? render : fn;
        /** @type {number} */
        var dist = Math.sqrt((x2 - x) * (x2 - x) + (y2 - y) * (y2 - y));
        /** @type {number} */
        var ratio = (dist - d / 3) / dist;
        if (1 & size) {
          /** @type {number} */
          tox = Math.round(x + (x2 - x) * ratio);
          /** @type {number} */
          toy = Math.round(y + (y2 - y) * ratio);
        } else {
          /** @type {number} */
          tox = x2;
          /** @type {number} */
          toy = y2;
        }
        if (2 & size) {
          right = x + (x2 - x) * (1 - ratio);
          bottom = y + (y2 - y) * (1 - ratio);
        } else {
          /** @type {number} */
          right = x;
          /** @type {number} */
          bottom = y;
        }
        ctx.beginPath();
        ctx.moveTo(right, bottom);
        ctx.lineTo(tox, toy);
        ctx.stroke();
        /** @type {number} */
        var a = Math.atan2(y2 - y, x2 - x);
        /** @type {number} */
        var rad = Math.abs(d / Math.cos(c));
        if (1 & size) {
          var d = a + Math.PI + c;
          var tx = x2 + Math.cos(d) * rad;
          var yi = y2 + Math.sin(d) * rad;
          /** @type {number} */
          var r = a + Math.PI - c;
          var x4 = x2 + Math.cos(r) * rad;
          var y4 = y2 + Math.sin(r) * rad;
          callback(ctx, tx, yi, x2, y2, x4, y4, fn);
        }
        if (2 & size) {
          d = a + c;
          tx = x + Math.cos(d) * rad;
          yi = y + Math.sin(d) * rad;
          /** @type {number} */
          r = a - c;
          x4 = x + Math.cos(r) * rad;
          y4 = y + Math.sin(r) * rad;
          callback(ctx, tx, yi, x, y, x4, y4, fn);
        }
      };
      return {
        drawArrow : drawArrow,
        drawArcedArrow : drawArcedArrow
      };
    }();
    mixin.exports = storeMixin;
  },
  Ufk5 : function(module, exports, __webpack_require__) {
    module.exports = {
      default : __webpack_require__("mJKx"),
      __esModule : true
    };
  },
  UoBj : function(module, level, generator) {
    (function(__webpack_module_template_argument_0__) {
      module.exports = function(Chartist, me) {
        var DOM = me.document;
        var keys = {
          NONE : 0,
          NOOP : 1,
          UP : 2,
          RIGHT : 3,
          DOWN : 4,
          LEFT : 5,
          LEFT_RIGHT : 6
        };
        var defaultOptions = {
          con : "",
          minDistance : 4,
          onPullStart : function() {
          },
          onMove : function() {
          },
          onPullEnd : function() {
          }
        };
        /**
         * @param {!Object} options
         * @return {undefined}
         */
        var init = function(options) {
          if ("string" == typeof options.con) {
            options.con = DOM.querySelector(options.con);
          }
          this.options = Chartist.extend({}, defaultOptions, options);
          /** @type {boolean} */
          this.hasTouch = false;
          /** @type {number} */
          this.direction = keys.NONE;
          /** @type {number} */
          this.distanceX = this.startY = this.startX = 0;
          /** @type {boolean} */
          this.isPull = false;
          this.initEvent();
        };
        return init.prototype = {
          initEvent : function() {
            var that = this;
            /**
             * @param {!Object} e
             * @return {undefined}
             */
            this._touchStart = function(e) {
              that.__start(e);
            };
            /**
             * @param {!Event} event
             * @return {undefined}
             */
            this._touchMove = function(event) {
              that.__move(event);
            };
            /**
             * @param {!Event} e
             * @return {undefined}
             */
            this._touchEnd = function(e) {
              that.__end(e);
            };
            this.options.con.addEventListener("touchstart", this._touchStart, false);
            this.options.con.addEventListener("touchmove", this._touchMove, false);
            this.options.con.addEventListener("touchend", this._touchEnd, false);
          },
          detachEvent : function() {
            this.options.con.removeEventListener("touchstart", this._touchStart, false);
            this.options.con.removeEventListener("touchmove", this._touchMove, false);
            this.options.con.removeEventListener("touchend", this._touchEnd, false);
          },
          __start : function(e) {
            e = e.targetTouches;
            if (1 === e.length) {
              this.startX = e[0].pageX;
              this.startY = e[0].pageY;
              /** @type {number} */
              this.direction = keys.NONE;
              /** @type {number} */
              this.distanceX = 0;
              /** @type {boolean} */
              this.hasTouch = true;
              /** @type {number} */
              this.startScrollY = me.scrollY;
            }
          },
          __move : function(evt) {
            if (this.hasTouch) {
              if (this.direction === keys.UP) {
                return;
              }
              var event = evt.targetTouches[0];
              if (this.direction === keys.NONE) {
                /** @type {number} */
                this.distanceX = event.pageX - this.startX;
                /** @type {number} */
                this.distanceY = event.pageY - this.startY;
                /** @type {number} */
                var abs_dy = Math.abs(this.distanceY);
                /** @type {number} */
                var abs_dx = Math.abs(this.distanceX);
                if (abs_dx + abs_dy > this.options.minDistance) {
                  /** @type {number} */
                  this.direction = abs_dx > 1.73 * abs_dy ? keys.LEFT_RIGHT : abs_dy > 1.73 * abs_dx ? this.distanceY < 0 ? keys.UP : keys.DOWN : keys.NOOP;
                  if (this.startScrollY < 10 && this.distanceY > 0) {
                    /** @type {number} */
                    this.direction = keys.DOWN;
                  }
                }
                if (this.startScrollY < 10 && this.direction === keys.DOWN && this.distanceY > this.options.minDistance) {
                  /** @type {boolean} */
                  this.isPull = true;
                  this.options.onPullStart(evt, this.distanceY);
                }
              }
              if (this.isPull && this.direction === keys.DOWN) {
                /** @type {number} */
                this.distanceY = event.pageY - this.startY;
                /** @type {number} */
                this.refreshY = parseInt(this.distanceY * this.options.pullRatio);
                this.options.onMove(evt, this.distanceY);
              }
            }
          },
          __end : function(e) {
            if (!(!this.hasTouch || keys.LEFT_RIGHT !== this.direction && keys.DOWN !== this.direction)) {
              if (this.direction === keys.LEFT_RIGHT) {
                e.preventDefault();
                this.options.onPullEnd(e, this.distanceX, keys.LEFT_RIGHT);
              }
              if (this.direction === keys.DOWN && this.isPull) {
                e.preventDefault();
                this.options.onPullEnd(e, this.distanceY, keys.DOWN);
              }
            }
            /** @type {boolean} */
            this.hasTouch = false;
            /** @type {boolean} */
            this.isPull = false;
          }
        }, {
          init : function(selector) {
            return new init(selector);
          },
          DIRECTION : keys
        };
      }(__webpack_module_template_argument_0__, window);
    }).call(level, generator("gXQ3"));
  },
  VPAO : function(eta, lmbda, n) {
    !function(options, doc, n) {
      /**
       * @param {string} g
       * @return {?}
       */
      function render(g) {
        var i = parseuri("__tasessionId");
        return i ? i && g && (set("__tasessionId", i, {
          expires : 1800
        }), iMachine = false) : (x = (new Date).getTime(), i = "" + getRandomCharacters(9) + (new Date).getTime(), set("__tasessionId", i, {
          expires : 1800
        }), iMachine = true), i;
      }
      /**
       * @param {number} size
       * @return {?}
       */
      function getRandomCharacters(size) {
        /** @type {string} */
        var s = "";
        for (; s.length < size; s = s + Math.random().toString(36).substr(2)) {
        }
        return s.substr(0, size);
      }
      /**
       * @param {!Array} obj
       * @return {?}
       */
      function fn(obj) {
        var source;
        var prop;
        /** @type {number} */
        var i = 1;
        /** @type {number} */
        var argl = arguments.length;
        for (; i < argl; i++) {
          source = arguments[i];
          for (prop in source) {
            if (Object.prototype.hasOwnProperty.call(source, prop)) {
              obj[prop] = source[prop];
            }
          }
        }
        return obj;
      }
      /**
       * @param {string} url
       * @return {?}
       */
      function parseuri(url) {
        var kvpair;
        /** @type {!RegExp} */
        var embedReg = new RegExp("(^| )" + url + "=([^;]*)(;|$)");
        return (kvpair = doc.cookie.match(embedReg)) ? unescape(kvpair[2]) : null;
      }
      /**
       * @param {string} key
       * @param {?} value
       * @param {!Object} sess
       * @return {undefined}
       */
      function set(key, value, sess) {
        var expDate;
        var cookie = {
          path : "/"
        };
        fn(cookie, sess);
        if (cookie.expires) {
          /** @type {!Date} */
          expDate = new Date;
          expDate.setTime(expDate.getTime() + 1E3 * sess.expires);
        }
        /** @type {string} */
        doc.cookie = [key, "=", escape(value), cookie.expires ? "; expires=" + expDate.toUTCString() : "", cookie.path ? "; path=" + cookie.path : "", cookie.domain ? "; domain=" + cookie.domain : "", cookie.secure ? "; secure" : ""].join("");
      }
      var u = {};
      var new_value = {};
      /** @type {number} */
      var x = (new Date).getTime();
      /** @type {boolean} */
      var iMachine = false;
      /**
       * @param {?} obj
       * @return {undefined}
       */
      u.setup = function(obj) {
        fn(new_value, obj);
      };
      /**
       * @param {string} type
       * @param {?} callback
       * @return {undefined}
       */
      u.send = function(type, callback) {
        /** @type {!Array} */
        var drilldownLevelLabels = [];
        var obj = {};
        if (fn(obj, new_value, callback, {
          sid : render("event" === type),
          type : type
        }), "close" !== type || (obj.st = (new Date).getTime() - x, !iMachine)) {
          var prop;
          for (prop in obj) {
            drilldownLevelLabels.push(prop + "=" + obj[prop]);
          }
          drilldownLevelLabels.push("t=" + (new Date).getTime());
          drilldownLevelLabels.push("source=wap");
          /** @type {!Image} */
          options._ta_log_img_ = new Image;
          /** @type {string} */
          options._ta_log_img_.src = "//m.toutiao.com/user_log/?" + drilldownLevelLabels.join("&");
        }
      };
      /**
       * @param {?} event
       * @return {undefined}
       */
      options.onpagehide = function(event) {
        u.send("close", {});
      };
      options.taAnalysis = u;
    }(window, document);
  },
  "X+OT" : function(formatters, customFormatters) {
    !function(self) {
      /**
       * @param {string} name
       * @return {?}
       */
      function normalizeName(name) {
        if ("string" != typeof name && (name = String(name)), /[^a-z0-9\-#$%&'*+.\^_`|~]/i.test(name)) {
          throw new TypeError("Invalid character in header field name");
        }
        return name.toLowerCase();
      }
      /**
       * @param {string} name
       * @return {?}
       */
      function normalizeValue(name) {
        return "string" != typeof name && (name = String(name)), name;
      }
      /**
       * @param {!Array} items
       * @return {?}
       */
      function each(items) {
        var iterable = {
          next : function() {
            var _eof = items.shift();
            return {
              done : void 0 === _eof,
              value : _eof
            };
          }
        };
        return support.iterable && (iterable[Symbol.iterator] = function() {
          return iterable;
        }), iterable;
      }
      /**
       * @param {!Object} headers
       * @return {undefined}
       */
      function Headers(headers) {
        this.map = {};
        if (headers instanceof Headers) {
          headers.forEach(function(value, rows) {
            this.append(rows, value);
          }, this);
        } else {
          if (Array.isArray(headers)) {
            headers.forEach(function(header) {
              this.append(header[0], header[1]);
            }, this);
          } else {
            if (headers) {
              Object.getOwnPropertyNames(headers).forEach(function(name) {
                this.append(name, headers[name]);
              }, this);
            }
          }
        }
      }
      /**
       * @param {?} body
       * @return {?}
       */
      function consumed(body) {
        if (body.bodyUsed) {
          return Promise.reject(new TypeError("Already read"));
        }
        /** @type {boolean} */
        body.bodyUsed = true;
      }
      /**
       * @param {!Object} file
       * @return {?}
       */
      function require(file) {
        return new Promise(function(fileCallback, callback) {
          /**
           * @return {undefined}
           */
          file.onload = function() {
            fileCallback(file.result);
          };
          /**
           * @return {undefined}
           */
          file.onerror = function() {
            callback(file.error);
          };
        });
      }
      /**
       * @param {?} value
       * @return {?}
       */
      function done(value) {
        /** @type {!FileReader} */
        var f = new FileReader;
        var result = require(f);
        return f.readAsArrayBuffer(value), result;
      }
      /**
       * @param {?} blob
       * @return {?}
       */
      function readBlobAsText(blob) {
        /** @type {!FileReader} */
        var f = new FileReader;
        var version = require(f);
        return f.readAsText(blob), version;
      }
      /**
       * @param {?} data
       * @return {?}
       */
      function readArrayBufferAsText(data) {
        /** @type {!Uint8Array} */
        var buf = new Uint8Array(data);
        /** @type {!Array} */
        var n = new Array(buf.length);
        /** @type {number} */
        var i = 0;
        for (; i < buf.length; i++) {
          /** @type {string} */
          n[i] = String.fromCharCode(buf[i]);
        }
        return n.join("");
      }
      /**
       * @param {!Object} buffer
       * @return {?}
       */
      function bufferClone(buffer) {
        if (buffer.slice) {
          return buffer.slice(0);
        }
        /** @type {!Uint8Array} */
        var tmp = new Uint8Array(buffer.byteLength);
        return tmp.set(new Uint8Array(buffer)), tmp.buffer;
      }
      /**
       * @return {?}
       */
      function Body() {
        return this.bodyUsed = false, this._initBody = function(body) {
          if (this._bodyInit = body, body) {
            if ("string" == typeof body) {
              /** @type {string} */
              this._bodyText = body;
            } else {
              if (support.blob && Blob.prototype.isPrototypeOf(body)) {
                /** @type {string} */
                this._bodyBlob = body;
              } else {
                if (support.formData && FormData.prototype.isPrototypeOf(body)) {
                  /** @type {string} */
                  this._bodyFormData = body;
                } else {
                  if (support.searchParams && URLSearchParams.prototype.isPrototypeOf(body)) {
                    this._bodyText = body.toString();
                  } else {
                    if (support.arrayBuffer && support.blob && isDataView(body)) {
                      this._bodyArrayBuffer = bufferClone(body.buffer);
                      /** @type {!Blob} */
                      this._bodyInit = new Blob([this._bodyArrayBuffer]);
                    } else {
                      if (!support.arrayBuffer || !ArrayBuffer.prototype.isPrototypeOf(body) && !isArrayBufferView(body)) {
                        throw new Error("unsupported BodyInit type");
                      }
                      this._bodyArrayBuffer = bufferClone(body);
                    }
                  }
                }
              }
            }
          } else {
            /** @type {string} */
            this._bodyText = "";
          }
          if (!this.headers.get("content-type")) {
            if ("string" == typeof body) {
              this.headers.set("content-type", "text/plain;charset=UTF-8");
            } else {
              if (this._bodyBlob && this._bodyBlob.type) {
                this.headers.set("content-type", this._bodyBlob.type);
              } else {
                if (support.searchParams && URLSearchParams.prototype.isPrototypeOf(body)) {
                  this.headers.set("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
                }
              }
            }
          }
        }, support.blob && (this.blob = function() {
          var rejected = consumed(this);
          if (rejected) {
            return rejected;
          }
          if (this._bodyBlob) {
            return Promise.resolve(this._bodyBlob);
          }
          if (this._bodyArrayBuffer) {
            return Promise.resolve(new Blob([this._bodyArrayBuffer]));
          }
          if (this._bodyFormData) {
            throw new Error("could not read FormData body as blob");
          }
          return Promise.resolve(new Blob([this._bodyText]));
        }, this.arrayBuffer = function() {
          return this._bodyArrayBuffer ? consumed(this) || Promise.resolve(this._bodyArrayBuffer) : this.blob().then(done);
        }), this.text = function() {
          var rejected = consumed(this);
          if (rejected) {
            return rejected;
          }
          if (this._bodyBlob) {
            return readBlobAsText(this._bodyBlob);
          }
          if (this._bodyArrayBuffer) {
            return Promise.resolve(readArrayBufferAsText(this._bodyArrayBuffer));
          }
          if (this._bodyFormData) {
            throw new Error("could not read FormData body as text");
          }
          return Promise.resolve(this._bodyText);
        }, support.formData && (this.formData = function() {
          return this.text().then(decode);
        }), this.json = function() {
          return this.text().then(JSON.parse);
        }, this;
      }
      /**
       * @param {string} method
       * @return {?}
       */
      function normalizeMethod(method) {
        var t = method.toUpperCase();
        return methods.indexOf(t) > -1 ? t : method;
      }
      /**
       * @param {!Object} input
       * @param {!Object} options
       * @return {undefined}
       */
      function Request(input, options) {
        options = options || {};
        var body = options.body;
        if (input instanceof Request) {
          if (input.bodyUsed) {
            throw new TypeError("Already read");
          }
          this.url = input.url;
          this.credentials = input.credentials;
          if (!options.headers) {
            this.headers = new Headers(input.headers);
          }
          this.method = input.method;
          this.mode = input.mode;
          if (!(body || null == input._bodyInit)) {
            body = input._bodyInit;
            /** @type {boolean} */
            input.bodyUsed = true;
          }
        } else {
          /** @type {string} */
          this.url = String(input);
        }
        if (this.credentials = options.credentials || this.credentials || "omit", !options.headers && this.headers || (this.headers = new Headers(options.headers)), this.method = normalizeMethod(options.method || this.method || "GET"), this.mode = options.mode || this.mode || null, this.referrer = null, ("GET" === this.method || "HEAD" === this.method) && body) {
          throw new TypeError("Body not allowed for GET or HEAD requests");
        }
        this._initBody(body);
      }
      /**
       * @param {!Object} a
       * @return {?}
       */
      function decode(a) {
        /** @type {!FormData} */
        var form = new FormData;
        return a.trim().split("&").forEach(function(clusterShardData) {
          if (clusterShardData) {
            var headersAndBody = clusterShardData.split("=");
            var url = headersAndBody.shift().replace(/\+/g, " ");
            var filePath = headersAndBody.join("=").replace(/\+/g, " ");
            form.append(decodeURIComponent(url), decodeURIComponent(filePath));
          }
        }), form;
      }
      /**
       * @param {string} dates
       * @return {?}
       */
      function headers(dates) {
        var headers = new Headers;
        return dates.split(/\r?\n/).forEach(function(clusterShardData) {
          var headersAndBody = clusterShardData.split(":");
          var key = headersAndBody.shift().trim();
          if (key) {
            var value = headersAndBody.join(":").trim();
            headers.append(key, value);
          }
        }), headers;
      }
      /**
       * @param {string} bodyInit
       * @param {!Object} options
       * @return {undefined}
       */
      function Response(bodyInit, options) {
        if (!options) {
          options = {};
        }
        /** @type {string} */
        this.type = "default";
        this.status = "status" in options ? options.status : 200;
        /** @type {boolean} */
        this.ok = this.status >= 200 && this.status < 300;
        this.statusText = "statusText" in options ? options.statusText : "OK";
        this.headers = new Headers(options.headers);
        this.url = options.url || "";
        this._initBody(bodyInit);
      }
      if (!self.fetch) {
        var support = {
          searchParams : "URLSearchParams" in self,
          iterable : "Symbol" in self && "iterator" in Symbol,
          blob : "FileReader" in self && "Blob" in self && function() {
            try {
              return new Blob, true;
            } catch (e) {
              return false;
            }
          }(),
          formData : "FormData" in self,
          arrayBuffer : "ArrayBuffer" in self
        };
        if (support.arrayBuffer) {
          /** @type {!Array} */
          var orderedPaneIds = ["[object Int8Array]", "[object Uint8Array]", "[object Uint8ClampedArray]", "[object Int16Array]", "[object Uint16Array]", "[object Int32Array]", "[object Uint32Array]", "[object Float32Array]", "[object Float64Array]"];
          /**
           * @param {string} obj
           * @return {?}
           */
          var isDataView = function(obj) {
            return obj && DataView.prototype.isPrototypeOf(obj);
          };
          /** @type {function(*): boolean} */
          var isArrayBufferView = ArrayBuffer.isView || function(id) {
            return id && orderedPaneIds.indexOf(Object.prototype.toString.call(id)) > -1;
          };
        }
        /**
         * @param {!Object} name
         * @param {!Object} value
         * @return {undefined}
         */
        Headers.prototype.append = function(name, value) {
          name = normalizeName(name);
          value = normalizeValue(value);
          var oldValue = this.map[name];
          this.map[name] = oldValue ? oldValue + "," + value : value;
        };
        /**
         * @param {string} name
         * @return {undefined}
         */
        Headers.prototype.delete = function(name) {
          delete this.map[normalizeName(name)];
        };
        /**
         * @param {string} name
         * @return {?}
         */
        Headers.prototype.get = function(name) {
          return name = normalizeName(name), this.has(name) ? this.map[name] : null;
        };
        /**
         * @param {string} name
         * @return {?}
         */
        Headers.prototype.has = function(name) {
          return this.map.hasOwnProperty(normalizeName(name));
        };
        /**
         * @param {!Object} name
         * @param {string} value
         * @return {undefined}
         */
        Headers.prototype.set = function(name, value) {
          this.map[normalizeName(name)] = normalizeValue(value);
        };
        /**
         * @param {!Function} callback
         * @param {?} thisObj
         * @return {undefined}
         */
        Headers.prototype.forEach = function(callback, thisObj) {
          var i;
          for (i in this.map) {
            if (this.map.hasOwnProperty(i)) {
              callback.call(thisObj, this.map[i], i, this);
            }
          }
        };
        /**
         * @return {?}
         */
        Headers.prototype.keys = function() {
          /** @type {!Array} */
          var items = [];
          return this.forEach(function(canCreateDiscussions, voicemail) {
            items.push(voicemail);
          }), each(items);
        };
        /**
         * @return {?}
         */
        Headers.prototype.values = function() {
          /** @type {!Array} */
          var items = [];
          return this.forEach(function(voicemail) {
            items.push(voicemail);
          }), each(items);
        };
        /**
         * @return {?}
         */
        Headers.prototype.entries = function() {
          /** @type {!Array} */
          var items = [];
          return this.forEach(function(name, i) {
            items.push([i, name]);
          }), each(items);
        };
        if (support.iterable) {
          /** @type {function(): ?} */
          Headers.prototype[Symbol.iterator] = Headers.prototype.entries;
        }
        /** @type {!Array} */
        var methods = ["DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT"];
        /**
         * @return {?}
         */
        Request.prototype.clone = function() {
          return new Request(this, {
            body : this._bodyInit
          });
        };
        Body.call(Request.prototype);
        Body.call(Response.prototype);
        /**
         * @return {?}
         */
        Response.prototype.clone = function() {
          return new Response(this._bodyInit, {
            status : this.status,
            statusText : this.statusText,
            headers : new Headers(this.headers),
            url : this.url
          });
        };
        /**
         * @return {?}
         */
        Response.error = function() {
          var response = new Response(null, {
            status : 0,
            statusText : ""
          });
          return response.type = "error", response;
        };
        /** @type {!Array} */
        var optForFields = [301, 302, 303, 307, 308];
        /**
         * @param {string} e
         * @param {!Object} name
         * @return {?}
         */
        Response.redirect = function(e, name) {
          if (-1 === optForFields.indexOf(name)) {
            throw new RangeError("Invalid status code");
          }
          return new Response(null, {
            status : name,
            headers : {
              location : e
            }
          });
        };
        /** @type {function(!Object): undefined} */
        self.Headers = Headers;
        /** @type {function(!Object, !Object): undefined} */
        self.Request = Request;
        /** @type {function(string, !Object): undefined} */
        self.Response = Response;
        /**
         * @param {?} method
         * @param {boolean} url
         * @return {?}
         */
        self.fetch = function(method, url) {
          return new Promise(function(resolve, reject) {
            var request = new Request(method, url);
            /** @type {!XMLHttpRequest} */
            var xhr = new XMLHttpRequest;
            /**
             * @return {undefined}
             */
            xhr.onload = function() {
              var options = {
                status : xhr.status,
                statusText : xhr.statusText,
                headers : headers(xhr.getAllResponseHeaders() || "")
              };
              options.url = "responseURL" in xhr ? xhr.responseURL : options.headers.get("X-Request-URL");
              /** @type {(Object|null|string)} */
              var tres = "response" in xhr ? xhr.response : xhr.responseText;
              resolve(new Response(tres, options));
            };
            /**
             * @return {undefined}
             */
            xhr.onerror = function() {
              reject(new TypeError("Network request failed"));
            };
            /**
             * @return {undefined}
             */
            xhr.ontimeout = function() {
              reject(new TypeError("Network request failed"));
            };
            xhr.open(request.method, request.url, true);
            if ("include" === request.credentials) {
              /** @type {boolean} */
              xhr.withCredentials = true;
            }
            if ("responseType" in xhr && support.blob) {
              /** @type {string} */
              xhr.responseType = "blob";
            }
            request.headers.forEach(function(type, i) {
              xhr.setRequestHeader(i, type);
            });
            xhr.send(void 0 === request._bodyInit ? null : request._bodyInit);
          });
        };
        /** @type {boolean} */
        self.fetch.polyfill = true;
      }
    }("undefined" != typeof self ? self : this);
  },
  X3Bo : function(module, exports, __webpack_require__) {
    __webpack_require__("+LfV");
    module.exports = __webpack_require__("qGgm").Object.keys;
  },
  XMdZ : function(blob, id, require) {
    var utils = require("6uqe");
    var formats = require("tF0L");
    var arrayPrefixGenerators = {
      brackets : function(prefix) {
        return prefix + "[]";
      },
      indices : function(key, prefix) {
        return key + "[" + prefix + "]";
      },
      repeat : function(s) {
        return s;
      }
    };
    /** @type {function(this:Date): string} */
    var toISO = Date.prototype.toISOString;
    var defaults = {
      delimiter : "&",
      encode : true,
      encoder : utils.encode,
      encodeValuesOnly : false,
      serializeDate : function(date) {
        return toISO.call(date);
      },
      skipNulls : false,
      strictNullHandling : false
    };
    /**
     * @param {?} value
     * @param {string} prefix
     * @param {?} generateArrayPrefix
     * @param {string} strictNullHandling
     * @param {boolean} skipNulls
     * @param {boolean} encoder
     * @param {!Object} filter
     * @param {!Function} sort
     * @param {string} allowDots
     * @param {!Function} serializeDate
     * @param {?} formatter
     * @param {string} encodeValuesOnly
     * @return {?}
     */
    var stringify = function stringify(value, prefix, generateArrayPrefix, strictNullHandling, skipNulls, encoder, filter, sort, allowDots, serializeDate, formatter, encodeValuesOnly) {
      var obj = value;
      if ("function" == typeof filter) {
        obj = filter(prefix, obj);
      } else {
        if (obj instanceof Date) {
          obj = serializeDate(obj);
        } else {
          if (null === obj) {
            if (strictNullHandling) {
              return encoder && !encodeValuesOnly ? encoder(prefix, defaults.encoder) : prefix;
            }
            /** @type {string} */
            obj = "";
          }
        }
      }
      if ("string" == typeof obj || "number" == typeof obj || "boolean" == typeof obj || utils.isBuffer(obj)) {
        if (encoder) {
          return [formatter(encodeValuesOnly ? prefix : encoder(prefix, defaults.encoder)) + "=" + formatter(encoder(obj, defaults.encoder))];
        }
        return [formatter(prefix) + "=" + formatter(String(obj))];
      }
      /** @type {!Array} */
      var values = [];
      if (void 0 === obj) {
        return values;
      }
      var objKeys;
      if (Array.isArray(filter)) {
        /** @type {!Object} */
        objKeys = filter;
      } else {
        /** @type {!Array<string>} */
        var keys = Object.keys(obj);
        /** @type {!Array<string>} */
        objKeys = sort ? keys.sort(sort) : keys;
      }
      /** @type {number} */
      var i = 0;
      for (; i < objKeys.length; ++i) {
        var key = objKeys[i];
        if (!(skipNulls && null === obj[key])) {
          /** @type {!Array<?>} */
          values = Array.isArray(obj) ? values.concat(stringify(obj[key], generateArrayPrefix(prefix, key), generateArrayPrefix, strictNullHandling, skipNulls, encoder, filter, sort, allowDots, serializeDate, formatter, encodeValuesOnly)) : values.concat(stringify(obj[key], prefix + (allowDots ? "." + key : "[" + key + "]"), generateArrayPrefix, strictNullHandling, skipNulls, encoder, filter, sort, allowDots, serializeDate, formatter, encodeValuesOnly));
        }
      }
      return values;
    };
    /**
     * @param {!Object} name
     * @param {string} obj
     * @return {?}
     */
    blob.exports = function(name, obj) {
      /** @type {!Object} */
      var value = name;
      var options = obj ? utils.assign({}, obj) : {};
      if (null !== options.encoder && void 0 !== options.encoder && "function" != typeof options.encoder) {
        throw new TypeError("Encoder has to be a function.");
      }
      var delimiter = void 0 === options.delimiter ? defaults.delimiter : options.delimiter;
      /** @type {boolean} */
      var strictNullHandling = "boolean" == typeof options.strictNullHandling ? options.strictNullHandling : defaults.strictNullHandling;
      /** @type {boolean} */
      var skipNulls = "boolean" == typeof options.skipNulls ? options.skipNulls : defaults.skipNulls;
      /** @type {boolean} */
      var encode = "boolean" == typeof options.encode ? options.encode : defaults.encode;
      var encoder = "function" == typeof options.encoder ? options.encoder : defaults.encoder;
      /** @type {(!Function|null)} */
      var sort = "function" == typeof options.sort ? options.sort : null;
      var allowDots = void 0 !== options.allowDots && options.allowDots;
      /** @type {!Function} */
      var serializeDate = "function" == typeof options.serializeDate ? options.serializeDate : defaults.serializeDate;
      /** @type {boolean} */
      var encodeValuesOnly = "boolean" == typeof options.encodeValuesOnly ? options.encodeValuesOnly : defaults.encodeValuesOnly;
      if (void 0 === options.format) {
        options.format = formats.default;
      } else {
        if (!Object.prototype.hasOwnProperty.call(formats.formatters, options.format)) {
          throw new TypeError("Unknown format option provided.");
        }
      }
      var objKeys;
      var filter;
      var formatter = formats.formatters[options.format];
      if ("function" == typeof options.filter) {
        /** @type {!Function} */
        filter = options.filter;
        value = filter("", value);
      } else {
        if (Array.isArray(options.filter)) {
          filter = options.filter;
          objKeys = filter;
        }
      }
      /** @type {!Array} */
      var keys = [];
      if ("object" != typeof value || null === value) {
        return "";
      }
      var arrayFormat;
      arrayFormat = options.arrayFormat in arrayPrefixGenerators ? options.arrayFormat : "indices" in options ? options.indices ? "indices" : "repeat" : "indices";
      var generateArrayPrefix = arrayPrefixGenerators[arrayFormat];
      if (!objKeys) {
        /** @type {!Array<string>} */
        objKeys = Object.keys(value);
      }
      if (sort) {
        objKeys.sort(sort);
      }
      /** @type {number} */
      var i = 0;
      for (; i < objKeys.length; ++i) {
        /** @type {string} */
        var key = objKeys[i];
        if (!(skipNulls && null === value[key])) {
          /** @type {!Array<?>} */
          keys = keys.concat(stringify(value[key], key, generateArrayPrefix, strictNullHandling, skipNulls, encode ? encoder : null, filter, sort, allowDots, serializeDate, formatter, encodeValuesOnly));
        }
      }
      /** @type {string} */
      var index = keys.join(delimiter);
      /** @type {string} */
      var controlsCount = true === options.addQueryPrefix ? "?" : "";
      return index.length > 0 ? controlsCount + index : "";
    };
  },
  "XX4+" : function(module, selector, convertToImages) {
    /**
     * @param {!Object} name
     * @return {?}
     */
    function r(name) {
      return null !== name && "object" == typeof name;
    }
    /** @type {function(!Object): ?} */
    module.exports = r;
  },
  Xamz : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _AboutPage = __webpack_require__("mRYa");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _AppDownload = __webpack_require__("IJ1K");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _UiRippleInk = __webpack_require__("GF8f");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _deepAssign = __webpack_require__("YWnE");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _buildPageNumber = __webpack_require__("lxt5");
    var _buildPageNumber2 = _interopRequireDefault(_buildPageNumber);
    var storeMixin = function(e) {
      /**
       * @param {?} props
       * @return {?}
       */
      function ReflexElement(props) {
        (0, _UiIcon2.default)(this, ReflexElement);
        var localTask = (0, _AboutPage2.default)(this, (ReflexElement.__proto__ || (0, _normalizeDataUri2.default)(ReflexElement)).call(this, props));
        return localTask.state = {
          showMsg : false
        }, localTask;
      }
      return (0, _AppDownload2.default)(ReflexElement, e), (0, _classlist2.default)(ReflexElement, [{
        key : "appendPopBanner",
        value : function() {
          var e = this;
          _UiRippleInk2.default.unstable_renderSubtreeIntoContainer(this, _prepareStyleProperties2.default.createElement(_buildPageNumber2.default, {
            handleClose : function() {
              e.handleCloseClick();
            }
          }), this.container);
        }
      }, {
        key : "componentDidMount",
        value : function() {
          if (!_deepAssign2.default.getCookieForLocal("show_msg")) {
            this.setState({
              showMsg : true
            });
          }
        }
      }, {
        key : "createContainerElement",
        value : function() {
          /** @type {!Element} */
          this.container = document.createElement("div");
          document.body.appendChild(this.container);
        }
      }, {
        key : "onMsgClick",
        value : function() {
          this.setState({
            showMsg : false
          });
          _deepAssign2.default.setCookieForLocal("show_msg", true, 864E5);
          window.maevent("left_button", "click");
          this.createContainerElement();
          this.appendPopBanner();
        }
      }, {
        key : "handleCloseClick",
        value : function() {
          document.body.removeChild(this.container);
        }
      }, {
        key : "render",
        value : function() {
          var e = this;
          return _prepareStyleProperties2.default.createElement("a", {
            href : "javascript:;",
            className : "msg-box",
            onClick : function() {
              return e.onMsgClick();
            }
          }, this.state.showMsg && _prepareStyleProperties2.default.createElement("div", {
            className : "circle"
          }));
        }
      }]), ReflexElement;
    }(_prepareStyleProperties.Component);
    mixin.exports = storeMixin;
  },
  XgqU : function(module, exports, __webpack_require__) {
    var $export = __webpack_require__("K0Kg");
    $export($export.S + $export.F, "Object", {
      assign : __webpack_require__("JBQp")
    });
  },
  YNWe : function(formatters, customFormatters) {
  },
  YWnE : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    /**
     * @return {?}
     */
    function thumb_click() {
      try {
        return localStorage.setItem("test", "test"), localStorage.removeItem("test"), true;
      } catch (e) {
        return false;
      }
    }
    /**
     * @param {string} undefined
     * @return {?}
     */
    function log(undefined) {
      var key;
      for (key in localStorage) {
        /** @type {!Array<string>} */
        var splits = key.split("___");
        if (3 === splits.length && splits[0] === undefined) {
          /** @type {number} */
          var half_rows = parseInt(splits[1]);
          /** @type {number} */
          var _matrix_rows = parseInt(splits[2]);
          if (Date.now() - half_rows < _matrix_rows) {
            return localStorage[key];
          }
        }
      }
      return null;
    }
    /**
     * @param {string} id
     * @param {boolean} level
     * @param {number} i
     * @return {undefined}
     */
    function update(id, level, i) {
      var key;
      for (key in localStorage) {
        if (key.split("__")[0] === id) {
          localStorage.removeItem(key);
        }
      }
      /** @type {boolean} */
      localStorage[id + "___" + Date.now() + "___" + i] = level;
    }
    /**
     * @param {string} value
     * @param {string} i
     * @return {?}
     */
    function _appendQueryParam(value, i) {
      if (!i) {
        return value;
      }
      var s;
      /** @type {!Element} */
      var o = document.createElement("a");
      return o.href = value, s = o.search ? o.search + "&" + i : "?" + i, o.protocol + "//" + o.host + o.pathname + s + o.hash;
    }
    /**
     * @param {string} key
     * @return {?}
     */
    function init(key) {
      /** @type {string} */
      var s = location.search;
      /** @type {!Array<string>} */
      var tilesToCheck = s.substring(1).split("&");
      var methods = {};
      /** @type {number} */
      var i = 0;
      /** @type {number} */
      var len = tilesToCheck.length;
      for (; i < len; i++) {
        /** @type {string} */
        var t = tilesToCheck[i];
        if (t) {
          /** @type {string} */
          methods[t.substring(0, t.indexOf("=")).toLowerCase()] = t.substring(t.indexOf("=") + 1, t.length);
        }
      }
      if (!key) {
        return methods;
      }
      var value = methods[key.toLowerCase()];
      return value ? value.trim() : "";
    }
    /**
     * @return {?}
     */
    function hash() {
      /** @type {string} */
      var componentsStr = location.hash.substr(1);
      var options = {};
      if (componentsStr) {
        /** @type {!Array<string>} */
        var strCookies = componentsStr.split("&");
        /** @type {number} */
        var i = 0;
        for (; i < strCookies.length; i++) {
          /** @type {!Array<string>} */
          var spltdt = strCookies[i].split("=");
          /** @type {string} */
          options[spltdt[0]] = spltdt[1];
        }
      }
      if ("string" == typeof arguments[0]) {
        return options[arguments[0]];
      }
      if ("object" === (0, _UiIcon2.default)(arguments[0])) {
        var prop;
        for (prop in arguments[0]) {
          options[prop] = arguments[0][prop];
        }
        var micropost = (0, _normalizeDataUri2.default)(options).map(function(cleanMe) {
          return "h=" + options[cleanMe];
        }).join("&");
        location.href = "#" + micropost.substring(0, micropost.length - 1);
      }
    }
    /**
     * @return {?}
     */
    function _initSys() {
      /** @type {string} */
      var scriptCursorIndex = "Other";
      /** @type {string} */
      var ua = window.navigator.userAgent;
      var platforms = {
        Wechat : /micromessenger/,
        QQBrowser : /qqbrowser/,
        UC : /ubrowser|ucbrowser|ucweb/,
        Shoujibaidu : /baiduboxapp|baiduhd|bidubrowser|baidubrowser/,
        SamsungBrowser : /samsungbrowser/,
        MiuiBrowser : /miuibrowser/,
        Sogou : /sogoumobilebrowser|sogousearch/,
        Explorer2345 : /2345explorer|2345chrome|mb2345browser/,
        Liebao : /lbbrowser/,
        Weibo : /__weibo__/,
        OPPO : /oppobrowser/,
        toutiao : /newsarticle/,
        MobileQQ : /mobile.*qq/,
        Firefox : /firefox/,
        Maxthon : /maxthon/,
        Se360 : /360se/,
        Ee360 : /360ee/,
        Safari : /(iphone|ipad).*version.*mobile.*safari/,
        Chrome : /chrome|crios/,
        AndroidBrowser : /android.*safari|android.*release.*browser/
      };
      var index;
      for (index in platforms) {
        if (platforms[index].exec(ua.toLowerCase())) {
          /** @type {string} */
          scriptCursorIndex = index;
          break;
        }
      }
      return scriptCursorIndex;
    }
    /**
     * @param {!NodeList} message
     * @return {?}
     */
    function preprocessLiteral(message) {
      return (0, _normalizeDataUri2.default)(message).map(function(description) {
        return [description, message[description]].join("=");
      }).join("&");
    }
    /**
     * @param {!Object} script
     * @return {?}
     */
    function defaultStateParser(script) {
      return JSON.parse((0, _prepareStyleProperties2.default)(script));
    }
    var _prepareStyleProperties = __webpack_require__("p7ii");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _normalizeDataUri = __webpack_require__("mZJ8");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("gf5I");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    /**
     * @param {string} key
     * @param {number} value
     * @param {!Object} options
     * @return {?}
     */
    var cookie = function(key, value, options) {
      if (void 0 === value) {
        /** @type {null} */
        var cookieValue = null;
        if (document.cookie && "" !== document.cookie) {
          /** @type {!Array<string>} */
          var termFragments = document.cookie.split(";");
          /** @type {number} */
          var i = 0;
          for (; i < termFragments.length; i++) {
            /** @type {string} */
            var diffUnnormalized = termFragments[i].trim();
            if (diffUnnormalized.substring(0, key.length + 1) === key + "=") {
              /** @type {string} */
              cookieValue = decodeURIComponent(diffUnnormalized.substring(key.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
      options = options || {};
      if (null === value) {
        /** @type {string} */
        value = "";
        /** @type {number} */
        options.expires = -1;
      }
      /** @type {string} */
      var CanonicalHeaders = "";
      if (options.expires && ("number" == typeof options.expires || options.expires.toUTCString)) {
        var date;
        if ("number" == typeof options.expires) {
          /** @type {!Date} */
          date = new Date;
          date.setTime(date.getTime() + options.expires);
        } else {
          date = options.expires;
        }
        CanonicalHeaders = "; expires=" + date.toUTCString();
      }
      /** @type {string} */
      var flipYPart = options.path ? "; path=" + options.path : "";
      /** @type {string} */
      var inlineClass = options.domain ? "; domain=" + options.domain : "";
      /** @type {string} */
      var dataAttributes = options.secure ? "; secure" : "";
      /** @type {string} */
      document.cookie = [key, "=", encodeURIComponent(value), CanonicalHeaders, flipYPart, inlineClass, dataAttributes].join("");
    };
    var node = {
      vendor : function() {
        /** @type {!Array} */
        var prefixes = ["O", "ms", "Moz", "Khtml", "Webkit", "webkit", ""];
        /** @type {!Element} */
        var lineGuide = document.createElement("div");
        /** @type {number} */
        var i = prefixes.length;
        for (; i--;) {
          var prefix = prefixes[i];
          if ((prefix ? prefix + "Transform" : "transform") in lineGuide.style) {
            return prefix;
          }
        }
        return null;
      },
      prefix : function(name, value) {
        if (null !== node.vendor()) {
          /** @type {string} */
          var opt_by = node.vendor() ? "-" + node.vendor().toLowerCase() + "-" : "";
          var getdate = node.vendor() || "";
          if (value) {
            return opt_by + name.replace(/([A-Z])/g, function(p_Interval, canCreateDiscussions) {
              return "-" + p_Interval.toLowerCase();
            });
          }
          return getdate + ("" !== node.vendor() ? name.charAt(0).toUpperCase() + name.substr(1) : name).replace(/(-[a-z])/g, function(hashComponent, canCreateDiscussions) {
            return hashComponent.charAt(1).toUpperCase();
          });
        }
      },
      canRun2d : function() {
        return null !== node.vendor();
      },
      canRun3d : function() {
        /** @type {!Element} */
        var e = document.createElement("div");
        if (!node.canRun2d() || !window.getComputedStyle) {
          return false;
        }
        var x = node.prefix("transform");
        document.body.appendChild(e);
        /** @type {string} */
        e.style[x] = "translate3d(1px,1px,1px)";
        var n = window.getComputedStyle(e)[x] || "";
        return document.body.removeChild(e), !!/^matrix3d\((.*)\)$/.exec(n);
      },
      canRunCanvas : function() {
        var chatCanvas;
        try {
          return chatCanvas = document.createElement("canvas"), chatCanvas.getContext("2d"), true;
        } catch (e) {
          return false;
        }
      },
      canRunWebgl : function() {
        var canvas;
        var ctx;
        try {
          return canvas = document.createElement("canvas"), ctx = canvas.getContext("webgl") || canvas.getContext("experimental-webgl"), ctx.getSupportedExtensions(), true;
        } catch (e) {
          return false;
        }
      },
      canUsePageVisibility : function() {
        return null !== node.vendor() && void 0 !== document[node.prefix("hidden")];
      }
    };
    /**
     * @return {?}
     */
    var map = function() {
      return node.canUsePageVisibility() ? document[node.prefix("hidden")] ? "hidden" : "visible" : "unknown";
    };
    module.exports = {
      cookie : cookie,
      support : node,
      pageVisible : map,
      localStorageEnabled : thumb_click,
      getCookieForLocal : log,
      setCookieForLocal : update,
      appendQuery : _appendQueryParam,
      request : init,
      hash : hash,
      getBrowserName : _initSys,
      toQuery : preprocessLiteral,
      cloneDeep : defaultStateParser
    };
  },
  "Yyv+" : function(formatters, customFormatters) {
  },
  ZD21 : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    Object.defineProperty(exports, "__esModule", {
      value : true
    });
    var _UiIcon = __webpack_require__("iltz");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("fvPU");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _deepAssign = __webpack_require__("hJ6a");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _UiRippleInk = __webpack_require__("mRYa");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _AboutPage = __webpack_require__("IJ1K");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    var _AppDownload = __webpack_require__("Cqu5");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    __webpack_require__("DiDM");
    var ReactSwipe = function(e) {
      /**
       * @param {?} props
       * @return {?}
       */
      function ReflexElement(props) {
        (0, _classlist2.default)(this, ReflexElement);
        var localTask = (0, _UiRippleInk2.default)(this, (ReflexElement.__proto__ || (0, _UiIcon2.default)(ReflexElement)).call(this, props));
        return localTask.state = {
          rotateRefreshBtn : props.rotateRefreshBtn || false
        }, localTask;
      }
      return (0, _AboutPage2.default)(ReflexElement, e), (0, _deepAssign2.default)(ReflexElement, [{
        key : "componentWillReceiveProps",
        value : function(name) {
          this.setState({
            rotateRefreshBtn : name.rotateRefreshBtn
          });
        }
      }, {
        key : "onRefreshBtnClick",
        value : function() {
          var boilerStateMachine = this;
          this.setState({
            rotateRefreshBtn : true
          });
          setTimeout(function() {
            boilerStateMachine.setState({
              rotateRefreshBtn : false
            });
          }, 1E3);
          if (this.props.onRefreshClick) {
            this.props.onRefreshClick();
          }
        }
      }, {
        key : "render",
        value : function() {
          var e = this;
          var customCls = this.props.className || "";
          var langClass = (0, _AppDownload2.default)("refresh_btn", {
            rotate : this.state.rotateRefreshBtn
          });
          return _prepareStyleProperties2.default.createElement("div", {
            className : "refreshBtn-container " + customCls,
            onClick : function() {
              return e.onRefreshBtnClick();
            }
          }, _prepareStyleProperties2.default.createElement("i", {
            className : langClass
          }));
        }
      }]), ReflexElement;
    }(_prepareStyleProperties.Component);
    ReactSwipe.propTypes = {
      onRefreshClick : _propTypes2.default.func,
      rotateRefreshBtn : _propTypes2.default.bool,
      className : _propTypes2.default.string
    };
    exports.default = ReactSwipe;
  },
  aZsa : function(module, object, instantiate) {
    module.exports = instantiate("uGEv");
  },
  afpQ : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _deepAssign = __webpack_require__("mRYa");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _AboutPage = __webpack_require__("IJ1K");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    var _AppDownload = __webpack_require__("J5EE");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var _noframeworkWaypoints = __webpack_require__("Cqu5");
    var _noframeworkWaypoints2 = _interopRequireDefault(_noframeworkWaypoints);
    var hash = __webpack_require__("H1Va");
    /**
     * @param {?} options
     * @return {?}
     */
    var render = function(options) {
      var data = options.datum;
      var langClass = (0, _noframeworkWaypoints2.default)("dotdot", "line3", {
        "image-margin-right" : data.middle_mode
      });
      var val = (0, _noframeworkWaypoints2.default)("src", "space", {
        recommend_label : "\u767e\u5ea6\u7ecf\u9a8c" === data.source
      });
      var ans1 = (0, _noframeworkWaypoints2.default)("dislike-news", "fr", {
        "mid-space" : data.middle_mode
      });
      var valueClassName = (0, _noframeworkWaypoints2.default)("item_detail", {
        desc : data.middle_mode
      });
      return _prepareStyleProperties2.default.createElement("a", {
        href : "javascript: void(0)",
        "data-action-label" : data.action_label,
        "data-tag" : data.tag,
        className : "article_link clearfix "
      }, _prepareStyleProperties2.default.createElement("div", {
        className : valueClassName
      }, _prepareStyleProperties2.default.createElement("h3", {
        className : langClass
      }, data.title), data.more_mode && _prepareStyleProperties2.default.createElement("div", {
        className : "list_image"
      }, _prepareStyleProperties2.default.createElement("ul", {
        className : "clearfix"
      }, data.image_list.map(function(smiley, awsKey) {
        return _prepareStyleProperties2.default.createElement("li", {
          key : awsKey,
          className : "list_img_holder"
        }, _prepareStyleProperties2.default.createElement(_AppDownload2.default, {
          src : smiley.url
        }));
      }))), data.large_mode && _prepareStyleProperties2.default.createElement("div", {
        className : "list_img_holder_large list_img_holder_large_fix"
      }, _prepareStyleProperties2.default.createElement(_AppDownload2.default, {
        src : data.large_image_url
      }), data.has_video && _prepareStyleProperties2.default.createElement("span", {
        className : "video-btn"
      })), _prepareStyleProperties2.default.createElement("div", {
        className : "item_info"
      }, _prepareStyleProperties2.default.createElement("div", null, data.is_stick && _prepareStyleProperties2.default.createElement("span", {
        className : "stick_label space"
      }, data.label || "\u7f6e\u9876"), data.hot && _prepareStyleProperties2.default.createElement("span", {
        className : "hot_label space"
      }, "\u70ed"), data.recommend && _prepareStyleProperties2.default.createElement("span", {
        className : "recommend_label space"
      }, "\u8350"), data.subject_label && _prepareStyleProperties2.default.createElement("span", {
        className : "subject_label"
      }, " ", data.subject_label), !data.subject_label && _prepareStyleProperties2.default.createElement("span", {
        className : val
      }, data.source), _prepareStyleProperties2.default.createElement("span", {
        className : "cmt space"
      }, "\u8bc4\u8bba ", data.comment_count), !data.middle_mode && _prepareStyleProperties2.default.createElement("span", {
        className : "time",
        title : data.datetime
      }, data.timeago), _prepareStyleProperties2.default.createElement("span", {
        "data-id" : data.group_id,
        className : ans1
      })))), data.middle_mode && _prepareStyleProperties2.default.createElement("div", {
        className : "list_img_holder"
      }, _prepareStyleProperties2.default.createElement(_AppDownload2.default, {
        src : data.image_url
      }), data.has_video && _prepareStyleProperties2.default.createElement("span", {
        className : "video-btn"
      })));
    };
    render.propTypes = {
      datum : _propTypes2.default.object
    };
    var PercentageSymbol = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _UiIcon2.default)(this, Agent), (0, _deepAssign2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).apply(this, arguments));
      }
      return (0, _AboutPage2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "handleClick",
        value : function(value) {
          window.maevent("feed", this.props.currentChannel, "click-" + value.index);
          (0, hash.actionLog)({
            label : value.action_label,
            value : value.group_id,
            extra_data : {
              item_id : value.item_id || 0
            }
          });
          location.href = value.source_url;
        }
      }, {
        key : "render",
        value : function() {
          var proto = this;
          var options = this.props.datum;
          if (options.has_video) {
            /** @type {boolean} */
            options.large_mode = false;
            /** @type {boolean} */
            options.middle_mode = true;
            options.image_url = options.image_url || options.large_image_url;
            if (!(options.image_url && options.large_image_url)) {
              /** @type {boolean} */
              options.middle_mode = false;
            }
          }
          var langClass = (0, _noframeworkWaypoints2.default)({
            middle_mode : options.middle_mode,
            has_action : true,
            "item-hidden" : options.honey
          });
          return _prepareStyleProperties2.default.createElement("section", {
            className : langClass,
            "data-hot-time" : options.behot_time,
            "data-group-id" : options.group_id,
            "data-item-id" : options.item_id,
            "data-format" : "0",
            onClick : function() {
              return proto.handleClick(options);
            }
          }, _prepareStyleProperties2.default.createElement(render, {
            datum : options
          }));
        }
      }]), Agent;
    }(_prepareStyleProperties.Component);
    PercentageSymbol.propTypes = {
      datum : _propTypes2.default.object,
      currentChannel : _propTypes2.default.string
    };
    module.exports = PercentageSymbol;
  },
  bChP : function(module, data, callback) {
    /**
     * @return {undefined}
     */
    function YM() {
    }
    /**
     * @param {string} e
     * @return {undefined}
     */
    function init(e) {
      !function(data, doc, id, addedRenderer, isIron, i) {
        /** @type {string} */
        data.ToutiaoAnalyticsObject = id;
        data[id] = data[id] || function() {
          (data[id].q = data[id].q || []).push(arguments);
        };
        /** @type {number} */
        data[id].t = 1 * new Date;
        /** @type {string} */
        data[id].s = "";
        /** @type {string} */
        data[id].i = i;
        /** @type {!Element} */
        var node = doc.createElement("script");
        if (node.async = 1, node.src = "//s3.bytecdn.cn/ta/resource/v0/analytics.js?v=0.1.15", doc.getElementsByTagName("head")[0].appendChild(node), i) {
          /** @type {!Element} */
          var layer = document.createElement("iframe");
          /** @type {string} */
          layer.style.display = "none";
          /** @type {string} */
          layer.id = "bytedance-ba-cid-iframe";
          layer.addEventListener("load", function() {
            /** @type {boolean} */
            this.loaded = true;
          }, false);
          /** @type {string} */
          layer.src = i;
          document.getElementsByTagName("body")[0].appendChild(layer);
        }
      }(window, document, "ba", 0, 0, "//s3.bytecdn.cn/ta/resource/v0/crossDomain.html?v=0.1.15");
      window.ba("create", e, {
        crossDomain : true
      });
      window.ba("send", "pageview");
    }
    /**
     * @param {string} category
     * @param {string} type
     * @param {!Object} label
     * @param {number} path
     * @param {?} msg
     * @return {undefined}
     */
    function noteEvent(category, type, label, path, msg) {
      console.log("ba:" + category + "," + type + "," + label);
      window.ba("send", "event", {
        eventCategory : category,
        eventAction : type,
        eventLabel : label
      });
    }
    /**
     * @return {undefined}
     */
    function handleInit() {
      init(yargs.default.browser.weixin ? "941fa8db85144e" : "2016b6cb651225");
      /** @type {function(string, string, !Object, number, ?): undefined} */
      window.baevent = noteEvent;
    }
    var fields = callback("gT+X");
    var yargs = function(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }(fields);
    /** @type {function(): undefined} */
    window.baevent = YM;
    /** @type {function(): undefined} */
    window.baeventTest = YM;
    /** @type {function(): undefined} */
    window.resendBA = YM;
    module.exports = {
      init : handleInit
    };
  },
  "bF+g" : function(module, exports, __webpack_require__) {
    var $export = __webpack_require__("K0Kg");
    $export($export.S + $export.F * !__webpack_require__("n/J0"), "Object", {
      defineProperty : __webpack_require__("cuVL").f
    });
  },
  bVOP : function(module, exports, __webpack_require__) {
    (function($) {
      /**
       * @param {!Object} obj
       * @return {?}
       */
      function _interopRequireDefault(obj) {
        return obj && obj.__esModule ? obj : {
          default : obj
        };
      }
      /**
       * @return {?}
       */
      function write() {
        var x = _prepareStyleProperties2.default.cookie("tt_webid");
        return x ? parseInt(x).toString() === x ? x : parseInt(x / Math.pow(2, 32)).toString() : null;
      }
      /**
       * @return {undefined}
       */
      function go() {
        window.scrollTo(0, 0);
      }
      /**
       * @return {?}
       */
      function searchRelativePath() {
        if (!_deepAssign2.default.browser.weixin) {
          return false;
        }
        /** @type {number} */
        var e = _prepareStyleProperties2.default.request("isappinstalled") - 0;
        var name = _prepareStyleProperties2.default.request("wxshare_count");
        return !(!e || name && !(name < 2));
      }
      /**
       * @param {string} cmd
       * @return {?}
       */
      function isChangeDirectory(cmd) {
        return cmd.match(/https?:\/\/(m\.)?toutiao\.com\/[a|i](\d+)/i);
      }
      /**
       * @param {string} key
       * @param {number} value
       * @return {?}
       */
      function propertyStringReplacer(key, value) {
        if (value = void 0 !== value && value, window.ttGTM) {
          /** @type {null} */
          var dict = null;
          return dict = window.isListPage ? window.ttGTM.list : _deepAssign2.default.browser.weixin ? window.ttGTM.weixin : window.ttGTM.detail, dict = dict || {}, key in dict ? dict[key] : value;
        }
        return value;
      }
      /**
       * @param {string} data
       * @param {?} path
       * @return {?}
       */
      function getParam(data, path) {
        if (data && "?" !== data[0]) {
          /** @type {string} */
          data = "?" + data;
        }
        var q;
        var b;
        return q = new RegExp("[\\?&]" + encodeURIComponent(path) + "=([^&#]*)"), b = q.exec(data), null === b ? "" : decodeURIComponent(b[1].replace(/\+/g, " "));
      }
      /**
       * @param {!Object} options
       * @return {?}
       */
      function init(options) {
        var name;
        var cachedConfigList = {
          joke_essay : 5,
          news_article : 14,
          news_article_social : 20,
          joke_essay_social : 21,
          saying_essay_social : 22,
          explore_article : 25,
          joke_zone : 27,
          toutiaoribao : 118
        };
        var i = options.app || _prepareStyleProperties2.default.request("app") || "news_article";
        /** @type {number} */
        var group = 1;
        return _deepAssign2.default.os.android && (group = 3), i.length ? (name = cachedConfigList[i], 21 !== name && 24 !== name || (name = 5), 22 === name && (name = 9), 20 === name && 3 === group && (name = 14), "snssdk" + name + group + "://") : "";
      }
      /**
       * @param {!Object} options
       * @return {?}
       */
      function render(options) {
        /**
         * @param {string} data
         * @param {!Object} val
         * @return {?}
         */
        function t(data, val) {
          /** @type {null} */
          var key = null;
          return val && val.isNewVideo && (key = 64), key && (data = data + ("&flags=" + key)), data;
        }
        var key = init(options);
        var i = options.gdLabel || "click_weixin_home";
        var type = options.type || "home";
        var ns = options.id;
        /** @type {string} */
        var x = "";
        switch(type) {
          case "detail":
            /** @type {string} */
            x = key + "detail?groupid=" + ns + "&gd_label=" + i;
            key = t(x, options);
            break;
          case "comment":
            x = key + "detail?groupid=" + ns + "&showcomment=1&gd_label=" + i + "&gd_ext_json=" + (0, _normalizeDataUri2.default)({
              enter_comment : i
            });
            key = t(x, options);
            break;
          case "mediaProfile":
            x = key + "media_account?media_id=" + ns + "&gd_ext_json=" + (0, _normalizeDataUri2.default)({
              event : "pgc_profile",
              label : i
            });
            break;
          case "home":
            x = key + "home/news?growth_from=" + i + "&gd_ext_json=" + (0, _normalizeDataUri2.default)({
              event : "home",
              label : i
            });
        }
        return x = x + "&needlaunchlog=1";
      }
      /**
       * @param {string} key
       * @return {?}
       */
      function setAttribute(key) {
        return _prepareStyleProperties2.default.cookie(key) || _prepareStyleProperties2.default.request(key) || "";
      }
      /**
       * @return {?}
       */
      function resize() {
        return {
          __type__ : "app_track",
          resolution : window.screen.availWidth * window.devicePixelRatio + "*" + window.screen.availHeight * window.devicePixelRatio,
          webid : write() || "",
          utm_source : setAttribute("utm_source")
        };
      }
      /**
       * @param {!Array} fnArgs
       * @return {?}
       */
      function c(fnArgs) {
        /**
         * @param {number} i
         * @return {?}
         */
        var f = function(i) {
          /** @type {!Array} */
          var t = [];
          /** @type {number} */
          var whichFriend = 0;
          for (; whichFriend < i; whichFriend++) {
            /** @type {string} */
            var r = String.fromCharCode(Math.floor(26 * Math.random()) + 65);
            if (Math.ceil(10 * Math.random()) % 2 == 1) {
              /** @type {string} */
              r = r.toLowerCase();
            }
            t.push(r);
          }
          return t.join("");
        };
        /**
         * @return {?}
         */
        var d = function() {
          return Math.ceil(15 * Math.random());
        };
        var v = {};
        return fnArgs.forEach(function(n) {
          var o = f(d()) + f(d());
          v[n] = o;
        }), {
          map : v
        };
      }
      /**
       * @return {undefined}
       */
      function Ellipsis() {
        /**
         * @param {!Object} instance
         * @return {undefined}
         */
        function resize(instance) {
          /** @type {number} */
          var documentHeight = document.body.scrollHeight;
          if ((window.scrollY || window.pageYOffset || document.body.scrollTop || document.documentElement.scrollTop) >= documentHeight - window.innerHeight - scrollOffset) {
            $(window).trigger("scrollBottom", instance.type);
          }
          if ("scroll" === instance.type) {
            if (_takingTooLongTimeout) {
              clearTimeout(_takingTooLongTimeout);
            }
            /** @type {number} */
            _takingTooLongTimeout = setTimeout(function() {
              $(window).trigger("scrollEnd");
            }, 300);
          }
        }
        var _takingTooLongTimeout;
        /** @type {number} */
        var scrollOffset = 100 * (window.responsive || {
          dpr : 1
        }).dpr;
        $(window).on("scroll load afterflow", resize);
      }
      /**
       * @return {?}
       */
      function v() {
        var w = write();
        /** @type {(number|undefined)} */
        var t = null !== w ? parseInt(w) % 10 : void 0;
        return [1, 2].indexOf(t) > -1 && t;
      }
      /**
       * @param {string} endpoint
       * @return {?}
       */
      function post(endpoint) {
        return fetch(endpoint).then(function(data) {
          return data;
        }, function(possibleErrorMessage) {
          throw new Error(possibleErrorMessage);
        }).then(function(rawResp) {
          return rawResp.json();
        }).then(function(canCreateDiscussions) {
        });
      }
      /**
       * @param {!Object} url
       * @return {?}
       */
      function test(url) {
        var hash = (0, _noframeworkWaypoints2.default)({}, url, {
          gdLabel : _deepAssign2.default.browser.weixin ? "click_weixin_local" : "click_wap_local",
          app : "news_article"
        });
        var html = render(hash);
        /** @type {string} */
        var expected = "open_url=" + encodeURIComponent(html);
        /** @type {string} */
        var msg = "http://127.0.0.1:28192?" + expected;
        return post("http://[::1]:28192?" + expected).then(function(canCreateDiscussions) {
        }, function(canCreateDiscussions) {
          return post(msg);
        });
      }
      /**
       * @return {?}
       */
      function normalizeFbPhoneNumber() {
        return "CN" === window.country_code && !(["\u5317\u4eac", "\u4e0a\u6d77", "\u5e7f\u5dde", "\u6df1\u5733"].indexOf(window.city) > -1);
      }
      var _noframeworkWaypoints = __webpack_require__("dU2U");
      var _noframeworkWaypoints2 = _interopRequireDefault(_noframeworkWaypoints);
      var _normalizeDataUri = __webpack_require__("p7ii");
      var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
      var _deepAssign = __webpack_require__("gT+X");
      var _deepAssign2 = _interopRequireDefault(_deepAssign);
      var _prepareStyleProperties = __webpack_require__("YWnE");
      var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
      __webpack_require__("X+OT");
      __webpack_require__("wtgB").polyfill();
      /**
       * @return {undefined}
       */
      window.loadimg = function() {
      };
      /**
       * @return {undefined}
       */
      window.errorimg = function() {
      };
      var M = function() {
        var NATIVE_GEBCN = normalizeFbPhoneNumber();
        var GEBCN = _deepAssign2.default.browser.weixin && _deepAssign2.default.os.android;
        /** @type {string} */
        var token = "";
        return NATIVE_GEBCN && GEBCN && (token = "http://d.toutiao.com/y9BJ/"), token;
      }();
      var position = {
        scrollTop : go,
        isAppInstalled : searchRelativePath,
        isGroupUrl : isChangeDirectory,
        getGTMValue : propertyStringReplacer,
        getParam : getParam,
        getScheme : init,
        getNativeLink : render,
        getUTMValue : setAttribute,
        getAppTrackData : resize,
        confused : c,
        initScrollEvents : Ellipsis,
        testAD : v,
        getTTWebID : write,
        androidLocalServer : test,
        bottomBannerSDKShortLink : M
      };
      module.exports = position;
    }).call(exports, __webpack_require__("gXQ3"));
  },
  bljy : function(rawCodewords, version) {
    Function(function(canCreateDiscussions) {
      return '\u0013e(e,a,r){\u0014(b[e]||(b[e]=t("x,y","\u0014x "+e+" y"\u0015)(r,a)}\u0013a(e,a,r){\u0014(k[r]||(k[r]=t("x,y","\u0014new x[y]("+Array(r+1).join(",x[\u0016y]")\u0017(1)+")"\u0015)(e,a)}\u0013r(e,a,r){\u0018n,t,s={},b=s.d=r?r.d+1:0;for(s["$"+b]=s,t=0;t<b;t\u0016)s[n="$"+t]=r[n];for(t=0,b=s\u0019=a\u0019;t<b;t\u0016)s[t]=a[t];\u0014c(e,0,s)}\u0013c(t,b,k){\u0013u(e){v[x\u0016]=e}\u0013f\u001a{\u0014g=\u0012,t\u0017ing(b\u001bg)}\u0013l\u001a{try{y=c(t,b,k)}catch(e){h=e,y=l}}for(\u0018h,y,d,g,v=[],x=0;;)switch(g=\u0012){case 1:u(!\u0011)\u001c4:\u0010f\u001a\u001c5:u(\u0013(e){\u0018a=0,r=e\u0019;\u0014\u0013\u001a{\u0018c=a<r;\u0014c&&u(e[a\u0016]),c}}(\u0011\u0015\u001c6:y=\u0011,u(\u0011(y\u0015\u001c8:if(g=\u0012,l\u001a\u001bg,g=\u0012,y===c)b+=g;else if(y!==l)\u0014y\u001c9:\u0010c\u001c10:u(s(\u0011\u0015\u001c11:y=\u0011,u(\u0011+y)\u001c12:for(y=f\u001a,d=[],g=0;g<y\u0019;g\u0016)d[g]=y.charCodeAt(g)^g+y\u0019;u(String.fromCharCode.apply(null,d\u0015\u001c13:y=\u0011,h=delete \u0011[y]\u001c14:\u0010\u0012\u001c59:u((g=\u0012)?(y=x,v.slice(x-=g,y\u0015:[])\u001c61:u(\u0011[\u0012])\u001c62:g=\u0011,k[0]=65599*k[0]+k[1].charCodeAt(g)>>>0\u001c65:h=\u0011,y=\u0011,\u0011[y]=h\u001c66:u(e(t[b\u0016],\u0011,\u0011\u0015\u001c67:y=\u0011,d=\u0011,u((g=\u0011).x===c?r(g.y,y,k):g.apply(d,y\u0015\u001c68:u(e((g=t[b\u0016])<"<"?(b--,f\u001a):g+g,\u0011,\u0011\u0015\u001c70:u(!1)\u001c71:\u0010n\u001c72:\u0010+f\u001a\u001c73:u(parseInt(f\u001a,36\u0015\u001c75:if(\u0011){b\u0016\u001dcase 74:g=\u0012<<16>>16\u001bg\u001c76:u(k[\u0012])\u001c77:y=\u0011,u(\u0011[y])\u001c78:g=\u0012,u(a(v,x-=g+1,g\u0015\u001c79:g=\u0012,u(k["$"+g])\u001c81:h=\u0011,\u0011[f\u001a]=h\u001c82:u(\u0011[f\u001a])\u001c83:h=\u0011,k[\u0012]=h\u001c84:\u0010!0\u001c85:\u0010void 0\u001c86:u(v[x-1])\u001c88:h=\u0011,y=\u0011,\u0010h,\u0010y\u001c89:u(\u0013\u001a{\u0013e\u001a{\u0014r(e.y,arguments,k)}\u0014e.y=f\u001a,e.x=c,e}\u001a)\u001c90:\u0010null\u001c91:\u0010h\u001c93:h=\u0011\u001c0:\u0014\u0011;default:u((g<<16>>16)-16)}}\u0018n=this,t=n.Function,s=Object.keys||\u0013(e){\u0018a={},r=0;for(\u0018c in e)a[r\u0016]=c;\u0014a\u0019=r,a},b={},k={};\u0014r'.replace(/[\u0010-\u001f]/g,
      function(strUtf8) {
        return canCreateDiscussions[15 & strUtf8.charCodeAt(0)];
      });
    }("v[x++]=\u0010v[--x]\u0010t.charCodeAt(b++)-32\u0010function \u0010return \u0010))\u0010++\u0010.substr\u0010var \u0010.length\u0010()\u0010,b+=\u0010;break;case \u0010;break}".split("\u0010")))()('gr$Daten \u0418b/s!l y\u0352y\u0139g,(lfi~ah`{mv,-n|jqewVxp{rvmmx,&eff\u007fkx[!cs"l".Pq%widthl"@q&heightl"vr*getContextx$"2d[!cs#l#,*;?|u.|uc{uq$fontl#vr(fillTextx$$\u9f98\u0e11\u0e20\uacbd2<[#c}l#2q*shadowBlurl#1q-shadowOffsetXl#$$limeq+shadowColorl#vr#arcx88802[%c}l#vr&strokex[ c}l"v,)}eOmyoZB]mx[ cs!0s$l$Pb<k7l l!r&lengthb%^l$1+s$j\u0002l  s#i$1ek1s$gr#tack4)zgr#tac$! +0o![#cj?o ]!l$b%s"o ]!l"l$b*b^0d#>>>s!0s%yA0s"l"l!r&lengthb<k+l"^l"1+s"j\u0005l  s&l&z0l!$ +["cs\'(0l#i\'1ps9wxb&s() &{s)/s(gr&Stringr,fromCharCodes)0s*yWl ._b&s o!])l l Jb<k$.aj;l .Tb<k$.gj/l .^b<k&i"-4j!\u001f+& s+yPo!]+s!l!l Hd>&l!l Bd>&+l!l <d>&+l!l 6d>&+l!l &+ s,y=o!o!]/q"13o!l q"10o!],l 2d>& s.{s-yMo!o!]0q"13o!]*Ld<l 4d#>>>b|s!o!l q"10o!],l!& s/yIo!o!].q"13o!],o!]*Jd<l 6d#>>>b|&o!]+l &+ s0l-l!&l-l!i\'1z141z4b/@d<l"b|&+l-l(l!b^&+l-l&zl\'g,)gk}ejo{\u007fcm,)|yn~Lij~em["cl$b%@d<l&zl\'l $ +["cl$b%b|&+l-l%8d<@b|l!b^&+ q$sign ',
    [Object.defineProperty(version, "__esModule", {
      value : true
    })]);
  },
  dU2U : function(module, exports, __webpack_require__) {
    module.exports = {
      default : __webpack_require__("RIhk"),
      __esModule : true
    };
  },
  dWRr : function(formatters, customFormatters) {
  },
  efr4 : function(mixin, doPost) {
    /**
     * @param {!Object} name
     * @param {string} text
     * @param {!Object} obj
     * @param {?} r
     * @return {?}
     */
    mixin.exports = function(name, text, obj, r) {
      /** @type {function(!Object, !Object, !Object, ?, !Function, !Function): undefined} */
      var oldRoot = obj.root;
      /**
       * @param {!Object} env
       * @param {!Object} context
       * @param {!Object} frame
       * @param {?} name
       * @param {!Function} done
       * @param {!Function} cb
       * @return {undefined}
       */
      obj.root = function(env, context, frame, name, done, cb) {
        var oldGetTemplate = env.getTemplate;
        /**
         * @param {!Function} app
         * @param {!Array} url
         * @param {?} identifier
         * @param {?} options
         * @param {number} element
         * @return {undefined}
         */
        env.getTemplate = function(app, url, identifier, options, element) {
          if ("function" == typeof url) {
            /** @type {boolean} */
            element = url = false;
          }
          /**
           * @param {(!Function|string)} name
           * @return {?}
           */
          var template = function(name) {
            try {
              return r[name];
            } catch (t) {
              if (frame.get("_require")) {
                return frame.get("_require")(name);
              }
              console.warn('Could not load template "%s"', name);
            }
          };
          var s = template(app);
          frame.set("_require", template);
          if (url) {
            s.compile();
          }
          element(null, s);
        };
        oldRoot(env, context, frame, name, done, function(fallbackReleases, bucketNotification) {
          env.getTemplate = oldGetTemplate;
          cb(fallbackReleases, bucketNotification);
        });
      };
      var params = {
        obj : obj,
        type : "code"
      };
      return new name.Template(params, text);
    };
  },
  f3r1 : function(blob, id, require) {
    var checkPropTypes = require("mzD8");
    var createElement = require("HMaR");
    var url = require("0hfc");
    /**
     * @return {?}
     */
    blob.exports = function() {
      /**
       * @param {!Object} name
       * @param {string} value
       * @param {!Function} fn
       * @param {?} settings
       * @param {?} doc
       * @param {?} location
       * @return {undefined}
       */
      function shim(name, value, fn, settings, doc, location) {
        if (location !== url) {
          createElement(false, "Calling PropTypes validators directly is not supported by the `prop-types` package. Use PropTypes.checkPropTypes() to call them. Read more at http://fb.me/use-check-prop-types");
        }
      }
      /**
       * @return {?}
       */
      function getShim() {
        return shim;
      }
      /** @type {function(!Object, string, !Function, ?, ?, ?): undefined} */
      shim.isRequired = shim;
      var ReactPropTypes = {
        array : shim,
        bool : shim,
        func : shim,
        number : shim,
        object : shim,
        string : shim,
        symbol : shim,
        any : shim,
        arrayOf : getShim,
        element : shim,
        instanceOf : getShim,
        node : shim,
        objectOf : getShim,
        oneOf : getShim,
        oneOfType : getShim,
        shape : getShim,
        exact : getShim
      };
      return ReactPropTypes.checkPropTypes = checkPropTypes, ReactPropTypes.PropTypes = ReactPropTypes, ReactPropTypes;
    };
  },
  fvPU : function(module, exports, __weex_require__) {
    /** @type {boolean} */
    exports.__esModule = true;
    /**
     * @param {!Object} name
     * @param {!Function} type
     * @return {undefined}
     */
    exports.default = function(name, type) {
      if (!(name instanceof type)) {
        throw new TypeError("Cannot call a class as a function");
      }
    };
  },
  hAp8 : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _AboutPage = __webpack_require__("mRYa");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _deepAssign = __webpack_require__("IJ1K");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    var _AppDownload = __webpack_require__("YWnE");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var HorizontalScroller = __webpack_require__("aZsa");
    __webpack_require__("QLF1");
    /** @type {boolean} */
    var isOpen = "ttvideo" === _AppDownload2.default.request("activity") || "m.ixigua.com" === location.host;
    var PercentageSymbol = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _UiIcon2.default)(this, Agent), (0, _AboutPage2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).apply(this, arguments));
      }
      return (0, _deepAssign2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "render",
        value : function() {
          return _prepareStyleProperties2.default.createElement(HorizontalScroller, {
            transitionName : "refreshTip",
            transitionEnterTimeout : 500,
            transitionLeaveTimeout : 300
          }, this.props.showRefreshTip && _prepareStyleProperties2.default.createElement("p", {
            className : "refresh-tip",
            key : "refreshTip"
          }, "\u4e3a\u4f60\u63a8\u8350\u4e86", this.props.fetchNumber, isOpen ? "\u4e2a\u89c6\u9891" : "\u7bc7\u6587\u7ae0"));
        }
      }]), Agent;
    }(_prepareStyleProperties.Component);
    PercentageSymbol.propTypes = {
      showRefreshTip : _propTypes2.default.bool,
      fetchNumber : _propTypes2.default.number
    };
    module.exports = PercentageSymbol;
  },
  hJ6a : function(module, exports, __weex_require__) {
    /** @type {boolean} */
    exports.__esModule = true;
    var storage = __weex_require__("DhyE");
    var initialState = function(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }(storage);
    exports.default = function() {
      /**
       * @param {!Function} b
       * @param {string} r
       * @return {undefined}
       */
      function e(b, r) {
        /** @type {number} */
        var i = 0;
        for (; i < r.length; i++) {
          var current = r[i];
          current.enumerable = current.enumerable || false;
          /** @type {boolean} */
          current.configurable = true;
          if ("value" in current) {
            /** @type {boolean} */
            current.writable = true;
          }
          (0, initialState.default)(b, current.key, current);
        }
      }
      return function(t, r, n) {
        return r && e(t.prototype, r), n && e(t, n), t;
      };
    }();
  },
  hK0m : function(f, m, n) {
    (function(_) {
      /**
       * @param {!Object} obj
       * @return {?}
       */
      function _interopRequireDefault(obj) {
        return obj && obj.__esModule ? obj : {
          default : obj
        };
      }
      /**
       * @param {!Object} name
       * @return {undefined}
       */
      function callback(name) {
        var item = {
          downloadLink : "//d.toutiao.com/e6jY/",
          yybLink : "tmast://appdetails?r=0.27985643851570785&pname=com.ss.android.article.news&oplist=1%3B2&via=ANDROIDWXZ.YYB.OTHERBROWSER&channelid=000116083232363434363139&appid=213141",
          nativeLink : "",
          universalLink : "",
          openUrl : ""
        };
        (0, _prepareStyleProperties2.default)(item, name || {});
        if ("m.toutiaoribao.cn" === location.host) {
          /** @type {string} */
          item.downloadLink = "http://d.toutiaoribao.cn/NtNA/";
          /** @type {string} */
          item.app = "toutiaoribao";
          if ("toutiaoribao_newssocial" === _normalizeDataUri2.default.request("app")) {
            /** @type {string} */
            item.downloadLink = "https://d.toutiaoribao.cn/LUQB/";
          }
        }
        /** @type {string} */
        var r = "click_" + (o.browser.weixin ? "weixin" : "wap") + "_" + (window.isListPage ? "list" : "detail") + "_" + item.pos;
        (0, _prepareStyleProperties2.default)(item, {
          gdLabel : r
        });
        if (window.group_id) {
          _.extend(true, item, {
            id : window.group_id,
            type : "detail",
            isNewVideo : window.isNewVideoPage
          });
        }
        item.nativeLink = item.nativeLink || m.getNativeLink(item);
        if (o.os.ios) {
          if (o.browser.weixin) {
            l.jumpToNativeapp(item);
            setTimeout(function() {
              next.gotoAppDownload(item);
            }, 1E3);
          } else {
            next.gotoAppDownload(item);
            setTimeout(function() {
              l.jumpToNativeapp(item);
            }, 1E3);
          }
        } else {
          l.jumpToNativeapp(item);
          next.gotoAppDownload(item);
        }
      }
      var _prepareStyleProperties = n("dU2U");
      var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
      var _normalizeDataUri = n("YWnE");
      var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
      var next = n("84PZ");
      var l = n("4/IU");
      var m = n("bVOP");
      var o = n("gT+X");
      /** @type {function(!Object): undefined} */
      f.exports = callback;
    }).call(m, n("gXQ3"));
  },
  kZEW : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    /**
     * @return {undefined}
     */
    function init() {
      x.forEach(function(header) {
        if (!header.visible && create(header)) {
          comments.push(header);
          /** @type {boolean} */
          header.visible = true;
          header.props.onFirstInView();
        }
      });
      checkIfLevelsAreDefined();
    }
    /**
     * @return {undefined}
     */
    function checkIfLevelsAreDefined() {
      comments.forEach(function(c, canCreateDiscussions) {
        /** @type {number} */
        var n = x.indexOf(c);
        if (n > -1) {
          x.splice(n, 1);
        }
      });
    }
    /**
     * @param {!Object} component
     * @return {?}
     */
    function create(component) {
      var listElement = _reactDom2.default.findDOMNode(component);
      var fixedMargins = listElement.getBoundingClientRect();
      return fixedMargins.top >= 0 && fixedMargins.top <= (window.innerHeight || document.documentElement.clientHeight) || fixedMargins.bottom >= 0 && fixedMargins.bottom <= (window.innerHeight || document.documentElement.clientHeight);
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _deepAssign = __webpack_require__("mRYa");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _UiRippleInk = __webpack_require__("IJ1K");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _react = __webpack_require__("V80v");
    var _reactDom = (_interopRequireDefault(_react), __webpack_require__("GF8f"));
    var _reactDom2 = _interopRequireDefault(_reactDom);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    /** @type {!Array} */
    var x = [];
    /** @type {!Array} */
    var comments = [];
    var Context = function(_EventEmitter) {
      /**
       * @return {?}
       */
      function Agent() {
        return (0, _UiIcon2.default)(this, Agent), (0, _deepAssign2.default)(this, (Agent.__proto__ || (0, _normalizeDataUri2.default)(Agent)).apply(this, arguments));
      }
      return (0, _UiRippleInk2.default)(Agent, _EventEmitter), (0, _classlist2.default)(Agent, [{
        key : "componentDidMount",
        value : function() {
          if (0 === x.length) {
            window.addEventListener("scroll", init);
          }
          x.push(this);
          init();
        }
      }, {
        key : "componentWillUnmount",
        value : function() {
          /** @type {number} */
          var e = x.indexOf(this);
          if (-1 !== e) {
            x.splice(e, 1);
          }
          if (0 === x.length) {
            window.removeEventListener("scroll", init);
          }
        }
      }, {
        key : "render",
        value : function() {
          return this.props.children;
        }
      }]), Agent;
    }(_react.Component);
    Context.propTypes = {
      children : _propTypes2.default.oneOfType([_propTypes2.default.arrayOf(_propTypes2.default.node), _propTypes2.default.node])
    };
    mixin.exports = Context;
  },
  lH70 : function(module, layer, $) {
    var Radio;
    var self = $("3Cyt");
    Radio = self.currentEnv ? self.currentEnv : self.currentEnv = new self.Environment([], {
      dev : false,
      autoescape : true,
      throwOnUndefined : false,
      trimBlocks : false,
      lstripBlocks : false
    });
    var wreqr = self.webpackDependencies || (self.webpackDependencies = {});
    var factory = $("efr4");
    !function() {
      (self.nunjucksPrecompiled = self.nunjucksPrecompiled || {})["app/components/ListCardAD/template.nunjucks"] = function() {
        /**
         * @param {!Object} env
         * @param {!Object} context
         * @param {!Object} data
         * @param {?} $
         * @param {!Function} cb
         * @return {undefined}
         */
        function init(env, context, data, $, cb) {
          /** @type {string} */
          var t = "";
          try {
            /** @type {null} */
            var self = null;
            if (t = t + '\n<i class="icon_ad">\n    <span data-show="show"\n        ad-log-extra="', t = t + $.suppressValue($.contextOrFrameLookup(context, data, "log_extra"), env.opts.autoescape), t = t + '"\n        data-track="', t = t + $.suppressValue($.contextOrFrameLookup(context, data, "ad_track_url"), env.opts.autoescape), t = t + '"\n        ad-id="', t = t + $.suppressValue($.contextOrFrameLookup(context, data, "ad_id"), env.opts.autoescape), t = t + '"\n        ad-tag="embeded_ad"\n        ad-label="',
            t = t + $.suppressValue($.contextOrFrameLookup(context, data, "ad_label"), env.opts.autoescape), t = t + '">\n    </span>\n</i>\n\n', $.contextOrFrameLookup(context, data, "is_download_ad") || $.contextOrFrameLookup(context, data, "is_phone_ad")) {
              if (t = t + '\n<div class="article_link clearfix creative_type"\n    ad-tag="{tag}}"\n    ad-url="', t = t + $.suppressValue($.contextOrFrameLookup(context, data, "source_url"), env.opts.autoescape), t = t + '"\n    ', $.contextOrFrameLookup(context, data, "is_download_ad") && (t = t + 'ad-load="true"'), t = t + '\n    ad-id="', t = t + $.suppressValue($.contextOrFrameLookup(context, data, "ad_id"), env.opts.autoescape), t = t + '"\n    ad-log-extra="', t = t + $.suppressValue($.contextOrFrameLookup(context,
              data, "log_extra"), env.opts.autoescape), t = t + '">\n\n    ', 2 == $.contextOrFrameLookup(context, data, "image_mode") && (t = t + '\n    <div class="desc">\n    '), t = t + '\n\n    <h3 class="dotdot line3 ', 2 == $.contextOrFrameLookup(context, data, "image_mode") && (t = t + "image-margin-right"), t = t + '"\n        ', $.contextOrFrameLookup(context, data, "highlight") && (t = t + 'highlight="', t = t + $.suppressValue(env.getFilter("dump").call(context, $.memberLookup($.contextOrFrameLookup(context,
              data, "highlight"), "title")), env.opts.autoescape), t = t + '"'), t = t + ">\n        ", t = t + $.suppressValue($.contextOrFrameLookup(context, data, "title"), env.opts.autoescape), t = t + "\n    </h3>\n\n    ", 4 == $.contextOrFrameLookup(context, data, "image_mode")) {
                /** @type {string} */
                t = t + '\n    <div class="list_image">\n        <ul class="clearfix">\n            ';
                data = data.push();
                var key = $.contextOrFrameLookup(context, data, "imglist");
                if (key) {
                  key = $.fromIterator(key);
                  var count = key.length;
                  /** @type {number} */
                  var index = 0;
                  for (; index < key.length; index++) {
                    var value = key[index];
                    data.set("img", value);
                    data.set("loop.index", index + 1);
                    data.set("loop.index0", index);
                    data.set("loop.revindex", count - index);
                    data.set("loop.revindex0", count - index - 1);
                    data.set("loop.first", 0 === index);
                    data.set("loop.last", index === count - 1);
                    data.set("loop.length", count);
                    /** @type {string} */
                    t = t + '\n            <li class="list_img_holder">\n                <img src="';
                    t = t + $.suppressValue($.memberLookup(value, "url"), env.opts.autoescape);
                    /** @type {string} */
                    t = t + "\" onerror='errorimg.call(this)' onload='loadimg.call(this)'>\n            </li>\n            ";
                  }
                }
                data = data.pop();
                /** @type {string} */
                t = t + "\n        </ul>\n    </div>\n    ";
              }
              /** @type {string} */
              t = t + "\n\n    ";
              if (3 == $.contextOrFrameLookup(context, data, "image_mode")) {
                /** @type {string} */
                t = t + '\n    <div class="list_img_holder_large ';
                if (!$.contextOrFrameLookup(context, data, "ad_label")) {
                  /** @type {string} */
                  t = t + "list_img_holder_large_fix";
                }
                /** @type {string} */
                t = t + '">\n        <img ';
                if (!$.contextOrFrameLookup(context, data, "ad_type")) {
                  /** @type {string} */
                  t = t + 'src="';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "image_url"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + '"';
                }
                /** @type {string} */
                t = t + " \n            onerror='errorimg.call(this)'  \n            onload='loadimg.call(this)' />\n        ";
                if ($.contextOrFrameLookup(context, data, "has_video")) {
                  /** @type {string} */
                  t = t + '\n        <span class="video-btn"></span>\n        ';
                }
                /** @type {string} */
                t = t + '\n    </div>\n\n    <div class="text_info large_info">\n        ';
                if ($.contextOrFrameLookup(context, data, "source")) {
                  /** @type {string} */
                  t = t + '\n        <span class="source">';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "source"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + "</span>\n        ";
                }
                /** @type {string} */
                t = t + "\n\n        ";
                if ($.contextOrFrameLookup(context, data, "is_download_ad")) {
                  /** @type {string} */
                  t = t + '\n        <span class="download" ad-url="';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "download_url"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + '">\u7acb\u5373\u4e0b\u8f7d</span>\n        ';
                }
                /** @type {string} */
                t = t + "\n\n        ";
                if ($.contextOrFrameLookup(context, data, "is_phone_ad")) {
                  /** @type {string} */
                  t = t + '\n        <span class="phone" ad-url="';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "phone_number"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + '">';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "button_text"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + "</span>\n        ";
                }
                /** @type {string} */
                t = t + "\n    </div>\n    ";
              }
              /** @type {string} */
              t = t + '\n\n    <div class="item_info">\n        ';
              if ($.contextOrFrameLookup(context, data, "ad_label")) {
                /** @type {string} */
                t = t + '\n        <span class="gg_label space">';
                t = t + $.suppressValue($.contextOrFrameLookup(context, data, "ad_label"), env.opts.autoescape);
                /** @type {string} */
                t = t + "</span>\n        ";
              }
              /** @type {string} */
              t = t + '\n\n        <span class="cmt space">\u8bc4\u8bba ';
              t = t + $.suppressValue($.contextOrFrameLookup(context, data, "comment_count"), env.opts.autoescape);
              /** @type {string} */
              t = t + "</span>\n\n        ";
              if (2 == !$.contextOrFrameLookup(context, data, "image_mode")) {
                /** @type {string} */
                t = t + '\n        <span class="time" title="';
                t = t + $.suppressValue($.contextOrFrameLookup(context, data, "datetime"), env.opts.autoescape);
                /** @type {string} */
                t = t + '">';
                t = t + $.suppressValue($.contextOrFrameLookup(context, data, "timeago"), env.opts.autoescape);
                /** @type {string} */
                t = t + "</span>\n        ";
              }
              /** @type {string} */
              t = t + "\n    </div>\n\n    ";
              if (2 == $.contextOrFrameLookup(context, data, "image_mode")) {
                /** @type {string} */
                t = t + '\n    </div>\n    <div class="list_img_holder ">\n        <img src="';
                t = t + $.suppressValue($.contextOrFrameLookup(context, data, "image_url"), env.opts.autoescape);
                /** @type {string} */
                t = t + "\" onerror='errorimg.call(this)'  onload='loadimg.call(this)'>\n    </div>\n    ";
              }
              /** @type {string} */
              t = t + "\n\n    ";
              if (!(2 != $.contextOrFrameLookup(context, data, "image_mode") && 4 != $.contextOrFrameLookup(context, data, "image_mode"))) {
                /** @type {string} */
                t = t + '\n    <div class="text_info">\n        ';
                if ($.contextOrFrameLookup(context, data, "source")) {
                  /** @type {string} */
                  t = t + '\n        <span class="source">';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "source"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + "</span>\n        ";
                }
                /** @type {string} */
                t = t + "\n\n        ";
                if ($.contextOrFrameLookup(context, data, "is_download_ad")) {
                  /** @type {string} */
                  t = t + '\n        <span class="download" ad-url="';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "download_url"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + '">\u7acb\u5373\u4e0b\u8f7d</span>\n        ';
                }
                /** @type {string} */
                t = t + "\n\n        ";
                if ($.contextOrFrameLookup(context, data, "is_phone_ad")) {
                  /** @type {string} */
                  t = t + '\n        <span class="phone" ad-url="';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "phone_number"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + '">';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "button_text"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + "</span>\n        ";
                }
                /** @type {string} */
                t = t + "\n    </div>\n    ";
              }
              /** @type {string} */
              t = t + "\n</div>\n";
            } else {
              if (t = t + '\n<a href="', t = t + $.suppressValue($.contextOrFrameLookup(context, data, "source_url"), env.opts.autoescape), t = t + '"\n    class="article_link clearfix "\n    data-action-label="', t = t + $.suppressValue($.contextOrFrameLookup(context, data, "action_label"), env.opts.autoescape), t = t + '"\n    data-tag="', t = t + $.suppressValue($.contextOrFrameLookup(context, data, "tag"), env.opts.autoescape), t = t + '">\n\n    ', $.contextOrFrameLookup(context, data, "middle_mode") &&
              (t = t + '\n    <div class="desc">\n    '), t = t + '\n\n    <h3 class="dotdot line3 ', $.contextOrFrameLookup(context, data, "middle_mode") && (t = t + "image-margin-right"), t = t + '"\n        ', $.contextOrFrameLookup(context, data, "highlight") && (t = t + 'highlight="', t = t + $.suppressValue(env.getFilter("jsonify").call(context, $.memberLookup($.contextOrFrameLookup(context, data, "highlight"), "title")), env.opts.autoescape), t = t + '"'), t = t + ">\n        ", t = t + $.suppressValue($.contextOrFrameLookup(context,
              data, "title"), env.opts.autoescape), t = t + "\n    </h3>\n\n    ", $.contextOrFrameLookup(context, data, "more_mode")) {
                /** @type {string} */
                t = t + '\n    <div class="list_image">\n        <ul class="clearfix">\n            ';
                data = data.push();
                var items = $.contextOrFrameLookup(context, data, "image_list");
                if (items) {
                  items = $.fromIterator(items);
                  var count = items.length;
                  /** @type {number} */
                  var index = 0;
                  for (; index < items.length; index++) {
                    var s = items[index];
                    data.set("img", s);
                    data.set("loop.index", index + 1);
                    data.set("loop.index0", index);
                    data.set("loop.revindex", count - index);
                    data.set("loop.revindex0", count - index - 1);
                    data.set("loop.first", 0 === index);
                    data.set("loop.last", index === count - 1);
                    data.set("loop.length", count);
                    /** @type {string} */
                    t = t + '\n            <li class="list_img_holder">\n                <img src="';
                    t = t + $.suppressValue($.memberLookup(s, "url"), env.opts.autoescape);
                    /** @type {string} */
                    t = t + "\" onerror='errorimg.call(this)' onload='loadimg.call(this)'>\n            </li>\n            ";
                  }
                }
                data = data.pop();
                /** @type {string} */
                t = t + "\n        </ul>\n    </div>\n    ";
              }
              /** @type {string} */
              t = t + "\n\n    ";
              if ($.contextOrFrameLookup(context, data, "large_mode") || "taobao" == $.contextOrFrameLookup(context, data, "ad_type")) {
                /** @type {string} */
                t = t + '\n    <div class="list_img_holder_large ';
                if (!$.contextOrFrameLookup(context, data, "ad_label")) {
                  /** @type {string} */
                  t = t + "list_img_holder_large_fix";
                }
                /** @type {string} */
                t = t + '">\n        <img ';
                if (!$.contextOrFrameLookup(context, data, "ad_type")) {
                  /** @type {string} */
                  t = t + 'src="';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "large_image_url"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + '"';
                }
                /** @type {string} */
                t = t + "\n            onerror='errorimg.call(this)'\n            onload='loadimg.call(this)' />\n        ";
                if ($.contextOrFrameLookup(context, data, "has_video")) {
                  /** @type {string} */
                  t = t + '\n        <span class="video-btn"></span>\n        ';
                }
                /** @type {string} */
                t = t + "\n    </div>\n    ";
              }
              /** @type {string} */
              t = t + '\n    <div class="item_info">\n        ';
              if ($.contextOrFrameLookup(context, data, "hot")) {
                /** @type {string} */
                t = t + '\n        <span class="hot_label space">\u70ed</span>\n        ';
              }
              /** @type {string} */
              t = t + "\n\n        ";
              if ($.contextOrFrameLookup(context, data, "recommend")) {
                /** @type {string} */
                t = t + '\n        <span class="recommend_label space">\u8350</span>\n        ';
              }
              /** @type {string} */
              t = t + "\n\n        ";
              if ($.contextOrFrameLookup(context, data, "subject_label")) {
                /** @type {string} */
                t = t + '\n        <span class="subject_label">';
                t = t + $.suppressValue($.contextOrFrameLookup(context, data, "subject_label"), env.opts.autoescape);
                /** @type {string} */
                t = t + "</span>\n        ";
              }
              /** @type {string} */
              t = t + "\n\n        ";
              if ($.contextOrFrameLookup(context, data, "ad_label")) {
                /** @type {string} */
                t = t + '\n        <span class="gg_label space">';
                t = t + $.suppressValue($.contextOrFrameLookup(context, data, "ad_label"), env.opts.autoescape);
                /** @type {string} */
                t = t + "</span>\n        ";
              }
              /** @type {string} */
              t = t + "\n\n        ";
              if (!$.contextOrFrameLookup(context, data, "subject_label")) {
                /** @type {string} */
                t = t + '\n        <span class="src space';
                if ("\u767e\u5ea6\u7ecf\u9a8c" == $.contextOrFrameLookup(context, data, "source")) {
                  /** @type {string} */
                  t = t + "recommend_label";
                }
                /** @type {string} */
                t = t + '">';
                t = t + $.suppressValue($.contextOrFrameLookup(context, data, "source"), env.opts.autoescape);
                /** @type {string} */
                t = t + "</span>";
              }
              /** @type {string} */
              t = t + '\n\n        <span class="cmt space">\u8bc4\u8bba ';
              t = t + $.suppressValue($.contextOrFrameLookup(context, data, "comment_count"), env.opts.autoescape);
              /** @type {string} */
              t = t + "</span>\n\n        ";
              if (!$.contextOrFrameLookup(context, data, "middle_mode")) {
                /** @type {string} */
                t = t + '\n        <span class="time" title="';
                t = t + $.suppressValue($.contextOrFrameLookup(context, data, "datetime"), env.opts.autoescape);
                /** @type {string} */
                t = t + '">';
                t = t + $.suppressValue($.contextOrFrameLookup(context, data, "timeago"), env.opts.autoescape);
                /** @type {string} */
                t = t + "</span>\n        ";
              }
              /** @type {string} */
              t = t + '\n\n        <span data-id="';
              t = t + $.suppressValue($.contextOrFrameLookup(context, data, "group_id"), env.opts.autoescape);
              /** @type {string} */
              t = t + '"\n            class="dislike-news ';
              if ($.contextOrFrameLookup(context, data, "middle_mode")) {
                /** @type {string} */
                t = t + "mid-space";
              }
              /** @type {string} */
              t = t + ' fr">\n        </span>\n    </div>\n    ';
              if ($.contextOrFrameLookup(context, data, "middle_mode")) {
                /** @type {string} */
                t = t + '\n    </div>\n    <div class="list_img_holder">\n        <img ';
                if (!$.contextOrFrameLookup(context, data, "ad_type")) {
                  /** @type {string} */
                  t = t + 'src="';
                  t = t + $.suppressValue($.contextOrFrameLookup(context, data, "image_url"), env.opts.autoescape);
                  /** @type {string} */
                  t = t + '"';
                }
                /** @type {string} */
                t = t + "\n            onerror='errorimg.call(this)'\n            onload='loadimg.call(this)'/>\n        ";
                if ($.contextOrFrameLookup(context, data, "has_video")) {
                  /** @type {string} */
                  t = t + '\n        <span class="video-btn"></span>\n        ';
                }
                /** @type {string} */
                t = t + "\n    </div>\n    ";
              }
              /** @type {string} */
              t = t + "\n";
            }
            /** @type {string} */
            t = t + "\n</a>\n";
            if (self) {
              self.rootRenderFunc(env, context, data, $, cb);
            } else {
              cb(null, t);
            }
          } catch (err) {
            cb($.handleError(err, null, null));
          }
        }
        return {
          root : init
        };
      }();
    }();
    module.exports = factory(self, Radio, self.nunjucksPrecompiled["app/components/ListCardAD/template.nunjucks"], wreqr);
  },
  lxt5 : function(mixin, doPost, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _UiRippleInk = __webpack_require__("mRYa");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _AboutPage = __webpack_require__("IJ1K");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _deepAssign = __webpack_require__("nhKt");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _AppDownload = __webpack_require__("hK0m");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    __webpack_require__("dWRr");
    var PercentageSymbol = function(leftFence) {
      /**
       * @param {?} props
       * @return {?}
       */
      function ReflexElement(props) {
        return (0, _UiIcon2.default)(this, ReflexElement), (0, _UiRippleInk2.default)(this, (ReflexElement.__proto__ || (0, _normalizeDataUri2.default)(ReflexElement)).call(this, props));
      }
      return (0, _AboutPage2.default)(ReflexElement, leftFence), (0, _classlist2.default)(ReflexElement, [{
        key : "handleClose",
        value : function() {
          window.maevent("left_top", "close", "");
          this.props.handleClose();
        }
      }, {
        key : "handleDownload",
        value : function() {
          window.maevent("left_top", "download");
          (0, _AppDownload2.default)({
            downloadLink : "//d.toutiao.com/2ePc/"
          });
        }
      }, {
        key : "render",
        value : function() {
          var subject = this;
          return _prepareStyleProperties2.default.createElement("div", {
            id : "pageletPopupBanner",
            className : "tt-modal"
          }, _prepareStyleProperties2.default.createElement("div", {
            className : "popup"
          }, _prepareStyleProperties2.default.createElement("div", {
            className : "banner"
          }), _prepareStyleProperties2.default.createElement("p", null, "\u5df2\u52a0\u8f7d\u597d\u60a8\u611f\u5174\u8da3\u7684\u5934\u6761"), _prepareStyleProperties2.default.createElement("div", {
            className : "download-btn",
            "data-node" : "downloadBtn",
            onClick : function() {
              return subject.handleDownload();
            }
          }, "\u7acb\u5373\u6253\u5f00"), _prepareStyleProperties2.default.createElement("div", {
            className : "close",
            "data-node" : "close",
            onClick : function() {
              subject.handleClose();
            }
          })));
        }
      }]), ReflexElement;
    }(_prepareStyleProperties.Component);
    PercentageSymbol.propTypes = {
      handleClose : _deepAssign2.default.func
    };
    mixin.exports = PercentageSymbol;
  },
  mJKx : function(mixin, doPost, __webpack_require__) {
    __webpack_require__("HjcX");
    var Obj = __webpack_require__("qGgm").Object;
    /**
     * @param {!Object} name
     * @param {string} type
     * @return {?}
     */
    mixin.exports = function(name, type) {
      return Obj.create(name, type);
    };
  },
  mRYa : function(module, exports, __weex_require__) {
    /** @type {boolean} */
    exports.__esModule = true;
    var storage = __weex_require__("gf5I");
    var initialState = function(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }(storage);
    /**
     * @param {!Object} name
     * @param {number} value
     * @return {?}
     */
    exports.default = function(name, value) {
      if (!name) {
        throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
      }
      return !value || "object" !== (void 0 === value ? "undefined" : (0, initialState.default)(value)) && "function" != typeof value ? name : value;
    };
  },
  mSCD : function(mixin, args, parseAsUTC) {
    /**
     * @return {undefined}
     */
    var storeMixin = function() {
    };
    /** @type {function(): undefined} */
    mixin.exports = storeMixin;
  },
  mZJ8 : function(module, exports, __webpack_require__) {
    module.exports = {
      default : __webpack_require__("X3Bo"),
      __esModule : true
    };
  },
  mr6U : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
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
     * @param {!Object} e
     * @param {!Object} t
     * @return {undefined}
     */
    function _inherits(e, t) {
      if ("function" != typeof t && null !== t) {
        throw new TypeError("Super expression must either be null or a function, not " + typeof t);
      }
      /** @type {!Object} */
      e.prototype = Object.create(t && t.prototype, {
        constructor : {
          value : e,
          enumerable : false,
          writable : true,
          configurable : true
        }
      });
      if (t) {
        if (Object.setPrototypeOf) {
          Object.setPrototypeOf(e, t);
        } else {
          /** @type {!Object} */
          e.__proto__ = t;
        }
      }
    }
    /**
     * @param {!Element} s
     * @param {!Function} type
     * @return {?}
     */
    function filter(s, type) {
      return events.length ? events.forEach(function(n) {
        return s.addEventListener(n, type, false);
      }) : setTimeout(type, 0), function() {
        if (events.length) {
          events.forEach(function(eventName) {
            return s.removeEventListener(eventName, type, false);
          });
        }
      };
    }
    /** @type {boolean} */
    exports.__esModule = true;
    /** @type {function(!Object, ...(Object|null)): !Object} */
    var _extends = Object.assign || function(name) {
      /** @type {number} */
      var index = 1;
      for (; index < arguments.length; index++) {
        var options = arguments[index];
        var option;
        for (option in options) {
          if (Object.prototype.hasOwnProperty.call(options, option)) {
            name[option] = options[option];
          }
        }
      }
      return name;
    };
    var _deepAssign = __webpack_require__("oem/");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _classlist = __webpack_require__("N/n7");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _UiIcon = __webpack_require__("Qsus");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _properties = __webpack_require__("w2KC");
    var _react = __webpack_require__("V80v");
    var _react2 = _interopRequireDefault(_react);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    var ReactDOM = __webpack_require__("GF8f");
    var _PropTypes = __webpack_require__("MKUs");
    /** @type {!Array} */
    var events = [];
    if (_properties.transitionEnd) {
      events.push(_properties.transitionEnd);
    }
    if (_properties.animationEnd) {
      events.push(_properties.animationEnd);
    }
    var CSSTransitionGroupChild = (_propTypes2.default.node, _PropTypes.nameShape.isRequired, _propTypes2.default.bool, _propTypes2.default.bool, _propTypes2.default.bool, _propTypes2.default.number, _propTypes2.default.number, _propTypes2.default.number, function(_React$Component) {
      /**
       * @return {?}
       */
      function CSSTransitionGroupChild() {
        var i;
        var _this;
        var _ret;
        _classCallCheck(this, CSSTransitionGroupChild);
        /** @type {number} */
        var _len8 = arguments.length;
        /** @type {!Array} */
        var args = Array(_len8);
        /** @type {number} */
        var _key8 = 0;
        for (; _key8 < _len8; _key8++) {
          args[_key8] = arguments[_key8];
        }
        return i = _this = _possibleConstructorReturn(this, _React$Component.call.apply(_React$Component, [this].concat(args))), _this.componentWillAppear = function(done) {
          if (_this.props.appear) {
            _this.transition("appear", done, _this.props.appearTimeout);
          } else {
            done();
          }
        }, _this.componentWillEnter = function(done) {
          if (_this.props.enter) {
            _this.transition("enter", done, _this.props.enterTimeout);
          } else {
            done();
          }
        }, _this.componentWillLeave = function(done) {
          if (_this.props.leave) {
            _this.transition("leave", done, _this.props.leaveTimeout);
          } else {
            done();
          }
        }, _ret = i, _possibleConstructorReturn(_this, _ret);
      }
      return _inherits(CSSTransitionGroupChild, _React$Component), CSSTransitionGroupChild.prototype.componentWillMount = function() {
        /** @type {!Array} */
        this.classNameAndNodeQueue = [];
        /** @type {!Array} */
        this.transitionTimeouts = [];
      }, CSSTransitionGroupChild.prototype.componentWillUnmount = function() {
        /** @type {boolean} */
        this.unmounted = true;
        if (this.timeout) {
          clearTimeout(this.timeout);
        }
        this.transitionTimeouts.forEach(function(e) {
          clearTimeout(e);
        });
        /** @type {number} */
        this.classNameAndNodeQueue.length = 0;
      }, CSSTransitionGroupChild.prototype.transition = function(animationType, finishCallback, userSpecifiedDelay) {
        var node = (0, ReactDOM.findDOMNode)(this);
        if (!node) {
          return void(finishCallback && finishCallback());
        }
        var classname = this.props.name[animationType] || this.props.name + "-" + animationType;
        var activeClassName = this.props.name[animationType + "Active"] || classname + "-active";
        /** @type {null} */
        var timeout = null;
        var val = void 0;
        (0, _deepAssign2.default)(node, classname);
        this.queueClassAndNode(activeClassName, node);
        /**
         * @param {!Object} n
         * @return {undefined}
         */
        var callback = function(n) {
          if (!(n && n.target !== node)) {
            clearTimeout(timeout);
            if (val) {
              val();
            }
            (0, _classlist2.default)(node, classname);
            (0, _classlist2.default)(node, activeClassName);
            if (val) {
              val();
            }
            if (finishCallback) {
              finishCallback();
            }
          }
        };
        if (userSpecifiedDelay) {
          /** @type {number} */
          timeout = setTimeout(callback, userSpecifiedDelay);
          this.transitionTimeouts.push(timeout);
        } else {
          if (_properties.transitionEnd) {
            val = filter(node, callback);
          }
        }
      }, CSSTransitionGroupChild.prototype.queueClassAndNode = function(className, node) {
        var _this2 = this;
        this.classNameAndNodeQueue.push({
          className : className,
          node : node
        });
        if (!this.rafHandle) {
          this.rafHandle = (0, _UiIcon2.default)(function() {
            return _this2.flushClassNameAndNodeQueue();
          });
        }
      }, CSSTransitionGroupChild.prototype.flushClassNameAndNodeQueue = function() {
        if (!this.unmounted) {
          this.classNameAndNodeQueue.forEach(function(thread) {
            thread.node.scrollTop;
            (0, _deepAssign2.default)(thread.node, thread.className);
          });
        }
        /** @type {number} */
        this.classNameAndNodeQueue.length = 0;
        /** @type {null} */
        this.rafHandle = null;
      }, CSSTransitionGroupChild.prototype.render = function() {
        /** @type {!Object} */
        var props = _extends({}, this.props);
        return delete props.name, delete props.appear, delete props.enter, delete props.leave, delete props.appearTimeout, delete props.enterTimeout, delete props.leaveTimeout, delete props.children, _react2.default.cloneElement(_react2.default.Children.only(this.props.children), props);
      }, CSSTransitionGroupChild;
    }(_react2.default.Component));
    /** @type {string} */
    CSSTransitionGroupChild.displayName = "CSSTransitionGroupChild";
    CSSTransitionGroupChild.propTypes = {};
    exports.default = CSSTransitionGroupChild;
    module.exports = exports.default;
  },
  nhKt : function(blob, options, seriesStackIndexCallback) {
    blob.exports = seriesStackIndexCallback("f3r1")();
  },
  oFNu : function(module, id, require) {
    (function($) {
      /**
       * @param {!Object} obj
       * @return {?}
       */
      function $(obj) {
        return obj && obj.__esModule ? obj : {
          default : obj
        };
      }
      /**
       * @param {!Object} query
       * @return {undefined}
       */
      function send(query) {
        var key = query.cache_key || "listArticleReact___all__";
        var value = query.data || [];
        try {
          localStorage[key] = (0, file.default)(value);
          /** @type {number} */
          localStorage[key + "_lastmodified"] = +new Date;
        } catch (e) {
          console.log("\u6d4f\u89c8\u5668\u5df2\u7981\u7528localStorage!");
        }
      }
      /**
       * @param {!Object} options
       * @return {?}
       */
      function callback(options) {
        var cache_key = options.cache_key;
        var endpointStore = options.listData;
        var fileId = options.channel;
        if (!cache_key) {
          return false;
        }
        if (endpointStore[fileId]) {
          return false;
        }
        if (!res.default.localStorageEnabled) {
          return false;
        }
        if (!localStorage.getItem(cache_key)) {
          return false;
        }
        /** @type {number} */
        var width = Number(localStorage.getItem(cache_key + "_lastmodified" || 0));
        /** @type {number} */
        var screen_width = +new Date - width;
        return !("number" != typeof width || screen_width >= 6E5);
      }
      var qrcode = require("KC+J");
      var option = $(qrcode);
      var permissions = require("mZJ8");
      var result = $(permissions);
      var c = require("iltz");
      var mainCanvas = $(c);
      var button2 = require("fvPU");
      var button = $(button2);
      var srvc = require("hJ6a");
      var item = $(srvc);
      var button1 = require("mRYa");
      var node = $(button1);
      var y = require("IJ1K");
      var $origin = $(y);
      var sources = require("p7ii");
      var file = $(sources);
      var Path = require("V80v");
      var p = $(Path);
      var _propTypes = require("nhKt");
      var _propTypes2 = $(_propTypes);
      var query = require("2SGS");
      var field = $(query);
      var audio = require("xDfE");
      var doc = $(audio);
      var S = require("RvJg");
      var t = $(S);
      var schema = require("BQpG");
      var props = $(schema);
      var transform = require("wFHU");
      var filter = $(transform);
      var event = require("8ICI");
      var top_up = $(event);
      var _DraggableCore = require("hAp8");
      var _DraggableCore2 = $(_DraggableCore);
      var b = require("6+Kz");
      var plan = $(b);
      var window = require("+YOn");
      var wrappedWindow = $(window);
      var otherOp = require("YWnE");
      var res = $(otherOp);
      var pfile = require("LC85");
      var f = $(pfile);
      var XMLHttpRequest = require("1+Ds");
      var z = require("Pekt");
      var a = $(z);
      var m = require("0wW8");
      var markStart = $(m);
      var test2 = require("bVOP");
      var log = $(test2);
      var pt = require("FKII");
      var o = $(pt);
      var aws4 = require("bljy");
      require("Fsns");
      require("s+Cy");
      require("YNWe");
      require("+6Wo");
      var Item = function(e) {
        /**
         * @param {?} shapes
         * @return {?}
         */
        function Tile(shapes) {
          (0, button.default)(this, Tile);
          var self = (0, node.default)(this, (Tile.__proto__ || (0, mainCanvas.default)(Tile)).call(this, shapes));
          return (0, wrappedWindow.default)(), self.channelCategoryList = self.props.topMenuInfo.list, self.defaultCategory = self.props.topMenuInfo.defaultCategory, self.state = {
            GTMValue : {},
            tabList : self.getTabs(),
            defaultChannel : self.getInitCurrentChannel(),
            currentChannel : "",
            listData : {},
            fetchNumber : 0,
            showRefreshTip : false,
            fetchTips : XMLHttpRequest.NETWORKTIPS.LOADING,
            doADTest : {
              position : 0,
              doADTest : false
            },
            showAuditInfo : false
          }, self.channelScrollPosition = {}, self.fetchLock = false, self;
        }
        return (0, $origin.default)(Tile, e), (0, item.default)(Tile, [{
          key : "getTabs",
          value : function() {
            var sbox = this;
            var t = res.default.localStorageEnabled() ? localStorage.menuDefaults : "";
            return (t ? t.split(",") : (0, result.default)(this.channelCategoryList).slice(0, 12)).reduce(function(t, eid) {
              if (sbox.channelCategoryList[eid]) {
                return t[eid] = sbox.channelCategoryList[eid], t;
              }
            }, {});
          }
        }, {
          key : "getInitCurrentChannel",
          value : function() {
            var e = res.default.hash("channel") || res.default.request("channel") || this.defaultCategory;
            return -1 === (0, result.default)(this.channelCategoryList).indexOf(e) && (e = this.defaultCategory), -1 === (0, result.default)(this.getTabs()).indexOf(e) && (e = this.defaultCategory), window.maevent("channel", e, ""), e;
          }
        }, {
          key : "changeHash",
          value : function(name, type) {
            var prefix = function() {
              /** @type {!Array} */
              var drilldownLevelLabels = [];
              var dbNames = res.default.request();
              var i;
              for (i in dbNames) {
                if ("channel" !== i) {
                  drilldownLevelLabels.push([i, encodeURIComponent(dbNames[i])].join("="));
                }
              }
              return drilldownLevelLabels.join("&") || "";
            }();
            /** @type {string} */
            var newHash = (prefix ? prefix + "&" : "") + [type, type].join("#");
            if (history.replaceState) {
              history.replaceState({
                channel : name
              }, null, location.pathname + "?" + newHash);
            } else {
              /** @type {string} */
              location.hash = type;
            }
          }
        }, {
          key : "shouldFetchListData",
          value : function(name, value) {
            if (callback({
              cache_key : "listArticleReact_" + name,
              listData : value,
              channel : name
            })) {
              /** @type {*} */
              var rhs = JSON.parse(localStorage.getItem("listArticleReact_" + name));
              return value[name] = rhs, this.setState({
                listData : value
              }), false;
            }
            return !this.fetchLock;
          }
        }, {
          key : "fetchListData",
          value : function(name, value) {
            var self = this;
            /** @type {boolean} */
            this.fetchLock = true;
            var docs = this.state.listData;
            var undefined = value ? value.direction || "prepend" : "prepend";
            var result = docs[name] || [];
            /** @type {number} */
            var auto = 0;
            /** @type {number} */
            var noOpInitialize = 0;
            if (result.length) {
              auto = result[result.length - 1].behot_time;
              noOpInitialize = result[0].behot_time;
            }
            var params = {
              tag : name,
              ac : "wap",
              count : 20,
              format : "json_raw",
              as : (0, markStart.default)().as,
              cp : (0, markStart.default)().cp,
              max_behot_time : "append" === undefined ? auto : void 0,
              min_behot_time : "prepend" === undefined ? noOpInitialize : void 0,
              _signature : (0, aws4.sign)(auto || ""),
              i : auto || ""
            };
            f.default.get("/list/?" + a.default.stringify(params)).end(function(n, configElement) {
              if (self.fetchLock = false, n) {
                return self.setState({
                  fetchTips : XMLHttpRequest.NETWORKTIPS.RETRY
                }), null;
              }
              /** @type {*} */
              var tb = JSON.parse(configElement.text);
              if (0 === tb.return_count) {
                return self.setState({
                  fetchTips : XMLHttpRequest.NETWORKTIPS.RECOMMENDEMPTY
                }), null;
              }
              var items = tb.data;
              if (self.state.doADTest.doADTest) {
                items.splice(self.state.doADTest.position - 1, 0, {
                  doADTest : true
                });
              }
              send({
                cache_key : "listArticleReact_" + (name || "__all__"),
                data : items
              });
              if ("append" === undefined) {
                /** @type {!Array<?>} */
                result = [].concat(result, items);
                if (window.refreshCount) {
                  window.refreshCount = window.refreshCount + 1;
                } else {
                  /** @type {number} */
                  window.refreshCount = 1;
                }
              } else {
                if ("prepend" === undefined) {
                  result = result.filter(function(options) {
                    return -1 === items.map(function(options) {
                      return options.group_id;
                    }).indexOf(options.group_id);
                  });
                  /** @type {!Array<?>} */
                  result = [].concat(items, result);
                }
              }
              if ("prepend" === undefined) {
                self.setState({
                  showRefreshTip : true
                });
                setTimeout(function() {
                  self.setState({
                    showRefreshTip : false
                  });
                }, 2E3);
                log.default.scrollTop();
              }
              setTimeout(function() {
                $(window).trigger("load");
              }, 300);
              docs[name] = result;
              self.setState({
                listData : docs,
                fetchNumber : tb.return_count,
                fetchTips : XMLHttpRequest.NETWORKTIPS.LOADING
              });
            });
          }
        }, {
          key : "fetchListDataIfNeed",
          value : function(name, type) {
            var boilerStateMachine = this;
            if (this.shouldFetchListData(name, this.state.listData)) {
              this.setState({
                rotateRefreshBtn : true
              });
              setTimeout(function() {
                boilerStateMachine.setState({
                  rotateRefreshBtn : false
                });
              }, 1E3);
              this.fetchListData(name, type);
            }
          }
        }, {
          key : "handleRefreshBtnClick",
          value : function(name, type) {
            var _name = name || this.state.currentChannel;
            if (this.shouldFetchListData(_name, this.state.listData)) {
              this.fetchListData(_name, type);
            }
            /** @type {boolean} */
            o.default.scrollChangeDisable = true;
            window.maevent("refresh", "click");
          }
        }, {
          key : "handleMenuClick",
          value : function(name, type) {
            if (!this.state.listData[name]) {
              this.fetchListDataIfNeed(name);
            }
            this.changeHash(name, type);
            this.changeChannelScrollPosition(name);
            this.setState({
              currentChannel : name
            });
            window.maevent("channel", name, "");
          }
        }, {
          key : "changeChannelScrollPosition",
          value : function(name) {
            var goToKey = this.state.currentChannel;
            /** @type {number} */
            this.channelScrollPosition[goToKey] = window.scrollY;
            window.scrollTo(0, this.channelScrollPosition[name] || 0);
          }
        }, {
          key : "handleMoreClick",
          value : function() {
            window.location = res.default.appendQuery("/channels/", "need_open_window=1");
            window.maevent("channel", "channel_more");
          }
        }, {
          key : "getListData",
          value : function(name) {
            this.fetchListDataIfNeed(this.state.currentChannel, name);
          }
        }, {
          key : "handleScroll",
          value : function(name) {
            if (!("append" === name && log.default.checkReferrer && window.refreshCount >= 20)) {
              this.getListData({
                direction : name
              });
            }
          }
        }, {
          key : "handleAddADMaterial",
          value : function(name) {
            var state = this.state;
            var cache = state.listData;
            cache[state.currentChannel].splice(name.pos, 0, {
              showAdMaterial : true,
              adMaterial : name.adMaterial
            });
            this.setState({
              listData : cache
            });
            this.fetchListData();
          }
        }, {
          key : "handleLoadGTMScript",
          value : function(name) {
            this.setState({
              GTMValue : name
            });
          }
        }, {
          key : "handleDoADTest",
          value : function(name) {
            this.setState({
              doADTest : {
                position : name,
                doADTest : true
              }
            });
          }
        }, {
          key : "componentWillMount",
          value : function() {
            var channel = this.state.defaultChannel;
            this.setState({
              currentChannel : channel
            });
          }
        }, {
          key : "componentDidMount",
          value : function() {
            this.fetchListDataIfNeed(this.state.defaultChannel);
          }
        }, {
          key : "render",
          value : function() {
            var self = this;
            var _SAlertContentTmpl2 = this.state.GTMValue.hideTopBar;
            var state = this.state;
            var tabList = state.tabList;
            var c = state.currentChannel;
            var info = state.listData;
            var end = state.fetchNumber;
            var idnum2expr = state.showRefreshTip;
            var tips = state.fetchTips;
            var newSelectionEnd = state.rotateRefreshBtn;
            var targetHandlerInfos = state.GTMValue;
            if (this.props.isLite) {
              /** @type {boolean} */
              _SAlertContentTmpl2 = false;
            }
            var DropIndicator = this.props.Header || field.default;
            var FormioElement = this.props.TopMenu || doc.default;
            var TodosLogin = this.props.MainContent || t.default;
            var ControlledText = this.props.DownloadBanner || props.default;
            return p.default.createElement("div", {
              id : "indexContainer",
              className : "indexContainer " + (_SAlertContentTmpl2 ? "hideHeader " : "withHeader ") + (this.props.className || "")
            }, p.default.createElement(DropIndicator, (0, option.default)({
              GTMValue : targetHandlerInfos,
              rotateRefreshBtn : newSelectionEnd,
              onRefreshBtnClick : function() {
                self.handleRefreshBtnClick();
              },
              onClickShowAuditInfo : function() {
                return self.setState({
                  showAuditInfo : !self.state.showAuditInfo
                });
              },
              showAuditInfo : this.state.showAuditInfo
            }, this.props)), this.state.showAuditInfo ? p.default.createElement(plan.default, null) : p.default.createElement("div", null, p.default.createElement(FormioElement, {
              GTMValue : targetHandlerInfos,
              tabList : tabList,
              defaultChannel : this.state.defaultChannel,
              onMenuClick : function(name, value) {
                self.handleMenuClick(name, value);
              },
              onMoreClick : function() {
                self.handleMoreClick();
              }
            }), end ? p.default.createElement(_DraggableCore2.default, {
              fetchNumber : end,
              showRefreshTip : idnum2expr
            }) : null, p.default.createElement(filter.default, {
              handleScroll : function(name) {
                return self.handleScroll(name);
              }
            }, p.default.createElement(TodosLogin, {
              GTMValue : targetHandlerInfos,
              listData : info[c] || [],
              tips : tips,
              currentChannel : c,
              addADMaterial : function(name) {
                self.handleAddADMaterial(name);
              }
            })), p.default.createElement(top_up.default, {
              loadGTMScript : function(dappId) {
                self.handleLoadGTMScript(dappId);
              }
            }), !this.props.hideDownloadBanner && p.default.createElement(ControlledText, null)));
          }
        }]), Tile;
      }(Path.Component);
      Item.propTypes = {
        topMenuInfo : _propTypes2.default.object,
        GTMValue : _propTypes2.default.object,
        className : _propTypes2.default.string,
        hideBonus : _propTypes2.default.bool,
        hideDownloadBanner : _propTypes2.default.bool,
        isLite : _propTypes2.default.bool,
        Header : _propTypes2.default.func,
        TopMenu : _propTypes2.default.func,
        MainContent : _propTypes2.default.func,
        DownloadBanner : _propTypes2.default.func
      };
      module.exports = Item;
    }).call(id, require("gXQ3"));
  },
  "oem/" : function(module, root, scale) {
    /**
     * @param {!Object} name
     * @param {string} value
     * @return {undefined}
     */
    function add(name, value) {
      if (name.classList) {
        name.classList.add(value);
      } else {
        if (!(0, i.default)(name, value)) {
          if ("string" == typeof name.className) {
            /** @type {string} */
            name.className = name.className + " " + value;
          } else {
            name.setAttribute("class", (name.className && name.className.baseVal || "") + " " + value);
          }
        }
      }
    }
    Object.defineProperty(root, "__esModule", {
      value : true
    });
    /** @type {function(!Object, string): undefined} */
    root.default = add;
    var a = scale("uJiS");
    var i = function(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }(a);
    /** @type {function(!Object, string): undefined} */
    module.exports = root.default;
  },
  onnB : function(module, data) {
    /**
     * @return {undefined}
     */
    function Base() {
      /** @type {!Array} */
      this._defaults = [];
    }
    ["use", "on", "once", "set", "query", "type", "accept", "auth", "withCredentials", "sortQuery", "retry", "ok", "redirects", "timeout", "buffer", "serialize", "parse", "ca", "key", "pfx", "cert"].forEach(function(name) {
      /**
       * @return {?}
       */
      Base.prototype[name] = function() {
        return this._defaults.push({
          fn : name,
          arguments : arguments
        }), this;
      };
    });
    /**
     * @param {undefined} context
     * @return {undefined}
     */
    Base.prototype._setDefaults = function(context) {
      this._defaults.forEach(function(call) {
        context[call.fn].apply(context, call.arguments);
      });
    };
    /** @type {function(): undefined} */
    module.exports = Base;
  },
  p7ii : function(module, exports, __webpack_require__) {
    module.exports = {
      default : __webpack_require__("Jfdv"),
      __esModule : true
    };
  },
  pcGs : function(module, layer, $) {
    /**
     * @param {!Object} name
     * @return {?}
     */
    function ResponseBase(name) {
      if (name) {
        return mixin(name);
      }
    }
    /**
     * @param {!Object} object
     * @return {?}
     */
    function mixin(object) {
      var key;
      for (key in ResponseBase.prototype) {
        object[key] = ResponseBase.prototype[key];
      }
      return object;
    }
    var self = $("CDT0");
    /** @type {function(!Object): ?} */
    module.exports = ResponseBase;
    /**
     * @param {string} name
     * @return {?}
     */
    ResponseBase.prototype.get = function(name) {
      return this.header[name.toLowerCase()];
    };
    /**
     * @param {!Object} header
     * @return {undefined}
     */
    ResponseBase.prototype._setHeaderProperties = function(header) {
      var value = header["content-type"] || "";
      this.type = self.type(value);
      var a = self.params(value);
      var prop;
      for (prop in a) {
        this[prop] = a[prop];
      }
      this.links = {};
      try {
        if (header.link) {
          this.links = self.parseLinks(header.link);
        }
      } catch (e) {
      }
    };
    /**
     * @param {number} status
     * @return {undefined}
     */
    ResponseBase.prototype._setStatusProperties = function(status) {
      /** @type {number} */
      var type = status / 100 | 0;
      this.status = this.statusCode = status;
      /** @type {number} */
      this.statusType = type;
      /** @type {boolean} */
      this.info = 1 == type;
      /** @type {boolean} */
      this.ok = 2 == type;
      /** @type {boolean} */
      this.redirect = 3 == type;
      /** @type {boolean} */
      this.clientError = 4 == type;
      /** @type {boolean} */
      this.serverError = 5 == type;
      this.error = (4 == type || 5 == type) && this.toError();
      /** @type {boolean} */
      this.accepted = 202 == status;
      /** @type {boolean} */
      this.noContent = 204 == status;
      /** @type {boolean} */
      this.badRequest = 400 == status;
      /** @type {boolean} */
      this.unauthorized = 401 == status;
      /** @type {boolean} */
      this.notAcceptable = 406 == status;
      /** @type {boolean} */
      this.forbidden = 403 == status;
      /** @type {boolean} */
      this.notFound = 404 == status;
    };
  },
  pnWs : function(mixin, args, parseAsUTC) {
    /**
     * @param {!Array} array
     * @param {!Function} fn
     * @return {?}
     */
    function normalize(array, fn) {
      if (array.map) {
        return array.map(fn);
      }
      /** @type {!Array} */
      var r = [];
      /** @type {number} */
      var i = 0;
      for (; i < array.length; i++) {
        r.push(fn(array[i], i));
      }
      return r;
    }
    /**
     * @param {!Object} v
     * @return {?}
     */
    var stringifyPrimitive = function(v) {
      switch(typeof v) {
        case "string":
          return v;
        case "boolean":
          return v ? "true" : "false";
        case "number":
          return isFinite(v) ? v : "";
        default:
          return "";
      }
    };
    /**
     * @param {!Object} name
     * @param {string} str
     * @param {string} parent
     * @param {string} obj
     * @return {?}
     */
    mixin.exports = function(name, str, parent, obj) {
      return str = str || "&", parent = parent || "=", null === name && (name = void 0), "object" == typeof name ? normalize(recurse(name), function(k) {
        var prefix = encodeURIComponent(stringifyPrimitive(k)) + parent;
        return isNaN(name[k]) ? normalize(name[k], function(name) {
          return prefix + encodeURIComponent(stringifyPrimitive(name));
        }).join(str) : prefix + encodeURIComponent(stringifyPrimitive(name[k]));
      }).join(str) : obj ? encodeURIComponent(stringifyPrimitive(obj)) + parent + encodeURIComponent(stringifyPrimitive(name)) : "";
    };
    /** @type {function(*): boolean} */
    var isNaN = Array.isArray || function(obj) {
      return "[object Array]" === Object.prototype.toString.call(obj);
    };
    /** @type {function(!Object): !Array<string>} */
    var recurse = Object.keys || function(name) {
      /** @type {!Array} */
      var colorDist = [];
      var n;
      for (n in name) {
        if (Object.prototype.hasOwnProperty.call(name, n)) {
          colorDist.push(n);
        }
      }
      return colorDist;
    };
  },
  "s+Cy" : function(formatters, customFormatters) {
  },
  tF0L : function(module, selector, convertToImages) {
    /** @type {function(this:string, (RegExp|null|string), (!Function|null|string)): string} */
    var replace = String.prototype.replace;
    /** @type {!RegExp} */
    var reUnescape = /%20/g;
    module.exports = {
      default : "RFC3986",
      formatters : {
        RFC1738 : function(value) {
          return replace.call(value, reUnescape, "+");
        },
        RFC3986 : function(value) {
          return value;
        }
      },
      RFC1738 : "RFC1738",
      RFC3986 : "RFC3986"
    };
  },
  uGEv : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
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
     * @param {!Object} e
     * @param {!Object} t
     * @return {undefined}
     */
    function _inherits(e, t) {
      if ("function" != typeof t && null !== t) {
        throw new TypeError("Super expression must either be null or a function, not " + typeof t);
      }
      /** @type {!Object} */
      e.prototype = Object.create(t && t.prototype, {
        constructor : {
          value : e,
          enumerable : false,
          writable : true,
          configurable : true
        }
      });
      if (t) {
        if (Object.setPrototypeOf) {
          Object.setPrototypeOf(e, t);
        } else {
          /** @type {!Object} */
          e.__proto__ = t;
        }
      }
    }
    /** @type {boolean} */
    exports.__esModule = true;
    /** @type {function(!Object, ...(Object|null)): !Object} */
    var _extends = Object.assign || function(name) {
      /** @type {number} */
      var index = 1;
      for (; index < arguments.length; index++) {
        var options = arguments[index];
        var option;
        for (option in options) {
          if (Object.prototype.hasOwnProperty.call(options, option)) {
            name[option] = options[option];
          }
        }
      }
      return name;
    };
    var _react = __webpack_require__("V80v");
    var _react2 = _interopRequireDefault(_react);
    var _normalizeDataUri = __webpack_require__("nhKt");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("LHhu");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _CalendarDay = __webpack_require__("mr6U");
    var _CalendarDay2 = _interopRequireDefault(_CalendarDay);
    var _PropTypes = __webpack_require__("MKUs");
    var defaultProps = (_PropTypes.nameShape.isRequired, _normalizeDataUri2.default.bool, _normalizeDataUri2.default.bool, _normalizeDataUri2.default.bool, (0, _PropTypes.transitionTimeout)("Appear"), (0, _PropTypes.transitionTimeout)("Enter"), (0, _PropTypes.transitionTimeout)("Leave"), {
      transitionAppear : false,
      transitionEnter : true,
      transitionLeave : true
    });
    var CSSTransitionGroup = function(_React$Component) {
      /**
       * @return {?}
       */
      function CSSTransitionGroup() {
        var i;
        var _this;
        var _ret;
        _classCallCheck(this, CSSTransitionGroup);
        /** @type {number} */
        var _len8 = arguments.length;
        /** @type {!Array} */
        var args = Array(_len8);
        /** @type {number} */
        var _key8 = 0;
        for (; _key8 < _len8; _key8++) {
          args[_key8] = arguments[_key8];
        }
        return i = _this = _possibleConstructorReturn(this, _React$Component.call.apply(_React$Component, [this].concat(args))), _this._wrapChild = function(child) {
          return _react2.default.createElement(_CalendarDay2.default, {
            name : _this.props.transitionName,
            appear : _this.props.transitionAppear,
            enter : _this.props.transitionEnter,
            leave : _this.props.transitionLeave,
            appearTimeout : _this.props.transitionAppearTimeout,
            enterTimeout : _this.props.transitionEnterTimeout,
            leaveTimeout : _this.props.transitionLeaveTimeout
          }, child);
        }, _ret = i, _possibleConstructorReturn(_this, _ret);
      }
      return _inherits(CSSTransitionGroup, _React$Component), CSSTransitionGroup.prototype.render = function() {
        return _react2.default.createElement(_UiIcon2.default, _extends({}, this.props, {
          childFactory : this._wrapChild
        }));
      }, CSSTransitionGroup;
    }(_react2.default.Component);
    /** @type {string} */
    CSSTransitionGroup.displayName = "CSSTransitionGroup";
    CSSTransitionGroup.propTypes = {};
    CSSTransitionGroup.defaultProps = defaultProps;
    exports.default = CSSTransitionGroup;
    module.exports = exports.default;
  },
  uJiS : function(module, exports, __weex_require__) {
    /**
     * @param {!Object} name
     * @param {string} type
     * @return {?}
     */
    function add(name, type) {
      return name.classList ? !!type && name.classList.contains(type) : -1 !== (" " + (name.className.baseVal || name.className) + " ").indexOf(" " + type + " ");
    }
    Object.defineProperty(exports, "__esModule", {
      value : true
    });
    /** @type {function(!Object, string): ?} */
    exports.default = add;
    /** @type {function(!Object, string): ?} */
    module.exports = exports.default;
  },
  w2KC : function(module, exports, __weex_require__) {
    Object.defineProperty(exports, "__esModule", {
      value : true
    });
    exports.animationEnd = exports.animationDelay = exports.animationTiming = exports.animationDuration = exports.animationName = exports.transitionEnd = exports.transitionDuration = exports.transitionDelay = exports.transitionTiming = exports.transitionProperty = exports.transform = void 0;
    var storage = __weex_require__("/BaA");
    var initialState = function(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }(storage);
    /** @type {string} */
    var transform = "transform";
    var prefix = void 0;
    var transitionEnd = void 0;
    var animationEnd = void 0;
    var transitionProperty = void 0;
    var transitionDuration = void 0;
    var transitionTiming = void 0;
    var transitionDelay = void 0;
    var animationName = void 0;
    var animationDuration = void 0;
    var animationTiming = void 0;
    var animationDelay = void 0;
    if (initialState.default) {
      var _getTransitionPropert = function() {
        /** @type {!CSSStyleDeclaration} */
        var style = document.createElement("div").style;
        var transitions = {
          O : function(s) {
            return "o" + s.toLowerCase();
          },
          Moz : function(s) {
            return s.toLowerCase();
          },
          Webkit : function(e) {
            return "webkit" + e;
          },
          ms : function(type) {
            return "MS" + type;
          }
        };
        /** @type {!Array<string>} */
        var parts = Object.keys(transitions);
        var transitionEnd = void 0;
        var animationEnd = void 0;
        /** @type {string} */
        var flag = "";
        /** @type {number} */
        var i = 0;
        for (; i < parts.length; i++) {
          /** @type {string} */
          var vendor = parts[i];
          if (vendor + "TransitionProperty" in style) {
            /** @type {string} */
            flag = "-" + vendor.toLowerCase();
            transitionEnd = transitions[vendor]("TransitionEnd");
            animationEnd = transitions[vendor]("AnimationEnd");
            break;
          }
        }
        return !transitionEnd && "transitionProperty" in style && (transitionEnd = "transitionend"), !animationEnd && "animationName" in style && (animationEnd = "animationend"), style = null, {
          animationEnd : animationEnd,
          transitionEnd : transitionEnd,
          prefix : flag
        };
      }();
      prefix = _getTransitionPropert.prefix;
      exports.transitionEnd = transitionEnd = _getTransitionPropert.transitionEnd;
      exports.animationEnd = animationEnd = _getTransitionPropert.animationEnd;
      /** @type {string} */
      exports.transform = transform = prefix + "-" + transform;
      /** @type {string} */
      exports.transitionProperty = transitionProperty = prefix + "-transition-property";
      /** @type {string} */
      exports.transitionDuration = transitionDuration = prefix + "-transition-duration";
      /** @type {string} */
      exports.transitionDelay = transitionDelay = prefix + "-transition-delay";
      /** @type {string} */
      exports.transitionTiming = transitionTiming = prefix + "-transition-timing-function";
      /** @type {string} */
      exports.animationName = animationName = prefix + "-animation-name";
      /** @type {string} */
      exports.animationDuration = animationDuration = prefix + "-animation-duration";
      /** @type {string} */
      exports.animationTiming = animationTiming = prefix + "-animation-delay";
      /** @type {string} */
      exports.animationDelay = animationDelay = prefix + "-animation-timing-function";
    }
    /** @type {string} */
    exports.transform = transform;
    /** @type {(string|undefined)} */
    exports.transitionProperty = transitionProperty;
    /** @type {(string|undefined)} */
    exports.transitionTiming = transitionTiming;
    /** @type {(string|undefined)} */
    exports.transitionDelay = transitionDelay;
    /** @type {(string|undefined)} */
    exports.transitionDuration = transitionDuration;
    exports.transitionEnd = transitionEnd;
    /** @type {(string|undefined)} */
    exports.animationName = animationName;
    /** @type {(string|undefined)} */
    exports.animationDuration = animationDuration;
    /** @type {(string|undefined)} */
    exports.animationTiming = animationTiming;
    /** @type {(string|undefined)} */
    exports.animationDelay = animationDelay;
    exports.animationEnd = animationEnd;
    exports.default = {
      transform : transform,
      end : transitionEnd,
      property : transitionProperty,
      timing : transitionTiming,
      delay : transitionDelay,
      duration : transitionDuration
    };
  },
  wFHU : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _normalizeDataUri = __webpack_require__("iltz");
    var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
    var _UiIcon = __webpack_require__("fvPU");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("hJ6a");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _deepAssign = __webpack_require__("mRYa");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _UiRippleInk = __webpack_require__("IJ1K");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    var Popover = function(leftFence) {
      /**
       * @return {?}
       */
      function ReflexElement() {
        (0, _UiIcon2.default)(this, ReflexElement);
        var _this = (0, _deepAssign2.default)(this, (ReflexElement.__proto__ || (0, _normalizeDataUri2.default)(ReflexElement)).call(this));
        return _this.handleScroll = _this.handleScroll.bind(_this), _this.handleTouchStart = _this.handleTouchStart.bind(_this), _this.handleTouchEnd = _this.handleTouchEnd.bind(_this), _this.state = {
          scrollY : 0,
          touchStartY : 0
        }, _this;
      }
      return (0, _UiRippleInk2.default)(ReflexElement, leftFence), (0, _classlist2.default)(ReflexElement, [{
        key : "componentDidMount",
        value : function() {
          window.addEventListener("scroll", this.handleScroll);
          window.addEventListener("touchstart", this.handleTouchStart);
          window.addEventListener("touchend", this.handleTouchEnd);
        }
      }, {
        key : "componentWillUnmount",
        value : function() {
          window.removeEventListener("scroll", this.handleScroll);
          window.removeEventListener("touchstart", this.handleTouchStart);
          window.removeEventListener("touchend", this.handleTouchEnd);
        }
      }, {
        key : "handleScroll",
        value : function(name) {
          /** @type {number} */
          var scrollOffset = 100 * (window.responsive || {
            dpr : 1
          }).dpr;
          /** @type {number} */
          var documentHeight = document.body.scrollHeight;
          if ((window.scrollY || window.pageYOffset || document.body.scrollTop || document.documentElement.scrollTop) >= documentHeight - window.innerHeight - scrollOffset) {
            this.props.handleScroll("append");
          }
        }
      }, {
        key : "handleTouchStart",
        value : function(name) {
          var cursor_y = name.changedTouches[0].clientY;
          this.setState({
            touchStartY : cursor_y
          });
          /** @type {number} */
          var scrollY = window.scrollY || window.pageYOffset || document.body.scrollTop || document.documentElement.scrollTop;
          this.setState({
            scrollY : scrollY
          });
        }
      }, {
        key : "handleTouchEnd",
        value : function(name) {
          var pageY = name.changedTouches[0].clientY;
          if (this.state.scrollY <= 0) {
            if (pageY - this.state.touchStartY > 100) {
              name.preventDefault();
              this.props.handleScroll("prepend");
            }
          }
        }
      }, {
        key : "render",
        value : function() {
          return _prepareStyleProperties2.default.createElement("div", null, this.props.children);
        }
      }]), ReflexElement;
    }(_prepareStyleProperties.Component);
    Popover.propTypes = {
      handleScroll : _propTypes2.default.func,
      children : _propTypes2.default.oneOfType([_propTypes2.default.arrayOf(_propTypes2.default.node), _propTypes2.default.node])
    };
    Popover.defaultProps = {
      handleScroll : function() {
      }
    };
    module.exports = Popover;
  },
  wYmI : function(module, exports, __webpack_require__) {
    var getDocumentCollection = __webpack_require__("OPoG");
    var r = __webpack_require__("5z3G");
    /**
     * @param {!Object} e
     * @param {string} key
     * @return {undefined}
     */
    var check = function(e, key) {
      if (r(e), !getDocumentCollection(key) && null !== key) {
        throw TypeError(key + ": can't set as prototype!");
      }
    };
    module.exports = {
      set : Object.setPrototypeOf || ("__proto__" in {} ? function(e, notTranslate, _) {
        try {
          _ = __webpack_require__("QgN4")(Function.call, __webpack_require__("faNU").f(Object.prototype, "__proto__").set, 2);
          _(e, []);
          /** @type {boolean} */
          notTranslate = !(e instanceof Array);
        } catch (e) {
          /** @type {boolean} */
          notTranslate = true;
        }
        return function(params, a) {
          return check(params, a), notTranslate ? params.__proto__ = a : _(params, a), params;
        };
      }({}, false) : void 0),
      check : check
    };
  },
  wtgB : function(module, exports, __webpack_require__) {
    (function(process, global) {
      !function(addedRenderer, factory) {
        module.exports = factory();
      }(0, function() {
        /**
         * @param {!Object} value
         * @return {?}
         */
        function isObject(value) {
          /** @type {string} */
          var type = typeof value;
          return null !== value && ("object" === type || "function" === type);
        }
        /**
         * @param {!Object} value
         * @return {?}
         */
        function isFunction(value) {
          return "function" == typeof value;
        }
        /**
         * @param {?} fn
         * @return {undefined}
         */
        function setScheduler(fn) {
          setTimeout = fn;
        }
        /**
         * @param {?} asapFn
         * @return {undefined}
         */
        function setAsap(asapFn) {
          asap = asapFn;
        }
        /**
         * @return {?}
         */
        function fetch() {
          return void 0 !== query ? function() {
            query(callback);
          } : next();
        }
        /**
         * @return {?}
         */
        function next() {
          /** @type {function((!Function|null|string), number=, ...*): number} */
          var delay = setTimeout;
          return function() {
            return delay(callback, 1);
          };
        }
        /**
         * @return {undefined}
         */
        function callback() {
          /** @type {number} */
          var i = 0;
          for (; i < lib$rsvp$asap$$len; i = i + 2) {
            (0, lib$rsvp$asap$$queue[i])(lib$rsvp$asap$$queue[i + 1]);
            lib$rsvp$asap$$queue[i] = void 0;
            lib$rsvp$asap$$queue[i + 1] = void 0;
          }
          /** @type {number} */
          lib$rsvp$asap$$len = 0;
        }
        /**
         * @param {!Function} onFulfillment
         * @param {!Function} onRejection
         * @return {?}
         */
        function then(onFulfillment, onRejection) {
          var parent = this;
          var child = new this.constructor(noop);
          if (void 0 === child[PROMISE_ID]) {
            makePromise(child);
          }
          var state = parent._state;
          if (state) {
            var callback = arguments[state - 1];
            asap(function() {
              return invokeCallback(state, child, callback, parent._result);
            });
          } else {
            subscribe(parent, child, onFulfillment, onRejection);
          }
          return child;
        }
        /**
         * @param {!Object} value
         * @return {?}
         */
        function resolve(value) {
          var Promise = this;
          if (value && "object" == typeof value && value.constructor === Promise) {
            return value;
          }
          var promise = new Promise(noop);
          return _resolve(promise, value), promise;
        }
        /**
         * @return {undefined}
         */
        function noop() {
        }
        /**
         * @return {?}
         */
        function selfFulfillment() {
          return new TypeError("You cannot resolve a promise with itself");
        }
        /**
         * @return {?}
         */
        function cannotReturnOwn() {
          return new TypeError("A promises callback cannot return that same promise.");
        }
        /**
         * @param {!Object} promise
         * @return {?}
         */
        function getThen(promise) {
          try {
            return promise.then;
          } catch (fn) {
            return $.error = fn, $;
          }
        }
        /**
         * @param {!Function} then
         * @param {!Object} value
         * @param {!Function} fulfillmentHandler
         * @param {!Function} rejectionHandler
         * @return {?}
         */
        function tryThen(then, value, fulfillmentHandler, rejectionHandler) {
          try {
            then.call(value, fulfillmentHandler, rejectionHandler);
          } catch (e) {
            return e;
          }
        }
        /**
         * @param {!Object} promise
         * @param {!Object} thenable
         * @param {!Object} then
         * @return {undefined}
         */
        function handleForeignThenable(promise, thenable, then) {
          asap(function(promise) {
            /** @type {boolean} */
            var sealed = false;
            var error = tryThen(then, thenable, function(value) {
              if (!sealed) {
                /** @type {boolean} */
                sealed = true;
                if (thenable !== value) {
                  _resolve(promise, value);
                } else {
                  fulfill(promise, value);
                }
              }
            }, function(value) {
              if (!sealed) {
                /** @type {boolean} */
                sealed = true;
                _reject(promise, value);
              }
            }, "Settle: " + (promise._label || " unknown promise"));
            if (!sealed && error) {
              /** @type {boolean} */
              sealed = true;
              _reject(promise, error);
            }
          }, promise);
        }
        /**
         * @param {!Object} promise
         * @param {!Object} thenable
         * @return {undefined}
         */
        function handleOwnThenable(promise, thenable) {
          if (thenable._state === FULFILLED) {
            fulfill(promise, thenable._result);
          } else {
            if (thenable._state === REJECTED) {
              _reject(promise, thenable._result);
            } else {
              subscribe(thenable, void 0, function(value) {
                return _resolve(promise, value);
              }, function(value) {
                return _reject(promise, value);
              });
            }
          }
        }
        /**
         * @param {!Object} promise
         * @param {!Object} maybeThenable
         * @param {!Object} then$$
         * @return {undefined}
         */
        function handleMaybeThenable(promise, maybeThenable, then$$) {
          if (maybeThenable.constructor === promise.constructor && then$$ === then && maybeThenable.constructor.resolve === resolve) {
            handleOwnThenable(promise, maybeThenable);
          } else {
            if (then$$ === $) {
              _reject(promise, $.error);
              /** @type {null} */
              $.error = null;
            } else {
              if (void 0 === then$$) {
                fulfill(promise, maybeThenable);
              } else {
                if (isFunction(then$$)) {
                  handleForeignThenable(promise, maybeThenable, then$$);
                } else {
                  fulfill(promise, maybeThenable);
                }
              }
            }
          }
        }
        /**
         * @param {!Object} promise
         * @param {!Object} value
         * @return {undefined}
         */
        function _resolve(promise, value) {
          if (promise === value) {
            _reject(promise, selfFulfillment());
          } else {
            if (isObject(value)) {
              handleMaybeThenable(promise, value, getThen(value));
            } else {
              fulfill(promise, value);
            }
          }
        }
        /**
         * @param {!Request} promise
         * @return {undefined}
         */
        function publishRejection(promise) {
          if (promise._onerror) {
            promise._onerror(promise._result);
          }
          publish(promise);
        }
        /**
         * @param {!Object} promise
         * @param {!Object} value
         * @return {undefined}
         */
        function fulfill(promise, value) {
          if (promise._state === PENDING) {
            /** @type {!Object} */
            promise._result = value;
            /** @type {number} */
            promise._state = FULFILLED;
            if (0 !== promise._subscribers.length) {
              asap(publish, promise);
            }
          }
        }
        /**
         * @param {!Object} promise
         * @param {!Object} reason
         * @return {undefined}
         */
        function _reject(promise, reason) {
          if (promise._state === PENDING) {
            /** @type {number} */
            promise._state = REJECTED;
            /** @type {!Object} */
            promise._result = reason;
            asap(publishRejection, promise);
          }
        }
        /**
         * @param {!Object} parent
         * @param {!Object} child
         * @param {!Function} onFulfillment
         * @param {!Function} onRejection
         * @return {undefined}
         */
        function subscribe(parent, child, onFulfillment, onRejection) {
          var _subscribers = parent._subscribers;
          var length = _subscribers.length;
          /** @type {null} */
          parent._onerror = null;
          /** @type {!Object} */
          _subscribers[length] = child;
          /** @type {!Function} */
          _subscribers[length + FULFILLED] = onFulfillment;
          /** @type {!Function} */
          _subscribers[length + REJECTED] = onRejection;
          if (0 === length && parent._state) {
            asap(publish, parent);
          }
        }
        /**
         * @param {!Request} promise
         * @return {undefined}
         */
        function publish(promise) {
          var subscribers = promise._subscribers;
          var settled = promise._state;
          if (0 !== subscribers.length) {
            var child = void 0;
            var callback = void 0;
            var detail = promise._result;
            /** @type {number} */
            var i = 0;
            for (; i < subscribers.length; i = i + 3) {
              child = subscribers[i];
              callback = subscribers[i + settled];
              if (child) {
                invokeCallback(settled, child, callback, detail);
              } else {
                callback(detail);
              }
            }
            /** @type {number} */
            promise._subscribers.length = 0;
          }
        }
        /**
         * @param {!Object} callback
         * @param {number} detail
         * @return {?}
         */
        function tryCatch(callback, detail) {
          try {
            return callback(detail);
          } catch (fn) {
            return $.error = fn, $;
          }
        }
        /**
         * @param {number} settled
         * @param {!Object} promise
         * @param {!Object} callback
         * @param {number} detail
         * @return {?}
         */
        function invokeCallback(settled, promise, callback, detail) {
          var hasCallback = isFunction(callback);
          var value = void 0;
          var error = void 0;
          var succeeded = void 0;
          var l = void 0;
          if (hasCallback) {
            if (value = tryCatch(callback, detail), value === $ ? (l = true, error = value.error, value.error = null) : succeeded = true, promise === value) {
              return void _reject(promise, cannotReturnOwn());
            }
          } else {
            /** @type {number} */
            value = detail;
            /** @type {boolean} */
            succeeded = true;
          }
          if (!(promise._state !== PENDING)) {
            if (hasCallback && succeeded) {
              _resolve(promise, value);
            } else {
              if (l) {
                _reject(promise, error);
              } else {
                if (settled === FULFILLED) {
                  fulfill(promise, value);
                } else {
                  if (settled === REJECTED) {
                    _reject(promise, value);
                  }
                }
              }
            }
          }
        }
        /**
         * @param {!Object} promise
         * @param {!Function} callback
         * @return {undefined}
         */
        function each(promise, callback) {
          try {
            callback(function(value) {
              _resolve(promise, value);
            }, function(value) {
              _reject(promise, value);
            });
          } catch (reason) {
            _reject(promise, reason);
          }
        }
        /**
         * @return {?}
         */
        function fakeToken() {
          return id++;
        }
        /**
         * @param {!Object} promise
         * @return {undefined}
         */
        function makePromise(promise) {
          /** @type {number} */
          promise[PROMISE_ID] = id++;
          promise._state = void 0;
          promise._result = void 0;
          /** @type {!Array} */
          promise._subscribers = [];
        }
        /**
         * @return {?}
         */
        function validationError() {
          return new Error("Array Methods must be provided an Array");
        }
        /**
         * @param {?} entries
         * @return {?}
         */
        function all(entries) {
          return (new Enumerator(this, entries)).promise;
        }
        /**
         * @param {!Object} a
         * @return {?}
         */
        function race(a) {
          var c = this;
          return new c(isArray(a) ? function(success, reject) {
            var az = a.length;
            /** @type {number} */
            var i = 0;
            for (; i < az; i++) {
              c.resolve(a[i]).then(success, reject);
            }
          } : function(canCreateDiscussions, reject) {
            return reject(new TypeError("You must pass an array to race."));
          });
        }
        /**
         * @param {?} reason
         * @return {?}
         */
        function reject(reason) {
          var Constructor = this;
          var promise = new Constructor(noop);
          return _reject(promise, reason), promise;
        }
        /**
         * @return {?}
         */
        function splitText() {
          throw new TypeError("You must pass a resolver function as the first argument to the promise constructor");
        }
        /**
         * @return {?}
         */
        function getDate() {
          throw new TypeError("Failed to construct 'Promise': Please use the 'new' operator, this object constructor cannot be called as a function.");
        }
        /**
         * @return {undefined}
         */
        function polyfill() {
          var local = void 0;
          if (void 0 !== global) {
            /** @type {number} */
            local = global;
          } else {
            if ("undefined" != typeof self) {
              /** @type {!Window} */
              local = self;
            } else {
              try {
                local = Function("return this")();
              } catch (e) {
                throw new Error("polyfill failed because global object is unavailable in this environment");
              }
            }
          }
          var P = local.Promise;
          if (P) {
            /** @type {null} */
            var r = null;
            try {
              /** @type {string} */
              r = Object.prototype.toString.call(P.resolve());
            } catch (e) {
            }
            if ("[object Promise]" === r && !P.cast) {
              return;
            }
          }
          local.Promise = Promise;
        }
        var _isArray = void 0;
        /** @type {!Function} */
        _isArray = Array.isArray ? Array.isArray : function(obj) {
          return "[object Array]" === Object.prototype.toString.call(obj);
        };
        /** @type {!Function} */
        var isArray = _isArray;
        /** @type {number} */
        var lib$rsvp$asap$$len = 0;
        var query = void 0;
        var setTimeout = void 0;
        /**
         * @param {!Function} callback
         * @param {!Object} arg
         * @return {undefined}
         */
        var asap = function(callback, arg) {
          /** @type {!Function} */
          lib$rsvp$asap$$queue[lib$rsvp$asap$$len] = callback;
          /** @type {!Object} */
          lib$rsvp$asap$$queue[lib$rsvp$asap$$len + 1] = arg;
          if (2 === (lib$rsvp$asap$$len = lib$rsvp$asap$$len + 2)) {
            if (setTimeout) {
              setTimeout(callback);
            } else {
              rawAsap();
            }
          }
        };
        /** @type {(Window|undefined)} */
        var global = "undefined" != typeof window ? window : void 0;
        /** @type {(Window|{})} */
        var scope = global || {};
        var BrowserMutationObserver = scope.MutationObserver || scope.WebKitMutationObserver;
        /** @type {boolean} */
        var queryBoth = "undefined" == typeof self && void 0 !== process && "[object process]" === {}.toString.call(process);
        /** @type {boolean} */
        var rawDataIsList = "undefined" != typeof Uint8ClampedArray && "undefined" != typeof importScripts && "undefined" != typeof MessageChannel;
        /** @type {!Array} */
        var lib$rsvp$asap$$queue = new Array(1e3);
        var rawAsap = void 0;
        rawAsap = queryBoth ? function() {
          return function() {
            return process.nextTick(callback);
          };
        }() : BrowserMutationObserver ? function() {
          /** @type {number} */
          var t = 0;
          var observer = new BrowserMutationObserver(callback);
          /** @type {!Text} */
          var event = document.createTextNode("");
          return observer.observe(event, {
            characterData : true
          }), function() {
            /** @type {number} */
            event.data = t = ++t % 2;
          };
        }() : rawDataIsList ? function() {
          /** @type {!MessageChannel} */
          var channel = new MessageChannel;
          return channel.port1.onmessage = callback, function() {
            return channel.port2.postMessage(0);
          };
        }() : void 0 === global ? function() {
          try {
            var vertx = Function("return this")().require("vertx");
            return query = vertx.runOnLoop || vertx.runOnContext, fetch();
          } catch (e) {
            return next();
          }
        }() : next();
        /** @type {string} */
        var PROMISE_ID = Math.random().toString(36).substring(2);
        var PENDING = void 0;
        /** @type {number} */
        var FULFILLED = 1;
        /** @type {number} */
        var REJECTED = 2;
        var $ = {
          error : null
        };
        /** @type {number} */
        var id = 0;
        var Enumerator = function() {
          /**
           * @param {!Function} Constructor
           * @param {!Object} input
           * @return {undefined}
           */
          function Enumerator(Constructor, input) {
            /** @type {!Function} */
            this._instanceConstructor = Constructor;
            this.promise = new Constructor(noop);
            if (!this.promise[PROMISE_ID]) {
              makePromise(this.promise);
            }
            if (isArray(input)) {
              this.length = input.length;
              this._remaining = input.length;
              /** @type {!Array} */
              this._result = new Array(this.length);
              if (0 === this.length) {
                fulfill(this.promise, this._result);
              } else {
                this.length = this.length || 0;
                this._enumerate(input);
                if (0 === this._remaining) {
                  fulfill(this.promise, this._result);
                }
              }
            } else {
              _reject(this.promise, validationError());
            }
          }
          return Enumerator.prototype._enumerate = function(input) {
            /** @type {number} */
            var i = 0;
            for (; this._state === PENDING && i < input.length; i++) {
              this._eachEntry(input[i], i);
            }
          }, Enumerator.prototype._eachEntry = function(entry, i) {
            var c = this._instanceConstructor;
            var resolve$$ = c.resolve;
            if (resolve$$ === resolve) {
              var _then = getThen(entry);
              if (_then === then && entry._state !== PENDING) {
                this._settledAt(entry._state, i, entry._result);
              } else {
                if ("function" != typeof _then) {
                  this._remaining--;
                  /** @type {!Object} */
                  this._result[i] = entry;
                } else {
                  if (c === Promise) {
                    var promise = new c(noop);
                    handleMaybeThenable(promise, entry, _then);
                    this._willSettleAt(promise, i);
                  } else {
                    this._willSettleAt(new c(function(resolve$$) {
                      return resolve$$(entry);
                    }), i);
                  }
                }
              }
            } else {
              this._willSettleAt(resolve$$(entry), i);
            }
          }, Enumerator.prototype._settledAt = function(state, i, value) {
            var promise = this.promise;
            if (promise._state === PENDING) {
              this._remaining--;
              if (state === REJECTED) {
                _reject(promise, value);
              } else {
                /** @type {!Object} */
                this._result[i] = value;
              }
            }
            if (0 === this._remaining) {
              fulfill(promise, this._result);
            }
          }, Enumerator.prototype._willSettleAt = function(promise, i) {
            var enumerator = this;
            subscribe(promise, void 0, function(value) {
              return enumerator._settledAt(FULFILLED, i, value);
            }, function(value) {
              return enumerator._settledAt(REJECTED, i, value);
            });
          }, Enumerator;
        }();
        var Promise = function() {
          /**
           * @param {!Function} callback
           * @return {undefined}
           */
          function d(callback) {
            this[PROMISE_ID] = fakeToken();
            this._result = this._state = void 0;
            /** @type {!Array} */
            this._subscribers = [];
            if (noop !== callback) {
              if ("function" != typeof callback) {
                splitText();
              }
              if (this instanceof d) {
                each(this, callback);
              } else {
                getDate();
              }
            }
          }
          return d.prototype.catch = function(reject) {
            return this.then(null, reject);
          }, d.prototype.finally = function(callback) {
            var object = this;
            var f = object.constructor;
            return object.then(function(canCreateDiscussions) {
              return f.resolve(callback()).then(function() {
                return canCreateDiscussions;
              });
            }, function(canCreateDiscussions) {
              return f.resolve(callback()).then(function() {
                throw canCreateDiscussions;
              });
            });
          }, d;
        }();
        return Promise.prototype.then = then, Promise.all = all, Promise.race = race, Promise.resolve = resolve, Promise.reject = reject, Promise._setScheduler = setScheduler, Promise._setAsap = setAsap, Promise._asap = asap, Promise.polyfill = polyfill, Promise.Promise = Promise, Promise;
      });
    }).call(exports, __webpack_require__("RxL3"), __webpack_require__("dTv7"));
  },
  xDfE : function(module, exports, __webpack_require__) {
    /**
     * @param {!Object} obj
     * @return {?}
     */
    function _interopRequireDefault(obj) {
      return obj && obj.__esModule ? obj : {
        default : obj
      };
    }
    var _UiIcon = __webpack_require__("mZJ8");
    var _UiIcon2 = _interopRequireDefault(_UiIcon);
    var _classlist = __webpack_require__("iltz");
    var _classlist2 = _interopRequireDefault(_classlist);
    var _deepAssign = __webpack_require__("fvPU");
    var _deepAssign2 = _interopRequireDefault(_deepAssign);
    var _AboutPage = __webpack_require__("hJ6a");
    var _AboutPage2 = _interopRequireDefault(_AboutPage);
    var _AppDownload = __webpack_require__("mRYa");
    var _AppDownload2 = _interopRequireDefault(_AppDownload);
    var _UiRippleInk = __webpack_require__("IJ1K");
    var _UiRippleInk2 = _interopRequireDefault(_UiRippleInk);
    var _prepareStyleProperties = __webpack_require__("V80v");
    var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
    var _propTypes = __webpack_require__("nhKt");
    var _propTypes2 = _interopRequireDefault(_propTypes);
    var _noframeworkWaypoints = __webpack_require__("Cqu5");
    var _noframeworkWaypoints2 = _interopRequireDefault(_noframeworkWaypoints);
    __webpack_require__("RfGB");
    var PercentageSymbol = function(e) {
      /**
       * @param {?} props
       * @return {?}
       */
      function ReflexElement(props) {
        (0, _deepAssign2.default)(this, ReflexElement);
        var localTask = (0, _AppDownload2.default)(this, (ReflexElement.__proto__ || (0, _classlist2.default)(ReflexElement)).call(this, props));
        return localTask.state = {
          currentChannel : props.defaultChannel
        }, localTask;
      }
      return (0, _UiRippleInk2.default)(ReflexElement, e), (0, _AboutPage2.default)(ReflexElement, [{
        key : "onMenuClick",
        value : function(value) {
          if ("news_car" === value.currentTarget.dataset.channel) {
            return void(location.href = "https://m.dcdapp.com/?zt=tt_m_car");
          }
          var key = value.currentTarget.dataset.channel;
          var text = value.currentTarget.dataset.query;
          this.setState({
            currentChannel : key
          });
          if (this.props.onMenuClick) {
            this.props.onMenuClick(key, text);
          }
          value.preventDefault();
        }
      }, {
        key : "onMoreClick",
        value : function(name) {
          if (this.props.onMoreClick) {
            this.props.onMoreClick();
          }
          name.preventDefault();
        }
      }, {
        key : "componentDidMount",
        value : function() {
          var channelConfig = this.state.currentChannel;
          var artistTrack = this._topMenuList.querySelector('[data-channel="' + channelConfig + '"]');
          this.doTabSwitch(artistTrack);
        }
      }, {
        key : "componentDidUpdate",
        value : function() {
          var channelConfig = this.state.currentChannel;
          var artistTrack = this._topMenuList.querySelector('[data-channel="' + channelConfig + '"]');
          this.doTabSwitch(artistTrack);
        }
      }, {
        key : "doTabSwitch",
        value : function(value) {
          var target = value.parentNode;
          /** @type {!Object} */
          var icon = value;
          /** @type {number} */
          var timeBarWidth = document.body.clientWidth;
          var width = target.clientWidth;
          var y = target.scrollWidth;
          var x = target.scrollLeft;
          var size = icon.clientWidth;
          var _x = icon.getBoundingClientRect().left;
          var scroll_left = void 0;
          scroll_left = _x + x <= width / 2 - size / 2 ? 0 : _x + x > y - width / 2 - size / 2 ? Math.max(y - width, 0) : -timeBarWidth / 2 + size / 2 + _x + x;
          target.scrollLeft = scroll_left;
        }
      }, {
        key : "render",
        value : function() {
          var self = this;
          var data = this.props.tabList;
          var options = this.props.GTMValue || {};
          var filterText = options.hideTopMenuMore || this.props.hideTopMenuMore;
          var customCls = this.props.className || "";
          return _prepareStyleProperties2.default.createElement("div", {
            className : "top_menu_bar " + customCls
          }, filterText ? null : _prepareStyleProperties2.default.createElement("div", {
            className : "top_menu_more"
          }, _prepareStyleProperties2.default.createElement("div", {
            className : "list_shadow"
          }), _prepareStyleProperties2.default.createElement("a", {
            className : "more_btn",
            href : "javascript:void(0)",
            onClick : function(position) {
              return self.onMoreClick(position);
            }
          }, _prepareStyleProperties2.default.createElement("span", {
            className : "cross"
          }))), _prepareStyleProperties2.default.createElement("div", {
            className : "top_menu_list",
            ref : function(track) {
              /** @type {!Document} */
              self._topMenuList = track;
            }
          }, (0, _UiIcon2.default)(data).map(function(channel) {
            var c = (0, _noframeworkWaypoints2.default)("btn", {
              cur : channel === self.state.currentChannel
            });
            return _prepareStyleProperties2.default.createElement("a", {
              href : "javascript:void(0)",
              key : channel,
              "data-channel" : channel,
              "data-query" : "channel=" + channel,
              className : c,
              onClick : function(position) {
                return self.onMenuClick(position);
              }
            }, data[channel]);
          })));
        }
      }]), ReflexElement;
    }(_prepareStyleProperties.Component);
    PercentageSymbol.propTypes = {
      defaultChannel : _propTypes2.default.string,
      tabList : _propTypes2.default.object,
      GTMValue : _propTypes2.default.object,
      onMenuClick : _propTypes2.default.func,
      onMoreClick : _propTypes2.default.func,
      hideTopMenuMore : _propTypes2.default.bool,
      className : _propTypes2.default.string
    };
    module.exports = PercentageSymbol;
  },
  xPW0 : function(someChunks, module, require) {
    module.decode = module.parse = require("Ah8g");
    module.encode = module.stringify = require("pnWs");
  },
  xsko : function(formatters, customFormatters) {
  },
  yRjA : function(module, exports, __webpack_require__) {
    (function(jQuery) {
      /**
       * @param {!Object} obj
       * @return {?}
       */
      function _interopRequireDefault(obj) {
        return obj && obj.__esModule ? obj : {
          default : obj
        };
      }
      /**
       * @return {undefined}
       */
      function YM() {
      }
      /**
       * @return {?}
       */
      function write() {
        return !window.isListPage && _UiIcon2.default.browser.weixin;
      }
      /**
       * @return {undefined}
       */
      function trackGA() {
        !function(i, s, o, addedRenderer, r, a, editorElem) {
          /** @type {string} */
          i.GoogleAnalyticsObject = r;
          i[r] = i[r] || function() {
            (i[r].q = i[r].q || []).push(arguments);
          };
          /** @type {number} */
          i[r].l = 1 * new Date;
          /** @type {!Element} */
          a = s.createElement(o);
          /** @type {!Element} */
          editorElem = s.getElementsByTagName(o)[0];
          /** @type {number} */
          a.async = 1;
          /** @type {string} */
          a.src = "//www.google-analytics.com/analytics.js";
          editorElem.parentNode.insertBefore(a, editorElem);
        }(window, document, "script", 0, "ga");
      }
      /**
       * @return {undefined}
       */
      function setupVizAnalytics() {
        window.ga("create", "UA-28423340-36", "auto", "testTracker", {
          siteSpeedSampleRate : 100
        });
        /**
         * @param {string} data
         * @param {string} name
         * @param {!Object} value
         * @param {number} item
         * @param {?} meta
         * @return {undefined}
         */
        window.gaeventTest = function(data, name, value, item, meta) {
          console.log("gaTest:" + data + "," + name + "," + value);
          if ("event" !== data) {
            window.ga("testTracker.send", "event", data, name, value, void 0 !== item ? item : 1, meta);
          }
        };
      }
      /**
       * @return {?}
       */
      function close() {
        if (!_UiIcon2.default.browser.weixin) {
          return false;
        }
        var a;
        var object;
        try {
          a = sessionStorage.getItem("weixinlist_query");
          object = sessionStorage.getItem("weixinlist_count");
        } catch (deprecationWarning) {
          console.warn(deprecationWarning);
        }
        if (object && "1" === object) {
          var r = data.default.request(null, true);
          /** @type {string} */
          var key = location.hash;
          /** @type {string} */
          var port = location.host;
          var s = r;
          /** @type {string} */
          var c = location.pathname + "?" + a;
          history.replaceState(null, null, c);
          var value = jQuery.request(null, true);
          s = jQuery.extend({}, r, value, {
            weixin_list : 1
          });
          var _DOT_ = (0, _normalizeDataUri2.default)(s).map(function(i) {
            return i + "=" + s[i];
          }).join("&");
          /** @type {string} */
          var url = "//" + port + location.pathname + "?" + _DOT_ + key;
          history.replaceState(null, null, url);
        }
      }
      /**
       * @return {undefined}
       */
      function open() {
        /** @type {number} */
        var crop_growth = 17;
        if (write()) {
          /** @type {number} */
          crop_growth = 16;
        }
        if (_UiIcon2.default.browser.weixin) {
          /** @type {number} */
          crop_growth = 41;
        }
        /** @type {string} */
        var TRACKING_ID = "UA-28423340-" + crop_growth;
        if (navigator.userAgent.indexOf("ArticleStreamSdk") > -1 || "open" === data.default.request("utm_campaign")) {
          /** @type {string} */
          TRACKING_ID = "UA-28423340-11";
        } else {
          if ("m.ixigua.com" === location.host) {
            /** @type {string} */
            TRACKING_ID = "UA-28423340-51";
          }
        }
        window.ga("create", TRACKING_ID, "auto", {
          siteSpeedSampleRate : 100
        });
      }
      /**
       * @return {undefined}
       */
      function navigate() {
        /** @type {string} */
        var url = location.pathname;
        if (url && -1 !== url.indexOf("/sem/")) {
          window.ga("send", "pageview", {
            page : url
          });
        } else {
          window.ga("send", "pageview", location.pathname + location.search + location.hash);
        }
      }
      /**
       * @return {undefined}
       */
      function init() {
        var url = data.default.request("wxshare_count");
        if (!isNaN(url) && url > 0) {
          window.ga("set", "dimension1", url);
        }
        var category = data.default.request("wxshare_banner");
        if (!isNaN(category) && category > 0) {
          window.ga("set", "dimension10", category);
        }
        var page = data.default.request("readmore");
        if (!isNaN(page) && page > 0) {
          window.ga("set", "dimension2", page);
        }
        var contentExperimentId = data.default.hash("channel") || data.default.request("channel") || "__all__";
        if (contentExperimentId) {
          window.ga("set", "dimension4", contentExperimentId);
        }
        /** @type {number} */
        var id = Number(window.hasVideo);
        if (0 !== id && 1 !== id || window.ga("set", "dimension5", id), write()) {
          var url = data.default.request("app");
          if (url) {
            window.ga("set", "dimension6", url);
          }
          var category = data.default.request("utm_medium");
          if (category) {
            window.ga("set", "dimension7", category);
          }
          var aStatedRank = data.default.request("isappinstalled");
          if (!isNaN(aStatedRank) && aStatedRank >= 0) {
            window.ga("set", "dimension8", aStatedRank - 0 ? 1 : 0);
          }
        } else {
          window.ga(function($this) {
            var url = $this.get("clientId");
            window.ga("set", "dimension7", url);
          });
          window.ga("set", "dimension6", data.default.getBrowserName());
          window.ga("set", "dimension8", navigator.userAgent);
          window.ga("set", "dimension9", window.city || "");
        }
        /** @type {string} */
        var originalPath = location.pathname;
        if (originalPath && -1 !== originalPath.indexOf("/sem/") && data.default.request("atdl")) {
          window.ga("set", "dimension5", data.default.request("atdl"));
        }
      }
      /**
       * @return {?}
       */
      function parse() {
        /** @type {number} */
        var b = 2;
        if (write()) {
          /** @type {number} */
          b = 5;
        }
        var total_pageviews_raw = _classlist2.default.getTTWebID();
        /** @type {(number|undefined)} */
        var a = null !== total_pageviews_raw ? parseInt(total_pageviews_raw) % 100 : void 0;
        return !isNaN(a) && a >= 1 && a <= b;
      }
      /**
       * @return {undefined}
       */
      function load() {
        /** @type {!Image} */
        var e = new Image;
        /** @type {string} */
        e.src = location.protocol + "//" + location.hostname + "/__utm.gif?utmp=" + encodeURIComponent(location.href);
        /**
         * @param {?} fileLoadedEvent
         * @return {undefined}
         */
        e.onload = function(fileLoadedEvent) {
          jQuery(this).remove();
        };
        jQuery(function() {
          jQuery("body").append(e);
        });
        window.addEventListener("error", function(exception, blob, undefined) {
          /** @type {!Object} */
          var error = exception;
          /** @type {string} */
          var file = blob;
          /** @type {string} */
          var lineNumber = undefined;
          if ("object" === (void 0 === exception ? "undefined" : (0, _prepareStyleProperties2.default)(exception))) {
            error = exception.message;
            file = exception.fileName;
            lineNumber = exception.lineNumber;
          }
          /** @type {string} */
          var message = "[" + file + " (" + lineNumber + ")]" + error;
          if (Math.floor(100 * Math.random()) < 10) {
            window.ga("send", "exception", {
              exDescription : message,
              exFatal : false
            });
          }
        });
      }
      /**
       * @param {string} url
       * @param {string} name
       * @param {!Object} label
       * @param {number} data
       * @param {?} meta
       * @return {undefined}
       */
      function report(url, name, label, data, meta) {
        console.log("ga:" + url + "," + name + "," + label);
        window.ga("send", "event", url, name, label, void 0 !== data ? data : 1, meta);
      }
      /**
       * @param {string} type
       * @return {undefined}
       */
      function search(type) {
        window.ga("send", "pageview", location.pathname + location.search + location.hash);
        console.log("ga:pageview", location.pathname + location.search + location.hash);
      }
      /**
       * @return {undefined}
       */
      function api() {
        if (!write()) {
          (function() {
            /** @type {!Element} */
            var youtube_script = document.createElement("script");
            /** @type {string} */
            youtube_script.src = "//hm.baidu.com/hm.js?23e756494636a870d09e32c92e64fdd6";
            /** @type {!Element} */
            var wafCss = document.getElementsByTagName("script")[0];
            wafCss.parentNode.insertBefore(youtube_script, wafCss);
          })();
        }
      }
      /**
       * @return {undefined}
       */
      function setupGoogle() {
        window._taq.push(["create", "TT-growth-01", "m.toutiao.com"]);
        window._taq.push(["trackinit", "mobile", "wap", 1]);
        (function() {
          /** @type {!Element} */
          var script = document.createElement("script");
          /** @type {string} */
          script.type = "text/javascript";
          /** @type {boolean} */
          script.async = true;
          /** @type {string} */
          script.src = document.location.protocol + "//s3.pstatp.com/adstatic/resource/landing_log/dist/1.0.13/static/js/toutiao-analytics.js";
          /** @type {!Element} */
          var wafCss = document.getElementsByTagName("script")[0];
          wafCss.parentNode.insertBefore(script, wafCss);
        })();
      }
      /**
       * @return {undefined}
       */
      function _init() {
        trackGA();
        setupVizAnalytics();
        close();
        setupGoogle();
        if (parse()) {
          open();
          init();
          navigate();
          api();
          load();
          /** @type {function(string, string, !Object, number, ?): undefined} */
          window.gaevent = report;
          /** @type {function(string): undefined} */
          window.resendGA = search;
          window.gaqpush = window.gaqpush;
        }
      }
      var _prepareStyleProperties = __webpack_require__("gf5I");
      var _prepareStyleProperties2 = _interopRequireDefault(_prepareStyleProperties);
      var _normalizeDataUri = __webpack_require__("mZJ8");
      var _normalizeDataUri2 = _interopRequireDefault(_normalizeDataUri);
      var _UiIcon = __webpack_require__("gT+X");
      var _UiIcon2 = _interopRequireDefault(_UiIcon);
      var _AboutPage = __webpack_require__("YWnE");
      var data = _interopRequireDefault(_AboutPage);
      var _classlist = __webpack_require__("bVOP");
      var _classlist2 = _interopRequireDefault(_classlist);
      /** @type {function(): undefined} */
      window.gaevent = YM;
      /** @type {function(): undefined} */
      window.gaqpush = YM;
      /** @type {function(): undefined} */
      window.resendGA = YM;
      /** @type {function(): undefined} */
      window.gaeventTest = YM;
      window._taq = window._taq || [];
      module.exports = {
        init : _init
      };
    }).call(exports, __webpack_require__("gXQ3"));
  }
}, [1]);
