from api import PetFriends
from settings import valid_email, valid_password, unvalid_email, unvalid_password, unvalid_auth_key
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

def test_get_api_key_for_unvalid_email(email=unvalid_email, password=valid_password):
    """Получить уникальный ключ c невалидной почтой"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_unvalid_pass(email=valid_email, password=unvalid_password):
    """Получить уникальный ключ с невалидным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Почти", "кот", "4", "image/ram.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_create_pet_simple_with_valid_data(name='пес', animal_type='Соб', age='2'):
    """Проверяем, что можно добавить питомца без фото с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_set_photo_with_valid_data(pet_photo='image/ram.jpg'):
    """Проверяем что можно добавить питомцу фото"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] is not None
    else:
        raise Exception("There is no my pets")

def test_update_self_pet_info_age_symbols(name='', animal_type='', age='cTЕЪYHяёдУжЩЙжМdиЛGbГQfшIU'):
        """Поле "возраст" - ввести символы. Ожидается 400, сейчас баг - поле принимает значения."""
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 400
        else:
            raise Exception("There is no my pets")
def test_update_self_pet_long_age(name='', animal_type='', age=34534534878768572725894256985254785635673465413781675731569563476762182889213450475634781657806187346817363774675630430478813674657647568474444444444413680745613780456183746504387563874379065):
    """Добавить 256 цифр для строки возраст. Сейчас баг, количество принимается!"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
    else:
        raise Exception("There is no my pets")

def test_update_self_pet_negative_age(name='', animal_type='', age=-5):
    """Добавить отрицательное значение возраста у питомца. Сейчас баг, значение добавляется!"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
    else:
        raise Exception("There is no my pets")
