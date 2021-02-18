import georasters as gr

path = "C:/EVA/THESIS/code/testdata/tiff/2000032.tiff"

data =gr.from_file(path)
data.plot()