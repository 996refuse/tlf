#### cats, pager, price
    * from: html

#### stock
    * from: api
    * url1: http://www.d1.com.cn/ajax/flow/listInCart.jsp
        * method: post
        * args: (id, type, count)
        * description:
        > 对于‘男装、女装’分类需要再请求url2
    * url2: http://m.d1.cn/ajax/flow/InCartnew.jsp?gdsid=%1&count=1&skuId=%2
        * method: get
        * %1: 商品ID
        * %2: skuid(从url1返回)