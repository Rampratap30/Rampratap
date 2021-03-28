package com.xml;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;


public class GetValueFromXML {

	public static void main(String[] args) throws ParserConfigurationException, SAXException, IOException, XPathExpressionException {
		String XML =
				  "<?xml version = \"1.0\" encoding = \"UTF-8\"?>\n"
				      + "<ns0:GetADSLProfileResponse xmlns:ns0 = \"http://\">\n"
				      + "  <ns0:HEADER>\n"
				      + "    <ns0:REQUEST_ID>TRILOK</ns0:REQUEST_ID>\n"
				      + "    <ns0:SOURCE>Success</ns0:SOURCE>\n"
				      + "  </ns0:HEADER>\n"
				      + "</ns0:GetADSLProfileResponse> ";
				DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
				DocumentBuilder builder = factory.newDocumentBuilder();
				Document document;
				try (InputStream in = new ByteArrayInputStream(XML.getBytes(StandardCharsets.UTF_8))) {
				  document = builder.parse(in);
				}

				XPath xPath = XPathFactory.newInstance().newXPath();
				XPathExpression expr = xPath.compile("/*[local-name()='GetADSLProfileResponse']/*[local-name()='HEADER']/*");

				NodeList nodeList = (NodeList) expr.evaluate(document, XPathConstants.NODESET);
				for (int i = 0; i < nodeList.getLength(); i++) {
				  Node node = nodeList.item(i);
				  System.out.println(node.getNodeName() + ": " + node.getTextContent());
				}

	}

}
