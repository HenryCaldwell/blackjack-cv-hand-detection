"""
Module for managing a deck of playing cards.

This module provides a CardDeck class that tracks the count of each card in a standard deck. Each card 
(A, 2-10, J, Q, K) is initialized with 4 copies (scaled by deck size). The class maintains a running count using
the Hi-Lo system and offers methods for removing a card, retrieving the current counts of cards, and getting both
the running and true counts.
"""

from typing import Dict
from debugging.logger import setup_logger

logger = setup_logger(__name__)

_CARD_LABELS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

_HI_LO_VALUES = {
  "2": 1,
  "3": 1,
  "4": 1,
  "5": 1,
  "6": 1,
  "7": 0,
  "8": 0,
  "9": 0,
  "10": -1,
  "J": -1,
  "Q": -1,
  "K": -1,
  "A": -1
}

class CardDeck:
  def __init__(self, size: int) -> None:
    """
    Initializes a new CardDeck with a standard count for each card.

    Parameters:
      size (int): The number of decks combined (each deck has 52 cards).
    
    Attributes:
      size (int): The number of decks combined (each deck has 52 cards).
      cards (dict): A dictionary mapping card labels (e.g., "A", "2", ..., "K") to their counts.
      running_count (int): The current running count, updated incrementally on each card removal.
    """
    self.size = size
    self.cards = {label: 4 * size for label in _CARD_LABELS}
    self.running_count = 0
    logger.info("Initialized CardDeck with %d deck(s)", size)

  def remove_card(self, card_label: str) -> bool:
    """
    Removes one instance of the specified card from the deck and updates the running count.
    
    If the card is available (i.e., count > 0), its count is decremented by one and the running count is updated
    using the Hi-Lo system. If the card is not available, no changes are made.
    
    Parameters:
      card_label (str): The label of the card to remove (e.g., "A", "10", "K").
      
    Returns:
      bool: True if a card was successfully removed, False otherwise.
    """
    # Check if the card is available in the deck
    if card_label in self.cards and self.cards[card_label] > 0:
      self.cards[card_label] -= 1  # Decrement the card count by one
      self.running_count += _HI_LO_VALUES.get(card_label, 0)  # Update the running count
      logger.info("Removed card: %s", card_label)
      return True
    else:
      logger.warning("Failed to remove card: %s (card not available)", card_label)
      return False
  
  def get_counts(self) -> Dict[str, int]:
    """
    Retrieves a copy of the current card counts in the deck.
    
    Returns:
      dict: A dictionary containing the card counts, with card labels as keys.
    """
    return self.cards.copy()
  
  def get_running_count(self) -> int:
    """
    Retrieves the current running count of the deck.
    
    Returns:
      int: The current running count, updated using the Hi-Lo system.
    """
    return self.running_count
  
  def get_true_count(self) -> float:
    """
    Calculates the true count of the deck.
    
    The true count is defined as the running count divided by the number of decks remaining. The number of decks
    remaining is computed as the total remaining cards divided by 52.
    
    Returns:
      float: The true count if decks remain, otherwise the running count.
    """
    remaining_cards = sum(self.cards.values())
    decks_remaining = remaining_cards / 52.0

    if decks_remaining > 0:
      return self.running_count / decks_remaining
    else:
      return self.running_count