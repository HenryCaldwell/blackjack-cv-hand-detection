"""
Module for blackjack game helper functions.

This module provides helper functions for evaluating blackjack hands. Functions include determining if a hand is
soft, calculating the hand outcome between the player and the dealer, and (if needed) wrapping or reusing scoring
functions.
"""

def calculate_hand_score(cards):
  """
  Calculates the total score for a hand of cards.
  
  This function adds:
    - 1 for each Ace (initially) and later adds 10 if doing so does not bust the hand.
    - 10 for any face card (K, Q, J).
    - The integer value for numeric cards.
  
  Parameters:
    cards (list of str): A list of card labels (e.g., "A", "2", "J").
    
  Returns:
    int: The optimal total score for the hand.
  """
  base_score = 0
  ace_count = 0

  for card in cards:
    if card == "A":
      ace_count += 1
      base_score += 1
    else:
      base_score += int(card) if card.isdigit() else 10

  # Adjust for Aces
  while ace_count > 0 and base_score + 10 <= 21:
    base_score += 10
    ace_count -= 1

  return base_score

def is_soft_hand(cards):
  """
  Determines if a given hand is soft.

  A hand is soft if it contains at least one Ace that can be counted as 11 without busting. This function
  initially counts all Aces as 1 and then checks if adding 10 to the total would keep it at or below 21.

  Parameters:
    hand_cards (list of str): List of card labels in the hand.
  
  Returns:
    bool: True if the hand is soft, False otherwise.
  """
  base_score = 0
  ace_count = 0

  for card in cards:
      if card == "A":
          ace_count += 1
          base_score += 1
      else:
          base_score += int(card) if card.isdigit() else 10

  return ace_count > 0 and (base_score + 10) <= 21

def evaluate_outcome(player_hand, dealer_hand, is_split, blackjack_odds=1.5, natural_blackjack_splits=False):
  """
  Evaluates the outcome of a blackjack round given the player's and dealer's hands.
  
  Parameters:
    player_hand (list of str): The player's card labels.
    dealer_hand (list of str): The dealer's card labels.
    is_split (bool): True if the player's hand is the result of a split.
    blackjack_odds (float): The payout odds for a natural blackjack (default 1.5).
    natural_blackjack_splits (bool): Whether natural blackjack counts are allowed on split hands.
    
  Returns:
    float: The outcome of the hand:
            1.0 if the player wins,
            -1.0 if the player loses,
            0.0 for a push,
            or blackjack_odds if the player has a natural blackjack (and wins by that rule).
  """
  player_score = calculate_hand_score(player_hand)
  dealer_score = calculate_hand_score(dealer_hand)
  player_hand_size = len(player_hand)
  dealer_hand_size = len(dealer_hand)

  # Determine if the player has a natural blackjack.
  player_natural_blackjack = (player_score == 21 and player_hand_size == 2 and 
                              (not is_split or natural_blackjack_splits))
  # Determine if the dealer has a natural blackjack.
  dealer_natural_blackjack = (dealer_score == 21 and dealer_hand_size == 2)

  if player_natural_blackjack and dealer_natural_blackjack:
    return 0.0
  elif player_natural_blackjack:
    return blackjack_odds
  elif dealer_natural_blackjack:
    return -1.0
  elif player_score > 21:
    return -1.0
  elif dealer_score > 21:
    return 1.0
  elif player_score > dealer_score:
    return 1.0
  elif player_score < dealer_score:
    return -1.0
  else:
    return 0.0