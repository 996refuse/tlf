#### cats
    * type: html
    * method: get
    * url: http://www.s.cn/list

#### pager
    * type: html
    * method: get
    * url: http://www.s.cn/list
    * xpath: //div[@class='clearfix']/table/tr/td[@class='pagernum']/a[last()]

#### price, stock
    * type: html
    * method: get
    * url: http://www.s.cn/list/pgX #return from pager
        * X: page number
    * price:
        * xpath: //div[@class='product_list']/dl
    * stock:
        * regex: (?<=store\"\:).+(?=\,)
