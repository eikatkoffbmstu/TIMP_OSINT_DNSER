import dns.resolver
import sys
import time
from tqdm import tqdm
import json

def get_dns_info(domain, record_types=None):
    if record_types is None:
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    results = {}
    
    for record in tqdm(record_types, desc="Запрос DNS записей"):
        try:
            answers = dns.resolver.resolve(domain, record)
            results[record] = [str(answer) for answer in answers]
        except dns.resolver.NoAnswer:
            results[record] = ['Записей не найдено']
        except dns.resolver.NXDOMAIN:
            print(f'Домен {domain} не существует')
            sys.exit(1)
        except Exception as e:
            results[record] = [f'Ошибка: {str(e)}']
        time.sleep(0.5)  
    
    return results
def display_dns_info(dns_info):
    for record_type, records in dns_info.items():
        print(f'{record_type} записи:')
        for record in records:
            print(f'  {record}')
        print()

def display_record_info():
    print("Типы записей ресурсов:")
    print("A-запись (Address record). Связывает доменное имя с IPv4-адресом.")
    print("AAAA-запись (IPv6 Address record). Связывает доменное имя с IPv6-адресом.")
    print("CNAME-запись (Canonical Name record). Устанавливает соответствие между альтернативным и каноническим доменными именами.")
    print("MX-запись (Mail exchange record). Указывает на почтовый сервер для домена.")
    print("NS-запись (Name server record). Указывает на DNS-сервер, авторитетный для домена.")
    print("PTR-запись (Pointer record). Используется для обратного DNS-поиска.")
    print("SRV-запись (Service locator record). Указывает местоположение сервера для службы.")
    print("TXT-запись (Text record). Предоставляет информацию о домене в текстовом формате.")
    print("SOA-запись (Start of authority record). Указывает на DNS-сервер, источник авторитетной информации для домена.")
    print()

def display_welcome_screen():
    print(r"""
        ######  #     #  #####         ######  #######  #####  ####### #       #     # ####### ######  
        #     # ##    # #     #        #     # #       #     # #     # #       #     # #       #     # 
        #     # # #   # #              #     # #       #       #     # #       #     # #       #     # 
        #     # #  #  #  #####         ######  #####    #####  #     # #       #     # #####   ######  
        #     # #   # #       #        #   #   #             # #     # #        #   #  #       #   #   
        #     # #    ## #     #        #    #  #       #     # #     # #         # #   #       #    #  
        ######  #     #  #####         #     # #######  #####  ####### #######    #    ####### #     #
                    
                                   Добро пожаловать в DNS Инструмент!
    """)

def save_to_json(data, filename='dns_info.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Информация сохранена в файл {filename}")
def main():
    display_welcome_screen()
    input("Нажмите любую кнопку для продолжения...")
    
    while True:
        print("\nМеню:")
        print("1. Получить информацию о всех DNS записях")
        print("2. Получить информацию о конкретной DNS записи")
        print("H. Получить основную информацию по всем DNS записям")
        print("Q. Выйти")
        
        choice = input("Выберите опцию: ").strip().upper()
        
        if choice == '1':
            domain = input("Введите домен: ").strip()
            dns_info = get_dns_info(domain)
            display_dns_info(dns_info)
            
            save_choice = input("Сохранить информацию в JSON? (Y/n): ").strip().lower()
            if save_choice == 'y' or save_choice == '':
                save_to_json(dns_info)
        
        elif choice == '2':
            user_input = input("Введите домен и тип записи (например, 'example.com A'): ").strip()
            try:
                domain, record_type = user_input.split()
                dns_info = get_dns_info(domain, [record_type])
                display_dns_info(dns_info)
                
                save_choice = input("Сохранить информацию в JSON? (Y/n): ").strip().lower()
                if save_choice == 'y' or save_choice == '':
                    save_to_json(dns_info)
            except ValueError:
                print("Ошибка: введите домен и тип записи через пробел.")
        
        elif choice == 'H':
            display_record_info()

            return_choice = input("Нажмите R для возврата в основное меню: ").strip().upper()
            if return_choice == 'R':
                continue
        
        elif choice == 'Q':
            print("Выход из программы.")
            break
        
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
if __name__ == '__main__':
    main()