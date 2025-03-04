"""
Module for interfacing with a Java-based EV (Expected Value) Engine using JPype.

This module provides functions to convert Python data structures into Java-compatible arrays and a wrapper class,
EVEngineWrapper, that initializes the Java Virtual Machine (JVM), loads the EV engine from a specified JAR file,
and calculates EV for various game actions.
"""

import jpype
import jpype.imports
from jpype.types import JInt, JArray
from debugging.logger import setup_logger

logger = setup_logger(__name__)

def _deck_to_java_array(deck):
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

def _hand_to_java_array_list(hand):
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
  ArrayList = jpype.JClass("java.util.ArrayList")  # Retrieve the Java ArrayList class using JPype
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

class EVEngineWrapper:
  """
  A wrapper class for interacting with the Java-based EV Engine.

  This class manages the lifecycle of the Java Virtual Machine (JVM), loads the EV engine
  from the specified JAR file, and exposes a method to calculate the expected value for different
  game actions (stand, hit, double, split).
  """
  def __init__(self, jar_path="java/build/EVEngine.jar", java_class="jsrc.evaluation.EVEngine"):
    """
    Initialize the EVEngineWrapper instance.

    Parameters:
      jar_path (str): The path to the JAR file containing the EV engine.
      java_class (str): The fully qualified Java class name of the EV engine.
    """
    self.jar_path = jar_path
    self.java_class = java_class
    self.started = False
    self._start_jvm()

  def _start_jvm(self):
    """
    Start the Java Virtual Machine (JVM) and initialize the EV engine.

    Checks if the JVM is already started; if not, it starts the JVM using the provided classpath. After the JVM
    is running, the EV engine Java class is loaded, and an instance is created.
    """
    # Check if the JVM is already started to avoid multiple initializations
    if not jpype.isJVMStarted():
      jpype.startJVM(classpath=[self.jar_path])
      logger.info("JVM started with classpath: %s", self.jar_path)
    else:
      logger.info("JVM already started")

    self.EVEngineClass = jpype.JClass(self.java_class)  # Load the EV engine Java class using its fully qualified name
    self.ev_engine = self.EVEngineClass()
    self.started = True

  def calculate_ev(self, action, deck, player_hand, dealer_hand):
    """
    Calculate the expected value (EV) for a given game action using the EV engine.

    The method maps the provided action to a corresponding method in the EV engine, converts the deck and hands
    into Java-compatible formats, and then calls the engine's EV calculation method.

    Parameters:
      action (str): The game action for which to calculate EV (e.g., "stand", "hit", "double", "split").
      deck (dict): A dictionary representing the deck composition.
      player_hand (list of str): The player's hand represented as a list of card strings.
      dealer_hand (list of str): The dealer's hand represented as a list of card strings.

    Returns:
      The expected value calculated by the EV engine.

    Raises:
      ValueError: If the action is not one of the supported actions.
    """
    # Define a mapping from action names to the corresponding EV engine methods
    method_mapping = {
      "stand": self.ev_engine.calculateStandEV,
      "hit": self.ev_engine.calculateHitEV,
      "double": self.ev_engine.calculateDoubleEV,
      "split": self.ev_engine.calculateSplitEV,
    }

    if action not in method_mapping:
      raise ValueError(f"Unknown action: {action}")

    value_counts_java = _deck_to_java_array(deck)
    player_hand_java = _hand_to_java_array_list(player_hand)
    dealer_hand_java = _hand_to_java_array_list(dealer_hand)

    ev = method_mapping[action](value_counts_java, player_hand_java, dealer_hand_java)  # Retrieve the appropriate EV calculation method based on the action and execute it
    return ev

  def shutdown(self):
    """
    Shutdown the Java Virtual Machine (JVM).

    Safely shuts down the JVM if it is running, ensuring that all resources are properly released.
    """
    if jpype.isJVMStarted():
      jpype.shutdownJVM()
      logger.info("JVM shutdown")
