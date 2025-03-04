"""
Module for interfacing with a Java-based EV (Expected Value) Engine using JPype.

This module provides the EVEngineWrapper class, which manages the Java Virtual Machine (JVM) lifecycle, loads the
EV engine from a specified JAR file, and calculates expected values for various blackjack actions (e.g., stand,
hit, double, split).
"""

import jpype
from blackjack.jpype_utils import deck_to_java_array, hand_to_java_array_list
from debugging.logger import setup_logger

logger = setup_logger(__name__)

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

    value_counts_java = deck_to_java_array(deck)
    player_hand_java = hand_to_java_array_list(player_hand)
    dealer_hand_java = hand_to_java_array_list(dealer_hand)

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
