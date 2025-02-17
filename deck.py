"""
Module for managing a deck of playing cards.

This module provides a CardDeck class that tracks the count of each card in a standard deck.
Each card (A, 2-10, J, Q, K) is initialized with 4 copies (representing the four suits).
The class offers methods for removing a card (decrementing its count) and retrieving the current counts.
"""

class CardDeck:
  def __init__(self):
    """
    Initializes a new CardDeck with a standard count for each card.
    
    Attributes:
      cards (dict): A dictionary mapping card labels (e.g., "A", "2", ..., "K") to their counts.
    """
    self.cards = {
      "A": 4,
      "2": 4,
      "3": 4,
      "4": 4,
      "5": 4,
      "6": 4,
      "7": 4,
      "8": 4,
      "9": 4,
      "10": 4,
      "J": 4,
      "Q": 4,
      "K": 4
    }

  def remove_card(self, card_label):
    """
    Removes one instance of the specified card from the deck.
    
    If the card is available (i.e., count > 0), its count is decremented by one.
    If the card is not available, a message is printed indicating that no copies are left.
    
    Parameters:
      card_label (str): The label of the card to remove (e.g., "A", "10", "K").
      
    Returns:
      bool: True if a card was successfully removed, False otherwise.
    """
    # Check if the card is available in the deck
    if card_label in self.cards and self.cards[card_label] > 0:
      self.cards[card_label] -= 1 # Decrement the card count by one
      print("Removed one", card_label, "New count:", self.cards[card_label])

      return True
    else:
      print("No", card_label, "left in deck.")
      return False
  
  def get_counts(self):
    """
    Retrieves a copy of the current card counts in the deck.
    
    Returns:
      dict: A dictionary containing the card counts, with card labels as keys.
    """
    return self.cards.copy()