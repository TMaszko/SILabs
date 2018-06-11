import numpy as np
import cv2


def get_perspective_transformation(pair_points):
    return cv2.getPerspectiveTransform(src=np.float32(np.array(pair_points)[:, 0]),
                                       dst=np.float32(np.array(pair_points)[:, 1]))


def get_affine_transformation(pair_points):
    # points_matrices = create_point_matrices(np.array(pair_points)[:, 0])
    # vector_of_points_on_second_images = create_vector_from_points_on_second_image(np.array(pair_points)[:, 1])
    # print(points_matrices)
    # print(vector_of_points_on_second_images)

    # inversed_matrix = np.linalg.inv(points_matrices)
    # affine_transform_vector = inversed_matrix @ vector_of_points_on_second_images
    # except np.linalg.linalg.LinAlgError:
    #     affine_transform_vector = np.zeros([6, 1])
    # for idx in range(0, len(affine_transform_vector), 2):
    #     el = affine_transform_vector[idx][0]
    #     print(affine_transform_vector[idx + 1])
    #     col = np.array([[el], affine_transform_vector[idx + 1]])
    #     result = np.concatenate((result, col), axis=1) if result is not None else col

    # print(affine_transform_vector)
    # print('resultVECTOR: ' + str(result))
    # print(np.array(pair_points)[:, 0])
    # print('----------------')
    # print(np.array(pair_points)[:, 1])
    affine_transform_matrices = cv2.getAffineTransform(src=np.float32(np.array(pair_points)[:, 0]),
                                                       dst=np.float32(np.array(pair_points)[:, 1]))

    # print('resultVector: ' + str(result))
    affine_transform_matrices = np.concatenate((affine_transform_matrices, [[0, 0, 1]]), axis=0)
    return affine_transform_matrices


def create_point_matrices(points_from_first_image):
    result = None
    for point in points_from_first_image:
        x = point[0]
        y = point[1]
        row = np.array([
            [x, y, 1, 0, 0, 0],
            [0, 0, 0, x, y, 1]
        ])
        result = np.concatenate((result, row), axis=0) if result is not None else row
        # print('result: ' + str(result))

    return result


def create_vector_from_points_on_second_image(points_from_second_image):
    result = []
    for point in points_from_second_image:
        result.append(point[0])
        result.append(point[1])

    return np.array(result).reshape([6, 1])


def calculate_model_error(model, pair_of_points):
    second_point_coords = np.array(pair_of_points[1])
    # print('second coords:', str(second_point_coords))
    first_point_coords = np.concatenate((pair_of_points[0], [1]), axis=0)
    after_transformation_point = model @ first_point_coords.reshape([3, 1])
    return np.linalg.norm(second_point_coords - after_transformation_point[:, 0][:2])


def start_ransac(pair_of_points, pair_of_points_prepared_to_get_sample, num_iterations, get_samples, get_model, n, maxerror):
    best_model = []
    best_score = 0
    best_inliners = []
    for _ in range(num_iterations):
        pair_of_points_to_compute_transformation = get_samples(pair_of_points_prepared_to_get_sample, n)
        model = get_model(pair_of_points_to_compute_transformation)
        score = 0
        inliners = []
        for pair in pair_of_points:
            error = calculate_model_error(model, pair)
            # print(error)
            if error < maxerror:
                score += 1
                inliners.append(pair)
        if score > best_score:
            best_score = score
            best_model = model
            best_inliners = inliners

    # print(best_model)
    return (best_model[:2], best_inliners)


def get_samples(pair_of_points, n):
    arr = np.arange(len(pair_of_points))
    np.random.shuffle(arr)
    # print('INDEXES')
    # print(arr[:n])
    # print('POINTS----------------')
    # print(np.array(pair_of_points)[arr[:n]])
    return np.array(pair_of_points)[arr[:n]]

