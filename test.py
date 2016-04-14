Given function rand5() returns 0,1,2,3,4 eq dist, randomly


def rand7():
	v1 = rand5() # 0/1/2/3/4
	if (v1 < 2):
		v2 = v1 + rand5()%2 # adds 0 or 1 or 2 to 0 or 1 or 2
