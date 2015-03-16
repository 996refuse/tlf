def task_filter(x): 
    return {
            "url": x,
            } 


"""
http://www.miyabaobei.com/instant/item/getOutletsItemsInfo?ids=1001463-1014908-1004202-1007429-1007427-1005020-1000344-1000363-1000743-1000897-1000898-1000899-1000343-1000744-1001462-1002153-1002156-1002161-1002163-1002165-1002794-1002870-1003896-1004100-1004116-1004118-1004199-1004432-1004433-1005021-1005060-1005061-1007319-1007320-1007426-1010341-1012907-1012913-1013691-1013693-

"""



def stock_task_filter(items):
    l = len(items)
    n = l / 40 
    if l % 40:
        n += 1 
    ret = []
    base ="http://www.miyabaobei.com/instant/item/getOutletsItemsInfo?ids="
    for i in range(n): 
        group = items[i*40:(i+1)*40] 
        ids = "-".join([k[1] for k in group]) + "-"
        ret.append({
                "url": base+ids
                })
    return ret



