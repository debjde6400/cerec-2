package jfr.cerec.pattern;

import jfr.cerec.sentence.ISentence;

public interface IStructureGenerator {
	
	/**
	 * Generates the sentence structure of this sentence by disregarding leaf nodes
	 * @param sentence Sentence, from which the structure shall be generated
	 * @return The sentence structure of this sentence
	 */
	public IStructure generateStructure(ISentence sentence);
}
