#package jfr.cerec.util;

class GlobalConfiguration:

  '''/**
   * Option for incremental sentence structures: the sentence structure generator will only generate
   * as many nodes in the structure tree, as it is necessary to differentiate from all existing patterns
   * as well as all previously discarded non-causal sentences
   */
  public static final boolean incrementalSentenceStructure = true;

  /**
   * This parameter defines, what kind of tag is used when searching for an eligible differentiator.
   * The following options are available:
   *  - useDependencyTagsForEligibilityCheck = true : dependency tags
   *  - useDependencyTagsForEligibilityCheck = false : part-of-speech tags
   */
  public static boolean useDependencyTagsForEligibilityCheck;

  /**
   * Log levels, where the current log level has to be lower then the log levels of info, warn, and
   * error in order for them to be shown. Log level 0 will permit all log messages to be shown
   */
  public static final int CURRENT_LOG_LEVEL = 100;
  public static final int LOG_LEVEL_INFO = 20;
  public static final int LOG_LEVEL_WARN = 50;
  public static final int LOG_LEVEL_ERROR = 80;

  /**
   * String prefix before all log messages of the CELogger
   */
  public static final String LOG_PREFIX = "cerec";'''

  incrementalSentenceStructure = True
  useDependencyTagsForEligibilityCheck = False

  CURRENT_LOG_LEVEL = 100
  LOG_LEVEL_INFO = 20
  LOG_LEVEL_WARN = 50
  LOG_LEVEL_ERROR = 80


