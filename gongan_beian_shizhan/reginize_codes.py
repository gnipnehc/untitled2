from gongan_beian_shizhan.save_img import save_screen
import requests
image_path = 'code.jpg'


def soc_code():
    files = {'image': open(image_path, 'rb')}

    responce = requests.post('http://127.0.0.1:8081/predict', files=files)

    if responce.status_code != 200:
        raise Exception
    return responce.json()['prediction']


print(soc_code())
