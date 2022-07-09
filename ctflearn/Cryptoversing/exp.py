from operator import xor

for c in "h_b0}EcDOR":
	print chr(xor(ord(c), 0x10))
for c in "+G)uh(jl,vL":
	print chr(xor(ord(c), 0x18))
# CTFlearn{xOr_mUsT_B3_1mp0rt4nT}
