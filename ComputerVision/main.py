import datetime

import cv2
import numpy as np
from matplotlib import pyplot as plt
from ransac import *

IMAGES_DIR = "images"


def get_key_points_from_image(image):
    img = cv2.imread(IMAGES_DIR + '/' + image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    sift = cv2.xfeatures2d.SIFT_create()
    kp, desc = sift.detectAndCompute(img, None)
    print(desc.shape)
    return {
        'kp': kp,
        'desc': desc,
        'img': img
    }


def get_num_of_neighbours_of_pairs_of_key_points(pair_with_neighbours, all_pairs_with_neighbours):
    return len([(_pair[0][0], _pair[1][0]) for _pair in all_pairs_with_neighbours if
                _pair[0][0] in pair_with_neighbours[0][1] and _pair[1][0] in pair_with_neighbours[1][1]])


def get_neighbours_of_key_point(point_descriptor, points_descriptors, criterium):
    result = [np.sum(np.abs(desc - point_descriptor)) for index, desc in enumerate(points_descriptors)]
    result = np.array(result)
    # for index, desc in enumerate(points_descriptors):
    #     print(np.sum(np.abs(desc - point_descriptor)))
    return np.argsort(result)[: criterium]


def get_distances_from_one_point_to_all_points_in_other_images(desc, key_points_from_second_image):
    return np.sum(np.abs(np.subtract(desc.reshape(1, 128), key_points_from_second_image)), axis=1)


def find_mutual_neighbour(index1, index2, nearest_neighbours):
    # print(index1)
    # print(index2)
    # print(nearest_neighbours)
    result = [(_index1, _index2) for _index1, _index2 in nearest_neighbours if index1 == _index1 and index2 == _index2]
    return result[0] if len(result) > 0 else None


0


def get_pairs_of_key_points_nearest_mutual_neighbour(key_points_from_first_image, key_points_from_second_image):
    first_list = [(index, int(np.argmin(
        get_distances_from_one_point_to_all_points_in_other_images(desc, key_points_from_second_image))))
                  for index, desc in enumerate(key_points_from_first_image)]
    print(first_list)
    dtype = [('index1', int), ('index2', int)]
    print(np.sort(np.array(first_list, dtype=dtype), order=['index1']).tolist())
    print('lenfirst:' + str(len(first_list)))
    second_list = [(int(np.argmin(
        get_distances_from_one_point_to_all_points_in_other_images(
            desc,
            key_points_from_first_image))), index)
        for index, desc in enumerate(key_points_from_second_image)]

    print('second list' + str(second_list))
    print(np.sort(np.array(second_list, dtype=dtype), order=['index1']).tolist())
    nearest_neighbours = np.array(first_list + second_list)
    print(nearest_neighbours.shape)
    print(np.sort(np.array(nearest_neighbours, dtype=dtype), order=['index1']).tolist())
    result = np.array([find_mutual_neighbour(index1, index2, nearest_neighbours[(index + 1):])
                       for index, (index1, index2) in enumerate(nearest_neighbours)])
    print(result.shape)
    arr = []
    for el in result:
        if el is not None:
            arr.append(el)

    print(arr[48])
    print(arr[49])
    return arr


def remove_duplicates(pairs):
    result = []
    for (el, el2) in pairs:
        if (el, el2) not in result:
            result.append((el, el2))
    return result


first_image_data = get_key_points_from_image('xd1.jpg')
second_image_data = get_key_points_from_image('xd.jpg')
pairs_of_mutual_neighbours = get_pairs_of_key_points_nearest_mutual_neighbour(first_image_data['desc'],
                                                                              second_image_data['desc'])

print(pairs_of_mutual_neighbours)

# pairs_of_mutual_neighbours = remove_duplicates(pairs_of_mutual_neighbours)
print('num of pairs')
print(len(pairs_of_mutual_neighbours))
# print(pairs_of_mutual_neighbours)

neighbours = [((index1, get_neighbours_of_key_point(first_image_data['desc'][index1], np.concatenate(
    (first_image_data['desc'][0:index1], first_image_data['desc'][(index1 + 1):])), 100)),
               (index2, get_neighbours_of_key_point(second_image_data['desc'][index2], np.concatenate(
                   (second_image_data['desc'][0:index2], second_image_data['desc'][(index2 + 1):])), 100)))
              for (index1, index2) in
              pairs_of_mutual_neighbours]

after_processing_key_points = [(pair_with_neighbours[0][0], pair_with_neighbours[1][0],
                                get_num_of_neighbours_of_pairs_of_key_points(pair_with_neighbours, neighbours)) for
                               pair_with_neighbours in neighbours]

print(after_processing_key_points)
pairs_to_process = [(pair_with_num_of_neigh[0], pair_with_num_of_neigh[1]) for pair_with_num_of_neigh in
                    after_processing_key_points if pair_with_num_of_neigh[2] >= 10]

# pairs_to_process = pairs_of_mutual_neighbours
pairs_of_key_points = [(first_image_data['kp'][index1].pt, second_image_data['kp'][index2].pt) for
                       (index1, index2) in pairs_to_process]

# num_of_pairs = len(pairs_of_key_points)


start_time = datetime.datetime.now()
# best_model, inliners = start_ransac(pairs_of_key_points, pairs_of_key_points, 100, get_samples,
#                                     get_affine_transformation, 3, 50)
# best_model, inliners = start_ransac(pairs_of_key_points, pairs_of_key_points , 100, get_samples, get_perspective_transformation, 4, 50)
print((datetime.datetime.now() - start_time).seconds)
# cv2.warpAffine(first_image_data, best_model, second_image_data['img'])

# print(after_processing_key_points)
# print(len(after_processing_key_points))
print(first_image_data['img'].shape[:2][0])
# after_processing_key_points = inliners
after_processing_key_points = pairs_of_key_points
concatenate_images = np.concatenate((first_image_data['img'], second_image_data['img']), axis=0)
plt.imshow(concatenate_images)
plt.plot(([point[0][0] for point in after_processing_key_points],
          [point[1][0] for point in after_processing_key_points]),
         ([point[0][1] for point in after_processing_key_points],
          [point[1][1] + first_image_data['img'].shape[:2][0] for point in after_processing_key_points]))
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
