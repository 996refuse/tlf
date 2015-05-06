#import pyrant
import binascii
import re
import pdb

site_template=  {
     1: '/aw/d/@?/;/aw/d/@/;/aw/d/@?;/aw/d/@;/dp/product-description/@?/;/dp/product-description/@/;/dp/product-description/@?;/dp/product-description/@;/product/@?/;/product/@/;/product/@?;/product/@;/dp/@?/;/dp/@/;/dp/@?;/dp/@;asin=@&;asin=@;gp/aw/ol/@/',
     2: 'pid=@&;pid=@;product_id=@&;product_id=@?;product_id=@;http://product.dangdang.com/@.html',
     3: '360buy.com/product/@.html;360buy.com/@.html;jd.com/product/@.html;www.jd.com/tuan/[0-9]+-@.html;;re.jd.com/cps/item/@.html;jd.com/@.html;/bigimage.aspx?id=@&;/bigimage.aspx\\?id=@;wareId=@&;wareId=@',
     4: '/index@.shtml',
     5: '',
     6: '/product/@.html;/goods@/;/goods@_;/goods@-;/goods@',
     7: 'Product/@.htm',
     8: 'product/@/;product/@',
     9: 'www.redbaby.com.cn/[^/]+/@.html',
     10: 'goodscode=@&;goodscode=@;/item/[^/]+/@&;/item/[^/]+/@?;/item/[^/]+/@',
     11: '/goods-@.html',
     12: '/product/@.html',
     13: 'product.lefeng.com/[^/]+/@.html;product/@.html;productId=@&;productId=@;/product/index/pid/@&;/product/index/pid/@?;/product/index/pid/@',
     14: 'http://www.s.cn/@.html',
     15: '/item-@.html;gwdid=@;pid=@&;pid=@',
     16: '/product/@.html',
     17: '/p-@.html;stylecode=@&;stylecode=@',
     18: 'Goods.GoodsId=@.html',
     19: 'http://item.vancl.com/@.html;http://item.vt.vancl.com/@.html;http://m.vancl.com/style/index/@&;http://m.vancl.com/style/index/@?;http://m.vancl.com/style/index/@',
     20: 'product-@.html',
     21: '/detail-[a-zA-Z]+-@.html;/shoe-@.html;/bag-@.html;/clothes-@.html;/product/detail/@.html;/outlets/detail/[0-9]+-@.html',
     22: 'shoe-@.html;pid=@&;pid=@',
     23: 'http://www.buy007.com/[^/]/[^/]/@.html',
     24: 'commodity-@-;commodity-@.htm;/tbk-@.htm;id=@&;id=@',
     25: 'm.suning.com/product/@.html;/snupgbpv_10052_10051_@_;product.suning.com/0[0-9]+/@.html;product.suning.com/@-;product.suning.com/@.html;_-[0-9]+_@_;/sprd_10052_[0-9]+_@__.html;productId=@&;productId=@;_10052_[0-9]+_@_',
     26: 'product/@.html',
     27: '/product-@.html;ProductInfo.aspx\\?id=@&;ProductInfo.aspx\\?id=@;ProductInfo.aspx\\?g@',
     28: 'item.gome.com.cn/@.html;/product-@-1-0.html;/product-@-0-0.html;/product/@.html;product/@-',
     29: 'product-[0-9]+-@.htm',
     30: '/d-@.html',
     31: 's.yhd.com/item/[0-9]+_@?;s.yhd.com/item/[0-9]+_@/;s.yhd.com/item/[0-9]+_@;item/lp/[0-9]+_@?;item/lp/[0-9]+_@/;item/lp/[0-9]+_@;/item/@?;/item/@_;/item/@&;/item/@;productID=@&;productID=@;product/@_;product/@?;product/@;/mw/productsquid/@/',
     32: 'Product-[0-9]+-@.htm;Product-[0-9]+-@&;Product.do\\?id=@&;Product.do\\?id=@;related-[0-9]+-@.htm',
     33: 'product/single/@',
     34: 'product/@.html',
     35: 'product/@.html;/product/@.shtml;xiu.com/@.shtml',
     36: '/item/@&;/item/@?;/item/@;pshow-@.html;itemid/@&;itemid/@;itemid=@&;itemid=@',
     37: 'http://item.vjia.com/@.html;Product_@/;StyleDetail_[0-9]+_@_;/detail/[0-9]+/@/',
     38: 'product/[0-9]+/[0-9]+/@.htm',
     39: 'product/@.htm',
     40: 'goods/[^/]+/[^/]+/@.html;goods/[^/]+/@.html;goods/@.html;id=@&;id=@',
     41: 'product/N@.htm;product/N@.shtml;product/U@.htm;product/U@.shtml;product-N@.;product-U@.',
     42: 'pr_id=@&;pr_id=@',
     43: 'goods/@.html;/product/@.html', 
     45: 'itemno=@&;itemno=@',
     46: 'gcd=@&;gcd=@',
     47: 'goods-@.html', 
     49: 'product-@.jhtml',
     50: 'product/@.html',
     51: 'product_@.html',
     52: 'product-@.shtml',
     53: '-@.html',
     54: 'products/info/@.html;product/info/@.html',
     55: 'productId=@&;productId=@',
     56: 'goods-@.html',
     57: 'goods_@.html',
     58: 'prono=@&;prono=@',
     59: 'proid=T@&;proid=T@;proid=@&;proid=@;/product/T@.aspx;/product/@.aspx',
     60: 'BookInfo.aspx\\?id=@&;BookInfo.aspx\\?id=@;china-pub.com/@&;china-pub.com/@?;china-pub.com/@',
     61: 'www.bookschina.com/@.htm;book_id=@&;book_id=@',
     62: '/product/@/;/product/@&;/product/@',
     63: 'pno=@&;pidno=@&;pidno=@;/Product/@.html',
     64: 'products/@.html;product/@.html', 
     66: 'http://item.yintai.com/@.htm;itemcode=@&;itemcode=@',
     67: 'goods_[0-9]+-@.html;goods-@.html',
     68: 'search/final-@.htm', 
     70: 'product/[^/]+/@.html',
     71: 'item_@.html;prodID=@&;prodID=@',
     72: 'gid=@&;gid=@;www.happigo.com/[^/]+/[^/]+/[^/]+/@.html;mall.happigo.com/goods-@.html',
     73: '/product/@.html',
     74: 'goods-@-',
     75: 'id=@&;id=@',
     76: 'id=@&;id=@', 
     78: 'http://www.new7.com/product/info/@-;http://www.new7.com/product/@-;http://www.new7.com/product/info/@.html;http://www.new7.com/product/@.html',
     79: 'key=@&;key=@',
     80: 'product.pcbaby.com.cn/a/@.html', 
     82: 'www.binggo.com/[^/]+/@.html',
     83: '&id=@&;&id=@;mallstItemId=@&;mallstItemId=@;id=@&;id=@',
     84: 'productid=@&;Productid=@&;productid=@;Productid=@;/watchs/@.html;/bag/@.html;/cosmetic/@.html;/jewelry/@.html',
     85: 'prod-@.html;comid=@&;comid=@;product/@.htm',
     86: 'deal/[a-z]+[0-9]+p@zc.html;deal/[a-z]+[0-9]+p@.html;product_@.html;product_id=@&;product_id=@;deal/@.html;hash_id=@',
     87: 'id=@&;id=@',
     88: 'goods@.htm',
     89: 'product/@.html',
     90: 'goodsdetail-@.html;goodsdetaila-@.html',
     91: 'product/pro@.html',
     92: 'product-@.html',
     93: '/p_@.html;/p_@.shtml;/sku-([0-9a-z]+-)+@.html;/sku-([0-9a-z]+-)+@.shtml;productid/@',
     94: '/item/@_;/item/@?;/item/@;productID=@&;productID=@;product/@_;product/@?;product/@.html;product/@',
     95: '/product-@.shtml',
     96: '/smoke-product-@.html',
     97: '/product/@.html',
     98: '/product/@.html;pdtID=@&;pdtID=@;PdtId=@;PdtId=@&;http://item.muyingzhijia.com/@.html',
     99: '/lingshi-@.htm',
     100: '/goods_@.shtml;/Goods/@.shtml',
     101: 'goods/@.html', 
     103: 'http://www.jiuxian.com/goods-@.html;/goods/view/@&;/goods/view/@',
     104: '/goods-@.html',
     105: '/product-@.html',
     106: 'p-@.html;productID=@&;productID=@',
     107: '/goods@.htm',
     108: '/item-id-@.htm',
     109: '/item/@.html',
     110: 'http://detail.bookuu.com/@.html',
     111: '/product/@.html',
     112: 'product-@.html',
     113: '/Goods/StyleDetail_@.htm',
     114: '/goodsinfo/@.html',
     115: '/product/@&;/product/@',
     116: '/goods-@.html',
     117: '/Product-@.htm',
     118: '/Product/p-@.html',
     119: 'product-@.html',
     120: 'product-@.html',
     121: 'product-@.html',
     122: '/shoe-\\S+-\\S+-@.html',
     123: '&id=@&;&id=@;mallstItemId=@&;mallstItemId=@;id=@&;id=@',
     124: '/pid-@.jhtml;pid=@&;pid=@',
     125: '/product/@.html;/product-@.html;/product-@.mobi',
     126: '/products/[0-9]+/@.html',
     127: '/item-@.html',
     128: '/product-@.html',
     129: 'detail-([0-9]+-)+@.html;product_id=@&;product_id=@;product-[0-9]+-@-intro.html',
     130: '/goods-@-;/goods-@.html',
     131: '/product_@_',
     132: '/item/@-',
     133: '&id=@;&Id@',
     134: '/product/@.html;/item-[^-]+-@,;/item-@,;/item-[^-]+-@&;/item-[^-]+-@?;/item-[^-]+-@;/item-@&;/item-@?;/item-@',
     135: 'product-@.html',
     136: '/product/@/;/product/@?;/product/@', 
     138: '/goods-@.html',
     139: 'miqi.cn/[^/]+/p@.htm;id=@',
     140: '/product/@.html;/group/@.html;/product/@',
     141: '/product/@-', 
     155: '/product/@.html', 
     166: 'http://www.taoshu.com/@.html',
     167: 'http://item.mi.com/@.html;/item/@?;/item/@&;/item/@', 
     169: '/book/@/;/book/@?;/book/@', 
     174: '/product/@.html',
     175: '/product/@.html', 
     178: '/web/pro/@&;/web/pro/@?;/web/pro/@',
     179: 'deal/[a-z]+[0-9]+p@zc.html;deal/[a-z]+[0-9]+p@.html;product_@.html;product_id=@&;product_id=@;deal/@.html;hash_id=@',
     180: '/item/@/;/item/@?;/item/@',
     181: 'http://item.feifei.com/[A-Za-z]+@.html',
     195: '/item-@.html',
     210: 'http://www.supuy.com/products/@.html',
     217: 'http://www.rrs.com/items/@',
     218: 'http://tv.coocaa.com/goods/@.htm',
     1015: '/item-@.html;pid=@&;pid=@',
     1025: '_-[0-9]+_@_;/sprd_10052_10051_@__.html;productId=@&;productId=@;_10052_10051_@_',
     1031: '/item/@_;/item/@?;/item/@;productID=@&;productID=@;product/@_;product/@?;product/@',
     1032: 'Product-[0-9]+-@.htm;Product-[0-9]+-@&;Product.do?id=@&;Product.do?id=@',
     1124: '/pid-@.jhtml;pid=@&;pid=@', 
     2015: '/item-@.html;pid=@&;pid=@', 
     2031: '/item/@_;/item/@?;/item/@;productID=@&;productID=@;product/@_;product/@?;product/@',
     2032: 'Product-[0-9]+-@.htm;Product-[0-9]+-@&;Product.do?id=@&;Product.do?id=@', 
     3015: '/item-@.html;pid=@&;pid=@', 
     3031: '/item/@_;/item/@?;/item/@;productID=@&;productID=@;product/@_;product/@?;product/@', 
     4015: '/item-@.html;pid=@&;pid=@',
     4031: '/item/@_;/item/@?;/item/@;productID=@&;productID=@;product/@_;product/@?;product/@',
     5015: '/item-@.html;pid=@&;pid=@'
 }


TT_SERVER = ""

def gen_urlcrc(site_id, url): 
    url = url.split("#")[0] 
    pid = url.split("?")[0]
    if site_id not in site_template:
        return pid.replace("&", "")
    tm = site_template[site_id]
    for i in tm.split(";"):
        pair = i.split("@") 
        if len(pair) != 2:
            continue
        start_id = pair[0]
        end_id = pair[1]
        m = re.search(start_id, url, re.I)
        if m:
            pos_start = m.end(0)
            if not end_id:
                pid = url[pos_start:]
                break 
            pos_end = url.find(end_id, pos_start) 
            if pos_end > 0:
                pid = url[pos_start:pos_end]
                break 
    return pid.replace("&", "")


sp_site = set((25, 1025, 2025, 3025, 31, 1031, 2031, 3031, 4031)) 

def get_urlcrc(site_id, url):
    if site_id in sp_site:
        return url
    pid = gen_urlcrc(site_id, url)
    if site_id in (1, 7, 66):
        pid = pid.upper() 
    if pid:
        try:
            n = int(pid)
            if n > 2147483647:
                return binascii.crc32(pid)
            return n
        except ValueError:    
            return binascii.crc32(pid) 
    url = url.split("#")[0]
    return binascii.crc32(url.upper()) 
