# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WoocommerceItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	
	name = scrapy.Field()
	sale_price = scrapy.Field()
	regular_price = scrapy.Field()
	currency = scrapy.Field()
	categories = scrapy.Field()
	description = scrapy.Field()
	
	url = scrapy.Field()
	sku = scrapy.Field()
	published = scrapy.Field()
	is_featured = scrapy.Field()
	visibility_in_catalog = scrapy.Field()
	short_description = scrapy.Field()

	date_sale_price_starts = scrapy.Field()
	date_sale_price_ends = scrapy.Field()
	tax_status = scrapy.Field()
	tax_class = scrapy.Field()
	in_stock = scrapy.Field()
	stock = scrapy.Field()
	backorders_allowed = scrapy.Field()
	sold_individually = scrapy.Field()
	weight = scrapy.Field()
	length = scrapy.Field()
	width = scrapy.Field()
	height = scrapy.Field()
	allow_customer_reviews = scrapy.Field()
	purchase_note = scrapy.Field()

	tags = scrapy.Field()
	shipping_class = scrapy.Field()
	images = scrapy.Field()
	download_limit = scrapy.Field()
	download_expiry_days = scrapy.Field()
	parent = scrapy.Field()
	grouped_products = scrapy.Field()
	upsells = scrapy.Field()
	cross_sells = scrapy.Field()
	external_URL = scrapy.Field()
	button_text = scrapy.Field()
	position = scrapy.Field()

	attribute_1_name = scrapy.Field()
	attribute_1_values = scrapy.Field()
	attribute_1_visible = scrapy.Field()
	attribute_1_global = scrapy.Field()
	attribute_2_name = scrapy.Field()
	attribute_2_values = scrapy.Field()
	attribute_2_visible = scrapy.Field()
	attribute_2_global = scrapy.Field()
	meta__wpcom_is_markdown = scrapy.Field()
	download_1_name = scrapy.Field()
	download_1_URL	 = scrapy.Field()
	download_2_name = scrapy.Field()
	download_2_URL = scrapy.Field()
