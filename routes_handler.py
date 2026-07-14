import re
import ipaddress
import logging
from pathlib import Path
from routeros_api import RouterOsApiPool

# Конфигурация логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Исключение для ошибок валидации"""
    pass


def validate_ip(ip_str: str) -> bool:
    """
    Проверка корректности IP-адреса.
    
    Args:
        ip_str: IP-адрес для проверки
        
    Returns:
        True если валидный IP адрес
        
    Raises:
        ValidationError: если IP адрес невалидный
    """
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        raise ValidationError(f"Невалидный IP адрес: {ip_str}")


def validate_cidr(cidr_str: str) -> bool:
    """
    Проверка корректности CIDR нотации (например: 192.168.1.0/24).
    
    Args:
        cidr_str: CIDR для проверки
        
    Returns:
        True если валидная CIDR нотация
        
    Raises:
        ValidationError: если CIDR невалидная
    """
    try:
        ipaddress.ip_network(cidr_str, strict=False)
        return True
    except ValueError:
        raise ValidationError(f"Невалидная CIDR нотация: {cidr_str}")


def validate_gateway(gateway_str: str) -> bool:
    """
    Проверка корректности шлюза.
    
    Args:
        gateway_str: IP-адрес шлюза
        
    Returns:
        True если валидный шлюз
        
    Raises:
        ValidationError: если шлюз невалидный
    """
    return validate_ip(gateway_str)


def load_networks_from_file(file_path: str) -> list:
    """
    Загрузка списка сетей из файла.
    
    Args:
        file_path: путь к файлу со списком сетей
        
    Returns:
        Список валидных CIDR нотаций
        
    Raises:
        FileNotFoundError: если файл не найден
        ValidationError: если есть невалидные записи в файле
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    
    networks = []
    invalid_lines = []
    
    try:
        with open(path, encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                net = line.strip()
                
                # Пропускаем пустые строки и комментарии
                if not net or net.startswith('#'):
                    continue
                
                try:
                    validate_cidr(net)
                    networks.append(net)
                except ValidationError as e:
                    invalid_lines.append(f"Строка {line_num}: {net} - {str(e)}")
    
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {str(e)}")
    
    if invalid_lines:
        error_msg = "Найдены невалидные записи:\n" + "\n".join(invalid_lines)
        raise ValidationError(error_msg)
    
    if not networks:
        raise ValidationError("Файл не содержит валидных сетей")
    
    logger.info(f"Загружено {len(networks)} сетей из файла {file_path}")
    return networks


def upload_routes_to_mikrotik(
    router_ip: str,
    username: str,
    password: str,
    gateway: str,
    networks: list,
    comment: str = ""
) -> dict:
    """
    Загрузка маршрутов в MikroTik.
    
    Args:
        router_ip: IP адрес MikroTik
        username: имя пользователя
        password: пароль
        gateway: IP адрес шлюза
        networks: список сетей (CIDR)
        comment: комментарий к маршрутам
        
    Returns:
        Словарь с результатами:
        {
            'success': int - количество добавленных маршрутов,
            'failed': int - количество ошибок,
            'errors': list - список ошибок
        }
    """
    # Валидация входных данных
    validate_ip(router_ip)
    validate_ip(username) if re.match(r'^\d+\.\d+\.\d+\.\d+$', username) else None
    validate_gateway(gateway)
    
    result = {
        'success': 0,
        'failed': 0,
        'errors': []
    }
    
    api_pool = None
    try:
        logger.info(f"Подключение к MikroTik {router_ip}...")
        api_pool = RouterOsApiPool(
            router_ip,
            username=username,
            password=password,
            plaintext_login=True
        )
        api = api_pool.get_api()
        logger.info("Подключение успешно")
        
        route_resource = api.get_resource('/ip/route')
        
        for network in networks:
            try:
                logger.info(f"Добавляю маршрут: {network} через {gateway}")
                route_resource.add(
                    dst_address=network,
                    gateway=gateway,
                    comment=comment or None
                )
                result['success'] += 1
            except Exception as e:
                error_msg = f"Ошибка при добавлении маршрута {network}: {str(e)}"
                logger.error(error_msg)
                result['errors'].append(error_msg)
                result['failed'] += 1
        
        logger.info(f"Загрузка завершена. Успешно: {result['success']}, Ошибок: {result['failed']}")
        
    except Exception as e:
        error_msg = f"Ошибка подключения к MikroTik: {str(e)}"
        logger.error(error_msg)
        result['errors'].append(error_msg)
        result['failed'] = len(networks)
    
    finally:
        if api_pool:
            try:
                api_pool.disconnect()
                logger.info("Отключено от MikroTik")
            except Exception as e:
                logger.error(f"Ошибка при отключении: {str(e)}")
    
    return result
