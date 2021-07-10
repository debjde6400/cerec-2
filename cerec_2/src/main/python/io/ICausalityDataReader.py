'''package jfr.cerec.io;

import java.io.File;
import java.util.ArrayList;

import jfr.cerec.data.CausalityData;

/**
 *
 * @author Julian Frattini
 *
 * Interface for reader classes, which read causality examples.
 */

public interface ICausalityDataReader {

	/**
	 * Initializes the reader with a filename
	 * @param filename Location of the file containing the causality examples
	 */
	public void initialize(String filename);

	/**
	 * Initializes the reader with a file
	 * @param examplefile File containing the causality examples
	 */
	public void initialize(File examplefile);

	/**
	 * Checks, if the reader has been correctly initialized and is ready to use
	 * @return True, if the reader has been initialized and is ready to use
	 */
	public boolean isInitialized();

	/**
	 * Reads the causality examples, if the reader was correctly initialized, and returns them
	 * @return Set of causality examples
	 */
	public ArrayList<CausalityData> readExamples();
}
'''