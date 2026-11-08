Name:		doxia-module-xhtml5
Version:	2.2.0
Release:	1
Summary:	Doxia module for XHTML5 documents
Group:		Development/Java
License:	ASL 2.0
URL:		https://maven.apache.org/doxia/doxia/
Source0:	https://github.com/apache/maven-doxia/archive/refs/tags/doxia-%{version}.tar.gz#/doxia-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:	doxia-core >= 2.2.0
Requires:	doxia-core >= 2.2.0
BuildRequires:	mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:	doxia-sink-api >= 2.2.0
Requires:	doxia-sink-api >= 2.2.0
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(org.slf4j:slf4j-parent:pom::)
BuildRequires:	mvn(javax.inject:javax.inject)
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.codehaus.plexus:plexus:pom::)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
Doxia reads and writes XHTML5. Meta and class attributes are read
through SinkEventAttributes. XML pull-parser classes come from
plexus-utils, and string helpers come from Doxia Core.

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
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version in (
    ("org.apache.maven.doxia", "doxia-core", "%{version}"),
    ("org.apache.maven.doxia", "doxia-sink-api", "%{version}"),
    ("org.slf4j", "slf4j-api", "1.7.36"),
    ("javax.inject", "javax.inject", "1"),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2"),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
# Sisu loads @Named classes from this index. The indexer plugin is not packaged.
python - <<'PY'
import re
from pathlib import Path
root = Path("src/main/java")
names = []
for path in sorted(root.rglob("*.java")):
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"\b(?:class|interface|enum)\s+([A-Za-z0-9_]+)", text)
    if not match:
        continue
    if "@Named" not in text[:match.start()]:
        continue
    pkg = re.search(r"(?m)^package\s+([A-Za-z0-9_.]+)\s*;", text)
    if not pkg:
        continue
    names.append(pkg.group(1) + "." + match.group(1))
if names:
    dest = Path("src/main/resources/META-INF/sisu")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "javax.inject.Named").write_text("\n".join(names) + "\n", encoding="utf-8")
PY
rm -rf doxia-core doxia-modules doxia-sink-api doxia-test-docs

%files -f .mfiles
%doc README.md
