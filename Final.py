import random

def monte_carlo_simulation(n_trials, user_parameters, opponent_parameters):
    """Run the Monte Carlo simulation for an end-game scenario."""
    three_point_wins = 0
    foul_strategy_wins = 0

    for _ in range(n_trials):
        # Simulation starts with 30 seconds on the clock
        if simulate_three_point_strategy(user_parameters, opponent_parameters, 30):
            three_point_wins += 1
        if simulate_foul_strategy(user_parameters, opponent_parameters, 30):
            foul_strategy_wins += 1

    # Calculate probabilities
    three_point_win_probability = (three_point_wins / n_trials) * 100
    foul_strategy_win_probability = (foul_strategy_wins / n_trials) * 100

    return three_point_win_probability, foul_strategy_win_probability


def simulate_three_point_strategy(user_parameters, opponent_parameters, time_left):
    """Simulate the 3-point strategy with time deductions."""
    while time_left > 0:
        # Attempt a 3-point shot (takes 4 seconds)
        time_left -= 4
        if time_left <= 0:
            break  # Break if time runs out after a shot attempt
        if random.random() < user_parameters["three_point_probability"]:
            return True  # Win if the shot is made

        # Missed 3-point, opponent gets defensive rebound (7 seconds)
        time_left -= 7
        if time_left <= 0:
            break  # Break if time runs out after an opponent rebound
        if random.random() < opponent_parameters["two_point_probability"]:
            return False  # Opponent scores and wins the game

    # Overtime chance if time runs out and no one scores
    if time_left <= 0 and random.random() < user_parameters["overtime_win_probability"]:
        return True  # Win in overtime

    return False  # Lose


def simulate_foul_strategy(user_parameters, opponent_parameters, time_left):
    """Simulate the foul strategy with time adjustments."""
    while time_left > 0:
        # Fouling takes 2 seconds
        time_left -= 2
        if time_left <= 0:
            break  # Break if time runs out after foul

        # Opponent free throws (no time deduction for the actual free throw attempts)
        points_from_free_throws = 0
        for _ in range(2):  # Two free throws
            if random.random() < opponent_parameters["free_throw_probability"]:
                points_from_free_throws += 1

        # Defensive rebound and subsequent shot (7 seconds)
        time_left -= 7
        if time_left <= 0:
            break  # Break if time runs out after defensive rebound
        if points_from_free_throws < 2:  # Less than 2 points from free throws
            # Attempt a 2-point shot (3 seconds)
            time_left -= 3
            if time_left > 0 and random.random() < user_parameters["two_point_probability"]:
                return True  # Win by scoring 2 points

    return False  # Lose


def get_user_input():
    """Get and validate user input for team parameters."""
    while True:
        try:
            three_point_probability = float(input("Your team's 3-point probability: "))
            if not (0 <= three_point_probability <= 1):
                raise ValueError("Statistic must be between 0 and 1.")
            two_point_probability = float(input("Your team's 2-point probability: "))
            if not (0 <= two_point_probability <= 1):
                raise ValueError("Statistic must be between 0 and 1.")
            overtime_win_probability = float(input("Your team's overtime win probability: "))
            if not (0 <= overtime_win_probability <= 1):
                raise ValueError("Statistic must be between 0 and 1.")
            offensive_rebound_probability = float(input("Your team's offensive rebound probability: "))
            if not (0 <= offensive_rebound_probability <= 1):
                raise ValueError("Statistic must be between 0 and 1.")
            
            # Return valid inputs as a dictionary
            return {
                "three_point_probability": three_point_probability,
                "two_point_probability": two_point_probability,
                "overtime_win_probability": overtime_win_probability,
                "offensive_rebound_probability": offensive_rebound_probability,
            }
        
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a number between 0 and 1.")


def main():
    print("Welcome to the Basketball End-Game Monte Carlo Simulation!")

    print("\nCurrent score: 67-70")

    # Acquire and validate user input
    user_parameters = get_user_input()

    # Randomly generate opponent parameters
    opponent_parameters = {
        "free_throw_probability": random.uniform(0, 1),  # Random free-throw probability
        "two_point_probability": random.uniform(0, 1),  # Random two-point probability
    }

    print("\nRandomly generated opponent parameters:")
    print(f"Opponent's free-throw probability: {opponent_parameters['free_throw_probability']:.2f}")
    print(f"Opponent's 2-point probability: {opponent_parameters['two_point_probability']:.2f}")

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

    three_point_win_probability, foul_strategy_win_probability = monte_carlo_simulation(
        n_trials, user_parameters, opponent_parameters
    )

    # Display simulation results
    print("\nSimulation Results:")
    print(f"Win probability (3-point strategy): {three_point_win_probability:.2f}%")
    print(f"Win probability (Foul strategy): {foul_strategy_win_probability:.2f}%")


if __name__ == "__main__":
    main()
