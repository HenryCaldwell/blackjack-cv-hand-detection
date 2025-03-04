package jsrc.evaluation;

/**
 * Contains all the configurable rules for the blackjack game. Modify these
 * constants to change the behavior of
 * EV calculations.
 */
public final class Config {
  // ###########################################################
  // # Deck and Payout Settings
  // ###########################################################

  // Payout multiplier for a natural blackjack
  public static final double BLACKJACK_ODDS = 1.5;

  // ###########################################################
  // # Player Settings
  // ###########################################################

  // Flag indicating if the dealer hits on a soft 17
  public static final boolean CAN_SURRENDER = true;

  // ###########################################################
  // # Dealer Settings
  // ###########################################################

  // Flag indicating if the dealer hits on a soft 17
  public static final boolean DEALER_HITS_ON_SOFT_17 = true;
  // Flag indicating if the dealer peeks for blackjack
  public static final boolean DEALER_PEAKS_FOR_21 = true;

  // ###########################################################
  // # Splitting and Doubling Rules
  // ###########################################################

  // Flag indicating if a split hand dealt a natural blackjack is considered a
  // blackjack
  public static final boolean NATURAL_BLACKJACK_SPLITS = false;
  // Flag indicating if the player can double down after splitting
  public static final boolean DOUBLE_AFTER_SPLIT = true;
  // Flag indicating if the player can hit after splitting aces
  public static final boolean HIT_SPLIT_ACES = false;
  // Flag indicating if the player can double down after splitting aces
  // This rule requires both HIT_SPLIT_ACES and DOUBLE_AFTER_SPLIT to be true
  public static final boolean DOUBLE_SPLIT_ACES = false;

  // Private constructor to prevent instantiation.
  private Config() {
    throw new UnsupportedOperationException("GameRules is a utility class and cannot be instantiated.");
  }
}
