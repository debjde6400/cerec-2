package jfr.cerec.util;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.StringJoiner;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class PUREConverter {
	
	public static void main(String[] args) throws SAXException, IOException, ParserConfigurationException {
		String filepath = "C:\\Users\\juf\\Documents\\Promotion\\Libraries\\requirements-xml\\XMLZIPFile\\";
		
		File[] files = new File(filepath).listFiles();
		for(File file : files) {
			writePureRequirementsToJson(file.getAbsolutePath());
		}
	}
	
	private static void writePureRequirementsToJson(String filepath) throws SAXException, IOException, ParserConfigurationException {
		String[] fileelements = filepath.split("\\\\");
		String filename = "pure_" + fileelements[fileelements.length-1].split("\\.")[0].split("-")[1].trim();
		System.out.println(filename + ":");
		NodeList requirements = getRequirementsFromDocument(filepath);
		System.out.println(" - requirements: " + requirements.getLength());
		ArrayList<String> sentences = getSentencesFromRequirements(requirements);
		System.out.println(" - sentences: " + sentences.size());
		writeSentencesToJson("src" + File.separator + "main" + File.separator + "resources" + File.separator + "pure_input" + File.separator + filename + ".json", sentences);
	}

	private static NodeList getRequirementsFromDocument(String filepath) throws SAXException, IOException, ParserConfigurationException {
		File file = new File(filepath);
		
		if(file.exists()) {
			DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
			Document document = documentBuilder.parse(file);
			
			NodeList requirements = document.getElementsByTagName("text_body");
			return requirements;
		} else {
			return null;
		}
	}
	
	private static ArrayList<String> getSentencesFromRequirements(NodeList requirements) {
		ArrayList<String> sentences = new ArrayList<String>();
		int ineligible = 0;
		
		for(int i = 0; i < requirements.getLength(); i++) {
			Node requirement = requirements.item(i);
			if(((Element) requirement).getElementsByTagName("enum").getLength() == 0  &&
					((Element) requirement).getElementsByTagName("itemize").getLength() == 0) {
				String textContent = requirement.getTextContent().strip();
				String[] textSentences = textContent.split("\\.|!");
				for(String s : textSentences) {
					s = s.strip();
					if(!s.isEmpty()) {
						s = s.replaceAll("\\r|\\n", " ");
						s = s.replaceAll(" +", " ");
						s = s.replaceAll("\"", "'");
						if(!s.substring(s.length()-1).equals("\\.") || !s.substring(s.length()-1).equals("!"))
							s = s + ".";
						sentences.add(s);
					}
				}
			} else {
				//System.out.println("The following sentence is more complex:" + requirement.getTextContent());
				ineligible++;
			}
		}
		System.out.println(" - ineligible: " + ineligible);
		return sentences;
	}
	
	private static void writeSentencesToJson(String filepath, ArrayList<String> sentences) throws FileNotFoundException {
		try (PrintWriter out = new PrintWriter(filepath)) {
			out.println("[");
			StringJoiner sj = new StringJoiner(",");
			for(String sentence : sentences) {
				sj.add("\t{\n\t\t\"sentence\": \"" + sentence + "\"\n\t}");
			}
			out.println(sj.toString());
			out.println("]");
			out.close();
		} 
	}
}
