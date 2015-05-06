def module_test(res):
	assert(res)

def module_test_not(res):
	assert(not res)

def module_test_stock(res):
	assert(res[0][3])

def module_test_stock_not(res):
	assert(not res[0][3])
