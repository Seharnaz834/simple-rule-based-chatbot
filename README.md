# Simple Rule-Based Chatbot — "Nova"

**Internship Hands-On Project — Pynexia Technology**
**Submitted by: Sehar Naz**

A terminal chatbot built **only** on predefined rules — no machine learning, no external libraries. Nova cleans what you type, matches it against keyword intents and if-then regex rules, remembers your name — and also calculates, knows 51 capital cities, defines 34 concepts, names famous inventors, and tells the live time and date.

## Assignment Tasks Covered

- Build a simple chatbot using predefined rules, keywords, and conditional patterns.
- Accept user input, clean text, and match keywords using pattern matching.
- Generate responses based on if-then rules and intent mappings.
- Maintain a coherent text-based conversational flow in the terminal.

## How Nova Works (5 stages)

1. **Input** — a chat loop reads a line from the terminal.
2. **Clean** — `clean_text()` lowercases, removes punctuation, collapses spaces.
3. **If-then rules** — regex patterns capture the user's name, recall it later, and respond to feelings.
4. **Smart rules** — a calculator (sums, percentages, squares, multiplication tables), capital cities, a definition dictionary, famous inventors, and live time & date read from the system clock.
5. **Intent match** — 25 intents are scored by keyword hits. Longer, specific phrases outrank generic words, and single-word keywords must match a whole token. No match? A rotating fallback steers the user back to known topics.

**Intents (25):** greeting · how_are_you · bot_identity · creator · bot_age · bot_location · internship · python_help · ai_topics · search_algorithms · study_tips · weather · sports · entertainment · food · travel · gaming · pakistan · health_tips · favourites · insult · help · thanks · joke · farewell

## How to Run

```bash
python chatbot.py           # interactive chat
python chatbot.py --demo    # scripted sample conversation (reproducible)
python chatbot.py --test    # built-in assertion test suite
```

Only Python 3 and its standard library (`re`, `random`, `string`, `sys`) are needed.

## Testing

```
ALL TESTS PASSED (41/41 checks)
```

The suite checks one realistic sentence per intent, a nonsense input that must match no intent, text cleaning, name memory, and 12 smart-rule answers (arithmetic, capitals, definitions, inventors, live time and date). During development it caught three real bugs — a scoring tie, a substring trap (keyword `ai` firing inside `explain`), and the text cleaner deleting the `+` sign before the calculator could see it — all fixed and permanently covered by tests. See the PDF report for details.

## Files in This Repository

- `chatbot.py` — complete source code
- `program_output.txt` — actual verified demo conversation transcript
- `Sehar_Naz_Rule_Based_Chatbot_Pynexia_Technology.pdf` — full 18-page project report

## Sample Conversation

```
Nova: Hello! I am Nova, a rule-based chatbot.
You: My name is Sehar
Nova: Nice to meet you, Sehar! I will remember your name. Ask me anything - or type 'help'.
You: What is my name?
Nova: Your name is Sehar - see, my memory rule works!
You: What is 24 x 6?
Nova: 24 x 6 = 144.
You: What is the capital of Japan?
Nova: The capital of Japan is Tokyo.
You: What is photosynthesis?
Nova: Photosynthesis: the process by which green plants use sunlight, water and carbon dioxide to make their food (glucose) and release oxygen.
You: What is BFS and DFS?
Nova: BFS explores a state space level by level and guarantees the shortest solution; DFS dives deep first...
You: Bye
Nova: See you soon! Type anytime to start a new conversation. (Nice chatting with you, Sehar!)
```
