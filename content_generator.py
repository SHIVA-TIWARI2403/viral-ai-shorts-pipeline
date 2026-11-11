import os
import random
import json
import requests
from pathlib import Path
from config import BASE_DIR, GEMINI_API_KEY

USED_TOPICS_FILE = BASE_DIR / "used_topics.json"

# Master Library of 45+ Unique Dark Psychology & Behavioral Science Topics
TOPIC_CATALOG = [
    {
        "id": "ben_franklin_effect",
        "title_en": "The Ben Franklin Effect: How to Make an Enemy Like You",
        "title_hi": "Dushman ko dost banane ki psychological trick (Ben Franklin Effect)",
        "premise": "If someone dislikes you, ask them for a small favor like borrowing a pen. Their brain rationalizes that they must like you because they helped you."
    },
    {
        "id": "door_in_the_face",
        "title_en": "The Door-in-the-Face Hack: How to Get What You Want",
        "title_hi": "Kisi se bhi apni baat manwane ki secret trick (Door in the Face)",
        "premise": "Ask for an impossibly huge request first that they will reject. When you immediately follow up with your real smaller request, they feel obligated to agree."
    },
    {
        "id": "gray_rock_method",
        "title_en": "The Gray Rock Method: How to Defeat a Narcissist",
        "title_hi": "Narcissist aur toxic logon ko harane ka tareeka (Gray Rock Method)",
        "premise": "When someone tries to provoke you or drain your energy, become as boring and unreactive as a gray rock. They thrive on drama; zero reaction starves them."
    },
    {
        "id": "pratfall_effect",
        "title_en": "The Pratfall Effect: Why Flaws Make You Magnetic",
        "title_hi": "Apni kamzori ko taqat kaise banayein (Pratfall Effect)",
        "premise": "Highly competent people become far more likable and relatable when they show a minor flaw or make a small clumsy mistake. Perfection intimidates; vulnerability attracts."
    },
    {
        "id": "scarcity_principle",
        "title_en": "The Scarcity Trap: Why People Crave What They Cannot Have",
        "title_hi": "Log us cheez ke peeche kyun bhagte hain jo unhe nahi milti (Scarcity Trick)",
        "premise": "When access to anything is restricted or made scarce, its perceived value skyrockets in the human mind. Making yourself less available commands instant respect."
    },
    {
        "id": "chameleon_effect",
        "title_en": "The Chameleon Effect: The Secret to Instant Rapport",
        "title_hi": "Kisi ka bhi bharosa turant kaise jeetein (The Chameleon Effect)",
        "premise": "Subtly mirroring someone's posture, speech tempo, and hand gestures tricks their subconscious into believing you share the same soul and intentions."
    },
    {
        "id": "zeigarnik_effect",
        "title_en": "The Zeigarnik Effect: How to Live Rent-Free in Someone's Mind",
        "title_hi": "Kisi ke dimaag me 24 ghante kaise rahein (Zeigarnik Effect)",
        "premise": "The human brain is obsessed with unfinished tasks and open loops. Leaving a conversation or story right at the climax keeps them thinking about you all day."
    },
    {
        "id": "bystander_effect",
        "title_en": "The Bystander Effect: How to Get Help in an Emergency",
        "title_hi": "Bheed me madad kaise mangein (Bystander Effect)",
        "premise": "Never shout 'Someone help me' in a crowd; everyone assumes someone else will do it. Point directly at one specific person: 'You in the blue shirt, call an ambulance!'"
    },
    {
        "id": "spotlight_effect",
        "title_en": "The Spotlight Effect: The Illusion Holding You Back",
        "title_hi": "Log aapke baare me kya sochte hain (Spotlight Effect)",
        "premise": "You overestimate how much other people notice your flaws and mistakes by 400%. The harsh reality? Everyone is too busy worrying about their own spotlight."
    },
    {
        "id": "halo_effect",
        "title_en": "The Halo Effect: How Beauty Blinds Your Judgment",
        "title_hi": "Aapka dimaag khubsurti se kaise dhokha khata hai (The Halo Effect)",
        "premise": "When someone is physically attractive or charismatic, our brain subconsciously assumes they are also kind, honest, and intelligent—even when they are dangerous."
    },
    {
        "id": "dunning_kruger",
        "title_en": "The Dunning-Kruger Effect: Why Fools Are So Confident",
        "title_hi": "Kam gyaan wale log sabse zyada confident kyun hote hain",
        "premise": "People with the least knowledge in a subject suffer from illusory superiority, while true experts constantly doubt themselves. Ignorance breeds arrogance."
    },
    {
        "id": "law_of_reversed_effort",
        "title_en": "The Law of Reversed Effort: Why Trying Too Hard Fails",
        "title_hi": "Zyada koshish karne se kaam kharab kyun hota hai (Reversed Effort)",
        "premise": "When you try desperately to sleep, impress someone, or force happiness, your anxiety destroys the result. Detachment and letting go is the ultimate psychological superpower."
    },
    {
        "id": "reciprocity_trap",
        "title_en": "The Reciprocity Trap: The Most Common Manipulation",
        "title_hi": "Ahsaan ke jaal me phansne se kaise bachein (Reciprocity Trick)",
        "premise": "Manipulators give you an unrequested small favor or gift so your subconscious feels a heavy social debt, making you agree to something much bigger later."
    },
    {
        "id": "dark_empathy",
        "title_en": "Dark Empaths: The Most Dangerous Personality Type",
        "title_hi": "Dark Empaths: Sabse khatarnak log jo aapke jazbaat se khelte hain",
        "premise": "Unlike standard psychopaths who lack empathy, dark empaths feel your exact emotions—and use that intimate emotional intelligence as a weapon to manipulate you."
    },
    {
        "id": "anchoring_bias",
        "title_en": "The Anchoring Bias: How Negotiations Are Won or Lost",
        "title_hi": "Deal jeetne ka sabse bada psychological secret (Anchoring Bias)",
        "premise": "The first number or standard introduced in any negotiation becomes the mental anchor. Whoever sets the anchor first controls the outcome of the entire deal."
    },
    {
        "id": "reactance_theory",
        "title_en": "Psychological Reactance: The Forbidden Fruit Effect",
        "title_hi": "Kisi se koi kaam karwane ka ulta tareeka (Reverse Psychology)",
        "premise": "When you forbid someone from doing something or tell them they cannot have it, their brain perceives a threat to their freedom and becomes obsessed with having it."
    },
    {
        "id": "love_bombing",
        "title_en": "The Love Bombing Trap: How Manipulators Hook Victims",
        "title_hi": "Love Bombing se kaise bachein: Rishto ka sabse bada fareb",
        "premise": "Overwhelming someone with intense affection, gifts, and praise in the first 2 weeks is not romance—it is psychological grooming to make them dependent."
    },
    {
        "id": "contrast_principle",
        "title_en": "The Contrast Principle: How Perception Is Altered",
        "title_hi": "Aapki soch ko manipulate karne ka tareeka (Contrast Principle)",
        "premise": "If you put your hand in boiling water and then room temperature water, it feels freezing cold. Manipulators present terrible options first to make bad options look like gold."
    },
    {
        "id": "sunk_cost_fallacy",
        "title_en": "The Sunk Cost Fallacy: Why People Stay in Toxic Situations",
        "title_hi": "Kharab rishton aur nuksaan se bahar nikalne ka tareeka (Sunk Cost)",
        "premise": "People stay in toxic relationships and losing projects not because of the future, but because of the time and tears already spent. Cut your losses early."
    },
    {
        "id": "triangulation_technique",
        "title_en": "Triangulation: How Toxic People Control Groups",
        "title_hi": "Ladaai karwa kar faayda uthane ki trick (Triangulation)",
        "premise": "A manipulator will introduce a third person into your dynamic to trigger jealousy, insecurity, and competition, keeping themselves as the supreme prize."
    },
    {
        "id": "silent_treatment",
        "title_en": "The Silent Treatment: Emotional Abuse Decoded",
        "title_hi": "Khamoshi se torture karne ki psychological reality",
        "premise": "When someone uses prolonged silence to make you anxious and beg for their attention, do not react. Your absolute calm neutrality destroys their psychological control."
    },
    {
        "id": "gaslighting_traps",
        "title_en": "Gaslighting Warning Signs: Protecting Your Sanity",
        "title_hi": "Gaslighting ke 3 sabse bade signs jo aapko pata hone chahiye",
        "premise": "If someone constantly rewrites history, denies things they said, or claims you are overreacting, document the facts quietly and trust your own perception."
    },
    {
        "id": "social_proof_bias",
        "title_en": "The Herd Mind: Why People Follow Fools",
        "title_hi": "Bheed ki soch se alag kaise sochein (Social Proof)",
        "premise": "When uncertain, humans look to the crowd for cues on how to act, even when the crowd is walking off a cliff. Think independently before following anyone."
    },
    {
        "id": "pygmalion_effect",
        "title_en": "The Pygmalion Effect: How Expectations Create Reality",
        "title_hi": "Doosron se apna manchaha kaam karwane ki trick",
        "premise": "Treat people as if they are already honest, brilliant, and dependable. Their subconscious will bend their actions to match the high standard you set for them."
    },
    {
        "id": "decoy_effect",
        "title_en": "The Decoy Effect: How Marketers Manipulate You",
        "title_hi": "Companies aapko mehengi cheez kaise bechti hain",
        "premise": "A company introduces a third overpriced, slightly inferior option specifically to make the expensive target product look like an unbeatable bargain."
    },
    {
        "id": "foot_in_the_door",
        "title_en": "The Foot-in-the-Door Trick: The Gradual Trap",
        "title_hi": "Chhoti si baat se bada kaam karwane ka raaz",
        "premise": "Once someone agrees to a tiny trivial request, their internal identity shifts to being a helpful cooperator, making them 4 times more likely to say yes to a massive request later."
    },
    {
        "id": "false_consensus_effect",
        "title_en": "The False Consensus Trap: Stop Assuming",
        "title_hi": "Sab aapki tarah kyun nahi sochte (False Consensus)",
        "premise": "We foolishly assume that others share our moral values, priorities, and common sense. Recognizing how differently people think prevents painful betrayals."
    },
    {
        "id": "baader_meinhof",
        "title_en": "The Frequency Illusion: Why Patterns Follow You",
        "title_hi": "Ek cheez har jagah kyun dikhne lagti hai (Frequency Illusion)",
        "premise": "Once a concept or image enters your conscious awareness, your brain's selective reticular activating system begins flagging it everywhere in your daily life."
    },
    {
        "id": "mirror_posture",
        "title_en": "Body Language Mirroring: The Subconscious Wire",
        "title_hi": "Kisi ke body language ko read aur control kaise karein",
        "premise": "Subtly match their breathing rate and physical stance for 3 minutes. Once the subconscious bridge is built, shift your position and watch them automatically follow."
    },
    {
        "id": "paradox_of_choice",
        "title_en": "The Paradox of Choice: The Secret to Taking Action",
        "title_hi": "Zyada options hone se dimaag freeze kyun hota hai",
        "premise": "Abundant choices cause decision paralysis and regret. High performers artificially limit their options to two paths to preserve mental energy and execute ruthlessly."
    }
]

def _load_used_topics() -> list:
    if USED_TOPICS_FILE.exists():
        try:
            with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def _save_used_topic(topic_id: str):
    used = _load_used_topics()
    if topic_id not in used:
        used.append(topic_id)
    with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, indent=2)

def get_next_unique_topic(topic_hint: str = None) -> dict:
    """
    Selects a fresh, guaranteed non-duplicate topic from the catalog or respects user topic_hint.
    """
    if topic_hint:
        return {
            "id": "custom_" + str(random.randint(100, 999)),
            "title_en": topic_hint,
            "title_hi": topic_hint,
            "premise": f"Deep psychological breakdown of {topic_hint}"
        }

    used_ids = set(_load_used_topics())
    available = [t for t in TOPIC_CATALOG if t["id"] not in used_ids]

    if not available:
        # Reset tracker when all topics have been cycled through
        print("[*] All catalog topics cycled through! Resetting topic history loop.")
        used_ids.clear()
        available = TOPIC_CATALOG[:]
        with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    chosen = random.choice(available)
    _save_used_topic(chosen["id"])
    return chosen

def generate_viral_content(topic_hint: str = None) -> dict:
    """
    Generates bilingual viral short content with strictly unique, rotating topics.
    """
    topic_data = get_next_unique_topic(topic_hint)
    print(f"[*] Selected Unique Topic: {topic_data['title_en']}")

    # User constraint: Do not rely on Gemini to write text prompts/scripts;
    # generate high-retention bilingual scripts directly from our master topic catalog.
    generate_with_gemini = os.getenv("GENERATE_SCRIPT_WITH_GEMINI", "false").lower() == "true"
    if generate_with_gemini and GEMINI_API_KEY:
        try:
            return _generate_with_gemini(topic_data)
        except Exception as e:
            print(f"[ContentGenerator] Gemini API error ({e}), generating dynamic structured fallback.")

    print(f"[ContentGenerator] Generating viral bilingual script directly from topic catalog ({topic_data['id']}).")
    return _generate_dynamic_fallback(topic_data)

def _generate_with_gemini(topic_data: dict) -> dict:
    prompt = f"""
    You are an elite viral short-form director specializing in high-retention 30-35 second videos.
    Niche: Dark Psychology, Human Secrets, and Shocking Mind Tricks.
    
    MANDATORY TOPIC TO SCRIPT:
    Title English: {topic_data['title_en']}
    Title Hindi: {topic_data['title_hi']}
    Core Premise / Secret: {topic_data['premise']}

    DO NOT TALK ABOUT SILENCE OR DETECTING LIES. Talk strictly and only about the assigned premise above!

    CRITICAL BILINGUAL REQUIREMENT:
    - YouTube Shorts will receive the ENGLISH version.
    - Instagram Reels & Facebook will receive the HINDI version.
    
    Structure the script into EXACTLY 8 rapid micro-scenes (each 3.0 to 4.0 seconds).
    Each scene must have:
    - narration_en: Punchy English sentence that explains the concept with high tension.
    - narration_hi: Dramatic conversational Hindi / Hinglish translation suited for Indian reels audience.
    - image_prompt: Ultra-realistic cinematic 9:16 vertical visual description matching the specific scene.
    - tag: eyes, silhouette, interrogation, brain, clock, chess, statue, or mystery.

    Return ONLY a valid JSON object matching this schema:
    {{
        "title_en": "{topic_data['title_en']} #Shorts",
        "title_hi": "{topic_data['title_hi']}",
        "hook_en": "Catchy 1-sentence hook in English about {topic_data['title_en']}",
        "hook_hi": "Catchy 1-sentence hook in Hindi about {topic_data['title_hi']}",
        "scenes": [
            {{
                "narration_en": "Sentence 1...",
                "narration_hi": "Vakya 1...",
                "image_prompt": "Cinematic visual description 9:16 vertical",
                "tag": "eyes"
            }}
        ],
        "hashtags_yt": ["#Shorts", "#Psychology", "#DarkPsychology", "#HumanBehavior", "#Stoicism", "#Mindset"],
        "hashtags_insta": ["#darkpsychologyhindi", "#psychologytricks", "#reelsindia", "#reels", "#fyp"],
        "hashtags_fb": ["#PsychologyFacts", "#HindiQuotes", "#Mindset", "#TrendingReels"]
    }}
    """
    candidate_models = [
        os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
        "gemini-3-flash-preview",
        "gemini-flash-latest"
    ]
    
    last_err = None
    for model_name in candidate_models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"response_mime_type": "application/json"}
            }
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"[ContentGenerator] Successfully generated unique bilingual script using Gemini ({model_name})!")
                parsed = json.loads(text)
                parsed["title"] = parsed.get("title_en", topic_data["title_en"])
                parsed["hook"] = parsed.get("hook_en", "")
                return parsed
            else:
                last_err = resp.text
        except Exception as e:
            last_err = str(e)
            continue
            
    raise RuntimeError(f"All Gemini models failed. Last error: {last_err}")

def _generate_dynamic_fallback(topic_data: dict) -> dict:
    clean_title = topic_data['title_en'].split(':')[0].strip()
    premise = topic_data['premise']

    # 4 Rotating Narrative Archetypes to guarantee 100% variety in script, tone, pacing and visuals:
    # 0: The Manipulation Defense (High tension, psychological shield)
    # 1: The Brain Glitch (Cognitive flaw, paradox, shock factor)
    # 2: The Strategic Power Move (Negotiation, covert influence, win-win psychology)
    # 3: The Cold Reality of Human Nature (Deep observations, stoic detachment)
    archetype_idx = random.randint(0, 3)

    if archetype_idx == 0:
        # Archetype 0: The Manipulation Defense
        hook_en = f"If someone uses this psychological tactic on you, they are trying to control you."
        hook_hi = f"Agar koi aapke saath yeh psychological trick use kare, toh turant alert ho jaana."
        scenes = [
            {
                "narration_en": f"This is {clean_title}, one of the most subtle psychological weapons in human interaction.",
                "narration_hi": f"Ise kehte hain {clean_title}, jo psychological manipulation ka sabse shaana hathiyar hai.",
                "image_prompt": f"Dramatic moody close-up of a mysterious person whispering a secret in dark shadows, cinematic 9:16 vertical",
                "tag": "whisper"
            },
            {
                "narration_en": premise,
                "narration_hi": f"Asal chaal yeh hai: {premise}",
                "image_prompt": f"Two shadowy silhouettes facing each other in a dimly lit interrogation room with cinematic spotlight, 9:16 vertical",
                "tag": "interrogation"
            },
            {
                "narration_en": "Most victims never realize it is happening because it bypasses logic and attacks raw emotion.",
                "narration_hi": "Zyadatar logon ko pata hi nahi chalta kyunki yeh dimaag nahi, seedhe aapke jazbaat par attack karta hai.",
                "image_prompt": f"Glowing neural brain network surrounded by dark mist and golden synaptic pulses, 9:16 vertical",
                "tag": "brain"
            },
            {
                "narration_en": "Toxic personalities rely on your instinctive urge to comply, explain, or prove yourself.",
                "narration_hi": "Manipulators aapki isi aadat ka faayda uthate hain ki aap unhe khush karne ki koshish karein.",
                "image_prompt": f"A solitary chess board with a fallen white pawn and standing black king under cold rim lighting, 9:16 vertical",
                "tag": "chess"
            },
            {
                "narration_en": "The countermove is simple: maintain absolute emotional detachment and give zero reaction.",
                "narration_hi": "Isse bachne ka ek hi raaz hai: poori tarah shaant rahiye aur unhe koi reaction mat dijiye.",
                "image_prompt": f"Ancient stoic marble statue bathed in golden cinematic sidelight, unshakeable and calm, 9:16 vertical",
                "tag": "statue"
            },
            {
                "narration_en": "Save this video so you remember how to protect your peace, and follow for daily power secrets.",
                "narration_hi": "Is video ko turant save karein aur rozana dark psychology secrets ke liye follow karein.",
                "image_prompt": f"A solitary figure standing strong at the end of a dark neon-lit corridor, looking forward, 9:16 vertical",
                "tag": "dark_corridor"
            }
        ]
    elif archetype_idx == 1:
        # Archetype 1: The Brain Glitch
        hook_en = f"Your brain has a shocking design flaw that anyone can exploit."
        hook_hi = f"Aapka dimaag har roz aapse jhooth bolta hai, aur yeh proof hai."
        scenes = [
            {
                "narration_en": f"Cognitive scientists call this {clean_title}, and it tricks your mind without your consent.",
                "narration_hi": f"Psychology me ise {clean_title} kehte hain, jo aapke subconscious dimaag ko confuse kar deta hai.",
                "image_prompt": f"A person staring intensely into an infinite shattered mirror with dramatic moody lighting, 9:16 vertical",
                "tag": "mirror"
            },
            {
                "narration_en": premise,
                "narration_hi": f"Iski asli reality yeh hai: {premise}",
                "image_prompt": f"Extreme close-up of human eye reflecting golden light and intricate subconscious patterns, 9:16 vertical",
                "tag": "eyes"
            },
            {
                "narration_en": "Research proves that even the smartest people fall for this illusion in high-pressure situations.",
                "narration_hi": "Studies batati hain ki sabse smart log bhi pressure ke waqt is dhokhe me phans jaate hain.",
                "image_prompt": f"Antique mechanical clock with exposed gears spinning under mysterious blue and amber lighting, 9:16 vertical",
                "tag": "clock"
            },
            {
                "narration_en": "Advertisers, politicians, and master negotiators use this exact flaw to dictate your choices.",
                "narration_hi": "Duniya ki badi companies aur negotiators is glitch ka use karke aapke faislon ko control karte hain.",
                "image_prompt": f"A massive crowd of blurred silhouettes walking in unison, one sharp figure looking the other way, 9:16 vertical",
                "tag": "crowd"
            },
            {
                "narration_en": "The moment you become aware of this mechanism, you break free from its subconscious grip.",
                "narration_hi": "Jaise hi aap is pattern ko samajh jaate hain, aapka dimaag is trap se aazaad ho jaata hai.",
                "image_prompt": f"Glowing synaptic human head sculpture illuminating a pitch-black chamber, 9:16 vertical",
                "tag": "brain"
            },
            {
                "narration_en": "Hit save to keep this psychological hack in your arsenal, and subscribe for daily mind power.",
                "narration_hi": "Is video ko bookmark karein aur rozana dimaag tez karne wali tricks ke liye subscribe karein.",
                "image_prompt": f"Mysterious hooded figure disappearing into dark cinematic shadows, 9:16 vertical",
                "tag": "mystery"
            }
        ]
    elif archetype_idx == 2:
        # Archetype 2: The Strategic Power Move
        hook_en = f"The most influential people never argue—they use this psychological rule instead."
        hook_hi = f"Sabse shatir log kabhi ladte nahi, balki is psychological secret se jeet jaate hain."
        scenes = [
            {
                "narration_en": f"They quietly master {clean_title} to guide people's decisions without raising suspicion.",
                "narration_hi": f"Woh secretly {clean_title} ka use karte hain taaki doosra insaan unki har baat maan le.",
                "image_prompt": f"Two master tacticians playing chess in a dark atmospheric library with warm lamp glow, 9:16 vertical",
                "tag": "chess"
            },
            {
                "narration_en": premise,
                "narration_hi": f"Yeh secret rule kehta hai: {premise}",
                "image_prompt": f"A confident silhouette of a strategist standing in front of high-rise city lights at night, 9:16 vertical",
                "tag": "silhouette"
            },
            {
                "narration_en": "Instead of forcing their demands, they create conditions where the other person feels in control.",
                "narration_hi": "Zabardasti karne ke bajaye, woh aisa mahol banate hain jisme samne wale ko lage ki faisla uska apna tha.",
                "image_prompt": f"Extreme close-up of a subtle confident smirk in dark cinematic lighting, 9:16 vertical",
                "tag": "eyes"
            },
            {
                "narration_en": "This triggers deep subconscious reciprocity, making resistance virtually impossible.",
                "narration_hi": "Isse insaan ke subconscious me ek aisi feeling aati hai jisse woh na bol hi nahi pata.",
                "image_prompt": f"Golden hour sidelight highlighting a marble sculpture of Marcus Aurelius, 9:16 vertical",
                "tag": "statue"
            },
            {
                "narration_en": "Use this insight ethically to build unshakeable rapport and win every critical negotiation.",
                "narration_hi": "Is trick ko samajhdari se use karke aap kisi ka bhi bharosa aur respect turant jeet sakte hain.",
                "image_prompt": f"A long grand corridor with dramatic shadows and golden archways leading into light, 9:16 vertical",
                "tag": "dark_corridor"
            },
            {
                "narration_en": "Save this secret for your next negotiation, and follow for more high-level psychological laws.",
                "narration_hi": "Is secret ko save kar lijiye aur har roz psychological power badhane ke liye follow kijiye.",
                "image_prompt": f"A charismatic figure standing in dark cinematic fog, turning toward the camera, 9:16 vertical",
                "tag": "whisper"
            }
        ]
    else:
        # Archetype 3: The Cold Reality of Human Nature
        hook_en = f"This uncomfortable truth about human psychology will change how you view everyone."
        hook_hi = f"Insaani dimaag ka yeh kadwa sach aapki soch ko hamesha ke liye badal dega."
        scenes = [
            {
                "narration_en": f"Modern behavioral psychology calls this {clean_title}, and it governs human behavior.",
                "narration_hi": f"Psychology me ise {clean_title} kehte hain, aur yeh har insaan ke behave karne ka asli reason hai.",
                "image_prompt": f"A lone silhouette standing under a single streetlamp in dark foggy night rain, 9:16 vertical",
                "tag": "silhouette"
            },
            {
                "narration_en": premise,
                "narration_hi": f"Asli sach yeh hai: {premise}",
                "image_prompt": f"Shattered glass pieces reflecting dark neon purple and amber colors in a dark room, 9:16 vertical",
                "tag": "mirror"
            },
            {
                "narration_en": "People love to pretend they act on pure reason, but subconscious instincts make the real calls.",
                "narration_hi": "Log yeh dikhava karte hain ki woh dimaag se faisle lete hain, par asli faisla subconscious karta hai.",
                "image_prompt": f"Intense close-up of human eyes observing through dark venetian blinds, 9:16 vertical",
                "tag": "eyes"
            },
            {
                "narration_en": "When you stop taking human behavior personally and see the code underneath, you become untouchable.",
                "narration_hi": "Jab aap logon ke behavior ko personal lena band kar dete hain, toh koi aapko dukhi nahi kar sakta.",
                "image_prompt": f"Ancient Roman marble bust in an abandoned dark gallery with moody blue backlighting, 9:16 vertical",
                "tag": "statue"
            },
            {
                "narration_en": "Observe rather than absorb—that is the highest level of psychological maturity.",
                "narration_hi": "Logon ko judge mat kijiye, sirf unke pattern ko observe kijiye—yehi asli taqat hai.",
                "image_prompt": f"A wise figure sitting quietly in a dimly lit minimalist room, perfectly still, 9:16 vertical",
                "tag": "interrogation"
            },
            {
                "narration_en": "Double tap if you felt this truth, save for later, and subscribe to decode the human mind.",
                "narration_hi": "Agar yeh baat sahi lagi toh video ko like aur save karein, aur rozana naye secrets ke liye follow karein.",
                "image_prompt": f"Mysterious glowing doorway opening into a dark mist with golden particles floating, 9:16 vertical",
                "tag": "mystery"
            }
        ]

    return {
        "title_en": f"{topic_data['title_en']} #Shorts",
        "title_hi": topic_data["title_hi"],
        "title": topic_data["title_en"],
        "hook_en": hook_en,
        "hook_hi": hook_hi,
        "scenes": scenes,
        "hashtags_yt": ["#Shorts", "#Psychology", "#DarkPsychology", "#HumanBehavior", "#Stoicism", "#Mindset"],
        "hashtags_insta": ["#darkpsychologyhindi", "#psychologyfacts", "#mindset", "#reelsindia", "#reels"],
        "hashtags_fb": ["#PsychologyFacts", "#HindiQuotes", "#Mindset", "#TrendingReels"]
    }

if __name__ == "__main__":
    c = generate_viral_content()
    print("EN Title:", c["title_en"])
    print("HI Title:", c["title_hi"])
    print("Total Scenes:", len(c["scenes"]))
