   <wsdl:output message="vbox:IConsole_powerButtonResultMsg"/>
      <wsdl:fault name="InvalidObjectFault" message="vbox:InvalidObjectFaultMsg"/>
      <wsdl:fault name="RuntimeFault" message="vbox:RuntimeFaultMsg"/>
    </wsdl:operation>
    <wsdl:operation name="IConsole_sleepButton">
      <wsdl:input message="vbox:IConsole_sleepButtonRequestMsg"/>
      <wsdl:output message="vbox:IConsole_sleepButtonResultMsg"/>
      <wsdl:fault name="InvalidObjectFault" message="vbox:InvalidObjectFaultMsg"/>
      <wsdl:fault name="RuntimeFault" message="vbox:RuntimeFaultMsg"/>
    </wsdl:operation>
    <wsdl:operation name="IConsole_getPowerButtonHandled">
      <wsdl:input message="