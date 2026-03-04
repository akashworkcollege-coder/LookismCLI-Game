#!/usr/bin/env python3
"""
LOOKISM: AWAKENED FIST - COMPLETE CANON EDITION
ALL 51 FIGHTING CHARACTERS - 100% Manhwa Accurate
ENHANCED JOHAN COPY MECHANICS - COMPLETE ABILITY DESCRIPTIONS
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
# CONFIGURATION
# ============================================================================

TEXT_SPEED = 0.03  # Faster default text speed
BATTLE_START_DELAY = 1.0
TURN_DELAY = 0.5
ACTION_DELAY = 0.3
VICTORY_DELAY = 1.5
SAVE_FILE = "lookism_save.json"


def slow_print(text, delay=None):
    """Print text character by character for dramatic effect"""
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
        """Save game progress to file"""
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(game_state, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False

    @staticmethod
    def load_game():
        """Load game progress from file"""
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
        """Delete save file"""
        try:
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
                return True
            return False
        except:
            return False


# ============================================================================
# CANON GYEONGJI (REALM) SYSTEM
# ============================================================================

class Realm(Enum):
    NONE = "⚪ None"
    SPEED = "🔵 Speed"
    STRENGTH = "🔴 Strength"
    TENACITY = "🟢 Tenacity"
    TECHNIQUE = "🩷 Technique"
    OVERCOMING = "🟣 Overcoming"


class RealmEffect:
    """Separate class to handle realm effects properly"""

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
# COMPLETE PATH SYSTEM WITH ALL INFINITY TECHNIQUES
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
    JAKE_GAPRYONG = "👑 Jake Kim's Gapryong Blood"
    GUN_YAMAZAKI = "🏯 Gun Park's Yamazaki Heir"
    GUN_CONSTANT_UI = "👁️ Gun Park's Constant UI"
    GOO_MOONLIGHT = "🌙 Goo Kim's Moonlight Sword"
    GOO_FIFTH = "✨ Goo Kim's Fifth Sword"
    JOONGOO_HWARANG = "⚔️ Kim Jun-gu's Hwarang Sword"
    JOONGOO_ARMED = "🗡️ Kim Jun-gu's Armed Beast"

    # WORKERS
    MANDEOK_POWER = "💪 Mandeok's Titan Strength"
    CAP_GUY_CQC = "🔫 Cap Guy's CQC Master"
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
# ============================================================================

INFINITY_TECHNIQUES = {
    # GEN 0 LEGENDS
    Path.GAPRYONG_CONVICTION: {
        "name": "👑 INFINITE GAPRYONG: Legend's Fist",
        "cost": 150,
        "dmg": (300, 400),
        "desc": "The legendary fist that defeated the Yamazaki Syndicate. Gapryong Kim's ultimate conviction - a punch that changed the course of Gen 0 and brought peace to the underworld."
    },
    Path.TOM_LEE_WILD: {
        "name": "🐅 INFINITE WILD: Tom Lee Special",
        "cost": 140,
        "dmg": (280, 380),
        "desc": "Tom Lee's ultimate technique. Biting, slashing, pure animal instinct. 'I'm gonna tear his bones apart.' A wild flurry that combines every dirty fighting technique imaginable."
    },
    Path.CHARLES_ELITE: {
        "name": "🎭 INFINITE ELITE: Chairman's Authority",
        "cost": 145,
        "dmg": (290, 390),
        "desc": "Charles Choi's invisible attacks. The puppet master's final move - a strike so fast and precise it cannot be seen, only felt when it's too late."
    },
    Path.JINYOUNG_COPY: {
        "name": "🔄 INFINITE COPY: Medical Genius",
        "cost": 135,
        "dmg": (270, 370),
        "desc": "Jinyoung Park's perfect copy ability. Any technique seen once can be replicated with surgical precision. The ultimate expression of his genius."
    },
    Path.BAEKHO_BEAST: {
        "name": "🐯 INFINITE BEAST: White Tiger's Wrath",
        "cost": 130,
        "dmg": (260, 360),
        "desc": "Baekho's beast mode unleashed. The White Tiger's ultimate technique - a devastating barrage that channels the ferocity of a cornered tiger."
    },
    Path.GAPRYONG_FIST_MEMBER: {
        "name": "👊 INFINITE FIST: Legendary Crew",
        "cost": 120,
        "dmg": (240, 340),
        "desc": "The combined strength of Gapryong's Fist. Legends stand together - a synchronized assault that only members of the legendary crew can execute."
    },

    # 1ST GENERATION KINGS
    Path.JAMES_LEE_INVISIBLE: {
        "name": "👑 INFINITE JAMES: Legend of the 1st Gen",
        "cost": 150,
        "dmg": (300, 420),
        "desc": "James Lee's perfected invisible attacks. The peak of the 1st Generation - a dance of death so beautiful and so lethal that it single-handedly dismantled an entire era of fighting."
    },
    Path.GITAE_KIM: {
        "name": "⚡ INFINITE GITAE: Gapryong's Shadow",
        "cost": 145,
        "dmg": (290, 400),
        "desc": "Gitae Kim inherits his father's power. The unknown technique of the King of Seoul - raw, brutal, and carrying the weight of his legendary bloodline."
    },
    Path.JICHANG_HAND_BLADE: {
        "name": "🩷 INFINITE HAND BLADE: King's Edge",
        "cost": 135,
        "dmg": (270, 380),
        "desc": "Jichang Kwak's ultimate hand blade technique. Cuts through anything - his hands become like forged steel, capable of severing bone and concrete alike."
    },
    Path.TAESOO_MA_FIST: {
        "name": "🔴 INFINITE RIGHT HAND: Ansan's Pride",
        "cost": 140,
        "dmg": (280, 400),
        "desc": "Taesoo Ma's right fist - no technique, just overwhelming power. The fist that ruled Ansan, backed by sheer determination and raw strength."
    },
    Path.GONGSEOB_IRON: {
        "name": "🔨 INFINITE IRON: The Monk's Fortress",
        "cost": 130,
        "dmg": (260, 360),
        "desc": "Gongseob Ji's iron boxing. Speed and durability combined into an unbreakable fighting style that makes him a living fortress."
    },
    Path.SEOKDU_HEADBUTT: {
        "name": "💢 INFINITE HEADBUTT: Suwon's Crown",
        "cost": 125,
        "dmg": (250, 350),
        "desc": "Seokdu Wang's legendary headbutt. His forehead is harder than steel - a single strike can end a fight instantly."
    },
    Path.JAEGYEON_SPEED: {
        "name": "🔵 INFINITE SPEED: Incheon Flash",
        "cost": 135,
        "dmg": (270, 370),
        "desc": "Jaegyeon Na's ultimate speed. He doesn't move - he simply arrives. Before you can blink, the fight is already over."
    },
    Path.SEONGJI_MONSTER: {
        "name": "🦍 INFINITE MONSTER: Cheonliang's King",
        "cost": 140,
        "dmg": (280, 390),
        "desc": "Seongji Yuk's mastery of Ssireum, Judo, and Kudo combined into a monstrous fighting style that devours opponents whole."
    },
    Path.JINRANG_CONVICTION: {
        "name": "👑 INFINITE DISCIPLE: True Conviction",
        "cost": 150,
        "dmg": (300, 420),
        "desc": "Jinrang's ultimate technique. As Gapryong's true disciple, his conviction is absolute - a fist that carries his master's legacy."
    },

    # GEN 2 CREW LEADERS
    Path.DANIEL_UI: {
        "name": "👁️ INFINITE UI: Perfect Body",
        "cost": 100,
        "dmg": (250, 350),
        "desc": "Daniel's Ultra Instinct awakening. The body moves before the mind - a state of pure, instinctive combat where every movement is perfect."
    },
    Path.DANIEL_COPY: {
        "name": "⚡ INFINITE COPY: Perfect Replication",
        "cost": 90,
        "dmg": (220, 320),
        "desc": "Daniel's copy ability at its peak. Any technique becomes his own, replicated with such precision that even the original user would be impressed."
    },
    Path.ZACK_IRON: {
        "name": "🔨 INFINITE IRON BOXING: Shining Star",
        "cost": 80,
        "dmg": (200, 300),
        "desc": "Zack's ultimate iron boxing technique. The star shines brightest at the end - a combination of Gongseob Ji's teachings and his own burning determination."
    },
    Path.JOHAN_GOD_EYE: {
        "name": "👁️ INFINITE GOD EYE: Ultimate Copy",
        "cost": 95,
        "dmg": (230, 330),
        "desc": "Johan's God Eye sees all. Perfect replication of any technique, even through blindness - he doesn't need to see to understand your every move."
    },
    Path.JOHAN_CHOREOGRAPHY: {
        "name": "💃 INFINITE CHOREOGRAPHY: Dance of Death",
        "cost": 85,
        "dmg": (210, 310),
        "desc": "Johan's dance combat perfected. Flowing movements that destroy, created from K-Pop choreography and turned into an art form of violence."
    },
    Path.VASCO_SYSTEMA: {
        "name": "🇷🇺 INFINITE SYSTEMA: Russian Cross",
        "cost": 80,
        "dmg": (200, 300),
        "desc": "Vasco's Systema mastery. The Russian martial art at its peak - a fluid, unpredictable style that adapts to any threat."
    },
    Path.VASCO_MUAY_THAI: {
        "name": "🇹🇭 INFINITE MUAY THAI: Sunken Fist",
        "cost": 85,
        "dmg": (210, 310),
        "desc": "Vasco's Muay Thai legend. The fist that sank ships - devastating elbow and knee strikes honed through inhuman training."
    },
    Path.JAY_KALI: {
        "name": "🇵🇭 INFINITE KALI: Twin Blade Dance",
        "cost": 75,
        "dmg": (190, 290),
        "desc": "Jay's Kali mastery. Twin blades moving as one - a whirlwind of steel that leaves no opening for counterattack."
    },
    Path.ELI_BEAST: {
        "name": "🦁 INFINITE BEAST: King of Beasts",
        "cost": 85,
        "dmg": (210, 310),
        "desc": "Eli's beast mode unleashed. Pure animal instinct - he fights like a cornered wolf, using every part of his body as a weapon."
    },
    Path.ELI_TOM_LEE: {
        "name": "🐅 INFINITE WILD: Inherited Instinct",
        "cost": 90,
        "dmg": (220, 320),
        "desc": "Eli inherits Tom Lee's wild style. The student surpasses the master - incorporating the legendary wildness into his own beastly arsenal."
    },
    Path.WARREN_JKD: {
        "name": "🥋 INFINITE JKD: Way of the Intercepting Fist",
        "cost": 75,
        "dmg": (190, 290),
        "desc": "Warren's Jeet Kune Do mastery. Bruce Lee's philosophy perfected - intercepting attacks before they fully form."
    },
    Path.WARREN_CQC: {
        "name": "🔫 INFINITE CQC: NEW Full Release",
        "cost": 95,
        "dmg": (230, 330),
        "desc": "Warren's CQC operator technique. Military precision at its finest - developed through years of training with Manager Kim."
    },
    Path.WARREN_HEART: {
        "name": "💔 INFINITE HEART: One-Inch Punch",
        "cost": 80,
        "dmg": (200, 300),
        "desc": "Warren's heart attack punch. The one-inch punch that stops hearts - devastating power from zero distance."
    },
    Path.JAKE_CONVICTION: {
        "name": "⚖️ INFINITE CONVICTION: Will of Iron",
        "cost": 85,
        "dmg": (210, 310),
        "desc": "Jake's conviction-powered strikes. Willpower made manifest - each punch carries the weight of his determination."
    },
    Path.JAKE_GAPRYONG: {
        "name": "👑 INFINITE BLOOD: Inherited Fist",
        "cost": 100,
        "dmg": (240, 340),
        "desc": "Jake inherits Gapryong's legendary fist. Bloodline awakened - the same conviction that made his father the strongest."
    },
    Path.GUN_YAMAZAKI: {
        "name": "🏯 INFINITE YAMAZAKI: Black Bone",
        "cost": 110,
        "dmg": (250, 350),
        "desc": "Gun's Yamazaki heritage unleashed. The darkness within - a technique passed down through generations of the infamous syndicate."
    },
    Path.GUN_CONSTANT_UI: {
        "name": "👁️ INFINITE UI: Perpetual Awakening",
        "cost": 120,
        "dmg": (260, 360),
        "desc": "Gun's constant Ultra Instinct. Always awakened, always perfect - a state of perpetual combat readiness."
    },
    Path.GOO_MOONLIGHT: {
        "name": "🌙 INFINITE MOONLIGHT: Three Sword Style",
        "cost": 95,
        "dmg": (230, 330),
        "desc": "Goo's moonlight sword technique. Three swords, infinite possibilities - each strike flows into the next like phases of the moon."
    },
    Path.GOO_FIFTH: {
        "name": "✨ INFINITE FIFTH: Impossible Technique",
        "cost": 130,
        "dmg": (270, 370),
        "desc": "Goo's legendary fifth sword. A technique that shouldn't exist - a sword style that defies the laws of combat."
    },
    Path.JOONGOO_HWARANG: {
        "name": "⚔️ INFINITE HWARANG: Blade Dance",
        "cost": 100,
        "dmg": (240, 340),
        "desc": "Kim Jun-gu's Hwarang sword technique. Cuts that sever goblins - an ancient style passed down through generations."
    },
    Path.JOONGOO_ARMED: {
        "name": "🗡️ INFINITE ARMED: Top 3 When Armed",
        "cost": 110,
        "dmg": (250, 350),
        "desc": "Kim Jun-gu with his weapon. Top 3 in the world when armed - his true power only manifests with a blade in hand."
    },

    # WORKERS
    Path.MANDEOK_POWER: {
        "name": "💪 INFINITE TITAN: Earth Shaker",
        "cost": 100,
        "dmg": (240, 340),
        "desc": "Mandeok's raw power unleashed. A strike that shakes the earth - pure, devastating strength without any technique."
    },
    Path.CAP_GUY_CQC: {
        "name": "🔫 INFINITE CQC: Code 66",
        "cost": 95,
        "dmg": (230, 330),
        "desc": "Cap Guy's ultimate CQC. Silver Yarn threads bind and cut - a unique style combining military precision with supernatural elements."
    },
    Path.XIAOLUNG_MUAY_THAI: {
        "name": "🇹🇭 INFINITE MUAY THAI: Death Blow",
        "cost": 90,
        "dmg": (220, 320),
        "desc": "Xiaolung's perfected Muay Thai. Elbows and knees become death - the eight limbs of Muay Thai perfected to their lethal peak."
    },
    Path.RYUHEI_YAKUZA: {
        "name": "⚔️ INFINITE YAKUZA: Gang Lord",
        "cost": 85,
        "dmg": (210, 310),
        "desc": "Ryuhei's yakuza style. Dirty fighting at its peak - street-smart, ruthless, and effective."
    },
    Path.SAMUEL_AMBITION: {
        "name": "👑 INFINITE AMBITION: King's Path",
        "cost": 95,
        "dmg": (230, 330),
        "desc": "Samuel's ambition-fueled power. The betrayer's strength knows no limits - his drive to become king manifests in every strike."
    },
    Path.SINU_INVISIBLE: {
        "name": "🌀 INFINITE INVISIBLE: Ghost Fist",
        "cost": 90,
        "dmg": (220, 320),
        "desc": "Sinu Han's invisible attacks. Unseeable, unavoidable - a hybrid of hand and leg techniques that come from nowhere."
    },
    Path.LOGAN_BULLY: {
        "name": "👊 INFINITE BULLY: Cheap Shot",
        "cost": 60,
        "dmg": (150, 250),
        "desc": "Logan Lee's ultimate cheap shot. When you least expect it - a coward's strike that somehow always finds its mark."
    },

    # CHEONLIANG
    Path.VIN_JIN_SSIREUM: {
        "name": "🇰🇷 INFINITE SSIREUM: Wrestling God",
        "cost": 90,
        "dmg": (220, 320),
        "desc": "Vin Jin's perfected ssireum. Throws that break bones - traditional Korean wrestling elevated to an art of destruction."
    },
    Path.SEONGJI_MARTIAL: {
        "name": "🥋 INFINITE MARTIAL: Triple Threat",
        "cost": 100,
        "dmg": (240, 340),
        "desc": "Seongji's combination of ssireum, judo, and kudo. A complete martial artist who mastered three distinct styles."
    },
    Path.HAN_JAEHA: {
        "name": "🤼 INFINITE TRADITION: Cheonliang Wrestling",
        "cost": 70,
        "dmg": (180, 280),
        "desc": "Han Jaeha's traditional ssireum. Pure Korean wrestling - honoring the techniques passed down through generations."
    },
    Path.BAEK_SEONG_TAEKKYON: {
        "name": "🦢 INFINITE FLOW: Taekkyon Dance",
        "cost": 75,
        "dmg": (190, 290),
        "desc": "Baek Seong's flowing taekkyon. Dance-like movements that confuse and destroy - the graceful art of Korean footwork."
    },

    # YAMAZAKI
    Path.SHINGEN_YAMAZAKI: {
        "name": "🏯 INFINITE YAMAZAKI: Syndicate's Wrath",
        "cost": 160,
        "dmg": (320, 450),
        "desc": "Shingen Yamazaki's ultimate. The head of the Yamazaki Syndicate unleashes the full fury of the infamous organization."
    },
    Path.PARK_FATHER: {
        "name": "❓ INFINITE MYSTERY: Bloodline Secret",
        "cost": 140,
        "dmg": (300, 400),
        "desc": "Park Jonggun's father's mysterious technique. The source of Gun's power - a secret lost to time but felt in every strike."
    },

    # LAW ENFORCEMENT
    Path.KIM_MINJAE_JUDO: {
        "name": "🥋 INFINITE JUDO: Police Force",
        "cost": 65,
        "dmg": (170, 270),
        "desc": "Kim Minjae's perfected judo throws. Law and order brought to the streets - using an opponent's force against them."
    },
    Path.DETECTIVE_KANG_BOXING: {
        "name": "🥊 INFINITE DETECTIVE: Veteran's Fist",
        "cost": 70,
        "dmg": (180, 280),
        "desc": "Detective Kang's veteran boxing. Years of experience packed into every punch - street-smart and effective."
    }
}


# ============================================================================
# BASE CHARACTER CLASS WITH FIXES
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

        # Status flags
        self.stunned = False
        self.bound = False
        self.exhausted = False

        # Special mode flags
        self.ui_mode = False
        self.ui_timer = 0
        self.beast_mode = False
        self.beast_timer = 0
        self.veinous_rage = False
        self.silver_yarn_active = False
        self.muscle_boost = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        # Apply damage reduction from realms
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
        """Base damage multiplier - override in specific characters"""
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

        return mult, buffs

    def apply_realm_regen(self):
        """Apply realm regeneration effects"""
        if self.active_realm == Realm.TENACITY:
            self.heal(15)
            return True
        return False

    def to_dict(self):
        """Convert character to dictionary for saving"""
        return {
            'name': self.name,
            'path': self.path.name if self.path else None,
            'path_level': self.path_level,
            'path_exp': self.path_exp,
            'hp': self.hp,
            'energy': self.energy,
            'active_realm': self.active_realm.name if self.active_realm != Realm.NONE else None,
            'form': self.form,
            'ui_mode': self.ui_mode,
            'ui_timer': self.ui_timer,
            'beast_mode': self.beast_mode,
            'beast_timer': self.beast_timer
        }

    def from_dict(self, data):
        """Load character from dictionary"""
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

        self.form = data.get('form', 'Normal')
        self.ui_mode = data.get('ui_mode', False)
        self.ui_timer = data.get('ui_timer', 0)
        self.beast_mode = data.get('beast_mode', False)
        self.beast_timer = data.get('beast_timer', 0)

    def choose_path(self, path):
        """Choose a path for the character"""
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
        """Reset current path"""
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
# ENEMY CLASS WITH FIXED ABILITIES
# ============================================================================

class Enemy(Character):
    def __init__(self, name, title, hp, energy, abilities, rank, affiliation="", realm_list=None):
        super().__init__(name, title, hp, energy, realm_list)
        # Add cost to abilities
        self.abilities = {}
        for key, abil in abilities.items():
            self.abilities[key] = {
                "name": abil["name"],
                "dmg": abil["dmg"],
                "cost": abil.get("cost", 20),  # Default cost if missing
                "type": abil.get("type", "damage"),
                "desc": abil.get("desc", f"{abil['name']} - A basic attack.")
            }
        self.rank = rank
        self.affiliation = affiliation
        self.ai_pattern = []


# ============================================================================
# COMPLETE CHARACTER CLASSES - ALL 51 FIGHTERS WITH DESCRIPTIONS
# ============================================================================

# ===== GEN 0 LEGENDS =====

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
        self.abilities = {
            '1': {"name": "👑 Conviction Punch", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "The foundation of Gapryong's style. A punch backed by unshakeable belief - the same conviction that united Gen 0."},
            '2': {"name": "👑 Gapryong's Fist", "cost": 40, "dmg": (130, 180), "type": "damage",
                  "desc": "The legendary fist that defeated the Yamazaki Syndicate. A single strike carrying the weight of an entire generation."},
            '3': {"name": "👑 Will to Protect", "cost": 35, "dmg": (110, 160), "type": "damage",
                  "desc": "A technique born from Gapryong's desire to protect his crew. Each strike carries the strength of his bonds."},
            '4': {"name": "👑 Legend's Legacy", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "The accumulated power of a legend. Gapryong shows why he stood at the peak of Gen 0."},
            '5': {"name": "🛡️ Gapryong's Defense", "cost": 25, "dmg": (0, 0), "type": "utility",
                  "desc": "The defensive stance of a leader. Gapryong protects those behind him, reducing damage by 50% this turn."}
        }


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
        self.abilities = {
            '1': {"name": "🐅 Wild Strike", "cost": 25, "dmg": (90, 140), "type": "damage",
                  "desc": "A primal, untamed strike. Tom Lee fights like a wild animal - no rules, no technique, just pure aggression."},
            '2': {"name": "🐅 Tom Lee Special", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "His signature move. A combination of biting, clawing, and striking that leaves opponents torn apart."},
            '3': {"name": "🐅 Gen 0 Power", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Raw power from the legendary era. A reminder of why Tom Lee was feared even among the strongest."},
            '4': {"name": "🐅 Bite Force", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "Literally biting his opponents. Tom Lee's jaw strength is comparable to a wild animal's - terrifying and effective."}
        }


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
        self.abilities = {
            '1': {"name": "🎭 Invisible Strike", "cost": 30, "dmg": (90, 140), "type": "damage",
                  "desc": "A strike too fast to see. Charles Choi's invisible attacks come from nowhere - you only feel them after they've landed."},
            '2': {"name": "🎭 Chairman's Authority", "cost": 40, "dmg": (120, 170), "type": "damage",
                  "desc": "The power of the HNH Group chairman. A devastating strike backed by decades of manipulation and control."},
            '3': {"name": "🎭 Elite Technique", "cost": 35, "dmg": (110, 160), "type": "damage",
                  "desc": "A technique passed down through Gapryong's Fist. Refined, elegant, and lethal."},
            '4': {"name": "🎭 Truth of Two Bodies", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "The secret technique behind the two bodies mystery. A devastating combination that reveals the truth of his power."}
        }


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
        self.abilities = {
            '1': {"name": "🔄 Copy: Taekwondo", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Perfect replication of Taekwondo techniques. Jinyoung's genius allows him to copy any martial art after seeing it once."},
            '2': {"name": "🔄 Copy: Karate", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Flawless Karate techniques. The precision of a master, achieved through pure analytical ability."},
            '3': {"name": "🔄 Copy: Boxing", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "World-class boxing technique. Jabs and crosses executed with mechanical perfection."},
            '4': {"name": "🔄 Medical Precision", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "Combining medical knowledge with combat. Jinyoung strikes vital points with surgical accuracy."}
        }


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
        self.abilities = {
            '1': {"name": "🐯 Tiger Strike", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "A strike with the ferocity of a white tiger. Baekho channels the spirit of the beast."},
            '2': {"name": "🐯 Beast Mode", "cost": 40, "dmg": (130, 180), "type": "damage",
                  "desc": "Unleashing his inner beast. Baekho's attacks become more savage and unpredictable."},
            '3': {"name": "🐯 White Tiger's Claw", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "Raking claw strikes that tear through defenses. The signature move of the White Tiger."}
        }


# ===== 1ST GENERATION KINGS =====

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
        self.abilities = {
            '1': {"name": "👑 Invisible Kick", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "A kick that can't be seen. James Lee's speed transcends human perception - you'll be on the ground before you know what hit you."},
            '2': {"name": "👑 Perfect Form", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Technique perfected to its absolute peak. Every movement is economical, efficient, and deadly."},
            '3': {"name": "👑 One Man Circle", "cost": 50, "dmg": (170, 220), "type": "damage",
                  "desc": "The technique that dismantled the 1st Generation. A devastating combination that leaves no survivors standing."},
            '4': {"name": "👑 Legend's Speed", "cost": 30, "dmg": (0, 0), "type": "buff",
                  "desc": "Tapping into legendary speed. James becomes even faster, increasing damage by 30% for 3 turns."}
        }


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
        self.abilities = {
            '1': {"name": "⚡ Gapryong's Blood", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "The blood of Gapryong flows through him. Gitae taps into his inherited power, striking with legendary force."},
            '2': {"name": "⚡ Inherited Power", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Power passed down through generations. Gitae unleashes the full potential of his bloodline."},
            '3': {"name": "⚡ King's Authority", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "The commanding presence of Seoul's king. A strike that demands submission."}
        }


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
        self.abilities = {
            '1': {"name": "🩷 Hand Blade", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "Jichang's signature technique. His hand becomes like a forged blade, capable of cutting through concrete."},
            '2': {"name": "🩷 Double Edge", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "A devastating combination of two hand blade strikes. The first cuts, the second finishes."},
            '3': {"name": "🩷 Seoul King's Pride", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "The pride of Seoul's king manifested. A technique that carries the weight of his territory."}
        }


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
        self.abilities = {
            '1': {"name": "🔴 Right Hand", "cost": 35, "dmg": (130, 180), "type": "damage",
                  "desc": "Taesoo's legendary right fist. No technique, no strategy - just overwhelming, destructive power."},
            '2': {"name": "🔴 No Technique", "cost": 40, "dmg": (150, 200), "type": "damage",
                  "desc": "Pure, raw strength. Taesoo abandons all pretense of technique and simply destroys with brute force."},
            '3': {"name": "🔴 Ansan King", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "The pride of Ansan. A strike that represents Taesoo's reign as the undisputed king of his territory."}
        }


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
        self.abilities = {
            '1': {"name": "🩷 Iron Boxing", "cost": 25, "dmg": (90, 140), "type": "damage",
                  "desc": "Gongseob's unique style combining speed with iron-like durability. His fists are weapons, his body a shield."},
            '2': {"name": "🩷 Speed Technique", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "Blazing fast strikes that blur the line between offense and defense. Gongseob's speed is his greatest asset."},
            '3': {"name": "🩷 Tungsten Defense", "cost": 20, "dmg": (0, 0), "type": "utility",
                  "desc": "Adopting an impenetrable defensive stance. Gongseob's body becomes as hard as tungsten, reducing damage by 70% this turn."}
        }


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
        self.abilities = {
            '1': {"name": "💢 Headbutt", "cost": 30, "dmg": (120, 170), "type": "damage",
                  "desc": "Seokdu's primary weapon - his forehead. Harder than steel, a single headbutt can end a fight instantly."},
            '2': {"name": "💢 Iron Forehead", "cost": 25, "dmg": (100, 150), "type": "damage",
                  "desc": "Years of training have made Seokdu's forehead unbreakable. He strikes with the force of a battering ram."},
            '3': {"name": "💢 Suwon's Crown", "cost": 35, "dmg": (140, 190), "type": "damage",
                  "desc": "The king's ultimate headbutt. Seokdu puts his entire body weight behind his signature move."}
        }


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
        self.abilities = {
            '1': {"name": "🔵 Incheon Speed", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "The speed of Incheon's king. Jaegyeon moves faster than the eye can track, striking from impossible angles."},
            '2': {"name": "🔵 Faster Than Light", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Exaggerated by legend, but not by much. Jaegyeon's speed approaches the absolute limit of human capability."},
            '3': {"name": "🔵 King of Incheon", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "The pride of Incheon manifested. A flurry of strikes that overwhelms any defense."}
        }


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
        self.abilities = {
            '1': {"name": "🇰🇷 Ssireum: Throw", "cost": 25, "dmg": (90, 140), "type": "damage",
                  "desc": "Traditional Korean wrestling technique. Seongji uses his opponent's momentum against them, slamming them to the ground."},
            '2': {"name": "🥋 Judo: Ippon", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "A perfect Judo throw. Seongji's mastery of grappling allows him to control any opponent."},
            '3': {"name": "🥋 Kudo: Dirty Boxing", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "The brutal striking of Kudo. Seongji combines dirty boxing with his grappling base for devastating results."},
            '4': {"name": "🦍 Monster Mode", "cost": 45, "dmg": (160, 210), "type": "damage",
                  "desc": "Unleashing his monstrous side. Seongji abandons technique for pure, savage power."}
        }


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
        self.abilities = {
            '1': {"name": "👑 Jinrang's Conviction", "cost": 35, "dmg": (130, 180), "type": "damage",
                  "desc": "The conviction of Gapryong's true disciple. Jinrang's strikes carry the same weight as his master's."},
            '2': {"name": "👑 Gapryong's Disciple", "cost": 40, "dmg": (150, 200), "type": "damage",
                  "desc": "Techniques passed down directly from Gapryong. Jinrang fights with the legacy of the strongest."},
            '3': {"name": "👑 Busan King", "cost": 45, "dmg": (170, 220), "type": "damage",
                  "desc": "The authority of Busan's king. Jinrang commands respect with every strike."},
            '4': {"name": "👑 True Conviction", "cost": 60, "dmg": (200, 250), "type": "damage",
                  "desc": "The ultimate expression of his faith in Gapryong's teachings. A fist that cannot be denied."}
        }


# ===== GEN 2 CREW LEADERS =====

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

        self.abilities = {
            '1': {"name": "👊 Desperate Flailing", "cost": 10, "dmg": (20, 35), "type": "damage",
                  "desc": "Early Daniel's fighting style - or lack thereof. Wild, uncoordinated swings born of desperation."},
            '2': {"name": "🔄 Instinctive Copy", "cost": 20, "dmg": (30, 50), "type": "damage",
                  "desc": "Daniel's natural copying ability. He unconsciously replicates techniques he's seen, though imperfectly."},
            '3': {"name": "🇷🇺 Systema: Ryabina", "cost": 25, "dmg": (50, 70), "type": "damage",
                  "desc": "A Systema technique learned from Sophia. A devastating strike that targets vital points."},
            '4': {"name": "⚡ Copy: Zack's Counter", "cost": 25, "dmg": (55, 80), "type": "damage",
                  "desc": "Daniel replicates Zack Lee's signature counter punch. Perfect form, perfect timing."},
            '5': {"name": "⚡ Copy: Vasco's Sunken Fist", "cost": 30, "dmg": (65, 90), "type": "damage",
                  "desc": "Vasco's Muay Thai technique, perfectly copied. A devastating downward strike."},
            '6': {"name": "⚡ Copy: Eli's Animal Instinct", "cost": 30, "dmg": (70, 95), "type": "damage",
                  "desc": "Eli Jang's wild style replicated. Daniel fights with unexpected, animalistic movements."},
            '7': {"name": "⚡ Copy: Jake's Conviction", "cost": 35, "dmg": (75, 105), "type": "damage",
                  "desc": "Jake Kim's conviction-powered strikes. Daniel taps into the same determination."},
            '8': {"name": "⚡ Copy: Johan's Choreography", "cost": 40, "dmg": (80, 115), "type": "damage",
                  "desc": "Johan Seong's dance combat. Daniel flows through attacks like a deadly performance."},
            '9': {"name": "⚡ Copy: Gun's Taekwondo", "cost": 35, "dmg": (80, 110), "type": "damage",
                  "desc": "Gun Park's Taekwondo mastery. Daniel executes spinning kicks with perfect form."},
            '10': {"name": "🩷 Jichang's Hand Blade", "cost": 45, "dmg": (90, 130), "type": "damage",
                   "desc": "Jichang Kwak's legendary technique. Daniel's hand becomes a blade, cutting through defenses."},
            '11': {"name": "👑 Gapryong's Conviction", "cost": 60, "dmg": (120, 180), "type": "damage",
                   "desc": "The ultimate copy - Gapryong Kim's legendary fist. Daniel channels the conviction of the strongest."},
            '12': {"name": "👁️ Ultra Instinct", "cost": 100, "dmg": (0, 0), "type": "ui",
                   "desc": "Daniel's ultimate awakening. His body moves before his mind, achieving perfect, instinctive combat. +150% damage for 3 turns."}
        }

    def activate_ui(self):
        self.ui_mode = True
        self.ui_timer = 3
        self.form = "ULTRA INSTINCT"
        self.heal(50)
        return "👁️👁️👁️👁️👁️ ULTRA INSTINCT! White hair awakens! Daniel's body moves on its own, achieving perfect combat!"

    def get_damage_multiplier(self):
        mult, buffs = super().get_damage_multiplier()
        if self.ui_mode:
            mult *= 2.5
        return mult, buffs


class ZackLee(Character):
    def __init__(self):
        super().__init__("Zack Lee", "The Iron Boxer", 380, 280, [Realm.SPEED])
        self.canon_episode = 1
        self.paths_available = [Path.ZACK_IRON]
        self.heat_mode = False
        self.abilities = {
            '1': {"name": "🔨 Iron Fortress Stance", "cost": 15, "dmg": (0, 0), "type": "buff",
                  "desc": "Gongseob Ji's defensive stance. Zack becomes an immovable object, reducing damage by 50% for 2 turns."},
            '2': {"name": "🔨 Iron Fist", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Zack's fists become as hard as iron. A straightforward but powerful boxing combination."},
            '3': {"name": "🥊 Jab", "cost": 15, "dmg": (35, 55), "type": "damage",
                  "desc": "A lightning-fast jab. Zack uses it to measure distance and set up heavier strikes."},
            '4': {"name": "🥊 Cross", "cost": 20, "dmg": (45, 70), "type": "damage",
                  "desc": "A powerful cross punch. Zack puts his full body weight behind this strike."},
            '5': {"name": "⚡ Counter Punch", "cost": 30, "dmg": (75, 110), "type": "damage",
                  "desc": "Zack's specialty. He waits for the opponent to commit, then strikes with perfect timing."},
            '6': {"name": "💫 Shining Star", "cost": 50, "dmg": (100, 150), "type": "damage",
                  "desc": "Zack's ultimate technique. A blinding combination that leaves opponents seeing stars - both literally and figuratively."}
        }


class JohanSeong(Character):
    """Johan Seong - The God Eye - Enhanced Copy Mechanics with Descriptions"""

    def __init__(self, blind=True):
        super().__init__(
            "Johan Seong",
            "The God Eye",
            400, 300,
            [Realm.TECHNIQUE, Realm.SPEED, Realm.OVERCOMING]
        )
        self.canon_episode = 100
        self.blind = blind
        self.god_eye_active = False
        self.copy_count = 0
        self.max_copy = 10  # Can copy up to 10 techniques
        self.copied_techniques = []  # Store technique names
        self.copied_techniques_data = {}  # Store technique data for later use
        self.paths_available = [Path.JOHAN_GOD_EYE, Path.JOHAN_CHOREOGRAPHY]

        # Track viewing count for each technique
        self.technique_view_count = {}

        # Base abilities with descriptions
        self.abilities = {
            '1': {"name": "👁️ Copy: Taekwondo", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Johan's God Eye analyzes and replicates Taekwondo. Spinning kicks and precise strikes executed with perfect form."},
            '2': {"name": "👁️ Copy: Boxing", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Perfect boxing technique. Jabs, crosses, and hooks delivered with the precision of a champion."},
            '3': {"name": "👁️ Copy: Karate", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Traditional Karate strikes. Powerful, linear techniques with devastating focus."},
            '4': {"name": "👁️ Copy: Judo", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Judo throws and grappling. Johan uses an opponent's momentum against them with mechanical precision."},
            '5': {"name": "👁️ Copy: Aikido", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Aikido's flowing redirection. Johan turns attacks back on their users with minimal effort."},
            '6': {"name": "👁️ Copy: Capoeira", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "The dance-like movements of Capoeira. Johan weaves and strikes in a continuous flow."},
            '7': {"name": "💃 Choreography: God Dog", "cost": 40, "dmg": (85, 120), "type": "damage",
                  "desc": "Johan's original style, born from K-Pop choreography. A deadly dance that confuses and destroys."},
            '8': {"name": "💃 Choreography: Perfected", "cost": 45, "dmg": (95, 140), "type": "damage",
                  "desc": "The ultimate expression of his dance combat. Every movement flows into the next like a performance."},
            '9': {"name": "👁️ God Eye Activation", "cost": 30, "dmg": (0, 0), "type": "buff",
                  "desc": "Activating his God Eye. Johan's perception sharpens, allowing him to see and copy techniques more easily. +30% copy chance for 5 turns."},
        }

        # Add blindness passive if applicable
        if blind:
            self.abilities['10'] = {"name": "🕶️ Blindness (Overcoming)", "cost": 0, "dmg": (0, 0), "type": "passive",
                                    "desc": "Johan fights despite his blindness. His other senses sharpen, granting +30% damage from overcoming his disability."}
            self.title = "The Blind God Eye"

    def activate_god_eye(self):
        """Activate the God Eye ability"""
        self.god_eye_active = True
        self.form = "GOD EYE AWAKENED"
        return "👁️👁️👁️ GOD EYE ACTIVATED! All techniques become visible! +30% copy chance!"

    def copy_technique(self, enemy_technique, target=None):
        """Copy an enemy technique with enhanced tracking"""
        # Track view count
        if enemy_technique in self.technique_view_count:
            self.technique_view_count[enemy_technique] += 1
        else:
            self.technique_view_count[enemy_technique] = 1

        # Check if already copied
        if enemy_technique in self.copied_techniques:
            # Update damage based on more views
            if enemy_technique in self.copied_techniques_data:
                old_data = self.copied_techniques_data[enemy_technique]
                new_views = self.technique_view_count[enemy_technique]

                # Increase damage based on additional views
                base_dmg = 60
                view_bonus = min(50, new_views * 5)  # Max +50 damage
                new_dmg = base_dmg + view_bonus

                # Update the ability
                key = old_data["key"]
                self.abilities[key]["dmg"] = (new_dmg, new_dmg + 30)
                self.abilities[key]["views"] = new_views
                self.abilities[key]["desc"] = f"Johan's copied {enemy_technique}. Seen {new_views} times, now dealing {new_dmg}-{new_dmg+30} damage."

                # Update stored data
                self.copied_techniques_data[enemy_technique]["views"] = new_views
                self.copied_techniques_data[enemy_technique]["damage"] = (new_dmg, new_dmg + 30)

                return f"🔄 {enemy_technique} improved! (Now seen {new_views} times, +{view_bonus} damage)"
            return f"Already copied {enemy_technique} (Seen {self.technique_view_count[enemy_technique]} times)"

        # Check copy limit
        if self.copy_count >= self.max_copy:
            return None

        # Copy new technique
        self.copied_techniques.append(enemy_technique)
        self.copy_count += 1

        # Calculate copied technique damage based on how many times seen
        base_dmg = 60
        view_bonus = min(50, self.technique_view_count[enemy_technique] * 5)  # +5 damage per view, max +50
        total_dmg = base_dmg + view_bonus

        # Add new ability slot dynamically
        new_key = str(10 + self.copy_count)
        self.abilities[new_key] = {
            "name": f"👁️ Copy: {enemy_technique}",
            "cost": 25,
            "dmg": (total_dmg, total_dmg + 30),
            "type": "damage",
            "views": self.technique_view_count[enemy_technique],
            "desc": f"Johan's God Eye copies {enemy_technique}. Seen {self.technique_view_count[enemy_technique]} time(s), dealing {total_dmg}-{total_dmg+30} damage."
        }

        # Store technique data
        self.copied_techniques_data[enemy_technique] = {
            "key": new_key,
            "views": self.technique_view_count[enemy_technique],
            "damage": (total_dmg, total_dmg + 30)
        }

        view_word = "time" if self.technique_view_count[enemy_technique] == 1 else "times"
        return f"✅ Johan copies {enemy_technique}! (Seen {self.technique_view_count[enemy_technique]} {view_word})"

    def calculate_copy_chance(self, technique_name, target, enemy_rank):
        """Calculate copy chance based on various factors"""
        chance = 0.3  # Base 30%
        factors = []

        # Factor 1: God Eye active = +30%
        if self.god_eye_active:
            chance += 0.3
            factors.append("God Eye active (+30%)")

        # Factor 2: Technique already seen before = +20% per subsequent view (max +60%)
        if technique_name in self.technique_view_count:
            view_bonus = min(0.6, self.technique_view_count[technique_name] * 0.2)
            if view_bonus > 0:
                chance += view_bonus
                factors.append(f"Seen {self.technique_view_count[technique_name]}x (+{int(view_bonus * 100)}%)")

        # Factor 3: Technique used on Johan directly = +40%
        if target == self:
            chance += 0.4
            factors.append("Direct hit (+40%)")

        # Factor 4: Johan below 50% HP = +20% (overcoming limits)
        if self.hp < self.max_hp * 0.5:
            chance += 0.2
            factors.append("Low HP (+20%)")

        # Factor 5: Technique is from a boss/unique enemy (rank < 20) = +10%
        if enemy_rank < 20:
            chance += 0.1
            factors.append("Boss technique (+10%)")

        # Cap at 90% max (never 100% for balance)
        chance = min(0.9, chance)

        return chance, factors

    def get_damage_multiplier(self):
        mult, buffs = super().get_damage_multiplier()
        if self.god_eye_active:
            mult *= 1.8
            buffs.append("👁️ GOD EYE")
        if self.blind:
            # Blindness gives +30% damage from overcoming
            mult *= 1.3
            buffs.append("🕶️ OVERCOMING BLINDNESS")

        # Additional multiplier based on number of copied techniques
        if self.copy_count > 0:
            technique_mastery = 1.0 + (self.copy_count * 0.02)  # +2% per copied technique
            mult *= technique_mastery
            buffs.append(f"📚 {self.copy_count} TECHNIQUES")

        return mult, buffs

    def get_copy_stats(self):
        """Display copy statistics"""
        print(f"\n📊 JOHAN'S COPY STATISTICS:")
        print(f"   • Techniques Copied: {self.copy_count}/{self.max_copy}")
        print(f"   • God Eye Active: {'✅' if self.god_eye_active else '❌'}")
        print(f"   • Blindness: {'✅' if self.blind else '❌'} (+30% damage)")
        print(f"\n   📖 COPIED TECHNIQUES:")
        for technique, data in self.copied_techniques_data.items():
            print(f"      • {technique}: Seen {data['views']}x | DMG: {data['damage'][0]}-{data['damage'][1]}")

        if self.technique_view_count:
            print(f"\n   👁️ TECHNIQUES OBSERVED:")
            for technique, views in self.technique_view_count.items():
                if technique not in self.copied_techniques:
                    print(f"      • {technique}: Seen {views}x (not copied yet)")


class Vasco(Character):
    def __init__(self):
        super().__init__("Vasco", "The Hero of Justice", 450, 260, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 1
        self.paths_available = [Path.VASCO_SYSTEMA, Path.VASCO_MUAY_THAI]
        self.abilities = {
            '1': {"name": "🇷🇺 Systema: Ryabina", "cost": 20, "dmg": (50, 70), "type": "damage",
                  "desc": "A Russian Systema technique. Vasco targets vital points with precise, fluid strikes learned from Sophia."},
            '2': {"name": "🇷🇺 Russian Cross", "cost": 35, "dmg": (75, 105), "type": "damage",
                  "desc": "A devastating Systema combination. Vasco crosses his opponents' defenses with brutal efficiency."},
            '3': {"name": "🇹🇭 Muay Thai: Death Blow", "cost": 40, "dmg": (90, 130), "type": "damage",
                  "desc": "Vasco's signature Muay Thai technique. A devastating elbow or knee strike that can end fights instantly."},
            '4': {"name": "👊 Sunken Fist", "cost": 30, "dmg": (70, 100), "type": "damage",
                  "desc": "The legendary fist that sank ships. Vasco's ultimate technique, born from his training with the Brekdak crew."}
        }


class JayHong(Character):
    def __init__(self):
        super().__init__("Jay Hong", "The Silent Blade", 380, 270, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 1
        self.paths_available = [Path.JAY_KALI]
        self.abilities = {
            '1': {"name": "🇷🇺 Systema: Neutralizer", "cost": 20, "dmg": (45, 65), "type": "damage",
                  "desc": "A Systema counter-technique. Jay neutralizes threats with silent, efficient movements."},
            '2': {"name": "🇵🇭 Kali: Double Baston", "cost": 25, "dmg": (50, 75), "type": "damage",
                  "desc": "Filipino Kali stick fighting. Jay wields twin weapons with deadly precision."},
            '3': {"name": "🇵🇭 Kali: Karambit", "cost": 30, "dmg": (65, 90), "type": "damage",
                  "desc": "The curved blade of Kali. Jay's strikes hook around defenses for devastating effect."},
            '4': {"name": "🛡️ Motorcycle Helmet", "cost": 15, "dmg": (0, 0), "type": "utility",
                  "desc": "Jay's signature defense. Using his helmet as a shield, he reduces damage by 50% this turn."}
        }


class EliJang(Character):
    def __init__(self):
        super().__init__("Eli Jang", "The Wild", 410, 260, [Realm.TECHNIQUE])
        self.canon_episode = 150
        self.paths_available = [Path.ELI_BEAST, Path.ELI_TOM_LEE]
        self.beast_mode = False
        self.beast_timer = 0
        self.abilities = {
            '1': {"name": "🐺 Wolf Strike", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Eli strikes like a wolf - sudden, savage, and aimed at vital points."},
            '2': {"name": "🦅 Talon Kick", "cost": 25, "dmg": (60, 85), "type": "damage",
                  "desc": "A kick like an eagle's talon. Eli's striking precision is almost animalistic."},
            '3': {"name": "🦁 Beast Mode", "cost": 45, "dmg": (0, 0), "type": "buff",
                  "desc": "Unleashing his inner beast. Eli's fighting becomes purely instinctual, increasing damage by 60% for 3 turns."},
            '4': {"name": "👴 Tom Lee Special", "cost": 40, "dmg": (85, 125), "type": "damage",
                  "desc": "The wild technique inherited from Tom Lee. Eli combines his beast style with the legendary wildness."}
        }

    def activate_beast_mode(self):
        self.beast_mode = True
        self.beast_timer = 3
        return "🦁🦁🦁 BEAST MODE! Eli abandons all technique for pure animal instinct! +60% damage!"

    def get_damage_multiplier(self):
        mult, buffs = super().get_damage_multiplier()
        if self.beast_mode:
            mult *= 1.6
            buffs.append("🦁 BEAST")
        return mult, buffs


class WarrenChae(Character):
    def __init__(self):
        super().__init__("Warren Chae", "Gangdong's Mighty", 390, 260, [Realm.STRENGTH])
        self.canon_episode = 277
        self.paths_available = [Path.WARREN_JKD, Path.WARREN_CQC, Path.WARREN_HEART]
        self.exhausted = False
        self.abilities = {
            '1': {"name": "🥋 Jeet Kune Do: Interception", "cost": 20, "dmg": (55, 80), "type": "damage",
                  "desc": "Bruce Lee's philosophy - intercepting the attack before it fully forms. Warren strikes as opponents commit."},
            '2': {"name": "🔫 CQC Foundation", "cost": 30, "dmg": (70, 100), "type": "damage",
                  "desc": "Close Quarters Combat fundamentals. Warren's training with Manager Kim shows in every precise movement."},
            '3': {"name": "⚡ NEW CQC: Full Release", "cost": 70, "dmg": (120, 170), "type": "damage",
                  "desc": "The complete CQC system. Warren unleashes everything he's learned in a devastating combination. Causes exhaustion."},
            '4': {"name": "💔 Heart Attack Punch", "cost": 60, "dmg": (110, 160), "type": "damage",
                  "desc": "The legendary one-inch punch. Warren generates massive force from zero distance, stopping hearts."}
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
                  "desc": "The will of Gapryong flows through his son. Jake taps into his father's legendary determination."},
            '3': {"name": "👑 Gapryong's Blood", "cost": 70, "dmg": (120, 180), "type": "damage",
                  "desc": "The power of his bloodline fully awakened. Jake strikes with the force of his heritage."},
            '4': {"name": "⚖️ Conviction Mode", "cost": 45, "dmg": (0, 0), "type": "buff",
                  "desc": "Entering a state of pure conviction. Jake's willpower increases his damage by 50% for 3 turns."}
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
                  "desc": "Gun's Taekwondo mastery. A spinning roundhouse kick delivered with perfect form and devastating power."},
            '2': {"name": "🥋 Kyokushin: Straight", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "The straight punch of Kyokushin Karate. Gun generates massive power from proper hip rotation."},
            '3': {"name": "🖤 Black Bone", "cost": 70, "dmg": (130, 200), "type": "damage",
                  "desc": "The legendary technique of the Yamazaki clan. Gun's ultimate move, passed down through generations."},
            '4': {"name": "👁️ Constant UI", "cost": 0, "dmg": (0, 0), "type": "passive",
                  "desc": "Gun exists in a state of perpetual Ultra Instinct. When below 50% HP, his damage increases by 50%."}
        }

    def get_damage_multiplier(self):
        mult, buffs = super().get_damage_multiplier()
        if self.permanent_ui and self.hp < self.max_hp * 0.5:
            mult *= 1.5
            buffs.append("👁️ UI AWAKENING")
        return mult, buffs


class GooKim(Character):
    def __init__(self):
        super().__init__("Goo Kim", "The Moonlight Sword", 480, 300, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 300
        self.paths_available = [Path.GOO_MOONLIGHT, Path.GOO_FIFTH]
        self.abilities = {
            '1': {"name": "🖊️ Pen Sword", "cost": 15, "dmg": (45, 70), "type": "damage",
                  "desc": "Goo's signature - using a pen as a sword. Even the humblest object becomes lethal in his hands."},
            '2': {"name": "🌙 First Sword: Early Moon", "cost": 30, "dmg": (75, 105), "type": "damage",
                  "desc": "The first form of Moonlight Sword. A rising crescent slash that catches opponents off guard."},
            '3': {"name": "🌓 Second Sword: Crescent Moon", "cost": 35, "dmg": (80, 115), "type": "damage",
                  "desc": "The second form. A sweeping horizontal slash that covers wide arcs."},
            '4': {"name": "🌕 Third Sword: Full Moon", "cost": 45, "dmg": (100, 145), "type": "damage",
                  "desc": "The third form. A complete circular motion that strikes from all directions."},
            '5': {"name": "🌑 Zero Sword: Lunar Eclipse", "cost": 60, "dmg": (130, 190), "type": "counter",
                  "desc": "The ultimate counter technique. Goo waits in perfect stillness, then strikes when the moon is darkest."},
            '6': {"name": "✨ Fifth Sword", "cost": 90, "dmg": (170, 250), "type": "damage",
                  "desc": "The legendary fifth sword - a technique that shouldn't exist. Goo transcends the limits of swordplay."}
        }


class KimJungu(Character):
    def __init__(self):
        super().__init__("Kim Jun-gu", "The Hwarang Sword", 520, 290, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 500
        self.paths_available = [Path.JOONGOO_HWARANG, Path.JOONGOO_ARMED]
        self.abilities = {
            '1': {"name": "🖊️ Pen Pierce", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "A pen becomes a deadly weapon. Jun-gu's precision allows him to pierce with any object."},
            '2': {"name": "🔗 Chain Whip", "cost": 30, "dmg": (75, 110), "type": "damage",
                  "desc": "Using a chain as a whip. Jun-gu's reach and unpredictability make him dangerous at any range."},
            '3': {"name": "⚔️ Hwarang Sword", "cost": 60, "dmg": (140, 210), "type": "damage",
                  "desc": "The ancient sword technique of the Hwarang. Jun-gu channels the spirit of Korea's legendary warriors."},
            '4': {"name": "⚔️ Hwarang: Blade Dance", "cost": 70, "dmg": (160, 240), "type": "damage",
                  "desc": "The ultimate Hwarang technique. A dance of blades that leaves no opening for counterattack."}
        }


class ManagerKim(Character):
    def __init__(self):
        super().__init__("Manager Kim", "The Senior Manager", 480, 300,
                         [Realm.TECHNIQUE, Realm.TENACITY, Realm.STRENGTH])
        self.canon_episode = 290
        self.code_66 = True
        self.veinous_rage = False
        self.silver_yarn_active = False
        self.paths_available = [Path.CAP_GUY_CQC]
        self.abilities = {
            '1': {"name": "🎖️ Special Forces Training", "cost": 0, "dmg": (0, 0), "type": "passive",
                  "desc": "Manager Kim's military background. Years of special forces training make him always combat-ready."},
            '2': {"name": "🔫 CQC: Vital Strikes", "cost": 25, "dmg": (65, 90), "type": "damage",
                  "desc": "Close Quarters Combat targeting vital points. Manager Kim ends fights with surgical precision."},
            '3': {"name": "⚪ Silver Yarn: Thread Bind", "cost": 20, "dmg": (0, 0), "type": "utility",
                  "desc": "Using silver yarn as a weapon. Manager Kim binds opponents with nearly invisible threads. 60% chance to immobilize."},
            '4': {"name": "66 CODE: Full Release", "cost": 70, "dmg": (130, 190), "type": "damage",
                  "desc": "The legendary Code 66 technique. Manager Kim's ultimate move, developed during his most dangerous missions."}
        }


# ===== WORKERS =====

class Mandeok(Character):
    def __init__(self):
        super().__init__("Mandeok", "The Titan", 480, 300, [Realm.STRENGTH])
        self.canon_episode = 400
        self.paths_available = [Path.MANDEOK_POWER]
        self.abilities = {
            '1': {"name": "💪 Power Punch", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "A punch backed by Mandeok's titanic strength. No technique, just overwhelming power."},
            '2': {"name": "🌍 Earth Shaker", "cost": 40, "dmg": (110, 160), "type": "damage",
                  "desc": "Mandeok strikes the ground, creating shockwaves that destabilize opponents."},
            '3': {"name": "🗿 Titan Strike", "cost": 50, "dmg": (130, 190), "type": "damage",
                  "desc": "The full power of the Titan. Mandeok unleashes everything in one devastating blow."}
        }


class CapGuy(Character):
    def __init__(self):
        super().__init__("Cap Guy", "The Senior Manager", 450, 320, [Realm.TECHNIQUE])
        self.canon_episode = 400
        self.paths_available = [Path.CAP_GUY_CQC]
        self.abilities = {
            '1': {"name": "🔫 CQC: Foundation", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "The fundamentals of Close Quarters Combat. Cap Guy's strikes are precise and efficient."},
            '2': {"name": "⚪ Silver Yarn", "cost": 20, "dmg": (0, 0), "type": "utility",
                  "desc": "Cap Guy's signature weapon. Silver yarn threads bind and cut, immobilizing opponents."},
            '3': {"name": "66 CODE", "cost": 70, "dmg": (140, 200), "type": "damage",
                  "desc": "The legendary technique. Cap Guy unleashes his full potential in a devastating combination."}
        }


class Xiaolung(Character):
    def __init__(self):
        super().__init__("Xiaolung", "Muay Thai Genius", 440, 280, [Realm.SPEED, Realm.STRENGTH])
        self.canon_episode = 400
        self.paths_available = [Path.XIAOLUNG_MUAY_THAI]
        self.abilities = {
            '1': {"name": "🇹🇭 Muay Thai: Elbow", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "The sharpest weapon in Muay Thai. Xiaolung's elbow strikes can cut opponents like blades."},
            '2': {"name": "🇹🇭 Muay Thai: Knee", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Devastating knee strikes in the clinch. Xiaolung dominates at close range."},
            '3': {"name": "🇹🇭 Thai Clinch", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "The Muay Thai clinch. Xiaolung controls opponents while delivering brutal knees."},
            '4': {"name": "🇹🇭 Muay Thai Mastery", "cost": 50, "dmg": (130, 180), "type": "damage",
                  "desc": "The complete Muay Thai arsenal. Xiaolung combines elbows, knees, and kicks in a devastating flurry."}
        }


class Ryuhei(Character):
    def __init__(self):
        super().__init__("Ryuhei", "Yakuza Executive", 430, 270, [Realm.TECHNIQUE])
        self.canon_episode = 400
        self.paths_available = [Path.RYUHEI_YAKUZA]
        self.abilities = {
            '1': {"name": "⚔️ Yakuza Strike", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Dirty, effective street fighting. Ryuhei fights like a true yakuza - no rules, only victory."},
            '2': {"name": "🏴 Gang Style", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "The fighting style of organized crime. Ryuhei uses group tactics even when alone."},
            '3': {"name": "⚫ Yamazaki Blood", "cost": 40, "dmg": (120, 170), "type": "damage",
                  "desc": "The dark heritage of the Yamazaki clan flows in his veins. Ryuhei taps into that power."}
        }


class SamuelSeo(Character):
    def __init__(self):
        super().__init__("Samuel Seo", "The Betrayer", 460, 290, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 300
        self.paths_available = [Path.SAMUEL_AMBITION]
        self.abilities = {
            '1': {"name": "👑 King's Ambition", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "Samuel's burning desire to be king fuels his attacks. Each strike carries his ambition."},
            '2': {"name": "💢 Betrayal", "cost": 25, "dmg": (80, 120), "type": "damage",
                  "desc": "A cheap shot born from betrayal. Samuel strikes when opponents least expect it."},
            '3': {"name": "⚡ Workers Executive", "cost": 40, "dmg": (120, 170), "type": "damage",
                  "desc": "The power of a Workers executive. Samuel's position gives him confidence and strength."},
            '4': {"name": "👑 Path to Kingship", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "Samuel's ultimate technique. He pours all his ambition into one devastating strike."}
        }


class SinuHan(Character):
    def __init__(self):
        super().__init__("Sinu Han", "The Ghost", 420, 280, [Realm.SPEED, Realm.TECHNIQUE])
        self.canon_episode = 300
        self.paths_available = [Path.SINU_INVISIBLE]
        self.abilities = {
            '1': {"name": "🌀 Invisible Punch", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "desc": "A punch that can't be seen. Sinu's speed makes his strikes appear from nowhere."},
            '2': {"name": "🌀 Invisible Kick", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "desc": "An invisible kick combining speed and technique. Sinu's legs are as deadly as his hands."},
            '3': {"name": "🌀 Ghost Fist", "cost": 45, "dmg": (120, 170), "type": "damage",
                  "desc": "The ultimate invisible attack. Sinu strikes from all angles simultaneously, like a ghost."}
        }


class LoganLee(Character):
    def __init__(self):
        super().__init__("Logan Lee", "The Bully", 350, 220, [])
        self.canon_episode = 1
        self.paths_available = [Path.LOGAN_BULLY]
        self.abilities = {
            '1': {"name": "👊 Bully Punch", "cost": 20, "dmg": (50, 80), "type": "damage",
                  "desc": "A bully's punch - meant to intimidate more than injure. Still hurts, though."},
            '2': {"name": "😤 Intimidation", "cost": 15, "dmg": (0, 0), "type": "utility",
                  "desc": "Logan uses his size and reputation to intimidate. 40% chance to stun the target."},
            '3': {"name": "💢 Cheap Shot", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Logan's specialty. A dirty, underhanded strike when opponents aren't looking."}
        }


# ===== CHEONLIANG =====

class VinJin(Character):
    def __init__(self):
        super().__init__("Vin Jin", "Ssireum Genius", 440, 270, [Realm.STRENGTH])
        self.canon_episode = 500
        self.paths_available = [Path.VIN_JIN_SSIREUM]
        self.abilities = {
            '1': {"name": "🇰🇷 Ssireum: Throw", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Traditional Korean wrestling throw. Vin Jin uses leverage and technique to slam opponents."},
            '2': {"name": "🇰🇷 Ssireum: Grapple", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "A powerful grappling technique. Vin Jin controls opponents with his wrestling background."},
            '3': {"name": "🥋 Judo: Ippon", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "A perfect Judo throw. Vin Jin incorporates other grappling arts into his ssireum base."},
            '4': {"name": "🥋 Kudo: Dirty Boxing", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "The dirty boxing of Kudo. Vin Jin strikes in the clinch with brutal efficiency."},
            '5': {"name": "🕶️ Sunglasses Off", "cost": 50, "dmg": (140, 190), "type": "damage",
                  "desc": "Vin Jin removes his sunglasses - a sign he's serious. His true power emerges."}
        }


class HanJaeha(Character):
    def __init__(self):
        super().__init__("Han Jaeha", "Cheonliang Wrestler", 380, 240, [Realm.STRENGTH])
        self.canon_episode = 500
        self.paths_available = [Path.HAN_JAEHA]
        self.abilities = {
            '1': {"name": "🤼 Traditional Throw", "cost": 20, "dmg": (60, 90), "type": "damage",
                  "desc": "A classic ssireum throw. Han Jaeha honors the traditions of Korean wrestling."},
            '2': {"name": "🤼 Grapple Lock", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "A controlling grapple. Han Jaeha locks opponents down with his wrestling skills."},
            '3': {"name": "🤼 Cheonliang Pride", "cost": 35, "dmg": (100, 140), "type": "damage",
                  "desc": "The pride of Cheonliang. Han Jaeha fights for his hometown with everything he has."}
        }


class BaekSeong(Character):
    def __init__(self):
        super().__init__("Baek Seong", "Taekkyon Dancer", 370, 250, [Realm.SPEED, Realm.TECHNIQUE])
        self.canon_episode = 500
        self.paths_available = [Path.BAEK_SEONG_TAEKKYON]
        self.abilities = {
            '1': {"name": "🦢 Flowing Step", "cost": 20, "dmg": (50, 80), "type": "damage",
                  "desc": "The graceful footwork of Taekkyon. Baek Seong flows like water, striking from unexpected angles."},
            '2': {"name": "🦢 Taekkyon Kick", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "A traditional Taekkyon kick. Fluid, deceptive, and surprisingly powerful."},
            '3': {"name": "🦢 Dance of Blades", "cost": 40, "dmg": (110, 150), "type": "damage",
                  "desc": "Taekkyon's ultimate form. Baek Seong dances through opponents, each step a strike."}
        }


# ===== YAMAZAKI =====

class ShingenYamazaki(Character):
    def __init__(self):
        super().__init__("Shingen Yamazaki", "Yamazaki Head", 650, 380,
                         [Realm.STRENGTH, Realm.TENACITY, Realm.TECHNIQUE, Realm.OVERCOMING])
        self.canon_episode = 0
        self.paths_available = [Path.SHINGEN_YAMAZAKI]
        self.abilities = {
            '1': {"name": "🏯 Yamazaki Style", "cost": 40, "dmg": (130, 180), "type": "damage",
                  "desc": "The fundamental techniques of the Yamazaki clan. Shingen demonstrates why his family is feared."},
            '2': {"name": "🏯 Syndicate's Wrath", "cost": 55, "dmg": (170, 220), "type": "damage",
                  "desc": "The collective fury of the Yamazaki Syndicate. Shingen channels generations of darkness."},
            '3': {"name": "🏯 Black Bone", "cost": 70, "dmg": (210, 270), "type": "damage",
                  "desc": "The legendary technique of the Yamazaki head. A devastating strike that carries the clan's legacy."},
            '4': {"name": "🏯 Inherited Darkness", "cost": 85, "dmg": (250, 320), "type": "damage",
                  "desc": "The ultimate Yamazaki technique. Shingen unleashes the full power of his bloodline."}
        }


class ParkFather(Character):
    def __init__(self):
        super().__init__("Park Jonggun's Father", "The Mystery", 550, 340,
                         [Realm.STRENGTH, Realm.TECHNIQUE])
        self.canon_episode = 0
        self.paths_available = [Path.PARK_FATHER]
        self.abilities = {
            '1': {"name": "❓ Unknown Technique", "cost": 35, "dmg": (110, 160), "type": "damage",
                  "desc": "A mysterious technique lost to time. The source of Gun's power remains shrouded in mystery."},
            '2': {"name": "❓ Bloodline Secret", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "The secret of the Park bloodline. A technique passed from father to son."},
            '3': {"name": "❓ Father's Shadow", "cost": 65, "dmg": (190, 250), "type": "damage",
                  "desc": "The shadow of the father looms large. A technique that Gun would later inherit and perfect."}
        }


# ===== LAW ENFORCEMENT =====

class KimMinjae(Character):
    def __init__(self):
        super().__init__("Kim Minjae", "Police Officer", 380, 240, [Realm.TECHNIQUE])
        self.canon_episode = 200
        self.paths_available = [Path.KIM_MINJAE_JUDO]
        self.abilities = {
            '1': {"name": "🥋 Judo Throw", "cost": 20, "dmg": (50, 80), "type": "damage",
                  "desc": "A clean Judo throw. Kim Minjae uses an opponent's momentum against them, just like in training."},
            '2': {"name": "🥋 Ippon Seoi Nage", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "desc": "The one-arm shoulder throw. A classic Judo technique executed with police precision."},
            '3': {"name": "🥋 Police Training", "cost": 35, "dmg": (90, 130), "type": "damage",
                  "desc": "Years of police training culminate in this technique. Law and order brought to the streets."}
        }


class DetectiveKang(Character):
    def __init__(self):
        super().__init__("Detective Kang", "Veteran Detective", 390, 250, [Realm.SPEED])
        self.canon_episode = 200
        self.paths_available = [Path.DETECTIVE_KANG_BOXING]
        self.abilities = {
            '1': {"name": "🥊 Detective's Jab", "cost": 20, "dmg": (50, 80), "type": "damage",
                  "desc": "A quick jab honed through years of street work. Detective Kang uses it to keep criminals at bay."},
            '2': {"name": "🥊 Veteran Cross", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "desc": "A powerful cross backed by decades of experience. Detective Kang's veteran instincts guide every punch."},
            '3': {"name": "🥊 Experience Counts", "cost": 35, "dmg": (100, 140), "type": "damage",
                  "desc": "Years on the force have taught him well. Detective Kang's experience makes every strike count."}
        }


# ============================================================================
# ENEMY CREATION FUNCTIONS - ALL WITH PROPER ENERGY COSTS AND DESCRIPTIONS
# ============================================================================

def create_enemy_frame_soldier():
    abilities = {
        '1': {"name": "Fist Strike", "dmg": (25, 40), "cost": 15,
              "desc": "A basic punch from a Frame soldier. Unrefined but dangerous in numbers."}
    }
    enemy = Enemy("Frame Soldier", "Elite Grunt", 150, 100, abilities, 100, "Frame")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_jhigh_bully():
    abilities = {
        '1': {"name": "School Punch", "dmg": (20, 35), "cost": 10,
              "desc": "A bully's punch - meant to intimidate more than injure. Still hurts, though."}
    }
    enemy = Enemy("J High Bully", "School Thug", 100, 80, abilities, 120, "J High")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_logan_lee():
    abilities = {
        '1': {"name": "Bully Punch", "dmg": (35, 55), "cost": 20,
              "desc": "Logan's bullying style. A heavy punch meant to establish dominance."},
        '2': {"name": "Intimidation", "dmg": (30, 50), "cost": 15,
              "desc": "Logan uses his size to intimidate. May stun weaker opponents."},
        '3': {"name": "Cheap Shot", "dmg": (40, 65), "cost": 25,
              "desc": "Logan's specialty. A dirty strike when you least expect it."}
    }
    enemy = Enemy("Logan Lee", "The Bully", 300, 180, abilities, 85, "Independent")
    enemy.ai_pattern = ['3', '1', '2']
    return enemy


def create_enemy_zack_lee():
    abilities = {
        '1': {"name": "Jab", "dmg": (35, 55), "cost": 15,
              "desc": "A lightning-fast jab. Zack uses it to measure distance and set up heavier strikes."},
        '2': {"name": "Cross", "dmg": (45, 70), "cost": 20,
              "desc": "A powerful cross punch. Zack puts his full body weight behind this strike."},
        '3': {"name": "Counter", "dmg": (60, 85), "cost": 30,
              "desc": "Zack's specialty. He waits for the opponent to commit, then strikes with perfect timing."}
    }
    enemy = Enemy("Zack Lee", "The Iron Boxer", 380, 280, abilities, 35, "J High")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_vasco_enemy():
    abilities = {
        '1': {"name": "Systema Strike", "dmg": (50, 70), "cost": 20,
              "desc": "A Russian Systema technique. Vasco targets vital points with precise, fluid movements."},
        '2': {"name": "Sunken Fist", "dmg": (70, 100), "cost": 30,
              "desc": "The legendary fist that sank ships. Vasco's ultimate technique."},
        '3': {"name": "Run Over", "dmg": (65, 95), "cost": 25,
              "desc": "Vasco charges forward like a truck. His determination is unstoppable."}
    }
    enemy = Enemy("Vasco", "The Hero", 450, 260, abilities, 30, "Burn Knuckles")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jay_hong_enemy():
    abilities = {
        '1': {"name": "Systema", "dmg": (45, 65), "cost": 20,
              "desc": "Silent, efficient Systema techniques. Jay neutralizes threats quietly."},
        '2': {"name": "Kali", "dmg": (50, 75), "cost": 25,
              "desc": "Filipino Kali knife fighting. Jay's blade work is precise and deadly."}
    }
    enemy = Enemy("Jay Hong", "The Silent", 380, 270, abilities, 40, "J High")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_johan_seong_enemy():
    """Johan Seong as an enemy - Manhwa accurate"""
    abilities = {
        '1': {"name": "👁️ Copy: Taekwondo", "dmg": (50, 75), "cost": 20,
              "desc": "Perfect Taekwondo copied by the God Eye. Spinning kicks with flawless form."},
        '2': {"name": "👁️ Copy: Boxing", "dmg": (50, 75), "cost": 20,
              "desc": "World-class boxing technique. Jabs and crosses executed with mechanical precision."},
        '3': {"name": "👁️ Copy: Karate", "dmg": (50, 75), "cost": 20,
              "desc": "Traditional Karate strikes. Powerful, linear techniques."},
        '4': {"name": "💃 Choreography: God Dog", "dmg": (85, 120), "cost": 40,
              "desc": "Johan's original style - dance combat. A deadly performance."},
        '5': {"name": "👁️ God Eye", "dmg": (95, 140), "cost": 45,
              "desc": "The God Eye awakens. Johan sees everything, countering perfectly."}
    }
    enemy = Enemy("Johan Seong", "The God Eye", 400, 300, abilities, 15, "God Dog")
    enemy.ai_pattern = ['5', '4', '3', '2', '1']
    # Add blindness passive
    enemy.blind = True
    return enemy


def create_enemy_eli_jang_enemy():
    abilities = {
        '1': {"name": "Animal Strike", "dmg": (50, 75), "cost": 20,
              "desc": "Eli strikes like a wild animal - unpredictable and savage."},
        '2': {"name": "Talon Kick", "dmg": (60, 85), "cost": 25,
              "desc": "A kick like an eagle's talon. Eli's precision is almost animalistic."},
        '3': {"name": "Beast Mode", "dmg": (85, 120), "cost": 45,
              "desc": "Eli unleashes his inner beast. His fighting becomes purely instinctual."}
    }
    enemy = Enemy("Eli Jang", "The Wild", 410, 260, abilities, 16, "Hostel")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_warren_chae_enemy():
    abilities = {
        '1': {"name": "JKD: Interception", "dmg": (60, 85), "cost": 20,
              "desc": "Jeet Kune Do interception. Warren strikes as opponents commit to attacks."},
        '2': {"name": "Shield Strike", "dmg": (65, 90), "cost": 25,
              "desc": "Using his shield as a weapon. Warren combines defense and offense."},
        '3': {"name": "Counter", "dmg": (70, 100), "cost": 30,
              "desc": "A perfectly timed counter. Warren's experience shows."},
        '4': {"name": "NEW CQC", "dmg": (90, 130), "cost": 70,
              "desc": "The complete CQC system. Warren's ultimate technique."}
    }
    enemy = Enemy("Warren Chae", "Hostel Executive", 390, 260, abilities, 30, "Hostel")
    enemy.ai_pattern = ['4', '3', '2', '1']
    return enemy


def create_enemy_jake_kim_enemy():
    abilities = {
        '1': {"name": "Conviction Punch", "dmg": (60, 85), "cost": 25,
              "desc": "A punch backed by pure conviction. Jake's willpower manifests in every strike."},
        '2': {"name": "Inherited Will", "dmg": (95, 140), "cost": 50,
              "desc": "The will of Gapryong flows through his son. Jake taps into legendary determination."},
        '3': {"name": "Gapryong's Blood", "dmg": (120, 180), "cost": 70,
              "desc": "The power of his bloodline fully awakened. Jake strikes with inherited force."}
    }
    enemy = Enemy("Jake Kim", "The Conviction", 430, 270, abilities, 12, "Big Deal")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jerry_kwon():
    abilities = {
        '1': {"name": "Gift Punch", "dmg": (65, 95), "cost": 30,
              "desc": "A gift from Jake - the strength to protect. Jerry's loyalty fuels his strikes."},
        '2': {"name": "Rhino Charge", "dmg": (70, 105), "cost": 35,
              "desc": "Jerry charges like a rhino - unstoppable and devastating."},
        '3': {"name": "Loyalty to Jake", "dmg": (80, 115), "cost": 40,
              "desc": "Jerry's unwavering loyalty makes him fight beyond his limits."}
    }
    enemy = Enemy("Jerry Kwon", "Big Deal Executive", 420, 250, abilities, 25, "Big Deal")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_sally():
    abilities = {
        '1': {"name": "Sally Special", "dmg": (45, 70), "cost": 20,
              "desc": "Sally's unique fighting style - unorthodox but effective."},
        '2': {"name": "Family Support", "dmg": (40, 65), "cost": 15,
              "desc": "Fighting for her family. Sally draws strength from her bonds."}
    }
    enemy = Enemy("Sally", "Hostel Manager", 320, 200, abilities, 60, "Hostel")
    enemy.ai_pattern = ['1', '2']
    return enemy


def create_enemy_brad():
    abilities = {
        '1': {"name": "Brad Punch", "dmg": (50, 75), "cost": 20,
              "desc": "A straightforward punch. Brad's strength is simple but effective."},
        '2': {"name": "Big Deal Loyalty", "dmg": (55, 80), "cost": 25,
              "desc": "Fighting for Big Deal. Brad's loyalty makes him push harder."}
    }
    enemy = Enemy("Brad", "Big Deal Member", 350, 220, abilities, 55, "Big Deal")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_jace_park():
    abilities = {
        '1': {"name": "Strategy", "dmg": (40, 60), "cost": 15,
              "desc": "Jace's strategic mind. He finds openings others miss."},
        '2': {"name": "Tactical Strike", "dmg": (45, 70), "cost": 20,
              "desc": "A strike planned with tactical precision. Jace thinks several moves ahead."}
    }
    enemy = Enemy("Jace Park", "Burn Knuckles Strategist", 330, 210, abilities, 58, "Burn Knuckles")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_burn_knuckles():
    abilities = {
        '1': {"name": "Burn Knuckle Punch", "dmg": (35, 55), "cost": 15,
              "desc": "A punch from a Burn Knuckles member. Fueled by their burning justice."},
        '2': {"name": "Justice Strike", "dmg": (40, 60), "cost": 20,
              "desc": "Striking for justice. Burn Knuckles members fight for what's right."}
    }
    enemy = Enemy("Burn Knuckles Member", "Hero Wannabe", 280, 180, abilities, 70, "Burn Knuckles")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_god_dog_member():
    abilities = {
        '1': {"name": "Fist Strike", "dmg": (25, 40), "cost": 15,
              "desc": "A basic fist strike. God Dog soldiers fight for their leader."}
    }
    enemy = Enemy("God Dog Member", "Crew Soldier", 140, 100, abilities, 100, "God Dog")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_god_dog_elite():
    abilities = {
        '1': {"name": "Power Strike", "dmg": (40, 60), "cost": 20,
              "desc": "A powerful strike from an elite God Dog member. More dangerous than regular soldiers."},
        '2': {"name": "Crew Combo", "dmg": (45, 65), "cost": 25,
              "desc": "A combination attack. God Dog elites fight as a unit."}
    }
    enemy = Enemy("God Dog Elite", "Crew Veteran", 200, 140, abilities, 75, "God Dog")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_hostel_member():
    abilities = {
        '1': {"name": "Street Fighting", "dmg": (35, 55), "cost": 20,
              "desc": "Dirty street fighting. Hostel members learned to fight in the streets."},
        '2': {"name": "Ambush", "dmg": (40, 60), "cost": 25,
              "desc": "Attacking from ambush. Hostel members use guerilla tactics."}
    }
    enemy = Enemy("Hostel Member", "Family Crew", 170, 120, abilities, 80, "Hostel")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_big_deal_member():
    abilities = {
        '1': {"name": "Fist Strike", "dmg": (30, 50), "cost": 15,
              "desc": "A basic fist strike. Big Deal soldiers fight for their family."},
        '2': {"name": "Loyalty", "dmg": (0, 0), "cost": 10, "type": "buff",
              "desc": "Loyalty to Big Deal. The soldier fights harder for his crew."}
    }
    enemy = Enemy("Big Deal Member", "Crew Soldier", 180, 130, abilities, 78, "Big Deal")
    enemy.ai_pattern = ['1', '2']
    return enemy


def create_enemy_workers_member():
    abilities = {
        '1': {"name": "Corporate Strike", "dmg": (35, 55), "cost": 20,
              "desc": "A strike backed by corporate power. Workers members are well-trained."}
    }
    enemy = Enemy("Workers Member", "Corporate Soldier", 160, 110, abilities, 90, "Workers")
    enemy.ai_pattern = ['1']
    return enemy


def create_enemy_workers_affiliate():
    abilities = {
        '1': {"name": "Affiliate Technique", "dmg": (60, 85), "cost": 25,
              "desc": "Techniques from a Workers affiliate. Each affiliate has unique skills."},
        '2': {"name": "Corporate Power", "dmg": (65, 95), "cost": 30,
              "desc": "The full power of Workers backing this affiliate."}
    }
    enemy = Enemy("Workers Affiliate", "1st Affiliate", 360, 230, abilities, 42, "Workers")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_eugene():
    abilities = {
        '1': {"name": "Corporate Strategy", "dmg": (30, 50), "cost": 20,
              "desc": "Eugene's strategic mind. He finds weaknesses in any plan."},
        '2': {"name": "Workers' Orders", "dmg": (35, 55), "cost": 25,
              "desc": "Issuing orders as the head of Workers. Eugene commands respect."}
    }
    enemy = Enemy("Eugene", "Workers Executive", 300, 250, abilities, 65, "Workers")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_xiaolung():
    abilities = {
        '1': {"name": "🇹🇭 Muay Thai: Elbow", "dmg": (80, 120), "cost": 30,
              "desc": "The sharpest weapon in Muay Thai. Xiaolung's elbow strikes can cut like blades."},
        '2': {"name": "🇹🇭 Muay Thai: Knee", "dmg": (85, 125), "cost": 30,
              "desc": "Devastating knee strikes. Xiaolung dominates at close range."},
        '3': {"name": "🇹🇭 Thai Clinch", "dmg": (75, 110), "cost": 25,
              "desc": "The Muay Thai clinch. Xiaolung controls opponents while delivering brutal knees."},
        '4': {"name": "🇹🇭 Muay Thai Mastery", "dmg": (110, 170), "cost": 50,
              "desc": "The complete Muay Thai arsenal. Xiaolung's ultimate technique."}
    }
    enemy = Enemy("Xiaolung", "Muay Thai Genius", 550, 300, abilities, 14, "Workers")
    enemy.ai_pattern = ['4', '1', '2', '3']
    return enemy


def create_enemy_mandeok():
    abilities = {
        '1': {"name": "💪 Power Punch", "dmg": (90, 130), "cost": 35,
              "desc": "A punch backed by titanic strength. Mandeok's raw power is overwhelming."},
        '2': {"name": "🌍 Earth Shaker", "dmg": (100, 150), "cost": 40,
              "desc": "Mandeok strikes the ground, creating shockwaves that destabilize opponents."},
        '3': {"name": "🗿 Titan Strike", "dmg": (120, 180), "cost": 50,
              "desc": "The full power of the Titan. Mandeok's ultimate technique."}
    }
    enemy = Enemy("Mandeok", "The Titan", 600, 280, abilities, 13, "Workers")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_vin_jin():
    abilities = {
        '1': {"name": "🇰🇷 Ssireum: Throw", "dmg": (75, 110), "cost": 30,
              "desc": "Traditional Korean wrestling throw. Vin Jin uses leverage to slam opponents."},
        '2': {"name": "🇰🇷 Ssireum: Grapple", "dmg": (70, 105), "cost": 30,
              "desc": "A powerful grappling technique. Vin Jin controls opponents with wrestling."},
        '3': {"name": "🥋 Judo: Ippon", "dmg": (80, 115), "cost": 35,
              "desc": "A perfect Judo throw. Vin Jin incorporates other grappling arts."},
        '4': {"name": "🥋 Kudo: Dirty Boxing", "dmg": (85, 120), "cost": 35,
              "desc": "The dirty boxing of Kudo. Vin Jin strikes in the clinch."},
        '5': {"name": "🕶️ Sunglasses Off", "dmg": (110, 160), "cost": 50,
              "desc": "Vin Jin removes his sunglasses. His true power emerges."}
    }
    enemy = Enemy("Vin Jin", "Ssireum Genius", 520, 280, abilities, 28, "Workers")
    enemy.ai_pattern = ['5', '4', '3', '2', '1']
    return enemy


def create_enemy_ryuhei():
    abilities = {
        '1': {"name": "⚔️ Yakuza Strike", "dmg": (80, 115), "cost": 30,
              "desc": "Dirty, effective street fighting. Ryuhei fights like a true yakuza."},
        '2': {"name": "🏴 Gang Style", "dmg": (85, 120), "cost": 35,
              "desc": "The fighting style of organized crime. Ryuhei uses group tactics."},
        '3': {"name": "⚫ Yamazaki Blood", "dmg": (100, 150), "cost": 45,
              "desc": "The dark heritage of the Yamazaki clan flows in his veins."}
    }
    enemy = Enemy("Ryuhei", "Yakuza Executive", 540, 290, abilities, 24, "Workers")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_samuel_seo():
    abilities = {
        '1': {"name": "👑 King's Ambition", "dmg": (85, 125), "cost": 35,
              "desc": "Samuel's burning desire to be king fuels his attacks."},
        '2': {"name": "💢 Betrayal", "dmg": (80, 120), "cost": 30,
              "desc": "A cheap shot born from betrayal. Samuel strikes unexpectedly."},
        '3': {"name": "⚡ Workers Executive", "dmg": (95, 140), "cost": 40,
              "desc": "The power of a Workers executive. Samuel's position gives him strength."},
        '4': {"name": "👑 Path to Kingship", "dmg": (110, 170), "cost": 50,
              "desc": "Samuel's ultimate technique. All his ambition in one strike."}
    }
    enemy = Enemy("Samuel Seo", "The Betrayer", 560, 300, abilities, 18, "Workers")
    enemy.ai_pattern = ['4', '3', '1', '2']
    return enemy


def create_enemy_taesoo_ma():
    abilities = {
        '1': {"name": "🔴 Right Hand", "dmg": (110, 170), "cost": 45,
              "desc": "Taesoo's legendary right fist. Pure, overwhelming power."},
        '2': {"name": "🔴 Ansan King", "dmg": (120, 180), "cost": 50,
              "desc": "The pride of Ansan. Taesoo's ultimate strike as king."}
    }
    enemy = Enemy("Taesoo Ma", "King of Ansan", 580, 300, abilities, 8, "1st Gen")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_gongseob_ji():
    abilities = {
        '1': {"name": "🩷 Speed Technique", "dmg": (95, 140), "cost": 40,
              "desc": "Blazing fast strikes. Gongseob's speed is his greatest asset."},
        '2': {"name": "🩷 Vice King", "dmg": (100, 150), "cost": 45,
              "desc": "The pride of the Vice King. Gongseob's ultimate technique."}
    }
    enemy = Enemy("Gongseob Ji", "Vice King", 500, 280, abilities, 11, "1st Gen")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_jichang_kwak():
    abilities = {
        '1': {"name": "🩷 Hand Blade", "dmg": (100, 155), "cost": 40,
              "desc": "Jichang's signature technique. His hand becomes a blade."},
        '2': {"name": "👑 Seoul King", "dmg": (110, 170), "cost": 50,
              "desc": "The pride of Seoul's king. Jichang's ultimate strike."}
    }
    enemy = Enemy("Jichang Kwak", "King of Seoul", 550, 300, abilities, 7, "1st Gen")
    enemy.ai_pattern = ['2', '1']
    return enemy


def create_enemy_gun_park_enemy():
    abilities = {
        '1': {"name": "Taekwondo", "dmg": (65, 90), "cost": 25,
              "desc": "Gun's Taekwondo mastery. Spinning kicks with perfect form."},
        '2': {"name": "Kyokushin", "dmg": (70, 100), "cost": 30,
              "desc": "Kyokushin Karate. Gun generates massive power from hip rotation."},
        '3': {"name": "Black Bone", "dmg": (130, 200), "cost": 70,
              "desc": "The legendary Yamazaki technique. Gun's ultimate move."}
    }
    enemy = Enemy("Gun Park", "Legend of Gen 1", 500, 320, abilities, 5, "Independent")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_goo_kim_enemy():
    abilities = {
        '1': {"name": "Makeshift Sword", "dmg": (45, 70), "cost": 20,
              "desc": "Goo's signature - using anything as a sword. Even a pen becomes lethal."},
        '2': {"name": "Full Moon", "dmg": (100, 145), "cost": 45,
              "desc": "The third form of Moonlight Sword. A complete circular motion."},
        '3': {"name": "Fifth Sword", "dmg": (170, 250), "cost": 90,
              "desc": "The legendary fifth sword. A technique that shouldn't exist."}
    }
    enemy = Enemy("Goo Kim", "The Moonlight Sword", 480, 300, abilities, 5, "Independent")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_kim_jungu_enemy():
    abilities = {
        '1': {"name": "Improvised Weapon", "dmg": (70, 100), "cost": 30,
              "desc": "Jun-gu uses anything as a weapon. His creativity is deadly."},
        '2': {"name": "Hwarang Sword", "dmg": (140, 210), "cost": 60,
              "desc": "The ancient sword technique of the Hwarang."},
        '3': {"name": "Blade Dance", "dmg": (160, 240), "cost": 70,
              "desc": "The ultimate Hwarang technique. A dance of blades."}
    }
    enemy = Enemy("Kim Jun-gu", "The Hwarang Sword", 520, 290, abilities, 4, "Independent")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_manager_kim_enemy():
    abilities = {
        '1': {"name": "CQC Strike", "dmg": (65, 90), "cost": 25,
              "desc": "Close Quarters Combat. Manager Kim's strikes are precise and efficient."},
        '2': {"name": "Silver Yarn", "dmg": (100, 140), "cost": 20, "type": "utility",
              "desc": "Using silver yarn as a weapon. Binds and cuts opponents."},
        '3': {"name": "66 CODE", "dmg": (130, 190), "cost": 70,
              "desc": "The legendary Code 66 technique. Manager Kim's ultimate move."}
    }
    enemy = Enemy("Manager Kim", "The Senior Manager", 480, 300, abilities, 5, "White Tiger")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jinrang_enemy():
    abilities = {
        '1': {"name": "Jinrang's Conviction", "dmg": (130, 190), "cost": 50,
              "desc": "The conviction of Gapryong's disciple. Jinrang's strikes carry his master's legacy."},
        '2': {"name": "Busan King", "dmg": (140, 210), "cost": 55,
              "desc": "The authority of Busan's king. Jinrang commands respect."},
        '3': {"name": "True Conviction", "dmg": (170, 250), "cost": 70,
              "desc": "The ultimate expression of his faith in Gapryong's teachings."}
    }
    enemy = Enemy("Jinrang", "King of Busan", 750, 380, abilities, 2, "Busan")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_jaegyeon_na_enemy():
    abilities = {
        '1': {"name": "Incheon Speed", "dmg": (100, 150), "cost": 40,
              "desc": "The speed of Incheon's king. Jaegyeon moves faster than the eye can track."},
        '2': {"name": "Betrayal", "dmg": (95, 145), "cost": 35,
              "desc": "A strike born from betrayal. Jaegyeon's true nature revealed."},
        '3': {"name": "Faster Than Light", "dmg": (150, 230), "cost": 60,
              "desc": "Speed approaching the absolute limit. Jaegyeon's ultimate technique."}
    }
    enemy = Enemy("Jaegyeon Na", "King of Incheon", 620, 350, abilities, 6, "Busan")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_charles_choi():
    abilities = {
        '1': {"name": "🎭 Puppet Master", "dmg": (90, 140), "cost": 35,
              "desc": "Charles manipulates the battlefield like a puppet master."},
        '2': {"name": "🏛️ Chairman's Authority", "dmg": (110, 170), "cost": 45,
              "desc": "The authority of HNH Group's chairman. A devastating strike."},
        '3': {"name": "👤 HNH Group", "dmg": (100, 160), "cost": 40,
              "desc": "The power of his organization backing every move."},
        '4': {"name": "🎭 Truth of Two Bodies", "dmg": (130, 200), "cost": 60,
              "desc": "The secret technique behind the two bodies mystery. Charles's ultimate move."}
    }
    enemy = Enemy("Charles Choi", "The Puppet Master", 650, 350, abilities, 3, "HNH Chairman")
    enemy.ai_pattern = ['4', '3', '2', '1']
    return enemy


def create_enemy_tom_lee():
    abilities = {
        '1': {"name": "🐅 Wild Strike", "dmg": (100, 150), "cost": 35,
              "desc": "A primal, untamed strike. Tom Lee fights like a wild animal."},
        '2': {"name": "🐅 Tom Lee Special", "dmg": (120, 180), "cost": 45,
              "desc": "His signature move. Biting, clawing, and striking combined."},
        '3': {"name": "🐅 Gen 0 Power", "dmg": (140, 210), "cost": 55,
              "desc": "Raw power from the legendary era. A reminder of why Tom Lee was feared."}
    }
    enemy = Enemy("Tom Lee", "The Wild", 650, 350, abilities, 5, "Gen 0")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


def create_enemy_gapryong_kim():
    abilities = {
        '1': {"name": "👑 Conviction of the Strongest", "dmg": (120, 180), "cost": 45,
              "desc": "The conviction that made him the strongest. Gapryong's will manifests."},
        '2': {"name": "👑 Gapryong's Fist", "dmg": (150, 220), "cost": 55,
              "desc": "The legendary fist that defeated the Yamazaki Syndicate."},
        '3': {"name": "👑 Will to Protect", "dmg": (130, 200), "cost": 50,
              "desc": "A technique born from Gapryong's desire to protect his crew."},
        '4': {"name": "👑 Legend's Legacy", "dmg": (180, 280), "cost": 70,
              "desc": "The accumulated power of a legend. Gapryong's ultimate technique."}
    }
    enemy = Enemy("Gapryong Kim", "The Strongest", 800, 400, abilities, 0, "Gen 0 Legend")
    enemy.ai_pattern = ['4', '2', '3', '1']
    return enemy


def create_enemy_cheon_shinmyeong():
    abilities = {
        '1': {"name": "🔮 Dark Exorcism", "dmg": (90, 140), "cost": 35,
              "desc": "Dark shamanistic powers. Cheon Shin-myeong's exorcism techniques are deadly."},
        '2': {"name": "🔮 Cheonliang Rule", "dmg": (100, 150), "cost": 40,
              "desc": "The rule of Cheonliang. The shaman's authority manifested."},
        '3': {"name": "🔮 Puppeteer", "dmg": (80, 120), "cost": 30,
              "desc": "Controlling others like puppets. The shaman's true nature."}
    }
    enemy = Enemy("Cheon Shin-myeong", "The Shaman", 480, 320, abilities, 0, "Cheonliang")
    enemy.ai_pattern = ['3', '2', '1']
    return enemy


# ============================================================================
# FIXED GAME CLASS WITH ENHANCED JOHAN COPY MECHANICS
# ============================================================================

class LookismGame:
    def __init__(self, load_saved=True):
        # Initialize all characters
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

        # Gen 0
        self.gapryong = GapryongKim()
        self.tom_lee = TomLee()
        self.charles_choi = CharlesChoi()
        self.jinyoung = JinyoungPark()
        self.baekho = Baekho()

        # 1st Gen Kings
        self.james_lee = JamesLee()
        self.gitae = GitaeKim()
        self.jichang = JichangKwak()
        self.taesoo = TaesooMa()
        self.gongseob = GongseobJi()
        self.seokdu = SeokduWang()
        self.jaegyeon = JaegyeonNa()
        self.seongji = SeongjiYuk()
        self.jinrang = Jinrang()

        # Workers
        self.mandeok = Mandeok()
        self.cap_guy = CapGuy()
        self.xiaolung = Xiaolung()
        self.ryuhei = Ryuhei()
        self.samuel = SamuelSeo()
        self.sinu = SinuHan()
        self.logan = LoganLee()

        # Cheonliang
        self.vin_jin = VinJin()
        self.han_jaeha = HanJaeha()
        self.baek_seong = BaekSeong()

        # Yamazaki
        self.shingen = ShingenYamazaki()
        self.park_father = ParkFather()

        # Law Enforcement
        self.kim_minjae = KimMinjae()
        self.detective_kang = DetectiveKang()

        # ALL PLAYABLE CHARACTERS (51 total)
        self.all_characters = self.compile_all_characters()

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

        # Load saved game if requested (only once)
        if load_saved:
            loaded = self.load_game()
            if loaded:
                print("✅ Game loaded successfully!")
            else:
                print("🆕 Starting new game...")

    def compile_all_characters(self):
        """Compile all characters into a single list"""
        return [
            # Gen 0
            self.gapryong, self.tom_lee, self.charles_choi, self.jinyoung, self.baekho,
            # 1st Gen
            self.james_lee, self.gitae, self.jichang, self.taesoo, self.gongseob,
            self.seokdu, self.jaegyeon, self.seongji, self.jinrang,
            # Workers
            self.mandeok, self.cap_guy, self.xiaolung, self.ryuhei, self.samuel,
            self.sinu, self.logan,
            # Cheonliang
            self.vin_jin, self.han_jaeha, self.baek_seong,
            # Yamazaki
            self.shingen, self.park_father,
            # Law
            self.kim_minjae, self.detective_kang,
            # Existing
            self.daniel, self.zack, self.johan, self.vasco, self.jay,
            self.eli, self.warren, self.jake, self.gun, self.goo,
            self.joongoo, self.manager_kim
        ]

    # FIXED: Path management without infinite recursion
    def choose_character_path(self, character):
        """Choose a path for a character - FIXED recursion issue"""
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

        # No path currently - show available paths
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

    # ENHANCED: Enemy turn with Johan copy mechanics
    def enemy_turn(self, enemy):
        if not enemy.is_alive():
            return
        if not any(c.is_alive() for c in self.party):
            return

        # Check stun/bound status
        if enemy.stunned:
            self.add_log(f"⚡ {enemy.name} is stunned and cannot act!")
            enemy.stunned = False
            time.sleep(0.5)
            return
        if enemy.bound:
            self.add_log(f"⚪ {enemy.name} is bound and cannot act!")
            enemy.bound = False
            time.sleep(0.5)
            return

        # Regenerate energy
        enemy.energy = min(enemy.max_energy, enemy.energy + 10)

        # Choose ability based on AI pattern
        if enemy.ai_pattern:
            # Find first available ability with enough energy
            for pattern_key in enemy.ai_pattern:
                if pattern_key in enemy.abilities:
                    abil = enemy.abilities[pattern_key]
                    if enemy.energy >= abil.get("cost", 20):
                        # Use this ability
                        enemy.energy -= abil.get("cost", 20)
                        targets = [c for c in self.party if c.is_alive()]
                        if targets:
                            t = random.choice(targets)
                            dmg = random.randint(abil["dmg"][0], abil["dmg"][1])

                            # Apply damage multiplier from buffs
                            mult, _ = t.get_damage_multiplier()
                            dmg = int(dmg * mult)

                            if t.defending:
                                dmg = int(dmg * 0.5)
                                t.defending = False
                                self.add_log(f"🛡️ {t.name} blocks!")

                            t.take_damage(dmg)
                            self.add_log(f"{enemy.name} uses {abil['name']} for {dmg} damage!")

                            # ===== ENHANCED JOHAN COPY MECHANIC =====
                            # Check if Johan is in the party and alive
                            johan = None
                            for char in self.party:
                                if char.name == "Johan Seong" and char.is_alive():
                                    johan = char
                                    break

                            if johan and hasattr(johan, 'copy_technique') and hasattr(johan, 'calculate_copy_chance'):
                                # Calculate copy chance based on multiple factors
                                copy_chance, factors = johan.calculate_copy_chance(abil['name'], t, enemy.rank)

                                # Display chance factors if debug mode or high chance
                                if copy_chance > 0.5 or random.random() < 0.1:  # Show sometimes
                                    factors_str = " + ".join(factors) if factors else "Base"
                                    self.add_log(f"👁️ Johan's copy chance: {int(copy_chance * 100)}% [{factors_str}]")

                                # Attempt copy
                                if random.random() < copy_chance:
                                    result = johan.copy_technique(abil['name'], t)
                                    if result:
                                        self.add_log(f"👁️✨ {result}")
                                    else:
                                        if johan.copy_count >= johan.max_copy:
                                            self.add_log(f"📦 Johan's copy limit reached ({johan.max_copy}/10)!")
                                else:
                                    # Track view even if copy fails
                                    if abil['name'] in johan.technique_view_count:
                                        johan.technique_view_count[abil['name']] += 1
                                    else:
                                        johan.technique_view_count[abil['name']] = 1
                            # ===== END ENHANCED COPY MECHANIC =====

                            time.sleep(0.8)
                            return

            # If no ability with enough energy, use basic attack
            first_abil = list(enemy.abilities.values())[0]
            if enemy.energy >= first_abil.get("cost", 20):
                enemy.energy -= first_abil.get("cost", 20)
                targets = [c for c in self.party if c.is_alive()]
                if targets:
                    t = random.choice(targets)
                    dmg = random.randint(first_abil["dmg"][0], first_abil["dmg"][1])

                    mult, _ = t.get_damage_multiplier()
                    dmg = int(dmg * mult)

                    if t.defending:
                        dmg = int(dmg * 0.5)
                        t.defending = False

                    t.take_damage(dmg)
                    self.add_log(f"{enemy.name} uses {first_abil['name']} for {dmg} damage!")

                    # Also check for Johan copy on basic attack
                    johan = None
                    for char in self.party:
                        if char.name == "Johan Seong" and char.is_alive():
                            johan = char
                            break

                    if johan and hasattr(johan, 'copy_technique'):
                        copy_chance, _ = johan.calculate_copy_chance(first_abil['name'], t, enemy.rank)
                        if random.random() < copy_chance:
                            result = johan.copy_technique(first_abil['name'], t)
                            if result:
                                self.add_log(f"👁️✨ {result}")

                    time.sleep(0.8)

    # FIXED: Cleanup with proper status management
    def cleanup(self):
        """Clean up after turn - FIXED status management"""
        for c in self.party + self.enemies:
            c.defending = False

            # Realm timer
            if hasattr(c, 'realm_timer') and c.realm_timer > 0:
                c.realm_timer -= 1
                if c.realm_timer <= 0:
                    c.active_realm = Realm.NONE
                    c.realm_effect = None
                    if hasattr(c, 'name'):
                        self.add_log(f"{c.name}'s realm fades.")

            # UI timer
            if hasattr(c, 'ui_mode') and c.ui_mode:
                c.ui_timer -= 1
                if c.ui_timer <= 0:
                    c.ui_mode = False
                    if hasattr(c, 'name'):
                        self.add_log(f"{c.name}'s Ultra Instinct fades.")

            # Beast mode timer
            if hasattr(c, 'beast_mode') and c.beast_mode:
                c.beast_timer -= 1
                if c.beast_timer <= 0:
                    c.beast_mode = False
                    if hasattr(c, 'name'):
                        self.add_log(f"{c.name}'s Beast Mode fades.")

            # God Eye timer (for Johan)
            if hasattr(c, 'god_eye_active') and c.god_eye_active:
                if random.random() < 0.1:  # 10% chance to deactivate each turn
                    c.god_eye_active = False
                    if hasattr(c, 'name'):
                        self.add_log(f"{c.name}'s God Eye fades.")

            # Apply realm regeneration
            if hasattr(c, 'apply_realm_regen'):
                if c.apply_realm_regen():
                    self.add_log(f"🟢 {c.name} regenerates 15 HP from Tenacity Realm.")

            # Random debuff removal (30% chance per debuff)
            if hasattr(c, 'stunned') and c.stunned and random.random() < 0.3:
                c.stunned = False
                self.add_log(f"⚡ {c.name} recovers from stun!")

            if hasattr(c, 'bound') and c.bound and random.random() < 0.3:
                c.bound = False
                self.add_log(f"⚪ {c.name} breaks free from binds!")

            time.sleep(0.2)

    # FIXED: Use ability with proper realm names and descriptions
    def use_ability(self, character):
        """Use an ability - FIXED realm detection with descriptions"""
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

        # Build available abilities (with energy check)
        available = {}
        for key, abil in character.abilities.items():
            if character.energy < abil["cost"]:
                continue
            available[key] = abil

        print("\n" + "📋 AVAILABLE ABILITIES:")
        print("-" * 110)
        time.sleep(0.2)

        # Sort and display abilities by type
        damage_abilities = {k: v for k, v in available.items() if v.get("type") == "damage"}
        buff_abilities = {k: v for k, v in available.items() if v.get("type") in ["buff", "ui"]}
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

        # Infinity technique
        if character.infinity_technique and character.energy >= character.infinity_technique['cost']:
            it = character.infinity_technique
            print(f"\n  ✨ INFINITY TECHNIQUE (99):")
            print(f"     99. {it['name']} | {it['cost']}E | {it['dmg'][0]}-{it['dmg'][1]} DMG")

        # Special option for Johan to view copy stats
        if character.name == "Johan Seong" and hasattr(character, 'get_copy_stats'):
            print(f"\n  📊 VIEW COPY STATS (98)")

        print("\n" + "🎮 COMMANDS:")
        print("  0. 📖 Describe Ability")
        print("  00. 🔮 Activate Realm (if available)")
        print("  000. 🛤️ Choose/View Path")
        print("  0000. ⏭️ Skip Turn (+15E)")
        print("  00000. ↩️ Back")
        if character.name == "Johan Seong":
            print("  98. 📊 View Copy Statistics")
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
        if choice == '98' and character.name == "Johan Seong":
            character.get_copy_stats()
            input("\nPress Enter to continue...")
            return self.use_ability(character)
        if choice == '0':
            print("\n📖 SELECT ABILITY NUMBER TO DESCRIBE:")
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

                # Apply damage multipliers
                mult, buffs = character.get_damage_multiplier()
                dmg = int(dmg * mult)

                target.take_damage(dmg)
                print("\n" + "✨" * 55)
                slow_print(f"✨✨✨ {it['name']} ✨✨✨", 0.05)
                print("✨" * 55)
                time.sleep(0.5)
                self.add_log(f"{character.name} unleashes their INFINITY TECHNIQUE for {dmg} damage!")
                self.add_log(f"📖 {it['desc']}")

                time.sleep(ACTION_DELAY)
                return True

        if choice in available:
            ability = available[choice]
            character.energy = max(0, character.energy - ability["cost"])

            if ability.get("type") == "ui":
                if hasattr(character, 'activate_ui'):
                    self.add_log(character.activate_ui())

            elif ability.get("type") == "buff":
                # Check for specific buffs
                if character.name == "Eli Jang" and "Beast Mode" in ability["name"]:
                    if hasattr(character, 'activate_beast_mode'):
                        self.add_log(character.activate_beast_mode())
                elif character.name == "Johan Seong" and "God Eye" in ability["name"]:
                    if hasattr(character, 'activate_god_eye'):
                        self.add_log(character.activate_god_eye())
                elif character.name == "Vasco" and "Muscle Enhancement" in ability["name"]:
                    character.muscle_boost = True
                    self.add_log("💪 MUSCLE ENHANCEMENT! +30% damage")
                else:
                    self.add_log(f"{character.name} uses {ability['name']}!")
                    if "desc" in ability:
                        self.add_log(f"📖 {ability['desc']}")

            elif ability.get("type") == "utility":
                if "Thread Bind" in ability["name"]:
                    for e in self.enemies:
                        if e.is_alive() and random.random() < 0.6:
                            e.bound = True
                            self.add_log(f"⚪ {e.name} is bound by silver threads!")
                else:
                    self.add_log(f"{character.name} uses {ability['name']}!")
                    if "desc" in ability:
                        self.add_log(f"📖 {ability['desc']}")

            elif ability.get("type") == "damage" or "dmg" in ability:
                target = self.select_target()
                if target:
                    dmg = random.randint(ability["dmg"][0], ability["dmg"][1])

                    # Apply damage multipliers
                    mult, buffs = character.get_damage_multiplier()
                    dmg = int(dmg * mult)

                    target.take_damage(dmg)
                    self.add_log(f"{character.name} uses {ability['name']} for {dmg} damage!")
                    if "desc" in ability:
                        self.add_log(f"📖 {ability['desc']}")

            time.sleep(ACTION_DELAY)
            return True
        else:
            print("❌ Invalid ability number. Try again.")
            time.sleep(0.5)
            return self.use_ability(character)

    def display_ability_description(self, abil):
        """Display ability description"""
        print("\n" + "─" * 80)
        slow_print(f"📖 {abil['name']}", 0.04)
        print("─" * 80)
        if "desc" in abil:
            slow_print(abil['desc'], 0.02)
        if "cost" in abil:
            print(f"\n⚡ Energy Cost: {abil['cost']}")
        if "dmg" in abil and abil["dmg"] != (0, 0):
            print(f"💢 Damage: {abil['dmg'][0]}-{abil['dmg'][1]}")
        if "heal" in abil:
            print(f"💚 Healing: {abil['heal'][0]}-{abil['heal'][1]}")
        print("─" * 80)
        input("Press Enter to continue...")
        print()

    def select_target(self, allies=False):
        """Select a target - FIXED with validation"""
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

        while True:
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

    def display_health_bars(self):
        """Display health bars for party and enemies"""
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

                if member.ui_mode:
                    status.append("👁️UI")
                if member.beast_mode:
                    status.append("🦁BEAST")
                if hasattr(member, 'god_eye_active') and member.god_eye_active:
                    status.append("👁️GOD EYE")
                if member.veinous_rage:
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

                # Show copy count for Johan
                if member.name == "Johan Seong" and hasattr(member, 'copy_count') and member.copy_count > 0:
                    status.append(f"📚{member.copy_count}")

                status_str = " | ".join(status) if status else ""
                print(f"{member.name:20} |{bar}| {member.hp:3}/{member.max_hp:3} HP {member.energy:3}E  {status_str}")
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
                if enemy.stunned:
                    debuff.append("⚡STUN")
                if enemy.bound:
                    debuff.append("⚪BOUND")
                debuff_str = " | ".join(debuff) if debuff else ""
                rank_display = f" [Rank:{enemy.rank}]" if hasattr(enemy, 'rank') else ""
                affil = f" [{enemy.affiliation}]" if enemy.affiliation else ""
                print(f"{enemy.name:20} |{bar}| {enemy.hp:3}/{enemy.max_hp:3} HP{affil}{rank_display} {debuff_str}")
                time.sleep(0.1)

        print("=" * 110)
        time.sleep(0.5)

    # FIXED: Party selection with proper validation
    def select_party(self, max_size=4):
        """Select party members - FIXED validation"""
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
                copy_info = f" [📚{char.copy_count}/10]" if char.name == "Johan Seong" and hasattr(char,
                                                                                                  'copy_count') and char.copy_count > 0 else ""
                print(f"  {i + 1}. {char.name} [{char.title}]{path_info}{copy_info} - {char.hp}/{char.max_hp} HP")
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
            # Verify these characters exist and are alive
            auto_chars = []
            for name in ["Daniel Park", "Vasco", "Zack Lee", "Jay Hong"]:
                for char in self.all_characters:
                    if char.name == name and char.is_alive():
                        auto_chars.append(char)
                        break
            if len(auto_chars) == 4:
                return auto_chars
            else:
                print("❌ Auto-select failed. Please select manually.")
                return self.select_party(max_size)

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
                        # Verify character is still alive
                        if char.is_alive():
                            selected.append(char)
                            print(f"  ✓ Added {char.name}")
                        else:
                            print(f"  ✗ {char.name} is not alive!")
                    else:
                        print(f"  ✗ {char.name} already selected")
                else:
                    print(f"  ✗ Invalid number (must be 1-{len(available)})")
            except ValueError:
                print("  ✗ Invalid input (enter a number)")

        if selected:
            return selected
        else:
            print("No characters selected. Using auto-select.")
            return [self.daniel, self.vasco, self.zack, self.jay]

    # FIXED: Battle with proper EXP scaling
    def battle(self, enemies, party=None):
        """Battle system - FIXED EXP scaling"""
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

            # Player phase - each character gets 15 energy per turn
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

            # Enemy phase
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

            # Award EXP based on enemy strength
            for char in self.party:
                if char.is_alive() and char.path:
                    # Calculate EXP based on enemy ranks
                    total_rank = sum([e.rank for e in self.enemies])
                    exp_gain = max(5, min(50, total_rank // len(self.enemies)))
                    char.path_exp += exp_gain

                    # Level up if enough EXP
                    while char.path_exp >= 100:
                        char.path_level += 1
                        char.path_exp -= 100
                        self.add_log(f"✨ {char.name}'s path leveled up to {char.path_level}!")

            self.save_game()
            time.sleep(VICTORY_DELAY)
            return True

    def add_log(self, message):
        """Add message to battle log"""
        print(f"[T{self.turn_count}] ", end='')
        slow_print(message, 0.02)
        time.sleep(0.2)

    # FIXED: Save/Load with complete state
    def save_game(self):
        """Save game state - FIXED with complete data"""
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
            print("\n💾 Game saved successfully!")
            return True
        return False

    def load_game(self):
        """Load game state - FIXED with complete data"""
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
        """Rest and recover all characters"""
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
            char.realm_effect = None
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
            char.veinous_rage = False
            char.silver_yarn_active = False
            char.muscle_boost = False

            print(f"  ✦ {char.name} fully recovered!")
            time.sleep(0.1)

        print("\n✦ Party fully healed and recovered! ✦")
        self.save_game()
        time.sleep(1.5)

    def path_management_menu(self):
        """Path management menu"""
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
                copy_info = f" [📚{char.copy_count}/10]" if char.name == "Johan Seong" and hasattr(char,
                                                                                                  'copy_count') and char.copy_count > 0 else ""
                print(f"  {i + 1}. {char.name}{copy_info} - {path_info} (Lv.{char.path_level})")
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
        """Story mode - Full implementation"""
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
                 ("Chapter 5: God Dog Soldiers", [create_enemy_god_dog_member(), create_enemy_god_dog_member()]),
                 ("Chapter 6: God Dog Elite", [create_enemy_god_dog_elite(), create_enemy_god_dog_member()]),
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
                 ("Chapter 14: Workers Affiliates", [create_enemy_workers_member(), create_enemy_workers_affiliate()]),
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

                # Update story progress
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

    def check_unlocks(self):
        """Check and apply unlocks"""
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

        if not self.unlocked_characters["Charles Choi"] and self.story_progress.get("charles_choi_defeated", False):
            self.unlocked_characters["Charles Choi"] = True
            new_unlocks.append("Charles Choi - The Puppet Master")

        if not self.unlocked_characters["Tom Lee"] and self.story_progress.get("tom_lee_defeated", False):
            self.unlocked_characters["Tom Lee"] = True
            new_unlocks.append("Tom Lee - The Wild")

        if not self.unlocked_characters["Gapryong Kim"] and self.story_progress.get("gapryong_defeated", False):
            self.unlocked_characters["Gapryong Kim"] = True
            new_unlocks.append("Gapryong Kim - The Strongest of Gen 0")

        if new_unlocks:
            print("\n✨✨✨ NEW CHARACTERS UNLOCKED! ✨✨✨")
            for char in new_unlocks:
                print(f"  ✅ {char}")
            self.save_game()
        else:
            print("\nNo new unlocks yet. Keep fighting!")

        time.sleep(2)

    def crew_gauntlet_mode(self):
        """Crew Gauntlet mode"""
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
        """Boss Rush mode"""
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
        """Endless Survival mode"""
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
        """Training Room mode"""
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
        """Statistics and Records mode"""
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
                copy_info = f" [📚{char.copy_count}/10]" if char.name == "Johan Seong" and hasattr(char,
                                                                                                  'copy_count') and char.copy_count > 0 else ""
                print(f"  • {char.name}{copy_info}: Lv.{char.path_level} ({char.path_exp}/100 EXP)")
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
    """Main game function"""
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

    # Check for existing save (only once)
    save_exists = os.path.exists(SAVE_FILE)
    game = None

    if save_exists:
        print("\n💾 Existing save file found!")
        load_choice = input("Load previous game? (y/n): ").lower()
        if load_choice == 'y':
            game = LookismGame(load_saved=True)  # This will load once
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
                        # Create new game instance
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