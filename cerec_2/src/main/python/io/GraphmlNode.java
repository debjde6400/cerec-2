package jfr.cerec.io;

import java.util.ArrayList;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class GraphmlNode implements GraphmlElement {
	private int index;
	//private Object reference;
	
	private String label;
	private int x;
	private int y;
	
	private String color;
	private boolean borderDisabled;
	private int fontSize;
	
	private ArrayList<GraphmlEdge> outgoingDependencyEdges;
	private GraphmlEdge incomingDependencyEdge;

	public GraphmlNode(int index) {
		super();
		this.index = index;
		
		color = "";
		borderDisabled = false;
		fontSize = 12;
		outgoingDependencyEdges = new ArrayList<GraphmlEdge>();
	}

	public GraphmlNode(int index, String label, int x, int y) {
		super();
		this.index = index;
		//this.reference = reference;
		this.label = label;
		this.x = x;
		this.y = y;

		color = "";
		borderDisabled = false;
		fontSize = 12;
		outgoingDependencyEdges = new ArrayList<GraphmlEdge>();
	}
	
	/*public Object getReference() {
		return reference;
	}

	public void setReference(Object reference) {
		this.reference = reference;
	}*/

	public int getIndex() {
		return index;
	}
	
	public String getLabel() {
		return label;
	}
	
	public void setLabel(String label) {
		this.label = label;
	}
	
	public String getColor() {
		return color;
	}

	public void setColor(String color) {
		this.color = color;
	}

	public boolean isBorderDisabled() {
		return borderDisabled;
	}

	public void setBorderDisabled(boolean borderDisabled) {
		this.borderDisabled = borderDisabled;
	}
	
	public int getFontSize() {
		return fontSize;
	}

	public void setFontSize(int fontSize) {
		this.fontSize = fontSize;
	}

	public int getX() {
		return x;
	}
	
	public void setX(int x) {
		this.x = x;
	}
	
	public int getY() {
		return y;
	}
	
	public void setY(int y) {
		this.y = y;
	}
	
	public void addOutgoingDependencyEdge(GraphmlEdge edge) {
		outgoingDependencyEdges.add(edge);
	}

	public ArrayList<GraphmlEdge> getOutgoingDependencyEdges() {
		return outgoingDependencyEdges;
	}

	public GraphmlEdge getIncomingDependencyEdge() {
		return incomingDependencyEdge;
	}

	public void setIncomingDependencyEdge(GraphmlEdge incomingDependencyEdge) {
		this.incomingDependencyEdge = incomingDependencyEdge;
	}

	@Override
	public Element getGraphmlCode(Document doc) {
		Element node = doc.createElement("node");
		node.setAttribute("id", "n"+index);
		
		Element data = doc.createElement("data");
		data.setAttribute("key", "d6");
		node.appendChild(data);
		
		Element yShapeNode = doc.createElement("y:ShapeNode");
		data.appendChild(yShapeNode);
		
		Element geometry = doc.createElement("y:Geometry");
		geometry.setAttribute("height", "40.0");
		geometry.setAttribute("width", "90.0");
		geometry.setAttribute("x", String.valueOf(x));
		geometry.setAttribute("y", String.valueOf(y));
		yShapeNode.appendChild(geometry);

		Element fill = doc.createElement("y:Fill");
		if(color.isEmpty()) {
			fill.setAttribute("hasColor", "false");
		} else {
			fill.setAttribute("color", color);
		}
		fill.setAttribute("transparent", "false");
		yShapeNode.appendChild(fill);

		Element borderStyle = doc.createElement("y:BorderStyle");
		if(!borderDisabled) {
			borderStyle.setAttribute("color", "#000000");
		} else {
			borderStyle.setAttribute("hasColor", "false");
		}
		borderStyle.setAttribute("raised", "false");
		borderStyle.setAttribute("type", "line");
		borderStyle.setAttribute("width", "1.0");
		yShapeNode.appendChild(borderStyle);
		
		Element nodeLabel = doc.createElement("y:NodeLabel");
		nodeLabel.setAttribute("alignment", "#center");
		nodeLabel.setAttribute("autoSizePolicy", "content");
		nodeLabel.setAttribute("fontFamily", "Dialog");
		nodeLabel.setAttribute("fontSize", String.valueOf(fontSize));
		nodeLabel.setAttribute("fontStyle", "plain");
		nodeLabel.setAttribute("hasBackgroundColor", "false");
		nodeLabel.setAttribute("hasLineColor", "false");
		nodeLabel.setAttribute("height", "20.0");
		nodeLabel.setAttribute("horizontalTextPosition", "center");
		nodeLabel.setAttribute("iconTextGap", "4");
		nodeLabel.setAttribute("modelName", "custom");
		nodeLabel.setAttribute("textColor", "#000000");
		nodeLabel.setAttribute("verticalTextPosition", "bottom");
		nodeLabel.setAttribute("visible", "true");
		nodeLabel.setAttribute("width", "80");
		nodeLabel.setAttribute("x", "6.0");
		nodeLabel.setAttribute("xml:space", "preserve");
		nodeLabel.setAttribute("y", "11.0");
		yShapeNode.appendChild(nodeLabel);
		
		nodeLabel.setTextContent(label);
		
		Element labelModel = doc.createElement("y:LabelModel");
		nodeLabel.appendChild(labelModel);
		
		Element smartNodeLabelModel = doc.createElement("y:SmartNodeLabelModel");
		smartNodeLabelModel.setAttribute("distance", "4.0");
		labelModel.appendChild(smartNodeLabelModel);
		
		Element modelParameter = doc.createElement("y:ModelParameter");
		nodeLabel.appendChild(modelParameter);
		
		Element smartNodeLabelModelParameter = doc.createElement("y:SmartNodeLabelModelParameter");
		smartNodeLabelModelParameter.setAttribute("labelRatioX", "0.0");
		smartNodeLabelModelParameter.setAttribute("labelRatioY", "0.0");
		smartNodeLabelModelParameter.setAttribute("nodeRatioX", "0.0");
		smartNodeLabelModelParameter.setAttribute("nodeRatioY", "0.0");
		smartNodeLabelModelParameter.setAttribute("offsetX", "0.0");
		smartNodeLabelModelParameter.setAttribute("offsetY", "0.0");
		smartNodeLabelModelParameter.setAttribute("upX", "0.0");
		smartNodeLabelModelParameter.setAttribute("upY", "-1.0");
		modelParameter.appendChild(smartNodeLabelModelParameter);
		
		Element shape = doc.createElement("y:Shape");
		borderStyle.setAttribute("type", "#rectangle");
		yShapeNode.appendChild(shape);

		return node;
	}
}
