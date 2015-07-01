import spider 
import pdb


def load_func():
    import os.path
    func = spider.load_func("os.path.dirname") 
    assert func == os.path.dirname


def load_price_range(): 
    import os
    c = """#a
    b
    c
    d
    #e
    f
    g
    """ 
    fn = "/tmp/test.tmp"
    f = open(fn, "w+")
    f.write(c)
    f.close() 
    result = spider.load_price_range(fn)
    os.remove(fn)
    assert "a" in result and result['a'] == ["b", "c", "d"]
    assert "e" in result and result["e"] == ["f", "g"] 
    x = spider.replace_url_with_ranges(["n", "a", "e"], result) 
    assert len(x) == len(["n", "b", "c", "d", "f", "g"])
    assert "f" in x and "g" in x and "e" not in x



def forward_file(): 
    import zlib
    spider.CONFIG["fconfig"] = {
            "type": "url",
            "path": "/tmp",
            "compress": True,
            } 
    spider.forward_file({
        "text": "abcd",
        "url": "test.url.tmp",
        })
    assert zlib.decompress(open("/tmp/test.url.tmp").read()) == "abcd"
    spider.CONFIG["fconfig"] = { 
            "type": "xpath",
            "path": "/tmp",
            "compress": True,
            "suffix": ".tmp",
            "xpath": "//title/text()"
            } 
    text = "<html><title>abcd</title></html>"
    spider.forward_file({ 
        "text": text,
        "url": "test.url.tmp",
        }) 
    assert zlib.decompress(open("/tmp/abcd.tmp").read()) == text 



def redis_nodes(): 
    spider.CONFIG["site_id"] = 1111
    nodes = {}
    dst = {
            "node": "default",
            "name": "anyname",
            "queue_pat": ("%s_%s", "site_id")
            } 
    spider.eval_lua_scripts_for_node(nodes, dst) 
    assert "default" in nodes and dst["name"] == "anyname_1111"
    node = nodes["default"]
    spider.list_push_n(node, "list_push_n_test", *[1,2,3,4])
    assert node.llen("list_push_n_test") == 4 
    assert len(spider.list_pop_n(node, "list_push_n_test", 4)) == 4
    spider.set_push_n(node, "set_push_n_test", *[1,2,3,4])
    assert node.scard("set_push_n_test") == 4 
    assert len(spider.set_pop_n(node, "set_push_n_test", 4)) == 4 
    dst = {
            "node": "default",
            "name": "anyname",
            "queue_pat": ("%s_%s_suffix", "site_id")
            } 
    spider.eval_lua_scripts_for_node(nodes, dst) 
    assert dst["name"] == "anyname_1111_suffix"



def forward_dst():
    import redis
    dst = {
            "node": "default",
            "name": "anyname",
            "type": "kv", 
            } 
    db = { 
            "host": "127.0.0.1",
            "port": 6379,
            "db": 0 
        }
    r = redis.StrictRedis(**db) 
    spider.forward_one(r, {1 : 2}, dst)
    assert r.get("1") == "2"


def is_worker_alive():
    import os
    assert spider.is_worker_alive(os.getpid(), "test", "me")
    assert not spider.is_worker_alive(0xfffffff, "bug", "bug") 



def diff_promo():
    from spider import llkv
    import msgpack
    profile = {
            "llkv": llkv.Connection("127.0.0.1", 8000)
            }
    l = [("1-1", "abc"), ("1-2", "efg")]
    result = spider.diff_promo_items(profile, l)
    assert result == l



def format_price():
    from spider import format_price
    spider.CONFIG["site_id"] = "test"
    pdb.set_trace()
    ret = format_price([("1", 2, 1), ("2", "2", 1), (3, 2, 1), (4, -1, 1)]) 
    assert ret == [("test", 1, 200, 1), ("test", 2, 200, 1), ("test", 3, 200, 1), ("test", 4, -1, -1)] 



all_cases = (
        ("write to file", forward_file),
        ("split price range", load_price_range),
        ("load function", load_func),
        ("redis nodes",redis_nodes),
        ("forward data", forward_dst),
        ("is worker alive", is_worker_alive),
        ("format price", format_price)
        #("diff promo", diff_promo), 
        ) 
