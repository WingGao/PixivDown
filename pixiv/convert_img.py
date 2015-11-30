__author__ = 'Wing'
import base64

jpgtxt = base64.encodestring(open("test.png", "rb").read())

f = open("jpg1_b64.txt", "w")
f.write(jpgtxt)
f.close()

# ----
newjpgtxt = open("jpg1_b64.txt", "rb").read()

g = open("out.png", "w")
g.write(base64.decodestring(newjpgtxt))
g.close()