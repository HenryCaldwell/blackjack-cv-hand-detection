package java.evaluation;

/**
 * Contains all the configurable rules for the blackjack game. Modify these
 * constants to change the behavior of
 * EV calculations.
 */
public final class GameRules {
  // ###########################################################
  // # Deck and Payout Settings
  // ###########################################################

  // The number of standard decks used in the game (valid values: 1 - 8).
  public static final int NUMBER_OF_DECKS = 6;
  // The payout multiplier for a natural blackjack.
  public static final double BLACKJACK_ODDS = 1.5;

  // ###########################################################
  // # Player Settings
  // ###########################################################

  // Determines if the player is allowed to surrender as their first move.
  public static final boolean CAN_SURRENDER = true;

  // ###########################################################
  // # Dealer Settings
  // ###########################################################

  // Determines if the dealer will hit on a soft 17.
  public static final boolean DEALER_HITS_ON_SOFT_17 = true;
  // Determines if the dealer will check ("peek") for blackjack when showing an
  // ace or a ten-value card.
  public static final boolean DEALER_PEAKS_FOR_21 = true;

  // ###########################################################
  // # Splitting and Doubling Rules
  // ###########################################################

  // Determines if a split hand being dealt a natural 21 is considered a
  // blackjack.
  public static final boolean NATURAL_BLACKJACK_SPLITS = false;
  // Determines if the player is allowed to double after splitting.
  public static final boolean DOUBLE_AFTER_SPLIT = true;
  // Determines if the player is allowed to hit after splitting aces.
  public static final boolean HIT_SPLIT_ACES = false;
  // Determines if the player is allowed to double after splitting aces.
  // Note: This rule requires both HIT_SPLIT_ACES and DOUBLE_AFTER_SPLIT to be
  // true.
  public static final boolean DOUBLE_SPLIT_ACES = false;

  // Private constructor to prevent instantiation.
  private GameRules() {
    throw new UnsupportedOperationException("GameRules is a utility class and cannot be instantiated.");
  }
}
