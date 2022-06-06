import numpy as np

from image import Image


def load_as_ppm(file_path: str) -> Image:
    with open(file_path, 'r') as file:
        lines = list(map(lambda x: x.rstrip(), file.readlines()))
        img_comments: list[str] = []
        comment: str = lines[1]
        index = 1
        while comment.startswith('#'):
            img_comments.append(comment[1:])
            index += 1
            comment = lines[index]
        dimensions = [int(i) for i in lines[index].split(' ')]
        dimensions[0], dimensions[1] = dimensions[1], dimensions[0]
        index += 1
        data = list(map(lambda x: str(x).split(' ')
                        if False
                        else list(filter(lambda c: c in ['1', '0'], list(x))),
                    lines[index:]))
        payload = np.array([int(color) for colors in data for color in colors if len(color) > 0])
        result_payload = payload.reshape((dimensions[0], dimensions[1])) 
        name_index = file_path.split('/')
        name = file_path if len(name_index) == 0 else name_index[-1]
        result_img = Image(data=result_payload,
                           name=name,
                           origin_file_path=file_path,
                           )
        return result_img


    
