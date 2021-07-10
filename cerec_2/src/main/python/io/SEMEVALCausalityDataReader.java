package jfr.cerec.io;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

import org.apache.commons.io.FileUtils;

import jfr.cerec.data.CausalityData;

public class SEMEVALCausalityDataReader implements ICausalityDataReader {
	
	private String content;

	@Override
	public void initialize(String filename) {
		File file = new File(filename);
		content = "";
		initialize(file);
	}

	@Override
	public void initialize(File file) {
		content = "";
		try {
			content = FileUtils.readFileToString(file, StandardCharsets.UTF_8);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	@Override
	public boolean isInitialized() {
		return !content.isEmpty();
	}

	@Override
	public ArrayList<CausalityData> readExamples() {
		ArrayList<CausalityData> examples = new ArrayList<CausalityData>();
		
		String[] entries = content.split("\r\n\r\n");
		
		for(String entry : entries) {
			String[] lines = entry.split("\r\n");
			
			if(lines.length > 1) {
				CausalityData example = null;
				
				String sentence = lines[0].split("\t")[1];
				sentence = sentence.substring(1, sentence.length()-1);
				String pureSentence = sentence.replaceAll("<...?>", "");
				
				if(lines[1].startsWith("Cause-Effect")) {
					String causeIndicator = lines[1].split("[\\(||\\)]")[1].split(",")[0];
					String effectIndicator = lines[1].split("[\\(||\\)]")[1].split(",")[1];
					
					String cause = getEncapsuled(sentence, causeIndicator);
					String effect = getEncapsuled(sentence, effectIndicator);
					
					example = new CausalityData(pureSentence, cause, effect);
				} else {
					example = new CausalityData(pureSentence);
				}
				
				examples.add(example);
			}
		}
		
		return examples;
	}
	
	private String getEncapsuled(String sentence, String indicator) {
		String result = sentence.split("<" + indicator + ">")[1];
		result = result.split("</" + indicator + ">")[0];
		return result;
	}
}
