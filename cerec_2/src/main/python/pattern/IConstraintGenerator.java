package jfr.cerec.pattern;

import java.util.ArrayList;

import jfr.cerec.sentence.Fragment;

public interface IConstraintGenerator {

	/**
	 * Determines, if the given type of constraint generator can differentiate the herd from the intruder
	 * @param herd List of accepted fragments, that shall maintain their integrity
	 * @param intruder Fragment that should be differentiated from the herd
	 * @return True, if the given constraint type can differentiate the intruder from the herd
	 */
	public boolean differentiates(ArrayList<Fragment> herd, Fragment intruder);
	
	/**
	 * Generates a constraint that differentiates the herd from the intruder
	 * @param herd List of accepted fragments, that shall maintain their integrity
	 * @param intruder Fragment that should be differentiated from the herd
	 * @return All possible constraints, that when applied to the current node level, will differentiate the herd from the intruder
	 */
	public ArrayList<IConstraint> generateConstraints(ArrayList<Fragment> herd, Fragment intruder);
}
