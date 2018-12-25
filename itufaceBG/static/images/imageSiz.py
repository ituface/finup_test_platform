from PIL import Image
import numpy as np
img=Image.open('./support.png')

out=img.resize((300,300))
out.show()
out.save('../supports.png')
