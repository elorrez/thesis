import wget
import numpy as np

#Download the txt file

url = "https://modis-land.gsfc.nasa.gov/pdf/sn_bound_10deg.txt"
wget.download(url)

data = np.genfromtxt('sn_bound_10deg.txt',
                     skip_header = 7,
                     skip_footer = 3)



