package jfr.cerec.io;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import jfr.cerec.pattern.ConstituentStructure;
import jfr.cerec.pattern.DependencyStructure;
import jfr.cerec.pattern.DependencyStructureElement;
import jfr.cerec.pattern.IConstraint;
import jfr.cerec.pattern.IPattern;
import jfr.cerec.pattern.IStructure;
import jfr.cerec.pattern.IStructureElement;
import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.ISentence;
import jfr.cerec.sentence.Leaf;
import jfr.cerec.util.CELogger;

public class GraphmlPatternWriter implements IPatternWriter {

	/**
	 * Path, where the graph file is to be stored
	 */
	private String filepath;
	
	/**
	 * Counters for the unique indices of nodes and edges
	 */
	private int nodeCounter;
	private int edgeCounter;
	
	/**
	 * Color (hex-) values for nodes of specific type
	 */
	private String nodeColorChunk;
	private String nodeColorStructure;
	
	public GraphmlPatternWriter(String filepath) {
		this.filepath = filepath;
		
		nodeColorChunk = "#c0c0c0";
		nodeColorStructure = "#FFCC00";
	}
	
	public void setFilepath(String filepath) {
		this.filepath = filepath;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean writePatterns(String filename, ArrayList<IPattern> patterns) {
		try {
			// initiate the builder
			DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
		    DocumentBuilder docBuilder = docFactory.newDocumentBuilder();
		    Document doc = docBuilder.newDocument();
		    
		    // generate the xml code representing the graphml root
		    GraphmlRoot graphroot = new GraphmlRoot();
		    Element graphRoot = graphroot.getGraphmlCode(doc);
		    
		    // generate the xml code for all patterns and accepted sentences
		    generatePatterns(doc, patterns, graphRoot);
		    
		    // finalize the building process
		    TransformerFactory transformerFactory = TransformerFactory.newInstance();
		    Transformer transformer = transformerFactory.newTransformer();
		    DOMSource source = new DOMSource(doc);
		    
		    // save the file
		    StreamResult result = new StreamResult(new File(filepath + File.separator + filename + ".graphml"));
		    transformer.transform(source, result);
		    System.out.println("File saved!");
		    return true;
		} catch (TransformerConfigurationException e) {
			CELogger.log().error("TransformerConfigurationException in the GraphmlPatternWriter:\n" + e.getMessage());
		} catch (TransformerException e) {
			CELogger.log().error("TransformerException in the GraphmlPatternWriter:\n" + e.getMessage());
		} catch (ParserConfigurationException e) {
			CELogger.log().error("ParserConfigurationException in the GraphmlPatternWriter:\n" + e.getMessage());
		}
		
		return false;
	}
	
	/**
	 * Generates the graphml-compliant xml code representing the patterns including accepted sentences
	 * @param doc DOM document for which the elements are generated
	 * @param patterns List of patterns to be added to the graph
	 * @param root Root node of the graph in the DOM document
	 */
	private void generatePatterns(Document doc, ArrayList<IPattern> patterns, Element root) {
		// calculate the maximum width and depth of patterns in order to synchronize spacing
		int maxStructureWidth = getMaxWidthOfPatternStructures(patterns);
		int maxSentenceDepth = getMaxDepthOfPatternStructures(patterns);
		int maxDependencyCount = getMaxDependencyRelationCount(patterns);
		
		int currentYOffset = 0;
		for(IPattern pattern : patterns) {
			// create a node for the index, so the pattern graph can be identified
			GraphmlNode index = new GraphmlNode(nodeCounter++, String.valueOf(pattern.getIndex()), -200, currentYOffset);
			index.setBorderDisabled(true);
			index.setFontSize(16);
			root.appendChild(index.getGraphmlCode(doc));
			
			// generate the graph for the structure
			generatePatternStructure(doc, pattern, root, currentYOffset);
			
			// generate the graph of each sentence
			int currentXOffset = maxStructureWidth*100 + 200;
			for(ISentence sentence : pattern.getAccepted()) {
				generateSentence(doc, sentence, root, currentXOffset, currentYOffset);
				currentXOffset = currentXOffset + sentence.getRootConstituent().getAllLeafs().size()*100 + 100;
			}
			currentYOffset = currentYOffset + maxSentenceDepth*100 + maxDependencyCount*8 + 100;
		}
	}
	
	/**
	 * Generate a graph for the structure of the pattern
	 * @param doc DOM document for which the elements are generated
	 * @param pattern The pattern to be visualized
	 * @param root Root node of the graph in the DOM document
	 * @param currentY The current y-position at which the structure is to be placed
	 */
	private void generatePatternStructure(Document doc, IPattern pattern, Element root, int currentY) {
		// determine, of which type the structure is and call the according method
		IStructure structure = pattern.getStructure();
		if(structure instanceof DependencyStructure) {
			generateDependencyStructure(doc, root, (DependencyStructureElement) pattern.getStructure().getRoot(), currentY);
		} else if(structure instanceof ConstituentStructure) {
			generateConstituentStructure(doc, root, (ConstituentStructure) pattern.getStructure(), currentY);
		} else {
			CELogger.log().warn("GraphmlPattern does not have a structure generator for the structure type '" + structure.getClass().getSimpleName() + "'");
		}
	}
	
	/**
	 * Generate a graph for a dependency structure of the pattern
	 * @param doc DOM document for which the elements are generated
	 * @param graphmlRoot Root node of the graph in the DOM document
	 * @param root Root node of the dependency structure
	 * @param currentY The current y-position at which the structure is to be placed
	 */
	private void generateDependencyStructure(Document doc, Element graphmlRoot, DependencyStructureElement root, int currentY) {
		// generate the graph nodes for all dependency structure elements (leaf nodes of the sentence) 
		HashMap<DependencyStructureElement, GraphmlNode> nodes = new HashMap<DependencyStructureElement, GraphmlNode>();
		generateDependencyStructureElements(doc, root, currentY, nodes);
		
		// order the elements by their position in the sentence
		ArrayList<DependencyStructureElement> dElements = new ArrayList<DependencyStructureElement>();
		dElements.addAll(nodes.keySet());
		Collections.sort(dElements, (o1, o2) -> o1.getPosition()-o2.getPosition());
		int offsetX = 0;
		for(DependencyStructureElement de : dElements) {
			nodes.get(de).setX(offsetX);
			offsetX = offsetX + 100;
		}
		
		// add all nodes to the graphml code
		for(DependencyStructureElement dse : nodes.keySet()) {
			graphmlRoot.appendChild(nodes.get(dse).getGraphmlCode(doc));
		}
		
		// generate edges
		ArrayList<GraphmlEdge> edges = new ArrayList<GraphmlEdge>();
		generateDependencyStructureEdges(doc, root, edges, nodes);
		Collections.sort(edges, (e1, e2) -> (int) (e1.getDistance()-e2.getDistance()));
		// add a vertical offset to the edges to increase the readability of the graph
		int verticalOffset = 15;
		for(GraphmlEdge edge : edges) {
			edge.setVerticalOffset(verticalOffset);
			verticalOffset = verticalOffset + 8;
		}
		
		// identify and visualize the root node
		GraphmlNode rootDependent = nodes.get(root);
		GraphmlEdge rootEdge = new GraphmlEdge(edgeCounter++, rootDependent, rootDependent);
		rootEdge.setLabel(root.getTag());
		edges.add(rootEdge);
		
		// add all edges to the graphml code
		for(GraphmlEdge edge : edges) {
			graphmlRoot.appendChild(edge.getGraphmlCode(doc));
		}
	}
	
	/**
	 * Generate a graphml node for this dependency structure element and continue recursively with all governed elements
	 * @param doc DOM document for which the elements are generated
	 * @param root Root node of the dependency structure
	 * @param currentY The current y-position at which the structure is to be placed
	 * @param nodes HashMap in which all graphml nodes are stored with respect to their referring dependency structure element
	 */
	private void generateDependencyStructureElements(Document doc, DependencyStructureElement root, int currentY, HashMap<DependencyStructureElement, GraphmlNode> nodes) {
		// create a node with an empty label
		GraphmlNode node = new GraphmlNode(nodeCounter++, "", 0, currentY);
		node.setColor(nodeColorStructure);
		nodes.put(root, node);
		
		// continue recursively
		for(IStructureElement child : root.getChildren()) {
			generateDependencyStructureElements(doc, (DependencyStructureElement) child, currentY, nodes);
		}
	}
	
	/**
	 * Generate all edges between the existing graphml nodes
	 * @param doc DOM document for which the elements are generated
	 * @param parent Current dependency structure element, from which the dependency relations are modeled in graphml edges
	 * @param edges ArrayList in which all graphml edges are stored
	 * @param nodes HashMap in which all graphml nodes are stored with respect to their referring dependency structure element
	 */
	private void generateDependencyStructureEdges(Document doc, DependencyStructureElement parent, ArrayList<GraphmlEdge> edges, HashMap<DependencyStructureElement, GraphmlNode> nodes) {
		GraphmlNode parentNode = nodes.get(parent);
		// create an edge from the parent to every child 
		for(IStructureElement child : parent.getChildren()) {
			GraphmlNode childNode = nodes.get(child);
			
			GraphmlEdge edge = new GraphmlEdge(edgeCounter++, parentNode, childNode);
			edge.setLabel(child.getTag());
			edges.add(edge);
			
			// recursively continue
			generateDependencyStructureEdges(doc, (DependencyStructureElement) child, edges, nodes);
		}
	}
	
	/**
	 * Generate a graph for a dependency structure of the pattern
	 * @param doc DOM document for which the elements are generated
	 * @param graphmlRoot Root node of the graph in the DOM document
	 * @param structure Structure of the pattern
	 * @param y The current y-position at which the structure is to be placed
	 */
	private void generateConstituentStructure(Document doc, Element graphmlRoot, ConstituentStructure structure, int y) {		
		int levelOfMaxWidth = structure.getMaxWidth(true);
		int structureDepth = structure.getRoot().getDepth();
		
		HashMap<IStructureElement, GraphmlNode> nodes = new HashMap<IStructureElement, GraphmlNode>();
		ArrayList<GraphmlEdge> edges = new ArrayList<GraphmlEdge>();
		int currentX = 0;
		int currentY = y + (structureDepth - levelOfMaxWidth)*-100;
		for(IStructureElement nodeAtLevel : structure.getElementsAtLevel(levelOfMaxWidth)) {
			String nodeText = nodeAtLevel.getTag();
			for(IConstraint c : nodeAtLevel.getConstraints()) {
				nodeText = nodeText + "\n" + c.toString();
			}
			
			GraphmlNode node = new GraphmlNode(nodeCounter++, nodeText, currentX, currentY);
			node.setColor(nodeColorStructure);
			currentX = currentX + 100;
			nodes.put(nodeAtLevel, node);
		}
		
		// add all leafs below the widest level
		for(int currentLevel = levelOfMaxWidth+1; currentLevel < structureDepth; currentLevel++) {
			currentY = y + (structureDepth - currentLevel)*-100;
			ArrayList<IStructureElement> currentNodes = structure.getElementsAtLevel(currentLevel);
			for(IStructureElement currentNode : currentNodes) {
				GraphmlNode parent = nodes.get(currentNode.getParent());
				IStructureElement currentParent = currentNode.getParent();
				currentX = parent.getX() + (currentParent.getChildren().indexOf(currentNode) - currentParent.getChildren().size()/2)*100;
				
				GraphmlNode node = new GraphmlNode(nodeCounter++, currentNode.getTag(), currentX, currentY);
				node.setColor(nodeColorStructure);
				nodes.put(currentNode, node);
				
				GraphmlEdge edge = new GraphmlEdge(edgeCounter++, parent, node);
				edge.setDiagonalBreak(true);
				edges.add(edge);
			}
		}
		
		// add all leafs above the widest level
		for(int currentLevel = levelOfMaxWidth-1; currentLevel >= 0; currentLevel--) {
			currentY = y + (structureDepth - currentLevel)*-100;
			ArrayList<IStructureElement> currentNodes = structure.getElementsAtLevel(currentLevel);
			int currentXOffset = 0;
			for(IStructureElement currentNode : currentNodes) {
				if(!currentNode.getChildren().isEmpty()) {
					// if the current node is parenting existing nodes, place it in near vicinity
					currentX = 0;
					for(IStructureElement child : currentNode.getChildren()) {
						currentX = currentX + nodes.get(child).getX();
					}
					currentX = (int) (currentX / currentNode.getChildren().size());
					
					GraphmlNode node = new GraphmlNode(nodeCounter++, currentNode.getTag(), currentX, currentY);
					node.setColor(nodeColorStructure);
					nodes.put(currentNode, node);
					
					for(IStructureElement child : currentNode.getChildren()) {
						GraphmlEdge edge = new GraphmlEdge(edgeCounter++, node, nodes.get(child));
						edge.setDiagonalBreak(true);
						edges.add(edge);
					}
				} else {
					// if the current node is not parenting existing nodes, place it next to the last node
					currentX = currentXOffset;
					GraphmlNode node = new GraphmlNode(nodeCounter++, currentNode.getTag(), currentX, currentY);
					node.setColor(nodeColorStructure);
					nodes.put(currentNode, node);
				}
				currentXOffset = currentX+100;
			}
		}
		
		// add all nodes to the graphml code
		for(IStructureElement fragment : nodes.keySet()) {
			GraphmlNode node = nodes.get(fragment);
			graphmlRoot.appendChild(node.getGraphmlCode(doc));
		}
		// add all edges to the graphml code
		for(GraphmlEdge edge : edges) {
			graphmlRoot.appendChild(edge.getGraphmlCode(doc));
		}
	}
	
	/**
	 * Generates a graph for a single sentence in internal representation form
	 * @param doc DOM document for which the elements are generated
	 * @param sentence The sentence to be visualized
	 * @param graphmlRoot Root node of the graph in the DOM document
	 * @param x The current x-position at which the sentence is to be placed
	 * @param y The current y-position at which the sentence is to be placed
	 */
	private void generateSentence(Document doc, ISentence sentence, Element graphmlRoot, int x, int y) {
		Fragment root = sentence.getRootConstituent();
		ArrayList<Leaf> leafs = root.getAllLeafs();
		Collections.sort(leafs, (l1, l2) -> l1.getPosition()-l2.getPosition()); 
		
		// add all leafs to the list of nodes
		HashMap<Fragment, GraphmlNode> nodes = new HashMap<Fragment, GraphmlNode>();
		int currentX = x;
		for(Leaf leaf : leafs) {
			GraphmlNode node = new GraphmlNode(nodeCounter++, leaf.getTag() + "\n" + leaf.getCoveredText(), currentX, y);
			currentX = currentX + 100;
			nodes.put(leaf, node);
		}
		
		ArrayList<Fragment> currentLevelOfConstituents = new ArrayList<Fragment>();
		currentLevelOfConstituents.addAll(leafs);
		ArrayList<Fragment> nextLevelOfConstituents = new ArrayList<Fragment>();
		ArrayList<Fragment> postponed = new ArrayList<Fragment>();
		ArrayList<GraphmlEdge> edges = new ArrayList<GraphmlEdge>();
		// add all chunks to the list of nodes
		int currentY = y-100;
		while(!currentLevelOfConstituents.isEmpty()) {
			// gather all parent nodes of the current node level that will be processed next
			for(Fragment fragment : currentLevelOfConstituents) {
				if(!nextLevelOfConstituents.contains(fragment.getParent()) && fragment.getParent() != null) {
					nextLevelOfConstituents.add(fragment.getParent());
				}
			}
			
			for(Fragment fragment : nextLevelOfConstituents) {
				// check if all children are already added to the set
				boolean allChildrenAddedToSet = true;
				for(Fragment child : fragment.getChildren()) {
					if(!nodes.containsKey(child)) {
						allChildrenAddedToSet = false;
						break;
					}
				}
				
				if(!allChildrenAddedToSet) {
					// not all children are already added to the set of nodes, postpone adding the parent
					postponed.add(fragment);
				}
			}
			
			for(Fragment fragment : nextLevelOfConstituents) {
				// check if all children are already added to the set of nodes, so the parent can be added
				if(!postponed.contains(fragment)) {
					// calculate the position of the parent node
					int fragmentX = 0;
					for(Fragment child : fragment.getChildren()) {
						fragmentX = fragmentX + nodes.get(child).getX();
					}
					fragmentX = fragmentX / fragment.getChildren().size();
					
					// generate a new graphml node if none exists yet
					GraphmlNode node = null;
					if(!nodes.containsKey(fragment)) {
						node = new GraphmlNode(nodeCounter++, fragment.getTag(), fragmentX, currentY);
						node.setColor(nodeColorChunk);
						nodes.put(fragment, node);
					} else {
						node = nodes.get(fragment);
					}
					
					// add edges from the parent to all children
					for(Fragment child : fragment.getChildren()) {
						GraphmlEdge edge = new GraphmlEdge(edgeCounter++, node, nodes.get(child));
						edge.setDiagonalBreak(true);
						edges.add(edge);
					}
				} 
			}
			
			// continue with the next level of node also regarding postponed nodes
			currentLevelOfConstituents = nextLevelOfConstituents;
			nextLevelOfConstituents = new ArrayList<Fragment>();
			nextLevelOfConstituents.addAll(postponed);
			postponed = new ArrayList<Fragment>();
			
			currentY = currentY - 100;
		}
		
		// generate dependency relations
		ArrayList<GraphmlEdge> dependencyEdges = new ArrayList<GraphmlEdge>();
		generateDependencyStructureEdgesForSentence(doc, sentence.getRootDependency(), dependencyEdges, nodes);
		Collections.sort(edges, (e1, e2) -> (int) (e1.getDistance()-e2.getDistance()));
		int verticalOffset = 15;
		for(GraphmlEdge edge : dependencyEdges) {
			edge.setVerticalOffset(verticalOffset);
			verticalOffset = verticalOffset + 8;
		}
		edges.addAll(dependencyEdges);
		// add edge to ROOT
		GraphmlNode dependencyRoot = nodes.get(sentence.getRootDependency());
		GraphmlEdge rootEdge = new GraphmlEdge(edgeCounter++, dependencyRoot, dependencyRoot);
		rootEdge.setLabel(sentence.getRootDependency().getDependencyRelationType());
		edges.add(rootEdge);
		
		// add all nodes to the graphml code
		for(Fragment fragment : nodes.keySet()) {
			GraphmlNode node = nodes.get(fragment);
			graphmlRoot.appendChild(node.getGraphmlCode(doc));
		}
		// add all edges to the graphml code
		for(GraphmlEdge edge : edges) {
			graphmlRoot.appendChild(edge.getGraphmlCode(doc));
		}
	}
	
	/**
	 * Generates the dependency structure edges for a sentence
	 * @param doc DOM document for which the elements are generated
	 * @param parent Current node parenting governed leaf nodes
	 * @param edges ArrayList of graphml edges where all generated edges will be stored
	 * @param nodes HashMap in which all graphml nodes are stored with respect to their referring dependency structure element
	 */
	private void generateDependencyStructureEdgesForSentence(Document doc, Leaf parent, ArrayList<GraphmlEdge> edges, HashMap<Fragment, GraphmlNode> nodes) {
		GraphmlNode parentNode = nodes.get(parent);
		for(Leaf child : parent.getGoverned()) {
			// create an edge from the parent to every child 
			GraphmlNode childNode = nodes.get(child);
			
			GraphmlEdge edge = new GraphmlEdge(edgeCounter++, parentNode, childNode);
			edge.setLabel(child.getDependencyRelationType());
			edges.add(edge);
			
			// continue recursively
			generateDependencyStructureEdgesForSentence(doc, child, edges, nodes);
		}
	}
	
	/**
	 * Calculate the maximum width of a all pattern structures
	 * @param patterns List of patterns
	 * @return Maximum number of nodes on one level within all pattern structures
	 */
	private int getMaxWidthOfPatternStructures(ArrayList<IPattern> patterns) {
		int max = 0;
		for(IPattern pattern : patterns) {
			int current = pattern.getStructure().getWidth();
			if(current > max)
				max = current;
		}
		return max;
	}

	/**
	 * Calculate the maximum depth of all pattern's accepted sentences
	 * @param patterns List of patterns
	 * @return Maximum number of consecutive nodes in the tree structure of an accepted sentence
	 */
	private int getMaxDepthOfPatternStructures(ArrayList<IPattern> patterns) {
		int max = 0;
		for(IPattern pattern : patterns) {
			for(ISentence sentence : pattern.getAccepted()) {
				int current = sentence.getRootConstituent().getDepth();
				if(current > max)
					max = current;
			}
		}
		return max;
	}
	
	/**
	 * Calculate the maximum number if dependency relations of all pattern's accepted sentences
	 * @param patterns List of patterns
	 * @return Maximum number of dependency relations in a sentence
	 */
	private int getMaxDependencyRelationCount(ArrayList<IPattern> patterns) {
		int max = 0;
		for(IPattern pattern : patterns) {
			for(ISentence sentence : pattern.getAccepted()) {
				int current = sentence.getRootConstituent().getAllLeafs().size()-1;
				if(current > max)
					max = current;
			}
		}
		return max;
	}
	
	
	public Document generatePatternDocument(IPattern pattern) {
		try {
			// initiate the builder
			DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
		    DocumentBuilder docBuilder = docFactory.newDocumentBuilder();
		    Document doc = docBuilder.newDocument();
		    
		    // generate the xml code representing the graphml root
		    Element rootElement = doc.createElement("graphml");
			doc.appendChild(rootElement);
		    
		    // generate the xml code for all patterns and accepted sentences
		    generatePatternStructure(doc, pattern, rootElement, 0);
		    
		    // finalize the building process
		    TransformerFactory transformerFactory = TransformerFactory.newInstance();
		    Transformer transformer = transformerFactory.newTransformer();
		    DOMSource source = new DOMSource(doc);
		    
		    // save the file
		    StreamResult result = new StreamResult(new File(filepath + File.separator + "pattern.graphml"));
		    transformer.transform(source, result);
		    System.out.println("File saved!");
		    
		    return doc;
		} catch (ParserConfigurationException e) {
			CELogger.log().error("ParserConfigurationException in the GraphmlPatternWriter:\n" + e.getMessage());
		} catch (TransformerConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (TransformerException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return null;
	}
}
