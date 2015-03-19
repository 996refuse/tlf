#### price, stock
    * type: api
    * method: get
    * url: http://list.mi.com/accessories/ajaxView/0-0-0-a-b-0
        * arguments:
            * a:
                * 0: 显示全部商品
                * 1: 显示有货商品
            * b: 页序号
        * return: json as j
    * pager:
        * pagenum: j['data']['total_pages']
    * price: j['data']['product']['price_min']
    * stock: !j['data']['product']['is_cos']
        * is_cos: 缺货标记