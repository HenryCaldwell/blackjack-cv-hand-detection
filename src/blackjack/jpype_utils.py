"""
Module for JPype Conversion Utilities.

This module provides helper functions to convert Python data structures into Java-compatible formats
required by the EV engine.
"""

from jpype import JInt, JArray, JClass

def deck_to_java_array(deck):
  """
  Convert a Python dictionary representing a deck into a Java integer array.

  The deck dictionary maps card identifiers to their counts. The conversion logic is as follows:
    - The first element is the count for aces ("A").
    - The next eight elements are counts for cards "2" through "9".
    - The final element aggregates counts for "10", "J", "Q", and "K".

  Parameters:
    deck (dict): Dictionary with keys as card values ("A", "2", ..., "K") and integer counts as values.

  Returns:
    JArray(JInt): A Java array of integers containing the deck counts in the expected order.
  """
  ace_count = deck.get("A", 0)  # Retrieve the count for aces
  digit_counts = [deck.get(str(i), 0) for i in range(2, 10)]  # Retrieve counts for cards 2 to 9
  ten_count = deck.get("10", 0) + deck.get("J", 0) + deck.get("Q", 0) + deck.get("K", 0)  # Aggregate counts for 10, J, Q, K into a single count
  deck_values = [ace_count] + digit_counts + [ten_count]  # Combine the counts into one list
  return JArray(JInt)([JInt(val) for val in deck_values])  # Convert each integer to a JInt and return as a Java int array

def hand_to_java_array_list(hand):
  """
  Convert a Python list representing a hand of cards into a Java ArrayList of integers.

  Each card in the hand is processed:
    - 'A' is converted to the value 1.
    - Numeric strings are converted to their integer value.
    - Face cards (or any non-numeric card other than "A") are assigned a value of 10.

  Parameters:
    hand (list of str): A list of card representations (e.g., ["A", "7", "K"]).

  Returns:
    java.util.ArrayList: A Java ArrayList with the integer values corresponding to each card.
  """
  ArrayList = JClass("java.util.ArrayList")  # Retrieve the Java ArrayList class using JPype
  java_values = ArrayList()  # Create an instance of Java ArrayList to hold card values

  # Process each card in the hand and determine its numerical value
  for card in hand:
    if card.upper() == "A":
      value = 1
    elif card.isdigit():
      value = int(card)
    else:
      value = 10

    java_values.add(JInt(value))  # Add the converted value to the Java ArrayList

  return java_values