import random
"""
Код представляет собой консольную мини-игру на языке Python, 
в которой игрок сражается с противниками с помощью оружия.
"""


class Character:
    """
    Базовый класс для персонажа в игре.
    """

    def __init__(self, name, health, mana):
        """
        Инициализация персонажа.

        name: Имя персонажа.
        health: Количество здоровья персонажа.
        mana: Количество маны персонажа.
        """
        self.name = name
        self.health = health
        self.mana = mana

    def take_damage(self, damage):
        """
        Нанесение урона персонажу.

        damage: Количество урона.
        """
        self.health -= damage
        print(f"{self.name} получил {damage} урона. "
              f"Осталось здоровья: {self.health}")

    def gain_health(self, health):
        """
        Восстановление здоровья персонажа.

        health: Количество восстанавливаемого здоровья.
        """
        self.health += health
        print(f"{self.name} восстановил {health} здоровья. "
              f"Осталось здоровья: {self.health}")

    def gain_mana(self, mana):
        """
        Восстановление маны персонажа.

        mana: Количество восстанавливаемой маны.
        """
        self.mana += mana
        print(f"{self.name} восстановил {mana} маны. "
              f"Осталось маны: {self.mana}")

    def is_alive(self):
        """
        Проверка, жив ли персонаж.

        return True, если персонаж жив, иначе False.
        """
        return self.health > 0


class Player(Character):
    """
    Класс для управления игроком.
    """

    def __init__(self, name, health, mana, weapon):
        """
        Инициализация игрока.

        name: Имя игрока.
        health: Количество здоровья игрока.
        mana: Количество маны игрока.
        weapon: Оружие игрока.
        """
        super().__init__(name, health, mana)
        self.weapon = weapon

    def attack(self, enemy):
        """
        Атака противника обычным оружием.

        enemy: Противник, которого атакует игрок.
        """
        damage = self.weapon.damage
        enemy.take_damage(damage)
        mana_gain = random.randint(5, 10)
        self.gain_mana(mana_gain)


    def special_attack(self, enemy):
        """
        Специальная атака противника, требующая маны.

        enemy: Противник, которого атакует игрок.
        """
        if self.mana >= self.weapon.special_mana_cost:
            self.mana -= self.weapon.special_mana_cost
            special_damage = self.weapon.special_damage
            enemy.take_damage(special_damage)
            print(f"{self.name} использовал специальную атаку "
                  f"{self.weapon.special_name} на {enemy.name}, "
                  f"нанеся {special_damage} урона.")
        else:
            print(f"У {self.name} недостаточно маны для специальной атаки.")

    def retreat(self, enemy):
        """
        Отступление игрока, которое наносит урон, но восстанавливает ману.

        enemy: Противник, атакующий игрока.
        """
        retreat_damage = random.randint(5, 10)
        # Полученный урон при отступлении
        mana_gain = random.randint(15, 20)
        # Восстановленная мана при отступлении
        self.take_damage(retreat_damage)
        self.gain_mana(mana_gain)
        print(f"{self.name} отступил, получив {retreat_damage} "
              f"урона, но восстановив {mana_gain} маны.")


class Enemy(Character):
    """
    Класс для создания врагов.
    """

    def __init__(self, name, health, mana):
        """
        Инициализация врага.

        name: Имя врага.
        health: Количество здоровья врага.
        mana: Количество маны врага.
        """
        super().__init__(name, health, mana)

    def attack(self, player):
        """
        Атака игрока.

        player: Игрок, которого атакует враг.
        """
        damage = random.randint(15, 20)
        player.take_damage(damage)


class Weapon:
    """
    Класс для описания оружия.
    """

    def __init__(self, name, damage, special_name, special_damage,
                 special_mana_cost):
        """
        Инициализация оружия.

        name: Название оружия.
        damage: Урон, наносимый обычной атакой.
        special_name: Название специальной атаки.
        special_damage: Урон, наносимый специальной атакой.
        special_mana_cost: Стоимость специальной атаки в мане.
        """
        self.name = name
        self.damage = damage
        self.special_name = special_name
        self.special_damage = special_damage
        self.special_mana_cost = special_mana_cost


class Battle:
    """
    Класс для управления сражениями.
    """

    def __init__(self, player, enemy):
        """
        Инициализация боя.

        player: Игрок.
        enemy: Враг.
        """
        self.player = player
        self.enemy = enemy

    def start(self):
        """
        Начало боя.
        """
        print(f"\nБой между {self.player.name} и {self.enemy.name} начался!")
        while self.player.is_alive() and self.enemy.is_alive():
            self.player_turn()
            if not self.enemy.is_alive():
                break
            self.enemy_turn()

        if self.player.is_alive():
            print(f"{self.player.name} победил!")
        else:
            print(f"{self.player.name} потерпел поражение.")

    def player_turn(self):
        """
        Ход игрока.
        """
        action = input("Выберите действие "
                       "(атака/способность/отступ): ").strip().lower()
        if action == "атака":
            self.player.attack(self.enemy)
        elif action == "способность":
            self.player.special_attack(self.enemy)
        elif action == "отступ":
            self.player.retreat(self.enemy)
        else:
            print("Неверное действие. Попробуйте снова.")

    def enemy_turn(self):
        """
        Ход врага.
        """
        self.enemy.attack(self.player)


class Game:
    """
    Класс для общей логики игры.
    """

    def __init__(self):
        """
        Инициализация игры.
        """
        self.player = None
        self.enemies = []

    def create_player(self):
        """
        Создание игрока.
        """
        name = input("Введите имя игрока: ").strip()
        weapon_choice = input("Выберите оружие "
                              "(меч/магический посох/лук): ").strip().lower()
        if weapon_choice == "меч":
            weapon = Weapon("Меч", 15, "Разруб", 30, 20)
        elif weapon_choice == "магический посох":
            weapon = Weapon("Магический посох", 10, "Гром", 40, 30)
        elif weapon_choice == "лук":
            weapon = Weapon("Лук", 12, "Огненная стрела", 25, 15)
        else:
            print("Неверный выбор оружия. Выбрано оружие по умолчанию - Меч.")
            weapon = Weapon("Меч", 15, "Разруб", 30, 20)
        self.player = Player(name, 100, 50, weapon)

    def create_enemies(self):
        """
        Создание списка врагов.
        """
        self.enemies.append(Enemy("Орк", 50, 20))
        self.enemies.append(Enemy("Дракон", 70, 30))
        self.enemies.append(Enemy("Гоблин", 40, 15))
        self.enemies.append(Enemy("Кентавр", 60, 25))
        self.enemies.append(Enemy("Черная эльфа", 55, 20))

    def start_battles(self):
        """
        Начало всех сражений.
        """
        for i, enemy in enumerate(self.enemies, start=1):
            print(f"\nСражение {i}:")
            battle = Battle(self.player, enemy)
            battle.start()
            if not self.player.is_alive():
                break
            if self.player.is_alive():
                self.player.gain_health(20)
                print(f"{self.player.name} восстановил 20 "
                      f"здоровья после сражения.")

    def run(self):
        """
        Запуск игры.
        """
        self.create_player()
        self.create_enemies()
        self.start_battles()


if __name__ == "__main__":
    game = Game()
    game.run()