package jfr.cerec.io;

import java.util.ArrayList;

import jfr.cerec.pattern.IPattern;

public interface IPatternWriter {
	
	/**
	 * Writes the list of pattern into a readable format
	 * @param filename The name under which this file will be written
	 * @param patterns The list of patterns to be written
	 * @return True, if the writing process succeeded
	 */
	public boolean writePatterns(String filename, ArrayList<IPattern> patterns);
}
