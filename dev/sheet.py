import sys
from PIL import Image
out=sys.argv[1]; files=sys.argv[2:]
ims=[Image.open(f).convert('RGBA') for f in files]
h=500
ims=[i.resize((int(i.width*h/i.height),h)) for i in ims]
c=Image.new('RGB',(sum(i.width for i in ims),h),(190,200,190)); x=0
for i in ims: c.paste(i,(x,0),i); x+=i.width
c.save(out)
