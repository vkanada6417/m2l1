from random import randint
import requests

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = self.random_pokemon_number()
        self.level = 1
        self.experience = 0
        self.hunger = 50
        self.is_rare = False
        self.hp = 100
        self.power = 10
        
        
        data = self.fetch_data()
        if data:
            self.name = data.get('name', 'Unknown')
            self.img = data.get('sprites', {}).get('front_default', 'No Image')
            self.height = data.get('height', 0)
            self.weight = data.get('weight', 0)
            self.types = [t['type']['name'] for t in data.get('types', [])]
            self.abilities = [a['ability']['name'] for a in data.get('abilities', [])]
        else:
            self.name = "Pikachu"
            self.img = "No Image"
            self.height = 0
            self.weight = 0
            self.types = []
            self.abilities = []
        
        Pokemon.pokemons[pokemon_trainer] = self

    def random_pokemon_number(self):
        self.is_rare = randint(1, 100) <= 5
        return randint(1, 1000)

    def fetch_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def info(self):
        rarity = "Редкий" if self.is_rare else "Обычный"
        types = ", ".join(self.types) if self.types else "Unknown"
        abilities = ", ".join(self.abilities) if self.abilities else "None"
        return (f"Имя: {self.name}\n"
                f"Редкость: {rarity}\n"
                f"Уровень: {self.level}\n"
                f"Опыт: {self.experience}\n"
                f"Сытость: {self.hunger}\n"
                f"Рост: {self.height / 10} м\n"
                f"Вес: {self.weight / 10} кг\n"
                f"Типы: {types}\n"
                f"Способности: {abilities}")

    def show_img(self):
        return self.img

    # Методы для взаимодействия
    def feed(self):
        if self.hunger < 100:
            self.hunger = min(self.hunger + 20, 100)
            return "Покемон накормлен! Сытость увеличилась."
        return "Покемон уже сыт!"

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        return f"Поздравляем! {self.name} достиг уровня {self.level}!"

    def check_hunger(self):
        if self.hunger > 0:
            self.hunger -= 5
        else:
            return f"{self.name} голоден! Скоро он перестанет расти."

    def add_achievement(self):
        return f"Поздравляем! Вы получили достижение за владение редким покемоном: {self.name}!"
    
    def heal(self, amount):
        self.hp += amount
        if self.hp > 100:
            self.hp = 100
        return f"Здоровье покемона восстановлено на {amount} единиц."

class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = 120  
        self.power = 15 

    def info(self):
        return "У тебя покемон-волшебник\n" + super().info()

    def attack(self, enemy):
        return super().attack(enemy)

class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = 90  
        self.power = 20  

    def info(self):
        return "У тебя покемон-боец\n" + super().info()

    def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой: {super_power} "
