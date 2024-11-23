import random

def monte_carlo_simulation(n_trials, user_params, opponent_params):
    """Run the Monte Carlo simulation for the end-game scenario."""
    three_pointer_wins = 0
    foul_strategy_wins = 0

    for _ in range(n_trials):
        # Simulate starting with 30 seconds on the clock
        if simulate_three_pointer_strategy(user_params, opponent_params, 30):
            three_pointer_wins += 1
        if simulate_foul_strategy(user_params, opponent_params, 30):
            foul_strategy_wins += 1

    # Calculate percentages
    three_pointer_win_percentage = (three_pointer_wins / n_trials) * 100
    foul_strategy_win_percentage = (foul_strategy_wins / n_trials) * 100

    return three_pointer_win_percentage, foul_strategy_win_percentage


def simulate_three_pointer_strategy(user_params, opponent_params, time_left):
    """Simulate the 3-pointer strategy."""
    time_left -= 4  # Attempting a 3-pointer takes 4 seconds
    if random.random() < user_params["three_point_percentage"]:
        return True  # Win immediately

    # Missed 3-pointer; simulate defensive rebound and subsequent shot
    time_left -= 7  # Defensive rebound and shot attempt
    if time_left > 0 and random.random() < opponent_params["two_point_percentage"]:
        return False  # Opponent scores, lose the game

    # Overtime chance if time runs out and no one scores
    if time_left <= 0 and random.random() < user_params["overtime_win_percentage"]:
        return True  # Win in overtime

    return False  # Lose


def simulate_foul_strategy(user_params, opponent_params, time_left):
    """Simulate the foul strategy."""
    time_left -= 2  # Fouling takes 2 seconds

    # Opponent free throws
    points_from_free_throws = 0
    for _ in range(2):  # Two free throws
        if random.random() < opponent_params["free_throw_percentage"]:
            points_from_free_throws += 1

    # Defensive rebound and subsequent shot
    time_left -= 7  # Defensive possession
    if time_left <= 0:
        return False  # Time ran out

    if points_from_free_throws < 2:  # Less than 2 points from free throws
        time_left -= 3  # Attempting a 2-point shot takes 3 seconds
        if time_left > 0 and random.random() < user_params["two_point_percentage"]:
            return True  # Win by scoring 2 points

    return False  # Lose


def get_user_input():
    """Get and validate user input for team parameters."""
    while True:
        try:
            three_point_percentage = float(input("Your team's 3-point percentage: "))
            if not (0 <= three_point_percentage <= 1):
                raise ValueError("Value must be between 0 and 1.")
            two_point_percentage = float(input("Your team's 2-point percentage: "))
            if not (0 <= two_point_percentage <= 1):
                raise ValueError("Value must be between 0 and 1.")
            overtime_win_percentage = float(input("Your team's overtime win percentage: "))
            if not (0 <= overtime_win_percentage <= 1):
                raise ValueError("Value must be between 0 and 1.")
            offensive_rebound_probability = float(input("Your team's offensive rebound probability: "))
            if not (0 <= offensive_rebound_probability <= 1):
                raise ValueError("Value must be between 0 and 1.")
            
            # Return valid inputs as a dictionary
            return {
                "three_point_percentage": three_point_percentage,
                "two_point_percentage": two_point_percentage,
                "overtime_win_percentage": overtime_win_percentage,
                "offensive_rebound_probability": offensive_rebound_probability,
            }
        
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a value between 0 and 1.")


def main():
    print("Welcome to the Basketball End-Game Monte Carlo Simulation!")

    # Display the score message before user input
    print("\nCurrent score: 67-70")

    # Get and validate user input
    user_params = get_user_input()

    # Randomly generate opponent parameters
    opponent_params = {
        "free_throw_percentage": random.uniform(0, 1),  # Random free-throw percentage
        "two_point_percentage": random.uniform(0, 1),  # Random two-point percentage
    }

    print("\nRandomly generated opponent parameters:")
    print(f"Opponent's free-throw percentage: {opponent_params['free_throw_percentage']:.2f}")
    print(f"Opponent's 2-point percentage: {opponent_params['two_point_percentage']:.2f}")

    # Number of trials
    while True:
        try:
            n_trials = int(input("\nEnter the number of trials for the simulation: "))
            if n_trials <= 0:
                raise ValueError("Number of trials must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a positive integer.")

    print("\nRunning Monte Carlo simulation for basketball end-game scenarios...")

    three_pointer_win_percentage, foul_strategy_win_percentage = monte_carlo_simulation(
        n_trials, user_params, opponent_params
    )

    # Display simulation results
    print("\nSimulation Results:")
    print(f"Win Percentage (3-pointer strategy): {three_pointer_win_percentage:.2f}%")
    print(f"Win Percentage (Foul strategy): {foul_strategy_win_percentage:.2f}%")


if __name__ == "__main__":
    main()
