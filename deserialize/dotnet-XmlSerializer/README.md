# XmlDeserializer with GetType Exploit

## Quick Start
```
> csc -out:ser.exe MyXmlSerializer.cs

> .\ser.exe hello 1 xml.txt

> csc -out:deser.exe MyXmlDeserializer.cs

> .\deser.exe evil.txt
```
