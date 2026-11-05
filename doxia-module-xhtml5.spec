Name:		doxia-module-xhtml5
Version:	2.0.0
Release:	1
Summary:	Doxia module for XHTML5 documents
Group:		Development/Java
License:	ASL 2.0
URL:		https://maven.apache.org/doxia/doxia/
Source0:	https://github.com/apache/maven-doxia/archive/refs/tags/doxia-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:	mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(javax.inject:javax.inject)
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	mvn(org.apache.commons:commons-lang3)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
Doxia reads and writes XHTML5. The module inherits Doxia Core from
the reactor parent. XML pull-parser classes come from plexus-utils.

%prep
%autosetup -n maven-doxia-doxia-%{version}
rm -rf src
mv doxia-modules/doxia-module-xhtml5/src src
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.doxia")
add(root, "artifactId", "doxia-module-xhtml5")
add(root, "version", "%{version}")
add(root, "name", "Doxia :: XHTML5 Module")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version in (
    ("org.apache.maven.doxia", "doxia-core", "%{version}"),
    ("org.apache.maven.doxia", "doxia-sink-api", "%{version}"),
    ("org.slf4j", "slf4j-api", "1.7.36"),
    ("javax.inject", "javax.inject", "1"),
    ("org.codehaus.plexus", "plexus-utils", "3.6.0"),
    ("commons-io", "commons-io", "2.22.0"),
    ("org.apache.commons", "commons-lang3", "3.21.0"),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
rm -rf doxia-core doxia-modules doxia-sink-api doxia-test-docs

%files -f .mfiles
%doc README.md
