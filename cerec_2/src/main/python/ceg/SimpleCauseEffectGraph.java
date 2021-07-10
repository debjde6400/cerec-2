package jfr.cerec.ceg;

import java.util.ArrayList;

/**
 * 
 * @author Julian Frattini
 * Simple version of a cause-effect-graph only containing one cause-phrase and one effect-phrase.
 * More complex relations like the resolution of conjunctions, negations, or else, is neglected here
 */

@Deprecated
public class SimpleCauseEffectGraph {//implements ICauseEffectGraph {

	private ArrayList<CausalPhrase> causalNodes;
	private CausalPhrase cause;
	private CausalPhrase effect;
	
	public SimpleCauseEffectGraph(String cause, String effect) {
		this.cause = new CausalPhrase(cause);
		this.effect = new CausalPhrase(effect);
		
		causalNodes = new ArrayList<CausalPhrase>();
		causalNodes.add(this.cause);
		causalNodes.add(this.effect);
	}

	public ArrayList<CausalPhrase> getCausalNodes() {
		return causalNodes;
	}
	
	/**
	 * {@inheritDoc}
	 */
	//@Override
	public String getCause() {
		return cause.getPhrase();
	}

	/**
	 * {@inheritDoc}
	 */
	//@Override
	public String getEffect() {
		return effect.getPhrase();
	}
	
	/**
	 * {@inheritDoc}
	 */
	//@Override
	public String getCausePrepared() {
		return prepareExpression(cause.getPhrase());
	}

	/**
	 * {@inheritDoc}
	 */
	//@Override
	public String getEffectPrepared() {
		return prepareExpression(effect.getPhrase());
	}
	
	/**
	 * Counters some NLP-specific processing faults like splitting n't from negated words
	 * @param expression Expression to be corrected
	 * @return cause/effect expression corrected of NLP-processing faults
	 */
	private String prepareExpression(String expression) {
		String result = expression;
		
		if(result.contains("n't")) {
			result = result.replaceAll("n't", " n't");
		}
		if(result.contains("'s")) {
			result = result.replaceAll("'s", " 's");
		}
		
		return result;
	}

	/**
	 * {@inheritDoc}
	 */
	/*@Override
	public boolean equals(ICauseEffectGraph other) {
		CELogger.log().info("Checking compliance between CEG's:");
		CELogger.log().info("  - generated: '" + getCause() + "' -> '" + getEffect() + "'");
		CELogger.log().info("  - given: '" + other.getCausePrepared() + "' -> '" + other.getEffectPrepared() + "'");
		
		
		if(!getCause().equals(other.getCausePrepared())) {
			CELogger.log().warn("ERROR: The causes do not align:");
			CELogger.log().warn("\t- " + getCause());
			CELogger.log().warn("\t- " + other.getCausePrepared());
			return false;
		}
		if(!getEffect().equals(other.getEffectPrepared())) {
			CELogger.log().warn("ERROR: The effects do not align:");
			CELogger.log().warn("\t- " + getEffect());
			CELogger.log().warn("\t- " + other.getEffectPrepared());
			return false;
		}
		return true;
	}*/
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public String toString() {
		return cause.getPhrase() + " -> " + effect.getPhrase();
	}
}
