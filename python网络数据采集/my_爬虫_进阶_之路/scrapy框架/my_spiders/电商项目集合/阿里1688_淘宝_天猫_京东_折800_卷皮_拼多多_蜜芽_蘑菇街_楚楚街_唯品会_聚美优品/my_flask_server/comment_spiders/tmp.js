'use strict';
define("mui/cover/sliding-menu/index", function(parseInt, i, module) {
  /**
   * @param {!AudioNode} service
   * @param {!Function} name
   * @return {undefined}
   */
  function remove(service, name) {
    if (!(service instanceof name)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }
  /**
   * @param {string} name
   * @param {string} options
   * @return {?}
   */
  function append(name, options) {
    if (!name) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }
    return options && (typeof options === "object" || typeof options === "function") ? options : name;
  }
  /**
   * @param {!Object} subClass
   * @param {!Object} superClass
   * @return {undefined}
   */
  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }
    /** @type {!Object} */
    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor : {
        value : subClass,
        enumerable : false,
        writable : true,
        configurable : true
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
  var isFunction = function() {
    /**
     * @param {!Function} val
     * @param {!NodeList} props
     * @return {undefined}
     */
    function e(val, props) {
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
        Object.defineProperty(val, descriptor.key, descriptor);
      }
    }
    return function(i, klass, a) {
      if (klass) {
        e(i.prototype, klass);
      }
      if (a) {
        e(i, a);
      }
      return i;
    };
  }();
  parseInt("mui/zepto/event");
  var individual = parseInt("mui/cover/index");
  parseInt("mui/cover/sliding-menu/index.css");
  /** @type {string} */
  var DOUBLE_PARAGRAPH = '<header>        <h1></h1>        <a class="back">\u8fd4\u56de</a>    </header>    <div class="body"></div>';
  var Individual = function(_WebInspector$GeneralTreeElement) {
    /**
     * @param {!Object} options
     * @return {?}
     */
    function initialize(options) {
      remove(this, initialize);
      /** @type {!Object} */
      options = Object.assign({
        headerContent : "\u6807\u9898",
        bodyContent : "",
        setWebViewTitle : false
      }, options);
      var el = append(this, Object.getPrototypeOf(initialize).call(this, options));
      /** @type {!Object} */
      el.config = options;
      /** @type {boolean} */
      el.config.hideHeader = options.hideHeaderInApp === true && navigator.userAgent.indexOf("AliApp") !== -1;
      el.setContent(DOUBLE_PARAGRAPH);
      if (el.config.hideHeader) {
        el.$el.find("header").addClass("hide");
      }
      el.setHeaderContent(options.headerContent).setBodyContent(options.bodyContent).bindBack().bindScroll();
      if (el.config.setWebViewTitle) {
        el.bindTitleChange();
      }
      return el;
    }
    _inherits(initialize, _WebInspector$GeneralTreeElement);
    isFunction(initialize, [{
      key : "bindScroll",
      value : function init() {
        var _this = this;
        var inner = this.$el.find(".body");
        var __prevent = this.config.touchstart || function(event) {
          if (["INPUT", "TEXTAREA", "BUTTON", "SELECT", "A"].indexOf(event.target.nodeName) === -1) {
            event.preventDefault();
          }
        };
        this.$el.find("header").on("touchstart", function(event) {
          __prevent(event);
        });
        var verticalTouchStart;
        inner.on("touchstart", function(s) {
          verticalTouchStart = s.touches[0].pageY;
        }).on("touchmove", function(e) {
          if (!_this.showed) {
            return;
          }
          var eventy = e.touches[0].pageY;
          var tabContent = inner[0];
          if (eventy - verticalTouchStart > 0 && tabContent.scrollTop === 0) {
            __prevent(e);
          } else {
            if (eventy - verticalTouchStart < 0 && tabContent.scrollTop + inner.height() === tabContent.scrollHeight) {
              __prevent(e);
            }
          }
        });
        return this;
      }
    }, {
      key : "bindBack",
      value : function link() {
        var $trashTreeContextMenu = this;
        if (!this.config.hideHeader) {
          this.$el.find("header .back").on("click", function(event) {
            event.preventDefault();
            $trashTreeContextMenu.hide();
          });
        }
        return this;
      }
    }, {
      key : "bindTitleChange",
      value : function link() {
        var $ = this;
        if (!this.config.hideHeader) {
          return this;
        }
        this.on("show", function() {
          $.setWebViewTitle($.config.headerContent);
        }).on("hide", function() {
          $.setWebViewTitle(document.title);
        });
        return this;
      }
    }, {
      key : "setWebViewTitle",
      value : function setSelectedTask(task) {
        try {
          Ali.setTitle({
            text : task
          });
        } catch (i) {
        }
      }
    }, {
      key : "setHeaderContent",
      value : function buildHeaders(token) {
        /** @type {string} */
        this.config.headerContent = token;
        this.$el.find("header h1").empty().append(token);
        return this;
      }
    }, {
      key : "setBodyContent",
      value : function main_chat_title(action) {
        this.$el.find(".body").empty().append(action);
        return this;
      }
    }]);
    return initialize;
  }(individual);
  module.exports = Individual;
});
define("mui/cover/index", function(require, i, module) {
  /**
   * @param {!AudioNode} value
   * @param {!Function} type
   * @return {undefined}
   */
  function _get(value, type) {
    if (!(value instanceof type)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }
  var eqPartial = function() {
    /**
     * @param {!Function} val
     * @param {!NodeList} props
     * @return {undefined}
     */
    function e(val, props) {
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
        Object.defineProperty(val, descriptor.key, descriptor);
      }
    }
    return function(i, klass, a) {
      if (klass) {
        e(i.prototype, klass);
      }
      if (a) {
        e(i, a);
      }
      return i;
    };
  }();
  var $ = require("mui/zepto/zepto");
  var r = require("mui/custom-event/index");
  require("mui/cover/index.css");
  var h = function() {
    /** @type {!Element} */
    var dataTick = document.createElement("div");
    /** @type {string} */
    dataTick.style.position = "fixed";
    return dataTick.style.position === "fixed";
  }();
  /** @type {string} */
  var MOUSE_DOWN = "onTransitionEnd" in window ? "transitionEnd" : "webkitTransitionEnd";
  /** @type {string} */
  var prefix = "mui-cover";
  /** @type {number} */
  var uid = 0;
  var Injector = function() {
    /**
     * @param {!Object} options
     * @return {undefined}
     */
    function render(options) {
      _get(this, render);
      this.config = options || {};
      this.renderUI().bindUI().bindRoute();
    }
    eqPartial(render, [{
      key : "renderUI",
      value : function UITextArea() {
        this.$el = $('<div class="mui-cover"></div>');
        if (!h) {
          this.$el.css({
            position : "absolute"
          });
        }
        if (this.config.className) {
          this.$el.addClass(this.config.className);
        }
        $("body").append(this.$el);
        return this;
      }
    }, {
      key : "bindUI",
      value : function init() {
        var onInspectorMove = function() {
          this.$el.css("height", window.innerHeight);
        }.bind(this);
        var elem = $("body");
        this.on("show", function() {
          if (!h) {
            window.addEventListener("resize", onInspectorMove);
          }
          elem.css("-webkit-tap-highlight-color", "transparent");
        }).on("hide", function() {
          if (!h) {
            window.removeEventListener("resize", onInspectorMove);
          }
          elem.css("-webkit-tap-highlight-color", "");
        });
        return this;
      }
    }, {
      key : "bindRoute",
      value : function init() {
        var $innerblock = this;
        if (this.config.disableRoute) {
          return this;
        }
        /** @type {string} */
        var hash = "#" + (this.config.route || prefix + "-" + uid);
        uid++;
        if (hash === location.hash) {
          this.show();
        }
        this.on("show", function() {
          if (location.hash !== hash) {
            /** @type {string} */
            location.hash = hash;
          }
        }).on("hide", function() {
          if (location.hash === hash) {
            if (history.length && history.length > 1) {
              history.back();
            } else {
              if (history.replaceState) {
                history.replaceState(null, document.title, location.href.replace(hash, ""));
              }
            }
          }
        });
        window.addEventListener("hashchange", function() {
          if (location.hash === hash) {
            $innerblock.show();
          } else {
            $innerblock.hide();
          }
        });
        return this;
      }
    }, {
      key : "setContent",
      value : function refresh_configurable_extensions_list(e) {
        this.$el.empty().append(e);
        return this;
      }
    }, {
      key : "show",
      value : function initialize() {
        var e = this;
        /** @type {boolean} */
        this.showed = true;
        if (!h) {
          this.$el.css({
            top : window.pageYOffset,
            height : window.innerHeight
          });
        }
        this.$el.show();
        setTimeout(function() {
          e.$el.addClass("show");
          e.trigger("show");
        }, 50);
        return this;
      }
    }, {
      key : "hide",
      value : function Dialog() {
        var idealSelect = this;
        if (this.showed) {
          /** @type {boolean} */
          this.showed = false;
        } else {
          return this;
        }
        var callback = undefined;
        this.$el.on(MOUSE_DOWN, callback = function destroy() {
          idealSelect.$el.hide();
          idealSelect.$el.off(MOUSE_DOWN, callback);
        });
        this.$el.removeClass("show");
        this.trigger("hide");
        return this;
      }
    }, {
      key : "destroy",
      value : function hideMeFN() {
        this.hide();
        this.$el.remove();
      }
    }]);
    return render;
  }();
  Object.assign(Injector.prototype, r);
  module.exports = Injector;
});
define("mui/review-m/instance/detail", ["mui/zepto/zepto", "mui/zepto/event", "mui/zepto/touch", "mui/review-m/index.css", "mui/dlp/index", "mui/datalazylist/", "mui/crossimage/", "mui/review-m/widgets/utils.js", "mui/review-m/tpl/main.xtpl", "mui/review-m/tpl/list.xtpl", "mui/review-m/tpl/tags.xtpl"], function(require, i, module) {
  /**
   * @param {!AudioNode} v
   * @param {!Function} node
   * @return {undefined}
   */
  function fill(v, node) {
    if (!(v instanceof node)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }
  var isSourcedFromRequire = function() {
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
  var $ = require("mui/zepto/zepto");
  require("mui/zepto/event");
  require("mui/zepto/touch");
  require("mui/review-m/index.css");
  var self = require("mui/dlp/index");
  var Controller = require("mui/datalazylist/");
  var s = require("mui/crossimage/");
  var o = require("mui/review-m/widgets/utils.js");
  var delete_button_col = require("mui/review-m/tpl/main.xtpl");
  var expect = require("mui/review-m/tpl/list.xtpl");
  var d = require("mui/review-m/tpl/tags.xtpl");
  var baseConfig = {
    "el_wrap" : "#J_CommentsWrapper",
    "el_filterwrap" : "#J_CommentsWrapper ul.filter",
    "el_listwrap" : "#J_CommentsWrapper ul.list",
    "el_allcomments" : "#J_AllComments",
    "el_addcomments" : "#J_AddComments",
    "el_imgcommetns" : "#J_ImgComments",
    "el_imgcommetns_num" : "#J_ImgCommentsNum",
    "isShowTagsCloud" : true
  };
  var storeMixin = function() {
    /**
     * @return {?}
     */
    function init() {
      var DEFAULT_CONFIG = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      if (fill(this, init), this.config = {}, this.els = {}, this.config = Object.assign(baseConfig, DEFAULT_CONFIG), this.ajaxParams = {
        "itemId" : this.config.itemId || 0,
        "sellerId" : this.config.sellerId || 0,
        "order" : 3,
        "append" : 0,
        "content" : 0,
        "currentPage" : 1,
        "pageSize" : 10,
        "tagId" : ""
      }, !this.ajaxParams.itemId) {
        return false;
      }
      this.initDom();
      this.initList();
      this.bindEvents();
      if (this.config.isShowTagsCloud) {
        this.initCloudTags();
      }
    }
    return isSourcedFromRequire(init, [{
      "key" : "initDom",
      "value" : function() {
        var _config = this.config;
        if (!_config.el) {
          return false;
        }
        $(_config.el).html(delete_button_col());
        this.els = {
          "wrap" : $(_config.el).find(_config.el_wrap),
          "filterWrap" : $(_config.el).find(_config.el_filterwrap),
          "filterByAll" : $(_config.el).find(_config.el_allcomments),
          "filterByAdd" : $(_config.el).find(_config.el_addcomments),
          "filterByImg" : $(_config.el).find(_config.el_imgcommetns),
          "filterImgNum" : $(_config.el).find(_config.el_imgcommetns_num),
          "listWrap" : $(_config.el).find(_config.el_listwrap)
        };
        /** @type {null} */
        this.gallery = null;
        if (window.app && window.app.ImageViewer) {
          this.gallery = window.app.ImageViewer;
        }
      }
    }, {
      "key" : "initList",
      "value" : function() {
        var self = this;
        $(this.els.wrap).append('<ul class="list"></ul><div class="loading-icon"></div>');
        this.els.listWrap = $(this.config.el_listwrap);
        this.dllInstance = new Controller({
          "render" : new Controller.NodeRender({
            "el" : this.els.listWrap,
            "renderBuffer" : 6 * (window.screen.height || 667),
            "createDom" : function(tab) {
              return $(expect(tab.item));
            }
          }),
          "loader" : new Controller.FixedSizeDataLoader({
            "onData" : function(options, callback) {
              var data = {
                "currentPage" : options.page + 1
              };
              self.fetchListData(data, function() {
                var $allPanels = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
                var rows = (arguments[1], $allPanels.rateList || []);
                if (callback) {
                  callback(rows);
                }
                if (0 === options.page) {
                  self.renderImgFilter($allPanels);
                  if (rows.length < self.ajaxParams.pageSize) {
                    self.renderErrorList({
                      "text" : "\u8be5\u5546\u54c1\u6682\u65e0\u8bc4\u8bba\u3002"
                    });
                  }
                }
                if (rows.length < self.ajaxParams.pageSize) {
                  self.removeLoading();
                }
                if (window.app && window.app.atp) {
                  app.atp.sendAtpanel("mtmalldetail.1.37");
                }
              }, function(a, n) {
                if (0 === options.page) {
                  self.renderErrorList({
                    "error" : true,
                    "text" : "\u6570\u636e\u8bf7\u6c42\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u518d\u8bd5"
                  });
                } else {
                  callback([]);
                }
                self.removeLoading();
              });
            }
          })
        });
      }
    }, {
      "key" : "bindEvents",
      "value" : function() {
        var options = this;
        $(this.els.filterWrap).on("tap", "li", function(event) {
          event.preventDefault();
          var current = $(this).data("id") || "";
          $(options.els.filterWrap).find("li").removeClass("current");
          $(this).addClass("current");
          options.ajaxParams.tagId = current && "picture" !== current ? current : "";
          if (current && "picture" === current) {
            /** @type {number} */
            options.ajaxParams.picture = 1;
          } else {
            delete options.ajaxParams.picture;
          }
          if (current && "append" === current) {
            /** @type {number} */
            options.ajaxParams.append = 1;
            if (window.app && window.app.atp) {
              app.atp.sendAtpanel("mtmalldetail.1.34");
            }
          } else {
            /** @type {number} */
            options.ajaxParams.append = 0;
          }
          options.removeLoading();
          options.removeList();
          options.dllInstance.pause();
          options.initList();
        });
        $(this.els.wrap).on("tap", "img.comment-pic", function(event) {
          if (event) {
            event.preventDefault();
          }
          var iframe = $(this);
          var node = $(iframe).parents("li");
          var linkSelected = $(iframe).parents("ul.pics").find("img") || [];
          /** @type {!Array} */
          var history = [];
          /** @type {number} */
          var l = 0;
          for (; l < linkSelected.length; l++) {
            history.push($(linkSelected[l]).data("url"));
          }
          if (options.gallery) {
            options.gallery.init(history, $(node).index(), iframe[0]);
            if (window.app && window.app.atp) {
              app.atp.sendAtpanel("mtmalldetail.1.36");
            }
          }
        });
      }
    }, {
      "key" : "fetchListData",
      "value" : function() {
        var args = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        var resolve = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : function() {
        };
        var temp_err = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : function() {
        };
        /** @type {string} */
        var img = "//rate.tmall.com/list_detail_rate.htm";
        img = o.mergeParams(img, Object.assign(this.ajaxParams, args));
        /**
         * @return {?}
         */
        var handler = function() {
          var argumentsParam = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
          var options = argumentsParam.rateDetail;
          if (options && options.rateList && options.rateList.length) {
            /**
             * @param {string} options
             * @return {?}
             */
            var addValidationMessages = function(options) {
              return options.substring(0, 11);
            };
            /**
             * @param {string} attribs
             * @return {?}
             */
            var format = function(attribs) {
              return attribs = attribs.split(";"), attribs.map(function(clusterShardData) {
                var position = clusterShardData.split(":");
                return {
                  "k" : position[0],
                  "v" : position[1]
                };
              });
            };
            return options.rateList = options.rateList.map(function($scope) {
              if ($scope.rateDate_display = addValidationMessages($scope.rateDate), $scope.appendComment && ($scope.appendComment.days_display = $scope.appendComment.days <= 0 ? "\u5f53\u5929" : $scope.appendComment.days + "\u5929\u540e", $scope.appendComment.content_display = $scope.appendComment.content.replace(/\\n/g, "<br>")), $scope.attrs = [], $scope.auctionSku && ($scope.attrs = $scope.attrs.concat(format($scope.auctionSku))), $scope.userInfo && ($scope.attrs = $scope.attrs.concat(format($scope.userInfo))),
              $scope.rateContent_display = $scope.rateContent ? $scope.rateContent.replace(/\\n/g, "<br>") : "\u6b64\u7528\u6237\u6ca1\u6709\u586b\u5199\u8bc4\u8bba\uff01", $scope.pics && $scope.pics.length) {
                var ncells = $scope.pics.length || 0;
                /** @type {!Array} */
                $scope.pics_display = [];
                /** @type {number} */
                var i = 0;
                for (; i < ncells; i++) {
                  $scope.pics_display[i] = s.getFitUrl($scope.pics[i], 55, 55);
                }
              }
              if ($scope.appendComment && $scope.appendComment.pics && $scope.appendComment.pics.length) {
                var cell_amount = $scope.appendComment.pics.length || 0;
                /** @type {!Array} */
                $scope.appendComment.pics_display = [];
                /** @type {number} */
                var i = 0;
                for (; i < cell_amount; i++) {
                  $scope.appendComment.pics_display[i] = s.getFitUrl($scope.appendComment.pics[i], 55, 55);
                }
              }
              return $scope;
            }), options;
          }
        };
        self.jsonp({
          "url" : img,
          "localCacheType" : "localStorage",
          "cacheValidTime" : 3e5,
          "success" : function(data, stats) {
            if (resolve) {
              resolve(handler(data), stats);
            }
          },
          "error" : function(f, data) {
            if (temp_err) {
              temp_err(data);
            }
          }
        });
      }
    }, {
      "key" : "initCloudTags",
      "value" : function() {
        var $body = this;
        /** @type {string} */
        var i = "//rate.tmall.com/listTagClouds.htm";
        i = o.mergeParams(i, {
          "itemId" : this.config.itemId,
          "isAll" : true,
          "isInner" : true
        });
        if (self) {
          self.jsonp({
            "url" : i,
            "localCacheType" : "localStorage",
            "cacheValidTime" : 3e5,
            "success" : function(s, xhr) {
              var a = s ? s.tags : {};
              if (a && a.tagClouds && a.tagClouds.length) {
                $($body.els.filterWrap).append($(d(a)));
              }
            }
          });
        }
      }
    }, {
      "key" : "renderImgFilter",
      "value" : function() {
        var dataProcessor = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        if (dataProcessor && dataProcessor.rateCount && dataProcessor.rateCount.picNum) {
          $(this.els.filterImgNum).text(dataProcessor.rateCount.picNum);
        } else {
          $(this.els.filterByImg).hide();
        }
      }
    }, {
      "key" : "renderErrorList",
      "value" : function() {
        var menuOption = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
        var getdate = menuOption.text || "";
        $(this.els.listWrap).append('<li class="item error">' + getdate + "</li>");
      }
    }, {
      "key" : "removeList",
      "value" : function() {
        $(this.els.listWrap).remove();
      }
    }, {
      "key" : "removeLoading",
      "value" : function() {
        $(this.els.wrap).find("div.loading-icon").remove();
      }
    }]), init;
  }();
  module.exports = storeMixin;
});
define("mui/datalazylist/index", ["mui/zepto/zepto", "mui/zepto/event", "mui/datalazylist/render/node", "mui/datalazylist/render/multinode", "mui/datalazylist/loader/page", "mui/datalazylist/loader/static"], function(require, canCreateDiscussions, module) {
  /**
   * @return {?}
   */
  function f() {
    return d.extend.apply(this, arguments);
  }
  /**
   * @param {!Array} e
   * @return {undefined}
   */
  function check(e) {
    if (enable && window.console) {
      console.log(e);
    }
  }
  /**
   * @param {!Function} fn
   * @param {number} timeout
   * @param {!Object} context
   * @return {?}
   */
  function setTimeout(fn, timeout, context) {
    /**
     * @return {undefined}
     */
    function fn() {
      if (result) {
        result.cancel();
        /** @type {number} */
        result = 0;
      }
      /** @type {number} */
      w_seq_type = +new Date;
      fn.apply(context || this, arguments);
      /** @type {number} */
      v_seq_type = +new Date;
    }
    /**
     * @param {!Function} s
     * @param {number} t
     * @return {?}
     */
    function callback(s, t) {
      /** @type {number} */
      var n = setTimeout(s, t);
      return {
        "cancel" : function() {
          clearTimeout(n);
        }
      };
    }
    var result;
    /** @type {number} */
    var w_seq_type = 0;
    /** @type {number} */
    var v_seq_type = 0;
    timeout = timeout || 150;
    /**
     * @return {undefined}
     */
    var handler = function() {
      /** @type {!Arguments} */
      var originalArguments = arguments;
      if (!w_seq_type || v_seq_type >= w_seq_type && +new Date - v_seq_type > timeout || v_seq_type < w_seq_type && +new Date - w_seq_type > 8 * timeout) {
        fn();
      } else {
        if (result) {
          result.cancel();
        }
        result = callback(function() {
          fn.apply(null, originalArguments);
        }, timeout);
      }
    };
    return handler.stop = function() {
      if (result) {
        result.cancel();
        /** @type {number} */
        result = 0;
      }
    }, handler;
  }
  /**
   * @param {?} action
   * @return {undefined}
   */
  function exports(action) {
    /**
     * @return {undefined}
     */
    function end() {
      /** @type {number} */
      var connectNumber = +new Date;
      if (!(item > 1 || 1 === item && connectNumber - concurency < 1024)) {
        /** @type {number} */
        item = 1;
        /** @type {number} */
        concurency = connectNumber;
        if (_takingTooLongTimeout) {
          clearTimeout(_takingTooLongTimeout);
        }
        /** @type {number} */
        _takingTooLongTimeout = setTimeout(function() {
          /** @type {number} */
          item = 0;
          t();
        }, 2048);
      }
    }
    /**
     * @return {undefined}
     */
    function n() {
      end();
      t();
    }
    var that = this;
    f(that, action);
    var u;
    var result;
    var _this;
    var item;
    var self;
    var _takingTooLongTimeout;
    var _currentEmbedded = action.scrollPanel;
    /**
     * @param {?} stat
     * @return {?}
     */
    var next = function(stat) {
      return self.get(stat);
    };
    /**
     * @return {?}
     */
    var init = function() {
      if (_this && self && u) {
        var b;
        var a;
        var e = that.minIndex || 0;
        /** @type {number} */
        var options = Math.min(that.maxIndex !== undefined ? that.maxIndex : Number.MAX_VALUE, self.totalNum !== undefined ? self.totalNum - 1 : Number.MAX_VALUE);
        if (that.onStart) {
          that.onStart(result, e, options, item);
        }
        _this.start(result, e, options, item);
        for (; result[0] < result[1] && (b = result[1] > options + 1 && result[1] - options - 1 || _this.checkRemove(result[1] - 1, 1));) {
          a = _this.remove(result[1] - 1, 1, b);
          result[1] -= a;
          check(["remove", 1, b, a]);
        }
        for (; result[0] < result[1] && (b = e > result[0] && e - result[0] || _this.checkRemove(result[0], -1));) {
          a = _this.remove(result[0], -1, b);
          result[0] += a;
          check(["remove", -1, b, a]);
        }
        _this.adjust(result, e, options);
        if (result[0] < e && result[0] == result[1]) {
          result[0] = result[1] = e;
        }
        for (; result[0] > e && (b = _this.checkAdd(result[0] - 1, -1));) {
          if (self.fetch(result[0] - 1), !next(result[0] - 1)) {
            return self.fetch(result[0] - 1, t);
          }
          a = _this.add(result[0] - 1, -1, b, next);
          result[0] -= a;
          check(["add", -1, b, a]);
        }
        for (; result[1] <= options && (b = _this.checkAdd(result[1], 1));) {
          if (self.fetch(result[1]), !next(result[1])) {
            return self.fetch(result[1], t);
          }
          a = _this.add(result[1], 1, b, next);
          result[1] += a;
          check(["add", 1, b, a]);
        }
        _this.finish(result, e, options);
        if (that.onFinish) {
          that.onFinish(result, e, options);
        }
      }
    };
    var t = setTimeout(init, 100);
    /** @type {number} */
    var concurency = 0;
    /**
     * @param {!Object} p
     * @return {undefined}
     */
    that.setLoader = function(p) {
      /** @type {!Object} */
      self = p;
    };
    /**
     * @param {!Object} render
     * @return {undefined}
     */
    that.setRender = function(render) {
      /** @type {!Array} */
      result = [0, 0];
      /** @type {!Object} */
      _this = render;
    };
    /**
     * @return {undefined}
     */
    that.pause = function() {
      if (u) {
        $(window).off("scroll touchmove resize", n);
        if (_currentEmbedded) {
          $(_currentEmbedded).off("scroll touchmove", n);
        }
        /** @type {number} */
        item = 2;
        t.stop();
        init();
        /** @type {boolean} */
        u = false;
      }
    };
    /**
     * @return {undefined}
     */
    that.resume = function() {
      if (!u) {
        /** @type {boolean} */
        u = true;
        /** @type {number} */
        item = 0;
        end();
        $(window).on("scroll touchmove resize", n);
        if (_currentEmbedded) {
          $(_currentEmbedded).on("scroll touchmove", n);
        }
      }
    };
    that.refresh = t;
    if (that.loader) {
      that.setLoader(that.loader);
    }
    if (that.render) {
      that.setRender(that.render);
    }
    if (false !== that.start) {
      that.resume();
      t();
      d(function() {
        t();
        setTimeout(t, 2048);
      });
    }
  }
  var d = require("mui/zepto/zepto");
  var $ = require("mui/zepto/event");
  /** @type {boolean} */
  var enable = location.href.indexOf("debug") > -1;
  exports.NodeRender = require("mui/datalazylist/render/node");
  exports.MultiNodeRender = require("mui/datalazylist/render/multinode");
  /**
   * @param {?} name
   * @return {?}
   */
  exports.FixedSizeDataLoader = function(name) {
    return exports.RandomSizeDataLoader(f({
      "fixedSize" : true
    }, name));
  };
  exports.RandomSizeDataLoader = require("mui/datalazylist/loader/page");
  exports.StaticDataLoader = require("mui/datalazylist/loader/static");
  /** @type {function(?): undefined} */
  module.exports = exports;
});
define("mui/datalazylist/render/node", ["mui/zepto/zepto"], function(require, canCreateDiscussions, context) {
  /**
   * @param {!Node} obj
   * @return {undefined}
   */
  function fn(obj) {
    if (obj.parentNode) {
      obj.parentNode.removeChild(obj);
    }
  }
  /**
   * @param {!Node} obj
   * @return {?}
   */
  function wrap(obj) {
    return obj.nextSibling;
  }
  /**
   * @param {?} elem
   * @param {string} style
   * @param {string} value
   * @return {undefined}
   */
  function callback(elem, style, value) {
    $(elem).css(style, value);
  }
  /**
   * @param {?} obj
   * @param {string} prop
   * @return {?}
   */
  function get(obj, prop) {
    return $(obj).css(prop);
  }
  /**
   * @return {?}
   */
  function getWindowSize() {
    /** @type {!Window} */
    var win = window;
    var doc = win.document;
    var body = doc.body;
    var cursor = doc.documentElement;
    return win.innerHeight || "CSS1Compat" === doc.compatMode && cursor.clientHeight || body && body.clientHeight || cursor.clientHeight;
  }
  /**
   * @param {!Object} elem
   * @param {string} name
   * @return {?}
   */
  function getStyle(elem, name) {
    try {
      return window.getComputedStyle ? window.getComputedStyle(elem, name) : domObj.currentStyle[name];
    } catch (o) {
      return elem.style[name];
    }
  }
  /**
   * @param {!Object} elem
   * @return {?}
   */
  function render(elem) {
    if (9 == elem.nodeType) {
      return Math.max(document.document.documentElement.scrollHeight || 0, document.body.documentElement.scrollHeight || 0, getWindowSize());
    }
    var value = elem.offsetHeight;
    return value > 0 ? value : (value = getStyle(elem, "height"), (null == value || Number(value) < 0) && (value = elem.style.height || 0), value = parseFloat(value) || 0, value = value + (parseFloat(getStyle(elem, "paddingTop")) || 0), value = value + (parseFloat(getStyle(elem, "borderTopHeight")) || 0), value = value + (parseFloat(getStyle(elem, "paddingBottom")) || 0), value = value + (parseFloat(getStyle(elem, "borderBottomHeight")) || 0));
  }
  /**
   * @return {?}
   */
  function getScroll() {
    /** @type {!Window} */
    var win = window;
    var doc = win.document;
    win.pageXOffset;
    return 1 * (win.pageYOffset || 0) + 1 * (doc.documentElement.scrollLeft || 0) + 1 * (doc.body.scrollLeft || 0);
  }
  /**
   * @return {?}
   */
  function scrollTop() {
    /** @type {!Window} */
    var win = window;
    var doc = win.document;
    return 1 * (win.pageXOffset || 0) + 1 * (doc.documentElement.scrollTop || 0) + 1 * (doc.body.scrollTop || 0);
  }
  /**
   * @param {!Object} obj
   * @return {?}
   */
  function getOffset(obj) {
    var scrollLeft = getScroll();
    var viewportTop = scrollTop();
    if (obj.getBoundingClientRect) {
      var ownerRect = obj.getBoundingClientRect();
      /** @type {!HTMLDocument} */
      var doc = document;
      /** @type {!HTMLBodyElement} */
      var body = doc.body;
      /** @type {!Element} */
      var docElem = doc && doc.documentElement;
      /** @type {number} */
      var zoom = parseFloat(getStyle(obj, "zoom")) || 1;
      scrollLeft = scrollLeft + (ownerRect.left * zoom - (docElem.clientLeft || body.clientLeft || 0));
      viewportTop = viewportTop + (ownerRect.top * zoom - (docElem.clientTop || body.clientTop || 0));
    }
    return {
      "left" : scrollLeft,
      "top" : viewportTop
    };
  }
  /**
   * @param {?} x
   * @param {number} y
   * @return {?}
   */
  function elementFromPoint(x, y) {
    if (document.elementFromPoint) {
      /** @type {(Element|null)} */
      var elem = document.elementFromPoint(x, y);
      for (; elem && elem.__dllIndex === undefined;) {
        /** @type {(Element|null)} */
        elem = elem.parentElement;
      }
      return elem;
    }
  }
  /**
   * @param {number} me
   * @return {?}
   */
  function init(me) {
    me = me || {};
    var marginTop;
    var height;
    var offsetY;
    var offset;
    var tailMaxLeft;
    var col;
    var r;
    var top;
    var y;
    var a = me.el;
    var el = me.state;
    var b = el && el.get("dataSec");
    var par = el && el.get("ph");
    var element = me.scrollParent;
    var data = {};
    var map = {};
    /** @type {number} */
    var $i12 = 0;
    if (b && (b[0] < 0 || b[1] <= b[0])) {
      /** @type {null} */
      b = null;
    }
    if ("string" == typeof a) {
      a = $(a);
    }
    if (!a.nodeType && a.get) {
      a = a.get(0);
    }
    var target = $(a).find(".startPointer", a).get(0);
    var parent = $(a).find(".endPointer", a).get(0);
    return target || (target = $('<div class="startPointer"></div>'), target.prependTo(a), target = target[0]), parent || (parent = $('<div class="endPointer"></div>'), parent.appendTo(a), parent = parent[0]), callback(target, "paddingTop", "0px"), callback(parent, "paddingBottom", "0px"), callback(parent, "clear", "both"), {
      "start" : function(arr, n, agent, email) {
        if ($i12++, marginTop = scrollTop() + getOffset(document.body).top, height = getWindowSize(), offsetY = me.renderBuffer || (column ? 4 : 2) * height, 2 == email && (offsetY = Math.min(0, offsetY)), 1 == email && (offsetY = Math.min(height / 2, offsetY)), offset = Math.max(me.destroyBuffer || height * (column ? 8 : 4), offsetY), 2 == email && (offset = Math.min(height / 2, offset)), tailMaxLeft = me.scrollBuffer || 0, col = me.groupSize || 1, r = me.defaultSize || 256, top = height + marginTop,
        y = 0 + marginTop, element) {
          /** @type {number} */
          var offset = Math.max(getOffset(target).top, 0) - getOffset(element).top;
          if (offset < 0) {
            /** @type {number} */
            y = y - offset;
          }
          /** @type {number} */
          top = Math.min(top, offset(element).top + render(element));
        }
        if (arr[0] <= n) {
          callback(target, "paddingTop", "0px");
        }
      },
      "checkRemove" : function(start, file) {
        var i;
        var element;
        if (-1 == file) {
          /** @type {number} */
          i = start;
          for (; (element = map[i]) && !(getOffset(element).top + render(element) >= y - offset); i++) {
          }
          return Math.max(0, i - i % col - start);
        }
        /** @type {number} */
        i = start;
        for (; i >= 0 && (element = map[i]) && !(getOffset(element).top <= top + offset); i--) {
        }
        return Math.max(0, start - (i + col - i % col) + 1);
      },
      "remove" : function(i, n, d) {
        var k;
        var node;
        if (-1 == n) {
          var doc;
          var top;
          var scrollY;
          /** @type {number} */
          var height = parseInt(get(target, "paddingTop"), 10);
          /** @type {!Array} */
          var a = [];
          /** @type {number} */
          k = i;
          for (; k < i + d && (node = map[k]); k++) {
            doc = wrap(node);
            a.push(node);
            if (k == i) {
              top = node.offsetTop;
            }
            scrollY = node.offsetTop + node.offsetHeight;
          }
          var y = doc.offsetTop;
          callback(target, "paddingTop", height + (scrollY - top) + "px");
          /** @type {number} */
          var j = a.length - 1;
          for (; j >= 0; j--) {
            fn(a[j]);
          }
          /** @type {number} */
          var total = y - doc.offsetTop + (scrollY - top);
          /** @type {number} */
          j = 0;
          for (; j < a.length; j++) {
            delete map[i + j];
            /** @type {number} */
            data[i + j] = total / a.length;
          }
          return callback(target, "paddingTop", height + total + "px"), a.length;
        }
        /** @type {number} */
        k = i;
        for (; k > i - d && (node = map[k]); k--) {
          delete map[k];
          fn(node);
        }
        return i - k;
      },
      "adjust" : function(t, c, x) {
        if (t[0] == t[1]) {
          if (b) {
            return t[0] = t[1] = b[0], target.style.paddingTop = (par && par[0] || 0) + "px", parent.style.paddingBottom = (par && par[1] || 0) + "px", void el.checkScroll();
          }
          var n = t[0];
          /** @type {number} */
          var i = y - (getOffset(target).top + render(target));
          /** @type {number} */
          var k = parseInt(get(target, "paddingTop"), 10);
          for (; i < 0 && n > c;) {
            var m = data[n];
            if (m === undefined) {
              m = data[n] = r;
            }
            i = i + m;
            /** @type {number} */
            k = k - m;
            /** @type {number} */
            n = n - 1;
          }
          for (; i > 0 && n < x;) {
            m = data[n];
            if (m === undefined && (m = data[n] = r), i < m) {
              break;
            }
            /** @type {number} */
            i = i - m;
            k = k + m;
            n = n + 1;
          }
          callback(target, "paddingTop", k + "px");
          /** @type {number} */
          t[0] = t[1] = n - n % col;
        }
        if (t[0] <= c) {
          callback(target, "paddingTop", "0px");
        }
      },
      "checkAdd" : function(a, now) {
        return -1 == now ? b ? a >= b[0] ? a + 1 - b[0] : 0 : (a + 1) % col != 0 ? (a + 1) % col : getOffset(target).top + render(target) > y - offsetY ? col : 0 : b ? a < b[1] ? b[1] - a : 0 : a % col != 0 ? col - a % col : getOffset(0 === a ? target : parent).top < top + offsetY ? col : 0;
      },
      "add" : function(i, n, r, next) {
        /** @type {!Array} */
        var list = [];
        /** @type {number} */
        var leftAcum = 0;
        /** @type {!DocumentFragment} */
        var button = document.createDocumentFragment();
        if (-1 == n) {
          /** @type {number} */
          var j = i;
          for (; j > i - r && next(j); j--) {
            var item = {
              "item" : next(j),
              "index" : j
            };
            var val = me.createDom(item);
            if (!val.nodeType && val.get) {
              val = val.get(0);
            }
            map[j] = item.el = val;
            val.__dllIndex = j;
            $(item.el).prependTo(button);
            list.push(item);
          }
          var wrapper = wrap(target);
          var top = wrapper.offsetTop;
          if ($(button).insertAfter(target), me.initDom) {
            /** @type {number} */
            j = 0;
            /** @type {number} */
            var i = list.length;
            for (; j < i; j++) {
              me.initDom(list[j]);
            }
          }
          /** @type {number} */
          j = 0;
          for (; j < list.length; j++) {
            item = list[j];
            leftAcum = leftAcum + (data[item.index] || (wrapper.offsetTop - top) / list.length || r);
          }
          callback(target, "paddingTop", parseInt(get(target, "paddingTop"), 10) - leftAcum + "px");
        } else {
          /** @type {number} */
          j = i;
          for (; j < i + r && next(j); j++) {
            item = {
              "item" : next(j),
              "index" : j
            };
            val = me.createDom(item);
            if (!val.nodeType && val.get) {
              val = val.get(0);
            }
            map[j] = item.el = val;
            val.__dllIndex = j;
            $(item.el).appendTo(button);
            list.push(item);
          }
          if ($(button).insertBefore(parent), me.initDom) {
            /** @type {number} */
            j = 0;
            /** @type {number} */
            i = list.length;
            for (; j < i; j++) {
              me.initDom(list[j]);
            }
          }
        }
        return list.length;
      },
      "finish" : function(a, fn, receiver) {
        if (b && (b[0] < a[0] || b[1] > a[1] ? callback(parent, "paddingBottom", par[1] - (parent.offsetTop - target.offsetTop) + "px") : (b = null, par = null)), !b) {
          if (el) {
            /** @type {!Array} */
            var styles = [a[0], a[1]];
            /** @type {number} */
            var data = parseInt(get(target, "paddingTop"), 10);
            /** @type {number} */
            var dst = parseInt(get(parent, "paddingBottom"), 10) + (parent.offsetTop - target.offsetTop);
            var node = map[styles[0]];
            var elem = map[styles[1] - 1];
            if (node && elem && node != elem) {
              var coords = getOffset(node);
              var pos = getOffset(elem);
              var container = scrollTop() > coords.top + node.offsetHeight && elementFromPoint(coords.left + 1, 1) || node;
              var parent = scrollTop() + height < pos.top && elementFromPoint(pos.left + 1, height - 1) || elem;
              if (container != node) {
                /** @type {number} */
                data = data + (getOffset(container).top - coords.top);
                styles[0] = container.__dllIndex;
              }
              if (parent != elem) {
                /** @type {number} */
                dst = dst + (pos.top + elem.offsetHeight - getOffset(parent).top - parent.offsetHeight);
                styles[1] = parent.__dllIndex + 1;
              }
            }
            el.set("dataSec", styles);
            el.set("ph", [data, dst - data]);
          }
          callback(parent, "paddingBottom", Math.min(tailMaxLeft, (receiver + 1 - a[1]) * r) + "px");
        }
      },
      "destroy" : function() {
        var element;
        for (; (element = target.nextSibling) && element != parent;) {
          fn(element);
        }
        fn(target);
        fn(parent);
        /** @type {null} */
        target = null;
        /** @type {null} */
        parent = null;
        map = {};
        data = {};
        me = {};
      }
    };
  }
  var $ = require("mui/zepto/zepto");
  /** @type {(Array<string>|null)} */
  var column = navigator.userAgent.match(/iPad|iPod|iPhone/);
  /**
   * @param {?} selector
   * @return {?}
   */
  init.getDOMNode = function(selector) {
    return $(selector).get(0);
  };
  /** @type {function(number): ?} */
  context.exports = init;
});
define("mui/datalazylist/render/multinode", ["mui/datalazylist/render/node"], function(require, canCreateDiscussions, context) {
  /**
   * @param {!Object} self
   * @return {?}
   */
  function init(self) {
    /**
     * @param {string} t
     * @param {number} s
     * @return {?}
     */
    function $(t, s) {
      return bind(Math.max(t - s, 0) / length);
    }
    /**
     * @param {number} s
     * @param {number} i
     * @return {?}
     */
    function func(s, i) {
      return s * length + i;
    }
    self = self || {};
    var items = self.els;
    var state = self.state;
    /** @type {!Array} */
    var rows = [];
    /** @type {!Array} */
    var slices = [];
    var length = items.length;
    /** @type {function(?): number} */
    var bind = Math.ceil;
    /** @type {number} */
    var i = 0;
    length = items.length;
    for (; i < length; i++) {
      el = Node.getDOMNode(items[i]);
      slices.push([0, 0]);
      self.el = el;
      /** @type {null} */
      self.els = null;
      self.state = state && state.getState("C" + i);
      rows.push(new Node(self));
    }
    return {
      "start" : function(e, target, obj, item) {
        /** @type {number} */
        var i = 0;
        for (; i < length; i++) {
          rows[i].start(slices[i], $(target, i), $(obj + 1, i) - 1, item);
        }
      },
      "checkRemove" : function(i, item) {
        if (-1 == item) {
          /** @type {number} */
          var minInRow = Number.MAX_VALUE;
          /** @type {number} */
          var j = i;
          for (; j < i + length; j++) {
            var i = rows[j % length].checkRemove($(j, j % length), item);
            /** @type {number} */
            minInRow = Math.min(minInRow, j + i * length);
          }
          return minInRow - i;
        }
        /** @type {number} */
        var widestInView = 0;
        /** @type {number} */
        j = i;
        for (; j >= 0 && j > i - length; j--) {
          i = rows[j % length].checkRemove($(j, j % length), item);
          /** @type {number} */
          widestInView = Math.max(widestInView, j - i * length);
        }
        return i - widestInView;
      },
      "remove" : function(start, v, end) {
        /** @type {number} */
        var d = 0;
        if (-1 == v) {
          /** @type {number} */
          var i = start;
          for (; i < start + end && i < start + length; i++) {
            var str = rows[i % length].remove($(i, i % length), v, bind((end - (i - start)) / length));
            slices[i % length][0] += str;
            d = d + str;
          }
        } else {
          /** @type {number} */
          i = start;
          for (; i >= 0 && i > start - end && i > start - length; i--) {
            str = rows[i % length].remove($(i, i % length), v, bind((end - (start - i)) / length));
            slices[i % length][1] -= str;
            d = d + str;
          }
        }
        return d;
      },
      "adjust" : function(r, o, c) {
        /** @type {number} */
        var x = Number.MAX_VALUE;
        /** @type {number} */
        var i = 0;
        for (; i < length; i++) {
          rows[i].adjust(slices[i], $(o, i), $(c, i));
          /** @type {number} */
          x = Math.min(x, func(slices[i][0], i));
        }
        if (r[0] == r[1]) {
          /** @type {number} */
          r[0] = r[1] = x;
          /** @type {number} */
          i = 0;
          for (; i < length; i++) {
            /** @type {number} */
            slices[i][0] = slices[i][1] = bind(Math.max(x - i, 0) / length);
          }
        }
      },
      "checkAdd" : function(n, prop) {
        if (-1 == prop) {
          var r = n + 1;
          /** @type {number} */
          var i = n;
          for (; i >= 0 && i > n - length; i--) {
            var val = rows[i % length].checkAdd($(i, i % length), prop);
            if (val) {
              /** @type {number} */
              r = Math.min(r, i - (val - 1) * length);
            }
          }
          return n + 1 - r;
        }
        /** @type {number} */
        var row = n - 1;
        /** @type {number} */
        i = n;
        for (; i < n + length; i++) {
          val = rows[i % length].checkAdd($(i, i % length), prop);
          if (val) {
            /** @type {number} */
            row = Math.max(row, i + (val - 1) * length);
          }
        }
        return row - (n - 1);
      },
      "add" : function(start, r, end, callback) {
        /** @type {number} */
        var result = 0;
        if (-1 == r) {
          /** @type {number} */
          var i = start;
          for (; i >= 0 && i > start - end && i > start - length; i--) {
            var fd = rows[i % length].add($(i, i % length), r, bind((end - (start - i)) / length), function(number) {
              return callback(func(number, i % length));
            });
            slices[i % length][0] -= fd;
            result = result + fd;
          }
        } else {
          /** @type {number} */
          i = start;
          for (; i < start + end && i < start + length; i++) {
            fd = rows[i % length].add($(i, i % length), r, bind((end - (i - start)) / length), function(number) {
              return callback(func(number, i % length));
            });
            slices[i % length][1] += fd;
            result = result + fd;
          }
        }
        return result;
      },
      "finish" : function(_, e, position) {
        /** @type {number} */
        var i = 0;
        /** @type {number} */
        var rowsNum = rows.length;
        for (; i < rowsNum; i++) {
          rows[i].finish(slices[i], $(e, i), $(position + 1, i) - 1);
        }
      },
      "destroy" : function() {
        /** @type {number} */
        var i = 0;
        /** @type {number} */
        var rowsNum = rows.length;
        for (; i < rowsNum; i++) {
          rows[i].destroy();
        }
      }
    };
  }
  var Node = require("mui/datalazylist/render/node");
  /** @type {function(!Object): ?} */
  context.exports = init;
});
define("mui/datalazylist/loader/page", function(canCreateDiscussions, isSlidingUp, meta) {
  /**
   * @param {!Function} filter
   * @return {?}
   */
  function clone(filter) {
    var eventObj;
    var callback;
    var o;
    /** @type {!Array} */
    var _posPoints = [];
    return function(o, a) {
      return 0 === a || a || (a = 1), 1 & a && !callback && (callback = true, filter(function(event) {
        eventObj = event;
        for (; o = _posPoints.shift();) {
          if (o) {
            o.apply(null, [eventObj]);
          }
        }
      })), eventObj !== undefined ? (o && o.apply(null, [eventObj]), eventObj) : (2 & a || o && _posPoints.push(o), eventObj);
    };
  }
  /**
   * @param {!Object} options
   * @return {?}
   */
  function pagination(options) {
    options = options || {};
    var specificListeners = {};
    var limit = options.pageSize;
    var x = options.page || 0;
    var runnerX = options.maxPage || Number.MAX_VALUE;
    var name = options.preloadNum;
    var data = {
      "length" : 0
    };
    return {
      "get" : function(str) {
        return data[str];
      },
      "fetchPage" : function(i, page) {
        var self = this;
        specificListeners[i] = specificListeners[i] || clone(function(unsafeTermFn) {
          /**
           * @return {undefined}
           */
          function init() {
            var params = {
              "page" : i
            };
            options.onData.apply(self, [params, function($scope) {
              if (!params.complete) {
                /** @type {number} */
                params.complete = 1;
                var n = $scope.length;
                if (!limit && options.fixedSize) {
                  limit = n;
                }
                /** @type {number} */
                var s = limit ? i * limit : data.length;
                /** @type {number} */
                var p = 0;
                for (; p < n; p++) {
                  if (!data[p + s]) {
                    data[p + s] = $scope[p];
                    data.length++;
                  }
                }
                if (limit && limit > n || !n || self.totalPage == i + 1) {
                  self.totalNum = limit ? s + n : data.length;
                }
                unsafeTermFn($scope);
              }
            }]);
          }
          if (i > 0 && !limit) {
            self.fetchPage(options.fixedSize ? 0 : i - 1, init);
          } else {
            init();
          }
        });
        specificListeners[i](page);
      },
      "fetch" : function(p, cb, err) {
        /**
         * @return {undefined}
         */
        function sendRequest() {
          v.fetchPage(limit ? Math.floor(p / limit) : x, function(ordered_rend_list) {
            if (!data[p] && ordered_rend_list && ordered_rend_list.length && (v.totalNum === undefined || v.totalNum > p) && x < runnerX) {
              return x++, sendRequest();
            }
            if (cb) {
              cb(data[p]);
            }
            if (!err && name && "complete" === document.readyState) {
              v.fetch(p + name, null, true);
            }
          });
        }
        var v = this;
        if (data[p] || v.totalNum <= p || x > runnerX) {
          return cb && cb(data[p]);
        }
        sendRequest();
      }
    };
  }
  /** @type {function(!Object): ?} */
  meta.exports = pagination;
});
define("mui/datalazylist/loader/static", function(canCreateDiscussions, isSlidingUp, module) {
  /**
   * @param {!Object} a
   * @return {?}
   */
  function api(a) {
    return {
      "totalNum" : a.length,
      "get" : function(num) {
        return a[num];
      },
      "fetch" : function(key, n) {
        if (n) {
          n(a[key]);
        }
      }
    };
  }
  /** @type {function(!Object): ?} */
  module.exports = api;
});
define("mui/review-m/widgets/utils", function(canCreateDiscussions, i, mixin) {
  var isObject = function() {
    /**
     * @param {?} options
     * @param {number} index
     * @return {?}
     */
    function flattenElements(options, index) {
      /** @type {!Array} */
      var result = [];
      /** @type {boolean} */
      var _n = true;
      /** @type {boolean} */
      var a = false;
      var _iteratorError17 = undefined;
      try {
        var info;
        var _i = options[Symbol.iterator]();
        for (; !(_n = (info = _i.next()).done) && (result.push(info.value), !index || result.length !== index); _n = true) {
        }
      } catch (o) {
        /** @type {boolean} */
        a = true;
        _iteratorError17 = err;
      } finally {
        try {
          if (!_n && _i["return"]) {
            _i["return"]();
          }
        } finally {
          if (a) {
            throw _iteratorError17;
          }
        }
      }
      return result;
    }
    return function(arr, options) {
      if (Array.isArray(arr)) {
        return arr;
      }
      if (Symbol.iterator in Object(arr)) {
        return flattenElements(arr, options);
      }
      throw new TypeError("Invalid attempt to destructure non-iterable instance");
    };
  }();
  /** @type {function(?): ?} */
  var isArray = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(lineStringProperty) {
    return typeof lineStringProperty;
  } : function(obj) {
    return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
  };
  mixin.exports = {
    "mergeParams" : function() {
      var url = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "";
      var value = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
      /** @type {!RegExp} */
      var content = /^([^\?]*)(\?){0,1}(.*)$/;
      if ("object" === (void 0 === value ? "undefined" : isArray(value))) {
        /** @type {!Array} */
        var ret = [];
        /** @type {function(!Object<?,T>): !Array<Array<(T|string)>>} */
        var range = (Object.keys, Object.values, Object.entries);
        /** @type {boolean} */
        var _n = true;
        /** @type {boolean} */
        var o = false;
        var _iteratorError17 = undefined;
        try {
          var result;
          var _i = range(value)[Symbol.iterator]();
          for (; !(_n = (result = _i.next()).done); _n = true) {
            var obj = isObject(result.value, 2);
            var method = obj[0];
            var dpVal = obj[1];
            if (dpVal) {
              ret.push([method, "=", dpVal.toString()].join(""));
            }
          }
        } catch (v) {
          /** @type {boolean} */
          o = true;
          _iteratorError17 = err;
        } finally {
          try {
            if (!_n && _i["return"]) {
              _i["return"]();
            }
          } finally {
            if (o) {
              throw _iteratorError17;
            }
          }
        }
        /** @type {string} */
        ret = ret.join("&");
        if (ret) {
          /** @type {string} */
          ret = ret + "&";
        }
        url = url.replace(content, "$1?" + ret + "$3") || url;
      }
      if ("string" == typeof value) {
        /** @type {string} */
        var val = value;
        if (val) {
          /** @type {string} */
          val = val + "&";
        }
        url = url.replace(content, "$1?" + val + "$3") || url;
      }
      return url;
    }
  };
});
define("mui/review-m/tpl/main.xtpl", function(saveNotifs, i, module) {
  var convertService = saveNotifs("mui/xtemplate/index");
  module.exports = function(dtill, Element) {
    var element;
    /**
     * @param {?} indata2
     * @return {?}
     */
    var a = function(indata2) {
      var self = this;
      var root = self.root;
      var sample = self.buffer;
      var scope = self.scope;
      var options = (self.runtime, self.name, self.pos, scope.data, scope.affix, root.nativeCommands);
      var utils = root.utils;
      return utils.callFn, utils.callDataFn, utils.callCommand, options.range, options.foreach, options.forin, options.each, options["with"], options["if"], options.set, options.include, options.parse, options.extend, options.block, options.macro, options["debugger"], sample.data += '<div id="J_CommentsWrapper" class="review-content">\n    <ul class="filter">\n        <li id="J_AllComments" class="comment-filter-none current">\u5168\u90e8</li>\n        <li id="J_AddComments" class="comment-filter-append" data-id="append">\u8ffd\u52a0</li>\n        <li id="J_ImgComments" class="comment-filter-img" data-id="picture">\u6709\u56fe(<b id="J_ImgCommentsNum" class="comment-filter-imgnum num">0</b>)</li>\n    </ul>\n    ',
      sample.data += "\n</div>\n", sample;
    };
    return function(img) {
      return (element = element || new Element(a)) && element.render(img) || "";
    };
  }("", convertService);
});
define("mui/review-m/tpl/list.xtpl", function(saveNotifs, i, module) {
  var convertService = saveNotifs("mui/xtemplate/index");
  module.exports = function(dtill, Element) {
    var element;
    /**
     * @param {?} undefined
     * @return {?}
     */
    var render = function(undefined) {
      /**
       * @param {!Object} to
       * @param {!Object} str
       * @param {?} left
       * @return {?}
       */
      function add(to, str, left) {
        return to.data, to.affix, str.data += '\n            <span class="vip">\u8d85\u7ea7\u4f1a\u5458</span>\n            ', str;
      }
      /**
       * @param {!Object} scope
       * @param {!Object} str
       * @param {?} undefined
       * @return {?}
       */
      function error(scope, str, undefined) {
        var o = scope.data;
        var affix = scope.affix;
        str.data += '\n    <p class="reply">\u638c\u67dc\u56de\u590d:';
        /** @type {number} */
        _segmentStart.line = 13;
        var e = (t = affix.reply) !== undefined ? t : (t = o.reply) !== undefined ? t : scope.resolveLooseUp(["reply"]);
        return str = str.write(e), str.data += "</p>\n    ", str;
      }
      /**
       * @param {!Object} scope
       * @param {!Object} node
       * @param {?} undefined
       * @return {?}
       */
      function foreach(scope, node, undefined) {
        var data = scope.data;
        var affix = scope.affix;
        node.data += '\n          <li><img class="comment-pic" data-url="';
        /** @type {number} */
        _segmentStart.line = 18;
        var type = (t = affix.xindex) !== undefined ? t : (t = data.xindex) !== undefined ? t : scope.resolveLooseUp(["xindex"]);
        var label = scope.resolveLoose(["pics", type], 1);
        node = node.writeEscaped(label);
        node.data += '" src="';
        var text = data;
        return node = node.writeEscaped(text), node.data += '" alt="\u7528\u6237\u8bc4\u8bba"/></li>\n        ', node;
      }
      /**
       * @param {!Object} scope
       * @param {!Object} options
       * @param {?} undefined
       * @return {?}
       */
      function b(scope, options, undefined) {
        var child = scope.data;
        var affix = scope.affix;
        options.data += '\n    <ul class="pics">\n        ';
        /** @type {number} */
        _segmentStart.line = 17;
        /** @type {number} */
        _segmentStart.line = 17;
        var obj = (t = affix.pics_display) !== undefined ? t : (t = child.pics_display) !== undefined ? t : scope.resolveLooseUp(["pics_display"]);
        return options = self.call(node, scope, {
          "params" : [obj],
          "fn" : foreach
        }, options), options.data += "\n    </ul>\n    ", options;
      }
      /**
       * @param {!Object} scope
       * @param {!Object} str
       * @param {?} undefined
       * @return {?}
       */
      function get(scope, str, undefined) {
        var child = scope.data;
        var affix = scope.affix;
        str.data += '\n             <p class="reply">\u638c\u67dc\u56de\u590d:';
        /** @type {number} */
        _segmentStart.line = 27;
        var r = (t = affix.appendComment) !== undefined ? null != t ? views = t.reply : t : (t = child.appendComment) !== undefined ? null != t ? views = t.reply : t : scope.resolveLooseUp(["appendComment", "reply"]);
        return str = str.write(r), str.data += "</p>\n        ", str;
      }
      /**
       * @param {!Object} scope
       * @param {!Object} context
       * @param {?} undefined
       * @return {?}
       */
      function a(scope, context, undefined) {
        var data = scope.data;
        var affix = scope.affix;
        context.data += '\n                <li><a href="';
        /** @type {number} */
        _segmentStart.line = 32;
        var table = data;
        context = context.writeEscaped(table);
        context.data += '" target="_blank"><img class="comment-pic" data-url="';
        var $obj = (t = affix.xindex) !== undefined ? t : (t = data.xindex) !== undefined ? t : scope.resolveLooseUp(["xindex"]);
        var contextAdditions = scope.resolveLoose(["appendComment", "pics", $obj], 1);
        context = context.writeEscaped(contextAdditions);
        context.data += '" src="';
        var root = data;
        return context = context.writeEscaped(root), context.data += '" alt="\u7528\u6237\u8ffd\u8bc4"/></a></li>\n            ', context;
      }
      /**
       * @param {!Object} scope
       * @param {!Object} result
       * @param {?} setname1
       * @return {?}
       */
      function setup(scope, result, setname1) {
        var child = scope.data;
        var affix = scope.affix;
        result.data += '\n        <ul class="pics">\n            ';
        /** @type {number} */
        _segmentStart.line = 31;
        /** @type {number} */
        _segmentStart.line = 31;
        var id1Tbl1 = (t = affix.appendComment) !== setname1 ? null != t ? views = t.pics_display : t : (t = child.appendComment) !== setname1 ? null != t ? views = t.pics_display : t : scope.resolveLooseUp(["appendComment", "pics_display"]);
        return result = self.call(node, scope, {
          "params" : [id1Tbl1],
          "fn" : a
        }, result), result.data += "\n        </ul>\n        ", result;
      }
      /**
       * @param {!Object} scope
       * @param {!Object} buffer
       * @param {?} isLast
       * @return {?}
       */
      function render(scope, buffer, isLast) {
        var child = scope.data;
        var affix = scope.affix;
        buffer.data += '\n    <div class="add">\n        <p class="title">';
        /** @type {number} */
        _segmentStart.line = 24;
        var id1 = (t = affix.appendComment) !== isLast ? null != t ? views = t.days_display : t : (t = child.appendComment) !== isLast ? null != t ? views = t.days_display : t : scope.resolveLooseUp(["appendComment", "days_display"]);
        buffer = buffer.writeEscaped(id1);
        buffer.data += "\u8ffd\u8bc4</p>\n        <blockquote>";
        /** @type {number} */
        _segmentStart.line = 25;
        var entry = (t = affix.appendComment) !== isLast ? null != t ? views = t.content_display : t : (t = child.appendComment) !== isLast ? null != t ? views = t.content_display : t : scope.resolveLooseUp(["appendComment", "content_display"]);
        buffer = buffer.write(entry);
        buffer.data += "</blockquote>\n        ";
        /** @type {number} */
        _segmentStart.line = 26;
        /** @type {number} */
        _segmentStart.line = 26;
        var id1Tbl1 = (t = affix.appendComment) !== isLast ? null != t ? views = t.reply : t : (t = child.appendComment) !== isLast ? null != t ? views = t.reply : t : scope.resolveLooseUp(["appendComment", "reply"]);
        buffer = callback.call(node, scope, {
          "params" : [id1Tbl1],
          "fn" : get
        }, buffer);
        buffer.data += "\n        ";
        /** @type {number} */
        _segmentStart.line = 29;
        /** @type {number} */
        _segmentStart.line = 29;
        var id1Tbl2 = (t = affix.appendComment) !== isLast ? null != t ? views = t.pics : t : (t = child.appendComment) !== isLast ? null != t ? views = t.pics : t : scope.resolveLooseUp(["appendComment", "pics"]);
        return buffer = callback.call(node, scope, {
          "params" : [id1Tbl2],
          "fn" : setup
        }, buffer), buffer.data += "\n    </div>\n    ", buffer;
      }
      /**
       * @param {!Object} item
       * @param {!Object} buffer
       * @param {?} undefined
       * @return {?}
       */
      function set(item, buffer, undefined) {
        var position = item.data;
        var a = item.affix;
        buffer.data += "\n            <li>";
        /** @type {number} */
        _segmentStart.line = 40;
        var id1 = (t = a.k) !== undefined ? t : position.k;
        buffer = buffer.writeEscaped(id1);
        buffer.data += "\uff1a";
        var id0 = (t = a.v) !== undefined ? t : position.v;
        return buffer = buffer.writeEscaped(id0), buffer.data += "</li>\n        ", buffer;
      }
      var t;
      var views;
      var node = this;
      var root = node.root;
      var data = node.buffer;
      var s = node.scope;
      var _segmentStart = (node.runtime, node.name, node.pos);
      var that = s.data;
      var val = s.affix;
      var options = root.nativeCommands;
      var utils = root.utils;
      var self = (utils.callFn, utils.callDataFn, utils.callCommand, options.range, options.foreach, options.forin, options.each);
      var callback = (options["with"], options["if"]);
      options.set;
      options.include;
      options.parse;
      options.extend;
      options.block;
      options.macro;
      options["debugger"];
      data.data += '<li class="item">\n    <div class="info">\n        <div class="author">\n            <span class="nick">';
      /** @type {number} */
      _segmentStart.line = 4;
      var label = (t = val.displayUserNick) !== undefined ? t : (t = that.displayUserNick) !== undefined ? t : s.resolveLooseUp(["displayUserNick"]);
      data = data.writeEscaped(label);
      data.data += "</span>\n            ";
      /** @type {number} */
      _segmentStart.line = 5;
      var obj = (t = val.goldUser) !== undefined ? t : (t = that.goldUser) !== undefined ? t : s.resolveLooseUp(["goldUser"]);
      data = callback.call(node, s, {
        "params" : [obj],
        "fn" : add
      }, data);
      data.data += "\n        </div>\n        <time>";
      /** @type {number} */
      _segmentStart.line = 9;
      var type = (t = val.rateDate_display) !== undefined ? t : (t = that.rateDate_display) !== undefined ? t : s.resolveLooseUp(["rateDate_display"]);
      data = data.writeEscaped(type);
      data.data += "</time>\n    </div>\n    <blockquote>";
      /** @type {number} */
      _segmentStart.line = 11;
      var str = (t = val.rateContent_display) !== undefined ? t : (t = that.rateContent_display) !== undefined ? t : s.resolveLooseUp(["rateContent_display"]);
      data = data.write(str);
      data.data += "</blockquote>\n    ";
      /** @type {number} */
      _segmentStart.line = 12;
      /** @type {number} */
      _segmentStart.line = 12;
      var id2Tbl1 = (t = val.reply) !== undefined ? t : (t = that.reply) !== undefined ? t : s.resolveLooseUp(["reply"]);
      data = callback.call(node, s, {
        "params" : [id2Tbl1],
        "fn" : error
      }, data);
      data.data += "\n    ";
      /** @type {number} */
      _segmentStart.line = 15;
      /** @type {number} */
      _segmentStart.line = 15;
      var id2Tbl2 = (t = val.pics) !== undefined ? t : (t = that.pics) !== undefined ? t : s.resolveLooseUp(["pics"]);
      data = callback.call(node, s, {
        "params" : [id2Tbl2],
        "fn" : b
      }, data);
      data.data += "\n    ";
      /** @type {number} */
      _segmentStart.line = 22;
      /** @type {number} */
      _segmentStart.line = 22;
      var id1Tbl1 = (t = val.appendComment) !== undefined ? t : (t = that.appendComment) !== undefined ? t : s.resolveLooseUp(["appendComment"]);
      data = callback.call(node, s, {
        "params" : [id1Tbl1],
        "fn" : render
      }, data);
      data.data += '\n    <ul class="sku">\n        ';
      /** @type {number} */
      _segmentStart.line = 39;
      /** @type {number} */
      _segmentStart.line = 39;
      var id1Tbl2 = (t = val.attrs) !== undefined ? t : (t = that.attrs) !== undefined ? t : s.resolveLooseUp(["attrs"]);
      return data = self.call(node, s, {
        "params" : [id1Tbl2],
        "fn" : set
      }, data), data.data += "\n    </ul>\n</li>\n", data;
    };
    return function(img) {
      return (element = element || new Element(render)) && element.render(img) || "";
    };
  }("", convertService);
});
define("mui/review-m/tpl/tags.xtpl", function(NFA, canCreateDiscussions, module) {
  var m = NFA("mui/xtemplate/index");
  module.exports = function(dtill, Element) {
    var element;
    /**
     * @param {?} undefined
     * @return {?}
     */
    var a = function(undefined) {
      /**
       * @param {!Object} options
       * @param {!Object} str
       * @param {?} undefined
       * @return {?}
       */
      function b(options, str, undefined) {
        var n = options.data;
        var edge = options.affix;
        str.data += "(";
        var tmp = (val = edge.count) !== undefined ? val : n.count;
        return str = str.writeEscaped(tmp), str.data += ")", str;
      }
      /**
       * @param {!Object} parent
       * @param {!Object} data
       * @param {?} undefined
       * @return {?}
       */
      function add(parent, data, undefined) {
        var node = parent.data;
        var tag = parent.affix;
        data.data += '\n    <li class="tag-product" data-id="';
        /** @type {number} */
        _segmentStart.line = 3;
        var label = (val = tag.id) !== undefined ? val : node.id;
        data = data.writeEscaped(label);
        data.data += '">\n      ';
        /** @type {number} */
        _segmentStart.line = 4;
        var text = (val = tag.tag) !== undefined ? val : node.tag;
        data = data.writeEscaped(text);
        data.data += "";
        var value = (val = tag.count) !== undefined ? val : node.count;
        return data = self.call(config, parent, {
          "params" : [value],
          "fn" : b
        }, data), data.data += "\n    </li>\n  ", data;
      }
      /**
       * @param {!Object} scope
       * @param {!Object} options
       * @param {?} undefined
       * @return {?}
       */
      function a(scope, options, undefined) {
        var node = scope.data;
        var ngModel = scope.affix;
        options.data += "\n  ";
        /** @type {number} */
        _segmentStart.line = 2;
        /** @type {number} */
        _segmentStart.line = 2;
        var value = (val = ngModel.tagClouds) !== undefined ? val : (val = node.tagClouds) !== undefined ? val : scope.resolveLooseUp(["tagClouds"]);
        return options = t.call(config, scope, {
          "params" : [value],
          "fn" : add
        }, options), options.data += "\n", options;
      }
      var val;
      var colWidth;
      var config = this;
      var api = config.root;
      var value = config.buffer;
      var scope = config.scope;
      var _segmentStart = (config.runtime, config.name, config.pos);
      var f = scope.data;
      var ngModel = scope.affix;
      var options = api.nativeCommands;
      var c = api.utils;
      var t = (c.callFn, c.callDataFn, c.callCommand, options.range, options.foreach, options.forin, options.each);
      var self = (options["with"], options["if"]);
      options.set;
      options.include;
      options.parse;
      options.extend;
      options.block;
      options.macro;
      options["debugger"];
      value.data += "";
      /** @type {number} */
      _segmentStart.line = 1;
      /** @type {number} */
      _segmentStart.line = 1;
      var id1Tbl1 = (val = ngModel.tagClouds) !== undefined ? null != val ? colWidth = val.length : val : (val = f.tagClouds) !== undefined ? null != val ? colWidth = val.length : val : scope.resolveLooseUp(["tagClouds", "length"]);
      return value = self.call(config, scope, {
        "params" : [id1Tbl1],
        "fn" : a
      }, value), value.data += "\n", value;
    };
    return function(img) {
      return (element = element || new Element(a)) && element.render(img) || "";
    };
  }("", m);
});
