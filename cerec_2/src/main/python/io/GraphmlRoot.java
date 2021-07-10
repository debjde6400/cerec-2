package jfr.cerec.io;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class GraphmlRoot implements GraphmlElement {

	@Override
	public Element getGraphmlCode(Document doc) {
		Element rootElement = doc.createElement("graphml");
		rootElement.setAttribute("xmlns", "http://graphml.graphdrawing.org/xmlns");
		rootElement.setAttribute("xmlns:java", "http://www.yworks.com/xml/yfiles-common/1.0/java");
		rootElement.setAttribute("xmlns:sys", "http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0");
		rootElement.setAttribute("xmlns:x", "http://www.yworks.com/xml/yfiles-common/markup/2.0");
		rootElement.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance");
		rootElement.setAttribute("xmlns:y", "http://www.yworks.com/xml/graphml");
		rootElement.setAttribute("xmlns:yed", "http://www.yworks.com/xml/yed/3");
		rootElement.setAttribute("xsi:schemaLocation", "http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd");
		doc.appendChild(rootElement);
		
		Element key_0 = doc.createElement("key");
		key_0.setAttribute("attr.name", "Description");
		key_0.setAttribute("attr.type", "string");
		key_0.setAttribute("for", "graph");
		key_0.setAttribute("id", "d0");
		rootElement.appendChild(key_0);

		Element key_1 = doc.createElement("key");
		key_1.setAttribute("for", "port");
		key_1.setAttribute("id", "d1");
		key_1.setAttribute("yfiles.type", "portgraphics");
		rootElement.appendChild(key_1);
		
		Element key_2 = doc.createElement("key");
		key_2.setAttribute("for", "port");
		key_2.setAttribute("id", "d2");
		key_2.setAttribute("yfiles.type", "portgeometry");
		rootElement.appendChild(key_2);
		
		Element key_3 = doc.createElement("key");
		key_3.setAttribute("for", "port");
		key_3.setAttribute("id", "d3");
		key_3.setAttribute("yfiles.type", "portuserdata");
		rootElement.appendChild(key_3);
		
		Element key_4 = doc.createElement("key");
		key_4.setAttribute("attr.name", "url");
		key_4.setAttribute("attr.type", "string");
		key_4.setAttribute("for", "node");
		key_4.setAttribute("id", "d4");
		rootElement.appendChild(key_4);
		
		Element key_5 = doc.createElement("key");
		key_5.setAttribute("attr.name", "description");
		key_5.setAttribute("attr.type", "string");
		key_5.setAttribute("for", "node");
		key_5.setAttribute("id", "d5");
		rootElement.appendChild(key_5);
		
		Element key_6 = doc.createElement("key");
		key_6.setAttribute("for", "node");
		key_6.setAttribute("id", "d6");
		key_6.setAttribute("yfiles.type", "nodegraphics");
		rootElement.appendChild(key_6);
		
		Element key_7 = doc.createElement("key");
		key_7.setAttribute("for", "graphml");
		key_7.setAttribute("id", "d7");
		key_7.setAttribute("yfiles.type", "resources");
		rootElement.appendChild(key_7);

		Element key_8 = doc.createElement("key");
		key_8.setAttribute("attr.name", "url");
		key_8.setAttribute("attr.type", "string");
		key_8.setAttribute("for", "edge");
		key_8.setAttribute("id", "d8");
		rootElement.appendChild(key_8);
		
		Element key_9 = doc.createElement("key");
		key_9.setAttribute("attr.name", "description");
		key_9.setAttribute("attr.type", "string");
		key_9.setAttribute("for", "edge");
		key_9.setAttribute("id", "d9");
		rootElement.appendChild(key_9);
		
		Element key_10 = doc.createElement("key");
		key_10.setAttribute("for", "edge");
		key_10.setAttribute("id", "d10");
		key_10.setAttribute("yfiles.type", "edgegraphics");
		rootElement.appendChild(key_10);
		
		Element graph = doc.createElement("graph");
		graph.setAttribute("edgedefault", "directed");
		graph.setAttribute("id", "G");
		rootElement.appendChild(graph);
		
		Element data = doc.createElement("data");
		graph.setAttribute("key", "d0");
		graph.setAttribute("xml:space", "preserve");
		graph.appendChild(data);
		
		Element data7 = doc.createElement("data");
		data7.setAttribute("key", "d7");
		rootElement.appendChild(data7);
		
		Element yResources = doc.createElement("y:Resources");
		data7.appendChild(yResources);
		
		return graph;
	}
}
