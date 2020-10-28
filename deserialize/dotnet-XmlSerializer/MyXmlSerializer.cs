using System;
using System.IO;
using System.Xml;
using System.Xml.Serialization;

namespace MyXMLSerializer
{
    class Program
    {
        static void Main(string[] args)
        {
            String txt = args[0];
            int myClass = Int32.Parse(args[1]);

            if (myClass == 1)
            {
                AAA myText = new AAA();
                myText.text = txt;
                CustomSerializer(myText, args[2]);
            }
            else
            {
                BBB myText = new BBB();
                myText.text = txt;
                CustomSerializer(myText, args[2]);
            }
        }

        static void CustomSerializer(Object myObj, String fileName)
        {
            XmlDocument xmlDocument = new XmlDocument();
            XmlElement xmlElement = xmlDocument.CreateElement("customRootNode");
            xmlDocument.AppendChild(xmlElement);
            XmlElement xmlElement2 = xmlDocument.CreateElement("item");
            xmlElement2.SetAttribute("objectType", myObj.GetType().AssemblyQualifiedName);
            XmlDocument xmlDocument2 = new XmlDocument();
            XmlSerializer xmlSerializer = new XmlSerializer(myObj.GetType());
            StringWriter writer = new StringWriter();
            xmlSerializer.Serialize(writer, myObj);
            xmlDocument2.LoadXml(writer.ToString());
            xmlElement2.AppendChild(xmlDocument.ImportNode(xmlDocument2.DocumentElement, true));
            xmlElement.AppendChild(xmlElement2);

            File.WriteAllText(fileName, xmlDocument.OuterXml);
        }
    }

    public class AAA
    {
        private String _text;

        public String text
        {
            get { return _text; }
            set { _text = value; Console.WriteLine("Hello AAA: " + _text); }
        }
    }

    public class BBB
    {
        private String _text;

        public String text
        {
            get { return _text; }
            set { _text = value; Console.WriteLine("Hello BBB: " + _text); }
        }
    }
}
