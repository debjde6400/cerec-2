package jfr.cerec.main;

import java.util.ArrayList;

import jfr.cerec.ceg.ICauseEffectGraph;
import jfr.cerec.data.CausalityData;
import jfr.cerec.pattern.IPattern;
import jfr.cerec.sentence.ISentence;

public interface ICauseEffectRecognition {

	/**
	 * Returns all the patterns generated in the training process
	 * @return List of existing patterns
	 */
	public ArrayList<IPattern> getPatterns();
	
	/**
	 * Resets the knowledge database by deleting all existing patterns
	 */
	public void reset();	

	 /* Formalizes a sentence via the configured DKPro sentence parser
	 * @param sentence The sentence in natural language
	 * @return The sentence in formalized form
	 */
	public ISentence formalizeSentence(String sentence);

	/**
	 * Attempts to generate a cause-effect-graph from a sentence
	 * @param sentence The sentence, where the causality shall be extracted
	 * @return A cause-effect-graph, if the sentence is causal and the pattern known
	 */
	public ICauseEffectGraph getCEG(String sentence);
	
	public IPattern getCompliantPattern(String sentence);

	/**
	 * Trains the algorithm with a new sentence pattern
	 * @param sentence A causality example containing a sentence and a cause-effect-graph
	 * @return The result of the training process
	 */
	public CerecResult train(CausalityData sentence);
	
	/**
	 * Checks whether a causality example is valid (cause-/effect-phrase must be a valid substring of the sentence
	 * @param sentence The causality example, which is to be checked
	 * @return True, if the causality example is valid
	 */
	public boolean isExampleValid(CausalityData sentence);

	/**
	 * Stores the state of the patterns database and list of non-causal sentences for restoring
	 */
	public void snapshot();

	/**
	 * Restores a previously snapshotted status of the patterns database and list of non-causal sentences
	 */
	public void restore();
}