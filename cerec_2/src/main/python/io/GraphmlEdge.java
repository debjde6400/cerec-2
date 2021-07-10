package jfr.cerec.io;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class GraphmlEdge implements GraphmlElement {
	
	private int index;
	private GraphmlNode source;
	private GraphmlNode target;
	
	/**
	 * Vertical offset for better display of dependency relations
	 */
	private int verticalOffset;
	/**
	 * Diagonal break point for better display of large constituency trees
	 */
	private boolean diagonalBreak;
	
	private String label;

	public GraphmlEdge(int index, GraphmlNode source, GraphmlNode target) {
		super();
		this.index = index;

		setSource(source);
		setTarget(target);
		
		label = "";
	}

	public int getIndex() {
		return index;
	}

	public void setIndex(int index) {
		this.index = index;
	}

	public String getLabel() {
		return label;
	}

	public void setLabel(String label) {
		this.label = label;
	}

	public GraphmlNode getSource() {
		return source;
	}

	public void setSource(GraphmlNode source) {
		this.source = source;
		this.source.addOutgoingDependencyEdge(this);
	}

	public GraphmlNode getTarget() {
		return target;
	}

	public void setTarget(GraphmlNode target) {
		this.target = target;
		this.target.setIncomingDependencyEdge(this);
	}
	
	public double getDistance() {
		int spanX = target.getX() - source.getX();
		int spanY = target.getY() - source.getY();
		return Math.sqrt(spanX*spanX + spanY*spanY);
	}

	public int getVerticalOffset() {
		return verticalOffset;
	}

	public void setVerticalOffset(int verticalOffset) {
		this.verticalOffset = verticalOffset;
	}

	public boolean isDiagonalBreak() {
		return diagonalBreak;
	}

	public void setDiagonalBreak(boolean diagonalBreak) {
		this.diagonalBreak = diagonalBreak;
	}

	@Override
	public Element getGraphmlCode(Document doc) {
		Element edge = doc.createElement("edge");
		edge.setAttribute("id", "e"+index);
		edge.setAttribute("source", "n" + source.getIndex());
		edge.setAttribute("target", "n" + target.getIndex());
		
		Element data9 = doc.createElement("data");
		data9.setAttribute("key", "d9");
		edge.appendChild(data9);
		
		Element data10 = doc.createElement("data");
		data10.setAttribute("key", "d10");
		edge.appendChild(data10);

		Element polyLineEdge = doc.createElement("y:PolyLineEdge");
		data10.appendChild(polyLineEdge);

		Element path = doc.createElement("y:Path");
		path.setAttribute("sx", "0.0");
		path.setAttribute("sv", "0.0");
		path.setAttribute("tx", "0.0");
		path.setAttribute("tv", "0.0");
		polyLineEdge.appendChild(path);
		
		if(verticalOffset > 0) {
			Element point1 = doc.createElement("y:Point");
			point1.setAttribute("x", String.valueOf(source.getX()+45+getOutgoingOffset()));
			point1.setAttribute("y", String.valueOf(source.getY()+40));
			path.appendChild(point1);
			
			Element point2 = doc.createElement("y:Point");
			point2.setAttribute("x", String.valueOf(source.getX()+45+getOutgoingOffset()));
			point2.setAttribute("y", String.valueOf(source.getY()+40+verticalOffset));
			path.appendChild(point2);

			Element point3 = doc.createElement("y:Point");
			point3.setAttribute("x", String.valueOf(target.getX()+45));
			point3.setAttribute("y", String.valueOf(target.getY()+40+verticalOffset));
			path.appendChild(point3);
		} else if(diagonalBreak) {
			Element point = doc.createElement("y:Point");
			point.setAttribute("x", String.valueOf(target.getX()+45));
			point.setAttribute("y", String.valueOf(source.getY()+60));
			path.appendChild(point);
		}
		/*Element point = doc.createElement("y:Point");
		point.setAttribute("x", "10.0");
		point.setAttribute("y", "70.0");
		path.appendChild(point);*/
		
		Element lineStyle = doc.createElement("y:LineStyle");
		lineStyle.setAttribute("color", "#000000");
		lineStyle.setAttribute("type", "line");
		lineStyle.setAttribute("width", "1.0");
		polyLineEdge.appendChild(lineStyle);

		Element arrows = doc.createElement("y:Arrows");
		arrows.setAttribute("source", "none");
		arrows.setAttribute("target", "standard");
		polyLineEdge.appendChild(arrows);
		
		if(!label.isEmpty()) {
			Element edgeLabel = doc.createElement("y:EdgeLabel");
			edgeLabel.setAttribute("alignment", "center");
			edgeLabel.setAttribute("backgroundColor", "#FFFFFFD8");
			edgeLabel.setAttribute("configuration", "AutoFlippingLabel");
			edgeLabel.setAttribute("distance", "2.0");
			edgeLabel.setAttribute("fontFamily", "Dialog");
			edgeLabel.setAttribute("fontSize", "12");
			edgeLabel.setAttribute("fontStyle", "plain");
			edgeLabel.setAttribute("hasLineColor", "false");
			edgeLabel.setAttribute("height", "20.0");
			edgeLabel.setAttribute("horizontalTextPosition", "center");
			edgeLabel.setAttribute("iconTextGap", "4");
			edgeLabel.setAttribute("modelName", "custom");
			edgeLabel.setAttribute("preferredPlacement", "anywhere");
			edgeLabel.setAttribute("ratio", "0.5");
			edgeLabel.setAttribute("textColor", "#000000");
			edgeLabel.setAttribute("verticalTextPosition", "bottom");
			edgeLabel.setAttribute("visible", "true");
			edgeLabel.setAttribute("width", "25");
			edgeLabel.setAttribute("x", "95");
			edgeLabel.setAttribute("xml:space", "preserve");
			edgeLabel.setAttribute("y", "-10.0");
			edgeLabel.setTextContent(label);
			polyLineEdge.appendChild(edgeLabel);
			
			Element labelModel = doc.createElement("y:LabelModel");
			edgeLabel.appendChild(labelModel);
			
			Element smartEdgeLabelModel = doc.createElement("y:SmartEdgeLabelModel");
			smartEdgeLabelModel.setAttribute("autoRotationEnabled", "false");
			smartEdgeLabelModel.setAttribute("defaultAngle", "0.0");
			smartEdgeLabelModel.setAttribute("defaultDistance", "10.0");
			labelModel.appendChild(smartEdgeLabelModel);
			
			Element modelParameter = doc.createElement("y:ModelParameter");
			edgeLabel.appendChild(modelParameter);
			
			Element smartEdgeLabelModelParameter = doc.createElement("y:SmartEdgeLabelModelParameter");
			smartEdgeLabelModelParameter.setAttribute("angle", "0.0");
			smartEdgeLabelModelParameter.setAttribute("distance", "30.0");
			smartEdgeLabelModelParameter.setAttribute("distanceToCenter", "true");
			smartEdgeLabelModelParameter.setAttribute("position", "center");
			smartEdgeLabelModelParameter.setAttribute("ratio", "0.5");
			smartEdgeLabelModelParameter.setAttribute("segment", "1");
			modelParameter.appendChild(smartEdgeLabelModelParameter);
			
			Element preferredPlacementDescriptor = doc.createElement("y:PreferredPlacementDescriptor");
			preferredPlacementDescriptor.setAttribute("angle", "0.0");
			preferredPlacementDescriptor.setAttribute("angleOffsetOnRightSide", "0");
			preferredPlacementDescriptor.setAttribute("angleReference", "absolute");
			preferredPlacementDescriptor.setAttribute("angleRotationOnRightSide", "co");
			preferredPlacementDescriptor.setAttribute("distance", "-1.0");
			preferredPlacementDescriptor.setAttribute("frozen", "true");
			preferredPlacementDescriptor.setAttribute("placement", "anywhere");
			preferredPlacementDescriptor.setAttribute("side", "anywhere");
			preferredPlacementDescriptor.setAttribute("sideReference", "relative_to_edge_flow");
			edgeLabel.appendChild(preferredPlacementDescriptor);
		}
		
		Element bendStyle = doc.createElement("y:BendStyle");
		arrows.setAttribute("smoothed", "false");
		polyLineEdge.appendChild(bendStyle);
		
		return edge;
	}

	private int getOutgoingOffset() {
		int nOutgoing = source.getOutgoingDependencyEdges().size();
		int outgoingIndex = source.getOutgoingDependencyEdges().indexOf(this);
		
		int step = 5;
		
		if(source.getIncomingDependencyEdge() == null) {
			return (outgoingIndex - (nOutgoing/2)) * step;
		} else {
			if((outgoingIndex < (nOutgoing/2)))
				return (outgoingIndex - (nOutgoing/2)) * step - step;
			else 
				return (outgoingIndex - (nOutgoing/2)) * step + step;
		}
	}
}
