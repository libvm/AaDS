import pandas as pd
import subprocess
import hashlib

dataset = pd.read_excel("scoring_data_v.1.2.xlsx")
hashes_md5 = dataset['Номер телефона']
numbers = open('word_list.txt', 'r').read().splitlines()
hashes_md5.to_csv('hashes_md5.txt', sep='\n', index=False, header=False)

def unsalt_set(salted_set, salt):
    unsalted_set = list()
    for i in range (len(salted_set)):
        unsalted_set.append(str(int(salted_set[i]) + salt))
    return unsalted_set

def calculate_salt(salted_numbers):
    for salted_number in salted_numbers:
        salt = int(salted_number) - int(numbers[0])
        if salt < 0:
            continue
        i = 1
        while (str(int(numbers[i]) + salt)) in salted_numbers:
            i += 1
            if i == 5:
                print(f'Соль найдена: {salt}')
                return salt
    return None

class Set():
    def __init__(self,input_name, output_name, method, number_of_method):
        self.input_name = input_name
        self.output_name = output_name
        self.method = method
        self.number_of_method = number_of_method
        
    method: str
    number_of_method: int
    input_name: str
    output_name: str
    hashes: list
    unhashed: list
        
    def hash(self, decrypted_set):
        hash_list = []
        for num in decrypted_set:
            num_in_bytes = num.encode('utf-8')
            hash_obj = hashlib.new(self.method)
            hash_obj.update(num_in_bytes)
            
            hashed_result = hash_obj.hexdigest()
            hash_list.append(hashed_result)
        self.hashes = hash_list
    
    def unhash_set(self):
        command = [
            'hashcat',
            '--potfile-disable',
            '-m', f'{self.number_of_method}',
            '-a', '3',
            self.input_name,
            '-1 89', '?1?d?d?d?d?d?d?d?d?d?d',
            'word_list.txt',
            '--hook-threads=4',
            '--optimized-kernel-enable',
            '-w', '4',
            '--outfile', self.output_name,
            '--outfile-format=2',
            '--remove',
        ]
        subprocess.run(command)

def main():
    md5 = Set('hashes_md5.txt', 'unhashed_md5_with_salt.txt', 'md5', 0)
    
    md5.unhash_set() # расхеширование данных, захешированных md5
    unhashed_salted_md5 = open(md5.output_name, 'r').read().splitlines()
    
    salt = calculate_salt(unhashed_salted_md5) # высчитывание соли
    
    unhashed_md5 = unsalt_set(unhashed_salted_md5, salt) # вычитание высчитанной соли из номеров
    open('unhashed_md5.txt', 'w').write('\n'.join(unhashed_md5))
    
    sets = list() # инициализация списка объектов для разных хеш-функций
    sets.append(Set('hashes_sha1.txt', 'unhashed_sha1.txt', 'sha1', 100))
    sets.append(Set('hashes_sha224.txt', 'unhashed_sha224.txt', 'sha224', 1300))
    sets.append(Set('hashes_sha256.txt', 'unhashed_sha256.txt', 'sha256', 1400))
        
    for i in range(len(sets)):
        sets[i].hash(unhashed_md5) # хеширование номеров выбранной хеш-функцией
        open(sets[i].input_name, 'w').write('\n'.join(sets[i].hashes))
        
        sets[i].unhash_set() # расхеширование номеров, захешированной определенной хеш-функцией
        sets[i].unhashed = open(sets[i].output_name, 'r').read().splitlines()
        
        if set(unhashed_md5) == set(sets[i].unhashed):
            print(f'Расхешированные данные по md5 и {sets[i].method} эквивалентны')
    
if __name__ == "__main__":
    main()