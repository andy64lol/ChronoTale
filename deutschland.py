"""
Deutschland: A HOI4-style Text-Based Strategy Game
===================================================
A text-based grand strategy game inspired by Hearts of Iron 4, where you
manage a nation through economic, diplomatic, and military challenges.

Features:
- Nation management: economy, military, research
- Event-based story progression
- Historical context with alternative history possibilities
- Focus tree system for national development
- War and diplomacy mechanics
- Colorful terminal interface using colorama
"""

import os
import sys
import time
import random
import json
import math
import textwrap
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

# Game constants
VERSION = "1.2.0"
SAVE_FOLDER = "saves"
MAX_SAVE_SLOTS = 5

# Game ending types
ENDINGS = {
    # Positive Endings
    "fuhrers_reich": {
        "name": "The Führer's Reich",
        "description": ("Under your leadership, the Third Reich has achieved total domination "
                        "of Europe. Fascism reigns supreme, and Germany stands as the uncontested "
                        "hegemon of the continent. The thousand-year Reich that Hitler envisioned "
                        "has become reality."),
        "requirements": {
            "player_nation": "germany",
            "government": "Fascist",
            "conquered_nations": [
                "france", "poland", "belgium", "netherlands", 
                "denmark", "norway", "yugoslavia"
            ],
            "year_min": 1940
        },
        "type": "victory"
    },

    # Spain Endings
    "spanish_blue_division": {
        "name": "The Blue Division",
        "description": ("While officially maintaining neutrality, you have sent the División "
                        "Azul to fight alongside German forces against the Soviet Union. These "
                        "Spanish volunteers have distinguished themselves on the Eastern Front, "
                        "and Franco's regime enjoys increased favor with the Axis powers while "
                        "still avoiding a full declaration of war that might leave Spain vulnerable."),
        "requirements": {
            "player_nation": "spain",
            "focus_completed": ["anti_communist_volunteers"],
            "not_at_war": True
        },
        "type": "victory"
    },
    "spanish_empire_restored": {
        "name": "The Restored Spanish Empire",
        "description": ("Taking advantage of the chaotic war in Europe, you have reclaimed "
                        "Gibraltar from the British and expanded into North Africa. Franco's regime "
                        "has successfully restored parts of the old Spanish Empire, elevating Spain "
                        "once again to the status of a colonial power while carefully avoiding direct "
                        "confrontation with the major combatants."),
        "requirements": {
            "player_nation": "spain",
            "focus_completed": ["reclaim_empire", "gibraltar_operation"],
            "government": "Fascist"
        },
        "type": "victory"
    },
    "spanish_republicans_triumphant": {
        "name": "La España Republicana",
        "description": ("In a shocking turn of events, Republican forces have regained control "
                        "of your country. The fascist government of Francisco Franco has been overthrown, "
                        "democracy has been restored, and Spain has joined the Allied powers in "
                        "their struggle against fascism throughout Europe. The dream of a democratic "
                        "Spain lives on."),
        "requirements": {
            "player_nation": "spain",
            "focus_completed": ["restore_republic", "join_allies"],
            "government": "Democratic"
        },
        "type": "victory"
    },

    # Turkey Endings
    "new_ottoman_empire": {
        "name": "The New Ottoman Empire",
        "description": ("You have seized the opportunity provided by the global conflict to "
                        "restore former Ottoman territories in the Middle East and Balkans. Under "
                        "your leadership, Turkey has once again become a major power straddling "
                        "Europe and Asia, reclaiming its historical position as a dominant force "
                        "in the region."),
        "requirements": {
            "player_nation": "turkey",
            "focus_completed": ["ottoman_restoration", "balkan_dominance"],
            "conquered_nations": ["greece", "bulgaria"],
            "year_min": 1942
        },
        "type": "victory"
    },
    "turkish_neutrality_triumph": {
        "name": "The Neutral Mediator",
        "description": ("Through cautious diplomacy and strategic positioning, you have "
                        "successfully maintained neutrality throughout the devastating global "
                        "conflict. Your nation has prospered by trading with both sides while "
                        "building up its industrial and military capacity. As Europe lies in ruins, "
                        "Turkey stands poised to become a significant regional power in the post-war era."),
        "requirements": {
            "player_nation": "turkey",
            "focus_completed": ["strategic_neutrality", "industrial_modernization"],
            "not_at_war": True,
            "stability": 70
        },
        "type": "victory"
    },

    # Sweden Endings
    "nordic_union": {
        "name": "The Nordic Union",
        "description": "You have united the Nordic countries under a defensive alliance that has successfully maintained independence throughout the war. This 'Third Way' between the warring powers has preserved Scandinavian democracy and prosperity while much of Europe burns.",
        "requirements": {
            "player_nation": "sweden",
            "focus_completed": ["nordic_defense_pact", "scandinavian_cooperation"],
            "alliance_with": ["finland", "norway", "denmark"],
            "not_conquered": ["finland", "norway", "denmark"]
        },
        "type": "victory"
    },
    "swedish_iron_giant": {
        "name": "The Iron Giant",
        "description": "You have leveraged Sweden's vast iron resources to build a powerful industrial base and military. By carefully balancing relations with all major powers while remaining officially neutral, your nation has emerged from the war as one of the wealthiest and most stable in Europe, poised to play a major role in post-war reconstruction.",
        "requirements": {
            "player_nation": "sweden",
            "focus_completed": ["expand_mining_operations", "industrial_self_sufficiency"],
            "stability": 80,
            "not_at_war": True,
            "year_min": 1943
        },
        "type": "victory"
    },

    # Nationalist China Endings
    "china_unified": {
        "name": "China Unified",
        "description": "After years of struggle against both Japanese invaders and Communist insurgents, your Nationalist government has reunified China under its banner. With the Japanese expelled from the mainland and the Communist threat neutralized, China stands ready to take its place as a major power in the post-war order.",
        "requirements": {
            "player_nation": "nationalist_china",
            "focus_completed": ["anti_communist_campaign", "modernize_military"],
            "conquered_nations": ["communist_china"],
            "not_conquered": ["nationalist_china"]
        },
        "type": "victory"
    },
    "chinese_democracy": {
        "name": "The Chinese Republic",
        "description": "Your Nationalist government has successfully implemented democratic reforms while maintaining stability and territorial integrity. With support from Western democracies, China has emerged from conflict as a democratic nation with growing economic strength and international respect.",
        "requirements": {
            "player_nation": "nationalist_china",
            "focus_completed": ["constitutional_reforms", "american_aid_program"],
            "government": "Democratic",
            "stability": 70
        },
        "type": "victory"
    },
    "greater_east_asia": {
        "name": "Co-Prosperity Sphere Leader",
        "description": "In a shocking turn of events, you have joined Japan's Greater East Asia Co-Prosperity Sphere and become its dominant partner. Taking advantage of Japan's weakened position later in the war, your China has essentially taken control of the alliance, establishing itself as the preeminent power in East Asia.",
        "requirements": {
            "player_nation": "nationalist_china",
            "focus_completed": ["sino_japanese_cooperation", "asian_leadership"],
            "alliance_with": ["japan"],
            "stability": 60
        },
        "type": "victory"
    },

    # Communist China Endings
    "peoples_republic": {
        "name": "The People's Republic of China",
        "description": "Your Chinese Communist Party has triumphed in the civil war, establishing the People's Republic of China. Under Chairman Mao's leadership, the new communist state is implementing sweeping land reforms and industrialization programs while consolidating control over the vast nation.",
        "requirements": {
            "player_nation": "communist_china",
            "focus_completed": ["peoples_war", "defeat_nationalists"],
            "conquered_nations": ["nationalist_china"],
            "government": "Communist"
        },
        "type": "victory"
    },
    "sino_soviet_alliance": {
        "name": "Sino-Soviet Alliance",
        "description": "You have formed a powerful alliance with the Soviet Union, creating a unified communist bloc that spans the Eurasian continent. With Soviet industrial aid and military support, your China is rapidly developing into a formidable power that will shape the future of Asia and the world.",
        "requirements": {
            "player_nation": "communist_china",
            "focus_completed": ["soviet_advisors", "socialist_industrialization"],
            "alliance_with": ["ussr"],
            "stability": 65
        },
        "type": "victory"
    },
    "third_way_socialism": {
        "name": "The Third Way",
        "description": "You have charted your own unique path to socialism, independent of Soviet influence. By balancing pragmatic economic policies with revolutionary ideology, your China has created a distinct model of development that maintains communist principles while adapting to Chinese realities.",
        "requirements": {
            "player_nation": "communist_china",
            "focus_completed": ["self_reliance", "chinese_characteristics"],
            "stability": 70,
            "not_at_war": True
        },
        "type": "victory"
    },

    # Ultranationalist Endings for Each Nation
    "greater_german_reich": {
        "name": "The Greater Germanic Reich",
        "description": "You have achieved Hitler's ultimate vision - a vast empire stretching from the Atlantic to the Urals. All opposition has been crushed, and Germanic peoples dominate Europe. The New Order has been established, and the Third Reich will last a thousand years.",
        "requirements": {
            "player_nation": "germany",
            "government": "Fascist",
            "conquered_nations": ["france", "poland", "belgium", "netherlands", "denmark", "norway", "yugoslavia", "greece", "ussr"],
            "year_min": 1943
        },
        "type": "victory"
    },
    "italian_empire_reborn": {
        "name": "The New Roman Empire",
        "description": "You have fulfilled Mussolini's promise to restore the glory of ancient Rome. Italian dominance extends across the Mediterranean, with control of North Africa, the Balkans, and parts of the Middle East. The Mediterranean has truly become Mare Nostrum - 'Our Sea'.",
        "requirements": {
            "player_nation": "italy",
            "government": "Fascist",
            "conquered_nations": ["france", "greece", "yugoslavia", "turkey"],
            "focus_completed": ["roman_ambitions"]
        },
        "type": "victory"
    },
    "rising_sun_ascendant": {
        "name": "Empire of the Rising Sun",
        "description": "You have established complete dominance over East Asia and the Pacific. Western colonial powers have been expelled from their territories, and Japan now controls the vast resources of China, Southeast Asia, and the Pacific islands. The Greater East Asia Co-Prosperity Sphere has become reality.",
        "requirements": {
            "player_nation": "japan",
            "government": "Fascist",
            "conquered_nations": ["china", "philippines", "netherlands_east_indies", "malaya"],
            "focus_completed": ["greater_east_asia"]
        },
        "type": "victory"
    },
    "soviet_world_revolution": {
        "name": "Global Soviet Revolution",
        "description": "You have fulfilled Marx's prediction of world revolution. Your Red Army tanks have rolled across Europe, toppling capitalist governments and establishing workers' states. With Germany crushed and Europe turned red, the tide of communism is unstoppable.",
        "requirements": {
            "player_nation": "ussr",
            "government": "Communist",
            "conquered_nations": ["germany", "poland", "romania", "hungary", "czechoslovakia"],
            "focus_completed": ["world_revolution"]
        },
        "type": "victory"
    },
    "british_empire_preserved": {
        "name": "The Sun Never Sets",
        "description": "Against all odds, you have not only survived but have emerged stronger than before. With continental enemies defeated and the Empire preserved, Britain remains the dominant global power. The sun shall never set on your British Empire.",
        "requirements": {
            "player_nation": "uk",
            "focus_completed": ["imperial_federation", "secure_empire"],
            "conquered_nations": ["germany", "italy"],
            "not_conquered": ["india", "malaya", "egypt"]
        },
        "type": "victory"
    },
    "polish_intermarium": {
        "name": "The Intermarium",
        "description": "You have achieved Poland's long-held dream of creating a federation of Central and Eastern European states as a buffer between Germany and Russia. This 'Międzymorze' alliance stretches from the Baltic to the Black Sea, with Poland as its leader.",
        "requirements": {
            "player_nation": "poland",
            "government": "Military",
            "focus_completed": ["intermarium_alliance"],
            "conquered_nations": ["lithuania", "belarus"],
            "alliance_with": ["romania", "czechoslovakia", "hungary"]
        },
        "type": "victory"
    },
    "turkish_neo_ottoman": {
        "name": "Neo-Ottoman Caliphate",
        "description": "You have reclaimed Turkey's Ottoman legacy, expanding throughout the Middle East and North Africa. The Caliphate has been restored, and Turkish influence extends across the former Ottoman territories. Istanbul once again is the center of a powerful Islamic empire.",
        "requirements": {
            "player_nation": "turkey",
            "government": "Fascist",
            "focus_completed": ["restore_caliphate", "ottoman_ambitions"],
            "conquered_nations": ["syria", "iraq", "greece", "egypt"]
        },
        "type": "victory"
    },
    "spanish_falangist_empire": {
        "name": "The Falangist Empire",
        "description": "Under Franco's leadership, you have rebuilt Spain's colonial empire and established it as a major European power. With territories in Africa, control of Gibraltar, and influence across Latin America, Spain has reclaimed its place among the world's great powers.",
        "requirements": {
            "player_nation": "spain",
            "government": "Fascist",
            "focus_completed": ["falangist_state", "colonial_restoration"],
            "conquered_nations": ["portugal"]
        },
        "type": "victory"
    },
    "swedish_nordic_empire": {
        "name": "Nordic Empire",
        "description": "You have abandoned Sweden's historical neutrality and established dominance over all Nordic countries. This new regional power controls the Baltic Sea and the valuable resources of Scandinavia, creating a formidable empire in Northern Europe.",
        "requirements": {
            "player_nation": "sweden",
            "government": "Fascist",
            "focus_completed": ["swedish_militarism"],
            "conquered_nations": ["norway", "finland", "denmark"]
        },
        "type": "victory"
    },
    "greater_china": {
        "name": "Greater Chinese Empire",
        "description": "You have unified all Chinese territories and extended your influence throughout East Asia. Under the iron rule of the Kuomintang, China has become an ultranationalist power that has driven out foreign influences and reclaimed its position as the Middle Kingdom.",
        "requirements": {
            "player_nation": "nationalist_china",
            "government": "Fascist",
            "focus_completed": ["chinese_nationalism", "reclaim_lost_territories"],
            "conquered_nations": ["communist_china", "tibet", "mongolia"]
        },
        "type": "victory"
    },
    "communist_asia": {
        "name": "Communist Federation of Asia",
        "description": "Your revolution has spread beyond China's borders, with communist regimes established throughout East and Southeast Asia. Under your leadership, this federation of communist states has become a powerful bloc rivaling both the Soviet Union and Western powers.",
        "requirements": {
            "player_nation": "communist_china",
            "government": "Communist",
            "focus_completed": ["permanent_revolution", "asian_communism"],
            "conquered_nations": ["nationalist_china", "korea", "thailand"]
        },
        "type": "victory"
    },
    "philippine_dominance": {
        "name": "Philippine Dominance",
        "description": "You have led the Philippines from colonial rule to become a dominant power in Southeast Asia. Building on American support and your strategic position, you have established military and economic control over neighboring territories and waters.",
        "requirements": {
            "player_nation": "philippines",
            "focus_completed": ["philippine_nationalism", "pacific_security"],
            "conquered_nations": ["malaya", "netherlands_east_indies"]
        },
        "type": "victory"
    },
    "thai_southeast_asia": {
        "name": "Thai Dominion",
        "description": "You have reclaimed Thailand's historical territories and established your nation as the dominant power in mainland Southeast Asia. Under your military leadership, Thailand controls the strategic regions of Indochina and the Malay Peninsula.",
        "requirements": {
            "player_nation": "thailand",
            "government": "Military",
            "focus_completed": ["greater_thailand", "military_supremacy"],
            "conquered_nations": ["burma", "french_indochina", "malaya"]
        },
        "type": "victory"
    },
    "dutch_colonial_fortress": {
        "name": "Colonial Fortress",
        "description": "You have broken free from the Netherlands and established the East Indies as a powerful independent state controlling the resource-rich islands of Southeast Asia. Your strategic position and vast resources make you the gatekeeper of Asian trade.",
        "requirements": {
            "player_nation": "netherlands_east_indies",
            "focus_completed": ["resource_dominance", "naval_supremacy"],
            "conquered_nations": ["malaya", "philippines"]
        },
        "type": "victory"
    },
    "australian_pacific_dominion": {
        "name": "Pacific Dominion",
        "description": "You have led Australia out from Britain's shadow to establish its own empire in the South Pacific. With control of numerous islands and influence throughout the region, Australia has become a major power in its own right under your leadership.",
        "requirements": {
            "player_nation": "australia",
            "focus_completed": ["australian_imperialism", "pacific_strategy"],
            "conquered_nations": ["netherlands_east_indies", "new_guinea"]
        },
        "type": "victory"
    },
    "marx_revival": {
        "name": "The Revival of Karl Marx's Dreams of a Free Deutschland",
        "description": "Your Communist revolution has succeeded in Germany! The workers have cast off their chains and you have established a true proletarian state. Karl Marx's vision of a communist Germany has been realized under your leadership, and the revolution is spreading across Europe.",
        "requirements": {
            "player_nation": "germany",
            "government": "Communist",
            "stability": 65,
            "conquered_nations": ["poland"],
            "in_faction_with": ["ussr"]
        },
        "type": "victory"
    },
    "center_of_democracy": {
        "name": "The Center of Democracy",
        "description": "You have transformed Germany into a beacon of democratic values in the heart of Europe. Rejecting both fascism and communism, you have established a stable, prosperous democratic state that serves as a model for other nations.",
        "requirements": {
            "player_nation": "germany",
            "government": "Democratic",
            "stability": 80,
            "war_support": 25,
            "year_min": 1939
        },
        "type": "victory"
    },
    "european_union": {
        "name": "Europe Under a Union",
        "description": "Rather than conquest, you have led Germany in the formation of a peaceful European Union. Nations have voluntarily joined this new economic and political alliance you've created, fostering unprecedented cooperation and prosperity across the continent.",
        "requirements": {
            "player_nation": "germany",
            "government": "Democratic",
            "faction_members_count": 5,
            "year_min": 1940
        },
        "type": "victory"
    },
    "kaiser_return": {
        "name": "Kaiser's Return",
        "description": "You have restored the monarchy! Under your leadership, the Hohenzollern dynasty once again sits on the German throne. The Kaiser rules with a firm but fair hand, and you have returned Germany to its imperial glory while maintaining modern governance.",
        "requirements": {
            "player_nation": "germany",
            "government": "Monarchist",
            "stability": 70,
            "completed_focus": "restore_kaiser"
        },
        "type": "victory"
    },
    "greater_germanic_reich": {
        "name": "The Greater Germanic Reich",
        "description": "You have realized the dream of a unified Germanic Empire! All German-speaking peoples and territories are now united under the glorious banner of your Reich. Austria, Switzerland, the Sudetenland, Alsace-Lorraine, Luxembourg, and German enclaves throughout Europe have been incorporated into a single, mighty Germanic state that dominates Central Europe. The borders now reflect the true ethnic and cultural boundaries of the Germanic peoples. This is not merely a conquest but a historical reunification, fulfilling the ancient vision of a united Volk. With the combined industrial might, cultural heritage, and military power of all Germanic peoples, you have created a new continental superpower that will shape the destiny of Europe for a thousand years to come.",
        "requirements": {
            "player_nation": "germany",
            "government": "Fascist",
            "conquered_nations": ["austria", "switzerland", "czechoslovakia", "luxembourg", "liechtenstein"],
            "partial_control": ["france", "poland", "belgium", "netherlands", "denmark"],
            "stability": 70,
            "war_support": 80,
            "year_min": 1940,
            "completed_focus": "anschluss"
        },
        "type": "victory"
    },
    "global_socialist_republic": {
        "name": "Global Socialist Republic",
        "description": "Under your leadership, Germany has become the center of a worldwide socialist revolution. Together with the Soviet Union, you have spread communism across Europe and beyond. The workers of the world have truly united, just as Marx and Engels envisioned.",
        "requirements": {
            "player_nation": "germany",
            "government": "Communist",
            "conquered_nations": ["france", "italy", "poland"],
            "in_faction_with": ["ussr"],
            "year_min": 1942
        },
        "type": "victory"
    },
    "new_rhineland": {
        "name": "The New Rhineland Federation",
        "description": "Under your guidance, a new democratic federation has emerged in the heart of Europe, centered around the Rhine river. You have led Germany to embrace democratic values and form a peaceful federation with its western neighbors, creating a powerful economic and political union. This federation you've built serves as a bulwark against both fascism and communism, ensuring peace and prosperity for its citizens. The Rhineland, once a contested region, now stands as the symbol of European cooperation and unity.",
        "requirements": {
            "player_nation": "germany",
            "government": "Democratic",
            "in_faction_with": ["france", "belgium", "netherlands", "luxembourg"],
            "stability": 85,
            "war_support": 30,
            "year_min": 1942,
            "completed_focus": "european_cooperation"
        },
        "type": "victory"
    },
    "kaisers_great_return": {
        "name": "Kaiser's Great Return and the New Order of Deutsch",
        "description": "You have restored the German monarchy with unprecedented power. Under your leadership, Kaiser Wilhelm III rules a new German Reich that encompasses much of Europe. This neo-feudal empire you've created combines modern industry with traditional aristocratic values, creating a unique socioeconomic system that rejects both communism and liberal democracy.",
        "requirements": {
            "player_nation": "germany",
            "government": "Monarchist",
            "stability": 80,
            "conquered_nations": ["france", "poland", "belgium", "netherlands"],
            "year_min": 1941
        },
        "type": "victory"
    },
    "marxist_united_earth": {
        "name": "The New Red Rising Nation of the Marxist State of United Earth",
        "description": "What began as your German revolution has transformed into a global communist utopia under your leadership. The boundaries between nations have dissolved as you've inspired workers everywhere to rise up against capitalism. Earth is now unified under a single Marxist government, with Berlin as its capital. Under your guidance, humanity stands ready to spread the revolution to the stars.",
        "requirements": {
            "player_nation": "germany",
            "government": "Communist",
            "conquered_nations": ["france", "italy", "uk", "poland"],
            "in_faction_with": ["ussr"],
            "year_min": 1944
        },
        "type": "victory"
    },
    "popes_roman_empire": {
        "name": "Pope's New Roman Empire: Sacred Germanic Roman Empire's Return",
        "description": "In a shocking turn of events, you have formed an alliance between Germany and the Vatican to create a new Holy Roman Empire. This theocratic state you've established unites German military might with Catholic spiritual authority. Under your arrangement, the Pope and Kaiser rule as dual sovereigns over a Europe returning to faith-based governance in the modern age.",
        "requirements": {
            "player_nation": "germany",
            "government": "Monarchist",
            "stability": 75,
            "conquered_nations": ["italy", "france", "poland", "austria"],
            "year_min": 1942
        },
        "type": "victory"
    },
    "one_banner_union": {
        "name": "New Union of German People Under One Banner",
        "description": "Under your leadership, all German-speaking peoples and territories have been united under a single flag. This Greater Germania you've created includes not just Germany and Austria, but parts of Switzerland, Poland, Czechoslovakia, and beyond. Cultural unity and shared language form the foundation of this new ethnic state that fulfills the dream of a unified German people.",
        "requirements": {
            "player_nation": "germany",
            "conquered_nations": ["austria", "czechoslovakia", "poland"],
            "stability": 70,
            "year_min": 1940
        },
        "type": "victory"
    },
    "center_of_germania": {
        "name": "Center of Germania: Union of Germanic Languages Nation",
        "description": "Beyond mere German unity, you've created a pan-Germanic federation uniting all Germanic peoples. Germans, Dutch, Danes, Swedes, Norwegians, and even the English are now part of a single cultural and political entity bound by their shared linguistic heritage. This Germanic Union you've established stands as a formidable power bloc dominating northern Europe.",
        "requirements": {
            "player_nation": "germany",
            "conquered_nations": ["denmark", "norway", "sweden", "netherlands", "belgium"],
            "stability": 65,
            "year_min": 1942
        },
        "type": "victory"
    },
    "satanist_theocracy": {
        "name": "Union for the Hell: Germanic Satanist Theocracy",
        "description": "What began as your political reform has devolved into something far darker. Under your influence, a radical occult movement has seized control of Germany, establishing a state-sponsored satanic church. Ancient pagan rituals blend with modern fascist aesthetics in this bizarre theocracy you've created that terrifies and fascinates the world in equal measure.",
        "requirements": {
            "player_nation": "germany",
            "stability": 50,
            "war_support": 90,
            "year_min": 1940,
            "internal_conflicts": 1
        },
        "type": "victory"
    },

    # Bad Endings
    "permanent_civil_war": {
        "name": "Permanent Civil War",
        "description": "Under your leadership, Germany has descended into chaos. Multiple factions fight for control, and the nation is torn apart by a never-ending civil war. Your dream of a unified Germany lies in ruins as warlords carve out territories across the former reich.",
        "requirements": {
            "player_nation": "germany",
            "stability": 20,
            "war_support": 90,
            "internal_conflicts": 3
        },
        "type": "disaster"
    },
    "nuclear_annihilation": {
        "name": "Nuclear Annihilation",
        "description": "The war has escalated beyond all control under your leadership. Experimental atomic weapons have been deployed against German cities. Berlin is a radioactive crater, and millions are dead. The Germany you fought to build has effectively ceased to exist in the atomic fire.",
        "requirements": {
            "player_nation": "germany",
            "war_with": ["usa", "uk"],
            "year_min": 1945,
            "world_tension": 90
        },
        "type": "disaster"
    },
    "soviet_occupation": {
        "name": "Soviet Occupation",
        "description": "The Red Army has swept across Germany, crushing all resistance. The Soviet flag flies over the ruins of Berlin, and Stalin's commissars impose a brutal communist regime. Your leadership has led Germany from one totalitarian system to another as your nation falls under Soviet control.",
        "requirements": {
            "player_nation": "germany",
            "government": "Fascist",
            "at_war_with": ["ussr"],
            "stability": 30,
            "year_min": 1942
        },
        "type": "disaster"
    },
    "allied_partition": {
        "name": "Allied Partition",
        "description": "Germany has been utterly defeated by the Allied powers under your rule. The country you led is now divided into occupation zones, and its future as a unified nation is uncertain. German sovereignty is a thing of the past as foreign powers determine its fate, erasing your legacy.",
        "requirements": {
            "player_nation": "germany",
            "government": "Fascist",
            "at_war_with": ["usa", "uk", "france"],
            "stability": 25,
            "year_min": 1943
        },
        "type": "disaster"
    },
    "economic_collapse": {
        "name": "Economic Collapse",
        "description": "Your policies have led to complete economic ruin. Hyperinflation has returned with a vengeance, unemployment is rampant, and the German mark is worthless. The society you attempted to rebuild breaks down as hunger and desperation drive people to extremes.",
        "requirements": {
            "player_nation": "germany",
            "civilian_factories": 5,
            "military_factories": 2,
            "stability": 15,
            "year_min": 1938
        },
        "type": "disaster"
    },
    "purge_backfire": {
        "name": "The Purge Backfires",
        "description": "Your attempts to consolidate power through purges have backfired catastrophically. Military officers, seeing the writing on the wall, staged a coup against your leadership. You were shot while trying to escape, and the Germany you tried to control now faces an uncertain future under military rule.",
        "requirements": {
            "player_nation": "germany",
            "government": "Communist",
            "completed_focus": "great_purge",
            "stability": 30,
            "war_support": 60
        },
        "type": "disaster"
    },
    "coup_detat": {
        "name": "Coup d'Etat",
        "description": "Elements of the military, dissatisfied with your leadership, have seized control of the government. You are under house arrest, and generals now dictate policy. Your vision for Germany dies as martial law is declared across the nation.",
        "requirements": {
            "stability": 25,
            "war_support": 40,
            "at_war": True
        },
        "type": "disaster"
    },
    "assassination": {
        "name": "Leadership Assassination",
        "description": "A successful assassination plot has ended your rule. As your body was carried from the Reich Chancellery, power struggles erupted among your lieutenants. Germany is leaderless as factions vie for control amid growing chaos.",
        "requirements": {
            "stability": 35,
            "internal_conflicts": 2,
            "year_min": 1939
        },
        "type": "disaster"
    },
    "failed_nation": {
        "name": "Failed Nation",
        "description": "Germany has collapsed as a coherent state. Economic mismanagement, political infighting, and military failures have left the country in ruins. Foreign powers carve up German territory, and the concept of Germany as a unified nation-state may be lost to history for generations.",
        "requirements": {
            "stability": 10,
            "war_support": 20,
            "year_min": 1940
        },
        "type": "disaster"
    },
    "permanent_german_partition": {
        "name": "Permanent German Partition",
        "description": "The division of Germany has become permanent. East and West Germany have solidified into separate states with different ideologies, economies, and alliances. The Berlin Wall stands as a physical manifestation of the Cold War, and German reunification seems an impossible dream.",
        "requirements": {
            "at_war_with": ["usa", "uk", "france", "ussr"],
            "stability": 30,
            "year_min": 1945
        },
        "type": "disaster"
    },
    "churchills_plan": {
        "name": "Churchill's Pastoral Plan",
        "description": "Following Germany's defeat, Churchill's extreme proposal to deindustrialize Germany and return it to a pastoral state has been implemented. Industrial machinery has been dismantled, factories demolished, and urban centers depopulated. Germany is now a rural agricultural nation with limited technology and industry.",
        "requirements": {
            "at_war_with": ["uk"],
            "stability": 20,
            "military_factories": 2,
            "year_min": 1944
        },
        "type": "disaster"
    },
    "third_world_war": {
        "name": "Third World War: Humanity's Last Day on Earth",
        "description": "What began as a European conflict has escalated into global nuclear annihilation. Experimental atomic weapons have been deployed by multiple nations, resulting in unprecedented destruction. Human civilization itself now hangs in the balance as radiation and nuclear winter spread across the planet.",
        "requirements": {
            "at_war_with": ["usa", "uk", "france", "ussr"],
            "war_support": 80,
            "year_min": 1945
        },
        "type": "disaster"
    },
    "bavarian_independence": {
        "name": "Failed Unification: Independent German States",
        "description": "The German nation has fractured along regional lines. Bavaria, Saxony, Prussia, and other historical regions have declared independence, reverting to a pre-unification status quo. The dream of German unity that began in 1871 has ended, with the country now a patchwork of competing states.",
        "requirements": {
            "stability": 15,
            "internal_conflicts": 3,
            "year_min": 1939
        },
        "type": "disaster"
    },
    "rhineland_breakaway": {
        "name": "The New Rhineland Republic",
        "description": "The western regions of Germany have broken away to form the independent Rhineland Republic. With support from France and the Low Countries, this new democratic state has renounced German nationalism and embraced European integration. The remainder of Germany grows increasingly isolated.",
        "requirements": {
            "stability": 25,
            "internal_conflicts": 2,
            "year_min": 1940
        },
        "type": "disaster"
    },
    "morgenthau_germany": {
        "name": "Morgenthau's Agricultural Germany",
        "description": "The Morgenthau Plan has been fully implemented. Germany has been completely deindustrialized and converted into an agricultural country. Heavy industry is forbidden, cities have been depopulated, and millions of Germans now work as farmers. The great industrial power of Europe is no more.",
        "requirements": {
            "at_war_with": ["usa"],
            "stability": 20,
            "military_factories": 1,
            "year_min": 1944
        },
        "type": "disaster"
    },
    "churchill_plan": {
        "name": "Churchill's Plan: The United States of Europe",
        "description": "Winston Churchill's vision for post-war Germany has been realized. Rather than punitive measures, Germany has been reformed and integrated into a new European federation. This 'United States of Europe' includes former rivals working together under democratic principles, with Germany serving as the industrial and economic core. Though initially under Allied oversight, Germany has retained its cultural identity and industrial capacity, while being firmly embedded in a cooperative European framework designed to prevent future conflicts. The old militarism has been replaced by economic cooperation and shared prosperity.",
        "requirements": {
            "conquered_by": ["united_kingdom"],
            "government": "Democratic",
            "stability": 65,
            "world_tension": 10,
            "year_min": 1945
        },
        "type": "special"
    },
    "intermarium_federation": {
        "name": "The Intermarium Federation",
        "description": "Against all odds, Poland has managed to realize Józef Piłsudski's grand vision of an Intermarium - a federation of nations stretching from the Baltic to the Black Sea. This alliance of Central and Eastern European nations, led by Poland, provides a powerful counterbalance to both German and Soviet ambitions. With shared military coordination, economic integration, and diplomatic unity, the federation has become a significant European power, ensuring security and prosperity for all its member states.",
        "requirements": {
            "player_nation": "poland",
            "government": "Democratic",
            "stability": 70,
            "war_support": 50,
            "year_min": 1942,
            "faction_members_count": 5,
            "completed_focus": "intermarum_alliance"
        },
        "type": "victory"
    },
    "polish_commonwealth_restored": {
        "name": "The Polish-Lithuanian Commonwealth Reborn",
        "description": "Through diplomatic skill and strategic vision, Poland has recreated a modern version of the once-great Polish-Lithuanian Commonwealth. Uniting Poland, Lithuania, Latvia, Estonia, and parts of Ukraine under a single federal monarchy, this new Commonwealth has reclaimed its historical position as a major European power. With a constitutional monarchy balancing central authority with regional autonomy, the Commonwealth combines traditional values with modern democratic principles, creating a powerful and stable force in Eastern Europe.",
        "requirements": {
            "player_nation": "poland",
            "government": "Non-Aligned",
            "stability": 75,
            "war_support": 60,
            "conquered_nations": ["lithuania", "latvia", "estonia"],
            "partial_control": ["ukraine", "belarus"],
            "completed_focus": "restore_polish_monarchy"
        },
        "type": "victory"
    },
    "yugoslavia_balkan_federation": {
        "name": "The Balkan Federation",
        "description": "Yugoslavia has successfully united the diverse peoples of the Balkans under a single federal state. This federation, built on principles of equality and workers' self-management, has created a unique socialist system distinct from the Soviet model. With its industrial base rapidly expanding and ethnic tensions largely resolved, the Balkan Federation has emerged as a significant European power, offering a third path between Western capitalism and Eastern state socialism.",
        "requirements": {
            "player_nation": "yugoslavia",
            "government": "Communist",
            "stability": 70,
            "war_support": 40,
            "conquered_nations": ["albania", "bulgaria"],
            "partial_control": ["greece", "romania"],
            "completed_focus": "balkan_federation"
        },
        "type": "victory"
    },
    "greater_yugoslavia": {
        "name": "Greater Yugoslavia",
        "description": "Under strong monarchical leadership, Yugoslavia has expanded its borders to encompass historical Serbian lands and strategic territories throughout the Balkans. This enlarged kingdom has established itself as the dominant power in Southeastern Europe, effectively balancing between the great powers while maintaining its independence. The royal dynasty presides over a centralized state that has achieved stability through firm governance and military strength.",
        "requirements": {
            "player_nation": "yugoslavia",
            "government": "Non-Aligned",
            "stability": 65,
            "war_support": 70,
            "conquered_nations": ["albania"],
            "partial_control": ["greece", "bulgaria", "romania", "hungary"],
            "completed_focus": "royal_dictatorship"
        },
        "type": "victory"
    },
    "yugoslavian_collapse": {
        "name": "The Collapse of Yugoslavia",
        "description": "Unable to manage its internal ethnic tensions, Yugoslavia has fractured into multiple warring states. The dream of South Slavic unity lies in ruins as nationalist movements have taken control in each region, leading to bitter conflicts and ethnic cleansing. Foreign powers have intervened to pursue their own interests, turning the Balkans once again into Europe's powder keg.",
        "requirements": {
            "player_nation": "yugoslavia",
            "stability": 20,
            "internal_conflicts": 3,
            "at_war_with": ["germany", "italy"],
            "year_min": 1940
        },
        "type": "disaster"
    },
    "benelux_federation": {
        "name": "The Benelux Federation",
        "description": "Belgium, the Netherlands, and Luxembourg have united to form a powerful federation at the heart of Europe. Building on their shared cultural and economic ties, this democratic federation has created a unified market, military, and foreign policy. By pooling their industrial and colonial resources, the Benelux Federation has emerged as a significant European power capable of standing alongside larger nations while maintaining peace and prosperity for its citizens.",
        "requirements": {
            "player_nation": "belgium",
            "government": "Democratic",
            "stability": 75,
            "war_support": 40,
            "conquered_nations": ["netherlands", "luxembourg"],
            "completed_focus": "benelux_defense_agreement"
        },
        "type": "victory"
    },
    "belgian_colossus": {
        "name": "The Belgian Colossus",
        "description": "Belgium has risen from its position as a small neutral state to become a significant power in Europe. With expanded territories and close ties to Germany, Belgium now controls key industrial regions and strategic locations across Western Europe. The Belgian flag flies over parts of France and the Netherlands, creating a greater Belgian state that has finally achieved the power and recognition it has long desired.",
        "requirements": {
            "player_nation": "belgium",
            "government": "Fascist",
            "stability": 60,
            "war_support": 70,
            "partial_control": ["france", "netherlands"],
            "completed_focus": "greater_belgium"
        },
        "type": "victory"
    },
    "congo_exploitation": {
        "name": "The Belgian Colonial Exploitation",
        "description": "Belgium has poured all its resources into exploiting the vast mineral wealth of the Congo. While this has resulted in enormous profits flowing back to Belgium, it has come at a terrible human cost. The colonial regime has implemented brutal labor policies, causing widespread suffering among the Congolese population. Belgium's economy is now almost entirely dependent on colonial resources, transforming the nation into a colonial parasite rather than a modern European state.",
        "requirements": {
            "player_nation": "belgium",
            "stability": 30,
            "completed_focus": "integrate_congo_resources",
            "year_min": 1940
        },
        "type": "disaster"
    },
    "greater_dutch_kingdom": {
        "name": "The Greater Dutch Kingdom",
        "description": "The Netherlands has expanded its borders to include Flanders and parts of northern Germany, creating a unified Dutch-speaking nation. This greater Dutch state has become a significant power in northwestern Europe, with a strong economy based on trade, industry, and colonial resources. By leveraging its strategic position at the mouth of several key European rivers, the Greater Dutch Kingdom has secured its place as a respected middle power with significant influence in European affairs.",
        "requirements": {
            "player_nation": "netherlands",
            "stability": 60,
            "war_support": 70,
            "completed_focus": "greater_netherlands",
            "completed_focus2": "reclaim_frisian_islands"
        },
        "type": "victory"
    },
    "dutch_colonial_empire": {
        "name": "The Dutch Colonial Empire",
        "description": "The Netherlands has successfully secured and expanded its colonial holdings, creating one of the world's largest and most profitable colonial empires. The Dutch East Indies have been firmly integrated into the motherland's economy, providing vast resources and markets for Dutch goods. Through a combination of military strength and diplomatic skill, the Netherlands has managed to navigate the turbulent waters of global politics and preserve its global colonial network when other empires have faltered or collapsed.",
        "requirements": {
            "player_nation": "netherlands",
            "stability": 70,
            "completed_focus": "protect_east_indies",
            "completed_focus2": "colonial_nationalism",
            "year_min": 1942
        },
        "type": "victory"
    },
    "indonesian_independence": {
        "name": "Indonesian Independence",
        "description": "The Netherlands' attempt to grant limited autonomy to Indonesia has unexpectedly accelerated nationalist sentiment in the colony. As the Dutch found themselves increasingly entangled in European conflicts, Indonesian nationalist leaders seized the opportunity to declare independence. Unable to maintain control over its most valuable colony, the Netherlands has been forced to recognize Indonesian sovereignty, marking the beginning of the end for the once-mighty Dutch colonial empire and severely diminishing the Netherlands' status as a global power.",
        "requirements": {
            "player_nation": "netherlands",
            "stability": 40,
            "completed_focus": "indonesian_autonomy",
            "at_war": True,
            "year_min": 1942
        },
        "type": "disaster"
    },
    "roman_empire_restored": {
        "name": "The New Roman Empire",
        "description": "Under Mussolini's leadership, Italy has successfully reclaimed much of the territory of the ancient Roman Empire. Italian forces now control vast territories around the Mediterranean, from Spain to Greece, from North Africa to the Balkans. The Mediterranean has truly become Mare Nostrum—'Our Sea'—as Roman legions once again march through former provinces. Rome has been restored as the center of a great empire, with Mussolini as its Caesar, fulfilling the fascist dream of a reborn Roman glory and imperial destiny.",
        "requirements": {
            "player_nation": "italy",
            "stability": 60,
            "war_support": 80,
            "completed_focus": "roman_empire",
            "conquered_nations": ["greece", "yugoslavia"],
            "partial_control": ["france", "egypt"]
        },
        "type": "victory"
    },
    "italian_strategic_independence": {
        "name": "Italy's Independent Path",
        "description": "Avoiding the fatal German alliance, Italy has charted its own course through the turbulent waters of European politics. By maintaining a careful balance between the major powers and developing its own sphere of influence in the Mediterranean and Balkans, Italy has emerged as a respected middle power with significant diplomatic leverage. Under Mussolini's pragmatic leadership, Italy has secured its national interests without the devastating consequences of a world war, achieving fascist goals of national greatness through strategic independence rather than destructive conflict.",
        "requirements": {
            "player_nation": "italy",
            "stability": 70,
            "completed_focus": "maintain_independence",
            "year_min": 1942,
            "not_at_war": True
        },
        "type": "victory"
    },
    "italian_civil_war": {
        "name": "Italian Civil War",
        "description": "Mussolini's regime has collapsed under the weight of military failures and economic hardship. The country has descended into civil war as fascists, communists, monarchists, and democrats battle for control of Italy's future. Former allies have betrayed each other, regions have declared independence, and foreign powers intervene to support their preferred factions. The Italian people suffer tremendously as their nation tears itself apart, with cities reduced to rubble and the countryside ravaged by competing armies. The dream of Italian greatness has given way to a nightmare of fratricidal conflict.",
        "requirements": {
            "player_nation": "italy",
            "stability": 25,
            "war_support": 30,
            "at_war": True,
            "year_min": 1941
        },
        "type": "disaster"
    },
    "greater_east_asia_prosperity": {
        "name": "Greater East Asia Co-Prosperity Sphere",
        "description": "Japan has successfully liberated East and Southeast Asia from Western colonial rule, establishing a new order under Japanese leadership. The vast resources of the region now flow to support Japanese industry and military might, while former colonies enjoy unprecedented economic development under Japanese guidance. From Korea to Indonesia, from the Philippines to Indochina, the Rising Sun flag flies proudly over a new Asian empire that has forever broken the chains of Western domination and established a new order based on Asian values and Japanese leadership.",
        "requirements": {
            "player_nation": "japan",
            "stability": 70,
            "completed_focus": "greater_east_asia",
            "conquered_nations": ["indonesia", "malaysia"],
            "partial_control": ["china"],
            "year_min": 1942
        },
        "type": "victory"
    },
    "japanese_hegemony": {
        "name": "The Pacific Century",
        "description": "In a stunning reversal of power, Japan has defeated the United States and established complete hegemony over the Pacific Ocean. American territories like Hawaii, the Philippines, and Guam have fallen under Japanese control, while the US mainland itself has been forced to accept unfavorable peace terms. The humiliation of Pearl Harbor has been compounded by a series of decisive Japanese naval victories, forever shattering American power in Asia. With uncontested control of the Pacific and East Asia's resources, Japan has truly emerged as a global superpower, beginning what historians will call 'The Pacific Century.'",
        "requirements": {
            "player_nation": "japan",
            "stability": 65,
            "completed_focus": "strike_pearl_harbor",
            "war_support": 80,
            "conquered_nations": ["usa_pacific"],
            "year_min": 1943
        },
        "type": "victory"
    },
    "asian_peace_treaty": {
        "name": "The Tokyo Peace Treaty",
        "description": "Through skillful diplomacy rather than destructive war, Japan has secured its position as East Asia's dominant power. By negotiating with Western powers from a position of strength while avoiding direct conflict, Japan has gained recognition for its special interests in China and Southeast Asia without the catastrophic costs of a Pacific war. Trade agreements favorable to Japan have secured access to vital resources, while military limitations on Western presence in Asia have removed threats to Japanese security. This diplomatic triumph has established Japan as a respected great power while preserving peace and prosperity.",
        "requirements": {
            "player_nation": "japan",
            "stability": 80,
            "completed_focus": "pacific_neutrality",
            "not_at_war": True,
            "year_min": 1942
        },
        "type": "victory"
    },
    "japanese_defeat": {
        "name": "The Fire Bombing of Japan",
        "description": "Japan's imperial ambitions have ended in catastrophic defeat. American bombers reign supreme in the skies over Japan, reducing its cities to ash with relentless firebombing campaigns. The once-mighty Imperial Navy lies at the bottom of the Pacific, while American forces advance inexorably toward the Home Islands. Food shortages, economic collapse, and a desperate military situation have created a humanitarian crisis of unprecedented scale. The dream of a Greater East Asia Co-Prosperity Sphere has given way to the nightmare of defeat, occupation, and national humiliation as Japan faces the prospect of unconditional surrender.",
        "requirements": {
            "player_nation": "japan",
            "stability": 20,
            "war_support": 30,
            "at_war_with": ["usa", "uk"],
            "year_min": 1944
        },
        "type": "disaster"
    }
}

# Political Parties
POLITICAL_PARTIES = {
    "germany": {
        "NSDAP": {
            "name": "National Socialist German Workers' Party",
            "ideology": "Fascist",
            "leader": "Adolf Hitler",
            "support": 65,
            "description": "The ruling fascist party that promises to restore German greatness and expand living space for the German people."
        },
        "KPD": {
            "name": "Communist Party of Germany",
            "ideology": "Communist",
            "leader": "Ernst Thälmann",
            "support": 10,
            "description": "Revolutionary communist party seeking to establish a worker's state and align with the Soviet Union."
        },
        "SPD": {
            "name": "Social Democratic Party of Germany",
            "ideology": "Democratic",
            "leader": "Otto Wels",
            "support": 15,
            "description": "Democratic socialists advocating for workers' rights within a democratic framework."
        },
        "Zentrum": {
            "name": "Centre Party",
            "ideology": "Democratic",
            "leader": "Ludwig Kaas",
            "support": 5,
            "description": "Catholic political party advocating for Christian democracy and moderate policies."
        },
        "DNVP": {
            "name": "German National People's Party",
            "ideology": "Monarchist",
            "leader": "Alfred Hugenberg",
            "support": 5,
            "description": "Conservative nationalist party with monarchist tendencies and traditional values."
        }
    },
    "usa_parties_1": {
        "Democratic": {
            "name": "Democratic Party",
            "ideology": "Democratic",
            "leader": "Franklin D. Roosevelt",
            "support": 55,
            "description": "Progressive party championing social programs and international cooperation."
        },
        "Republican": {
            "name": "Republican Party",
            "ideology": "Democratic",
            "leader": "Alf Landon",
            "support": 40,
            "description": "Conservative party advocating for limited government and business interests."
        },
        "CPUSA": {
            "name": "Communist Party USA",
            "ideology": "Communist",
            "leader": "Earl Browder",
            "support": 2,
            "description": "Far-left party seeking to establish a socialist state in America."
        },
        "America First": {
            "name": "America First Committee",
            "ideology": "Fascist",
            "leader": "Charles Lindbergh",
            "support": 3,
            "description": "Nationalist isolationist movement with fascist sympathies."
        },
        "Socialists": {
            "name": "Socialist Party of America",
            "ideology": "Communist",
            "leader": "Norman Thomas",
            "support": 5,
            "description": "Left-wing party advocating for radical economic reforms and workers' rights."
        }
    },
    "uk": {
        "Conservative": {
            "name": "Conservative Party",
            "ideology": "Democratic",
            "leader": "Stanley Baldwin",
            "support": 50,
            "description": "Traditional conservative party supporting the British Empire and stability."
        },
        "Labour": {
            "name": "Labour Party",
            "ideology": "Democratic",
            "leader": "Clement Attlee",
            "support": 40,
            "description": "Democratic socialist party representing working class interests."
        },
        "CPGB": {
            "name": "Communist Party of Great Britain",
            "ideology": "Communist",
            "leader": "Harry Pollitt",
            "support": 5,
            "description": "Revolutionary communist party supported by Moscow."
        },
        "BUF": {
            "name": "British Union of Fascists",
            "ideology": "Fascist",
            "leader": "Oswald Mosley",
            "support": 5,
            "description": "Ultranationalist party inspired by Italian Fascism."
        }
    },
    "france": {
        "SFIO": {
            "name": "French Section of the Workers' International",
            "ideology": "Democratic",
            "leader": "Léon Blum",
            "support": 35,
            "description": "Democratic socialist party leading the Popular Front coalition."
        },
        "Radical": {
            "name": "Radical Party",
            "ideology": "Democratic",
            "leader": "Édouard Daladier",
            "support": 30,
            "description": "Center-left liberal party supporting the republic."
        },
        "PCF": {
            "name": "French Communist Party",
            "ideology": "Communist",
            "leader": "Maurice Thorez",
            "support": 15,
            "description": "Revolutionary Marxist party aligned with the Soviet Union."
        },
        "AF": {
            "name": "Action Française",
            "ideology": "Fascist",
            "leader": "Charles Maurras",
            "support": 10,
            "description": "Far-right monarchist and nationalist movement."
        },
        "PSF": {
            "name": "French Social Party",
            "ideology": "Fascist",
            "leader": "François de La Rocque",
            "support": 10,
            "description": "Nationalist anti-communist party with fascist tendencies."
        },
        "Popular_Front": {
            "name": "Popular Front",
            "ideology": "Democratic",
            "leader": "Léon Blum",
            "support": 60,
            "description": "Left-wing coalition of socialists, communists, and liberals."
        },
        "Conservatives": {
            "name": "National Bloc",
            "ideology": "Democratic",
            "leader": "Pierre-Étienne Flandin",
            "support": 30,
            "description": "Conservative faction opposing the Popular Front's reforms."
        },
    },
    "ussr": {
        "CPSU": {
            "name": "Communist Party of the Soviet Union",
            "ideology": "Communist",
            "leader": "Joseph Stalin",
            "support": 99,
            "description": "The only legal party in the Soviet Union, enforcing Stalinist leadership."
        },
        "Left Opposition": {
            "name": "Left Opposition",
            "ideology": "Communist",
            "leader": "Leon Trotsky (in exile)",
            "support": 1,
            "description": "Suppressed faction advocating for international permanent revolution."
        }
    },
    "italy": {
        "PNF": {
            "name": "National Fascist Party",
            "ideology": "Fascist",
            "leader": "Benito Mussolini",
            "support": 85,
            "description": "Ruling fascist party that has consolidated totalitarian control."
        },
        "PCI": {
            "name": "Italian Communist Party",
            "ideology": "Communist",
            "leader": "Palmiro Togliatti",
            "support": 10,
            "description": "Underground communist resistance to fascism."
        },
        "Monarchists": {
            "name": "Monarchist Faction",
            "ideology": "Monarchist",
            "leader": "Victor Emmanuel III",
            "support": 5,
            "description": "Supporters of the King who maintain a degree of independence from fascism."
        }
    },
    "japan": {
        "Imperial": {
            "name": "Imperial Rule Assistance Association",
            "ideology": "Fascist",
            "leader": "Fumimaro Konoe",
            "support": 70,
            "description": "Nationalist party supporting Emperor Hirohito and Japanese expansionism."
        },
        "Moderates": {
            "name": "Constitutional Moderates",
            "ideology": "Democratic",
            "leader": "Kijūrō Shidehara",
            "support": 20,
            "description": "Conservative faction advocating for measured diplomacy and constitutional monarchy."
        },
        "Militarists": {
            "name": "Imperial Army Faction",
            "ideology": "Ultranationalist",
            "leader": "Hideki Tojo",
            "support": 10,
            "description": "Radical militarists pushing for aggressive expansion in Asia."
        }
    },
    "spain": {
        "Republicans": {
            "name": "Popular Front",
            "ideology": "Democratic",
            "leader": "Manuel Azaña",
            "support": 50,
            "description": "Left-wing coalition of republicans, socialists, and communists."
        },
        "Nationalists": {
            "name": "Nationalist Front",
            "ideology": "Fascist",
            "leader": "Francisco Franco",
            "support": 45,
            "description": "Right-wing coalition of monarchists, falangists, and military leaders."
        },
        "Anarchists": {
            "name": "CNT-FAI",
            "ideology": "Anarchist",
            "leader": "Buenaventura Durruti",
            "support": 5,
            "description": "Anarcho-syndicalist movement advocating for workers' control and revolution."
        }
    },
    "china": {
        "Kuomintang": {
            "name": "Chinese Nationalist Party",
            "ideology": "Democratic",
            "leader": "Chiang Kai-shek",
            "support": 60,
            "description": "Nationalist government struggling against Japanese invasion and communist insurgency."
        },
        "CCP": {
            "name": "Chinese Communist Party",
            "ideology": "Communist",
            "leader": "Mao Zedong",
            "support": 20,
            "description": "Revolutionary communist movement building support in rural areas."
        },
        "Warlords": {
            "name": "Regional Warlords",
            "ideology": "Non-Aligned",
            "leader": "Various",
            "support": 20,
            "description": "Independent military leaders controlling different regions of China."
        }
    },
    "turkey": {
        "CHP": {
            "name": "Republican People's Party",
            "ideology": "Democratic",
            "leader": "Mustafa Kemal Atatürk",
            "support": 90,
            "description": "Kemalist party leading Turkey's modernization and secularization efforts."
        },
        "Conservatives": {
            "name": "Islamic Conservatives",
            "ideology": "Non-Aligned",
            "leader": "Various Clerics",
            "support": 5,
            "description": "Religious leaders opposed to the secular reforms of Atatürk."
        },
        "Militarists": {
            "name": "Military Nationalists",
            "ideology": "Fascist",
            "leader": "Various Officers",
            "support": 5,
            "description": "Officers advocating for stronger Turkish expansionism and military rule."
        }
    },
    "sweden": {
        "SAP": {
            "name": "Social Democratic Workers' Party",
            "ideology": "Democratic",
            "leader": "Per Albin Hansson",
            "support": 45,
            "description": "Social democratic party building the 'Folkhemmet' (People's Home) welfare system."
        },
        "Farmers": {
            "name": "Farmer's League",
            "ideology": "Democratic",
            "leader": "Axel Pehrsson-Bramstorp",
            "support": 30,
            "description": "Centrist agrarian party representing rural interests."
        },
        "Conservatives": {
            "name": "National Organization",
            "ideology": "Democratic",
            "leader": "Gösta Bagge",
            "support": 25,
            "description": "Conservative party supporting traditional values and constitutional monarchy."
        }
    },
    "greece": {
        "Monarchists": {
            "name": "People's Party",
            "ideology": "Monarchist",
            "leader": "Konstantinos Tsaldaris",
            "support": 45,
            "description": "Conservative monarchist party supporting King George II."
        },
        "Liberals": {
            "name": "Liberal Party",
            "ideology": "Democratic",
            "leader": "Themistoklis Sophoulis",
            "support": 40,
            "description": "Center-left republican opposition."
        },
        "KKE": {
            "name": "Communist Party of Greece",
            "ideology": "Communist",
            "leader": "Nikos Zachariadis",
            "support": 15,
            "description": "Revolutionary communist party with growing popular support."
        }
    },
    "romania": {
        "Liberals": {
            "name": "National Liberal Party",
            "ideology": "Democratic",
            "leader": "Ion Duca",
            "support": 40,
            "description": "Traditional liberal party representing the business interests."
        },
        "Peasants": {
            "name": "National Peasants' Party",
            "ideology": "Democratic",
            "leader": "Iuliu Maniu",
            "support": 30,
            "description": "Centrist agrarian party representing rural Romania."
        },
        "Iron_Guard": {
            "name": "Iron Guard",
            "ideology": "Fascist",
            "leader": "Corneliu Zelea Codreanu",
            "support": 30,
            "description": "Ultranationalist fascist party with strong anti-Semitic ideology."
        }
    }
}

# Game state
game_state = {
    "year": 1936,
    "month": 1,
    "player_nation": "",
    "nations": {},
    "focus_progress": None,
    "events": [],
    "wars": [],
    "research": {},
    "message_log": [],
    "difficulty": "normal",
    "game_speed": 1,
    "paused": False,
    "historical_ai": True,
    "last_save": None,
    "internal_conflicts": 0,
    "achieved_ending": None,
    "political_influence": 0
}

# Nation data
NATIONS = {
    "germany": {
        "name": "Deutschland",
        "color": Fore.RED,
        "leader": "Adolf Hitler",
        "government": "Fascist",
        "stability": 70,
        "war_support": 60,
        "industry": {
            "civilian_factories": 16,
            "military_factories": 6,
            "dockyards": 2,
            "infrastructure": 5,
        },
        "resources": {
            "steel": 20,
            "oil": 2,
            "aluminum": 8,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 24,
            "manpower": 600000,
            "equipment": {
                "infantry_equipment": 80000,
                "artillery": 2400,
                "tanks": 400,
            },
        },
        "navy": {
            "ships": {
                "battleships": 2,
                "cruisers": 6,
                "destroyers": 12,
                "submarines": 10,
            },
        },
        "air_force": {
            "fighters": 180,
            "bombers": 120,
        },
        "neighbors": ["france", "poland", "czechoslovakia", "austria", "switzerland", "denmark", "netherlands", "belgium", "lithuania"],
        "focus_tree": "german_focus_tree",
        "playable": True,
        "description": "The German Reich stands at a crossroads. With Adolf Hitler's leadership, you can restore Germany to its former glory through rearmament and expansion, or choose an alternate path for the nation. Germany offers the most developed gameplay with multiple paths and special events.",
    },
    "france": {
        "name": "France",
        "color": Fore.BLUE,
        "leader": "Albert Lebrun",
        "government": "Democratic",
        "stability": 65,
        "war_support": 25,
        "industry": {
            "civilian_factories": 14,
            "military_factories": 6,
            "dockyards": 4,
            "infrastructure": 6,
        },
        "resources": {
            "steel": 30,
            "oil": 0,
            "aluminum": 15,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 28,
            "manpower": 500000,
            "equipment": {
                "infantry_equipment": 75000,
                "artillery": 3000,
                "tanks": 600,
            },
        },
        "navy": {
            "ships": {
                "battleships": 5,
                "cruisers": 12,
                "destroyers": 30,
                "submarines": 15,
            },
        },
        "air_force": {
            "fighters": 160,
            "bombers": 100,
        },
        "neighbors": ["germany", "italy", "switzerland", "belgium", "spain"],
        "focus_tree": "french_focus_tree",
        "playable": True,
        "description": "France, a declining great power, faces the challenge of confronting a resurgent Germany. Can you strengthen France's economy and military to stand against fascism, or will you chart a different course? Choose between upholding democracy, embracing communism, or turning to fascism yourself.",
    },
    "uk": {
        "name": "United Kingdom",
        "color": Fore.CYAN,
        "leader": "Stanley Baldwin",
        "government": "Democratic",
        "stability": 80,
        "war_support": 30,
        "industry": {
            "civilian_factories": 18,
            "military_factories": 8,
            "dockyards": 10,
            "infrastructure": 7,
        },
        "resources": {
            "steel": 25,
            "oil": 8,
            "aluminum": 10,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 18,
            "manpower": 400000,
            "equipment": {
                "infantry_equipment": 60000,
                "artillery": 2000,
                "tanks": 350,
            },
        },
        "navy": {
            "ships": {
                "battleships": 12,
                "cruisers": 30,
                "destroyers": 80,
                "submarines": 25,
            },
        },
        "air_force": {
            "fighters": 200,
            "bombers": 180,
        },
        "neighbors": ["ireland", "france"],
        "focus_tree": "british_focus_tree",
        "playable": True,
        "description": "The British Empire, though still vast, faces challenges from all sides. Economic pressures, colonial unrest, and the rise of fascism threaten British dominance. Will you maintain democracy and prepare for the coming storm, preserve the Empire at all costs, or perhaps pursue a more radical agenda?",
    },
    "italy": {
        "name": "Italy",
        "color": Fore.GREEN,
        "leader": "Benito Mussolini",
        "government": "Fascist",
        "stability": 65,
        "war_support": 55,
        "industry": {
            "civilian_factories": 10,
            "military_factories": 4,
            "dockyards": 5,
            "infrastructure": 4,
        },
        "resources": {
            "steel": 10,
            "oil": 0,
            "aluminum": 5,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 16,
            "manpower": 300000,
            "equipment": {
                "infantry_equipment": 50000,
                "artillery": 1800,
                "tanks": 200,
            },
        },
        "navy": {
            "ships": {
                "battleships": 4,
                "cruisers": 12,
                "destroyers": 30,
                "submarines": 20,
            },
        },
        "air_force": {
            "fighters": 120,
            "bombers": 80,
        },
        "neighbors": ["france", "switzerland", "austria", "yugoslavia", "albania", "greece"],
        "focus_tree": "italian_focus_tree",
        "playable": True,
        "description": "Mussolini's Italy seeks to reclaim the glory of Ancient Rome and establish a new Mediterranean empire. Despite a faltering economy and limited industrial capacity, Italy's ambitions are grand. Will you create a new Roman Empire, reform the nation's economy, or perhaps return the monarchy to true power?",
    },
    "ussr": {
        "name": "Soviet Union",
        "color": Fore.RED,
        "leader": "Joseph Stalin",
        "government": "Communist",
        "stability": 55,
        "war_support": 40,
        "industry": {
            "civilian_factories": 22,
            "military_factories": 12,
            "dockyards": 3,
            "infrastructure": 3,
        },
        "resources": {
            "steel": 100,
            "oil": 80,
            "aluminum": 30,
            "rubber": 0,
            "tungsten": 10,
            "chromium": 30,
        },
        "army": {
            "divisions": 40,
            "manpower": 1200000,
            "equipment": {
                "infantry_equipment": 120000,
                "artillery": 5000,
                "tanks": 1500,
            },
        },
        "navy": {
            "ships": {
                "battleships": 1,
                "cruisers": 7,
                "destroyers": 25,
                "submarines": 15,
            },
        },
        "air_force": {
            "fighters": 300,
            "bombers": 200,
        },
        "neighbors": ["finland", "estonia", "latvia", "lithuania", "poland", "romania", "persia", "afghanistan", "china", "mongolia", "japan"],
        "focus_tree": "soviet_focus_tree",
        "playable": True,
        "description": "The Soviet Union under Stalin's iron grip is transforming rapidly from an agricultural society into an industrial powerhouse. Internal purges have weakened the military but solidified political control. Will you maintain the Stalinist course, pursue a more moderate socialism, or even restore the Tsarist monarchy?",
    },
    "usa": {
        "name": "United States",
        "color": Fore.BLUE,
        "leader": "Franklin D. Roosevelt",
        "government": "Democratic",
        "stability": 85,
        "war_support": 10,
        "industry": {
            "civilian_factories": 30,
            "military_factories": 6,
            "dockyards": 8,
            "infrastructure": 7,
        },
        "resources": {
            "steel": 150,
            "oil": 200,
            "aluminum": 60,
            "rubber": 0,
            "tungsten": 20,
            "chromium": 10,
        },
        "army": {
            "divisions": 12,
            "manpower": 200000,
            "equipment": {
                "infantry_equipment": 40000,
                "artillery": 1500,
                "tanks": 300,
            },
        },
        "navy": {
            "ships": {
                "battleships": 15,
                "cruisers": 30,
                "destroyers": 90,
                "submarines": 30,
            },
        },
        "air_force": {
            "fighters": 150,
            "bombers": 100,
        },
        "neighbors": ["canada", "mexico"],
        "focus_tree": "usa_focus_tree",
        "playable": True,
        "description": "The United States remains mired in the Great Depression, with strong isolationist sentiment keeping it out of European affairs. However, its industrial potential is unmatched. Will you lead America out of isolationism to confront the Axis threat, focus on economic recovery, or perhaps take a more radical political turn?",
    },
    "japan": {
        "name": "Japan",
        "color": Fore.LIGHTRED_EX,
        "leader": "Hirohito",
        "government": "Fascist",
        "stability": 70,
        "war_support": 60,
        "industry": {
            "civilian_factories": 14,
            "military_factories": 8,
            "dockyards": 8,
            "infrastructure": 5,
        },
        "resources": {
            "steel": 20,
            "oil": 0,
            "aluminum": 10,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 24,
            "manpower": 600000,
            "equipment": {
                "infantry_equipment": 70000,
                "artillery": 2800,
                "tanks": 300,
            },
        },
        "navy": {
            "ships": {
                "battleships": 10,
                "cruisers": 20,
                "destroyers": 60,
                "submarines": 25,
            },
        },
        "air_force": {
            "fighters": 180,
            "bombers": 140,
        },
        "neighbors": ["china", "ussr", "korea"],
        "focus_tree": "japanese_focus_tree",
    },
    "poland": {
        "name": "Poland",
        "color": Fore.WHITE,
        "leader": "Ignacy Mościcki",
        "government": "Neutral",
        "stability": 45,
        "war_support": 40,
        "industry": {
            "civilian_factories": 5,
            "military_factories": 2,
            "dockyards": 1,
            "infrastructure": 3,
        },
        "resources": {
            "steel": 5,
            "oil": 0,
            "aluminum": 0,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 12,
            "manpower": 250000,
            "equipment": {
                "infantry_equipment": 30000,
                "artillery": 800,
                "tanks": 100,
            },
        },
        "air_force": {
            "fighters": 30,
            "bombers": 10,
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 0,
                "destroyers": 2,
                "submarines": 2,
            },
        },
        "neighbors": ["germany", "czechoslovakia", "lithuania", "latvia", "ussr"],
        "focus_tree": "polish_focus_tree",
        "playable": True,
        "description": "Caught between two aggressive powers - Nazi Germany and the Soviet Union - Poland faces an existential crisis. With limited industrial capacity but a proud military tradition, can you navigate the dangerous waters of European politics and preserve Polish independence?",
    },
    "yugoslavia": {
        "name": "Yugoslavia",
        "color": Fore.BLUE,
        "leader": "Prince Paul",
        "government": "Neutral",
        "stability": 40,
        "war_support": 30,
        "industry": {
            "civilian_factories": 4,
            "military_factories": 2,
            "dockyards": 1,
            "infrastructure": 2,
        },
        "resources": {
            "steel": 8,
            "oil": 2,
            "aluminum": 6,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 4,
        },
        "army": {
            "divisions": 10,
            "manpower": 200000,
            "equipment": {
                "infantry_equipment": 25000,
                "artillery": 600,
                "tanks": 50,
            },
        },
        "air_force": {
            "fighters": 20,
            "bombers": 5,
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 0,
                "destroyers": 1,
                "submarines": 1,
            },
        },
        "neighbors": ["italy", "germany", "hungary", "romania", "bulgaria", "greece", "albania"],
        "focus_tree": "yugoslavian_focus_tree",
        "playable": True,
        "description": "A young multiethnic kingdom with deep internal divisions, Yugoslavia is surrounded by stronger neighbors with territorial ambitions. Can you unite the diverse peoples of the Balkans into a coherent nation, or will ethnic tensions tear the country apart?",
    },
    "spain": {
        "name": "Spain",
        "color": Fore.YELLOW,
        "leader": "Francisco Franco",
        "government": "Fascist",
        "stability": 40,
        "war_support": 30,
        "industry": {
            "civilian_factories": 6,
            "military_factories": 2,
            "dockyards": 3,
            "infrastructure": 3,
        },
        "resources": {
            "steel": 5,
            "oil": 0,
            "aluminum": 0,
            "rubber": 0,
            "tungsten": 10,
            "chromium": 0,
        },
        "army": {
            "divisions": 14,
            "manpower": 250000,
            "equipment": {
                "infantry_equipment": 30000,
                "artillery": 500,
                "tanks": 50,
            },
        },
        "navy": {
            "ships": {
                "battleships": 1,
                "cruisers": 4,
                "destroyers": 8,
                "submarines": 2,
            },
        },
        "air_force": {
            "fighters": 50,
            "bombers": 20,
        },
        "neighbors": ["france", "portugal"],
        "focus_tree": "spanish_focus_tree",
        "playable": True,
        "description": "Spain is recovering from its brutal Civil War, where the Nationalist forces led by Francisco Franco defeated the Republican government. The country is exhausted, divided, and devastated by years of fighting. Will you maintain neutrality, align with the Axis powers whose support helped Franco win, or take a different path?",
    },
    "turkey": {
        "name": "Turkey",
        "color": Fore.RED,
        "leader": "İsmet İnönü",
        "government": "Democratic",
        "stability": 70,
        "war_support": 20,
        "industry": {
            "civilian_factories": 5,
            "military_factories": 2,
            "dockyards": 1,
            "infrastructure": 3,
        },
        "resources": {
            "steel": 5,
            "oil": 0,
            "aluminum": 0,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 20,
        },
        "army": {
            "divisions": 12,
            "manpower": 200000,
            "equipment": {
                "infantry_equipment": 25000,
                "artillery": 400,
                "tanks": 20,
            },
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 2,
                "destroyers": 4,
                "submarines": 1,
            },
        },
        "air_force": {
            "fighters": 30,
            "bombers": 10,
        },
        "neighbors": ["greece", "bulgaria", "ussr", "syria", "iraq", "iran"],
        "focus_tree": "turkish_focus_tree",
        "playable": True,
        "description": "Rising from the ashes of the Ottoman Empire, Turkey under President İnönü is working to maintain Atatürk's legacy of modernization and secularism. Positioned at the crossroads of Europe and Asia, Turkey's strategic location makes it crucial to both Axis and Allied interests. Will you continue the path of neutrality, or use the war to reclaim former Ottoman territories?",
    },
    "sweden": {
        "name": "Sweden",
        "color": Fore.BLUE,
        "leader": "Per Albin Hansson",
        "government": "Democratic",
        "stability": 90,
        "war_support": 10,
        "industry": {
            "civilian_factories": 8,
            "military_factories": 3,
            "dockyards": 2,
            "infrastructure": 6,
        },
        "resources": {
            "steel": 40,
            "oil": 0,
            "aluminum": 0,
            "rubber": 0,
            "tungsten": 10,
            "chromium": 0,
        },
        "army": {
            "divisions": 8,
            "manpower": 150000,
            "equipment": {
                "infantry_equipment": 20000,
                "artillery": 300,
                "tanks": 40,
            },
        },
        "navy": {
            "ships": {
                "battleships": 2,
                "cruisers": 3,
                "destroyers": 8,
                "submarines": 10,
            },
        },
        "air_force": {
            "fighters": 60,
            "bombers": 20,
        },
        "neighbors": ["norway", "finland"],
        "focus_tree": "swedish_focus_tree",
        "playable": True,
        "description": "Sweden enjoys peace and prosperity while much of Europe spirals into conflict. Its neutrality policy has kept it out of wars for over a century, but with Nazi Germany dominating neighboring Norway and Denmark, and the Soviet Union attacking Finland, maintaining this neutrality will be challenging. Sweden's vast iron ore resources are coveted by all major powers. Can you guide Sweden safely through the storm?",
    },
    "thailand": {
        "name": "Thailand",
        "color": Fore.LIGHTRED_EX,
        "leader": "Plaek Phibunsongkhram",
        "government": "Military",
        "stability": 60,
        "war_support": 25,
        "industry": {
            "civilian_factories": 3,
            "military_factories": 2,
            "dockyards": 1,
            "infrastructure": 2,
        },
        "resources": {
            "steel": 5,
            "oil": 0,
            "aluminum": 0,
            "rubber": 20,
            "tungsten": 5,
            "chromium": 0,
        },
        "army": {
            "divisions": 8,
            "manpower": 120000,
            "equipment": {
                "infantry_equipment": 18000,
                "artillery": 200,
                "tanks": 10,
            },
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 2,
                "destroyers": 4,
                "submarines": 0,
            },
        },
        "air_force": {
            "fighters": 30,
            "bombers": 15,
        },
        "neighbors": ["burma", "french_indochina", "malaya"],
        "focus_tree": "thailand_focus_tree",
        "playable": True,
        "description": "Thailand (formerly Siam) is caught between powerful colonial empires in Southeast Asia. Japan's expansion threatens the regional balance of power, while Thailand's own ambitions to reclaim lost territories could lead to confrontation with Britain and France. Will you align with Japan's Co-Prosperity Sphere, remain neutral, or support the Allied powers?",
    },
    "philippines": {
        "name": "Philippines",
        "color": Fore.BLUE,
        "leader": "Manuel L. Quezon",
        "government": "Democratic",
        "stability": 65,
        "war_support": 15,
        "industry": {
            "civilian_factories": 2,
            "military_factories": 1,
            "dockyards": 1,
            "infrastructure": 2,
        },
        "resources": {
            "steel": 2,
            "oil": 0,
            "aluminum": 0,
            "rubber": 5,
            "tungsten": 0,
            "chromium": 10,
        },
        "army": {
            "divisions": 5,
            "manpower": 80000,
            "equipment": {
                "infantry_equipment": 12000,
                "artillery": 100,
                "tanks": 0,
            },
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 0,
                "destroyers": 2,
                "submarines": 0,
            },
        },
        "air_force": {
            "fighters": 20,
            "bombers": 10,
        },
        "neighbors": [],
        "focus_tree": "philippines_focus_tree",
        "playable": True,
        "description": "A Commonwealth of the United States on the path to independence, the Philippines faces the looming threat of Japanese expansion. With limited military capabilities and U.S. protection, your decisions will determine whether the islands can defend against invasion or must endure occupation. Will you strengthen ties with America, push for immediate independence, or navigate a different path?",
    },
    "netherlands_east_indies": {
        "name": "Dutch East Indies",
        "color": Fore.LIGHTBLUE_EX,
        "leader": "Governor-General A.W.L. Tjarda van Starkenborgh Stachouwer",
        "government": "Colonial",
        "stability": 55,
        "war_support": 20,
        "industry": {
            "civilian_factories": 3,
            "military_factories": 1,
            "dockyards": 1,
            "infrastructure": 2,
        },
        "resources": {
            "steel": 5,
            "oil": 30,
            "aluminum": 5,
            "rubber": 40,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 4,
            "manpower": 60000,
            "equipment": {
                "infantry_equipment": 10000,
                "artillery": 80,
                "tanks": 0,
            },
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 3,
                "destroyers": 7,
                "submarines": 13,
            },
        },
        "air_force": {
            "fighters": 25,
            "bombers": 15,
        },
        "neighbors": ["malaya", "thailand", "philippines"],
        "focus_tree": "east_indies_focus_tree",
        "playable": True,
        "description": "Rich in oil and rubber, the Dutch East Indies (modern Indonesia) is a prime target for resource-hungry Japan. With the Netherlands occupied by Germany, the colony faces potential isolation from Allied support. Will you strengthen defenses to resist invasion, negotiate with Japan to preserve independence, or rise up against colonial rule altogether?",
    },
    "australia": {
        "name": "Australia",
        "color": Fore.LIGHTGREEN_EX,
        "leader": "John Curtin",
        "government": "Democratic",
        "stability": 80,
        "war_support": 40,
        "industry": {
            "civilian_factories": 6,
            "military_factories": 3,
            "dockyards": 2,
            "infrastructure": 4,
        },
        "resources": {
            "steel": 15,
            "oil": 0,
            "aluminum": 5,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 10,
        },
        "army": {
            "divisions": 6,
            "manpower": 150000,
            "equipment": {
                "infantry_equipment": 20000,
                "artillery": 400,
                "tanks": 100,
            },
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 6,
                "destroyers": 10,
                "submarines": 2,
            },
        },
        "air_force": {
            "fighters": 60,
            "bombers": 40,
        },
        "neighbors": [],
        "focus_tree": "australia_focus_tree",
        "playable": True,
        "description": "A loyal dominion of the British Empire, Australia faces hard choices as Japanese expansion threatens the Pacific. With most of its expeditionary forces fighting in Europe and North Africa, Australia's homeland defenses are stretched thin. Will you continue supporting Britain's war effort, pivot to defend the homeland, or seek closer ties with the United States?",
    },
    "nationalist_china": {
        "name": "Nationalist China",
        "color": Fore.BLUE,
        "leader": "Chiang Kai-shek",
        "government": "Military",
        "stability": 40,
        "war_support": 70,
        "industry": {
            "civilian_factories": 5,
            "military_factories": 3,
            "dockyards": 1,
            "infrastructure": 2,
        },
        "resources": {
            "steel": 15,
            "oil": 2,
            "aluminum": 5,
            "rubber": 2,
            "tungsten": 20,
            "chromium": 5,
        },
        "army": {
            "divisions": 30,
            "manpower": 800000,
            "equipment": {
                "infantry_equipment": 80000,
                "artillery": 600,
                "tanks": 80,
            },
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 2,
                "destroyers": 8,
                "submarines": 0,
            },
        },
        "air_force": {
            "fighters": 40,
            "bombers": 20,
        },
        "neighbors": ["japan", "communist_china", "tibet", "mongolia"],
        "focus_tree": "nationalist_china_focus_tree",
        "playable": True,
        "description": "The Republic of China under Chiang Kai-shek faces a desperate struggle for survival against Japanese invasion and Communist insurgency. With limited industrial capacity but vast manpower, China must modernize while fighting off foreign aggression and internal divisions. Can you unite the nation, defeat the Japanese, and build a new China?",
    },
    "communist_china": {
        "name": "Communist China",
        "color": Fore.RED,
        "leader": "Mao Zedong",
        "government": "Communist",
        "stability": 60,
        "war_support": 60,
        "industry": {
            "civilian_factories": 1,
            "military_factories": 1,
            "dockyards": 0,
            "infrastructure": 1,
        },
        "resources": {
            "steel": 5,
            "oil": 0,
            "aluminum": 0,
            "rubber": 0,
            "tungsten": 5,
            "chromium": 0,
        },
        "army": {
            "divisions": 8,
            "manpower": 200000,
            "equipment": {
                "infantry_equipment": 20000,
                "artillery": 100,
                "tanks": 0,
            },
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 0,
                "destroyers": 0,
                "submarines": 0,
            },
        },
        "air_force": {
            "fighters": 5,
            "bombers": 2,
        },
        "neighbors": ["nationalist_china", "mongolia"],
        "focus_tree": "communist_china_focus_tree",
        "playable": True,
        "description": "The Chinese Communist Party controls a small but growing base in rural China, using guerrilla tactics against both Japanese invaders and Nationalist forces. With limited resources but growing popular support, the Communists must expand their influence and build toward revolution. Will you cooperate with the Nationalists against Japan, or focus on the coming civil war?",
    },
    "belgium": {
        "name": "Belgium",
        "color": Fore.YELLOW,
        "leader": "Leopold III",
        "government": "Democratic",
        "stability": 65,
        "war_support": 15,
        "industry": {
            "civilian_factories": 6,
            "military_factories": 2,
            "dockyards": 1,
            "infrastructure": 5,
        },
        "resources": {
            "steel": 12,
            "oil": 0,
            "aluminum": 0,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 8,
            "manpower": 150000,
            "equipment": {
                "infantry_equipment": 20000,
                "artillery": 400,
                "tanks": 30,
            },
        },
        "air_force": {
            "fighters": 15,
            "bombers": 5,
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 0,
                "destroyers": 1,
                "submarines": 0,
            },
        },
        "neighbors": ["france", "germany", "netherlands", "luxembourg"],
        "focus_tree": "belgian_focus_tree",
        "playable": True,
        "description": "A small but industrialized nation caught between the great powers of Europe, Belgium relies on neutrality and international guarantees for its security. Can you maintain independence through diplomacy, or must you prepare for the worst?",
    },
    "netherlands": {
        "name": "Netherlands",
        "color": Fore.LIGHTBLUE_EX,
        "leader": "Hendrikus Colijn",
        "government": "Democratic",
        "stability": 70,
        "war_support": 10,
        "industry": {
            "civilian_factories": 7,
            "military_factories": 2,
            "dockyards": 3,
            "infrastructure": 6,
        },
        "resources": {
            "steel": 3,
            "oil": 0,
            "aluminum": 0,
            "rubber": 25,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 7,
            "manpower": 120000,
            "equipment": {
                "infantry_equipment": 18000,
                "artillery": 300,
                "tanks": 20,
            },
        },
        "air_force": {
            "fighters": 20,
            "bombers": 8,
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 2,
                "destroyers": 8,
                "submarines": 10,
            },
        },
        "neighbors": ["germany", "belgium"],
        "focus_tree": "dutch_focus_tree",
        "playable": True,
        "description": "Though small in Europe, the Netherlands possesses a vast colonial empire in the East Indies. Can you defend both homeland and colonies from aggression while balancing the economic needs of a trading nation?",
    },
    "denmark": {
        "name": "Denmark",
        "color": Fore.RED,
        "leader": "Thorvald Stauning",
        "government": "Democratic",
        "stability": 80,
        "war_support": 10,
        "industry": {
            "civilian_factories": 4,
            "military_factories": 1,
            "dockyards": 2,
            "infrastructure": 6,
        },
        "resources": {
            "steel": 2,
            "oil": 0,
            "aluminum": 0,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 3,
            "manpower": 50000,
            "equipment": {
                "infantry_equipment": 10000,
                "artillery": 150,
                "tanks": 10,
            },
        },
        "air_force": {
            "fighters": 8,
            "bombers": 0,
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 0,
                "destroyers": 3,
                "submarines": 4,
            },
        },
        "neighbors": ["germany", "sweden"],
        "focus_tree": "danish_focus_tree",
        "playable": True,
        "description": "A small Scandinavian democracy with a direct border with Nazi Germany, Denmark has embraced neutrality in hopes of avoiding conflict. Can you maintain independence through diplomacy or find allies to protect you?",
    },
    "norway": {
        "name": "Norway",
        "color": Fore.RED,
        "leader": "Johan Nygaardsvold",
        "government": "Democratic",
        "stability": 75,
        "war_support": 10,
        "industry": {
            "civilian_factories": 3,
            "military_factories": 1,
            "dockyards": 2,
            "infrastructure": 4,
        },
        "resources": {
            "steel": 5,
            "oil": 0,
            "aluminum": 8,
            "rubber": 0,
            "tungsten": 6,
            "chromium": 0,
        },
        "army": {
            "divisions": 4,
            "manpower": 60000,
            "equipment": {
                "infantry_equipment": 12000,
                "artillery": 200,
                "tanks": 5,
            },
        },
        "air_force": {
            "fighters": 10,
            "bombers": 0,
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 0,
                "destroyers": 4,
                "submarines": 6,
            },
        },
        "neighbors": ["sweden", "finland"],
        "focus_tree": "norwegian_focus_tree",
        "playable": True,
        "description": "Norway's strategic position controlling access to the Baltic Sea and its valuable resources make it a tempting target for major powers. Can you maintain neutrality, or will you be forced to choose sides in the coming conflict?",
    },
    "austria": {
        "name": "Austria",
        "color": Fore.WHITE,
        "leader": "Kurt Schuschnigg",
        "government": "Neutral",
        "stability": 30,
        "war_support": 20,
        "industry": {
            "civilian_factories": 4,
            "military_factories": 1,
            "dockyards": 0,
            "infrastructure": 4,
        },
        "resources": {
            "steel": 6,
            "oil": 1,
            "aluminum": 2,
            "rubber": 0,
            "tungsten": 0,
            "chromium": 0,
        },
        "army": {
            "divisions": 5,
            "manpower": 80000,
            "equipment": {
                "infantry_equipment": 15000,
                "artillery": 250,
                "tanks": 0,
            },
        },
        "air_force": {
            "fighters": 5,
            "bombers": 0,
        },
        "navy": {
            "ships": {
                "battleships": 0,
                "cruisers": 0,
                "destroyers": 0,
                "submarines": 0,
            },
        },
        "neighbors": ["germany", "italy", "czechoslovakia", "hungary", "switzerland"],
        "focus_tree": "austrian_focus_tree",
        "playable": True,
        "description": "The remnant of a once-great empire, Austria stands at a crossroads. Internal pressure for Anschluss (union) with Germany is growing, while the economy struggles. Can you preserve Austrian independence, or forge a new path for this proud nation?",
    },
}

# Focus trees
FOCUS_TREES = {
    "polish_focus_tree": {
        "fortify_borders": {
            "title": "Fortify the Borders",
            "description": "With aggressive neighbors on both sides, we must strengthen our border defenses to deter invasion.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 5,
                "war_support": 10,
            },
            "position": [1, 1],
        },
        "military_modernization": {
            "title": "Military Modernization",
            "description": "Poland's military needs modern equipment to stand against the war machines of Germany and the Soviet Union.",
            "time": 70,
            "prerequisites": ["fortify_borders"],
            "mutually_exclusive": [],
            "effects": {
                "production_bonus": {
                    "military_factories": 10,
                    "tanks": 15,
                    "aircraft": 10,
                },
            },
            "position": [1, 2],
        },
        "seek_western_allies": {
            "title": "Seek Western Allies",
            "description": "Poland cannot stand alone. We must secure firm guarantees from Britain and France.",
            "time": 70,
            "prerequisites": ["fortify_borders"],
            "mutually_exclusive": ["seek_accommodation_with_germany"],
            "effects": {
                "stability": 10,
                "relation_bonus": {
                    "uk": 30,
                    "france": 30,
                    "germany": -20,
                },
            },
            "position": [0, 2],
        },
        "polish_british_alliance": {
            "title": "Polish-British Alliance",
            "description": "Formalize our alliance with Great Britain to deter German aggression.",
            "time": 70,
            "prerequisites": ["seek_western_allies"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "war_support": 15,
                "relation_bonus": {
                    "uk": 50,
                },
                "guarantee": ["uk"],
            },
            "position": [0, 3],
        },
        "seek_accommodation_with_germany": {
            "title": "Accommodate German Demands",
            "description": "Perhaps giving up some territory to Germany will satisfy their demands and preserve our independence.",
            "time": 70,
            "prerequisites": ["fortify_borders"],
            "mutually_exclusive": ["seek_western_allies"],
            "effects": {
                "stability": -5,
                "war_support": -10,
                "relation_bonus": {
                    "germany": 30,
                },
            },
            "position": [2, 2],
        },
        "polish_german_non_aggression_pact": {
            "title": "Polish-German Non-Aggression Pact",
            "description": "Sign a ten-year non-aggression pact with Germany to secure our western border temporarily.",
            "time": 70,
            "prerequisites": ["seek_accommodation_with_germany"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "relation_bonus": {
                    "germany": 40,
                    "france": -20,
                    "uk": -20,
                },
                "non_aggression": ["germany"],
            },
            "position": [2, 3],
        },
        "develop_central_industrial_region": {
            "title": "Develop Central Industrial Region",
            "description": "Invest heavily in the Central Industrial Region (COP) to boost our industrial capacity.",
            "time": 70,
            "prerequisites": ["military_modernization"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 2,
                "military_factories": 1,
                "stability": 5,
            },
            "position": [1, 3],
        },
        "intermarum_alliance": {
            "title": "Intermarium Alliance",
            "description": "Form an alliance of nations between Germany and the Soviet Union, from the Baltic to the Black Sea.",
            "time": 70,
            "prerequisites": ["polish_british_alliance", "develop_central_industrial_region"],
            "mutually_exclusive": ["communist_revolution"],
            "effects": {
                "stability": 10,
                "war_support": 15,
                "relation_bonus": {
                    "romania": 40,
                    "hungary": 30,
                    "czechoslovakia": 30,
                    "lithuania": 30,
                    "latvia": 30,
                    "estonia": 30,
                },
                "create_faction": "Intermarium Alliance",
            },
            "position": [0, 4],
        },
        "polish_soviet_cooperation": {
            "title": "Polish-Soviet Cooperation",
            "description": "Seek improved relations with the Soviet Union despite our historical enmity.",
            "time": 70,
            "prerequisites": ["polish_german_non_aggression_pact"],
            "mutually_exclusive": ["prepare_for_total_defense"],
            "effects": {
                "stability": -5,
                "war_support": -10,
                "relation_bonus": {
                    "ussr": 30,
                },
            },
            "position": [3, 4],
        },
        "prepare_for_total_defense": {
            "title": "Prepare for Total Defense",
            "description": "We cannot trust any great power. Poland must prepare to defend itself against all potential aggressors.",
            "time": 70,
            "prerequisites": ["develop_central_industrial_region"],
            "mutually_exclusive": ["polish_soviet_cooperation", "communist_revolution"],
            "effects": {
                "stability": 5,
                "war_support": 30,
                "military_factories": 1,
            },
            "position": [1, 4],
        },
        "communist_revolution": {
            "title": "Communist Revolution",
            "description": "The only way to save Poland from fascist aggression is to embrace communism and align with the Soviet Union.",
            "time": 70,
            "prerequisites": ["develop_central_industrial_region"],
            "mutually_exclusive": ["intermarum_alliance", "prepare_for_total_defense"],
            "effects": {
                "stability": -20,
                "war_support": 10,
                "government_change": "Communist",
                "relation_bonus": {
                    "ussr": 50,
                    "uk": -30,
                    "france": -30,
                    "germany": -50,
                },
            },
            "position": [2, 4],
        },
        "restore_polish_monarchy": {
            "title": "Restore the Polish Monarchy",
            "description": "Restore the Polish monarchy to unite the nation under a strong figurehead in these dangerous times.",
            "time": 70,
            "prerequisites": ["prepare_for_total_defense"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "war_support": 10,
                "government_change": "Non-Aligned",
                "new_leader": "Prince Augustus Czartoryski",
            },
            "position": [1, 5],
        },
    },
    "yugoslavian_focus_tree": {
        "balance_ethnic_tensions": {
            "title": "Balance Ethnic Tensions",
            "description": "Yugoslavia is a patchwork of different ethnic groups. We must carefully balance their interests to maintain unity.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "political_power": 50,
            },
            "position": [1, 1],
        },
        "industrialize_croatia": {
            "title": "Industrialize Croatia",
            "description": "Focus industrial development in Croatia to strengthen the economy and integrate this region more closely.",
            "time": 70,
            "prerequisites": ["balance_ethnic_tensions"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "stability": 5,
            },
            "position": [0, 2],
        },
        "serbian_military_tradition": {
            "title": "Serbian Military Tradition",
            "description": "Build upon Serbia's proud military history to strengthen the Yugoslav armed forces.",
            "time": 70,
            "prerequisites": ["balance_ethnic_tensions"],
            "mutually_exclusive": [],
            "effects": {
                "military_factories": 1,
                "war_support": 10,
            },
            "position": [2, 2],
        },
        "federal_structure": {
            "title": "Federal Structure Reform",
            "description": "Reorganize Yugoslavia into a true federation of equal constituent republics to better address ethnic concerns.",
            "time": 70,
            "prerequisites": ["balance_ethnic_tensions"],
            "mutually_exclusive": ["serbian_domination"],
            "effects": {
                "stability": 20,
                "war_support": -5,
                "government_change": "Democratic",
            },
            "position": [1, 2],
        },
        "croatian_autonomy": {
            "title": "Croatian Autonomy",
            "description": "Grant greater autonomy to Croatia within the federation to address their national aspirations.",
            "time": 70,
            "prerequisites": ["federal_structure", "industrialize_croatia"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "civilian_factories": 1,
            },
            "position": [0, 3],
        },
        "serbian_domination": {
            "title": "Serbian Domination",
            "description": "Serbia is the dominant force in Yugoslavia and should rightfully lead the nation with a firm hand.",
            "time": 70,
            "prerequisites": ["serbian_military_tradition"],
            "mutually_exclusive": ["federal_structure"],
            "effects": {
                "stability": -10,
                "war_support": 15,
                "government_change": "Neutral",
            },
            "position": [2, 3],
        },
        "royal_dictatorship": {
            "title": "Royal Dictatorship",
            "description": "King Alexander's assassination has shown that democracy cannot work in our divided nation. Strengthen royal authority to maintain order.",
            "time": 70,
            "prerequisites": ["serbian_domination"],
            "mutually_exclusive": ["workers_councils"],
            "effects": {
                "stability": 15,
                "war_support": 10,
                "government_change": "Non-Aligned",
            },
            "position": [3, 4],
        },
        "workers_councils": {
            "title": "Workers' Councils",
            "description": "Implement a system of workers' self-management to build a unique Yugoslav path to socialism.",
            "time": 70,
            "prerequisites": ["federal_structure"],
            "mutually_exclusive": ["royal_dictatorship", "democratic_constitution"],
            "effects": {
                "stability": 5,
                "civilian_factories": 2,
                "government_change": "Communist",
            },
            "position": [1, 4],
        },
        "democratic_constitution": {
            "title": "Democratic Constitution",
            "description": "Draft a new constitution enshrining democratic principles and guaranteeing rights for all ethnic groups.",
            "time": 70,
            "prerequisites": ["federal_structure"],
            "mutually_exclusive": ["workers_councils", "royal_dictatorship"],
            "effects": {
                "stability": 15,
                "war_support": -5,
                "government_change": "Democratic",
            },
            "position": [0, 4],
        },
        "align_with_little_entente": {
            "title": "Align with Little Entente",
            "description": "Strengthen our ties with Czechoslovakia and Romania to form a powerful alliance against revisionist neighbors.",
            "time": 70,
            "prerequisites": ["balance_ethnic_tensions"],
            "mutually_exclusive": ["seek_italian_friendship"],
            "effects": {
                "relation_bonus": {
                    "czechoslovakia": 40,
                    "romania": 40,
                    "france": 20,
                },
                "guarantee": ["czechoslovakia", "romania"],
            },
            "position": [1, 3],
        },
        "seek_italian_friendship": {
            "title": "Seek Italian Friendship",
            "description": "Improve relations with Fascist Italy to secure our western border and gain a powerful ally.",
            "time": 70,
            "prerequisites": ["serbian_domination"],
            "mutually_exclusive": ["align_with_little_entente"],
            "effects": {
                "stability": 5,
                "relation_bonus": {
                    "italy": 50,
                    "france": -20,
                    "uk": -10,
                },
                "non_aggression": ["italy"],
            },
            "position": [2, 4],
        },
        "expand_naval_facilities": {
            "title": "Expand Adriatic Naval Facilities",
            "description": "Develop our Adriatic coast with modern naval facilities to establish Yugoslavia as a naval power in the Mediterranean.",
            "time": 70,
            "prerequisites": ["seek_italian_friendship"],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 2,
                "civilian_factories": 1,
            },
            "position": [3, 5],
        },
        "balkan_federation": {
            "title": "Balkan Federation",
            "description": "Propose a federation of Balkan states to overcome historical divisions and create a powerful regional bloc.",
            "time": 70,
            "prerequisites": ["workers_councils"],
            "mutually_exclusive": [],
            "effects": {
                "relation_bonus": {
                    "bulgaria": 40,
                    "romania": 30,
                    "greece": 30,
                    "albania": 50,
                },
                "create_faction": "Balkan Federation",
            },
            "position": [1, 5],
        },
        "adriatic_defense_line": {
            "title": "Adriatic Defense Line",
            "description": "Fortify our coastline against potential Italian aggression, focusing on key strategic points.",
            "time": 70,
            "prerequisites": ["align_with_little_entente"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 5,
                "war_support": 10,
            },
            "position": [0, 5],
        },
    },
    "belgian_focus_tree": {
        "strengthen_neutrality": {
            "title": "Strengthen Neutrality",
            "description": "Belgium's neutrality has been guaranteed by international treaty. We must reinforce this diplomatic position.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "war_support": -5,
                "relation_bonus": {
                    "uk": 10,
                    "france": 10,
                    "germany": 10,
                },
            },
            "position": [1, 1],
        },
        "expand_antwerp_port": {
            "title": "Expand Antwerp Port",
            "description": "Antwerp is one of Europe's major ports. Expanding it will boost our economy and international importance.",
            "time": 70,
            "prerequisites": ["strengthen_neutrality"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "dockyards": 1,
            },
            "position": [1, 2],
        },
        "fortify_german_border": {
            "title": "Fortify German Border",
            "description": "Despite our neutrality, we must prepare for the worst. Build defensive fortifications along our eastern border.",
            "time": 70,
            "prerequisites": ["strengthen_neutrality"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 10,
                "stability": -5,
                "relation_bonus": {
                    "germany": -10,
                },
            },
            "position": [2, 2],
        },
        "industrial_development": {
            "title": "Wallonian Industrial Development",
            "description": "Invest in the heavy industries of Wallonia to strengthen our economy and military potential.",
            "time": 70,
            "prerequisites": ["expand_antwerp_port"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "military_factories": 1,
            },
            "position": [0, 3],
        },
        "integrate_congo_resources": {
            "title": "Integrate Congo Resources",
            "description": "Our colony in the Congo contains vast resources that can be better integrated into our war economy.",
            "time": 70,
            "prerequisites": ["industrial_development"],
            "mutually_exclusive": [],
            "effects": {
                "resources": {
                    "rubber": 10,
                    "tungsten": 5,
                    "steel": 5,
                },
            },
            "position": [0, 4],
        },
        "french_military_cooperation": {
            "title": "French Military Cooperation",
            "description": "Coordinate our defensive plans with France to ensure mutual support in case of German aggression.",
            "time": 70,
            "prerequisites": ["fortify_german_border"],
            "mutually_exclusive": ["abandon_neutrality"],
            "effects": {
                "war_support": 15,
                "relation_bonus": {
                    "france": 30,
                    "germany": -20,
                },
                "guarantee": ["france"],
            },
            "position": [2, 3],
        },
        "abandon_neutrality": {
            "title": "Abandon Neutrality",
            "description": "Our neutrality has not served us well in past conflicts. We must take a more active stance in European affairs.",
            "time": 70,
            "prerequisites": ["fortify_german_border", "expand_antwerp_port"],
            "mutually_exclusive": ["french_military_cooperation"],
            "effects": {
                "stability": -10,
                "war_support": 20,
            },
            "position": [1, 3],
        },
        "ally_with_germany": {
            "title": "Alliance with Germany",
            "description": "Perhaps aligning with the rising power of Germany is our best path to security and prosperity.",
            "time": 70,
            "prerequisites": ["abandon_neutrality"],
            "mutually_exclusive": ["join_allies"],
            "effects": {
                "relation_bonus": {
                    "germany": 50,
                    "france": -40,
                    "uk": -40,
                },
                "stability": -5,
                "join_faction": "axis",
            },
            "position": [0, 5],
        },
        "join_allies": {
            "title": "Join the Allies",
            "description": "Our best hope lies with Britain and France. We should formally join their alliance against German aggression.",
            "time": 70,
            "prerequisites": ["abandon_neutrality", "french_military_cooperation"],
            "mutually_exclusive": ["ally_with_germany"],
            "effects": {
                "relation_bonus": {
                    "uk": 50,
                    "france": 50,
                    "germany": -40,
                },
                "stability": 10,
                "join_faction": "allies",
            },
            "position": [2, 4],
        },
        "expand_military_industry": {
            "title": "Expand Military Industry",
            "description": "Significantly expand our arms production capabilities to prepare for possible conflict.",
            "time": 70,
            "prerequisites": ["ally_with_germany", "join_allies"],
            "mutually_exclusive": [],
            "effects": {
                "military_factories": 2,
            },
            "position": [1, 5],
        },
        "benelux_defense_agreement": {
            "title": "Benelux Defense Agreement",
            "description": "Form a defensive alliance with the Netherlands and Luxembourg to better protect our mutual interests.",
            "time": 70,
            "prerequisites": ["join_allies"],
            "mutually_exclusive": [],
            "effects": {
                "relation_bonus": {
                    "netherlands": 50,
                    "luxembourg": 50,
                },
                "create_faction": "Benelux Alliance",
            },
            "position": [3, 5],
        },
        "greater_belgium": {
            "title": "Greater Belgium",
            "description": "Reclaim territories historically connected to Belgium, including parts of northern France and southern Netherlands.",
            "time": 70,
            "prerequisites": ["ally_with_germany"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 20,
                "stability": -10,
                "gain_territory": "netherlands",
            },
            "position": [0, 6],
        },
    },
    "spanish_focus_tree": {
        "civil_war_recovery": {
            "title": "Civil War Recovery",
            "description": "Spain has been devastated by the civil war. We must focus on rebuilding our nation's infrastructure and healing the wounds of this fratricidal conflict.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "civilian_factories": 2,
                "resources": {
                    "steel": 5,
                    "tungsten": 5
                }
            },
            "position": [1, 1]
        },
        "falangist_consolidation": {
            "title": "Falangist Consolidation",
            "description": "Strengthen Franco's rule and the Falangist party's grip on power, crushing any remaining Republican resistance.",
            "time": 70,
            "prerequisites": ["civil_war_recovery"],
            "mutually_exclusive": ["republican_underground"],
            "effects": {
                "stability": 15,
                "war_support": 10,
                "political_influence": 20
            },
            "position": [0, 2]
        },
        "republican_underground": {
            "title": "Republican Underground",
            "description": "Secretly support the remaining Republican forces operating underground. The dream of a democratic Spain is not dead.",
            "time": 70,
            "prerequisites": ["civil_war_recovery"],
            "mutually_exclusive": ["falangist_consolidation"],
            "effects": {
                "stability": -10,
                "political_influence": 15
            },
            "position": [2, 2]
        },
        "anti_communist_volunteers": {
            "title": "Anti-Communist Volunteers",
            "description": "Send Spanish volunteers to fight against the Soviet Union alongside German forces, maintaining official neutrality while supporting the Axis fight against communism.",
            "time": 70,
            "prerequisites": ["falangist_consolidation"],
            "mutually_exclusive": [],
            "effects": {
                "relation_bonus": {
                    "germany": 20,
                    "italy": 10,
                    "ussr": -20
                },
                "army_organization": 5
            },
            "position": [0, 3]
        },
        "reclaim_empire": {
            "title": "Reclaim the Empire",
            "description": "Spain once ruled a vast empire. The time has come to reclaim our rightful territories and restore Spanish glory.",
            "time": 70,
            "prerequisites": ["falangist_consolidation"],
            "mutually_exclusive": [],
            "effects": {
                "claim_territory": ["north_africa", "latin_america"],
                "war_support": 15
            },
            "position": [1, 3]
        },
        "restore_republic": {
            "title": "Restore the Republic",
            "description": "The time has come to overthrow Franco's fascist regime and restore the democratic Spanish Republic.",
            "time": 70,
            "prerequisites": ["republican_underground"],
            "mutually_exclusive": [],
            "effects": {
                "government": "Democratic",
                "stability": -20,
                "political_influence": 30
            },
            "position": [2, 3]
        },
        "gibraltar_operation": {
            "title": "Operation Felix",
            "description": "Seize the opportunity to reclaim Gibraltar from the British, securing this strategic point for Spain.",
            "time": 70,
            "prerequisites": ["reclaim_empire"],
            "mutually_exclusive": [],
            "effects": {
                "relation_bonus": {
                    "uk": -40
                },
                "claim_territory": ["gibraltar"]
            },
            "position": [1, 4]
        },
        "join_allies": {
            "title": "Join the Allies",
            "description": "With the Republic restored, we will join the Allied powers in their fight against fascism across Europe.",
            "time": 70,
            "prerequisites": ["restore_republic"],
            "mutually_exclusive": [],
            "effects": {
                "relation_bonus": {
                    "uk": 40,
                    "france": 40,
                    "usa": 40,
                    "germany": -50,
                    "italy": -50
                },
                "join_faction": "Allies"
            },
            "position": [2, 4]
        }
    },

    "turkish_focus_tree": {
        "kemalist_reforms": {
            "title": "Kemalist Reforms",
            "description": "Continue Atatürk's modernization reforms to transform Turkey into a secular, Western-oriented nation.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "political_influence": 20,
                "civilian_factories": 1
            },
            "position": [1, 1]
        },
        "strategic_neutrality": {
            "title": "Strategic Neutrality",
            "description": "Turkey must carefully balance relations with all major powers while maintaining its neutrality in the growing conflict.",
            "time": 70,
            "prerequisites": ["kemalist_reforms"],
            "mutually_exclusive": ["ottoman_restoration"],
            "effects": {
                "stability": 15,
                "relation_bonus": {
                    "germany": 10,
                    "uk": 10,
                    "ussr": 10
                }
            },
            "position": [0, 2]
        },
        "ottoman_restoration": {
            "title": "Neo-Ottoman Ambitions",
            "description": "The collapse of imperial order in Europe presents an opportunity to reclaim former Ottoman territories and restore Turkish influence.",
            "time": 70,
            "prerequisites": ["kemalist_reforms"],
            "mutually_exclusive": ["strategic_neutrality"],
            "effects": {
                "war_support": 20,
                "claim_territory": ["cyprus", "syria", "iraq"],
                "stability": -5
            },
            "position": [2, 2]
        },
        "industrial_modernization": {
            "title": "Industrial Modernization",
            "description": "Invest heavily in industrial development to transform Turkey's largely agricultural economy into a modern industrial power.",
            "time": 70,
            "prerequisites": ["strategic_neutrality"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 3,
                "military_factories": 1,
                "resources": {
                    "steel": 10,
                    "chromium": 5
                }
            },
            "position": [0, 3]
        },
        "balkan_dominance": {
            "title": "Balkan Dominance",
            "description": "Expand Turkish influence in the Balkans, potentially reclaiming territories lost after World War I.",
            "time": 70,
            "prerequisites": ["ottoman_restoration"],
            "mutually_exclusive": [],
            "effects": {
                "claim_territory": ["thrace", "aegean_islands"],
                "relation_bonus": {
                    "greece": -30,
                    "bulgaria": -10
                }
            },
            "position": [2, 3]
        }
    },

    "swedish_focus_tree": {
        "maintain_neutrality": {
            "title": "Maintain Swedish Neutrality",
            "description": "Sweden has a long tradition of neutrality in European conflicts. We must carefully navigate the brewing storm to keep our nation out of the war.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "war_support": -10,
                "relation_bonus": {
                    "germany": 5,
                    "uk": 5
                }
            },
            "position": [1, 1]
        },
        "expand_mining_operations": {
            "title": "Expand Mining Operations",
            "description": "Sweden's vast iron ore deposits are crucial to the German war machine. By expanding our mining operations, we can leverage this valuable resource for diplomatic advantage.",
            "time": 70,
            "prerequisites": ["maintain_neutrality"],
            "mutually_exclusive": [],
            "effects": {
                "resources": {
                    "steel": 30,
                    "tungsten": 10
                },
                "civilian_factories": 2
            },
            "position": [0, 2]
        },
        "nordic_defense_pact": {
            "title": "Nordic Defense Pact",
            "description": "Form a defensive alliance with our Nordic neighbors to protect against potential aggression from Germany or the Soviet Union.",
            "time": 70,
            "prerequisites": ["maintain_neutrality"],
            "mutually_exclusive": [],
            "effects": {
                "relation_bonus": {
                    "finland": 30,
                    "norway": 30,
                    "denmark": 30
                },
                "create_faction": "Nordic Council"
            },
            "position": [2, 2]
        },
        "industrial_self_sufficiency": {
            "title": "Industrial Self-Sufficiency",
            "description": "Develop Sweden's industrial base to reduce dependency on imports that could be disrupted by the war.",
            "time": 70,
            "prerequisites": ["expand_mining_operations"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 3,
                "military_factories": 2,
                "stability": 10
            },
            "position": [0, 3]
        },
        "scandinavian_cooperation": {
            "title": "Scandinavian Cooperation",
            "description": "Deepen economic and military ties with our Scandinavian neighbors to create a stronger united front against external threats.",
            "time": 70,
            "prerequisites": ["nordic_defense_pact"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "military_factories": 1,
                "alliance_with": ["norway", "denmark", "finland"]
            },
            "position": [2, 3]
        }
    },

    "soviet_focus_tree": {
        "five_year_plan": {
            "title": "The Second Five Year Plan",
            "description": "Continue Stalin's ambitious industrialization program to transform the Soviet Union into a modern industrial power.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 3,
                "military_factories": 2,
                "stability": -5,
            },
            "position": [1, 1],
        },
        "nkvd_expansion": {
            "title": "Expand the NKVD",
            "description": "Strengthen state security to deal with counter-revolutionaries and saboteurs undermining our socialist progress.",
            "time": 70,
            "prerequisites": ["five_year_plan"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "war_support": 5,
                "political_influence": 20,
            },
            "position": [0, 2],
        },
        "collectivization": {
            "title": "Complete Collectivization",
            "description": "Finish the collectivization of agriculture to increase production efficiency and break the power of the kulaks.",
            "time": 70,
            "prerequisites": ["five_year_plan"],
            "mutually_exclusive": [],
            "effects": {
                "stability": -10,
                "resources": {
                    "food": 15,
                },
            },
            "position": [1, 2],
        },
        "military_industry": {
            "title": "Military Industrialization",
            "description": "Prioritize heavy industry and military production to prepare for the inevitable conflict with capitalist powers.",
            "time": 70,
            "prerequisites": ["five_year_plan"],
            "mutually_exclusive": [],
            "effects": {
                "military_factories": 3,
                "resources": {
                    "steel": 10,
                    "oil": 5,
                },
            },
            "position": [2, 2],
        },
        "great_purge": {
            "title": "The Great Purge",
            "description": "Cleanse the party, military, and society of potential traitors and Trotskyist elements to ensure loyalty to Stalin.",
            "time": 70,
            "prerequisites": ["nkvd_expansion"],
            "mutually_exclusive": ["rehabilitate_trotsky"],
            "effects": {
                "stability": 20,
                "war_support": -10,
                "army_organization": -15,
            },
            "position": [0, 3],
        },
        "rehabilitate_trotsky": {
            "title": "Rehabilitate Trotsky",
            "description": "In a shocking turn of events, restore Leon Trotsky to a position of influence and embrace his theory of permanent revolution.",
            "time": 70,
            "prerequisites": ["nkvd_expansion"],
            "mutually_exclusive": ["great_purge"],
            "effects": {
                "stability": -15,
                "war_support": 15,
                "political_influence": 30,
            },
            "position": [0, 4],
        },
        "red_army_expansion": {
            "title": "Red Army Modernization",
            "description": "Invest heavily in expanding and modernizing our armed forces to face any capitalist aggression.",
            "time": 70,
            "prerequisites": ["military_industry", "collectivization"],
            "mutually_exclusive": [],
            "effects": {
                "military_factories": 2,
                "army_organization": 10,
                "resources": {
                    "tungsten": 5,
                    "aluminum": 10,
                },
            },
            "position": [1, 3],
        },
        "international_revolution": {
            "title": "Support International Revolution",
            "description": "Increase aid to communist movements worldwide to spread the revolution beyond Soviet borders.",
            "time": 70,
            "prerequisites": ["rehabilitate_trotsky"],
            "mutually_exclusive": ["socialism_in_one_country"],
            "effects": {
                "stability": -5,
                "war_support": 20,
                "political_influence": 40,
                "relation_bonus": {
                    "germany": -20,
                    "uk": -20,
                    "france": -20,
                },
            },
            "position": [-1, 5],
        },
        "socialism_in_one_country": {
            "title": "Socialism in One Country",
            "description": "Focus on building socialism within the Soviet Union rather than risky international adventures.",
            "time": 70,
            "prerequisites": ["great_purge", "red_army_expansion"],
            "mutually_exclusive": ["international_revolution"],
            "effects": {
                "stability": 15,
                "civilian_factories": 2,
                "political_influence": 20,
            },
            "position": [1, 4],
        },
        "defensive_line": {
            "title": "Stalin Line Fortifications",
            "description": "Construct a series of fortifications along our western border to defend against potential German aggression.",
            "time": 70,
            "prerequisites": ["socialism_in_one_country"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 5,
                "war_support": 10,
                "relation_bonus": {
                    "germany": -10,
                },
            },
            "position": [1, 5],
        },
        "third_international": {
            "title": "Strengthen the Comintern",
            "description": "Reinvigorate the Third International as a counter to growing fascist power in Europe.",
            "time": 70,
            "prerequisites": ["international_revolution"],
            "mutually_exclusive": [],
            "effects": {
                "create_faction": "Comintern",
                "political_influence": 30,
                "relation_bonus": {
                    "france": 10,  # to the French Communist Party
                    "germany": 10,  # to the German Communist Party
                },
            },
            "position": [-1, 6],
        },
        "pact_with_germany": {
            "title": "Molotov-Ribbentrop Pact",
            "description": "Sign a non-aggression pact with Nazi Germany to buy time and potentially divide Eastern Europe into spheres of influence.",
            "time": 70,
            "prerequisites": ["defensive_line", "socialism_in_one_country"],
            "mutually_exclusive": ["anti_fascist_alliance"],
            "effects": {
                "relation_bonus": {
                    "germany": 50,
                    "poland": -30,
                    "finland": -30,
                    "romania": -30,
                },
                "claim_territory": ["finland", "poland_east", "romania"],
            },
            "position": [2, 5],
        },
        "anti_fascist_alliance": {
            "title": "Anti-Fascist Alliance",
            "description": "Set aside ideological differences temporarily to form an alliance with Western democracies against the fascist threat.",
            "time": 70,
            "prerequisites": ["defensive_line"],
            "mutually_exclusive": ["pact_with_germany"],
            "effects": {
                "relation_bonus": {
                    "uk": 30,
                    "france": 30,
                    "germany": -40,
                },
            },
            "position": [0, 6],
        },
        "claims_on_finland": {
            "title": "Claims on Finnish Territory",
            "description": "Demand territorial concessions from Finland to secure Leningrad's northern approaches.",
            "time": 70,
            "prerequisites": ["pact_with_germany"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 10,
                "claim_territory": ["finland"],
                "relation_bonus": {
                    "finland": -50,
                },
            },
            "position": [3, 6],
        },
        "red_tanks": {
            "title": "Soviet Tank Program",
            "description": "Accelerate the development and production of advanced tank designs like the T-34 and KV series.",
            "time": 70,
            "prerequisites": ["red_army_expansion"],
            "mutually_exclusive": [],
            "effects": {
                "military_factories": 2,
                "army_research_bonus": 15,
            },
            "position": [1, 7],
        },
        "world_revolution": {
            "title": "World Revolution",
            "description": "The time has come to spread the revolution globally and overthrow the capitalist order once and for all.",
            "time": 70,
            "prerequisites": ["third_international", "red_tanks"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 25,
                "stability": -5,
                "political_influence": 50,
                "claim_territory": ["europe"],
            },
            "position": [0, 8],
        },
    },
    "japanese_focus_tree": {
        "marco_polo_bridge": {
            "title": "Marco Polo Bridge Incident",
            "description": "The clash at the Marco Polo Bridge has provided us with a pretext to expand our presence in China. We must seize this opportunity for further expansion.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 15,
                "claim_territory": ["china"],
            },
            "position": [1, 1],
        },
        "southern_expansion": {
            "title": "Southern Expansion Doctrine",
            "description": "Japan's future lies in the resource-rich lands of Southeast Asia. We must prepare to secure these vital territories.",
            "time": 70,
            "prerequisites": ["marco_polo_bridge"],
            "mutually_exclusive": ["northern_expansion"],
            "effects": {
                "relation_bonus": {
                    "uk": -20,
                    "usa": -20,
                    "netherlands": -20,
                },
                "claim_territory": ["indonesia", "malaysia"],
            },
            "position": [0, 2],
        },
        "northern_expansion": {
            "title": "Northern Expansion Doctrine",
            "description": "The Soviet Union poses the greatest threat to our ambitions in Asia. We must focus our military preparations against them.",
            "time": 70,
            "prerequisites": ["marco_polo_bridge"],
            "mutually_exclusive": ["southern_expansion"],
            "effects": {
                "relation_bonus": {
                    "soviet": -30,
                },
                "claim_territory": ["mongolia", "siberia"],
            },
            "position": [2, 2],
        },
        "imperial_glory": {
            "title": "Imperial Glory",
            "description": "The divine Emperor's rule must be extended to guide the peoples of Asia toward a new era of prosperity under Japanese leadership.",
            "time": 70,
            "prerequisites": ["marco_polo_bridge"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "war_support": 10,
                "political_influence": 25,
            },
            "position": [1, 2],
        },
        "economic_expansion": {
            "title": "Industrial Development",
            "description": "To support our military ambitions, we must rapidly expand our industrial capacity and resource exploitation.",
            "time": 70,
            "prerequisites": ["imperial_glory"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 2,
                "military_factories": 2,
            },
            "position": [1, 3],
        },
        "zero_fighter": {
            "title": "Zero Fighter Development",
            "description": "Invest in the development of the A6M Zero fighter, which will give us air superiority across the Pacific.",
            "time": 70,
            "prerequisites": ["economic_expansion"],
            "mutually_exclusive": [],
            "effects": {
                "military_factories": 1,
                "air_research_bonus": 15,
            },
            "position": [0, 4],
        },
        "naval_expansion": {
            "title": "Imperial Japanese Navy Expansion",
            "description": "The navy is the key to Japanese power projection in the Pacific. We must build more carriers and battleships.",
            "time": 70,
            "prerequisites": ["economic_expansion"],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 3,
                "navy_research_bonus": 15,
            },
            "position": [2, 4],
        },
        "greater_east_asia": {
            "title": "Greater East Asia Co-Prosperity Sphere",
            "description": "Create a new economic and political bloc of Asian nations under Japanese leadership, free from Western colonialism.",
            "time": 70,
            "prerequisites": ["southern_expansion", "imperial_glory"],
            "mutually_exclusive": [],
            "effects": {
                "create_faction": "Co-Prosperity Sphere",
                "political_influence": 50,
            },
            "position": [0, 5],
        },
        "puppet_manchuria": {
            "title": "Manchukuo Development",
            "description": "Further develop our puppet state in Manchuria as a base for industrial development and military operations in China.",
            "time": 70,
            "prerequisites": ["northern_expansion", "imperial_glory"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "military_factories": 1,
                "resources": {
                    "steel": 10,
                    "aluminum": 5,
                },
            },
            "position": [2, 5],
        },
        "anti_comintern": {
            "title": "Anti-Comintern Pact",
            "description": "Form an alliance with Germany against the threat of international communism and Soviet expansion.",
            "time": 70,
            "prerequisites": ["northern_expansion"],
            "mutually_exclusive": ["pacific_neutrality"],
            "effects": {
                "relation_bonus": {
                    "germany": 50,
                    "italy": 30,
                    "soviet": -40,
                },
                "join_faction": "axis",
            },
            "position": [3, 3],
        },
        "pacific_neutrality": {
            "title": "Pacific Non-Aggression",
            "description": "Seek diplomatic solutions with Western powers to secure our interests while avoiding a devastating war.",
            "time": 70,
            "prerequisites": ["imperial_glory"],
            "mutually_exclusive": ["anti_comintern", "greater_east_asia"],
            "effects": {
                "stability": 15,
                "relation_bonus": {
                    "usa": 30,
                    "uk": 30,
                },
            },
            "position": [1, 5],
        },
        "strike_pearl_harbor": {
            "title": "Strike South: Pearl Harbor",
            "description": "A bold surprise attack on the American Pacific Fleet will buy us the time needed to secure the resources of Southeast Asia.",
            "time": 70,
            "prerequisites": ["greater_east_asia", "naval_expansion"],
            "mutually_exclusive": ["pacific_neutrality"],
            "effects": {
                "war_support": 25,
                "stability": -10,
                "declare_war": ["usa"],
            },
            "position": [1, 6],
        },
    },
    "italian_focus_tree": {
        "ethiopian_war": {
            "title": "The Ethiopian War",
            "description": "Our conquest of Ethiopia has demonstrated Italy's military might. We must consolidate our gains and establish proper colonial administration.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 10,
                "resources": {
                    "steel": 5,
                    "chromium": 5,
                },
            },
            "position": [1, 1],
        },
        "industrial_north": {
            "title": "Industrialize Northern Italy",
            "description": "Focus industrial development in the Po Valley to create a strong manufacturing base for Italy.",
            "time": 70,
            "prerequisites": ["ethiopian_war"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 2,
                "military_factories": 1,
            },
            "position": [0, 2],
        },
        "strengthen_fascist_rule": {
            "title": "Strengthen Fascist Rule",
            "description": "Solidify the PNF's control over all aspects of Italian society and crush any remaining opposition.",
            "time": 70,
            "prerequisites": ["ethiopian_war"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "political_influence": 50,
            },
            "position": [1, 2],
        },
        "naval_expansion": {
            "title": "Mare Nostrum",
            "description": "The Mediterranean is rightfully an Italian lake. Expand our naval capabilities to dominate this vital sea.",
            "time": 70,
            "prerequisites": ["ethiopian_war"],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 2,
                "navy_research_bonus": 10,
            },
            "position": [2, 2],
        },
        "balkan_diplomacy": {
            "title": "Balkan Diplomacy",
            "description": "Strengthen our ties with the Balkan nations to increase Italian influence in the region.",
            "time": 70,
            "prerequisites": ["strengthen_fascist_rule"],
            "mutually_exclusive": [],
            "effects": {
                "relation_bonus": {
                    "yugoslavia": 15,
                    "romania": 15,
                    "bulgaria": 15,
                    "greece": 15,
                },
            },
            "position": [1, 3],
        },
        "albanian_occupation": {
            "title": "Occupy Albania",
            "description": "Albania is key to controlling the Adriatic. We should formally annex it to secure our strategic position.",
            "time": 70,
            "prerequisites": ["balkan_diplomacy"],
            "mutually_exclusive": [],
            "effects": {
                "gain_territory": "albania",
                "military_factories": 1,
                "relation_bonus": {
                    "yugoslavia": -20,
                    "greece": -20,
                },
            },
            "position": [2, 4],
        },
        "german_alignment": {
            "title": "Align with Germany",
            "description": "Germany and Italy share ideological values and strategic interests. We should formalize our partnership.",
            "time": 70,
            "prerequisites": ["strengthen_fascist_rule"],
            "mutually_exclusive": ["maintain_independence"],
            "effects": {
                "relation_bonus": {
                    "germany": 50,
                    "uk": -20,
                    "france": -20,
                },
                "join_faction": "axis",
            },
            "position": [0, 4],
        },
        "maintain_independence": {
            "title": "Independent Foreign Policy",
            "description": "Italy's interests are not always aligned with Germany's. We should maintain our independence and pursue our own objectives.",
            "time": 70,
            "prerequisites": ["strengthen_fascist_rule", "balkan_diplomacy"],
            "mutually_exclusive": ["german_alignment"],
            "effects": {
                "stability": 5,
                "political_influence": 25,
                "relation_bonus": {
                    "germany": -10,
                    "uk": 10,
                    "france": 10,
                },
            },
            "position": [1, 4],
        },
        "spanish_intervention": {
            "title": "Intervene in Spain",
            "description": "The Spanish Civil War presents an opportunity to support Franco and establish another fascist ally in the Mediterranean.",
            "time": 70,
            "prerequisites": ["german_alignment"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 5,
                "relation_bonus": {
                    "spain": 30,
                    "france": -10,
                },
            },
            "position": [0, 5],
        },
        "roman_empire": {
            "title": "Restore the Roman Empire",
            "description": "It is time to reclaim the glory of Rome and rebuild our ancient empire across the Mediterranean.",
            "time": 70,
            "prerequisites": ["albanian_occupation", "spanish_intervention"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 25,
                "stability": -5,
                "political_influence": 50,
                "claim_territory": ["france", "greece", "yugoslavia", "egypt"],
            },
            "position": [1, 6],
        },
        "libyan_expansion": {
            "title": "Develop Libya",
            "description": "Invest in our Libyan colony to strengthen our presence in North Africa.",
            "time": 70,
            "prerequisites": ["naval_expansion"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "military_factories": 1,
                "resources": {
                    "oil": 5,
                },
            },
            "position": [3, 3],
        },
        "claims_on_france": {
            "title": "Claims on French Territory",
            "description": "Corsica, Nice, and Savoy rightfully belong to Italy. We must prepare to reclaim these territories.",
            "time": 70,
            "prerequisites": ["german_alignment"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 10,
                "relation_bonus": {
                    "france": -30,
                },
                "claim_territory": ["france"],
            },
            "position": [0, 6],
        },
    },
    "dutch_focus_tree": {
        "protect_east_indies": {
            "title": "Protect the East Indies",
            "description": "Our colonial possessions in the East Indies are vital to our economy and status as a global power. We must protect them.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 1,
                "navy_research_bonus": 10,
            },
            "position": [1, 1],
        },
        "trade_expansion": {
            "title": "Trade Expansion",
            "description": "As a traditional trading nation, we should focus on expanding our commercial networks around the world.",
            "time": 70,
            "prerequisites": ["protect_east_indies"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 2,
                "resource_gain": {
                    "rubber": 5,
                    "oil": 5,
                },
            },
            "position": [1, 2],
        },
        "water_defenses": {
            "title": "Water Defenses",
            "description": "The Netherlands has a long tradition of using water as a defensive measure. Prepare plans to flood strategic areas if invasion threatens.",
            "time": 70,
            "prerequisites": ["protect_east_indies"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 5,
                "war_support": 10,
            },
            "position": [2, 2],
        },
        "modernize_port_rotterdam": {
            "title": "Modernize Rotterdam Port",
            "description": "Rotterdam is one of Europe's most important ports. Expanding and modernizing its facilities will boost our economy.",
            "time": 70,
            "prerequisites": ["trade_expansion"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "dockyards": 1,
                "stability": 5
            },
            "position": [0, 3],
        },
        "philips_industrial_development": {
            "title": "Philips Industrial Expansion",
            "description": "Support the expansion of Philips Electronics to become a leader in technological development.",
            "time": 70,
            "prerequisites": ["trade_expansion"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "research_slots": 1,
                "tech_research_bonus": 5
            },
            "position": [1, 3],
        },
        "focus_defensive_preparations": {
            "title": "Defensive Preparations",
            "description": "We must fortify key defensive positions along our borders to protect against possible German aggression.",
            "time": 70,
            "prerequisites": ["water_defenses"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 15,
                "military_factories": 1,
                "relation_bonus": {
                    "germany": -10,
                }
            },
            "position": [2, 3],
        },
        "neutrality_at_all_costs": {
            "title": "Maintain Strict Neutrality",
            "description": "Our neutrality protected us during the Great War. We must maintain this policy at all costs.",
            "time": 70,
            "prerequisites": ["water_defenses", "philips_industrial_development"],
            "mutually_exclusive": ["abandon_neutrality"],
            "effects": {
                "stability": 15,
                "war_support": -10,
                "relation_bonus": {
                    "germany": 10,
                    "uk": 10,
                    "france": 10,
                },
            },
            "position": [1, 4],
        },
        "abandon_neutrality": {
            "title": "Abandon Neutrality",
            "description": "The changing political landscape of Europe suggests that neutrality may no longer be a viable policy. We must choose sides.",
            "time": 70,
            "prerequisites": ["focus_defensive_preparations", "philips_industrial_development"],
            "mutually_exclusive": ["neutrality_at_all_costs"],
            "effects": {
                "stability": -10,
                "war_support": 20,
            },
            "position": [2, 4],
        },
        "ally_with_germany": {
            "title": "Accommodation with Germany",
            "description": "Given our vulnerable position, perhaps accommodation with Germany is the most pragmatic path forward.",
            "time": 70,
            "prerequisites": ["abandon_neutrality"],
            "mutually_exclusive": ["ally_with_uk"],
            "effects": {
                "relation_bonus": {
                    "germany": 50,
                    "uk": -30,
                    "france": -30,
                },
                "join_faction": "axis",
            },
            "position": [3, 5],
        },
        "ally_with_uk": {
            "title": "Alliance with Britain",
            "description": "Britain has long been our protector against continental hegemony. We should formally align with them.",
            "time": 70,
            "prerequisites": ["abandon_neutrality"],
            "mutually_exclusive": ["ally_with_germany"],
            "effects": {
                "relation_bonus": {
                    "uk": 50,
                    "france": 30,
                    "germany": -40,
                },
                "join_faction": "allies",
            },
            "position": [1, 5],
        },
        "dutch_east_indies_army": {
            "title": "Strengthen East Indies Army",
            "description": "We must significantly strengthen our colonial forces in the East Indies to protect against Japanese expansion.",
            "time": 70,
            "prerequisites": ["ally_with_uk"],
            "mutually_exclusive": [],
            "effects": {
                "military_factories": 1,
                "war_support": 10,
                "relation_bonus": {
                    "japan": -20,
                },
            },
            "position": [0, 6],
        },
        "colonial_nationalism": {
            "title": "Colonial Nationalism",
            "description": "Foster a sense of national identity in our colonies to ensure their loyalty to the Netherlands.",
            "time": 70,
            "prerequisites": ["dutch_east_indies_army"],
            "mutually_exclusive": ["indonesian_autonomy"],
            "effects": {
                "stability": 10,
                "resources": {
                    "rubber": 10,
                    "oil": 10,
                },
            },
            "position": [0, 7],
        },
        "indonesian_autonomy": {
            "title": "Indonesian Autonomy",
            "description": "Grant greater autonomy to Indonesian nationalists to secure their cooperation in our war effort.",
            "time": 70,
            "prerequisites": ["dutch_east_indies_army"],
            "mutually_exclusive": ["colonial_nationalism"],
            "effects": {
                "stability": -5,
                "war_support": 15,
                "military_factories": 1,
            },
            "position": [1, 7],
        },
        "greater_netherlands": {
            "title": "Greater Netherlands",
            "description": "Revive historical claims to Flanders and other historically Dutch territories.",
            "time": 70,
            "prerequisites": ["ally_with_germany"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 20,
                "stability": -10,
                "relation_bonus": {
                    "belgium": -50,
                    "france": -20,
                },
                "gain_territory": "belgium",
            },
            "position": [3, 6],
        },
        "reclaim_frisian_islands": {
            "title": "Reclaim the Frisian Islands",
            "description": "The German-held East Frisian Islands should be rightfully Dutch. We shall reclaim them.",
            "time": 70,
            "prerequisites": ["greater_netherlands"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 15,
                "gain_territory": "germany",
            },
            "position": [3, 7],
        },
    },
    "danish_focus_tree": {
        "nordic_cooperation": {
            "title": "Nordic Cooperation",
            "description": "Strengthen ties with our Scandinavian neighbors to present a united diplomatic front.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "relation_bonus": {
                    "sweden": 20,
                    "norway": 20,
                },
            },
            "position": [1, 1],
        },
        "agricultural_exports": {
            "title": "Agricultural Exports",
            "description": "Denmark's agricultural sector is highly developed. Focus on increasing exports to strengthen our economy.",
            "time": 70,
            "prerequisites": ["nordic_cooperation"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "stability": 5,
            },
            "position": [0, 2],
        },
        "small_nation_diplomacy": {
            "title": "Small Nation Diplomacy",
            "description": "As a small nation, we must rely on diplomatic skill rather than military might to navigate the dangerous waters of European politics.",
            "time": 70,
            "prerequisites": ["nordic_cooperation"],
            "mutually_exclusive": [],
            "effects": {
                "political_power": 100,
                "stability": 5,
            },
            "position": [2, 2],
        },
    },
    "norwegian_focus_tree": {
        "merchant_marine": {
            "title": "Merchant Marine",
            "description": "Norway's large merchant fleet is crucial to our economy and international standing. Expand and modernize it.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 1,
                "civilian_factories": 1,
            },
            "position": [1, 1],
        },
        "hydroelectric_power": {
            "title": "Hydroelectric Power",
            "description": "Norway's mountainous terrain is perfect for hydroelectric power generation. Develop this resource to power industrial growth.",
            "time": 70,
            "prerequisites": ["merchant_marine"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "military_factories": 1,
            },
            "position": [0, 2],
        },
        "coastal_defenses": {
            "title": "Coastal Defenses",
            "description": "Norway's long coastline is vulnerable to naval invasion. Strengthen coastal fortifications and defenses.",
            "time": 70,
            "prerequisites": ["merchant_marine"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 10,
                "stability": 5,
            },
            "position": [2, 2],
        },
    },
    "austrian_focus_tree": {
        "constitutional_reforms": {
            "title": "Constitutional Reforms",
            "description": "Reform the Austrian state to create a more stable political system capable of resisting external pressures.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "political_power": 50,
            },
            "position": [1, 1],
        },
        "alpine_fortifications": {
            "title": "Alpine Fortifications",
            "description": "The mountainous terrain of Austria provides natural defensive advantages. Fortify key passes and routes to deter invasion.",
            "time": 70,
            "prerequisites": ["constitutional_reforms"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 5,
                "war_support": 10,
            },
            "position": [0, 2],
        },
        "habsburg_restoration": {
            "title": "Habsburg Restoration",
            "description": "The ancient Habsburg dynasty ruled Austria for centuries. Restoring the monarchy could provide stability and legitimacy.",
            "time": 70,
            "prerequisites": ["constitutional_reforms"],
            "mutually_exclusive": ["resist_anschluss"],
            "effects": {
                "stability": 10,
                "war_support": 10,
                "government_change": "Monarchist",
            },
            "position": [1, 2],
        },
        "resist_anschluss": {
            "title": "Resist Anschluss",
            "description": "Germany seeks to absorb Austria into the Reich. We must resist these pressures and maintain our independence.",
            "time": 70,
            "prerequisites": ["constitutional_reforms"],
            "mutually_exclusive": ["habsburg_restoration"],
            "effects": {
                "stability": -5,
                "war_support": 15,
                "relation_bonus": {
                    "germany": -30,
                    "uk": 10,
                    "france": 10,
                },
            },
            "position": [2, 2],
        },
    },
    "german_focus_tree": {
        "rhineland": {
            "title": "Remilitarize the Rhineland",
            "description": "The Versailles Treaty prevents us from stationing troops in the Rhineland, which leaves western Germany vulnerable. We should reclaim our right to defend our borders.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 5,
                "war_support": 10,
                "world_tension": 5,
            },
            "position": [1, 1],
        },
        "ideological_crossroads": {
            "title": "Ideological Crossroads",
            "description": "Germany stands at a pivotal moment in history. We must choose our path forward: continue with fascism, embrace democracy, or pursue the communist ideal.",
            "time": 70,
            "prerequisites": ["rhineland"],
            "mutually_exclusive": [],
            "effects": {
                "stability": -5,
                "political_power": 150,
            },
            "position": [0, 2],
        },
        "democratic_reforms": {
            "title": "Democratic Reforms",
            "description": "Return Germany to a democratic path, renouncing the extremism of the Nazi party and restoring constitutional governance.",
            "time": 70,
            "prerequisites": ["ideological_crossroads"],
            "mutually_exclusive": ["communist_revolution", "fascist_loyalty"],
            "effects": {
                "stability": 10,
                "war_support": -15,
                "government_change": "Democratic",
                "new_leader": "Konrad Adenauer",
            },
            "position": [-1, 3],
        },
        "communist_revolution": {
            "title": "Communist Revolution",
            "description": "The time has come for the workers of Germany to rise up against capitalism and fascism alike. We shall bring about Karl Marx's vision for his homeland.",
            "time": 70,
            "prerequisites": ["ideological_crossroads"],
            "mutually_exclusive": ["democratic_reforms", "fascist_loyalty"],
            "effects": {
                "stability": -15,
                "war_support": 15,
                "government_change": "Communist",
                "new_leader": "Ernst Thälmann",
                "internal_conflicts": 1,
            },
            "position": [-2, 3],
        },
        "fascist_loyalty": {
            "title": "Loyalty to the Führer",
            "description": "Reaffirm our commitment to National Socialism and Hitler's leadership. The Reich shall continue on its destined path to greatness.",
            "time": 70,
            "prerequisites": ["ideological_crossroads"],
            "mutually_exclusive": ["communist_revolution", "democratic_reforms"],
            "effects": {
                "stability": 15,
                "war_support": 15,
            },
            "position": [0, 3],
        },
        "restore_kaiser": {
            "title": "Restore the Kaiser",
            "description": "The Hohenzollern monarchy brought Germany to its height of power. It is time to restore the Kaiser and rebuild the German Empire.",
            "time": 70,
            "prerequisites": ["democratic_reforms"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "war_support": 10,
                "government_change": "Monarchist",
                "new_leader": "Wilhelm III",
            },
            "position": [-1, 4],
        },
        "european_cooperation": {
            "title": "European Cooperation",
            "description": "Rather than conquest, Germany should lead a new era of European cooperation and integration.",
            "time": 70,
            "prerequisites": ["democratic_reforms"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "war_support": -10,
                "world_tension": -10,
                "diplomacy_bonus": 20,
            },
            "position": [-2, 4],
        },
        "workers_paradise": {
            "title": "Workers' Paradise",
            "description": "Create a true communist state in Germany, with worker-owned means of production and social equality for all.",
            "time": 70,
            "prerequisites": ["communist_revolution"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "civilian_factories": 3,
                "military_factories": 2,
            },
            "position": [-2, 4],
        },
        "align_with_soviet": {
            "title": "Align with Soviet Union",
            "description": "Forge a strong alliance with the Soviet Union to advance the cause of worldwide communist revolution.",
            "time": 70,
            "prerequisites": ["workers_paradise"],
            "mutually_exclusive": [],
            "effects": {
                "diplomacy": {
                    "ussr": 100,
                },
                "join_faction": "comintern",
            },
            "position": [-3, 5],
        },
        "stalin_pact": {
            "title": "The Stalin Pact",
            "description": "Sign a non-aggression pact with the Soviet Union that secretly divides Eastern Europe into spheres of influence.",
            "time": 70,
            "prerequisites": ["align_with_soviet"],
            "mutually_exclusive": [],
            "effects": {
                "diplomacy": {
                    "ussr": 50,
                    "poland": -30,
                },
                "stability": 10,
                "world_tension": -5,
            },
            "position": [-3, 6],
        },
        "revolutionary_army": {
            "title": "The Revolutionary Army",
            "description": "Reform the military along revolutionary lines, with political commissars ensuring loyalty to the communist cause.",
            "time": 70,
            "prerequisites": ["workers_paradise"],
            "mutually_exclusive": [],
            "effects": {
                "army": {
                    "divisions": 5,
                },
                "stability": -5,
                "war_support": 15,
            },
            "position": [-2, 5],
        },
        "great_purge": {
            "title": "The Great Purge",
            "description": "Eliminate potential opposition within the party and military to consolidate Communist control.",
            "time": 70,
            "prerequisites": ["revolutionary_army"],
            "mutually_exclusive": [],
            "effects": {
                "stability": -15,
                "war_support": -10,
                "political_power": 100,
                "internal_conflicts": 2,
            },
            "position": [-2, 6],
        },
        "export_revolution": {
            "title": "Export the Revolution",
            "description": "Support communist movements in neighboring countries to spread the revolution beyond Germany's borders.",
            "time": 70,
            "prerequisites": ["align_with_soviet", "revolutionary_army"],
            "mutually_exclusive": [],
            "effects": {
                "diplomacy": {
                    "france": -30,
                    "uk": -30,
                    "italy": -20,
                },
                "war_support": 20,
                "world_tension": 15,
            },
            "position": [-3, 7],
        },
        "democratic_coalition": {
            "title": "Democratic Coalition",
            "description": "Form a broad coalition government that represents all democratic factions within Germany.",
            "time": 70,
            "prerequisites": ["democratic_reforms"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 20,
                "war_support": -5,
                "political_power": 100,
            },
            "position": [-1, 5],
        },
        "western_allies": {
            "title": "Western Allies",
            "description": "Seek diplomatic and economic support from the Western democracies - France, Britain, and the United States.",
            "time": 70,
            "prerequisites": ["democratic_coalition"],
            "mutually_exclusive": [],
            "effects": {
                "diplomacy": {
                    "uk": 50,
                    "france": 50,
                    "usa": 30,
                },
                "civilian_factories": 2,
                "resources": {
                    "oil": 8,
                },
            },
            "position": [-1, 6],
        },
        "join_allies": {
            "title": "Join the Allies",
            "description": "Join the Allied powers, formally aligning democratic Germany with Britain and France against the threats of fascism and communism.",
            "time": 70,
            "prerequisites": ["western_allies"],
            "mutually_exclusive": [],
            "effects": {
                "join_faction": "allies",
                "stability": 10,
                "world_tension": -5,
            },
            "position": [-1, 7],
        },
        "european_federation": {
            "title": "European Federation",
            "description": "Propose a democratic federation of European states to prevent future wars and promote economic cooperation.",
            "time": 70,
            "prerequisites": ["european_cooperation"],
            "mutually_exclusive": [],
            "effects": {
                "diplomacy": {
                    "france": 30,
                    "belgium": 50,
                    "netherlands": 50,
                    "luxembourg": 50,
                },
                "stability": 15,
                "civilian_factories": 3,
            },
            "position": [-2, 5],
        },
        "invite_europe": {
            "title": "Invite European Nations",
            "description": "Extend formal invitations to neighboring countries to join the European economic and political community.",
            "time": 70,
            "prerequisites": ["european_federation"],
            "mutually_exclusive": [],
            "effects": {
                "diplomacy": {
                    "france": 50,
                    "italy": 30,
                    "belgium": 70,
                    "netherlands": 70,
                    "luxembourg": 70,
                },
                "create_faction": "european_union",
            },
            "position": [-2, 6],
        },
        "economic_miracle": {
            "title": "Economic Miracle",
            "description": "Implement free market reforms and infrastructure investments that jumpstart the German economy.",
            "time": 70,
            "prerequisites": ["democratic_coalition"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 5,
                "stability": 10,
                "infrastructure": 2,
            },
            "position": [0, 5],
        },
        "imperial_nostalgia": {
            "title": "Imperial Nostalgia",
            "description": "Foster a sense of nostalgia for the imperial era, highlighting the stability and prosperity under the Kaiser.",
            "time": 70,
            "prerequisites": ["democratic_reforms"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 5,
                "war_support": 5,
                "political_power": 50,
            },
            "position": [0, 4],
        },
        "military_tradition": {
            "title": "Prussian Military Tradition",
            "description": "Emphasize the honorable traditions of the Prussian military, distancing the army from Nazi extremism.",
            "time": 70,
            "prerequisites": ["imperial_nostalgia"],
            "mutually_exclusive": [],
            "effects": {
                "army_experience": 50,
                "war_support": 10,
            },
            "position": [0, 5],
        },
        "hohenzollern_loyalists": {
            "title": "Hohenzollern Loyalists",
            "description": "Organize political support for the restoration of the monarchy among conservatives and traditionalists.",
            "time": 70,
            "prerequisites": ["imperial_nostalgia", "military_tradition"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 5,
                "political_power": 100,
            },
            "position": [0, 6],
        },
        "third_way": {
            "title": "The Third Way",
            "description": "Chart a course between capitalism and communism with a balanced approach to economic and social policy.",
            "time": 70,
            "prerequisites": ["restore_kaiser"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "civilian_factories": 2,
                "military_factories": 1,
            },
            "position": [-1, 6],
        },
        "rearmament_program": {
            "title": "Royal Rearmament Program",
            "description": "Begin a measured military buildup under royal authority, emphasizing defensive capabilities.",
            "time": 70,
            "prerequisites": ["restore_kaiser"],
            "mutually_exclusive": [],
            "effects": {
                "military_factories": 3,
                "army": {
                    "divisions": 5,
                },
                "war_support": 15,
            },
            "position": [0, 7],
        },
        "naval_tradition": {
            "title": "Imperial Naval Tradition",
            "description": "Revive the proud naval tradition of Imperial Germany with investments in the Kriegsmarine.",
            "time": 70,
            "prerequisites": ["rearmament_program"],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 4,
                "navy": {
                    "ships": {
                        "battleships": 1,
                        "cruisers": 2,
                        "destroyers": 4,
                    },
                },
                "navy_experience": 50,
            },
            "position": [0, 8],
        },
        "nuclear_program": {
            "title": "Uranium Club",
            "description": "Establish a secret research program to explore the military applications of nuclear fission.",
            "time": 70,
            "prerequisites": ["fascist_loyalty"],
            "mutually_exclusive": [],
            "effects": {
                "research_bonus": {
                    "nuclear_tech": 50,
                },
                "world_tension": 5,
            },
            "position": [1, 4],
        },
        "blitzkrieg_doctrine": {
            "title": "Blitzkrieg Doctrine",
            "description": "Refine the revolutionary combined arms doctrine that emphasizes speed, surprise, and concentrated firepower.",
            "time": 70,
            "prerequisites": ["panzer_divisions"],
            "mutually_exclusive": [],
            "effects": {
                "army_experience": 50,
                "research_bonus": {
                    "land_doctrine": 20,
                },
            },
            "position": [1, 5],
        },
        "alliance_with_italy": {
            "title": "Alliance with Italy",
            "description": "Strengthen ties with Mussolini's Italy to form the core of a fascist bloc in Europe.",
            "time": 70,
            "prerequisites": ["fascist_loyalty"],
            "mutually_exclusive": [],
            "effects": {
                "diplomacy": {
                    "italy": 100,
                },
                "join_faction": "axis",
            },
            "position": [2, 4],
        },
        "alliance_with_japan": {
            "title": "Alliance with Japan",
            "description": "Extend the anti-communist pact to include Imperial Japan, creating a global fascist alliance.",
            "time": 70,
            "prerequisites": ["alliance_with_italy"],
            "mutually_exclusive": [],
            "effects": {
                "diplomacy": {
                    "japan": 100,
                },
                "world_tension": 5,
            },
            "position": [2, 5],
        },
        "lebensraum": {
            "title": "Lebensraum",
            "description": "Prepare for territorial expansion in Eastern Europe to secure living space for the German people.",
            "time": 70,
            "prerequisites": ["fascist_loyalty"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 20,
                "world_tension": 15,
            },
            "position": [3, 4],
        },
        "war_with_poland": {
            "title": "War with Poland",
            "description": "Launch a full-scale invasion of Poland to reclaim German territories and begin the expansion eastward.",
            "time": 70,
            "prerequisites": ["danzig_or_war", "molotov_ribbentrop_pact"],
            "mutually_exclusive": [],
            "effects": {
                "war_goal": "poland",
                "war_support": 15,
                "world_tension": 25,
            },
            "position": [2, 6],
        },
        "total_war": {
            "title": "Total War",
            "description": "Mobilize all of Germany's resources and population for an all-out war effort.",
            "time": 70,
            "prerequisites": ["war_with_poland"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": -3,
                "military_factories": 6,
                "war_support": 20,
                "stability": -10,
            },
            "position": [2, 7],
        },
        "anschluss": {
            "title": "Anschluss of Austria",
            "description": "The people of Austria are German by blood and culture. It is time to unite them with the Reich.",
            "time": 70,
            "prerequisites": ["rhineland"],
            "mutually_exclusive": [],
            "effects": {
                "annex": "austria",
                "civilian_factories": 4,
                "military_factories": 2,
                "stability": 5,
                "war_support": 5,
                "world_tension": 10,
            },
            "position": [1, 2],
        },
        "sudetenland": {
            "title": "Demand Sudetenland",
            "description": "The ethnic Germans in Czechoslovakia's Sudetenland region deserve to be part of the Reich.",
            "time": 70,
            "prerequisites": ["anschluss"],
            "mutually_exclusive": [],
            "effects": {
                "gain_territory": "czechoslovakia",
                "civilian_factories": 3,
                "military_factories": 2,
                "world_tension": 15,
            },
            "position": [1, 3],
        },
        "fate_czechoslovakia": {
            "title": "Fate of Czechoslovakia",
            "description": "With the Sudetenland secured, we must decide what to do with the remainder of Czechoslovakia.",
            "time": 70,
            "prerequisites": ["sudetenland"],
            "mutually_exclusive": [],
            "effects": {
                "annex": "czechoslovakia",
                "civilian_factories": 6,
                "military_factories": 4,
                "world_tension": 20,
            },
            "position": [1, 4],
        },
        "danzig_or_war": {
            "title": "Danzig or War",
            "description": "The Polish Corridor separates East Prussia from the rest of Germany. We must reclaim Danzig and secure a land connection.",
            "time": 70,
            "prerequisites": ["fate_czechoslovakia"],
            "mutually_exclusive": [],
            "effects": {
                "war_goal": "poland",
                "war_support": 10,
                "world_tension": 25,
            },
            "position": [1, 5],
        },
        "four_year_plan": {
            "title": "Four Year Plan",
            "description": "Implement the Four Year Plan to rapidly build up our industrial capacity for war.",
            "time": 70,
            "prerequisites": ["rhineland"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 4,
                "military_factories": 3,
                "production_efficiency": 10,
                "research_slots": 1,
            },
            "position": [2, 1],
        },
        "autarky": {
            "title": "Autarky",
            "description": "Implement policies to make Germany more self-sufficient in resources.",
            "time": 70,
            "prerequisites": ["four_year_plan"],
            "mutually_exclusive": [],
            "effects": {
                "resources": {
                    "steel": 10,
                    "oil": 5,
                    "aluminum": 5,
                },
                "stability": 5,
            },
            "position": [2, 2],
        },
        "westwall": {
            "title": "Westwall",
            "description": "Construct fortifications along our western border to protect against French aggression.",
            "time": 70,
            "prerequisites": ["four_year_plan"],
            "mutually_exclusive": [],
            "effects": {
                "fortification_west": 3,
                "construction_speed": 10,
            },
            "position": [3, 1],
        },
        "hermann_goring_werke": {
            "title": "Hermann Göring Werke",
            "description": "Establish the Hermann Göring Werke to boost our steel production.",
            "time": 70,
            "prerequisites": ["autarky"],
            "mutually_exclusive": [],
            "effects": {
                "resources": {
                    "steel": 20,
                    "aluminum": 10,
                },
                "production_efficiency": 5,
            },
            "position": [2, 3],
        },
        "kdf_wagen": {
            "title": "KdF-Wagen",
            "description": "Fund the development of the people's car, boosting civilian industry and infrastructure.",
            "time": 70,
            "prerequisites": ["autarky"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 3,
                "infrastructure": 1,
                "stability": 5,
            },
            "position": [2, 4],
        },
        "air_innovation": {
            "title": "Air Innovation",
            "description": "Invest in developing advanced aircraft technologies.",
            "time": 70,
            "prerequisites": ["four_year_plan"],
            "mutually_exclusive": [],
            "effects": {
                "research_bonus": {
                    "air_doctrine": 10,
                    "fighter": 10,
                    "bomber": 10,
                },
                "air_experience": 25,
            },
            "position": [3, 2],
        },
        "panzer_divisions": {
            "title": "Panzer Divisions",
            "description": "Develop and expand our armored forces for modern mobile warfare.",
            "time": 70,
            "prerequisites": ["four_year_plan"],
            "mutually_exclusive": [],
            "effects": {
                "army_experience": 25,
                "research_bonus": {
                    "armor": 15,
                    "motorized_equipment": 10,
                },
            },
            "position": [3, 3],
        },
        "u_boat_effort": {
            "title": "U-Boat Effort",
            "description": "Expand our submarine fleet to challenge British naval dominance.",
            "time": 70,
            "prerequisites": ["four_year_plan"],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 3,
                "research_bonus": {
                    "submarine_tech": 15,
                },
                "navy_experience": 25,
            },
            "position": [3, 4],
        },
        "molotov_ribbentrop_pact": {
            "title": "Molotov-Ribbentrop Pact",
            "description": "Negotiate a non-aggression pact with the Soviet Union to secure our eastern border while we deal with the West.",
            "time": 70,
            "prerequisites": ["danzig_or_war"],
            "mutually_exclusive": ["anti_comintern_pact"],
            "effects": {
                "non_aggression": "ussr",
                "diplomacy": 100,
                "world_tension": -10,
            },
            "position": [4, 5],
        },
        "anti_comintern_pact": {
            "title": "Anti-Comintern Pact",
            "description": "Form an alliance against the spread of communism, strengthening ties with other fascist nations.",
            "time": 70,
            "prerequisites": ["danzig_or_war"],
            "mutually_exclusive": ["molotov_ribbentrop_pact"],
            "effects": {
                "diplomacy": {
                    "italy": 50,
                    "japan": 50,
                },
                "stability": 5,
                "war_support": 5,
            },
            "position": [5, 5],
        },
    },
    # Other focus trees would be defined similarly

    "nationalist_china_focus_tree": {
        "resist_japan": {
            "title": "Resist Japanese Aggression",
            "description": "We must organize our forces to resist the Japanese invasion and protect Chinese sovereignty.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 20,
                "military_factories": 1,
            },
            "position": [1, 1],
        },
        "chinese_nationalism": {
            "title": "Chinese Nationalism",
            "description": "Foster a strong national identity based on Han Chinese traditions and rejection of foreign influences.",
            "time": 70,
            "prerequisites": ["resist_japan"],
            "mutually_exclusive": ["democratic_path"],
            "effects": {
                "government": "Fascist",
                "war_support": 15,
                "stability": 10,
            },
            "position": [0, 2],
        },
        "democratic_path": {
            "title": "Democratic Path",
            "description": "Implement Sun Yat-sen's vision of a democratic China with constitutional government.",
            "time": 70,
            "prerequisites": ["resist_japan"],
            "mutually_exclusive": ["chinese_nationalism"],
            "effects": {
                "government": "Democratic",
                "stability": 15,
                "political_power": 50,
            },
            "position": [2, 2],
        },
        "reclaim_lost_territories": {
            "title": "Reclaim Lost Territories",
            "description": "China must reclaim all territories historically part of the Chinese empire.",
            "time": 70,
            "prerequisites": ["chinese_nationalism"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 20,
                "claims": ["tibet", "mongolia", "korea"],
            },
            "position": [0, 3],
        },
        "modernize_military": {
            "title": "Military Modernization",
            "description": "Our army needs modern equipment and training to effectively combat Japanese forces.",
            "time": 70,
            "prerequisites": ["resist_japan"],
            "mutually_exclusive": [],
            "effects": {
                "army_experience": 50,
                "infantry_equipment": 10000,
                "artillery": 200,
            },
            "position": [1, 2],
        },
        "german_advisors": {
            "title": "German Military Advisors",
            "description": "German officers can provide valuable expertise to help modernize our forces.",
            "time": 70,
            "prerequisites": ["modernize_military"],
            "mutually_exclusive": ["american_aid_program"],
            "effects": {
                "relation_bonus": {
                    "germany": 30,
                },
                "tanks": 50,
                "army_experience": 30,
            },
            "position": [0, 3],
        },
        "american_aid_program": {
            "title": "American Aid Program",
            "description": "Seek military and economic assistance from the United States.",
            "time": 70,
            "prerequisites": ["modernize_military"],
            "mutually_exclusive": ["german_advisors"],
            "effects": {
                "relation_bonus": {
                    "usa": 30,
                },
                "civilian_factories": 2,
                "fighters": 30,
            },
            "position": [2, 3],
        },
        "industrial_relocation": {
            "title": "Industrial Relocation",
            "description": "Move our industries inland to protect them from Japanese bombing and invasion.",
            "time": 70,
            "prerequisites": ["resist_japan"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "military_factories": 1,
                "infrastructure": -1,
            },
            "position": [1, 3],
        },
        "anti_communist_campaign": {
            "title": "Anti-Communist Campaign",
            "description": "Focus on eliminating the Communist threat to ensure national unity against Japan.",
            "time": 70,
            "prerequisites": ["modernize_military"],
            "mutually_exclusive": ["united_front"],
            "effects": {
                "stability": -5,
                "war_support": 10,
                "war_with": ["communist_china"],
            },
            "position": [0, 4],
        },
        "united_front": {
            "title": "Second United Front",
            "description": "Form a temporary alliance with the Communists to focus on fighting Japan.",
            "time": 70,
            "prerequisites": ["modernize_military"],
            "mutually_exclusive": ["anti_communist_campaign"],
            "effects": {
                "stability": 10,
                "war_support": 15,
                "alliance_with": ["communist_china"],
            },
            "position": [2, 4],
        },
        "constitutional_reforms": {
            "title": "Constitutional Reforms",
            "description": "Implement democratic reforms to gain greater support from Western powers.",
            "time": 70,
            "prerequisites": ["american_aid_program"],
            "mutually_exclusive": [],
            "effects": {
                "government": "Democratic",
                "stability": 15,
                "relation_bonus": {
                    "usa": 20,
                    "uk": 20,
                },
            },
            "position": [2, 5],
        },
        "sino_japanese_cooperation": {
            "title": "Sino-Japanese Cooperation",
            "description": "Negotiate with Japan to end the conflict and join the Greater East Asia Co-Prosperity Sphere.",
            "time": 70,
            "prerequisites": ["german_advisors"],
            "mutually_exclusive": ["fight_to_the_end"],
            "effects": {
                "stability": 10,
                "peace_with": ["japan"],
                "alliance_with": ["japan"],
                "relation_bonus": {
                    "japan": 50,
                },
            },
            "position": [0, 5],
        },
        "fight_to_the_end": {
            "title": "Fight to the Last Man",
            "description": "We will never surrender to Japanese aggression no matter the cost.",
            "time": 70,
            "prerequisites": ["industrial_relocation"],
            "mutually_exclusive": ["sino_japanese_cooperation"],
            "effects": {
                "war_support": 25,
                "stability": -5,
                "resistance_strength": 20,
            },
            "position": [1, 5],
        },
        "asian_leadership": {
            "title": "Chinese Leadership in Asia",
            "description": "Position China as the natural leader of Asian peoples against Western imperialism.",
            "time": 70,
            "prerequisites": ["sino_japanese_cooperation"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "political_power": 100,
                "relation_bonus": {
                    "thailand": 30,
                    "philippines": 30,
                },
            },
            "position": [0, 6],
        },
    },

    "communist_china_focus_tree": {
        "guerrilla_warfare": {
            "title": "Guerrilla Warfare Doctrine",
            "description": "Develop our unique guerrilla warfare tactics to fight larger, better-equipped enemies.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "army_experience": 40,
                "infantry_equipment": 5000,
            },
            "position": [1, 1],
        },
        "permanent_revolution": {
            "title": "Permanent Revolution",
            "description": "The revolution must not stop at China's borders but spread throughout Asia and beyond.",
            "time": 70,
            "prerequisites": ["peoples_war"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 15,
                "stability": 5,
                "political_power": 50,
            },
            "position": [0, 6],
        },
        "asian_communism": {
            "title": "Asian Communist Federation",
            "description": "Create a new communist alliance of Asian nations independent from Moscow's control.",
            "time": 70,
            "prerequisites": ["permanent_revolution"],
            "mutually_exclusive": [],
            "effects": {
                "create_faction": "asian_communist_federation",
                "claims": ["thailand", "malaya", "netherlands_east_indies"],
            },
            "position": [0, 7],
        },
        "mass_mobilization": {
            "title": "Mass Mobilization",
            "description": "Mobilize the peasants and workers for our revolutionary cause.",
            "time": 70,
            "prerequisites": ["guerrilla_warfare"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "war_support": 15,
                "infantry_equipment": 5000,
            },
            "position": [1, 2],
        },
        "soviet_advisors": {
            "title": "Soviet Advisors",
            "description": "Request advisors and aid from the Soviet Union.",
            "time": 70,
            "prerequisites": ["mass_mobilization"],
            "mutually_exclusive": ["self_reliance"],
            "effects": {
                "relation_bonus": {
                    "ussr": 50,
                },
                "military_factories": 1,
                "artillery": 100,
            },
            "position": [0, 3],
        },
        "self_reliance": {
            "title": "Self-Reliance",
            "description": "Develop our own path to revolution without depending on foreign support.",
            "time": 70,
            "prerequisites": ["mass_mobilization"],
            "mutually_exclusive": ["soviet_advisors"],
            "effects": {
                "stability": 15,
                "civilian_factories": 1,
                "political_power": 100,
            },
            "position": [2, 3],
        },
        "peoples_war": {
            "title": "People's War",
            "description": "Our revolutionary war must be fought by and for the people, with politics commanding the gun.",
            "time": 70,
            "prerequisites": ["mass_mobilization"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 20,
                "stability": 10,
                "army_experience": 30,
            },
            "position": [1, 3],
        },
        "anti_japanese_resistance": {
            "title": "Anti-Japanese Resistance",
            "description": "Focus our efforts on fighting the Japanese invaders to gain popular support.",
            "time": 70,
            "prerequisites": ["peoples_war"],
            "mutually_exclusive": ["defeat_nationalists"],
            "effects": {
                "war_support": 15,
                "relation_bonus": {
                    "nationalist_china": 20,
                },
                "alliance_with": ["nationalist_china"],
            },
            "position": [0, 4],
        },
        "defeat_nationalists": {
            "title": "Defeat the Nationalists",
            "description": "Our primary goal must be defeating Chiang Kai-shek and his reactionary forces.",
            "time": 70,
            "prerequisites": ["peoples_war"],
            "mutually_exclusive": ["anti_japanese_resistance"],
            "effects": {
                "war_support": 10,
                "army_experience": 20,
                "war_with": ["nationalist_china"],
            },
            "position": [2, 4],
        },
        "land_reform": {
            "title": "Land Reform",
            "description": "Redistribute land from landlords to peasants to build support in rural areas.",
            "time": 70,
            "prerequisites": ["peoples_war"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 15,
                "political_power": 50,
                "infrastructure": 1,
            },
            "position": [1, 4],
        },
        "socialist_industrialization": {
            "title": "Socialist Industrialization",
            "description": "Begin building a modern industrial base with Soviet assistance.",
            "time": 70,
            "prerequisites": ["soviet_advisors"],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 2,
                "military_factories": 1,
                "relation_bonus": {
                    "ussr": 20,
                },
            },
            "position": [0, 5],
        },
        "chinese_characteristics": {
            "title": "Socialism with Chinese Characteristics",
            "description": "Adapt Marxist-Leninist principles to Chinese conditions and develop our own revolutionary theory.",
            "time": 70,
            "prerequisites": ["self_reliance"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 20,
                "political_power": 100,
                "relation_bonus": {
                    "ussr": -10,
                },
            },
            "position": [2, 5],
        },
        "liberated_areas": {
            "title": "Expand Liberated Areas",
            "description": "Establish revolutionary base areas to implement our policies and build popular support.",
            "time": 70,
            "prerequisites": ["land_reform"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "war_support": 10,
                "infantry_equipment": 5000,
            },
            "position": [1, 5],
        },
    },

    "thailand_focus_tree": {
        "domestic_development": {
            "title": "Domestic Development",
            "description": "Invest in our infrastructure and industry to strengthen the economy.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "civilian_factories": 1,
                "infrastructure": 1,
            },
            "position": [1, 1],
        },
        "military_government": {
            "title": "Military Government",
            "description": "Strengthen the role of the military in Thai politics and society.",
            "time": 70,
            "prerequisites": ["domestic_development"],
            "mutually_exclusive": ["democratic_reforms"],
            "effects": {
                "government": "Military",
                "stability": 5,
                "war_support": 10,
            },
            "position": [0, 2],
        },
        "democratic_reforms": {
            "title": "Democratic Reforms",
            "description": "Implement political reforms to create a constitutional monarchy with democratic institutions.",
            "time": 70,
            "prerequisites": ["domestic_development"],
            "mutually_exclusive": ["military_government"],
            "effects": {
                "government": "Democratic",
                "stability": 10,
                "political_power": 50,
            },
            "position": [2, 2],
        },
        "greater_thailand": {
            "title": "Greater Thailand",
            "description": "Reclaim territories that were historically part of the Thai kingdom but lost to colonial powers.",
            "time": 70,
            "prerequisites": ["military_government"],
            "mutually_exclusive": [],
            "effects": {
                "war_support": 15,
                "claims": ["french_indochina", "burma", "malaya"],
            },
            "position": [0, 3],
        },
        "military_supremacy": {
            "title": "Military Supremacy",
            "description": "Build the strongest military force in Southeast Asia to support our territorial ambitions.",
            "time": 70,
            "prerequisites": ["greater_thailand"],
            "mutually_exclusive": [],
            "effects": {
                "military_factories": 2,
                "army_experience": 30,
                "infantry_equipment": 10000,
            },
            "position": [0, 4],
        },
    },

    "philippines_focus_tree": {
        "commonwealth_status": {
            "title": "Commonwealth Status",
            "description": "Work within the framework of the Philippine Commonwealth to prepare for independence.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "political_power": 50,
            },
            "position": [1, 1],
        },
        "us_military_assistance": {
            "title": "US Military Assistance",
            "description": "Request increased military aid from the United States to strengthen our defenses.",
            "time": 70,
            "prerequisites": ["commonwealth_status"],
            "mutually_exclusive": ["independent_defense"],
            "effects": {
                "infantry_equipment": 5000,
                "fighters": 20,
                "relation_bonus": {
                    "usa": 30,
                },
            },
            "position": [0, 2],
        },
        "independent_defense": {
            "title": "Independent Defense",
            "description": "Develop our own military capabilities without relying on foreign assistance.",
            "time": 70,
            "prerequisites": ["commonwealth_status"],
            "mutually_exclusive": ["us_military_assistance"],
            "effects": {
                "military_factories": 1,
                "dockyards": 1,
                "war_support": 10,
            },
            "position": [2, 2],
        },
        "philippine_nationalism": {
            "title": "Philippine Nationalism",
            "description": "Foster a strong national identity and aim for a leading role in Southeast Asia.",
            "time": 70,
            "prerequisites": ["independent_defense"],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "war_support": 15,
                "government": "Military",
            },
            "position": [2, 3],
        },
        "pacific_security": {
            "title": "Pacific Security Zone",
            "description": "Establish Philippines as a regional security power in the western Pacific.",
            "time": 70,
            "prerequisites": ["philippine_nationalism"],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 1,
                "ships": {
                    "destroyers": 3,
                    "cruisers": 1,
                },
                "claims": ["malaya", "netherlands_east_indies"],
            },
            "position": [2, 4],
        },
    },

    "east_indies_focus_tree": {
        "colonial_administration": {
            "title": "Colonial Administration",
            "description": "Improve the efficiency of the colonial administration to better exploit resources.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 5,
                "political_power": 30,
            },
            "position": [1, 1],
        },
        "dutch_loyalism": {
            "title": "Dutch Loyalism",
            "description": "Strengthen ties with the Netherlands and remain a loyal colony.",
            "time": 70,
            "prerequisites": ["colonial_administration"],
            "mutually_exclusive": ["independence_movement"],
            "effects": {
                "stability": 10,
                "relation_bonus": {
                    "netherlands": 50,
                },
                "alliance_with": ["netherlands"],
            },
            "position": [0, 2],
        },
        "independence_movement": {
            "title": "Independence Movement",
            "description": "Support growing nationalist movements seeking independence from Dutch rule.",
            "time": 70,
            "prerequisites": ["colonial_administration"],
            "mutually_exclusive": ["dutch_loyalism"],
            "effects": {
                "stability": -5,
                "war_support": 15,
                "political_power": 50,
            },
            "position": [2, 2],
        },
        "resource_dominance": {
            "title": "Resource Dominance",
            "description": "Exploit our vast natural resources to build economic and political power.",
            "time": 70,
            "prerequisites": ["independence_movement"],
            "mutually_exclusive": [],
            "effects": {
                "resources": {
                    "oil": 15,
                    "rubber": 20,
                },
                "civilian_factories": 2,
            },
            "position": [2, 3],
        },
        "naval_supremacy": {
            "title": "Naval Supremacy",
            "description": "Build a powerful navy to control the waters of the Indonesian archipelago.",
            "time": 70,
            "prerequisites": ["resource_dominance"],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 2,
                "ships": {
                    "destroyers": 5,
                    "cruisers": 2,
                    "submarines": 5,
                },
                "claims": ["malaya", "philippines"],
            },
            "position": [2, 4],
        },
    },

    "australia_focus_tree": {
        "imperial_ties": {
            "title": "Imperial Ties",
            "description": "Strengthen our relationship with the British Empire and contribute to the war effort.",
            "time": 70,
            "prerequisites": [],
            "mutually_exclusive": [],
            "effects": {
                "stability": 10,
                "war_support": 10,
                "relation_bonus": {
                    "uk": 30,
                },
            },
            "position": [1, 1],
        },
        "expeditionary_forces": {
            "title": "Expeditionary Forces",
            "description": "Send Australian troops to fight alongside British forces in Europe and North Africa.",
            "time": 70,
            "prerequisites": ["imperial_ties"],
            "mutually_exclusive": ["home_defense"],
            "effects": {
                "war_support": 15,
                "relation_bonus": {
                    "uk": 20,
                },
                "infantry_equipment": 5000,
            },
            "position": [0, 2],
        },
        "home_defense": {
            "title": "Home Defense",
            "description": "Focus on defending Australia against potential Japanese aggression in the Pacific.",
            "time": 70,
            "prerequisites": ["imperial_ties"],
            "mutually_exclusive": ["expeditionary_forces"],
            "effects": {
                "military_factories": 1,
                "infantry_equipment": 10000,
                "fighters": 30,
            },
            "position": [2, 2],
        },
        "australian_imperialism": {
            "title": "Australian Imperialism",
            "description": "Establish Australia as an independent power with its own sphere of influence in the Pacific.",
            "time": 70,
            "prerequisites": ["home_defense"],
            "mutually_exclusive": [],
            "effects": {
                "government": "Military",
                "war_support": 15,
                "stability": 5,
            },
            "position": [2, 3],
        },
        "pacific_strategy": {
            "title": "Pacific Strategy",
            "description": "Develop a comprehensive strategy to control key territories in the South Pacific.",
            "time": 70,
            "prerequisites": ["australian_imperialism"],
            "mutually_exclusive": [],
            "effects": {
                "dockyards": 2,
                "ships": {
                    "cruisers": 2,
                    "destroyers": 4,
                },
                "claims": ["netherlands_east_indies", "new_guinea"],
            },
            "position": [2, 4],
        },
    }
}

# Building types for construction
BUILDINGS = {
    "civilian_factory": {
        "name": "Civilian Factory",
        "description": "Produces consumer goods and contributes to construction efforts",
        "cost": 3600,  # Construction time in "days"
        "resource_cost": {
            "steel": 100,
        },
        "tech_requirement": None,
        "effects": {
            "consumer_goods": 2,
            "construction_speed": 0.2,
        }
    },
    "military_factory": {
        "name": "Military Factory",
        "description": "Produces military equipment including tanks, artillery, and infantry equipment",
        "cost": 3600,
        "resource_cost": {
            "steel": 120,
        },
        "tech_requirement": None,
        "effects": {
            "production_capacity": 2,
        }
    },
    "dockyard": {
        "name": "Naval Dockyard",
        "description": "Constructs and repairs naval vessels",
        "cost": 4200,
        "resource_cost": {
            "steel": 150,
        },
        "tech_requirement": None,
        "effects": {
            "naval_production": 1,
        }
    },
    "infrastructure": {
        "name": "Infrastructure",
        "description": "Improves resource extraction and construction speed",
        "cost": 2400,
        "resource_cost": {
            "steel": 50,
        },
        "tech_requirement": None,
        "effects": {
            "resource_extraction": 0.1,
            "supply_capacity": 1,
            "construction_speed": 0.05,
        }
    },
    "air_base": {
        "name": "Air Base",
        "description": "Allows deployment and operation of aircraft",
        "cost": 3000,
        "resource_cost": {
            "steel": 100,
            "oil": 50,
        },
        "tech_requirement": None,
        "effects": {
            "air_capacity": 50,
        }
    },
    "radar_station": {
        "name": "Radar Station",
        "description": "Provides intelligence and early warning of enemy aircraft",
        "cost": 2100,
        "resource_cost": {
            "steel": 40,
            "aluminum": 20,
        },
        "tech_requirement": "basic_electronics",
        "effects": {
            "detection_range": 3,
            "intel_gathering": 0.1,
        }
    },
    "anti_air": {
        "name": "Anti-Air Defense",
        "description": "Provides protection against enemy air attacks",
        "cost": 1800,
        "resource_cost": {
            "steel": 60,
        },
        "tech_requirement": None,
        "effects": {
            "air_defense": 1,
        }
    },
    "coastal_bunker": {
        "name": "Coastal Bunker",
        "description": "Provides defense against naval invasions",
        "cost": 2400,
        "resource_cost": {
            "steel": 80,
        },
        "tech_requirement": None,
        "effects": {
            "naval_defense": 1.5,
        }
    },
    "nuclear_reactor": {
        "name": "Nuclear Reactor",
        "description": "Required for nuclear weapons research and production",
        "cost": 7200,
        "resource_cost": {
            "steel": 200,
            "aluminum": 100,
            "oil": 100,
        },
        "tech_requirement": "nuclear_reactor",
        "effects": {
            "nuclear_production": 1,
        }
    },
    "synthetic_refinery": {
        "name": "Synthetic Refinery",
        "description": "Converts coal into oil through synthetic production",
        "cost": 5400,
        "resource_cost": {
            "steel": 150,
        },
        "tech_requirement": "synthetic_oil",
        "effects": {
            "oil_production": 3,
        }
    },
}

# Research technologies
TECHNOLOGIES = {
    # Nuclear technologies
    "nuclear_physics": {
        "name": "Nuclear Physics",
        "category": "nuclear",
        "cost": 300,
        "year": 1940,
        "effects": {
            "enables": ["nuclear_research"],
        },
        "prerequisites": ["advanced_electronics"],
    },
    "nuclear_research": {
        "name": "Nuclear Research",
        "category": "nuclear",
        "cost": 350,
        "year": 1942,
        "effects": {
            "enables": ["atomic_bomb"],
            "construction_speed": {
                "nuclear_reactor": 0.15,
            },
        },
        "prerequisites": ["nuclear_physics"],
    },
    "atomic_bomb": {
        "name": "Atomic Bomb",
        "category": "nuclear",
        "cost": 500,
        "year": 1945,
        "effects": {
            "enables_weapon": "nuclear_weapon",
        },
        "prerequisites": ["nuclear_research"],
    },
    "nuclear_reactor": {
        "name": "Nuclear Reactor",
        "category": "nuclear",
        "cost": 400,
        "year": 1944,
        "effects": {
            "energy_output": 20,
            "enables_building": "nuclear_reactor",
        },
        "prerequisites": ["nuclear_research"],
    },

    # Advanced electronics (prerequisite for nuclear research)
    "advanced_electronics": {
        "name": "Advanced Electronics",
        "category": "electronics",
        "cost": 200,
        "year": 1939,
        "effects": {
            "research_speed": 0.05,
            "radar_efficiency": 0.1,
        },
        "prerequisites": ["basic_electronics"],
    },
    "basic_electronics": {
        "name": "Basic Electronics",
        "category": "electronics",
        "cost": 150,
        "year": 1936,
        "effects": {
            "research_speed": 0.03,
            "radar_range": 1,
        },
        "prerequisites": [],
    },

    # Construction technologies
    "construction_tech_1": {
        "name": "Basic Construction Engineering",
        "category": "industry",
        "cost": 100,
        "year": 1936,
        "effects": {
            "construction_speed": 0.1,
            "repair_speed": 0.1,
        },
        "prerequisites": [],
    },
    "construction_tech_2": {
        "name": "Improved Construction Engineering",
        "category": "industry",
        "cost": 150,
        "year": 1938,
        "effects": {
            "construction_speed": 0.15,
            "repair_speed": 0.15,
        },
        "prerequisites": ["construction_tech_1"],
    },
    "construction_tech_3": {
        "name": "Advanced Construction Engineering",
        "category": "industry",
        "cost": 200,
        "year": 1940,
        "effects": {
            "construction_speed": 0.2,
            "repair_speed": 0.2,
        },
        "prerequisites": ["construction_tech_2"],
    },
    "construction_tech_4": {
        "name": "Modern Construction Engineering",
        "category": "industry",
        "cost": 250,
        "year": 1942,
        "effects": {
            "construction_speed": 0.25,
            "repair_speed": 0.25,
        },
        "prerequisites": ["construction_tech_3"],
    },

    # Industrial technologies
    "industrial_efficiency_1": {
        "name": "Industrial Efficiency I",
        "category": "industry",
        "cost": 120,
        "year": 1936,
        "effects": {
            "factory_output": 0.1,
            "resources_extraction": 0.05,
        },
        "prerequisites": [],
    },
    "industrial_efficiency_2": {
        "name": "Industrial Efficiency II",
        "category": "industry",
        "cost": 180,
        "year": 1938,
        "effects": {
            "factory_output": 0.15,
            "resources_extraction": 0.1,
        },
        "prerequisites": ["industrial_efficiency_1"],
    },
    "industrial_efficiency_3": {
        "name": "Industrial Efficiency III",
        "category": "industry",
        "cost": 240,
        "year": 1940,
        "effects": {
            "factory_output": 0.2,
            "resources_extraction": 0.15,
        },
        "prerequisites": ["industrial_efficiency_2"],
    },
    "industrial_efficiency_4": {
        "name": "Industrial Efficiency IV",
        "category": "industry",
        "cost": 300,
        "year": 1942,
        "effects": {
            "factory_output": 0.25,
            "resources_extraction": 0.2,
        },
        "prerequisites": ["industrial_efficiency_3"],
    },

    # Original infantry techs
    "infantry_equipment_1": {
        "name": "Improved Infantry Equipment",
        "category": "infantry",
        "cost": 100,
        "year": 1936,
        "effects": {
            "infantry_attack": 0.1,
            "infantry_defense": 0.1,
        },
        "prerequisites": [],
    },
    "infantry_equipment_2": {
        "name": "Advanced Infantry Equipment",
        "category": "infantry",
        "cost": 180,
        "year": 1939,
        "effects": {
            "infantry_attack": 0.15,
            "infantry_defense": 0.15,
        },
        "prerequisites": ["infantry_equipment_1"],
    },
    "artillery_1": {
        "name": "Improved Artillery",
        "category": "artillery",
        "cost": 120,
        "year": 1936,
        "effects": {
            "artillery_attack": 0.15,
            "artillery_defense": 0.05,
        },
        "prerequisites": [],
    },
    "support_equipment_1": {
        "name": "Support Equipment",
        "category": "support",
        "cost": 80,
        "year": 1936,
        "effects": {
            "support_equipment_efficiency": 0.1,
        },
        "prerequisites": [],
    },
    "mechanical_computing": {
        "name": "Mechanical Computing",
        "category": "electronics",
        "cost": 100,
        "year": 1936,
        "effects": {
            "research_speed": 0.05,
            "encryption": 1,
            "decryption": 1,
        },
        "prerequisites": [],
    },
    "radio": {
        "name": "Radio",
        "category": "electronics",
        "cost": 120,
        "year": 1936,
        "effects": {
            "initiative": 0.1,
            "communication": 0.1,
        },
        "prerequisites": [],
    },
    "basic_tank": {
        "name": "Basic Light Tank",
        "category": "armor",
        "cost": 150,
        "year": 1936,
        "effects": {
            "tank_attack": 0.1,
            "tank_defense": 0.1,
            "tank_speed": 0.1,
        },
        "prerequisites": [],
    },
    "improved_light_tank": {
        "name": "Improved Light Tank",
        "category": "armor",
        "cost": 180,
        "year": 1937,
        "effects": {
            "tank_attack": 0.15,
            "tank_defense": 0.15,
            "tank_speed": 0.15,
        },
        "prerequisites": ["basic_tank"],
    },
    "basic_medium_tank": {
        "name": "Basic Medium Tank",
        "category": "armor",
        "cost": 200,
        "year": 1939,
        "effects": {
            "tank_attack": 0.25,
            "tank_defense": 0.25,
            "tank_speed": -0.05,
        },
        "prerequisites": ["improved_light_tank"],
    },
    "fighter1": {
        "name": "Early Fighter",
        "category": "air",
        "cost": 150,
        "year": 1936,
        "effects": {
            "fighter_attack": 0.1,
            "fighter_defense": 0.1,
            "fighter_agility": 0.1,
        },
        "prerequisites": [],
    },
    "fighter2": {
        "name": "Improved Fighter",
        "category": "air",
        "cost": 180,
        "year": 1939,
        "effects": {
            "fighter_attack": 0.15,
            "fighter_defense": 0.15,
            "fighter_agility": 0.15,
        },
        "prerequisites": ["fighter1"],
    },
    "cas1": {
        "name": "Close Air Support Aircraft",
        "category": "air",
        "cost": 150,
        "year": 1936,
        "effects": {
            "cas_ground_attack": 0.2,
        },
        "prerequisites": [],
    },
    "naval_bomber1": {
        "name": "Naval Bomber",
        "category": "air",
        "cost": 150,
        "year": 1936,
        "effects": {
            "naval_strike": 0.2,
        },
        "prerequisites": [],
    },
    "destroyer1": {
        "name": "Early Destroyer",
        "category": "naval",
        "cost": 140,
        "year": 1936,
        "effects": {
            "destroyer_attack": 0.1,
            "destroyer_defense": 0.1,
            "destroyer_anti_sub": 0.1,
        },
        "prerequisites": [],
    },
    "submarine1": {
        "name": "Early Submarine",
        "category": "naval",
        "cost": 140,
        "year": 1936,
        "effects": {
            "submarine_attack": 0.1,
            "submarine_defense": 0.1,
            "submarine_stealth": 0.1,
        },
        "prerequisites": [],
    },
    "cruiser1": {
        "name": "Early Cruiser",
        "category": "naval",
        "cost": 180,
        "year": 1936,
        "effects": {
            "cruiser_attack": 0.1,
            "cruiser_defense": 0.1,
        },
        "prerequisites": [],
    },
    "battleship1": {
        "name": "Early Battleship",
        "category": "naval",
        "cost": 200,
        "year": 1936,
        "effects": {
            "battleship_attack": 0.1,
            "battleship_defense": 0.1,
        },
        "prerequisites": [],
    },
    "construction1": {
        "name": "Construction I",
        "category": "industry",
        "cost": 120,
        "year": 1936,
        "effects": {
            "production_speed_buildings_factor": 0.1,
            "production_speed_bunker_factor": 0.1,
        },
        "prerequisites": [],
    },
    "construction2": {
        "name": "Construction II",
        "category": "industry",
        "cost": 180,
        "year": 1937,
        "effects": {
            "production_speed_buildings_factor": 0.1,
            "production_speed_bunker_factor": 0.1,
        },
        "prerequisites": ["construction1"],
    },
    "excavation1": {
        "name": "Excavation I",
        "category": "industry",
        "cost": 120,
        "year": 1936,
        "effects": {
            "local_resources_factor": 0.1,
        },
        "prerequisites": [],
    },
    "steel_production1": {
        "name": "Steel Production I",
        "category": "industry",
        "cost": 140,
        "year": 1936,
        "effects": {
            "steel_production": 0.1,
        },
        "prerequisites": [],
    },
    "oil_production1": {
        "name": "Oil Production I",
        "category": "industry",
        "cost": 140,
        "year": 1936,
        "effects": {
            "oil_production": 0.1,
        },
        "prerequisites": [],
    },
    "synthetic_rubber": {
        "name": "Synthetic Rubber",
        "category": "industry",
        "cost": 200,
        "year": 1937,
        "effects": {
            "rubber_production": 0.2,
        },
        "prerequisites": [],
    },
    "synthetic_oil": {
        "name": "Synthetic Oil",
        "category": "industry",
        "cost": 200,
        "year": 1937,
        "effects": {
            "oil_production": 0.2,
        },
        "prerequisites": [],
    },
    "motorised_infantry": {
        "name": "Motorized Infantry",
        "category": "infantry",
        "cost": 160,
        "year": 1936,
        "effects": {
            "motorized_attack": 0.1,
            "motorized_defense": 0.1,
            "motorized_speed": 0.1,
        },
        "prerequisites": [],
    },
    "mechanised_infantry": {
        "name": "Mechanized Infantry",
        "category": "infantry",
        "cost": 200,
        "year": 1940,
        "effects": {
            "mechanized_attack": 0.15,
            "mechanized_defense": 0.2,
            "mechanized_speed": 0.05,
        },
        "prerequisites": ["motorised_infantry"],
    },
}

# Events
EVENTS = {
    "spanish_civil_war": {
        "title": "Spanish Civil War",
        "description": "Civil war has broken out in Spain between the Republican government and Nationalist rebels led by Francisco Franco.",
        "trigger": {
            "year": 1936,
            "month": 7,
        },
        "options": {
            "send_volunteers_nationalists": {
                "text": "Send volunteers to the Nationalists",
                "effects": {
                    "war_support": 5,
                    "army_experience": 20,
                    "world_tension": 5,
                    "relations": {
                        "italy": 10,
                        "france": -10,
                        "uk": -10,
                    },
                },
            },
            "send_volunteers_republicans": {
                "text": "Send volunteers to the Republicans",
                "effects": {
                    "war_support": 5,
                    "army_experience": 20,
                    "world_tension": 5,
                    "relations": {
                        "ussr": 10,
                        "france": 5,
                        "italy": -10,
                    },
                },
                "requires_government": "Communist",
            },
            "non_intervention": {
                "text": "Maintain a policy of non-intervention",
                "effects": {
                    "stability": 5,
                    "world_tension": -2,
                },
            },
        },
    },
    "marco_polo_bridge": {
        "title": "Marco Polo Bridge Incident",
        "description": "Japanese and Chinese forces have clashed at the Marco Polo Bridge near Beijing, potentially sparking a wider conflict in Asia.",
        "trigger": {
            "year": 1937,
            "month": 7,
        },
        "options": {
            "support_japan": {
                "text": "Express support for Japan",
                "effects": {
                    "relations": {
                        "japan": 10,
                        "china": -10,
                        "usa": -5,
                    },
                },
            },
            "support_china": {
                "text": "Express support for China",
                "effects": {
                    "relations": {
                        "china": 10,
                        "japan": -10,
                        "usa": 5,
                    },
                },
                "requires_government": "Democratic",
            },
            "stay_neutral": {
                "text": "Maintain neutrality in Asian affairs",
                "effects": {
                    "stability": 2,
                },
            },
        },
    },
    "anschluss_event": {
        "title": "Anschluss of Austria",
        "description": "Germany has annexed Austria into the Reich, uniting the German peoples.",
        "trigger": {
            "focus_completed": "anschluss",
        },
        "options": {
            "celebrate": {
                "text": "A great day for the German people!",
                "effects": {
                    "stability": 5,
                    "war_support": 5,
                },
            },
        },
    },
    "munich_agreement": {
        "title": "Munich Agreement",
        "description": "The leaders of Germany, France, Britain, and Italy have agreed to the German annexation of the Sudetenland from Czechoslovakia in the name of peace.",
        "trigger": {
            "focus_completed": "sudetenland",
        },
        "options": {
            "celebrate": {
                "text": "Peace in our time... for now.",
                "effects": {
                    "stability": 5,
                    "war_support": 5,
                    "world_tension": -5,
                },
            },
        },
    },
    "czechoslovakia_occupation": {
        "title": "Occupation of Czechoslovakia",
        "description": "German forces have occupied the remainder of Czechoslovakia, breaking the Munich Agreement.",
        "trigger": {
            "focus_completed": "fate_czechoslovakia",
        },
        "options": {
            "address_nation": {
                "text": "Address the nation about our security needs",
                "effects": {
                    "stability": -5,
                    "war_support": 10,
                    "world_tension": 20,
                },
            },
        },
    },
    "polish_ultimatum": {
        "title": "Ultimatum to Poland",
        "description": "We have delivered an ultimatum to Poland demanding the return of Danzig to the Reich.",
        "trigger": {
            "focus_completed": "danzig_or_war",
        },
        "options": {
            "prepare_for_war": {
                "text": "Prepare for possible war",
                "effects": {
                    "war_support": 15,
                    "world_tension": 15,
                },
            },
        },
    },
    "molotov_ribbentrop_signed": {
        "title": "Molotov-Ribbentrop Pact Signed",
        "description": "Germany and the Soviet Union have signed a non-aggression pact, including secret protocols dividing Eastern Europe into spheres of influence.",
        "trigger": {
            "focus_completed": "molotov_ribbentrop_pact",
        },
        "options": {
            "secure_eastern_front": {
                "text": "Our eastern frontier is now secure",
                "effects": {
                    "stability": 10,
                    "war_support": 10,
                    "world_tension": -5,
                },
            },
        },
    },
    "communist_uprising": {
        "title": "Communist Uprising",
        "description": "Communist revolutionaries have taken to the streets across Germany, demanding the overthrow of the current regime and the establishment of a workers' state.",
        "trigger": {
            "focus_completed": "communist_revolution",
        },
        "options": {
            "support_revolution": {
                "text": "Support the revolution and address the people",
                "effects": {
                    "stability": -10,
                    "war_support": 15,
                    "internal_conflicts": 2,
                },
            },
        },
    },
    "thälmann_speech": {
        "title": "Thälmann's Address to the Nation",
        "description": "Ernst Thälmann, the new leader of Communist Germany, has given a rousing speech promising a better future for the working class and condemning the fascist threat.",
        "trigger": {
            "focus_completed": "workers_paradise",
        },
        "options": {
            "embrace_future": {
                "text": "A new era for the German working class!",
                "effects": {
                    "stability": 15,
                    "war_support": 10,
                },
            },
        },
    },
    "kaiser_restoration": {
        "title": "Restoration of the Monarchy",
        "description": "In a grand ceremony at the Berlin City Palace, Wilhelm III has been crowned as the new Kaiser of a restored German Empire. The Hohenzollern dynasty once again rules Germany.",
        "trigger": {
            "focus_completed": "restore_kaiser",
        },
        "options": {
            "long_live_kaiser": {
                "text": "Long live the Kaiser!",
                "effects": {
                    "stability": 20,
                    "war_support": 5,
                    "world_tension": -5,
                },
            },
        },
    },
    "democratic_elections": {
        "title": "Democratic Elections in Germany",
        "description": "For the first time since the rise of the Nazi Party, Germany has held free and fair democratic elections. Konrad Adenauer has been elected as the new Chancellor.",
        "trigger": {
            "focus_completed": "democratic_reforms",
        },
        "options": {
            "celebrate_democracy": {
                "text": "Democracy has returned to Germany!",
                "effects": {
                    "stability": 15,
                    "war_support": -10,
                },
            },
        },
    },
    "european_community": {
        "title": "Formation of the European Economic Community",
        "description": "Germany, France, Belgium, the Netherlands, and Luxembourg have agreed to form a new economic community to promote trade and cooperation in Europe.",
        "trigger": {
            "focus_completed": "invite_europe",
        },
        "options": {
            "new_era": {
                "text": "A new era of European cooperation begins!",
                "effects": {
                    "stability": 10,
                    "civilian_factories": 2,
                    "world_tension": -10,
                },
            },
        },
    },
    "great_purge_aftermath": {
        "title": "Aftermath of the Great Purge",
        "description": "The purge of counter-revolutionary elements has been completed, but at great cost. Many officers and officials were executed, some innocent. Military readiness has been affected.",
        "trigger": {
            "focus_completed": "great_purge",
        },
        "options": {
            "necessary_evil": {
                "text": "It was a necessary evil for the security of the revolution",
                "effects": {
                    "stability": -5,
                    "war_support": -5,
                    "army": {
                        "divisions": -2,
                    },
                    "internal_conflicts": 1,
                },
            },
        },
    },
    "wehrmacht_conspiracy": {
        "title": "Wehrmacht Conspiracy Uncovered",
        "description": "A group of high-ranking Wehrmacht officers has been discovered plotting against the government. Their motivations vary from disgust with Nazi policy to fears about the direction of the war.",
        "trigger": {
            "year": 1938,
            "month": 9,
            "government": "Fascist",
        },
        "options": {
            "execute_plotters": {
                "text": "Execute the plotters and purge the officer corps",
                "effects": {
                    "stability": -10,
                    "war_support": -5,
                    "army": {
                        "divisions": -1,
                    },
                    "internal_conflicts": 1,
                },
            },
            "show_mercy": {
                "text": "Show mercy to demonstrate strength",
                "effects": {
                    "stability": 5,
                    "political_power": -50,
                },
            },
        },
    },
    "naval_rearmament": {
        "title": "Naval Rearmament Program",
        "description": "The expansion of the Kriegsmarine has begun in earnest, with new shipyards breaking ground and existing ones expanding production capacity.",
        "trigger": {
            "focus_completed": "naval_tradition",
        },
        "options": {
            "rule_waves": {
                "text": "Germany will rule the waves once more!",
                "effects": {
                    "dockyards": 2,
                    "stability": 5,
                    "world_tension": 5,
                },
            },
        },
    },
    "economic_crisis": {
        "title": "Economic Crisis",
        "description": "Despite our best efforts, the German economy has entered a severe downturn. Unemployment is rising, and factories are closing.",
        "trigger": {
            "year": 1938,
            "month": 3,
            "stability": 30,
            "random": 25,  # 25% chance of triggering if other conditions met
        },
        "options": {
            "austerity": {
                "text": "Implement austerity measures",
                "effects": {
                    "stability": -15,
                    "civilian_factories": -2,
                    "military_factories": -1,
                },
            },
            "stimulus": {
                "text": "Launch an economic stimulus program",
                "effects": {
                    "stability": 10,
                    "civilian_factories": 1,
                    "political_power": -100,
                },
            },
        },
    },
    "generals_revolt": {
        "title": "Generals' Revolt",
        "description": "A group of generals, alarmed by the direction of the country, have staged an armed revolt against the government!",
        "trigger": {
            "stability": 25,
            "war_support": 60,
            "random": 20,  # 20% chance of triggering if other conditions met
        },
        "options": {
            "crush_revolt": {
                "text": "Crush the revolt with all available forces",
                "effects": {
                    "stability": -10,
                    "war_support": -15,
                    "army": {
                        "divisions": -3,
                    },
                    "internal_conflicts": 2,
                },
            },
            "negotiate": {
                "text": "Attempt to negotiate with the rebels",
                "effects": {
                    "stability": -5,
                    "political_power": -150,
                    "internal_conflicts": 1,
                },
            },
        },
    },
    "nuclear_breakthrough": {
        "title": "Nuclear Research Breakthrough",
        "description": "Our scientists have made a significant breakthrough in nuclear research, bringing us closer to harnessing the power of the atom for military purposes.",
        "trigger": {
            "focus_completed": "nuclear_program",
            "year": 1943,
        },
        "options": {
            "accelerate_research": {
                "text": "Accelerate the program at all costs",
                "effects": {
                    "civilian_factories": -2,
                    "military_factories": -1,
                    "research_bonus": {
                        "nuclear_tech": 25,
                    },
                },
            },
            "steady_approach": {
                "text": "Maintain a steady, methodical approach",
                "effects": {
                    "research_bonus": {
                        "nuclear_tech": 10,
                    },
                },
            },
        },
    },
    "stalingrad": {
        "title": "Battle of Stalingrad",
        "description": "Our forces are engaged in a brutal battle for control of Stalingrad. The fighting is house-to-house, and casualties are mounting.",
        "trigger": {
            "year": 1942,
            "month": 9,
            "at_war_with": ["ussr"],
        },
        "options": {
            "commit_reserves": {
                "text": "Commit all available reserves to the battle",
                "effects": {
                    "war_support": -10,
                    "stability": -5,
                    "army": {
                        "manpower": -100000,
                    },
                },
            },
            "strategic_withdrawal": {
                "text": "Order a strategic withdrawal from the city",
                "effects": {
                    "war_support": -15,
                    "stability": -10,
                    "world_tension": 5,
                },
            },
        },
    },
}

# Utility functions
def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color=Fore.WHITE, end="\n"):
    """Print text with color."""
    print(f"{color}{text}{Style.RESET_ALL}", end=end)

def print_header(text):
    """Print a formatted header."""
    width = 60
    print()
    print_colored("═" * width, Fore.BLUE)
    print_colored(f"{text.center(width)}", Fore.YELLOW + Style.BRIGHT)
    print_colored("═" * width, Fore.BLUE)
    print()

def print_subheader(text):
    """Print a formatted subheader."""
    width = 50
    print()
    print_colored(f"╔{'═' * (width-2)}╗", Fore.CYAN)
    print_colored(f"║{text.center(width-2)}║", Fore.CYAN)
    print_colored(f"╚{'═' * (width-2)}╝", Fore.CYAN)

def print_menu_option(key, description, color=Fore.CYAN):
    """Print a menu option."""
    print_colored(f"  {key}. {description}", color)

def input_colored(prompt, color=Fore.YELLOW):
    """Get user input with a colored prompt."""
    return input(f"{color}{prompt}{Style.RESET_ALL}")

def print_message(message, message_type="info"):
    """Print a formatted message with appropriate color based on type."""
    colors = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
        "event": Fore.MAGENTA,
    }
    color = colors.get(message_type, Fore.WHITE)
    print_colored(f"\n► {message}", color)

    if message_type != "prompt":
        game_state["message_log"].append({
            "text": message,
            "type": message_type,
            "date": f"{game_state['year']}.{game_state['month']}"
        })

def wait_for_input(message="Press Enter to continue..."):
    """Wait for user input with a message."""
    input_colored(f"\n{message}", Fore.CYAN)

def format_number(number):
    """Format number with commas for thousands."""
    return f"{number:,}"

def save_game():
    """Save the current game state to a file."""
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    # Display save slots
    print_subheader("Save Game")

    save_files = []
    for i in range(1, MAX_SAVE_SLOTS + 1):
        save_path = os.path.join(SAVE_FOLDER, f"save_{i}.json")
        save_info = "Empty"

        if os.path.exists(save_path):
            try:
                with open(save_path, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                    save_time = save_data.get("save_time", "Unknown")
                    player_nation = save_data.get("player_nation", "Unknown")
                    game_date = f"{save_data.get('year', '????')}.{save_data.get('month', '??')}"
                    save_info = f"{player_nation} - {game_date} ({save_time})"
            except json.JSONDecodeError:
                save_info = "Corrupted Save"
            except FileNotFoundError:
                save_info = "File Not Found"
            except (IOError, OSError, PermissionError) as e:
                save_info = "Error: " + str(e)[:20] + "..."

        save_files.append(save_info)
        print_colored(f"  {i}. {save_info}", Fore.CYAN)

    print_colored("  0. Cancel", Fore.RED)

    # Get save slot choice
    while True:
        try:
            choice = int(input_colored("\nSelect save slot (0-5): ", Fore.YELLOW))
            if 0 <= choice <= MAX_SAVE_SLOTS:
                break
            print_colored("Invalid slot number. Please choose between 0 and 5.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return False

    # Save game
    save_path = os.path.join(SAVE_FOLDER, f"save_{choice}.json")

    # Add save time
    save_data = game_state.copy()
    save_data["save_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=4)
        print_message(f"Game saved to slot {choice}.", "success")
        return True
    except (IOError, OSError, PermissionError, KeyError, TypeError, ValueError) as e:
        print_message(f"Error saving game: {e}", "error")
        return False

def load_game():
    """Load a game state from a save file."""
    if not os.path.exists(SAVE_FOLDER):
        print_message("No save folder found.", "error")
        return False

    # Display save slots
    print_subheader("Load Game")

    save_files = []
    for i in range(1, MAX_SAVE_SLOTS + 1):
        save_path = os.path.join(SAVE_FOLDER, f"save_{i}.json")
        save_info = "Empty"

        if os.path.exists(save_path):
            try:
                with open(save_path, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                    save_time = save_data.get("save_time", "Unknown")
                    player_nation = save_data.get("player_nation", "Unknown")
                    game_date = f"{save_data.get('year', '????')}.{save_data.get('month', '??')}"
                    save_info = f"{player_nation} - {game_date} ({save_time})"
            except json.JSONDecodeError:
                save_info = "Corrupted Save"
            except FileNotFoundError:
                save_info = "File Not Found"
            except (IOError, OSError, PermissionError) as e:
                save_info = "Error: " + str(e)[:20] + "..."

        save_files.append(save_info)
        print_colored(f"  {i}. {save_info}", Fore.CYAN)

    print_colored("  0. Cancel", Fore.RED)

    # Get load slot choice
    while True:
        try:
            choice = int(input_colored("\nSelect save slot to load (0-5): ", Fore.YELLOW))
            if 0 <= choice <= MAX_SAVE_SLOTS:
                break
            print_colored("Invalid slot number. Please choose between 0 and 5.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return False

    # Load game
    save_path = os.path.join(SAVE_FOLDER, f"save_{choice}.json")

    if not os.path.exists(save_path):
        print_message("Save file does not exist.", "error")
        return False

    try:
        with open(save_path, 'r', encoding='utf-8') as f:
            save_data = json.load(f)

        # Update game state
        for key, value in save_data.items():
            game_state[key] = value

        print_message(f"Game loaded from slot {choice}.", "success")
        return True
    except (IOError, OSError, PermissionError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print_message(f"Error loading game: {e}", "error")
        return False


def check_events():
    """Check for and trigger events based on game state."""
    # First check all types of event triggers
    for event_key, event_data in EVENTS.items():
        trigger = event_data.get("trigger", {})

        # Skip if this event was already triggered
        if "triggered_events" in game_state and event_key in game_state["triggered_events"]:
            continue

        event_can_trigger = True

        # Check date trigger
        if "year" in trigger and "month" in trigger:
            if game_state["year"] != trigger["year"] or game_state["month"] != trigger["month"]:
                event_can_trigger = False

        # Check focus completion trigger
        if "focus_completed" in trigger:
            required_focus = trigger["focus_completed"]
            if "completed_focuses" not in game_state or required_focus not in game_state["completed_focuses"]:
                event_can_trigger = False

        # Check government type
        if "government" in trigger:
            required_government = trigger["government"]
            player_government = game_state["nations"][game_state["player_nation"]]["government"]
            if player_government != required_government:
                event_can_trigger = False

        # Check stability threshold
        if "stability" in trigger:
            required_stability = trigger["stability"]
            player_stability = game_state["nations"][game_state["player_nation"]]["stability"]
            if player_stability > required_stability:  # For crises, we trigger below threshold
                event_can_trigger = False

        # Check at war with specific nations
        if "at_war_with" in trigger:
            required_enemies = trigger["at_war_with"]
            current_wars = game_state.get("at_war_with", [])

            for enemy in required_enemies:
                if enemy not in current_wars:
                    event_can_trigger = False
                    break

        # Check random chance
        if "random" in trigger:
            chance = trigger["random"]
            if random.randint(1, 100) > chance:
                event_can_trigger = False

        # If all conditions are met, queue the event
        if event_can_trigger:
            # Queue event
            if "event_queue" not in game_state:
                game_state["event_queue"] = []
            game_state["event_queue"].append(event_key)

            # Mark event as triggered
            if "triggered_events" not in game_state:
                game_state["triggered_events"] = []
            game_state["triggered_events"].append(event_key)

    # Process event queue
    if "event_queue" in game_state and game_state["event_queue"]:
        event_key = game_state["event_queue"].pop(0)
        show_event(event_key)

def show_event(event_key):
    """Display an event and handle player choices."""
    event_data = EVENTS[event_key]

    clear_screen()
    print_header("Event")

    print_colored(f"{event_data['title']}", Fore.YELLOW + Style.BRIGHT)
    print()
    print_colored(f"{event_data['description']}")
    print()

    # Display options
    options = event_data.get("options", {})
    available_options = {}

    for option_key, option_data in options.items():
        # Check if option has government requirement
        if "requires_government" in option_data:
            required_govt = option_data["requires_government"]
            current_govt = game_state["nations"][game_state["player_nation"]]["government"]
            if required_govt != current_govt:
                continue  # Skip this option if government type doesn't match

        # Option is available
        available_options[option_key] = option_data
        print_colored(f"\n[{option_key}] {option_data['text']}", Fore.CYAN)

        # Show effects if available
        if "effects" in option_data:
            for effect_key, effect_value in option_data["effects"].items():
                if effect_key == "stability":
                    print_colored(f"  Stability: {'+' if effect_value > 0 else ''}{effect_value}%", Fore.GREEN if effect_value > 0 else Fore.RED)
                elif effect_key == "war_support":
                    print_colored(f"  War Support: {'+' if effect_value > 0 else ''}{effect_value}%", Fore.GREEN if effect_value > 0 else Fore.RED)
                elif effect_key == "world_tension":
                    print_colored(f"  World Tension: {'+' if effect_value > 0 else ''}{effect_value}%", Fore.RED if effect_value > 0 else Fore.GREEN)
                elif effect_key == "army_experience":
                    print_colored(f"  Army Experience: +{effect_value}", Fore.GREEN)
                elif effect_key == "relations":
                    for country, rel_change in effect_value.items():
                        print_colored(f"  Relations with {country.title()}: {'+' if rel_change > 0 else ''}{rel_change}", Fore.GREEN if rel_change > 0 else Fore.RED)
                elif effect_key == "internal_conflicts":
                    print_colored(f"  Internal Conflicts: {'+' if effect_value > 0 else ''}{effect_value}", Fore.RED if effect_value > 0 else Fore.GREEN)
                elif effect_key == "political_power":
                    print_colored(f"  Political Power: {'+' if effect_value > 0 else ''}{effect_value}", Fore.GREEN if effect_value > 0 else Fore.RED)
                elif effect_key == "army":
                    for army_key, army_val in effect_value.items():
                        print_colored(f"  Army {army_key.title()}: {'+' if army_val > 0 else ''}{army_val}", Fore.GREEN if army_val > 0 else Fore.RED)
                elif effect_key == "civilian_factories":
                    print_colored(f"  Civilian Factories: {'+' if effect_value > 0 else ''}{effect_value}", Fore.GREEN if effect_value > 0 else Fore.RED)
                elif effect_key == "military_factories":
                    print_colored(f"  Military Factories: {'+' if effect_value > 0 else ''}{effect_value}", Fore.GREEN if effect_value > 0 else Fore.RED)
                elif effect_key == "dockyards":
                    print_colored(f"  Dockyards: {'+' if effect_value > 0 else ''}{effect_value}", Fore.GREEN if effect_value > 0 else Fore.RED)
                elif effect_key == "research_bonus":
                    for tech, bonus in effect_value.items():
                        print_colored(f"  Research bonus for {tech.replace('_', ' ').title()}: +{bonus}%", Fore.GREEN)

    # Make sure there's at least one available option
    if not available_options:
        print_colored("\nNo available options for your current government type.", Fore.RED)
        available_options["continue"] = {"text": "Continue"}

    # Get player choice
    while True:
        choice = input_colored("\nChoose an option: ", Fore.YELLOW).strip().lower()

        if choice in available_options:
            option_data = available_options[choice]

            # Apply effects
            if "effects" in option_data:
                effects = option_data["effects"]
                nation = game_state["nations"][game_state["player_nation"]]

                for effect_key, effect_value in effects.items():
                    if effect_key == "stability":
                        nation["stability"] = min(100, max(0, nation["stability"] + effect_value))
                    elif effect_key == "war_support":
                        nation["war_support"] = min(100, max(0, nation["war_support"] + effect_value))
                    elif effect_key == "world_tension":
                        game_state["world_tension"] = game_state.get("world_tension", 0) + effect_value
                    elif effect_key == "army_experience":
                        # We'd handle army experience here
                        pass
                    elif effect_key == "internal_conflicts":
                        game_state["internal_conflicts"] = game_state.get("internal_conflicts", 0) + effect_value
                    elif effect_key == "political_power":
                        game_state["political_power"] = game_state.get("political_power", 0) + effect_value
                    elif effect_key == "relations":
                        if "diplomacy" not in game_state:
                            game_state["diplomacy"] = {"relations": {}}
                        if "relations" not in game_state["diplomacy"]:
                            game_state["diplomacy"]["relations"] = {}

                        for country, rel_change in effect_value.items():
                            if country not in game_state["diplomacy"]["relations"]:
                                game_state["diplomacy"]["relations"][country] = 0
                            game_state["diplomacy"]["relations"][country] += rel_change
                    elif effect_key == "army":
                        for army_key, army_val in effect_value.items():
                            if army_key == "divisions":
                                nation["army"]["divisions"] = max(0, nation["army"]["divisions"] + army_val)
                            elif army_key == "manpower":
                                nation["army"]["manpower"] = max(0, nation["army"]["manpower"] + army_val)
                    elif effect_key == "civilian_factories":
                        nation["industry"]["civilian_factories"] = max(0, nation["industry"]["civilian_factories"] + effect_value)
                    elif effect_key == "military_factories":
                        nation["industry"]["military_factories"] = max(0, nation["industry"]["military_factories"] + effect_value)
                    elif effect_key == "dockyards":
                        nation["industry"]["dockyards"] = max(0, nation["industry"]["dockyards"] + effect_value)
                    elif effect_key == "research_bonus":
                        # We'd handle research bonuses here
                        pass

            break
        print_colored("Invalid option. Please try again.", Fore.RED)

    # Add to message log
    option_text = available_options[choice].get("text", "Continue")
    print_message(f"Event: {event_data['title']} - {option_text}", "event")

def check_endings():
    """Check if any game endings have been achieved."""
    # Skip if we've already achieved an ending
    if game_state.get("achieved_ending") is not None:
        return

    # Check for nation-specific endings
    player_nation_key = game_state["player_nation"]

    player_nation = game_state["nations"][game_state["player_nation"]]

    for ending_key, ending_data in ENDINGS.items():
        requirements = ending_data["requirements"]
        ending_achieved = True

        # Check if this ending is for a specific nation
        if "nation" in requirements and player_nation_key != requirements["nation"]:
            ending_achieved = False

        # Check government type
        if "government" in requirements and player_nation["government"] != requirements["government"]:
            ending_achieved = False

        # Check stability
        if "stability" in requirements and player_nation["stability"] < requirements["stability"]:
            ending_achieved = False

        # Check not_at_war condition
        if "not_at_war" in requirements and requirements["not_at_war"]:
            if player_nation.get("at_war_with") and len(player_nation.get("at_war_with", [])) > 0:
                ending_achieved = False

        # Check war support
        if "war_support" in requirements and player_nation["war_support"] < requirements["war_support"]:
            ending_achieved = False

        # Check minimum year
        if "year_min" in requirements and game_state["year"] < requirements["year_min"]:
            ending_achieved = False

        # Check conquered nations
        if "conquered_nations" in requirements:
            conquered = game_state.get("conquered_nations", [])
            for nation in requirements["conquered_nations"]:
                if nation not in conquered:
                    ending_achieved = False
                    break

        # Check completed focuses
        if "focus_completed" in requirements:
            completed_focuses = game_state.get("completed_focuses", [])
            for focus in requirements["focus_completed"]:
                if focus not in completed_focuses:
                    ending_achieved = False
                    break

        # Check alliance with nations
        if "alliance_with" in requirements:
            alliances = player_nation.get("alliance_with", [])
            for ally in requirements["alliance_with"]:
                if ally not in alliances:
                    ending_achieved = False
                    break

        # Check territories not conquered
        if "not_conquered" in requirements:
            conquered = game_state.get("conquered_nations", [])
            for nation in requirements["not_conquered"]:
                if nation in conquered:
                    ending_achieved = False
                    break

        # Check if Germany has been conquered by specific nations
        if "conquered_by" in requirements:
            conquerors = game_state.get("conquered_by", [])
            required_conquerors = requirements["conquered_by"]
            for nation in required_conquerors:
                if nation not in conquerors:
                    ending_achieved = False
                    break

        # Check partial control of nations
        if "partial_control" in requirements:
            partially_controlled = game_state.get("partial_control", [])
            for nation in requirements["partial_control"]:
                if nation not in partially_controlled:
                    ending_achieved = False
                    break

        # Check faction membership
        if "in_faction_with" in requirements:
            required_members = requirements["in_faction_with"]
            if ("diplomacy" not in game_state or
                "player_faction" not in game_state["diplomacy"] or
                game_state["diplomacy"]["player_faction"] is None or
                "factions" not in game_state["diplomacy"]):
                ending_achieved = False
            else:
                faction = game_state["diplomacy"]["player_faction"]
                if faction in game_state["diplomacy"]["factions"]:
                    faction_members = game_state["diplomacy"]["factions"][faction]["members"]
                    for member in required_members:
                        if member not in faction_members:
                            ending_achieved = False
                            break
                else:
                    ending_achieved = False

        # Check faction size
        if "faction_members_count" in requirements:
            if ("diplomacy" not in game_state or
                "player_faction" not in game_state["diplomacy"] or
                game_state["diplomacy"]["player_faction"] is None or
                "factions" not in game_state["diplomacy"]):
                ending_achieved = False
            else:
                faction = game_state["diplomacy"]["player_faction"]
                if faction in game_state["diplomacy"]["factions"]:
                    faction_members = game_state["diplomacy"]["factions"][faction]["members"]
                    if len(faction_members) < requirements["faction_members_count"]:
                        ending_achieved = False
                else:
                    ending_achieved = False

        # Check internal conflicts
        if "internal_conflicts" in requirements and game_state.get("internal_conflicts", 0) < requirements["internal_conflicts"]:
            ending_achieved = False

        # Check completed focus
        if "completed_focus" in requirements and requirements["completed_focus"] not in game_state.get("completed_focuses", []):
            ending_achieved = False

        # Check if at war with specific nations
        if "at_war_with" in requirements:
            required_enemies = requirements["at_war_with"]
            current_wars = game_state.get("at_war_with", [])
            for enemy in required_enemies:
                if enemy not in current_wars:
                    ending_achieved = False
                    break

        # Check if at war in general
        if "at_war" in requirements and requirements["at_war"] != (len(game_state.get("at_war_with", [])) > 0):
            ending_achieved = False

        # Check world tension
        if "world_tension" in requirements and game_state.get("world_tension", 0) < requirements["world_tension"]:
            ending_achieved = False

        # Check factory count
        if "civilian_factories" in requirements:
            if player_nation["industry"]["civilian_factories"] > requirements["civilian_factories"]:
                ending_achieved = False

        if "military_factories" in requirements:
            if player_nation["industry"]["military_factories"] > requirements["military_factories"]:
                ending_achieved = False

        # If all requirements are met, trigger the ending
        if ending_achieved:
            game_state["achieved_ending"] = ending_key
            show_ending(ending_key)
            break

def show_ending(ending_key):
    """Display the ending screen for the achieved ending."""
    clear_screen()

    ending_data = ENDINGS[ending_key]
    ending_type = ending_data.get("type", "victory")  # Default to victory if type not specified

    # Set header and colors based on ending type
    if ending_type == "victory":
        header_text = "VICTORY ACHIEVED"
        title_color = Fore.YELLOW + Style.BRIGHT
        desc_color = Fore.CYAN
        header_color = Fore.GREEN
    elif ending_type == "disaster":
        header_text = "DISASTER ENDING"
        title_color = Fore.RED + Style.BRIGHT
        desc_color = Fore.LIGHTRED_EX
        header_color = Fore.RED
    elif ending_type == "special":
        header_text = "SPECIAL HISTORICAL OUTCOME"
        title_color = Fore.MAGENTA + Style.BRIGHT
        desc_color = Fore.LIGHTCYAN_EX
        header_color = Fore.BLUE
    else:
        header_text = "GAME ENDING ACHIEVED"
        title_color = Fore.YELLOW + Style.BRIGHT
        desc_color = Fore.CYAN
        header_color = Fore.BLUE

    # Display header
    print_colored("=" * 60, header_color)
    print_colored(header_text.center(60), header_color + Style.BRIGHT)
    print_colored("=" * 60, header_color)

    # Display ending name
    print_colored(f"\n{ending_data['name']}", title_color)
    print()

    # Display ending description
    for line in textwrap.wrap(ending_data['description'], width=70):
        print_colored(line, desc_color)

    print("\n" + "=" * 60 + "\n")

    # Show game stats
    player_nation = game_state["nations"][game_state["player_nation"]]
    print_colored("Final Stats:", Fore.YELLOW)
    print_colored(f"Nation: {player_nation['name']}", Fore.WHITE)
    print_colored(f"Government: {player_nation['government']}", Fore.WHITE)
    print_colored(f"Leader: {player_nation['leader']}", Fore.WHITE)
    print_colored(f"Year: {game_state['year']}.{game_state['month']}", Fore.WHITE)

    # Set color based on value
    stability_color = Fore.GREEN if player_nation["stability"] >= 70 else Fore.YELLOW if player_nation["stability"] >= 40 else Fore.RED
    war_support_color = Fore.GREEN if player_nation["war_support"] >= 70 else Fore.YELLOW if player_nation["war_support"] >= 40 else Fore.RED

    print_colored(f"Stability: {player_nation['stability']}%", stability_color)
    print_colored(f"War Support: {player_nation['war_support']}%", war_support_color)

    # Show economic stats
    print_colored("\nEconomy:", Fore.YELLOW)
    print_colored(f"Civilian Factories: {player_nation['industry']['civilian_factories']}", Fore.WHITE)
    print_colored(f"Military Factories: {player_nation['industry']['military_factories']}", Fore.WHITE)
    print_colored(f"Dockyards: {player_nation['industry']['dockyards']}", Fore.WHITE)

    # Show military stats
    print_colored("\nMilitary:", Fore.YELLOW)
    print_colored(f"Divisions: {player_nation['army']['divisions']}", Fore.WHITE)
    print_colored(f"Manpower: {format_number(player_nation['army']['manpower'])}", Fore.WHITE)
    print_colored(f"Aircraft: {player_nation['air_force']['fighters'] + player_nation['air_force']['bombers']}", Fore.WHITE)
    print_colored(f"Ships: {sum(player_nation['navy']['ships'].values())}", Fore.WHITE)

    # Show conquered territories
    if game_state.get("conquered_nations"):
        print_colored("\nConquered Nations:", Fore.YELLOW)
        for nation_key in game_state["conquered_nations"]:
            if nation_key in NATIONS:
                print_colored(f"- {NATIONS[nation_key]['name']}", Fore.WHITE)

    # Show faction
    if ("diplomacy" in game_state and
        "player_faction" in game_state["diplomacy"] and
        game_state["diplomacy"]["player_faction"] is not None and
        "factions" in game_state["diplomacy"]):

        faction_key = game_state["diplomacy"]["player_faction"]
        if faction_key in game_state["diplomacy"]["factions"]:
            faction = game_state["diplomacy"]["factions"][faction_key]
            print_colored(f"\nYour Faction: {faction['name']}", Fore.YELLOW)
            print_colored("Members:", Fore.WHITE)
            for member_key in faction["members"]:
                if member_key in NATIONS:
                    print_colored(f"- {NATIONS[member_key]['name']}", Fore.WHITE)

    # Custom messages based on ending type
    print("\n" + "=" * 60 + "\n")
    if ending_type == "victory":
        print_colored("CONGRATULATIONS!", Fore.GREEN + Style.BRIGHT)
        print_colored("Your leadership has guided Germany to a new era of greatness!", Fore.GREEN)
    elif ending_type == "disaster":
        print_colored("DEFEAT", Fore.RED + Style.BRIGHT)
        print_colored("Your leadership has ended in catastrophe for Germany...", Fore.RED)

    print_colored("\nThank you for playing Deutschland!", Fore.CYAN)
    print_colored("You can return to the main menu or exit the game.", Fore.CYAN)

    # Wait for input
    wait_for_input("\nPress Enter to return to the main menu...")

    # Return to main menu
    show_main_menu()

def advance_time():
    """Advance the game time by one month and process effects."""
    # Process focus - reduce focus days_left by 30 days (1 month)
    if game_state["focus_progress"] is not None:
        try:
            # Reduce focus time by one month (30 days)
            days_to_reduce = 30
            current_days_left = game_state["focus_progress"]["days_left"]
            game_state["focus_progress"]["days_left"] = max(0, current_days_left - days_to_reduce)

            # Check if focus is complete
            if game_state["focus_progress"]["days_left"] <= 0:
                focus_key = game_state["focus_progress"]["key"]
                print_message(f"National focus '{FOCUS_TREES[game_state['nations'][game_state['player_nation']]['focus_tree']][focus_key]['title']}' completed!", "success")

                # Apply effects
                focus_tree = game_state["nations"][game_state["player_nation"]]["focus_tree"]
                focus_data = FOCUS_TREES[focus_tree][focus_key]
                apply_focus_effects(focus_key, focus_data)

                # Record completed focus
                if "completed_focuses" not in game_state:
                    game_state["completed_focuses"] = []
                game_state["completed_focuses"].append(focus_key)

                # Clear focus progress
                game_state["focus_progress"] = None
        except (TypeError, KeyError):
            # If there's an error, reset focus progress
            game_state["focus_progress"] = None

    # Process ultimatums
    if "diplomacy" in game_state and "active_ultimatums" in game_state["diplomacy"]:
        process_ultimatums()

    # Process construction projects
    process_construction()

    # Check for rebellion in low-autonomy subject states
    if "diplomacy" in game_state and "subject_states" in game_state["diplomacy"]:
        rebelling_nations = []

        for nation_key, data in game_state["diplomacy"]["subject_states"].items():
            autonomy = data.get("autonomy", 50)

            # Very low autonomy has a chance to trigger rebellion
            if autonomy < 15:
                # Higher chance for lower autonomy
                rebellion_chance = (15 - autonomy) * 2

                if random.randint(1, 100) <= rebellion_chance:
                    rebelling_nations.append(nation_key)
                    add_message(f"Rebellion in {NATIONS[nation_key]['name']}!", "error")

                    # Remove from subject states
                    del game_state["diplomacy"]["subject_states"][nation_key]

                    # Set relations to very negative
                    game_state["diplomacy"]["relations"][nation_key] = -80

                    # Potentially trigger war
                    if "status" not in game_state:
                        game_state["status"] = {}

                    game_state["status"][nation_key] = {
                        "at_war": True,
                        "at_war_with": game_state["player_nation"]
                    }

                    # Increase world tension
                    if "world_tension" in game_state:
                        game_state["world_tension"] += 5

        if rebelling_nations:
            print_message("Rebellion has broken out in one or more of your subject states!", "error")

    # Check for events
    check_events()

    # Check for endings
    check_endings()

    # Advance time - must be done last to ensure ultimatums are processed correctly
    game_state["month"] += 1
    if game_state["month"] > 12:
        game_state["month"] = 1
        game_state["year"] += 1

        # Process any expired casus belli at year end
        if "diplomacy" in game_state and "casus_belli" in game_state["diplomacy"]:
            for from_nation, targets in list(game_state["diplomacy"]["casus_belli"].items()):
                for to_nation, data in list(targets.items()):
                    if data["expires"] <= game_state["year"]:
                        del game_state["diplomacy"]["casus_belli"][from_nation][to_nation]

                        # If player's casus belli expired, notify them
                        if from_nation == game_state["player_nation"]:
                            add_message(f"Casus belli against {NATIONS[to_nation]['name']} has expired", "warning")

def select_focus():
    """Display and handle the national focus selection."""
    player_nation = game_state["player_nation"]
    nation_data = game_state["nations"][player_nation]
    focus_tree_name = nation_data["focus_tree"]
    focus_tree = FOCUS_TREES[focus_tree_name]

    # Get completed focuses
    completed_focuses = game_state.get("completed_focuses", [])

    clear_screen()
    print_header("National Focus")

    # Display current focus if any
    if game_state["focus_progress"] is not None:
        try:
            focus = game_state["focus_progress"]
            # pylint: disable=unsupported-membership-test,unsubscriptable-object
            if isinstance(focus, dict) and "key" in focus and "days_left" in focus:
                focus_details = focus_tree[focus["key"]]
                print_colored(f"Current Focus: {focus_details['title']}", Fore.YELLOW)
                print_colored(f"Days Remaining: {focus['days_left']}", Fore.CYAN)
                print()
                print_colored("1. Cancel Focus", Fore.RED)
                print_colored("0. Back", Fore.CYAN)
            else:
                print_colored("Current Focus: Invalid focus data", Fore.RED)
                game_state["focus_progress"] = None
                print_colored("0. Back", Fore.CYAN)
        except (KeyError, TypeError):
            print_colored("Current Focus: Error retrieving focus data", Fore.RED)
            game_state["focus_progress"] = None
            print_colored("0. Back", Fore.CYAN)

        choice = input_colored("\nSelect an option: ", Fore.YELLOW)

        if choice == "1":
            game_state["focus_progress"] = None
            print_message("Focus canceled.", "info")

        return

    # Display available focuses
    available_focuses = []
    for focus_key, focus_data in focus_tree.items():
        # Check if focus is already completed
        if focus_key in completed_focuses:
            continue

        # Check prerequisites
        can_select = True
        for prereq in focus_data.get("prerequisites", []):
            if prereq not in completed_focuses:
                can_select = False
                break

        # Check mutually exclusive focuses
        for mutual in focus_data.get("mutually_exclusive", []):
            if mutual in completed_focuses:
                can_select = False
                break

        if can_select:
            available_focuses.append((focus_key, focus_data))

    if not available_focuses:
        print_colored("No focuses available to select.", Fore.YELLOW)
        wait_for_input()
        return

    # Display available focuses
    print_colored("Available Focuses:", Fore.YELLOW)
    for i, (focus_key, focus_data) in enumerate(available_focuses, 1):
        print_colored(f"{i}. {focus_data['title']} ({focus_data['time']} days)", Fore.CYAN)
        print_colored(f"   {focus_data['description']}", Fore.WHITE)
        print()

    print_colored("0. Back", Fore.RED)

    # Get player choice
    while True:
        try:
            choice = int(input_colored("\nSelect a focus: ", Fore.YELLOW))
            if 0 <= choice <= len(available_focuses):
                break
            else:
                print_colored("Invalid option. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return

    # Set selected focus
    focus_key, focus_data = available_focuses[choice - 1]
    game_state["focus_progress"] = {
        "key": focus_key,
        "days_left": focus_data["time"]
    }

    print_message(f"Selected focus: {focus_data['title']}", "success")

def select_research():
    """Display and handle technology research selection."""
    try:
        # Initialize research structure if needed
        if "research" not in game_state:
            game_state["research"] = {
                "current_research": [],
                "completed_research": [],
                "research_slots": 3,
            }

        # Validate research is a dict
        if not isinstance(game_state["research"], dict):
            game_state["research"] = {
                "current_research": [],
                "completed_research": [],
                "research_slots": 3,
            }

        clear_screen()
        print_header("Research")

        # Initialize current_research if it doesn't exist
        if "current_research" not in game_state["research"]:
            game_state["research"]["current_research"] = []

        # Initialize completed_research if it doesn't exist
        if "completed_research" not in game_state["research"]:
            game_state["research"]["completed_research"] = []

        # Ensure research_slots exists
        if "research_slots" not in game_state["research"]:
            game_state["research"]["research_slots"] = 3
    except (KeyError, TypeError) as e:
        # If any error occurs, reset the research structure
        print_message(f"Research system error: {str(e)}", "error")
        game_state["research"] = {
            "current_research": [],
            "completed_research": [],
            "research_slots": 3
        }

    # Display current research projects
    if game_state["research"]["current_research"]:
        print_colored("Current Research:", Fore.YELLOW)
        for i, research in enumerate(game_state["research"]["current_research"], 1):
            tech_data = TECHNOLOGIES[research["key"]]
            progress_pct = (research["progress"] / tech_data["cost"]) * 100
            print_colored(f"{i}. {tech_data['name']} - {progress_pct:.1f}% ({research['progress']}/{tech_data['cost']})", Fore.CYAN)
            print_colored(f"   Category: {tech_data['category'].title()}", Fore.WHITE)
            print()
    else:
        print_colored("No active research projects.", Fore.YELLOW)

    # Check if all research slots are filled
    if len(game_state["research"]["current_research"]) >= game_state["research"]["research_slots"]:
        print_colored(f"All {game_state['research']['research_slots']} research slots are in use.", Fore.RED)
        wait_for_input()
        return

    # Display available technologies
    available_techs = []
    completed_research = game_state["research"]["completed_research"]

    for tech_key, tech_data in TECHNOLOGIES.items():
        # Skip if already researched or currently researching
        if tech_key in completed_research:
            continue

        already_researching = False
        for research in game_state["research"]["current_research"]:
            if research["key"] == tech_key:
                already_researching = True
                break

        if already_researching:
            continue

        # Check prerequisites
        can_research = True
        for prereq in tech_data.get("prerequisites", []):
            if prereq not in completed_research:
                can_research = False
                break

        # Check if tech is ahead of time (simplified)
        ahead_of_time = game_state["year"] < tech_data["year"]

        if can_research:
            available_techs.append((tech_key, tech_data, ahead_of_time))

    if not available_techs:
        print_colored("No technologies available to research.", Fore.YELLOW)
        wait_for_input()
        return

    # Display available technologies
    print_colored("\nAvailable Technologies:", Fore.YELLOW)

    # Group by category
    categories = {}
    for tech_key, tech_data, ahead_of_time in available_techs:
        category = tech_data["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append((tech_key, tech_data, ahead_of_time))

    # Display by category
    option_counter = 1
    tech_options = []

    for category, techs in sorted(categories.items()):
        print_colored(f"\n{category.upper()}", Fore.YELLOW + Style.BRIGHT)

        for tech_key, tech_data, ahead_of_time in techs:
            cost_text = str(tech_data["cost"])
            if ahead_of_time:
                cost_text += f" (Ahead of time: {tech_data['year']})"

            print_colored(f"{option_counter}. {tech_data['name']} - {cost_text}",
                         Fore.RED if ahead_of_time else Fore.CYAN)

            # Display effects
            if "effects" in tech_data:
                for effect_key, effect_value in tech_data["effects"].items():
                    value_text = f"+{effect_value:.1%}" if isinstance(effect_value, float) else f"+{effect_value}"
                    print_colored(f"   {effect_key.replace('_', ' ').title()}: {value_text}", Fore.GREEN)

            tech_options.append(tech_key)
            option_counter += 1

    print_colored("0. Back", Fore.RED)

    # Get player choice
    while True:
        try:
            choice = int(input_colored("\nSelect a technology to research: ", Fore.YELLOW))
            if 0 <= choice <= len(tech_options):
                break
            else:
                print_colored("Invalid option. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return

    # Start research
    selected_tech = tech_options[choice - 1]
    tech_data = TECHNOLOGIES[selected_tech]

    game_state["research"]["current_research"].append({
        "key": selected_tech,
        "progress": 0,
        "cost": tech_data["cost"]
    })

    print_message(f"Started research: {tech_data['name']}", "success")

def process_research():
    """Process ongoing research projects."""
    try:
        # Ensure research structure exists
        if "research" not in game_state:
            game_state["research"] = {
                "current_research": [],
                "completed_research": [],
                "research_slots": 3
            }
            return

        # Validate research structure
        if not isinstance(game_state["research"], dict):
            game_state["research"] = {
                "current_research": [],
                "completed_research": [],
                "research_slots": 3
            }
            return

        # Ensure current_research exists
        if "current_research" not in game_state["research"]:
            game_state["research"]["current_research"] = []
            return

        # Ensure completed_research exists
        if "completed_research" not in game_state["research"]:
            game_state["research"]["completed_research"] = []
            return

        # If no current research, nothing to process
        if not game_state["research"]["current_research"]:
            return

        # Add progress to each research project
        for research in game_state["research"]["current_research"]:
            research["progress"] += 1  # In a full game, this would be based on research speed

            # Check if research is complete
            if research["progress"] >= research["cost"]:
                tech_key = research["key"]
                tech_data = TECHNOLOGIES[tech_key]

                # Mark as completed
                game_state["research"]["completed_research"].append(tech_key)
                game_state["research"]["current_research"].remove(research)

                print_message(f"Research completed: {tech_data['name']}", "success")

                # Apply effects
                if "effects" in tech_data:
                    # In a full game, we would apply these effects to the player's nation
                    pass

                break  # Only complete one research per tick to avoid list modification issues
    except (KeyError, TypeError) as e:
        # If any error occurs, reset the research structure
        print_message(f"Research system error: {str(e)}", "error")
        game_state["research"] = {
            "current_research": [],
            "completed_research": [],
            "research_slots": 3
        }

def show_production():
    """Display and handle production management."""
    clear_screen()
    print_header("Production")

    # Initialize production state if needed
    if "production" not in game_state:
        game_state["production"] = {
            "queues": {
                "military_equipment": [],
                "naval": [],
                "air": [],
            },
            "factory_allocation": {
                "military_equipment": 0,
                "naval": 0,
                "air": 0,
            }
        }

    player_nation = game_state["player_nation"]
    nation_data = game_state["nations"][player_nation]

    # Display available factories
    military_factories = nation_data["industry"]["military_factories"]
    dockyards = nation_data["industry"]["dockyards"]

    print_colored("Factory Status:", Fore.YELLOW)
    print_colored(f"Military Factories: {military_factories}", Fore.CYAN)
    print_colored(f"Dockyards: {dockyards}", Fore.CYAN)
    print()

    # Display current allocations
    print_colored("Current Allocations:", Fore.YELLOW)
    allocated_mil = game_state["production"]["factory_allocation"]["military_equipment"]
    allocated_naval = game_state["production"]["factory_allocation"]["naval"]
    allocated_air = game_state["production"]["factory_allocation"]["air"]

    print_colored(f"Military Equipment: {allocated_mil}/{military_factories} factories", Fore.CYAN)
    print_colored(f"Naval Units: {allocated_naval}/{dockyards} dockyards", Fore.CYAN)
    print_colored(f"Air Units: {allocated_air}/{military_factories} factories", Fore.CYAN)
    print()

    # Display production queues
    print_colored("Production Queues:", Fore.YELLOW)

    # Military equipment
    print_colored("\nMilitary Equipment:", Fore.GREEN)
    if game_state["production"]["queues"]["military_equipment"]:
        for i, item in enumerate(game_state["production"]["queues"]["military_equipment"], 1):
            print_colored(f"{i}. {item['name']} - {item['progress']}/{item['cost']} ({item['factories']} factories)", Fore.CYAN)
    else:
        print_colored("  No equipment in production", Fore.RED)

    # Naval units
    print_colored("\nNaval Units:", Fore.GREEN)
    if game_state["production"]["queues"]["naval"]:
        for i, item in enumerate(game_state["production"]["queues"]["naval"], 1):
            print_colored(f"{i}. {item['name']} - {item['progress']}/{item['cost']} ({item['dockyards']} dockyards)", Fore.CYAN)
    else:
        print_colored("  No ships in production", Fore.RED)

    # Air units
    print_colored("\nAir Units:", Fore.GREEN)
    if game_state["production"]["queues"]["air"]:
        for i, item in enumerate(game_state["production"]["queues"]["air"], 1):
            print_colored(f"{i}. {item['name']} - {item['progress']}/{item['cost']} ({item['factories']} factories)", Fore.CYAN)
    else:
        print_colored("  No aircraft in production", Fore.RED)

    # Menu options
    print_colored("\nOptions:", Fore.YELLOW)
    print_colored("1. Add Military Equipment", Fore.CYAN)
    print_colored("2. Add Naval Unit", Fore.CYAN)
    print_colored("3. Add Air Unit", Fore.CYAN)
    print_colored("4. Manage Factory Allocation", Fore.CYAN)
    print_colored("0. Back", Fore.RED)

    # Get player choice
    choice = input_colored("\nSelect an option: ", Fore.YELLOW)

    if choice == "1":
        add_military_equipment()
    elif choice == "2":
        add_naval_unit()
    elif choice == "3":
        add_air_unit()
    elif choice == "4":
        manage_factory_allocation()

def add_military_equipment():
    """Add military equipment to production queue."""
    clear_screen()
    print_header("Add Military Equipment")

    # Display available equipment types
    equipment_types = {
        "infantry_equipment": {"name": "Infantry Equipment", "cost": 60},
        "artillery": {"name": "Artillery", "cost": 84},
        "anti_tank": {"name": "Anti-Tank", "cost": 96},
        "anti_air": {"name": "Anti-Air", "cost": 90},
        "motorized": {"name": "Motorized", "cost": 80},
        "light_tank": {"name": "Light Tank", "cost": 120},
        "medium_tank": {"name": "Medium Tank", "cost": 180},
        "heavy_tank": {"name": "Heavy Tank", "cost": 240},
    }

    print_colored("Available Equipment Types:", Fore.YELLOW)
    for i, (_, data) in enumerate(equipment_types.items(), 1):
        print_colored(f"{i}. {data['name']} - Cost: {data['cost']}", Fore.CYAN)

    print_colored("0. Back", Fore.RED)

    # Get equipment choice
    while True:
        try:
            choice = int(input_colored("\nSelect equipment type: ", Fore.YELLOW))
            if 0 <= choice <= len(equipment_types):
                break
            else:
                print_colored("Invalid option. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return

    # Get selected equipment
    equipment_key = list(equipment_types.keys())[choice - 1]
    equipment_data = equipment_types[equipment_key]

    # Get quantity
    while True:
        try:
            quantity = int(input_colored(f"How many {equipment_data['name']} to produce? ", Fore.YELLOW))
            if quantity > 0:
                break
            else:
                print_colored("Please enter a positive number.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    # Get factory allocation
    available_factories = (game_state["nations"][game_state["player_nation"]]["industry"]["military_factories"] -
                           game_state["production"]["factory_allocation"]["military_equipment"])

    if available_factories <= 0:
        print_colored("No factories available for production.", Fore.RED)
        wait_for_input()
        return

    while True:
        try:
            factories = int(input_colored(f"Allocate how many factories? (1-{available_factories}) ", Fore.YELLOW))
            if 1 <= factories <= available_factories:
                break
            else:
                print_colored(f"Please enter a number between 1 and {available_factories}.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    # Add to production queue
    game_state["production"]["queues"]["military_equipment"].append({
        "key": equipment_key,
        "name": equipment_data["name"],
        "cost": equipment_data["cost"],
        "progress": 0,
        "quantity": quantity,
        "completed": 0,
        "factories": factories
    })

    # Update factory allocation
    game_state["production"]["factory_allocation"]["military_equipment"] += factories

    print_message(f"Added {quantity} {equipment_data['name']} to production with {factories} factories.", "success")

def add_naval_unit():
    """Add naval unit to production queue."""
    clear_screen()
    print_header("Add Naval Unit")

    # Display available ship types
    ship_types = {
        "destroyer": {"name": "Destroyer", "cost": 180},
        "submarine": {"name": "Submarine", "cost": 160},
        "light_cruiser": {"name": "Light Cruiser", "cost": 300},
        "heavy_cruiser": {"name": "Heavy Cruiser", "cost": 400},
        "battleship": {"name": "Battleship", "cost": 800},
        "carrier": {"name": "Aircraft Carrier", "cost": 900},
    }

    print_colored("Available Ship Types:", Fore.YELLOW)
    for i, (_, data) in enumerate(ship_types.items(), 1):
        print_colored(f"{i}. {data['name']} - Cost: {data['cost']}", Fore.CYAN)

    print_colored("0. Back", Fore.RED)

    # Get ship choice
    while True:
        try:
            choice = int(input_colored("\nSelect ship type: ", Fore.YELLOW))
            if 0 <= choice <= len(ship_types):
                break
            print_colored("Invalid option. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return

    # Get selected ship
    ship_key = list(ship_types.keys())[choice - 1]
    ship_data = ship_types[ship_key]

    # Get quantity
    while True:
        try:
            quantity = int(input_colored(f"How many {ship_data['name']}s to produce? ", Fore.YELLOW))
            if quantity > 0:
                break
            print_colored("Please enter a positive number.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    # Get dockyard allocation
    available_dockyards = (game_state["nations"][game_state["player_nation"]]["industry"]["dockyards"] -
                           game_state["production"]["factory_allocation"]["naval"])

    if available_dockyards <= 0:
        print_colored("No dockyards available for production.", Fore.RED)
        wait_for_input()
        return

    while True:
        try:
            dockyards = int(input_colored(f"Allocate how many dockyards? (1-{available_dockyards}) ", Fore.YELLOW))
            if 1 <= dockyards <= available_dockyards:
                break
            else:
                print_colored(f"Please enter a number between 1 and {available_dockyards}.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    # Add to production queue
    game_state["production"]["queues"]["naval"].append({
        "key": ship_key,
        "name": ship_data["name"],
        "cost": ship_data["cost"],
        "progress": 0,
        "quantity": quantity,
        "completed": 0,
        "dockyards": dockyards
    })

    # Update dockyard allocation
    game_state["production"]["factory_allocation"]["naval"] += dockyards

    print_message(f"Added {quantity} {ship_data['name']} to production with {dockyards} dockyards.", "success")

def add_air_unit():
    """Add air unit to production queue."""
    clear_screen()
    print_header("Add Air Unit")

    # Display available aircraft types
    aircraft_types = {
        "fighter": {"name": "Fighter", "cost": 100},
        "cas": {"name": "Close Air Support", "cost": 120},
        "tactical_bomber": {"name": "Tactical Bomber", "cost": 160},
        "strategic_bomber": {"name": "Strategic Bomber", "cost": 240},
        "naval_bomber": {"name": "Naval Bomber", "cost": 130},
    }

    print_colored("Available Aircraft Types:", Fore.YELLOW)
    for i, (_, data) in enumerate(aircraft_types.items(), 1):
        print_colored(f"{i}. {data['name']} - Cost: {data['cost']}", Fore.CYAN)

    print_colored("0. Back", Fore.RED)

    # Get aircraft choice
    while True:
        try:
            choice = int(input_colored("\nSelect aircraft type: ", Fore.YELLOW))
            if 0 <= choice <= len(aircraft_types):
                break
            else:
                print_colored("Invalid option. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return

    # Get selected aircraft
    aircraft_key = list(aircraft_types.keys())[choice - 1]
    aircraft_data = aircraft_types[aircraft_key]

    # Get quantity
    while True:
        try:
            quantity = int(input_colored(f"How many {aircraft_data['name']} to produce? ", Fore.YELLOW))
            if quantity > 0:
                break
            else:
                print_colored("Please enter a positive number.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    # Get factory allocation
    available_factories = (game_state["nations"][game_state["player_nation"]]["industry"]["military_factories"] -
                           game_state["production"]["factory_allocation"]["air"])

    if available_factories <= 0:
        print_colored("No factories available for production.", Fore.RED)
        wait_for_input()
        return

    while True:
        try:
            factories = int(input_colored(f"Allocate how many factories? (1-{available_factories}) ", Fore.YELLOW))
            if 1 <= factories <= available_factories:
                break
            else:
                print_colored(f"Please enter a number between 1 and {available_factories}.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    # Add to production queue
    game_state["production"]["queues"]["air"].append({
        "key": aircraft_key,
        "name": aircraft_data["name"],
        "cost": aircraft_data["cost"],
        "progress": 0,
        "quantity": quantity,
        "completed": 0,
        "factories": factories
    })

    # Update factory allocation
    game_state["production"]["factory_allocation"]["air"] += factories

    print_message(f"Added {quantity} {aircraft_data['name']} to production with {factories} factories.", "success")

def manage_factory_allocation():
    """Manage factory allocation between production queues."""
    clear_screen()
    print_header("Manage Factory Allocation")

    # Display current production queues and allocations
    print_colored("Current Allocations:", Fore.YELLOW)

    player_nation = game_state["player_nation"]
    nation_data = game_state["nations"][player_nation]

    military_factories = nation_data["industry"]["military_factories"]
    dockyards = nation_data["industry"]["dockyards"]

    print_colored(f"Military Factories: {military_factories} total", Fore.CYAN)
    print_colored(f"Dockyards: {dockyards} total", Fore.CYAN)
    print()

    # For simplicity in this demo, we'll just show current allocations
    # In a full game, you'd want to allow redistributing factories between items

    print_colored("Military Equipment Production:", Fore.GREEN)
    for i, item in enumerate(game_state["production"]["queues"]["military_equipment"], 1):
        print_colored(f"{i}. {item['name']} ({item['completed']}/{item['quantity']}) - {item['factories']} factories", Fore.CYAN)

    print_colored("\nNaval Production:", Fore.GREEN)
    for i, item in enumerate(game_state["production"]["queues"]["naval"], 1):
        print_colored(f"{i}. {item['name']} ({item['completed']}/{item['quantity']}) - {item['dockyards']} dockyards", Fore.CYAN)

    print_colored("\nAir Production:", Fore.GREEN)
    for i, item in enumerate(game_state["production"]["queues"]["air"], 1):
        print_colored(f"{i}. {item['name']} ({item['completed']}/{item['quantity']}) - {item['factories']} factories", Fore.CYAN)

    wait_for_input()

def show_construction():
    """Display and handle the construction interface."""
    clear_screen()
    print_header("Construction")

    # Initialize construction state if needed
    if "construction" not in game_state:
        game_state["construction"] = {
            "queue": [],
            "completed": {}
        }

    player_nation = game_state["player_nation"]
    nation_data = game_state["nations"][player_nation]

    # Display available construction resources
    civ_factories = nation_data["industry"]["civilian_factories"]
    available_factories = max(0, civ_factories - 2)  # 2 factories always used for consumer goods

    print_colored("Construction Resources:", Fore.YELLOW)
    print_colored(f"Civilian Factories: {civ_factories} (Consumer Goods: 2, Available: {available_factories})", Fore.CYAN)
    print_colored(f"Infrastructure Level: {nation_data['industry']['infrastructure']}/10", Fore.CYAN)

    # Display current construction speed
    base_speed = 1.0
    infra_bonus = (nation_data['industry']['infrastructure'] - 5) * 0.05
    construction_bonus = 0.0

    # Apply research bonuses
    if "research" in game_state and "completed_research" in game_state["research"]:
        for tech in game_state["research"]["completed_research"]:
            if tech in TECHNOLOGIES and "effects" in TECHNOLOGIES[tech]:
                effects = TECHNOLOGIES[tech]["effects"]
                if "construction_speed" in effects:
                    construction_bonus += effects["construction_speed"]

    total_speed = base_speed + infra_bonus + construction_bonus
    print_colored(f"Construction Speed: {total_speed:.2f}x (Base: 1.0, Infrastructure: {infra_bonus:.2f}, Technology: {construction_bonus:.2f})", Fore.CYAN)
    print()

    # Display current construction queue
    if game_state["construction"]["queue"]:
        print_colored("Construction Queue:", Fore.YELLOW)
        for idx, project in enumerate(game_state["construction"]["queue"]):
            building_type = project["type"]
            building_data = BUILDINGS[building_type]
            progress_pct = (project["progress"] / building_data["cost"]) * 100
            factories_assigned = project["factories"]

            days_left = math.ceil((building_data["cost"] - project["progress"]) /
                                (factories_assigned * total_speed))

            print_colored(f"{idx+1}. {building_data['name']} - {progress_pct:.1f}% - {factories_assigned} factories - {days_left} days left", Fore.WHITE)
        print()
    else:
        print_colored("No construction projects in queue.", Fore.YELLOW)
        print()

    # Display completed buildings
    if game_state["construction"]["completed"]:
        print_colored("Completed Buildings:", Fore.GREEN)
        for building_type, count in game_state["construction"]["completed"].items():
            if count > 0:
                building_name = BUILDINGS[building_type]["name"]
                print_colored(f"{building_name}: {count}", Fore.WHITE)
        print()

    # Display options
    print_colored("Options:", Fore.YELLOW)
    print_colored("1. Add Construction Project", Fore.CYAN)
    print_colored("2. Adjust Factory Allocation", Fore.CYAN)
    print_colored("3. Cancel Project", Fore.CYAN)
    print_colored("0. Back", Fore.MAGENTA)

    choice = input_colored("\nSelect an option: ", Fore.YELLOW)

    if choice == "1":
        add_construction_project()
    elif choice == "2":
        adjust_factory_allocation()
    elif choice == "3":
        cancel_construction_project()

def add_construction_project():
    """Add a new construction project to the queue."""
    clear_screen()
    print_header("Add Construction Project")

    player_nation = game_state["player_nation"]
    nation_data = game_state["nations"][player_nation]

    available_factories = max(0, nation_data["industry"]["civilian_factories"] - 2)
    factories_in_use = 0
    for project in game_state["construction"]["queue"]:
        factories_in_use += project["factories"]

    remaining_factories = available_factories - factories_in_use

    print_colored(f"Available Civilian Factories: {remaining_factories}/{available_factories}", Fore.YELLOW)
    print()

    if remaining_factories <= 0:
        print_colored("No factories available for new construction projects. Adjust current projects first.", Fore.RED)
        wait_for_input()
        return

    # Display available building types
    print_colored("Available Building Types:", Fore.YELLOW)

    available_buildings = []
    for idx, (building_key, building) in enumerate(BUILDINGS.items()):
        can_build = True

        # Check technology requirements
        if building["tech_requirement"]:
            if "research" not in game_state or "completed_research" not in game_state["research"] or building["tech_requirement"] not in game_state["research"]["completed_research"]:
                can_build = False

        if can_build:
            available_buildings.append(building_key)
            days_estimate = math.ceil(building["cost"] / (1 * total_construction_speed()))
            print_colored(f"{idx+1}. {building['name']} - {days_estimate} days with 1 factory", Fore.CYAN)
            print_colored(f"   {building['description']}", Fore.WHITE)

            # Resource costs
            costs = []
            for resource, amount in building["resource_cost"].items():
                costs.append(f"{resource}: {amount}")

            print_colored(f"   Cost: {', '.join(costs)}", Fore.WHITE)
            print()

    if not available_buildings:
        print_colored("No buildings available to construct. Research required technologies first.", Fore.RED)
        wait_for_input()
        return

    choice = input_colored("Select building type (0 to cancel): ", Fore.YELLOW)

    try:
        idx = int(choice) - 1
        if idx == -1:
            return
        if 0 <= idx < len(available_buildings):
            building_key = available_buildings[idx]

            factories = input_colored(f"Assign factories (1-{remaining_factories}): ", Fore.YELLOW)
            try:
                factories = int(factories)
                if 1 <= factories <= remaining_factories:
                    # Add to construction queue
                    game_state["construction"]["queue"].append({
                        "type": building_key,
                        "progress": 0,
                        "factories": factories
                    })
                    print_colored(f"Added {BUILDINGS[building_key]['name']} to construction queue.", Fore.GREEN)
                else:
                    print_colored("Invalid number of factories.", Fore.RED)
            except ValueError:
                print_colored("Invalid input.", Fore.RED)
        else:
            print_colored("Invalid selection.", Fore.RED)
    except ValueError:
        print_colored("Invalid input.", Fore.RED)

    wait_for_input()

def adjust_factory_allocation():
    """Adjust factory allocation between construction projects."""
    clear_screen()
    print_header("Adjust Factory Allocation")

    if not game_state["construction"]["queue"]:
        print_colored("No construction projects in queue.", Fore.YELLOW)
        wait_for_input()
        return

    player_nation = game_state["player_nation"]
    nation_data = game_state["nations"][player_nation]

    available_factories = max(0, nation_data["industry"]["civilian_factories"] - 2)
    factories_in_use = 0

    # Display current allocation
    print_colored("Current Factory Allocation:", Fore.YELLOW)
    for idx, project in enumerate(game_state["construction"]["queue"]):
        building_name = BUILDINGS[project["type"]]["name"]
        factories = project["factories"]
        factories_in_use += factories
        print_colored(f"{idx+1}. {building_name}: {factories} factories", Fore.CYAN)

    print()
    print_colored(f"Total Factories: {available_factories}", Fore.YELLOW)
    print_colored(f"In Use: {factories_in_use}", Fore.YELLOW)
    print_colored(f"Available: {available_factories - factories_in_use}", Fore.YELLOW)
    print()

    # Select project to adjust
    project_idx = input_colored("Select project to adjust (0 to cancel): ", Fore.YELLOW)

    try:
        idx = int(project_idx) - 1
        if idx == -1:
            return

        if 0 <= idx < len(game_state["construction"]["queue"]):
            project = game_state["construction"]["queue"][idx]
            building_name = BUILDINGS[project["type"]]["name"]
            current_factories = project["factories"]

            print_colored(f"Adjusting factories for {building_name}", Fore.CYAN)
            print_colored(f"Current allocation: {current_factories} factories", Fore.CYAN)

            # Calculate max available factories for this project
            max_factories = available_factories - factories_in_use + current_factories

            new_factories = input_colored(f"New allocation (1-{max_factories}): ", Fore.YELLOW)

            try:
                new_factories = int(new_factories)
                if 1 <= new_factories <= max_factories:
                    project["factories"] = new_factories
                    print_colored(f"Factory allocation for {building_name} updated to {new_factories}.", Fore.GREEN)
                else:
                    print_colored("Invalid number of factories.", Fore.RED)
            except ValueError:
                print_colored("Invalid input.", Fore.RED)
        else:
            print_colored("Invalid selection.", Fore.RED)
    except ValueError:
        print_colored("Invalid input.", Fore.RED)

    wait_for_input()

def cancel_construction_project():
    """Cancel a construction project from the queue."""
    clear_screen()
    print_header("Cancel Construction Project")

    if not game_state["construction"]["queue"]:
        print_colored("No construction projects in queue.", Fore.YELLOW)
        wait_for_input()
        return

    # Display current projects
    print_colored("Current Construction Projects:", Fore.YELLOW)
    for idx, project in enumerate(game_state["construction"]["queue"]):
        building_name = BUILDINGS[project["type"]]["name"]
        progress_pct = (project["progress"] / BUILDINGS[project["type"]]["cost"]) * 100
        print_colored(f"{idx+1}. {building_name} - {progress_pct:.1f}% complete", Fore.CYAN)

    print()
    project_idx = input_colored("Select project to cancel (0 to cancel): ", Fore.YELLOW)

    try:
        idx = int(project_idx) - 1
        if idx == -1:
            return

        if 0 <= idx < len(game_state["construction"]["queue"]):
            project = game_state["construction"]["queue"][idx]
            building_name = BUILDINGS[project["type"]]["name"]

            confirm = input_colored(f"Are you sure you want to cancel {building_name}? Progress will be lost. (y/n): ", Fore.YELLOW)

            if confirm.lower() == "y":
                game_state["construction"]["queue"].pop(idx)
                print_colored(f"{building_name} construction canceled.", Fore.GREEN)
            else:
                print_colored("Cancellation aborted.", Fore.YELLOW)
        else:
            print_colored("Invalid selection.", Fore.RED)
    except ValueError:
        print_colored("Invalid input.", Fore.RED)

    wait_for_input()

def total_construction_speed():
    """Calculate the total construction speed multiplier based on infrastructure and technologies."""
    player_nation = game_state["player_nation"]
    nation_data = game_state["nations"][player_nation]

    base_speed = 1.0
    infra_bonus = (nation_data['industry']['infrastructure'] - 5) * 0.05
    construction_bonus = 0.0

    # Apply research bonuses
    if "research" in game_state and "completed_research" in game_state["research"]:
        for tech in game_state["research"]["completed_research"]:
            if tech in TECHNOLOGIES and "effects" in TECHNOLOGIES[tech]:
                effects = TECHNOLOGIES[tech]["effects"]
                if "construction_speed" in effects:
                    construction_bonus += effects["construction_speed"]

    return max(0.1, base_speed + infra_bonus + construction_bonus)

def process_construction():
    """Process ongoing construction projects."""
    if "construction" not in game_state:
        game_state["construction"] = {
            "queue": [],
            "completed": {}
        }

    if not game_state["construction"]["queue"]:
        return

    speed_multiplier = total_construction_speed()

    # Process each project
    completed_projects = []
    for idx, project in enumerate(game_state["construction"]["queue"]):
        building_type = project["type"]
        building_data = BUILDINGS[building_type]
        factories = project["factories"]

        # Calculate progress this turn
        progress_per_day = factories * speed_multiplier
        project["progress"] += progress_per_day * 30  # Monthly progress

        # Check if project is completed
        if project["progress"] >= building_data["cost"]:
            completed_projects.append(idx)

            # Update completed buildings count
            if building_type not in game_state["construction"]["completed"]:
                game_state["construction"]["completed"][building_type] = 0
            game_state["construction"]["completed"][building_type] += 1

            # Apply building effects to nation
            player_nation = game_state["player_nation"]
            nation_data = game_state["nations"][player_nation]

            # Update nation based on building type
            if building_type == "civilian_factory":
                nation_data["industry"]["civilian_factories"] += 1
            elif building_type == "military_factory":
                nation_data["industry"]["military_factories"] += 1
            elif building_type == "dockyard":
                nation_data["industry"]["dockyards"] += 1
            elif building_type == "infrastructure":
                nation_data["industry"]["infrastructure"] = min(10, nation_data["industry"]["infrastructure"] + 1)

            print_message(f"Construction completed: {building_data['name']}", "success")

    # Remove completed projects (in reverse order to avoid index issues)
    for idx in sorted(completed_projects, reverse=True):
        game_state["construction"]["queue"].pop(idx)

def process_production():
    """Process ongoing production."""
    if "production" not in game_state:
        return

    # Process military equipment
    for item in game_state["production"]["queues"]["military_equipment"]:
        # Progress is based on number of factories
        # In a real game, efficiency and other factors would be considered
        progress_per_tick = item["factories"] * 0.5
        item["progress"] += progress_per_tick

        # Check if an item is completed
        while item["progress"] >= item["cost"] and item["completed"] < item["quantity"]:
            item["progress"] -= item["cost"]
            item["completed"] += 1

            # Add equipment to nation's arsenal
            equipment_type = item["key"]
            if equipment_type in game_state["nations"][game_state["player_nation"]]["army"]["equipment"]:
                game_state["nations"][game_state["player_nation"]]["army"]["equipment"][equipment_type] += 1
            else:
                game_state["nations"][game_state["player_nation"]]["army"]["equipment"][equipment_type] = 1

            # If all items are completed, remove from queue and free factories
            if item["completed"] >= item["quantity"]:
                game_state["production"]["factory_allocation"]["military_equipment"] -= item["factories"]
                game_state["production"]["queues"]["military_equipment"].remove(item)
                print_message(f"Production completed: {item['quantity']} {item['name']}", "success")
                break

    # Process naval units (similar logic)
    for item in game_state["production"]["queues"]["naval"]:
        progress_per_tick = item["dockyards"] * 0.3  # Naval units take longer
        item["progress"] += progress_per_tick

        while item["progress"] >= item["cost"] and item["completed"] < item["quantity"]:
            item["progress"] -= item["cost"]
            item["completed"] += 1

            # Add ship to navy
            ship_type = item["key"]
            if ship_type in game_state["nations"][game_state["player_nation"]]["navy"]["ships"]:
                game_state["nations"][game_state["player_nation"]]["navy"]["ships"][ship_type] += 1
            else:
                game_state["nations"][game_state["player_nation"]]["navy"]["ships"][ship_type] = 1

            if item["completed"] >= item["quantity"]:
                game_state["production"]["factory_allocation"]["naval"] -= item["dockyards"]
                game_state["production"]["queues"]["naval"].remove(item)
                print_message(f"Production completed: {item['quantity']} {item['name']}", "success")
                break

    # Process air units
    for item in game_state["production"]["queues"]["air"]:
        progress_per_tick = item["factories"] * 0.4
        item["progress"] += progress_per_tick

        while item["progress"] >= item["cost"] and item["completed"] < item["quantity"]:
            item["progress"] -= item["cost"]
            item["completed"] += 1

            # Add aircraft to air force
            aircraft_type = item["key"]
            if aircraft_type == "fighter":
                game_state["nations"][game_state["player_nation"]]["air_force"]["fighters"] += 1
            elif aircraft_type in ["tactical_bomber", "strategic_bomber", "cas", "naval_bomber"]:
                game_state["nations"][game_state["player_nation"]]["air_force"]["bombers"] += 1

            if item["completed"] >= item["quantity"]:
                game_state["production"]["factory_allocation"]["air"] -= item["factories"]
                game_state["production"]["queues"]["air"].remove(item)
                print_message(f"Production completed: {item['quantity']} {item['name']}", "success")
                break

def show_diplomacy():
    """Display and handle diplomacy screen."""
    clear_screen()
    print_header("Diplomacy")

    # Initialize diplomacy if needed
    if "diplomacy" not in game_state:
        game_state["diplomacy"] = {
            "relations": {},
            "factions": {
                "axis": {
                    "name": "Axis",
                    "leader": "germany",
                    "members": ["germany", "italy"],
                },
                "allies": {
                    "name": "Allies",
                    "leader": "uk",
                    "members": ["uk", "france"],
                },
                "comintern": {
                    "name": "Comintern",
                    "leader": "ussr",
                    "members": ["ussr"],
                },
            },
            "player_faction": None,
            "subject_states": {},  # Nations that are puppets/satellites/etc.
            "overlord": None,      # If the player is a subject state
            "relation_types": {
                "at_war": "At War",
                "alliance": "Alliance",
                "non_aggression": "Non-Aggression Pact",
                "trade_agreement": "Trade Agreement",
                "puppet": "Puppet State",
                "satellite": "Satellite State",
                "imperial_subject": "Imperial Subject",
                "colonial_subject": "Colonial Territory",
            },
            "active_ultimatums": [],
        }

        # Initialize relations
        for nation_key in NATIONS:
            if nation_key != game_state["player_nation"]:
                base_relation = 0

                # Set initial relations based on government type and historical context
                player_govt = game_state["nations"][game_state["player_nation"]]["government"]
                nation_govt = NATIONS[nation_key]["government"]

                # Similar governments get better relations
                if player_govt == nation_govt:
                    base_relation += 20

                # Historical context adjustments
                if game_state["player_nation"] == "germany":
                    if nation_key == "italy":
                        base_relation += 40  # Axis buddy
                    elif nation_key == "japan":
                        base_relation += 30  # Potential ally
                    elif nation_key in ["uk", "france", "usa"]:
                        base_relation -= 30  # Historical enemies
                    elif nation_key == "ussr":
                        base_relation -= 50  # Ideological enemies

                game_state["diplomacy"]["relations"][nation_key] = base_relation

    # Find player's faction
    player_nation = game_state["player_nation"]
    for faction_key, faction_data in game_state["diplomacy"]["factions"].items():
        if player_nation in faction_data["members"]:
            game_state["diplomacy"]["player_faction"] = faction_key
            break

    # Display player faction
    if game_state["diplomacy"]["player_faction"]:
        faction_key = game_state["diplomacy"]["player_faction"]
        faction_data = game_state["diplomacy"]["factions"][faction_key]
        print_colored(f"Your Faction: {faction_data['name']}", Fore.GREEN)
        print_colored(f"Leader: {NATIONS[faction_data['leader']]['name']}", Fore.CYAN)
        print_colored("Members:", Fore.CYAN)
        for member in faction_data["members"]:
            print_colored(f"  {NATIONS[member]['name']}", Fore.CYAN)
        print()
    else:
        print_colored("You are not part of any faction.", Fore.YELLOW)
        print()

    # Display subject status if player is a puppet/satellite
    if game_state["diplomacy"]["overlord"]:
        overlord_key = game_state["diplomacy"]["overlord"]["nation"]
        subject_type = game_state["diplomacy"]["overlord"]["type"]
        subject_name = game_state["diplomacy"]["relation_types"][subject_type]
        print_colored(f"Diplomatic Status: {subject_name} of {NATIONS[overlord_key]['name']}", Fore.RED)
        print()

    # Display puppet states if player has any
    if game_state["diplomacy"]["subject_states"]:
        print_colored("Subject States:", Fore.GREEN)
        for nation_key, data in game_state["diplomacy"]["subject_states"].items():
            subject_type = data["type"]
            subject_name = game_state["diplomacy"]["relation_types"][subject_type]
            print_colored(f"  {NATIONS[nation_key]['name']} - {subject_name}", Fore.CYAN)
        print()

    # Display diplomatic relations
    print_colored("Diplomatic Relations:", Fore.YELLOW)

    # Sort nations by relation value
    sorted_relations = sorted(
        game_state["diplomacy"]["relations"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    for nation_key, relation in sorted_relations:
        nation_name = NATIONS[nation_key]["name"]

        # Color based on relation value
        if relation >= 80:
            color = Fore.GREEN
            status = "Friendly"
        elif relation >= 50:
            color = Fore.CYAN
            status = "Cordial"
        elif relation >= 0:
            color = Fore.YELLOW
            status = "Neutral"
        elif relation >= -50:
            color = Fore.RED
            status = "Poor"
        else:
            color = Fore.RED + Style.BRIGHT
            status = "Hostile"

        print_colored(f"{nation_name}: {relation} ({status})", color)

    print()
    print_colored("Options:", Fore.YELLOW)
    print_colored("1. Improve Relations", Fore.CYAN)
    print_colored("2. Request Alliance", Fore.CYAN)
    print_colored("3. Declare War", Fore.RED)
    print_colored("4. Issue Ultimatum", Fore.RED)
    print_colored("5. Manage Subject States", Fore.CYAN)
    print_colored("0. Back", Fore.MAGENTA)

    choice = input_colored("\nSelect an option: ", Fore.YELLOW)

    if choice == "1":
        improve_relations()
    elif choice == "2":
        request_alliance()
    elif choice == "3":
        declare_war()
    elif choice == "4":
        issue_ultimatum()
    elif choice == "5":
        manage_subject_states()

def improve_relations():
    """Improve relations with another nation."""
    clear_screen()
    print_header("Improve Relations")

    # Display nations to improve relations with
    print_colored("Select a nation to improve relations with:", Fore.YELLOW)

    # Sort nations by relation value
    sorted_relations = sorted(
        game_state["diplomacy"]["relations"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    nation_options = []
    for i, (nation_key, relation) in enumerate(sorted_relations, 1):
        nation_name = NATIONS[nation_key]["name"]

        # Color based on relation value
        if relation >= 80:
            color = Fore.GREEN
            status = "Friendly"
        elif relation >= 50:
            color = Fore.CYAN
            status = "Cordial"
        elif relation >= 0:
            color = Fore.YELLOW
            status = "Neutral"
        elif relation >= -50:
            color = Fore.RED
            status = "Poor"
        else:
            color = Fore.RED + Style.BRIGHT
            status = "Hostile"

        print_colored(f"{i}. {nation_name}: {relation} ({status})", color)
        nation_options.append(nation_key)

    print_colored("0. Back", Fore.RED)

    # Get player choice
    while True:
        try:
            choice = int(input_colored("\nSelect a nation: ", Fore.YELLOW))
            if 0 <= choice <= len(nation_options):
                break
            else:
                print_colored("Invalid option. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return

    # Selected nation
    nation_key = nation_options[choice - 1]
    nation_name = NATIONS[nation_key]["name"]

    # Display improvement options
    print_colored(f"\nImprove relations with {nation_name}:", Fore.YELLOW)
    print_colored("1. Send diplomatic mission (+5 relations)", Fore.CYAN)
    print_colored("2. Improve trade relations (+10 relations)", Fore.CYAN)
    print_colored("3. Non-aggression pact proposal (+15 relations)", Fore.CYAN)
    print_colored("0. Back", Fore.RED)

    action_choice = input_colored("\nSelect an action: ", Fore.YELLOW)

    if action_choice == "0":
        return

    # Apply relation improvement
    if action_choice == "1":
        game_state["diplomacy"]["relations"][nation_key] += 5
        print_message(f"Diplomatic mission sent to {nation_name}. Relations improved by 5.", "success")
    elif action_choice == "2":
        game_state["diplomacy"]["relations"][nation_key] += 10
        print_message(f"Trade relations improved with {nation_name}. Relations improved by 10.", "success")
    elif action_choice == "3":
        game_state["diplomacy"]["relations"][nation_key] += 15
        print_message(f"Non-aggression pact proposed to {nation_name}. Relations improved by 15.", "success")

        # In a full game, this would trigger an AI decision based on relation level and other factors

def request_alliance():
    """Request an alliance with another nation."""
    clear_screen()
    print_header("Request Alliance")

    # Display nations to request alliance with
    print_colored("Select a nation to request alliance with:", Fore.YELLOW)

    # Filter to nations with good relations
    alliance_candidates = []
    for nation_key, relation in game_state["diplomacy"]["relations"].items():
        if relation >= 50:  # Only nations with cordial or better relations
            alliance_candidates.append((nation_key, relation))

    # Sort by relation value
    alliance_candidates.sort(key=lambda x: x[1], reverse=True)

    if not alliance_candidates:
        print_colored("No suitable nations for alliance. Improve relations first.", Fore.RED)
        wait_for_input()
        return

    nation_options = []
    for i, (nation_key, relation) in enumerate(alliance_candidates, 1):
        nation_name = NATIONS[nation_key]["name"]
        print_colored(f"{i}. {nation_name}: {relation}", Fore.CYAN)
        nation_options.append(nation_key)

    print_colored("0. Back", Fore.RED)

    # Get player choice
    while True:
        try:
            choice = int(input_colored("\nSelect a nation: ", Fore.YELLOW))
            if 0 <= choice <= len(nation_options):
                break
            else:
                print_colored("Invalid option. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return

    # Selected nation
    nation_key = nation_options[choice - 1]
    nation_name = NATIONS[nation_key]["name"]
    relation = game_state["diplomacy"]["relations"][nation_key]

    # Determine chance of acceptance based on relation
    accept_chance = (relation - 50) * 2

    print_colored(f"\nRequesting alliance with {nation_name}...", Fore.YELLOW)

    # Simulate response
    if random.randint(1, 100) <= accept_chance:
        print_colored(f"{nation_name} has accepted your alliance request!", Fore.GREEN)

        # Check if player is already in a faction
        if game_state["diplomacy"]["player_faction"]:
            # Add the nation to player's faction
            faction_key = game_state["diplomacy"]["player_faction"]
            game_state["diplomacy"]["factions"][faction_key]["members"].append(nation_key)
        else:
            # Create a new faction
            faction_name = f"{NATIONS[game_state['player_nation']]['name']} Alliance"
            new_faction_key = f"player_faction_{len(game_state['diplomacy']['factions'])}"

            game_state["diplomacy"]["factions"][new_faction_key] = {
                "name": faction_name,
                "leader": game_state["player_nation"],
                "members": [game_state["player_nation"], nation_key]
            }

            game_state["diplomacy"]["player_faction"] = new_faction_key

        # Improve relations further
        game_state["diplomacy"]["relations"][nation_key] += 25
    else:
        print_colored(f"{nation_name} has declined your alliance request.", Fore.RED)

        # Relations still improve slightly from the attempt
        game_state["diplomacy"]["relations"][nation_key] += 5

    wait_for_input()

def issue_ultimatum():
    """Issue an ultimatum to another nation."""
    clear_screen()
    print_header("Issue Ultimatum")

    # Check if player is already at war with any major power
    player_nation = game_state["player_nation"]
    at_war_with_major = False
    major_powers = ["germany", "uk", "france", "usa", "ussr", "japan", "italy"]

    for nation_key, status in game_state.get("status", {}).items():
        if nation_key in major_powers and status.get("at_war", False) and status.get("at_war_with", "") == player_nation:
            at_war_with_major = True
            break

    if at_war_with_major:
        print_colored("You are already at war with a major power. Focus on that conflict before issuing ultimatums.", Fore.RED)
        wait_for_input()
        return

    # Display nations that can receive ultimatums (not allies or at war)
    print_colored("Select a nation to issue an ultimatum to:", Fore.YELLOW)

    nation_options = []

    for i, (nation_key, relation) in enumerate(sorted(game_state["diplomacy"]["relations"].items(), key=lambda x: x[1]), 1):
        # Skip nations already at war or allies
        is_ally = False
        if game_state["diplomacy"]["player_faction"]:
            faction_data = game_state["diplomacy"]["factions"][game_state["diplomacy"]["player_faction"]]
            is_ally = nation_key in faction_data["members"]

        is_subject = nation_key in game_state["diplomacy"]["subject_states"]

        at_war = False
        if "status" in game_state and nation_key in game_state["status"]:
            at_war = game_state["status"][nation_key].get("at_war", False)

        if not at_war and not is_ally and not is_subject:
            nation_name = NATIONS[nation_key]["name"]
            print_colored(f"{i}. {nation_name} - Relation: {relation}", Fore.CYAN)
            nation_options.append(nation_key)

    if not nation_options:
        print_colored("No suitable nations to issue ultimatums to.", Fore.RED)
        wait_for_input()
        return

    print_colored("0. Back", Fore.RED)

    # Get player choice
    choice = input_colored("\nSelect a nation: ", Fore.YELLOW)

    try:
        idx = int(choice) - 1
        if idx == -1:
            return

        if 0 <= idx < len(nation_options):
            target_nation = nation_options[idx]

            # Display ultimatum options
            clear_screen()
            print_header(f"Ultimatum to {NATIONS[target_nation]['name']}")

            print_colored("Select ultimatum type:", Fore.YELLOW)
            print_colored("1. Demand Territory", Fore.CYAN)
            print_colored("2. Demand Resources", Fore.CYAN)
            print_colored("3. Demand Puppet Status", Fore.CYAN)
            print_colored("4. Demand Military Access", Fore.CYAN)
            print_colored("0. Back", Fore.RED)

            ultimatum_choice = input_colored("\nSelect ultimatum type: ", Fore.YELLOW)

            if ultimatum_choice == "0":
                return

            # Chance of acceptance based on relations and relative power
            relation_value = game_state["diplomacy"]["relations"][target_nation]

            player_strength = calculate_national_strength(player_nation)
            target_strength = calculate_national_strength(target_nation)
            power_ratio = player_strength / max(1, target_strength)

            # Base acceptance chance
            accept_chance = 0

            # Modify based on ultimatum type
            demand_type = ""
            if ultimatum_choice == "1":
                demand_type = "territory"
                accept_chance = -30  # Territory is hard to get
            elif ultimatum_choice == "2":
                demand_type = "resources"
                accept_chance = 0    # Resources are easier
            elif ultimatum_choice == "3":
                demand_type = "puppet"
                accept_chance = -40  # Puppet status is hardest
            elif ultimatum_choice == "4":
                demand_type = "military_access"
                accept_chance = 10   # Military access is easiest

            # Modify by relations
            accept_chance += relation_value / 2

            # Modify by power ratio - stronger nations can push demands
            if power_ratio > 2:
                accept_chance += 30
            elif power_ratio > 1.5:
                accept_chance += 20
            elif power_ratio > 1:
                accept_chance += 10
            else:
                accept_chance -= 20  # Weaker nations get penalized

            # Add some randomness
            accept_chance += random.randint(-10, 10)

            # Add ultimatum to the list
            ultimatum_id = f"ultimatum_{len(game_state['diplomacy']['active_ultimatums']) + 1}"

            game_state["diplomacy"]["active_ultimatums"].append({
                "id": ultimatum_id,
                "from_nation": player_nation,
                "to_nation": target_nation,
                "type": demand_type,
                "accept_chance": min(max(accept_chance, 5), 95),  # Cap between 5% and 95%
                "issued_date": f"{game_state['year']}.{game_state['month']}",
                "expires": game_state["month"] + 1 if game_state["month"] < 12 else 1,  # Expires next month
                "accepted": None,
            })

            # Display ultimatum info
            clear_screen()
            print_header("Ultimatum Issued")
            print_colored(f"You have issued an ultimatum to {NATIONS[target_nation]['name']}.", Fore.YELLOW)
            print_colored(f"Demand: {demand_type.replace('_', ' ').title()}", Fore.CYAN)

            # Hint at acceptance chance without giving exact number
            if accept_chance > 70:
                print_colored("Your advisors believe they are likely to accept.", Fore.GREEN)
            elif accept_chance > 40:
                print_colored("Your advisors believe they may accept.", Fore.YELLOW)
            elif accept_chance > 20:
                print_colored("Your advisors believe acceptance is uncertain.", Fore.YELLOW)
            else:
                print_colored("Your advisors believe they will likely reject this demand.", Fore.RED)

            print_colored("\nThe nation has one month to respond to your ultimatum.", Fore.CYAN)
            print_colored("If they reject, you will have a casus belli against them.", Fore.RED)

            # Diplomatic tension increases
            world_tension_increase = 0
            if demand_type == "territory":
                world_tension_increase = 5
            elif demand_type == "puppet":
                world_tension_increase = 8
            elif demand_type == "resources":
                world_tension_increase = 3
            elif demand_type == "military_access":
                world_tension_increase = 2

            if "world_tension" in game_state:
                game_state["world_tension"] += world_tension_increase

            print_colored(f"\nWorld tension has increased by {world_tension_increase}%", Fore.RED)

            game_state["diplomacy"]["relations"][target_nation] -= 10
            print_colored(f"\nRelations with {NATIONS[target_nation]['name']} have decreased by 10", Fore.RED)

            # Add to message log
            add_message(f"Ultimatum issued to {NATIONS[target_nation]['name']}", "warning")

            wait_for_input()
        else:
            print_colored("Invalid selection.", Fore.RED)
            wait_for_input()
    except ValueError:
        print_colored("Invalid input.", Fore.RED)
        wait_for_input()

def manage_subject_states():
    """Manage puppet and subject states."""
    clear_screen()
    print_header("Manage Subject States")

    if not game_state["diplomacy"]["subject_states"]:
        print_colored("You don't have any subject states to manage.", Fore.YELLOW)
        wait_for_input()
        return

    # Display current subject states
    print_colored("Your Subject States:", Fore.YELLOW)

    subject_options = []
    for i, (nation_key, data) in enumerate(game_state["diplomacy"]["subject_states"].items(), 1):
        subject_type = data["type"]
        subject_name = game_state["diplomacy"]["relation_types"][subject_type]
        nation_name = NATIONS[nation_key]["name"]

        print_colored(f"{i}. {nation_name} - {subject_name}", Fore.CYAN)
        subject_options.append(nation_key)

    print_colored("0. Back", Fore.RED)

    # Get player choice
    choice = input_colored("\nSelect a subject state to manage: ", Fore.YELLOW)

    try:
        idx = int(choice) - 1
        if idx == -1:
            return

        if 0 <= idx < len(subject_options):
            subject_nation = subject_options[idx]
            subject_data = game_state["diplomacy"]["subject_states"][subject_nation]
            subject_type = subject_data["type"]

            # Display management options
            clear_screen()
            print_header(f"Manage {NATIONS[subject_nation]['name']}")

            print_colored(f"Status: {game_state['diplomacy']['relation_types'][subject_type]}", Fore.CYAN)
            print_colored(f"Autonomy: {subject_data.get('autonomy', 50)}%", Fore.CYAN)

            print_colored("\nOptions:", Fore.YELLOW)
            print_colored("1. Change Subject Type", Fore.CYAN)
            print_colored("2. Extract Resources", Fore.CYAN)
            print_colored("3. Increase Autonomy", Fore.GREEN)
            print_colored("4. Decrease Autonomy", Fore.RED)
            print_colored("5. Release as Independent", Fore.RED)
            print_colored("0. Back", Fore.MAGENTA)

            subject_choice = input_colored("\nSelect an option: ", Fore.YELLOW)

            if subject_choice == "1":
                change_subject_type(subject_nation)
            elif subject_choice == "2":
                extract_resources(subject_nation)
            elif subject_choice == "3":
                change_autonomy(subject_nation, 10)
            elif subject_choice == "4":
                change_autonomy(subject_nation, -10)
            elif subject_choice == "5":
                release_subject(subject_nation)
        else:
            print_colored("Invalid selection.", Fore.RED)
            wait_for_input()
    except ValueError:
        print_colored("Invalid input.", Fore.RED)
        wait_for_input()

def change_subject_type(nation_key):
    """Change the type of a subject state."""
    clear_screen()
    print_header(f"Change Subject Type - {NATIONS[nation_key]['name']}")

    current_type = game_state["diplomacy"]["subject_states"][nation_key]["type"]
    print_colored(f"Current Type: {game_state['diplomacy']['relation_types'][current_type]}", Fore.CYAN)

    # Display available subject types
    print_colored("\nSelect new subject type:", Fore.YELLOW)
    print_colored("1. Puppet State", Fore.CYAN)
    print_colored("2. Satellite State", Fore.CYAN)
    print_colored("3. Imperial Subject", Fore.CYAN)
    print_colored("4. Colonial Territory", Fore.CYAN)
    print_colored("0. Cancel", Fore.RED)

    choice = input_colored("\nSelect an option: ", Fore.YELLOW)

    new_type = None
    if choice == "1":
        new_type = "puppet"
    elif choice == "2":
        new_type = "satellite"
    elif choice == "3":
        new_type = "imperial_subject"
    elif choice == "4":
        new_type = "colonial_subject"

    if new_type and new_type != current_type:
        # Change the subject type
        game_state["diplomacy"]["subject_states"][nation_key]["type"] = new_type
        print_colored(f"Changed {NATIONS[nation_key]['name']} to {game_state['diplomacy']['relation_types'][new_type]}", Fore.GREEN)

        # Update autonomy based on new type
        if new_type == "puppet":
            game_state["diplomacy"]["subject_states"][nation_key]["autonomy"] = 20
        elif new_type == "satellite":
            game_state["diplomacy"]["subject_states"][nation_key]["autonomy"] = 40
        elif new_type == "imperial_subject":
            game_state["diplomacy"]["subject_states"][nation_key]["autonomy"] = 30
        elif new_type == "colonial_subject":
            game_state["diplomacy"]["subject_states"][nation_key]["autonomy"] = 10

        # Add to message log
        add_message(f"Changed {NATIONS[nation_key]['name']} to {game_state['diplomacy']['relation_types'][new_type]}", "info")

    wait_for_input()

def extract_resources(nation_key):
    """Extract resources from a subject state."""
    clear_screen()
    print_header(f"Extract Resources - {NATIONS[nation_key]['name']}")

    # Calculate available resources
    nation_data = NATIONS[nation_key]
    autonomy = game_state["diplomacy"]["subject_states"][nation_key].get("autonomy", 50)

    # Higher autonomy means fewer resources can be extracted
    extraction_percent = (100 - autonomy) / 100

    print_colored("Available Resources:", Fore.YELLOW)

    if "resources" in nation_data:
        resources = []
        for resource, amount in nation_data["resources"].items():
            extractable = max(0, int(amount * extraction_percent))
            if extractable > 0:
                resources.append((resource, extractable))
                print_colored(f"{resource.title()}: {extractable}", Fore.CYAN)

        if not resources:
            print_colored("No resources available for extraction.", Fore.RED)
            wait_for_input()
            return

        print_colored("\nExtracting resources will decrease autonomy and relations.", Fore.RED)
        confirm = input_colored("Proceed with extraction? (y/n): ", Fore.YELLOW)

        if confirm.lower() == "y":
            # Extract resources
            player_nation = game_state["player_nation"]

            for resource, amount in resources:
                if resource not in game_state["nations"][player_nation].get("resources", {}):
                    if "resources" not in game_state["nations"][player_nation]:
                        game_state["nations"][player_nation]["resources"] = {}
                    game_state["nations"][player_nation]["resources"][resource] = 0

                game_state["nations"][player_nation]["resources"][resource] += amount

            # Decrease autonomy and relations
            game_state["diplomacy"]["subject_states"][nation_key]["autonomy"] = max(0, autonomy - 5)
            game_state["diplomacy"]["relations"][nation_key] -= 10

            # Add to message log
            add_message(f"Extracted resources from {NATIONS[nation_key]['name']}", "success")
            print_colored("Resources extracted successfully.", Fore.GREEN)
        else:
            print_colored("Extraction cancelled.", Fore.YELLOW)
    else:
        print_colored("No resources available for extraction.", Fore.RED)

    wait_for_input()

def change_autonomy(nation_key, amount):
    """Change the autonomy level of a subject state."""
    clear_screen()
    print_header(f"Change Autonomy - {NATIONS[nation_key]['name']}")

    current_autonomy = game_state["diplomacy"]["subject_states"][nation_key].get("autonomy", 50)
    new_autonomy = max(0, min(100, current_autonomy + amount))

    game_state["diplomacy"]["subject_states"][nation_key]["autonomy"] = new_autonomy

    if amount > 0:
        game_state["diplomacy"]["relations"][nation_key] += 5
        print_colored(f"Increased autonomy of {NATIONS[nation_key]['name']} to {new_autonomy}%", Fore.GREEN)
        print_colored("Relations improved by 5", Fore.GREEN)
        add_message(f"Increased autonomy of {NATIONS[nation_key]['name']}", "info")
    else:
        game_state["diplomacy"]["relations"][nation_key] -= 5
        print_colored(f"Decreased autonomy of {NATIONS[nation_key]['name']} to {new_autonomy}%", Fore.RED)
        print_colored("Relations decreased by 5", Fore.RED)
        add_message(f"Decreased autonomy of {NATIONS[nation_key]['name']}", "warning")

    # Check for rebellion if autonomy is too low
    if new_autonomy < 10 and random.randint(1, 100) > 70:
        print_colored(f"\nWARNING: Unrest is growing in {NATIONS[nation_key]['name']}!", Fore.RED + Style.BRIGHT)
        print_colored("There is a risk of rebellion if autonomy remains too low.", Fore.RED)

    wait_for_input()

def release_subject(nation_key):
    """Release a subject state as independent."""
    clear_screen()
    print_header(f"Release Subject - {NATIONS[nation_key]['name']}")

    print_colored("Are you sure you want to release this nation as independent?", Fore.RED)
    print_colored("This will end your control over them, but will improve relations significantly.", Fore.YELLOW)

    confirm = input_colored("Confirm release? (y/n): ", Fore.YELLOW)

    if confirm.lower() == "y":
        # Remove from subject states
        del game_state["diplomacy"]["subject_states"][nation_key]

        # Improve relations
        game_state["diplomacy"]["relations"][nation_key] += 40

        print_colored(f"{NATIONS[nation_key]['name']} has been released as an independent nation.", Fore.GREEN)
        print_colored("Relations have improved by 40", Fore.GREEN)

        # Add to message log
        add_message(f"Released {NATIONS[nation_key]['name']} as independent", "info")
    else:
        print_colored("Release cancelled.", Fore.YELLOW)

    wait_for_input()

def calculate_national_strength(nation_key):
    """Calculate the overall strength of a nation for diplomacy calculations."""
    nation_data = game_state["nations"][nation_key]

    military_strength = (
        nation_data["army"]["divisions"] * 5 +
        sum(nation_data["navy"]["ships"].values()) * 10 +
        (nation_data["air_force"]["fighters"] + nation_data["air_force"]["bombers"]) * 3
    )

    industrial_strength = (
        nation_data["industry"]["civilian_factories"] * 1 +
        nation_data["industry"]["military_factories"] * 2 +
        nation_data["industry"]["dockyards"] * 1.5
    )

    return military_strength + industrial_strength

def add_message(text, message_type="info"):
    """Add a message to the message log."""
    if "message_log" not in game_state:
        game_state["message_log"] = []

    game_state["message_log"].append({
        "text": text,
        "type": message_type,
        "date": f"{game_state['year']}.{game_state['month']}"
    })

def process_ultimatums():
    """Process any active ultimatums."""
    if "diplomacy" not in game_state or "active_ultimatums" not in game_state["diplomacy"]:
        return

    current_month = game_state["month"]
    ultimatums_to_remove = []

    for idx, ultimatum in enumerate(game_state["diplomacy"]["active_ultimatums"]):
        if ultimatum["expires"] == current_month and ultimatum["accepted"] is None:
            # Time to resolve this ultimatum
            accept_chance = ultimatum["accept_chance"]
            roll = random.randint(1, 100)

            accepted = roll <= accept_chance
            ultimatum["accepted"] = accepted

            from_nation = ultimatum["from_nation"]
            to_nation = ultimatum["to_nation"]
            demand_type = ultimatum["type"]

            if accepted:
                # Handle acceptance based on demand type
                if demand_type == "territory":
                    # In a real implementation, would transfer actual territory
                    add_message(f"{NATIONS[to_nation]['name']} has ceded territory to {NATIONS[from_nation]['name']}", "success")
                elif demand_type == "resources":
                    # Transfer some resources
                    if "resources" in NATIONS[to_nation]:
                        for resource, amount in NATIONS[to_nation]["resources"].items():
                            if resource not in game_state["nations"][from_nation].get("resources", {}):
                                if "resources" not in game_state["nations"][from_nation]:
                                    game_state["nations"][from_nation]["resources"] = {}
                                game_state["nations"][from_nation]["resources"][resource] = 0

                            transfer_amount = max(1, int(amount * 0.3))
                            game_state["nations"][from_nation]["resources"][resource] += transfer_amount

                    add_message(f"{NATIONS[to_nation]['name']} has agreed to send resources", "success")
                elif demand_type == "puppet":
                    # Make the nation a puppet
                    if "subject_states" not in game_state["diplomacy"]:
                        game_state["diplomacy"]["subject_states"] = {}

                    game_state["diplomacy"]["subject_states"][to_nation] = {
                        "type": "puppet",
                        "autonomy": 20,
                        "since": f"{game_state['year']}.{game_state['month']}"
                    }

                    add_message(f"{NATIONS[to_nation]['name']} is now a puppet state", "success")
                elif demand_type == "military_access":
                    # Grant military access
                    if "military_access" not in game_state["diplomacy"]:
                        game_state["diplomacy"]["military_access"] = {}

                    if to_nation not in game_state["diplomacy"]["military_access"]:
                        game_state["diplomacy"]["military_access"][to_nation] = []

                    game_state["diplomacy"]["military_access"][to_nation].append(from_nation)

                    add_message(f"{NATIONS[to_nation]['name']} has granted military access", "success")

                # Improve relations slightly
                game_state["diplomacy"]["relations"][to_nation] += 5
            else:
                # Ultimatum rejected
                add_message(f"{NATIONS[to_nation]['name']} has rejected the ultimatum", "error")

                # Decrease relations significantly
                game_state["diplomacy"]["relations"][to_nation] -= 20

                # Grant casus belli
                if "casus_belli" not in game_state["diplomacy"]:
                    game_state["diplomacy"]["casus_belli"] = {}

                if from_nation not in game_state["diplomacy"]["casus_belli"]:
                    game_state["diplomacy"]["casus_belli"][from_nation] = {}

                game_state["diplomacy"]["casus_belli"][from_nation][to_nation] = {
                    "type": "rejected_ultimatum",
                    "expires": game_state["year"] + 1  # Expires in 1 year
                }

                # Increase world tension
                if "world_tension" in game_state:
                    game_state["world_tension"] += 5

            # Mark for removal
            ultimatums_to_remove.append(idx)

    # Remove processed ultimatums (in reverse order to avoid index issues)
    for idx in sorted(ultimatums_to_remove, reverse=True):
        del game_state["diplomacy"]["active_ultimatums"][idx]

def declare_war():
    """Declare war on another nation."""
    clear_screen()
    print_header("Declare War")

    print_colored("WARNING: Declaring war has serious consequences!", Fore.RED + Style.BRIGHT)
    print_colored("It will increase world tension and may draw other nations into the conflict.", Fore.RED)
    print()

    # Display nations to declare war on
    print_colored("Select a nation to declare war on:", Fore.YELLOW)

    # List all nations except those already at war or in same faction
    war_candidates = []

    # Get list of nations you're already at war with
    at_war_with = game_state.get("wars", [])

    # Get list of nations in your faction
    in_faction_with = []
    if game_state["diplomacy"]["player_faction"]:
        in_faction_with = game_state["diplomacy"]["factions"][game_state["diplomacy"]["player_faction"]]["members"]

    for nation_key in NATIONS:
        if (nation_key != game_state["player_nation"] and
            nation_key not in at_war_with and
            nation_key not in in_faction_with):
            relation = game_state["diplomacy"]["relations"].get(nation_key, 0)
            war_candidates.append((nation_key, relation))

    # Sort by relation value
    war_candidates.sort(key=lambda x: x[1])

    if not war_candidates:
        print_colored("No suitable nations to declare war on.", Fore.RED)
        wait_for_input()
        return

    nation_options = []
    for i, (nation_key, relation) in enumerate(war_candidates, 1):
        nation_name = NATIONS[nation_key]["name"]

        # Color based on relation value
        if relation >= 50:
            color = Fore.GREEN
            status = "Friendly"
        elif relation >= 0:
            color = Fore.YELLOW
            status = "Neutral"
        else:
            color = Fore.RED
            status = "Hostile"

        print_colored(f"{i}. {nation_name}: {relation} ({status})", color)
        nation_options.append(nation_key)

    print_colored("0. Back", Fore.RED)

    # Get player choice
    while True:
        try:
            choice = int(input_colored("\nSelect a nation: ", Fore.YELLOW))
            if 0 <= choice <= len(nation_options):
                break
            else:
                print_colored("Invalid option. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    if choice == 0:
        return

    # Selected nation
    nation_key = nation_options[choice - 1]
    nation_name = NATIONS[nation_key]["name"]

    # Confirm war declaration
    print_colored(f"\nAre you sure you want to declare war on {nation_name}?", Fore.RED)
    print_colored("This action cannot be undone.", Fore.RED)
    print_colored("y/n: ", Fore.YELLOW, end="")

    confirm = input().lower()

    if confirm != 'y':
        return

    # Declare war
    if "wars" not in game_state:
        game_state["wars"] = []

    game_state["wars"].append(nation_key)

    # Set relations to -100
    game_state["diplomacy"]["relations"][nation_key] = -100

    # Increase world tension
    # In a full game, this would be a more complex calculation

    # If the target nation is in a faction, potentially bring that faction into the war
    for _, faction_data in game_state["diplomacy"]["factions"].items():
        if nation_key in faction_data["members"]:
            # In a full game, this would involve faction logic and guarantees
            print_colored(f"Warning: {nation_name} is a member of the {faction_data['name']} faction.", Fore.RED)
            print_colored("Other members may join the war against you.", Fore.RED)
            break

    print_message(f"War declared on {nation_name}!", "warning")

    # Increase war support
    game_state["nations"][game_state["player_nation"]]["war_support"] += 5

    wait_for_input()

def show_nation_info():
    """Display detailed information about the player's nation."""
    clear_screen()
    print_header("Nation Information")

    player_nation = game_state["player_nation"]
    nation_data = game_state["nations"][player_nation]

    # Display basic info
    print_colored(f"Nation: {nation_data['name']}", Fore.YELLOW + Style.BRIGHT)
    print_colored(f"Leader: {nation_data['leader']}", Fore.YELLOW)
    print_colored(f"Government: {nation_data['government']}", Fore.YELLOW)
    print()

    # Display stability and war support
    print_colored("Political Status:", Fore.CYAN)
    stability = nation_data["stability"]
    war_support = nation_data["war_support"]

    # Color based on value
    stability_color = Fore.GREEN if stability >= 70 else Fore.YELLOW if stability >= 40 else Fore.RED
    war_support_color = Fore.GREEN if war_support >= 70 else Fore.YELLOW if war_support >= 40 else Fore.RED

    print_colored(f"Stability: {stability}%", stability_color)
    print_colored(f"War Support: {war_support}%", war_support_color)
    print()

    # Display industry
    print_colored("Industrial Capacity:", Fore.CYAN)
    print_colored(f"Civilian Factories: {nation_data['industry']['civilian_factories']}", Fore.WHITE)
    print_colored(f"Military Factories: {nation_data['industry']['military_factories']}", Fore.WHITE)
    print_colored(f"Dockyards: {nation_data['industry']['dockyards']}", Fore.WHITE)
    print_colored(f"Infrastructure Level: {nation_data['industry']['infrastructure']}", Fore.WHITE)
    print()

    # Display resources
    print_colored("Resources:", Fore.CYAN)
    for resource, amount in nation_data["resources"].items():
        color = Fore.GREEN if amount >= 20 else Fore.YELLOW if amount > 0 else Fore.RED
        print_colored(f"{resource.title()}: {amount}", color)
    print()

    # Display military
    print_colored("Military:", Fore.CYAN)
    print_colored(f"Divisions: {nation_data['army']['divisions']}", Fore.WHITE)
    print_colored(f"Manpower: {format_number(nation_data['army']['manpower'])}", Fore.WHITE)

    print_colored("\nEquipment:", Fore.CYAN)
    for equip_type, amount in nation_data['army']['equipment'].items():
        print_colored(f"{equip_type.replace('_', ' ').title()}: {format_number(amount)}", Fore.WHITE)

    print_colored("\nNavy:", Fore.CYAN)
    for ship_type, amount in nation_data['navy']['ships'].items():
        print_colored(f"{ship_type.replace('_', ' ').title()}: {amount}", Fore.WHITE)

    print_colored("\nAir Force:", Fore.CYAN)
    print_colored(f"Fighters: {nation_data['air_force']['fighters']}", Fore.WHITE)
    print_colored(f"Bombers: {nation_data['air_force']['bombers']}", Fore.WHITE)

    wait_for_input()

def show_message_log():
    """Display the message log."""
    clear_screen()
    print_header("Message Log")

    if not game_state["message_log"]:
        print_colored("No messages in log.", Fore.YELLOW)
        wait_for_input()
        return

    # Get most recent messages first
    messages = reversed(game_state["message_log"])

    for message in messages:
        message_text = message["text"]
        message_date = message["date"]
        message_type = message["type"]

        # Set color based on message type
        color = Fore.CYAN
        if message_type == "success":
            color = Fore.GREEN
        elif message_type == "warning":
            color = Fore.YELLOW
        elif message_type == "error":
            color = Fore.RED
        elif message_type == "event":
            color = Fore.MAGENTA

        print_colored(f"{message_date}: {message_text}", color)

    wait_for_input()

def show_help():
    """Display help information."""
    clear_screen()
    print_header("Help")

    help_topics = {
        "Gameplay": [
            "Deutschland is a text-based grand strategy game inspired by Hearts of Iron IV.",
            "Manage your nation through economic, diplomatic, and military challenges.",
            "The game advances month by month as you make strategic decisions."
        ],
        "National Focus": [
            "National Focuses represent major policy initiatives and political decisions.",
            "Each focus takes time to complete and provides specific bonuses or triggers events.",
            "You can only work on one focus at a time."
        ],
        "Research": [
            "Research new technologies to improve your military, industry, and infrastructure.",
            "Technologies may have prerequisites and may be ahead of their time.",
            "You have a limited number of research slots based on your nation."
        ],
        "Production": [
            "Allocate factories to produce military equipment, ships, and aircraft.",
            "Military factories produce land and air equipment.",
            "Dockyards produce naval vessels."
        ],
        "Diplomacy": [
            "Manage relations with other nations through diplomatic actions.",
            "Form alliances, improve relations, or declare war.",
            "Your government type affects your diplomatic options."
        ]
    }

    for topic, lines in help_topics.items():
        print_colored(f"{topic}:", Fore.YELLOW + Style.BRIGHT)
        for line in lines:
            print_colored(f"  {line}", Fore.CYAN)
        print()

    print_colored("Controls:", Fore.YELLOW + Style.BRIGHT)
    print_colored("  Enter numbers to select menu options", Fore.CYAN)
    print_colored("  Press Enter to continue after messages", Fore.CYAN)

    wait_for_input()

def show_country_selection():
    """Display country selection screen."""
    clear_screen()
    print_header("Country Selection")

    # Display major powers
    print_colored("Major Powers:", Fore.YELLOW + Style.BRIGHT)

    major_powers = [
        ("germany", "Germany - Fascist"),
        ("uk", "United Kingdom - Democratic"),
        ("france", "France - Democratic"),
        ("italy", "Italy - Fascist"),
        ("ussr", "Soviet Union - Communist"),
        ("usa", "United States - Democratic"),
        ("japan", "Japan - Fascist")
    ]

    for i, (key, name) in enumerate(major_powers, 1):
        # Set color based on ideology
        if "Fascist" in name:
            color = Fore.RED
        elif "Communist" in name:
            color = Fore.RED
        elif "Democratic" in name:
            color = Fore.BLUE
        else:
            color = Fore.CYAN

        print_colored(f"{i}. {name}", color)

    # Display minor powers with focus trees
    print_colored("\nMinor Powers with Focus Trees:", Fore.YELLOW + Style.BRIGHT)

    minor_powers = [
        ("poland", "Poland - Democratic"),
        ("yugoslavia", "Yugoslavia - Democratic"),
        ("belgium", "Belgium - Democratic"),
        ("netherlands", "Netherlands - Democratic"),
        ("spain", "Spain - Civil War"),
        ("china", "China - At War"),
        ("turkey", "Turkey - Democratic"),
        ("sweden", "Sweden - Democratic"),
        ("greece", "Greece - Monarchist"),
        ("romania", "Romania - Unstable")
    ]

    for i, (key, name) in enumerate(minor_powers, len(major_powers) + 1):
        # Set color based on ideology or special state
        if "Fascist" in name:
            color = Fore.RED
        elif "Communist" in name:
            color = Fore.RED
        elif "Democratic" in name:
            color = Fore.BLUE
        elif "Monarchist" in name:
            color = Fore.MAGENTA
        elif "Civil War" in name or "At War" in name or "Unstable" in name:
            color = Fore.YELLOW
        else:
            color = Fore.CYAN

        print_colored(f"{i}. {name}", color)

    # Get player choice
    while True:
        try:
            choice = int(input_colored("\nSelect a country: ", Fore.YELLOW))
            all_countries = major_powers + minor_powers
            if 1 <= choice <= len(all_countries):
                break
            else:
                print_colored("Invalid option. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Please enter a number.", Fore.RED)

    # Set player nation
    all_countries = major_powers + minor_powers
    nation_key = all_countries[choice - 1][0]
    game_state["player_nation"] = nation_key

    # Copy nation data to game state
    game_state["nations"] = {}
    for key, data in NATIONS.items():
        game_state["nations"][key] = data.copy()

    # Start in 1936
    game_state["year"] = 1936
    game_state["month"] = 1

    # Initialize research structure
    game_state["research"] = {
        "current_research": [],
        "completed_research": [],
        "research_slots": 3
    }

    return nation_key

def show_main_menu():
    """Display main menu."""
    clear_screen()

    # Display game title
    print(f"{Fore.RED}════════════════════════════════════════════════════════════")
    print(f"{Fore.YELLOW}                    Deutschland - 1936                    ")
    print(f"{Fore.RED}════════════════════════════════════════════════════════════")

    print(f"\n{Fore.YELLOW}A HOI4-Style Grand Strategy Game{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}Version {VERSION}{Style.RESET_ALL}")

    print_colored("\nMain Menu:", Fore.YELLOW)
    print_colored("1. New Game", Fore.CYAN)
    print_colored("2. Load Game", Fore.CYAN)
    print_colored("3. Help", Fore.CYAN)
    print_colored("4. Exit", Fore.RED)

    # Get player choice
    choice = input_colored("\nSelect an option: ", Fore.YELLOW)

    if choice == "1":
        nation = show_country_selection()
        show_new_game_intro(nation)
        game_loop()
    elif choice == "2":
        if load_game():
            game_loop()
        else:
            show_main_menu()
    elif choice == "3":
        show_help()
        show_main_menu()
    elif choice == "4":
        print_colored("\nThank you for playing Deutschland!", Fore.GREEN)
        print_colored("Exiting game...", Fore.RED)
        sys.exit()
    else:
        print_colored("Invalid option. Please try again.", Fore.RED)
        time.sleep(1)
        show_main_menu()

def show_new_game_intro(nation_key):
    """Show introduction for a new game."""
    clear_screen()

    nation_data = NATIONS[nation_key]

    print_header(f"The Rise of {nation_data['name']}")

    intro_text = {
        "germany": [
            "January 1936. The Third Reich stands at a crossroads.",
            "Three years have passed since Adolf Hitler became Chancellor of Germany.",
            "The humiliation of the Versailles Treaty still burns in the nation's memory.",
            "Germany yearns to reclaim its rightful place as a European power.",
            "",
            "Will you rebuild the German military might?",
            "Will you expand the Reich's borders to unite all German peoples?",
            "Will you challenge the established world order?",
            "",
            "The future of Germany - and perhaps the world - is in your hands."
        ],
        "uk": [
            "January 1936. The British Empire spans across the globe.",
            "Yet storm clouds gather over Europe as fascism rises in Germany and Italy.",
            "The Great Depression has weakened Britain's economy and military.",
            "As the leader of the world's greatest empire, you face difficult choices.",
            "",
            "Will you appease the aggressive dictators to preserve peace?",
            "Will you prepare for war to defend democracy?",
            "Will you maintain Britain's colonial dominance?",
            "",
            "The fate of the Empire - and perhaps civilization itself - is in your hands."
        ],
        "france": [
            "January 1936. France stands as the principal land power in Western Europe.",
            "But the wounds of the Great War have not fully healed.",
            "Political division tears at the nation's fabric as extremism grows.",
            "To the east, a resurgent Germany threatens the peace so dearly bought.",
            "",
            "Will you strengthen the defensive frontier against German aggression?",
            "Will you maintain your colonial empire as pressures mount?",
            "Will you reform the nation to meet the challenges ahead?",
            "",
            "The future of France - and the peace of Europe - is in your hands."
        ],
        "italy": [
            "January 1936. Mussolini's Fascist Italy seeks glory and empire.",
            "The conquest of Ethiopia is underway, defying the League of Nations.",
            "Italy dreams of recreating the Roman Empire's greatness in the Mediterranean.",
            "But resources are limited, and the great powers may oppose Italian ambitions.",
            "",
            "Will you build a new Roman Empire across the Mediterranean?",
            "Will you align with Hitler's Germany to challenge the status quo?",
            "Will you modernize Italy's military and industrial capacity?",
            "",
            "The destiny of Italy - and its place in history - is in your hands."
        ],
        "ussr": [
            "January 1936. The Soviet Union continues its revolutionary transformation.",
            "Stalin's Five-Year Plans industrialize the nation at tremendous human cost.",
            "The capitalist powers view the USSR with suspicion and hostility.",
            "Meanwhile, fascism rises in the west and Japanese imperialism threatens the east.",
            "",
            "Will you complete the Soviet industrialization to prepare for war?",
            "Will you spread communism to other nations through revolution?",
            "Will you purge political enemies to consolidate Stalin's power?",
            "",
            "The future of the workers' state - and world revolution - is in your hands."
        ],
        "usa": [
            "January 1936. The United States remains mired in the Great Depression.",
            "Isolationism dominates American foreign policy.",
            "But across the Atlantic and Pacific, aggressive powers threaten world peace.",
            "America possesses vast potential, but its military remains small and outdated.",
            "",
            "Will you maintain America's isolation or engage with the world?",
            "Will you prepare for potential conflicts in Europe and Asia?",
            "Will you complete the New Deal to revitalize the economy?",
            "",
            "The future of America - and its role in the world - is in your hands."
        ],
        "japan": [
            "January 1936. The Empire of Japan stands at a crossroads.",
            "The military exerts increasing control over the government.",
            "Resource-poor Japan seeks expansion to fuel its industrial growth.",
            "Tensions with China and the Western colonial powers continue to rise.",
            "",
            "Will you create a Greater East Asia Co-Prosperity Sphere under Japanese dominance?",
            "Will you challenge Western colonial powers for control of Asia?",
            "Will you secure the resources Japan needs through conquest?",
            "",
            "The destiny of the Japanese Empire - and all of Asia - is in your hands."
        ]
    }

    # Get intro text for selected nation
    intro = intro_text.get(nation_key, [
        "January 1936. A new chapter in history begins.",
        "As leader, you will guide your nation through uncertain times.",
        "The choices you make will determine the fate of your people.",
        "",
        "Will you lead with wisdom and foresight?",
        "The future is in your hands."
    ])

    # Display intro text with animation
    for line in intro:
        if line:
            for char in line:
                print(f"{nation_data['color']}{char}{Style.RESET_ALL}", end="", flush=True)
                time.sleep(0.01)
            print()
        else:
            print()
        time.sleep(0.5)

    wait_for_input("\nPress Enter to begin your journey...")

def show_game_menu():
    """Display in-game menu."""
    clear_screen()

    player_nation = game_state["player_nation"]
    nation_data = game_state["nations"][player_nation]

    # Display game header
    print_header(f"{nation_data['name']} - {game_state['year']}.{game_state['month']}")

    # Display nation stats
    print_colored(f"Leader: {nation_data['leader']} | Government: {nation_data['government']}", Fore.YELLOW)
    print_colored(f"Stability: {nation_data['stability']}% | War Support: {nation_data['war_support']}%", Fore.YELLOW)

    # Display industrial capacity
    print_colored("\nIndustrial Capacity:", Fore.CYAN)
    print_colored(f"Civilian Factories: {nation_data['industry']['civilian_factories']} | " +
                  f"Military Factories: {nation_data['industry']['military_factories']} | " +
                  f"Dockyards: {nation_data['industry']['dockyards']}", Fore.WHITE)

    # Display military overview
    print_colored("\nMilitary Overview:", Fore.CYAN)
    print_colored(f"Divisions: {nation_data['army']['divisions']} | " +
                  f"Ships: {sum(nation_data['navy']['ships'].values())} | " +
                  f"Aircraft: {nation_data['air_force']['fighters'] + nation_data['air_force']['bombers']}", Fore.WHITE)

    # Display current focus
    if game_state["focus_progress"] is not None and isinstance(game_state["focus_progress"], dict):
        focus = game_state["focus_progress"]
        try:
            # pylint: disable=unsupported-membership-test,unsubscriptable-object
            if isinstance(focus, dict) and "key" in focus and "days_left" in focus:
                focus_tree = FOCUS_TREES[nation_data["focus_tree"]]
                focus_details = focus_tree[focus["key"]]
                print_colored(f"\nCurrent Focus: {focus_details['title']} ({focus['days_left']} days left)", Fore.GREEN)
            else:
                print_colored("\nNo current focus selected.", Fore.YELLOW)
        except (KeyError, TypeError):
            print_colored("\nError displaying current focus.", Fore.RED)
            game_state["focus_progress"] = None
    else:
        print_colored("\nNo current focus selected.", Fore.YELLOW)

    # Display current research
    try:
        if "research" in game_state and isinstance(game_state["research"], dict) and \
           "current_research" in game_state["research"] and game_state["research"]["current_research"]:
            print_colored("\nResearch Projects:", Fore.GREEN)
            for research in game_state["research"]["current_research"]:
                tech_data = TECHNOLOGIES[research["key"]]
                progress_pct = (research["progress"] / tech_data["cost"]) * 100
                print_colored(f"  {tech_data['name']} - {progress_pct:.1f}%", Fore.CYAN)
    except (KeyError, TypeError) as e:
        # If there's an error, initialize the research structure
        print_message(f"Research system error: {str(e)}", "error")
        game_state["research"] = {
            "current_research": [],
            "completed_research": [],
            "research_slots": 3
        }

    # Display menu options
    print_colored("\nOptions:", Fore.YELLOW)
    print_colored("1. National Focus", Fore.CYAN)
    print_colored("2. Research", Fore.CYAN)
    print_colored("3. Production", Fore.CYAN)
    print_colored("4. Construction", Fore.CYAN)
    print_colored("5. Diplomacy", Fore.CYAN)
    print_colored("6. Nation Info", Fore.CYAN)
    print_colored("7. Message Log", Fore.CYAN)
    print_colored("8. Advance Time (1 Month)", Fore.GREEN)
    print_colored("9. Save Game", Fore.MAGENTA)
    print_colored("H. Help", Fore.MAGENTA)
    print_colored("0. Exit to Main Menu", Fore.RED)

    # Get player choice
    choice = input_colored("\nSelect an option: ", Fore.YELLOW)

    if choice == "1":
        select_focus()
    elif choice == "2":
        select_research()
    elif choice == "3":
        show_production()
    elif choice == "4":
        show_construction()
    elif choice == "5":
        show_diplomacy()
    elif choice == "6":
        show_nation_info()
    elif choice == "7":
        show_message_log()
    elif choice == "8":
        # Advance time by one month
        advance_time()
        # Also process research, production, and construction
        process_research()
        process_production()
        process_construction()
        print_message(f"Advanced to {game_state['year']}.{game_state['month']}", "info")
    elif choice == "9":
        save_game()
    elif choice.lower() == "h":
        show_help()
    elif choice == "0":
        # Confirm exit
        print_colored("\nAny unsaved progress will be lost. Are you sure? (y/n): ", Fore.RED, end="")
        confirm = input().lower()

        if confirm == 'y':
            return False

    return True

def game_loop():
    """Main game loop."""
    running = True

    while running:
        running = show_game_menu()

    # Return to main menu
    show_main_menu()

def check_launcher():
    """Check if script was called from the main launcher."""
    if 'LAUNCHED_FROM_LAUNCHER' not in os.environ:
        print("This game should be launched through the launch.py launcher.")
        print("Please run 'python3 launch.py' to access all games.")
        input("Press Enter to exit...")
        sys.exit()

def main():
    """Main entry point for the game."""
    # Check if launched from the menu
    check_launcher()

    # Initialize colorama
    init(autoreset=True)

    # Create save folder if it doesn't exist
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    # Show main menu
    show_main_menu()

# Function needs to be defined here and moved above advance_time for proper reference
def apply_focus_effects(focus_key, focus_data):
    """Apply the effects of a completed focus.

    Args:
        focus_key (str): The key of the completed focus
        focus_data (dict): The focus data containing effects
    """
    try:
        # Apply effects
        if "effects" in focus_data:
            effects = focus_data["effects"]
            nation = game_state["nations"][game_state["player_nation"]]

            for key, value in effects.items():
                if key == "stability":
                    nation["stability"] = min(100, max(0, nation["stability"] + value))
                elif key == "war_support":
                    nation["war_support"] = min(100, max(0, nation["war_support"] + value))
                elif key == "civilian_factories":
                    nation["industry"]["civilian_factories"] += value
                elif key == "military_factories":
                    nation["industry"]["military_factories"] += value
                elif key == "dockyards":
                    nation["industry"]["dockyards"] += value
                elif key == "world_tension":
                    # Handle world tension (simplified)
                    game_state["world_tension"] = game_state.get("world_tension", 0) + value
                elif key == "annex":
                    # Handle annexation (simplified)
                    if "conquered_nations" not in game_state:
                        game_state["conquered_nations"] = []
                    game_state["conquered_nations"].append(value)
                    print_message(f"Annexed {value}.", "success")
                elif key == "gain_territory":
                    # Handle territory gain (simplified)
                    if "partial_control" not in game_state:
                        game_state["partial_control"] = []
                    game_state["partial_control"].append(value)
                    print_message(f"Gained territory from {value}.", "success")
                elif key == "resources":
                    for resource, amount in value.items():
                        nation["resources"][resource] += amount
                elif key == "government_change":
                    old_government = nation["government"]
                    nation["government"] = value
                    print_message(f"Government changed from {old_government} to {value}!", "event")
                elif key == "new_leader":
                    old_leader = nation["leader"]
                    nation["leader"] = value
                    print_message(f"New leader: {value} has taken power, replacing {old_leader}!", "event")
                elif key == "internal_conflicts":
                    game_state["internal_conflicts"] += value
                    print_message(f"Internal conflicts have {'increased' if value > 0 else 'decreased'}!", "warning" if value > 0 else "success")
                elif key == "join_faction":
                    # Handle joining faction (simplified)
                    print_message(f"Joined faction: {value}", "success")
                elif key == "create_faction":
                    # Handle creating a new faction
                    game_state["player_faction"] = value
                    print_message(f"Created new faction: {value}", "success")
                elif key == "guarantee":
                    # Handle guarantees
                    print_message(f"Received guarantee from {', '.join(value)}", "success")
                elif key == "non_aggression":
                    # Handle non-aggression pacts
                    print_message(f"Signed non-aggression pact with {', '.join(value)}", "success")
                elif key == "military_access":
                    # Handle military access (simplified)
                    print_message(f"Gained military access to {value}", "success")
                elif key == "opinion_modifier":
                    # Handle opinion modifier (simplified)
                    target, amount = value
                    print_message(f"Opinion with {target} changed by {amount}", "info")
                elif key == "relation_bonus":
                    for country, amount in value.items():
                        print_message(f"Relations with {country} changed by {amount}", "info")
                elif key == "war_goal":
                    print_message(f"Gained war goal against {value}", "warning")
                elif key == "production_bonus":
                    for industry_type, bonus in value.items():
                        print_message(f"Production efficiency for {industry_type} increased by {bonus}%", "success")

        # Add record of completed focus
        if "completed_focuses" not in game_state:
            game_state["completed_focuses"] = []
        if focus_key not in game_state["completed_focuses"]:
            game_state["completed_focuses"].append(focus_key)

    except (KeyError, TypeError) as e:
        # Handle any errors
        print_message(f"Error applying focus effects: {str(e)}", "error")

if __name__ == "__main__":
    main()
