"""
Simple Rule-Based Chatbot - "Nova" (Version 2)
Pynexia Technology - Internship Hands-On Project
Author: Sehar Naz

A terminal chatbot built ONLY on predefined rules:
  1. clean_text()      - normalises raw user input
  2. If-then rules     - regex patterns that extract information
                         (the user's name, feelings) and reply personally
  3. Smart rules       - a calculator, capital cities, a definition
                         dictionary, famous inventors, live time & date
  4. Intent matching   - keyword scoring against a 25-intent map
  5. Memory            - the bot remembers the user's name and
                         uses it, keeping the conversation coherent

Nova answers far more than small talk - maths, general knowledge
and everyday questions - but every answer still comes from a rule
its author wrote. That is what "rule-based" means.

Run:
  python chatbot.py          -> interactive chat
  python chatbot.py --demo   -> scripted sample conversation
  python chatbot.py --test   -> built-in assertion test suite
"""
import random
import re
import string
import sys
from datetime import datetime

BOT_NAME = "Nova"

# ----------------------------------------------------------------------
# 1. INTENT MAP - each intent owns keywords and ready-made responses
# ----------------------------------------------------------------------
INTENTS = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "salam", "aoa", "good morning",
                     "good afternoon", "good evening"],
        "responses": [
            "Hello! I am Nova, your rule-based assistant. Ask me almost anything - or type 'help'.",
            "Hi there! I can chat, calculate, define terms and answer general questions. Try me!",
        ],
    },
    "how_are_you": {
        "keywords": ["how are you", "how do you feel", "how is it going"],
        "responses": [
            "I am just a set of rules, but all my rules are firing happily. How are you?",
        ],
    },
    "bot_identity": {
        "keywords": ["your name", "who are you", "what are you", "are you robot",
                     "are you human", "about yourself"],
        "responses": [
            "I am Nova, a rule-based chatbot written in Python. I do not learn - "
            "I match your words against keywords, rules and knowledge my author wrote.",
        ],
    },
    "creator": {
        "keywords": ["who made you", "who created you", "who built you",
                     "your creator", "your author", "your developer"],
        "responses": [
            "I was created by Sehar Naz as a hands-on project for the Pynexia "
            "Technology internship - every rule I follow was written by her.",
        ],
    },
    "bot_age": {
        "keywords": ["how old are you", "your age", "when were you born",
                     "your birthday"],
        "responses": [
            "I was born the day my code first ran - so I am brand new, and I never age. "
            "Rule-based bots have that one advantage over humans.",
        ],
    },
    "bot_location": {
        "keywords": ["where are you", "where do you live", "your location",
                     "where are you from"],
        "responses": [
            "I live inside this Python program, wherever it runs - right now, inside your terminal. "
            "No rent, no commute.",
        ],
    },
    "internship": {
        "keywords": ["internship", "intern", "pynexia", "training", "join"],
        "responses": [
            "This chatbot is a hands-on project from the Pynexia Technology internship. "
            "Interns here learn by building small AI projects - like the Water Jug search "
            "program and this chatbot.",
        ],
    },
    "python_help": {
        "keywords": ["python", "code", "coding", "programming", "program"],
        "responses": [
            "Python tip: break every problem into small functions. In this very file, "
            "clean_text(), match_intent() and respond() each do exactly one job - "
            "that is why the code is easy to test.",
        ],
    },
    "ai_topics": {
        "keywords": ["artificial intelligence", " ai ", "machine learning",
                     "deep learning", "neural"],
        "responses": [
            "Artificial Intelligence is about making programs act intelligently. "
            "I am the oldest kind of AI - rule-based. Modern AI like machine learning "
            "learns patterns from data instead of following hand-written rules.",
        ],
    },
    "search_algorithms": {
        "keywords": ["bfs", "dfs", "breadth", "depth", "search algorithm",
                     "water jug"],
        "responses": [
            "BFS explores a state space level by level and guarantees the shortest "
            "solution; DFS dives deep first and uses less memory. My author's Water Jug "
            "project measured both: BFS solved it in 4 steps, DFS in 6.",
        ],
    },
    "study_tips": {
        "keywords": ["study", "learn", "tip", "tips", "practice", "exam"],
        "responses": [
            "A study rule that always works: build first, read second. Type every code "
            "sample yourself, change one line, and predict what happens before you run it.",
        ],
    },
    "weather": {
        "keywords": ["weather", "rain", "raining", "sunny", "forecast",
                     "temperature outside"],
        "responses": [
            "Honest answer: I cannot check live weather - I have no internet and no sensors. "
            "A weather app can. What I CAN do is calculate, define and explain - try me!",
        ],
    },
    "sports": {
        "keywords": ["sport", "sports", "cricket", "football", "hockey",
                     "tennis", "athlete"],
        "responses": [
            "Sports are a great topic! Cricket, football, hockey - regular play builds "
            "fitness, focus and teamwork. The golden rule for any sport: consistency "
            "beats intensity.",
        ],
    },
    "entertainment": {
        "keywords": ["movie", "film", "music", "song", "sing", "drama", "actor"],
        "responses": [
            "Movies and music are wonderful - they are how stories travel. I cannot play "
            "anything (I am text-only), but tell me a genre and I will happily chat about it.",
        ],
    },
    "food": {
        "keywords": ["food", "hungry", "eat", "pizza", "biryani", "breakfast",
                     "lunch", "dinner", "recipe"],
        "responses": [
            "Food talk! A balanced plate rule: half vegetables, a quarter protein, "
            "a quarter grains. And if you are cooking biryani - I fully support that decision.",
        ],
    },
    "travel": {
        "keywords": ["travel", "trip", "vacation", "holiday", "tour", "journey"],
        "responses": [
            "Travel tip from my rule book: plan the route, keep documents copied in two "
            "places, and always leave one unplanned hour a day - that is where the best "
            "memories hide.",
        ],
    },
    "gaming": {
        "keywords": ["game", "gaming", "video game", "pubg", "minecraft",
                     "playstation", "xbox"],
        "responses": [
            "Games train reflexes, strategy and patience. My only gaming rule: "
            "for every hour of gaming, give your eyes and back a ten-minute break.",
        ],
    },
    "pakistan": {
        "keywords": ["pakistan", "pakistani"],
        "responses": [
            "Pakistan: founded on 14 August 1947, capital Islamabad, national language Urdu, "
            "currency the rupee, and founder Quaid-e-Azam Muhammad Ali Jinnah. "
            "Ask me 'capital of Pakistan' style questions for other countries too!",
        ],
    },
    "health_tips": {
        "keywords": ["health", "healthy", "fitness", "weight", "diet", "sleep",
                     "exercise daily"],
        "responses": [
            "Three health rules that never expire: sleep 7-8 hours, move your body daily, "
            "and drink water before you feel thirsty. Small habits, repeated, beat big resolutions.",
        ],
    },
    "favourites": {
        "keywords": ["favourite", "favorite"],
        "responses": [
            "My favourite thing? A perfectly matched keyword. My favourite colour is "
            "terminal green, and my favourite food is data - I consume it very responsibly.",
        ],
    },
    "insult": {
        "keywords": ["stupid", "dumb", "idiot", "useless", "bad bot", "shut up",
                     "hate you"],
        "responses": [
            "That is okay - I am a simple rule-based bot, so feedback genuinely helps. "
            "Tell me what I got wrong, and try 'help' to see what I am actually good at.",
        ],
    },
    "help": {
        "keywords": ["help", "options", "menu", "what can you do", "features"],
        "responses": [
            "Lots! Chat with me, tell me your name, ask me to calculate ('what is 24 x 6'), "
            "ask capitals ('capital of Japan'), definitions ('what is photosynthesis'), "
            "inventors ('who invented the telephone'), or the time and date. Type 'bye' to end.",
        ],
    },
    "thanks": {
        "keywords": ["thank", "thanks", "shukriya", "great", "awesome", "nice"],
        "responses": [
            "You are welcome! Rules or not, helping you made my day.",
            "Any time! That is literally what I am programmed for.",
        ],
    },
    "joke": {
        "keywords": ["joke", "funny", "laugh"],
        "responses": [
            "Why did the rule-based chatbot break up with the database? "
            "Too many unresolved queries.",
            "I would tell you a UDP joke, but you might not get it - "
            "and I cannot resend it, I only follow rules.",
        ],
    },
    "farewell": {
        "keywords": ["bye", "goodbye", "quit", "exit", "see you", "allah hafiz"],
        "responses": [
            "Goodbye! Thanks for chatting with me.",
            "See you soon! Type anytime to start a new conversation.",
        ],
    },
}

FALLBACKS = [
    "I do not have a rule for that one yet. But try me on maths, capitals, definitions, "
        "inventors, time, Python, AI, sports, food, travel - or type 'help'.",
    "That is outside my current rule book. My author can add a rule for it - meanwhile, "
        "type 'help' to see everything I do know.",
    "Interesting question! Rule-based bots like me only answer what we are taught. Ask me "
        "a calculation, a capital city, or a 'what is ...' definition instead.",
]

EXIT_WORDS = {"bye", "goodbye", "quit", "exit"}

# ----------------------------------------------------------------------
# 2. KNOWLEDGE BASES - used by the smart rules (section 5)
# ----------------------------------------------------------------------
CAPITALS = {
    "pakistan": "Islamabad", "india": "New Delhi", "bangladesh": "Dhaka",
    "china": "Beijing", "japan": "Tokyo", "nepal": "Kathmandu",
    "sri lanka": "Sri Jayawardenepura Kotte", "afghanistan": "Kabul",
    "iran": "Tehran", "iraq": "Baghdad", "saudi arabia": "Riyadh",
    "uae": "Abu Dhabi", "united arab emirates": "Abu Dhabi",
    "qatar": "Doha", "turkey": "Ankara", "russia": "Moscow",
    "ukraine": "Kyiv", "france": "Paris", "germany": "Berlin",
    "italy": "Rome", "spain": "Madrid", "portugal": "Lisbon",
    "uk": "London", "united kingdom": "London", "england": "London",
    "ireland": "Dublin", "netherlands": "Amsterdam", "switzerland": "Bern",
    "sweden": "Stockholm", "norway": "Oslo", "denmark": "Copenhagen",
    "usa": "Washington, D.C.", "united states": "Washington, D.C.",
    "america": "Washington, D.C.", "canada": "Ottawa", "mexico": "Mexico City",
    "brazil": "Brasilia", "argentina": "Buenos Aires", "egypt": "Cairo",
    "south africa": "Pretoria", "nigeria": "Abuja", "kenya": "Nairobi",
    "australia": "Canberra", "new zealand": "Wellington",
    "indonesia": "Jakarta", "malaysia": "Kuala Lumpur",
    "singapore": "Singapore", "thailand": "Bangkok", "vietnam": "Hanoi",
    "south korea": "Seoul", "korea": "Seoul",
}

DEFINITIONS = {
    "photosynthesis": "the process by which green plants use sunlight, water and carbon dioxide to make "
        "their food (glucose) and release oxygen",
    "gravity": "the force that pulls objects toward each other - on Earth, it is what pulls "
        "everything down toward the planet's centre",
    "evaporation": "the process by which a liquid slowly changes into a gas or vapour, like water drying "
        "up in sunlight",
    "condensation": "the process by which a gas or vapour changes back into a liquid, like droplets "
        "forming on a cold glass",
    "water cycle": "the continuous movement of water between the Earth and the sky through evaporation, "
        "condensation and precipitation (rain)",
    "electricity": "a form of energy carried by the movement of electrons, used to power lights, "
        "machines and almost everything modern",
    "magnet": "an object that attracts iron and some other metals, and has a north and a south pole",
    "volcano": "an opening in the Earth's crust through which lava, ash and gases can erupt from "
        "below the surface",
    "earthquake": "a sudden shaking of the ground caused by movement of rock below the Earth's surface",
    "tsunami": "a series of very large ocean waves, usually caused by an underwater earthquake",
    "solar system": "the Sun and everything bound to it by gravity - eight planets, their moons, "
        "asteroids and comets",
    "black hole": "a region in space where gravity is so strong that nothing, not even light, can "
        "escape from it",
    "atom": "the smallest unit of ordinary matter - everything around you is made of atoms",
    "molecule": "two or more atoms joined together, like a water molecule made of two hydrogen atoms "
        "and one oxygen atom",
    "oxygen": "a gas in the air that humans and animals must breathe to live; it makes up about 21% "
        "of the atmosphere",
    "carbon dioxide": "a gas produced when we breathe out and when fuels burn; plants absorb it for "
        "photosynthesis",
    "vitamin": "a natural substance found in food that the body needs in small amounts to stay healthy",
    "protein": "a nutrient the body uses to build and repair muscles and tissues, found in meat, "
        "eggs, milk, lentils and beans",
    "bacteria": "tiny single-celled living organisms found almost everywhere - most are harmless and "
        "many are helpful",
    "virus": "a tiny particle that can only multiply inside the living cells of an organism, and "
        "can cause illnesses like flu",
    "computer": "an electronic machine that processes data - it takes input, follows instructions "
        "(programs), and produces output",
    "internet": "a worldwide network connecting billions of computers so they can share information "
        "and communicate",
    "robot": "a machine that can carry out tasks automatically, often by following a program or "
        "sensing its surroundings",
    "algorithm": "a step-by-step set of instructions for solving a problem or completing a task - a "
        "recipe for a computer",
    "database": "an organised collection of data stored electronically, so it can be searched, "
        "updated and managed easily",
    "website": "a collection of connected web pages under one address on the internet, like the "
        "pages you open in a browser",
    "smartphone": "a mobile phone that also works as a small computer - it runs apps, browses the "
        "internet and takes photos",
    "democracy": "a system of government in which the people choose their leaders by voting in "
        "elections",
    "economy": "the system by which a country produces, buys and sells goods and services, and "
        "manages its money and resources",
    "pollution": "harmful substances introduced into the air, water or land, which damage the "
        "environment and health",
    "climate change": "long-term changes in Earth's temperatures and weather patterns, largely driven by "
        "human activities in recent times",
    "recycling": "processing used materials like paper, plastic and glass so they can be made into new "
        "products instead of waste",
    "exercise": "physical activity done to keep the body fit and healthy, such as walking, running or "
        "playing sports",
    "meditation": "a practice of focusing the mind - often on breathing - to become calm, clear and "
        "relaxed",
}

INVENTORS = {
    "telephone": "Alexander Graham Bell, in 1876",
    "light bulb": "Thomas Edison, who made the first practical bulb in 1879",
    "bulb": "Thomas Edison, who made the first practical bulb in 1879",
    "computer": "Charles Babbage, who designed the first mechanical computer concept in the 1830s",
    "aeroplane": "the Wright brothers, Orville and Wilbur, in 1903",
    "airplane": "the Wright brothers, Orville and Wilbur, in 1903",
    "penicillin": "Alexander Fleming, in 1928",
    "printing press": "Johannes Gutenberg, around 1440",
    "world wide web": "Tim Berners-Lee, in 1989",
    "internet": "many pioneers - but the World Wide Web on top of it was created by Tim Berners-Lee "
        "in 1989",
}

# ----------------------------------------------------------------------
# 3. TEXT CLEANING - lowercase, strip punctuation, collapse spaces
# ----------------------------------------------------------------------


def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ----------------------------------------------------------------------
# 4. INTENT MATCHING - score every intent by keyword hits, pick best
# ----------------------------------------------------------------------


def match_intent(cleaned):
    best_intent = None
    best_score = 0
    tokens = cleaned.split()
    for intent, data in INTENTS.items():
        score = 0
        for keyword in data["keywords"]:
            key = keyword.strip()
            # Single words must match a whole token (so "ai" does
            # not fire inside "explain"); phrases match as substrings.
            hit = key in tokens if " " not in key else key in cleaned
            if hit:
                # Longer (more specific) phrases weigh more, so
                # "how are you" beats a plain "hello" in the same
                # sentence - specific beats generic on ties.
                score += len(key.split())
        if score > best_score:
            best_intent = intent
            best_score = score
    return best_intent


# ----------------------------------------------------------------------
# 5. IF-THEN RULES - checked BEFORE intent matching.
#    Personal rules extract facts; smart rules compute & look up.
# ----------------------------------------------------------------------

memory = {"user_name": None}

NOT_A_NAME = {"fine", "good", "ok", "okay", "bored", "tired", "hungry",
              "happy", "sad", "busy", "ready", "here", "sorry", "done"}


def personal_rules(text):
    match = re.search(r"my name is ([a-z]+)", text)
    if match:
        name = match.group(1).capitalize()
        memory["user_name"] = name
        return f"Nice to meet you, {name}! I will remember your name. Ask me anything - or type 'help'."

    match = re.search(r"i am ([a-z]+)", text)
    if match and match.group(1) not in NOT_A_NAME:
        name = match.group(1).capitalize()
        memory["user_name"] = name
        return f"Lovely to meet you, {name}! What would you like to talk about?"

    if re.search(r"\bi feel (sad|tired|bored|stressed)\b", text):
        return ("I am sorry to hear that. A small rule for hard days: "
                "one tiny task at a time - momentum beats motivation.")

    if re.search(r"\bi feel (happy|great|good|excited)\b", text):
        return "That is wonderful! Positive energy is the best time to learn something new."

    if re.search(r"\bwhat is my name\b", text):
        if memory["user_name"]:
            return f"Your name is {memory['user_name']} - see, my memory rule works!"
        return "You have not told me yet. Say: 'my name is ...' and I will remember it."

    return None


def _fmt(number):
    return str(int(number)) if float(number).is_integer() else f"{number:.2f}"


def smart_rules(text):
    # --- calculator: "what is 24 x 6", "12 + 5", "10 percent of 250" ---
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:percent|%)\s*of\s*(\d+(?:\.\d+)?)", text)
    if match:
        a, b = float(match.group(1)), float(match.group(2))
        return f"{_fmt(a)} percent of {_fmt(b)} is {_fmt(a * b / 100)}."

    match = re.search(r"table of (\d{1,3})\b", text)
    if match:
        n = int(match.group(1))
        lines = [f"Here is the multiplication table of {n}:"]
        lines += [f"{n} x {i} = {n * i}" for i in range(1, 11)]
        return "\n".join(lines)

    match = re.search(r"(square|cube) of (\d+(?:\.\d+)?)", text)
    if match:
        n = float(match.group(2))
        result = n * n if match.group(1) == "square" else n * n * n
        return f"The {match.group(1)} of {_fmt(n)} is {_fmt(result)}."

    words = (text.replace(" plus ", " + ").replace(" minus ", " - ")
             .replace(" multiplied by ", " * ").replace(" divided by ", " / ")
             .replace(" times ", " * "))
    match = re.search(r"(\d+(?:\.\d+)?)\s*([+\-*/x])\s*(\d+(?:\.\d+)?)", words)
    if match:
        a, op, b = float(match.group(1)), match.group(2), float(match.group(3))
        if op == "/" and b == 0:
            return "Division by zero is undefined - even my rules cannot do that one."
        result = {"+" : a + b, "-": a - b, "*": a * b,
                  "x": a * b, "/": a / b}[op]
        return f"{_fmt(a)} {op} {_fmt(b)} = {_fmt(result)}."

    # --- capital cities: "capital of japan" ---
    match = re.search(r"capital (?:city )?of ([a-z ]+)", text)
    if match:
        country = match.group(1).strip()
        if country in CAPITALS:
            return f"The capital of {country.title()} is {CAPITALS[country]}."
        return (f"I do not know the capital of {country.title()} yet - "
                "my rule book covers 50+ countries, mostly the well-known ones.")

    # --- inventors: "who invented the telephone" ---
    match = re.search(r"who (?:invented|created|discovered) the ([a-z ]+)", text)
    if match:
        thing = match.group(1).strip()
        if thing in INVENTORS:
            return f"The {thing} was credited to {INVENTORS[thing]}."
        return f"I do not have the inventor of the {thing} in my rule book yet."

    # --- live time & date ---
    tokens = text.split()
    if "time" in tokens and ("what" in tokens or "current" in tokens or "now" in tokens):
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."
    if ("date" in tokens or "day" in tokens) and ("today" in tokens or "what" in tokens):
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

    # --- definitions: "what is photosynthesis", "define gravity" ---
    if re.search(r"^(what is|what are|define|explain|meaning of|tell me about)\b", text):
        for term, meaning in DEFINITIONS.items():
            if " " in term:
                hit = term in text
            else:
                hit = term in tokens
            if hit:
                return f"{term.capitalize()}: {meaning}."

    return None


def apply_rules(raw_text):
    text = clean_text(raw_text)
    reply = personal_rules(text)
    if reply is not None:
        return reply
    # Smart rules get a maths-friendly cleaning: the normal cleaner
    # deletes + - * / as punctuation, which would destroy expressions
    # like "12 + 5" before the calculator ever sees them.
    maths = raw_text.lower()
    keep = "+-*/%"
    drop = "".join(c for c in string.punctuation if c not in keep)
    maths = maths.translate(str.maketrans("", "", drop))
    maths = re.sub(r"\s+", " ", maths).strip()
    return smart_rules(maths)


# ----------------------------------------------------------------------
# 6. RESPONSE ENGINE - rules first, then intents, then fallback
# ----------------------------------------------------------------------


def respond(raw_text):
    rule_reply = apply_rules(raw_text)
    if rule_reply is not None:
        return rule_reply

    intent = match_intent(clean_text(raw_text))
    if intent is not None:
        reply = random.choice(INTENTS[intent]["responses"])
        if memory["user_name"] and intent == "farewell":
            reply = f"{reply} (Nice chatting with you, {memory['user_name']}!)"
        return reply

    return random.choice(FALLBACKS)


def is_exit(raw_text):
    return clean_text(raw_text) in EXIT_WORDS or \
        match_intent(clean_text(raw_text)) == "farewell"


# ----------------------------------------------------------------------
# 7. CONVERSATION LOOPS - interactive, scripted demo, and self-tests
# ----------------------------------------------------------------------


def chat():
    print(f"{BOT_NAME}: Hello! I am {BOT_NAME}, a rule-based chatbot.")
    print(f"{BOT_NAME}: Ask me almost anything - type 'help' to see what I can do, or 'bye' to exit.")
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{BOT_NAME}: Goodbye!")
            break
        if not user.strip():
            continue
        print(f"{BOT_NAME}: {respond(user)}")
        if is_exit(user):
            break


DEMO_INPUTS = [
    "Hello!",
    "My name is Sehar",
    "What is my name?",
    "What is 24 x 6?",
    "What is the capital of Japan?",
    "What is photosynthesis?",
    "Who invented the telephone?",
    "What time is it?",
    "Tell me about the internship at Pynexia",
    "What is BFS and DFS?",
    "I feel stressed today",
    "Tell me a joke",
    "asdf qwerty zzz",
    "Thank you!",
    "Bye",
]


def demo():
    random.seed(7)
    print(f"{BOT_NAME}: Hello! I am {BOT_NAME}, a rule-based chatbot.")
    print(f"{BOT_NAME}: Ask me almost anything - type 'help' to see what I can do, or 'bye' to exit.")
    for user in DEMO_INPUTS:
        print(f"You: {user}")
        print(f"{BOT_NAME}: {respond(user)}")
        if is_exit(user):
            break


def run_tests():
    intent_cases = [
        ("Hello!!!", "greeting"),
        ("HELLO, how are you?", "how_are_you"),
        ("What is your name?", "bot_identity"),
        ("who created you?", "creator"),
        ("how old are you?", "bot_age"),
        ("where do you live?", "bot_location"),
        ("Tell me about the internship", "internship"),
        ("I love PYTHON coding", "python_help"),
        ("What is machine learning?", "ai_topics"),
        ("Explain BFS please", "search_algorithms"),
        ("any study tips?", "study_tips"),
        ("how is the weather today?", "weather"),
        ("I love cricket", "sports"),
        ("let us watch a movie", "entertainment"),
        ("I am hungry, want pizza", "food"),
        ("planning a travel trip", "travel"),
        ("do you like gaming?", "gaming"),
        ("tell me about pakistan", "pakistan"),
        ("health and fitness advice", "health_tips"),
        ("what is your favourite colour?", "favourites"),
        ("you are stupid", "insult"),
        ("help me", "help"),
        ("thank you so much", "thanks"),
        ("tell me a funny joke", "joke"),
        ("goodbye", "farewell"),
        ("xyzzy nonsense words", None),
    ]
    passed = 0
    for raw, expected in intent_cases:
        got = match_intent(clean_text(raw))
        assert got == expected, f"{raw!r}: expected {expected}, got {got}"
        passed += 1

    assert clean_text("  HeLLo,   World!! ") == "hello world"
    passed += 1

    memory["user_name"] = None
    reply = respond("my name is sehar")
    assert memory["user_name"] == "Sehar", "name rule failed"
    assert "Sehar" in reply
    passed += 1

    reply = respond("what is my name?")
    assert "Sehar" in reply, "memory recall failed"
    passed += 1

    smart_cases = [
        ("what is 24 x 6?", "144"),
        ("calculate 12 + 5", "17"),
        ("what is 10 percent of 250?", "25"),
        ("square of 9", "81"),
        ("table of 7", "7 x 10 = 70"),
        ("what is the capital of japan?", "Tokyo"),
        ("capital of pakistan", "Islamabad"),
        ("what is photosynthesis?", "sunlight"),
        ("define gravity", "force"),
        ("who invented the telephone?", "Bell"),
        ("what time is it?", ":"),
        ("what is the date today?", str(datetime.now().year)),
    ]
    for raw, expected_part in smart_cases:
        reply = respond(raw)
        assert expected_part in reply, f"{raw!r}: expected {expected_part!r} in {reply!r}"
        passed += 1

    print(f"ALL TESTS PASSED ({passed}/{passed} checks)")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    elif "--test" in sys.argv:
        run_tests()
    else:
        chat()
