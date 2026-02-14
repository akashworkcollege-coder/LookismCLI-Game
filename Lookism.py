#!/usr/bin/env python3
"""
LOOKISM: AWAKENED FIST - COMPLETE CANON EDITION
FULLY FIXED VERSION - No healing abilities, pure combat!
BUTTONS REMAPPED TO NUMBERS - Easier input!
100% Manhwa Accurate • Based on Park Tae-joon's Lookism (2014-2025)
"""

import random
import time
import sys
from enum import Enum

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
# PATH SYSTEM
# ============================================================================

class Path(Enum):
    # Daniel Park
    ULTRA_INSTINCT = "👁️ Ultra Instinct - The body fights on its own"
    COPY_MASTER = "⚡ Copy Master - Perfect replication of any technique"
    SECOND_BODY = "🔄 Dual Vessel - Master of both bodies"
    HERO_PATH = "👊 Hero of Justice - Inherit Vasco's will"
    UI_MASTER = "👑 UI Master - Voluntary control over Ultra Instinct"

    # Johan Seong
    GOD_EYE = "👁️ God Eye - Perfect copy, sees through all techniques"
    CHOREOGRAPHY = "💃 Dance of Blades - Unique dance-based combat"
    BLIND_SAGE = "🕶️ Blind Sage - Fights without sight"
    INFINITE_COPY = "♾️ Infinity Technique - Copy without limits"

    # Vasco
    SYSTEMA_MASTER = "🇷🇺 Systema Master - Flowing Russian martial art"
    MUAY_THAI_LEGEND = "🇹🇭 Muay Thai Legend - Devastating strikes"
    BURN_KNUCKLE_KING = "🔥 Burn Knuckle King - Ultimate justice fist"

    # Zack Lee
    COUNTER_GENIUS = "⚡ Counter Genius - Perfect timing"
    SHINING_STAR = "💫 Shining Star - Ultimate one-punch finish"
    BOXING_EMPEROR = "👑 Boxing Emperor - Undisputed king of the ring"

    # Jay Hong
    SILENT_PROTECTOR = "🤫 Silent Protector - Ultimate defense"
    KALI_MASTER = "🇵🇭 Kali Master - Twin blade perfection"

    # Eli Jang
    BEAST_KING = "🦁 Beast King - Full animal instinct release"
    HOSTEL_FATHER = "👶 Father's Strength - Fights for Yenna"
    TOM_LEE_LEGACY = "🐅 Tom Lee Legacy - Inheritor of The Wild"

    # Warren Chae
    JKD_MASTER = "🥋 Jeet Kune Do Master - Bruce Lee's philosophy"
    CQC_OPERATOR = "🔫 CQC Operator - Military precision"
    NEW_CQC_CREATOR = "⚡ NEW CQC Creator - JKD + CQC hybrid"
    HEART_ATTACK = "💔 Heart Attack Punch - One-inch punch to the heart"

    # Jake Kim
    CONVICTION_KING = "⚖️ Conviction King - Willpower becomes power"
    GAPRYONG_BLOOD = "👑 Gapryong's Blood - Inheritor of legendary fist"
    BIG_DEAL_LEADER = "🤝 Big Deal Leader - Power of crew solidarity"

    # Gun Park
    YAMAZAKI_HEIR = "🏯 Yamazaki Heir - The darkness within"
    GENIUS_OF_COMBAT = "🎯 Genius of Combat - Master of 4+ martial arts"
    ULTRA_INSTINCT_CONSTANT = "👁️ Constant UI - Permanent Ultra Instinct"
    BLACK_BONE = "🖤 Black Bone - Ultimate Yamazaki technique"

    # Goo Kim
    MOONLIGHT_SWORD = "🌙 Moonlight Sword - Legendary 50 Moonlight Style"
    MAKESHIFT_MASTER = "🖊️ Makeshift Master - Any object becomes deadly"
    FIFTH_SWORD = "✨ Fifth Sword - Technique thought impossible"

    # Kim Jun-gu
    HWARANG_SWORD = "⚔️ Hwarang Sword - Cuts even goblins"
    IMPROVISED_WEAPON = "🔗 Improvised Weapon Master"
    ARMED_BEAST = "🗡️ Armed Beast - Top 3 in the verse when armed"

    # Jinrang
    GAPRYONG_DISCIPLE = "👑 Gapryong's Disciple - True conviction"
    BUSAN_KING = "🏆 King of Busan - Ruler of the south"

    # Jaegyeon Na
    INCHEON_SPEED = "🔵 Incheon Speed - Fastest man in Korea"
    BETRAYER = "🗡️ Betrayer - Traitor's strength"

    # Manager Kim
    SPECIAL_FORCES = "🎖️ Special Forces - Former black ops, Code 66"
    PROTECTIVE_FATHER = "👨‍👧 Protective Father - Fights for Minji, unstoppable"
    CQC_MASTER = "🔫 CQC Master - Close Quarter Combat perfection"


# ============================================================================
# INFINITY TECHNIQUES DATABASE
# ============================================================================

INFINITY_TECHNIQUES = {
    # Daniel Park
    Path.ULTRA_INSTINCT: {
        "name": "👁️ INFINITE UI: White God",
        "cost": 120,
        "dmg": (200, 300),
        "desc": "The pinnacle of Ultra Instinct. White hair flows endlessly. Perfect evasion, perfect counter, perfect strike."
    },
    Path.COPY_MASTER: {
        "name": "⚡ INFINITE COPY: Omni-Directional Replication",
        "cost": 110,
        "dmg": (180, 270),
        "desc": "Daniel copies EVERY technique he has ever seen simultaneously."
    },
    Path.SECOND_BODY: {
        "name": "🔄 INFINITE SWITCH: Dual Existence",
        "cost": 100,
        "dmg": (170, 250),
        "desc": "Daniel and his second body fight as one. Two perspectives, infinite possibilities."
    },
    Path.HERO_PATH: {
        "name": "👊 INFINITE JUSTICE: Hero's Conviction",
        "cost": 100,
        "dmg": (160, 240),
        "desc": "Daniel inherits Vasco's will. Justice compressed into infinite fists."
    },
    Path.UI_MASTER: {
        "name": "👑 INFINITE MASTERY: Voluntary God",
        "cost": 130,
        "dmg": (220, 330),
        "desc": "Voluntary control over Ultra Instinct. White hair at will."
    },

    # Johan Seong
    Path.GOD_EYE: {
        "name": "👁️ INFINITE GOD EYE: Omniscient Copy",
        "cost": 120,
        "dmg": (190, 280),
        "desc": "Sees through all techniques, past, present, and future. Copy without limit."
    },
    Path.CHOREOGRAPHY: {
        "name": "💃 INFINITE CHOREOGRAPHY: Final Performance",
        "cost": 110,
        "dmg": (180, 270),
        "desc": "A flawless sequence of 1000 strikes from every conceivable angle."
    },
    Path.BLIND_SAGE: {
        "name": "🕶️ INFINITE BLINDNESS: Sight Beyond Sight",
        "cost": 100,
        "dmg": (170, 260),
        "desc": "Johan transcends his blindness. He feels the air, hears the heartbeat."
    },
    Path.INFINITE_COPY: {
        "name": "♾️ INFINITE TECHNIQUE: Transcendent God Eye",
        "cost": 130,
        "dmg": (210, 320),
        "desc": "Copy without seeing. Copy without existing. Creates techniques that never existed."
    },

    # Vasco
    Path.SYSTEMA_MASTER: {
        "name": "🇷🇺 INFINITE SYSTEMA: Russian Winter",
        "cost": 100,
        "dmg": (150, 230),
        "desc": "Flowing like water, unpredictable like wind. The art of the Russian special forces."
    },
    Path.MUAY_THAI_LEGEND: {
        "name": "🇹🇭 INFINITE MUAY THAI: Death Blow of the Gods",
        "cost": 110,
        "dmg": (170, 260),
        "desc": "Shin becomes a blade, elbow a spear, knee a battering ram."
    },
    Path.BURN_KNUCKLE_KING: {
        "name": "🔥 INFINITE BURN KNUCKLES: Sunken Fist of Apocalypse",
        "cost": 100,
        "dmg": (160, 250),
        "desc": "Justice manifests as pure destructive power."
    },

    # Zack Lee
    Path.COUNTER_GENIUS: {
        "name": "⚡ INFINITE COUNTER: Zero Reaction Time",
        "cost": 90,
        "dmg": (140, 220),
        "desc": "The moment an attack is thrown, Zack's fist has already landed."
    },
    Path.SHINING_STAR: {
        "name": "💫 INFINITE SHINING STAR: Supernova",
        "cost": 100,
        "dmg": (160, 250),
        "desc": "A single punch containing every ounce of his being. For Mira."
    },
    Path.BOXING_EMPEROR: {
        "name": "👑 INFINITE BOXING: Undisputed",
        "cost": 95,
        "dmg": (150, 240),
        "desc": "Zack transcends boxing itself. He IS boxing."
    },

    # Jay Hong
    Path.SILENT_PROTECTOR: {
        "name": "🤫 INFINITE SILENCE: Guardian Angel",
        "cost": 90,
        "dmg": (0, 0),
        "desc": "Jay becomes Daniel's shadow, taking all damage for him."
    },
    Path.KALI_MASTER: {
        "name": "🇵🇭 INFINITE KALI: Blade Storm",
        "cost": 95,
        "dmg": (150, 230),
        "desc": "Twin blades become a whirlwind of destruction."
    },

    # Eli Jang
    Path.BEAST_KING: {
        "name": "🦁 INFINITE BEAST: King of the Jungle",
        "cost": 110,
        "dmg": (170, 260),
        "desc": "Eli fully surrenders to his animal instincts. No wasted movement."
    },
    Path.HOSTEL_FATHER: {
        "name": "👶 INFINITE FATHER: Yenna's Smile",
        "cost": 120,
        "dmg": (190, 290),
        "desc": "For Yenna's future, Eli surpasses every limit. A father's love is infinite."
    },
    Path.TOM_LEE_LEGACY: {
        "name": "🐅 INFINITE WILD: Tom Lee's Successor",
        "cost": 100,
        "dmg": (160, 250),
        "desc": "The Wild, passed down from Gen 0, flows through Eli's veins."
    },

    # Warren Chae
    Path.JKD_MASTER: {
        "name": "🥋 INFINITE JKD: Bruce Lee's Spirit",
        "cost": 90,
        "dmg": (140, 220),
        "desc": "Be water, my friend. Formless, shapeless, yet overwhelming."
    },
    Path.CQC_OPERATOR: {
        "name": "🔫 INFINITE CQC: Manager Kim's Legacy",
        "cost": 100,
        "dmg": (150, 240),
        "desc": "Military precision. Maximum efficiency. Minimum movement."
    },
    Path.NEW_CQC_CREATOR: {
        "name": "⚡ INFINITE NEW CQC: The Uncopyable",
        "cost": 120,
        "dmg": (180, 280),
        "desc": "JKD + CQC = a style with NO DISCERNIBLE PATTERN. Even Johan cannot copy it."
    },
    Path.HEART_ATTACK: {
        "name": "💔 INFINITE HEART: Cardiac Arrest",
        "cost": 110,
        "dmg": (170, 270),
        "desc": "One-inch punch to the heart. Bypasses all durability."
    },

    # Jake Kim
    Path.CONVICTION_KING: {
        "name": "⚖️ INFINITE CONVICTION: Unshakeable Will",
        "cost": 100,
        "dmg": (160, 250),
        "desc": "Jake's will becomes absolute. Mind over matter."
    },
    Path.GAPRYONG_BLOOD: {
        "name": "👑 INFINITE GAPRYONG: Legend's Return",
        "cost": 120,
        "dmg": (200, 300),
        "desc": "For a moment, Gapryong Kim stands again. The legendary fist."
    },
    Path.BIG_DEAL_LEADER: {
        "name": "🤝 INFINITE BIG DEAL: Crew Solidarity",
        "cost": 90,
        "dmg": (140, 230),
        "desc": "Jerry's loyalty, Brad's courage - they all flow through him."
    },

    # Gun Park
    Path.YAMAZAKI_HEIR: {
        "name": "🏯 INFINITE YAMAZAKI: Shingen's Shadow",
        "cost": 130,
        "dmg": (220, 330),
        "desc": "The darkness within becomes unlimited power."
    },
    Path.GENIUS_OF_COMBAT: {
        "name": "🎯 INFINITE GENIUS: Martial God",
        "cost": 120,
        "dmg": (200, 310),
        "desc": "All martial arts are expressions of one truth: Gun Park is the strongest."
    },
    Path.ULTRA_INSTINCT_CONSTANT: {
        "name": "👁️ INFINITE UI: Permanent Awakening",
        "cost": 140,
        "dmg": (240, 360),
        "desc": "Permanent, voluntary Ultra Instinct. His hair is perpetually white."
    },
    Path.BLACK_BONE: {
        "name": "🖤 INFINITE BLACK BONE: Yamazaki's Wrath",
        "cost": 150,
        "dmg": (260, 400),
        "desc": "Ultimate technique passed down through generations of Yamazaki."
    },

    # Goo Kim
    Path.MOONLIGHT_SWORD: {
        "name": "🌙 INFINITE MOONLIGHT: Total Lunar Eclipse",
        "cost": 120,
        "dmg": (190, 290),
        "desc": "All five Moonlight Sword techniques simultaneously."
    },
    Path.MAKESHIFT_MASTER: {
        "name": "🖊️ INFINITE MAKESHIFT: Everything is a Sword",
        "cost": 100,
        "dmg": (160, 250),
        "desc": "In his hands, the air itself becomes a blade."
    },
    Path.FIFTH_SWORD: {
        "name": "✨ INFINITE FIFTH: Technique Beyond God",
        "cost": 150,
        "dmg": (270, 400),
        "desc": "The technique thought impossible. It cuts through reality itself."
    },

    # Kim Jun-gu
    Path.HWARANG_SWORD: {
        "name": "⚔️ INFINITE HWARANG: Goblin Slayer",
        "cost": 130,
        "dmg": (210, 320),
        "desc": "The legendary blade that cuts even goblins."
    },
    Path.IMPROVISED_WEAPON: {
        "name": "🔗 INFINITE IMPROVISATION: Everything is Lethal",
        "cost": 110,
        "dmg": (180, 280),
        "desc": "A pen, a chain, a spring - all weapons."
    },
    Path.ARMED_BEAST: {
        "name": "🗡️ INFINITE ARMED: Top 3 in the Verse",
        "cost": 140,
        "dmg": (250, 380),
        "desc": "Fully armed, Jun-gu takes his place among the three strongest."
    },

    # Jinrang
    Path.GAPRYONG_DISCIPLE: {
        "name": "👑 INFINITE DISCIPLE: True Conviction",
        "cost": 140,
        "dmg": (230, 350),
        "desc": "Jinrang proves he is Gapryong's TRUE disciple."
    },
    Path.BUSAN_KING: {
        "name": "🏆 INFINITE KING: Ruler of the South",
        "cost": 130,
        "dmg": (210, 330),
        "desc": "Jinrang solidifies his reign as the King of Busan."
    },

    # Jaegyeon Na
    Path.INCHEON_SPEED: {
        "name": "🔵 INFINITE SPEED: Faster Than Light",
        "cost": 110,
        "dmg": (170, 270),
        "desc": "He does not move - he simply arrives."
    },
    Path.BETRAYER: {
        "name": "🗡️ INFINITE BETRAYAL: No Hesitation",
        "cost": 100,
        "dmg": (160, 260),
        "desc": "No loyalty, no guilt, no hesitation. The traitor's path."
    },

    # Manager Kim
    Path.SPECIAL_FORCES: {
        "name": "🎖️ INFINITE SPECIAL FORCES: Code 66",
        "cost": 130,
        "dmg": (210, 320),
        "desc": "Former black ops and special forces member. Two units were dedicated to him. His combat experience is unmatched."
    },
    Path.PROTECTIVE_FATHER: {
        "name": "👨‍👧 INFINITE FATHER: For Minji",
        "cost": 140,
        "dmg": (240, 360),
        "desc": "When his daughter Minji is threatened, Manager Kim becomes unstoppable. He will destroy everything in his path."
    },
    Path.CQC_MASTER: {
        "name": "🔫 INFINITE CQC: White Tiger's Finest",
        "cost": 120,
        "dmg": (190, 290),
        "desc": "Close Quarter Combat perfected through decades of experience. Every strike hits a vital point. Every movement is lethal."
    }
}


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
            self.path = path
            self.infinity_technique = INFINITY_TECHNIQUES.get(path)
            if self.infinity_technique:
                return f"\n✨✨✨ {self.name} walks the path of {path.value} ✨✨✨\n\n{self.infinity_technique['desc']}\n"
            return f"\n{self.name} walks the path of {path.value}\n"
        return f"\n{path} is not available for {self.name}\n"


# ============================================================================
# DANIEL PARK
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

        self.paths_available = [
            Path.ULTRA_INSTINCT,
            Path.COPY_MASTER,
            Path.SECOND_BODY,
            Path.HERO_PATH,
            Path.UI_MASTER
        ]

        self._load_abilities()

    def _load_abilities(self):
        self.abilities['1'] = {
            "name": "👊 Desperate Flailing",
            "cost": 10,
            "dmg": (20, 35),
            "type": "damage",
            "desc": "EP 1-50: Daniel has NO fighting skill. Pure desperation."
        }
        self.abilities['2'] = {
            "name": "🔄 Instinctive Copy",
            "cost": 20,
            "dmg": (30, 50),
            "type": "damage",
            "desc": "EP 50-100: Subconscious copying. Unreliable, low accuracy."
        }
        self.abilities['3'] = {
            "name": "🇷🇺 Systema: Ryabina",
            "cost": 25,
            "dmg": (50, 70),
            "type": "damage",
            "desc": "EP 150: Learned from Sophia. Russian martial art."
        }
        self.abilities['4'] = {
            "name": "🇷🇺 Systema: Otmashka",
            "cost": 30,
            "dmg": (60, 85),
            "type": "damage",
            "desc": "Swing-through strike. Maximum momentum."
        }
        self.abilities['5'] = {
            "name": "⚡ Copy: Zack's Counter",
            "cost": 25,
            "dmg": (55, 80),
            "type": "damage",
            "desc": "Perfect counter timing."
        }
        self.abilities['6'] = {
            "name": "⚡ Copy: Vasco's Sunken Fist",
            "cost": 30,
            "dmg": (65, 90),
            "type": "damage",
            "desc": "Justice compressed into a fist."
        }
        self.abilities['7'] = {
            "name": "⚡ Copy: Eli's Animal Instinct",
            "cost": 30,
            "dmg": (70, 95),
            "type": "damage",
            "desc": "Wild, efficient. No wasted movement."
        }
        self.abilities['8'] = {
            "name": "⚡ Copy: Jake's Conviction",
            "cost": 35,
            "dmg": (75, 105),
            "type": "damage",
            "desc": "Willpower becomes power."
        }
        self.abilities['9'] = {
            "name": "⚡ Copy: Johan's Choreography",
            "cost": 40,
            "dmg": (80, 115),
            "type": "damage",
            "desc": "Dance-like combat. Unpredictable angles."
        }
        self.abilities['10'] = {
            "name": "⚡ Copy: Gun's Taekwondo",
            "cost": 35,
            "dmg": (80, 110),
            "type": "damage",
            "desc": "Perfect spinning back kick."
        }
        self.abilities['11'] = {
            "name": "⚡ Copy: Goo's Sword Style",
            "cost": 40,
            "dmg": (85, 120),
            "type": "damage",
            "desc": "Makeshift sword. Any object becomes deadly."
        }
        self.abilities['12'] = {
            "name": "🩷 Jichang's Hand Blade",
            "cost": 45,
            "dmg": (90, 130),
            "type": "damage",
            "desc": "Knife-hand strike. CANNOT DAMAGE JINRANG."
        }
        self.abilities['13'] = {
            "name": "👑 Gapryong's Conviction",
            "cost": 60,
            "dmg": (120, 180),
            "type": "damage",
            "desc": "The legendary punch. DOES NOT WORK ON JINRANG."
        }
        self.abilities['14'] = {"name": "🔵 Realm of Speed", "cost": 50, "dmg": (0, 0), "type": "realm"}
        self.abilities['15'] = {"name": "🔴 Realm of Strength", "cost": 50, "dmg": (0, 0), "type": "realm"}
        self.abilities['16'] = {"name": "🟢 Realm of Tenacity", "cost": 50, "dmg": (0, 0), "type": "realm"}
        self.abilities['17'] = {"name": "🩷 Realm of Technique", "cost": 50, "dmg": (0, 0), "type": "realm"}
        self.abilities['18'] = {"name": "🟣 Realm of Overcoming", "cost": 50, "dmg": (0, 0), "type": "realm"}
        self.abilities['19'] = {
            "name": "👁️ Ultra Instinct",
            "cost": 100,
            "dmg": (0, 0),
            "type": "ui",
            "desc": "WHITE HAIR AWAKENING. Body fights on its own. Perfect evasion."
        }

    def activate_ui(self):
        self.ui_mode = True
        self.ui_timer = 3
        self.form = "ULTRA INSTINCT"
        self.hp = min(self.max_hp, self.hp + 50)
        return "👁️👁️👁️👁️👁️ ULTRA INSTINCT! White hair awakens! Perfect evasion!"

    def get_damage_multiplier(self):
        mult = 1.0
        buffs = []
        if self.active_realm == Realm.STRENGTH:
            mult *= 1.7
            buffs.append("🔴 STRENGTH")
        elif self.active_realm == Realm.OVERCOMING and self.hp < self.max_hp * 0.3:
            mult *= 2.0
            buffs.append("🟣 OVERCOMING")
        if self.ui_mode:
            mult *= 2.5
            buffs.append("👁️ ULTRA INSTINCT")
        return mult, buffs


# ============================================================================
# ZACK LEE - THE IRON BOXER
# ============================================================================

class ZackLee(Character):
    def __init__(self):
        super().__init__(
            "Zack Lee",
            "The Iron Boxer",
            380, 280,
            [Realm.SPEED]
        )

        self.canon_episode = 1
        self.paths_available = [Path.COUNTER_GENIUS, Path.SHINING_STAR, Path.BOXING_EMPEROR]
        self.footwork_active = False
        self.footwork_timer = 0
        self.heat_mode = False
        self.heat_timer = 0

        self.abilities['1'] = {
            "name": "🥊 Jab",
            "cost": 15,
            "dmg": (35, 55),
            "type": "damage",
            "desc": "Lightning fast lead punch. Sets up combinations. Classic outboxer technique."
        }
        self.abilities['2'] = {
            "name": "🥊 Cross",
            "cost": 20,
            "dmg": (45, 70),
            "type": "damage",
            "desc": "Powerful rear straight. Speed is Zack's specialty."
        }
        self.abilities['3'] = {
            "name": "🥊 Hook",
            "cost": 20,
            "dmg": (50, 75),
            "type": "damage",
            "desc": "Devastating curved punch. Rarely targets the body, focuses on head shots."
        }
        self.abilities['4'] = {
            "name": "🥊 Uppercut",
            "cost": 25,
            "dmg": (55, 80),
            "type": "damage",
            "desc": "Explosive rising strike. Keeps opponents at range."
        }
        self.abilities['5'] = {
            "name": "🥊 1-2-3 Combo",
            "cost": 30,
            "dmg": (70, 100),
            "type": "damage",
            "desc": "Jab, cross, hook. Classic boxing combination. Quick combos are Zack's specialty."
        }
        self.abilities['6'] = {
            "name": "⚡ Counter Punch",
            "cost": 30,
            "dmg": (75, 110),
            "type": "damage",
            "desc": "Perfect timing counter. Double damage if enemy attacked. Zack's timing is legendary."
        }
        self.abilities['7'] = {
            "name": "🔄 Hit and Run",
            "cost": 25,
            "dmg": (50, 75),
            "type": "damage",
            "desc": "Outboxer style. Strike then evade. Minimizes time in opponent's range."
        }
        self.abilities['8'] = {
            "name": "🛡️ Philly Shell",
            "cost": 20,
            "dmg": (0, 0),
            "type": "utility",
            "desc": "Mayweather-style defense. Deflects punches with shoulder. -40% damage next turn."
        }
        self.abilities['9'] = {
            "name": "🏃 Footwork",
            "cost": 20,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "Superior boxing movement. +25% evasion (3 turns). Speed is everything."
        }
        self.abilities['10'] = {
            "name": "💫 Shining Star",
            "cost": 50,
            "dmg": (100, 150),
            "type": "damage",
            "desc": "Zack's ultimate technique. All his power in one perfect punch. For Mira."
        }
        self.abilities['11'] = {
            "name": "❤️ For Mira",
            "cost": 35,
            "dmg": (85, 120),
            "type": "damage",
            "desc": "Power increases when protecting Mira. A boxer's pride fuels his strikes."
        }
        self.abilities['12'] = {
            "name": "🔥 Heat Mode",
            "cost": 45,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "Activates when feeling self-hatred. Body becomes hot, heart feels like bursting. +50% damage, adaptive fighting (3 turns)."
        }


# ============================================================================
# JOHAN SEONG
# ============================================================================

class JohanSeong(Character):
    def __init__(self, blind=True):
        super().__init__(
            "Johan Seong",
            "The God Eye",
            400, 300,
            [Realm.TECHNIQUE, Realm.SPEED]
        )

        self.canon_episode = 100
        self.blind = blind
        self.god_eye_active = False

        self.paths_available = [
            Path.GOD_EYE,
            Path.CHOREOGRAPHY,
            Path.BLIND_SAGE,
            Path.INFINITE_COPY
        ]

        self._load_abilities()

    def _load_abilities(self):
        self.abilities['1'] = {
            "name": "👁️ Copy: Taekwondo",
            "cost": 20,
            "dmg": (50, 75),
            "type": "damage",
            "desc": "Perfect Gun-style Taekwondo."
        }
        self.abilities['2'] = {
            "name": "👁️ Copy: Karate",
            "cost": 20,
            "dmg": (50, 75),
            "type": "damage",
            "desc": "Perfect Kyokushin Karate."
        }
        self.abilities['3'] = {
            "name": "👁️ Copy: Boxing",
            "cost": 20,
            "dmg": (50, 75),
            "type": "damage",
            "desc": "Perfect Boxing. Counter-specialist."
        }
        self.abilities['4'] = {
            "name": "👁️ Copy: Capoeira",
            "cost": 20,
            "dmg": (50, 75),
            "type": "damage",
            "desc": "Perfect Capoeira. Flowing, evasive."
        }
        self.abilities['5'] = {
            "name": "💃 Choreography",
            "cost": 40,
            "dmg": (85, 120),
            "type": "damage",
            "desc": "Johan's signature. Dance-like combat."
        }
        self.abilities['6'] = {
            "name": "💃 Choreography: Finale",
            "cost": 60,
            "dmg": (110, 160),
            "type": "damage",
            "desc": "The climax of Johan's dance."
        }
        self.abilities['7'] = {
            "name": "👁️ God Eye",
            "cost": 45,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "Johan's copy talent peaks. +50% damage."
        }
        if self.blind:
            self.abilities['8'] = {
                "name": "🕶️ Blindness",
                "cost": 0,
                "dmg": (0, 0),
                "type": "passive",
                "desc": "CANON: Johan went blind. 30% accuracy penalty."
            }
            self.abilities['9'] = {
                "name": "🕶️ Blind Fighting",
                "cost": 30,
                "dmg": (70, 100),
                "type": "damage",
                "desc": "Johan fights despite blindness."
            }
        self.abilities['10'] = {
            "name": "🕊️ Mira's Memory",
            "cost": 35,
            "dmg": (80, 115),
            "type": "damage",
            "desc": "Johan remembers why he started fighting."
        }
        self.form = "Blind" if self.blind else "God Eye"


# ============================================================================
# VASCO
# ============================================================================

class Vasco(Character):
    def __init__(self):
        super().__init__(
            "Vasco",
            "The Hero of Justice",
            450, 260,
            [Realm.STRENGTH, Realm.TENACITY]
        )

        self.canon_episode = 1
        self.muscle_boost = False
        self.boost_timer = 0
        self.muay_thai_learned = True

        self.paths_available = [
            Path.SYSTEMA_MASTER,
            Path.MUAY_THAI_LEGEND,
            Path.BURN_KNUCKLE_KING
        ]

        self._load_abilities()

    def _load_abilities(self):
        self.abilities['1'] = {
            "name": "🇷🇺 Systema: Ryabina",
            "cost": 20,
            "dmg": (50, 70),
            "type": "damage",
            "desc": "PRIMARY: 'Rowan Tree'. Flowing, circular strikes."
        }
        self.abilities['2'] = {
            "name": "🇷🇺 Systema: Perelesnik",
            "cost": 25,
            "dmg": (55, 80),
            "type": "damage",
            "desc": "'Whirlwind'. Continuous spinning attacks."
        }
        self.abilities['3'] = {
            "name": "🇷🇺 Systema: Otmashka",
            "cost": 30,
            "dmg": (65, 90),
            "type": "damage",
            "desc": "Swing-through strike. Maximum momentum."
        }
        self.abilities['4'] = {
            "name": "🇷🇺 Russian Cross",
            "cost": 35,
            "dmg": (75, 105),
            "type": "damage",
            "desc": "Vasco's signature Systema technique."
        }
        self.abilities['5'] = {
            "name": "🇹🇭 Muay Thai: Roundhouse",
            "cost": 25,
            "dmg": (60, 85),
            "type": "damage",
            "desc": "SECONDARY: Shin-based kick."
        }
        self.abilities['6'] = {
            "name": "🇹🇭 Muay Thai: Death Blow",
            "cost": 40,
            "dmg": (90, 130),
            "type": "damage",
            "desc": "Vasco's ultimate Muay Thai technique."
        }
        self.abilities['7'] = {
            "name": "👊 Sunken Fist",
            "cost": 30,
            "dmg": (70, 100),
            "type": "damage",
            "desc": "Justice compressed into a single fist."
        }
        self.abilities['8'] = {
            "name": "🔥 Burn Knuckles Combo",
            "cost": 35,
            "dmg": (75, 110),
            "type": "damage",
            "desc": "Relentless barrage. Justice never stops."
        }
        self.abilities['9'] = {
            "name": "🏃 Run Over",
            "cost": 30,
            "dmg": (65, 95),
            "type": "damage",
            "desc": "Charges forward with overwhelming momentum."
        }
        self.abilities['10'] = {
            "name": "🛡️ Protect the Weak",
            "cost": 25,
            "dmg": (0, 0),
            "type": "utility",
            "desc": "Vasco takes damage for an ally. -70% damage."
        }
        self.abilities['11'] = {
            "name": "💪 Muscle Enhancement",
            "cost": 30,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "Intense training results. +30% damage (5 turns)."
        }

    def get_damage_multiplier(self):
        mult = 1.0
        buffs = []
        if self.muscle_boost:
            mult *= 1.3
            buffs.append("💪 MUSCLE")
        return mult, buffs


# ============================================================================
# JAY HONG
# ============================================================================

class JayHong(Character):
    def __init__(self):
        super().__init__(
            "Jay Hong",
            "The Silent Blade",
            380, 270,
            [Realm.TECHNIQUE, Realm.SPEED]
        )

        self.canon_episode = 1
        self.paths_available = [Path.SILENT_PROTECTOR, Path.KALI_MASTER]

        self.abilities['1'] = {
            "name": "🇷🇺 Systema: Neutralizer",
            "cost": 20,
            "dmg": (45, 65),
            "type": "damage",
            "desc": "Redirectional. Turns opponent's force against them."
        }
        self.abilities['2'] = {
            "name": "🇷🇺 Systema: Breaker",
            "cost": 25,
            "dmg": (50, 75),
            "type": "damage",
            "desc": "Joint strikes and pressure points."
        }
        self.abilities['3'] = {
            "name": "🇷🇺 Systema: Medved",
            "cost": 30,
            "dmg": (60, 85),
            "type": "damage",
            "desc": "'The Bear'. Overwhelming forward pressure."
        }
        self.abilities['4'] = {
            "name": "🇵🇭 Kali: Double Baston",
            "cost": 25,
            "dmg": (50, 75),
            "type": "damage",
            "desc": "Twin stick fighting. Uses motorcycle helmet."
        }
        self.abilities['5'] = {
            "name": "🇵🇭 Kali: Espada y Daga",
            "cost": 35,
            "dmg": (70, 95),
            "type": "damage",
            "desc": "Sword and dagger style."
        }
        self.abilities['6'] = {
            "name": "🛡️ Motorcycle Helmet",
            "cost": 15,
            "dmg": (0, 0),
            "type": "utility",
            "desc": "Reduces damage by 50%."
        }
        self.abilities['7'] = {
            "name": "💝 Gift",
            "cost": 20,
            "dmg": (0, 0),
            "type": "utility",
            "desc": "Jay gives Daniel expensive clothes. No healing, just encouragement."
        }
        self.abilities['8'] = {
            "name": "🐶 Inu's Puppies",
            "cost": 25,
            "dmg": (0, 0),
            "type": "utility",
            "desc": "Puppies distract enemies. 50% stun chance."
        }
        self.abilities['9'] = {
            "name": "🩷 Silence",
            "cost": 0,
            "dmg": (0, 0),
            "type": "passive",
            "desc": "Jay does NOT speak. Immune to taunt. 10% evasion."
        }


# ============================================================================
# ELI JANG
# ============================================================================

class EliJang(Character):
    def __init__(self):
        super().__init__(
            "Eli Jang",
            "The Wild",
            410, 260,
            [Realm.TECHNIQUE]
        )

        self.canon_episode = 150
        self.paths_available = [Path.BEAST_KING, Path.HOSTEL_FATHER, Path.TOM_LEE_LEGACY]
        self.beast_mode = False
        self.beast_timer = 0

        self.abilities['1'] = {"name": "🐺 Wolf Strike", "cost": 20, "dmg": (50, 75), "type": "damage"}
        self.abilities['2'] = {"name": "🦅 Talon Kick", "cost": 25, "dmg": (60, 85), "type": "damage"}
        self.abilities['3'] = {"name": "🐍 Viper Punch", "cost": 25, "dmg": (60, 90), "type": "damage"}
        self.abilities['4'] = {"name": "🐅 Tiger Claw", "cost": 30, "dmg": (70, 100), "type": "damage"}
        self.abilities['5'] = {
            "name": "🦁 Beast Mode",
            "cost": 45,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "+60% damage, +40% evasion (3 turns)."
        }
        self.abilities['6'] = {
            "name": "👴 Tom Lee Special",
            "cost": 40,
            "dmg": (85, 125),
            "type": "damage",
            "desc": "Taught by Gen 0 legend Tom Lee."
        }
        self.abilities['7'] = {
            "name": "👶 For Yenna",
            "cost": 50,
            "dmg": (100, 150),
            "type": "damage",
            "desc": "Eli's daughter. His ultimate motivation."
        }
        self.abilities['8'] = {"name": "🏚️ Hostel Leader", "cost": 35, "dmg": (70, 105), "type": "damage"}
        self.abilities['9'] = {
            "name": "🛡️ Hostel Defense",
            "cost": 30,
            "dmg": (0, 0),
            "type": "utility",
            "desc": "-50% damage to allies."
        }

    def activate_beast_mode(self):
        self.beast_mode = True
        self.beast_timer = 3
        self.form = "Beast Mode"
        return "🦁🦁🦁 BEAST MODE! +60% damage, +40% evasion (3 turns)"

    def get_damage_multiplier(self):
        mult = 1.0
        if self.beast_mode:
            mult *= 1.6
        return mult, ["🦁 BEAST"] if self.beast_mode else []


# ============================================================================
# WARREN CHAE
# ============================================================================

class WarrenChae(Character):
    def __init__(self):
        super().__init__(
            "Warren Chae",
            "Gangdong's Mighty",
            390, 260,
            [Realm.STRENGTH]
        )

        self.canon_episode = 277
        self.jkd_mastery = True
        self.smk_trained = True
        self.cqc_trained = True
        self.new_cqc_unlocked = True
        self.mastery_achieved = True
        self.exhausted = False

        self.paths_available = [
            Path.JKD_MASTER,
            Path.CQC_OPERATOR,
            Path.NEW_CQC_CREATOR,
            Path.HEART_ATTACK
        ]

        self._load_abilities()

    def _load_abilities(self):
        self.abilities['1'] = {
            "name": "🥋 Jeet Kune Do: Interception",
            "cost": 20,
            "dmg": (55, 80),
            "type": "damage",
            "desc": "Self-taught through 1,000+ street fights."
        }
        self.abilities['2'] = {
            "name": "🥋 JKD: Vital Strikes",
            "cost": 25,
            "dmg": (60, 85),
            "type": "damage",
            "desc": "Attacks the weakest areas of the body."
        }
        self.abilities['3'] = {
            "name": "🥋 JKD: No Block",
            "cost": 15,
            "dmg": (0, 0),
            "type": "passive",
            "desc": "Warren never blocks. +30% damage, -20% defense."
        }
        self.abilities['4'] = {
            "name": "👴 Manager Kim's Tutelage",
            "cost": 0,
            "dmg": (0, 0),
            "type": "passive",
            "desc": "SMK corrected Warren's JKD foundation. +15% accuracy to all JKD moves."
        }
        self.abilities['5'] = {
            "name": "🦶 Silent Step",
            "cost": 15,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "Next attack has +40% critical chance."
        }
        self.abilities['6'] = {
            "name": "🔫 CQC Foundation",
            "cost": 30,
            "dmg": (70, 100),
            "type": "damage",
            "desc": "Military Close Quarter Combat."
        }
        self.abilities['7'] = {
            "name": "🔫 CQC: 3ft Radius",
            "cost": 35,
            "dmg": (75, 110),
            "type": "damage",
            "desc": "Continuous attacks. Opponent cannot escape."
        }
        self.abilities['8'] = {
            "name": "⚡ NEW CQC: Awakening",
            "cost": 50,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "NO DISCERNIBLE PATTERN. Cannot be copied."
        }
        self.abilities['9'] = {
            "name": "⚡ NEW CQC: Full Release",
            "cost": 70,
            "dmg": (120, 170),
            "type": "damage",
            "desc": "DRAWBACK: Exhausted after use."
        }
        self.abilities['10'] = {
            "name": "👑 Mastery: Overcoming",
            "cost": 45,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "Can fight 1st Generation Kings."
        }
        self.abilities['11'] = {
            "name": "💔 Heart Attack Punch",
            "cost": 60,
            "dmg": (110, 160),
            "type": "damage",
            "desc": "One-inch punch to the heart. Durability negation."
        }

    def use_new_cqc(self):
        self.exhausted = True
        return "⚡⚡⚡ NEW CQC: FULL RELEASE! Cannot act next turn!"


# ============================================================================
# JAKE KIM
# ============================================================================

class JakeKim(Character):
    def __init__(self):
        super().__init__(
            "Jake Kim",
            "The Conviction",
            430, 270,
            [Realm.OVERCOMING]
        )

        self.canon_episode = 200
        self.paths_available = [Path.CONVICTION_KING, Path.GAPRYONG_BLOOD, Path.BIG_DEAL_LEADER]
        self.conviction_mode = False

        self.abilities['1'] = {
            "name": "⚖️ Conviction Punch",
            "cost": 25,
            "dmg": (60, 85),
            "type": "damage",
            "desc": "Jake's will manifests as power."
        }
        self.abilities['2'] = {
            "name": "⚖️ Unshakeable Will",
            "cost": 30,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "+40% damage, immune to fear."
        }
        self.abilities['3'] = {
            "name": "⚖️ Conviction Mode",
            "cost": 45,
            "dmg": (0, 0),
            "type": "realm",
            "desc": "+100% damage when below 30% HP."
        }
        self.abilities['4'] = {
            "name": "🛡️ Big Deal Defense",
            "cost": 25,
            "dmg": (0, 0),
            "type": "utility",
            "desc": "-60% damage to all allies."
        }
        self.abilities['5'] = {
            "name": "🤝 Crew Solidarity",
            "cost": 30,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "Big Deal's loyalty strengthens Jake. +30% damage for 3 turns."
        }
        self.abilities['6'] = {
            "name": "🦏 Jerry's Gift",
            "cost": 20,
            "dmg": (55, 80),
            "type": "damage",
            "desc": "Jerry Kwon's loyalty strengthens Jake."
        }
        self.abilities['7'] = {
            "name": "👑 Inherited Will",
            "cost": 50,
            "dmg": (95, 140),
            "type": "damage",
            "desc": "Jake channels his father's legendary power."
        }
        self.abilities['8'] = {
            "name": "👑 Gapryong's Blood",
            "cost": 70,
            "dmg": (120, 180),
            "type": "damage",
            "desc": "The blood of the strongest."
        }
        self.abilities['9'] = {
            "name": "🥋 Gangseop's Style",
            "cost": 35,
            "dmg": (75, 110),
            "type": "damage",
            "desc": "Technique from Gapryong's disciple."
        }


# ============================================================================
# GUN PARK
# ============================================================================

class GunPark(Character):
    def __init__(self):
        super().__init__(
            "Gun Park",
            "Legend of Gen 1",
            500, 320,
            [Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE]
        )

        self.canon_episode = 300
        self.paths_available = [
            Path.YAMAZAKI_HEIR,
            Path.GENIUS_OF_COMBAT,
            Path.ULTRA_INSTINCT_CONSTANT,
            Path.BLACK_BONE
        ]
        self.permanent_ui = True
        self.form = "Ultra Instinct"

        self.abilities['1'] = {"name": "🥋 Taekwondo: Roundhouse", "cost": 20, "dmg": (65, 90), "type": "damage"}
        self.abilities['2'] = {"name": "🥋 Taekwondo: Spinning Back Kick", "cost": 30, "dmg": (80, 115),
                               "type": "damage"}
        self.abilities['3'] = {"name": "🥋 Taekwondo: 540 Kick", "cost": 40, "dmg": (95, 135), "type": "damage"}
        self.abilities['4'] = {"name": "🥋 Kyokushin: Straight", "cost": 25, "dmg": (70, 100), "type": "damage"}
        self.abilities['5'] = {"name": "🥋 Kyokushin: Tameshiwari", "cost": 35, "dmg": (85, 125), "type": "damage"}
        self.abilities['6'] = {"name": "🥋 Aikido: Irimi", "cost": 25, "dmg": (65, 95), "type": "damage"}
        self.abilities['7'] = {"name": "🥋 Aikido: Kokyu", "cost": 30, "dmg": (70, 105), "type": "damage"}
        self.abilities['8'] = {"name": "🇧🇷 Capoeira: Ginga", "cost": 25, "dmg": (60, 90), "type": "damage"}
        self.abilities['9'] = {"name": "🇧🇷 Capoeira: Armada", "cost": 35, "dmg": (80, 120), "type": "damage"}
        self.abilities['10'] = {"name": "🔨 Tonfa Strike", "cost": 30, "dmg": (75, 110), "type": "damage"}
        self.abilities['11'] = {"name": "⚡ Stun Baton", "cost": 35, "dmg": (80, 115), "type": "damage"}
        self.abilities['12'] = {"name": "🖤 Black Bone", "cost": 70, "dmg": (130, 200), "type": "damage"}
        self.abilities['13'] = {
            "name": "👁️ Ultra Instinct",
            "cost": 0,
            "dmg": (0, 0),
            "type": "passive",
            "desc": "Permanent 30% evasion, 20% counter."
        }
        self.abilities['14'] = {"name": "🏯 Yamazaki Heir", "cost": 50, "dmg": (100, 155), "type": "damage"}


# ============================================================================
# GOO KIM
# ============================================================================

class GooKim(Character):
    def __init__(self):
        super().__init__(
            "Goo Kim",
            "The Moonlight Sword",
            480, 300,
            [Realm.TECHNIQUE, Realm.SPEED]
        )

        self.canon_episode = 300
        self.paths_available = [Path.MOONLIGHT_SWORD, Path.MAKESHIFT_MASTER, Path.FIFTH_SWORD]
        self.form = "Moonlight Sword"

        self.abilities['1'] = {"name": "🖊️ Pen Sword", "cost": 15, "dmg": (45, 70), "type": "damage"}
        self.abilities['2'] = {"name": "🧹 Broom Sword", "cost": 20, "dmg": (50, 75), "type": "damage"}
        self.abilities['3'] = {"name": "🥢 Chopstick Sword", "cost": 20, "dmg": (50, 75), "type": "damage"}
        self.abilities['4'] = {"name": "📱 Phone Sword", "cost": 25, "dmg": (55, 80), "type": "damage"}
        self.abilities['5'] = {"name": "🌙 First Sword: Early Moon", "cost": 30, "dmg": (75, 105), "type": "damage"}
        self.abilities['6'] = {"name": "🌓 Second Sword: Crescent Moon", "cost": 35, "dmg": (80, 115), "type": "damage"}
        self.abilities['7'] = {"name": "🌕 Third Sword: Full Moon", "cost": 45, "dmg": (100, 145), "type": "damage"}
        self.abilities['8'] = {
            "name": "🌑 Zero Sword: Lunar Eclipse",
            "cost": 60,
            "dmg": (130, 190),
            "type": "counter",
            "desc": "Take reduced damage, pierce opponent's heart."
        }
        self.abilities['9'] = {"name": "✨ Fifth Sword", "cost": 90, "dmg": (170, 250), "type": "damage"}
        self.abilities['10'] = {"name": "💰 Yakuza Deal", "cost": 40, "dmg": (90, 135), "type": "damage"}


# ============================================================================
# KIM JUN-GU
# ============================================================================

class KimJungu(Character):
    def __init__(self):
        super().__init__(
            "Kim Jun-gu",
            "The Hwarang Sword",
            520, 290,
            [Realm.TECHNIQUE, Realm.SPEED]
        )

        self.canon_episode = 500
        self.paths_available = [Path.HWARANG_SWORD, Path.IMPROVISED_WEAPON, Path.ARMED_BEAST]
        self.armed = True
        self.form = "Armed"

        self.abilities['1'] = {"name": "👊 Bare-Handed Strike", "cost": 20, "dmg": (55, 80), "type": "damage"}
        self.abilities['2'] = {"name": "🖊️ Pen Pierce", "cost": 25, "dmg": (70, 100), "type": "damage"}
        self.abilities['3'] = {"name": "🔗 Chain Whip", "cost": 30, "dmg": (75, 110), "type": "damage"}
        self.abilities['4'] = {"name": "🥢 Iron Chopsticks", "cost": 30, "dmg": (80, 115), "type": "damage"}
        self.abilities['5'] = {"name": "👓 Broken Glasses", "cost": 25, "dmg": (65, 95), "type": "damage"}
        self.abilities['6'] = {"name": "⏱️ Spring Blade", "cost": 35, "dmg": (85, 125), "type": "damage"}
        self.abilities['7'] = {"name": "🗡️ Scimitar", "cost": 40, "dmg": (100, 150), "type": "damage"}
        self.abilities['8'] = {"name": "⚔️ Hwarang Sword", "cost": 60, "dmg": (140, 210), "type": "damage"}
        self.abilities['9'] = {"name": "⚔️ Hwarang: Blade Dance", "cost": 70, "dmg": (160, 240), "type": "damage"}
        self.abilities['10'] = {
            "name": "🔄 Improvisation",
            "cost": 20,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "Next attack +50% damage."
        }
        self.abilities['11'] = {
            "name": "🛡️ Tenacity",
            "cost": 0,
            "dmg": (0, 0),
            "type": "passive",
            "desc": "Reduced damage from blunt attacks."
        }


# ============================================================================
# JINRANG
# ============================================================================

class Jinrang(Character):
    def __init__(self):
        super().__init__(
            "Jinrang",
            "King of Busan",
            750, 380,
            [Realm.STRENGTH, Realm.OVERCOMING]
        )

        self.canon_episode = 580
        self.paths_available = [Path.GAPRYONG_DISCIPLE, Path.BUSAN_KING]

        self.abilities['1'] = {"name": "👑 Jinrang's Conviction", "cost": 40, "dmg": (130, 190), "type": "damage"}
        self.abilities['2'] = {"name": "👑 Gapryong's Disciple", "cost": 50, "dmg": (120, 180), "type": "damage"}
        self.abilities['3'] = {"name": "👑 Busan King", "cost": 60, "dmg": (140, 210), "type": "damage"}
        self.abilities['4'] = {"name": "👑 True Conviction", "cost": 80, "dmg": (170, 250), "type": "damage"}
        self.abilities['5'] = {"name": "🛡️ Gapryong's Defense", "cost": 30, "dmg": (0, 0), "type": "utility"}

        self.special = "IMMUNE to Gapryong's Copy and Jichang's Hand Blade"


# ============================================================================
# JAEGYEON NA
# ============================================================================

class JaegyeonNa(Character):
    def __init__(self):
        super().__init__(
            "Jaegyeon Na",
            "King of Incheon",
            620, 350,
            [Realm.SPEED]
        )

        self.canon_episode = 544
        self.paths_available = [Path.INCHEON_SPEED, Path.BETRAYER]

        self.abilities['1'] = {"name": "🔵 Incheon Speed", "cost": 35, "dmg": (100, 150), "type": "damage"}
        self.abilities['2'] = {"name": "🗡️ Betrayal", "cost": 40, "dmg": (95, 145), "type": "damage"}
        self.abilities['3'] = {"name": "🔵 King of Incheon", "cost": 50, "dmg": (120, 180), "type": "damage"}
        self.abilities['4'] = {"name": "🔵 Faster Than Light", "cost": 70, "dmg": (150, 230), "type": "damage"}


# ============================================================================
# MANAGER KIM
# ============================================================================

class ManagerKim(Character):
    def __init__(self):
        super().__init__(
            "Manager Kim",
            "The Senior Manager",
            480, 300,
            [Realm.TECHNIQUE, Realm.TENACITY, Realm.STRENGTH]
        )

        self.canon_episode = 290
        self.daughter_minji = True
        self.white_tiger_employee = True
        self.special_forces_vet = True
        self.code_66 = True
        self.veinous_rage = False
        self.rage_timer = 0

        self.paths_available = [
            Path.SPECIAL_FORCES,
            Path.PROTECTIVE_FATHER,
            Path.CQC_MASTER
        ]

        self._load_abilities()

    def _load_abilities(self):
        self.abilities['1'] = {
            "name": "🎖️ Special Forces Training",
            "cost": 0,
            "dmg": (0, 0),
            "type": "passive",
            "desc": "Former black ops and special forces member. Two units were dedicated to him. Permanent +20% damage, +15% evasion."
        }
        self.abilities['2'] = {
            "name": "🔫 CQC: Vital Strikes",
            "cost": 25,
            "dmg": (65, 90),
            "type": "damage",
            "desc": "Close Quarter Combat perfected. Every strike hits a vital point. Military precision."
        }
        self.abilities['3'] = {
            "name": "🔫 CQC: 3ft Kill Zone",
            "cost": 35,
            "dmg": (80, 115),
            "type": "damage",
            "desc": "Within 3 feet, Manager Kim is unbeatable. Continuous attacks to vital areas."
        }
        self.abilities['4'] = {
            "name": "🛡️ Battle-Scarred",
            "cost": 0,
            "dmg": (0, 0),
            "type": "passive",
            "desc": "Numerous bullet wounds and cuts cover his body. He's survived everything. -15% damage taken."
        }
        self.abilities['5'] = {
            "name": "👁️ Veinous Rage",
            "cost": 40,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "When angered, excessive veins emerge and eyes become bloodshot. +50% damage, ignores pain (4 turns)."
        }
        self.abilities['6'] = {
            "name": "👨‍👧 For Minji",
            "cost": 50,
            "dmg": (100, 150),
            "type": "damage",
            "desc": "When his daughter Minji is threatened, Manager Kim becomes unstoppable. Massive damage increase."
        }
        self.abilities['7'] = {
            "name": "🔍 Father's Determination",
            "cost": 30,
            "dmg": (0, 0),
            "type": "utility",
            "desc": "Will destroy everything in his path to find his daughter. Removes all debuffs, next attack guaranteed critical."
        }
        self.abilities['8'] = {
            "name": "🐯 White Tiger Agent",
            "cost": 25,
            "dmg": (60, 85),
            "type": "damage",
            "desc": "Employed by Tom Lee at the White Tiger Job Centre. Professional, efficient, lethal."
        }
        self.abilities['9'] = {
            "name": "😐 Unassuming Demeanor",
            "cost": 15,
            "dmg": (0, 0),
            "type": "buff",
            "desc": "Appears as an average middle-aged man. Enemies underestimate him. +30% critical chance next attack."
        }
        self.abilities['10'] = {
            "name": "66 CODE: Full Release",
            "cost": 70,
            "dmg": (130, 190),
            "type": "damage",
            "desc": "His former code name. When he fully unleashes his special forces training, nothing stands in his way."
        }
        self.abilities['11'] = {
            "name": "🔪 Improvised Weapons",
            "cost": 30,
            "dmg": (70, 100),
            "type": "damage",
            "desc": "Anything becomes a weapon in his hands. Pens, tools, everyday objects - all deadly."
        }

    def get_damage_multiplier(self):
        mult = 1.2
        buffs = ["🎖️ SPECIAL FORCES"]

        if self.veinous_rage:
            mult *= 1.5
            buffs.append("👁️ RAGE")
        if self.active_realm == Realm.STRENGTH:
            mult *= 1.7
            buffs.append("🔴 STRENGTH")
        elif self.active_realm == Realm.TECHNIQUE:
            mult *= 1.4
            buffs.append("🩷 TECHNIQUE")

        return mult, buffs


# ============================================================================
# MIRA KIM - REMOVED FROM PLAYABLE ROSTER (Non-combatant)
# ============================================================================

class MiraKim(Character):
    def __init__(self):
        super().__init__(
            "Mira Kim",
            "The Heart",
            200, 200,
            []
        )

        self.canon_episode = 1
        self.paths_available = []
        # No combat abilities - she's a non-combatant character
        self.abilities = {}
        self.affiliation = "J High"


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
# ENEMY CREATION FUNCTIONS
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
        '3': {"name": "Cheap Shot", "dmg": (40, 65)},
    }
    enemy = Enemy("Logan Lee", "The Bully", 300, 180, abilities, 85, "Independent")
    enemy.ai_pattern = ['3', '1', '2']
    return enemy


def create_enemy_johan_seong_enemy():
    abilities = {
        '1': {"name": "Copy: Taekwondo", "dmg": (50, 75)},
        '2': {"name": "Copy: Boxing", "dmg": (50, 75)},
        '3': {"name": "Choreography", "dmg": (85, 120)},
        '4': {"name": "God Eye", "dmg": (95, 140)},
    }
    enemy = Enemy("Johan Seong", "The God Eye", 400, 300, abilities, 15, "God Dog")
    enemy.ai_pattern = ['4', '3', '2', '1']
    return enemy


def create_enemy_vasco_enemy():
    abilities = {
        '1': {"name": "Systema Strike", "dmg": (50, 70)},
        '2': {"name": "Sunken Fist", "dmg": (70, 100)},
        '3': {"name": "Run Over", "dmg": (65, 95)},
    }
    enemy = Enemy("Vasco", "The Hero", 450, 260, abilities, 30, "Burn Knuckles")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_zack_lee():
    abilities = {
        '1': {"name": "Jab", "dmg": (35, 55)},
        '2': {"name": "Cross", "dmg": (45, 70)},
        '3': {"name": "Counter", "dmg": (60, 85)},
    }
    enemy = Enemy("Zack Lee", "The Iron Boxer", 380, 280, abilities, 35, "J High")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jay_hong_enemy():
    abilities = {
        '1': {"name": "Systema", "dmg": (45, 65)},
        '2': {"name": "Kali", "dmg": (50, 75)},
    }
    enemy = Enemy("Jay Hong", "The Silent", 380, 270, abilities, 40, "J High")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_eli_jang_enemy():
    abilities = {
        '1': {"name": "Animal Strike", "dmg": (50, 75)},
        '2': {"name": "Talon Kick", "dmg": (60, 85)},
        '3': {"name": "Beast Mode", "dmg": (85, 120)},
    }
    enemy = Enemy("Eli Jang", "The Wild", 410, 260, abilities, 16, "Hostel")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_warren_chae_enemy():
    abilities = {
        '1': {"name": "JKD: Interception", "dmg": (60, 85)},
        '2': {"name": "Shield Strike", "dmg": (65, 90)},
        '3': {"name": "Counter", "dmg": (70, 100)},
        '4': {"name": "NEW CQC", "dmg": (90, 130)},
    }
    enemy = Enemy("Warren Chae", "Hostel Executive", 390, 260, abilities, 30, "Hostel")
    enemy.ai_pattern = ['4', '3', '2', '1']
    return enemy


def create_enemy_jake_kim_enemy():
    abilities = {
        '1': {"name": "Conviction Punch", "dmg": (60, 85)},
        '2': {"name": "Inherited Will", "dmg": (95, 140)},
        '3': {"name": "Gapryong's Blood", "dmg": (120, 180)},
    }
    enemy = Enemy("Jake Kim", "The Conviction", 430, 270, abilities, 12, "Big Deal")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jerry_kwon():
    abilities = {
        '1': {"name": "Gift Punch", "dmg": (65, 95)},
        '2': {"name": "Rhino Charge", "dmg": (70, 105)},
        '3': {"name": "Loyalty to Jake", "dmg": (80, 115)},
    }
    enemy = Enemy("Jerry Kwon", "Big Deal Executive", 420, 250, abilities, 25, "Big Deal")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_xiaolung():
    abilities = {
        '1': {"name": "🇹🇭 Muay Thai: Elbow", "dmg": (80, 120)},
        '2': {"name": "🇹🇭 Muay Thai: Knee", "dmg": (85, 125)},
        '3': {"name": "🇹🇭 Thai Clinch", "dmg": (75, 110)},
        '4': {"name": "🇹🇭 Muay Thai Mastery", "dmg": (110, 170)},
    }
    enemy = Enemy("Xiaolung", "Muay Thai Genius", 550, 300, abilities, 14, "Workers")
    enemy.ai_pattern = ['4', '1', '2', '3']
    return enemy


def create_enemy_mandeok():
    abilities = {
        '1': {"name": "💪 Power Punch", "dmg": (90, 130)},
        '2': {"name": "🌍 Earth Shaker", "dmg": (100, 150)},
        '3': {"name": "🗿 Titan Strike", "dmg": (120, 180)},
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
        '5': {"name": "🕶️ Sunglasses Off", "dmg": (110, 160)},
    }
    enemy = Enemy("Vin Jin", "Ssireum Genius", 520, 280, abilities, 28, "Workers")
    enemy.ai_pattern = ['5', '4', '3', '2', '1']
    return enemy


def create_enemy_ryuhei():
    abilities = {
        '1': {"name": "⚔️ Yakuza Strike", "dmg": (80, 115)},
        '2': {"name": "🏴 Gang Style", "dmg": (85, 120)},
        '3': {"name": "⚫ Yamazaki Blood", "dmg": (100, 150)},
    }
    enemy = Enemy("Ryuhei", "Yakuza Executive", 540, 290, abilities, 24, "Workers")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_samuel_seo():
    abilities = {
        '1': {"name": "👑 King's Ambition", "dmg": (85, 125)},
        '2': {"name": "💢 Betrayal", "dmg": (80, 120)},
        '3': {"name": "⚡ Workers Executive", "dmg": (95, 140)},
        '4': {"name": "👑 Path to Kingship", "dmg": (110, 170)},
    }
    enemy = Enemy("Samuel Seo", "The Betrayer", 560, 300, abilities, 18, "Workers")
    enemy.ai_pattern = ['4', '3', '1', '2']
    return enemy


def create_enemy_eugene():
    abilities = {
        '1': {"name": "📊 Corporate Command", "dmg": (50, 80)},
        '2': {"name": "📈 Strategic Planning", "dmg": (0, 0)},
        '3': {"name": "🏭 Summon Affiliate", "dmg": (0, 0)},
    }
    enemy = Enemy("Eugene", "Workers CEO", 350, 300, abilities, 10, "Workers")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_taesoo_ma():
    abilities = {
        '1': {"name": "🔴 Right Hand", "dmg": (110, 170)},
        '2': {"name": "🔴 Ansan King", "dmg": (120, 180)},
    }
    enemy = Enemy("Taesoo Ma", "King of Ansan", 580, 300, abilities, 8, "1st Gen")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_gongseob_ji():
    abilities = {
        '1': {"name": "🩷 Speed Technique", "dmg": (95, 140)},
        '2': {"name": "🩷 Vice King", "dmg": (100, 150)},
    }
    enemy = Enemy("Gongseob Ji", "Vice King", 500, 280, abilities, 11, "1st Gen")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_jichang_kwak():
    abilities = {
        '1': {"name": "🩷 Hand Blade", "dmg": (100, 155)},
        '2': {"name": "👑 Seoul King", "dmg": (110, 170)},
    }
    enemy = Enemy("Jichang Kwak", "King of Seoul", 550, 300, abilities, 7, "1st Gen")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_gun_park_enemy():
    abilities = {
        '1': {"name": "Taekwondo", "dmg": (65, 90)},
        '2': {"name": "Kyokushin", "dmg": (70, 100)},
        '3': {"name": "Black Bone", "dmg": (130, 200)},
    }
    enemy = Enemy("Gun Park", "Legend of Gen 1", 500, 320, abilities, 5, "Independent")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_goo_kim_enemy():
    abilities = {
        '1': {"name": "Makeshift Sword", "dmg": (45, 70)},
        '2': {"name": "Full Moon", "dmg": (100, 145)},
        '3': {"name": "Fifth Sword", "dmg": (170, 250)},
    }
    enemy = Enemy("Goo Kim", "The Moonlight Sword", 480, 300, abilities, 5, "Independent")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_kim_jungu_enemy():
    abilities = {
        '1': {"name": "Improvised Weapon", "dmg": (70, 100)},
        '2': {"name": "Hwarang Sword", "dmg": (140, 210)},
        '3': {"name": "Blade Dance", "dmg": (160, 240)},
    }
    enemy = Enemy("Kim Jun-gu", "The Hwarang Sword", 520, 290, abilities, 4, "Independent")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jinrang_enemy():
    abilities = {
        '1': {"name": "Jinrang's Conviction", "dmg": (130, 190)},
        '2': {"name": "Busan King", "dmg": (140, 210)},
        '3': {"name": "True Conviction", "dmg": (170, 250)},
    }
    enemy = Enemy("Jinrang", "King of Busan", 750, 380, abilities, 2, "Busan")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jaegyeon_na_enemy():
    abilities = {
        '1': {"name": "Incheon Speed", "dmg": (100, 150)},
        '2': {"name": "Betrayal", "dmg": (95, 145)},
        '3': {"name": "Faster Than Light", "dmg": (150, 230)},
    }
    enemy = Enemy("Jaegyeon Na", "King of Incheon", 620, 350, abilities, 6, "Busan")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_charles_choi():
    abilities = {
        '1': {"name": "🎭 Puppet Master", "dmg": (90, 140)},
        '2': {"name": "🏛️ Chairman's Authority", "dmg": (110, 170)},
        '3': {"name": "👤 HNH Group", "dmg": (100, 160)},
        '4': {"name": "🎭 Truth of Two Bodies", "dmg": (130, 200)},
    }
    enemy = Enemy("Charles Choi", "The Puppet Master", 650, 350, abilities, 3, "HNH Chairman")
    enemy.ai_pattern = ['4', '3', '2', '1']
    return enemy


def create_enemy_tom_lee():
    abilities = {
        '1': {"name": "🐅 Wild Strike", "dmg": (100, 150)},
        '2': {"name": "🐅 Tom Lee Special", "dmg": (120, 180)},
        '3': {"name": "🐅 Gen 0 Power", "dmg": (140, 210)},
    }
    enemy = Enemy("Tom Lee", "The Wild", 650, 350, abilities, 5, "Gen 0")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_gapryong_kim():
    abilities = {
        '1': {"name": "👑 Conviction of the Strongest", "dmg": (120, 180)},
        '2': {"name": "👑 Gapryong's Fist", "dmg": (150, 220)},
        '3': {"name": "👑 Will to Protect", "dmg": (130, 200)},
        '4': {"name": "👑 Legend's Legacy", "dmg": (180, 280)},
    }
    enemy = Enemy("Gapryong Kim", "The Strongest", 800, 400, abilities, 0, "Gen 0 Legend")
    enemy.ai_pattern = ['4', '2', '3', '1']
    return enemy


def create_enemy_god_dog_member():
    abilities = {'1': {"name": "Fist Strike", "dmg": (25, 40)}}
    enemy = Enemy("God Dog Member", "Crew Soldier", 140, 100, abilities, 100, "God Dog")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_god_dog_elite():
    abilities = {
        '1': {"name": "Power Strike", "dmg": (40, 60)},
        '2': {"name": "Crew Combo", "dmg": (45, 65)},
    }
    enemy = Enemy("God Dog Elite", "Crew Veteran", 200, 140, abilities, 75, "God Dog")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_hostel_member():
    abilities = {
        '1': {"name": "Street Fighting", "dmg": (35, 55)},
        '2': {"name": "Ambush", "dmg": (40, 60)},
    }
    enemy = Enemy("Hostel Member", "Family Crew", 170, 120, abilities, 80, "Hostel")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_big_deal_member():
    abilities = {
        '1': {"name": "Fist Strike", "dmg": (30, 50)},
        '2': {"name": "Loyalty", "dmg": (0, 0)},
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
        '2': {"name": "Corporate Power", "dmg": (65, 95)},
    }
    enemy = Enemy("Workers Affiliate", "1st Affiliate", 360, 230, abilities, 42, "Workers")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_sally():
    abilities = {
        '1': {"name": "Quick Strike", "dmg": (45, 70)},
        '2': {"name": "Tactical Hit", "dmg": (50, 75)},
    }
    enemy = Enemy("Sally", "Hostel Executive", 310, 200, abilities, 55, "Hostel")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_brad():
    abilities = {
        '1': {"name": "Power Fist", "dmg": (55, 80)},
        '2': {"name": "Reinforced Strike", "dmg": (60, 85)},
    }
    enemy = Enemy("Brad", "Big Deal Executive", 350, 220, abilities, 48, "Big Deal")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_jace_park():
    abilities = {
        '1': {"name": "Strategic Strike", "dmg": (45, 70)},
        '2': {"name": "Tactical Retreat", "dmg": (0, 0)},
        '3': {"name": "Support", "dmg": (0, 0)},
    }
    enemy = Enemy("Jace Park", "The Strategist", 300, 210, abilities, 60, "Burn Knuckles")
    enemy.ai_pattern = ['3', '1', '2']
    return enemy


def create_enemy_burn_knuckles():
    abilities = {
        '1': {"name": "Fist of Justice", "dmg": (30, 50)},
        '2': {"name": "Team Attack", "dmg": (35, 55)},
    }
    enemy = Enemy("Burn Knuckles", "Justice Crew", 160, 110, abilities, 85, "Burn Knuckles")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_jhigh_bully():
    abilities = {'1': {"name": "School Punch", "dmg": (20, 35)}}
    enemy = Enemy("J High Bully", "School Thug", 100, 80, abilities, 120, "J High")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_cheon_shinmyeong():
    abilities = {
        '1': {"name": "🔮 Dark Exorcism", "dmg": (90, 140)},
        '2': {"name": "🔮 Cheonliang Rule", "dmg": (100, 150)},
        '3': {"name": "🔮 Puppeteer", "dmg": (80, 120)},
    }
    enemy = Enemy("Cheon Shin-myeong", "The Shaman", 480, 320, abilities, 0, "Cheonliang")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_manager_kim_enemy():
    abilities = {
        '1': {"name": "CQC Strike", "dmg": (65, 90)},
        '2': {"name": "66 CODE", "dmg": (130, 190)},
    }
    enemy = Enemy("Manager Kim", "The Senior Manager", 480, 300, abilities, 5, "White Tiger")
    enemy.ai_pattern = ['2', '1']
    return enemy


# ============================================================================
# GAME CLASS - COMPLETE WITH ALL METHODS
# ============================================================================

class LookismGame:
    def __init__(self):
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
        self.mira = MiraKim()  # Non-combatant, won't be in party selection
        self.jinrang = Jinrang()
        self.jaegyeon = JaegyeonNa()
        self.manager_kim = ManagerKim()

        # Only combat characters are in the playable roster
        self.all_characters = [
            self.daniel, self.zack, self.johan, self.vasco, self.jay,
            self.eli, self.warren, self.jake, self.gun, self.goo,
            self.joongoo, self.jinrang, self.jaegyeon, self.manager_kim
        ]

        self.party = []
        self.enemies = []
        self.turn_count = 0
        self.victories = 0
        self.total_kills = 0
        self.wave = 0
        self.current_arc = "J High"

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

                if member.name == "Daniel Park":
                    status.append(f"FORM: {member.form}")
                    if member.ui_mode:
                        status.append("👁️UI")
                        status.append(f"⏳{member.ui_timer}")
                elif member.name == "Vasco":
                    if member.muscle_boost:
                        status.append("💪BOOST")
                elif member.name == "Eli Jang":
                    if member.beast_mode:
                        status.append("🦁BEAST")
                        status.append(f"⏳{member.beast_timer}")
                elif member.name == "Johan Seong":
                    status.append(f"FORM: {member.form}")
                elif member.name == "Warren Chae":
                    if member.exhausted:
                        status.append("😮‍💨EXHAUSTED")
                elif member.name == "Manager Kim":
                    if member.veinous_rage:
                        status.append("👁️RAGE")
                        status.append(f"⏳{member.rage_timer}")

                if member.active_realm != Realm.NONE:
                    realm_icons = {
                        Realm.SPEED: "🔵",
                        Realm.STRENGTH: "🔴",
                        Realm.TENACITY: "🟢",
                        Realm.TECHNIQUE: "🩷",
                        Realm.OVERCOMING: "🟣"
                    }
                    status.append(f"{realm_icons.get(member.active_realm, '')}REALM")
                    status.append(f"⏳{member.realm_timer}")

                if member.path:
                    path_names = {
                        Path.ULTRA_INSTINCT: "👁️UI",
                        Path.COPY_MASTER: "⚡COPY",
                        Path.GOD_EYE: "👁️GOD",
                        Path.CHOREOGRAPHY: "💃DANCE",
                        Path.SYSTEMA_MASTER: "🇷🇺SYS",
                        Path.MUAY_THAI_LEGEND: "🇹🇭MT",
                        Path.NEW_CQC_CREATOR: "⚡CQC",
                        Path.HEART_ATTACK: "💔HEART",
                        Path.YAMAZAKI_HEIR: "🏯YAM",
                        Path.MOONLIGHT_SWORD: "🌙MOON",
                        Path.HWARANG_SWORD: "⚔️HWA",
                        Path.SPECIAL_FORCES: "🎖️SF",
                        Path.PROTECTIVE_FATHER: "👨‍👧PAPA",
                        Path.CQC_MASTER: "🔫CQC",
                    }
                    status.append(path_names.get(member.path, ""))

                status_str = " | ".join(filter(None, status)) if status else ""
                print(f"{member.name:15} |{bar}| {member.hp:3}/{member.max_hp:3} HP {member.energy:3}E  {status_str}")
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
                if "counter" in enemy.debuffs:
                    debuff.append("🔄COUNTER")
                if "analyzed" in enemy.debuffs:
                    debuff.append("👁️ANALYZED")
                debuff_str = " | ".join(debuff) if debuff else ""
                affil = f" [{enemy.affiliation}]" if enemy.affiliation else ""
                realm_info = ""
                if enemy.active_realm != Realm.NONE:
                    realm_icons = {
                        Realm.SPEED: "🔵",
                        Realm.STRENGTH: "🔴",
                        Realm.TENACITY: "🟢",
                        Realm.TECHNIQUE: "🩷",
                        Realm.OVERCOMING: "🟣"
                    }
                    realm_info = f" {realm_icons.get(enemy.active_realm, '')}"
                print(
                    f"{enemy.name:15} |{bar}| {enemy.hp:3}/{enemy.max_hp:3} HP (R{enemy.rank}){affil}{realm_info} {debuff_str}")
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
            print(f"\n{character.name} already walks the path of {character.path.value}")
            time.sleep(1)
            return True

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
        if hasattr(character, 'exhausted') and character.exhausted:
            self.add_log(f"{character.name} is exhausted from NEW CQC and cannot act this turn!")
            character.exhausted = False
            character.energy = min(character.max_energy, character.energy + 15)
            time.sleep(ACTION_DELAY)
            return True

        print(f"\n" + "=" * 110)
        slow_print(f"✦✦✦ {character.name} [{character.title}] ✦✦✦", 0.03)
        print("=" * 110)
        print(f"❤️ HP: {character.hp}/{character.max_hp}  ⚡ Energy: {character.energy}/{character.max_energy}")
        if character.path:
            print(f"🛤️ PATH: {character.path.value}")
        if character.active_realm != Realm.NONE:
            realm_icons = {
                Realm.SPEED: "🔵",
                Realm.STRENGTH: "🔴",
                Realm.TENACITY: "🟢",
                Realm.TECHNIQUE: "🩷",
                Realm.OVERCOMING: "🟣"
            }
            print(f"{realm_icons.get(character.active_realm, '')} REALM ACTIVE: {character.realm_timer} turns left")
        print("-" * 110)
        time.sleep(0.3)

        if character.name == "Daniel Park":
            print(f"⚡ FORM: {character.form}")
            if character.ui_mode:
                print("   👁️ ULTRA INSTINCT [ACTIVE] - Perfect evasion, +150% damage")
        elif character.name == "Gun Park":
            print("   🛡️ PERMANENT UI - 30% evasion, 20% counter")
        elif character.name == "Johan Seong" and character.blind:
            print("   🕶️ BLIND - 30% accuracy penalty")
        elif character.name == "Manager Kim":
            print("   🎖️ SPECIAL FORCES - +20% damage, +15% evasion")
            if character.veinous_rage:
                print("   👁️ VEINOUS RAGE [ACTIVE] - +50% damage, ignores pain")

        available = {}
        for key, abil in character.abilities.items():
            if character.energy < abil["cost"]:
                continue
            if character.name == "Daniel Park":
                if abil.get("name") == "👁️ Ultra Instinct" and character.ui_mode:
                    continue
            elif character.name == "Eli Jang":
                if abil.get("name") == "🦁 Beast Mode" and character.beast_mode:
                    continue
            elif character.name == "Warren Chae":
                if abil.get("name") == "⚡ NEW CQC: Full Release" and character.exhausted:
                    continue
            elif character.name == "Manager Kim":
                if abil.get("name") == "👁️ Veinous Rage" and character.veinous_rage:
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

                if character.name == "Daniel Park" and target.name == "Jinrang":
                    if it['name'] in ["👑 Gapryong's Conviction", "🩷 Jichang's Hand Blade"]:
                        self.add_log("❌ Jinrang's conviction is stronger! The technique has no effect!")
                        dmg = 0

                target.take_damage(dmg)

                print("\n" + "✨" * 55)
                slow_print(f"✨✨✨ {it['name']} ✨✨✨", 0.05)
                print("✨" * 55)
                time.sleep(0.5)
                self.add_log(f"{character.name} unleashes their INFINITY TECHNIQUE for {dmg} damage!")

                if "Ultra Instinct" in it['name'] or "UI" in it['name']:
                    character.ui_mode = True
                    character.ui_timer = 2
                if "Heart Attack" in it['name']:
                    self.add_log("💔 The target's heart stops for a moment!")
                    target.debuffs.append("stun")
                if "Fifth Sword" in it['name']:
                    self.add_log("✨ The technique thought impossible... now perfected!")
                if "Code 66" in it['name'] or "SPECIAL FORCES" in it['name']:
                    self.add_log("🎖️ His former code name... unleashed!")

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
                    character.boost_timer = 5
                    self.add_log("💪💪💪 MUSCLE ENHANCEMENT! +30% damage (5 turns)")
                elif character.name == "Johan Seong" and "God Eye" in ability["name"]:
                    character.god_eye_active = True
                    self.add_log("👁️👁️👁️ GOD EYE ACTIVATED! +50% damage")
                elif character.name == "Manager Kim" and "Veinous Rage" in ability["name"]:
                    character.veinous_rage = True
                    character.rage_timer = 4
                    self.add_log("👁️👁️👁️ VEINOUS RAGE! Excessive veins emerge! +50% damage, ignores pain (4 turns)")
                elif character.name == "Zack Lee" and "Heat Mode" in ability["name"]:
                    character.heat_mode = True
                    character.heat_timer = 3
                    self.add_log("🔥🔥🔥 HEAT MODE! Body becomes hot! +50% damage, adaptive fighting (3 turns)")
                else:
                    self.add_log(f"{character.name} uses {ability['name']}!")

            elif ability.get("type") == "utility":
                if "Protect" in ability["name"]:
                    target = self.select_target(allies=True)
                    if target:
                        character.buffs.append("protecting")
                        self.add_log(f"🛡️ {character.name} protects {target.name}!")
                elif "Defense" in ability["name"]:
                    character.defending = True
                    self.add_log(f"🛡️ {character.name} takes a defensive stance!")
                elif "Jace's Strategy" in ability["name"]:
                    character.buffs.append("strategy")
                    self.add_log(f"🧠 Jace's strategy! Vasco's next attack +30% damage!")
                elif "Gift" in ability["name"]:
                    self.add_log(f"💝 Jay gives Daniel expensive clothes as encouragement!")
                    character.buffs.append("encouraged")
                elif "Inu's Puppies" in ability["name"]:
                    self.add_log("🐶🐶🐶 Inu's puppies rush in and distract the enemies!")
                    for e in self.enemies:
                        if random.random() < 0.5:
                            e.debuffs.append("stun")
                elif "Father's Determination" in ability["name"]:
                    character.buffs = []
                    character.debuffs = []
                    character.buffs.append("guaranteed_critical")
                    self.add_log("🔍 FATHER'S DETERMINATION! Manager Kim will find his daughter! Next attack guaranteed critical!")
                elif "Unassuming Demeanor" in ability["name"]:
                    character.buffs.append("critical_next")
                    self.add_log("😐 Enemies underestimate the middle-aged man... +30% critical chance next attack!")
                else:
                    self.add_log(f"{character.name} uses {ability['name']}!")

            elif ability.get("type") == "passive":
                self.add_log(f"✨ {ability['name']} is always active.")
                return self.use_ability(character)

            elif ability.get("type") == "damage" or "dmg" in ability:
                target = self.select_target()
                if target:
                    dmg = random.randint(ability["dmg"][0], ability["dmg"][1])

                    if hasattr(character, 'get_damage_multiplier'):
                        mult, buffs = character.get_damage_multiplier()
                        dmg = int(dmg * mult)

                    if "Counter" in ability["name"] and character.name == "Zack Lee":
                        if random.random() < 0.5:
                            dmg *= 2
                            self.add_log("⚡ PERFECT COUNTER! Double damage!")

                    if "For Yenna" in ability["name"]:
                        self.add_log("👶 ELI FIGHTS FOR YENNA! A father's love knows no limits!")
                    if "Heart Attack Punch" in ability["name"]:
                        self.add_log("💔 HEART ATTACK PUNCH! One-inch strike to the heart!")
                    if "Fifth Sword" in ability["name"]:
                        self.add_log("✨ THE FIFTH SWORD! Technique thought impossible!")
                    if "Black Bone" in ability["name"]:
                        self.add_log("🖤 BLACK BONE! Yamazaki's ultimate technique!")
                    if "66 CODE" in ability["name"]:
                        self.add_log("🎖️ 66 CODE! Special forces training fully unleashed!")
                    if "For Minji" in ability["name"]:
                        self.add_log("👨‍👧 FOR MINJI! Manager Kim becomes unstoppable!")

                    if "guaranteed_critical" in character.buffs:
                        dmg = int(dmg * 2)
                        character.buffs.remove("guaranteed_critical")
                        self.add_log("✨ CRITICAL HIT! Father's determination pays off!")
                    elif "critical_next" in character.buffs:
                        if random.random() < 0.3:
                            dmg = int(dmg * 2)
                            self.add_log("✨ CRITICAL HIT! Enemies underestimated him!")
                        character.buffs.remove("critical_next")

                    if character.name == "Daniel Park" and target.name == "Jinrang":
                        if ability["name"] in ["🩷 Jichang's Hand Blade", "👑 Gapryong's Conviction"]:
                            self.add_log("❌ Jinrang's conviction is stronger! The technique has no effect!")
                            dmg = 0

                    target.take_damage(dmg)
                    self.add_log(f"{character.name} uses {ability['name']} for {dmg} damage!")

                    if ability.get("drawback") == "exhausted":
                        character.exhausted = True
                        self.add_log("😮‍💨 Warren is exhausted from using NEW CQC! Cannot act next turn!")

            time.sleep(ACTION_DELAY)
            return True
        else:
            print("❌ Invalid ability. Try again.")
            time.sleep(0.5)
            return self.use_ability(character)

    def get_damage_multiplier(self, character):
        mult = 1.0
        buffs = []

        if hasattr(character, 'active_realm'):
            if character.active_realm == Realm.STRENGTH:
                mult *= 1.7
                buffs.append("🔴 STRENGTH")
            elif character.active_realm == Realm.OVERCOMING and character.hp < character.max_hp * 0.3:
                mult *= 2.0
                buffs.append("🟣 OVERCOMING")
            elif character.active_realm == Realm.TECHNIQUE:
                mult *= 1.4
                buffs.append("🩷 TECHNIQUE")
            elif character.active_realm == Realm.SPEED:
                buffs.append("🔵 SPEED")

        if hasattr(character, 'ui_mode') and character.ui_mode:
            mult *= 2.5
            buffs.append("👁️ UI")
        if hasattr(character, 'beast_mode') and character.beast_mode:
            mult *= 1.6
            buffs.append("🦁 BEAST")
        if hasattr(character, 'muscle_boost') and character.muscle_boost:
            mult *= 1.3
            buffs.append("💪 MUSCLE")
        if hasattr(character, 'god_eye_active') and character.god_eye_active:
            mult *= 1.5
            buffs.append("👁️ GOD EYE")
        if hasattr(character, 'heat_mode') and character.heat_mode:
            mult *= 1.5
            buffs.append("🔥 HEAT")
        if hasattr(character, 'veinous_rage') and character.veinous_rage:
            mult *= 1.5
            buffs.append("👁️ RAGE")

        return mult, buffs

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

                if enemy.active_realm == Realm.STRENGTH:
                    dmg = int(dmg * 1.5)
                elif enemy.active_realm == Realm.TECHNIQUE:
                    if random.random() < 0.3:
                        dmg = int(dmg * 1.8)
                        self.add_log(f"🩷 {enemy.name}'s technique is perfect!")

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
                    c.form = "Normal"
                    if hasattr(c, 'name'):
                        self.add_log(f"{c.name}'s realm fades.")

            if hasattr(c, 'ui_mode') and c.ui_mode:
                c.ui_timer -= 1
                if c.ui_timer <= 0:
                    c.ui_mode = False
                    c.form = "Normal"
                    self.add_log(f"👁️ {c.name}'s Ultra Instinct fades.")

            if hasattr(c, 'beast_mode') and c.beast_mode:
                c.beast_timer -= 1
                if c.beast_timer <= 0:
                    c.beast_mode = False
                    c.form = "Normal"
                    self.add_log(f"🦁 {c.name}'s Beast Mode fades.")

            if hasattr(c, 'heat_mode') and c.heat_mode:
                c.heat_timer -= 1
                if c.heat_timer <= 0:
                    c.heat_mode = False
                    self.add_log(f"🔥 {c.name}'s Heat Mode fades.")

            if hasattr(c, 'veinous_rage') and c.veinous_rage:
                c.rage_timer -= 1
                if c.rage_timer <= 0:
                    c.veinous_rage = False
                    self.add_log(f"👁️ {c.name}'s Veinous Rage fades.")

            if hasattr(c, 'boost_timer') and c.boost_timer > 0:
                c.boost_timer -= 1
                if c.boost_timer <= 0 and hasattr(c, 'muscle_boost'):
                    c.muscle_boost = False
                    self.add_log(f"💪 {c.name}'s Muscle Enhancement fades.")

            to_remove = []
            for debuff in c.debuffs:
                if random.random() < 0.3:
                    to_remove.append(debuff)

            for debuff in to_remove:
                if debuff in c.debuffs:
                    c.debuffs.remove(debuff)
                    if hasattr(c, 'name'):
                        self.add_log(f"{c.name}'s {debuff} wore off.")

            time.sleep(0.2)

    def select_party(self, max_size=4):
        print("\n" + "=" * 110)
        slow_print("✦✦✦ SELECT YOUR PARTY ✦✦✦", 0.03)
        print("=" * 110)
        print(f"Choose up to {max_size} characters for this battle:")
        print("-" * 110)

        available = []
        for i, char in enumerate(self.all_characters):
            if char.is_alive():
                path_info = f" [{char.path.name}]" if char.path else ""
                print(f"  {i + 1}. {char.name} [{char.title}]{path_info} - {char.hp}/{char.max_hp} HP")
                available.append(char)
            time.sleep(0.05)

        print(f"\n  a. Auto-select (Daniel, Vasco, Zack, Jay)")
        print("  c. Cancel")
        print("-" * 110)

        choice = input("> ").strip().lower()
        if choice == 'c':
            return None
        if choice == 'a':
            return [self.daniel, self.vasco, self.zack, self.jay]

        selected = []
        print("\nEnter character numbers (1-14), one per line. Empty line to finish:")

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
            if hasattr(char, 'heat_mode'):
                char.heat_mode = False
                char.heat_timer = 0
            if hasattr(char, 'veinous_rage'):
                char.veinous_rage = False
                char.rage_timer = 0
            if hasattr(char, 'muscle_boost'):
                char.muscle_boost = False
                char.boost_timer = 0
            if hasattr(char, 'exhausted'):
                char.exhausted = False
            if hasattr(char, 'god_eye_active'):
                char.god_eye_active = False

            print(f"  ✦ {char.name} fully recovered!")
            time.sleep(0.1)

        print("\n✦ Party fully healed and recovered! ✦")
        time.sleep(1.5)

    def story_mode(self):
        print("\n" + "=" * 110)
        slow_print("📖📖📖 STORY MODE: THE COMPLETE LOOKISM 📖📖📖", 0.03)
        print("=" * 110)
        slow_print("Based on Park Tae-joon's manhwa (2014-2025)", 0.02)
        slow_print("Current to Chapter 581+ • Busan Arc • Jinrang • Jaegyeon Na Betrayal", 0.02)
        print("=" * 110)
        time.sleep(1)

        arcs = [
            ("ARC 1: J HIGH & THE TWO BODIES (Ep 1-100)",
             [
                 ("Prologue: The Transfer Student", [create_enemy_jhigh_bully()]),
                 ("Chapter 1: Logan Lee", [create_enemy_logan_lee()]),
                 ("Chapter 2: Zack's Challenge", [create_enemy_zack_lee()]),
                 ("Chapter 3: Vasco Appears", [create_enemy_vasco_enemy()]),
                 ("Chapter 4: Jay's Protection", [create_enemy_jay_hong_enemy()])
             ]),
            ("ARC 2: GOD DOG (Ep 100-200)",
             [
                 ("Chapter 5: God Dog Soldiers", [create_enemy_god_dog_member(), create_enemy_god_dog_member()]),
                 ("Chapter 6: God Dog Elite", [create_enemy_god_dog_elite(), create_enemy_god_dog_member()]),
                 ("Chapter 7: Johan Seong", [create_enemy_johan_seong_enemy()])
             ]),
            ("ARC 3: HOSTEL (Ep 200-300)",
             [
                 ("Chapter 8: Hostel Family", [create_enemy_hostel_member(), create_enemy_sally()]),
                 ("Chapter 9: Warren Chae", [create_enemy_warren_chae_enemy()]),
                 ("Chapter 10: Eli Jang", [create_enemy_eli_jang_enemy()])
             ]),
            ("ARC 4: BIG DEAL (Ep 300-400)",
             [
                 ("Chapter 11: Big Deal Soldiers", [create_enemy_big_deal_member(), create_enemy_brad()]),
                 ("Chapter 12: Jerry Kwon", [create_enemy_jerry_kwon()]),
                 ("Chapter 13: Jake Kim", [create_enemy_jake_kim_enemy()])
             ]),
            ("ARC 5: WORKERS (Ep 400-500)",
             [
                 ("Chapter 14: Workers Affiliates", [create_enemy_workers_member(), create_enemy_workers_affiliate()]),
                 ("Chapter 15: Xiaolung", [create_enemy_xiaolung()]),
                 ("Chapter 16: Mandeok", [create_enemy_mandeok()]),
                 ("Chapter 17: Samuel Seo", [create_enemy_samuel_seo()]),
                 ("Chapter 18: Eugene", [create_enemy_eugene()])
             ]),
            ("ARC 6: CHEONLIANG (Ep 500-550)",
             [
                 ("Chapter 19: Vin Jin", [create_enemy_vin_jin()]),
                 ("Chapter 20: Ryuhei", [create_enemy_ryuhei()]),
                 ("Chapter 21: The Shaman", [create_enemy_cheon_shinmyeong()])
             ]),
            ("ARC 7: 1ST GENERATION (Ep 550-570)",
             [
                 ("Chapter 22: Taesoo Ma", [create_enemy_taesoo_ma()]),
                 ("Chapter 23: Gongseob Ji", [create_enemy_gongseob_ji()]),
                 ("Chapter 24: Jichang Kwak", [create_enemy_jichang_kwak()])
             ]),
            ("ARC 8: BUSAN (Ep 570-581+)",
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

                if chapter != chapters[-1][0]:
                    self.rest()

            print("\n" + "=" * 110)
            slow_print("✨ NEW PATHS AVAILABLE ✨", 0.03)
            print("=" * 110)
            print("Your characters have grown. Choose their paths:")
            time.sleep(0.5)

            for char in [self.daniel, self.vasco, self.zack, self.jay, self.johan,
                         self.eli, self.warren, self.jake, self.gun, self.goo, self.joongoo, self.manager_kim]:
                if not char.path and char in party:
                    print(f"\n{char.name} can now choose a path:")
                    self.choose_character_path(char)

        print("\n" + "=" * 110)
        slow_print("🏆🏆🏆 STORY MODE COMPLETE! 🏆🏆🏆", 0.04)
        print("=" * 110)
        slow_print("You have experienced the complete Lookism story!", 0.02)
        print(f"Total victories: {self.victories}")
        print(f"Enemies defeated: {self.total_kills}")
        print("=" * 110)
        time.sleep(3)
        return True

    def crew_gauntlet_mode(self):
        print("\n" + "=" * 110)
        slow_print("🏆🏆🏆 CREW GAUNTLET 🏆🏆🏆", 0.04)
        print("=" * 110)
        slow_print("Face all the major crews in order of difficulty!", 0.02)
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
        time.sleep(3)
        return True

    def boss_rush_mode(self):
        print("\n" + "=" * 110)
        slow_print("👑👑👑 BOSS RUSH 👑👑👑", 0.04)
        print("=" * 110)
        slow_print("Face the most powerful enemies back-to-back!", 0.02)
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

        print("\n" + "=" * 110)
        slow_print("👑👑👑 BOSS RUSH COMPLETE! 👑👑👑", 0.04)
        print("=" * 110)
        slow_print("You have defeated every major boss in Lookism!", 0.02)
        print(f"Total victories: {self.victories}")
        print("=" * 110)
        time.sleep(3)
        return True

    def survival_mode(self):
        print("\n" + "=" * 110)
        slow_print("♾️♾️♾️ ENDLESS SURVIVAL ♾️♾️♾️", 0.04)
        print("=" * 110)
        slow_print("Fight wave after wave of enemies!", 0.02)
        slow_print("How long can you last?", 0.02)
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
        slow_print("Practice against any character in the game.", 0.02)
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
        print("  b. Back")
        print()

        choice = input("> ").strip()
        print()

        if choice.lower() == 'b':
            return

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
            if char.path:
                path_names = {
                    Path.ULTRA_INSTINCT: "👁️ UI",
                    Path.COPY_MASTER: "⚡ COPY",
                    Path.SECOND_BODY: "🔄 DUAL",
                    Path.GOD_EYE: "👁️ GOD",
                    Path.CHOREOGRAPHY: "💃 DANCE",
                    Path.SYSTEMA_MASTER: "🇷🇺 SYS",
                    Path.MUAY_THAI_LEGEND: "🇹🇭 MT",
                    Path.BURN_KNUCKLE_KING: "🔥 BURN",
                    Path.NEW_CQC_CREATOR: "⚡ CQC",
                    Path.HEART_ATTACK: "💔 HEART",
                    Path.YAMAZAKI_HEIR: "🏯 YAM",
                    Path.MOONLIGHT_SWORD: "🌙 MOON",
                    Path.HWARANG_SWORD: "⚔️ HWA",
                    Path.SPECIAL_FORCES: "🎖️ SF",
                    Path.PROTECTIVE_FATHER: "👨‍👧 PAPA",
                    Path.CQC_MASTER: "🔫 CQC",
                }
                path_icon = path_names.get(char.path, "")
                print(f"  • {char.name}: {path_icon} Lv.{char.path_level} ({char.path_exp}/100 EXP)")
            else:
                print(f"  • {char.name}: No path chosen")
        print()

        print("🔓 UNLOCKABLE CHARACTERS:")
        print("  • Jinrang - Complete Busan Arc")
        print("  • Jaegyeon Na - Complete Busan Arc")
        print("  • Gapryong Kim - Complete Boss Rush")
        print("  • Manager Kim - Available from start")
        print()

        input("Press Enter to return to menu...")
        print()


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    print("\n" + "=" * 110)
    slow_print("    👊👊👊 LOOKISM: AWAKENED FIST 👊👊👊", 0.03)
    print("    COMPLETE CANON EDITION - 100% MANHWA ACCURATE")
    print("    Based on Park Tae-joon's Lookism (2014-2025)")
    print("    Current to Chapter 581+ • Busan Arc • Jinrang")
    print("=" * 110)
    print("\n🎮 GAME MODES:")
    time.sleep(0.3)
    print("  1. 📖 Story Mode - Complete canon story (Ep 1-581+)")
    print("  2. 🏆 Crew Gauntlet - Fight through all crews")
    print("  3. 👑 Boss Rush - Only major villains & legends")
    print("  4. ♾️ Endless Survival - How many waves?")
    print("  5. 🥋 Training Room - Practice against any character")
    print("  6. 📊 Stats & Records")
    print("  7. ❌ Exit")
    print("=" * 110)
    print("\n📚 PATH SYSTEM:")
    time.sleep(0.2)
    print("   • Each character has 3-4 unique paths")
    print("   • Paths unlock INFINITY TECHNIQUES")
    print("   • Choose wisely - your destiny awaits")
    print("=" * 110)
    print("\n🔓 UNLOCKABLE CHARACTERS:")
    print("   • Jinrang - King of Busan")
    print("   • Jaegyeon Na - King of Incheon")
    print("   • Gapryong Kim - The Strongest of Gen 0")
    print("   • Manager Kim - The Senior Manager (Available now)")
    print("=" * 110)
    time.sleep(1)

    game = LookismGame()

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
        print("7. ❌ Exit")
        print("-" * 110)

        choice = input("> ").strip()
        print()

        if choice == "1":
            game = LookismGame()
            game.story_mode()
        elif choice == "2":
            game = LookismGame()
            game.crew_gauntlet_mode()
        elif choice == "3":
            game = LookismGame()
            game.boss_rush_mode()
        elif choice == "4":
            game = LookismGame()
            game.survival_mode()
        elif choice == "5":
            game.training_mode()
        elif choice == "6":
            game.stats_mode()
        elif choice == "7":
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