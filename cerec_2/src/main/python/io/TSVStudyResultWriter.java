package jfr.cerec.io;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.StringJoiner;

public class TSVStudyResultWriter implements IStudyResultWriter {
	
	private String filepath;
	private PrintWriter writer;
	
	public TSVStudyResultWriter(String filepath) {
		this.filepath = filepath;
	}

	@Override
	public boolean writeStudy(String filename, String[][] results) {
		try {
			writeResult(filename, results);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return false;
	}
	
	private void writeResult(String filename, String[][] results) throws IOException {
		File file = new File(filepath + File.separator + filename + ".tsv");
		
		file.createNewFile();
		writer = new PrintWriter(file) ;
					
		StringJoiner rows = new StringJoiner("\n");
		for(int i = 0; i < results.length; i++) {
			StringJoiner columns = new StringJoiner("\t");
			for(int j = 0; j < results[i].length; j++) {
				columns.add(results[i][j]);
			}
			rows.add(columns.toString());
		}
		writer.write(rows.toString());
		
		writer.close();
	}

}
