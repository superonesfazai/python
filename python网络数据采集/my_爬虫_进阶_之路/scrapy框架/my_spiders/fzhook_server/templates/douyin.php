<?php

 
//在这里设置网站信息
$title		="标题";
$keywords	="我是网站关键词";
$description="我是网站描述";

?>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://lib.baomitu.com/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://lib.baomitu.com/bootstrap-table/1.12.1/bootstrap-table.min.css" rel="stylesheet">
    <title><?php echo $title;?></title>
    <meta name="keywords" content="<?php echo $keywords;?>">
    <meta name="description" content="<?php echo $description;?>">
</head>
<body>

<div class="container">
    <div class="jumbotron">
        <h1>抖音短视频在线解析</h1>
        <p>完美还原视频的最初模样~</p>
    </div>
    <input class="form-control" type="text" id="url" placeholder="请将APP里复制的视频链接粘贴到这里"><br>
    <button type="submit" class="btn btn-success btn-lg btn-block" id="magic">点击还原！</button><br>
    <div id="str"></div>
</div>
<script src="https://lib.baomitu.com/jquery/3.3.1/jquery.min.js"></script>
<script src="https://lib.baomitu.com/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="https://lib.baomitu.com/layer/3.1.1/layer.js"></script>
<script type="text/javascript">
    $(document).ready(function(){
        $('#magic').click(function(){
            layer.load(1, {shade: [0.1,'#fff']});
            $.ajax({
                type: "POST",
                url: "http://douyin.qlike.cn/parse.php?app=douyin",
                dataType: "html",
                data:"url="+$.trim($("#url").val()),
                success: function(data){
                    layer.closeAll('loading');
                    $("#str").html(data);
                },
                error: function(error) {
                    layer.closeAll('loading');
                    layer.msg('出错了，请再试一下！');
                }
            });
        });
    });
</script>
</body>
</html>

