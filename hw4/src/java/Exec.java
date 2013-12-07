import java.io.*;

class StreamGobbler extends Thread {
  InputStream is;
  PrintStream os;
 
  StreamGobbler(InputStream is, PrintStream os) {
    this.is = is;
    this.os = os;
  }
 
  public void run() {
    try {
      int c;
      while ((c = is.read()) != -1)
          os.print((char) c);
    } catch (IOException x) {
      // handle error
    }
  }
}

class StreamFeeder extends Thread {
  InputStream is;
  PrintStream os;
 
  StreamGobbler(InputStream is, PrintStream os) {
    this.is = is;
    this.os = os;
  }
 
  public void run() {
    try {
      int c;
      while ((c = is.read()) != -1)
          os.print((char) c);
    } catch (IOException x) {
      // handle error
    }
  }
}
 
public class Exec {
  public static void main(String[] args)
    throws IOException, InterruptedException {
 
    Runtime rt = Runtime.getRuntime();
    Process proc = rt.exec("cowsay hey");
 
    // Any error message?
    StreamGobbler errorGobbler =
        new StreamGobbler(proc.getErrorStream(), System.err);
 
    // Any output?
    StreamGobbler outputGobbler =
        new StreamGobbler(proc.getInputStream(), System.out);
 
    errorGobbler.start();
    outputGobbler.start();
 
    // Any error?
    int exitVal = proc.waitFor();
    errorGobbler.join();   // Handle condition where the
    outputGobbler.join();  // process ends before the threads finish
  }
}