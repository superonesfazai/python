var page = require('webpage').create();
var videoUrl = phantom.args[0];
var page.open(videoUrl, function (){
    window.setTimeout(function(){
        phantom.exit();
    }, 10);
});