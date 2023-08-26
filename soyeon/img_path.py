import os

class_names = []
char_path = r'../img/face'

def list_directories(path):
    """
    지정된 경로의 폴더를 출력합니다.
    """
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isdir(full_path):
            class_names.append(name)


list_directories(char_path)
print(class_names)