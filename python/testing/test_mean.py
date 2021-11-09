import os

filepath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\Data_week5\Dark_Test2(f1000)_data.raw"

dirpath, filename = os.path.split(filepath)
print("filepath:{}\ndirpath: {}\nfilename: {}".format(filepath, dirpath, filename))

new_filename = "some_new_filename.txt"

new_filepath = os.path.join(dirpath, new_filename)

print("new_filepath: {}\ndirpath: {}\nnew_filename: {}".format(new_filepath, dirpath, new_filename))

print("old file {}".format(os.path.isfile(filepath)))
print("new file {}".format(os.path.isfile(new_filepath)))
