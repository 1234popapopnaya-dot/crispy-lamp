import pygame
import random
import sys
import math
import os
import json

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Рыбалка Трофеев")
clock = pygame.time.Clock()

TEXTURE_PATH = "/storage/emulated/0/FishingGame/"
SOUND_PATH = "/storage/emulated/0/FishingGame/sounds/"
SAVE_PATH = "/storage/emulated/0/FishingGame/save.json"

os.makedirs(TEXTURE_PATH, exist_ok=True)
os.makedirs(SOUND_PATH, exist_ok=True)

# Цвета
DARK_BLUE = (15, 70, 160)
BLUE = (50, 160, 255)
SAND = (220, 190, 130)
WHITE = (255, 255, 255)
RED = (230, 40, 40)
BROWN = (100, 60, 25)
GOLD = (255, 200, 0)
BLACK = (0, 0, 0)
WOOD_DARK = (70, 40, 15)
GRAY = (120, 120, 120)
GREEN = (34, 139, 34)
ORANGE = (255, 165, 0)

WATER_H = SCREEN_HEIGHT - 100
BEACH_H = 100

# Вес рыбы
FISH_WEIGHT = {
    "Карась": {"min": 0.3, "max": 1.2, "strength": 1.0, "price_per_kg": 80},
    "Окунь": {"min": 0.5, "max": 1.8, "strength": 1.2, "price_per_kg": 70},
    "Карп": {"min": 1.0, "max": 3.5, "strength": 1.8, "price_per_kg": 60},
    "Щука": {"min": 1.5, "max": 5.0, "strength": 2.2, "price_per_kg": 80},
    "Сом": {"min": 3.0, "max": 15.0, "strength": 3.5, "price_per_kg": 50},
    "Дракон": {"min": 20.0, "max": 100.0, "strength": 10.0, "price_per_kg": 200},
}

# 8 классов рыбаков
CLASSES = {
    1: {"name": "Новичок", "price": 0, "luck": 1.0, "fight": 1.0, "sell": 1.0, "level": 1, "emoji": "🪤", "color": BROWN},
    2: {"name": "Опытный", "price": 500, "luck": 1.3, "fight": 1.2, "sell": 1.0, "level": 3, "emoji": "🎣", "color": (0, 100, 200)},
    3: {"name": "Мастер", "price": 1500, "luck": 1.6, "fight": 1.5, "sell": 1.0, "level": 5, "emoji": "🏆", "color": GREEN},
    4: {"name": "Пират", "price": 2000, "luck": 1.5, "fight": 1.3, "sell": 1.5, "level": 4, "emoji": "🏴‍☠️", "color": (139, 0, 0)},
    5: {"name": "Киберрыбак", "price": 3000, "luck": 1.2, "fight": 2.0, "sell": 1.0, "level": 6, "emoji": "🤖", "color": (0, 255, 255)},
    6: {"name": "Маг воды", "price": 4000, "luck": 2.0, "fight": 1.2, "sell": 1.3, "level": 7, "emoji": "🔮", "color": (128, 0, 128)},
    7: {"name": "Легенда", "price": 5000, "luck": 2.0, "fight": 2.0, "sell": 1.5, "level": 8, "emoji": "👑", "color": GOLD},
    8: {"name": "Драконий страж", "price": 10000, "luck": 3.0, "fight": 3.0, "sell": 2.0, "level": 10, "emoji": "🐉", "color": (139, 0, 0)},
}

# Рыбы
FISH_DATA = {
    "Карась": {"chance": 0.6, "price": 50, "color": (192, 192, 192), "file": "crucian.png"},
    "Окунь": {"chance": 0.4, "price": 80, "color": (46, 139, 87), "file": "perch.png"},
    "Карп": {"chance": 0.2, "price": 150, "color": (184, 134, 11), "file": "carp.png"},
    "Щука": {"chance": 0.1, "price": 250, "color": (85, 107, 47), "file": "pike.png"},
    "Сом": {"chance": 0.05, "price": 500, "color": (40, 40, 50), "file": "catfish.png"},
    "Дракон": {"chance": 0.005, "price": 5000, "color": (139, 0, 0), "file": "dragon.png"},
}

# Удочки
RODS = {
    1: {"name": "Бамбуковая", "price": 0, "luck": 1.0, "fight": 1.0, "level": 1},
    2: {"name": "Спиннинг", "price": 100, "luck": 1.5, "fight": 1.3, "level": 2},
    3: {"name": "Шторм", "price": 300, "luck": 2.2, "fight": 1.6, "level": 3},
    4: {"name": "Алмазная", "price": 1000, "luck": 3.5, "fight": 2.0, "level": 5},
}

# 5 прикормок
BAITS = {
    2: {"name": "Жмых", "price": 15, "target": "Карп", "bonus": 3.0, "level": 1},
    3: {"name": "Червь", "price": 20, "target": "Окунь", "bonus": 3.0, "level": 1},
    4: {"name": "Малёк", "price": 30, "target": None, "bonus": 2.0, "level": 2},
    5: {"name": "Жемчуг", "price": 100, "target": None, "bonus": 2.5, "level": 4},
    6: {"name": "Кровь дракона", "price": 500, "target": None, "bonus": 4.0, "level": 6},
}

# 4 лодки
BOATS = {
    1: {"name": "Нет лодки", "price": 0, "bonus": 1.0, "level": 1, "sound": None},
    2: {"name": "Резиновая", "price": 1000, "bonus": 1.3, "level": 4, "sound": "rubber_boat.wav"},
    3: {"name": "Моторная", "price": 3000, "bonus": 1.6, "level": 6, "sound": "motor_boat.wav"},
    4: {"name": "Яхта", "price": 8000, "bonus": 2.0, "level": 8, "sound": "yacht.wav"},
}

# Переменные
player_x = SCREEN_WIDTH // 2 - 20
player_y = WATER_H + BEACH_H - 55
player_speed = 5

WALK_MIN_X = 30
WALK_MAX_X = SCREEN_WIDTH - 65
WALK_MIN_Y = WATER_H + 10
WALK_MAX_Y = SCREEN_HEIGHT - 45

money = 150
current_rod = RODS[1]
current_class = 1
current_boat = 1
inventory_baits = {2: 1, 3: 1, 4: 1, 5: 0, 6: 0}
level = 1
xp = 0
xp_to_next = 100

shop_open = False
class_shop_open = False
boat_shop_open = False

# Кнопки
btn_fish = pygame.Rect(650, 480, 130, 80)
btn_shop = pygame.Rect(650, 390, 130, 50)
btn_class = pygame.Rect(650, 330, 130, 50)
btn_boat = pygame.Rect(650, 270, 130, 50)

btn_bait1 = pygame.Rect(20, SCREEN_HEIGHT - 70, 70, 45)
btn_bait2 = pygame.Rect(95, SCREEN_HEIGHT - 70, 70, 45)
btn_bait3 = pygame.Rect(170, SCREEN_HEIGHT - 70, 70, 45)
btn_bait4 = pygame.Rect(245, SCREEN_HEIGHT - 70, 70, 45)
btn_bait5 = pygame.Rect(320, SCREEN_HEIGHT - 70, 70, 45)

btn_up = pygame.Rect(430, 440, 45, 45)
btn_down = pygame.Rect(430, 530, 45, 45)
btn_left = pygame.Rect(375, 485, 45, 45)
btn_right = pygame.Rect(485, 485, 45, 45)

# Состояние
is_fishing = False
is_bite = False
fishing_timer = 0
bite_timer = 0
last_catch = None
last_weight = 0
message = "Нажмите РЫБАЛИТЬ"
wave = 0
step_timer = 0
current_bait = None

# Система борьбы
is_fighting = False
fight_power = 100
fight_fish_name = ""
fight_weight = 0
fight_strength = 0
fight_timer = 0

# Звук лодки
current_boat_sound = None
boat_moving = False
last_boat_pos = (0, 0)

def load_texture(filename, size=None):
    path = os.path.join(TEXTURE_PATH, filename)
    if os.path.exists(path):
        try:
            tex = pygame.image.load(path).convert_alpha()
            if size:
                tex = pygame.transform.scale(tex, size)
            return tex
        except:
            return None
    return None

def load_sound(filename, volume=0.7):
    path = os.path.join(SOUND_PATH, filename)
    if os.path.exists(path):
        try:
            s = pygame.mixer.Sound(path)
            s.set_volume(volume)
            return s
        except:
            return None
    return None

def play_sound(name):
    if name in SOUNDS and SOUNDS[name]:
        try:
            SOUNDS[name].play()
        except:
            pass

def add_xp(amount):
    global xp, level, xp_to_next
    xp += amount
    while xp >= xp_to_next:
        xp -= xp_to_next
        level += 1
        xp_to_next = int(xp_to_next * 1.5)
        play_sound("levelup")

def get_total_luck():
    c = CLASSES[current_class]
    r = current_rod
    b = BOATS[current_boat]
    return c["luck"] * r["luck"] * b["bonus"]

def get_sell_bonus():
    return CLASSES[current_class]["sell"]

def get_fight_bonus():
    c = CLASSES[current_class]
    r = current_rod
    return c["fight"] * r["fight"]

def get_fish_weight(name):
    data = FISH_WEIGHT[name]
    return round(random.uniform(data["min"], data["max"]), 2)

def get_fish_price(name, weight):
    data = FISH_WEIGHT[name]
    price_per_kg = data["price_per_kg"]
    base_price = FISH_DATA[name]["price"]
    return int(base_price + weight * price_per_kg)

def get_fish_strength(name, weight):
    data = FISH_WEIGHT[name]
    base_strength = data["strength"]
    return base_strength * (weight / data["min"])

def save_game():
    data = {"money": money, "rod": current_rod["name"], "class": current_class, "boat": current_boat, "baits": inventory_baits, "level": level, "xp": xp}
    try:
        with open(SAVE_PATH, "w") as f:
            json.dump(data, f)
    except:
        pass

def load_game():
    global money, current_rod, current_class, current_boat, inventory_baits, level, xp
    try:
        with open(SAVE_PATH, "r") as f:
            data = json.load(f)
            money = data.get("money", 150)
            rod_name = data.get("rod", "Бамбуковая")
            for r in RODS.values():
                if r["name"] == rod_name:
                    current_rod = r
            current_class = data.get("class", 1)
            current_boat = data.get("boat", 1)
            inventory_baits = data.get("baits", {2: 1, 3: 1, 4: 1, 5: 0, 6: 0})
            level = data.get("level", 1)
            xp = data.get("xp", 0)
    except:
        pass

def update_boat_sound():
    global current_boat_sound, boat_moving, last_boat_pos
    if current_boat == 1:
        if current_boat_sound:
            try:
                current_boat_sound.stop()
                current_boat_sound = None
            except:
                pass
            boat_moving = False
        return
    moving = (player_x != last_boat_pos[0] or player_y != last_boat_pos[1])
    if moving and not boat_moving:
        boat = BOATS[current_boat]
        if boat["sound"] and boat["sound"] in SOUNDS and SOUNDS[boat["sound"]]:
            if current_boat_sound:
                try:
                    current_boat_sound.stop()
                except:
                    pass
            current_boat_sound = SOUNDS[boat["sound"]]
            current_boat_sound.play(-1)
            boat_moving = True
    elif not moving and boat_moving:
        if current_boat_sound:
            try:
                current_boat_sound.stop()
                current_boat_sound = None
            except:
                pass
            boat_moving = False
    last_boat_pos = (player_x, player_y)

# Загрузка текстур
fisherman_tex = load_texture("fisherman.png", (35, 45))
lake_tex = load_texture("lake_bg.png", (SCREEN_WIDTH, WATER_H))
sand_tex = load_texture("sand.png", (50, 50))
shop_bg_tex = load_texture("shop_bg.png", (600, 500))

for name, data in FISH_DATA.items():
    tex = load_texture(data["file"], (60, 35))
    data["texture"] = tex

# Звуки
SOUNDS = {}
SOUNDS["bite"] = load_sound("bite.wav", 0.7)
SOUNDS["catch"] = load_sound("catch.wav", 0.6)
SOUNDS["cast"] = load_sound("cast.wav", 0.5)
SOUNDS["shop"] = load_sound("shop.wav", 0.5)
SOUNDS["walk"] = load_sound("walk.wav", 0.3)
SOUNDS["levelup"] = load_sound("levelup.wav", 0.8)
SOUNDS["rubber_boat"] = load_sound("rubber_boat.wav", 0.4)
SOUNDS["motor_boat"] = load_sound("motor_boat.wav", 0.5)
SOUNDS["yacht"] = load_sound("yacht.wav", 0.6)

bg_path = os.path.join(SOUND_PATH, "background.mp3")
if os.path.exists(bg_path):
    pygame.mixer.music.load(bg_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

load_game()

def draw_bg():
    global wave
    wave += 0.05
    if lake_tex:
        screen.blit(lake_tex, (0, 0))
    else:
        screen.fill(DARK_BLUE, (0, 0, SCREEN_WIDTH, WATER_H))
        for y in range(0, WATER_H, 25):
            for x in range(0, SCREEN_WIDTH, 50):
                wy = y + math.sin(wave + x * 0.05) * 3
                pygame.draw.line(screen, BLUE, (x, wy), (x + 30, wy), 2)
    if sand_tex:
        for x in range(0, SCREEN_WIDTH, 50):
            for y in range(WATER_H, SCREEN_HEIGHT, 50):
                screen.blit(sand_tex, (x, y))
    else:
        pygame.draw.rect(screen, SAND, (0, WATER_H, SCREEN_WIDTH, BEACH_H))

def draw_boat():
    if current_boat > 1:
        pygame.draw.ellipse(screen, BROWN, (player_x - 15, player_y + 15, 60, 20))
        pygame.draw.rect(screen, WOOD_DARK, (player_x - 10, player_y + 10, 50, 10))

def draw_fisherman():
    if fisherman_tex:
        screen.blit(fisherman_tex, (player_x, player_y))
    else:
        c = CLASSES[current_class]
        pygame.draw.rect(screen, c["color"], (player_x, player_y, 30, 40), border_radius=5)
        pygame.draw.circle(screen, (255, 220, 180), (player_x + 15, player_y - 8), 12)
        pygame.draw.rect(screen, BLACK, (player_x + 3, player_y - 15, 24, 8))
    rod_end = (player_x + 45, player_y - 15)
    pygame.draw.line(screen, BROWN, (player_x + 25, player_y + 10), rod_end, 3)
    if is_fishing and not is_fighting:
        fx = rod_end[0] + 30
        fy = rod_end[1] + 10 + (random.randint(-3, 3) if is_bite else 0)
        pygame.draw.line(screen, WHITE, rod_end, (fx, fy), 1)
        pygame.draw.circle(screen, RED, (int(fx), int(fy)), 6)
        pygame.draw.circle(screen, WHITE, (int(fx), int(fy) - 2), 3)

def draw_fight():
    if is_fighting:
        bar_width = 400
        bar_height = 30
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 200
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, RED, (bar_x, bar_y, int(bar_width * (100 - fight_power) / 100), bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * fight_power / 100), bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 3)
        font = pygame.font.SysFont("Arial", 20, True)
        screen.blit(font.render(f"БОРЬБА! {fight_fish_name} ({fight_weight} кг)", True, GOLD), (SCREEN_WIDTH//2 - 150, bar_y - 30))
        screen.blit(font.render(f"Сила: {int(fight_power)}%", True, WHITE), (SCREEN_WIDTH//2 - 50, bar_y + bar_height + 5))

def draw_caught():
    if last_catch and not is_fighting:
        data = FISH_DATA[last_catch]
        if data.get("texture"):
            screen.blit(data["texture"], (player_x - 20, player_y - 45))
        else:
            pygame.draw.ellipse(screen, data["color"], (player_x - 20, player_y - 45, 50, 30))
        font = pygame.font.SysFont("Arial", 14, True)
        screen.blit(font.render(f"{last_catch} ({last_weight} кг)", True, GOLD), (player_x - 25, player_y - 63))

def start_fight(fish_name, weight, strength):
    global is_fighting, fight_power, fight_fish_name, fight_weight, fight_strength, is_bite, is_fishing, fight_timer
    is_fighting = True
    fight_power = 100
    fight_fish_name = fish_name
    fight_weight = weight
    fight_strength = strength
    is_bite = False
    is_fishing = True
    fight_timer = 0
    message = f"⚡ {fish_name} ({weight} кг) сопротивляется! ЖМИ 'РЫБАЛИТЬ'!"

def update_fight():
    global fight_power, is_fighting, is_bite, is_fishing, message, fight_timer
    if not is_fighting:
        return
    fight_timer += 1
    if fight_timer > 30:
        fight_timer = 0
        fight_bonus = get_fight_bonus()
        damage = random.randint(5, 15) + int(fight_strength * 2)
        damage = int(damage / fight_bonus)
        fight_power -= damage
        message = f"⚡ Борьба! {fight_fish_name} ({fight_weight} кг) | Сила: {fight_power}%"
        if fight_power <= 0:
            is_fighting = False
            is_bite = False
            is_fishing = False
            message = f"❌ Рыба сорвалась! ({fight_fish_name} {fight_weight} кг)"

def fight_catch():
    global is_fighting, last_catch, last_weight, money, xp, message, is_bite, is_fishing, fight_power
    if not is_fighting:
        return
    fight_bonus = get_fight_bonus()
    power_bonus = fight_power / 100
    fish_name = fight_fish_name
    weight = fight_weight
    base_price = get_fish_price(fish_name, weight)
    sell_bonus = get_sell_bonus()
    price = int(base_price * sell_bonus * (0.8 + power_bonus * 0.4))
    xp_gain = int(10 + weight * 5 * power_bonus)
    last_catch = fish_name
    last_weight = weight
    money += price
    add_xp(xp_gain)
    message = f"Пойман {fish_name} ({weight} кг)! +{price} руб (+{xp_gain} XP)"
    play_sound("catch")
    is_fighting = False
    is_bite = False
    is_fishing = False

def catch_fish():
    global money, last_catch, last_weight, message, xp, is_bite, is_fishing
    fishes = list(FISH_DATA.keys())
    random.shuffle(fishes)
    luck = get_total_luck()
    sell = get_sell_bonus()
    for name in fishes:
        data = FISH_DATA[name]
        chance = data["chance"] * luck
        if current_bait and BAITS.get(current_bait, {}).get("target") == name:
            chance *= BAITS[current_bait]["bonus"]
        elif current_bait and BAITS.get(current_bait, {}).get("target") is None:
            chance *= BAITS[current_bait]["bonus"]
        if random.random() < chance:
            weight = get_fish_weight(name)
            strength = get_fish_strength(name, weight)
            fight_bonus = get_fight_bonus()
            actual_strength = strength / fight_bonus
            if actual_strength > 1.5:
                start_fight(name, weight, actual_strength)
            else:
                price = get_fish_price(name, weight)
                final_price = int(price * sell)
                xp_gain = int(10 + weight * 3)
                last_catch = name
                last_weight = weight
                money += final_price
                add_xp(xp_gain)
                message = f"Пойман {name} ({weight} кг)! +{final_price} руб (+{xp_gain} XP)"
                play_sound("catch")
            return
    message = "Сорвалась!"

def draw_class_shop():
    global money, current_class, class_shop_open, message
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    panel = pygame.Rect(100, 50, 600, 500)
    if shop_bg_tex:
        screen.blit(shop_bg_tex, (panel.x, panel.y))
    pygame.draw.rect(screen, BROWN, panel, border_radius=15)
    pygame.draw.rect(screen, GOLD, panel, 4, border_radius=15)
    font = pygame.font.SysFont("Arial", 20, True)
    screen.blit(font.render("ВЫБОР КЛАССА", True, GOLD), (SCREEN_WIDTH//2 - 100, 70))
    y = 120
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    for cid, c in CLASSES.items():
        if c["level"] <= level and current_class != cid:
            btn = pygame.Rect(150, y, 500, 55)
            pygame.draw.rect(screen, (160, 100, 60), btn, border_radius=8)
            color = WHITE if money >= c["price"] else RED
            screen.blit(font.render(f"{c['emoji']} {c['name']} - {c['price']} руб", True, color), (170, y + 18))
            if btn.collidepoint(mouse_pos) and click and money >= c["price"]:
                money -= c["price"]
                current_class = cid
                message = f"Выбран {c['name']}!"
                play_sound("shop")
                pygame.time.wait(200)
            y += 65
    close = pygame.Rect(300, 520, 200, 35)
    pygame.draw.rect(screen, RED, close, border_radius=10)
    screen.blit(font.render("ЗАКРЫТЬ", True, WHITE), (375, 527))
    if close.collidepoint(mouse_pos) and click:
        class_shop_open = False
        pygame.time.wait(200)

def draw_boat_shop():
    global money, current_boat, boat_shop_open, message
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    panel = pygame.Rect(100, 50, 600, 500)
    if shop_bg_tex:
        screen.blit(shop_bg_tex, (panel.x, panel.y))
    pygame.draw.rect(screen, BROWN, panel, border_radius=15)
    pygame.draw.rect(screen, GOLD, panel, 4, border_radius=15)
    font = pygame.font.SysFont("Arial", 20, True)
    screen.blit(font.render("МАГАЗИН ЛОДОК", True, GOLD), (SCREEN_WIDTH//2 - 100, 70))
    y = 120
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    for bid, b in BOATS.items():
        if b["level"] <= level and current_boat != bid:
            btn = pygame.Rect(150, y, 500, 55)
            pygame.draw.rect(screen, (160, 100, 60), btn, border_radius=8)
            color = WHITE if money >= b["price"] else RED
            screen.blit(font.render(f"🚤 {b['name']} (x{b['bonus']}) - {b['price']} руб", True, color), (170, y + 18))
            if btn.collidepoint(mouse_pos) and click and money >= b["price"]:
                current_boat = bid
                money -= b["price"]
                message = f"Куплена {b['name']}!"
                play_sound("shop")
                update_boat_sound()
                pygame.time.wait(200)
            y += 65
    close = pygame.Rect(300, 520, 200, 35)
    pygame.draw.rect(screen, RED, close, border_radius=10)
    screen.blit(font.render("ЗАКРЫТЬ", True, WHITE), (375, 527))
    if close.collidepoint(mouse_pos) and click:
        boat_shop_open = False
        pygame.time.wait(200)

def draw_shop():
    global money, current_rod, inventory_baits, shop_open, message
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    panel = pygame.Rect(100, 50, 600, 500)
    if shop_bg_tex:
        screen.blit(shop_bg_tex, (panel.x, panel.y))
    pygame.draw.rect(screen, BROWN, panel, border_radius=15)
    pygame.draw.rect(screen, GOLD, panel, 4, border_radius=15)
    font = pygame.font.SysFont("Arial", 20, True)
    screen.blit(font.render("ЛАВКА СНАСТЕЙ", True, GOLD), (SCREEN_WIDTH//2 - 100, 70))
    y = 120
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    for rid, r in RODS.items():
        if r["level"] <= level and current_rod["name"] != r["name"]:
            btn = pygame.Rect(150, y, 500, 50)
            pygame.draw.rect(screen, (160, 100, 60), btn, border_radius=8)
            color = WHITE if money >= r["price"] else RED
            screen.blit(font.render(f"🎣 {r['name']} (x{r['luck']}) - {r['price']} руб", True, color), (170, y + 14))
            if btn.collidepoint(mouse_pos) and click and money >= r["price"]:
                current_rod = r
                money -= r["price"]
                message = f"Куплена {r['name']}!"
                play_sound("shop")
                pygame.time.wait(200)
            y += 60
    for bid, b in BAITS.items():
        if b["level"] <= level:
            btn = pygame.Rect(150, y, 500, 50)
            pygame.draw.rect(screen, (160, 100, 60), btn, border_radius=8)
            color = WHITE if money >= b["price"] else RED
            screen.blit(font.render(f"🪱 {b['name']} - {b['price']} руб", True, color), (170, y + 14))
            if btn.collidepoint(mouse_pos) and click and money >= b["price"]:
                inventory_baits[bid] = inventory_baits.get(bid, 0) + 1
                money -= b["price"]
                message = f"Куплен {b['name']}!"
                play_sound("shop")
                pygame.time.wait(200)
            y += 60
    close = pygame.Rect(300, 520, 200, 35)
    pygame.draw.rect(screen, RED, close, border_radius=10)
    screen.blit(font.render("ЗАКРЫТЬ", True, WHITE), (375, 527))
    if close.collidepoint(mouse_pos) and click:
        shop_open = False
        pygame.time.wait(200)

# ========== ГЛАВНЫЙ ЦИКЛ ==========
running = True
while running:
    wave += 0.05
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    update_boat_sound()
    update_fight()
    
    if step_timer > 0:
        step_timer -= 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shop_open and not class_shop_open and not boat_shop_open:
                if is_fighting:
                    fight_catch()
                elif btn_fish.collidepoint(mouse_pos):
                    if not is_fishing:
                        is_fishing = True
                        fishing_timer = random.randint(60, 150)
                        is_bite = False
                        message = "Забросили удочку..."
                        play_sound("cast")
                    elif is_bite:
                        catch_fish()
                        is_bite = False
                        is_fishing = False
                elif btn_shop.collidepoint(mouse_pos):
                    shop_open = True
                elif btn_class.collidepoint(mouse_pos):
                    class_shop_open = True
                elif btn_boat.collidepoint(mouse_pos):
                    boat_shop_open = True
                elif btn_bait1.collidepoint(mouse_pos) and inventory_baits.get(2, 0) > 0:
                    inventory_baits[2] -= 1
                    current_bait = 2
                    message = "Использован Жмых"
                elif btn_bait2.collidepoint(mouse_pos) and inventory_baits.get(3, 0) > 0:
                    inventory_baits[3] -= 1
                    current_bait = 3
                    message = "Использован Червь"
                elif btn_bait3.collidepoint(mouse_pos) and inventory_baits.get(4, 0) > 0:
                    inventory_baits[4] -= 1
                    current_bait = 4
                    message = "Использован Малёк"
                elif btn_bait4.collidepoint(mouse_pos) and inventory_baits.get(5, 0) > 0:
                    inventory_baits[5] -= 1
                    current_bait = 5
                    message = "Использован Жемчуг"
                elif btn_bait5.collidepoint(mouse_pos) and inventory_baits.get(6, 0) > 0:
                    inventory_baits[6] -= 1
                    current_bait = 6
                    message = "Использована Кровь дракона"
                elif btn_up.collidepoint(mouse_pos):
                    player_y = max(WALK_MIN_Y, player_y - player_speed)
                    if step_timer == 0:
                        play_sound("walk")
                        step_timer = 15
                elif btn_down.collidepoint(mouse_pos):
                    player_y = min(WALK_MAX_Y, player_y + player_speed)
                    if step_timer == 0:
                        play_sound("walk")
                        step_timer = 15
                elif btn_left.collidepoint(mouse_pos):
                    player_x = max(WALK_MIN_X, player_x - player_speed)
                    if step_timer == 0:
                        play_sound("walk")
                        step_timer = 15
                elif btn_right.collidepoint(mouse_pos):
                    player_x = min(WALK_MAX_X, player_x + player_speed)
                    if step_timer == 0:
                        play_sound("walk")
                        step_timer = 15
    
    if not shop_open and not class_shop_open and not boat_shop_open and not is_fighting:
        if is_fishing and not is_bite:
            if fishing_timer > 0:
                fishing_timer -= 1
                if fishing_timer == 0:
                    is_bite = True
                    bite_timer = 80
                    message = "КЛЮЁТ!!! ЖМИ 'РЫБАЛИТЬ'!"
                    play_sound("bite")
        elif is_bite:
            bite_timer -= 1
            if bite_timer <= 0:
                is_bite = False
                is_fishing = False
                message = "Упустили рыбу!"
    
    draw_bg()
    draw_fisherman()
    draw_boat()
    draw_caught()
    draw_fight()
    
    if not shop_open and not class_shop_open and not boat_shop_open and not is_fighting:
        font = pygame.font.SysFont("Arial", 14, True)
        pygame.draw.rect(screen, BLACK, btn_fish, border_radius=15)
        pygame.draw.rect(screen, GOLD if is_bite else WHITE, btn_fish, 3, border_radius=15)
        btn_text = "ПОДСЕКАЙ!" if is_bite else "РЫБАЛИТЬ"
        screen.blit(font.render(btn_text, True, GOLD if is_bite else WHITE), (btn_fish.x + 18, btn_fish.y + 30))
        
        pygame.draw.rect(screen, BLACK, btn_shop, border_radius=10)
        pygame.draw.rect(screen, WHITE, btn_shop, 2, border_radius=10)
        screen.blit(font.render("МАГАЗИН", True, WHITE), (btn_shop.x + 25, btn_shop.y + 15))
        
        pygame.draw.rect(screen, BLACK, btn_class, border_radius=10)
        pygame.draw.rect(screen, WHITE, btn_class, 2, border_radius=10)
        screen.blit(font.render("КЛАССЫ", True, WHITE), (btn_class.x + 28, btn_class.y + 15))
        
        pygame.draw.rect(screen, BLACK, btn_boat, border_radius=10)
        pygame.draw.rect(screen, WHITE, btn_boat, 2, border_radius=10)
        screen.blit(font.render("ЛОДКИ", True, WHITE), (btn_boat.x + 30, btn_boat.y + 15))
        
        for btn, bid, name in [(btn_bait1, 2, "Жмых"), (btn_bait2, 3, "Червь"), (btn_bait3, 4, "Малёк"), (btn_bait4, 5, "Жемчуг"), (btn_bait5, 6, "Кровь")]:
            cnt = inventory_baits.get(bid, 0)
            pygame.draw.rect(screen, BROWN, btn, border_radius=5)
            col = GOLD if cnt > 0 else GRAY
            pygame.draw.rect(screen, col, btn, 2, border_radius=5)
            screen.blit(font.render(name, True, WHITE), (btn.x + 10, btn.y + 6))
            screen.blit(font.render(str(cnt), True, GOLD), (btn.x + 30, btn.y + 26))
        
        for btn, sym in [(btn_up, "▲"), (btn_down, "▼"), (btn_left, "◀"), (btn_right, "▶")]:
            pygame.draw.rect(screen, BLACK, btn, border_radius=8)
            pygame.draw.rect(screen, WHITE, btn, 1, border_radius=8)
            screen.blit(font.render(sym, True, WHITE), (btn.x + 15, btn.y + 13))
        
        status = pygame.Surface((500, 35))
        status.fill(BLACK)
        status.set_alpha(150)
        screen.blit(status, (10, 10))
        c = CLASSES[current_class]
        b = BOATS[current_boat]
        screen.blit(font.render(f"💰 {money} руб | 🎣 {current_rod['name']} | 👤 {c['name']} | 🚤 {b['name']}", True, GOLD), (20, 18))
        
        exp_fill = int((xp / xp_to_next) * 150)
        pygame.draw.rect(screen, GRAY, (10, 55, 150, 8))
        pygame.draw.rect(screen, GOLD, (10, 55, exp_fill, 8))
        screen.blit(font.render(f"LVL {level}", True, GOLD), (10, 42))
        
        msg = font.render(message, True, WHITE)
        msg_surf = pygame.Surface((msg.get_width() + 20, 30))
        msg_surf.fill(BLACK)
        msg_surf.set_alpha(180)
        screen.blit(msg_surf, (10, 70))
        screen.blit(msg, (20, 76))
    
    elif class_shop_open:
        draw_class_shop()
    elif boat_shop_open:
        draw_boat_shop()
    elif shop_open:
        draw_shop()
    
    pygame.display.flip()
    clock.tick(60)

if current_boat_sound:
    try:
        current_boat_sound.stop()
    except:
        pass

pygame.quit()
sys.exit()