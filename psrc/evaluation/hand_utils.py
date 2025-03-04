"""
Module for hand evaluation utilities.

This module provides helper functions for evaluating blackjack hands. It includes functionality for calculating
the total score of a hand, correctly handling the flexible value of Aces and the fixed value of face cards.
"""

def calculate_hand_score(cards):
  """
  Calculate the total score of a blackjack hand.

  This function computes the hand's score by iterating through each card and adding its value. Face cards
  (non-digit and non-Ace cards) are assigned a value of 10, while numeric cards are converted directly to their
  integer value. Aces are initially counted as 1, then adjusted to 11 if it does not cause the score to exceed 21.

  Parameters:
    cards (list of str): The hand of cards, where each card is represented as a string (e.g., "A", "4", "J").

  Returns:
    int: The total score of the hand according to blackjack rules.
  """
  base_score = 0
  ace_count = 0

  # Loop through each card in the hand to calculate the base score
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