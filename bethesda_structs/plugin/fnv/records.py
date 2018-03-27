# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

from construct import *
from multidict import CIMultiDict

from ._common import *


ACTI_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Sound - Looping'),
    ('VNAM', FNV_FormID(['SOUN']) * 'Sound - Activation'),
    ('INAM', FNV_FormID(['SOUN']) * 'Radio Template'),
    ('RNAM', FNV_FormID(['TACT']) * 'Radio Station'),
    ('WNAM', FNV_FormID(['WATR']) * 'Water Type'),
    ('XATO', CString('utf8') * 'Activation Prompt'),
],
    **FNV_ModelCollection,
    **FNV_DestructionCollection
)


AMMO_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Struct(
        "speed" / Float32l,
        "flags" / FlagsEnum(
            Int8ul,
            ignores_normal_weapon_resistance=0x1,
            non_playable=0x2
        ),
        "unused" / Bytes(3),
        "value" / Int32sl,
        "clip_rounds" / Int8ul
    )),
    ('DAT2', Struct(
        "projectiles_per_shot" / Int32ul,
        "projectile" / FNV_FormID(['PROJ']),
        "weight" / Float32l,
        "consumed_ammo" / FNV_FormID(['AMMO', 'MISC']),
        "consumed_percentage" / Float32l
    )),
    ('ONAM', CString('utf8') * 'Short Name'),
    ('QNAM', CString('utf8') * 'Abbreviation'),
    ('RCIL', FNV_FormID(['AMEF']) * 'Ammo Effect'),
],
    **FNV_ModelCollection,
    **FNV_DestructionCollection
)


ARMO_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('EITM', FNV_FormID(['ENCH', 'SPEL']) * 'Object Effect'),
    ('BMDT', Struct(
        "biped_flags" / FlagsEnum(
            Int32ul,
            head=0x00000001,
            hair=0x00000002,
            upper_body=0x00000004,
            left_hand=0x00000008,
            right_hand=0x00000010,
            weapon=0x00000020,
            pipboy=0x00000040,
            backpack=0x00000080,
            necklace=0x00000100,
            headband=0x00000200,
            hat=0x00000400,
            eye_glasses=0x00000800,
            nose_ring=0x00001000,
            earrings=0x00002000,
            mask=0x00004000,
            choker=0x00008000,
            mouth_object=0x00010000,
            body_addon_1=0x00020000,
            body_addon_2=0x00040000,
            body_addon_3=0x00080000
        ),
        "general_flags" / FlagsEnum(
            Int8ul,
            unknown_1=0x01,
            unknown_2=0x02,
            has_backpack=0x04,
            medium=0x08,
            unknown_3=0x10,
            power_armor=0x20,
            non_playable=0x40,
            heavy=0x80
        ),
        "unused" / GreedyBytes
    ) * 'Biped Data'),
    ('ICON', CString('utf8') * 'Male Inventory Icon Filename'),
    ('MICO', CString('utf8') * 'Male Message Icon Filename'),
    ('ICO2', CString('utf8') * 'Female Inventory Icon Filename'),
    ('MIC2', CString('utf8') * 'Female Message Icon Filename'),
    ('BMCT', CString('utf8') * 'Ragdoll Constraint Template'),
    ('REPL', FNV_FormID(['FLST']) * 'Repair List'),
    ('BIPL', FNV_FormID(['FLST']) * 'Biped Model List'),
    ('ETYP', FNV_EquipmentTypeEnum * 'Equipment Type'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Struct(
        "value" / Int32sl,
        "max_condition" / Int32sl,
        "weight" / Float32l
    ) * 'Data'),
    ('DNAM', Struct(
        "ar" / ExprAdapter(Int16sl, (obj_ / 100), (obj_ * 100)), # NOTE: value is divided by 100
        "flags" / FlagsEnum(
            Int16ul,
            modulates_voice=0x0001
        ),
        "dt" / Float32l,
        "_unknown_0" / Bytes(4)
    ) * 'Unknown'), # FIXME: missing description
    ('BNAM', Enum(
        Int32ul,
        no=0,
        yes=1
    ) * 'Overrides Animation Sounds'),
    ('SNAM', Struct(
        "sound" / FNV_FormID(['SOUN']),
        "chance" / Int8ul,
        "_unknown_0" / Bytes(3),
        "type" / Enum(
            Int32ul,
            run=19,
            run_in_armor=20,
            sneak=21,
            sneak_in_armor=22,
            walk=23,
            walk_in_armor=24
        )
    ) * 'Animation Sound'),
    ('TNAM', FNV_FormID(['ARMO']) * 'Animation Sound Template')
],
    **FNV_ModelCollection,
    **FNV_Model2Collection,
    **FNV_Model3Collection,
    **FNV_Model4Collection
)


CONT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('DATA', Struct(
        "flags" / FlagsEnum(
            Int8ul,
            _unknown_0=0x1,
            respawns=0x2
        ),
        "weight" / Float32l
    ) * 'Data'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Sound - Open'),
    ('QNAM', FNV_FormID(['SOUN']) * 'Sound - Close'),
    ('RNAM', FNV_FormID(['SOUN']) * 'Sound - Random / Looping'),
],
    **FNV_ModelCollection,
    **FNV_ItemCollection,
    **FNV_DestructionCollection
)


DOOR_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Sound - Open'),
    ('ANAM', FNV_FormID(['SOUN']) * 'Sound - Close'),
    ('BNAM', FNV_FormID(['SOUN']) * 'Sound - Looping'),
    ('FNAM', FlagsEnum(
        Int8ul,
        _unknown_0=0x01,
        automatic_door=0x02,
        hidden=0x04,
        minimal_use=0x08,
        sliding_door=0x10
    ) * 'Flags'),
],
    **FNV_ModelCollection,
    **FNV_DestructionCollection
)


FACT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('FULL', CString('utf8') * 'Name'),
    ('XNAM', Struct(
        "faction" / FNV_FormID(['FACT', 'RACE']),
        "modifier" / Int32sl,
        "group_combat_reaction" / Enum(
            Int32ul,
            neutral=0,
            enemy=1,
            ally=2,
            friend=3
        )
    ) * 'Relation'),
    ('DATA', Struct(
        "flags_1" / FlagsEnum(
            Int8ul,
            hidden_from_pc=0x01,
            evil=0x02,
            special_combat=0x04
        ),
        "flags_2" / FlagsEnum(
            Int8ul,
            track_crime=0x01,
            allow_sell=0x02
        ),
        "unused" / Byte[2]
    ) * 'Data'),
    ('CNAM', Float32l * 'Unused'),
    ('RNAM', Int32sl * 'Rank Number'),
    ('MNAM', CString('utf8') * 'Male'),
    ('FNAM', CString('utf8') * 'Female'),
    ('INAM', CString('utf8') * 'Insignia (unused)'),
    ('WMI1', FNV_FormID(['REPU']) * 'Reputation')
])


KEYM_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Struct(
        "value" / Int32sl,
        "weight" / Float32l
    ) * 'Data'),
    ('RNAM', FNV_FormID(['SOUN']) * 'Sound - Random/Looping')
],
    **FNV_ModelCollection,
    **FNV_DestructionCollection
)


MISC_Subrecords = KEYM_Subrecords


NAVI_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('NVER', Int32ul * 'Version'),
    ('NVMI', Struct(
        "_unknown_0" / Bytes(4),
        "navigation_mesh" / FNV_FormID(['NAVM']),
        "location" / FNV_FormID(['CELL', 'WRLD']),
        "grid_x" / Int16sl,
        "grid_y" / Int16sl,
        "_unknown_1" / GreedyBytes
    ) * 'Navigation Map Info'),
    ('NVCI', Struct(
        "_unknown_0" / FNV_FormID(['NAVM']),
        "_unknown_1" / FNV_FormID(['NAVM']),
        "_unknown_2" / FNV_FormID(['NAVM']),
        "door" / FNV_FormID(['REFR']),
    ) * 'Unknown')
])


NOTE_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Enum(
        Int8ul,
        sound=0,
        text=1,
        image=2,
        voice=3
    ) * 'Type'),
    ('XNAM', CString('utf8') * 'Texture'),
    ('TNAM', CString('utf8') * 'Text / Topic'),
    ('SNAM', FNV_FormID(['SOUN', 'NPC_', 'CREA']) * 'Sound / Actor'),
],
    **FNV_ModelCollection
)


NPC__Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ACBS', Struct(
        "flags" / FlagsEnum(
            Int32ul,
            biped=0x00000001,
            essential=0x00000002,
            is_chargen_face_preset=0x00000004,
            respawn=0x00000008,
            auto_calc_stats=0x00000010,
            _unknown_0=0x00000020,
            _unknown_1=0x00000040,
            level_mult=0x00000080,
            use_template=0x00000100,
            low_level_processing=0x00000200,
            _unknown_2=0x00000400,
            no_blood_spray=0x00000800,
            no_blood_decal=0x00001000,
            _unknown_3=0x00002000,
            _unknown_4=0x00004000,
            _unknown_5=0x00008000,
            _unknown_6=0x00010000,
            _unknown_7=0x00020000,
            _unknown_8=0x00040000,
            _unknown_9=0x00080000,
            no_vats_melee=0x00100000,
            _unknown_10=0x00200000,
            can_be_all_races=0x00400000,
            auto_calc_services=0x00800000,
            _unknown_11=0x01000000,
            _unknown_12=0x02000000,
            no_knockdowns=0x03000000,
            not_pushable=0x08000000,
            _unknown_13=0x10000000,
            _unknown_14=0x20000000,
            not_rotating_to_headtrack=0x40000000,
            _unknown_15=0x80000000
        ),
        "fatigue" / Int16ul,
        "barter_gold" / Int16ul,
        "level" / Int16sl,
        "calc_min" / Int16ul,
        "calc_max" / Int16ul,
        "speed_multiplier" / Int16ul,
        "karma" / Float32l,
        "disposition_base" / Int16sl,
        "template_flags" / FlagsEnum(
            Int16ul,
            use_traits=0x0001,
            use_stats=0x0002,
            use_factions=0x0004,
            use_actor_effect_list=0x0008,
            use_ai_data=0x0010,
            use_ai_packages=0x0020,
            use_model=0x0040,
            use_base_data=0x0080,
            use_inventory=0x0100,
            use_script=0x0200,
        ),
    ) * 'Configuration'),
    ('SNAM', Struct(
        "faction" / FNV_FormID(['FACT']),
        "rank" / Int8ul,
        "unused" / Bytes(3)
    ) * 'Faction'),
    ('INAM', FNV_FormID(['LVLI']) * 'Death Item'),
    ('VTCK', FNV_FormID(['VTCP']) * 'Voice'),
    ('TPLT', FNV_FormID(['NPC_', 'LVLN']) * 'Template'),
    ('RNAM', FNV_FormID(['RACE']) * 'Race'),
    ('SPLO', FNV_FormID(['SPEL']) * 'Actor Effect'),
    ('EITM', FNV_FormID(['ENCH', 'SPEL']) * 'Unarmed Attack Effect'),
    ('EAMT', FNV_AttackAnimationsEnum * 'Unarmed Attack Animation'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('AIDT', Struct(
        "aggression" / Enum(
            Int8ul,
            unaggressive=0,
            aggressive=1,
            very_aggressive=2,
            frenzied=3
        ),
        "confidence" / Enum(
            Int8ul,
            cowardly=0,
            cautious=1,
            average=2,
            brave=3,
            foolhardy=4
        ),
        "energy_level" / Int8ul,
        "responsibility" / Int8ul,
        "mood" / Enum(
            Int8ul,
            neutral=0,
            afraid=1,
            annoyed=2,
            cocky=3,
            drugged=4,
            pleasant=5,
            angry=6,
            sad=7
        ),
        "services" / FNV_ServiceFlags,
        "teaches" / FNV_SkillEnum,
        "maximum_training_level" / Int8ul,
        "assistance" / Enum(
            Int8sl,
            helps_nobody=0,
            helps_allies=1,
            helps_friends_and_allies=2
        ),
        "aggro_radius_behavior" / FlagsEnum(
            Int8ul,
            aggro_radius_behavior=0x01
        ),
        "aggro_radius" / Int32sl,
    ) * 'AI Data'),
    ('PKID', FNV_FormID(['PACK']) * 'Package'),
    ('CNAM', FNV_FormID(['CLAS']) * 'Class'),
    ('DATA', Struct(
        "base_health" / Int32sl,
        "strength" / Int8ul,
        "perception"  / Int8ul,
        "endurance" / Int8ul,
        "charisma" / Int8ul,
        "intelligence" / Int8ul,
        "agility" / Int8ul,
        "luck" / Int8ul,
        "unused" / Optional(GreedyBytes)
    ) * 'Data'),
    ('DNAM', Struct(
        "barter_value" / Int8ul,
        "big_guns_value" / Int8ul,
        "energy_weapons_value" / Int8ul,
        "explosives_value" / Int8ul,
        "lockpick_value" / Int8ul,
        "medicine_value" / Int8ul,
        "melee_weapons_value" / Int8ul,
        "repair_value" / Int8ul,
        "science_value" / Int8ul,
        "guns_value" / Int8ul,
        "sneak_value" / Int8ul,
        "speech_value" / Int8ul,
        "survival_value" / Int8ul,
        "unarmed_value" / Int8ul,
        "barter_offset" / Int8ul,
        "big_guns_offset" / Int8ul,
        "energy_weapons_offset" / Int8ul,
        "explosives_offset" / Int8ul,
        "lockpick_offset" / Int8ul,
        "medicine_offset" / Int8ul,
        "melee_weapons_offset" / Int8ul,
        "repair_offset" / Int8ul,
        "science_offset" / Int8ul,
        "guns_offset" / Int8ul,
        "sneak_offset" / Int8ul,
        "speech_offset" / Int8ul,
        "survival_offset" / Int8ul,
        "unarmed_offset" / Int8ul,
    ) * 'Skills'),
    ('PNAM', FNV_FormID(['HDPT']) * 'Head Part'),
    ('HNAM', FNV_FormID(['HAIR']) * 'Hair'),
    ('LNAM', Float32l * 'Hair Length'),
    ('ENAM', FNV_FormID(['EYES']) * 'Eyes'),
    ('HCLR', FNV_RGBAStruct * 'Hair Color'),
    ('ZNAM', FNV_FormID(['CSTY'])),
    ('NAM4', FNV_ImpactMaterialEnum * 'Impact Material Type'),
    ('FGGS', GreedyBytes * 'Facegen Geometry - Symmetric'),
    ('FGGA', GreedyBytes * 'Facegen Geometry - Asymmetric'),
    ('FGTS', GreedyBytes * 'Facegen Texture - Symmetric'),
    ('NAM5', Int16ul * 'Unknown'),
    ('NAM6', Float32l * 'Height'),
    ('NAM7', Float32l * 'Weight'),
],
    **FNV_ModelCollection,
    **FNV_ItemCollection,
    **FNV_DestructionCollection
)


SCPT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID')
],
    **FNV_ScriptCollection
)


STAT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('BRUS', Enum(
        Int8sl,
        none=-1,
        bush_a=0,
        bush_b=1,
        bush_c=2,
        bush_d=3,
        bush_e=4,
        bush_f=5,
        bush_g=6,
        bush_h=7,
        bush_i=8,
        bush_j=9
    ) * 'Passthrough Sound'),
    ('RNAM', FNV_FormID(['SOUN']) * 'Sound - Random / Looping')
],
    **FNV_ModelCollection
)


TACT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', FNV_ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Looping Sound'),
    ('VNAM', FNV_FormID(['VTYP']) * 'Voice Type'),
    ('INAM', FNV_FormID(['SOUN']) * 'Radio Template'),
],
    **FNV_ModelCollection,
    **FNV_DestructionCollection
)


TES4_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OFST', GreedyBytes * 'Unknown'),
    ('DELE', GreedyBytes * 'Unknown'),
    ('HEDR', Struct(
        "version" / Float32l,
        "num_records" / Int32ul,
        "next_object_id" / Int32ul
    ) * 'Header'),
    ('CNAM', CString('utf8') * 'Author'),
    ('SNAM', CString('utf8') * 'Description'),
    ('MAST', CString('utf8') * 'Master'),
    ('DATA', Int64ul * 'File Size'),
    ('ONAM', GreedyRange(Int32ul) * 'Overridden Records'), # FIXME: Greedy FNV_FormID([REFR, ACHR, ACRE, PMIS, PBEA, PGRE, LAND, NAVM])
    ('SCRN', GreedyBytes * 'Screenshot')
])


RecordMap = CIMultiDict({
    'ACTI': ACTI_Subrecords,
    'AMMO': AMMO_Subrecords,
    'ARMO': ARMO_Subrecords,
    'CONT': CONT_Subrecords,
    'DOOR': DOOR_Subrecords,
    'FACT': FACT_Subrecords,
    'KEYM': KEYM_Subrecords,
    'MISC': MISC_Subrecords,
    'NAVI': NAVI_Subrecords,
    'NOTE': NOTE_Subrecords,
    'NPC_': NPC__Subrecords,
    'SCPT': SCPT_Subrecords,
    'STAT': STAT_Subrecords,
    'TACT': TACT_Subrecords,
    'TES4': TES4_Subrecords
})
