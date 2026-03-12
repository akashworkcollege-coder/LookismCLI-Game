#!/usr/bin/env python3
"""
LOOKISM: AWAKENED FIST - COMPLETE CANON EDITION v12
ALL 39 PLAYABLE CHARACTERS — Manhwa Accurate
Based on Park Tae-joon's Lookism (2014-2025) & Manager Kim (Spin-off)

═══════════════════════════════════════════════════════════
v4 FIXES (all bugs and canon issues from review):
═══════════════════════════════════════════════════════════

BUG FIXES:
  BUG-A:  Realm SPEED evasion off-by-one — now checks realm_timer > 0
  BUG-B:  Double defense reduction fixed — Iron Fortress uses ONLY temp_buff,
           not both defending flag AND temp_buff (was 75% reduction, now correct 50%)
  BUG-C:  enemy_turn defending reduction removed — take_damage handles it via temp_buffs
  BUG-F:  Boss Rush and Crew Gauntlet now use lambda factories (fresh enemies each attempt)
  BUG-H:  Realm timer starts at 6 so player gets 5 effective turns after cleanup tick
  BUG-O:  temp_buffs now serialized in to_dict/from_dict

MECHANICS FIXES:
  MECH-1: RealmEffect values now drive actual combat — armor_break, accuracy, double_strike
           evasion, counter, regen, berserk_threshold all read from realm_effect dict
  MECH-3: STRENGTH realm armor_break implemented — ignores 40% of target def reduction
  MECH-4: TECHNIQUE realm accuracy implemented — +40% damage (representing precision)
  MECH-5: SPEED realm double strike now also applies to infinity techniques
  MECH-6: path_level now grants +2% damage per level (meaningful progression)
  MECH-7: veinous_rage wired to a new Johan "Veinous Rage" ability (3-turn buff)
  MECH-8: silver_yarn_active now tracked and shown in status display
  MECH-9: muscle_boost wired to Mandeok "Titan Boost" ability (3-turn buff)
  MECH-10: Enemy fallback-ability-too-expensive now shows "conserves energy" message

CANON FIXES:
  CANON-H: Eli Jang realms set to [STRENGTH, OVERCOMING] (was [])
  CANON-L: Shingen Yamazaki realm_list set to [] — not a Korean Gyeongji user
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
    """
    MECH-1 FIX: These values are now actually read in combat.
    evasion        → checked in enemy_turn
    double_strike  → checked in use_ability and infinity block
    damage_mult    → applied in get_damage_multiplier via STRENGTH realm
    armor_break    → applied in take_damage via MECH-3
    damage_reduction → applied in take_damage via TENACITY
    regen          → applied in cleanup via apply_realm_regen
    accuracy       → applied as bonus damage mult in get_damage_multiplier via TECHNIQUE
    counter        → checked in enemy_turn
    berserk_threshold / berserk_mult → applied in get_damage_multiplier via OVERCOMING
    """
    REALM_DATA = {
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
            "accuracy_mult": 1.4,
            "counter": 0.25,
            "desc": "Perfected form! +40% damage (precision), 25% counter"
        },
        Realm.OVERCOMING: {
            "berserk_threshold": 0.3,
            "berserk_mult": 2.0,
            "desc": "Born from limits! +100% damage when below 30% HP"
        }
    }

    @staticmethod
    def apply(realm, character):
        data = RealmEffect.REALM_DATA.get(realm, {})
        result = dict(data)
        result["desc"] = data.get("desc", f"{realm.value} activated!")
        return result


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
    JAKE_GAPRYONG = "👑 Jake Kim's Inherited Bloodline"
    GUN_YAMAZAKI = "🏯 Gun Park's Black Bone Path"
    GUN_CONSTANT_UI = "👁️ Gun Park's Constant UI"
    GOO_MOONLIGHT = "🌙 Goo Kim's Moonlight Sword"
    GOO_FIFTH = "✨ Goo Kim's Fifth Sword"
    JOONGOO_HWARANG = "⚔️ Kim Jun-gu's Hwarang Sword"
    JOONGOO_ARMED = "🗡️ Kim Jun-gu's Armed Beast"

    # WORKERS / MANAGER KIM
    MANDEOK_POWER = "💪 Mandeok's Titan Strength"
    MANAGER_KIM_CQC = "🔫 Manager Kim's CQC & Code 66"
    XIAOLUNG_MUAY_THAI = "🇹🇭 Xiaolung's Muay Thai Genius"
    RYUHEI_YAKUZA = "⚔️ Ryuhei's Yakuza Style"
    SAMUEL_AMBITION = "👑 Samuel Seo's King's Ambition"
    SINU_INVISIBLE = "🌀 Sinu Han's Invisible Attacks"
    LOGAN_BULLY = "👊 Logan Lee's Bully Brawling"

    # CHEONLIANG
    VIN_JIN_SSIREUM = "🇰🇷 Vin Jin's Judo & Mujin Ssireum"
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
    Path.GAPRYONG_CONVICTION: {
        "name": "👑 INFINITE GAPRYONG: Legend's Fist",
        "cost": 150, "dmg": (300, 420),
        "desc": "The legendary fist that defeated the Yamazaki Syndicate. Gapryong Kim's ultimate conviction."
    },
    Path.TOM_LEE_WILD: {
        "name": "🐅 INFINITE WILD: Tom Lee Special",
        "cost": 140, "dmg": (280, 390),
        "desc": "Tom Lee's ultimate technique. Biting, slashing, pure animal instinct."
    },
    Path.CHARLES_ELITE: {
        "name": "🎭 INFINITE ELITE: The Invisible Chairman",
        "cost": 145, "dmg": (290, 400),
        "desc": "Charles Choi's invisible attacks. The puppet master's final move."
    },
    Path.JINYOUNG_COPY: {
        "name": "🔄 INFINITE COPY: Medical Genius",
        "cost": 135, "dmg": (270, 370),
        "desc": "Jinyoung Park's perfect copy ability replicated with surgical precision."
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
    Path.JAMES_LEE_INVISIBLE: {
        "name": "👑 INFINITE JAMES: The Invisible King",
        "cost": 150, "dmg": (270, 390),
        "desc": "James Lee's perfected invisible attacks. The peak of the 1st Generation."
    },
    Path.GITAE_KIM: {
        "name": "⚡ INFINITE GITAE: King of Seoul's Wrath",
        "cost": 145, "dmg": (290, 400),
        "desc": "Gitae Kim inherits his father's power. Gapryong's strength flows through his fist."
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
        "name": "🔨 INFINITE IRON: King of Daegu's Fortress",
        "cost": 130, "dmg": (260, 360),
        "desc": "Gongseob Ji's iron boxing. Speed and durability combined."
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
        "desc": "Seongji Yuk's mastery of Ssireum, Judo, and Kudo combined."
    },
    Path.JINRANG_CONVICTION: {
        "name": "👑 INFINITE DISCIPLE: True Conviction",
        "cost": 150, "dmg": (300, 420),
        "desc": "Jinrang's ultimate technique. As Gapryong's true disciple, his conviction is absolute."
    },
    Path.DANIEL_UI: {
        "name": "👁️ INFINITE UI: Perfect Body",
        "cost": 100, "dmg": (250, 350),
        "desc": "Daniel's Ultra Instinct. Eyes invert to pure black — the body fights with zero thought, only instinct. Hereditary to the Yamazaki bloodline; how Daniel has it remains unknown."
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
        "desc": "Johan's God Eye sees all. Perfect replication."
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
        "desc": "Jay's Kali mastery. Twin blades moving as one."
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
        "desc": "Gun unleashes the Black Bone technique — the lethal art mastered through Yamazaki training."
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
    Path.MANAGER_KIM_CQC: {
        "name": "🔫 INFINITE CODE 66: Silver Yarn Execution",
        "cost": 95, "dmg": (230, 330),
        "desc": "Manager Kim's ultimate technique. Silver Yarn threads bind and Code 66 finishes."
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
    # Logan Lee intentionally has NO infinity technique (he's a bully, not a martial artist)
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
    },
    Path.LOGAN_BULLY: {
        "name": "👊 INFINITE BULLY: Logan's Reign",
        "cost": 60, "dmg": (160, 220),
        "desc": "Logan Lee's full bully dominance — raw intimidation, cheap shots, and overwhelming physical pressure."
    },
}


# ============================================================================
# BASE CHARACTER CLASS
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
        self.veinous_rage_timer = 0
        self.silver_yarn_active = False
        self.silver_yarn_timer = 0
        self.muscle_boost = False
        self.muscle_boost_timer = 0
        # temp_buffs: list of {'name': str, 'dmg_mult': float, 'def_mult': float, 'turns': int}
        self.temp_buffs = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg, armor_break=False):
        """
        BUG-B FIX: Only temp_buffs reduce damage here.
                   The 'defending' flag is no longer used for damage reduction —
                   Iron Fortress sets a temp_buff instead.
        BUG-C FIX: enemy_turn no longer pre-halves damage for defending players.
        MECH-3 FIX: armor_break=True from STRENGTH realm bypasses 40% of reductions.
        """
        # Apply temp defensive buffs
        for buff in self.temp_buffs:
            def_mult = buff.get('def_mult', 1.0)
            if def_mult != 1.0:
                if armor_break:
                    # STRENGTH realm armor break: reduction only 40% as effective
                    partial = 1.0 - (1.0 - def_mult) * 0.6
                    dmg = int(dmg * partial)
                else:
                    dmg = int(dmg * def_mult)

        # Tenacity realm reduction
        if self.active_realm == Realm.TENACITY:
            if armor_break:
                dmg = int(dmg * 0.7)   # armor break reduces tenacity from 50% to 30% effective
            else:
                dmg = int(dmg * 0.5)

        # DUAL BODY: True Body gets 15% innate damage reduction (tougher trained frame)
        if hasattr(self, 'active_body') and self.active_body == 'true':
            if armor_break:
                dmg = int(dmg * 0.94)  # armor break reduces the bonus to ~6%
            else:
                dmg = int(dmg * 0.85)

        # ENDURANCE MASTERY nullify (GongseobJi): 30% chance to completely absorb hit
        if hasattr(self, 'endurance_nullify_chance') and not armor_break:
            if random.random() < self.endurance_nullify_chance:
                dmg = 0  # nullified — endurance mastery absorbed the hit

        # GEN 0 DURABILITY (TomLee): 20% dmg reduction
        if hasattr(self, 'gen0_durability') and not armor_break:
            dmg = int(dmg * 0.80)

        # PATRIARCH AURA (Shingen): 15% reduction when Shingen is on player's team
        # Applied via character receiving damage — handled here
        if hasattr(self, 'patriarch_aura') and not armor_break:
            dmg = int(dmg * 0.85)

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
        # BUG-H FIX: timer starts at 6 so after cleanup tick player gets 5 effective turns
        self.realm_timer = 6
        self.realm_effect = RealmEffect.apply(realm, self)
        self.form = f"REALM: {realm.name}"
        return f"\n✨ {realm.value} REALM ACTIVATED!\n{self.realm_effect['desc']}\n"

    def get_damage_multiplier(self):
        """
        Single source of truth for damage multipliers.
        MECH-6 FIX: path_level now grants +2% damage per level above 1.
        MECH-4 FIX: TECHNIQUE realm accuracy_mult applied here.
        """
        mult = 1.0
        buffs = []

        # Realm bonuses
        if self.active_realm == Realm.STRENGTH:
            realm_mult = self.realm_effect.get('damage_mult', 1.7) if self.realm_effect else 1.7
            mult *= realm_mult
            buffs.append("🔴 STRENGTH")
        elif self.active_realm == Realm.TECHNIQUE:
            # MECH-4: accuracy represented as damage bonus for precision strikes
            tech_mult = self.realm_effect.get('accuracy_mult', 1.4) if self.realm_effect else 1.4
            mult *= tech_mult
            buffs.append("🩷 TECHNIQUE")
        elif self.active_realm == Realm.OVERCOMING:
            threshold = self.realm_effect.get('berserk_threshold', 0.3) if self.realm_effect else 0.3
            berserk_mult = self.realm_effect.get('berserk_mult', 2.0) if self.realm_effect else 2.0
            if self.hp < self.max_hp * threshold:
                mult *= berserk_mult
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

        # Timed buffs (temp_buffs list)
        for buff in self.temp_buffs:
            dmg_mult = buff.get('dmg_mult', 1.0)
            if dmg_mult != 1.0:
                mult *= dmg_mult
                buffs.append(f"⚡{buff['name'][:8]}({buff['turns']}T)")

        # MECH-6: path level bonus — +2% per level above 1, capped at +40% (level 21)
        if self.path and self.path_level > 1:
            level_bonus = 1.0 + min(0.40, (self.path_level - 1) * 0.02)
            mult *= level_bonus
            buffs.append(f"🛤️Lv{self.path_level}(+{round((level_bonus-1)*100)}%)")

        # DUAL BODY: body type modifier
        # Perfect Body = natural 1.0x (baseline — elite physical frame)
        # True Body (post-Gun) = 0.85x ATK but +15% damage reduction (handled in take_damage)
        if hasattr(self, 'active_body') and self.active_body == 'true':
            mult *= 0.85
            buffs.append("🔵TRUEBODY(-15%atk)")

        # RIGHT HAND PHILOSOPHY (Taesoo Ma): +20% when using right-hand-only approach
        if hasattr(self, 'right_hand_charge'):
            mult *= 1.20
            buffs.append("🔴RIGHTHAND(+20%)")

        # CONVICTION STACKS (Jinrang): each stack = +10% dmg
        if hasattr(self, 'conviction_stacks') and self.conviction_stacks > 0:
            conv_bonus = 1.0 + (self.conviction_stacks * 0.10)
            mult *= conv_bonus
            buffs.append(f"👑CONVICTION{self.conviction_stacks}(+{self.conviction_stacks*10}%)")

        # HEAT MODE (Vasco): +50% when active
        if hasattr(self, 'heat_mode_active') and self.heat_mode_active:
            mult *= 1.50
            buffs.append("🔥HEATMODE(+50%)")

        # GLASSES OFF (Vin Jin): +60% when glasses removed
        if hasattr(self, 'glasses_on') and not self.glasses_on:
            mult *= 1.60
            buffs.append("🕶️GLASSESOFF(+60%)")

        # LAST STAND BURST (Jinrang): +70% when last stand conviction activated
        if hasattr(self, 'last_stand_burst') and self.last_stand_burst:
            mult *= 1.70
            buffs.append("👑LASTSTAND(+70%)")

        # TAEKKYON RHYTHM (BaekSeong): +15% per stack
        if hasattr(self, 'rhythm_stacks') and self.rhythm_stacks > 0:
            rhythm_bonus = 1.0 + (self.rhythm_stacks * 0.15)
            mult *= rhythm_bonus
            buffs.append(f"🦢RHYTHM{self.rhythm_stacks}(+{self.rhythm_stacks*15}%)")

        # SELF-HATRED (Samuel Seo): when active, x2.0
        if hasattr(self, 'self_hatred_active') and self.self_hatred_active:
            mult *= 2.0
            buffs.append("💢SELFHATRED(x2.0)")

        # PATRIARCH AURA (Shingen): ALL enemies deal -15% to party
        # This is handled in take_damage via enemy_turn detection
        # Here we just add it to self's mult if Shingen is on the team (handled externally)

        return mult, buffs

    def apply_realm_regen(self):
        if self.active_realm == Realm.TENACITY:
            regen = self.realm_effect.get('regen', 15) if self.realm_effect else 15
            self.heal(regen)
            return regen
        return 0

    def to_dict(self):
        # BUG-V1 FIX: silver_yarn_active + silver_yarn_timer now included
        # BUG-X12 FIX: permanent_ui included (GunPark Constant UI must survive save/load)
        # BUG-X13 FIX: path_history included so reset_path() undo works after load
        d = {
            'name': self.name,
            'path': self.path.name if self.path else None,
            'path_level': self.path_level,
            'path_exp': self.path_exp,
            'path_history': [p.name for p in self.path_history],
            'hp': self.hp,
            'energy': self.energy,
            'active_realm': self.active_realm.name if self.active_realm != Realm.NONE else None,
            'realm_timer': self.realm_timer,
            'form': self.form,
            'ui_mode': self.ui_mode,
            'ui_timer': self.ui_timer,
            'beast_mode': self.beast_mode,
            'beast_timer': self.beast_timer,
            'veinous_rage': self.veinous_rage,
            'veinous_rage_timer': self.veinous_rage_timer,
            'muscle_boost': self.muscle_boost,
            'muscle_boost_timer': self.muscle_boost_timer,
            'silver_yarn_active': self.silver_yarn_active,
            'silver_yarn_timer': self.silver_yarn_timer,
            'temp_buffs': self.temp_buffs,
        }
        # BUG-X12 FIX: only include permanent_ui if the character has it
        if hasattr(self, 'permanent_ui'):
            d['permanent_ui'] = self.permanent_ui
        # DUAL BODY: serialize both body pools if this is Daniel
        if hasattr(self, 'active_body'):
            d['active_body']        = self.active_body
            d['perfect_hp']         = self.perfect_hp
            d['perfect_max_hp']     = self.perfect_max_hp
            d['perfect_energy']     = self.perfect_energy
            d['perfect_max_energy'] = self.perfect_max_energy
            d['true_hp']            = self.true_hp
            d['true_max_hp']        = self.true_max_hp
            d['true_energy']        = self.true_energy
            d['true_max_energy']    = self.true_max_energy
            d['dual_sync_active']   = self.dual_sync_active
            d['dual_sync_timer']    = self.dual_sync_timer
        return d

    def from_dict(self, data):
        if data.get('path'):
            for path in Path:
                if path.name == data['path']:
                    self.path = path
                    self.infinity_technique = INFINITY_TECHNIQUES.get(path)
                    break
        self.path_level = data.get('path_level', 1)
        self.path_exp = data.get('path_exp', 0)
        # BUG-X13 FIX: restore path_history so reset_path() undo works after load
        raw_history = data.get('path_history', [])
        self.path_history = []
        for pname in raw_history:
            for path in Path:
                if path.name == pname:
                    self.path_history.append(path)
                    break
        self.hp = data.get('hp', self.max_hp)
        self.energy = data.get('energy', self.max_energy)

        realm_name = data.get('active_realm')
        if realm_name:
            for realm in Realm:
                if realm.name == realm_name:
                    self.active_realm = realm
                    self.realm_effect = RealmEffect.apply(realm, self)
                    break
        self.realm_timer = data.get('realm_timer', 0)
        self.form = data.get('form', 'Normal')
        self.ui_mode = data.get('ui_mode', False)
        self.ui_timer = data.get('ui_timer', 0)
        self.beast_mode = data.get('beast_mode', False)
        self.beast_timer = data.get('beast_timer', 0)
        self.veinous_rage = data.get('veinous_rage', False)
        self.veinous_rage_timer = data.get('veinous_rage_timer', 0)
        self.muscle_boost = data.get('muscle_boost', False)
        self.muscle_boost_timer = data.get('muscle_boost_timer', 0)
        # BUG-V1 FIX: restore silver_yarn state
        self.silver_yarn_active = data.get('silver_yarn_active', False)
        self.silver_yarn_timer = data.get('silver_yarn_timer', 0)
        # BUG-O FIX: restore temp_buffs
        self.temp_buffs = data.get('temp_buffs', [])
        # BUG-X12 FIX: restore permanent_ui if present (GunPark Constant UI)
        if 'permanent_ui' in data and hasattr(self, 'permanent_ui'):
            self.permanent_ui = data['permanent_ui']
        # DUAL BODY: restore both pools if this is Daniel
        if hasattr(self, 'active_body'):
            self.active_body        = data.get('active_body', 'perfect')
            self.perfect_hp         = data.get('perfect_hp', self.perfect_max_hp)
            self.perfect_max_hp     = data.get('perfect_max_hp', self.perfect_max_hp)
            self.perfect_energy     = data.get('perfect_energy', self.perfect_max_energy)
            self.perfect_max_energy = data.get('perfect_max_energy', self.perfect_max_energy)
            self.true_hp            = data.get('true_hp', self.true_max_hp)
            self.true_max_hp        = data.get('true_max_hp', self.true_max_hp)
            self.true_energy        = data.get('true_energy', self.true_max_energy)
            self.true_max_energy    = data.get('true_max_energy', self.true_max_energy)
            self.dual_sync_active   = data.get('dual_sync_active', False)
            self.dual_sync_timer    = data.get('dual_sync_timer', 0)
            # Sync live hp/energy/max_hp/max_energy to the active body's pool
            if self.active_body == 'perfect':
                self.hp = self.perfect_hp; self.max_hp = self.perfect_max_hp
                self.energy = self.perfect_energy; self.max_energy = self.perfect_max_energy
            else:
                self.hp = self.true_hp; self.max_hp = self.true_max_hp
                self.energy = self.true_energy; self.max_energy = self.true_max_energy

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
        self.paths_available = [Path.GAPRYONG_CONVICTION, Path.GAPRYONG_FIST_MEMBER]
        # PROTECT INSTINCT: if any party member drops below 20% HP,
        # Gapryong intercepts the next attack directed at them. Once per battle.
        self.protect_intercept_available = True
        self.protect_target = None
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
                  "desc": "Defensive stance. Adds -50% damage reduction buff for 2 turns."}
        }


class TomLee(Character):
    def __init__(self):
        super().__init__("Tom Lee", "The Wild", 850, 380,
                         [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 0
        self.affiliation = "Gen 0 / Ten Geniuses"
        self.paths_available = [Path.TOM_LEE_WILD, Path.GAPRYONG_FIST_MEMBER]
        # ANIMAL INSTINCT: wild fighting — unpredictable, targets weak points.
        # Canon: "fighting without thought, only instinct" — targets eyes/groin.
        # Tom defeated Eli multiple times without even looking at him.
        self.animal_instinct = False
        self.animal_instinct_timer = 0
        # GEN 0 DURABILITY: Tom can take hits from Johan, Warren, etc. with little harm.
        # Passive 20% damage reduction built into take_damage via temp_buff on init.
        self.gen0_durability = True  # flagged for use_ability bonus hit logic
        self.abilities = {
            '1': {"name": "🐅 Wild Strike", "cost": 25, "dmg": (90, 140), "type": "damage",
                  "desc": "A primal, untamed strike. Tom Lee fights like a wild animal."},
            '2': {"name": "🐅 Tom Lee Special", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "Biting, clawing, and striking combined. His signature move."},
            '3': {"name": "🐅 Gen 0 Power", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Raw power from the legendary era."},
            '4': {"name": "🐅 Bite Force", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "Literally biting his opponents. Tom Lee's jaw strength rivals a wild animal."},
            '5': {"name": "🐅 Animal Instinct", "cost": 50, "dmg": (0, 0), "type": "buff",
                  "desc": "CANON: no-thought fighting. Each attack has 30% chance of a free improvised weapon bonus hit. +40% dmg, 3 turns."},
            '6': {"name": "🐅 Lunge Charge", "cost": 45, "dmg": (160, 220), "type": "damage",
                  "armor_break": True,
                  "desc": "UNIQUE SKILL: Tom lowers into a lunge stance, concentrates strength in his legs, then pierces through with his hands. Split a police car in half."}
        }


class CharlesChoi(Character):
    def __init__(self):
        super().__init__("Charles Choi", "Elite", 800, 360,
                         [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 0
        self.affiliation = "HNH Group / Ten Geniuses"
        self.paths_available = [Path.CHARLES_ELITE, Path.GAPRYONG_FIST_MEMBER]
        # ANALYTICAL PREDICTION: 20% passive dodge (reads fighters at UI level).
        self.analytical_dodge = 0.20
        self.abilities = {
            '1': {"name": "🎭 Invisible Strike", "cost": 30, "dmg": (90, 140), "type": "damage",
                  "armor_break": True,
                  "desc": "CANON: speed so great the strike is invisible. Bypasses all defense."},
            '2': {"name": "🎭 Chairman's Authority", "cost": 40, "dmg": (120, 170), "type": "damage",
                  "desc": "The power of the HNH Group chairman. Decades of manipulation made manifest."},
            '3': {"name": "🎭 Elite Technique", "cost": 35, "dmg": (110, 160), "type": "damage",
                  "desc": "A technique passed down through Gapryong's Fist."},
            '4': {"name": "🎭 Truth of Two Bodies", "cost": 50, "dmg": (0, 0), "type": "weakness_expose",
                  "desc": "Charles exploits the weakness of his opponent's fighting style. Enemy takes +25% damage for 2 turns."},
            '5': {"name": "🎭 Elusive Form", "cost": 30, "dmg": (0, 0), "type": "buff",
                  "desc": "Charles enters a flow state. Analytical prediction: +30% damage, +20% dodge, for 3 turns."}
        }


class JinyoungPark(Character):
    def __init__(self):
        super().__init__("Jinyoung Park", "The Medical Genius", 780, 350, [Realm.TECHNIQUE])
        self.canon_episode = 0
        self.paths_available = [Path.JINYOUNG_COPY, Path.GAPRYONG_FIST_MEMBER]
        # MIRROR KING: copies opponent masteries, not just motions — wiki.
        # 40% chance to counter with the attacker's technique at full mastery.
        self.mirror_copy_ready = False
        self.mirror_copy_technique = ""
        self.mastery_copy_stacks = 0   # builds per turn in mirror_copy mode
        self.affiliation = "Gen 0 / Gapryong's Fist"
        self.abilities = {
            '1': {"name": "🔄 Copy: Taekwondo", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Perfect replication of Taekwondo."},
            '2': {"name": "🔄 Copy: Karate", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Flawless Karate. Precision via pure analytical ability."},
            '3': {"name": "🔄 Copy: Boxing", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "World-class boxing, mechanically perfect."},
            '4': {"name": "🔄 Copy: Judo", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Perfect Judo throws, replicating the master's movements exactly."},
            '5': {"name": "🔄 Copy: Systema", "cost": 25, "dmg": (80, 130), "type": "damage",
                  "desc": "Russian Systema techniques replicated."},
            '6': {"name": "🔄 Medical Precision", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "Surgical strikes on vital points — nerve clusters, pressure points."},
            '7': {"name": "🔄 Mirror King: Mastery Copy", "cost": 60, "dmg": (0, 0), "type": "buff",
                  "desc": "CANON: copies opponent's MASTERY, not just motion. For 3 attacks, Jinyoung copies a Gen 0 legend's physique. +90% dmg next 3 hits."},
            '8': {"name": "💊 Medical Debilitate", "cost": 40, "dmg": (70, 100), "type": "debilitate",
                  "desc": "Medical genius targets nerve clusters. Enemy attack power -30% for 3 turns."}
        }


class Baekho(Character):
    def __init__(self):
        super().__init__("Baekho Kwon", "The White Tiger", 820, 370, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 0
        self.paths_available = [Path.BAEKHO_BEAST, Path.GAPRYONG_FIST_MEMBER]
        self.affiliation = "Gen 0 / Gapryong's Fist"
        self.abilities = {
            '1': {"name": "🐯 Tiger Strike", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "A strike with the ferocity of a white tiger."},
            # BUG-V3 FIX: type changed from 'damage' to 'buff' so activate_beast_mode is called
            '2': {"name": "🐯 Beast Mode", "cost": 40, "dmg": (0, 0), "type": "buff",
                  "desc": "Unleashing his inner beast. +60% damage for 3 turns."},
            '3': {"name": "🐯 White Tiger's Claw", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "Raking claw strikes that tear through defenses."}
        }

    def activate_beast_mode(self):
        self.beast_mode = True
        self.beast_timer = 3
        return "🐯🐯🐯 BEAST MODE! Baekho unleashes the White Tiger! +60% damage for 3 turns!"


# ===== 1ST GENERATION KINGS =====

class JamesLee(Character):
    def __init__(self):
        super().__init__("James Lee", "Legend of 1st Gen", 880, 390, [Realm.SPEED, Realm.TECHNIQUE])
        self.canon_episode = 0
        self.affiliation = "1st Generation / Ten Geniuses"
        self.paths_available = [Path.JAMES_LEE_INVISIBLE]
        self.abilities = {
            '1': {"name": "👑 Invisible Kick", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "desc": "A kick that can't be seen. James Lee's speed transcends human perception."},
            '2': {"name": "👑 Perfect Form", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "desc": "Technique perfected to its absolute peak. Every movement economical and deadly."},
            '3': {"name": "👑 One Man Circle", "cost": 50, "dmg": (170, 220), "type": "damage",
                  "desc": "The technique that dismantled the 1st Generation."},
            '4': {"name": "👑 Legend's Speed", "cost": 30, "dmg": (0, 0), "type": "buff",
                  "desc": "Tapping into legendary speed. +30% damage for 3 turns."}
        }


class GitaeKim(Character):
    def __init__(self):
        super().__init__("Gitae Kim", "King of Seoul", 860, 380, [Realm.STRENGTH, Realm.OVERCOMING])
        self.canon_episode = 0
        self.paths_available = [Path.GITAE_KIM]
        # INHERITED RAGE: damage scales with HP lost (OVERCOMING realm mechanic).
        # 0-30% lost: 1.0x | 30-60%: 1.3x | 60-80%: 1.7x | 80%+: 2.2x
        # INNATE STRENGTH: Warren confirms Ch.468 — "that's not a martial art, just innate strength."
        # Can't be copied by normal copy users. 25% chance each attack is armor_break.
        self.innate_strength = True
        self.abilities = {
            '1': {"name": "⚡ Gapryong's Blood", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "innate": True,
                  "desc": "INNATE STRENGTH: not technique — raw bloodline power. 25% armor_break chance."},
            '2': {"name": "⚡ Inherited Power", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "innate": True,
                  "desc": "Power passed down through generations — cannot be copied."},
            '3': {"name": "⚡ King's Authority", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "desc": "The commanding presence of Seoul's king."},
            '4': {"name": "🔁 Imitation: Enemy Style", "cost": 45, "dmg": (0, 0), "type": "buff",
                  "desc": "CANON: Gitae copies opponents' strengths instinctively. +40% dmg for 2 turns. Gitae's imitation style."}
        }


class JichangKwak(Character):
    def __init__(self):
        super().__init__("Jichang Kwak", "The White Viper", 800, 360, [Realm.SPEED, Realm.TECHNIQUE])
        self.canon_episode = 0
        self.paths_available = [Path.JICHANG_HAND_BLADE]
        # BLADE EDGE: Jichang trained hands/forearms to blade sharpness. Canon: TV Tropes.
        # Hand Blade attacks are always armor_break.
        # DOUBLE EDGE: guaranteed second strike at 50% (two-chop combo).
        self.blade_combo_ready = False  # set by Double Edge, consumed on next hit
        self.abilities = {
            '1': {"name": "🩷 Hand Blade", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "armor_break": True,
                  "desc": "CANON: hands trained to blade-sharp edges. Always bypasses armor. Can slice through defenses."},
            '2': {"name": "🩷 Double Edge", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "armor_break": True, "double_chop": True,
                  "desc": "Two Hand Blade strikes in one motion. Always armor_break + guaranteed follow-up at 50% dmg."},
            '3': {"name": "🩷 Seoul King's Pride", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "armor_break": True,
                  "desc": "Concentrated hand blade — the power that made even Elite want him as a bodyguard."},
            '4': {"name": "🩷 Nerve Slice", "cost": 25, "dmg": (80, 110), "type": "damage",
                  "armor_break": True, "stun_chance": 0.35,
                  "desc": "A nerve-point strike with blade-hand. 35% stun chance — cuts nerve clusters."}
        }


class TaesooMa(Character):
    def __init__(self):
        super().__init__("Taesoo Ma", "King of Ansan", 820, 350, [Realm.STRENGTH])
        self.canon_episode = 0
        self.paths_available = [Path.TAESOO_MA_FIST]
        self.affiliation = "1st Generation"
        # RIGHT HAND PHILOSOPHY: "I fight because I am a man." Only uses right fist.
        # Every Right Hand / Ansan King attack: +20% dmg bonus (commitment).
        # ULTIMATE FIST: all muscle power into one strike. So powerful it injures his own hand.
        self.right_hand_charge = 0   # increments each turn, consumed by Ultimate Fist
        self.abilities = {
            '1': {"name": "🔴 Right Hand", "cost": 35, "dmg": (130, 180), "type": "damage",
                  "right_hand": True,
                  "desc": "CANON: only ever the right fist. Philosophy over technique. +20% dmg bonus from conviction."},
            '2': {"name": "🔴 No Technique", "cost": 40, "dmg": (150, 200), "type": "damage",
                  "right_hand": True,
                  "desc": "Pure raw strength. Right fist only. Untouchable conviction."},
            '3': {"name": "🔴 Ansan King", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "right_hand": True,
                  "desc": "The pride of Ansan. Right fist conviction."},
            '4': {"name": "🔴 Ultimate Fist", "cost": 80, "dmg": (220, 280), "type": "ultimate_fist",
                  "desc": "CANON Ch.Unique: every muscle channeled into the right wrist. Both Strength+Speed mastery. Injures own hand (-25HP self-damage). Uncopyable."}
        }


class GongseobJi(Character):
    def __init__(self):
        super().__init__("Gongseob Ji", "King of Daegu", 750, 340, [Realm.SPEED, Realm.TENACITY])
        self.canon_episode = 0
        self.affiliation = "1st Generation"
        self.paths_available = [Path.GONGSEOB_IRON]
        # ONE STEP ONE KILL: invented after losing legs to James Lee.
        # Uses Speed Mastery to dodge+counter in ONE step. Technique + Speed in single strike.
        # ENDURANCE MASTERY: green glow. 30% passive chance to completely nullify damage.
        self.endurance_nullify_chance = 0.30
        self.abilities = {
            '1': {"name": "🩷 Iron Boxing", "cost": 25, "dmg": (90, 140), "type": "damage",
                  "desc": "Gongseob's style combining speed with iron-like durability."},
            '2': {"name": "🩷 Speed Technique", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "Blazing fast strikes blurring offense and defense."},
            '3': {"name": "🩷 Tungsten Defense", "cost": 20, "dmg": (0, 0), "type": "utility",
                  "desc": "Endurance mastery: -70% damage for 1 turn (active version of passive nullification)."},
            '4': {"name": "🩷 One Step, One Kill", "cost": 50, "dmg": (140, 190), "type": "counter",
                  "desc": "UNIQUE SKILL (canon). Speed Mastery dodge + critical counter in ONE step. Counters next attack. Technique+Speed mastery combined."}
        }


class SeokduWang(Character):
    def __init__(self):
        super().__init__("Seokdu Wang", "King of Suwon", 780, 330, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 0
        self.paths_available = [Path.SEOKDU_HEADBUTT]
        self.affiliation = "1st Generation"
        # IRON FOREHEAD: TV Tropes — "trained his forehead to kill with a single headbutt."
        # All headbutt attacks are armor_break. 20% stun chance on headbutt.
        self.abilities = {
            '1': {"name": "💢 Headbutt", "cost": 30, "dmg": (120, 170), "type": "damage",
                  "armor_break": True, "stun_chance": 0.20,
                  "desc": "CANON: forehead trained to lethal hardness. Always armor_break. 20% stun."},
            '2': {"name": "💢 Iron Forehead", "cost": 25, "dmg": (100, 150), "type": "damage",
                  "armor_break": True, "stun_chance": 0.20,
                  "desc": "Years of training. Unbreakable forehead. Cannot be absorbed by endurance."},
            '3': {"name": "💢 Suwon's Crown", "cost": 35, "dmg": (140, 190), "type": "damage",
                  "armor_break": True, "stun_chance": 0.30,
                  "desc": "The king's ultimate headbutt — lethal forehead strike."},
            '4': {"name": "💢 Iron Crown Stance", "cost": 20, "dmg": (0, 0), "type": "buff",
                  "desc": "Seokdu lowers his head and enters a defensive stance. -30% damage received + forehead attacks deal +40% damage for 2 turns."}
        }


class JaegyeonNa(Character):
    def __init__(self):
        super().__init__("Jaegyeon Na", "King of Incheon", 770, 360, [Realm.SPEED])
        self.canon_episode = 544
        self.paths_available = [Path.JAEGYEON_SPEED]
        self.affiliation = "1st Generation"
        # INVISIBLE ATTACKS: speed mastery. One of three characters who mastered invisible attacks.
        # All attacks are armor_break (too fast to block). "Faster Than Light" = double strike.
        # Also uses Yugang Ha's unique technique (speed+technique in single step).
        self.abilities = {
            '1': {"name": "🔵 Incheon Speed", "cost": 30, "dmg": (100, 150), "type": "damage",
                  "armor_break": True,
                  "desc": "CANON: speed mastery — invisible attack. Too fast to block."},
            '2': {"name": "🔵 Faster Than Light", "cost": 40, "dmg": (140, 190), "type": "damage",
                  "armor_break": True, "forced_double": True,
                  "desc": "CANON: master-level invisible attack. Always deals double strike — first hit too fast to see, second follows instantly."},
            '3': {"name": "🔵 King of Incheon", "cost": 35, "dmg": (120, 170), "type": "damage",
                  "armor_break": True,
                  "desc": "Invisible attack — Jaegyeon's pride as king."},
            '4': {"name": "🔵 One Step Technique", "cost": 45, "dmg": (150, 200), "type": "counter",
                  "armor_break": True,
                  "desc": "Yugang Ha's unique technique: Speed+Technique mastery in a single step. Counter-strike that lands from any angle."}
        }


class SeongjiYuk(Character):
    def __init__(self):
        super().__init__("Seongji Yuk", "King of Cheonliang", 820, 370,
                         [Realm.STRENGTH, Realm.TECHNIQUE, Realm.OVERCOMING])
        self.canon_episode = 500
        self.paths_available = [Path.SEONGJI_MONSTER, Path.SEONGJI_MARTIAL]
        # RIB CRUSH DEBUFF: each Mujin Ssireum use reduces target max_hp by 8%.
        self.rib_crush_count = {}  # enemy_name -> count
        self.abilities = {
            '1': {"name": "🇰🇷 Ssireum: Throw", "cost": 25, "dmg": (90, 140), "type": "damage",
                  "desc": "Jin Mujin's Ssireum — wrestling that breaks bones with pure grip strength."},
            '2': {"name": "🇰🇷 Mujin Ssireum: Rib Crush", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "Seongji grabs three ribs in each hand and bends them until they crack."},
            '3': {"name": "🥋 Yaksha Kudo", "cost": 30, "dmg": (110, 160), "type": "damage",
                  "desc": "Kudo taught to Seongji by the Yamazaki brothers' Yakshas — grappling + striking lethal combo."},
            '4': {"name": "🦍 Monster Mode", "cost": 45, "dmg": (0, 0), "type": "buff",
                  "desc": "CANON: Seongji enters a feral state. +80% dmg for 3 turns. Enemy ATK -20% from fear. Body grows visibly tense."}
        }

    def activate_monster_mode(self):
        self.beast_mode = True
        self.beast_timer = 3
        # Add enemy ATK debuff via temp_buff on self (used as debuff signal in enemy_turn)
        self.monster_mode_active = True
        return "🦍🦍🦍 MONSTER MODE! Seongji Yuk transforms! +80% damage for 3 turns! Enemy ATK -20%!"


class Jinrang(Character):
    def __init__(self):
        super().__init__("Jinrang", "King of Busan", 830, 380, [Realm.STRENGTH, Realm.OVERCOMING])
        self.canon_episode = 580
        self.affiliation = "Busan / Gapryong's Disciple"
        self.paths_available = [Path.JINRANG_CONVICTION]
        # LAST STAND: below 30% HP, once per battle: survive at 1HP,
        # then gain +70% dmg for 2 turns (conviction burst).
        self.last_stand_available = True
        self.last_stand_burst = False
        self.last_stand_burst_timer = 0
        # CONVICTION STACKS: Canon — "True Conviction" is uncopyable because it's powered
        # by genuine belief, not technique. Each hit Jinrang takes builds conviction.
        # +10% dmg per stack (max 5 stacks = +50% dmg).
        self.conviction_stacks = 0
        self.max_conviction_stacks = 5
        self.abilities = {
            '1': {"name": "👑 Jinrang's Conviction", "cost": 35, "dmg": (130, 180), "type": "damage",
                  "conviction": True,
                  "desc": "Conviction-powered strike. Each hit TAKEN adds a conviction stack (+10% dmg)."},
            '2': {"name": "👑 Gapryong's Disciple", "cost": 40, "dmg": (150, 200), "type": "damage",
                  "conviction": True,
                  "desc": "Techniques passed directly from Gapryong. Grows stronger as battle intensifies."},
            '3': {"name": "👑 Busan King", "cost": 45, "dmg": (170, 220), "type": "damage",
                  "conviction": True,
                  "desc": "The authority of Busan's king."},
            '4': {"name": "👑 True Conviction", "cost": 60, "dmg": (200, 250), "type": "damage",
                  "conviction": True, "uncopyable": True,
                  "desc": "CANON: uncopyable. Copy Technique wiki states Daniel cannot replicate the ESSENCE of Jinrang's Conviction. Powered by pure belief."}
        }


# ===== GEN 2 CREW LEADERS =====

class DanielPark(Character):
    def __init__(self, episode_state="current"):
        super().__init__("Daniel Park", "The Second Body", 320, 300, [])
        self.episode_state = episode_state
        self.canon_episode = 581
        self.sophia_trained = True
        self.jichang_copied = True
        self.gapryong_copied = True
        self.form = "Normal"
        self.switch_available = True
        self.paths_available = [Path.DANIEL_UI, Path.DANIEL_COPY]

        # ── DUAL BODY SYSTEM ─────────────────────────────────────────────────
        # Daniel has two separate bodies. active_body = "perfect" or "true".
        # Each body has its own HP/energy pool. The inactive body's stats are
        # stored here and swapped when Body Swap is used.
        # Perfect Body (2nd body): higher ATK multiplier, lower HP
        # True Body (original, post-Gun training): lower ATK, higher HP/defense
        self.active_body        = "perfect"   # currently in control

        # Perfect Body pool (the one in active combat by default)
        self.perfect_hp         = self.hp         # 320
        self.perfect_max_hp     = self.max_hp     # 320
        self.perfect_energy     = self.energy     # 300
        self.perfect_max_energy = self.max_energy # 300

        # True Body pool — post-Gun training, shorter reach but tougher
        self.true_hp            = 380   # tankier
        self.true_max_hp        = 380
        self.true_energy        = 260   # less energy (weaker frame)
        self.true_max_energy    = 260

        # Dual Body Sync state — both bodies fight simultaneously
        self.dual_sync_active   = False
        self.dual_sync_timer    = 0     # turns remaining
        # ─────────────────────────────────────────────────────────────────────

        self.abilities = {
            '1':  {"name": "👊 Desperate Flailing", "cost": 10, "dmg": (20, 35), "type": "damage",
                   "desc": "Early Daniel's fighting style — wild, uncoordinated swings born of desperation."},
            '2':  {"name": "🔄 Instinctive Copy", "cost": 20, "dmg": (30, 50), "type": "damage",
                   "desc": "Daniel's natural copying ability. Reactive and instinctive, not deliberate."},
            '3':  {"name": "🇷🇺 Systema: Ryabina", "cost": 25, "dmg": (50, 70), "type": "damage",
                   "desc": "A Systema technique learned from Sophia. Targets vital points."},
            '4':  {"name": "⚡ Copy: Zack's Counter", "cost": 25, "dmg": (55, 80), "type": "damage",
                   "desc": "Daniel replicates Zack Lee's signature counter punch."},
            '5':  {"name": "⚡ Copy: Vasco's Sunken Fist", "cost": 30, "dmg": (65, 90), "type": "damage",
                   "desc": "Vasco's Muay Thai technique, instinctively copied."},
            '6':  {"name": "⚡ Copy: Eli's Animal Instinct", "cost": 30, "dmg": (70, 95), "type": "damage",
                   "desc": "Eli Jang's wild style replicated."},
            '7':  {"name": "⚡ Copy: Jake's Conviction", "cost": 35, "dmg": (75, 105), "type": "damage",
                   "desc": "Jake Kim's conviction-powered strikes."},
            '8':  {"name": "⚡ Copy: Johan's Choreography", "cost": 40, "dmg": (80, 115), "type": "damage",
                   "desc": "Johan Seong's dance combat."},
            '9':  {"name": "⚡ Copy: Gun's Taekwondo", "cost": 35, "dmg": (80, 110), "type": "damage",
                   "desc": "Gun Park's Taekwondo mastery."},
            '10': {"name": "🩷 Jichang's Hand Blade", "cost": 45, "dmg": (90, 130), "type": "damage",
                   "desc": "Jichang Kwak's legendary technique."},
            '11': {"name": "👑 Gapryong's Conviction", "cost": 60, "dmg": (120, 180), "type": "damage",
                   "desc": "The ultimate instinctive response — Daniel's body channels Gapryong's fist."},
            '12': {"name": "👁️ Ultra Instinct", "cost": 100, "dmg": (0, 0), "type": "ui",
                   "desc": "Daniel's ultimate awakening. Body moves before mind. +150% damage for 3 turns."},
            '13': {"name": "🔁 Body Swap", "cost": 40, "dmg": (0, 0), "type": "body_swap",
                   "desc": "Daniel shifts his consciousness to his other body. Swaps HP/energy pools. "
                           "Perfect Body: high ATK, 320HP. True Body: tank, 380HP, lower ATK."},
            '14': {"name": "👥 Dual Body Sync", "cost": 150, "dmg": (0, 0), "type": "dual_sync",
                   "desc": "ULTIMATE — Ch.470. Both bodies fight simultaneously for 3 turns. "
                           "Every attack triggers a free follow-up from the second body (70% dmg). "
                           "Requires: path Lv5+, UI path chosen, both body HP > 0."}
        }

    def activate_ui(self):
        self.ui_mode = True
        self.ui_timer = 3
        self.form = "ULTRA INSTINCT"
        self.heal(50)
        body_tag = "PERFECT BODY" if self.active_body == "perfect" else "TRUE BODY"
        return f"👁️👁️👁️ ULTRA INSTINCT [{body_tag}]! Eyes go black — reversed pupils! Body moves on pure instinct!"


class ZackLee(Character):
    def __init__(self):
        super().__init__("Zack Lee", "The Iron Boxer", 380, 280, [])
        self.canon_episode = 1
        self.paths_available = [Path.ZACK_IRON]
        self.affiliation = "J High"
        # HEAT MODE: canon — activates when Zack is overwhelmed.
        # In Heat Mode, Zack starts using techniques he never learned before,
        # including redirecting attacks. Impressive enough to make Mandeok get serious.
        # Mechanically: auto-triggers at ≤30% HP OR manually activated.
        # +60% dmg, +25% evasion, can redirect attacks (20% chance), 3 turns.
        self.heat_mode = False
        self.heat_mode_timer = 0
        self.heat_mode_triggered = False  # track if already auto-triggered this battle
        self.abilities = {
            # BUG-W1 FIX: was type="utility" — handler lives in atype=="buff" block, so buff never applied
            '1': {"name": "🔨 Iron Fortress Stance", "cost": 15, "dmg": (0, 0), "type": "buff",
                  "desc": "Defensive iron stance. -50% damage received for 2 turns."},
            '2': {"name": "🔨 Iron Fist", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Zack's fists become as hard as iron."},
            '3': {"name": "🥊 Jab", "cost": 15, "dmg": (35, 55), "type": "damage",
                  "desc": "Lightning-fast jab to measure distance."},
            '4': {"name": "🥊 Cross", "cost": 20, "dmg": (45, 70), "type": "damage",
                  "desc": "Full body weight behind this cross."},
            '5': {"name": "⚡ Counter Punch", "cost": 30, "dmg": (75, 110), "type": "damage",
                  "desc": "Zack's specialty. Waits for commitment, strikes with perfect timing."},
            '6': {"name": "💫 Shining Star", "cost": 50, "dmg": (100, 150), "type": "damage",
                  "desc": "Zack's ultimate technique. A blinding combination."}
        }


class JohanSeong(Character):
    def __init__(self, blind=True):
        super().__init__("Johan Seong", "The God Eye", 400, 300,
                         [Realm.TECHNIQUE, Realm.SPEED, Realm.OVERCOMING])
        self.canon_episode = 55
        self.affiliation = "God Dog"
        self.blind = blind
        self.god_eye_active = False
        self.god_eye_timer = 0
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
                  "desc": "Perfect boxing replication."},
            '3': {"name": "👁️ Copy: Karate", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Traditional Karate strikes."},
            '4': {"name": "👁️ Copy: Judo", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Judo throws with mechanical precision."},
            '5': {"name": "👁️ Copy: Aikido", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Aikido's flowing redirection."},
            '6': {"name": "👁️ Copy: Capoeira", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Dance-like Capoeira movements."},
            '7': {"name": "💃 Choreography: God Dog", "cost": 40, "dmg": (85, 120), "type": "damage",
                  "desc": "Johan's original style born from K-Pop choreography. A deadly dance."},
            '8': {"name": "💃 Choreography: Perfected", "cost": 45, "dmg": (95, 140), "type": "damage",
                  "desc": "The ultimate expression of his dance combat."},
            '9': {"name": "👁️ God Eye Activation", "cost": 30, "dmg": (0, 0), "type": "buff",
                  "desc": "Activates God Eye for 5 turns. +30% copy chance. Johan senses via vibration."},
            # MECH-7 FIX: Veinous Rage wired to Johan as his extreme-will ability
            'V': {"name": "👁️ Veinous Rage", "cost": 50, "dmg": (0, 0), "type": "buff",
                  "desc": "Johan pushes past his limits. Veins pulse visibly. +80% damage for 3 turns."},
        }
        if blind:
            self.abilities['P'] = {
                "name": "🕶️ Blindness (Overcoming)", "cost": 0, "dmg": (0, 0), "type": "passive",
                "desc": "Johan fights despite blindness. Other senses sharpen. +30% damage from overcoming."
            }
            self.title = "The Blind God Eye"

    def activate_god_eye(self):
        self.god_eye_active = True
        self.god_eye_timer = 5
        self.form = "GOD EYE AWAKENED"
        return "👁️👁️👁️ GOD EYE ACTIVATED for 5 turns! +30% copy chance!"

    def copy_technique(self, enemy_technique, target=None):
        if enemy_technique in self.technique_view_count:
            self.technique_view_count[enemy_technique] += 1
        else:
            self.technique_view_count[enemy_technique] = 1

        if enemy_technique in self.copied_techniques:
            # BUG-V2 FIX: if data dict is missing the entry (list/dict desync after save/load),
            # rebuild the data entry from scratch rather than dead-ending with a wrong message.
            if enemy_technique not in self.copied_techniques_data:
                new_views = self.technique_view_count[enemy_technique]
                base_dmg = 60
                view_bonus = min(50, new_views * 5)
                total_dmg = base_dmg + view_bonus
                # Find the first unused key slot for this technique
                existing_copy_keys = {v.get('key') for v in self.copied_techniques_data.values()}
                new_key = str(10 + self.copy_count)
                while new_key in existing_copy_keys or new_key in self.abilities:
                    new_key = str(int(new_key) + 1)
                self.abilities[new_key] = {
                    "name": f"👁️ Copy: {enemy_technique}",
                    "cost": 25,
                    "dmg": (total_dmg, total_dmg + 30),
                    "type": "damage",
                    "views": new_views,
                    "desc": (f"Johan's God Eye copies {enemy_technique}. "
                             f"Heard {new_views}×, dealing {total_dmg}-{total_dmg+30} dmg.")
                }
                self.copied_techniques_data[enemy_technique] = {
                    "key": new_key,
                    "views": new_views,
                    "damage": (total_dmg, total_dmg + 30)
                }
                return f"🔄 {enemy_technique} re-registered! (Heard {new_views}×)"
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
        super().from_dict(data)
        self.god_eye_active = data.get('god_eye_active', False)
        self.god_eye_timer = data.get('god_eye_timer', 0)
        self.copy_count = data.get('copy_count', 0)
        self.copied_techniques = data.get('copied_techniques', [])
        self.copied_techniques_data = data.get('copied_techniques_data', {})
        self.technique_view_count = data.get('technique_view_count', {})
        self.blind = data.get('blind', True)

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
        # RUNNER'S HIGH: Brekdak Forbidden Move #1.
        # Eyes go pale white, all stats doubled, sanity maintained. 2 turns.
        self.runners_high = False
        self.runners_high_timer = 0
        # HEAT MODE: VS Battles wiki — "Higher with Heat Mode."
        # Triggers when HP drops below 40% — passion/rage amplifier.
        self.heat_mode_active = False
        self.heat_mode_triggered = False  # once per battle auto-trigger
        self.affiliation = "Burn Knuckles"
        self.abilities = {
            '1': {"name": "🇷🇺 Systema: Ryabina", "cost": 20, "dmg": (50, 70), "type": "damage",
                  "desc": "Russian Systema vital-point strike learned from Sophia."},
            '2': {"name": "🇷🇺 Russian Cross", "cost": 35, "dmg": (75, 105), "type": "damage",
                  "desc": "Devastating Systema combination."},
            '3': {"name": "🇹🇭 Muay Thai: Death Blow", "cost": 40, "dmg": (90, 130), "type": "damage",
                  "desc": "Vasco's signature Muay Thai. A devastating elbow or knee that ends fights."},
            '4': {"name": "👊 Sunken Fist", "cost": 30, "dmg": (70, 100), "type": "damage",
                  "desc": "The fist that sank ships."},
            '5': {"name": "🔥 Hero's Resolve", "cost": 35, "dmg": (0, 0), "type": "buff",
                  "desc": "Vasco's burning heart. +40% dmg for 3 turns. Heals Vasco +25HP (passion overcomes injury)."}
        }


class JayHong(Character):
    def __init__(self):
        super().__init__("Jay Hong", "The Silent Blade", 380, 270, [])
        self.canon_episode = 1
        self.paths_available = [Path.JAY_KALI]
        self.affiliation = "J High / God Dog"
        self.abilities = {
            '1': {"name": "🇷🇺 Systema: Neutralizer", "cost": 20, "dmg": (45, 65), "type": "damage",
                  "desc": "A Systema counter. Jay neutralizes threats with silent efficiency."},
            '2': {"name": "🇵🇭 Kali: Double Baston", "cost": 25, "dmg": (50, 75), "type": "damage",
                  "desc": "Filipino Kali stick fighting. Twin weapons with deadly precision."},
            '3': {"name": "🇵🇭 Kali: Karambit", "cost": 30, "dmg": (65, 90), "type": "damage",
                  "desc": "The curved blade of Kali. Hooks around defenses devastatingly."},
            '4': {"name": "🛡️ Motorcycle Helmet", "cost": 15, "dmg": (0, 0), "type": "utility",
                  "desc": "Jay's signature defense. Helmet as shield — -50% damage for 1 turn."}
        }


class EliJang(Character):
    def __init__(self):
        # CANON-H FIX: Eli Jang realms set to [STRENGTH, OVERCOMING]
        super().__init__("Eli Jang", "The Wild", 410, 260, [Realm.STRENGTH, Realm.OVERCOMING])
        self.canon_episode = 150
        self.affiliation = "Hostel"
        self.paths_available = [Path.ELI_BEAST, Path.ELI_TOM_LEE]
        # IMPROVISED WEAPON: 25% chance to grab weapon (+50% dmg) after any attack.
        # Also: 15% chance to bind target with grabbed items.
        self.improvised_weapon_chance = 0.25
        self.abilities = {
            '1': {"name": "🐺 Wolf Strike", "cost": 20, "dmg": (50, 75), "type": "damage",
                  "desc": "Eli strikes like a wolf — sudden, savage, aimed at vital points."},
            '2': {"name": "🦅 Talon Kick", "cost": 25, "dmg": (60, 85), "type": "damage",
                  "desc": "A kick like an eagle's talon."},
            '3': {"name": "🦁 Beast Mode", "cost": 45, "dmg": (0, 0), "type": "buff",
                  "desc": "Unleashing his inner beast. +60% damage for 3 turns."},
            '4': {"name": "👴 Tom Lee Special", "cost": 40, "dmg": (85, 125), "type": "damage",
                  "desc": "The wild technique inherited from Tom Lee."}
        }

    def activate_beast_mode(self):
        self.beast_mode = True
        self.beast_timer = 3
        return "🦁🦁🦁 BEAST MODE! Eli abandons all technique for pure animal instinct! +60% damage!"


class WarrenChae(Character):
    def __init__(self):
        super().__init__("Warren Chae", "Gangdong's Mighty", 390, 260, [Realm.STRENGTH])
        self.canon_episode = 277
        self.affiliation = "Hostel"
        self.paths_available = [Path.WARREN_JKD, Path.WARREN_CQC, Path.WARREN_HEART]
        # CQC REDIRECT: Manager Kim taught Warren attack redirection (Ch.293).
        # Passive 25% chance to redirect incoming attack back at attacker.
        self.cqc_redirect_chance = 0.25
        self.exhausted = False
        # MENTOR'S LEGACY: after Full CQC Release, 20% chance Warren channels Manager Kim's form.
        self.mentors_legacy_chance = 0.20
        self.abilities = {
            '1': {"name": "🥋 Jeet Kune Do: Interception", "cost": 20, "dmg": (55, 80), "type": "damage",
                  "desc": "Bruce Lee's philosophy — intercepting before the attack fully forms."},
            '2': {"name": "🔫 CQC Foundation", "cost": 30, "dmg": (70, 100), "type": "damage",
                  "desc": "Close Quarters Combat fundamentals honed with Manager Kim."},
            '3': {"name": "⚡ NEW CQC: Full Release", "cost": 70, "dmg": (120, 170), "type": "damage",
                  "desc": "The complete CQC system unleashed. Causes exhaustion. 20% chance: Mentor's Legacy activates."},
            '4': {"name": "💔 Heart Attack Punch", "cost": 60, "dmg": (110, 160), "type": "damage",
                  "armor_break": True, "heart_attack": True,
                  "desc": "CANON: targets the heart directly. Always armor_break — bypasses ALL defense. One-inch heart punch."}
        }


class JakeKim(Character):
    def __init__(self):
        super().__init__("Jake Kim", "The Conviction", 430, 270, [Realm.OVERCOMING])
        self.canon_episode = 200
        self.affiliation = "Big Deal"
        self.paths_available = [Path.JAKE_CONVICTION, Path.JAKE_GAPRYONG]
        # CONVICTION STACKS: gains +10% dmg per hit taken below 50% HP (max 5).
        # At max stacks: leaves afterimages, +20% evasion bonus.
        self.conviction_stacks = 0
        self.max_conviction_stacks = 5
        self.abilities = {
            '1': {"name": "⚖️ Conviction Punch", "cost": 25, "dmg": (60, 85), "type": "damage",
                  "desc": "A punch backed by pure conviction."},
            '2': {"name": "👑 Inherited Will", "cost": 50, "dmg": (95, 140), "type": "damage",
                  "desc": "The will of Gapryong flows through his son."},
            '3': {"name": "👑 Gapryong's Blood", "cost": 70, "dmg": (120, 180), "type": "damage",
                  "desc": "Bloodline potential awakened."},
            '4': {"name": "⚖️ Conviction Mode", "cost": 45, "dmg": (0, 0), "type": "buff",
                  "desc": "State of pure conviction. +50% damage for 3 turns."}
        }


class GunPark(Character):
    def __init__(self):
        super().__init__("Gun Park", "The Black Bone", 500, 320,
                         [Realm.STRENGTH, Realm.TECHNIQUE])
        self.canon_episode = 300
        self.affiliation = "Ten Geniuses / Yamazaki Syndicate"
        self.paths_available = [Path.GUN_YAMAZAKI, Path.GUN_CONSTANT_UI]
        self.permanent_ui = True
        self.abilities = {
            '1': {"name": "🥋 Taekwondo: Roundhouse", "cost": 20, "dmg": (65, 90), "type": "damage",
                  "desc": "Gun's Taekwondo mastery."},
            '2': {"name": "🥋 Kyokushin: Straight", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "desc": "The straight punch of Kyokushin Karate."},
            '3': {"name": "🖤 Black Bone", "cost": 70, "dmg": (130, 200), "type": "damage",
                  "desc": "The legendary Yamazaki technique."},
            '4': {"name": "👁️ Constant UI [PASSIVE — always +30%]", "cost": 0, "dmg": (0, 0), "type": "passive",
                  "desc": "Gun exists in perpetual Ultra Instinct. Always active: +30% to all damage."}
        }

    def get_damage_multiplier(self):
        mult, buffs = super().get_damage_multiplier()
        if self.permanent_ui:
            mult *= 1.3
            buffs.append("👁️ CONSTANT UI")
        return mult, buffs


class GooKim(Character):
    def __init__(self):
        super().__init__("Goo Kim", "The Moonlight Sword", 480, 300, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 300
        self.affiliation = "Ten Geniuses / 1.5 Generation"
        self.paths_available = [Path.GOO_MOONLIGHT, Path.GOO_FIFTH]
        self.abilities = {
            '1': {"name": "🖊️ Pen Sword", "cost": 15, "dmg": (45, 70), "type": "damage",
                  "desc": "Goo's signature — even a pen becomes lethal in his hands."},
            '2': {"name": "🌙 First Sword: Early Moon", "cost": 30, "dmg": (75, 105), "type": "damage",
                  "desc": "Rising crescent slash."},
            '3': {"name": "🌓 Second Sword: Crescent Moon", "cost": 35, "dmg": (80, 115), "type": "damage",
                  "desc": "Sweeping horizontal slash."},
            '4': {"name": "🌕 Third Sword: Full Moon", "cost": 45, "dmg": (100, 145), "type": "damage",
                  "desc": "Complete circular motion striking from all directions."},
            '5': {"name": "🌑 Zero Sword: Lunar Eclipse", "cost": 60, "dmg": (130, 190), "type": "counter",
                  "desc": "Ultimate counter. Perfect stillness, then strikes."},
            '6': {"name": "✨ Fifth Sword", "cost": 90, "dmg": (170, 250), "type": "damage",
                  "desc": "The legendary fifth sword. A technique that shouldn't exist."}
        }


class KimJungu(Character):
    def __init__(self):
        super().__init__("Kim Jun-gu", "The Hwarang Sword", 520, 290, [Realm.TECHNIQUE, Realm.SPEED])
        self.canon_episode = 500
        self.affiliation = "Independent"
        self.paths_available = [Path.JOONGOO_HWARANG, Path.JOONGOO_ARMED]
        # PEN AS SWORD: precision vital-point targeting. Pen Pierce = always armor_break.
        self.abilities = {
            '1': {"name": "🖊️ Pen Pierce", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "armor_break": True, "vital_strike": True,
                  "desc": "CANON: precision vital-point targeting — even a pen is lethal. Always armor_break."},
            '2': {"name": "🔗 Chain Whip", "cost": 30, "dmg": (75, 110), "type": "damage",
                  "desc": "Flexible chain weapon. Unpredictable reach."},
            '3': {"name": "⚔️ Hwarang Sword", "cost": 60, "dmg": (140, 210), "type": "damage",
                  "armor_break": True,
                  "desc": "Ancient Hwarang sword technique — targets vital arteries."},
            '4': {"name": "⚔️ Hwarang: Blade Dance", "cost": 70, "dmg": (160, 240), "type": "damage",
                  "armor_break": True,
                  "desc": "Ultimate Hwarang technique — relentless vital-point assault."},
            '5': {"name": "🖊️ Vital Point: Bleeding", "cost": 45, "dmg": (90, 130), "type": "debilitate",
                  "armor_break": True,
                  "desc": "Targets nerve clusters and artery pressure points. Enemy takes +20% dmg for 2 turns."}
        }


class ManagerKim(Character):
    def __init__(self):
        super().__init__("Manager Kim", "The Senior Manager", 480, 300,
                         [Realm.TECHNIQUE, Realm.TENACITY, Realm.STRENGTH])
        self.canon_episode = 290
        self.code_66 = True
        self.veinous_rage = False
        self.silver_yarn_active = False
        self.paths_available = [Path.MANAGER_KIM_CQC]
        self.abilities = {
            '1': {"name": "🎖️ Special Forces Training [PASSIVE +10%]", "cost": 0, "dmg": (0, 0), "type": "passive",
                  "desc": "Manager Kim's military background. Always combat-ready. Passive: +10% all damage."},
            '2': {"name": "🔫 CQC: Vital Strikes", "cost": 25, "dmg": (65, 90), "type": "damage",
                  "desc": "Close Quarters Combat targeting vital points."},
            '3': {"name": "⚪ Silver Yarn: Thread Bind", "cost": 20, "dmg": (0, 0), "type": "utility",
                  "desc": "Silver yarn binds opponents. 60% immobilize chance. Activates silver_yarn status."},
            '4': {"name": "66 CODE: Full Release", "cost": 70, "dmg": (130, 190), "type": "damage",
                  "desc": "The legendary Code 66. Manager Kim's ultimate."}
        }

    def get_damage_multiplier(self):
        mult, buffs = super().get_damage_multiplier()
        mult *= 1.1
        buffs.append("🎖️ SF TRAINING")
        # MECH-8 FIX: silver_yarn gives +20% damage while active (threads restrict enemy movement)
        if self.silver_yarn_active:
            mult *= 1.2
            buffs.append(f"⚪ YARN({self.silver_yarn_timer}T)")
        return mult, buffs


CapGuy = ManagerKim


# ===== WORKERS =====

class Mandeok(Character):
    def __init__(self):
        super().__init__("Mandeok Bang", "The Titan", 480, 300, [Realm.STRENGTH])
        self.canon_episode = 400
        self.paths_available = [Path.MANDEOK_POWER]
        # IMMOVABLE: 20% innate damage reduction (titan mass).
        self.immovable_reduction = 0.20
        self.abilities = {
            '1': {"name": "💪 Power Punch", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "A punch backed by titanic strength."},
            '2': {"name": "🌍 Earth Shaker", "cost": 40, "dmg": (110, 160), "type": "damage",
                  "desc": "Mandeok strikes the ground, creating destabilizing shockwaves."},
            '3': {"name": "🗿 Titan Strike", "cost": 50, "dmg": (130, 190), "type": "damage",
                  "desc": "The full power of the Titan."},
            # MECH-9 FIX: Titan Boost ability wires muscle_boost
            '4': {"name": "💪 Titan Boost", "cost": 35, "dmg": (0, 0), "type": "buff",
                  "desc": "Mandeok pumps up to maximum capacity. +30% damage for 3 turns."}
        }

    def activate_titan_boost(self):
        self.muscle_boost = True
        self.muscle_boost_timer = 3
        return "💪💪💪 TITAN BOOST! Mandeok swells to maximum capacity! +30% damage for 3 turns!"


class Xiaolung(Character):
    def __init__(self):
        super().__init__("Xiaolung", "Muay Thai Genius", 440, 280, [Realm.SPEED, Realm.STRENGTH])
        self.canon_episode = 400
        self.paths_available = [Path.XIAOLUNG_MUAY_THAI]
        self.affiliation = "Workers"
        # THAI CLINCH: grabbing opponent's head and delivering repeated knees.
        # Clinch_active adds free knee follow-up after each attack for 2 turns.
        self.clinch_active = False
        self.clinch_timer = 0
        self.abilities = {
            '1': {"name": "🇹🇭 Muay Thai: Elbow", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "The sharpest elbow weapon in Muay Thai — harder than any punch."},
            '2': {"name": "🇹🇭 Muay Thai: Knee", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Devastating rising knee from the clinch."},
            '3': {"name": "🇹🇭 Thai Clinch", "cost": 30, "dmg": (90, 130), "type": "clinch",
                  "desc": "CANON: Thai plum clinch — controls head, delivers knees/elbows. For 2 turns, every attack triggers free knee follow-up (50% dmg)."},
            '4': {"name": "🇹🇭 Muay Thai Mastery", "cost": 50, "dmg": (130, 180), "type": "damage",
                  "desc": "Complete 8-limb arsenal — fists, elbows, knees, shins. The art of 8 limbs."},
            '5': {"name": "🇹🇭 8 Limbs Barrage", "cost": 70, "dmg": (160, 220), "type": "damage",
                  "desc": "All 8 Muay Thai weapons unleashed simultaneously. Strikes from all angles."}
        }


class Ryuhei(Character):
    def __init__(self):
        super().__init__("Ryuhei", "Yakuza Executive", 430, 270, [Realm.TECHNIQUE])
        self.canon_episode = 400
        self.affiliation = "Workers (Yakuza)"
        self.paths_available = [Path.RYUHEI_YAKUZA]
        # GANG BACKUP: Ryuhei can call on yakuza subordinates.
        # 30% chance each attack triggers Gang Backup bonus hit (45% dmg).
        self.gang_backup_chance = 0.30
        self.abilities = {
            '1': {"name": "⚔️ Yakuza Strike", "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Dirty effective street fighting — no honor, maximum efficiency."},
            '2': {"name": "🏴 Gang Style", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "Organized crime: multiple strikes, improvised weapons, psychological pressure."},
            '3': {"name": "⚫ Yakuza Finisher", "cost": 40, "dmg": (120, 170), "type": "damage",
                  "desc": "Ruthless yakuza execution — targets vital organs."},
            '4': {"name": "😈 Yakuza Intimidation", "cost": 20, "dmg": (0, 0), "type": "utility",
                  "desc": "Yakuza psychological warfare. 45% stun chance (paralyzed by fear of the organization)."}
        }


class SamuelSeo(Character):
    def __init__(self):
        super().__init__("Samuel Seo", "The Betrayer", 460, 290, [Realm.STRENGTH, Realm.TENACITY])
        self.canon_episode = 300
        self.affiliation = "Workers"
        self.paths_available = [Path.SAMUEL_AMBITION]
        # SELF-HATRED: below 40% HP, damage x2.0 (self-loathing = rage amplifier).
        self.self_hatred_active = False
        # AMBUSH READY: first attack of each battle has +50% bonus (betrayer always strikes first).
        self.ambush_available = True
        self.abilities = {
            '1': {"name": "👑 King's Ambition", "cost": 30, "dmg": (90, 130), "type": "damage",
                  "desc": "Burning ambition — every strike powered by the need to be king."},
            '2': {"name": "💢 Betrayal", "cost": 25, "dmg": (80, 120), "type": "damage",
                  "ambush": True,
                  "desc": "CANON: dirty ambush strike. If ambush_available, +50% first-strike bonus."},
            '3': {"name": "⚡ Workers Executive", "cost": 40, "dmg": (120, 170), "type": "damage",
                  "desc": "Power of a Workers executive — durability + animal instinct."},
            '4': {"name": "👑 Path to Kingship", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "All ambition poured into one strike. Scales with self-hatred."},
            '5': {"name": "💢 Self-Hatred Mode", "cost": 40, "dmg": (0, 0), "type": "buff",
                  "desc": "Below 40% HP: Samuel's self-loathing becomes power. +100% dmg for 2 turns."}
        }


class SinuHan(Character):
    def __init__(self):
        super().__init__("Sinu Han", "The Ghost", 420, 280, [Realm.SPEED, Realm.TECHNIQUE])
        self.canon_episode = 300
        self.paths_available = [Path.SINU_INVISIBLE]
        # INVISIBLE ATTACKS: Speed+Technique mastery combined. Taesoo says his invisible
        # attacks are "a level of mastery greater than his requiring great speed."
        # Sinu is in the God tier — scales to James Lee.
        # ALL attacks are invisible = armor_break.
        # ATTACK REDIRECT (Ch.422): redirects attacks with a pinky. 35% passive redirect.
        self.redirect_chance = 0.35
        self.ghost_form_active = False
        self.ghost_form_timer = 0
        self.affiliation = "Workers"
        self.abilities = {
            '1': {"name": "🌀 Invisible Punch", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "armor_break": True,
                  "desc": "CANON: speed+technique mastery = invisible. Cannot be blocked or defended against."},
            '2': {"name": "🌀 Invisible Kick", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "armor_break": True,
                  "desc": "Invisible kick — combination of speed and technique mastery. Impossible to defend."},
            '3': {"name": "🌀 Ghost Fist", "cost": 45, "dmg": (120, 170), "type": "damage",
                  "armor_break": True,
                  "desc": "The ultimate invisible attack. Even masters can't see it coming."},
            '4': {"name": "🌀 Ghost Form", "cost": 60, "dmg": (0, 0), "type": "buff",
                  "desc": "CANON: Sinu enters pure ghost state. 3 turns: all attacks armor_break + 25% dodge + 40% redirect chance."}
        }


class LoganLee(Character):
    def __init__(self):
        super().__init__("Logan Lee", "The Bully", 350, 220, [])
        self.canon_episode = 1
        self.affiliation = "J High"
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
        super().__init__("Vin Jin", "King of Heavens", 440, 270, [Realm.STRENGTH])
        self.canon_episode = 500
        self.affiliation = "Workers / Cheonliang"
        self.paths_available = [Path.VIN_JIN_SSIREUM]
        # GLASSES OFF: removing sunglasses signals power escalation.
        # When glasses off: +60% dmg. Kani Basami causes bind. Mujin can uproot trees.
        # CBR: "after training and skipping the glasses, Vin Jin became one of the strongest of Gen 2."
        self.glasses_on = True
        self.abilities = {
            '1': {"name": "🥋 Judo: Kani Basami",     "cost": 25, "dmg": (70, 110), "type": "damage",
                  "bind_chance": 0.40,
                  "desc": "CANON: forbidden scissors throw. 40% bind — legs locked around opponent, immobilized."},
            '2': {"name": "🥋 Kudo: Bone Crusher",   "cost": 25, "dmg": (70, 110), "type": "damage",
                  "desc": "Kudo: superhuman grip strength crushes bones. Immense raw power."},
            '3': {"name": "🇰🇷 Mujin Ssireum",        "cost": 35, "dmg": (95, 140), "type": "damage",
                  "bind_chance": 0.50,
                  "desc": "Bone-breaking grip — uproots full-grown trees. 50% bind chance."},
            '4': {"name": "🕶️ Glasses Off: Frenzy",  "cost": 40, "dmg": (110, 155), "type": "damage",
                  "desc": "Without sunglasses: restraint gone. Wild, savage striking."},
            '5': {"name": "🕶️ Sunglasses Off",        "cost": 55, "dmg": (0, 0), "type": "buff",
                  "desc": "CANON: Vin Jin removes sunglasses — this is his power-up moment. +60% dmg for 3 turns. Glasses_off state active."}
        }

    def activate_sunglasses_off(self):
        self.glasses_on = False
        self.beast_mode = True
        self.beast_timer = 3
        return "🕶️🕶️🕶️ SUNGLASSES OFF! Vin Jin's restraint shatters! +60% damage for 3 turns!"


class HanJaeha(Character):
    def __init__(self):
        super().__init__("Han Jaeha", "Cheonliang Wrestler", 380, 240, [])
        self.canon_episode = 500
        self.paths_available = [Path.HAN_JAEHA]
        self.affiliation = "Cheonliang"
        # GRAPPLER: throws can bind the opponent (pinned on the ground).
        self.abilities = {
            '1': {"name": "🤼 Traditional Throw", "cost": 20, "dmg": (60, 90), "type": "damage",
                  "bind_chance": 0.35,
                  "desc": "Classic ssireum throw — 35% bind (slammed to ground, pinned)."},
            '2': {"name": "🤼 Grapple Lock", "cost": 25, "dmg": (70, 100), "type": "damage",
                  "bind_chance": 0.50,
                  "desc": "Controlling grapple lock — 50% bind. Opponent completely immobilized."},
            '3': {"name": "🤼 Cheonliang Pride", "cost": 35, "dmg": (100, 140), "type": "damage",
                  "desc": "Traditional Cheonliang wrestling — pride technique."},
            '4': {"name": "🤼 Champion's Throw", "cost": 50, "dmg": (130, 175), "type": "damage",
                  "bind_chance": 0.80,
                  "desc": "Cheonliang champion's ultimate throw. Massive damage + 80% bind. Completely dominates the opponent."}
        }


class BaekSeong(Character):
    def __init__(self):
        super().__init__("Baek Seong", "Taekkyon Dancer", 370, 250, [])
        self.canon_episode = 500
        self.paths_available = [Path.BAEK_SEONG_TAEKKYON]
        self.affiliation = "Cheonliang"
        # TAEKKYON RHYTHM: consecutive attacks build rhythm stacks, each +15% dmg.
        # Missing a turn (defending, stunned) resets rhythm.
        self.rhythm_stacks = 0
        self.last_acted = False   # reset to False in cleanup if missed a turn
        self.abilities = {
            '1': {"name": "🦢 Flowing Step", "cost": 20, "dmg": (50, 80), "type": "dance",
                  "desc": "Graceful Taekkyon footwork — flowing rhythm. Builds rhythm stack (+15% dmg per stack)."},
            '2': {"name": "🦢 Taekkyon Kick", "cost": 25, "dmg": (70, 100), "type": "dance",
                  "desc": "Traditional Taekkyon kick — keeps the rhythm going."},
            '3': {"name": "🦢 Dance of Blades", "cost": 40, "dmg": (110, 150), "type": "dance",
                  "desc": "Taekkyon's ultimate form — best with high rhythm."},
            '4': {"name": "🦢 Rhythm Break", "cost": 35, "dmg": (90, 130), "type": "dance",
                  "desc": "CANON: Taekkyon uses rhythm and misdirection. Surprise rhythm break — enemy loses defensive stance. 35% stun."}
        }


# ===== YAMAZAKI =====

class ShingenYamazaki(Character):
    def __init__(self):
        # CANON-L FIX: Shingen is not a Korean Gyeongji user — realm_list=[]
        super().__init__("Shingen Yamazaki", "Yamazaki Head", 650, 380, [])
        self.canon_episode = 0
        self.affiliation = "Yamazaki Syndicate"
        self.paths_available = [Path.SHINGEN_YAMAZAKI]
        # PATRIARCH'S AURA: Gen 0 Yamazaki head. His presence reduces enemy aggression.
        # Passive: all enemies deal 15% less damage (overwhelming intimidation).
        # INHERITED DARKNESS: nuclear option — channels all of Yamazaki clan's power.
        # Costs 40HP self-damage but deals catastrophic damage.
        self.patriarch_aura = True
        self.abilities = {
            '1': {"name": "🏯 Yamazaki Style", "cost": 40, "dmg": (130, 180), "type": "damage",
                  "desc": "Fundamental Yamazaki clan techniques."},
            '2': {"name": "🏯 Syndicate's Wrath", "cost": 55, "dmg": (170, 220), "type": "damage",
                  "desc": "Collective fury of the Yamazaki Syndicate behind each strike."},
            '3': {"name": "🏯 Black Bone", "cost": 70, "dmg": (210, 270), "type": "damage",
                  "desc": "The legendary Black Bone technique — passed to Gun Park."},
            '4': {"name": "🏯 Inherited Darkness", "cost": 85, "dmg": (300, 380), "type": "patriarch_ultimate",
                  "desc": "NUCLEAR OPTION: Shingen channels ALL of the Yamazaki clan's darkness. -40HP self-damage but devastating. Gen 0 patriarch's true power."}
        }


class ParkFather(Character):
    def __init__(self):
        super().__init__("Park Jonggun's Father", "⚠️ Fan Creation — Unconfirmed in Manhwa", 550, 340,
                         [Realm.STRENGTH, Realm.TECHNIQUE])
        self.canon_episode = 0
        self.affiliation = "Unknown"
        self.paths_available = [Path.PARK_FATHER]
        self.abilities = {
            '1': {"name": "❓ Unknown Technique", "cost": 35, "dmg": (110, 160), "type": "damage",
                  "desc": "A mysterious technique lost to time."},
            '2': {"name": "❓ Bloodline Secret", "cost": 50, "dmg": (150, 200), "type": "damage",
                  "desc": "The secret of the Park bloodline."},
            '3': {"name": "❓ Father's Shadow", "cost": 65, "dmg": (190, 250), "type": "damage",
                  "desc": "The shadow of the father looms large."}
        }


# ===== LAW ENFORCEMENT =====

class KimMinjae(Character):
    def __init__(self):
        super().__init__("Kim Minjae", "Police Officer", 380, 240, [Realm.TECHNIQUE])
        self.canon_episode = 200
        self.paths_available = [Path.KIM_MINJAE_JUDO]
        self.abilities = {
            '1': {"name": "🥋 Judo Throw", "cost": 20, "dmg": (50, 80), "type": "damage",
                  "desc": "A clean Judo throw."},
            '2': {"name": "🥋 Ippon Seoi Nage", "cost": 30, "dmg": (80, 120), "type": "damage",
                  "desc": "One-arm shoulder throw."},
            '3': {"name": "🥋 Police Training", "cost": 35, "dmg": (90, 130), "type": "damage",
                  "desc": "Years of police training."}
        }


class DetectiveKang(Character):
    def __init__(self):
        super().__init__("Detective Kang", "Veteran Detective", 390, 250, [Realm.SPEED])
        self.canon_episode = 200
        self.paths_available = [Path.DETECTIVE_KANG_BOXING]
        self.affiliation = "Law Enforcement"
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
    abilities = {'1': {"name": "Fist Strike", "dmg": (25, 40), "cost": 15, "desc": "A basic punch."}}
    e = Enemy("Frame Soldier", "Elite Grunt", 150, 100, abilities, 100, "Frame")
    e.ai_pattern = ['1']
    return e

def create_enemy_jhigh_bully():
    abilities = {'1': {"name": "School Punch", "dmg": (20, 35), "cost": 10, "desc": "A bully's punch."}}
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
        '1': {"name": "Jab", "dmg": (35, 55), "cost": 15, "desc": "Lightning jab."},
        '2': {"name": "Cross", "dmg": (45, 70), "cost": 20, "desc": "Full body weight cross."},
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
        '2': {"name": "👁️ Copy: Boxing",    "dmg": (50, 75), "cost": 20, "desc": "Champion-level boxing."},
        '3': {"name": "👁️ Copy: Karate",    "dmg": (50, 75), "cost": 20, "desc": "Traditional Karate strikes."},
        '4': {"name": "💃 Choreography: God Dog", "dmg": (85, 120), "cost": 40, "desc": "Dance combat performance."},
        '5': {"name": "👁️ God Eye",          "dmg": (95, 140), "cost": 45, "desc": "The God Eye awakens."}
    }
    e = Enemy("Johan Seong", "The God Eye", 400, 300, abilities, 15, "God Dog")
    e.ai_pattern = ['5', '4', '3', '2', '1']
    e.blind = True
    return e

def create_enemy_eli_jang_enemy():
    abilities = {
        '1': {"name": "Animal Strike", "dmg": (50, 75), "cost": 20, "desc": "Unpredictable savage strike."},
        '2': {"name": "Talon Kick",    "dmg": (60, 85), "cost": 25, "desc": "Eagle talon kick."},
        '3': {"name": "Beast Mode",    "dmg": (85, 120), "cost": 45, "desc": "Pure animal instinct unleashed."}
    }
    e = Enemy("Eli Jang", "The Wild", 410, 260, abilities, 16, "Hostel")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_warren_chae_enemy():
    abilities = {
        '1': {"name": "JKD: Interception", "dmg": (60, 85),  "cost": 20, "desc": "Jeet Kune Do interception."},
        '2': {"name": "Shield Strike",     "dmg": (65, 90),  "cost": 25, "desc": "Shield as weapon."},
        '3': {"name": "Counter",           "dmg": (70, 100), "cost": 30, "desc": "Perfectly timed counter."},
        '4': {"name": "NEW CQC",           "dmg": (90, 130), "cost": 70, "desc": "Complete CQC system."}
    }
    e = Enemy("Warren Chae", "Hostel Executive", 390, 260, abilities, 30, "Hostel")
    e.ai_pattern = ['4', '3', '2', '1']
    return e

def create_enemy_jake_kim_enemy():
    abilities = {
        '1': {"name": "Conviction Punch", "dmg": (60, 85),   "cost": 25, "desc": "Punch backed by conviction."},
        '2': {"name": "Inherited Will",   "dmg": (95, 140),  "cost": 50, "desc": "Gapryong's will."},
        '3': {"name": "Gapryong's Blood", "dmg": (120, 180), "cost": 70, "desc": "Bloodline power awakened."}
    }
    e = Enemy("Jake Kim", "The Conviction", 430, 270, abilities, 12, "Big Deal")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_jerry_kwon():
    abilities = {
        '1': {"name": "Gift Punch",     "dmg": (65, 95),  "cost": 30, "desc": "Strength given as a gift from Jake."},
        '2': {"name": "Rhino Charge",   "dmg": (70, 105), "cost": 35, "desc": "Charges like a rhino."},
        '3': {"name": "Loyalty to Jake","dmg": (80, 115), "cost": 40, "desc": "Loyalty pushes beyond limits."}
    }
    e = Enemy("Jerry Kwon", "Big Deal Executive", 420, 250, abilities, 25, "Big Deal")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_sally():
    abilities = {
        '1': {"name": "Sally Special",  "dmg": (45, 70), "cost": 20, "desc": "Unorthodox but effective style."},
        '2': {"name": "Family Support", "dmg": (40, 65), "cost": 15, "desc": "Fighting for family."}
    }
    e = Enemy("Sally", "Hostel Manager", 320, 200, abilities, 60, "Hostel")
    e.ai_pattern = ['1', '2']
    return e

def create_enemy_brad():
    abilities = {
        '1': {"name": "Brad Punch",       "dmg": (50, 75), "cost": 20, "desc": "Straightforward strength."},
        '2': {"name": "Big Deal Loyalty", "dmg": (55, 80), "cost": 25, "desc": "Loyalty pushes harder."}
    }
    e = Enemy("Brad", "Big Deal Member", 350, 220, abilities, 55, "Big Deal")
    e.ai_pattern = ['2', '1']
    return e

def create_enemy_jace_park():
    abilities = {
        '1': {"name": "Strategy",       "dmg": (40, 60), "cost": 15, "desc": "Strategic mind finds openings."},
        '2': {"name": "Tactical Strike","dmg": (45, 70), "cost": 20, "desc": "Planned tactical strike."}
    }
    e = Enemy("Jace Park", "Burn Knuckles Strategist", 330, 210, abilities, 58, "Burn Knuckles")
    e.ai_pattern = ['2', '1']
    return e

def create_enemy_burn_knuckles():
    abilities = {
        '1': {"name": "Burn Knuckle Punch","dmg": (35, 55), "cost": 15, "desc": "Fueled by burning justice."},
        '2': {"name": "Justice Strike",    "dmg": (40, 60), "cost": 20, "desc": "Striking for justice."}
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
        '1': {"name": "Power Strike", "dmg": (40, 60), "cost": 20, "desc": "Elite member strike."},
        '2': {"name": "Crew Combo",   "dmg": (45, 65), "cost": 25, "desc": "Combination attack."}
    }
    e = Enemy("God Dog Elite", "Crew Veteran", 200, 140, abilities, 75, "God Dog")
    e.ai_pattern = ['2', '1']
    return e

def create_enemy_hostel_member():
    abilities = {
        '1': {"name": "Street Fighting","dmg": (35, 55), "cost": 20, "desc": "Dirty street fighting."},
        '2': {"name": "Ambush",         "dmg": (40, 60), "cost": 25, "desc": "Guerilla ambush tactics."}
    }
    e = Enemy("Hostel Member", "Family Crew", 170, 120, abilities, 80, "Hostel")
    e.ai_pattern = ['2', '1']
    return e

def create_enemy_big_deal_member():
    abilities = {
        '1': {"name": "Fist Strike",   "dmg": (30, 50), "cost": 15, "desc": "Fighting for Big Deal family."},
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
        '1': {"name": "Affiliate Technique","dmg": (60, 85), "cost": 25, "desc": "Unique affiliate skills."},
        '2': {"name": "Corporate Power",    "dmg": (65, 95), "cost": 30, "desc": "Full Workers backing."}
    }
    e = Enemy("Workers Affiliate", "1st Affiliate", 360, 230, abilities, 42, "Workers")
    e.ai_pattern = ['2', '1']
    return e

def create_enemy_eugene():
    abilities = {
        '1': {"name": "Corporate Strategy","dmg": (30, 50), "cost": 20, "desc": "Finds weaknesses."},
        '2': {"name": "Workers' Orders",   "dmg": (35, 55), "cost": 25, "desc": "Commands respect."}
    }
    e = Enemy("Eugene", "Workers Executive", 300, 250, abilities, 65, "Workers")
    e.ai_pattern = ['2', '1']
    return e

def create_enemy_xiaolung():
    abilities = {
        '1': {"name": "🇹🇭 Muay Thai: Elbow",   "dmg": (80, 120),  "cost": 30, "desc": "Elbow strikes."},
        '2': {"name": "🇹🇭 Muay Thai: Knee",    "dmg": (85, 125),  "cost": 30, "desc": "Devastating knee strikes."},
        '3': {"name": "🇹🇭 Thai Clinch",        "dmg": (75, 110),  "cost": 25, "desc": "Controls while delivering knees."},
        '4': {"name": "🇹🇭 Muay Thai Mastery",  "dmg": (110, 170), "cost": 50, "desc": "Complete Muay Thai arsenal."}
    }
    e = Enemy("Xiaolung", "Muay Thai Genius", 550, 300, abilities, 14, "Workers")
    e.ai_pattern = ['4', '1', '2', '3']
    return e

def create_enemy_mandeok():
    abilities = {
        '1': {"name": "💪 Power Punch",  "dmg": (90, 130),  "cost": 35, "desc": "Titanic strength punch."},
        '2': {"name": "🌍 Earth Shaker", "dmg": (100, 150), "cost": 40, "desc": "Ground-shaking shockwaves."},
        '3': {"name": "🗿 Titan Strike", "dmg": (120, 180), "cost": 50, "desc": "Full Titan power."}
    }
    e = Enemy("Mandeok Bang", "The Titan", 600, 280, abilities, 13, "Workers")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_vin_jin():
    abilities = {
        '1': {"name": "🥋 Judo: Kani Basami",       "dmg": (75, 110),  "cost": 30, "desc": "Forbidden scissors throw — breaks knees."},
        '2': {"name": "🥋 Kudo: Bone Crusher",       "dmg": (70, 105),  "cost": 30, "desc": "Grip + Kudo — shatters bones."},
        '3': {"name": "🇰🇷 Mujin Ssireum",           "dmg": (90, 130),  "cost": 35, "desc": "Jin Mujin's bone-breaking wrestling."},
        '4': {"name": "🕶️ Glasses Off: Frenzy",      "dmg": (100, 145), "cost": 40, "desc": "Sunglasses off — speed and power multiply."},
        '5': {"name": "🕶️ Sunglasses Off",            "dmg": (110, 160), "cost": 50, "desc": "King of Heavens. Full power."}
    }
    e = Enemy("Vin Jin", "King of Heavens", 520, 280, abilities, 28, "Cheonliang")
    e.ai_pattern = ['5', '4', '3', '2', '1']
    return e

def create_enemy_ryuhei():
    abilities = {
        '1': {"name": "⚔️ Yakuza Strike",  "dmg": (80, 115),  "cost": 30, "desc": "Dirty yakuza style."},
        '2': {"name": "🏴 Gang Style",     "dmg": (85, 120),  "cost": 35, "desc": "Organized crime tactics."},
        '3': {"name": "⚫ Yakuza Finisher", "dmg": (100, 150), "cost": 45, "desc": "Ruthless yakuza execution technique."}
    }
    e = Enemy("Ryuhei", "Yakuza Executive", 540, 290, abilities, 24, "Workers")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_samuel_seo():
    abilities = {
        '1': {"name": "👑 King's Ambition",    "dmg": (85, 125),  "cost": 35, "desc": "Burning ambition."},
        '2': {"name": "💢 Betrayal",           "dmg": (80, 120),  "cost": 30, "desc": "Cheap shot from betrayal."},
        '3': {"name": "⚡ Workers Executive",  "dmg": (95, 140),  "cost": 40, "desc": "Executive-level power."},
        '4': {"name": "👑 Path to Kingship",   "dmg": (110, 170), "cost": 50, "desc": "All ambition in one strike."}
    }
    e = Enemy("Samuel Seo", "The Betrayer", 560, 300, abilities, 18, "Workers")
    e.ai_pattern = ['4', '3', '1', '2']
    return e

def create_enemy_taesoo_ma():
    abilities = {
        '1': {"name": "🔴 Right Hand", "dmg": (110, 170), "cost": 45, "desc": "Legendary right fist."},
        '2': {"name": "🔴 Ansan King", "dmg": (120, 180), "cost": 50, "desc": "King's ultimate strike."}
    }
    e = Enemy("Taesoo Ma", "King of Ansan", 580, 300, abilities, 8, "1st Gen")
    e.ai_pattern = ['2', '1']
    return e

def create_enemy_gongseob_ji():
    abilities = {
        '1': {"name": "🩷 Speed Technique","dmg": (95, 140),  "cost": 40, "desc": "Blazing fast strikes."},
        '2': {"name": "🩷 Vice King",      "dmg": (100, 150), "cost": 45, "desc": "Pride of the Vice King."}
    }
    e = Enemy("Gongseob Ji", "King of Daegu", 500, 280, abilities, 11, "1st Gen")
    e.ai_pattern = ['2', '1']
    return e

def create_enemy_jichang_kwak():
    abilities = {
        '1': {"name": "🩷 Hand Blade", "dmg": (100, 155), "cost": 40, "desc": "Hand becomes a blade."},
        '2': {"name": "👑 Seoul King", "dmg": (110, 170), "cost": 50, "desc": "Pride of Seoul's king."}
    }
    e = Enemy("Jichang Kwak", "The White Viper", 550, 300, abilities, 7, "1st Gen")
    e.ai_pattern = ['2', '1']
    return e

def create_enemy_gun_park_enemy():
    abilities = {
        '1': {"name": "Taekwondo", "dmg": (65, 90),   "cost": 25, "desc": "Spinning kicks."},
        '2': {"name": "Kyokushin", "dmg": (70, 100),  "cost": 30, "desc": "Power from hip rotation."},
        '3': {"name": "Black Bone","dmg": (130, 200),  "cost": 70, "desc": "The legendary Yamazaki technique."}
    }
    e = Enemy("Gun Park", "The Black Bone", 500, 320, abilities, 5, "Independent")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_goo_kim_enemy():
    abilities = {
        '1': {"name": "Makeshift Sword","dmg": (45, 70),   "cost": 20, "desc": "Anything becomes a sword."},
        '2': {"name": "Full Moon",       "dmg": (100, 145), "cost": 45, "desc": "Complete circular slash."},
        '3': {"name": "Fifth Sword",     "dmg": (170, 250), "cost": 90, "desc": "A technique that shouldn't exist."}
    }
    e = Enemy("Goo Kim", "The Moonlight Sword", 480, 300, abilities, 5, "Independent")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_kim_jungu_enemy():
    abilities = {
        '1': {"name": "Improvised Weapon","dmg": (70, 100),  "cost": 30, "desc": "Deadly creativity."},
        '2': {"name": "Hwarang Sword",    "dmg": (140, 210), "cost": 60, "desc": "Ancient Hwarang technique."},
        '3': {"name": "Blade Dance",      "dmg": (160, 240), "cost": 70, "desc": "Ultimate blade dance."}
    }
    e = Enemy("Kim Jun-gu", "The Hwarang Sword", 520, 290, abilities, 4, "Independent")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_manager_kim_enemy():
    abilities = {
        '1': {"name": "CQC Strike",  "dmg": (65, 90),   "cost": 25, "desc": "Precise CQC vital-point strike."},
        '2': {"name": "Silver Yarn", "dmg": (100, 140),  "cost": 20, "type": "utility", "desc": "Silver yarn binds and cuts."},
        '3': {"name": "66 CODE",     "dmg": (130, 190),  "cost": 70, "desc": "The legendary Code 66."}
    }
    e = Enemy("Manager Kim", "The Senior Manager", 480, 300, abilities, 5, "Workers / Cheonliang")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_jinrang_enemy():
    abilities = {
        '1': {"name": "Jinrang's Conviction","dmg": (130, 190), "cost": 50, "desc": "Gapryong's disciple's conviction."},
        '2': {"name": "Busan King",           "dmg": (140, 210), "cost": 55, "desc": "Authority of Busan's king."},
        '3': {"name": "True Conviction",      "dmg": (170, 250), "cost": 70, "desc": "Ultimate faith in Gapryong's teachings."}
    }
    e = Enemy("Jinrang", "King of Busan", 750, 380, abilities, 2, "Busan")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_jaegyeon_na_enemy():
    abilities = {
        '1': {"name": "Incheon Speed",    "dmg": (100, 150), "cost": 40, "desc": "Speed that can't be tracked."},
        '2': {"name": "Betrayal",         "dmg": (95, 145),  "cost": 35, "desc": "True nature revealed."},
        '3': {"name": "Faster Than Light","dmg": (150, 230),  "cost": 60, "desc": "Absolute speed limit reached."}
    }
    e = Enemy("Jaegyeon Na", "King of Incheon", 620, 350, abilities, 6, "Busan / 1st Gen")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_charles_choi():
    abilities = {
        '1': {"name": "🎭 Puppet Master",      "dmg": (90, 140),  "cost": 35, "desc": "Manipulates the battlefield."},
        '2': {"name": "🏛️ Chairman's Authority","dmg": (110, 170), "cost": 45, "desc": "HNH Group chairman's power."},
        '3': {"name": "👤 HNH Group",          "dmg": (100, 160), "cost": 40, "desc": "Organization backing every move."},
        '4': {"name": "🎭 Truth of Two Bodies","dmg": (130, 200), "cost": 60, "desc": "The ultimate secret revealed."}
    }
    e = Enemy("Charles Choi", "Elite", 650, 350, abilities, 3, "HNH Group")
    e.ai_pattern = ['4', '3', '2', '1']
    return e

def create_enemy_tom_lee():
    abilities = {
        '1': {"name": "🐅 Wild Strike",  "dmg": (100, 150), "cost": 35, "desc": "Primal untamed strike."},
        '2': {"name": "🐅 Tom Lee Special","dmg": (120, 180),"cost": 45, "desc": "Biting, clawing, striking."},
        '3': {"name": "🐅 Gen 0 Power",  "dmg": (140, 210), "cost": 55, "desc": "Power from the legendary era."}
    }
    e = Enemy("Tom Lee", "The Wild", 650, 350, abilities, 5, "Gen 0")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_gapryong_kim():
    abilities = {
        '1': {"name": "👑 Conviction of the Strongest","dmg": (120, 180), "cost": 45, "desc": "The conviction that made him strongest."},
        '2': {"name": "👑 Gapryong's Fist",           "dmg": (150, 220), "cost": 55, "desc": "The fist that defeated the Yamazaki Syndicate."},
        '3': {"name": "👑 Will to Protect",            "dmg": (130, 200), "cost": 50, "desc": "Born from protecting his crew."},
        '4': {"name": "👑 Legend's Legacy",            "dmg": (180, 280), "cost": 70, "desc": "The accumulated power of a legend."}
    }
    e = Enemy("Gapryong Kim", "The Strongest", 800, 400, abilities, 0, "Gen 0 Legend")
    e.ai_pattern = ['4', '2', '3', '1']
    return e

def create_enemy_cheon_shinmyeong():  # CANON-Z1 FIX: rank was 0 (Gapryong-tier), corrected to 38
    abilities = {
        '1': {"name": "🔮 Dark Exorcism",  "dmg": (90, 140),  "cost": 35, "desc": "Shamanistic power techniques."},
        '2': {"name": "🔮 Cheonliang Rule","dmg": (100, 150), "cost": 40, "desc": "Shaman authority manifested."},
        '3': {"name": "🔮 Puppeteer",      "dmg": (80, 120),  "cost": 30, "desc": "Controlling others like puppets."}
    }
    e = Enemy("Cheon Shin-myeong", "The Shaman", 480, 320, abilities, 38, "Cheonliang")
    e.ai_pattern = ['3', '2', '1']
    return e

def create_enemy_seongji_yuk():
    abilities = {
        '1': {"name": "🇰🇷 Ssireum: Throw",  "dmg": (80, 120),  "cost": 30, "desc": "Korean wrestling throw."},
        '2': {"name": "🇰🇷 Mujin Ssireum: Rib Crush","dmg": (85, 130),  "cost": 35, "desc": "Bone-breaking grip — crushes ribs."},
        '3': {"name": "🥋 Yaksha Kudo",            "dmg": (90, 135),  "cost": 35, "desc": "Yamazaki Yaksha-taught Kudo."},
        '4': {"name": "🦍 Monster Mode",      "dmg": (130, 190), "cost": 55, "desc": "Monstrous power unleashed."},
    }
    e = Enemy("Seongji Yuk", "The Monster of Cheonliang", 600, 300, abilities, 9, "Cheonliang")
    e.ai_pattern = ['4', '3', '2', '1']
    return e

def create_enemy_sinu_han():
    abilities = {
        '1': {"name": "🌀 Invisible Punch","dmg": (85, 125),  "cost": 30, "desc": "Invisible punch from nowhere."},
        '2': {"name": "🌀 Invisible Kick", "dmg": (85, 125),  "cost": 30, "desc": "Invisible kick."},
        '3': {"name": "🌀 Ghost Fist",     "dmg": (120, 175), "cost": 50, "desc": "Ultimate invisible attack."},
    }
    e = Enemy("Sinu Han", "The Ghost", 500, 280, abilities, 20, "Workers")
    e.ai_pattern = ['3', '1', '2']
    return e


# ============================================================================
# MAIN GAME CLASS
# ============================================================================

class LookismGame:
    def __init__(self, load_saved=True):
        self.daniel     = DanielPark("current")
        self.zack       = ZackLee()
        self.johan      = JohanSeong(blind=True)
        self.vasco      = Vasco()
        self.jay        = JayHong()
        self.eli        = EliJang()
        self.warren     = WarrenChae()
        self.jake       = JakeKim()
        self.gun        = GunPark()
        self.goo        = GooKim()
        self.joongoo    = KimJungu()
        self.manager_kim = ManagerKim()

        self.gapryong   = GapryongKim()
        self.tom_lee    = TomLee()
        self.charles_choi = CharlesChoi()
        self.jinyoung   = JinyoungPark()
        self.baekho     = Baekho()

        self.james_lee  = JamesLee()
        self.gitae      = GitaeKim()
        self.jichang    = JichangKwak()
        self.taesoo     = TaesooMa()
        self.gongseob   = GongseobJi()
        self.seokdu     = SeokduWang()
        self.jaegyeon   = JaegyeonNa()
        self.seongji    = SeongjiYuk()
        self.jinrang    = Jinrang()

        self.mandeok    = Mandeok()
        self.xiaolung   = Xiaolung()
        self.ryuhei     = Ryuhei()
        self.samuel     = SamuelSeo()
        self.sinu       = SinuHan()
        self.logan      = LoganLee()

        self.vin_jin    = VinJin()
        self.han_jaeha  = HanJaeha()
        self.baek_seong = BaekSeong()

        self.shingen    = ShingenYamazaki()
        self.park_father = ParkFather()

        self.kim_minjae = KimMinjae()
        self.detective_kang = DetectiveKang()

        self.all_characters = self._compile_all_characters()

        self.unlocked_characters = {
            "Gapryong Kim": False, "Tom Lee": False, "Charles Choi": False,
            "Jinyoung Park": False, "Baekho Kwon": False, "James Lee": False,
            "Gitae Kim": False, "Shingen Yamazaki": False,
            "Park Jonggun's Father": False, "Jinrang": False, "Jaegyeon Na": False,
            # CANON-Y3 FIX: 1st Gen Kings should not be available from the start
            "Jichang Kwak": False, "Taesoo Ma": False,
            "Gongseob Ji": False, "Seokdu Wang": False,
        }
        self.unlock_requirements = {
            "Gapryong Kim":           "Complete Boss Rush Mode",
            "Tom Lee":                "Complete Secret Arc: Genesis",
            "Charles Choi":           "Complete Final Chapter",
            "Jinyoung Park":          "Complete Boss Rush Mode",
            "Baekho Kwon":            "Complete Boss Rush Mode",
            "James Lee":              "Complete Boss Rush Mode",
            "Gitae Kim":              "Complete Boss Rush Mode",
            "Shingen Yamazaki":       "Complete Boss Rush Mode",
            "Park Jonggun's Father":  "Complete Boss Rush Mode",
            "Jinrang":                "Complete Chapter 27: Jinrang's Return",
            "Jaegyeon Na":            "Complete Chapter 28: The Betrayal",
            # CANON-Y3 FIX: 1st Gen Kings unlocked by completing Arc 7
            "Jichang Kwak":           "Complete Arc 7: 1st Generation",
            "Taesoo Ma":              "Complete Arc 7: 1st Generation",
            "Gongseob Ji":            "Complete Arc 7: 1st Generation",
            "Seokdu Wang":            "Complete Arc 7: 1st Generation",
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
    # choose_character_path — while loop (no recursion)
    # -------------------------------------------------------------------------
    def choose_character_path(self, character):
        while True:
            if character.path:
                changes_left = self.path_changes_available
                print(f"\n{character.name} currently walks: {character.path.value}")
                print(f"Path Level: {character.path_level} | EXP: {character.path_exp}/100")
                # BUG-W5 FIX: show remaining changes and block if at zero
                print(f"🔄 Path changes remaining: {changes_left}")
                print("\n  1. Keep current path")
                if changes_left > 0:
                    print("  2. Change path (resets level/EXP, uses 1 change)")
                    print("  3. Reset path completely (uses 1 change)")
                else:
                    print("  2. Change path — ❌ No changes left")
                    print("  3. Reset path — ❌ No changes left")
                print("  b. Back")
                choice = input("> ").strip().lower()
                if choice == '1' or choice == 'b':
                    return True
                elif choice == '2':
                    if changes_left <= 0:
                        print("❌ No path changes remaining!")
                        continue
                    confirm = input(f"Change {character.name}'s path? Level and EXP will be lost if you pick a new one. (y/n): ").lower()
                    if confirm == 'y':
                        # BUG-Y3 FIX: stash old state; clear path so picker shows below;
                        #             but do NOT charge the change yet — only charge when the
                        #             player actually completes a new selection (not on back-out)
                        _old_path = character.path
                        _old_it   = character.infinity_technique
                        _old_lvl  = character.path_level
                        _old_exp  = character.path_exp
                        character.path = None
                        character.infinity_technique = None
                        character.path_level = 1
                        character.path_exp = 0
                        # falls through to path picker below; picker returns True on success
                        # or False on back — we catch the result after the loop continues
                        print(f"🔄 Choose a new path for {character.name}. ({changes_left} changes left — charged on confirm)")
                        # Set a flag so the picker below knows to charge or restore
                        character._pending_change = (_old_path, _old_it, _old_lvl, _old_exp)
                elif choice == '3':
                    if changes_left <= 0:
                        print("❌ No path changes remaining!")
                        continue
                    confirm = input(f"Clear {character.name}'s path entirely? (y/n): ").lower()
                    if confirm == 'y':
                        character.path = None
                        character.infinity_technique = None
                        character.path_level = 1
                        character.path_exp = 0
                        self.path_changes_available -= 1
                        print(f"🔄 {character.name}'s path cleared! ({self.path_changes_available} changes left)")
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
                # BUG-Y3 FIX: if we got here via choice '2', restore old state — no charge
                if hasattr(character, '_pending_change') and character._pending_change:
                    old_path, old_it, old_lvl, old_exp = character._pending_change
                    character.path = old_path
                    character.infinity_technique = old_it
                    character.path_level = old_lvl
                    character.path_exp = old_exp
                    character._pending_change = None
                    print(f"↩️ Path change cancelled. {character.name} keeps {character.path.value}.")
                return False
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(character.paths_available):
                    # BUG-Y3 FIX: charge the change only NOW that a new path was confirmed
                    was_pending = hasattr(character, '_pending_change') and character._pending_change
                    character._pending_change = None
                    result = character.choose_path(character.paths_available[idx])
                    if was_pending:
                        self.path_changes_available -= 1
                    slow_print(result, 0.03)
                    time.sleep(1)
                    return True
                else:
                    print("❌ Invalid number.")
            except ValueError:
                print("❌ Enter a number.")

    # -------------------------------------------------------------------------
    # enemy_turn
    # BUG-A FIX: realm_timer > 0 check guards evasion/counter
    # BUG-C FIX: no pre-halving for defending; take_damage handles via temp_buffs
    # MECH-3 FIX: STRENGTH realm armor_break passed to take_damage
    # -------------------------------------------------------------------------
    def enemy_turn(self, enemy):
        if not enemy.is_alive():
            return
        if not any(c.is_alive() for c in self.party):
            return

        if enemy.stunned:
            self.add_log(f"⚡ {enemy.name} is stunned!")
            # BUG-Y2 FIX: do NOT clear here — cleanup() owns expiry (30% early or guaranteed)
            time.sleep(0.5)
            return
        if enemy.bound:
            self.add_log(f"⚪ {enemy.name} is bound!")
            # BUG-Y2 FIX: do NOT clear here — cleanup() owns expiry
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
            if enemy.energy < abil.get("cost", 20):
                # MECH-10 FIX: show message instead of silent skip
                self.add_log(f"{enemy.name} conserves energy. (insufficient for any ability)")
                return
            chosen_abil = (first_key, abil)

        key, abil = chosen_abil
        enemy.energy -= abil.get("cost", 20)

        targets = [c for c in self.party if c.is_alive()]
        if not targets:
            return

        t = random.choice(targets)
        base_dmg = random.randint(abil["dmg"][0], abil["dmg"][1])

        enemy_mult, _ = enemy.get_damage_multiplier()
        dmg = int(base_dmg * enemy_mult)

        # MECH-3: check if enemy is in STRENGTH realm (armor_break)
        armor_break = (enemy.active_realm == Realm.STRENGTH and enemy.realm_timer > 0)

        # BUG-A FIX: only check evasion if realm is actually active (timer > 0)
        if t.active_realm == Realm.SPEED and t.realm_timer > 0:
            evasion = t.realm_effect.get('evasion', 0.5) if t.realm_effect else 0.5
            if random.random() < evasion:
                self.add_log(f"💨 {t.name}'s SPEED realm — attack evaded!")
                time.sleep(0.8)
                return

        # BUG-V5 FIX: handle utility-type enemy abilities (e.g. Silver Yarn bind)
        # Utility abilities deal their listed damage AND apply their special effect.
        if abil.get("type") == "utility" and "Silver Yarn" in abil.get("name", ""):
            bound_any = False
            for target_pc in self.party:
                if target_pc.is_alive() and random.random() < 0.6:
                    target_pc.bound = True
                    self.add_log(f"⚪ {enemy.name}'s Silver Yarn binds {target_pc.name}!")
                    bound_any = True
            if not bound_any:
                self.add_log(f"⚪ {enemy.name}'s Silver Yarn missed!")

        # BUG-C FIX: No pre-halving here. take_damage handles all reductions.
        t.take_damage(dmg, armor_break=armor_break)
        self.add_log(f"{enemy.name} uses {abil['name']} on {t.name} for {dmg} damage!")

        # TECHNIQUE realm counter — only if realm is actually active
        if t.active_realm == Realm.TECHNIQUE and t.realm_timer > 0 and t.is_alive():
            counter_chance = t.realm_effect.get('counter', 0.25) if t.realm_effect else 0.25
            if random.random() < counter_chance:
                counter_dmg = random.randint(30, 60)
                enemy.take_damage(counter_dmg)
                self.add_log(f"🩷 {t.name}'s TECHNIQUE realm — counter attack! {counter_dmg} to {enemy.name}!")

        # Johan Copy Mechanic
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
                jv = johan.technique_view_count
                jv[abil['name']] = jv.get(abil['name'], 0) + 1

        time.sleep(0.8)

    # -------------------------------------------------------------------------
    # cleanup
    # BUG-A FIX: realm_timer decremented after use, so timer > 0 in combat is safe
    # BUG-H: timer starts at 6, so first cleanup brings it to 5 effective turns
    # -------------------------------------------------------------------------
        # Post-enemy-attack passive mechanics: check all living party members
        for _pchar in self.party:
            if not _pchar.is_alive():
                continue
            # CONVICTION STACKS (Jinrang): builds with HP loss
            if hasattr(_pchar, 'conviction_stacks') and _pchar.max_hp > 0:
                hp_frac = _pchar.hp / _pchar.max_hp
                if hp_frac < 0.80 and _pchar.conviction_stacks < _pchar.max_conviction_stacks:
                    _pchar.conviction_stacks = min(_pchar.max_conviction_stacks, _pchar.conviction_stacks + 1)
                    self.add_log(f"👑 {_pchar.name}'s conviction grows from pain! ({_pchar.conviction_stacks}/{_pchar.max_conviction_stacks} stacks)")
            # HEAT MODE auto-trigger (Vasco): triggers once when HP < 40%
            if hasattr(_pchar, 'heat_mode_active') and not _pchar.heat_mode_active and not getattr(_pchar, 'heat_mode_triggered', False):
                if _pchar.hp / _pchar.max_hp < 0.40:
                    _pchar.heat_mode_active = True
                    _pchar.heat_mode_triggered = True
                    _pchar.temp_buffs.append({'name': 'HeatMode', 'dmg_mult': 1.50, 'def_mult': 1.0, 'turns': 3})
                    self.add_log(f"🔥🔥🔥 {_pchar.name}'s HEAT MODE activates! +50% dmg for 3 turns!")
            # SELF-HATRED auto-trigger (Samuel Seo): triggers when HP < 40%
            if hasattr(_pchar, 'self_hatred_active') and not _pchar.self_hatred_active:
                if _pchar.hp / _pchar.max_hp < 0.40:
                    _pchar.self_hatred_active = True
                    _pchar.temp_buffs.append({'name': 'SelfHatred', 'dmg_mult': 2.0, 'def_mult': 1.0, 'turns': 2})
                    self.add_log(f"💢💢💢 {_pchar.name}'s SELF-HATRED awakens below 40% HP! x2.0 dmg!")


    def cleanup(self):
        all_combatants = self.party + self.enemies

        for c in all_combatants:
            c.defending = False

        for c in self.party:
            # BUG-V6 FIX: don't tick timers on dead characters
            if not c.is_alive():
                continue
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

            # God Eye timer
            if hasattr(c, 'god_eye_active') and c.god_eye_active:
                c.god_eye_timer -= 1
                if c.god_eye_timer <= 0:
                    c.god_eye_active = False
                    c.god_eye_timer = 0
                    self.add_log(f"{c.name}'s God Eye fades.")
                else:
                    self.add_log(f"👁️ God Eye: {c.god_eye_timer} turns remaining.")

            # Veinous rage timer (MECH-7)
            if c.veinous_rage:
                c.veinous_rage_timer -= 1
                if c.veinous_rage_timer <= 0:
                    c.veinous_rage = False
                    self.add_log(f"{c.name}'s Veinous Rage fades.")

            # Muscle boost timer (MECH-9)
            if c.muscle_boost:
                c.muscle_boost_timer -= 1
                if c.muscle_boost_timer <= 0:
                    c.muscle_boost = False
                    self.add_log(f"{c.name}'s Titan Boost fades.")

            # Silver yarn timer (MECH-8)
            if c.silver_yarn_active:
                c.silver_yarn_timer -= 1
                if c.silver_yarn_timer <= 0:
                    c.silver_yarn_active = False
                    self.add_log(f"{c.name}'s Silver Yarn dissipates.")

            # Tenacity regen
            regen = c.apply_realm_regen()
            if regen > 0:
                self.add_log(f"🟢 {c.name} regenerates {regen} HP (Tenacity).")

            # CLINCH timer (Xiaolung)
            if hasattr(c, 'clinch_active') and c.clinch_active:
                c.clinch_timer -= 1
                if c.clinch_timer <= 0:
                    c.clinch_active = False
                    c.clinch_timer = 0
                    self.add_log(f"🇹🇭 {c.name}'s Thai Clinch released.")

            # ANIMAL INSTINCT timer (Tom Lee)
            if hasattr(c, 'animal_instinct') and c.animal_instinct:
                c.animal_instinct_timer -= 1
                if c.animal_instinct_timer <= 0:
                    c.animal_instinct = False
                    c.animal_instinct_timer = 0
                    self.add_log(f"🐅 {c.name}'s Animal Instinct fades.")

            # GHOST FORM timer (Sinu Han)
            if hasattr(c, 'ghost_form_active') and c.ghost_form_active:
                c.ghost_form_timer -= 1
                if c.ghost_form_timer <= 0:
                    c.ghost_form_active = False
                    c.ghost_form_timer = 0
                    self.add_log(f"🌀 {c.name}'s Ghost Form ends.")

            # LAST STAND BURST timer (Jinrang)
            if hasattr(c, 'last_stand_burst') and c.last_stand_burst:
                c.last_stand_burst_timer -= 1
                if c.last_stand_burst_timer <= 0:
                    c.last_stand_burst = False
                    c.last_stand_burst_timer = 0
                    self.add_log(f"👑 {c.name}'s Last Stand burst ends.")

            # TAEKKYON RHYTHM — reset if character didn't act this turn
            if hasattr(c, 'rhythm_stacks') and c.rhythm_stacks > 0:
                if not getattr(c, 'last_acted', False):
                    c.rhythm_stacks = 0
                    self.add_log(f"🦢 {c.name}'s Taekkyon rhythm broken!")
                c.last_acted = False  # reset for next turn

            # HEAT MODE timer — managed by temp_buff expiry, just reset flag when expired
            if hasattr(c, 'heat_mode_active') and c.heat_mode_active:
                if not any(b['name'] == 'HeatMode' for b in c.temp_buffs):
                    c.heat_mode_active = False

            # DUAL BODY SYNC timer
            if hasattr(c, 'dual_sync_active') and c.dual_sync_active:
                c.dual_sync_timer -= 1
                if c.dual_sync_timer <= 0:
                    c.dual_sync_active = False
                    c.dual_sync_timer  = 0
                    self.add_log(f"👥 {c.name}'s Dual Body Sync ends — second body retreats.")
                else:
                    self.add_log(f"👥 Dual Body Sync: {c.dual_sync_timer} turn(s) remaining.")

            # Sync live hp/energy back to the active pool before ticking other things
            if hasattr(c, 'active_body'):
                if c.active_body == 'perfect':
                    c.perfect_hp     = c.hp
                    c.perfect_energy = c.energy
                else:
                    c.true_hp     = c.hp
                    c.true_energy = c.energy

            # Tick down timed buffs
            expired = []
            for buff in c.temp_buffs:
                buff['turns'] -= 1
                if buff['turns'] <= 0:
                    expired.append(buff)
                    self.add_log(f"⏱️ {c.name}'s {buff['name']} buff expired.")
            for buff in expired:
                c.temp_buffs.remove(buff)

            # Status recovery — cleanup() is the SOLE authority on stun/bound expiry
            # BUG-Y2 FIX: 30% chance of early recovery each turn;
            #              if not recovered early, stun/bound is guaranteed cleared here
            #              so the max duration is 2 turns (lose turn + possible next-turn recovery)
            #              and min is 1 turn (lose current turn, recover in same cleanup)
            if c.stunned:
                if random.random() < 0.3:
                    c.stunned = False
                    self.add_log(f"⚡ {c.name} shakes off the stun early!")
                else:
                    c.stunned = False   # guaranteed clear after the turn was lost
            if c.bound:
                if random.random() < 0.3:
                    c.bound = False
                    self.add_log(f"⚪ {c.name} breaks free of the bindings!")
                else:
                    c.bound = False   # guaranteed clear after the turn was lost

        for e in self.enemies:
            # BUG-Y2 FIX: 30% early recovery; guaranteed clear after turn was lost
            if e.stunned:
                if random.random() < 0.3:
                    e.stunned = False
                else:
                    e.stunned = False   # guaranteed clear
            if e.bound:
                if random.random() < 0.3:
                    e.bound = False

        time.sleep(0.2)

    # -------------------------------------------------------------------------
    # DUAL BODY SYSTEM — Daniel Park specific
    # -------------------------------------------------------------------------
    def _daniel_body_swap(self, character):
        """Swap Daniel's active body. Saves current HP/energy, loads the other pool."""
        if not hasattr(character, 'active_body'):
            return "No dual body available."

        # Save current body's live stats back to its pool
        if character.active_body == 'perfect':
            character.perfect_hp     = character.hp
            character.perfect_energy = character.energy
        else:
            character.true_hp     = character.hp
            character.true_energy = character.energy

        # Cancel dual sync on swap (both bodies need their own turn to reposition)
        if character.dual_sync_active:
            character.dual_sync_active = False
            character.dual_sync_timer  = 0

        # Flip to other body
        if character.active_body == 'perfect':
            character.active_body = 'true'
            character.hp          = character.true_hp
            character.max_hp      = character.true_max_hp
            character.energy      = character.true_energy
            character.max_energy  = character.true_max_energy
            body_desc = "True Body"
            stat_note = "(380HP, 260E — tougher frame, lower ATK multiplier)"
        else:
            character.active_body = 'perfect'
            character.hp          = character.perfect_hp
            character.max_hp      = character.perfect_max_hp
            character.energy      = character.perfect_energy
            character.max_energy  = character.perfect_max_energy
            body_desc = "Perfect Body"
            stat_note = "(320HP, 300E — higher ATK multiplier, more energy)"

        if character.hp <= 0:
            # The inactive body was KO'd — swap back immediately
            if character.active_body == 'true':
                character.active_body = 'perfect'
                character.hp = character.perfect_hp; character.max_hp = character.perfect_max_hp
                character.energy = character.perfect_energy; character.max_energy = character.perfect_max_energy
            else:
                character.active_body = 'true'
                character.hp = character.true_hp; character.max_hp = character.true_max_hp
                character.energy = character.true_energy; character.max_energy = character.true_max_energy
            return f"❌ {character.name} cannot swap — {body_desc} has been knocked out!"

        lines_out = [
            f"",
            f"{'🔁'*30}",
            f"🔁🔁🔁 BODY SWAP — {body_desc} 🔁🔁🔁",
            f"{'🔁'*30}",
            f"Daniel's consciousness shifts! {stat_note}",
            f"HP: {character.hp}/{character.max_hp}  Energy: {character.energy}/{character.max_energy}",
        ]
        return "\n".join(lines_out)

    def _daniel_dual_sync(self, character):
        """Activate Dual Body Sync — both bodies fight for 3 turns."""
        if not hasattr(character, 'active_body'):
            return "No dual body available."

        # Check requirements: both bodies alive, path Lv5+, UI path chosen
        inactive_hp = character.true_hp if character.active_body == 'perfect' else character.perfect_hp
        if inactive_hp <= 0:
            return "❌ Dual Body Sync requires BOTH bodies to be alive!"
        if character.path_level < 5:
            return f"❌ Dual Body Sync requires Path Level 5+ (current: Lv.{character.path_level})"
        if character.path != Path.DANIEL_UI:
            return "❌ Dual Body Sync requires the DANIEL_UI path (Ultra Instinct path)"

        if character.dual_sync_active:
            return f"👥 Dual Body Sync is already active! ({character.dual_sync_timer} turns left)"

        character.dual_sync_active = True
        character.dual_sync_timer  = 3

        inactive_name = "True Body" if character.active_body == "perfect" else "Perfect Body"
        lines_out = [
            f"",
            f"{'👥'*30}",
            f"👥👥👥 DUAL BODY SYNC ACTIVATED 👥👥👥",
            f"{'👥'*30}",
            f"Both bodies enter battle simultaneously!",
            f"Canon: Ch.470 — moving so fast not even Warren could track them.",
            f"Every attack triggers a FREE follow-up from {inactive_name} (70% dmg)!",
            f"Duration: 3 turns",
        ]
        return "\n".join(lines_out)

    # -------------------------------------------------------------------------
    # use_ability — while loop, all mechanics wired
    # MECH-5 FIX: double strike also applies to infinity technique
    # BUG-B FIX: Iron Fortress sets ONLY temp_buff (no defending flag)
    # MECH-7/8/9 wired to abilities
    # -------------------------------------------------------------------------
    def use_ability(self, character):
        while True:
            if hasattr(character, 'exhausted') and character.exhausted:
                self.add_log(f"{character.name} is exhausted and cannot act! (Turn regen already applied)")
                character.exhausted = False
                time.sleep(ACTION_DELAY)
                return True

            # BUG-W2 FIX: stunned party members lose their turn
            # BUG-Y2 FIX: do NOT clear stun here — cleanup() is the sole authority on expiry
            if character.stunned:
                self.add_log(f"⚡ {character.name} is stunned and loses their turn!")
                time.sleep(ACTION_DELAY)
                return True

            # BUG-W3 FIX: bound party members lose their turn
            # BUG-Y2 FIX: do NOT clear bound here — cleanup() owns expiry (30% early or guaranteed)
            if character.bound:
                self.add_log(f"⚪ {character.name} is bound and cannot act!")
                time.sleep(ACTION_DELAY)
                return True

            print(f"\n{'=' * 90}")
            slow_print(f"✦✦✦ {character.name} [{character.title}] ✦✦✦", 0.03)
            print("=" * 90)
            print(f"❤️ HP: {character.hp}/{character.max_hp}  ⚡ Energy: {character.energy}/{character.max_energy}")
            if character.path:
                print(f"🛤️ PATH: {character.path.value[:50]} (Lv.{character.path_level}, +{min(40,(character.path_level-1)*2)}% dmg)")
            print("-" * 90)

            available = {k: v for k, v in character.abilities.items()
                         if character.energy >= v["cost"] and v.get("type") != "passive"}

            passive_ab = {k: v for k, v in character.abilities.items() if v.get("type") == "passive"}
            damage_ab  = {k: v for k, v in available.items() if v.get("type") in ["damage", "counter"]}
            buff_ab    = {k: v for k, v in available.items() if v.get("type") in ["buff", "ui", "body_swap", "dual_sync", "weakness_expose", "debilitate", "clinch", "dance"]}
            util_ab    = {k: v for k, v in available.items() if v.get("type") == "utility"}

            sort_key = lambda x: (0 if x.isdigit() else 1, int(x) if x.isdigit() else x)

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

            print("\n  0. 📖 Describe  |  00. 🔮 Realm  |  000. 🛤️ Path  |  0000. ⏭️ Skip (rest, turn regen only)  |  00000. ↩️ Back")
            print("-" * 90)

            choice = input("> ").strip()
            print()

            if choice == '00000':
                return False
            if choice == '0000':
                # BUG-V8 FIX: skip gives no extra energy — the +15 turn regen already fired
                # before use_ability was called. Adding another +15 here gave +30 total, unintended.
                self.add_log(f"{character.name} rests. (Turn regen already applied)")
                return True
            if choice == '000':
                self.choose_character_path(character)
                self.save_game()
                continue
            if choice == '00':
                if character.realms:
                    print("\n🔮 AVAILABLE REALMS:")
                    for i, realm in enumerate(character.realms):
                        effect = RealmEffect.REALM_DATA.get(realm, {})
                        print(f"  {i + 1}. {realm.value} — {effect.get('desc', '')}")
                    print("  b. Back")
                    rc = input("> ").strip()
                    if rc.lower() == 'b':
                        continue
                    if rc.isdigit():
                        idx = int(rc) - 1
                        if 0 <= idx < len(character.realms):
                            self.add_log(character.activate_realm(character.realms[idx]))
                            return True
                    print("❌ Invalid realm choice.")
                else:
                    print(f"{character.name} has no available realms.")
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

            # ── INFINITY TECHNIQUE ───────────────────────────────────────────
            if choice == '99' and it and character.energy >= it['cost']:
                target = self.select_target()
                if not target:
                    print("❌ No valid target.")
                    continue
                character.energy -= it['cost']
                dmg = random.randint(it['dmg'][0], it['dmg'][1])
                mult, buffs = character.get_damage_multiplier()
                dmg = int(dmg * mult)

                armor_break = (character.active_realm == Realm.STRENGTH and character.realm_timer > 0)
                target.take_damage(dmg, armor_break=armor_break)

                print("\n" + "✨" * 45)
                slow_print(f"✨✨✨ {it['name']} ✨✨✨", 0.05)
                print("✨" * 45)
                self.add_log(f"INFINITY TECHNIQUE! {dmg} damage to {target.name}!")
                if buffs:
                    self.add_log(f"   Multipliers: {', '.join(buffs)}")
                self.add_log(f"📖 {it['desc']}")

                # MECH-5 FIX: double strike applies to infinity technique too
                if character.active_realm == Realm.SPEED and character.realm_timer > 0:
                    ds_chance = character.realm_effect.get('double_strike', 0.3) if character.realm_effect else 0.3
                    if random.random() < ds_chance:
                        bonus = int(dmg * 0.6)
                        target.take_damage(bonus, armor_break=armor_break)
                        self.add_log(f"⚡ SPEED REALM: Double strike on INFINITY! +{bonus} bonus!")

                # DUAL BODY SYNC follow-up on infinity technique
                if hasattr(character, 'dual_sync_active') and character.dual_sync_active and target.is_alive():
                    inactive_hp = character.true_hp if character.active_body == 'perfect' else character.perfect_hp
                    if inactive_hp > 0:
                        sync_dmg = int(dmg * 0.70)
                        target.take_damage(sync_dmg, armor_break=armor_break)
                        inactive_name = "True Body" if character.active_body == "perfect" else "Perfect Body"
                        self.add_log(f"👥 DUAL SYNC: {inactive_name} mirrors the INFINITY! +{sync_dmg} damage!")

                return True

            # ── REGULAR ABILITIES ────────────────────────────────────────────
            if choice in available:
                ability = available[choice]
                character.energy = max(0, character.energy - ability["cost"])
                atype = ability.get("type", "damage")

                if atype == "ui":
                    if hasattr(character, 'activate_ui'):
                        self.add_log(character.activate_ui())

                elif atype == "body_swap":
                    if hasattr(character, 'active_body'):
                        self.add_log(self._daniel_body_swap(character))
                    else:
                        self.add_log(f"{character.name} cannot swap bodies.")

                elif atype == "dual_sync":
                    if hasattr(character, 'active_body'):
                        self.add_log(self._daniel_dual_sync(character))
                    else:
                        self.add_log(f"{character.name} cannot use Dual Body Sync.")

                elif atype == "weakness_expose":
                    # CharlesChoi: Truth of Two Bodies — enemy takes +25% dmg for 2 turns
                    alive = [e for e in self.enemies if e.is_alive()]
                    if alive:
                        tgt = alive[0]
                        tgt.temp_buffs.append({'name': 'Exposed', 'dmg_mult': 1.0, 'def_mult': 1.25, 'turns': 2})
                        self.add_log(f"🎭 TRUTH OF TWO BODIES! {tgt.name} is exposed — takes +25% damage for 2 turns!")

                elif atype == "debilitate":
                    # JinyoungPark Medical Debilitate / KimJungu Vital Point
                    alive = [e for e in self.enemies if e.is_alive()]
                    if alive:
                        tgt = random.choice(alive)
                        # Deal the damage component if ability has dmg
                        ab_dmg = ability.get('dmg', (0, 0))
                        if ab_dmg[1] > 0:
                            ab_armor_break = ability.get('armor_break', False)
                            dd, _ = self.calc_damage(character, tgt, ability['name'], ab_armor_break)
                            tgt.take_damage(dd, armor_break=ab_armor_break)
                            self.add_log(f"  ⚔️ {character.name} hits {tgt.name} for {dd} dmg!")
                        # Apply debuff
                        if "Medical" in ability['name'] or "Debilitate" in ability['name']:
                            tgt.temp_buffs.append({'name': 'Debilitated', 'dmg_mult': 0.70, 'def_mult': 1.0, 'turns': 3})
                            self.add_log(f"💊 MEDICAL DEBILITATE! {tgt.name} nerve clusters struck — ATK -30% for 3 turns!")
                        elif "Vital" in ability['name'] or "Bleeding" in ability['name']:
                            tgt.temp_buffs.append({'name': 'Bleeding', 'dmg_mult': 1.0, 'def_mult': 1.20, 'turns': 2})
                            self.add_log(f"🖊️ VITAL POINT! {tgt.name} exposed — takes +20% damage for 2 turns!")

                elif atype == "clinch":
                    # Xiaolung: Thai Clinch — enters clinch state for 2 turns + deals damage
                    alive = [e for e in self.enemies if e.is_alive()]
                    if alive:
                        tgt = random.choice(alive)
                        ab_armor_break = ability.get('armor_break', False)
                        dd, _ = self.calc_damage(character, tgt, ability['name'], ab_armor_break)
                        tgt.take_damage(dd)
                        character.clinch_active = True
                        character.clinch_timer = 2
                        self.add_log(f"🇹🇭 THAI CLINCH! {character.name} grabs {tgt.name}'s head! {dd} dmg! Free knee follow-ups for 2 turns!")

                elif atype == "dance":
                    # BaekSeong: Taekkyon dance rhythm — deals damage + builds rhythm stacks
                    alive = [e for e in self.enemies if e.is_alive()]
                    if alive:
                        tgt = random.choice(alive)
                        ab_armor_break = ability.get('armor_break', False)
                        stun_chance = ability.get('stun_chance', 0.35 if 'Rhythm Break' in ability['name'] else 0)
                        dd, _ = self.calc_damage(character, tgt, ability['name'], ab_armor_break)
                        # Rhythm bonus
                        if hasattr(character, 'rhythm_stacks') and character.rhythm_stacks > 0:
                            rhythm_bonus = character.rhythm_stacks * 0.15
                            dd = int(dd * (1 + rhythm_bonus))
                            self.add_log(f"🦢 RHYTHM x{character.rhythm_stacks}: +{int(rhythm_bonus*100)}% dmg bonus!")
                        tgt.take_damage(dd, armor_break=ab_armor_break)
                        self.add_log(f"🦢 {character.name} uses {ability['name']} on {tgt.name} for {dd} dmg!")
                        if hasattr(character, 'rhythm_stacks'):
                            character.rhythm_stacks = min(5, character.rhythm_stacks + 1)
                            character.last_acted = True
                            self.add_log(f"🦢 Rhythm stacks: {character.rhythm_stacks}/5")
                        if stun_chance and random.random() < stun_chance:
                            tgt.stunned = True
                            self.add_log(f"⚡ RHYTHM BREAK! {tgt.name} is stunned!")

                elif atype == "patriarch_ultimate":
                    # Shingen Yamazaki: Inherited Darkness — self-damage nuclear option
                    alive = [e for e in self.enemies if e.is_alive()]
                    if alive:
                        tgt = random.choice(alive)
                        ab_armor_break = True  # patriarch power bypasses all defense
                        dd, _ = self.calc_damage(character, tgt, ability['name'], ab_armor_break)
                        tgt.take_damage(dd, armor_break=True)
                        self_dmg = 40
                        character.hp = max(1, character.hp - self_dmg)
                        self.add_log(f"🏯🏯🏯 INHERITED DARKNESS! {character.name} channels ALL of Yamazaki's power! "
                                     f"{dd} dmg to {tgt.name}! -{self_dmg}HP self-sacrifice!")

                elif atype == "ultimate_fist":
                    # Taesoo Ma: Ultimate Fist — both Strength+Speed mastery. Injures hand.
                    alive = [e for e in self.enemies if e.is_alive()]
                    if alive:
                        tgt = random.choice(alive)
                        dd, _ = self.calc_damage(character, tgt, ability['name'], True)
                        tgt.take_damage(dd, armor_break=True)
                        self_dmg = 25
                        character.hp = max(1, character.hp - self_dmg)
                        self.add_log(f"🔴🔴🔴 ULTIMATE FIST! Every muscle channeled into ONE strike! "
                                     f"{dd} dmg to {tgt.name}! Taesoo's hand is injured (-{self_dmg}HP)!")

                elif atype == "buff":
                    if "Beast Mode" in ability["name"] and hasattr(character, 'activate_beast_mode'):
                        # BUG-V3 FIX: generic Beast Mode handler covers both Eli and Baekho
                        self.add_log(character.activate_beast_mode())
                    elif "Monster Mode" in ability["name"] and hasattr(character, 'activate_monster_mode'):
                        self.add_log(character.activate_monster_mode())
                    elif "Sunglasses Off" in ability["name"] and hasattr(character, 'activate_sunglasses_off'):
                        self.add_log(character.activate_sunglasses_off())
                    elif "Animal Instinct" in ability["name"] and hasattr(character, 'animal_instinct'):
                        character.animal_instinct = True
                        character.animal_instinct_timer = 3
                        character.temp_buffs.append({'name': 'AnimalInst', 'dmg_mult': 1.40, 'def_mult': 1.0, 'turns': 3})
                        self.add_log(f"🐅🐅🐅 ANIMAL INSTINCT! {character.name} abandons thought — pure predatory instinct! +40% dmg + 30% improvised weapon chance for 3 turns!")
                    elif "Hero's Resolve" in ability["name"] and hasattr(character, 'heat_mode_triggered'):
                        character.temp_buffs.append({'name': "HeroResolve", 'dmg_mult': 1.40, 'def_mult': 1.0, 'turns': 3})
                        character.heal(25)
                        self.add_log(f"🔥 HERO'S RESOLVE! {character.name} is fired up! +40% dmg, healed 25HP!")
                    elif "Iron Crown" in ability["name"]:
                        character.temp_buffs.append({'name': "IronCrown", 'dmg_mult': 1.40, 'def_mult': 0.70, 'turns': 2})
                        self.add_log(f"💢 IRON CROWN STANCE! {character.name} lowers head — +40% headbutt dmg, -30% dmg received for 2 turns!")
                    elif "Elusive Form" in ability["name"]:
                        character.temp_buffs.append({'name': "ElusiveForm", 'dmg_mult': 1.30, 'def_mult': 1.0, 'turns': 3})
                        self.add_log(f"🎭 ELUSIVE FORM! {character.name} enters analytical flow — +30% dmg, +20% dodge for 3 turns!")
                    elif "Imitation" in ability["name"]:
                        character.temp_buffs.append({'name': "Imitation", 'dmg_mult': 1.40, 'def_mult': 1.0, 'turns': 2})
                        self.add_log(f"⚡ IMITATION: {character.name} mirrors the enemy's strength! +40% dmg for 2 turns!")
                    elif "Mirror King" in ability["name"] or "Mastery Copy" in ability["name"]:
                        # Jinyoung: 3-hit mastery copy mode
                        character.temp_buffs.append({'name': "MastCopy", 'dmg_mult': 1.90, 'def_mult': 1.0, 'turns': 3})
                        self.add_log(f"🔄🔄🔄 MIRROR KING: MASTERY COPY! {character.name} copies a Gen 0 legend's physique! +90% dmg for 3 hits!")
                    elif "Ghost Form" in ability["name"] and hasattr(character, 'ghost_form_active'):
                        character.ghost_form_active = True
                        character.ghost_form_timer = 3
                        character.temp_buffs.append({'name': "GhostForm", 'dmg_mult': 1.25, 'def_mult': 1.0, 'turns': 3})
                        self.add_log(f"🌀🌀🌀 GHOST FORM! {character.name} becomes invisible! +25% dmg, all attacks guaranteed invisible (armor_break) for 3 turns!")
                    elif "Self-Hatred" in ability["name"] and hasattr(character, 'self_hatred_active'):
                        character.self_hatred_active = True
                        character.temp_buffs.append({'name': "SelfHatred", 'dmg_mult': 2.0, 'def_mult': 1.0, 'turns': 2})
                        self.add_log(f"💢💢💢 SELF-HATRED MODE! {character.name}'s self-loathing becomes power! x2.0 dmg for 2 turns!")
                    elif character.name == "Johan Seong" and "God Eye" in ability["name"]:
                        if hasattr(character, 'activate_god_eye'):
                            self.add_log(character.activate_god_eye())
                    elif character.name == "Johan Seong" and "Veinous Rage" in ability["name"]:
                        # MECH-7 FIX: wire Veinous Rage
                        character.veinous_rage = True
                        character.veinous_rage_timer = 3
                        self.add_log(f"👁️ {character.name} enters Veinous Rage! +80% damage for 3 turns!")
                    elif character.name == "Mandeok" and "Titan Boost" in ability["name"]:
                        # MECH-9 FIX: wire Titan Boost / muscle_boost
                        if hasattr(character, 'activate_titan_boost'):
                            self.add_log(character.activate_titan_boost())
                    elif "Iron Fortress" in ability["name"]:
                        # BUG-B FIX: ONLY temp_buff, NO defending flag
                        character.temp_buffs.append({'name': 'Iron Fortress', 'dmg_mult': 1.0, 'def_mult': 0.5, 'turns': 2})
                        self.add_log(f"🛡️ {character.name} enters Iron Fortress Stance! -50% damage for 2 turns!")
                    elif "Legend's Speed" in ability["name"]:
                        character.temp_buffs.append({'name': "Legend Speed", 'dmg_mult': 1.3, 'def_mult': 1.0, 'turns': 3})
                        self.add_log(f"⚡ {character.name} taps into legendary speed! +30% damage for 3 turns!")
                    elif "Conviction Mode" in ability["name"]:
                        character.temp_buffs.append({'name': "Conviction", 'dmg_mult': 1.5, 'def_mult': 1.0, 'turns': 3})
                        self.add_log(f"⚖️ {character.name} enters Conviction Mode! +50% damage for 3 turns!")
                    else:
                        self.add_log(f"{character.name} uses {ability['name']}!")
                        self.add_log(f"📖 {ability.get('desc', '')}")

                elif atype == "utility":
                    if "Thread Bind" in ability["name"] or "Silver Yarn" in ability["name"]:
                        bound_any = False
                        for e in self.enemies:
                            if e.is_alive() and random.random() < 0.6:
                                e.bound = True
                                self.add_log(f"⚪ {e.name} is bound by silver threads!")
                                bound_any = True
                        # MECH-8 FIX: activate silver_yarn_active on Manager Kim
                        if hasattr(character, 'silver_yarn_active'):
                            character.silver_yarn_active = True
                            character.silver_yarn_timer = 3
                            self.add_log(f"⚪ {character.name}'s Silver Yarn is active! +20% damage for 3 turns.")
                        if not bound_any:
                            self.add_log("⚪ Silver Yarn found no targets to bind.")
                    elif "Defense" in ability["name"] or "Helmet" in ability["name"]:
                        # BUG-V4 FIX: Gapryong's Defense desc says 2 turns — honour it.
                        # Jay's Motorcycle Helmet desc says 1 turn — honour that too.
                        def_turns = 2 if "Gapryong" in ability["name"] else 1
                        character.temp_buffs.append({'name': 'Defense', 'dmg_mult': 1.0, 'def_mult': 0.5, 'turns': def_turns})
                        self.add_log(f"🛡️ {character.name} takes a defensive stance! -50% damage for {def_turns} turn(s)!")
                    elif "Tungsten" in ability["name"]:
                        character.temp_buffs.append({'name': 'Tungsten Defense', 'dmg_mult': 1.0, 'def_mult': 0.3, 'turns': 1})
                        self.add_log(f"🛡️ {character.name}'s body becomes tungsten! -70% damage this turn!")
                    elif "Intimidation" in ability["name"]:
                        # BUG-07 retained: 40% stun
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

                elif atype in ["damage", "counter"]:
                    target = self.select_target()
                    if target:
                        base_dmg = random.randint(ability["dmg"][0], ability["dmg"][1])
                        mult, buffs = character.get_damage_multiplier()
                        dmg = int(base_dmg * mult)

                        armor_break = (character.active_realm == Realm.STRENGTH and character.realm_timer > 0)
                        # Ability-level armor_break flag
                        if ability.get('armor_break'):
                            armor_break = True
                        # INNATE STRENGTH: 25% armor_break chance on innate abilities
                        if ability.get('innate') and not armor_break:
                            if random.random() < 0.25:
                                armor_break = True
                                self.add_log(f"⚡ INNATE STRENGTH: {character.name}'s power bypasses defenses!")
                        # GHOST FORM: all attacks invisible (armor_break) while active
                        if hasattr(character, 'ghost_form_active') and character.ghost_form_active:
                            armor_break = True
                        target.take_damage(dmg, armor_break=armor_break)

                        self.add_log(f"{character.name} → {ability['name']} → {target.name}: {dmg} DMG")
                        if buffs:
                            self.add_log(f"   Multipliers active: {', '.join(buffs)}")
                        self.add_log(f"📖 {ability.get('desc', '')}")

                        # MECH-5: SPEED realm double strike (regular abilities)
                        if character.active_realm == Realm.SPEED and character.realm_timer > 0:
                            ds_chance = character.realm_effect.get('double_strike', 0.3) if character.realm_effect else 0.3
                            if random.random() < ds_chance:
                                bonus = int(dmg * 0.6)
                                target.take_damage(bonus, armor_break=armor_break)
                                self.add_log(f"⚡ SPEED REALM: Double strike! +{bonus} bonus damage!")

                        # Exhaust Warren after Full CQC + Mentor's Legacy chance
                        if character.name == "Warren Chae" and "Full Release" in ability["name"]:
                            character.exhausted = True
                            self.add_log("⚠️ Warren is exhausted after CQC Full Release!")
                            if hasattr(character, 'mentors_legacy_chance') and random.random() < character.mentors_legacy_chance:
                                character.temp_buffs.append({'name': "MentorLegacy", 'dmg_mult': 1.30, 'def_mult': 1.0, 'turns': 2})
                                self.add_log("🔫 MENTOR'S LEGACY! Warren channels Manager Kim's CQC form! +30% dmg for 2 turns!")

                        # FORCED DOUBLE STRIKE (Jaegyeon invisible mastery)
                        if ability.get('forced_double') and target.is_alive():
                            bonus_dmg = int(dmg * 0.80)
                            target.take_damage(bonus_dmg, armor_break=True)
                            self.add_log(f"🔵 INVISIBLE DOUBLE! Second strike immediately follows! +{bonus_dmg} dmg!")

                        # DOUBLE CHOP (Jichang Hand Blade combo)
                        if ability.get('double_chop') and target.is_alive():
                            bonus_dmg = int(dmg * 0.50)
                            target.take_damage(bonus_dmg, armor_break=True)
                            self.add_log(f"🩷 DOUBLE EDGE: Second blade chop follows! +{bonus_dmg} dmg!")

                        # BIND CHANCE from ability dict
                        if ability.get('bind_chance') and not target.bound:
                            if random.random() < ability['bind_chance']:
                                target.bound = True
                                self.add_log(f"⚪ {character.name}'s technique BINDS {target.name}!")

                        # STUN CHANCE from ability dict (Seokdu headbutt, Jichang nerve slice, etc.)
                        if ability.get('stun_chance') and not target.stunned:
                            if random.random() < ability['stun_chance']:
                                target.stunned = True
                                self.add_log(f"⚡ {character.name}'s strike STUNS {target.name}!")

                        # RIGHT HAND PHILOSOPHY (Taesoo Ma): +20% dmg already in mult via get_damage_multiplier
                        # but we show a message for flavor
                        if ability.get('right_hand'):
                            self.add_log(f"🔴 RIGHT HAND PHILOSOPHY: Taesoo fights as a man!")

                        # CONVICTION STACKS (Jinrang): each hit taken adds conviction
                        if ability.get('conviction') and hasattr(character, 'conviction_stacks'):
                            stack_bonus = character.conviction_stacks * 0.10
                            if stack_bonus > 0:
                                self.add_log(f"👑 CONVICTION x{character.conviction_stacks}: +{int(stack_bonus*100)}% dmg from belief!")

                        # AMBUSH (Samuel Seo): first-strike +50% bonus
                        if ability.get('ambush') and hasattr(character, 'ambush_available') and character.ambush_available:
                            ambush_bonus = int(dmg * 0.50)
                            target.take_damage(ambush_bonus, armor_break=True)
                            character.ambush_available = False
                            self.add_log(f"💢 BETRAYAL AMBUSH! First-strike surprise! +{ambush_bonus} bonus damage!")

                        # VITAL STRIKE (KimJungu): enemy takes +20% dmg for 2 turns
                        if ability.get('vital_strike') and target.is_alive():
                            target.temp_buffs.append({'name': 'VitalExp', 'dmg_mult': 1.0, 'def_mult': 1.20, 'turns': 2})
                            self.add_log(f"🖊️ VITAL POINT EXPOSED! {target.name} takes +20% dmg for 2 turns!")

                        # THAI CLINCH follow-up knee
                        if hasattr(character, 'clinch_active') and character.clinch_active and target.is_alive():
                            knee_dmg = int(dmg * 0.50)
                            target.take_damage(knee_dmg)
                            self.add_log(f"🇹🇭 CLINCH KNEE! Follow-up knee strike! +{knee_dmg} dmg!")

                        # ANIMAL INSTINCT Tom Lee improvised weapon follow-up
                        if hasattr(character, 'animal_instinct') and character.animal_instinct and target.is_alive():
                            if random.random() < 0.30:
                                weapon_dmg = int(dmg * 0.60)
                                target.take_damage(weapon_dmg, armor_break=True)
                                self.add_log(f"🐅 ANIMAL INSTINCT: Tom Lee grabs improvised weapon! +{weapon_dmg} extra damage!")

                        # GANG BACKUP Ryuhei
                        if hasattr(character, 'gang_backup_chance') and target.is_alive():
                            if random.random() < character.gang_backup_chance:
                                backup_dmg = int(dmg * 0.45)
                                target.take_damage(backup_dmg)
                                self.add_log(f"🏴 GANG BACKUP! Yakuza subordinate joins the attack! +{backup_dmg} dmg!")

                        # HEART ATTACK PUNCH: message flavor
                        if ability.get('heart_attack'):
                            self.add_log(f"💔 HEART ATTACK PUNCH! Targeting the heart directly! Defense is meaningless!")

                        # DUAL BODY SYNC follow-up hit
                        if hasattr(character, 'dual_sync_active') and character.dual_sync_active and target.is_alive():
                            inactive_hp = character.true_hp if character.active_body == 'perfect' else character.perfect_hp
                            if inactive_hp > 0:
                                sync_dmg = int(dmg * 0.70)
                                target.take_damage(sync_dmg, armor_break=armor_break)
                                inactive_name = "True Body" if character.active_body == "perfect" else "Perfect Body"
                                self.add_log(f"👥 DUAL SYNC: {inactive_name} follows up! +{sync_dmg} bonus damage!")

                time.sleep(ACTION_DELAY)
                return True

            else:
                print("❌ Invalid choice. Try again.")
                time.sleep(0.3)

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
                if member.veinous_rage:  status.append(f"👁️RAGE({member.veinous_rage_timer}T)")
                if member.muscle_boost:  status.append(f"💪BOOST({member.muscle_boost_timer}T)")
                if hasattr(member, 'silver_yarn_active') and member.silver_yarn_active:
                    status.append(f"⚪YARN({member.silver_yarn_timer}T)")
                if hasattr(member, 'god_eye_active') and member.god_eye_active:
                    status.append(f"👁️GOD EYE({member.god_eye_timer}T)")
                if member.active_realm != Realm.NONE:
                    status.append(f"{member.active_realm.value}({member.realm_timer}T)")
                if member.path:
                    status.append(f"Lv{member.path_level}")
                if member.name == "Johan Seong" and hasattr(member, 'copy_count') and member.copy_count > 0:
                    status.append(f"📚{member.copy_count}")
                if member.temp_buffs:
                    for b in member.temp_buffs:
                        status.append(f"🔰{b['name'][:6]}({b['turns']}T)")
                st = " | ".join(status)
                if hasattr(member, 'active_body'):
                    # Daniel: show active body marker + inactive body HP
                    ab = member.active_body
                    inactive_label = 'True' if ab == 'perfect' else 'Perfect'
                    inactive_hp = member.true_hp if ab == 'perfect' else member.perfect_hp
                    inactive_max = member.true_max_hp if ab == 'perfect' else member.perfect_max_hp
                    sync_tag = ' 👥SYNC' if member.dual_sync_active else ''
                    print(f"  {member.name:20}|{bar}| {member.hp:3}/{member.max_hp:3}HP "
                          f"{member.energy:3}E [{ab[:4].upper()}]{sync_tag}  {st}")
                    print(f"  {'  └─ '+inactive_label+' Body':20}|{'░'*40}| {inactive_hp:3}/{inactive_max:3}HP (inactive)")
                else:
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
                affil_info = f" | {char.affiliation}" if char.affiliation else ""
                realm_info = f" | {'/'.join(r.name for r in char.realms)}" if char.realms else " | No Realm"
                print(f"  {len(available)+1}. {char.name} — {char.title}{affil_info}{realm_info}{copy_info}{path_info}  {char.hp}/{char.max_hp}HP")
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
                    # BUG-X16 FIX: no free energy for stunned/bound chars — they lose their turn
                    if not char.stunned and not char.bound:
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
                    exp_gain = max(5, min(50, 105 - avg_rank))
                    char.path_exp += exp_gain
                    while char.path_exp >= 100:
                        char.path_level += 1
                        char.path_exp -= 100
                        self.add_log(f"✨ {char.name}'s path leveled up to Lv.{char.path_level}! (+{min(40,(char.path_level-1)*2)}% dmg bonus)")

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
            char.hp             = char.max_hp
            char.energy         = char.max_energy
            char.buffs          = []
            char.debuffs        = []
            char.defending      = False
            char.active_realm   = Realm.NONE
            char.realm_effect   = None
            char.realm_timer    = 0
            char.form           = "Normal"
            char.stunned        = False
            char.bound          = False
            char.exhausted      = False
            char.path_history   = []  # BUG-X11 FIX: clear undo stack on rest
            char.ui_mode        = False
            char.ui_timer       = 0
            char.beast_mode     = False
            char.beast_timer    = 0
            char.veinous_rage   = False
            char.veinous_rage_timer = 0
            char.muscle_boost   = False
            char.muscle_boost_timer = 0
            char.silver_yarn_active = False
            char.silver_yarn_timer  = 0
            char.temp_buffs     = []
            if hasattr(char, 'god_eye_active'):
                char.god_eye_active = False
                char.god_eye_timer = 0
            print(f"  ✦ {char.name} fully recovered!")
            time.sleep(0.05)
        self.save_game()
        time.sleep(1)

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
                path_info = f"[{char.path.value[:25]}] Lv.{char.path_level} (+{min(40,(char.path_level-1)*2)}%)" if char.path else "[No Path]"
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
            ("Jinrang",      "jinrang_defeated"),
            ("Jaegyeon Na",  "jaegyeon_defeated"),
            ("Charles Choi", "charles_choi_defeated"),
            ("Tom Lee",      "tom_lee_defeated"),
            ("Gapryong Kim", "gapryong_defeated"),
            # CANON-Y3 FIX: 1st Gen Kings unlocked when Arc 7 is complete
            ("Jichang Kwak", "arc7_complete"),
            ("Taesoo Ma",    "arc7_complete"),
            ("Gongseob Ji",  "arc7_complete"),
            ("Seokdu Wang",  "arc7_complete"),
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

    # -------------------------------------------------------------------------
    # STORY MODE — BUG-F FIX: lambda factories for all enemy lists
    # -------------------------------------------------------------------------
    def story_mode(self):
        print(f"\n{'=' * 90}")
        slow_print("📖 STORY MODE: THE COMPLETE LOOKISM 📖", 0.03)
        print("=" * 90)
        time.sleep(0.5)

        arcs = [
            ("ARC 1: J HIGH & THE TWO BODIES", [
                ("Prologue: The Transfer Student", lambda: [create_enemy_jhigh_bully()]),
                ("Chapter 1: Logan Lee",           lambda: [create_enemy_logan_lee()]),
                ("Chapter 2: Zack's Challenge",    lambda: [create_enemy_zack_lee()]),
                ("Chapter 3: Vasco Appears",       lambda: [create_enemy_vasco_enemy()]),
                ("Chapter 4: Jay's Protection",    lambda: [create_enemy_jay_hong_enemy()])
            ]),
            ("ARC 2: GOD DOG", [
                ("Chapter 5: God Dog Soldiers", lambda: [create_enemy_god_dog_member(), create_enemy_god_dog_member()]),
                ("Chapter 6: God Dog Elite",    lambda: [create_enemy_god_dog_elite(), create_enemy_god_dog_member()]),
                ("Chapter 7: Johan Seong",      lambda: [create_enemy_johan_seong_enemy()])
            ]),
            ("ARC 3: HOSTEL", [
                ("Chapter 8: Hostel Family", lambda: [create_enemy_hostel_member(), create_enemy_sally()]),
                ("Chapter 9: Warren Chae",   lambda: [create_enemy_warren_chae_enemy()]),
                ("Chapter 10: Eli Jang",     lambda: [create_enemy_eli_jang_enemy()])
            ]),
            ("ARC 4: BIG DEAL", [
                ("Chapter 11: Big Deal Soldiers", lambda: [create_enemy_big_deal_member(), create_enemy_brad()]),
                ("Chapter 12: Jerry Kwon",        lambda: [create_enemy_jerry_kwon()]),
                ("Chapter 13: Jake Kim",          lambda: [create_enemy_jake_kim_enemy()])
            ]),
            ("ARC 5: WORKERS", [
                ("Chapter 14: Workers Affiliates", lambda: [create_enemy_workers_member(), create_enemy_workers_affiliate()]),
                ("Chapter 15: Xiaolung",           lambda: [create_enemy_xiaolung()]),
                ("Chapter 16: Mandeok",            lambda: [create_enemy_mandeok()]),
                ("Chapter 17: Samuel Seo",         lambda: [create_enemy_samuel_seo()]),
                ("Chapter 18: Eugene",             lambda: [create_enemy_eugene()])
            ]),
            ("ARC 6: CHEONLIANG", [
                ("Chapter 19: Sinu Han",    lambda: [create_enemy_sinu_han()]),
                ("Chapter 20: Vin Jin",     lambda: [create_enemy_vin_jin()]),
                ("Chapter 21: Ryuhei",      lambda: [create_enemy_ryuhei()]),
                ("Chapter 22: Seongji Yuk", lambda: [create_enemy_seongji_yuk()]),
                ("Chapter 23: The Shaman",  lambda: [create_enemy_cheon_shinmyeong()])
            ]),
            ("ARC 7: 1ST GENERATION", [
                ("Chapter 24: Taesoo Ma",   lambda: [create_enemy_taesoo_ma()]),
                ("Chapter 25: Gongseob Ji", lambda: [create_enemy_gongseob_ji()]),
                ("Chapter 26: Jichang Kwak",lambda: [create_enemy_jichang_kwak()])
            ]),
            ("ARC 8: BUSAN", [
                ("Chapter 27: Jinrang's Return",  lambda: [create_enemy_jinrang_enemy()]),
                ("Chapter 28: The Betrayal",      lambda: [create_enemy_jaegyeon_na_enemy()]),
                ("Final Chapter: Charles Choi",   lambda: [create_enemy_charles_choi()])
            ]),
            ("SECRET ARC: GENESIS", [
                ("Gen 0: Tom Lee",      lambda: [create_enemy_tom_lee()]),
                ("Gen 0: Gapryong Kim", lambda: [create_enemy_gapryong_kim()])
            ])
        ]

        # BUG-W4 FIX: map arc index to the correct story_progress flag
        arc_complete_flags = [
            "arc1_complete", "arc2_complete", "arc3_complete", "arc4_complete",
            "arc5_complete", "arc6_complete", "arc7_complete", "arc8_complete",
            "gen0_complete"
        ]

        for arc_idx, (arc_name, chapters) in enumerate(arcs):
            print(f"\n{'🔥' * 45}")
            slow_print(f"🔥 {arc_name} 🔥", 0.03)
            print(f"{'🔥' * 45}")
            time.sleep(0.5)

            for i, (chapter, enemy_factory) in enumerate(chapters):
                print(f"\n📖 {chapter} ({i+1}/{len(chapters)})")
                party = self.select_party(4) or [self.daniel, self.vasco, self.zack, self.jay]
                input("Press Enter to begin...")

                enemies = enemy_factory()
                if not self.battle(enemies, party):
                    print("\n💀 GAME OVER")
                    time.sleep(2)
                    return False

                flag_map = {
                    "Chapter 27: Jinrang's Return": ("jinrang_defeated",),
                    "Chapter 28: The Betrayal":     ("jaegyeon_defeated",),
                    "Final Chapter: Charles Choi":  ("charles_choi_defeated",),
                    "Gen 0: Tom Lee":               ("tom_lee_defeated",),
                    "Gen 0: Gapryong Kim":          ("gapryong_defeated",)
                }
                for flag in flag_map.get(chapter, []):
                    self.story_progress[flag] = True
                    self.check_unlocks()

                if i < len(chapters) - 1:
                    self.rest()

            # BUG-W4 FIX: mark arc as complete after all its chapters are cleared
            if arc_idx < len(arc_complete_flags):
                self.story_progress[arc_complete_flags[arc_idx]] = True
                self.add_log(f"✅ {arc_name} complete!")
            self.save_game()

        print("\n🏆 STORY MODE COMPLETE!")
        self.save_game()
        time.sleep(2)
        return True

    # -------------------------------------------------------------------------
    # CREW GAUNTLET — BUG-F FIX: lambda factories
    # -------------------------------------------------------------------------
    def crew_gauntlet_mode(self):
        stages = [
            ("God Dog Recruits",    lambda: [create_enemy_god_dog_member(), create_enemy_god_dog_member()]),
            ("Burn Knuckles",       lambda: [create_enemy_burn_knuckles(), create_enemy_jace_park()]),
            ("Hostel Family",       lambda: [create_enemy_hostel_member(), create_enemy_sally()]),
            ("Big Deal Soldiers",   lambda: [create_enemy_big_deal_member(), create_enemy_brad()]),
            ("Workers Affiliates",  lambda: [create_enemy_workers_member(), create_enemy_workers_affiliate()]),
            ("God Dog Elite",       lambda: [create_enemy_god_dog_elite(), create_enemy_god_dog_elite()]),
            ("Hostel Executives",   lambda: [create_enemy_warren_chae_enemy()]),
            ("Big Deal Executive",  lambda: [create_enemy_jerry_kwon()]),
            ("Workers 3rd",         lambda: [create_enemy_mandeok()]),
            ("Workers 2nd",         lambda: [create_enemy_xiaolung()]),
            ("Vin Jin",             lambda: [create_enemy_vin_jin()]),
            ("Ryuhei",              lambda: [create_enemy_ryuhei()]),
            ("Johan Seong",         lambda: [create_enemy_johan_seong_enemy()]),
            ("Eli Jang",            lambda: [create_enemy_eli_jang_enemy()]),
            ("Jake Kim",            lambda: [create_enemy_jake_kim_enemy()]),
            ("Samuel Seo",          lambda: [create_enemy_samuel_seo()]),
            ("Gun Park",            lambda: [create_enemy_gun_park_enemy()]),
            ("Goo Kim",             lambda: [create_enemy_goo_kim_enemy()]),
            ("Kim Jun-gu",          lambda: [create_enemy_kim_jungu_enemy()]),
            ("Manager Kim",         lambda: [create_enemy_manager_kim_enemy()])
        ]

        print("\n🏆 CREW GAUNTLET")
        party = self.select_party(4) or [self.daniel, self.vasco, self.zack, self.jay]

        for i, (stage, enemy_factory) in enumerate(stages):
            self.wave = i + 1
            print(f"\n🏆 STAGE {self.wave}: {stage}")
            input("Press Enter...")

            enemies = enemy_factory()
            if not self.battle(enemies, party):
                print(f"\n💀 GAUNTLET FAILED at Stage {self.wave}")
                time.sleep(2)
                return False
            if i < len(stages) - 1:
                self.rest()

        print("\n🏆 CREW GAUNTLET COMPLETE!")
        self.save_game()
        return True

    # -------------------------------------------------------------------------
    # BOSS RUSH — BUG-F FIX: lambda factories
    # -------------------------------------------------------------------------
    def boss_rush_mode(self):
        bosses = [
            ("Logan Lee",    lambda: [create_enemy_logan_lee()]),
            ("Johan Seong",  lambda: [create_enemy_johan_seong_enemy()]),
            ("Eli Jang",     lambda: [create_enemy_eli_jang_enemy()]),
            ("Warren Chae",  lambda: [create_enemy_warren_chae_enemy()]),
            ("Jake Kim",     lambda: [create_enemy_jake_kim_enemy()]),
            ("Xiaolung",     lambda: [create_enemy_xiaolung()]),
            ("Mandeok",      lambda: [create_enemy_mandeok()]),
            ("Vin Jin",      lambda: [create_enemy_vin_jin()]),
            ("Ryuhei",       lambda: [create_enemy_ryuhei()]),
            ("Samuel Seo",   lambda: [create_enemy_samuel_seo()]),
            ("Taesoo Ma",    lambda: [create_enemy_taesoo_ma()]),
            ("Gongseob Ji",  lambda: [create_enemy_gongseob_ji()]),
            ("Jichang Kwak", lambda: [create_enemy_jichang_kwak()]),
            ("Gun Park",     lambda: [create_enemy_gun_park_enemy()]),
            ("Goo Kim",      lambda: [create_enemy_goo_kim_enemy()]),
            ("Kim Jun-gu",   lambda: [create_enemy_kim_jungu_enemy()]),
            ("Manager Kim",  lambda: [create_enemy_manager_kim_enemy()]),
            ("Jinrang",      lambda: [create_enemy_jinrang_enemy()]),
            ("Jaegyeon Na",  lambda: [create_enemy_jaegyeon_na_enemy()]),
            ("Charles Choi", lambda: [create_enemy_charles_choi()]),
            ("Tom Lee",      lambda: [create_enemy_tom_lee()]),
            ("Gapryong Kim", lambda: [create_enemy_gapryong_kim()])
        ]

        print("\n👑 BOSS RUSH — No rest between battles!")
        party = self.select_party(4) or [self.daniel, self.gun, self.goo, self.johan]

        for i, (boss, enemy_factory) in enumerate(bosses):
            self.wave = i + 1
            print(f"\n👑 BOSS {self.wave}: {boss}")
            input("Press Enter...")
            enemies = enemy_factory()
            if not self.battle(enemies, party):
                print(f"\n💀 BOSS RUSH FAILED at Boss {self.wave}")
                time.sleep(2)
                return False

        self.story_progress["boss_rush_complete"] = True
        self.unlocked_characters["James Lee"]          = True
        self.unlocked_characters["Gitae Kim"]          = True
        self.unlocked_characters["Gapryong Kim"]       = True
        # BUG-Y1 FIX: Shingen, Jinyoung, Baekho, Park Father had no unlock path —
        #             add them here as Boss Rush rewards (fitting: they're all Gen 0 / Yamazaki tier)
        self.unlocked_characters["Shingen Yamazaki"]   = True
        self.unlocked_characters["Jinyoung Park"]      = True
        self.unlocked_characters["Baekho Kwon"]          = True
        self.unlocked_characters["Park Jonggun's Father"] = True
        print("✨ UNLOCKED: James Lee, Gitae Kim, Gapryong Kim, Shingen Yamazaki, Jinyoung Park, Baekho, Park Jonggun's Father!")
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
            ("1",  "Frame Soldier",  create_enemy_frame_soldier),
            ("2",  "Logan Lee",      create_enemy_logan_lee),
            ("3",  "Johan Seong",    create_enemy_johan_seong_enemy),
            ("4",  "Vasco",          create_enemy_vasco_enemy),
            ("5",  "Zack Lee",       create_enemy_zack_lee),
            ("6",  "Jay Hong",       create_enemy_jay_hong_enemy),
            ("7",  "Eli Jang",       create_enemy_eli_jang_enemy),
            ("8",  "Warren Chae",    create_enemy_warren_chae_enemy),
            ("9",  "Jake Kim",       create_enemy_jake_kim_enemy),
            ("10", "Jerry Kwon",     create_enemy_jerry_kwon),
            ("11", "Xiaolung",       create_enemy_xiaolung),
            ("12", "Mandeok",        create_enemy_mandeok),
            ("13", "Vin Jin",        create_enemy_vin_jin),
            ("14", "Ryuhei",         create_enemy_ryuhei),
            ("15", "Samuel Seo",     create_enemy_samuel_seo),
            ("16", "Taesoo Ma",      create_enemy_taesoo_ma),
            ("17", "Gongseob Ji",    create_enemy_gongseob_ji),
            ("18", "Jichang Kwak",   create_enemy_jichang_kwak),
            ("19", "Gun Park",       create_enemy_gun_park_enemy),
            ("20", "Goo Kim",        create_enemy_goo_kim_enemy),
            ("21", "Kim Jun-gu",     create_enemy_kim_jungu_enemy),
            ("22", "Manager Kim",    create_enemy_manager_kim_enemy),
            ("23", "Jinrang",        create_enemy_jinrang_enemy),
            ("24", "Jaegyeon Na",    create_enemy_jaegyeon_na_enemy),
            ("25", "Charles Choi",   create_enemy_charles_choi),
            ("26", "Tom Lee",        create_enemy_tom_lee),
            ("27", "Gapryong Kim",   create_enemy_gapryong_kim),
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
                dmg_bonus = min(40, (char.path_level - 1) * 2)
                print(f"  • {char.name}{copy_info}: {char.path.value[:30]} Lv.{char.path_level} (+{dmg_bonus}% dmg) ({char.path_exp}/100 EXP)")
            else:
                print(f"  • {char.name}: No path")
        input("\nPress Enter...")


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    print(f"\n{'=' * 90}")
    slow_print("👊👊👊 LOOKISM: AWAKENED FIST v10 — DEEP RESEARCH CANON EDITION 👊👊👊", 0.02)
    print("    ALL BUGS FIXED | CANON CORRECTED | MECHANICS FULLY WIRED | 39 FIGHTERS")
    print("    Based on Park Tae-joon's Lookism (2014-2025)")
    print("=" * 90)
    print("\nv10 FIXES (Deep Research Canon Pass):")
    print("  ✅ CANON-Z1: Cheon Shinmyeong rank corrected to 38 (was 0, same as Gapryong)")
    print("  ✅ CANON-Z2: Ryuhei 'Yamazaki Blood' removed — he has no Yamazaki connection")
    print("  ✅ CANON-Z3: Vin Jin Judo/Kudo replaced with Ssireum-only + Dirty Brawling")
    print("  ✅ CANON-Z4: Jichang Kwak realms SPEED+STRENGTH → SPEED+TECHNIQUE")
    print("  ✅ CANON-Z5: Tom Lee TECHNIQUE realm removed (wild instinct, not technical)")
    print("  ✅ CANON-Z6: Gongseob Ji title 'The Monk' → 'The Vice King'")
    print("  ✅ CANON-Z7: All 39 characters now have correct affiliation strings")
    print("  ✅ CANON-Z8: Gun Park TENACITY realm removed → STRENGTH+TECHNIQUE only")
    print("  ✅ CANON-Z9: Gitae Kim title 'Unknown Heir' → 'Gapryong's Heir'")
    print("  ✅ BUG-V1: silver_yarn_active + silver_yarn_timer serialized in save/load")
    print("  ✅ BUG-V2: Johan copy_technique list/dict desync fixed (rebuild instead of dead-end)")
    print("  ✅ BUG-V3: Baekho Beast Mode now type=buff — correctly sets beast_mode flag (+60%)")
    print("  ✅ BUG-V4: Gapryong Defense now gives 2 turns as described (was hardcoded 1)")
    print("  ✅ BUG-V5: enemy_turn Silver Yarn bind effect now fires for enemy Manager Kim")
    print("  ✅ BUG-V6: cleanup() skips dead party members (no timer tick on corpses)")
    print("  ✅ BUG-V7: Fighter count corrected to 39 (was wrong 41)")
    print("  ✅ BUG-V8: Skip action energy fixed — gives +15 net (not +30 with regen doubling)")
    print("\nv4 FIXES:")
    print("  ✅ BUG-A:  Realm evasion/counter now guarded by realm_timer > 0")
    print("  ✅ BUG-B:  Iron Fortress double reduction fixed (was 75%, now correct 50%)")
    print("  ✅ BUG-C:  enemy_turn no longer pre-halves damage; take_damage handles it")
    print("  ✅ BUG-F:  Boss Rush & Crew Gauntlet now use lambda factories (no stale HP)")
    print("  ✅ BUG-H:  Realm timer starts at 6 → 5 effective combat turns")
    print("  ✅ BUG-O:  temp_buffs serialized in save/load")
    print("  ✅ MECH-1: RealmEffect values now drive actual combat checks")
    print("  ✅ MECH-3: STRENGTH realm armor_break reduces enemy defense effectiveness")
    print("  ✅ MECH-4: TECHNIQUE realm +40% accuracy represented as damage bonus")
    print("  ✅ MECH-5: SPEED double strike applies to infinity techniques too")
    print("  ✅ MECH-6: path_level grants +2% damage per level above 1")
    print("  ✅ MECH-7: Johan Veinous Rage ability wired (+80% damage, 3 turns)")
    print("  ✅ MECH-8: Manager Kim Silver Yarn status wired (+20% damage while active)")
    print("  ✅ MECH-9: Mandeok Titan Boost ability wired (+30% damage, 3 turns)")
    print("  ✅ MECH-10: Enemy fallback energy-fail shows 'conserves energy' message")
    print("  ✅ CANON-H: Eli Jang realms → [STRENGTH, OVERCOMING]")
    print("  ✅ CANON-L: Shingen Yamazaki realm_list → [] (not a Korean Gyeongji user)")
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
