import random
import json
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()


# Generate game content using Gemini
def generate_game_content():
    """Use Gemini to generate victim, suspects, alibis, clues, and contradictions"""
    print("\n*** Generating game scenario with AI... ***\n")
    
    prompt = """Generate a murder mystery game scenario in JSON format. Create:
        1. A victim (name and item stolen)
        2. Three unique suspects (name, profession, motive)
        3. Alibis for each suspect
        4. Three clues per suspect
        5. One contradiction per suspect (clue conflicts with alibi)

        Return ONLY valid JSON with this structure:
        {
            "victim": {
                "name": "item name",
                "value": "$X million",
                "location": "location name"
            },
            "suspects": [
                {
                    "name": "suspect name",
                    "profession": "profession",
                    "motive": "motive explanation",
                    "alibi": "alibi statement",
                    "clues": [
                        "clue 1",
                        "clue 2",
                        "clue 3"
                    ],
                    "contradiction": {
                        "clue": "the contradicting clue",
                        "alibi": "the alibi",
                        "explanation": "why this is a contradiction",
                        "points": 50
                    }
                }
            ]
        }

        Make it creative, logical, and interesting!
    """
    
    
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        response_text = response.text
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        game_data = json.loads(json_str)
        return game_data
    except Exception as e:
        print(f"Error generating content: {e}")
        return None


# Display the crime scene
def display_crime_scene(victim):
    print("\n" + "=" * 50)
    print("         CRIME SCENE REPORT")
    print("=" * 50)
    print(f"""
        Location: {victim['location']}
        Stolen Item: {victim['name']}
        Item Value: {victim['value']}
        Time of Theft: 9:30 PM, Friday Night

        CRIME SCENE DETAILS:
        - The vault was locked with a security code
        - Only 4 people had access to the code: the three suspects and the director
        - A security camera malfunction occurred at 9:20 PM
        - A muddy footprint was found near the vault
        - A coffee cup was left behind (fresh, still warm at time of discovery)

        YOUR TASK: Find clues and interrogate the suspects to identify the thief!
    """)
    print("=" * 50 + "\n")


# Display all suspects
def display_suspects(suspects):
    print("\n--- SUSPECTS ---")
    for index, suspect in enumerate(suspects, 1):
        print(f"{index}. {suspect['name']} - {suspect['profession']}")
    print()


# Check for contradictions
def check_contradictions(suspects, clues_found):
    print("\n--- ANALYZING CONTRADICTIONS ---")
    contradictions_found = []
    
    for suspect in suspects:
        contradiction = suspect['contradiction']
        # Check if both the clue and is in the clues found
        if contradiction['clue'] in clues_found:
            contradictions_found.append({
                "suspect": suspect['name'],
                "points": contradiction['points'],
                "explanation": contradiction['explanation']
            })
    
    if len(contradictions_found) == 0:
        print("No contradictions found yet. Keep looking for clues!\n")
        return 0
    else:
        total_points = 0
        for contradiction in contradictions_found:
            print(f"\n*** CONTRADICTION FOUND! ***")
            print(f"Suspect: {contradiction['suspect']}")
            print(f"Issue: {contradiction['explanation']}")
            print(f"Points Awarded: +{contradiction['points']}")
            total_points += contradiction['points']
        print()
        return total_points


# Interrogate a suspect
def interrogate_suspect(suspects, suspect_number, clues_found):
    if suspect_number < 1 or suspect_number > len(suspects):
        print("Invalid suspect number!")
        return
    
    suspect = suspects[suspect_number - 1]
    print(f"\n--- INTERROGATING {suspect['name'].upper()} ---")
    print(f"Profession: {suspect['profession']}")
    print(f"Alibi: {suspect['alibi']}\n")
    
    print("Generated Interrogation Questions and Responses:")
    print("-" * 40)
    print("Q: Where were you during the theft?")
    print(f"A: {suspect['alibi']}\n")
    print("Q: Tell me about yourself and your connection to the stolen item.")
    print(f"A: Motive - {suspect['motive']}\n")
    
    # Add this suspect's clues to the clues found
    print("[New clues discovered during interrogation!]")
    for clue in suspect['clues']:
        if clue not in clues_found:  # Only add if not already collected
            clues_found.append(clue)
            print(f"  + {clue}")
    print()


# Make an accusation
def make_accusation(suspects, accused_number, murderer_index, detective_score):
    if accused_number < 1 or accused_number > len(suspects):
        print("Invalid suspect number!")
        return False, detective_score
    
    accused = suspects[accused_number - 1]
    
    if accused_number - 1 == murderer_index:
        print(f"\n*** CORRECT! ***")
        print(f"{accused['name']} was the thief!")
        print(f"Motive: {accused['motive']}")
        bonus_points = 100
        detective_score += bonus_points
        print(f"Correct Accusation Bonus: +{bonus_points}")
        return True, detective_score
    else:
        print(f"\n*** WRONG! ***")
        print(f"{accused['name']} is not the thief.")
        print("Keep investigating...")
        return False, detective_score


# Main game function
def play_game():
    print("=" * 50)
    print("    MURDER MYSTERY: AI-GENERATED CASE")
    print("=" * 50)
    print()
    
    # Generate game content with Gemini
    game_data = generate_game_content()
    
    # Use fallback if generation fails
    if game_data is None:
        print("NO GEMINI RESPONSE.\n")
        return 0
    
    victim = game_data['victim']
    suspects = game_data['suspects']
    
    # Display crime scene with the generated victim
    display_crime_scene(victim)
    
    # Game setup
    print("A treasure has been stolen!")
    print("Three suspects are under investigation.")
    print("Interrogate them and find out who the thief is!\n")
    
    # Randomly choose thief
    murderer_index = random.randint(0, 2)
    clues_found = []
    detective_score = 0
    
    display_suspects(suspects)
    
    # Game loop
    game_won = False
    interrogations_done = 0
    max_interrogations = 5
    
    while not game_won and interrogations_done < max_interrogations:
        print(f"\n*** DETECTIVE SCORE: {detective_score} points ***\n")
        print("\n--- WHAT DO YOU WANT TO DO? ---")
        print("1. Interrogate a suspect")
        print("2. View clues")
        print("3. Check for contradictions")
        print("4. Make an accusation")
        print("5. Quit game")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            display_suspects(suspects)
            try:
                suspect_num = int(input("Enter suspect number to interrogate: "))
                interrogate_suspect(suspects, suspect_num, clues_found)
                interrogations_done += 1
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "2":
            print("\n--- CLUES COLLECTED ---")
            if len(clues_found) == 0:
                print("No clues collected yet. Interrogate suspects to find clues!")
            else:
                for index, clue in enumerate(clues_found, 1):
                    print(f"{index}. {clue}")
            print()
        
        elif choice == "3":
            contradiction_points = check_contradictions(suspects, clues_found)
            detective_score += contradiction_points
        
        elif choice == "4":
            display_suspects(suspects)
            try:
                accused_num = int(input("Enter suspect number to accuse: "))
                game_won, detective_score = make_accusation(suspects, accused_num, murderer_index, detective_score)
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "5":
            print("\nThanks for playing!")
            return
        
        else:
            print("Invalid choice! Please enter 1, 2, 3, 4, or 5.")
    
    if not game_won:
        print(f"\n*** GAME OVER ***")
        print(f"The thief was: {suspects[murderer_index]['name']}")
        print(f"Motive: {suspects[murderer_index]['motive']}")
    
    print(f"\n*** DETECTIVE SCORE: {detective_score} points ***\n")


# Run the game
if __name__ == "__main__":
    try:
        play_game()
        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again == "yes" or play_again == "y":
            play_game()
        else:
            print("Thanks for playing!")
    
    except Exception as e:
        print(f"Error: {e}")