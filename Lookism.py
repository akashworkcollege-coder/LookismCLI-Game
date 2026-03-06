#!/usr/bin/env python3
"""
LOOKISM: AWAKENED FIST - COMPLETE CANON EDITION v3
ALL 41 PLAYABLE CHARACTERS — Manhwa Accurate
Based on Park Tae-joon's Lookism (2014-2025) & Manager Kim (Spin-off)

FIXES v2 (10 fixes — see previous version notes)

NEW FIXES v3 (13 additional bugs + 15 canon corrections):
  BUG-01: Infinity energy not refunded when no target (energy deducted after target select now)
  BUG-02: Realm activation no longer free — costs the player's turn
  BUG-03: Passive abilities now displayed and excluded from ability selection
  BUG-04: James Lee 'Legend's Speed' now actually applies +30% dmg for 3 turns
  BUG-05: Zack Lee 'Iron Fortress Stance' now sets real -50% dmg reduction
  BUG-06: Jake Kim 'Conviction Mode' now applies +50% dmg for 3 turns
  BUG-07: Logan Lee 'Intimidation' now applies 40% stun chance to enemies
  BUG-08: Realm SPEED (evasion + double strike) and TECHNIQUE (counter) now functional
  BUG-09: Story mode enemies recreated fresh on each attempt (no stale 0-HP enemies)
  BUG-10: EXP formula inverted — stronger enemies now give more EXP
  BUG-11: choose_character_path '2' now correctly clears path for re-selection
  BUG-12: Infinity no-target case now returns True (no silent loop with spent energy)
  BUG-13: GunPark passive ability no longer listed as selectable action

  CANON-01: Vasco affiliation set to Burn Knuckles
  CANON-02: Gitae Kim title fixed (not 'King of Seoul' — that's Jichang)
  CANON-03: Jake Gapryong path renamed 'Hidden Bloodline (Unconfirmed)'
  CANON-04: Daniel reduced to SPEED + OVERCOMING realms only (current arc)
  CANON-07: Johan canon_episode corrected to 55
  CANON-10: Manager Kim affiliation fixed to Workers only
  CANON-11: Park Jonggun's Father labeled as Fan Creation
  CANON-14: Eli Jang realms fixed to STRENGTH + OVERCOMING (not TECHNIQUE)
  CANON-15: Shingen Yamazaki realms reduced (not a Korean Gyeongji user)
"""

import random
import time
import sys
import json
import os
from enum import Enum
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

TEXT_SPEED = 0.03
BATTLE_START_DELAY = 1.0
TURN_DELAY = 0.5
ACTION_DELAY = 0.3
VICTORY_DELAY = 1.5
SAVE_FILE = "lookism_save.json"


def slow_print(text, delay=None):
    if delay is None:
        delay = TEXT_SPEED
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


# ============================================================================
# SAVE/LOAD SYSTEM
# ============================================================================

class SaveSystem:
    @staticmethod
    def save_game(game_state):
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(game_state, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False

    @staticmethod
    def load_game():
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"❌ Load failed: {e}")
            return None

    @staticmethod
    def delete_save():
        try:
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
                return True
            return False
        except:
            return False


# ============================================================================
# CANON GYEONGJI (REALM/境地) SYSTEM
# ============================================================================

class Realm(Enum):
    NONE = "⚪ None"
    SPEED = "🔵 Speed"
    STRENGTH = "🔴 Strength"
    TENACITY = "🟢 Tenacity"
    TECHNIQUE = "🩷 Technique"
    OVERCOMING = "🟣 Overcoming"


class RealmEffect:
    @staticmethod
    def apply(realm, character):
        effects = {
            Realm.SPEED: {
                "evasion": 0.5,
                "double_strike": 0.3,
                "desc": "Attacks become invisible! +50% evasion, 30% double strike"
            },
            Realm.STRENGTH: {
                "damage_mult": 1.7,
                "armor_break": True,
                "desc": "Overwhelming power! +70% damage, armor break"
            },
            Realm.TENACITY: {
                "damage_reduction": 0.5,
                "regen": 15,
                "desc": "Extreme durability! -50% damage taken, +15 HP/turn"
            },
            Realm.TECHNIQUE: {
                "accuracy": 0.4,
                "counter": 0.25,
                "desc": "Perfected form! +40% accuracy, 25% counter"
            },
            Realm.OVERCOMING: {
                "berserk_threshold": 0.3,
                "damage_mult": 2.0,
                "desc": "Born from limits! +100% damage when below 30% HP"
            }
        }
        return effects.get(realm, {"desc": f"{realm.value} activated!"})


# ============================================================================
# COMPLETE PATH SYSTEM
# ============================================================================

class Path(Enum):
    # GEN 0 LEGENDS
    GAPRYONG_CONVICTION = "👑 Gapryong's Conviction"
    TOM_LEE_WILD = "🐅 Tom Lee's Wild"
    CHARLES_ELITE = "🎭 Charles Choi's Invisible Attacks"
    JINYOUNG_COPY = "🔄 Jinyoung Park's Copy"
    BAEKHO_BEAST = "🐯 Baekho's Beast Mode"
    GAPRYONG_FIST_MEMBER = "👊 Gapryong's Fist Member"

    # 1ST GENERATION KINGS
    JAMES_LEE_INVISIBLE = "👑 James Lee's Invisible Attacks"
    GITAE_KIM = "⚡ Gitae Kim"
    JICHANG_HAND_BLADE = "🩷 Jichang Kwak's Hand Blade"
    TAESOO_MA_FIST = "🔴 Taesoo Ma's Right Hand"
    GONGSEOB_IRON = "🔨 Gongseob Ji's Iron Boxing"
    SEOKDU_HEADBUTT = "💢 Seokdu Wang's Headbutt"
    JAEGYEON_SPEED = "🔵 Jaegyeon Na's Speed"
    SEONGJI_MONSTER = "🦍 Seongji Yuk's Monster Style"
    JINRANG_CONVICTION = "👑 Jinrang's True Conviction"

    # GEN 2 CREW LEADERS
    DANIEL_UI = "👁️ Daniel Park's Ultra Instinct"
    DANIEL_COPY = "⚡ Daniel Park's Copy Master"
    ZACK_IRON = "🔨 Zack Lee's Iron Boxing"
    JOHAN_GOD_EYE = "👁️ Johan Seong's God Eye"
    JOHAN_CHOREOGRAPHY = "💃 Johan Seong's Choreography"
    VASCO_SYSTEMA = "🇷🇺 Vasco's Systema Master"
    VASCO_MUAY_THAI = "🇹🇭 Vasco's Muay Thai Legend"
    JAY_KALI = "🇵🇭 Jay Hong's Kali Master"
    ELI_BEAST = "🦁 Eli Jang's Beast King"
    ELI_TOM_LEE = "🐅 Eli Jang's Tom Lee Legacy"
    WARREN_JKD = "🥋 Warren Chae's Jeet Kune Do"
    WARREN_CQC = "🔫 Warren Chae's CQC Operator"
    WARREN_HEART = "💔 Warren Chae's Heart Attack"
    JAKE_CONVICTION = "⚖️ Jake Kim's Conviction King"
    JAKE_GAPRYONG = "👑 Jake Kim's Hidden Bloodline (Unconfirmed)"
    GUN_YAMAZAKI = "🏯 Gun Park's Yamazaki Heir"
    GUN_CONSTANT_UI = "👁️ Gun Park's Constant UI"
    GOO_MOONLIGHT = "🌙 Goo Kim's Moonlight Sword"
    GOO_FIFTH = "✨ Goo Kim's Fifth Sword"
    JOONGOO_HWARANG = "⚔️ Kim Jun-gu's Hwarang Sword"
    JOONGOO_ARMED = "🗡️ Kim Jun-gu's Armed Beast"

    # WORKERS / MANAGER KIM (merged Cap Guy)
    MANDEOK_POWER = "💪 Mandeok's Titan Strength"
    MANAGER_KIM_CQC = "🔫 Manager Kim's CQC & Code 66"
    XIAOLUNG_MUAY_THAI = "🇹🇭 Xiaolung's Muay Thai Genius"
    RYUHEI_YAKUZA = "⚔️ Ryuhei's Yakuza Style"
    SAMUEL_AMBITION = "👑 Samuel Seo's King's Ambition"
    SINU_INVISIBLE = "🌀 Sinu Han's Invisible Attacks"
    LOGAN_BULLY = "👊 Logan Lee's Bully Brawling"

    # CHEONLIANG
    VIN_JIN_SSIREUM = "🇰🇷 Vin Jin's Ssireum Genius"
    SEONGJI_MARTIAL = "🥋 Seongji Yuk's Martial Arts"
    HAN_JAEHA = "🤼 Han Jaeha's Ssireum"
    BAEK_SEONG_TAEKKYON = "🦢 Baek Seong's Taekkyon"

    # YAMAZAKI
    SHINGEN_YAMAZAKI = "🏯 Shingen Yamazaki's Ultimate"
    PARK_FATHER = "❓ Park Jonggun's Father"

    # LAW ENFORCEMENT
    KIM_MINJAE_JUDO = "🥋 Kim Minjae's Judo"
    DETECTIVE_KANG_BOXING = "🥊 Detective Kang's Boxing"


# ============================================================================
# COMPLETE INFINITY TECHNIQUES DATABASE
# FIX #9: James Lee dmg lowered below Gapryong's (canon hierarchy)
# FIX #8: Logan Lee infinity technique REMOVED (non-canon)
# ============================================================================

INFINITY_TECHNIQUES = {
    Path.GAPRYONG_CONVICTION: {
        "name": "👑 INFINITE GAPRYONG: Legend's Fist",
        "cost": 150, "dmg": (300, 420),
        "desc": "The legendary fist that defeated the Yamazaki Syndicate. Gapryong Kim's ultimate conviction — a punch that changed the course of Gen 0 and brought peace to the underworld."
    },
    Path.TOM_LEE_WILD: {
        "name": "🐅 INFINITE WILD: Tom Lee Special",
        "cost": 140, "dmg": (280, 390),
        "desc": "Tom Lee's ultimate technique. Biting, slashing, pure animal instinct. 'I'm gonna tear his bones apart.' A wild flurry that combines every dirty fighting technique imaginable."
    },
    Path.CHARLES_ELITE: {
        "name": "🎭 INFINITE ELITE: Chairman's Authority",
        "cost": 145, "dmg": (290, 400),
        "desc": "Charles Choi's invisible attacks. The puppet master's final move — a strike so fast and precise it cannot be seen, only felt when it's too late."
    },
    Path.JINYOUNG_COPY: {
        "name": "🔄 INFINITE COPY: Medical Genius",
        "cost": 135, "dmg": (270, 370),
        "desc": "Jinyoung Park's perfect copy ability. Any technique seen once can be replicated with surgical precision. The ultimate expression of his genius."
    },
    Path.BAEKHO_BEAST: {
        "name": "🐯 INFINITE BEAST: White Tiger's Wrath",
        "cost": 130, "dmg": (260, 360),
        "desc": "Baekho's beast mode unleashed. The White Tiger's ultimate technique."
    },
    Path.GAPRYONG_FIST_MEMBER: {
        "name": "👊 INFINITE FIST: Legendary Crew",
        "cost": 120, "dmg": (240, 340),
        "desc": "The combined strength of Gapryong's Fist. Legends stand together."
    },
    # FIX #9: James Lee dmg (270-370) < Gapryong (300-420)
    Path.JAMES_LEE_INVISIBLE: {
        "name": "👑 INFINITE JAMES: Legend of the 1st Gen",
        "cost": 150, "dmg": (270, 390),
        "desc": "James Lee's perfected invisible attacks. The peak of the 1st Generation — a dance of death so beautiful and so lethal it single-handedly dismantled an entire era."
    },
    Path.GITAE_KIM: {
        "name": "⚡ INFINITE GITAE: Gapryong's Shadow",
        "cost": 145, "dmg": (290, 400),
        "desc": "Gitae Kim inherits his father's power. The unknown technique of the King of Seoul."
    },
    Path.JICHANG_HAND_BLADE: {
        "name": "🩷 INFINITE HAND BLADE: King's Edge",
        "cost": 135, "dmg": (270, 380),
        "desc": "Jichang Kwak's ultimate hand blade technique. His hands become forged steel."
    },
    Path.TAESOO_MA_FIST: {
        "name": "🔴 INFINITE RIGHT HAND: Ansan's Pride",
        "cost": 140, "dmg": (280, 400),
        "desc": "Taesoo Ma's right fist — no technique, just overwhelming power."
    },
    Path.GONGSEOB_IRON: {
        "name": "🔨 INFINITE IRON: The Monk's Fortress",
        "cost": 130, "dmg": (260, 360),
        "desc": "Gongseob Ji's iron boxing. Speed and durability combined into an unbreakable style."
    },
    Path.SEOKDU_HEADBUTT: {
        "name": "💢 INFINITE HEADBUTT: Suwon's Crown",
        "cost": 125, "dmg": (250, 350),
        "desc": "Seokdu Wang's legendary headbutt. His forehead is harder than steel."
    },
    Path.JAEGYEON_SPEED: {
        "name": "🔵 INFINITE SPEED: Incheon Flash",
        "cost": 135, "dmg": (270, 370),
        "desc": "Jaegyeon Na's ultimate speed. He doesn't move — he simply arrives."
    },
    Path.SEONGJI_MONSTER: {
        "name": "🦍 INFINITE MONSTER: Cheonliang's King",
        "cost": 140, "dmg": (280, 390),
        "desc": "Seongji Yuk's mastery of Ssireum, Judo, and Kudo combined into a monstrous style."
    },
    Path.JINRANG_CONVICTION: {
        "name": "👑 INFINITE DISCIPLE: True Conviction",
        "cost": 150, "dmg": (300, 420),
        "desc": "Jinrang's ultimate technique. As Gapryong's true disciple, his conviction is absolute."
    },
    Path.DANIEL_UI: {
        "name": "👁️ INFINITE UI: Perfect Body",
        "cost": 100, "dmg": (250, 350),
        "desc": "Daniel's Ultra Instinct awakening. The body moves before the mind."
    },
    Path.DANIEL_COPY: {
        "name": "⚡ INFINITE COPY: Perfect Replication",
        "cost": 90, "dmg": (220, 320),
        "desc": "Daniel's copy ability at its peak. Any technique becomes his own."
    },
    Path.ZACK_IRON: {
        "name": "🔨 INFINITE IRON BOXING: Shining Star",
        "cost": 80, "dmg": (200, 300),
        "desc": "Zack's ultimate iron boxing. The star shines brightest at the end."
    },
    Path.JOHAN_GOD_EYE: {
        "name": "👁️ INFINITE GOD EYE: Ultimate Copy",
        "cost": 95, "dmg": (230, 330),
        "desc": "Johan's God Eye sees all. Perfect replication — he doesn't need to see to understand."
    },
    Path.JOHAN_CHOREOGRAPHY: {
        "name": "💃 INFINITE CHOREOGRAPHY: Dance of Death",
        "cost": 85, "dmg": (210, 310),
        "desc": "Johan's dance combat perfected. Flowing movements from K-Pop turned lethal art."
    },
    Path.VASCO_SYSTEMA: {
        "name": "🇷🇺 INFINITE SYSTEMA: Russian Cross",
        "cost": 80, "dmg": (200, 300),
        "desc": "Vasco's Systema mastery. The Russian martial art at its peak."
    },
    Path.VASCO_MUAY_THAI: {
        "name": "🇹🇭 INFINITE MUAY THAI: Sunken Fist",
        "cost": 85, "dmg": (210, 310),
        "desc": "Vasco's Muay Thai legend. The fist that sank ships."
    },
    Path.JAY_KALI: {
        "name": "🇵🇭 INFINITE KALI: Twin Blade Dance",
        "cost": 75, "dmg": (190, 290),
        "desc": "Jay's Kali mastery. Twin blades moving as one — a whirlwind of steel."
    },
    Path.ELI_BEAST: {
        "name": "🦁 INFINITE BEAST: King of Beasts",
        "cost": 85, "dmg": (210, 310),
        "desc": "Eli's beast mode unleashed. Pure animal instinct."
    },
    Path.ELI_TOM_LEE: {
        "name": "🐅 INFINITE WILD: Inherited Instinct",
        "cost": 90, "dmg": (220, 320),
        "desc": "Eli inherits Tom Lee's wild style. The student surpasses the master."
    },
    Path.WARREN_JKD: {
        "name": "🥋 INFINITE JKD: Way of the Intercepting Fist",
        "cost": 75, "dmg": (190, 290),
        "desc": "Warren's Jeet Kune Do mastery. Bruce Lee's philosophy perfected."
    },
    Path.WARREN_CQC: {
        "name": "🔫 INFINITE CQC: NEW Full Release",
        "cost": 95, "dmg": (230, 330),
        "desc": "Warren's CQC operator technique. Military precision at its finest."
    },
    Path.WARREN_HEART: {
        "name": "💔 INFINITE HEART: One-Inch Punch",
        "cost": 80, "dmg": (200, 300),
        "desc": "Warren's heart attack punch. The one-inch punch that stops hearts."
    },
    Path.JAKE_CONVICTION: {
        "name": "⚖️ INFINITE CONVICTION: Will of Iron",
        "cost": 85, "dmg": (210, 310),
        "desc": "Jake's conviction-powered strikes. Willpower made manifest."
    },
    Path.JAKE_GAPRYONG: {
        "name": "👑 INFINITE BLOOD: Inherited Fist",
        "cost": 100, "dmg": (240, 340),
        "desc": "Jake's bloodline potential awakened. The same conviction that made his father the strongest."
    },
    Path.GUN_YAMAZAKI: {
        "name": "🏯 INFINITE YAMAZAKI: Black Bone",
        "cost": 110, "dmg": (250, 350),
        "desc": "Gun's Yamazaki heritage unleashed. The darkness within."
    },
    Path.GUN_CONSTANT_UI: {
        "name": "👁️ INFINITE UI: Perpetual Awakening",
        "cost": 120, "dmg": (260, 360),
        "desc": "Gun's constant Ultra Instinct. Always awakened, always perfect."
    },
    Path.GOO_MOONLIGHT: {
        "name": "🌙 INFINITE MOONLIGHT: Three Sword Style",
        "cost": 95, "dmg": (230, 330),
        "desc": "Goo's moonlight sword technique. Three swords, infinite possibilities."
    },
    Path.GOO_FIFTH: {
        "name": "✨ INFINITE FIFTH: Impossible Technique",
        "cost": 130, "dmg": (270, 370),
        "desc": "Goo's legendary fifth sword. A technique that shouldn't exist."
    },
    Path.JOONGOO_HWARANG: {
        "name": "⚔️ INFINITE HWARANG: Blade Dance",
        "cost": 100, "dmg": (240, 340),
        "desc": "Kim Jun-gu's Hwarang sword technique. Cuts that sever goblins."
    },
    Path.JOONGOO_ARMED: {
        "name": "🗡️ INFINITE ARMED: Top 3 When Armed",
        "cost": 110, "dmg": (250, 350),
        "desc": "Kim Jun-gu with his weapon. Top 3 in the world when armed."
    },
    Path.MANDEOK_POWER: {
        "name": "💪 INFINITE TITAN: Earth Shaker",
        "cost": 100, "dmg": (240, 340),
        "desc": "Mandeok's raw power unleashed. A strike that shakes the earth."
    },
    # FIX #5: Merged Cap Guy path into Manager Kim
    Path.MANAGER_KIM_CQC: {
        "name": "🔫 INFINITE CODE 66: Silver Yarn Execution",
        "cost": 95, "dmg": (230, 330),
        "desc": "Manager Kim's ultimate technique. Silver Yarn threads bind and Code 66 finishes. The true power of the Senior Manager revealed."
    },
    Path.XIAOLUNG_MUAY_THAI: {
        "name": "🇹🇭 INFINITE MUAY THAI: Death Blow",
        "cost": 90, "dmg": (220, 320),
        "desc": "Xiaolung's perfected Muay Thai. Elbows and knees become death."
    },
    Path.RYUHEI_YAKUZA: {
        "name": "⚔️ INFINITE YAKUZA: Gang Lord",
        "cost": 85, "dmg": (210, 310),
        "desc": "Ryuhei's yakuza style. Dirty fighting at its peak."
    },
    Path.SAMUEL_AMBITION: {
        "name": "👑 INFINITE AMBITION: King's Path",
        "cost": 95, "dmg": (230, 330),
        "desc": "Samuel's ambition-fueled power. The betrayer's strength knows no limits."
    },
    Path.SINU_INVISIBLE: {
        "name": "🌀 INFINITE INVISIBLE: Ghost Fist",
        "cost": 90, "dmg": (220, 320),
        "desc": "Sinu Han's invisible attacks. Unseeable, unavoidable."
    },
    # FIX #8: Logan Lee has NO infinity technique (he's a bully, not a martial artist)
    # Path.LOGAN_BULLY intentionally omitted from INFINITY_TECHNIQUES
    Path.VIN_JIN_SSIREUM: {
        "name": "🇰🇷 INFINITE SSIREUM: Wrestling God",
        "cost": 90, "dmg": (220, 320),
        "desc": "Vin Jin's perfected ssireum. Throws that break bones."
    },
    Path.SEONGJI_MARTIAL: {
        "name": "🥋 INFINITE MARTIAL: Triple Threat",
        "cost": 100, "dmg": (240, 340),
        "desc": "Seongji's combination of ssireum, judo, and kudo. A complete martial artist."
    },
    Path.HAN_JAEHA: {
        "name": "🤼 INFINITE TRADITION: Cheonliang Wrestling",
        "cost": 70, "dmg": (180, 280),
        "desc": "Han Jaeha's traditional ssireum. Pure Korean wrestling."
    },
    Path.BAEK_SEONG_TAEKKYON: {
        "name": "🦢 INFINITE FLOW: Taekkyon Dance",
        "cost": 75, "dmg": (190, 290),
        "desc": "Baek Seong's flowing taekkyon. Dance-like movements that confuse and destroy."
    },
    Path.SHINGEN_YAMAZAKI: {
        "name": "🏯 INFINITE YAMAZAKI: Syndicate's Wrath",
        "cost": 160, "dmg": (320, 450),
        "desc": "Shingen Yamazaki's ultimate. The head of the Yamazaki Syndicate unleashes full fury."
    },
    Path.PARK_FATHER: {
        "name": "❓ INFINITE MYSTERY: Bloodline Secret",
        "cost": 140, "dmg": (300, 400),
        "desc": "Park Jonggun's father's mysterious technique. The source of Gun's power."
    },
    Path.KIM_MINJAE_JUDO: {
        "name": "🥋 INFINITE JUDO: Police Force",
        "cost": 65, "dmg": (170, 270),
        "desc": "Kim Minjae's perfected judo throws. Law and order brought to the streets."
    },
    Path.DETECTIVE_KANG_BOXING: {
        "name": "🥊 INFINITE DETECTIVE: Veteran's Fist",
        "cost": 70, "dmg": (180, 280),
        "desc": "Detective Kang's veteran boxing. Years of experience packed into every punch."
    }
}


# ============================================================================
# BASE CHARACTER CLASS
# FIX #1: get_damage_multiplier() is the single source of truth for buffs.
#          Subclasses must NOT re-apply ui_mode or beast_mode — those are
#          handled here. Subclasses only add their OWN unique multipliers.
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
        self.realm_effect = None
        self.affiliation = ""
        self.canon_episode = 0
        self.path_level = 1
        self.path_exp = 0
        self.path_history = []

        self.stunned = False
        self.bound = False
        self.exhausted = False

        self.ui_mode = False
        self.ui_timer = 0
        self.beast_mode = False
        self.beast_timer = 0
        self.veinous_rage = False
        self.silver_yarn_active = False
        self.muscle_boost = False
        self.timed_buffs = {}  # FIX #16: {name: (multiplier, turns_remaining)}
        # Timed buff list: each entry is {'name': str, 'dmg_mult': float, 'def_mult': float, 'turns': int}
        self.temp_buffs = []
        # FIX #16: {name: (multiplier_float, turns_remaining)} — real timed buff system

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        # Apply temp defensive buffs
        for buff in self.temp_buffs:
            if buff.get('def_mult', 1.0) != 1.0:
                dmg = int(dmg * buff['def_mult'])
        if self.active_realm == Realm.TENACITY:
            dmg = int(dmg * 0.5)
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
        self.realm_effect = RealmEffect.apply(realm, self)
        self.form = f"REALM: {realm.name}"
        return f"\n✨ {realm.value} REALM ACTIVATED!\n{self.realm_effect['desc']}\n"

    def get_damage_multiplier(self):
        """
        Single source of truth for damage multipliers.
        FIX #1: Subclasses call super() and only ADD their own unique multipliers.
                 ui_mode, beast_mode, veinous_rage, muscle_boost all handled HERE.
                 Do NOT re-check these in subclass overrides.
        """
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
            buffs.append("👁️ UI")

        if self.beast_mode:
            mult *= 1.6
            buffs.append("🦁 BEAST")

        if self.veinous_rage:
            mult *= 1.8
            buffs.append("👁️ RAGE")

        if self.muscle_boost:
            mult *= 1.3
            buffs.append("💪 MUSCLE")

        # Timed buffs (BUG-04/05/06 fix): temp_buffs list entries
        for buff in self.temp_buffs:
            if buff.get('dmg_mult', 1.0) != 1.0:
                mult *= buff['dmg_mult']
                buffs.append(f"⚡{buff['name'][:8]}({buff['turns']}T)")

        return mult, buffs

    def apply_realm_regen(self):
        if self.active_realm == Realm.TENACITY:
            self.heal(15)
            return True
        return False

    def to_dict(self):
        return {
            'name': self.name,
            'path': self.path.name if self.path else None,
            'path_level': self.path_level,
            'path_exp': self.path_exp,
            'hp': self.hp,
            'energy': self.energy,
            'active_realm': self.active_realm.name if self.active_realm != Realm.NONE else None,
            'realm_timer': self.realm_timer,
            'form': self.form,
            'ui_mode': self.ui_mode,
            'ui_timer': self.ui_timer,
            'beast_mode': self.beast_mode,
            'beast_timer': self.beast_timer
        }

    def from_dict(self, data):
        if data.get('path'):
            for path in Path:
                if path.name == data['path']:
                    self.path = path
                    self.infinity_technique = INFINITY_TECHNIQUES.get(path)
                    break
        self.path_level = data.get('path_level', 1)
        self.path_exp = data.get('path_exp', 0)
        self.hp = data.get('hp', self.max_hp)
        self.energy = data.get('energy', self.max_energy)

        realm_name = data.get('active_realm')
        if realm_name:
            for realm in Realm:
                if realm.name == realm_name:
                    self.active_realm = realm
                    break
        self.realm_timer = data.get('realm_timer', 0)

        self.form = data.get('form', 'Normal')
        self.ui_mode = data.get('ui_mode', False)
        self.ui_timer = data.get('ui_timer', 0)
        self.beast_mode = data.get('beast_mode', False)
        self.beast_timer = data.get('beast_timer', 0)

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


# ============================================================================
# ENEMY CLASS
# ============================================================================

class Enemy(Character):
    def __init__(self, name, title, hp, energy, abilities, rank, affiliation="", realm_list=None):
        super().__init__(name, title, hp, energy, realm_list)
        self.abilities = {}
        for key, abil in abilities.items():
            self.abilities[key] = {
                "name": abil["name"],
                "dmg": abil["dmg"],
                "cost": abil.get("cost", 20),
                "type": abil.get("type", "damage"),
                "desc": abil.get("desc", f"{abil['name']} — a basic attack.")
            }
        self.rank = rank
        self.affiliation = affiliation
        self.ai_pattern = []


# ============================================================================
# PLAYABLE CHARACTERS
# ============================================================================

# ===== GEN 0 LEGENDS =====

class GapryongKim(Character):
    def __init__(self):
        super().__init__("Gapryong Kim", "The Strongest of Gen 0", 900, 400,
                         [Realm.SPEED, Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE, Realm.OVERCOMING])
        self.canon_episode = 0
        self.paths_available = [Path.GAPRYONG_CONVICTION]
        self.abilities = {
            '1': {"name": "👑 Conviction Punch", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "The foundation of Gapryong's style. A punch backed by unshakeable belief."},
            '2': {"name": "👑 Gapryong's Fist", "cost": 40, "dmg": (130, 180), "type": "damage",
                  "desc": "The legendary fist that defeated the Yamazaki Syndicate."},
            '3': {"name": "👑 Will to Protect", "cost": 35, "dmg": (110, 160), "type": "damage",
                  "desc": "A technique born from Gapryong's desire to protect his crew."},
            '4': {"name": "👑 Legend's Legacy", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "The accumulated power of a legend."},
            '5': {"name": "🛡️ Gapryong's Defense", "cost": 25, "dmg": (0, 0), "type": "utility",
                  "desc": "Defensive stance. Reduces incoming damage by 50% this turn."}
        }


class TomLee(Character):
    def __init__(self):
        super().__init__("Tom Lee", "The Wild", 850, 380,
                         [Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE])
        self.canon_episode = 0
        self.paths_available = [Path.TOM_LEE_WILD]
        self.abilities = {
            '1': {"name": "🐅 Wild Strike", "cost": 25, "dmg": (90, 140), "type": "damage",
                  "desc": "A primal, untamed strike. Tom Lee fights like a wild animal."},
            '2': {"name": "🐅 Tom Lee Special", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "Biting, clawing, and striking combined. His signature move."},
            '3': {"name": "🐅 Gen 0 Power", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Raw power from the legendary era."},
            '4': {"name": "🐅 Bite Force", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "Literally biting his opponents. Tom Lee's jaw strength rivals a wild animal."}
        }


class CharlesChoi(Character):
    def __init__(self):
        super().__init__("Charles Choi", "The Puppet Master", 800, 360,
                         [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 0
        self.paths_available = [Path.CHARLES_ELITE]
        self.abilities = {
            '1': {"name": "🎭 Invisible Strike", "cost": 30, "dmg": (90, 140), "type": "damage",
                  "desc": "A strike too fast to see. You only feel it after it's landed."},
            '2': {"name": "🎭 Chairman's Authority", "cost": 40, "dmg": (120, 170), "type": "damage",
                  "desc": "The power of the HNH Group chairman. Decades of manipulation made manifest."},
            '3': {"name": "🎭 Elite Technique", "cost": 35, "dmg": (110, 160), "type": "damage",
                  "desc": "A technique passed down through Gapryong's Fist. Refined, elegant, lethal."},
            '4': {"name": "🎭 Truth of Two Bodies", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "The secret behind the two bodies mystery. His ultimate technique."}
        }


class JinyoungPark(Character):
    def __init__(self):
        super().__init__("Jinyoung Park", "The Medical Genius", 780, 350, [Realm.TECHNIQUE])
        self.canon_episode = 0
        self.paths_available = [Path.JINYOUNG_COPY]
        self.abilities = {
            '1': {"name": "🔄 Copy: Taekwondo", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Perfect replication of Taekwondo. Jinyoung's genius copies any art after one viewing."},
            '2': {"name": "🔄 Copy: Karate", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Flawless Karate. Precision of a master via pure analytical ability."},
            '3': {"name": "🔄 Copy: Boxing", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "World-class boxing, mechanically perfect."},
            '4': {"name": "🔄 Copy: Judo", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Perfect Judo throws, replicating the master's movements exactly."},
            '5': {"name": "🔄 Copy: Systema", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Russian Systema techniques replicated. Jinyoung's breadth of copies is limitless."},
            '6': {"name": "🔄 Medical Precision", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "Combining medical knowledge with combat. Strikes vital points with surgical accuracy."}
        }


class Baekho(Character):
    def __init__(self):
        super().__init__("Baekho", "The White Tiger", 820, 370, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 0
        self.paths_available = [Path.BAEKHO_BEAST]
        self.abilities = {
            '1': {"name": "🐯 Tiger Strike", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "A strike with the ferocity of a white tiger."},
            '2': {"name": "🐯 Beast Mode", "cost": 40, "dmg": (130, 180), "type": "damage",
                  "desc": "Unleashing his inner beast. Attacks become savage and unpredictable."},
            '3': {"name": "🐯 White Tiger's Claw", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "Raking claw strikes that tear through defenses. The White Tiger's signature."}
        }


# ===== 1ST GENERATION KINGS =====

class JamesLee(Character):
    def __init__(self):
        super().__init__("James Lee", "Legend of 1st Gen", 880, 390, [Realm.SPEED, Realm.TECHNIQUE])
        self.canon_episode = 0
        self.paths_available = [Path.JAMES_LEE_INVISIBLE]
        self.abilities = {
            '1': {"name": "👑 Invisible Kick", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "A kick that can't be seen. James Lee's speed transcends human perception."},
            '2': {"name": "👑 Perfect Form", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Technique perfected to its absolute peak. Every movement economical and deadly."},
            '3': {"name": "👑 One Man Circle", "cost": 50, "dmg": (170, 220), "type": "damage",
                  "desc": "The technique that dismantled the 1st Generation. A devastating combination."},
            '4': {"name": "👑 Legend's Speed", "cost": 30, "dmg": (0, 0), "type": "buff",
                  "desc": "Tapping into legendary speed. +30% damage for 3 turns."}
        }


class GitaeKim(Character):
    def __init__(self):
        super().__init__("Gitae Kim", "Gapryong's Unknown Heir", 860, 380, [Realm.STRENGTH, Realm.OVERCOMING])
        self.canon_episode = 0
        self.paths_available = [Path.GITAE_KIM]
        self.abilities = {
            '1': {"name": "⚡ Gapryong's Blood", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "The blood of Gapryong flows through him. Gitae strikes with legendary inherited force."},
            '2': {"name": "⚡ Inherited Power", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Power passed down through generations. The full potential of his bloodline."},
            '3': {"name": "⚡ King's Authority", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "The commanding presence of Seoul's king."}
        }


class JichangKwak(Character):
    def __init__(self):
        super().__init__("Jichang Kwak", "King of Seoul", 800, 360, [Realm.SPEED, Realm.STRENGTH])
        self.canon_episode = 0
        self.paths_available = [Path.JICHANG_HAND_BLADE]
        self.abilities = {
            '1': {"name": "🩷 Hand Blade", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "Jichang's signature technique. His hand becomes like a forged blade."},
            '2': {"name": "🩷 Double Edge", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "A devastating combination of two hand blade strikes."},
            '3': {"name": "🩷 Seoul King's Pride", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "The pride of Seoul's king manifested."}
        }


class TaesooMa(Character):
    def __init__(self):
        super().__init__("Taesoo Ma", "King of Ansan", 820, 350, [Realm.STRENGTH])
        self.canon_episode = 0
        self.paths_available = [Path.TAESOO_MA_FIST]
        self.abilities = {
            '1': {"name": "🔴 Right Hand", "cost": 35, "dmg": (130, 180), "type": "damage",
                  "desc": "Taesoo's legendary right fist. No technique — just overwhelming power."},
            '2': {"name": "🔴 No Technique", "cost": 40, "dmg": (150, 200), "type": "damage",
                  "desc": "Pure raw strength. Taesoo abandons all pretense and simply destroys."},
            '3': {"name": "🔴 Ansan King", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "The pride of Ansan. Taesoo's reign as undisputed king."}
        }


class GongseobJi(Character):
    def __init__(self):
        # FIX: Added SPEED realm — Gongseob is a speed + iron body fighter, not pure technique
        super().__init__("Gongseob Ji", "The Monk", 750, 340, [Realm.SPEED, Realm.TECHNIQUE])
        self.canon_episode = 0
        self.paths_available = [Path.GONGSEOB_IRON]
        self.abilities = {
            '1': {"name": "🩷 Iron Boxing", "cost": 25, "dmg": (90, 140), "type": "damage",
                  "desc": "Gongseob's style combining speed with iron-like durability."},
            '2': {"name": "🩷 Speed Technique", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "Blazing fast strikes blurring offense and defense."},
            '3': {"name": "🩷 Tungsten Defense", "cost": 20, "dmg": (0, 0), "type": "utility",
                  "desc": "Impenetrable defensive stance. Gongseob's body becomes as hard as tungsten. -70% damage this turn."}
        }


class SeokduWang(Character):
    def __init__(self):
        super().__init__("Seokdu Wang", "King of Suwon", 780, 330, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 0
        self.paths_available = [Path.SEOKDU_HEADBUTT]
        self.abilities = {
            '1': {"name": "💢 Headbutt", "cost": 30, "dmg": (120, 170), "type": "damage",
                  "desc": "Seokdu's primary weapon — his forehead. Harder than steel."},
            '2': {"name": "💢 Iron Forehead", "cost": 25, "dmg": (100, 150), "type": "damage",
                  "desc": "Years of training made Seokdu's forehead unbreakable. Force of a battering ram."},
            '3': {"name": "💢 Suwon's Crown", "cost": 35, "dmg": (140, 190), "type": "damage",
                  "desc": "The king's ultimate headbutt. Full body weight behind his signature move."}
        }


class JaegyeonNa(Character):
    def __init__(self):
        super().__init__("Jaegyeon Na", "King of Incheon", 770, 360, [Realm.SPEED])
        self.canon_episode = 544
        self.paths_available = [Path.JAEGYEON_SPEED]
        self.abilities = {
            '1': {"name": "🔵 Incheon Speed", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "The speed of Incheon's king. Moves faster than the eye can track."},
            '2': {"name": "🔵 Faster Than Light", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Speed approaching the absolute limit of human capability."},
            '3': {"name": "🔵 King of Incheon", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "The pride of Incheon manifested. A flurry that overwhelms any defense."}
        }


class SeongjiYuk(Character):
    def __init__(self):
        super().__init__("Seongji Yuk", "The Monster of Cheonliang", 820, 370,
                         [Realm.STRENGTH, Realm.TECHNIQUE, Realm.OVERCOMING])
        self.canon_episode = 500
        self.paths_available = [Path.SEONGJI_MONSTER, Path.SEONGJI_MARTIAL]
        self.abilities = {
            '1': {"name": "🇰🇷 Ssireum: Throw", "cost": 25, "dmg": (90, 140), "type": "damage",
                  "desc": "Traditional Korean wrestling. Seongji uses momentum against opponents."},
            '2': {"name": "🥋 Judo: Ippon", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "A perfect Judo throw. Seongji controls any opponent."},
            '3': {"name": "🥋 Kudo: Dirty Boxing", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "The brutal striking of Kudo combined with his grappling base."},
            '4': {"name": "🦍 Monster Mode", "cost": 45, "dmg": (160, 210), "type": "damage",
                  "desc": "Unleashing his monstrous side. Pure savage power."}
        }


class Jinrang(Character):
    def __init__(self):
        super().__init__("Jinrang", "King of Busan", 830, 380, [Realm.STRENGTH, Realm.OVERCOMING])
        self.canon_episode = 580
        self.affiliation = "Busan / Gapryong's Disciple"  # FIX #20
        self.paths_available = [Path.JINRANG_CONVICTION]
        self.abilities = {
            '1': {"name": "👑 Jinrang's Conviction", "cost": 35, "dmg": (130, 180), "type": "damage",
                  "desc": "The conviction of Gapryong's true disciple. Carries the same weight as his master's strikes."},
            '2': {"name": "👑 Gapryong's Disciple", "cost": 40, "dmg": (150, 200), "type": "damage",
                  "desc": "Techniques passed directly from Gapryong. The legacy of the strongest."},
            '3': {"name": "👑 Busan King", "cost": 45, "dmg": (170, 220), "type": "damage",
                  "desc": "The authority of Busan's king. Commands respect with every strike."},
            '4': {"name": "👑 True Conviction", "cost": 60, "dmg": (200, 250), "type": "damage",
                  "desc": "The ultimate expression of his faith in Gapryong's teachings. A fist that cannot be denied."}
        }


# ===== GEN 2 CREW LEADERS =====

class DanielPark(Character):
    def __init__(self, episode_state="current"):
        # FIX #10: Reduced base HP to reflect early-story Daniel's weakness
        super().__init__("Daniel Park", "The Second Body", 320, 300,
                         [])  # FIX #21: Daniel has no confirmed Gyeongji in manhwa
        self.episode_state = episode_state
        self.canon_episode = 581
        self.sophia_trained = True
        self.jichang_copied = True
        self.gapryong_copied = True
        self.form = "Normal"
        self.switch_available = True
        self.paths_available = [Path.DANIEL_UI, Path.DANIEL_COPY]
        self.abilities = {
            '1': {"name": "👊 Desperate Flailing", "cost": 10, "dmg": (20, 35), "type": "damage",
                  "desc": "Early Daniel's fighting style — wild, uncoordinated swings born of desperation."},
            '2': {"name": "🔄 Instinctive Copy", "cost": 20, "dmg": (30, 50), "type": "damage",
                  "desc": "Daniel's natural copying ability. Reactive and instinctive, not deliberate."},
            '3': {"name": "🇷🇺 Systema: Ryabina", "cost": 25, "dmg": (50, 70), "type": "damage",
                  "desc": "A Systema technique learned from Sophia. Targets vital points."},
            '4': {"name": "⚡ Copy: Zack's Counter", "cost": 25, "dmg": (55, 80), "type": "damage",
                  "desc": "Daniel replicates Zack Lee's signature counter punch."},
            '5': {"name": "⚡ Copy: Vasco's Sunken Fist", "cost": 30, "dmg": (65, 90), "type": "damage",
                  "desc": "Vasco's Muay Thai technique, instinctively copied."},
            '6': {"name": "⚡ Copy: Eli's Animal Instinct", "cost": 30, "dmg": (70, 95), "type": "damage",
                  "desc": "Eli Jang's wild style replicated. Daniel fights with animalistic movements."},
            '7': {"name": "⚡ Copy: Jake's Conviction", "cost": 35, "dmg": (75, 105), "type": "damage",
                  "desc": "Jake Kim's conviction-powered strikes."},
            '8': {"name": "⚡ Copy: Johan's Choreography", "cost": 40, "dmg": (80, 115), "type": "damage",
                  "desc": "Johan Seong's dance combat. Daniel flows through attacks like a performance."},
            '9': {"name": "⚡ Copy: Gun's Taekwondo", "cost": 35, "dmg": (80, 110), "type": "damage",
                  "desc": "Gun Park's Taekwondo mastery. Spinning kicks with perfect form."},
            '10': {"name": "🩷 Jichang's Hand Blade", "cost": 45, "dmg": (90, 130), "type": "damage",
                   "desc": "Jichang Kwak's legendary technique. Daniel's hand becomes a blade."},
            '11': {"name": "👑 Gapryong's Conviction", "cost": 60, "dmg": (120, 180), "type": "damage",
                   "desc": "The ultimate copy — Gapryong Kim's legendary fist."},
            '12': {"name": "👁️ Ultra Instinct", "cost": 100, "dmg": (0, 0), "type": "ui",
                   "desc": "Daniel's ultimate awakening. Body moves before mind. +150% damage for 3 turns."}
        }

    def activate_ui(self):
        self.ui_mode = True
        self.ui_timer = 3
        self.form = "ULTRA INSTINCT"
        self.heal(50)
        return "👁️👁️👁️ ULTRA INSTINCT! White hair awakens! Daniel's body moves on its own!"

    # FIX #1: No ui_mode re-check here — base class handles it


class ZackLee(Character):
    def __init__(self):
        super().__init__("Zack Lee", "The Iron Boxer", 380, 280, [])  # FIX #22
        self.canon_episode = 1
        self.paths_available = [Path.ZACK_IRON]
        self.heat_mode = False
        self.abilities = {
            '1': {"name": "🔨 Iron Fortress Stance", "cost": 15, "dmg": (0, 0), "type": "utility",
                  "desc": "Defensive iron stance. -50% damage for 2 turns."},
            '2': {"name": "🔨 Iron Fist", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Zack's fists become as hard as iron. Straightforward but powerful."},
            '3': {"name": "🥊 Jab", "cost": 15, "dmg": (35, 55), "type": "damage",
                  "desc": "Lightning-fast jab to measure distance and set up heavier strikes."},
            '4': {"name": "🥊 Cross", "cost": 20, "dmg": (45, 70), "type": "damage",
                  "desc": "Full body weight behind this cross."},
            '5': {"name": "⚡ Counter Punch", "cost": 30, "dmg": (75, 110), "type": "damage",
                  "desc": "Zack's specialty. Waits for commitment, strikes with perfect timing."},
            '6': {"name": "💫 Shining Star", "cost": 50, "dmg": (100, 150), "type": "damage",
                  "desc": "Zack's ultimate technique. A blinding combination — the star shines brightest."}
        }


class JohanSeong(Character):
    """
    Johan Seong — The God Eye (blind).
    FIX #3: to_dict/from_dict now serializes copy data fully.
    FIX #4: God Eye uses god_eye_timer (turn-based) not random 10% decay.
    FIX #1: get_damage_multiplier only adds Johan-specific bonuses;
            base class handles ui/beast/rage/muscle.
    Canon note: Johan copies via SOUND/VIBRATION (blind), not sight.
                Copy chance is based on technique complexity (enemy rank proxy),
                not raw rank value.
    """
    def __init__(self, blind=True):
        super().__init__("Johan Seong", "The God Eye", 400, 300,
                         [Realm.TECHNIQUE, Realm.SPEED, Realm.OVERCOMING])
        self.canon_episode = 55
        self.blind = blind
        self.god_eye_active = False
        self.god_eye_timer = 0          # FIX #4: proper turn timer
        self.copy_count = 0
        self.max_copy = 10
        self.copied_techniques = []
        self.copied_techniques_data = {}
        self.technique_view_count = {}
        self.paths_available = [Path.JOHAN_GOD_EYE, Path.JOHAN_CHOREOGRAPHY]

        self.abilities = {
            '1': {"name": "👁️ Copy: Taekwondo", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "God Eye analyzes and replicates Taekwondo via vibration and sound."},
            '2': {"name": "👁️ Copy: Boxing", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Perfect boxing replication. Jabs and crosses with champion precision."},
            '3': {"name": "👁️ Copy: Karate", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Traditional Karate strikes. Powerful linear techniques with devastating focus."},
            '4': {"name": "👁️ Copy: Judo", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Judo throws. Johan uses an opponent's momentum with mechanical precision."},
            '5': {"name": "👁️ Copy: Aikido", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Aikido's flowing redirection. Johan turns attacks back on users."},
            '6': {"name": "👁️ Copy: Capoeira", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Dance-like Capoeira movements. Johan weaves and strikes in continuous flow."},
            '7': {"name": "💃 Choreography: God Dog", "cost": 40, "dmg": (85, 120), "type": "damage",
                  "desc": "Johan's original style born from K-Pop choreography. A deadly dance."},
            '8': {"name": "💃 Choreography: Perfected", "cost": 45, "dmg": (95, 140), "type": "damage",
                  "desc": "The ultimate expression of his dance combat. Every movement flows perfectly."},
            '9': {"name": "👁️ God Eye Activation", "cost": 30, "dmg": (0, 0), "type": "buff",
                  "desc": "Activates God Eye for 5 turns. +30% copy chance. Johan senses techniques through vibration."},
        }
        if blind:
            self.abilities['10'] = {
                "name": "🕶️ Blindness (Overcoming)", "cost": 0, "dmg": (0, 0), "type": "passive",
                "desc": "Johan fights despite blindness. Other senses sharpen. +30% damage from overcoming."
            }
            self.title = "The Blind God Eye"

    def activate_god_eye(self):
        self.god_eye_active = True
        self.god_eye_timer = 5   # FIX #4: 5-turn timer
        self.form = "GOD EYE AWAKENED"
        return "👁️👁️👁️ GOD EYE ACTIVATED for 5 turns! All techniques become readable! +30% copy chance!"

    def copy_technique(self, enemy_technique, target=None):
        if enemy_technique in self.technique_view_count:
            self.technique_view_count[enemy_technique] += 1
        else:
            self.technique_view_count[enemy_technique] = 1

        if enemy_technique in self.copied_techniques:
            if enemy_technique in self.copied_techniques_data:
                old_data = self.copied_techniques_data[enemy_technique]
                new_views = self.technique_view_count[enemy_technique]
                base_dmg = 60
                view_bonus = min(50, new_views * 5)
                new_dmg = base_dmg + view_bonus
                key = old_data["key"]
                self.abilities[key]["dmg"] = (new_dmg, new_dmg + 30)
                self.abilities[key]["views"] = new_views
                self.abilities[key]["desc"] = (f"Johan's copied {enemy_technique}. "
                                               f"Heard {new_views} times, dealing {new_dmg}-{new_dmg+30} dmg.")
                self.copied_techniques_data[enemy_technique]["views"] = new_views
                self.copied_techniques_data[enemy_technique]["damage"] = (new_dmg, new_dmg + 30)
                return f"🔄 {enemy_technique} improved! (Heard {new_views}×, +{view_bonus} dmg)"
            return f"Already copied {enemy_technique}"

        if self.copy_count >= self.max_copy:
            return None

        self.copied_techniques.append(enemy_technique)
        self.copy_count += 1
        base_dmg = 60
        view_bonus = min(50, self.technique_view_count[enemy_technique] * 5)
        total_dmg = base_dmg + view_bonus
        new_key = str(10 + self.copy_count)
        self.abilities[new_key] = {
            "name": f"👁️ Copy: {enemy_technique}",
            "cost": 25,
            "dmg": (total_dmg, total_dmg + 30),
            "type": "damage",
            "views": self.technique_view_count[enemy_technique],
            "desc": (f"Johan's God Eye copies {enemy_technique}. "
                     f"Heard {self.technique_view_count[enemy_technique]}×, "
                     f"dealing {total_dmg}-{total_dmg+30} dmg.")
        }
        self.copied_techniques_data[enemy_technique] = {
            "key": new_key,
            "views": self.technique_view_count[enemy_technique],
            "damage": (total_dmg, total_dmg + 30)
        }
        v = self.technique_view_count[enemy_technique]
        return f"✅ Johan copies {enemy_technique}! (Heard {v}×)"

    def calculate_copy_chance(self, technique_name, target, enemy_rank):
        """
        FIX: Canon-accurate copy chance — complexity-based (rank as proxy),
             not raw rank value. Lower rank = harder/more complex technique.
        """
        chance = 0.3
        factors = []

        if self.god_eye_active:
            chance += 0.3
            factors.append("God Eye (+30%)")

        if technique_name in self.technique_view_count:
            view_bonus = min(0.6, self.technique_view_count[technique_name] * 0.2)
            if view_bonus > 0:
                chance += view_bonus
                factors.append(f"Heard {self.technique_view_count[technique_name]}× (+{int(view_bonus*100)}%)")

        if target == self:
            chance += 0.4
            factors.append("Direct hit (+40%)")

        if self.hp < self.max_hp * 0.5:
            chance += 0.2
            factors.append("Low HP / Overcoming (+20%)")

        # FIX: More complex techniques (lower rank = stronger fighter) are HARDER to copy
        if enemy_rank < 10:
            chance -= 0.1
            factors.append("Elite technique (-10%)")
        elif enemy_rank < 30:
            chance += 0.05
            factors.append("Advanced technique (+5%)")

        chance = min(0.9, max(0.05, chance))
        return chance, factors

    def get_copy_stats(self):
        print(f"\n📊 JOHAN'S COPY STATISTICS:")
        print(f"   • Techniques Copied: {self.copy_count}/{self.max_copy}")
        print(f"   • God Eye Active: {'✅' if self.god_eye_active else '❌'} "
              f"({'%d turns left' % self.god_eye_timer if self.god_eye_active else 'inactive'})")
        print(f"   • Blindness: {'✅' if self.blind else '❌'} (+30% dmg overcoming)")
        print(f"\n   📖 COPIED TECHNIQUES:")
        for tech, data in self.copied_techniques_data.items():
            print(f"      • {tech}: Heard {data['views']}× | DMG: {data['damage'][0]}-{data['damage'][1]}")
        if self.technique_view_count:
            print(f"\n   👁️ TECHNIQUES OBSERVED (not yet copied):")
            for tech, views in self.technique_view_count.items():
                if tech not in self.copied_techniques:
                    print(f"      • {tech}: Heard {views}×")

    def get_damage_multiplier(self):
        # FIX #1: Base class handles ui/beast/rage. We only add Johan-unique bonuses.
        mult, buffs = super().get_damage_multiplier()

        if self.god_eye_active:
            mult *= 1.8
            buffs.append("👁️ GOD EYE")

        if self.blind:
            mult *= 1.3
            buffs.append("🕶️ BLIND OVERCOMING")

        if self.copy_count > 0:
            technique_mastery = 1.0 + (self.copy_count * 0.02)
            mult *= technique_mastery
            buffs.append(f"📚 {self.copy_count} TECHS")

        return mult, buffs

    def to_dict(self):
        # FIX #3: Serialize all copy state
        d = super().to_dict()
        d['god_eye_active'] = self.god_eye_active
        d['god_eye_timer'] = self.god_eye_timer
        d['copy_count'] = self.copy_count
        d['copied_techniques'] = self.copied_techniques
        d['copied_techniques_data'] = self.copied_techniques_data
        d['technique_view_count'] = self.technique_view_count
        d['blind'] = self.blind
        return d

    def from_dict(self, data):
        # FIX #3: Restore all copy state
        super().from_dict(data)
        self.god_eye_active = data.get('god_eye_active', False)
        self.god_eye_timer = data.get('god_eye_timer', 0)
        self.copy_count = data.get('copy_count', 0)
        self.copied_techniques = data.get('copied_techniques', [])
        self.copied_techniques_data = data.get('copied_techniques_data', {})
        self.technique_view_count = data.get('technique_view_count', {})
        self.blind = data.get('blind', True)

        # Rebuild copied ability slots from saved data
        for tech_name, tech_data in self.copied_techniques_data.items():
            key = tech_data.get('key')
            dmg = tech_data.get('damage', (60, 90))
            views = tech_data.get('views', 1)
            if key:
                self.abilities[key] = {
                    "name": f"👁️ Copy: {tech_name}",
                    "cost": 25,
                    "dmg": tuple(dmg),
                    "type": "damage",
                    "views": views,
                    "desc": f"Johan's copied {tech_name}. Heard {views}×, dealing {dmg[0]}-{dmg[1]} dmg."
                }


class Vasco(Character):
    def __init__(self):
        super().__init__("Vasco", "The Hero of Justice", 450, 260, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 1
        self.paths_available = [Path.VASCO_SYSTEMA, Path.VASCO_MUAY_THAI]
        self.affiliation = "Burn Knuckles"
        self.abilities = {
            '1': {"name": "🇷🇺 Systema: Ryabina", "cost": 20, "dmg": (50, 70), "type": "damage",
                  "desc": "Russian Systema vital-point strike learned from Sophia."},
            '2': {"name": "🇷🇺 Russian Cross", "cost": 35, "dmg": (75, 105), "type": "damage",
                  "desc": "Devastating Systema combination. Crosses opponents' defenses brutally."},
            '3': {"name": "🇹🇭 Muay Thai: Death Blow", "cost": 40, "dmg": (90, 130), "type": "damage",
                  "desc": "Vasco's signature Muay Thai. A devastating elbow or knee that ends fights."},
            '4': {"name": "👊 Sunken Fist", "cost": 30, "dmg": (70, 100), "type": "damage",
                  "desc": "The fist that sank ships. Vasco's ultimate, born from Brekdak training."}
        }


class JayHong(Character):
    def __init__(self):
        super().__init__("Jay Hong", "The Silent Blade", 380, 270, [])  # FIX #22
        self.canon_episode = 1
        self.paths_available = [Path.JAY_KALI]
        self.abilities = {
            '1': {"name": "🇷🇺 Systema: Neutralizer", "cost": 20, "dmg": (45, 65), "type": "damage",
                  "desc": "A Systema counter. Jay neutralizes threats with silent efficiency."},
            '2': {"name": "🇵🇭 Kali: Double Baston", "cost": 25, "dmg": (50, 75), "type": "damage",
                  "desc": "Filipino Kali stick fighting. Twin weapons with deadly precision."},
            '3': {"name": "🇵🇭 Kali: Karambit", "cost": 30, "dmg": (65, 90), "type": "damage",
                  "desc": "The curved blade of Kali. Hooks around defenses devastatingly."},
            '4': {"name": "🛡️ Motorcycle Helmet", "cost": 15, "dmg": (0, 0), "type": "utility",
                  "desc": "Jay's signature defense. Helmet as shield — -50% damage this turn."}
        }


class EliJang(Character):
    def __init__(self):
        super().__init__("Eli Jang", "The Wild", 410, 260, [])  # FIX #22
        self.canon_episode = 150
        self.paths_available = [Path.ELI_BEAST, Path.ELI_TOM_LEE]
        self.abilities = {
            '1': {"name": "🐺 Wolf Strike", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Eli strikes like a wolf — sudden, savage, aimed at vital points."},
            '2': {"name": "🦅 Talon Kick", "cost": 25, "dmg": (60, 85), "type": "damage",
                  "desc": "A kick like an eagle's talon. Striking precision almost animalistic."},
            '3': {"name": "🦁 Beast Mode", "cost": 45, "dmg": (0, 0), "type": "buff",
                  "desc": "Unleashing his inner beast. Purely instinctual. +60% damage for 3 turns."},
            '4': {"name": "👴 Tom Lee Special", "cost": 40, "dmg": (85, 125), "type": "damage",
                  "desc": "The wild technique inherited from Tom Lee. Beast style meets legendary wildness."}
        }

    def activate_beast_mode(self):
        self.beast_mode = True
        self.beast_timer = 3
        return "🦁🦁🦁 BEAST MODE! Eli abandons all technique for pure animal instinct! +60% damage!"

    # FIX #1: Removed redundant beast_mode re-check.
    #          Base class already multiplies by 1.6 when beast_mode is True.
    #          This override only exists to keep activate_beast_mode() accessible.


class WarrenChae(Character):
    def __init__(self):
        super().__init__("Warren Chae", "Gangdong's Mighty", 390, 260, [Realm.STRENGTH])
        self.canon_episode = 277
        self.paths_available = [Path.WARREN_JKD, Path.WARREN_CQC, Path.WARREN_HEART]
        self.exhausted = False
        self.abilities = {
            '1': {"name": "🥋 Jeet Kune Do: Interception", "cost": 20, "dmg": (55, 80), "type": "damage",
                  "desc": "Bruce Lee's philosophy — intercepting before the attack fully forms."},
            '2': {"name": "🔫 CQC Foundation", "cost": 30, "dmg": (70, 100), "type": "damage",
                  "desc": "Close Quarters Combat fundamentals honed with Manager Kim."},
            '3': {"name": "⚡ NEW CQC: Full Release", "cost": 70, "dmg": (120, 170), "type": "damage",
                  "desc": "The complete CQC system unleashed. Causes exhaustion afterward."},
            '4': {"name": "💔 Heart Attack Punch", "cost": 60, "dmg": (110, 160), "type": "damage",
                  "desc": "The legendary one-inch punch. Massive force from zero distance."}
        }


class JakeKim(Character):
    def __init__(self):
        super().__init__("Jake Kim", "The Conviction", 430, 270, [Realm.OVERCOMING])
        self.canon_episode = 200
        self.paths_available = [Path.JAKE_CONVICTION, Path.JAKE_GAPRYONG]
        self.abilities = {
            '1': {"name": "⚖️ Conviction Punch", "cost": 25, "dmg": (60, 85), "type": "damage",
                  "desc": "A punch backed by pure conviction. Jake's willpower manifests in every strike."},
            '2': {"name": "👑 Inherited Will", "cost": 50, "dmg": (95, 140), "type": "damage",
                  "desc": "The will of Gapryong flows through his son. Legendary determination tapped."},
            '3': {"name": "👑 Gapryong's Blood", "cost": 70, "dmg": (120, 180), "type": "damage",
                  "desc": "Bloodline potential awakened. Jake strikes with inherited force."},
            '4': {"name": "⚖️ Conviction Mode", "cost": 45, "dmg": (0, 0), "type": "buff",
                  "desc": "State of pure conviction. +50% damage for 3 turns."}
        }


class GunPark(Character):
    def __init__(self):
        super().__init__("Gun Park", "Legend of Gen 1", 500, 320,
                         [Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE])
        self.canon_episode = 300
        self.paths_available = [Path.GUN_YAMAZAKI, Path.GUN_CONSTANT_UI]
        self.permanent_ui = True
        self.abilities = {
            '1': {"name": "🥋 Taekwondo: Roundhouse", "cost": 20, "dmg": (65, 90), "type": "damage",
                  "desc": "Gun's Taekwondo mastery. Spinning roundhouse with devastating power."},
            '2': {"name": "🥋 Kyokushin: Straight", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "The straight punch of Kyokushin Karate. Massive power from hip rotation."},
            '3': {"name": "🖤 Black Bone", "cost": 70, "dmg": (130, 200), "type": "damage",
                  "desc": "The legendary Yamazaki technique. Passed down through generations."},
            '4': {"name": "👁️ Constant UI [PASSIVE — always +30%]", "cost": 0, "dmg": (0, 0), "type": "passive",
                  "desc": "Gun exists in perpetual Ultra Instinct. Always active: +30% to all damage."}
        }

    def get_damage_multiplier(self):
        # FIX #23: Constant UI always active (not HP-gated)
        mult, buffs = super().get_damage_multiplier()
        if self.permanent_ui:
            mult *= 1.3
            buffs.append("👁️ CONSTANT UI")
        return mult, buffs


class GooKim(Character):
    def __init__(self):
        super().__init__("Goo Kim", "The Moonlight Sword", 480, 300, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 300
        self.paths_available = [Path.GOO_MOONLIGHT, Path.GOO_FIFTH]
        self.abilities = {
            '1': {"name": "🖊️ Pen Sword", "cost": 15, "dmg": (45, 70), "type": "damage",
                  "desc": "Goo's signature — even a pen becomes lethal in his hands."},
            '2': {"name": "🌙 First Sword: Early Moon", "cost": 30, "dmg": (75, 105), "type": "damage",
                  "desc": "Rising crescent slash that catches opponents off guard."},
            '3': {"name": "🌓 Second Sword: Crescent Moon", "cost": 35, "dmg": (80, 115), "type": "damage",
                  "desc": "Sweeping horizontal slash covering wide arcs."},
            '4': {"name": "🌕 Third Sword: Full Moon", "cost": 45, "dmg": (100, 145), "type": "damage",
                  "desc": "Complete circular motion striking from all directions."},
            '5': {"name": "🌑 Zero Sword: Lunar Eclipse", "cost": 60, "dmg": (130, 190), "type": "counter",
                  "desc": "Ultimate counter. Perfect stillness, then strikes when the moon is darkest."},
            '6': {"name": "✨ Fifth Sword", "cost": 90, "dmg": (170, 250), "type": "damage",
                  "desc": "The legendary fifth sword. A technique that shouldn't exist."}
        }


class KimJungu(Character):
    def __init__(self):
        super().__init__("Kim Jun-gu", "The Hwarang Sword", 520, 290, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 500
        self.paths_available = [Path.JOONGOO_HWARANG, Path.JOONGOO_ARMED]
        self.abilities = {
            '1': {"name": "🖊️ Pen Pierce", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "A pen becomes a deadly weapon. Jun-gu's precision with any object."},
            '2': {"name": "🔗 Chain Whip", "cost": 30, "dmg": (75, 110), "type": "damage",
                  "desc": "Using a chain as a whip. Unpredictable at any range."},
            '3': {"name": "⚔️ Hwarang Sword", "cost": 60, "dmg": (140, 210), "type": "damage",
                  "desc": "The ancient sword technique of the Hwarang warriors."},
            '4': {"name": "⚔️ Hwarang: Blade Dance", "cost": 70, "dmg": (160, 240), "type": "damage",
                  "desc": "Ultimate Hwarang technique. A blade dance with no openings."}
        }


# FIX #5: Cap Guy IS Manager Kim. One unified character.
# "Cap Guy" was Manager Kim before his identity was revealed.
class ManagerKim(Character):
    def __init__(self):
        super().__init__("Manager Kim", "The Senior Manager", 480, 300,
                         [Realm.TECHNIQUE, Realm.TENACITY, Realm.STRENGTH])
        self.canon_episode = 290
        self.code_66 = True
        self.veinous_rage = False
        self.silver_yarn_active = False
        # Affiliation FIX: Manager Kim works for the Cheonliang/Workers organization
        self.affiliation = "Workers"
        self.paths_available = [Path.MANAGER_KIM_CQC]
        self.abilities = {
            '1': {"name": "🎖️ Special Forces Training", "cost": 0, "dmg": (0, 0), "type": "passive",
                  "desc": "Manager Kim's military background. Always combat-ready. Passive: +10% all damage."},
            '2': {"name": "🔫 CQC: Vital Strikes", "cost": 25, "dmg": (65, 90), "type": "damage",
                  "desc": "Close Quarters Combat targeting vital points. Surgical precision."},
            '3': {"name": "⚪ Silver Yarn: Thread Bind", "cost": 20, "dmg": (0, 0), "type": "utility",
                  "desc": "Silver yarn binds opponents with near-invisible threads. 60% immobilize chance."},
            '4': {"name": "66 CODE: Full Release", "cost": 70, "dmg": (130, 190), "type": "damage",
                  "desc": "The legendary Code 66. Manager Kim's ultimate, born from his most dangerous missions."}
        }

    def get_damage_multiplier(self):
        # Special Forces passive: +10% all damage
        mult, buffs = super().get_damage_multiplier()
        mult *= 1.1
        buffs.append("🎖️ SF TRAINING")
        return mult, buffs


# Create alias for backward compatibility and story reveal
CapGuy = ManagerKim


# ===== WORKERS =====

class Mandeok(Character):
    def __init__(self):
        super().__init__("Mandeok", "The Titan", 480, 300, [Realm.STRENGTH])
        self.canon_episode = 400
        self.paths_available = [Path.MANDEOK_POWER]
        self.abilities = {
            '1': {"name": "💪 Power Punch", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "A punch backed by titanic strength. No technique, just overwhelming power."},
            '2': {"name": "🌍 Earth Shaker", "cost": 40, "dmg": (110, 160), "type": "damage",
                  "desc": "Mandeok strikes the ground, creating destabilizing shockwaves."},
            '3': {"name": "🗿 Titan Strike", "cost": 50, "dmg": (130, 190), "type": "damage",
                  "desc": "The full power of the Titan. Everything in one devastating blow."}
        }


class Xiaolung(Character):
    def __init__(self):
        super().__init__("Xiaolung", "Muay Thai Genius", 440, 280, [Realm.SPEED, Realm.STRENGTH])
        self.canon_episode = 400
        self.paths_available = [Path.XIAOLUNG_MUAY_THAI]
        self.abilities = {
            '1': {"name": "🇹🇭 Muay Thai: Elbow", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "The sharpest weapon in Muay Thai. Elbow strikes that cut like blades."},
            '2': {"name": "🇹🇭 Muay Thai: Knee", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Devastating knee strikes in the clinch."},
            '3': {"name": "🇹🇭 Thai Clinch", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "Controlling opponents while delivering brutal knees."},
            '4': {"name": "🇹🇭 Muay Thai Mastery", "cost": 50, "dmg": (130, 180), "type": "damage",
                  "desc": "Complete Muay Thai arsenal. Elbows, knees, and kicks in a devastating flurry."}
        }


class Ryuhei(Character):
    def __init__(self):
        super().__init__("Ryuhei", "Yakuza Executive", 430, 270, [Realm.TECHNIQUE])
        self.canon_episode = 400
        self.paths_available = [Path.RYUHEI_YAKUZA]
        self.abilities = {
            '1': {"name": "⚔️ Yakuza Strike", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Dirty effective street fighting. No rules, only victory."},
            '2': {"name": "🏴 Gang Style", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "Organized crime fighting style. Group tactics even when alone."},
            '3': {"name": "⚫ Yamazaki Blood", "cost": 40, "dmg": (120, 170), "type": "damage",
                  "desc": "The dark heritage of the Yamazaki clan flows in his veins."}
        }


class SamuelSeo(Character):
    def __init__(self):
        super().__init__("Samuel Seo", "The Betrayer", 460, 290, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 300
        self.paths_available = [Path.SAMUEL_AMBITION]
        self.abilities = {
            '1': {"name": "👑 King's Ambition", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "Burning desire to be king fuels every strike."},
            '2': {"name": "💢 Betrayal", "cost": 25, "dmg": (80, 120), "type": "damage",
                  "desc": "A cheap shot born from betrayal. Strikes unexpectedly."},
            '3': {"name": "⚡ Workers Executive", "cost": 40, "dmg": (120, 170), "type": "damage",
                  "desc": "Power of a Workers executive. Position gives strength and confidence."},
            '4': {"name": "👑 Path to Kingship", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "All ambition poured into one devastating strike."}
        }


class SinuHan(Character):
    def __init__(self):
        super().__init__("Sinu Han", "The Ghost", 420, 280, [Realm.SPEED, Realm.TECHNIQUE])
        self.canon_episode = 300
        self.paths_available = [Path.SINU_INVISIBLE]
        self.abilities = {
            '1': {"name": "🌀 Invisible Punch", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "desc": "A punch that can't be seen. Sinu's speed makes strikes appear from nowhere."},
            '2': {"name": "🌀 Invisible Kick", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "desc": "Invisible kick combining speed and technique."},
            '3': {"name": "🌀 Ghost Fist", "cost": 45, "dmg": (120, 170), "type": "damage",
                  "desc": "The ultimate invisible attack. Strikes from all angles simultaneously."}
        }


class LoganLee(Character):
    def __init__(self):
        super().__init__("Logan Lee", "The Bully", 350, 220, [])
        self.canon_episode = 1
        # FIX #8: Logan has no infinity technique. Path still exists for flavor.
        self.paths_available = [Path.LOGAN_BULLY]
        self.abilities = {
            '1': {"name": "👊 Bully Punch", "cost": 20, "dmg": (50, 80), "type": "damage",
                  "desc": "A bully's punch — meant to intimidate more than injure."},
            '2': {"name": "😤 Intimidation", "cost": 15, "dmg": (0, 0), "type": "utility",
                  "desc": "Logan uses his size and reputation. 40% stun chance."},
            '3': {"name": "💢 Cheap Shot", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Logan's specialty. A dirty strike when opponents aren't looking."}
        }


# ===== CHEONLIANG =====

class VinJin(Character):
    def __init__(self):
        super().__init__("Vin Jin", "Ssireum Genius", 440, 270, [Realm.STRENGTH])
        self.canon_episode = 500
        self.paths_available = [Path.VIN_JIN_SSIREUM]
        self.abilities = {
            '1': {"name": "🇰🇷 Ssireum: Throw", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Traditional Korean wrestling throw. Leverage and technique combined."},
            '2': {"name": "🇰🇷 Ssireum: Grapple", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Powerful grappling control."},
            '3': {"name": "🥋 Judo: Ippon", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "Perfect Judo throw incorporating other grappling arts."},
            '4': {"name": "🥋 Kudo: Dirty Boxing", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "Dirty boxing in the clinch. Brutal efficiency."},
            '5': {"name": "🕶️ Sunglasses Off", "cost": 50, "dmg": (140, 190), "type": "damage",
                  "desc": "Vin Jin removes his sunglasses. His true power emerges."}
        }


class HanJaeha(Character):
    def __init__(self):
        super().__init__("Han Jaeha", "Cheonliang Wrestler", 380, 240, [])  # FIX #22
        self.canon_episode = 500
        self.paths_available = [Path.HAN_JAEHA]
        self.abilities = {
            '1': {"name": "🤼 Traditional Throw", "cost": 20, "dmg": (60, 90), "type": "damage",
                  "desc": "Classic ssireum throw honoring Korean wrestling traditions."},
            '2': {"name": "🤼 Grapple Lock", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "Controlling grapple locking opponents down."},
            '3': {"name": "🤼 Cheonliang Pride", "cost": 35, "dmg": (100, 140), "type": "damage",
                  "desc": "Pride of Cheonliang. Fighting for hometown with everything."}
        }


class BaekSeong(Character):
    def __init__(self):
        super().__init__("Baek Seong", "Taekkyon Dancer", 370, 250, [])  # FIX #22
        self.canon_episode = 500
        self.paths_available = [Path.BAEK_SEONG_TAEKKYON]
        self.abilities = {
            '1': {"name": "🦢 Flowing Step", "cost": 20, "dmg": (50, 80), "type": "damage",
                  "desc": "Graceful Taekkyon footwork. Flows like water from unexpected angles."},
            '2': {"name": "🦢 Taekkyon Kick", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "Traditional Taekkyon kick. Fluid, deceptive, surprisingly powerful."},
            '3': {"name": "🦢 Dance of Blades", "cost": 40, "dmg": (110, 150), "type": "damage",
                  "desc": "Taekkyon's ultimate form. Dances through opponents, each step a strike."}
        }


# ===== YAMAZAKI =====

class ShingenYamazaki(Character):
    def __init__(self):
        super().__init__("Shingen Yamazaki", "Yamazaki Head", 650, 380,
                         [Realm.STRENGTH, Realm.TENACITY])  # CANON: not shown using Korean Gyeongji realm system
        self.canon_episode = 0
        self.paths_available = [Path.SHINGEN_YAMAZAKI]
        self.abilities = {
            '1': {"name": "🏯 Yamazaki Style", "cost": 40, "dmg": (130, 180), "type": "damage",
                  "desc": "Fundamental Yamazaki clan techniques. Shingen shows why his family is feared."},
            '2': {"name": "🏯 Syndicate's Wrath", "cost": 55, "dmg": (170, 220), "type": "damage",
                  "desc": "Collective fury of the Yamazaki Syndicate. Generations of darkness."},
            '3': {"name": "🏯 Black Bone", "cost": 70, "dmg": (210, 270), "type": "damage",
                  "desc": "The legendary technique of the Yamazaki head."},
            '4': {"name": "🏯 Inherited Darkness", "cost": 85, "dmg": (250, 320), "type": "damage",
                  "desc": "The ultimate Yamazaki technique. Full bloodline power unleashed."}
        }


class ParkFather(Character):
    def __init__(self):
        super().__init__("Park Jonggun's Father", "⚠️ Fan Creation — Unconfirmed in Manhwa", 550, 340,
                         [Realm.STRENGTH, Realm.TECHNIQUE])
        self.canon_episode = 0
        self.paths_available = [Path.PARK_FATHER]
        self.abilities = {
            '1': {"name": "❓ Unknown Technique", "cost": 35, "dmg": (110, 160), "type": "damage",
                  "desc": "A mysterious technique lost to time. Source of Gun's power."},
            '2': {"name": "❓ Bloodline Secret", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "The secret of the Park bloodline. Passed father to son."},
            '3': {"name": "❓ Father's Shadow", "cost": 65, "dmg": (190, 250), "type": "damage",
                  "desc": "The shadow of the father looms large. Gun would later inherit this."}
        }


# ===== LAW ENFORCEMENT =====

class KimMinjae(Character):
    def __init__(self):
        super().__init__("Kim Minjae", "Police Officer", 380, 240, [Realm.TECHNIQUE])
        self.canon_episode = 200
        self.paths_available = [Path.KIM_MINJAE_JUDO]
        self.abilities = {
            '1': {"name": "🥋 Judo Throw", "cost": 20, "dmg": (50, 80), "type": "damage",
                  "desc": "A clean Judo throw. Uses opponent's momentum against them."},
            '2': {"name": "🥋 Ippon Seoi Nage", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "desc": "One-arm shoulder throw. Classic Judo with police precision."},
            '3': {"name": "🥋 Police Training", "cost": 35, "dmg": (90, 130), "type": "damage",
                  "desc": "Years of police training. Law and order brought to the streets."}
        }


class DetectiveKang(Character):
    def __init__(self):
        super().__init__("Detective Kang", "Veteran Detective", 390, 250, [Realm.SPEED])
        self.canon_episode = 200
        self.paths_available = [Path.DETECTIVE_KANG_BOXING]
        self.abilities = {
            '1': {"name": "🥊 Detective's Jab", "cost": 20, "dmg": (50, 80), "type": "damage",
                  "desc": "Quick jab honed through years of street work."},
            '2': {"name": "🥊 Veteran Cross", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "desc": "Powerful cross backed by decades of experience."},
            '3': {"name": "🥊 Experience Counts", "cost": 35, "dmg": (100, 140), "type": "damage",
                  "desc": "Years on the force. Every strike guided by veteran instinct."}
        }


# ============================================================================
# ENEMY CREATION FUNCTIONS
# ============================================================================

def create_enemy_frame_soldier():
    abilities = {'1': {"name": "Fist Strike", "dmg": (25, 40), "cost": 15,
                       "desc": "A basic punch from a Frame soldier."}}
    e = Enemy("Frame Soldier", "Elite Grunt", 150, 100, abilities, 100, "Frame")
    e.ai_pattern = ['1']
    return e


def create_enemy_jhigh_bully():
    abilities = {'1': {"name": "School Punch", "dmg": (20, 35), "cost": 10,
                       "desc": "A bully's punch — meant to intimidate."}}
    e = Enemy("J High Bully", "School Thug", 100, 80, abilities, 120, "J High")
    e.ai_pattern = ['1']
    return e


def create_enemy_logan_lee():
    abilities = {
        '1': {"name": "Bully Punch", "dmg": (35, 55), "cost": 20, "desc": "Heavy punch to establish dominance."},
        '2': {"name": "Intimidation", "dmg": (30, 50), "cost": 15, "desc": "Uses size to intimidate."},
        '3': {"name": "Cheap Shot", "dmg": (40, 65), "cost": 25, "desc": "Dirty strike when you least expect it."}
    }
    e = Enemy("Logan Lee", "The Bully", 300, 180, abilities, 85, "Independent")
    e.ai_pattern = ['3', '1', '2']
    return e


def create_enemy_zack_lee():
    abilities = {
        '1': {"name": "Jab", "dmg": (35, 55), "cost": 15, "desc": "Lightning jab to measure distance."},
        '2': {"name": "Cross", "dmg": (45, 70), "cost": 20, "desc": "Full body weight behind this cross."},
        '3': {"name": "Counter", "dmg": (60, 85), "cost": 30, "desc": "Perfect timing counter punch."}
    }
    e = Enemy("Zack Lee", "The Iron Boxer", 380, 280, abilities, 35, "J High")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_vasco_enemy():
    abilities = {
        '1': {"name": "Systema Strike", "dmg": (50, 70), "cost": 20, "desc": "Vital-point Systema strike."},
        '2': {"name": "Sunken Fist", "dmg": (70, 100), "cost": 30, "desc": "The fist that sank ships."},
        '3': {"name": "Run Over", "dmg": (65, 95), "cost": 25, "desc": "Charges forward like a truck."}
    }
    e = Enemy("Vasco", "The Hero", 450, 260, abilities, 30, "Burn Knuckles")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_jay_hong_enemy():
    abilities = {
        '1': {"name": "Systema", "dmg": (45, 65), "cost": 20, "desc": "Silent Systema techniques."},
        '2': {"name": "Kali", "dmg": (50, 75), "cost": 25, "desc": "Filipino Kali knife fighting."}
    }
    e = Enemy("Jay Hong", "The Silent", 380, 270, abilities, 40, "J High")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_johan_seong_enemy():
    abilities = {
        '1': {"name": "👁️ Copy: Taekwondo", "dmg": (50, 75), "cost": 20, "desc": "Perfect Taekwondo via God Eye."},
        '2': {"name": "👁️ Copy: Boxing", "dmg": (50, 75), "cost": 20, "desc": "Champion-level boxing replication."},
        '3': {"name": "👁️ Copy: Karate", "dmg": (50, 75), "cost": 20, "desc": "Traditional Karate strikes."},
        '4': {"name": "💃 Choreography: God Dog", "dmg": (85, 120), "cost": 40, "desc": "Dance combat performance."},
        '5': {"name": "👁️ God Eye", "dmg": (95, 140), "cost": 45, "desc": "The God Eye awakens — perfect counters."}
    }
    e = Enemy("Johan Seong", "The God Eye", 400, 300, abilities, 15, "God Dog")
    e.ai_pattern = ['5', '4', '3', '2', '1']
    e.blind = True
    return e


def create_enemy_eli_jang_enemy():
    abilities = {
        '1': {"name": "Animal Strike", "dmg": (50, 75), "cost": 20, "desc": "Unpredictable savage strike."},
        '2': {"name": "Talon Kick", "dmg": (60, 85), "cost": 25, "desc": "Eagle talon kick."},
        '3': {"name": "Beast Mode", "dmg": (85, 120), "cost": 45, "desc": "Pure animal instinct unleashed."}
    }
    e = Enemy("Eli Jang", "The Wild", 410, 260, abilities, 16, "Hostel")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_warren_chae_enemy():
    abilities = {
        '1': {"name": "JKD: Interception", "dmg": (60, 85), "cost": 20, "desc": "Jeet Kune Do interception."},
        '2': {"name": "Shield Strike", "dmg": (65, 90), "cost": 25, "desc": "Shield as weapon."},
        '3': {"name": "Counter", "dmg": (70, 100), "cost": 30, "desc": "Perfectly timed counter."},
        '4': {"name": "NEW CQC", "dmg": (90, 130), "cost": 70, "desc": "Complete CQC system."}
    }
    e = Enemy("Warren Chae", "Hostel Executive", 390, 260, abilities, 30, "Hostel")
    e.ai_pattern = ['4', '3', '2', '1']
    return e


def create_enemy_jake_kim_enemy():
    abilities = {
        '1': {"name": "Conviction Punch", "dmg": (60, 85), "cost": 25, "desc": "Punch backed by conviction."},
        '2': {"name": "Inherited Will", "dmg": (95, 140), "cost": 50, "desc": "Gapryong's will flows through him."},
        '3': {"name": "Gapryong's Blood", "dmg": (120, 180), "cost": 70, "desc": "Bloodline power awakened."}
    }
    e = Enemy("Jake Kim", "The Conviction", 430, 270, abilities, 12, "Big Deal")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_jerry_kwon():
    abilities = {
        '1': {"name": "Gift Punch", "dmg": (65, 95), "cost": 30, "desc": "Strength given as a gift from Jake."},
        '2': {"name": "Rhino Charge", "dmg": (70, 105), "cost": 35, "desc": "Charges like a rhino."},
        '3': {"name": "Loyalty to Jake", "dmg": (80, 115), "cost": 40, "desc": "Loyalty pushes beyond limits."}
    }
    e = Enemy("Jerry Kwon", "Big Deal Executive", 420, 250, abilities, 25, "Big Deal")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_sally():
    abilities = {
        '1': {"name": "Sally Special", "dmg": (45, 70), "cost": 20, "desc": "Unorthodox but effective style."},
        '2': {"name": "Family Support", "dmg": (40, 65), "cost": 15, "desc": "Fighting for family."}
    }
    e = Enemy("Sally", "Hostel Manager", 320, 200, abilities, 60, "Hostel")
    e.ai_pattern = ['1', '2']
    return e


def create_enemy_brad():
    abilities = {
        '1': {"name": "Brad Punch", "dmg": (50, 75), "cost": 20, "desc": "Straightforward strength."},
        '2': {"name": "Big Deal Loyalty", "dmg": (55, 80), "cost": 25, "desc": "Loyalty pushes harder."}
    }
    e = Enemy("Brad", "Big Deal Member", 350, 220, abilities, 55, "Big Deal")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_jace_park():
    abilities = {
        '1': {"name": "Strategy", "dmg": (40, 60), "cost": 15, "desc": "Strategic mind finds openings."},
        '2': {"name": "Tactical Strike", "dmg": (45, 70), "cost": 20, "desc": "Planned tactical strike."}
    }
    e = Enemy("Jace Park", "Burn Knuckles Strategist", 330, 210, abilities, 58, "Burn Knuckles")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_burn_knuckles():
    abilities = {
        '1': {"name": "Burn Knuckle Punch", "dmg": (35, 55), "cost": 15, "desc": "Fueled by burning justice."},
        '2': {"name": "Justice Strike", "dmg": (40, 60), "cost": 20, "desc": "Striking for justice."}
    }
    e = Enemy("Burn Knuckles Member", "Hero Wannabe", 280, 180, abilities, 70, "Burn Knuckles")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_god_dog_member():
    abilities = {'1': {"name": "Fist Strike", "dmg": (25, 40), "cost": 15, "desc": "Basic fist strike."}}
    e = Enemy("God Dog Member", "Crew Soldier", 140, 100, abilities, 100, "God Dog")
    e.ai_pattern = ['1']
    return e


def create_enemy_god_dog_elite():
    abilities = {
        '1': {"name": "Power Strike", "dmg": (40, 60), "cost": 20, "desc": "Powerful elite member strike."},
        '2': {"name": "Crew Combo", "dmg": (45, 65), "cost": 25, "desc": "Combination attack."}
    }
    e = Enemy("God Dog Elite", "Crew Veteran", 200, 140, abilities, 75, "God Dog")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_hostel_member():
    abilities = {
        '1': {"name": "Street Fighting", "dmg": (35, 55), "cost": 20, "desc": "Dirty street fighting."},
        '2': {"name": "Ambush", "dmg": (40, 60), "cost": 25, "desc": "Guerilla ambush tactics."}
    }
    e = Enemy("Hostel Member", "Family Crew", 170, 120, abilities, 80, "Hostel")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_big_deal_member():
    abilities = {
        '1': {"name": "Fist Strike", "dmg": (30, 50), "cost": 15, "desc": "Fighting for Big Deal family."},
        '2': {"name": "Loyalty Surge", "dmg": (35, 55), "cost": 20, "desc": "Loyalty pushes this soldier harder."}
    }
    e = Enemy("Big Deal Member", "Crew Soldier", 180, 130, abilities, 78, "Big Deal")
    e.ai_pattern = ['1', '2']
    return e


def create_enemy_workers_member():
    abilities = {'1': {"name": "Corporate Strike", "dmg": (35, 55), "cost": 20, "desc": "Well-trained Workers strike."}}
    e = Enemy("Workers Member", "Corporate Soldier", 160, 110, abilities, 90, "Workers")
    e.ai_pattern = ['1']
    return e


def create_enemy_workers_affiliate():
    abilities = {
        '1': {"name": "Affiliate Technique", "dmg": (60, 85), "cost": 25, "desc": "Unique affiliate skills."},
        '2': {"name": "Corporate Power", "dmg": (65, 95), "cost": 30, "desc": "Full Workers backing."}
    }
    e = Enemy("Workers Affiliate", "1st Affiliate", 360, 230, abilities, 42, "Workers")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_eugene():
    abilities = {
        '1': {"name": "Corporate Strategy", "dmg": (30, 50), "cost": 20, "desc": "Finds weaknesses in any plan."},
        '2': {"name": "Workers' Orders", "dmg": (35, 55), "cost": 25, "desc": "Commands respect as Workers head."}
    }
    e = Enemy("Eugene", "Workers Executive", 300, 250, abilities, 65, "Workers")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_xiaolung():
    abilities = {
        '1': {"name": "🇹🇭 Muay Thai: Elbow", "dmg": (80, 120), "cost": 30, "desc": "Elbow strikes that cut."},
        '2': {"name": "🇹🇭 Muay Thai: Knee", "dmg": (85, 125), "cost": 30, "desc": "Devastating knee strikes."},
        '3': {"name": "🇹🇭 Thai Clinch", "dmg": (75, 110), "cost": 25, "desc": "Controls while delivering knees."},
        '4': {"name": "🇹🇭 Muay Thai Mastery", "dmg": (110, 170), "cost": 50, "desc": "Complete Muay Thai arsenal."}
    }
    e = Enemy("Xiaolung", "Muay Thai Genius", 550, 300, abilities, 14, "Workers")
    e.ai_pattern = ['4', '1', '2', '3']
    return e


def create_enemy_mandeok():
    abilities = {
        '1': {"name": "💪 Power Punch", "dmg": (90, 130), "cost": 35, "desc": "Titanic strength punch."},
        '2': {"name": "🌍 Earth Shaker", "dmg": (100, 150), "cost": 40, "desc": "Ground-shaking shockwaves."},
        '3': {"name": "🗿 Titan Strike", "dmg": (120, 180), "cost": 50, "desc": "Full Titan power."}
    }
    e = Enemy("Mandeok", "The Titan", 600, 280, abilities, 13, "Workers")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_vin_jin():
    abilities = {
        '1': {"name": "🇰🇷 Ssireum: Throw", "dmg": (75, 110), "cost": 30, "desc": "Korean wrestling throw."},
        '2': {"name": "🇰🇷 Ssireum: Grapple", "dmg": (70, 105), "cost": 30, "desc": "Grappling control."},
        '3': {"name": "🥋 Judo: Ippon", "dmg": (80, 115), "cost": 35, "desc": "Perfect Judo throw."},
        '4': {"name": "🥋 Kudo: Dirty Boxing", "dmg": (85, 120), "cost": 35, "desc": "Dirty clinch boxing."},
        '5': {"name": "🕶️ Sunglasses Off", "dmg": (110, 160), "cost": 50, "desc": "True power emerges."}
    }
    e = Enemy("Vin Jin", "Ssireum Genius", 520, 280, abilities, 28, "Workers")
    e.ai_pattern = ['5', '4', '3', '2', '1']
    return e


def create_enemy_ryuhei():
    abilities = {
        '1': {"name": "⚔️ Yakuza Strike", "dmg": (80, 115), "cost": 30, "desc": "Dirty effective yakuza style."},
        '2': {"name": "🏴 Gang Style", "dmg": (85, 120), "cost": 35, "desc": "Organized crime tactics."},
        '3': {"name": "⚫ Yamazaki Blood", "dmg": (100, 150), "cost": 45, "desc": "Dark Yamazaki heritage."}
    }
    e = Enemy("Ryuhei", "Yakuza Executive", 540, 290, abilities, 24, "Workers")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_samuel_seo():
    abilities = {
        '1': {"name": "👑 King's Ambition", "dmg": (85, 125), "cost": 35, "desc": "Burning ambition to be king."},
        '2': {"name": "💢 Betrayal", "dmg": (80, 120), "cost": 30, "desc": "Cheap shot from betrayal."},
        '3': {"name": "⚡ Workers Executive", "dmg": (95, 140), "cost": 40, "desc": "Executive-level power."},
        '4': {"name": "👑 Path to Kingship", "dmg": (110, 170), "cost": 50, "desc": "All ambition in one strike."}
    }
    e = Enemy("Samuel Seo", "The Betrayer", 560, 300, abilities, 18, "Workers")
    e.ai_pattern = ['4', '3', '1', '2']
    return e


def create_enemy_taesoo_ma():
    abilities = {
        '1': {"name": "🔴 Right Hand", "dmg": (110, 170), "cost": 45, "desc": "Legendary right fist. Pure power."},
        '2': {"name": "🔴 Ansan King", "dmg": (120, 180), "cost": 50, "desc": "King's ultimate strike."}
    }
    e = Enemy("Taesoo Ma", "King of Ansan", 580, 300, abilities, 8, "1st Gen")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_gongseob_ji():
    abilities = {
        '1': {"name": "🩷 Speed Technique", "dmg": (95, 140), "cost": 40, "desc": "Blazing fast strikes."},
        '2': {"name": "🩷 Vice King", "dmg": (100, 150), "cost": 45, "desc": "Pride of the Vice King."}
    }
    e = Enemy("Gongseob Ji", "Vice King", 500, 280, abilities, 11, "1st Gen")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_jichang_kwak():
    abilities = {
        '1': {"name": "🩷 Hand Blade", "dmg": (100, 155), "cost": 40, "desc": "Hand becomes a blade."},
        '2': {"name": "👑 Seoul King", "dmg": (110, 170), "cost": 50, "desc": "Pride of Seoul's king."}
    }
    e = Enemy("Jichang Kwak", "King of Seoul", 550, 300, abilities, 7, "1st Gen")
    e.ai_pattern = ['2', '1']
    return e


def create_enemy_gun_park_enemy():
    abilities = {
        '1': {"name": "Taekwondo", "dmg": (65, 90), "cost": 25, "desc": "Spinning kicks with perfect form."},
        '2': {"name": "Kyokushin", "dmg": (70, 100), "cost": 30, "desc": "Power from hip rotation."},
        '3': {"name": "Black Bone", "dmg": (130, 200), "cost": 70, "desc": "The legendary Yamazaki technique."}
    }
    e = Enemy("Gun Park", "Legend of Gen 1", 500, 320, abilities, 5, "Independent")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_goo_kim_enemy():
    abilities = {
        '1': {"name": "Makeshift Sword", "dmg": (45, 70), "cost": 20, "desc": "Anything becomes a sword."},
        '2': {"name": "Full Moon", "dmg": (100, 145), "cost": 45, "desc": "Complete circular slash."},
        '3': {"name": "Fifth Sword", "dmg": (170, 250), "cost": 90, "desc": "A technique that shouldn't exist."}
    }
    e = Enemy("Goo Kim", "The Moonlight Sword", 480, 300, abilities, 5, "Independent")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_kim_jungu_enemy():
    abilities = {
        '1': {"name": "Improvised Weapon", "dmg": (70, 100), "cost": 30, "desc": "Deadly creativity."},
        '2': {"name": "Hwarang Sword", "dmg": (140, 210), "cost": 60, "desc": "Ancient Hwarang technique."},
        '3': {"name": "Blade Dance", "dmg": (160, 240), "cost": 70, "desc": "Ultimate blade dance."}
    }
    e = Enemy("Kim Jun-gu", "The Hwarang Sword", 520, 290, abilities, 4, "Independent")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_manager_kim_enemy():
    abilities = {
        '1': {"name": "CQC Strike", "dmg": (65, 90), "cost": 25, "desc": "Precise CQC vital-point strike."},
        '2': {"name": "Silver Yarn", "dmg": (100, 140), "cost": 20, "type": "utility",
              "desc": "Silver yarn binds and cuts."},
        '3': {"name": "66 CODE", "dmg": (130, 190), "cost": 70, "desc": "The legendary Code 66."}
    }
    e = Enemy("Manager Kim", "The Senior Manager", 480, 300, abilities, 5, "Workers / Cheonliang")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_jinrang_enemy():
    abilities = {
        '1': {"name": "Jinrang's Conviction", "dmg": (130, 190), "cost": 50,
              "desc": "Gapryong's disciple's conviction."},
        '2': {"name": "Busan King", "dmg": (140, 210), "cost": 55, "desc": "Authority of Busan's king."},
        '3': {"name": "True Conviction", "dmg": (170, 250), "cost": 70,
              "desc": "Ultimate faith in Gapryong's teachings."}
    }
    e = Enemy("Jinrang", "King of Busan", 750, 380, abilities, 2, "Busan")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_jaegyeon_na_enemy():
    abilities = {
        '1': {"name": "Incheon Speed", "dmg": (100, 150), "cost": 40, "desc": "Speed that can't be tracked."},
        '2': {"name": "Betrayal", "dmg": (95, 145), "cost": 35, "desc": "True nature revealed in a strike."},
        '3': {"name": "Faster Than Light", "dmg": (150, 230), "cost": 60, "desc": "Absolute speed limit reached."}
    }
    e = Enemy("Jaegyeon Na", "King of Incheon", 620, 350, abilities, 6, "Busan / 1st Gen")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_charles_choi():
    abilities = {
        '1': {"name": "🎭 Puppet Master", "dmg": (90, 140), "cost": 35, "desc": "Manipulates the battlefield."},
        '2': {"name": "🏛️ Chairman's Authority", "dmg": (110, 170), "cost": 45, "desc": "HNH Group chairman's power."},
        '3': {"name": "👤 HNH Group", "dmg": (100, 160), "cost": 40, "desc": "Organization backing every move."},
        '4': {"name": "🎭 Truth of Two Bodies", "dmg": (130, 200), "cost": 60, "desc": "The ultimate secret revealed."}
    }
    e = Enemy("Charles Choi", "The Puppet Master", 650, 350, abilities, 3, "HNH Chairman")
    e.ai_pattern = ['4', '3', '2', '1']
    return e


def create_enemy_tom_lee():
    abilities = {
        '1': {"name": "🐅 Wild Strike", "dmg": (100, 150), "cost": 35, "desc": "Primal untamed animal strike."},
        '2': {"name": "🐅 Tom Lee Special", "dmg": (120, 180), "cost": 45, "desc": "Biting, clawing, striking."},
        '3': {"name": "🐅 Gen 0 Power", "dmg": (140, 210), "cost": 55, "desc": "Power from the legendary era."}
    }
    e = Enemy("Tom Lee", "The Wild", 650, 350, abilities, 5, "Gen 0")
    e.ai_pattern = ['3', '2', '1']
    return e


def create_enemy_gapryong_kim():
    abilities = {
        '1': {"name": "👑 Conviction of the Strongest", "dmg": (120, 180), "cost": 45,
              "desc": "The conviction that made him strongest."},
        '2': {"name": "👑 Gapryong's Fist", "dmg": (150, 220), "cost": 55,
              "desc": "The fist that defeated the Yamazaki Syndicate."},
        '3': {"name": "👑 Will to Protect", "dmg": (130, 200), "cost": 50,
              "desc": "Born from protecting his crew."},
        '4': {"name": "👑 Legend's Legacy", "dmg": (180, 280), "cost": 70, "desc": "The accumulated power of a legend."}
    }
    e = Enemy("Gapryong Kim", "The Strongest", 800, 400, abilities, 0, "Gen 0 Legend")
    e.ai_pattern = ['4', '2', '3', '1']
    return e


def create_enemy_cheon_shinmyeong():
    abilities = {
        '1': {"name": "🔮 Dark Exorcism", "dmg": (90, 140), "cost": 35, "desc": "Shamanistic power techniques."},
        '2': {"name": "🔮 Cheonliang Rule", "dmg": (100, 150), "cost": 40, "desc": "Shaman authority manifested."},
        '3': {"name": "🔮 Puppeteer", "dmg": (80, 120), "cost": 30, "desc": "Controlling others like puppets."}
    }
    e = Enemy("Cheon Shin-myeong", "The Shaman", 480, 320, abilities, 0, "Cheonliang")
    e.ai_pattern = ['3', '2', '1']
    return e


# FIX #18: Seongji Yuk enemy — boss of Cheonliang fighting force
def create_enemy_seongji_yuk():
    abilities = {
        '1': {"name": "🇰🇷 Ssireum: Throw",   "dmg": (80, 120), "cost": 30, "desc": "Korean wrestling throw."},
        '2': {"name": "🥋 Judo: Ippon",        "dmg": (85, 130), "cost": 35, "desc": "Perfect Judo throw."},
        '3': {"name": "🥋 Kudo: Dirty Boxing", "dmg": (90, 135), "cost": 35, "desc": "Brutal clinch boxing."},
        '4': {"name": "🦍 Monster Mode",       "dmg": (130, 190), "cost": 55, "desc": "Monstrous power unleashed."},
    }
    e = Enemy("Seongji Yuk", "The Monster of Cheonliang", 600, 300, abilities, 9, "Cheonliang")
    e.ai_pattern = ['4', '3', '2', '1']
    return e


# FIX #19: Sinu Han enemy — Workers ghost fighter
def create_enemy_sinu_han():
    abilities = {
        '1': {"name": "🌀 Invisible Punch", "dmg": (85, 125), "cost": 30, "desc": "Invisible punch from nowhere."},
        '2': {"name": "🌀 Invisible Kick",  "dmg": (85, 125), "cost": 30, "desc": "Invisible kick, speed beyond tracking."},
        '3': {"name": "🌀 Ghost Fist",      "dmg": (120, 175), "cost": 50, "desc": "Ultimate invisible attack from all angles."},
    }
    e = Enemy("Sinu Han", "The Ghost", 500, 280, abilities, 20, "Workers")
    e.ai_pattern = ['3', '1', '2']
    return e

class LookismGame:
    def __init__(self, load_saved=True):
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

        self.gapryong = GapryongKim()
        self.tom_lee = TomLee()
        self.charles_choi = CharlesChoi()
        self.jinyoung = JinyoungPark()
        self.baekho = Baekho()

        self.james_lee = JamesLee()
        self.gitae = GitaeKim()
        self.jichang = JichangKwak()
        self.taesoo = TaesooMa()
        self.gongseob = GongseobJi()
        self.seokdu = SeokduWang()
        self.jaegyeon = JaegyeonNa()
        self.seongji = SeongjiYuk()
        self.jinrang = Jinrang()

        self.mandeok = Mandeok()
        self.xiaolung = Xiaolung()
        self.ryuhei = Ryuhei()
        self.samuel = SamuelSeo()
        self.sinu = SinuHan()
        self.logan = LoganLee()

        self.vin_jin = VinJin()
        self.han_jaeha = HanJaeha()
        self.baek_seong = BaekSeong()

        self.shingen = ShingenYamazaki()
        self.park_father = ParkFather()

        self.kim_minjae = KimMinjae()
        self.detective_kang = DetectiveKang()

        self.all_characters = self._compile_all_characters()

        self.unlocked_characters = {
            "Gapryong Kim": False, "Tom Lee": False, "Charles Choi": False,
            "Jinyoung Park": False, "Baekho": False, "James Lee": False,
            "Gitae Kim": False, "Shingen Yamazaki": False,
            "Park Jonggun's Father": False, "Jinrang": False, "Jaegyeon Na": False
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
        self.story_progress = {
            "arc1_complete": False, "arc2_complete": False, "arc3_complete": False,
            "arc4_complete": False, "arc5_complete": False, "arc6_complete": False,
            "arc7_complete": False, "arc8_complete": False, "gen0_complete": False,
            "boss_rush_complete": False, "jinrang_defeated": False,
            "jaegyeon_defeated": False, "charles_choi_defeated": False,
            "tom_lee_defeated": False, "gapryong_defeated": False
        }

        self.party = []
        self.enemies = []
        self.turn_count = 0
        self.victories = 0
        self.total_kills = 0
        self.wave = 0
        self.current_arc = "J High"
        self.path_changes_available = 3
        self._battle_log = []

        if load_saved:
            loaded = self.load_game()
            if loaded:
                print("✅ Game loaded successfully!")
            else:
                print("🆕 Starting new game...")

    def _compile_all_characters(self):
        return [
            self.gapryong, self.tom_lee, self.charles_choi, self.jinyoung, self.baekho,
            self.james_lee, self.gitae, self.jichang, self.taesoo, self.gongseob,
            self.seokdu, self.jaegyeon, self.seongji, self.jinrang,
            self.mandeok, self.manager_kim, self.xiaolung, self.ryuhei,
            self.samuel, self.sinu, self.logan,
            self.vin_jin, self.han_jaeha, self.baek_seong,
            self.shingen, self.park_father,
            self.kim_minjae, self.detective_kang,
            self.daniel, self.zack, self.johan, self.vasco, self.jay,
            self.eli, self.warren, self.jake, self.gun, self.goo,
            self.joongoo
        ]

    def add_log(self, message):
        print(f"[T{self.turn_count}] ", end='')
        slow_print(message, 0.02)
        time.sleep(0.2)

    # -------------------------------------------------------------------------
    # FIX #6: choose_character_path uses while loop instead of recursion
    # -------------------------------------------------------------------------
    def choose_character_path(self, character):
        while True:
            if character.path:
                print(f"\n{character.name} currently walks: {character.path.value}")
                print(f"Path Level: {character.path_level} | EXP: {character.path_exp}/100")
                print("\n  1. Keep current path")
                print("  2. Change path (resets level/EXP)")
                print("  3. Reset path completely")
                print("  b. Back")
                choice = input("> ").strip().lower()
                if choice == '1' or choice == 'b':
                    return True
                elif choice == '2':
                    confirm = input(f"Reset {character.name}'s path? Level and EXP lost. (y/n): ").lower()
                    if confirm == 'y':
                        # FIX BUG-11: Clear path so loop falls to selection screen
                        character.path = None
                        character.infinity_technique = None
                        character.path_level = 1
                        character.path_exp = 0
                        print("🔄 Path reset. Choose a new one.")
                    # loop continues — now character.path is None, falls to selection
                elif choice == '3':
                    confirm = input(f"Clear {character.name}'s path? (y/n): ").lower()
                    if confirm == 'y':
                        character.path = None
                        character.infinity_technique = None
                        character.path_level = 1
                        character.path_exp = 0
                        print(f"🔄 {character.name}'s path cleared!")
                        return True
                else:
                    print("❌ Invalid choice.")
                continue

            # No path — show selection
            print(f"\n{'=' * 90}")
            slow_print(f"✦✦✦ CHOOSE PATH FOR {character.name.upper()} ✦✦✦", 0.03)
            print("=" * 90)
            for i, path in enumerate(character.paths_available):
                print(f"\n  {i + 1}. {path.value}")
                if path in INFINITY_TECHNIQUES:
                    tech = INFINITY_TECHNIQUES[path]
                    print(f"     ➤ Infinity: {tech['name']}")
                    print(f"     ➤ {tech['desc'][:100]}...")
                time.sleep(0.1)
            print("\n  b. Back")

            choice = input("> ").strip().lower()
            if choice == 'b':
                return False
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(character.paths_available):
                    result = character.choose_path(character.paths_available[idx])
                    slow_print(result, 0.03)
                    time.sleep(1)
                    return True
                else:
                    print("❌ Invalid number.")
            except ValueError:
                print("❌ Enter a number.")

    # -------------------------------------------------------------------------
    # FIX #2: enemy_turn uses ENEMY's own multiplier, not the target's
    # FIX #4: God Eye timer decremented properly
    # -------------------------------------------------------------------------
    def enemy_turn(self, enemy):
        if not enemy.is_alive():
            return
        if not any(c.is_alive() for c in self.party):
            return

        if enemy.stunned:
            self.add_log(f"⚡ {enemy.name} is stunned!")
            enemy.stunned = False
            time.sleep(0.5)
            return
        if enemy.bound:
            self.add_log(f"⚪ {enemy.name} is bound!")
            enemy.bound = False
            time.sleep(0.5)
            return

        enemy.energy = min(enemy.max_energy, enemy.energy + 10)

        chosen_abil = None
        for pattern_key in enemy.ai_pattern:
            if pattern_key in enemy.abilities:
                abil = enemy.abilities[pattern_key]
                if enemy.energy >= abil.get("cost", 20):
                    chosen_abil = (pattern_key, abil)
                    break

        if chosen_abil is None:
            first_key = list(enemy.abilities.keys())[0]
            abil = enemy.abilities[first_key]
            chosen_abil = (first_key, abil)

        key, abil = chosen_abil
        if enemy.energy < abil.get("cost", 20):
            self.add_log(f"{enemy.name} conserves energy.")
            return

        enemy.energy -= abil.get("cost", 20)
        targets = [c for c in self.party if c.is_alive()]
        if not targets:
            return

        t = random.choice(targets)
        base_dmg = random.randint(abil["dmg"][0], abil["dmg"][1])

        # FIX #2: Use ENEMY's own multiplier
        enemy_mult, _ = enemy.get_damage_multiplier()
        dmg = int(base_dmg * enemy_mult)

        # FIX BUG-08: Apply target's SPEED realm evasion
        if t.active_realm == Realm.SPEED and random.random() < 0.5:
            self.add_log(f"💨 {t.name}'s SPEED realm — attack evaded!")
            time.sleep(0.8)
            return

        # Apply target's defense
        if t.defending:
            dmg = int(dmg * 0.5)
            t.defending = False
            self.add_log(f"🛡️ {t.name} blocks!")

        t.take_damage(dmg)
        self.add_log(f"{enemy.name} uses {abil['name']} on {t.name} for {dmg} damage!")

        # FIX BUG-08: TECHNIQUE realm counter — 25% chance to counter-attack
        if t.active_realm == Realm.TECHNIQUE and t.is_alive() and random.random() < 0.25:
            counter_dmg = random.randint(30, 60)
            enemy.take_damage(counter_dmg)
            self.add_log(f"🩷 {t.name}'s TECHNIQUE realm — counter attack! {counter_dmg} damage to {enemy.name}!")

        # ── Johan Copy Mechanic ──────────────────────────────────────────────
        johan = next((c for c in self.party if c.name == "Johan Seong" and c.is_alive()), None)
        if johan and hasattr(johan, 'copy_technique'):
            copy_chance, factors = johan.calculate_copy_chance(abil['name'], t, enemy.rank)
            factors_str = " + ".join(factors) if factors else "Base"
            if copy_chance > 0.5:
                self.add_log(f"👁️ Copy chance: {int(copy_chance * 100)}% [{factors_str}]")

            if random.random() < copy_chance:
                result = johan.copy_technique(abil['name'], t)
                if result:
                    self.add_log(f"👁️✨ {result}")
                elif johan.copy_count >= johan.max_copy:
                    self.add_log(f"📦 Johan's copy limit reached ({johan.max_copy}/10)!")
            else:
                # Still track observation even on failed copy
                jv = johan.technique_view_count
                jv[abil['name']] = jv.get(abil['name'], 0) + 1
        # ── End Johan Copy ───────────────────────────────────────────────────

        time.sleep(0.8)

    # -------------------------------------------------------------------------
    # FIX #7: cleanup() only applies player-specific effects to party members,
    #          not to enemies (enemies don't use realms/UI/etc.)
    # FIX #4: God Eye timer decremented here
    # -------------------------------------------------------------------------
    def cleanup(self):
        all_combatants = self.party + self.enemies

        # Defending flag reset for ALL
        for c in all_combatants:
            c.defending = False

        # Player-specific effects
        for c in self.party:
            # Realm timer
            if c.realm_timer > 0:
                c.realm_timer -= 1
                if c.realm_timer <= 0:
                    c.active_realm = Realm.NONE
                    c.realm_effect = None
                    self.add_log(f"{c.name}'s realm fades.")

            # UI timer
            if c.ui_mode:
                c.ui_timer -= 1
                if c.ui_timer <= 0:
                    c.ui_mode = False
                    self.add_log(f"{c.name}'s Ultra Instinct fades.")

            # Beast mode timer
            if c.beast_mode:
                c.beast_timer -= 1
                if c.beast_timer <= 0:
                    c.beast_mode = False
                    self.add_log(f"{c.name}'s Beast Mode fades.")

            # FIX #4: God Eye timer (proper turn countdown)
            if hasattr(c, 'god_eye_active') and c.god_eye_active:
                c.god_eye_timer -= 1
                if c.god_eye_timer <= 0:
                    c.god_eye_active = False
                    c.god_eye_timer = 0
                    self.add_log(f"{c.name}'s God Eye fades.")
                else:
                    self.add_log(f"👁️ God Eye: {c.god_eye_timer} turns remaining.")

            # Tenacity regen
            if c.apply_realm_regen():
                self.add_log(f"🟢 {c.name} regenerates 15 HP (Tenacity).")

            # Tick down timed buffs (BUG-04/05/06 fix)
            expired = []
            for buff in c.temp_buffs:
                buff['turns'] -= 1
                if buff['turns'] <= 0:
                    expired.append(buff)
                    self.add_log(f"⏱️ {c.name}'s {buff['name']} buff expired.")
            for buff in expired:
                c.temp_buffs.remove(buff)

            # Status recovery
            if c.stunned and random.random() < 0.3:
                c.stunned = False
                self.add_log(f"⚡ {c.name} recovers from stun!")
            if c.bound and random.random() < 0.3:
                c.bound = False
                self.add_log(f"⚪ {c.name} breaks free!")

        # Enemy status recovery only
        for e in self.enemies:
            if e.stunned and random.random() < 0.3:
                e.stunned = False
            if e.bound and random.random() < 0.3:
                e.bound = False

        time.sleep(0.2)

    # -------------------------------------------------------------------------
    # FIX #6: use_ability uses while loop instead of recursion
    # -------------------------------------------------------------------------
    def use_ability(self, character):
        while True:
            if hasattr(character, 'exhausted') and character.exhausted:
                self.add_log(f"{character.name} is exhausted and cannot act!")
                character.exhausted = False
                character.energy = min(character.max_energy, character.energy + 15)
                time.sleep(ACTION_DELAY)
                return True

            print(f"\n{'=' * 90}")
            slow_print(f"✦✦✦ {character.name} [{character.title}] ✦✦✦", 0.03)
            print("=" * 90)
            print(f"❤️ HP: {character.hp}/{character.max_hp}  ⚡ Energy: {character.energy}/{character.max_energy}")
            if character.path:
                print(f"🛤️ PATH: {character.path.value[:50]} (Lv.{character.path_level})")
            print("-" * 90)

            available = {k: v for k, v in character.abilities.items()
                         if character.energy >= v["cost"] and v.get("type") != "passive"}

            passive_ab = {k: v for k, v in character.abilities.items()
                          if v.get("type") == "passive"}

            damage_ab = {k: v for k, v in available.items() if v.get("type") == "damage"}
            buff_ab = {k: v for k, v in available.items() if v.get("type") in ["buff", "ui"]}
            util_ab = {k: v for k, v in available.items() if v.get("type") == "utility"}

            sort_key = lambda x: int(x) if x.isdigit() else x

            if damage_ab:
                print("  💢 DAMAGE:")
                for k in sorted(damage_ab, key=sort_key):
                    v = damage_ab[k]
                    print(f"    {k}. {v['name']:38} | {v['cost']}E | {v['dmg'][0]}-{v['dmg'][1]} DMG")
            if buff_ab:
                print("\n  💪 BUFFS:")
                for k in sorted(buff_ab, key=sort_key):
                    v = buff_ab[k]
                    print(f"    {k}. {v['name']:38} | {v['cost']}E | BUFF")
            if util_ab:
                print("\n  🛡️ UTILITY:")
                for k in sorted(util_ab, key=sort_key):
                    v = util_ab[k]
                    print(f"    {k}. {v['name']:38} | {v['cost']}E | UTILITY")

            if passive_ab:
                print("\n  ⚡ PASSIVES (always active):")
                for k in sorted(passive_ab, key=sort_key):
                    v = passive_ab[k]
                    print(f"    • {v['name']:38} | {v['desc'][:60]}")

            it = character.infinity_technique
            if it and character.energy >= it['cost']:
                print(f"\n  ✨ INFINITY (99): {it['name']} | {it['cost']}E | {it['dmg'][0]}-{it['dmg'][1]} DMG")

            if character.name == "Johan Seong":
                print(f"\n  📊 VIEW COPY STATS (98)")

            print("\n  0. 📖 Describe Ability  |  00. 🔮 Realm  |  000. 🛤️ Path  |  0000. ⏭️ Skip (+15E)  |  00000. ↩️ Back")
            print("-" * 90)

            choice = input("> ").strip()
            print()

            if choice == '00000':
                return False
            if choice == '0000':
                self.add_log(f"{character.name} skips turn. +15 Energy")
                character.energy = min(character.max_energy, character.energy + 15)
                return True
            if choice == '000':
                self.choose_character_path(character)
                self.save_game()
                continue
            if choice == '00':
                if character.realms:
                    print("\n🔮 AVAILABLE REALMS:")
                    for i, realm in enumerate(character.realms):
                        print(f"  {i + 1}. {realm.value}")
                    print("  b. Back")
                    rc = input("> ").strip()
                    if rc.lower() == 'b':
                        continue
                    if rc.isdigit():
                        idx = int(rc) - 1
                        if 0 <= idx < len(character.realms):
                            # FIX BUG-02: Realm activation costs the turn
                            self.add_log(character.activate_realm(character.realms[idx]))
                            return True
                    print("❌ Invalid realm choice.")
                else:
                    print(f"{character.name} cannot activate any realms.")
                continue
            if choice == '98' and character.name == "Johan Seong":
                character.get_copy_stats()
                input("\nPress Enter to continue...")
                continue
            if choice == '0':
                print("\n📖 SELECT ABILITY NUMBER TO DESCRIBE:")
                for k in sorted(available, key=sort_key):
                    print(f"  {k}. {available[k]['name']}")
                dc = input("> ").strip()
                if dc in available:
                    self._display_ability_desc(available[dc])
                continue
            if choice == '99' and it and character.energy >= it['cost']:
                # FIX BUG-01 & BUG-12: Select target BEFORE deducting energy
                target = self.select_target()
                if not target:
                    print("❌ No valid target.")
                    continue
                character.energy -= it['cost']
                dmg = random.randint(it['dmg'][0], it['dmg'][1])
                mult, buffs = character.get_damage_multiplier()
                dmg = int(dmg * mult)
                target.take_damage(dmg)
                print("\n" + "✨" * 45)
                slow_print(f"✨✨✨ {it['name']} ✨✨✨", 0.05)
                print("✨" * 45)
                self.add_log(f"INFINITY TECHNIQUE! {dmg} damage!")
                self.add_log(f"📖 {it['desc']}")
                return True

            if choice in available:
                ability = available[choice]
                character.energy = max(0, character.energy - ability["cost"])

                if ability.get("type") == "ui":
                    if hasattr(character, 'activate_ui'):
                        self.add_log(character.activate_ui())

                elif ability.get("type") == "buff":
                    if character.name == "Eli Jang" and "Beast Mode" in ability["name"]:
                        if hasattr(character, 'activate_beast_mode'):
                            self.add_log(character.activate_beast_mode())
                    elif character.name == "Johan Seong" and "God Eye" in ability["name"]:
                        if hasattr(character, 'activate_god_eye'):
                            self.add_log(character.activate_god_eye())
                    # FIX BUG-05: Zack Iron Fortress — set defending AND add def buff
                    elif "Iron Fortress" in ability["name"]:
                        character.defending = True
                        character.temp_buffs.append({'name': 'Iron Fortress', 'dmg_mult': 1.0, 'def_mult': 0.5, 'turns': 2})
                        self.add_log(f"🛡️ {character.name} enters Iron Fortress Stance! -50% damage for 2 turns!")
                    # FIX BUG-04: James Lee Legend's Speed — +30% damage for 3 turns
                    elif "Legend's Speed" in ability["name"]:
                        character.temp_buffs.append({'name': "Legend Speed", 'dmg_mult': 1.3, 'def_mult': 1.0, 'turns': 3})
                        self.add_log(f"⚡ {character.name} taps into legendary speed! +30% damage for 3 turns!")
                    # FIX BUG-06: Jake Conviction Mode — +50% damage for 3 turns
                    elif "Conviction Mode" in ability["name"]:
                        character.temp_buffs.append({'name': "Conviction", 'dmg_mult': 1.5, 'def_mult': 1.0, 'turns': 3})
                        self.add_log(f"⚖️ {character.name} enters Conviction Mode! +50% damage for 3 turns!")
                    else:
                        self.add_log(f"{character.name} uses {ability['name']}!")
                        self.add_log(f"📖 {ability.get('desc', '')}")

                elif ability.get("type") == "utility":
                    if "Thread Bind" in ability["name"]:
                        for e in self.enemies:
                            if e.is_alive() and random.random() < 0.6:
                                e.bound = True
                                self.add_log(f"⚪ {e.name} is bound by silver threads!")
                    elif "Defense" in ability["name"] or "Helmet" in ability["name"] or "Stance" in ability["name"]:
                        character.defending = True
                        self.add_log(f"🛡️ {character.name} takes a defensive stance!")
                    # FIX BUG-07: Logan Intimidation — apply 40% stun to enemies
                    elif "Intimidation" in ability["name"]:
                        stunned_any = False
                        for e in self.enemies:
                            if e.is_alive() and random.random() < 0.4:
                                e.stunned = True
                                self.add_log(f"😤 {e.name} is intimidated and stunned!")
                                stunned_any = True
                        if not stunned_any:
                            self.add_log(f"😤 {character.name}'s intimidation failed to stun anyone.")
                    else:
                        self.add_log(f"{character.name} uses {ability['name']}!")
                    self.add_log(f"📖 {ability.get('desc', '')}")

                elif ability.get("type") == "damage" or "dmg" in ability:
                    # FIX BUG-08: Select target first
                    target = self.select_target()
                    if target:
                        base_dmg = random.randint(ability["dmg"][0], ability["dmg"][1])
                        mult, buffs = character.get_damage_multiplier()
                        dmg = int(base_dmg * mult)
                        target.take_damage(dmg)
                        self.add_log(f"{character.name} → {ability['name']} → {target.name}: {dmg} DMG")
                        if buffs:
                            self.add_log(f"   Multipliers active: {', '.join(buffs)}")
                        self.add_log(f"📖 {ability.get('desc', '')}")

                        # FIX BUG-08: SPEED realm — 30% chance of double strike
                        if character.active_realm == Realm.SPEED and random.random() < 0.3:
                            bonus = int(dmg * 0.6)
                            target.take_damage(bonus)
                            self.add_log(f"⚡ SPEED REALM: Double strike! +{bonus} bonus damage!")

                        # FIX BUG-08: TECHNIQUE realm — 25% counter if hit (enemy version handled in enemy_turn)
                        # For player: TECHNIQUE gives +40% accuracy (already hits), but also 25% counter
                        # is applied when ENEMIES hit the player — handled in enemy_turn

                        # Exhaust Warren after Full CQC
                        if character.name == "Warren Chae" and "Full Release" in ability["name"]:
                            character.exhausted = True
                            self.add_log("⚠️ Warren is exhausted after CQC Full Release!")

                time.sleep(ACTION_DELAY)
                return True

            else:
                print("❌ Invalid choice. Try again.")
                time.sleep(0.3)
                # Loop continues

    def _display_ability_desc(self, abil):
        print("\n" + "─" * 70)
        slow_print(f"📖 {abil['name']}", 0.04)
        print("─" * 70)
        slow_print(abil.get('desc', 'No description.'), 0.02)
        print(f"\n⚡ Cost: {abil['cost']}   💢 Damage: {abil['dmg'][0]}-{abil['dmg'][1]}")
        print("─" * 70)
        input("Press Enter to continue...")

    def select_target(self, allies=False):
        if allies:
            targets = [c for c in self.party if c.is_alive()]
            label = "✦ SELECT ALLY"
        else:
            targets = [e for e in self.enemies if e.is_alive()]
            label = "☠ SELECT ENEMY"

        if not targets:
            return None

        print(f"\n{label}:")
        for i, t in enumerate(targets):
            print(f"  {i + 1}. {t.name} ({t.hp}/{t.max_hp} HP)")

        while True:
            choice = input("> ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(targets):
                    return targets[idx]
            except (ValueError, IndexError):
                pass
            print("❌ Invalid target.")

    def display_health_bars(self):
        print("\n" + "=" * 90)
        print("✦ PARTY:")
        for member in self.party:
            if member.is_alive():
                bar = "█" * int(40 * member.hp / member.max_hp) + "░" * int(40 * (1 - member.hp / member.max_hp))
                status = []
                if member.ui_mode:       status.append("👁️UI")
                if member.beast_mode:    status.append("🦁BEAST")
                if hasattr(member, 'god_eye_active') and member.god_eye_active:
                    status.append(f"👁️GOD EYE({member.god_eye_timer}T)")
                if member.active_realm != Realm.NONE:
                    status.append(f"REALM({member.realm_timer}T)")
                if member.path:
                    status.append(f"Lv{member.path_level}")
                if member.name == "Johan Seong" and hasattr(member, 'copy_count') and member.copy_count > 0:
                    status.append(f"📚{member.copy_count}")
                st = " | ".join(status)
                print(f"  {member.name:20}|{bar}| {member.hp:3}/{member.max_hp:3}HP {member.energy:3}E  {st}")

        print("☠ ENEMIES:")
        for enemy in self.enemies:
            if enemy.is_alive():
                bar = "█" * int(40 * enemy.hp / enemy.max_hp) + "░" * int(40 * (1 - enemy.hp / enemy.max_hp))
                debuffs = []
                if enemy.stunned: debuffs.append("⚡STUN")
                if enemy.bound:   debuffs.append("⚪BOUND")
                db = " ".join(debuffs)
                print(f"  {enemy.name:20}|{bar}| {enemy.hp:3}/{enemy.max_hp:3}HP [{enemy.affiliation}] Rank:{enemy.rank} {db}")
        print("=" * 90)
        time.sleep(0.3)

    def select_party(self, max_size=4):
        print(f"\n{'=' * 90}")
        slow_print("✦✦✦ SELECT YOUR PARTY ✦✦✦", 0.03)
        print("=" * 90)

        available = []
        for i, char in enumerate(self.all_characters):
            locked = self.unlocked_characters.get(char.name, True) is False
            if not locked and char.is_alive():
                copy_info = f" [📚{char.copy_count}]" if char.name == "Johan Seong" and hasattr(char, 'copy_count') and char.copy_count > 0 else ""
                path_info = f" [{char.path.name[:15]}]" if char.path else ""
                print(f"  {i + 1}. {char.name}{copy_info}{path_info} — {char.hp}/{char.max_hp}HP")
                available.append(char)
            elif locked:
                print(f"  {char.name} 🔒 {self.unlock_requirements.get(char.name, 'Locked')}")

        print("\n  a. Auto (Daniel, Vasco, Zack, Jay)  |  b. Back")

        while True:
            choice = input("> ").strip().lower()
            if choice == 'b':
                return None
            if choice == 'a':
                auto = [c for c in self.all_characters
                        if c.name in ("Daniel Park", "Vasco", "Zack Lee", "Jay Hong") and c.is_alive()]
                if len(auto) == 4:
                    return auto
                print("❌ Auto-select failed. Select manually.")
                continue

            selected = []
            print(f"Enter numbers (1-{len(available)}), blank line when done:")
            while len(selected) < max_size:
                num = input(f"Slot {len(selected) + 1}: ").strip()
                if not num:
                    break
                try:
                    idx = int(num) - 1
                    if 0 <= idx < len(available):
                        char = available[idx]
                        if char not in selected and char.is_alive():
                            selected.append(char)
                            print(f"  ✓ {char.name}")
                        else:
                            print("  ✗ Already selected or not alive.")
                    else:
                        print(f"  ✗ Must be 1-{len(available)}")
                except ValueError:
                    print("  ✗ Enter a number.")

            if selected:
                return selected
            print("No selection made. Try again.")

    def battle(self, enemies, party=None):
        self.enemies = enemies
        if party:
            self.party = party
        else:
            self.party = self.select_party()
            if not self.party:
                return False

        self.turn_count = 0

        print(f"\n{'=' * 90}")
        slow_print("⚔️⚔️⚔️ BATTLE START ⚔️⚔️⚔️", 0.04)
        print(f"✦ PARTY: {', '.join(c.name for c in self.party)}")
        print(f"☠ ENEMIES: {', '.join(e.name for e in self.enemies)}")
        print("=" * 90)
        time.sleep(BATTLE_START_DELAY)

        while True:
            self.turn_count += 1
            print(f"\n{'=' * 40} TURN {self.turn_count} {'=' * 40}")
            time.sleep(TURN_DELAY)

            for char in self.party:
                if char.is_alive():
                    char.energy = min(char.max_energy, char.energy + 15)
                    done = False
                    while not done:
                        self.display_health_bars()
                        done = self.use_ability(char)
                    if not any(e.is_alive() for e in self.enemies):
                        break

            if not any(e.is_alive() for e in self.enemies):
                break
            if not any(c.is_alive() for c in self.party):
                break

            print("\n☠ ENEMY PHASE")
            for enemy in self.enemies:
                if enemy.is_alive():
                    self.enemy_turn(enemy)
                    time.sleep(0.3)

            self.cleanup()

        self.display_health_bars()

        if any(e.is_alive() for e in self.enemies):
            print(f"\n{'=' * 90}")
            slow_print("💀💀💀 DEFEAT... 💀💀💀", 0.05)
            print("=" * 90)
            time.sleep(VICTORY_DELAY)
            return False
        else:
            print(f"\n{'=' * 90}")
            slow_print("✨✨✨ VICTORY! ✨✨✨", 0.05)
            print("=" * 90)
            self.victories += 1
            self.total_kills += sum(1 for e in self.enemies if not e.is_alive())

            for char in self.party:
                if char.is_alive() and char.path:
                    total_rank = sum(e.rank for e in self.enemies)
                    avg_rank = total_rank // max(len(self.enemies), 1)
                    # FIX BUG-10: Rank is inverted (lower = stronger), so invert for EXP
                    exp_gain = max(5, min(50, 105 - avg_rank))
                    char.path_exp += exp_gain
                    while char.path_exp >= 100:
                        char.path_level += 1
                        char.path_exp -= 100
                        self.add_log(f"✨ {char.name}'s path leveled up to {char.path_level}!")

            self.save_game()
            time.sleep(VICTORY_DELAY)
            return True

    def save_game(self):
        game_state = {
            'unlocked_characters': self.unlocked_characters,
            'story_progress': self.story_progress,
            'victories': self.victories,
            'total_kills': self.total_kills,
            'path_changes_available': self.path_changes_available,
            'current_arc': self.current_arc,
            'characters': {}
        }
        for char in self.all_characters:
            game_state['characters'][char.name] = char.to_dict()

        if SaveSystem.save_game(game_state):
            print("\n💾 Game saved!")
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
        self.path_changes_available = game_state.get('path_changes_available', 3)
        self.current_arc = game_state.get('current_arc', "J High")
        char_data = game_state.get('characters', {})
        for char in self.all_characters:
            if char.name in char_data:
                char.from_dict(char_data[char.name])
        return True

    def rest(self):
        print(f"\n{'=' * 90}")
        slow_print("🛌 RESTING & RECOVERY 🛌", 0.04)
        print("=" * 90)
        for char in self.all_characters:
            char.hp = char.max_hp
            char.energy = char.max_energy
            char.buffs = []
            char.debuffs = []
            char.defending = False
            char.active_realm = Realm.NONE
            char.realm_effect = None
            char.realm_timer = 0
            char.form = "Normal"
            char.stunned = False
            char.bound = False
            char.exhausted = False
            char.ui_mode = False
            char.ui_timer = 0
            char.beast_mode = False
            char.beast_timer = 0
            if hasattr(char, 'god_eye_active'):
                char.god_eye_active = False
                char.god_eye_timer = 0
            char.veinous_rage = False
            char.silver_yarn_active = False
            char.muscle_boost = False
            char.temp_buffs = []
            print(f"  ✦ {char.name} fully recovered!")
            time.sleep(0.05)
        self.save_game()
        time.sleep(1)

    # -------------------------------------------------------------------------
    # FIX #6: path_management_menu uses while loop
    # -------------------------------------------------------------------------
    def path_management_menu(self):
        while True:
            print(f"\n{'=' * 90}")
            slow_print("🛤️ PATH MANAGEMENT 🛤️", 0.03)
            print("=" * 90)
            for i, char in enumerate(self.all_characters):
                locked = self.unlocked_characters.get(char.name, True) is False
                if locked:
                    print(f"  {char.name} 🔒")
                    continue
                path_info = f"[{char.path.value[:25]}] Lv.{char.path_level}" if char.path else "[No Path]"
                copy_info = f" [📚{char.copy_count}]" if char.name == "Johan Seong" and hasattr(char, 'copy_count') and char.copy_count > 0 else ""
                print(f"  {i + 1}. {char.name}{copy_info} — {path_info}")

            print("\n  a. Reset ALL paths  |  s. Save  |  b. Back")
            choice = input("> ").strip().lower()

            if choice == 'b':
                return
            if choice == 's':
                self.save_game()
                continue
            if choice == 'a':
                if input("Reset ALL paths? (y/n): ").lower() == 'y':
                    for char in self.all_characters:
                        char.path = None
                        char.infinity_technique = None
                        char.path_level = 1
                        char.path_exp = 0
                        char.path_history = []
                    print("✨ All paths reset!")
                    self.save_game()
                continue

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.all_characters):
                    char = self.all_characters[idx]
                    locked = self.unlocked_characters.get(char.name, True) is False
                    if locked:
                        print(f"❌ {char.name} is locked.")
                    else:
                        self.choose_character_path(char)
                        self.save_game()
            except ValueError:
                print("❌ Invalid input.")

    def check_unlocks(self):
        new_unlocks = []
        checks = [
            ("Jinrang", "jinrang_defeated"),
            ("Jaegyeon Na", "jaegyeon_defeated"),
            ("Charles Choi", "charles_choi_defeated"),
            ("Tom Lee", "tom_lee_defeated"),
            ("Gapryong Kim", "gapryong_defeated"),
        ]
        for name, flag in checks:
            if not self.unlocked_characters.get(name, True) and self.story_progress.get(flag, False):
                self.unlocked_characters[name] = True
                new_unlocks.append(name)

        if new_unlocks:
            print("\n✨ NEW CHARACTERS UNLOCKED!")
            for n in new_unlocks:
                print(f"  ✅ {n}")
            self.save_game()
        time.sleep(1.5)

    def story_mode(self):
        print(f"\n{'=' * 90}")
        slow_print("📖 STORY MODE: THE COMPLETE LOOKISM 📖", 0.03)
        print("=" * 90)
        time.sleep(0.5)

        # FIX BUG-09: Store factory lambdas so enemies are recreated fresh each attempt
        arcs = [
            ("ARC 1: J HIGH & THE TWO BODIES", [
                ("Prologue: The Transfer Student", lambda: [create_enemy_jhigh_bully()]),
                ("Chapter 1: Logan Lee", lambda: [create_enemy_logan_lee()]),
                ("Chapter 2: Zack's Challenge", lambda: [create_enemy_zack_lee()]),
                ("Chapter 3: Vasco Appears", lambda: [create_enemy_vasco_enemy()]),
                ("Chapter 4: Jay's Protection", lambda: [create_enemy_jay_hong_enemy()])
            ]),
            ("ARC 2: GOD DOG", [
                ("Chapter 5: God Dog Soldiers", lambda: [create_enemy_god_dog_member(), create_enemy_god_dog_member()]),
                ("Chapter 6: God Dog Elite", lambda: [create_enemy_god_dog_elite(), create_enemy_god_dog_member()]),
                ("Chapter 7: Johan Seong", lambda: [create_enemy_johan_seong_enemy()])
            ]),
            ("ARC 3: HOSTEL", [
                ("Chapter 8: Hostel Family", lambda: [create_enemy_hostel_member(), create_enemy_sally()]),
                ("Chapter 9: Warren Chae", lambda: [create_enemy_warren_chae_enemy()]),
                ("Chapter 10: Eli Jang", lambda: [create_enemy_eli_jang_enemy()])
            ]),
            ("ARC 4: BIG DEAL", [
                ("Chapter 11: Big Deal Soldiers", lambda: [create_enemy_big_deal_member(), create_enemy_brad()]),
                ("Chapter 12: Jerry Kwon", lambda: [create_enemy_jerry_kwon()]),
                ("Chapter 13: Jake Kim", lambda: [create_enemy_jake_kim_enemy()])
            ]),
            ("ARC 5: WORKERS", [
                ("Chapter 14: Workers Affiliates", lambda: [create_enemy_workers_member(), create_enemy_workers_affiliate()]),
                ("Chapter 15: Xiaolung", lambda: [create_enemy_xiaolung()]),
                ("Chapter 16: Mandeok", lambda: [create_enemy_mandeok()]),
                ("Chapter 17: Samuel Seo", lambda: [create_enemy_samuel_seo()]),
                ("Chapter 18: Eugene", lambda: [create_enemy_eugene()])
            ]),
            ("ARC 6: CHEONLIANG", [
                ("Chapter 19: Sinu Han",    lambda: [create_enemy_sinu_han()]),
                ("Chapter 20: Vin Jin",     lambda: [create_enemy_vin_jin()]),
                ("Chapter 21: Ryuhei",      lambda: [create_enemy_ryuhei()]),
                ("Chapter 22: Seongji Yuk", lambda: [create_enemy_seongji_yuk()]),
                ("Chapter 23: The Shaman",  lambda: [create_enemy_cheon_shinmyeong()])
            ]),
            ("ARC 7: 1ST GENERATION", [
                ("Chapter 24: Taesoo Ma", lambda: [create_enemy_taesoo_ma()]),
                ("Chapter 25: Gongseob Ji", lambda: [create_enemy_gongseob_ji()]),
                ("Chapter 26: Jichang Kwak", lambda: [create_enemy_jichang_kwak()])
            ]),
            ("ARC 8: BUSAN", [
                ("Chapter 27: Jinrang's Return", lambda: [create_enemy_jinrang_enemy()]),
                ("Chapter 28: The Betrayal", lambda: [create_enemy_jaegyeon_na_enemy()]),
                ("Final Chapter: Charles Choi", lambda: [create_enemy_charles_choi()])
            ]),
            ("SECRET ARC: GENESIS", [
                ("Gen 0: Tom Lee", lambda: [create_enemy_tom_lee()]),
                ("Gen 0: Gapryong Kim", lambda: [create_enemy_gapryong_kim()])
            ])
        ]

        for arc_name, chapters in arcs:
            print(f"\n{'🔥' * 45}")
            slow_print(f"🔥 {arc_name} 🔥", 0.03)
            print(f"{'🔥' * 45}")
            time.sleep(0.5)

            for i, (chapter, enemy_factory) in enumerate(chapters):
                print(f"\n📖 {chapter} ({i+1}/{len(chapters)})")
                party = self.select_party(4) or [self.daniel, self.vasco, self.zack, self.jay]
                input("Press Enter to begin...")

                # FIX BUG-09: Create fresh enemies each attempt
                enemies = enemy_factory()
                if not self.battle(enemies, party):
                    print("\n💀 GAME OVER")
                    time.sleep(2)
                    return False

                # Track story flags
                flag_map = {
                    "Chapter 27: Jinrang's Return": ("jinrang_defeated",),
                    "Chapter 28: The Betrayal": ("jaegyeon_defeated",),
                    "Final Chapter: Charles Choi": ("charles_choi_defeated",),
                    "Gen 0: Tom Lee": ("tom_lee_defeated",),
                    "Gen 0: Gapryong Kim": ("gapryong_defeated",)
                }
                for flag in flag_map.get(chapter, []):
                    self.story_progress[flag] = True
                    self.check_unlocks()

                if i < len(chapters) - 1:
                    self.rest()

            self.save_game()

        print("\n🏆 STORY MODE COMPLETE!")
        self.save_game()
        time.sleep(2)
        return True

    def crew_gauntlet_mode(self):
        stages = [
            ("God Dog Recruits", [create_enemy_god_dog_member(), create_enemy_god_dog_member()]),
            ("Burn Knuckles", [create_enemy_burn_knuckles(), create_enemy_jace_park()]),
            ("Hostel Family", [create_enemy_hostel_member(), create_enemy_sally()]),
            ("Big Deal Soldiers", [create_enemy_big_deal_member(), create_enemy_brad()]),
            ("Workers Affiliates", [create_enemy_workers_member(), create_enemy_workers_affiliate()]),
            ("God Dog Elite", [create_enemy_god_dog_elite(), create_enemy_god_dog_elite()]),
            ("Hostel Executives", [create_enemy_warren_chae_enemy()]),
            ("Big Deal Executive", [create_enemy_jerry_kwon()]),
            ("Workers 3rd", [create_enemy_mandeok()]),
            ("Workers 2nd", [create_enemy_xiaolung()]),
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

        print("\n🏆 CREW GAUNTLET")
        party = self.select_party(4) or [self.daniel, self.vasco, self.zack, self.jay]

        for i, (stage, enemies) in enumerate(stages):
            self.wave = i + 1
            print(f"\n🏆 STAGE {self.wave}: {stage}")
            input("Press Enter...")

            if not self.battle(enemies, party):
                print(f"\n💀 GAUNTLET FAILED at Stage {self.wave}")
                time.sleep(2)
                return False
            if i < len(stages) - 1:
                self.rest()

        print("\n🏆 CREW GAUNTLET COMPLETE!")
        self.save_game()
        return True

    def boss_rush_mode(self):
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

        print("\n👑 BOSS RUSH — No rest between battles!")
        party = self.select_party(4) or [self.daniel, self.gun, self.goo, self.johan]

        for i, (boss, enemies) in enumerate(bosses):
            self.wave = i + 1
            print(f"\n👑 BOSS {self.wave}: {boss}")
            input("Press Enter...")
            if not self.battle(enemies, party):
                print(f"\n💀 BOSS RUSH FAILED at Boss {self.wave}")
                time.sleep(2)
                return False

        self.story_progress["boss_rush_complete"] = True
        # Unlock James Lee and Gitae on boss rush completion
        self.unlocked_characters["James Lee"] = True
        self.unlocked_characters["Gitae Kim"] = True
        self.unlocked_characters["Gapryong Kim"] = True
        print("✨ UNLOCKED: James Lee, Gitae Kim, Gapryong Kim!")
        self.save_game()
        print("\n👑 BOSS RUSH COMPLETE!")
        return True

    def survival_mode(self):
        print("\n♾️ ENDLESS SURVIVAL")
        party = self.select_party(4) or [self.daniel, self.vasco, self.zack, self.eli]
        wave = 0
        score = 0

        while True:
            wave += 1
            self.wave = wave
            print(f"\n🔥 WAVE {wave}")

            wave_enemies = []
            if wave <= 5:
                wave_enemies = [create_enemy_god_dog_member() for _ in range(min(3, wave))]
            elif wave <= 10:
                wave_enemies = [create_enemy_god_dog_elite(), create_enemy_god_dog_member(), create_enemy_god_dog_member()]
            elif wave <= 20:
                wave_enemies = [create_enemy_hostel_member(), create_enemy_big_deal_member(), create_enemy_workers_member()]
            elif wave <= 30:
                wave_enemies = [create_enemy_warren_chae_enemy(), create_enemy_jerry_kwon()]
            elif wave <= 40:
                wave_enemies = [create_enemy_mandeok(), create_enemy_xiaolung()]
            elif wave <= 50:
                wave_enemies = [create_enemy_vin_jin(), create_enemy_ryuhei()]
            else:
                wave_enemies = [random.choice([
                    create_enemy_gun_park_enemy, create_enemy_goo_kim_enemy,
                    create_enemy_kim_jungu_enemy, create_enemy_manager_kim_enemy,
                    create_enemy_jinrang_enemy, create_enemy_charles_choi,
                    create_enemy_gapryong_kim
                ])(), create_enemy_workers_affiliate(), create_enemy_workers_affiliate()]

            input("Press Enter...")
            if not self.battle(wave_enemies, party):
                print(f"\n☠️ SURVIVAL ENDED — Wave {wave} | Score: {score}")
                time.sleep(2)
                break

            score += wave * 100
            print(f"✨ Wave {wave} cleared! Score: {score}")
            self.save_game()

            if random.random() < 0.2:
                for c in party:
                    c.heal(int(c.max_hp * 0.2))
                    c.energy = min(c.max_energy, c.energy + int(c.max_energy * 0.2))
                print("🩹 Found supplies! +20% HP/Energy.")

        return score

    def training_mode(self):
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

        print("\n🥋 TRAINING ROOM")
        for key, name, _ in training_options:
            print(f"  {key}. {name}")
        print("  b. Back")

        choice = input("> ").strip()
        if choice.lower() == 'b':
            return

        for key, name, func in training_options:
            if choice == key:
                party = self.select_party(4) or [self.daniel, self.vasco, self.zack, self.jay]
                self.rest()
                self.battle([func()], party)
                return

    def stats_mode(self):
        print(f"\n{'=' * 90}")
        slow_print("📊 STATISTICS", 0.03)
        print("=" * 90)
        print(f"🏆 Victories: {self.victories}")
        print(f"💀 Enemies Defeated: {self.total_kills}")
        print()
        print("✦ CHARACTER PATHS:")
        for char in self.all_characters:
            locked = self.unlocked_characters.get(char.name, True) is False
            if locked:
                print(f"  • {char.name}: 🔒 {self.unlock_requirements.get(char.name, 'Locked')}")
            elif char.path:
                copy_info = f" [📚{char.copy_count}/10]" if char.name == "Johan Seong" and hasattr(char, 'copy_count') else ""
                print(f"  • {char.name}{copy_info}: {char.path.value[:30]} Lv.{char.path_level} ({char.path_exp}/100 EXP)")
            else:
                print(f"  • {char.name}: No path")
        input("\nPress Enter...")


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    print(f"\n{'=' * 90}")
    slow_print("👊👊👊 LOOKISM: AWAKENED FIST v2 — FIXED EDITION 👊👊👊", 0.02)
    print("    ALL BUGS FIXED | CANON CORRECTED | 41 PLAYABLE FIGHTERS")
    print("    Based on Park Tae-joon's Lookism (2014-2025)")
    print("=" * 90)
    print("\nFIXES APPLIED:")
    print("  ✅ Double UI/Beast multiplier bug fixed")
    print("  ✅ Enemy damage now uses enemy's own multiplier")
    print("  ✅ Johan save/load preserves all copied techniques")
    print("  ✅ God Eye uses proper 5-turn timer")
    print("  ✅ Cap Guy merged with Manager Kim (canon identity)")
    print("  ✅ Recursion replaced with while loops (no stack overflow)")
    print("  ✅ cleanup() only applies player buffs to party, not enemies")
    print("  ✅ Logan Lee has no infinity technique (he's a bully)")
    print("  ✅ James Lee's infinity DMG corrected below Gapryong's")
    print("  ✅ Daniel's HP reduced to reflect early-story weakness")
    print("=" * 90)
    time.sleep(0.5)

    save_exists = os.path.exists(SAVE_FILE)
    if save_exists:
        print("\n💾 Save file found!")
        load_choice = input("Load previous game? (y/n): ").lower()
        game = LookismGame(load_saved=(load_choice == 'y'))
    else:
        game = LookismGame(load_saved=False)

    while True:
        print(f"\n{'─' * 50}")
        print("MAIN MENU")
        print("─" * 50)
        print("1. 📖 Story Mode")
        print("2. 🏆 Crew Gauntlet")
        print("3. 👑 Boss Rush")
        print("4. ♾️  Endless Survival")
        print("5. 🥋 Training Room")
        print("6. 📊 Stats & Records")
        print("7. 🛤️  Path Management")
        print("8. 💾 Save/Load")
        print("9. ❌ Exit")
        print("─" * 50)

        choice = input("> ").strip()

        if choice == "1":   game.story_mode()
        elif choice == "2": game.crew_gauntlet_mode()
        elif choice == "3": game.boss_rush_mode()
        elif choice == "4": game.survival_mode()
        elif choice == "5": game.training_mode()
        elif choice == "6": game.stats_mode()
        elif choice == "7": game.path_management_menu()
        elif choice == "8":
            print("1. Save  2. Load  3. Delete  4. Back")
            sc = input("> ").strip()
            if sc == "1":   game.save_game()
            elif sc == "2": game.load_game() and print("✅ Loaded!")
            elif sc == "3":
                if input("Delete save? (y/n): ").lower() == 'y':
                    if SaveSystem.delete_save():
                        game = LookismGame(load_saved=False)
                        print("🗑️ Save deleted. New game started.")
            input("Press Enter...")
        elif choice == "9":
            if input("Save before exit? (y/n): ").lower() == 'y':
                game.save_game()
            slow_print("\nThanks for playing! See you next time, fighter.\n", 0.03)
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)
