"""
Monster Battle Arena - Game Berbasis OOP dengan Visual Monster
Dibuat untuk memenuhi UAS Pemrograman Berorientasi Objek

Konsep OOP yang diimplementasikan:
1. Encapsulation: Atribut private dan getter/setter
2. Inheritance: Class turunan dari Monster
3. Polymorphism: Method overriding untuk attack()

FITUR BARU: Visual monster dengan bentuk dan animasi
"""

import tkinter as tk
from tkinter import messagebox
import random
import math


# ==================== ENCAPSULATION ====================
class Monster:
    """
    Base class untuk semua monster
    Mendemonstrasikan ENCAPSULATION dengan atribut private
    """
    def __init__(self, name, max_hp, attack_power, element, color):
        self.__name = name  # Private attribute
        self.__max_hp = max_hp  # Private attribute
        self.__current_hp = max_hp  # Private attribute
        self.__attack_power = attack_power  # Private attribute
        self.__element = element  # Private attribute
        self.__color = color  # Private attribute untuk warna visual
    
    # Getter methods (Encapsulation)
    def get_name(self):
        return self.__name
    
    def get_max_hp(self):
        return self.__max_hp
    
    def get_current_hp(self):
        return self.__current_hp
    
    def get_attack_power(self):
        return self.__attack_power
    
    def get_element(self):
        return self.__element
    
    def get_color(self):
        return self.__color
    
    # Setter methods (Encapsulation)
    def set_current_hp(self, hp):
        self.__current_hp = max(0, min(hp, self.__max_hp))
    
    def take_damage(self, damage):
        """Mengurangi HP monster"""
        self.__current_hp = max(0, self.__current_hp - damage)
    
    def is_alive(self):
        """Mengecek apakah monster masih hidup"""
        return self.__current_hp > 0
    
    def get_hp_percentage(self):
        """Menghitung persentase HP untuk health bar"""
        return (self.__current_hp / self.__max_hp) * 100
    
    # Method yang akan di-override (Polymorphism)
    def attack(self, target):
        """
        Method dasar untuk menyerang
        Akan di-override oleh subclass (Polymorphism)
        """
        damage = self.__attack_power
        target.take_damage(damage)
        return damage
    
    def special_attack(self, target):
        """Special attack dengan damage lebih besar"""
        damage = int(self.__attack_power * 1.5)
        target.take_damage(damage)
        return damage
    
    # Method untuk mendapatkan bentuk visual monster
    def get_visual_shape(self):
        """Method yang akan di-override untuk bentuk visual berbeda"""
        return "circle"


# ==================== INHERITANCE & POLYMORPHISM ====================
class FireMonster(Monster):
    """
    Monster tipe Fire - INHERITANCE dari Monster
    Mendemonstrasikan POLYMORPHISM dengan override method attack()
    Visual: Bentuk seperti bola api dengan lidah api
    """
    def __init__(self, name="Flameo"):
        super().__init__(name, max_hp=100, attack_power=25, element="Fire", color="#FF4444")
    
    def attack(self, target):
        """Override: Serangan api dengan bonus damage ke Earth"""
        base_damage = self.get_attack_power()
        
        # Polymorphism: Perilaku berbeda berdasarkan elemen target
        if target.get_element() == "Earth":
            damage = int(base_damage * 1.5)  # Super effective!
        elif target.get_element() == "Water":
            damage = int(base_damage * 0.7)  # Not effective
        else:
            damage = base_damage
        
        target.take_damage(damage)
        return damage
    
    def special_attack(self, target):
        """Special: Fireball dengan area damage"""
        damage = int(self.get_attack_power() * 2)
        target.take_damage(damage)
        return damage
    
    def get_visual_shape(self):
        """Override: Fire monster berbentuk flame/api"""
        return "fire"


class WaterMonster(Monster):
    """
    Monster tipe Water - INHERITANCE dari Monster
    Mendemonstrasikan POLYMORPHISM dengan override method attack()
    Visual: Bentuk seperti tetesan air dengan gelombang
    """
    def __init__(self, name="Aqualis"):
        super().__init__(name, max_hp=120, attack_power=20, element="Water", color="#4444FF")
    
    def attack(self, target):
        """Override: Serangan air dengan bonus damage ke Fire"""
        base_damage = self.get_attack_power()
        
        # Polymorphism: Perilaku berbeda berdasarkan elemen target
        if target.get_element() == "Fire":
            damage = int(base_damage * 1.5)  # Super effective!
        elif target.get_element() == "Earth":
            damage = int(base_damage * 0.7)  # Not effective
        else:
            damage = base_damage
        
        target.take_damage(damage)
        return damage
    
    def special_attack(self, target):
        """Special: Tsunami dengan damage besar"""
        damage = int(self.get_attack_power() * 2.2)
        target.take_damage(damage)
        return damage
    
    def get_visual_shape(self):
        """Override: Water monster berbentuk droplet"""
        return "water"


class EarthMonster(Monster):
    """
    Monster tipe Earth - INHERITANCE dari Monster
    Mendemonstrasikan POLYMORPHISM dengan override method attack()
    Visual: Bentuk seperti batu dengan tekstur
    """
    def __init__(self, name="Terrados"):
        super().__init__(name, max_hp=140, attack_power=18, element="Earth", color="#44FF44")
    
    def attack(self, target):
        """Override: Serangan tanah dengan bonus damage ke Water"""
        base_damage = self.get_attack_power()
        
        # Polymorphism: Perilaku berbeda berdasarkan elemen target
        if target.get_element() == "Water":
            damage = int(base_damage * 1.5)  # Super effective!
        elif target.get_element() == "Fire":
            damage = int(base_damage * 0.7)  # Not effective
        else:
            damage = base_damage
        
        target.take_damage(damage)
        return damage
    
    def special_attack(self, target):
        """Special: Earthquake dengan damage area"""
        damage = int(self.get_attack_power() * 2.3)
        target.take_damage(damage)
        return damage
    
    def get_visual_shape(self):
        """Override: Earth monster berbentuk rock/batu"""
        return "earth"


# ==================== VISUAL MONSTER RENDERER ====================
class MonsterVisual:
    """
    Class untuk merender visual monster di canvas
    Mendemonstrasikan composition dan encapsulation
    """
    def __init__(self, canvas, x, y, monster, is_player=True):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.monster = monster
        self.is_player = is_player
        self.parts = []  # List untuk menyimpan ID objek canvas
        self.animation_offset = 0
        
    def draw(self):
        """Menggambar monster berdasarkan tipenya"""
        shape_type = self.monster.get_visual_shape()
        
        if shape_type == "fire":
            self.draw_fire_monster()
        elif shape_type == "water":
            self.draw_water_monster()
        elif shape_type == "earth":
            self.draw_earth_monster()
    
    def draw_fire_monster(self):
        """Menggambar Fire Monster - bentuk api"""
        color = self.monster.get_color()
        
        # Body - lingkaran besar
        body = self.canvas.create_oval(
            self.x - 40, self.y - 40,
            self.x + 40, self.y + 40,
            fill=color, outline="#CC0000", width=3
        )
        self.parts.append(body)
        
        # Inner glow
        inner = self.canvas.create_oval(
            self.x - 25, self.y - 25,
            self.x + 25, self.y + 25,
            fill="#FF8844", outline=""
        )
        self.parts.append(inner)
        
        # Flames (lidah api) - 3 buah
        for i in range(3):
            angle = (i - 1) * 40
            flame_x = self.x + math.cos(math.radians(270 + angle)) * 30
            flame_y = self.y + math.sin(math.radians(270 + angle)) * 30
            
            flame = self.canvas.create_polygon(
                flame_x, flame_y - 25,
                flame_x - 10, flame_y,
                flame_x + 10, flame_y,
                fill="#FFAA00", outline="#FF4400", width=2
            )
            self.parts.append(flame)
        
        # Eyes
        eye1 = self.canvas.create_oval(
            self.x - 15, self.y - 10,
            self.x - 5, self.y,
            fill="#FFFF00", outline="black"
        )
        eye2 = self.canvas.create_oval(
            self.x + 5, self.y - 10,
            self.x + 15, self.y,
            fill="#FFFF00", outline="black"
        )
        self.parts.extend([eye1, eye2])
        
        # Pupils
        pupil1 = self.canvas.create_oval(
            self.x - 12, self.y - 7,
            self.x - 8, self.y - 3,
            fill="black"
        )
        pupil2 = self.canvas.create_oval(
            self.x + 8, self.y - 7,
            self.x + 12, self.y - 3,
            fill="black"
        )
        self.parts.extend([pupil1, pupil2])
    
    def draw_water_monster(self):
        """Menggambar Water Monster - bentuk droplet"""
        color = self.monster.get_color()
        
        # Body - bentuk tetesan air
        body = self.canvas.create_polygon(
            self.x, self.y - 50,  # Top point
            self.x - 35, self.y,
            self.x - 30, self.y + 20,
            self.x, self.y + 35,  # Bottom
            self.x + 30, self.y + 20,
            self.x + 35, self.y,
            fill=color, outline="#0000CC", width=3, smooth=True
        )
        self.parts.append(body)
        
        # Inner highlight (white shine)
        highlight = self.canvas.create_oval(
            self.x - 15, self.y - 20,
            self.x + 5, self.y,
            fill="#AACCFF", outline=""
        )
        self.parts.append(highlight)
        
        # Waves (gelombang) - 3 garis bergelombang
        for i in range(3):
            wave_y = self.y - 10 + (i * 15)
            wave = self.canvas.create_line(
                self.x - 20, wave_y,
                self.x - 10, wave_y - 5,
                self.x, wave_y,
                self.x + 10, wave_y - 5,
                self.x + 20, wave_y,
                fill="#6688FF", width=2, smooth=True
            )
            self.parts.append(wave)
        
        # Eyes
        eye1 = self.canvas.create_oval(
            self.x - 15, self.y,
            self.x - 5, self.y + 10,
            fill="white", outline="black"
        )
        eye2 = self.canvas.create_oval(
            self.x + 5, self.y,
            self.x + 15, self.y + 10,
            fill="white", outline="black"
        )
        self.parts.extend([eye1, eye2])
        
        # Pupils
        pupil1 = self.canvas.create_oval(
            self.x - 12, self.y + 3,
            self.x - 8, self.y + 7,
            fill="#000088"
        )
        pupil2 = self.canvas.create_oval(
            self.x + 8, self.y + 3,
            self.x + 12, self.y + 7,
            fill="#000088"
        )
        self.parts.extend([pupil1, pupil2])
    
    def draw_earth_monster(self):
        """Menggambar Earth Monster - bentuk batu"""
        color = self.monster.get_color()
        
        # Body - bentuk batu (hexagon tidak beraturan)
        body = self.canvas.create_polygon(
            self.x, self.y - 45,
            self.x + 40, self.y - 20,
            self.x + 35, self.y + 30,
            self.x, self.y + 40,
            self.x - 35, self.y + 30,
            self.x - 40, self.y - 20,
            fill=color, outline="#228800", width=3
        )
        self.parts.append(body)
        
        # Cracks (retakan batu) - garis-garis
        crack1 = self.canvas.create_line(
            self.x - 20, self.y - 30,
            self.x - 10, self.y,
            self.x - 15, self.y + 20,
            fill="#116600", width=2
        )
        crack2 = self.canvas.create_line(
            self.x + 15, self.y - 25,
            self.x + 10, self.y + 5,
            self.x + 20, self.y + 25,
            fill="#116600", width=2
        )
        self.parts.extend([crack1, crack2])
        
        # Moss patches (lumut)
        moss1 = self.canvas.create_oval(
            self.x - 25, self.y + 15,
            self.x - 10, self.y + 25,
            fill="#338833", outline=""
        )
        moss2 = self.canvas.create_oval(
            self.x + 10, self.y - 10,
            self.x + 20, self.y,
            fill="#338833", outline=""
        )
        self.parts.extend([moss1, moss2])
        
        # Eyes (lebih kotak untuk kesan batu)
        eye1 = self.canvas.create_rectangle(
            self.x - 15, self.y - 5,
            self.x - 5, self.y + 5,
            fill="#88FF88", outline="black", width=2
        )
        eye2 = self.canvas.create_rectangle(
            self.x + 5, self.y - 5,
            self.x + 15, self.y + 5,
            fill="#88FF88", outline="black", width=2
        )
        self.parts.extend([eye1, eye2])
        
        # Pupils
        pupil1 = self.canvas.create_rectangle(
            self.x - 12, self.y - 2,
            self.x - 8, self.y + 2,
            fill="#004400"
        )
        pupil2 = self.canvas.create_rectangle(
            self.x + 8, self.y - 2,
            self.x + 12, self.y + 2,
            fill="#004400"
        )
        self.parts.extend([pupil1, pupil2])
    
    def animate_attack(self):
        """Animasi saat monster menyerang"""
        # Geser monster sedikit ke depan
        move_x = 20 if self.is_player else -20
        for part in self.parts:
            self.canvas.move(part, move_x, 0)
        
        # Kembali ke posisi awal setelah delay
        self.canvas.after(200, lambda: self.reset_position(move_x))
    
    def reset_position(self, move_x):
        """Reset posisi setelah animasi"""
        for part in self.parts:
            self.canvas.move(part, -move_x, 0)
    
    def shake(self):
        """Animasi shake saat terkena damage"""
        for i in range(3):
            offset = 10 if i % 2 == 0 else -10
            self.canvas.after(i * 50, lambda o=offset: self.apply_shake(o))
        self.canvas.after(150, lambda: self.apply_shake(0))
    
    def apply_shake(self, offset):
        """Apply shake offset"""
        if len(self.parts) > 0:
            current_x = self.canvas.coords(self.parts[0])[0]
            for part in self.parts:
                self.canvas.move(part, offset - self.animation_offset, 0)
            self.animation_offset = offset
    
    def clear(self):
        """Hapus semua parts dari canvas"""
        for part in self.parts:
            self.canvas.delete(part)
        self.parts = []


# ==================== GAME CONTROLLER ====================
class BattleGame:
    """
    Controller untuk mengatur logika game
    Mendemonstrasikan composition dan encapsulation
    """
    def __init__(self):
        self.__player_monster = None
        self.__enemy_monster = None
        self.__battle_log = []
        self.__wins = 0
        self.__losses = 0
    
    def set_player_monster(self, monster_type):
        """Memilih monster pemain"""
        if monster_type == "Fire":
            self.__player_monster = FireMonster("Your Flameo")
        elif monster_type == "Water":
            self.__player_monster = WaterMonster("Your Aqualis")
        elif monster_type == "Earth":
            self.__player_monster = EarthMonster("Your Terrados")
    
    def create_enemy_monster(self):
        """Membuat monster musuh secara random"""
        monster_types = [FireMonster, WaterMonster, EarthMonster]
        enemy_class = random.choice(monster_types)
        self.__enemy_monster = enemy_class("Enemy " + enemy_class.__name__.replace("Monster", ""))
    
    def get_player_monster(self):
        return self.__player_monster
    
    def get_enemy_monster(self):
        return self.__enemy_monster
    
    def player_attack(self, is_special=False):
        """Pemain menyerang musuh"""
        if is_special:
            damage = self.__player_monster.special_attack(self.__enemy_monster)
            attack_type = "SPECIAL ATTACK"
        else:
            damage = self.__player_monster.attack(self.__enemy_monster)
            attack_type = "ATTACK"
        
        log = f"{self.__player_monster.get_name()} uses {attack_type}! Deals {damage} damage!"
        self.__battle_log.append(log)
        return log
    
    def enemy_attack(self):
        """Musuh menyerang pemain"""
        is_special = random.random() < 0.3
        
        if is_special:
            damage = self.__enemy_monster.special_attack(self.__player_monster)
            attack_type = "SPECIAL ATTACK"
        else:
            damage = self.__enemy_monster.attack(self.__player_monster)
            attack_type = "ATTACK"
        
        log = f"{self.__enemy_monster.get_name()} uses {attack_type}! Deals {damage} damage!"
        self.__battle_log.append(log)
        return log
    
    def check_battle_end(self):
        """Mengecek apakah battle sudah selesai"""
        if not self.__player_monster.is_alive():
            self.__losses += 1
            return "lose"
        elif not self.__enemy_monster.is_alive():
            self.__wins += 1
            return "win"
        return None
    
    def get_stats(self):
        """Mendapatkan statistik win/lose"""
        return self.__wins, self.__losses
    
    def reset_battle(self):
        """Reset battle untuk pertarungan baru"""
        self.__player_monster = None
        self.__enemy_monster = None
        self.__battle_log = []


# ==================== GUI APPLICATION ====================
class MonsterBattleGUI:
    """
    GUI Application menggunakan Tkinter dengan Visual Monster
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Monster Battle Arena - Visual Edition")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        
        self.game = BattleGame()
        self.player_visual = None
        self.enemy_visual = None
        
        self.create_menu_screen()
    
    def clear_screen(self):
        """Membersihkan semua widget dari screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_menu_screen(self):
        """Membuat menu utama"""
        self.clear_screen()
        
        # Title
        title = tk.Label(
            self.root, 
            text="MONSTER BATTLE ARENA", 
            font=("Arial", 32, "bold"),
            bg="#1a1a2e",
            fg="#00ff88"
        )
        title.pack(pady=30)
        
        subtitle = tk.Label(
            self.root,
            text="Choose Your Monster!",
            font=("Arial", 18),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        subtitle.pack(pady=10)
        
        # Preview canvas untuk menampilkan monster
        preview_frame = tk.Frame(self.root, bg="#1a1a2e")
        preview_frame.pack(pady=20)
        
        # Fire preview
        fire_frame = tk.Frame(preview_frame, bg="#16213e", relief="raised", borderwidth=3)
        fire_frame.grid(row=0, column=0, padx=15)
        
        fire_canvas = tk.Canvas(fire_frame, width=150, height=150, bg="#0f3460", highlightthickness=0)
        fire_canvas.pack(pady=10)
        
        # Draw fire monster preview
        temp_fire = FireMonster()
        fire_vis = MonsterVisual(fire_canvas, 75, 75, temp_fire)
        fire_vis.draw()
        
        fire_btn = tk.Button(
            fire_frame,
            text="🔥 FIRE\nFlameo\nHP: 100 | ATK: 25",
            font=("Arial", 11, "bold"),
            bg="#ff4444",
            fg="white",
            width=15,
            height=3,
            command=lambda: self.start_battle("Fire")
        )
        fire_btn.pack(pady=10)
        
        # Water preview
        water_frame = tk.Frame(preview_frame, bg="#16213e", relief="raised", borderwidth=3)
        water_frame.grid(row=0, column=1, padx=15)
        
        water_canvas = tk.Canvas(water_frame, width=150, height=150, bg="#0f3460", highlightthickness=0)
        water_canvas.pack(pady=10)
        
        temp_water = WaterMonster()
        water_vis = MonsterVisual(water_canvas, 75, 75, temp_water)
        water_vis.draw()
        
        water_btn = tk.Button(
            water_frame,
            text="💧 WATER\nAqualis\nHP: 120 | ATK: 20",
            font=("Arial", 11, "bold"),
            bg="#4444ff",
            fg="white",
            width=15,
            height=3,
            command=lambda: self.start_battle("Water")
        )
        water_btn.pack(pady=10)
        
        # Earth preview
        earth_frame = tk.Frame(preview_frame, bg="#16213e", relief="raised", borderwidth=3)
        earth_frame.grid(row=0, column=2, padx=15)
        
        earth_canvas = tk.Canvas(earth_frame, width=150, height=150, bg="#0f3460", highlightthickness=0)
        earth_canvas.pack(pady=10)
        
        temp_earth = EarthMonster()
        earth_vis = MonsterVisual(earth_canvas, 75, 75, temp_earth)
        earth_vis.draw()
        
        earth_btn = tk.Button(
            earth_frame,
            text="🌍 EARTH\nTerrados\nHP: 140 | ATK: 18",
            font=("Arial", 11, "bold"),
            bg="#44ff44",
            fg="black",
            width=15,
            height=3,
            command=lambda: self.start_battle("Earth")
        )
        earth_btn.pack(pady=10)
        
        # Stats
        wins, losses = self.game.get_stats()
        stats = tk.Label(
            self.root,
            text=f"Stats - Wins: {wins} | Losses: {losses}",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg="#ffaa00"
        )
        stats.pack(pady=20)
    
    def start_battle(self, monster_type):
        """Memulai battle dengan monster yang dipilih"""
        self.game.set_player_monster(monster_type)
        self.game.create_enemy_monster()
        self.create_battle_screen()
    
    def create_battle_screen(self):
        """Membuat screen battle dengan visual monster"""
        self.clear_screen()
        
        # Title
        title = tk.Label(
            self.root,
            text="⚔️ BATTLE! ⚔️",
            font=("Arial", 24, "bold"),
            bg="#1a1a2e",
            fg="#ff0000"
        )
        title.pack(pady=10)
        
        # Battle arena canvas
        arena_frame = tk.Frame(self.root, bg="#16213e", relief="sunken", borderwidth=5)
        arena_frame.pack(pady=10)
        
        self.arena_canvas = tk.Canvas(
            arena_frame,
            width=800,
            height=250,
            bg="#0f3460",
            highlightthickness=0
        )
        self.arena_canvas.pack()
        
        # Draw monsters
        player = self.game.get_player_monster()
        enemy = self.game.get_enemy_monster()
        
        self.player_visual = MonsterVisual(self.arena_canvas, 150, 125, player, is_player=True)
        self.player_visual.draw()
        
        self.enemy_visual = MonsterVisual(self.arena_canvas, 650, 125, enemy, is_player=False)
        self.enemy_visual.draw()
        
        # Info panel
        info_frame = tk.Frame(self.root, bg="#1a1a2e")
        info_frame.pack(pady=10)
        
        # Player info
        player_frame = tk.Frame(info_frame, bg="#16213e", relief="raised", borderwidth=3)
        player_frame.grid(row=0, column=0, padx=20)
        
        tk.Label(
            player_frame,
            text=player.get_name(),
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#00ff88"
        ).pack(pady=5)
        
        tk.Label(
            player_frame,
            text=f"🔥 {player.get_element()}",
            font=("Arial", 11),
            bg="#16213e",
            fg="white"
        ).pack()
        
        self.player_hp_label = tk.Label(
            player_frame,
            text=f"HP: {player.get_current_hp()}/{player.get_max_hp()}",
            font=("Arial", 11),
            bg="#16213e",
            fg="white"
        )
        self.player_hp_label.pack(pady=5)
        
        self.player_hp_bar = tk.Canvas(player_frame, width=200, height=20, bg="#333333")
        self.player_hp_bar.pack(pady=5, padx=10, ipadx=5, ipady=5)
        
        # Enemy info
        enemy_frame = tk.Frame(info_frame, bg="#16213e", relief="raised", borderwidth=3)
        enemy_frame.grid(row=0, column=1, padx=20)
        
        tk.Label(
            enemy_frame,
            text=enemy.get_name(),
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#ff4444"
        ).pack(pady=5)
        
        tk.Label(
            enemy_frame,
            text=f"🔥 {enemy.get_element()}",
            font=("Arial", 11),
            bg="#16213e",
            fg="white"
        ).pack()
        
        self.enemy_hp_label = tk.Label(
            enemy_frame,
            text=f"HP: {enemy.get_current_hp()}/{enemy.get_max_hp()}",
            font=("Arial", 11),
            bg="#16213e",
            fg="white"
        )
        self.enemy_hp_label.pack(pady=5)
        
        self.enemy_hp_bar = tk.Canvas(enemy_frame, width=200, height=20, bg="#333333")
        self.enemy_hp_bar.pack(pady=5, padx=10, ipadx=5, ipady=5)
        
        # Battle log
        self.battle_log = tk.Text(
            self.root,
            height=6,
            width=80,
            font=("Courier", 10),
            bg="#0f3460",
            fg="#00ff88",
            state="disabled"
        )
        self.battle_log.pack(pady=10)
        
        # Action buttons
        action_frame = tk.Frame(self.root, bg="#1a1a2e")
        action_frame.pack(pady=10)
        
        self.attack_btn = tk.Button(
            action_frame,
            text="⚔️ ATTACK",
            font=("Arial", 13, "bold"),
            bg="#ff6600",
            fg="white",
            width=15,
            height=2,
            command=self.player_normal_attack
        )
        self.attack_btn.grid(row=0, column=0, padx=10)
        
        self.special_btn = tk.Button(
            action_frame,
            text="💥 SPECIAL ATTACK",
            font=("Arial", 13, "bold"),
            bg="#ff0066",
            fg="white",
            width=15,
            height=2,
            command=self.player_special_attack
        )
        self.special_btn.grid(row=0, column=1, padx=10)
        
        # Update display
        self.update_battle_display()
        self.add_battle_log("⚔️ Battle Start! Choose your action!")
    
    def update_battle_display(self):
        """Update tampilan HP dan health bar"""
        player = self.game.get_player_monster()
        enemy = self.game.get_enemy_monster()
        
        # Update player HP
        self.player_hp_label.config(
            text=f"HP: {player.get_current_hp()}/{player.get_max_hp()}"
        )
        self.player_hp_bar.delete("all")
        hp_width = int((player.get_hp_percentage() / 100) * 200)
        hp_color = "#00ff00" if player.get_hp_percentage() > 50 else "#ffaa00" if player.get_hp_percentage() > 25 else "#ff0000"
        self.player_hp_bar.create_rectangle(0, 0, hp_width, 20, fill=hp_color)
        
        # Update enemy HP
        self.enemy_hp_label.config(
            text=f"HP: {enemy.get_current_hp()}/{enemy.get_max_hp()}"
        )
        self.enemy_hp_bar.delete("all")
        hp_width = int((enemy.get_hp_percentage() / 100) * 200)
        hp_color = "#00ff00" if enemy.get_hp_percentage() > 50 else "#ffaa00" if enemy.get_hp_percentage() > 25 else "#ff0000"
        self.enemy_hp_bar.create_rectangle(0, 0, hp_width, 20, fill=hp_color)
    
    def add_battle_log(self, message):
        """Menambahkan pesan ke battle log"""
        self.battle_log.config(state="normal")
        self.battle_log.insert("end", message + "\n")
        self.battle_log.see("end")
        self.battle_log.config(state="disabled")
    
    def player_normal_attack(self):
        """Handle player normal attack dengan animasi"""
        self.disable_buttons()
        
        # Animasi attack
        self.player_visual.animate_attack()
        
        # Delay untuk sinkronisasi animasi
        self.root.after(200, self.execute_player_attack)
    
    def execute_player_attack(self):
        """Execute player attack setelah animasi"""
        log = self.game.player_attack(is_special=False)
        self.add_battle_log(log)
        
        # Animasi enemy terkena damage
        self.enemy_visual.shake()
        
        self.update_battle_display()
        
        result = self.game.check_battle_end()
        if result:
            self.end_battle(result)
            return
        
        self.root.after(1000, self.enemy_turn)
    
    def player_special_attack(self):
        """Handle player special attack dengan animasi"""
        self.disable_buttons()
        
        # Animasi special attack (lebih kuat)
        self.player_visual.animate_attack()
        
        self.root.after(200, self.execute_player_special)
    
    def execute_player_special(self):
        """Execute player special attack"""
        log = self.game.player_attack(is_special=True)
        self.add_battle_log(log)
        
        # Animasi enemy terkena damage
        self.enemy_visual.shake()
        
        self.update_battle_display()
        
        result = self.game.check_battle_end()
        if result:
            self.end_battle(result)
            return
        
        self.root.after(1000, self.enemy_turn)
    
    def enemy_turn(self):
        """Handle enemy turn dengan animasi"""
        # Animasi enemy attack
        self.enemy_visual.animate_attack()
        
        self.root.after(200, self.execute_enemy_attack)
    
    def execute_enemy_attack(self):
        """Execute enemy attack"""
        log = self.game.enemy_attack()
        self.add_battle_log(log)
        
        # Animasi player terkena damage
        self.player_visual.shake()
        
        self.update_battle_display()
        
        result = self.game.check_battle_end()
        if result:
            self.end_battle(result)
            return
        
        self.enable_buttons()
    
    def disable_buttons(self):
        """Disable action buttons"""
        self.attack_btn.config(state="disabled")
        self.special_btn.config(state="disabled")
    
    def enable_buttons(self):
        """Enable action buttons"""
        self.attack_btn.config(state="normal")
        self.special_btn.config(state="normal")
    
    def end_battle(self, result):
        """Handle battle end"""
        if result == "win":
            message = "🎉 VICTORY! You won the battle!"
            self.add_battle_log("\n" + message)
        else:
            message = "💀 DEFEAT! You lost the battle!"
            self.add_battle_log("\n" + message)
        
        self.disable_buttons()
        
        # Show return button
        return_btn = tk.Button(
            self.root,
            text="Return to Menu",
            font=("Arial", 14, "bold"),
            bg="#4444ff",
            fg="white",
            width=20,
            height=2,
            command=self.return_to_menu
        )
        return_btn.pack(pady=10)
    
    def return_to_menu(self):
        """Kembali ke menu utama"""
        self.game.reset_battle()
        self.create_menu_screen()


# ==================== MAIN PROGRAM ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = MonsterBattleGUI(root)
    root.mainloop()