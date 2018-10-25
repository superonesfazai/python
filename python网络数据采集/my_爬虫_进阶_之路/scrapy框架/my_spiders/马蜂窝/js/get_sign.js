function get_sign() {
    function post(func) {
        setTimeout(function() {
            func();
        }, paymentChannel.queryTimes < 21 ? 500 : 1e3);
    }

    function(canCreateDiscussions, e, floor) {
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
    }

    paymentChannel.signKey = (0, _thirdapp2.default)();
    sign = (0, _params2.default)(function(sideLength) {
        return [paymentChannel.departCode, paymentChannel.destCode, sideLength, paymentChannel.departDate, paymentChannel.destDate, sideLength].join("");
    }(paymentChannel.signKey));

    return sign;
}