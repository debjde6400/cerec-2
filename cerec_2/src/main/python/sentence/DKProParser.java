package jfr.cerec.sentence;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import jfr.cerec.util.Constants;
import jfr.cerec.util.Globals;

//import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.analysis_engine.AnalysisEngineDescription;
import org.apache.uima.cas.FeatureStructure;
import org.apache.uima.fit.factory.JCasFactory;
import org.apache.uima.fit.pipeline.SimplePipeline;
import org.apache.uima.fit.util.JCasUtil;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.cas.FSArray;


import static org.apache.uima.fit.factory.AnalysisEngineFactory.createEngine;
import static org.apache.uima.fit.factory.AnalysisEngineFactory.createEngineDescription;

import de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS;
import de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token;
import de.tudarmstadt.ukp.dkpro.core.api.syntax.type.constituent.Constituent;
import de.tudarmstadt.ukp.dkpro.core.api.syntax.type.dependency.Dependency;
import de.tudarmstadt.ukp.dkpro.core.maltparser.MaltParser;
//import de.tudarmstadt.ukp.dkpro.core.maltparser.MaltParser;
import de.tudarmstadt.ukp.dkpro.core.opennlp.OpenNlpChunker;
import de.tudarmstadt.ukp.dkpro.core.opennlp.OpenNlpParser;
import de.tudarmstadt.ukp.dkpro.core.opennlp.OpenNlpPosTagger;
import de.tudarmstadt.ukp.dkpro.core.opennlp.OpenNlpSegmenter;

/**
 * 
 * @author Julian Frattini
 * 
 * Wrapper around the natural language sentence annotation, utilizing the INLPService of specmate.
 * The purpose of this class is to formalize natural language sentences and parse them into the
 * specific internal representation, which currently consists of a combination of constituencies and
 * dependencies.
 */

public class DKProParser {	

	private Map<Language, AnalysisEngine> engines;
	private Logger logger;
	
	public DKProParser() {
		logger = Logger.getLogger(DKProParser.class);
		logger.setLevel(Level.OFF);
		//BasicConfigurator.configure();
		
		engines = new HashMap<Language, AnalysisEngine>();
		try {
			createEnglishPipeline();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
		
	private void createEnglishPipeline() throws Exception {
		logger.info("Initializing english NLP pipeline");

		AnalysisEngineDescription segmenter = null;
		AnalysisEngineDescription posTagger = null;
		AnalysisEngineDescription parser = null;
		AnalysisEngineDescription chunker = null;
		AnalysisEngineDescription dependencyParser = null;

		Language lang = Language.en;

		try {
			segmenter = createEngineDescription(OpenNlpSegmenter.class, OpenNlpSegmenter.PARAM_LANGUAGE, lang);
			posTagger = createEngineDescription(OpenNlpPosTagger.class, OpenNlpPosTagger.PARAM_LANGUAGE, lang, OpenNlpPosTagger.PARAM_VARIANT, "maxent");
			chunker = createEngineDescription(OpenNlpChunker.class, OpenNlpChunker.PARAM_LANGUAGE, lang);
			dependencyParser = createEngineDescription(MaltParser.class, MaltParser.PARAM_LANGUAGE, lang);
			parser = createEngineDescription(OpenNlpParser.class, OpenNlpParser.PARAM_PRINT_TAGSET, true, OpenNlpParser.PARAM_LANGUAGE, lang, OpenNlpParser.PARAM_WRITE_PENN_TREE, true, OpenNlpParser.PARAM_WRITE_POS, true);

			AnalysisEngine engine = createEngine(createEngineDescription(segmenter, posTagger, chunker, dependencyParser, parser));

			engines.put(lang, engine);
		} catch (Throwable e) {
			logger.warn("Could not create analys engine via DKPro");
			logger.warn("Reason: " + e.getMessage());
			throw new Exception("OpenNLP NLP service failed when starting. Reason: " + e.getMessage());
		}
	}

	/**
	 * Checks, whether a processing engine has been initialized for this specific language
	 * @param language The language enum of a specific language
	 * @return True, if the engine exists and is properly set up
	 */
	public boolean isEngineAvailable(Language language) {
		return engines.containsKey(language);
	}
	
	/**
	 * Formalize a natural language sentence
	 * @param text The sentence to be formalized
	 * @return Internal, formal representation of the sentence
	 */
	public Sentence createSentence(String text, Language language) {
		AnalysisEngine engine = engines.get(language);
		if(engine == null) {
			return null;
		}

		JCas processed = null;
		try {
			// process the text
			processed = JCasFactory.createJCas();
			processed.setDocumentText(text);
			processed.setDocumentLanguage(language.toString().toLowerCase());
			SimplePipeline.runPipeline(processed, engine);
			
			// depending on the extent of the pipeline, parse the JCas structure into the internal representation
			Fragment root = null;
			
			// parse the constituents into the internal representation
			Collection<Constituent> constituents = JCasUtil.select(processed, Constituent.class);
			if(!constituents.isEmpty()) {
				Constituent topConstituent = constituents.iterator().next();
				root = parseFeatureStructure(topConstituent, 0);
				
				// add the dependencies to the constituents
				Collection<POS> pos = JCasUtil.select(processed, POS.class);
				if(!pos.isEmpty()) {
					refineFragmentsWithPOS(root, pos);
				} else {
					logger.warn("The analysis engine for the language " + language + " does not contain part-of-speech-tagging!");
				}
				
				// add the dependencies to the constituents
				Collection<Dependency> dependencies = JCasUtil.select(processed, Dependency.class);
				if(!dependencies.isEmpty()) {
					parseDependencies(root, dependencies);
				} else {
					logger.warn("The analysis engine for the language " + language + " does not contain dependencies!");
				}

				// create a new sentence object 
				Sentence sentence = new Sentence(Globals.getInstance().getNewSentenceCounter(), root);
				return sentence;
			} else {
				logger.warn("The analysis engine for the language " + language + " does not contain constituents!");
			}
		} catch (Exception e) {
			logger.warn("Unable to parse and analyze sentence.");
			logger.warn("Reason: " + e.getMessage());
			e.printStackTrace();
		}
		return null;
	}
	
	/**
	 * Parses the feature structures of the constituency parser into the internal representation using fragments
	 * @param top Root node of the constituency parser
	 * @return Root node of the internal representation
	 */
	private Fragment parseFeatureStructure(FeatureStructure top, int index) {
		Fragment f = null;
		
		if(top instanceof Token) {
			// tokens represent leaf nodes
			Token token = (Token) top;
			String POStag = token.getPos().getPosValue();
			f = new Leaf(POStag, token.getCoveredText(), token.getBegin(), index);
		} else if (top instanceof Constituent) {
			// constituents represent inner nodes
			Constituent constituent = (Constituent) top;
			f = new Node(constituent.getConstituentType(), constituent.getCoveredText(), index);
			
			// recursively traverse child nodes and add the full tree
			if(constituent.getChildren() != null) {
				FSArray children = constituent.getChildren();
				for(int i = 0; i < children.size(); i++) {
					FeatureStructure child = children.get(i);
					((Node) f).addChild(parseFeatureStructure(child, i));
				}
			}
		}
		
		return f;
	}
	
	private void refineFragmentsWithPOS(Fragment root, Collection<POS> pos) {
		Leaf current = null;
		for(POS p : pos) {			
			current = root.getLeafByBeginIndex(p.getBegin());
			if(current != null) {
				if(current.getCoveredText().contentEquals(p.getCoveredText())) {
					current.setTag(p.getPosValue());
				} 
			}
		}
	}
	
	/**
	 * Parses all dependencies from the JCas object into the leaf elements of the sentence
	 * @param root Root of the parsed sentence
	 * @param dpc Dependency collection of the JCas object
	 */
	private void parseDependencies(Fragment root, Collection<Dependency> dpc) {
		ArrayList<Dependency> dependencies = new ArrayList<Dependency>(dpc);
		
		for(Dependency d : dependencies) {
			Token dependent = d.getDependent();
			Token governor = d.getGovernor();
			String relationType = d.getDependencyType();
			
			Leaf l_dependent = root.getLeafByBeginIndex(dependent.getBegin());
			Leaf l_governor = root.getLeafByBeginIndex(governor.getBegin());
			
			if(l_dependent != null && l_governor != null && relationType != null)
				l_dependent.setGovernor(l_governor, relationType);
		}
		
		// declare the only leaf node without a governor as ROOT node
		ArrayList<Leaf> tokenNodes = root.getAllLeafs();
		ArrayList<Leaf> ungoverned = new ArrayList<Leaf>();
		for(Leaf l : tokenNodes) {
			if(l.getGovernor() == null && l.getDependencyRelationType().isEmpty()) {
				ungoverned.add(l);
			}
		}
		
		if(ungoverned.size() > 1) {
			logger.warn("More than one leaf node is eligible as ROOT  dependency node.");
		} else if(ungoverned.size() < 1) {
			logger.warn("No leaf node is eligible as ROOT dependency node.");
		} else {
			ungoverned.get(0).setDependencyRelationType(Constants.DEPENDENCY_RELATION_TYPE_ROOT);
		}
	}
}

