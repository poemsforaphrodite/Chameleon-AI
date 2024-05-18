from openai import OpenAI
import random

client = OpenAI()

# Define a dictionary with descriptions for each sport
descriptions = {
    "Football": ["Running", "Goals", "Teams", "Field", "Kicking"],
    "Soccer": ["Dribbling", "Goals", "Teams", "Pitch", "Kicking"],
    "Golf": ["Clubs", "Hole", "Course", "Swinging", "Tee"],
    "Baseball": ["Batting", "Pitching", "Diamond", "Bases", "Home run"],
    "Basketball": ["Dribbling", "Shooting", "Hoop", "Court", "Teams"],
    "Ice Hockey": ["Puck", "Skating", "Goals", "Stick", "Rink"],
    "Sailing": ["Boat", "Wind", "Ocean", "Racing", "Sail"],
    "Squash": ["Racket", "Court", "Ball", "Wall", "Rally"],
    "Tennis": ["Racket", "Net", "Court", "Ball", "Serve"],
    "Badminton": ["Shuttlecock", "Racket", "Net", "Court", "Smash"],
    "Motor Racing": ["Cars", "Track", "Speed", "Lap", "Race"],
    "Wrestling": ["Grappling", "Ring", "Pin", "Throw", "Match"],
    "Lacrosse": ["Stick", "Ball", "Net", "Field", "Goals"],
    "Volleyball": ["Net", "Court", "Spike", "Serve", "Teams"],
    "Triathlon": ["Swimming", "Cycling", "Running", "Race", "Endurance"],
    "Cycling": ["Bicycle", "Race", "Pedaling", "Track", "Speed"]
}

def create_message(prompt):
    """
    Sends a message to the OpenAI API and retrieves the AI's response.
    """
    messages = [{
        "role": "system",
        "content": "You are playing the chameleon board game. Describe the sport's qualities without naming it directly. Do not mention the name of the sport at all. Do not write any of these words: [Football, Soccer, Golf, Baseball, Basketball, Ice Hockey, Sailing, Squash, Tennis, Badminton, Motor Racing, Wrestling, Lacrosse, Volleyball, Triathlon, Cycling]"
    }, {
        "role": "user",
        "content": prompt
    }]
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    return response.choices[0].message.content.strip()

def main():
    words = list(descriptions.keys())
    secret_word = random.choice(words)
    players = ["HUMAN", "AI1", "AI2" , "AI3"]
    chameleon = random.choice(players)
    rounds = 1
    discussions = {player: [] for player in players}  # Store discussions per player

    print("The Chameleon is randomly selected and not disclosed. Game starts now!")
    print("Discuss the secret word subtly without giving it away.\n")

    for round_number in range(rounds):
        print(f"Round {round_number + 1}")
        for player in players:
            prompt = "Enter your discussion input: "
            if player == "HUMAN":
                if chameleon == "HUMAN":
                    HUMAN_input = input(prompt + " (You are the Chameleon, act naturally without the secret word): ")
                else:
                    HUMAN_input = input(prompt + f" (The secret word is '{secret_word}'): ")
                discussions[player].append(HUMAN_input)
            else:
                if player == chameleon:
                    ai_response = create_message("ONLY WRITE ONE WORD. Act naturally without revealing the secret word. Do not name a sport. Do not mention the name of the sport at all.")
                else:
                    ai_response = random.choice(descriptions[secret_word])
                print(f"{player} says: {ai_response}")
                discussions[player].append(ai_response)

        print("\nTime to guess who the Chameleon is!")
        votes = {player: 0 for player in players}
        for player in players:
            if player == "HUMAN":
                vote = input(f"Who do you think the Chameleon is? (Options: {', '.join(players)}): ").strip().upper()
                #print(vote)
                if vote in votes:
                    votes[vote] += 1
            else:
                guess_chameleon_prompt = f"ONLY OUTPUT THE NAME OF THE PLAYER YOU THINK IS THE CHAMELEON. NOT ANYTHING ELSE. Based on the conversation, who do you think the Chameleon is among {', '.join(players)}? Choose one: " + " ".join([f"{p}: {' '.join(discussions[p])}" for p in players])
                ai_chameleon_guess = create_message(guess_chameleon_prompt)
                ai_chameleon_guess = ai_chameleon_guess.strip().upper()
                print(f"{player} thinks the Chameleon is: {ai_chameleon_guess}")
                if ai_chameleon_guess in votes:
                    votes[ai_chameleon_guess] += 1
                    #print(ai_chameleon_guess)
        # for vote in votes:
        #     print(vote)
        suspected_chameleon = max(votes, key=votes.get)
        print(f"Suspected Chameleon is {suspected_chameleon.capitalize()}")
        
        if suspected_chameleon == chameleon:
            print(f"The Chameleon was caught! {chameleon.capitalize()} has one chance to guess the word correctly.")
            if chameleon != "HUMAN":
                guess_prompt = "As the Chameleon, guess the secret word based on the discussion (one word only): " + " ".join([f"{p}: {' '.join(discussions[p])}" for p in players])
                chameleon_guess = create_message(guess_prompt)
                print(f"Chameleon's guess: {chameleon_guess}")
                if chameleon_guess.strip().upper() == secret_word.upper():
                    print("Chameleon guessed correctly! Chameleon wins.")
                else:
                    print("Chameleon guessed incorrectly. Other players win.")
            else:
                HUMAN_guess = input("You are the Chameleon! Guess the secret word (one word only): ").strip().upper()
                if HUMAN_guess == secret_word.upper():
                    print("Chameleon guessed correctly! Chameleon wins.")
                else:
                    print("Chameleon guessed incorrectly. Other players win.")
        else:
            print(f"The Chameleon was not caught. {chameleon.capitalize()} wins.")

        print("\nEnd of round", round_number + 1)
        print("----------------------------")

if __name__ == "__main__":
    main()
