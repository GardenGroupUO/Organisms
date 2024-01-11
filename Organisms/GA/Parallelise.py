
from multiprocessing import Pool

def parallelise(method, tasks, processes=1):
	print('--------------------------------------')
	print('mp.Pool(processes=processes) statement')
	print('Running '+str(method.__name__))
	pool = Pool(processes=processes)
	print('map_async statement')
	results = pool.map_async(method, tasks)
	print('wait statement')
	results.wait()
	print('results.get() statement')
	data = results.get()
	print('pool.close() statement')
	pool.close()
	print('pool.join() statement')
	pool.join()
	print('return data statement')
	print('--------------------------------------')
	return data
