import csv
# We compare the lists of coordinates with only NA values of the different variables:
# We look for the intersection between evi and each climate variable. These pixels will be left out of the analysis since these are the pixels that don't have EVI value
# the pixels that have all NA vlues in the climate vairables will need to be spatial interpolated.
# CRU: 39 pixels intersection between evi NA pixels and CRUtmp/pre NA pixles
# GPCC: 142 pixels intersection between EVI NA pixels and GPCC pixels

# save csv file with the coordinates of the pixels that are not in the intersection with evi --> these are the pixels
# that have to be interpolated

in_evi = "C:/EVA/THESIS/code/files/evi_na_values_pixels_list.csv"
in_CRU_HR_tmp = "C:/EVA/THESIS/code/files/CRU_HR_tmp_na_values_pixels_list.csv"
in_CRU_HR_pre = "C:/EVA/THESIS/code/files/CRU_HR_pre_na_values_pixels_list.csv"
#in_ERA_rad = "C:/EVA/THESIS/code/files/ERA_rad_na_values_pixels_list.csv"
in_GPCC_pre = "C:/EVA/THESIS/code/files/GPCC_pre_na_values_pixels_list.csv"
in_paths = [in_evi, in_CRU_HR_tmp, in_CRU_HR_pre, in_GPCC_pre]

na_lists = []
for path in in_paths:
    with open(path) as r:
        na_lists.append(list(csv.reader(r, delimiter=';')))

print(len(na_lists))
print(len(na_lists[0][0]))
print(len(na_lists[1][0]))
print(len(na_lists[2][0]))
print(len(na_lists[3][0]))


intersection_evi_crutmp = list(set(na_lists[0][0]) & set(na_lists[1][0]))
print(intersection_evi_crutmp)

intersection_evi_crupre = list(set(na_lists[0][0]) & set(na_lists[2][0]))
print(len(intersection_evi_crupre))

not_intersection_evi_cru = set(na_lists[1][0]) - set(na_lists[0][0])
print(not_intersection_evi_cru)
print(len(not_intersection_evi_cru))

with open(f"C:/EVA/THESIS/code/files/CRU_not_evi_na_values_pixels_list.csv", 'w+') as na_values_pixels_list:
   writer = csv.writer(na_values_pixels_list, delimiter=';')
   writer.writerow(not_intersection_evi_cru)

intersection_evi_gpcc = list(set(na_lists[0][0]) & set(na_lists[3][0]))
print(len(intersection_evi_gpcc))

not_intersection_evi_gpcc = set(na_lists[3][0]) - set(na_lists[0][0])

with open(f"C:/EVA/THESIS/code/files/GPCC_not_evi_na_values_pixels_list.csv", 'w+') as na_values_pixels_list:
   writer = csv.writer(na_values_pixels_list, delimiter=';')
   writer.writerow(not_intersection_evi_gpcc)
