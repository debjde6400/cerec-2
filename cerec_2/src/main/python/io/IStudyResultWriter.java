package jfr.cerec.io;

public interface IStudyResultWriter {
	
	/**
	 * Writes the content of a study into a given format
	 * @param filename Name of the file to save
	 * @param results Matrix of information to be saved
	 * @return True, if the writing process succeeded
	 */
	public boolean writeStudy(String filename, String[][] results);
}
