#### price, pagecount
    * from: api
    * method: et
    * url: 'http://shop.lenovo.com.cn/search/getproduct.do?plat=4&categorycode=%0&keyword=&sorder=0&spage=%1&sarry=1'
        %0: gid
        %1: pagenum

#### stock
    * from: api
    * method: get
    * url: http://shop.lenovo.com.cn/srv/getginfo.do?plat=4&gcodes=%0&salestype=0
        %0: gid
