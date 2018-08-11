--创建用户表:
--create table ali_spider_employee_table(
--	username varchar(11) primary key,
--	passwd varchar(30) not null
--);

-- 创建zhe_800_xianshimiaosha表
use Gather;

create table dbo.zhe_800_xianshimiaosha(
	id int identity(1,1) primary key,
	username nvarchar(50),
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_image_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	stock_info nvarchar(500),
	miaosha_time nvarchar(500),
	session_id varchar(40),
	page int
);

-- 创建juanpi_xianshimiaosha表
use Gather;

create table dbo.juanpi_xianshimiaosha(
	id int identity(1,1) primary key,
	username nvarchar(50),
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_image_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	stock_info nvarchar(500),
	miaosha_time nvarchar(500),
	tab_id int not null,
	page int not null
);

-- 创建pinduoduo_xianshimiaosha表
use Gather;

create table dbo.pinduoduo_xianshimiaosha(
	id int identity(1,1) primary key,
	username nvarchar(50),
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_image_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	stock_info nvarchar(500),
	miaosha_time nvarchar(500)
);

-- 创建jd优选达人推荐文章及其商品
use Gather;
create table dbo.jd_youxuan_daren_recommend(
	id int identity(1,1) primary key,
	nick_name nvarchar(50),
	head_url nvarchar(500),
	profile nvarchar(400),
	share_id varchar(100) not null unique,
	title nvarchar(400),
	comment_content nvarchar(max),
	share_img_url_list nvarchar(max),
	goods_id_list nvarchar(max),
	div_body nvarchar(max),
	gather_url nvarchar(400)
);

-- 创建zhe_800_pintuan表
create table dbo.zhe_800_pintuan(
	id int identity(1,1) primary key,
	username nvarchar(50),
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_img_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	all_sell_count nvarchar(100),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	page int
);


-- 创建juanpi_pintuan表
create table dbo.juanpi_pintuan(
	id int identity(1,1) primary key,
	username nvarchar(50),
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_image_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	all_sell_count nvarchar(100),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	page int
);

-- 创建taobao_tiantiantejia表
create table taobao_tiantiantejia(
	id int identity(1,1) primary key,
	shop_name nvarchar(200),
	account	nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_img_url nvarchar(max),
	sku_name nvarchar(max),
	sku_info nvarchar(max),
	month_sell_count nvarchar(100),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	tejia_begin_time datetime,
	tejia_end_time datetime,
	block_id varchar(20),
	tag_id varchar(50),
	father_sort nvarchar(50),
	child_sort nvarchar(50)
);

-- 创建sina_weibo表
create table sina_weibo(
	id int identity(1, 1) primary key,
	nick_name nvarchar(200) not null unique,
	sina_type nvarchar(40),
	head_img_url nvarchar(400)
)

-- 创建mia_xianshimiaosha表
create table mia_xianshimiaosha(
	id int identity(1,1) primary key,
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_image_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	miaosha_time nvarchar(500),
	miaosha_begin_time datetime,
	miaosha_end_time datetime,
	pid int
)

-- 创建mia_pintuan表
create table mia_pintuan(
	id int identity(1,1) primary key,
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	spider_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_img_url nvarchar(max),
	sku_name nvarchar(max),
	sku_info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	pintuan_time nvarchar(500),
	pintuan_begin_time datetime,
	pintuan_end_time datetime,
	all_sell_count varchar(40),
	pid int
)

-- 创建mogujie_miaosha表
create table mogujie_xianshimiaosha(
	id int identity(1,1) primary key,
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_image_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	miaosha_time nvarchar(500),
	miaosha_begin_time datetime,
	miaosha_end_time datetime,
	event_time int
)

-- 创建mogujie_pintuan表
create table mogujie_pintuan(
	id int identity(1,1) primary key,
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	spider_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_img_url nvarchar(max),
	sku_name nvarchar(max),
	sku_info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	pintuan_time nvarchar(500),
	pintuan_begin_time datetime,
	pintuan_end_time datetime,
	all_sell_count varchar(40),
	fcid int,
	page int,
	sort nvarchar(20)
)

-- 创建chuchujie_xianshimiaosha表
create table chuchujie_xianshimiaosha(
	id int identity(1,1) primary key,
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_image_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	miaosha_time nvarchar(500),
	miaosha_begin_time datetime,
	miaosha_end_time datetime,
	gender varchar(5),
	page int
)

-- 创建jumeiyoupin_xianshimiaosha表
create table jumeiyoupin_xianshimiaosha(
	id int identity(1,1) primary key,
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_image_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	miaosha_time nvarchar(500),
	miaosha_begin_time datetime,
	miaosha_end_time datetime,
	page int
)

-- 创建jumeiyoupin_pintuan表
create table jumeiyoupin_pintuan(
	id int identity(1,1) primary key,
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	spider_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_img_url nvarchar(max),
	sku_name nvarchar(max),
	sku_info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	pintuan_time nvarchar(500),
	pintuan_begin_time datetime,
	pintuan_end_time datetime,
	all_sell_count varchar(40),
  sort nvarchar(20),
	tab varchar(40),
	page int
)

-- 创建all_goods_comment表
create table all_goods_comment(
  id int IDENTITY(1, 1) PRIMARY KEY,
  goods_id VARCHAR(100) not NULL UNIQUE,
  create_time datetime,
  modify_time datetime,
  comment_info nvarchar(max)
)

-- 创建tao_qianggou_xianshimiaosha表
use Gather;
create table tao_qianggou_xianshimiaosha(
	id int identity(1,1) primary key,
	shop_name nvarchar(100),
	goods_name nvarchar(300),
	sub_title nvarchar(300),
	price decimal(18, 2),
	taobao_price decimal(18, 2),
	goods_url nvarchar(500),
	create_time datetime,
	detail_info nvarchar(max),
	all_image_url nvarchar(max),
	sku_name nvarchar(max),
	sku_Info nvarchar(max),
	property_info nvarchar(max),
	site_id int,
	goods_id varchar(100) not null unique,
	is_convert int,
	is_delete int,
	is_modfiy int,
	modfiy_time datetime,
	schedule nvarchar(500),
	miaosha_time nvarchar(500),
	miaosha_begin_time datetime,
	miaosha_end_time datetime,
	page int,
	spider_time nvarchar(50)
);

-- 创建goods_keywords表
create table goods_keywords(
  id int IDENTITY(1, 1) PRIMARY key,
  keyword nvarchar(300),
  is_delete INT DEFAULT 0
)

-- 创建goods与关键字的中间表
CREATE TABLE goods_id_and_keyword_middle_table(
  id int IDENTITY(1, 1) PRIMARY KEY,
  goods_id VARCHAR(300),
  keyword_id INT,
  is_delete INT DEFAULT 0
)