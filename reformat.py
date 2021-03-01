import numpy as np
from io import StringIO

data = np.loadtxt("./data/fruit_data.csv", dtype=np.int16,delimiter=',')

new_data = data[::2]

print(new_data)

# s = StringIO()
s = open("new_data", 'w')
np.savetxt(s, new_data, delimiter=',', fmt='%1.0f')
s.getvalue()
s.close()
