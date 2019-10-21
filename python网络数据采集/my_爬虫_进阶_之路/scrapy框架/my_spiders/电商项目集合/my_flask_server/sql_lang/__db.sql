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

-- 创建company_info表
use Gather;
create table company_info(
	id int identity(1,1) primary key,
	province_id varchar(30) not null,
	city_id varchar(30),
	unique_id nvarchar(200) not null unique,
	company_url nvarchar(max),
  company_link nvarchar(max),
  company_name nvarchar(300),
  legal_person nvarchar(50),
  phone nvarchar(max),
  email_address nvarchar(max),
  address nvarchar(1000),
  brief_introduction nvarchar(max),
  business_range nvarchar(max),
  founding_time datetime,
	create_time datetime,
	employees_num nvarchar(1000)
);

-- 创建新版采集评论存储表
create table goods_comment_new(
  id int identity(1,1) primary key,
  goods_id varchar(200) not null,
  create_time datetime not null,
  buyer_name nvarchar(200) not null,
  head_img_url nvarchar(max),
  sku_info nvarchar(max),
  purchase_quantify int,
  comment_content nvarchar(max) not null,
  comment_date datetime not null,
  img_url_list nvarchar(max),
  video_url nvarchar(max),
  star_level int,

  append_comment_content nvarchar(max),
  append_comment_date datetime,
  append_comment_img_url_list nvarchar(max),
);

-- 创建zwm_buss_settle_records表
create table zwm_buss_settle_records(
  id int identity(1, 1) primary key,
  unique_id nvarchar(100) not null,
  create_time datetime,
  shop_name nvarchar(200) not null,
  shop_id varchar(100) not null,
  agent_name nvarchar(150) not null,
  top_agent_name nvarchar(100) not null,
  date_settle_type nvarchar(50) not null,
  trans_amount decimal(18, 2) not null,
  service_charge decimal(18, 2) default 0,
  accounting_amount decimal(18, 2) not null,
  trans_date datetime not null,
  trans_status int not null ,
  settle_type nvarchar(50) not null,
  settle_date datetime,
);

-- 创建zwm_buss_manage_records表
create table zwm_buss_manage_records(
  id int identity(1, 1) primary key,
  unique_id nvarchar(100) not null,
  create_time datetime,
  modify_time datetime,
  agent_name nvarchar(150) not null,
  top_agent_name nvarchar(100) not null,
  shop_type nvarchar(100) not null,
  is_high_quality_shop int not null,      -- 0 否 1是
  shop_id varchar(100) not null,
  shop_chat_name nvarchar(200) not null,
  phone_num nvarchar(100) not null,
  shop_chant_num int not null,
  sale nvarchar(150) not null,
  is_real_time int not null,              -- 0 否 1是
  approve_date datetime,
  rate decimal(18, 4) not null,
  account_type nvarchar(100) not null,
  apply_time datetime,
  process_context nvarchar(2000),         --可为空
  is_non_contact int not null,            -- 0 否 1是
  approval_status int not null,           -- 审核通过0, 待审核1, 退回2
  approval_status_change_time datetime,
);

-- 创建荐好ops article_id去重表
create table recommend_good_ops_article_id_duplicate_removal(
  id int identity(1, 1) primary key,
  unique_id nvarchar(100) not null unique,
  create_time datetime,
);

create table coupon_info(
  id int identity(1, 1) primary key,
  unique_id nvarchar(100) not null unique,
  create_time datetime,
  goods_id varchar(200) not null,
  coupon_url nvarchar(1500) not null,
  coupon_display_name nvarchar(1000),
  coupon_value decimal(18, 2),
  threshold decimal(18, 2),
  begin_time datetime,
  end_time datetime,
  use_method nvarchar(2000),
);