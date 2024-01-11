echo "Deleting files in Build"
rm -r build
echo "Running Sphinx"
#pip3 install --user --upgrade sphinx sphinx-pyreverse sphinx-rtd-theme sphinx-tabs sphinxcontrib-plantuml sphinxcontrib-websupport
sphinx-build -b html source build
#sphinx-build -b latex source build
#sphinx-build -b wikipage source build
#sphinx-build -M latexpdf source build