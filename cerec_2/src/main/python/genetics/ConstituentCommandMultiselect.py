'''
/**
 *
 * @author Julian Frattini
 *
 * Command for vertical selection. Given a sentence in the form of a tree of syntactical nodes
 * select one of a specific type/content.
 */'''
from python.genetics.ConstituentCommand import ConstituentCommand

class ConstituentCommandMultiselect(ConstituentCommand):

  '''/**
   * List of selectors, that generate the desired expression
   */
  private ArrayList<ConstituentCommand> selectors;'''

  #public ConstituentCommandMultiselect(ArrayList<ConstituentCommand> selectors) {
  def __init__(self, selectors):
    super();
    self.selectors = selectors

  def getSelectors(self):
    return self.selectors

  def setSelectors(self, selectors):
    self.selectors = selectors;

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def generateOutput(self, fragment):
    output = [""]

    for selector in self.selectors:
      output.append(selector.generateOutput(fragment))
    
    return " ".join(output)
  

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def toString(self):
    sb = []

    sb.append("multiselect:")
    for s in self.selectors:
        sb.append("\n" + s.toString())

    return ' '.join(sb)

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getFinal(self):
    # a mutliselect does not require any adjustments to the final node
    return None
