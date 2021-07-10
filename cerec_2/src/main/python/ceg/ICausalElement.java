package jfr.cerec.ceg;

import jfr.cerec.genetics.ICommandGenerator;
import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.ISentence;

public abstract class ICausalElement {
	
	/**
	 * Creates a pattern of a cause-effect graph, where each causal phrase is replaced by
	 * a extraction algorithm capable of extracting the given phrase from the sentence
	 * @param sentence Sentence, of which this cause-effect graph conveys the causality relation
	 * @param extractionAlgorithmGenerator Generator of extraction algorithms
	 * @return The root node of the pattern of a cause-effect graph
	 */
	public abstract ICausalElement createPattern(ISentence sentence, ICommandGenerator extractionAlgorithmGenerator);
	
	/**
	 * Checks whether a construction has been without errors
	 * @return True, if no element of the tree is null
	 */
	public abstract boolean isComplete();
	
	/**.
	 * Resolves a cause-effect graph with placeholders to an actual cause-effect graph by
	 * replacing placeholders by the phrases extracted from the placeholder's extractors
	 * @param root Root node of the sentence
	 * @return The root node of the cause-effect graph generated from the sentence
	 */
	public abstract ICausalElement resolvePattern(Fragment root);
	
	/**
	 * Determines whether this causal element is equal to another given causal element
	 * @param other The compared causal element
	 * @return True, if the causal elements are equal
	 */
	public abstract boolean equals(ICausalElement other);
	
	/**
	 * Converts the cause-effect graph portion into human-readable form
	 */
	public abstract String toString(boolean pattern, String indent);
}
