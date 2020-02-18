import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, dump
from os.path import isfile, join, splitext
from os import listdir
import sys

extensionIdDict={".dll":"DLLComponents", ".exe":"ProductComponents", 
				".xml":"AdditionalComponents", ".manifest":"AdditionalComponents",
				".config":"AdditionalComponents", ".application":"AdditionalComponents"}

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def generateComponentGroup(dirPath,solDir,_id,extension):
	if (solDir == dirPath[:len(solDir)]):
		sourceDir = "$(var.SolutionDir)" + dirPath[len(solDir):]
	else:
		sourceDir = dirPath
	componentGroupAtt = {"Id":_id,"Directory":"INSTALLFOLDER","Source":sourceDir}
	componentGroup = Element("ComponentGroup",attrib=componentGroupAtt)
	fileList = [f for f in listdir(dirPath) if (isfile(join(dirPath,f)) and (splitext(f)[1])==extension)]
	
	if (fileList != []):
		for idx,f in enumerate(fileList):
			fName = splitext(f)[0]
			fFormat = splitext(f)[1]
			componentAttr = {"Id":fFormat.upper()[1:]+"_"+fName}
			component = SubElement(componentGroup, "Component", attrib=componentAttr)
			fileComponentAttr = {"Name":f}
			if (extension == ".exe"):
				fileComponentAttr.update({"KeyPath":"yes"})
			fileComponent = SubElement(component, "File",attrib=fileComponentAttr)
		return componentGroup
	
	return None

def generateFragment(componentGroup):
	fragment = Element("Fragment")
	fragment.append(componentGroup)
	return fragment

def generateFragment(componentGroupList):
	fragment = Element("Fragment")
	for componentGroup in componentGroupList:
		if (list(fragment) != []):
			idx = next((i for i,v in enumerate(fragment) if (componentGroup.tag == v.tag) and (componentGroup.attrib == v.attrib)),-1)
			if (idx != -1):
				for component in componentGroup:
					list(fragment)[idx].append(component)
			else:
				fragment.append(componentGroup)
		else:
			fragment.append(componentGroup)
	return fragment

def generateFeature(componentGroup,id,title,level="1"):
	featureAttr = {"Id":id,"Title":title,"Level":level}
	featureComponent = Element("Feature",featureAttr)
	componentGroupRefAttr = {}
	for i in componentGroup.items():
		if i[0]=="Id":
			componentGroupRefAttr.update({i[0]:i[1]})
	componentGroupRef = SubElement(featureComponent,"ComponentGroupRef",attrib=componentGroupRef)
	return componentGroupRef

def generateFeature(componentGroupList,id,title,level="1"):
	featureAttr = {"Id":id,"Title":title,"Level":level}
	featureComponent = Element("Feature",featureAttr)
	cGroupRefAttrList = []
	for componentGroup in componentGroupList:
		for i in componentGroup.items():
			componentGroupRefAttr = {}
			if i[0]=="Id":
				componentGroupRefAttr.update({i[0]:i[1]})
				if (componentGroupRefAttr in cGroupRefAttrList):
					break
				else:
					cGroupRefAttrList.append(componentGroupRefAttr)
			else:
				break
			componentGroupRef = SubElement(featureComponent,"ComponentGroupRef",attrib=componentGroupRefAttr)
			componentGroupRef.tail = "\n"
	
	return featureComponent



def main(**kwargs):
	

	ext = []
	directory = []
	componentGroupList = []
	solutionDir = ""
	targetProjectName = ""
	for key, val in kwargs.items():
		if (key=="extension"):
			ext = val
		elif (key=="dir"):
			directory=val
		elif (key=="sdir"):
			solutionDir=val
			
	try:		
		for xt in ext:
			xt = "."+xt
			_id = extensionIdDict[xt]
			for d in directory:
				c = generateComponentGroup(d,solutionDir,_id,xt)
				if (c != None):
					componentGroupList.append(c)
		
		fragment = generateFragment(componentGroupList)
		indent(fragment)
		print(ET.tostring(fragment).decode("utf-8"))

		feature = generateFeature(componentGroupList,"ProductFeature", title="LasermarkingTracker")
		indent(feature)
		print(ET.tostring(feature).decode("utf-8"))
	
	except Exception as e:
		print(e)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Python script for generating some of the parts of the WiX xml config file.")
	parser.add_argument("-d", "--dir", nargs='+', required=True, help="set the directory of the target files")
	parser.add_argument("-e", "--ext", nargs='+', required=True, help="file extensions to add to the configuration")
	parser.add_argument("-s", "--sdir", required=True, help="target solution directory")
	args = parser.parse_args()
	main(dir=args.dir, extension=args.ext, sdir=args.sdir)