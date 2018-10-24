var collectUrl_gsxt = "http://fwtj.gsxt.gov.cn";
var nodenum_gsxt = "320000"; //修改为省份节点号

function addScriptTag_gsxt(src) {
//	var script = document.createElement('script');
//	script.setAttribute("type", "text/javascript");
//	script.src = src;
	jQuery.ajax({
        url: src,
        async: true,
        type: 'get',
        dataType: 'JSONP'
    });
}

function searchKeywordCollect_gsxt(searchkeyword) {
	var param = "{'SEARCH_KEYWORD':'"+searchkeyword
	+"','NODENUM':'"+nodenum_gsxt+"'}";
	addScriptTag_gsxt(collectUrl_gsxt + "/statistics/addSearchLog?param=" + param);
}