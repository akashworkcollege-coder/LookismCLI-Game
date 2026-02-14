#!/usr/bin/env python3
"""
LOOKISM: AWAKENED FIST - COMPLETE CANON EDITION
ALL 51 FIGHTING CHARACTERS - 100% Manhwa Accurate
DEBUGGED VERSION - All methods and classes included
Based on Park Tae-joon's Lookism (2014-2025) & Manager Kim (Spin-off)
"""

import random
import time
import sys
import json
import os
from enum import Enum
from datetime import datetime

# ============================================================================
# SAVE/LOAD SYSTEM
# ============================================================================

SAVE_FILE = "lookism_save.json"


class SaveSystem:
    @staticmethod
    def save_game(game_state):
        """Save game progress to file"""
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(game_state, f, indent=4)
            return True
        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False

    @staticmethod
    def load_game():
        """Load game progress from file"""
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"❌ Load failed: {e}")
            return None

    @staticmethod
    def delete_save():
        """Delete save file"""
        try:
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
                return True
            return False
        except:
            return False


# ============================================================================
# TEXT SPEED CONTROL
# ============================================================================

TEXT_SPEED = 0.6
BATTLE_START_DELAY = 2.0
TURN_DELAY = 1.0
ACTION_DELAY = 0.8
VICTORY_DELAY = 2.5


def slow_print(text, delay=0.03):
    """Print text character by character for dramatic effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


# ============================================================================
# CANON GYEONGJI (REALM) SYSTEM
# ============================================================================

class Realm(Enum):
    NONE = "⚪ None"
    SPEED = "🔵 Speed - Invisible attacks, blue aura"
    STRENGTH = "🔴 Strength - Overwhelming power, red aura"
    TENACITY = "🟢 Tenacity - Extreme durability, green aura"
    TECHNIQUE = "🩷 Technique - Perfected form, pink aura"
    OVERCOMING = "🟣 Overcoming - Born from limits, purple aura"


# ============================================================================
# PATH SYSTEM - COMPLETE CANON PATHS
# ============================================================================

class Path(Enum):
    # GEN 0 LEGENDS
    GAPRYONG_CONVICTION = "👑 Gapryong's Conviction - The legendary fist that changed Gen 0"
    TOM_LEE_WILD = "🐅 Tom Lee's Wild - Animal instincts, biting, slashing"
    CHARLES_ELITE = "🎭 Charles Choi's Invisible Attacks - Elite technique from Gapryong's Fist"
    JINYOUNG_COPY = "🔄 Jinyoung Park's Copy - Perfect replication of any technique"
    BAEKHO_BEAST = "🐯 Baekho's Beast Mode - White Tiger's wild fighting"
    GAPRYONG_FIST_MEMBER = "👊 Gapryong's Fist Member - Legendary crew fighter"

    # 1ST GENERATION KINGS
    JAMES_LEE_INVISIBLE = "👑 James Lee's Invisible Attacks - The peak of 1st Gen"
    GITAE_KIM = "⚡ Gitae Kim - Gapryong's son, unknown style"
    JICHANG_HAND_BLADE = "🩷 Jichang Kwak's Hand Blade - Knife-hand mastery"
    TAESOO_MA_FIST = "🔴 Taesoo Ma's Right Hand - Pure power, no technique"
    GONGSEOB_IRON = "🔨 Gongseob Ji's Iron Boxing - Speed + Tungsten durability"
    SEOKDU_HEADBUTT = "💢 Seokdu Wang's Headbutt - Forehead specialist"
    JAEGYEON_SPEED = "🔵 Jaegyeon Na's Speed - Fastest man in Korea"
    SEONGJI_MONSTER = "🦍 Seongji Yuk's Monster Style - Ssireum + Judo + Kudo"
    JINRANG_CONVICTION = "👑 Jinrang's True Conviction - Gapryong's disciple"

    # GEN 2 CREW LEADERS
    DANIEL_UI = "👁️ Daniel Park's Ultra Instinct - White hair awakening"
    DANIEL_COPY = "⚡ Daniel Park's Copy Master - Perfect replication"
    ZACK_IRON = "🔨 Zack Lee's Iron Boxing - Gongseob Ji's style"
    JOHAN_GOD_EYE = "👁️ Johan Seong's God Eye - Ultimate copy"
    JOHAN_CHOREOGRAPHY = "💃 Johan Seong's Choreography - Dance combat"
    VASCO_SYSTEMA = "🇷🇺 Vasco's Systema Master - Russian martial art"
    VASCO_MUAY_THAI = "🇹🇭 Vasco's Muay Thai Legend - Devastating strikes"
    JAY_KALI = "🇵🇭 Jay Hong's Kali Master - Twin blade perfection"
    ELI_BEAST = "🦁 Eli Jang's Beast King - Animal instincts"
    ELI_TOM_LEE = "🐅 Eli Jang's Tom Lee Legacy - Inherited wild"
    WARREN_JKD = "🥋 Warren Chae's Jeet Kune Do - Bruce Lee's philosophy"
    WARREN_CQC = "🔫 Warren Chae's CQC Operator - Military precision"
    WARREN_HEART = "💔 Warren Chae's Heart Attack - One-inch punch"
    JAKE_CONVICTION = "⚖️ Jake Kim's Conviction King - Willpower"
    JAKE_GAPRYONG = "👑 Jake Kim's Gapryong Blood - Inherited fist"
    GUN_YAMAZAKI = "🏯 Gun Park's Yamazaki Heir - Darkness within"
    GUN_CONSTANT_UI = "👁️ Gun Park's Constant UI - Permanent awakening"
    GOO_MOONLIGHT = "🌙 Goo Kim's Moonlight Sword - 5 sword styles"
    GOO_FIFTH = "✨ Goo Kim's Fifth Sword - Technique impossible"
    JOONGOO_HWARANG = "⚔️ Kim Jun-gu's Hwarang Sword - Cuts goblins"
    JOONGOO_ARMED = "🗡️ Kim Jun-gu's Armed Beast - Top 3 when armed"

    # WORKERS
    MANDEOK_POWER = "💪 Mandeok's Titan Strength - Raw power"
    CAP_GUY_CQC = "🔫 Cap Guy's CQC Master - Silver Yarn threads"
    XIAOLUNG_MUAY_THAI = "🇹🇭 Xiaolung's Muay Thai Genius - Elbows and knees"
    RYUHEI_YAKUZA = "⚔️ Ryuhei's Yakuza Style - Gang fighting"
    SAMUEL_AMBITION = "👑 Samuel Seo's King's Ambition - Betrayer's strength"
    SINU_INVISIBLE = "🌀 Sinu Han's Invisible Attacks - Hands and legs"
    LOGAN_BULLY = "👊 Logan Lee's Bully Brawling - Cheap shots"

    # CHEONLIANG
    VIN_JIN_SSIREUM = "🇰🇷 Vin Jin's Ssireum Genius - Korean wrestling"
    SEONGJI_MARTIAL = "🥋 Seongji Yuk's Martial Arts - Ssireum + Judo + Kudo"
    HAN_JAEHA = "🤼 Han Jaeha's Ssireum - Traditional wrestling"
    BAEK_SEONG_TAEKKYON = "🦢 Baek Seong's Taekkyon - Flowing martial art"

    # YAMAZAKI
    SHINGEN_YAMAZAKI = "🏯 Shingen Yamazaki's Ultimate - Yamazaki head"
    PARK_FATHER = "❓ Park Jonggun's Father - Mysterious bloodline"

    # LAW ENFORCEMENT
    KIM_MINJAE_JUDO = "🥋 Kim Minjae's Judo - Police officer"
    DETECTIVE_KANG_BOXING = "🥊 Detective Kang's Boxing - Veteran detective"


# ============================================================================
# CHARACTER BASE CLASS
# ============================================================================

class Character:
    def __init__(self, name, title, hp, energy, realm_list=None):
        self.name = name
        self.title = title
        self.hp = hp
        self.max_hp = hp
        self.energy = energy
        self.max_energy = energy
        self.abilities = {}
        self.infinity_technique = None
        self.path = None
        self.paths_available = []
        self.buffs = []
        self.debuffs = []
        self.defending = False
        self.form = "Normal"
        self.realms = realm_list if realm_list else []
        self.active_realm = Realm.NONE
        self.realm_timer = 0
        self.affiliation = ""
        self.canon_episode = 0
        self.path_level = 1
        self.path_exp = 0
        self.path_history = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def activate_realm(self, realm):
        if realm not in self.realms:
            return f"{self.name} cannot use {realm.value}!"
        self.active_realm = realm
        self.realm_timer = 5
        self.form = f"REALM: {realm.name}"
        effects = {
            Realm.SPEED: "🔵 SPEED REALM - Attacks become invisible! +50% evasion, 30% double strike",
            Realm.STRENGTH: "🔴 STRENGTH REALM - Overwhelming power! +70% damage, armor break",
            Realm.TENACITY: "🟢 TENACITY REALM - Extreme durability! -50% damage taken, +15 HP/turn",
            Realm.TECHNIQUE: "🩷 TECHNIQUE REALM - Perfected form! +40% accuracy, 25% counter",
            Realm.OVERCOMING: "🟣 OVERCOMING REALM - Born from limits! +100% damage when below 30% HP"
        }
        return effects.get(realm, f"{realm.value} activated!")

    def choose_path(self, path):
        if path in self.paths_available:
            if self.path:
                self.path_history.append(self.path)
            self.path = path
            self.infinity_technique = INFINITY_TECHNIQUES.get(path)
            self.path_level = 1
            self.path_exp = 0
            if self.infinity_technique:
                return f"\n✨✨✨ {self.name} walks the path of {path.value} ✨✨✨\n\n{self.infinity_technique['desc']}\n"
            return f"\n{self.name} walks the path of {path.value}\n"
        return f"\n{path} is not available for {self.name}\n"

    def reset_path(self):
        if self.path_history:
            self.path = self.path_history.pop()
            self.infinity_technique = INFINITY_TECHNIQUES.get(self.path)
            self.path_level = 1
            self.path_exp = 0
            return f"🔄 {self.name} returns to previous path: {self.path.value}"
        else:
            self.path = None
            self.infinity_technique = None
            self.path_level = 1
            self.path_exp = 0
            return f"🔄 {self.name}'s path has been reset. Choose a new path!"

    def to_dict(self):
        """Convert character to dictionary for saving"""
        return {
            'name': self.name,
            'path': self.path.name if self.path else None,
            'path_level': self.path_level,
            'path_exp': self.path_exp,
            'hp': self.hp,
            'energy': self.energy
        }

    def from_dict(self, data):
        """Load character from dictionary"""
        if data['path']:
            for path in Path:
                if path.name == data['path']:
                    self.path = path
                    self.infinity_technique = INFINITY_TECHNIQUES.get(path)
                    break
        self.path_level = data['path_level']
        self.path_exp = data['path_exp']
        self.hp = data['hp']
        self.energy = data['energy']


# ============================================================================
# INFINITY TECHNIQUES DATABASE
# ============================================================================

INFINITY_TECHNIQUES = {
    # GEN 0 LEGENDS
    Path.GAPRYONG_CONVICTION: {
        "name": "👑 INFINITE GAPRYONG: Legend's Fist",
        "cost": 150,
        "dmg": (300, 400),
        "desc": "The legendary fist that defeated the Yamazaki Syndicate. Gapryong Kim's ultimate conviction - a punch that changed the course of Gen 0."
    },
    Path.TOM_LEE_WILD: {
        "name": "🐅 INFINITE WILD: Tom Lee Special",
        "cost": 140,
        "dmg": (280, 380),
        "desc": "Tom Lee's ultimate technique. Biting, slashing, pure animal instinct. 'I'm gonna tear his bones apart.'"
    },
    Path.CHARLES_ELITE: {
        "name": "🎭 INFINITE ELITE: Chairman's Authority",
        "cost": 145,
        "dmg": (290, 390),
        "desc": "Charles Choi's invisible attacks. The Vice Leader of Gapryong's Fist shows why he's the puppet master."
    },
    Path.JINYOUNG_COPY: {
        "name": "🔄 INFINITE COPY: Medical Genius",
        "cost": 135,
        "dmg": (270, 370),
        "desc": "Jinyoung Park's perfect copy ability. Any technique seen once can be replicated instantly."
    },
    Path.BAEKHO_BEAST: {
        "name": "🐯 INFINITE BEAST: White Tiger's Wrath",
        "cost": 130,
        "dmg": (260, 360),
        "desc": "Baekho's beast mode unleashed. The White Tiger shows why he's a Gen 0 legend."
    },

    # 1ST GENERATION KINGS
    Path.JAMES_LEE_INVISIBLE: {
        "name": "👑 INFINITE JAMES: Legend of the 1st Gen",
        "cost": 150,
        "dmg": (300, 420),
        "desc": "James Lee's perfected invisible attacks. The man who single-handedly dismantled the 1st Generation."
    },
    Path.GITAE_KIM: {
        "name": "⚡ INFINITE GITAE: Gapryong's Shadow",
        "cost": 145,
        "dmg": (290, 400),
        "desc": "Gitae Kim inherits his father's power. The King of Seoul's unknown technique."
    },
    Path.JICHANG_HAND_BLADE: {
        "name": "🩷 INFINITE HAND BLADE: King's Edge",
        "cost": 135,
        "dmg": (270, 380),
        "desc": "Jichang Kwak's ultimate hand blade technique. Cuts through anything. Note: Ineffective against Jinrang."
    },
    Path.TAESOO_MA_FIST: {
        "name": "🔴 INFINITE RIGHT HAND: Ansan's Pride",
        "cost": 140,
        "dmg": (280, 400),
        "desc": "Taesoo Ma's right fist - no technique, just overwhelming power. The fist that ruled Ansan."
    },
    Path.GONGSEOB_IRON: {
        "name": "🔨 INFINITE IRON: The Monk's Fortress",
        "cost": 130,
        "dmg": (260, 360),
        "desc": "Gongseob Ji's iron boxing. Speed and durability combined into an unbreakable fighting style."
    },
    Path.SEOKDU_HEADBUTT: {
        "name": "💢 INFINITE HEADBUTT: Suwon's Crown",
        "cost": 125,
        "dmg": (250, 350),
        "desc": "Seokdu Wang's legendary headbutt. His forehead is harder than steel."
    },
    Path.JAEGYEON_SPEED: {
        "name": "🔵 INFINITE SPEED: Incheon Flash",
        "cost": 135,
        "dmg": (270, 370),
        "desc": "Jaegyeon Na's ultimate speed. He doesn't move - he simply arrives."
    },
    Path.SEONGJI_MONSTER: {
        "name": "🦍 INFINITE MONSTER: Cheonliang's King",
        "cost": 140,
        "dmg": (280, 390),
        "desc": "Seongji Yuk's mastery of Ssireum, Judo, and Kudo combined into a monstrous fighting style."
    },
    Path.JINRANG_CONVICTION: {
        "name": "👑 INFINITE DISCIPLE: True Conviction",
        "cost": 150,
        "dmg": (300, 420),
        "desc": "Jinrang's ultimate technique. As Gapryong's true disciple, his conviction is absolute."
    },

    # WORKERS
    Path.MANDEOK_POWER: {
        "name": "💪 INFINITE TITAN: Earth Shaker",
        "cost": 140,
        "dmg": (280, 400),
        "desc": "Mandeok's raw power unleashed. A single strike that can shake the earth itself."
    },
    Path.CAP_GUY_CQC: {
        "name": "🔫 INFINITE CQC: Code 66",
        "cost": 135,
        "dmg": (270, 380),
        "desc": "Cap Guy's ultimate CQC technique. Silver Yarn threads dance through the air, binding and cutting."
    },
    Path.XIAOLUNG_MUAY_THAI: {
        "name": "🇹🇭 INFINITE MUAY THAI: Death Blow",
        "cost": 130,
        "dmg": (260, 370),
        "desc": "Xiaolung's perfected Muay Thai. Elbows and knees become deadly weapons."
    },
    Path.RYUHEI_YAKUZA: {
        "name": "⚔️ INFINITE YAKUZA: Gang Lord",
        "cost": 125,
        "dmg": (250, 360),
        "desc": "Ryuhei's yakuza style at its peak. Dirty fighting, gang tactics, overwhelming aggression."
    },
    Path.SAMUEL_AMBITION: {
        "name": "👑 INFINITE AMBITION: King's Path",
        "cost": 135,
        "dmg": (270, 380),
        "desc": "Samuel Seo's ambition-fueled power. The betrayer's strength knows no limits."
    },
    Path.SINU_INVISIBLE: {
        "name": "🌀 INFINITE INVISIBLE: Ghost Fist",
        "cost": 130,
        "dmg": (260, 370),
        "desc": "Sinu Han's invisible attacks - a hybrid of hand and leg techniques. Unseeable, unavoidable."
    },
    Path.LOGAN_BULLY: {
        "name": "👊 INFINITE BULLY: Cheap Shot",
        "cost": 100,
        "dmg": (200, 300),
        "desc": "Logan Lee's ultimate cheap shot. When you least expect it, he strikes."
    },

    # CHEONLIANG
    Path.VIN_JIN_SSIREUM: {
        "name": "🇰🇷 INFINITE SSIREUM: Wrestling God",
        "cost": 130,
        "dmg": (260, 370),
        "desc": "Vin Jin's perfected ssireum technique. Throws and grapples that break bones."
    },
    Path.SEONGJI_MARTIAL: {
        "name": "🥋 INFINITE MARTIAL: Triple Threat",
        "cost": 140,
        "dmg": (280, 390),
        "desc": "Seongji Yuk's combination of ssireum, judo, and kudo. A complete martial artist."
    },
    Path.HAN_JAEHA: {
        "name": "🤼 INFINITE TRADITION: Cheonliang Wrestling",
        "cost": 115,
        "dmg": (230, 330),
        "desc": "Han Jaeha's traditional ssireum technique. Pure Korean wrestling at its finest."
    },
    Path.BAEK_SEONG_TAEKKYON: {
        "name": "🦢 INFINITE FLOW: Taekkyon Dance",
        "cost": 120,
        "dmg": (240, 340),
        "desc": "Baek Seong's flowing taekkyon. Dance-like movements that confuse and destroy."
    },

    # YAMAZAKI
    Path.SHINGEN_YAMAZAKI: {
        "name": "🏯 INFINITE YAMAZAKI: Syndicate's Wrath",
        "cost": 160,
        "dmg": (320, 450),
        "desc": "Shingen Yamazaki's ultimate technique. The head of the Yamazaki Syndicate shows why they were feared."
    },
    Path.PARK_FATHER: {
        "name": "❓ INFINITE MYSTERY: Bloodline Secret",
        "cost": 140,
        "dmg": (280, 400),
        "desc": "Park Jonggun's father's mysterious technique. The source of Gun's power remains unknown."
    },

    # LAW ENFORCEMENT
    Path.KIM_MINJAE_JUDO: {
        "name": "🥋 INFINITE JUDO: Police Force",
        "cost": 110,
        "dmg": (220, 320),
        "desc": "Kim Minjae's perfected judo throws. Law and order brought to the streets."
    },
    Path.DETECTIVE_KANG_BOXING: {
        "name": "🥊 INFINITE DETECTIVE: Veteran's Fist",
        "cost": 115,
        "dmg": (230, 330),
        "desc": "Detective Kang's veteran boxing. Years of experience packed into every punch."
    }
}


# ============================================================================
# GEN 0 LEGENDS
# ============================================================================

class GapryongKim(Character):
    def __init__(self):
        super().__init__(
            "Gapryong Kim",
            "The Strongest of Gen 0",
            900, 400,
            [Realm.SPEED, Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE, Realm.OVERCOMING]
        )
        self.canon_episode = 0
        self.paths_available = [Path.GAPRYONG_CONVICTION]

        self.abilities['1'] = {"name": "👑 Conviction Punch", "cost": 30, "dmg": (100, 150), "type": "damage"}
        self.abilities['2'] = {"name": "👑 Gapryong's Fist", "cost": 40, "dmg": (130, 180), "type": "damage"}
        self.abilities['3'] = {"name": "👑 Will to Protect", "cost": 35, "dmg": (110, 160), "type": "damage"}
        self.abilities['4'] = {"name": "👑 Legend's Legacy", "cost": 50, "dmg": (150, 200), "type": "damage"}
        self.abilities['5'] = {"name": "🛡️ Gapryong's Defense", "cost": 25, "dmg": (0, 0), "type": "utility"}


class TomLee(Character):
    def __init__(self):
        super().__init__(
            "Tom Lee",
            "The Wild",
            850, 380,
            [Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE]
        )
        self.canon_episode = 0
        self.paths_available = [Path.TOM_LEE_WILD]

        self.abilities['1'] = {"name": "🐅 Wild Strike", "cost": 25, "dmg": (90, 140), "type": "damage"}
        self.abilities['2'] = {"name": "🐅 Tom Lee Special", "cost": 35, "dmg": (120, 170), "type": "damage"}
        self.abilities['3'] = {"name": "🐅 Gen 0 Power", "cost": 40, "dmg": (140, 190), "type": "damage"}
        self.abilities['4'] = {"name": "🐅 Bite Force", "cost": 30, "dmg": (100, 150), "type": "damage"}


class CharlesChoi(Character):
    def __init__(self):
        super().__init__(
            "Charles Choi",
            "The Puppet Master",
            800, 360,
            [Realm.TECHNIQUE, Realm.SPEED]
        )
        self.canon_episode = 0
        self.paths_available = [Path.CHARLES_ELITE]

        self.abilities['1'] = {"name": "🎭 Invisible Strike", "cost": 30, "dmg": (90, 140), "type": "damage"}
        self.abilities['2'] = {"name": "🎭 Chairman's Authority", "cost": 40, "dmg": (120, 170), "type": "damage"}
        self.abilities['3'] = {"name": "🎭 Elite Technique", "cost": 35, "dmg": (110, 160), "type": "damage"}
        self.abilities['4'] = {"name": "🎭 Truth of Two Bodies", "cost": 50, "dmg": (150, 200), "type": "damage"}


class JinyoungPark(Character):
    def __init__(self):
        super().__init__(
            "Jinyoung Park",
            "The Medical Genius",
            780, 350,
            [Realm.TECHNIQUE]
        )
        self.canon_episode = 0
        self.paths_available = [Path.JINYOUNG_COPY]

        self.abilities['1'] = {"name": "🔄 Copy: Taekwondo", "cost": 25, "dmg": (80, 130), "type": "damage"}
        self.abilities['2'] = {"name": "🔄 Copy: Karate", "cost": 25, "dmg": (80, 130), "type": "damage"}
        self.abilities['3'] = {"name": "🔄 Copy: Boxing", "cost": 25, "dmg": (80, 130), "type": "damage"}
        self.abilities['4'] = {"name": "🔄 Medical Precision", "cost": 30, "dmg": (100, 150), "type": "damage"}


class Baekho(Character):
    def __init__(self):
        super().__init__(
            "Baekho",
            "The White Tiger",
            820, 370,
            [Realm.STRENGTH, Realm.TENACITY]
        )
        self.canon_episode = 0
        self.paths_available = [Path.BAEKHO_BEAST]

        self.abilities['1'] = {"name": "🐯 Tiger Strike", "cost": 30, "dmg": (100, 150), "type": "damage"}
        self.abilities['2'] = {"name": "🐯 Beast Mode", "cost": 40, "dmg": (130, 180), "type": "damage"}
        self.abilities['3'] = {"name": "🐯 White Tiger's Claw", "cost": 35, "dmg": (120, 170), "type": "damage"}


# ============================================================================
# 1ST GENERATION KINGS
# ============================================================================

class JamesLee(Character):
    def __init__(self):
        super().__init__(
            "James Lee",
            "Legend of 1st Gen",
            880, 390,
            [Realm.SPEED, Realm.TECHNIQUE]
        )
        self.canon_episode = 0
        self.paths_available = [Path.JAMES_LEE_INVISIBLE]

        self.abilities['1'] = {"name": "👑 Invisible Kick", "cost": 35, "dmg": (120, 170), "type": "damage"}
        self.abilities['2'] = {"name": "👑 Perfect Form", "cost": 40, "dmg": (140, 190), "type": "damage"}
        self.abilities['3'] = {"name": "👑 One Man Circle", "cost": 50, "dmg": (170, 220), "type": "damage"}
        self.abilities['4'] = {"name": "👑 Legend's Speed", "cost": 30, "dmg": (0, 0), "type": "buff"}


class GitaeKim(Character):
    def __init__(self):
        super().__init__(
            "Gitae Kim",
            "King of Seoul",
            860, 380,
            [Realm.STRENGTH, Realm.OVERCOMING]
        )
        self.canon_episode = 0
        self.paths_available = [Path.GITAE_KIM]

        self.abilities['1'] = {"name": "⚡ Gapryong's Blood", "cost": 35, "dmg": (120, 170), "type": "damage"}
        self.abilities['2'] = {"name": "⚡ Inherited Power", "cost": 40, "dmg": (140, 190), "type": "damage"}
        self.abilities['3'] = {"name": "⚡ King's Authority", "cost": 30, "dmg": (100, 150), "type": "damage"}


class JichangKwak(Character):
    def __init__(self):
        super().__init__(
            "Jichang Kwak",
            "King of Seoul",
            800, 360,
            [Realm.SPEED, Realm.STRENGTH]
        )
        self.canon_episode = 0
        self.paths_available = [Path.JICHANG_HAND_BLADE]

        self.abilities['1'] = {"name": "🩷 Hand Blade", "cost": 30, "dmg": (100, 150), "type": "damage"}
        self.abilities['2'] = {"name": "🩷 Double Edge", "cost": 35, "dmg": (120, 170), "type": "damage"}
        self.abilities['3'] = {"name": "🩷 Seoul King's Pride", "cost": 40, "dmg": (140, 190), "type": "damage"}
        self.special = "CANNOT DAMAGE JINRANG"


class TaesooMa(Character):
    def __init__(self):
        super().__init__(
            "Taesoo Ma",
            "King of Ansan",
            820, 350,
            [Realm.STRENGTH]
        )
        self.canon_episode = 0
        self.paths_available = [Path.TAESOO_MA_FIST]

        self.abilities['1'] = {"name": "🔴 Right Hand", "cost": 35, "dmg": (130, 180), "type": "damage"}
        self.abilities['2'] = {"name": "🔴 No Technique", "cost": 40, "dmg": (150, 200), "type": "damage"}
        self.abilities['3'] = {"name": "🔴 Ansan King", "cost": 30, "dmg": (110, 160), "type": "damage"}


class GongseobJi(Character):
    def __init__(self):
        super().__init__(
            "Gongseob Ji",
            "The Monk",
            750, 340,
            [Realm.TECHNIQUE]
        )
        self.canon_episode = 0
        self.paths_available = [Path.GONGSEOB_IRON]

        self.abilities['1'] = {"name": "🩷 Iron Boxing", "cost": 25, "dmg": (90, 140), "type": "damage"}
        self.abilities['2'] = {"name": "🩷 Speed Technique", "cost": 30, "dmg": (110, 160), "type": "damage"}
        self.abilities['3'] = {"name": "🩷 Tungsten Defense", "cost": 20, "dmg": (0, 0), "type": "utility"}


class SeokduWang(Character):
    def __init__(self):
        super().__init__(
            "Seokdu Wang",
            "King of Suwon",
            780, 330,
            [Realm.STRENGTH, Realm.TENACITY]
        )
        self.canon_episode = 0
        self.paths_available = [Path.SEOKDU_HEADBUTT]

        self.abilities['1'] = {"name": "💢 Headbutt", "cost": 30, "dmg": (120, 170), "type": "damage"}
        self.abilities['2'] = {"name": "💢 Iron Forehead", "cost": 25, "dmg": (100, 150), "type": "damage"}
        self.abilities['3'] = {"name": "💢 Suwon's Crown", "cost": 35, "dmg": (140, 190), "type": "damage"}


class JaegyeonNa(Character):
    def __init__(self):
        super().__init__(
            "Jaegyeon Na",
            "King of Incheon",
            770, 360,
            [Realm.SPEED]
        )
        self.canon_episode = 544
        self.paths_available = [Path.JAEGYEON_SPEED]

        self.abilities['1'] = {"name": "🔵 Incheon Speed", "cost": 30, "dmg": (100, 150), "type": "damage"}
        self.abilities['2'] = {"name": "🔵 Faster Than Light", "cost": 40, "dmg": (140, 190), "type": "damage"}
        self.abilities['3'] = {"name": "🔵 King of Incheon", "cost": 35, "dmg": (120, 170), "type": "damage"}


class SeongjiYuk(Character):
    def __init__(self):
        super().__init__(
            "Seongji Yuk",
            "The Monster of Cheonliang",
            820, 370,
            [Realm.STRENGTH, Realm.TECHNIQUE, Realm.OVERCOMING]
        )
        self.canon_episode = 500
        self.paths_available = [Path.SEONGJI_MONSTER, Path.SEONGJI_MARTIAL]

        self.abilities['1'] = {"name": "🇰🇷 Ssireum: Throw", "cost": 25, "dmg": (90, 140), "type": "damage"}
        self.abilities['2'] = {"name": "🥋 Judo: Ippon", "cost": 30, "dmg": (110, 160), "type": "damage"}
        self.abilities['3'] = {"name": "🥋 Kudo: Dirty Boxing", "cost": 30, "dmg": (110, 160), "type": "damage"}
        self.abilities['4'] = {"name": "🦍 Monster Mode", "cost": 45, "dmg": (160, 210), "type": "damage"}


class Jinrang(Character):
    def __init__(self):
        super().__init__(
            "Jinrang",
            "King of Busan",
            830, 380,
            [Realm.STRENGTH, Realm.OVERCOMING]
        )
        self.canon_episode = 580
        self.paths_available = [Path.JINRANG_CONVICTION]

        self.abilities['1'] = {"name": "👑 Jinrang's Conviction", "cost": 35, "dmg": (130, 180), "type": "damage"}
        self.abilities['2'] = {"name": "👑 Gapryong's Disciple", "cost": 40, "dmg": (150, 200), "type": "damage"}
        self.abilities['3'] = {"name": "👑 Busan King", "cost": 45, "dmg": (170, 220), "type": "damage"}
        self.abilities['4'] = {"name": "👑 True Conviction", "cost": 60, "dmg": (200, 250), "type": "damage"}
        self.special = "IMMUNE to Gapryong's Copy and Jichang's Hand Blade"


# ============================================================================
# WORKERS
# ============================================================================

class Mandeok(Character):
    def __init__(self):
        super().__init__(
            "Mandeok",
            "The Titan",
            780, 320,
            [Realm.STRENGTH]
        )
        self.canon_episode = 400
        self.paths_available = [Path.MANDEOK_POWER]

        self.abilities['1'] = {"name": "💪 Power Punch", "cost": 30, "dmg": (120, 170), "type": "damage"}
        self.abilities['2'] = {"name": "🌍 Earth Shaker", "cost": 35, "dmg": (140, 190), "type": "damage"}
        self.abilities['3'] = {"name": "🗿 Titan Strike", "cost": 40, "dmg": (160, 210), "type": "damage"}


class CapGuy(Character):
    def __init__(self):
        super().__init__(
            "Cap Guy",
            "The Senior Manager",
            750, 340,
            [Realm.TECHNIQUE, Realm.TENACITY]
        )
        self.canon_episode = 290
        self.paths_available = [Path.CAP_GUY_CQC]

        self.abilities['1'] = {"name": "🔫 CQC: Vital Strikes", "cost": 25, "dmg": (90, 140), "type": "damage"}
        self.abilities['2'] = {"name": "⚪ Silver Yarn: Thread Bind", "cost": 20, "dmg": (0, 0), "type": "utility"}
        self.abilities['3'] = {"name": "⚪ Silver Yarn: Thread Slash", "cost": 30, "dmg": (110, 160), "type": "damage"}
        self.abilities['4'] = {"name": "66 CODE: Full Release", "cost": 50, "dmg": (160, 210), "type": "damage"}


class Xiaolung(Character):
    def __init__(self):
        super().__init__(
            "Xiaolung",
            "Muay Thai Genius",
            720, 330,
            [Realm.SPEED, Realm.STRENGTH]
        )
        self.canon_episode = 400
        self.paths_available = [Path.XIAOLUNG_MUAY_THAI]

        self.abilities['1'] = {"name": "🇹🇭 Muay Thai: Elbow", "cost": 25, "dmg": (90, 140), "type": "damage"}
        self.abilities['2'] = {"name": "🇹🇭 Muay Thai: Knee", "cost": 25, "dmg": (90, 140), "type": "damage"}
        self.abilities['3'] = {"name": "🇹🇭 Thai Clinch", "cost": 30, "dmg": (110, 160), "type": "damage"}
        self.abilities['4'] = {"name": "🇹🇭 Muay Thai Mastery", "cost": 40, "dmg": (150, 200), "type": "damage"}


class Ryuhei(Character):
    def __init__(self):
        super().__init__(
            "Ryuhei",
            "Yakuza Executive",
            700, 310,
            [Realm.TECHNIQUE]
        )
        self.canon_episode = 400
        self.paths_available = [Path.RYUHEI_YAKUZA]

        self.abilities['1'] = {"name": "⚔️ Yakuza Strike", "cost": 25, "dmg": (90, 140), "type": "damage"}
        self.abilities['2'] = {"name": "🏴 Gang Style", "cost": 30, "dmg": (110, 160), "type": "damage"}
        self.abilities['3'] = {"name": "⚫ Yamazaki Blood", "cost": 35, "dmg": (130, 180), "type": "damage"}


class SamuelSeo(Character):
    def __init__(self):
        super().__init__(
            "Samuel Seo",
            "The Betrayer",
            730, 330,
            [Realm.STRENGTH, Realm.TENACITY]
        )
        self.canon_episode = 300
        self.paths_available = [Path.SAMUEL_AMBITION]

        self.abilities['1'] = {"name": "👑 King's Ambition", "cost": 30, "dmg": (110, 160), "type": "damage"}
        self.abilities['2'] = {"name": "💢 Betrayal", "cost": 25, "dmg": (100, 150), "type": "damage"}
        self.abilities['3'] = {"name": "⚡ Workers Executive", "cost": 35, "dmg": (130, 180), "type": "damage"}
        self.abilities['4'] = {"name": "👑 Path to Kingship", "cost": 40, "dmg": (150, 200), "type": "damage"}


class SinuHan(Character):
    def __init__(self):
        super().__init__(
            "Sinu Han",
            "The Ghost",
            710, 340,
            [Realm.SPEED, Realm.TECHNIQUE]
        )
        self.canon_episode = 300
        self.paths_available = [Path.SINU_INVISIBLE]

        self.abilities['1'] = {"name": "🌀 Invisible Punch", "cost": 30, "dmg": (100, 150), "type": "damage"}
        self.abilities['2'] = {"name": "🌀 Invisible Kick", "cost": 30, "dmg": (100, 150), "type": "damage"}
        self.abilities['3'] = {"name": "🌀 Ghost Fist", "cost": 40, "dmg": (140, 190), "type": "damage"}


class LoganLee(Character):
    def __init__(self):
        super().__init__(
            "Logan Lee",
            "The Bully",
            550, 280,
            []
        )
        self.canon_episode = 1
        self.paths_available = [Path.LOGAN_BULLY]

        self.abilities['1'] = {"name": "👊 Bully Punch", "cost": 20, "dmg": (60, 110), "type": "damage"}
        self.abilities['2'] = {"name": "😤 Intimidation", "cost": 15, "dmg": (0, 0), "type": "utility"}
        self.abilities['3'] = {"name": "💢 Cheap Shot", "cost": 25, "dmg": (80, 130), "type": "damage"}


# ============================================================================
# CHEONLIANG
# ============================================================================

class VinJin(Character):
    def __init__(self):
        super().__init__(
            "Vin Jin",
            "Ssireum Genius",
            680, 310,
            [Realm.STRENGTH]
        )
        self.canon_episode = 500
        self.paths_available = [Path.VIN_JIN_SSIREUM]

        self.abilities['1'] = {"name": "🇰🇷 Ssireum: Throw", "cost": 25, "dmg": (90, 140), "type": "damage"}
        self.abilities['2'] = {"name": "🇰🇷 Ssireum: Grapple", "cost": 25, "dmg": (90, 140), "type": "damage"}
        self.abilities['3'] = {"name": "🥋 Judo: Ippon", "cost": 30, "dmg": (110, 160), "type": "damage"}
        self.abilities['4'] = {"name": "🥋 Kudo: Dirty Boxing", "cost": 30, "dmg": (110, 160), "type": "damage"}
        self.abilities['5'] = {"name": "🕶️ Sunglasses Off", "cost": 40, "dmg": (150, 200), "type": "damage"}


class HanJaeha(Character):
    def __init__(self):
        super().__init__(
            "Han Jaeha",
            "Cheonliang Wrestler",
            600, 290,
            [Realm.STRENGTH]
        )
        self.canon_episode = 500
        self.paths_available = [Path.HAN_JAEHA]

        self.abilities['1'] = {"name": "🤼 Traditional Throw", "cost": 20, "dmg": (70, 120), "type": "damage"}
        self.abilities['2'] = {"name": "🤼 Grapple Lock", "cost": 25, "dmg": (80, 130), "type": "damage"}
        self.abilities['3'] = {"name": "🤼 Cheonliang Pride", "cost": 30, "dmg": (100, 150), "type": "damage"}


class BaekSeong(Character):
    def __init__(self):
        super().__init__(
            "Baek Seong",
            "Taekkyon Dancer",
            590, 300,
            [Realm.SPEED, Realm.TECHNIQUE]
        )
        self.canon_episode = 500
        self.paths_available = [Path.BAEK_SEONG_TAEKKYON]

        self.abilities['1'] = {"name": "🦢 Flowing Step", "cost": 20, "dmg": (60, 110), "type": "damage"}
        self.abilities['2'] = {"name": "🦢 Taekkyon Kick", "cost": 25, "dmg": (80, 130), "type": "damage"}
        self.abilities['3'] = {"name": "🦢 Dance of Blades", "cost": 35, "dmg": (120, 170), "type": "damage"}


# ============================================================================
# YAMAZAKI
# ============================================================================

class ShingenYamazaki(Character):
    def __init__(self):
        super().__init__(
            "Shingen Yamazaki",
            "Yamazaki Head",
            950, 420,
            [Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE, Realm.OVERCOMING]
        )
        self.canon_episode = 0
        self.paths_available = [Path.SHINGEN_YAMAZAKI]

        self.abilities['1'] = {"name": "🏯 Yamazaki Style", "cost": 40, "dmg": (150, 200), "type": "damage"}
        self.abilities['2'] = {"name": "🏯 Syndicate's Wrath", "cost": 50, "dmg": (180, 230), "type": "damage"}
        self.abilities['3'] = {"name": "🏯 Black Bone", "cost": 60, "dmg": (210, 270), "type": "damage"}
        self.abilities['4'] = {"name": "🏯 Inherited Darkness", "cost": 70, "dmg": (250, 320), "type": "damage"}


class ParkFather(Character):
    def __init__(self):
        super().__init__(
            "Park Jonggun's Father",
            "The Mystery",
            800, 380,
            [Realm.STRENGTH, Realm.TECHNIQUE]
        )
        self.canon_episode = 0
        self.paths_available = [Path.PARK_FATHER]

        self.abilities['1'] = {"name": "❓ Unknown Technique", "cost": 35, "dmg": (130, 180), "type": "damage"}
        self.abilities['2'] = {"name": "❓ Bloodline Secret", "cost": 45, "dmg": (160, 210), "type": "damage"}
        self.abilities['3'] = {"name": "❓ Father's Shadow", "cost": 50, "dmg": (180, 230), "type": "damage"}


# ============================================================================
# LAW ENFORCEMENT
# ============================================================================

class KimMinjae(Character):
    def __init__(self):
        super().__init__(
            "Kim Minjae",
            "Police Officer",
            550, 280,
            [Realm.TECHNIQUE]
        )
        self.canon_episode = 200
        self.paths_available = [Path.KIM_MINJAE_JUDO]

        self.abilities['1'] = {"name": "🥋 Judo Throw", "cost": 20, "dmg": (60, 110), "type": "damage"}
        self.abilities['2'] = {"name": "🥋 Ippon Seoi Nage", "cost": 25, "dmg": (80, 130), "type": "damage"}
        self.abilities['3'] = {"name": "🥋 Police Training", "cost": 30, "dmg": (100, 150), "type": "damage"}


class DetectiveKang(Character):
    def __init__(self):
        super().__init__(
            "Detective Kang",
            "Veteran Detective",
            570, 290,
            [Realm.SPEED]
        )
        self.canon_episode = 200
        self.paths_available = [Path.DETECTIVE_KANG_BOXING]

        self.abilities['1'] = {"name": "🥊 Detective's Jab", "cost": 20, "dmg": (60, 110), "type": "damage"}
        self.abilities['2'] = {"name": "🥊 Veteran Cross", "cost": 25, "dmg": (80, 130), "type": "damage"}
        self.abilities['3'] = {"name": "🥊 Experience Counts", "cost": 30, "dmg": (100, 150), "type": "damage"}


# ============================================================================
# EXISTING CHARACTERS
# ============================================================================

class DanielPark(Character):
    def __init__(self, episode_state="current"):
        super().__init__(
            "Daniel Park",
            "The Second Body",
            420, 300,
            [Realm.SPEED, Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE, Realm.OVERCOMING]
        )
        self.episode_state = episode_state
        self.canon_episode = 581
        self.ui_mode = False
        self.ui_timer = 0
        self.sophia_trained = True
        self.jichang_copied = True
        self.gapryong_copied = True
        self.form = "Normal"
        self.switch_available = True
        self.paths_available = [Path.DANIEL_UI, Path.DANIEL_COPY]

        self.abilities['1'] = {"name": "👊 Desperate Flailing", "cost": 10, "dmg": (20, 35), "type": "damage"}
        self.abilities['2'] = {"name": "🔄 Instinctive Copy", "cost": 20, "dmg": (30, 50), "type": "damage"}
        self.abilities['3'] = {"name": "🇷🇺 Systema: Ryabina", "cost": 25, "dmg": (50, 70), "type": "damage"}
        self.abilities['4'] = {"name": "⚡ Copy: Zack's Counter", "cost": 25, "dmg": (55, 80), "type": "damage"}
        self.abilities['5'] = {"name": "⚡ Copy: Vasco's Sunken Fist", "cost": 30, "dmg": (65, 90), "type": "damage"}
        self.abilities['6'] = {"name": "⚡ Copy: Eli's Animal Instinct", "cost": 30, "dmg": (70, 95), "type": "damage"}
        self.abilities['7'] = {"name": "⚡ Copy: Jake's Conviction", "cost": 35, "dmg": (75, 105), "type": "damage"}
        self.abilities['8'] = {"name": "⚡ Copy: Johan's Choreography", "cost": 40, "dmg": (80, 115), "type": "damage"}
        self.abilities['9'] = {"name": "⚡ Copy: Gun's Taekwondo", "cost": 35, "dmg": (80, 110), "type": "damage"}
        self.abilities['10'] = {"name": "🩷 Jichang's Hand Blade", "cost": 45, "dmg": (90, 130), "type": "damage"}
        self.abilities['11'] = {"name": "👑 Gapryong's Conviction", "cost": 60, "dmg": (120, 180), "type": "damage"}
        self.abilities['12'] = {"name": "👁️ Ultra Instinct", "cost": 100, "dmg": (0, 0), "type": "ui"}

    def activate_ui(self):
        self.ui_mode = True
        self.ui_timer = 3
        self.form = "ULTRA INSTINCT"
        self.hp = min(self.max_hp, self.hp + 50)
        return "👁️👁️👁️👁️👁️ ULTRA INSTINCT! White hair awakens!"

    def get_damage_multiplier(self):
        mult = 1.0
        buffs = []
        if self.active_realm == Realm.STRENGTH:
            mult *= 1.7
            buffs.append("🔴 STRENGTH")
        if self.ui_mode:
            mult *= 2.5
            buffs.append("👁️ ULTRA INSTINCT")
        return mult, buffs


class ZackLee(Character):
    def __init__(self):
        super().__init__("Zack Lee", "The Iron Boxer", 380, 280, [Realm.SPEED])
        self.canon_episode = 1
        self.paths_available = [Path.ZACK_IRON]
        self.heat_mode = False
        self.abilities['1'] = {"name": "🔨 Iron Fortress Stance", "cost": 15, "dmg": (0, 0), "type": "buff"}
        self.abilities['2'] = {"name": "🔨 Iron Fist", "cost": 20, "dmg": (50, 75), "type": "damage"}
        self.abilities['3'] = {"name": "🥊 Jab", "cost": 15, "dmg": (35, 55), "type": "damage"}
        self.abilities['4'] = {"name": "🥊 Cross", "cost": 20, "dmg": (45, 70), "type": "damage"}
        self.abilities['5'] = {"name": "⚡ Counter Punch", "cost": 30, "dmg": (75, 110), "type": "damage"}
        self.abilities['6'] = {"name": "💫 Shining Star", "cost": 50, "dmg": (100, 150), "type": "damage"}


class JohanSeong(Character):
    def __init__(self, blind=True):
        super().__init__("Johan Seong", "The God Eye", 400, 300, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 100
        self.blind = blind
        self.paths_available = [Path.JOHAN_GOD_EYE, Path.JOHAN_CHOREOGRAPHY]
        self.abilities['1'] = {"name": "👁️ Copy: Taekwondo", "cost": 20, "dmg": (50, 75), "type": "damage"}
        self.abilities['2'] = {"name": "👁️ Copy: Boxing", "cost": 20, "dmg": (50, 75), "type": "damage"}
        self.abilities['3'] = {"name": "💃 Choreography", "cost": 40, "dmg": (85, 120), "type": "damage"}
        self.abilities['4'] = {"name": "👁️ God Eye", "cost": 45, "dmg": (0, 0), "type": "buff"}
        if blind:
            self.abilities['5'] = {"name": "🕶️ Blindness", "cost": 0, "dmg": (0, 0), "type": "passive"}


class Vasco(Character):
    def __init__(self):
        super().__init__("Vasco", "The Hero of Justice", 450, 260, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 1
        self.paths_available = [Path.VASCO_SYSTEMA, Path.VASCO_MUAY_THAI]
        self.abilities['1'] = {"name": "🇷🇺 Systema: Ryabina", "cost": 20, "dmg": (50, 70), "type": "damage"}
        self.abilities['2'] = {"name": "🇷🇺 Russian Cross", "cost": 35, "dmg": (75, 105), "type": "damage"}
        self.abilities['3'] = {"name": "🇹🇭 Muay Thai: Death Blow", "cost": 40, "dmg": (90, 130), "type": "damage"}
        self.abilities['4'] = {"name": "👊 Sunken Fist", "cost": 30, "dmg": (70, 100), "type": "damage"}


class JayHong(Character):
    def __init__(self):
        super().__init__("Jay Hong", "The Silent Blade", 380, 270, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 1
        self.paths_available = [Path.JAY_KALI]
        self.abilities['1'] = {"name": "🇷🇺 Systema: Neutralizer", "cost": 20, "dmg": (45, 65), "type": "damage"}
        self.abilities['2'] = {"name": "🇵🇭 Kali: Double Baston", "cost": 25, "dmg": (50, 75), "type": "damage"}
        self.abilities['3'] = {"name": "🇵🇭 Kali: Karambit", "cost": 30, "dmg": (65, 90), "type": "damage"}
        self.abilities['4'] = {"name": "🛡️ Motorcycle Helmet", "cost": 15, "dmg": (0, 0), "type": "utility"}


class EliJang(Character):
    def __init__(self):
        super().__init__("Eli Jang", "The Wild", 410, 260, [Realm.TECHNIQUE])
        self.canon_episode = 150
        self.paths_available = [Path.ELI_BEAST, Path.ELI_TOM_LEE]
        self.beast_mode = False
        self.abilities['1'] = {"name": "🐺 Wolf Strike", "cost": 20, "dmg": (50, 75), "type": "damage"}
        self.abilities['2'] = {"name": "🦅 Talon Kick", "cost": 25, "dmg": (60, 85), "type": "damage"}
        self.abilities['3'] = {"name": "🦁 Beast Mode", "cost": 45, "dmg": (0, 0), "type": "buff"}
        self.abilities['4'] = {"name": "👴 Tom Lee Special", "cost": 40, "dmg": (85, 125), "type": "damage"}

    def activate_beast_mode(self):
        self.beast_mode = True
        self.beast_timer = 3
        return "🦁🦁🦁 BEAST MODE! +60% damage!"


class WarrenChae(Character):
    def __init__(self):
        super().__init__("Warren Chae", "Gangdong's Mighty", 390, 260, [Realm.STRENGTH])
        self.canon_episode = 277
        self.paths_available = [Path.WARREN_JKD, Path.WARREN_CQC, Path.WARREN_HEART]
        self.exhausted = False
        self.abilities['1'] = {"name": "🥋 Jeet Kune Do: Interception", "cost": 20, "dmg": (55, 80), "type": "damage"}
        self.abilities['2'] = {"name": "🔫 CQC Foundation", "cost": 30, "dmg": (70, 100), "type": "damage"}
        self.abilities['3'] = {"name": "⚡ NEW CQC: Full Release", "cost": 70, "dmg": (120, 170), "type": "damage"}
        self.abilities['4'] = {"name": "💔 Heart Attack Punch", "cost": 60, "dmg": (110, 160), "type": "damage"}


class JakeKim(Character):
    def __init__(self):
        super().__init__("Jake Kim", "The Conviction", 430, 270, [Realm.OVERCOMING])
        self.canon_episode = 200
        self.paths_available = [Path.JAKE_CONVICTION, Path.JAKE_GAPRYONG]
        self.abilities['1'] = {"name": "⚖️ Conviction Punch", "cost": 25, "dmg": (60, 85), "type": "damage"}
        self.abilities['2'] = {"name": "👑 Inherited Will", "cost": 50, "dmg": (95, 140), "type": "damage"}
        self.abilities['3'] = {"name": "👑 Gapryong's Blood", "cost": 70, "dmg": (120, 180), "type": "damage"}
        self.abilities['4'] = {"name": "⚖️ Conviction Mode", "cost": 45, "dmg": (0, 0), "type": "realm"}


class GunPark(Character):
    def __init__(self):
        super().__init__("Gun Park", "Legend of Gen 1", 500, 320,
                         [Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE])
        self.canon_episode = 300
        self.paths_available = [Path.GUN_YAMAZAKI, Path.GUN_CONSTANT_UI]
        self.permanent_ui = True
        self.abilities['1'] = {"name": "🥋 Taekwondo: Roundhouse", "cost": 20, "dmg": (65, 90), "type": "damage"}
        self.abilities['2'] = {"name": "🥋 Kyokushin: Straight", "cost": 25, "dmg": (70, 100), "type": "damage"}
        self.abilities['3'] = {"name": "🖤 Black Bone", "cost": 70, "dmg": (130, 200), "type": "damage"}
        self.abilities['4'] = {"name": "👁️ Constant UI", "cost": 0, "dmg": (0, 0), "type": "passive"}


class GooKim(Character):
    def __init__(self):
        super().__init__("Goo Kim", "The Moonlight Sword", 480, 300, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 300
        self.paths_available = [Path.GOO_MOONLIGHT, Path.GOO_FIFTH]
        self.abilities['1'] = {"name": "🖊️ Pen Sword", "cost": 15, "dmg": (45, 70), "type": "damage"}
        self.abilities['2'] = {"name": "🌙 First Sword: Early Moon", "cost": 30, "dmg": (75, 105), "type": "damage"}
        self.abilities['3'] = {"name": "🌓 Second Sword: Crescent Moon", "cost": 35, "dmg": (80, 115), "type": "damage"}
        self.abilities['4'] = {"name": "🌕 Third Sword: Full Moon", "cost": 45, "dmg": (100, 145), "type": "damage"}
        self.abilities['5'] = {"name": "🌑 Zero Sword: Lunar Eclipse", "cost": 60, "dmg": (130, 190), "type": "counter"}
        self.abilities['6'] = {"name": "✨ Fifth Sword", "cost": 90, "dmg": (170, 250), "type": "damage"}


class KimJungu(Character):
    def __init__(self):
        super().__init__("Kim Jun-gu", "The Hwarang Sword", 520, 290, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 500
        self.paths_available = [Path.JOONGOO_HWARANG, Path.JOONGOO_ARMED]
        self.abilities['1'] = {"name": "🖊️ Pen Pierce", "cost": 25, "dmg": (70, 100), "type": "damage"}
        self.abilities['2'] = {"name": "🔗 Chain Whip", "cost": 30, "dmg": (75, 110), "type": "damage"}
        self.abilities['3'] = {"name": "⚔️ Hwarang Sword", "cost": 60, "dmg": (140, 210), "type": "damage"}
        self.abilities['4'] = {"name": "⚔️ Hwarang: Blade Dance", "cost": 70, "dmg": (160, 240), "type": "damage"}


class ManagerKim(Character):
    def __init__(self):
        super().__init__("Manager Kim", "The Senior Manager", 480, 300,
                         [Realm.TECHNIQUE, Realm.TENACITY, Realm.STRENGTH])
        self.canon_episode = 290
        self.code_66 = True
        self.veinous_rage = False
        self.silver_yarn_active = False
        self.paths_available = [Path.CAP_GUY_CQC]
        self.abilities['1'] = {"name": "🎖️ Special Forces Training", "cost": 0, "dmg": (0, 0), "type": "passive"}
        self.abilities['2'] = {"name": "🔫 CQC: Vital Strikes", "cost": 25, "dmg": (65, 90), "type": "damage"}
        self.abilities['3'] = {"name": "⚪ Silver Yarn: Thread Bind", "cost": 20, "dmg": (0, 0), "type": "utility"}
        self.abilities['4'] = {"name": "66 CODE: Full Release", "cost": 70, "dmg": (130, 190), "type": "damage"}


# ============================================================================
# ENEMY CLASS
# ============================================================================

class Enemy(Character):
    def __init__(self, name, title, hp, energy, abilities, rank, affiliation="", realm_list=None):
        super().__init__(name, title, hp, energy, realm_list)
        self.abilities = abilities
        self.rank = rank
        self.affiliation = affiliation
        self.ai_pattern = []


# ============================================================================
# MISSING ENEMY CREATION FUNCTIONS
# ============================================================================

def create_enemy_sally():
    abilities = {
        '1': {"name": "Sally Special", "dmg": (45, 70)},
        '2': {"name": "Family Support", "dmg": (40, 65)}
    }
    enemy = Enemy("Sally", "Hostel Manager", 320, 200, abilities, 60, "Hostel")
    enemy.ai_pattern = ['1', '2']
    return enemy


def create_enemy_brad():
    abilities = {
        '1': {"name": "Brad Punch", "dmg": (50, 75)},
        '2': {"name": "Big Deal Loyalty", "dmg": (55, 80)}
    }
    enemy = Enemy("Brad", "Big Deal Member", 350, 220, abilities, 55, "Big Deal")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_jace_park():
    abilities = {
        '1': {"name": "Strategy", "dmg": (40, 60)},
        '2': {"name": "Tactical Strike", "dmg": (45, 70)}
    }
    enemy = Enemy("Jace Park", "Burn Knuckles Strategist", 330, 210, abilities, 58, "Burn Knuckles")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_burn_knuckles():
    abilities = {
        '1': {"name": "Burn Knuckle Punch", "dmg": (35, 55)},
        '2': {"name": "Justice Strike", "dmg": (40, 60)}
    }
    enemy = Enemy("Burn Knuckles Member", "Hero Wannabe", 280, 180, abilities, 70, "Burn Knuckles")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_eugene():
    abilities = {
        '1': {"name": "Corporate Strategy", "dmg": (30, 50)},
        '2': {"name": "Workers' Orders", "dmg": (35, 55)}
    }
    enemy = Enemy("Eugene", "Workers Executive", 300, 250, abilities, 65, "Workers")
    enemy.ai_pattern = ['2', '1']
    return enemy


# ============================================================================
# EXISTING ENEMY CREATION FUNCTIONS
# ============================================================================

def create_enemy_frame_soldier():
    abilities = {'1': {"name": "Fist Strike", "dmg": (25, 40)}}
    enemy = Enemy("Frame Soldier", "Elite Grunt", 150, 100, abilities, 100, "Frame")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_logan_lee():
    abilities = {
        '1': {"name": "Bully Punch", "dmg": (35, 55)},
        '2': {"name": "Intimidation", "dmg": (30, 50)},
        '3': {"name": "Cheap Shot", "dmg": (40, 65)}
    }
    enemy = Enemy("Logan Lee", "The Bully", 300, 180, abilities, 85, "Independent")
    enemy.ai_pattern = ['3', '1', '2']
    return enemy


def create_enemy_jhigh_bully():
    abilities = {'1': {"name": "School Punch", "dmg": (20, 35)}}
    enemy = Enemy("J High Bully", "School Thug", 100, 80, abilities, 120, "J High")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_zack_lee():
    abilities = {
        '1': {"name": "Jab", "dmg": (35, 55)},
        '2': {"name": "Cross", "dmg": (45, 70)},
        '3': {"name": "Counter", "dmg": (60, 85)}
    }
    enemy = Enemy("Zack Lee", "The Iron Boxer", 380, 280, abilities, 35, "J High")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_vasco_enemy():
    abilities = {
        '1': {"name": "Systema Strike", "dmg": (50, 70)},
        '2': {"name": "Sunken Fist", "dmg": (70, 100)},
        '3': {"name": "Run Over", "dmg": (65, 95)}
    }
    enemy = Enemy("Vasco", "The Hero", 450, 260, abilities, 30, "Burn Knuckles")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jay_hong_enemy():
    abilities = {
        '1': {"name": "Systema", "dmg": (45, 65)},
        '2': {"name": "Kali", "dmg": (50, 75)}
    }
    enemy = Enemy("Jay Hong", "The Silent", 380, 270, abilities, 40, "J High")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_johan_seong_enemy():
    abilities = {
        '1': {"name": "Copy: Taekwondo", "dmg": (50, 75)},
        '2': {"name": "Copy: Boxing", "dmg": (50, 75)},
        '3': {"name": "Choreography", "dmg": (85, 120)},
        '4': {"name": "God Eye", "dmg": (95, 140)}
    }
    enemy = Enemy("Johan Seong", "The God Eye", 400, 300, abilities, 15, "God Dog")
    enemy.ai_pattern = ['4', '3', '2', '1']
    return enemy


def create_enemy_eli_jang_enemy():
    abilities = {
        '1': {"name": "Animal Strike", "dmg": (50, 75)},
        '2': {"name": "Talon Kick", "dmg": (60, 85)},
        '3': {"name": "Beast Mode", "dmg": (85, 120)}
    }
    enemy = Enemy("Eli Jang", "The Wild", 410, 260, abilities, 16, "Hostel")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_warren_chae_enemy():
    abilities = {
        '1': {"name": "JKD: Interception", "dmg": (60, 85)},
        '2': {"name": "Shield Strike", "dmg": (65, 90)},
        '3': {"name": "Counter", "dmg": (70, 100)},
        '4': {"name": "NEW CQC", "dmg": (90, 130)}
    }
    enemy = Enemy("Warren Chae", "Hostel Executive", 390, 260, abilities, 30, "Hostel")
    enemy.ai_pattern = ['4', '3', '2', '1']
    return enemy


def create_enemy_jake_kim_enemy():
    abilities = {
        '1': {"name": "Conviction Punch", "dmg": (60, 85)},
        '2': {"name": "Inherited Will", "dmg": (95, 140)},
        '3': {"name": "Gapryong's Blood", "dmg": (120, 180)}
    }
    enemy = Enemy("Jake Kim", "The Conviction", 430, 270, abilities, 12, "Big Deal")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jerry_kwon():
    abilities = {
        '1': {"name": "Gift Punch", "dmg": (65, 95)},
        '2': {"name": "Rhino Charge", "dmg": (70, 105)},
        '3': {"name": "Loyalty to Jake", "dmg": (80, 115)}
    }
    enemy = Enemy("Jerry Kwon", "Big Deal Executive", 420, 250, abilities, 25, "Big Deal")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_god_dog_member():
    abilities = {'1': {"name": "Fist Strike", "dmg": (25, 40)}}
    enemy = Enemy("God Dog Member", "Crew Soldier", 140, 100, abilities, 100, "God Dog")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_god_dog_elite():
    abilities = {
        '1': {"name": "Power Strike", "dmg": (40, 60)},
        '2': {"name": "Crew Combo", "dmg": (45, 65)}
    }
    enemy = Enemy("God Dog Elite", "Crew Veteran", 200, 140, abilities, 75, "God Dog")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_hostel_member():
    abilities = {
        '1': {"name": "Street Fighting", "dmg": (35, 55)},
        '2': {"name": "Ambush", "dmg": (40, 60)}
    }
    enemy = Enemy("Hostel Member", "Family Crew", 170, 120, abilities, 80, "Hostel")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_big_deal_member():
    abilities = {
        '1': {"name": "Fist Strike", "dmg": (30, 50)},
        '2': {"name": "Loyalty", "dmg": (0, 0)}
    }
    enemy = Enemy("Big Deal Member", "Crew Soldier", 180, 130, abilities, 78, "Big Deal")
    enemy.ai_pattern = ['1', '2']
    return enemy


def create_enemy_workers_member():
    abilities = {'1': {"name": "Corporate Strike", "dmg": (35, 55)}}
    enemy = Enemy("Workers Member", "Corporate Soldier", 160, 110, abilities, 90, "Workers")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_workers_affiliate():
    abilities = {
        '1': {"name": "Affiliate Technique", "dmg": (60, 85)},
        '2': {"name": "Corporate Power", "dmg": (65, 95)}
    }
    enemy = Enemy("Workers Affiliate", "1st Affiliate", 360, 230, abilities, 42, "Workers")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_xiaolung():
    abilities = {
        '1': {"name": "🇹🇭 Muay Thai: Elbow", "dmg": (80, 120)},
        '2': {"name": "🇹🇭 Muay Thai: Knee", "dmg": (85, 125)},
        '3': {"name": "🇹🇭 Thai Clinch", "dmg": (75, 110)},
        '4': {"name": "🇹🇭 Muay Thai Mastery", "dmg": (110, 170)}
    }
    enemy = Enemy("Xiaolung", "Muay Thai Genius", 550, 300, abilities, 14, "Workers")
    enemy.ai_pattern = ['4', '1', '2', '3']
    return enemy


def create_enemy_mandeok():
    abilities = {
        '1': {"name": "💪 Power Punch", "dmg": (90, 130)},
        '2': {"name": "🌍 Earth Shaker", "dmg": (100, 150)},
        '3': {"name": "🗿 Titan Strike", "dmg": (120, 180)}
    }
    enemy = Enemy("Mandeok", "The Titan", 600, 280, abilities, 13, "Workers")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_vin_jin():
    abilities = {
        '1': {"name": "🇰🇷 Ssireum: Throw", "dmg": (75, 110)},
        '2': {"name": "🇰🇷 Ssireum: Grapple", "dmg": (70, 105)},
        '3': {"name": "🥋 Judo: Ippon", "dmg": (80, 115)},
        '4': {"name": "🥋 Kudo: Dirty Boxing", "dmg": (85, 120)},
        '5': {"name": "🕶️ Sunglasses Off", "dmg": (110, 160)}
    }
    enemy = Enemy("Vin Jin", "Ssireum Genius", 520, 280, abilities, 28, "Workers")
    enemy.ai_pattern = ['5', '4', '3', '2', '1']
    return enemy


def create_enemy_ryuhei():
    abilities = {
        '1': {"name": "⚔️ Yakuza Strike", "dmg": (80, 115)},
        '2': {"name": "🏴 Gang Style", "dmg": (85, 120)},
        '3': {"name": "⚫ Yamazaki Blood", "dmg": (100, 150)}
    }
    enemy = Enemy("Ryuhei", "Yakuza Executive", 540, 290, abilities, 24, "Workers")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_samuel_seo():
    abilities = {
        '1': {"name": "👑 King's Ambition", "dmg": (85, 125)},
        '2': {"name": "💢 Betrayal", "dmg": (80, 120)},
        '3': {"name": "⚡ Workers Executive", "dmg": (95, 140)},
        '4': {"name": "👑 Path to Kingship", "dmg": (110, 170)}
    }
    enemy = Enemy("Samuel Seo", "The Betrayer", 560, 300, abilities, 18, "Workers")
    enemy.ai_pattern = ['4', '3', '1', '2']
    return enemy


def create_enemy_taesoo_ma():
    abilities = {
        '1': {"name": "🔴 Right Hand", "dmg": (110, 170)},
        '2': {"name": "🔴 Ansan King", "dmg": (120, 180)}
    }
    enemy = Enemy("Taesoo Ma", "King of Ansan", 580, 300, abilities, 8, "1st Gen")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_gongseob_ji():
    abilities = {
        '1': {"name": "🩷 Speed Technique", "dmg": (95, 140)},
        '2': {"name": "🩷 Vice King", "dmg": (100, 150)}
    }
    enemy = Enemy("Gongseob Ji", "Vice King", 500, 280, abilities, 11, "1st Gen")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_jichang_kwak():
    abilities = {
        '1': {"name": "🩷 Hand Blade", "dmg": (100, 155)},
        '2': {"name": "👑 Seoul King", "dmg": (110, 170)}
    }
    enemy = Enemy("Jichang Kwak", "King of Seoul", 550, 300, abilities, 7, "1st Gen")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_gun_park_enemy():
    abilities = {
        '1': {"name": "Taekwondo", "dmg": (65, 90)},
        '2': {"name": "Kyokushin", "dmg": (70, 100)},
        '3': {"name": "Black Bone", "dmg": (130, 200)}
    }
    enemy = Enemy("Gun Park", "Legend of Gen 1", 500, 320, abilities, 5, "Independent")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_goo_kim_enemy():
    abilities = {
        '1': {"name": "Makeshift Sword", "dmg": (45, 70)},
        '2': {"name": "Full Moon", "dmg": (100, 145)},
        '3': {"name": "Fifth Sword", "dmg": (170, 250)}
    }
    enemy = Enemy("Goo Kim", "The Moonlight Sword", 480, 300, abilities, 5, "Independent")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_kim_jungu_enemy():
    abilities = {
        '1': {"name": "Improvised Weapon", "dmg": (70, 100)},
        '2': {"name": "Hwarang Sword", "dmg": (140, 210)},
        '3': {"name": "Blade Dance", "dmg": (160, 240)}
    }
    enemy = Enemy("Kim Jun-gu", "The Hwarang Sword", 520, 290, abilities, 4, "Independent")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_manager_kim_enemy():
    abilities = {
        '1': {"name": "CQC Strike", "dmg": (65, 90)},
        '2': {"name": "Silver Yarn", "dmg": (100, 140)},
        '3': {"name": "66 CODE", "dmg": (130, 190)}
    }
    enemy = Enemy("Manager Kim", "The Senior Manager", 480, 300, abilities, 5, "White Tiger")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jinrang_enemy():
    abilities = {
        '1': {"name": "Jinrang's Conviction", "dmg": (130, 190)},
        '2': {"name": "Busan King", "dmg": (140, 210)},
        '3': {"name": "True Conviction", "dmg": (170, 250)}
    }
    enemy = Enemy("Jinrang", "King of Busan", 750, 380, abilities, 2, "Busan")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jaegyeon_na_enemy():
    abilities = {
        '1': {"name": "Incheon Speed", "dmg": (100, 150)},
        '2': {"name": "Betrayal", "dmg": (95, 145)},
        '3': {"name": "Faster Than Light", "dmg": (150, 230)}
    }
    enemy = Enemy("Jaegyeon Na", "King of Incheon", 620, 350, abilities, 6, "Busan")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_charles_choi():
    abilities = {
        '1': {"name": "🎭 Puppet Master", "dmg": (90, 140)},
        '2': {"name": "🏛️ Chairman's Authority", "dmg": (110, 170)},
        '3': {"name": "👤 HNH Group", "dmg": (100, 160)},
        '4': {"name": "🎭 Truth of Two Bodies", "dmg": (130, 200)}
    }
    enemy = Enemy("Charles Choi", "The Puppet Master", 650, 350, abilities, 3, "HNH Chairman")
    enemy.ai_pattern = ['4', '3', '2', '1']
    return enemy


def create_enemy_tom_lee():
    abilities = {
        '1': {"name": "🐅 Wild Strike", "dmg": (100, 150)},
        '2': {"name": "🐅 Tom Lee Special", "dmg": (120, 180)},
        '3': {"name": "🐅 Gen 0 Power", "dmg": (140, 210)}
    }
    enemy = Enemy("Tom Lee", "The Wild", 650, 350, abilities, 5, "Gen 0")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_gapryong_kim():
    abilities = {
        '1': {"name": "👑 Conviction of the Strongest", "dmg": (120, 180)},
        '2': {"name": "👑 Gapryong's Fist", "dmg": (150, 220)},
        '3': {"name": "👑 Will to Protect", "dmg": (130, 200)},
        '4': {"name": "👑 Legend's Legacy", "dmg": (180, 280)}
    }
    enemy = Enemy("Gapryong Kim", "The Strongest", 800, 400, abilities, 0, "Gen 0 Legend")
    enemy.ai_pattern = ['4', '2', '3', '1']
    return enemy


def create_enemy_cheon_shinmyeong():
    abilities = {
        '1': {"name": "🔮 Dark Exorcism", "dmg": (90, 140)},
        '2': {"name": "🔮 Cheonliang Rule", "dmg": (100, 150)},
        '3': {"name": "🔮 Puppeteer", "dmg": (80, 120)}
    }
    enemy = Enemy("Cheon Shin-myeong", "The Shaman", 480, 320, abilities, 0, "Cheonliang")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


# ============================================================================
# GAME CLASS
# ============================================================================

class LookismGame:
    def __init__(self, load_saved=True):
        # GEN 0 LEGENDS
        self.gapryong = GapryongKim()
        self.tom_lee = TomLee()
        self.charles_choi = CharlesChoi()
        self.jinyoung = JinyoungPark()
        self.baekho = Baekho()

        # 1ST GENERATION KINGS
        self.james_lee = JamesLee()
        self.gitae = GitaeKim()
        self.jichang = JichangKwak()
        self.taesoo = TaesooMa()
        self.gongseob = GongseobJi()
        self.seokdu = SeokduWang()
        self.jaegyeon = JaegyeonNa()
        self.seongji = SeongjiYuk()
        self.jinrang = Jinrang()

        # WORKERS
        self.mandeok = Mandeok()
        self.cap_guy = CapGuy()
        self.xiaolung = Xiaolung()
        self.ryuhei = Ryuhei()
        self.samuel = SamuelSeo()
        self.sinu = SinuHan()
        self.logan = LoganLee()

        # CHEONLIANG
        self.vin_jin = VinJin()
        self.han_jaeha = HanJaeha()
        self.baek_seong = BaekSeong()

        # YAMAZAKI
        self.shingen = ShingenYamazaki()
        self.park_father = ParkFather()

        # LAW ENFORCEMENT
        self.kim_minjae = KimMinjae()
        self.detective_kang = DetectiveKang()

        # EXISTING CHARACTERS
        self.daniel = DanielPark("current")
        self.zack = ZackLee()
        self.johan = JohanSeong(blind=True)
        self.vasco = Vasco()
        self.jay = JayHong()
        self.eli = EliJang()
        self.warren = WarrenChae()
        self.jake = JakeKim()
        self.gun = GunPark()
        self.goo = GooKim()
        self.joongoo = KimJungu()
        self.manager_kim = ManagerKim()

        # ALL PLAYABLE CHARACTERS (51 total)
        self.all_characters = [
            # GEN 0
            self.gapryong, self.tom_lee, self.charles_choi, self.jinyoung, self.baekho,
            # 1ST GEN
            self.james_lee, self.gitae, self.jichang, self.taesoo, self.gongseob,
            self.seokdu, self.jaegyeon, self.seongji, self.jinrang,
            # WORKERS
            self.mandeok, self.cap_guy, self.xiaolung, self.ryuhei, self.samuel,
            self.sinu, self.logan,
            # CHEONLIANG
            self.vin_jin, self.han_jaeha, self.baek_seong,
            # YAMAZAKI
            self.shingen, self.park_father,
            # LAW
            self.kim_minjae, self.detective_kang,
            # EXISTING
            self.daniel, self.zack, self.johan, self.vasco, self.jay,
            self.eli, self.warren, self.jake, self.gun, self.goo,
            self.joongoo, self.manager_kim
        ]

        # Unlock system
        self.unlocked_characters = {
            "Gapryong Kim": False,
            "Tom Lee": False,
            "Charles Choi": False,
            "Jinyoung Park": False,
            "Baekho": False,
            "James Lee": False,
            "Gitae Kim": False,
            "Shingen Yamazaki": False,
            "Park Jonggun's Father": False,
            "Jinrang": False,
            "Jaegyeon Na": False
        }

        self.unlock_requirements = {
            "Gapryong Kim": "Complete Boss Rush Mode",
            "Tom Lee": "Complete Secret Arc: Genesis",
            "Charles Choi": "Complete Final Chapter",
            "Jinyoung Park": "Complete Gen 0 Flashback",
            "Baekho": "Complete Gen 0 Flashback",
            "James Lee": "Complete Boss Rush Mode",
            "Gitae Kim": "Complete Boss Rush Mode",
            "Shingen Yamazaki": "Complete Gen 0 Flashback",
            "Park Jonggun's Father": "Complete Gen 0 Flashback",
            "Jinrang": "Complete Chapter 25: Jinrang's Return",
            "Jaegyeon Na": "Complete Chapter 26: The Betrayal"
        }

        # Story progress
        self.story_progress = {
            "arc1_complete": False,
            "arc2_complete": False,
            "arc3_complete": False,
            "arc4_complete": False,
            "arc5_complete": False,
            "arc6_complete": False,
            "arc7_complete": False,
            "arc8_complete": False,
            "gen0_complete": False,
            "boss_rush_complete": False,
            "jinrang_defeated": False,
            "jaegyeon_defeated": False,
            "charles_choi_defeated": False,
            "tom_lee_defeated": False,
            "gapryong_defeated": False
        }

        # Game stats
        self.party = []
        self.enemies = []
        self.turn_count = 0
        self.victories = 0
        self.total_kills = 0
        self.wave = 0
        self.current_arc = "J High"
        self.path_changes_available = 3

        # Load saved game if requested
        if load_saved:
            self.load_game()

    def add_log(self, message):
        print(f"[T{self.turn_count}] ", end='')
        slow_print(message, 0.02)
        time.sleep(0.2)

    def display_health_bars(self):
        print("\n" + "=" * 110)
        print("✦✦✦ PARTY STATUS ✦✦✦")
        print("-" * 110)
        time.sleep(0.3)

        for member in self.party:
            if member.is_alive():
                bar_len = 40
                filled = int(bar_len * member.hp / member.max_hp)
                bar = "█" * filled + "░" * (bar_len - filled)
                status = []

                if hasattr(member, 'ui_mode') and member.ui_mode:
                    status.append("👁️UI")
                if hasattr(member, 'beast_mode') and member.beast_mode:
                    status.append("🦁BEAST")
                if hasattr(member, 'veinous_rage') and member.veinous_rage:
                    status.append("👁️RAGE")

                if member.active_realm != Realm.NONE:
                    realm_icons = {
                        Realm.SPEED: "🔵",
                        Realm.STRENGTH: "🔴",
                        Realm.TENACITY: "🟢",
                        Realm.TECHNIQUE: "🩷",
                        Realm.OVERCOMING: "🟣"
                    }
                    status.append(f"{realm_icons.get(member.active_realm, '')}REALM")

                if member.path:
                    status.append("🛤️PATH")

                status_str = " | ".join(status) if status else ""
                print(
                    f"{member.name:20} |{bar}| {member.hp:3}/{member.max_hp:3} HP {member.energy:3}E  {status_str}")
                time.sleep(0.1)

        print("\n" + "=" * 110)
        print("☠☠☠ ENEMY STATUS ☠☠☠")
        print("-" * 110)
        time.sleep(0.3)

        for enemy in self.enemies:
            if enemy.is_alive():
                bar_len = 40
                filled = int(bar_len * enemy.hp / enemy.max_hp)
                bar = "█" * filled + "░" * (bar_len - filled)
                debuff = []
                if "stun" in enemy.debuffs:
                    debuff.append("⚡STUN")
                if "bound" in enemy.debuffs:
                    debuff.append("⚪BOUND")
                debuff_str = " | ".join(debuff) if debuff else ""
                affil = f" [{enemy.affiliation}]" if enemy.affiliation else ""
                print(f"{enemy.name:20} |{bar}| {enemy.hp:3}/{enemy.max_hp:3} HP{affil} {debuff_str}")
                time.sleep(0.1)

        print("=" * 110)
        time.sleep(0.5)

    def select_target(self, allies=False):
        if allies:
            targets = [c for c in self.party if c.is_alive()]
            if not targets:
                return None
            print("\n" + "✦" * 50)
            slow_print("✦✦✦ SELECT ALLY TARGET ✦✦✦", 0.03)
            print("✦" * 50)
            for i, t in enumerate(targets):
                print(f"  {i + 1}. {t.name} ({t.hp}/{t.max_hp} HP)")
                time.sleep(0.1)
        else:
            targets = [e for e in self.enemies if e.is_alive()]
            if not targets:
                return None
            print("\n" + "☠" * 50)
            slow_print("☠☠☠ SELECT ENEMY TARGET ☠☠☠", 0.03)
            print("☠" * 50)
            for i, t in enumerate(targets):
                print(f"  {i + 1}. {t.name} ({t.hp}/{t.max_hp} HP)")
                time.sleep(0.1)

        choice = input("> ").strip()
        print()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(targets):
                return targets[idx]
        except:
            pass
        print("❌ Invalid target. Try again.")
        time.sleep(0.5)
        return self.select_target(allies)

    def display_ability_description(self, abil):
        print("\n" + "─" * 80)
        slow_print(f"📖 {abil['name']}", 0.04)
        print("─" * 80)
        slow_print(abil['desc'], 0.02)
        if "cost" in abil:
            print(f"\n⚡ Energy Cost: {abil['cost']}")
        if "dmg" in abil and abil["dmg"] != (0, 0):
            print(f"💢 Damage: {abil['dmg'][0]}-{abil['dmg'][1]}")
        print("─" * 80)
        input("Press Enter to continue...")
        print()

    def choose_character_path(self, character):
        if character.path:
            print(f"\n{character.name} currently walks the path of {character.path.value}")
            print(f"Path Level: {character.path_level} | EXP: {character.path_exp}/100")
            print("\nOptions:")
            print("  1. Keep current path")
            print("  2. Change path (resets level and EXP)")
            print("  3. Reset path (no new path chosen yet)")
            print("  b. Back")

            choice = input("> ").strip()
            if choice == '1':
                return True
            elif choice == '2':
                confirm = input(
                    f"Are you sure you want to change {character.name}'s path? Level and EXP will reset. (y/n): ").lower()
                if confirm == 'y':
                    result = character.reset_path()
                    print(result)
                    time.sleep(1)
                    return self.choose_character_path(character)
                return True
            elif choice == '3':
                confirm = input(f"Reset {character.name}'s path completely? (y/n): ").lower()
                if confirm == 'y':
                    character.path = None
                    character.infinity_technique = None
                    character.path_level = 1
                    character.path_exp = 0
                    print(f"🔄 {character.name}'s path has been reset!")
                    time.sleep(1)
                    return self.choose_character_path(character)
                return True
            elif choice == 'b':
                return True
            else:
                print("❌ Invalid choice.")
                return self.choose_character_path(character)

        print(f"\n" + "=" * 110)
        slow_print(f"✦✦✦ CHOOSE {character.name.upper()}'S PATH ✦✦✦", 0.03)
        print("=" * 110)
        print(f"{character.name} [{character.title}]")
        print("-" * 110)

        for i, path in enumerate(character.paths_available):
            print(f"\n  {i + 1}. {path.value}")
            if path in INFINITY_TECHNIQUES:
                tech = INFINITY_TECHNIQUES[path]
                print(f"     ➤ Infinity Technique: {tech['name']}")
                print(f"     ➤ {tech['desc'][:100]}...")
            time.sleep(0.2)

        print("\n  b. Back")
        print("-" * 110)

        choice = input("> ").strip()
        if choice.lower() == 'b':
            return False

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(character.paths_available):
                selected_path = character.paths_available[idx]
                result = character.choose_path(selected_path)
                slow_print(result, 0.03)
                time.sleep(1)
                return True
        except:
            pass

        print("❌ Invalid choice.")
        time.sleep(0.5)
        return self.choose_character_path(character)

    def use_ability(self, character):
        # Check exhaustion
        if hasattr(character, 'exhausted') and character.exhausted:
            self.add_log(f"{character.name} is exhausted and cannot act this turn!")
            character.exhausted = False
            character.energy = min(character.max_energy, character.energy + 15)
            time.sleep(ACTION_DELAY)
            return True

        print(f"\n" + "=" * 110)
        slow_print(f"✦✦✦ {character.name} [{character.title}] ✦✦✦", 0.03)
        print("=" * 110)
        print(f"❤️ HP: {character.hp}/{character.max_hp}  ⚡ Energy: {character.energy}/{character.max_energy}")
        if character.path:
            print(f"🛤️ PATH: {character.path.value[:50]}...")
        print("-" * 110)
        time.sleep(0.3)

        # Build available abilities
        available = {}
        for key, abil in character.abilities.items():
            if character.energy < abil["cost"]:
                continue
            available[key] = abil

        print("\n" + "📋 AVAILABLE ABILITIES:")
        print("-" * 110)
        time.sleep(0.2)

        damage_abilities = {k: v for k, v in available.items() if v.get("type") == "damage"}
        buff_abilities = {k: v for k, v in available.items() if v.get("type") in ["buff", "realm", "ui"]}
        utility_abilities = {k: v for k, v in available.items() if v.get("type") == "utility"}

        if damage_abilities:
            print("  💢 DAMAGE:")
            for key in sorted(damage_abilities.keys(), key=lambda x: int(x) if x.isdigit() else x):
                abil = damage_abilities[key]
                d = abil["dmg"]
                print(f"    {key}. {abil['name']:35} | {abil['cost']}E | {d[0]}-{d[1]} DMG")
                time.sleep(0.05)

        if buff_abilities:
            print("\n  💪 BUFFS:")
            for key in sorted(buff_abilities.keys(), key=lambda x: int(x) if x.isdigit() else x):
                abil = buff_abilities[key]
                print(f"    {key}. {abil['name']:35} | {abil['cost']}E | BUFF")
                time.sleep(0.05)

        if utility_abilities:
            print("\n  🛡️ UTILITY:")
            for key in sorted(utility_abilities.keys(), key=lambda x: int(x) if x.isdigit() else x):
                abil = utility_abilities[key]
                print(f"    {key}. {abil['name']:35} | {abil['cost']}E | UTILITY")
                time.sleep(0.05)

        if character.infinity_technique and character.energy >= character.infinity_technique['cost']:
            it = character.infinity_technique
            print(f"\n  ✨ INFINITY TECHNIQUE (99):")
            print(f"     99. {it['name']} | {it['cost']}E | {it['dmg'][0]}-{it['dmg'][1]} DMG")

        print("\n" + "🎮 COMMANDS:")
        print("  0. Describe Ability")
        print("  00. Activate Realm (if available)")
        print("  000. Choose/View Path")
        print("  0000. Skip Turn (+15E)")
        print("  00000. Back")
        print("-" * 110)

        choice = input("> ").strip()
        print()

        if choice == '00000':
            return False
        if choice == '0000':
            self.add_log(f"{character.name} skips turn. +15 Energy")
            character.energy = min(character.max_energy, character.energy + 15)
            time.sleep(ACTION_DELAY)
            return True
        if choice == '000':
            self.choose_character_path(character)
            self.save_game()
            return self.use_ability(character)
        if choice == '00':
            if character.realms:
                print("\n🔮 AVAILABLE REALMS:")
                for i, realm in enumerate(character.realms):
                    print(f"  {i + 1}. {realm.value}")
                print("  b. Back")
                realm_choice = input("> ").strip()
                if realm_choice.isdigit():
                    idx = int(realm_choice) - 1
                    if 0 <= idx < len(character.realms):
                        self.add_log(character.activate_realm(character.realms[idx]))
                return self.use_ability(character)
            else:
                print(f"{character.name} cannot activate any realms.")
                return self.use_ability(character)
        if choice == '0':
            print("\n📖 SELECT ABILITY:")
            for key in sorted(available.keys(), key=lambda x: int(x) if x.isdigit() else x):
                abil = available[key]
                print(f"  {key}. {abil['name']}")
            desc_choice = input("> ").strip()
            if desc_choice in available:
                self.display_ability_description(available[desc_choice])
            return self.use_ability(character)
        if choice == '99' and character.infinity_technique and character.energy >= character.infinity_technique['cost']:
            it = character.infinity_technique
            character.energy -= it['cost']

            target = self.select_target()
            if target:
                dmg = random.randint(it['dmg'][0], it['dmg'][1])

                if hasattr(character, 'get_damage_multiplier'):
                    mult, buffs = character.get_damage_multiplier()
                    dmg = int(dmg * mult)

                target.take_damage(dmg)
                print("\n" + "✨" * 55)
                slow_print(f"✨✨✨ {it['name']} ✨✨✨", 0.05)
                print("✨" * 55)
                time.sleep(0.5)
                self.add_log(f"{character.name} unleashes their INFINITY TECHNIQUE for {dmg} damage!")

                time.sleep(ACTION_DELAY)
                return True

        if choice in available:
            ability = available[choice]
            character.energy = max(0, character.energy - ability["cost"])

            if ability.get("type") == "realm":
                realm_map = {
                    "🔵 Realm of Speed": Realm.SPEED,
                    "🔴 Realm of Strength": Realm.STRENGTH,
                    "🟢 Realm of Tenacity": Realm.TENACITY,
                    "🩷 Realm of Technique": Realm.TECHNIQUE,
                    "🟣 Realm of Overcoming": Realm.OVERCOMING
                }
                for name, realm in realm_map.items():
                    if name in ability["name"]:
                        self.add_log(character.activate_realm(realm))
                        break

            elif ability.get("type") == "ui":
                if hasattr(character, 'activate_ui'):
                    self.add_log(character.activate_ui())

            elif ability.get("type") == "buff":
                if character.name == "Eli Jang" and "Beast Mode" in ability["name"]:
                    self.add_log(character.activate_beast_mode())
                elif character.name == "Vasco" and "Muscle Enhancement" in ability["name"]:
                    character.muscle_boost = True
                    self.add_log("💪 MUSCLE ENHANCEMENT! +30% damage")
                else:
                    self.add_log(f"{character.name} uses {ability['name']}!")

            elif ability.get("type") == "utility":
                if "Thread Bind" in ability["name"]:
                    for e in self.enemies:
                        if random.random() < 0.6:
                            e.debuffs.append("bound")
                            self.add_log(f"⚪ {e.name} is bound by silver threads!")
                else:
                    self.add_log(f"{character.name} uses {ability['name']}!")

            elif ability.get("type") == "damage" or "dmg" in ability:
                target = self.select_target()
                if target:
                    dmg = random.randint(ability["dmg"][0], ability["dmg"][1])

                    if hasattr(character, 'get_damage_multiplier'):
                        mult, buffs = character.get_damage_multiplier()
                        dmg = int(dmg * mult)

                    target.take_damage(dmg)
                    self.add_log(f"{character.name} uses {ability['name']} for {dmg} damage!")

            time.sleep(ACTION_DELAY)
            return True
        else:
            print("❌ Invalid ability. Try again.")
            time.sleep(0.5)
            return self.use_ability(character)

    def enemy_turn(self, enemy):
        if not enemy.is_alive():
            return
        if not any(c.is_alive() for c in self.party):
            return
        if "stun" in enemy.debuffs:
            self.add_log(f"⚡ {enemy.name} is stunned and cannot act!")
            enemy.debuffs.remove("stun")
            time.sleep(0.5)
            return
        if "bound" in enemy.debuffs:
            self.add_log(f"⚪ {enemy.name} is bound and cannot act!")
            enemy.debuffs.remove("bound")
            time.sleep(0.5)
            return

        if enemy.ai_pattern:
            key = enemy.ai_pattern[self.turn_count % len(enemy.ai_pattern)]
            abil = enemy.abilities.get(key, list(enemy.abilities.values())[0])
            targets = [c for c in self.party if c.is_alive()]

            if targets:
                t = random.choice(targets)
                dmg = random.randint(abil["dmg"][0], abil["dmg"][1])

                if t.defending:
                    dmg = int(dmg * 0.5)
                    t.defending = False
                    self.add_log(f"🛡️ {t.name} blocks!")

                t.take_damage(dmg)
                self.add_log(f"{enemy.name} uses {abil['name']} for {dmg} damage!")
                time.sleep(0.8)

    def cleanup(self):
        for c in self.party + self.enemies:
            c.defending = False

            if hasattr(c, 'realm_timer') and c.realm_timer > 0:
                c.realm_timer -= 1
                if c.realm_timer <= 0:
                    c.active_realm = Realm.NONE
                    if hasattr(c, 'name'):
                        self.add_log(f"{c.name}'s realm fades.")

            if hasattr(c, 'ui_mode') and c.ui_mode:
                c.ui_timer -= 1
                if c.ui_timer <= 0:
                    c.ui_mode = False

            to_remove = []
            for debuff in c.debuffs:
                if random.random() < 0.3:
                    to_remove.append(debuff)

            for debuff in to_remove:
                if debuff in c.debuffs:
                    c.debuffs.remove(debuff)

            time.sleep(0.2)

    def save_game(self):
        game_state = {
            'unlocked_characters': self.unlocked_characters,
            'story_progress': self.story_progress,
            'victories': self.victories,
            'total_kills': self.total_kills,
            'characters': {}
        }

        for char in self.all_characters:
            game_state['characters'][char.name] = char.to_dict()

        if SaveSystem.save_game(game_state):
            print("\n💾 Game saved successfully!")
            return True
        return False

    def load_game(self):
        game_state = SaveSystem.load_game()
        if not game_state:
            return False

        self.unlocked_characters = game_state.get('unlocked_characters', self.unlocked_characters)
        self.story_progress = game_state.get('story_progress', self.story_progress)
        self.victories = game_state.get('victories', 0)
        self.total_kills = game_state.get('total_kills', 0)

        char_data = game_state.get('characters', {})
        for char in self.all_characters:
            if char.name in char_data:
                char.from_dict(char_data[char.name])

        print("\n📂 Game loaded successfully!")
        return True

    def check_unlocks(self):
        print("\n" + "=" * 110)
        slow_print("🔓 CHECKING UNLOCKS...", 0.03)
        print("=" * 110)

        new_unlocks = []

        if not self.unlocked_characters["Jinrang"] and self.story_progress.get("jinrang_defeated", False):
            self.unlocked_characters["Jinrang"] = True
            new_unlocks.append("Jinrang - King of Busan")

        if not self.unlocked_characters["Jaegyeon Na"] and self.story_progress.get("jaegyeon_defeated", False):
            self.unlocked_characters["Jaegyeon Na"] = True
            new_unlocks.append("Jaegyeon Na - King of Incheon")

        if new_unlocks:
            print("\n✨✨✨ NEW CHARACTERS UNLOCKED! ✨✨✨")
            for char in new_unlocks:
                print(f"  ✅ {char}")
            self.save_game()
        else:
            print("\nNo new unlocks yet. Keep fighting!")

        time.sleep(2)

    def select_party(self, max_size=4):
        print("\n" + "=" * 110)
        slow_print("✦✦✦ SELECT YOUR PARTY ✦✦✦", 0.03)
        print("=" * 110)
        print(f"Choose up to {max_size} characters for this battle:")
        print("-" * 110)

        available = []
        locked_list = []

        for i, char in enumerate(self.all_characters):
            is_locked = False
            if char.name in self.unlocked_characters:
                if not self.unlocked_characters[char.name]:
                    is_locked = True

            if char.is_alive() and not is_locked:
                path_info = f" [{char.path.name}]" if char.path else ""
                print(f"  {i + 1}. {char.name} [{char.title}]{path_info} - {char.hp}/{char.max_hp} HP")
                available.append(char)
            elif is_locked:
                locked_list.append(f"  {char.name} - 🔒 {self.unlock_requirements.get(char.name, 'Locked')}")
            time.sleep(0.05)

        if locked_list:
            print("\n🔒 LOCKED CHARACTERS:")
            for lock in locked_list:
                print(lock)

        print(f"\n  a. Auto-select (Daniel, Vasco, Zack, Jay)")
        print("  s. Save Game")
        print("  c. Cancel")
        print("-" * 110)

        choice = input("> ").strip().lower()
        if choice == 'c':
            return None
        if choice == 's':
            self.save_game()
            return self.select_party(max_size)
        if choice == 'a':
            return [self.daniel, self.vasco, self.zack, self.jay]

        selected = []
        print(f"\nEnter character numbers (1-{len(available)}), one per line. Empty line to finish:")

        while len(selected) < max_size:
            char_choice = input(f"Character {len(selected) + 1}: ").strip()
            if not char_choice:
                break
            try:
                idx = int(char_choice) - 1
                if 0 <= idx < len(available):
                    char = available[idx]
                    if char not in selected:
                        selected.append(char)
                        print(f"  ✓ Added {char.name}")
                    else:
                        print(f"  ✗ {char.name} already selected")
                else:
                    print("  ✗ Invalid number")
            except:
                print("  ✗ Invalid input")

        if selected:
            return selected
        else:
            return [self.daniel, self.vasco, self.zack, self.jay]

    def battle(self, enemies, party=None):
        self.enemies = enemies

        if party:
            self.party = party
        else:
            self.party = self.select_party()
            if not self.party:
                return False

        self.turn_count = 0

        print("\n" + "=" * 110)
        slow_print("⚔️⚔️⚔️ BATTLE START ⚔️⚔️⚔️", 0.04)
        print("=" * 110)
        print(f"✦ PARTY: {', '.join([c.name for c in self.party])}")
        print(f"☠ ENEMIES: {', '.join([e.name for e in self.enemies])}")
        if hasattr(self.enemies[0], 'affiliation') and self.enemies[0].affiliation:
            print(f"🏴 AFFILIATION: {self.enemies[0].affiliation}")
        print("=" * 110)
        time.sleep(BATTLE_START_DELAY)

        while True:
            self.turn_count += 1
            print(f"\n{'=' * 55} TURN {self.turn_count} {'=' * 55}")
            time.sleep(TURN_DELAY)

            for char in self.party:
                if char.is_alive():
                    char.energy = min(char.max_energy, char.energy + 15)
                    action = False
                    while not action:
                        self.display_health_bars()
                        action = self.use_ability(char)
                    if not any(e.is_alive() for e in self.enemies):
                        break

            if not any(e.is_alive() for e in self.enemies):
                break
            if not any(c.is_alive() for c in self.party):
                break

            print("\n" + "☠☠☠ ENEMY PHASE ☠☠☠")
            time.sleep(0.5)
            for enemy in self.enemies:
                if enemy.is_alive():
                    self.enemy_turn(enemy)
                    time.sleep(0.3)

            self.cleanup()

        self.display_health_bars()

        if any(e.is_alive() for e in self.enemies):
            print("\n" + "=" * 110)
            slow_print("💀💀💀 DEFEAT... 💀💀💀", 0.05)
            print("=" * 110)
            time.sleep(VICTORY_DELAY)
            return False
        else:
            print("\n" + "=" * 110)
            slow_print("✨✨✨ VICTORY! ✨✨✨", 0.05)
            print("=" * 110)
            self.victories += 1
            self.total_kills += len([e for e in self.enemies if not e.is_alive()])

            for char in self.party:
                if char.is_alive() and char.path:
                    char.path_exp += 10
                    if char.path_exp >= 100:
                        char.path_level += 1
                        char.path_exp = 0
                        self.add_log(f"✨ {char.name}'s path level increased to {char.path_level}!")

            self.save_game()
            time.sleep(VICTORY_DELAY)
            return True

    def rest(self):
        print("\n" + "=" * 110)
        slow_print("🛌🛌🛌 RESTING & RECOVERY 🛌🛌🛌", 0.04)
        print("=" * 110)
        time.sleep(0.5)

        for char in self.all_characters:
            char.hp = char.max_hp
            char.energy = char.max_energy
            char.buffs = []
            char.debuffs = []
            char.defending = False
            char.active_realm = Realm.NONE
            char.form = "Normal"

            if hasattr(char, 'ui_mode'):
                char.ui_mode = False
                char.ui_timer = 0
            if hasattr(char, 'beast_mode'):
                char.beast_mode = False
                char.beast_timer = 0
            if hasattr(char, 'veinous_rage'):
                char.veinous_rage = False
            if hasattr(char, 'silver_yarn_active'):
                char.silver_yarn_active = False
            if hasattr(char, 'muscle_boost'):
                char.muscle_boost = False
            if hasattr(char, 'exhausted'):
                char.exhausted = False

            print(f"  ✦ {char.name} fully recovered!")
            time.sleep(0.1)

        print("\n✦ Party fully healed and recovered! ✦")
        self.save_game()
        time.sleep(1.5)

    def path_management_menu(self):
        print("\n" + "=" * 110)
        slow_print("🛤️🛤️🛤️ PATH MANAGEMENT SYSTEM 🛤️🛤️🛤️", 0.03)
        print("=" * 110)
        print("Choose a character to manage their path:")
        print("-" * 110)

        for i, char in enumerate(self.all_characters):
            is_locked = False
            if char.name in self.unlocked_characters:
                if not self.unlocked_characters[char.name]:
                    is_locked = True

            if not is_locked:
                path_info = f"[{char.path.value[:30]}...]" if char.path else "[No Path]"
                print(f"  {i + 1}. {char.name} - {path_info} (Lv.{char.path_level})")
            else:
                print(f"  {char.name} - 🔒 LOCKED")
            time.sleep(0.05)

        print(f"\n  a. Reset ALL paths")
        print("  s. Save Game")
        print("  b. Back to main menu")
        print("-" * 110)

        choice = input("> ").strip().lower()
        print()

        if choice == 'b':
            return
        elif choice == 's':
            self.save_game()
            return self.path_management_menu()
        elif choice == 'a':
            confirm = input("Reset ALL character paths? This cannot be undone! (y/n): ").lower()
            if confirm == 'y':
                for char in self.all_characters:
                    char.path = None
                    char.infinity_technique = None
                    char.path_level = 1
                    char.path_exp = 0
                    char.path_history = []
                print("✨ ALL paths have been reset!")
                self.save_game()
                time.sleep(1)
            return self.path_management_menu()
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.all_characters):
                    char = self.all_characters[idx]
                    is_locked = False
                    if char.name in self.unlocked_characters:
                        if not self.unlocked_characters[char.name]:
                            is_locked = True
                            print(f"❌ {char.name} is locked! {self.unlock_requirements.get(char.name, 'Locked')}")
                            time.sleep(2)

                    if not is_locked:
                        self.choose_character_path(char)
                        self.save_game()
                    return self.path_management_menu()
            except:
                pass
            print("❌ Invalid choice.")
            time.sleep(0.5)
            return self.path_management_menu()

    def story_mode(self):
        print("\n" + "=" * 110)
        slow_print("📖📖📖 STORY MODE: THE COMPLETE LOOKISM 📖📖📖", 0.03)
        print("=" * 110)
        slow_print("Based on Park Tae-joon's manhwa (2014-2025)", 0.02)
        print("=" * 110)
        time.sleep(1)

        arcs = [
            ("ARC 1: J HIGH & THE TWO BODIES",
             [
                 ("Prologue: The Transfer Student", [create_enemy_jhigh_bully()]),
                 ("Chapter 1: Logan Lee", [create_enemy_logan_lee()]),
                 ("Chapter 2: Zack's Challenge", [create_enemy_zack_lee()]),
                 ("Chapter 3: Vasco Appears", [create_enemy_vasco_enemy()]),
                 ("Chapter 4: Jay's Protection", [create_enemy_jay_hong_enemy()])
             ]),
            ("ARC 2: GOD DOG",
             [
                 ("Chapter 5: God Dog Soldiers",
                  [create_enemy_god_dog_member(), create_enemy_god_dog_member()]),
                 ("Chapter 6: God Dog Elite",
                  [create_enemy_god_dog_elite(), create_enemy_god_dog_member()]),
                 ("Chapter 7: Johan Seong", [create_enemy_johan_seong_enemy()])
             ]),
            ("ARC 3: HOSTEL",
             [
                 ("Chapter 8: Hostel Family", [create_enemy_hostel_member(), create_enemy_sally()]),
                 ("Chapter 9: Warren Chae", [create_enemy_warren_chae_enemy()]),
                 ("Chapter 10: Eli Jang", [create_enemy_eli_jang_enemy()])
             ]),
            ("ARC 4: BIG DEAL",
             [
                 ("Chapter 11: Big Deal Soldiers", [create_enemy_big_deal_member(), create_enemy_brad()]),
                 ("Chapter 12: Jerry Kwon", [create_enemy_jerry_kwon()]),
                 ("Chapter 13: Jake Kim", [create_enemy_jake_kim_enemy()])
             ]),
            ("ARC 5: WORKERS",
             [
                 ("Chapter 14: Workers Affiliates",
                  [create_enemy_workers_member(), create_enemy_workers_affiliate()]),
                 ("Chapter 15: Xiaolung", [create_enemy_xiaolung()]),
                 ("Chapter 16: Mandeok", [create_enemy_mandeok()]),
                 ("Chapter 17: Samuel Seo", [create_enemy_samuel_seo()]),
                 ("Chapter 18: Eugene", [create_enemy_eugene()])
             ]),
            ("ARC 6: CHEONLIANG",
             [
                 ("Chapter 19: Vin Jin", [create_enemy_vin_jin()]),
                 ("Chapter 20: Ryuhei", [create_enemy_ryuhei()]),
                 ("Chapter 21: The Shaman", [create_enemy_cheon_shinmyeong()])
             ]),
            ("ARC 7: 1ST GENERATION",
             [
                 ("Chapter 22: Taesoo Ma", [create_enemy_taesoo_ma()]),
                 ("Chapter 23: Gongseob Ji", [create_enemy_gongseob_ji()]),
                 ("Chapter 24: Jichang Kwak", [create_enemy_jichang_kwak()])
             ]),
            ("ARC 8: BUSAN",
             [
                 ("Chapter 25: Jinrang's Return", [create_enemy_jinrang_enemy()]),
                 ("Chapter 26: The Betrayal", [create_enemy_jaegyeon_na_enemy()]),
                 ("Final Chapter: Charles Choi", [create_enemy_charles_choi()])
             ]),
            ("SECRET ARC: GENESIS",
             [
                 ("Gen 0: Tom Lee", [create_enemy_tom_lee()]),
                 ("Gen 0: Gapryong Kim", [create_enemy_gapryong_kim()])
             ])
        ]

        for arc_name, chapters in arcs:
            print("\n" + "🔥" * 110)
            slow_print(f"🔥 {arc_name} 🔥", 0.03)
            print("🔥" * 110)
            time.sleep(1)

            for i, (chapter, enemies) in enumerate(chapters):
                print("\n" + "!" * 110)
                slow_print(f"📖 {chapter}", 0.03)
                print(f"Battle {i + 1}/{len(chapters)} in this arc")
                print("!" * 110)
                time.sleep(0.5)

                party = self.select_party(4)
                if not party:
                    party = [self.daniel, self.vasco, self.zack, self.jay]

                input("Press Enter to continue...")
                print()

                if not self.battle(enemies, party):
                    print("\n💀 GAME OVER 💀")
                    print(f"Defeated at {chapter}")
                    time.sleep(2)
                    return False

                if chapter == "Chapter 25: Jinrang's Return":
                    self.story_progress["jinrang_defeated"] = True
                    self.check_unlocks()
                elif chapter == "Chapter 26: The Betrayal":
                    self.story_progress["jaegyeon_defeated"] = True
                    self.check_unlocks()
                elif chapter == "Final Chapter: Charles Choi":
                    self.story_progress["charles_choi_defeated"] = True
                elif chapter == "Gen 0: Tom Lee":
                    self.story_progress["tom_lee_defeated"] = True
                elif chapter == "Gen 0: Gapryong Kim":
                    self.story_progress["gapryong_defeated"] = True

                if chapter != chapters[-1][0]:
                    self.rest()

            self.save_game()

        print("\n" + "=" * 110)
        slow_print("🏆🏆🏆 STORY MODE COMPLETE! 🏆🏆🏆", 0.04)
        print("=" * 110)
        print(f"Total victories: {self.victories}")
        print(f"Enemies defeated: {self.total_kills}")
        print("=" * 110)
        self.save_game()
        time.sleep(3)
        return True

    def crew_gauntlet_mode(self):
        print("\n" + "=" * 110)
        slow_print("🏆🏆🏆 CREW GAUNTLET 🏆🏆🏆", 0.04)
        print("=" * 110)
        time.sleep(1)

        stages = [
            ("God Dog Recruits", [create_enemy_god_dog_member(), create_enemy_god_dog_member()]),
            ("Burn Knuckles", [create_enemy_burn_knuckles(), create_enemy_jace_park()]),
            ("Hostel Family", [create_enemy_hostel_member(), create_enemy_sally()]),
            ("Big Deal Soldiers", [create_enemy_big_deal_member(), create_enemy_brad()]),
            ("Workers Affiliates", [create_enemy_workers_member(), create_enemy_workers_affiliate()]),
            ("God Dog Elite", [create_enemy_god_dog_elite(), create_enemy_god_dog_elite()]),
            ("Hostel Executives", [create_enemy_warren_chae_enemy()]),
            ("Big Deal Executive", [create_enemy_jerry_kwon()]),
            ("Workers 3rd Affiliate", [create_enemy_mandeok()]),
            ("Workers 2nd Affiliate", [create_enemy_xiaolung()]),
            ("Vin Jin", [create_enemy_vin_jin()]),
            ("Ryuhei", [create_enemy_ryuhei()]),
            ("Johan Seong", [create_enemy_johan_seong_enemy()]),
            ("Eli Jang", [create_enemy_eli_jang_enemy()]),
            ("Jake Kim", [create_enemy_jake_kim_enemy()]),
            ("Samuel Seo", [create_enemy_samuel_seo()]),
            ("Gun Park", [create_enemy_gun_park_enemy()]),
            ("Goo Kim", [create_enemy_goo_kim_enemy()]),
            ("Kim Jun-gu", [create_enemy_kim_jungu_enemy()]),
            ("Manager Kim", [create_enemy_manager_kim_enemy()])
        ]

        for i, (stage, enemies) in enumerate(stages):
            self.wave = i + 1
            print("\n" + "!" * 110)
            slow_print(f"🏆 STAGE {self.wave}: {stage}", 0.03)
            print("!" * 110)
            time.sleep(0.5)

            party = self.select_party(4)
            if not party:
                party = [self.daniel, self.vasco, self.zack, self.jay]

            input("Press Enter to challenge...")
            print()

            if not self.battle(enemies, party):
                print("\n💀 GAUNTLET FAILED 💀")
                print(f"Defeated at Stage {self.wave}: {stage}")
                time.sleep(2)
                return False

            if i < len(stages) - 1:
                self.rest()

        print("\n" + "=" * 110)
        slow_print("🏆🏆🏆 CREW GAUNTLET COMPLETE! 🏆🏆🏆", 0.04)
        print("=" * 110)
        print(f"Total victories: {self.victories}")
        print(f"Enemies defeated: {self.total_kills}")
        print("=" * 110)
        self.save_game()
        time.sleep(3)
        return True

    def boss_rush_mode(self):
        print("\n" + "=" * 110)
        slow_print("👑👑👑 BOSS RUSH 👑👑👑", 0.04)
        print("=" * 110)
        slow_print("No rest between battles!", 0.02)
        print("=" * 110)
        time.sleep(1)

        bosses = [
            ("Logan Lee", [create_enemy_logan_lee()]),
            ("Johan Seong", [create_enemy_johan_seong_enemy()]),
            ("Eli Jang", [create_enemy_eli_jang_enemy()]),
            ("Warren Chae", [create_enemy_warren_chae_enemy()]),
            ("Jake Kim", [create_enemy_jake_kim_enemy()]),
            ("Xiaolung", [create_enemy_xiaolung()]),
            ("Mandeok", [create_enemy_mandeok()]),
            ("Vin Jin", [create_enemy_vin_jin()]),
            ("Ryuhei", [create_enemy_ryuhei()]),
            ("Samuel Seo", [create_enemy_samuel_seo()]),
            ("Taesoo Ma", [create_enemy_taesoo_ma()]),
            ("Gongseob Ji", [create_enemy_gongseob_ji()]),
            ("Jichang Kwak", [create_enemy_jichang_kwak()]),
            ("Gun Park", [create_enemy_gun_park_enemy()]),
            ("Goo Kim", [create_enemy_goo_kim_enemy()]),
            ("Kim Jun-gu", [create_enemy_kim_jungu_enemy()]),
            ("Manager Kim", [create_enemy_manager_kim_enemy()]),
            ("Jinrang", [create_enemy_jinrang_enemy()]),
            ("Jaegyeon Na", [create_enemy_jaegyeon_na_enemy()]),
            ("Charles Choi", [create_enemy_charles_choi()]),
            ("Tom Lee", [create_enemy_tom_lee()]),
            ("Gapryong Kim", [create_enemy_gapryong_kim()])
        ]

        party = self.select_party(4)
        if not party:
            party = [self.daniel, self.gun, self.goo, self.johan]

        for i, (boss, enemies) in enumerate(bosses):
            self.wave = i + 1
            print("\n" + "!" * 110)
            slow_print(f"👑 BOSS {self.wave}: {boss}", 0.03)
            print("!" * 110)
            time.sleep(0.5)

            input("Press Enter to challenge...")
            print()

            if not self.battle(enemies, party):
                print("\n💀 BOSS RUSH FAILED 💀")
                print(f"Defeated at Boss {self.wave}: {boss}")
                time.sleep(2)
                return False

            print("⚔️ Preparing next boss... ⚔️")
            time.sleep(1)

        self.story_progress["boss_rush_complete"] = True
        self.check_unlocks()
        self.save_game()

        print("\n" + "=" * 110)
        slow_print("👑👑👑 BOSS RUSH COMPLETE! 👑👑👑", 0.04)
        print("=" * 110)
        print(f"Total victories: {self.victories}")
        print("=" * 110)
        time.sleep(3)
        return True

    def survival_mode(self):
        print("\n" + "=" * 110)
        slow_print("♾️♾️♾️ ENDLESS SURVIVAL ♾️♾️♾️", 0.04)
        print("=" * 110)
        time.sleep(1)

        wave = 0
        score = 0

        party = self.select_party(4)
        if not party:
            party = [self.daniel, self.vasco, self.zack, self.eli]

        while True:
            wave += 1
            self.wave = wave

            print("\n" + "🔥" * 55)
            slow_print(f"🔥 WAVE {wave} 🔥", 0.05)
            print("🔥" * 55)
            time.sleep(0.5)

            wave_enemies = []

            if wave <= 5:
                count = min(3, wave)
                for _ in range(count):
                    wave_enemies.append(create_enemy_god_dog_member())
            elif wave <= 10:
                wave_enemies.append(create_enemy_god_dog_elite())
                wave_enemies.append(create_enemy_god_dog_member())
                wave_enemies.append(create_enemy_god_dog_member())
            elif wave <= 15:
                wave_enemies.append(create_enemy_hostel_member())
                wave_enemies.append(create_enemy_big_deal_member())
                wave_enemies.append(create_enemy_workers_member())
            elif wave <= 20:
                wave_enemies.append(create_enemy_sally())
                wave_enemies.append(create_enemy_brad())
                wave_enemies.append(create_enemy_jace_park())
            elif wave <= 25:
                wave_enemies.append(create_enemy_warren_chae_enemy())
                wave_enemies.append(create_enemy_jerry_kwon())
            elif wave <= 30:
                wave_enemies.append(create_enemy_mandeok())
                wave_enemies.append(create_enemy_xiaolung())
            elif wave <= 35:
                wave_enemies.append(create_enemy_vin_jin())
                wave_enemies.append(create_enemy_ryuhei())
            elif wave <= 40:
                wave_enemies.append(create_enemy_samuel_seo())
                wave_enemies.append(create_enemy_eugene())
            elif wave <= 45:
                wave_enemies.append(create_enemy_johan_seong_enemy())
                wave_enemies.append(create_enemy_eli_jang_enemy())
            elif wave <= 50:
                wave_enemies.append(create_enemy_jake_kim_enemy())
                wave_enemies.append(create_enemy_taesoo_ma())
            else:
                bosses = [
                    create_enemy_gun_park_enemy(),
                    create_enemy_goo_kim_enemy(),
                    create_enemy_kim_jungu_enemy(),
                    create_enemy_manager_kim_enemy(),
                    create_enemy_jinrang_enemy(),
                    create_enemy_charles_choi(),
                    create_enemy_gapryong_kim()
                ]
                wave_enemies.append(random.choice(bosses))
                wave_enemies.append(create_enemy_workers_affiliate())
                wave_enemies.append(create_enemy_workers_affiliate())

            input("Press Enter to face the wave...")
            print()

            if not self.battle(wave_enemies, party):
                print("\n" + "=" * 110)
                slow_print(f"☠️☠️☠️ SURVIVAL ENDED AT WAVE {wave} ☠️☠️☠️", 0.04)
                print("=" * 110)
                print(f"Enemies defeated: {self.total_kills}")
                print(f"Waves cleared: {wave - 1}")
                print(f"Score: {score}")
                print("=" * 110)
                time.sleep(3)
                break

            score += wave * 100
            print(f"\n✨ Wave {wave} cleared! Score: {score}")
            self.save_game()
            time.sleep(1)

            if random.random() < 0.2:
                for char in party:
                    char.hp = min(char.max_hp, char.hp + int(char.max_hp * 0.2))
                    char.energy = min(char.max_energy, char.energy + int(char.max_energy * 0.2))
                slow_print("🩹 Found supplies! Party recovers 20% HP/Energy.", 0.02)
                time.sleep(1)

        return score

    def training_mode(self):
        print("\n" + "=" * 110)
        slow_print("🥋🥋🥋 TRAINING ROOM 🥋🥋🥋", 0.04)
        print("=" * 110)
        time.sleep(0.5)

        training_options = [
            ("1", "Frame Soldier", create_enemy_frame_soldier),
            ("2", "Logan Lee", create_enemy_logan_lee),
            ("3", "Johan Seong", create_enemy_johan_seong_enemy),
            ("4", "Vasco", create_enemy_vasco_enemy),
            ("5", "Zack Lee", create_enemy_zack_lee),
            ("6", "Jay Hong", create_enemy_jay_hong_enemy),
            ("7", "Eli Jang", create_enemy_eli_jang_enemy),
            ("8", "Warren Chae", create_enemy_warren_chae_enemy),
            ("9", "Jake Kim", create_enemy_jake_kim_enemy),
            ("10", "Jerry Kwon", create_enemy_jerry_kwon),
            ("11", "Xiaolung", create_enemy_xiaolung),
            ("12", "Mandeok", create_enemy_mandeok),
            ("13", "Vin Jin", create_enemy_vin_jin),
            ("14", "Ryuhei", create_enemy_ryuhei),
            ("15", "Samuel Seo", create_enemy_samuel_seo),
            ("16", "Taesoo Ma", create_enemy_taesoo_ma),
            ("17", "Gongseob Ji", create_enemy_gongseob_ji),
            ("18", "Jichang Kwak", create_enemy_jichang_kwak),
            ("19", "Gun Park", create_enemy_gun_park_enemy),
            ("20", "Goo Kim", create_enemy_goo_kim_enemy),
            ("21", "Kim Jun-gu", create_enemy_kim_jungu_enemy),
            ("22", "Manager Kim", create_enemy_manager_kim_enemy),
            ("23", "Jinrang", create_enemy_jinrang_enemy),
            ("24", "Jaegyeon Na", create_enemy_jaegyeon_na_enemy),
            ("25", "Charles Choi", create_enemy_charles_choi),
            ("26", "Tom Lee", create_enemy_tom_lee),
            ("27", "Gapryong Kim", create_enemy_gapryong_kim),
        ]

        for key, name, _ in training_options:
            print(f"  {key}. {name}")
            time.sleep(0.02)
        print("  s. Save Game")
        print("  b. Back")
        print()

        choice = input("> ").strip()
        print()

        if choice.lower() == 'b':
            return
        if choice.lower() == 's':
            self.save_game()
            return self.training_mode()

        for key, name, func in training_options:
            if choice == key:
                print(f"\nSparring with {name}...")
                time.sleep(0.5)

                party = self.select_party(4)
                if not party:
                    party = [self.daniel, self.vasco, self.zack, self.jay]

                self.rest()
                self.battle([func()], party)
                break

    def stats_mode(self):
        print("\n" + "=" * 110)
        slow_print("📊 STATISTICS & RECORDS 📊", 0.04)
        print("=" * 110)

        print(f"🏆 Total Victories: {self.victories}")
        print(f"💀 Enemies Defeated: {self.total_kills}")
        print(f"⚔️ Battles Fought: {self.turn_count}")
        print()

        print("✦ CHARACTER PATHS:")
        for char in self.all_characters:
            is_locked = False
            if char.name in self.unlocked_characters:
                if not self.unlocked_characters[char.name]:
                    is_locked = True

            if char.path and not is_locked:
                print(f"  • {char.name}: Lv.{char.path_level} ({char.path_exp}/100 EXP)")
            elif is_locked:
                print(f"  • {char.name}: 🔒 {self.unlock_requirements.get(char.name, 'Locked')}")
            else:
                print(f"  • {char.name}: No path chosen")
        print()

        print("🔓 UNLOCK PROGRESS:")
        for name, unlocked in self.unlocked_characters.items():
            status = "✅ UNLOCKED" if unlocked else "🔒 Locked"
            print(f"  • {name}: {status}")

        input("\nPress Enter to return to menu...")
        print()


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    print("\n" + "=" * 110)
    slow_print("    👊👊👊 LOOKISM: AWAKENED FIST 👊👊👊", 0.03)
    print("    COMPLETE CANON EDITION - 51 PLAYABLE FIGHTERS")
    print("    Based on Park Tae-joon's Lookism (2014-2025)")
    print("=" * 110)
    print("\n✅ ROSTER BREAKDOWN:")
    print("   • GEN 0 (5): Gapryong Kim, Tom Lee, Charles Choi, Jinyoung Park, Baekho")
    print(
        "   • 1ST GEN (9): James Lee, Gitae Kim, Jichang Kwak, Taesoo Ma, Gongseob Ji, Seokdu Wang, Jaegyeon Na, Seongji Yuk, Jinrang")
    print(
        "   • GEN 2 (15): Daniel Park, Zack Lee, Johan Seong, Vasco, Jay Hong, Eli Jang, Warren Chae, Jake Kim, Gun Park, Goo Kim, Kim Jun-gu, Manager Kim + more")
    print("   • WORKERS (7): Mandeok, Cap Guy, Xiaolung, Ryuhei, Samuel Seo, Sinu Han, Logan Lee")
    print("   • CHEONLIANG (3): Vin Jin, Han Jaeha, Baek Seong")
    print("   • YAMAZAKI (2): Shingen Yamazaki, Park Jonggun's Father")
    print("   • LAW (2): Kim Minjae, Detective Kang")
    print("=" * 110)
    print("\n🎮 GAME MODES:")
    time.sleep(0.3)
    print("  1. 📖 Story Mode - Complete canon story (Ep 1-581+)")
    print("  2. 🏆 Crew Gauntlet - Fight through all crews")
    print("  3. 👑 Boss Rush - Only major villains & legends")
    print("  4. ♾️ Endless Survival - How many waves?")
    print("  5. 🥋 Training Room - Practice against any character")
    print("  6. 📊 Stats & Records")
    print("  7. 🛤️ Path Management - Change character paths anytime")
    print("  8. 💾 Save/Load - Manage your save file")
    print("  9. ❌ Exit")
    print("=" * 110)
    time.sleep(1)

    # Check for existing save
    if os.path.exists(SAVE_FILE):
        print("\n💾 Existing save file found!")
        load_choice = input("Load previous game? (y/n): ").lower()
        if load_choice == 'y':
            game = LookismGame(load_saved=True)
            print("✅ Game loaded successfully!")
        else:
            game = LookismGame(load_saved=False)
            print("🆕 Starting new game...")
    else:
        game = LookismGame(load_saved=False)
        print("🆕 No save file found. Starting new game...")

    time.sleep(1)

    while True:
        print("\n" + "-" * 110)
        print("✦ MAIN MENU ✦")
        print("-" * 110)
        print("1. 📖 Story Mode")
        print("2. 🏆 Crew Gauntlet")
        print("3. 👑 Boss Rush")
        print("4. ♾️ Endless Survival")
        print("5. 🥋 Training Room")
        print("6. 📊 Stats & Records")
        print("7. 🛤️ Path Management - Change paths anytime")
        print("8. 💾 Save/Load - Manage your save file")
        print("9. ❌ Exit")
        print("-" * 110)

        choice = input("> ").strip()
        print()

        if choice == "1":
            game.story_mode()
        elif choice == "2":
            game.crew_gauntlet_mode()
        elif choice == "3":
            game.boss_rush_mode()
        elif choice == "4":
            game.survival_mode()
        elif choice == "5":
            game.training_mode()
        elif choice == "6":
            game.stats_mode()
        elif choice == "7":
            game.path_management_menu()
        elif choice == "8":
            print("\n" + "=" * 110)
            slow_print("💾💾💾 SAVE/LOAD MANAGEMENT 💾💾💾", 0.03)
            print("=" * 110)
            print("1. 💾 Save Game")
            print("2. 📂 Load Game")
            print("3. 🗑️ Delete Save")
            print("4. 🔙 Back")
            print("-" * 110)

            save_choice = input("> ").strip()
            if save_choice == "1":
                game.save_game()
            elif save_choice == "2":
                if game.load_game():
                    print("✅ Game loaded!")
                else:
                    print("❌ No save file found!")
            elif save_choice == "3":
                confirm = input("Are you sure you want to delete your save? (y/n): ").lower()
                if confirm == 'y':
                    if SaveSystem.delete_save():
                        print("🗑️ Save file deleted!")
                        game = LookismGame(load_saved=False)
                    else:
                        print("❌ No save file found!")
            input("Press Enter to continue...")
        elif choice == "9":
            save_choice = input("Save before exiting? (y/n): ").lower()
            if save_choice == 'y':
                game.save_game()
            slow_print("\nThanks for playing Lookism: Awakened Fist!", 0.03)
            slow_print("See you next time, fighter.\n", 0.03)
            time.sleep(1)
            break
        else:
            print("❌ Invalid choice.")
            time.sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)