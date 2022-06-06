import numpy as np
from copy import copy
import morphology as operations


class Image:
    def __init__(self, data: np.ndarray,
                 name: str = None,
                 origin_file_path: str = None,
                 ):
        self.name = name
        self.origin_file_path = origin_file_path
        self.__data = data
        self.__dimensions = (data.shape[0], data.shape[1])
        self.__channels_number = 1 if len(data.shape) == 2 else data.shape[2]

    @property
    def dimensions(self) -> tuple[int, int]:
        return self.__dimensions

    @property
    def data(self) -> np.ndarray:
        return self.__data

    @data.setter
    def data(self, new_data: np.ndarray):
        self.__data = new_data
        self.__dimensions = (new_data.shape[0], new_data.shape[1])

    def subtract(self, image: 'Image') -> 'Image':
        result_image = copy(self)
        result_data = np.zeros(shape=self.data.shape)
        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                result_data[i, j] = np.max(self.data[i, j] - image.data[i, j], 0)
        result_image.data = result_data
        return result_image

    def erode(self, structuring_element: np.ndarray) -> 'Image':
        result = copy(self)
        result.data = operations.erode(self.data, structuring_element)
        return result

    def dilate(self, structuring_element: np.ndarray) -> 'Image':
        result = copy(self)
        result.data = operations.dilate(self.data, structuring_element)
        return result
