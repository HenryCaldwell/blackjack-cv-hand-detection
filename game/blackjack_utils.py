"""
Module for blackjack game helper functions.

This module provides helper functions for evaluating blackjack hands.
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