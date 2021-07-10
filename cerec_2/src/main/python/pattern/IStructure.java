package jfr.cerec.pattern;

import java.util.ArrayList;

import jfr.cerec.sentence.ISentence;

/**
 * 
 * @author Julian Frattini
 * 
 * Interface for the sentence structure. Its main purpose is to prove compliance
 * to a sentence. It is different to the internal representation of a sentence mainly
 * because it lacks all leaf nodes of a sentence's tree nodes.
 */

public interface IStructure {
	/**
	 * Yields the root node of the sentence structure's tree
	 * @return The root node of the sentence structure
	 */
	public IStructureElement getRoot();
	
	/**
	 * Checks equality to a different sentence structure
	 * @param other The sentence structure with which this one is compared
	 * @return True, if the two sentence structures are equal
	 */
	public boolean equals(IStructure other);
	
	/**
	 * Checks if a sentence is compliant to this sentence structure
	 * @param candidate The sentence which may be compliant to this structure
	 * @return True, if the inner nodes of the given candidate structure equals this sentence structure's nodes
	 */
	public boolean compliedBy(ISentence candidate);
	
	/**
	 * Attempts to differentiate the intruding sentence from the accepted sentences by establishing constraints
	 * @param accepted The list of all sentences, that are accepted by this pattern
	 * @param intruder The sentence, that is erroneously compliant to this structure
	 * @param constraintGenerators List of constraint generators that may differentiate the sentences
	 * @return If the process was successful a list of specification proposals, null if not
	 */
	public ArrayList<SpecificationProposal> differentiate(ArrayList<ISentence> accepted, ISentence intruder, ArrayList<IConstraintGenerator> constraintGenerators);
	
	/**
	 * Only for incremental structures: increase the precision of a structure by adding nodes to the tree
	 * @param accepted List of the accepted sentences, which should be maintained to be compliant to the structure
	 * @param intruder Sentence, where the relevant portion of the structure is erroneously compliant to the structure
	 * @return True, if a specification could differentiate the accepted sentences from the intruder
	 */
	public ArrayList<SpecificationProposal> specifySoftVersus(ArrayList<ISentence> accepted, ISentence intruder);
	
	/**
	 * Only for incremental structure: increasing the precision of a structure by adding nodes to the tree.
	 * In contrast to specifySoftVersus, this method will disregard the compliance of every other accepted sentence
	 * than the first accepted sentence, which is called the prime sentence
	 * @param prime Sentence, which's compliance is to be maintained throughout the specification process
	 * @param otherAccepted Accepted sentences of the pattern excluding the prime sentence
	 * @param intruder Sentence, where the relevant portion of the structure is erroneously compliant to the structure
	 * @return If the process was successful a list of specification proposals, null if not
	 */
	public ArrayList<SpecificationProposal> specifyHardVersus(ISentence prime, ArrayList<ISentence> otherAccepted, ISentence intruder);
	
	/**
	 * Reconsiders the position of each constraint by moving it as far down as possible
	 * @param accepted List of the accepted sentences
	 */
	public abstract void reevaluateConstraints(ArrayList<ISentence> accepted);
	
	/**
	 * Parses the given structure into a human-readable string form
	 * @return The structure in readable form
	 */
	@Override
	public String toString();
	
	/**
	 * Counts the number of elements contained in this structure
	 * @return Number of nodes within the tree structure
	 */
	public int size();
	
	public IStructure clone();
	
	public int getWidth();
}
