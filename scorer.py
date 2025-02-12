"""
Module for scoring card hands.

This module provides functions to determine the numeric values of playing cards and to calculate the total score 
of a hand. Special handling for Aces is provided, allowing them to be counted as either 1 or 11 based on the best 
possible outcome.
"""

def get_card_value(card):
  """
  Returns the numeric value for a given card label.
  
  Parameters:
    card (str): The card label (e.g., "A", "2", "J").
  
  Returns:
    int: The numeric score corresponding to the card label.
  """
  # Dictionary mapping card labels to their values
  CARD_VALUES = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
  }
  
  return CARD_VALUES.get(card, 0)

def calculate_hand_score(cards):
  """
  Calculates the total score for a hand of cards.
  
  Parameters:
    cards (list of str): A list of card labels.
  
  Returns:
    int: The total score for the hand, with Aces adjusted optimally.
  """
  total_value = 0
  num_aces = 0
  
  # Calculate initial score and count Aces
  for card in cards:
    total_value += get_card_value(card)

    if card == "A":
      num_aces += 1

  # Adjust for Aces if possible
  while num_aces > 0 and total_value + 10 <= 21:
    total_value += 10
    num_aces -= 1
  
  return total_value