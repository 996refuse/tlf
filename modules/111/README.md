#### cats, id
    * from: html

#### price
    * from: api
    * method: get
    * url: http://www.111.com.cn/interfaces/item/itemPrice.action?itemids=$gid
        * gid: 商品编号

#### stock
    * from: api
    * method: get
    * url: http://www.111.com.cn/interfaces/specials.action?itemid=$pid&pno=$pno'
        * pid: 商品编号
        * pno: unknown
    * description:
    > 可以从API中获得库存，但$pno需要从item_page中获得。