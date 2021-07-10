package jfr.cerec.util;

import java.io.PrintStream;

/**
 * 
 * @author Julian Frattini
 * 
 * Custom logger mainly tailored towards the evaluation of the author's master thesis
 */

public class CELogger {
	
	private static CELogger instance;
	private boolean initialized;
	
	private PrintStream out;
	
	public static CELogger log() {
		if(instance == null) {
			instance = new CELogger();
		} 
		return instance;
	}
	
	private CELogger() {
		initialized = false;
		out = null;
	}
	
	public void initialize(PrintStream out) {
		this.out = out;
		initialized = true;
	}
	
	public void initializeIfNeccessary(PrintStream out) {
		if(!initialized) {
			this.out = out;
			initialized = true;
		}
	}
	
	public void info(String text) {
		if(initialized) {
			log(GlobalConfiguration.LOG_LEVEL_INFO, text, out);
		}
	}
	
	public void warn(String text) {
		if(initialized) {
			log(GlobalConfiguration.LOG_LEVEL_WARN, "Warning: " + text, out);
		}
	}
	
	public void error(String text) {
		log(GlobalConfiguration.LOG_LEVEL_ERROR, "ERROR: " + text, 
				(initialized ? out : System.out));
	}
	
	public void print(String text) {
		out.println("[" + GlobalConfiguration.LOG_PREFIX + "] " + text);
	}
	
	private void log(int logLevel, String text, PrintStream out) {
		if(GlobalConfiguration.CURRENT_LOG_LEVEL <= logLevel) {
			out.println("[" + GlobalConfiguration.LOG_PREFIX + "] " + text);
		}
	}
}
