package jfr.cerec.sentence;

public interface ISentence {

	/**
	 * Provides the constituent root node of this sentence
	 * @return The constituent root fragment of the sentence
	 */
	public Fragment getRootConstituent();
	

	/**
	 * Provides the dependency root node of this sentence
	 * @return The dependency root fragment of the sentence
	 */
	public Leaf getRootDependency();
	
	/**
	 * Converts the fragment structure into a human-readable form
	 * @return The fragment structure of the sentence converted into a String
	 */
	@Override
	public String toString();
	
	/**
	 * Formats the fragments structure disregarding leaf nodes into human-readable output
	 * @param constituent True for constituent structure, false for dependency structure
	 * @return The sentence structure of the fragment
	 */
	public String structureToString(boolean constituent);
}
