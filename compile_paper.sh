#!/bin/bash
# compile_paper.sh - Compile Hope Genome academic paper

set -e  # Exit on error

echo "================================================"
echo "Hope Genome Paper Compilation Script"
echo "================================================"
echo ""

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo "❌ ERROR: pdflatex not found!"
    echo ""
    echo "Install LaTeX distribution:"
    echo "  Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "  macOS: brew install --cask mactex"
    echo "  Windows: https://miktex.org/download"
    exit 1
fi

# Check if bibtex is installed
if ! command -v bibtex &> /dev/null; then
    echo "❌ ERROR: bibtex not found!"
    echo "Please install complete LaTeX distribution"
    exit 1
fi

PAPER_FILE="hope_genome_paper"
OUTPUT_DIR="build"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "📄 Compiling $PAPER_FILE.tex..."
echo ""

# First pass
echo "🔄 Pass 1/4: Initial compilation..."
pdflatex -output-directory="$OUTPUT_DIR" "$PAPER_FILE.tex" > /dev/null 2>&1
echo "✅ Pass 1 complete"

# BibTeX for references
echo "🔄 Pass 2/4: Processing bibliography..."
cd "$OUTPUT_DIR"
bibtex "$PAPER_FILE" > /dev/null 2>&1
cd ..
echo "✅ Pass 2 complete"

# Second pass (resolve references)
echo "🔄 Pass 3/4: Resolving references..."
pdflatex -output-directory="$OUTPUT_DIR" "$PAPER_FILE.tex" > /dev/null 2>&1
echo "✅ Pass 3 complete"

# Final pass (finalize)
echo "🔄 Pass 4/4: Final compilation..."
pdflatex -output-directory="$OUTPUT_DIR" "$PAPER_FILE.tex" > /dev/null 2>&1
echo "✅ Pass 4 complete"

echo ""
echo "================================================"
echo "✅ Compilation successful!"
echo "================================================"
echo ""
echo "📁 Output file: $OUTPUT_DIR/$PAPER_FILE.pdf"

# Check file size
FILE_SIZE=$(du -h "$OUTPUT_DIR/$PAPER_FILE.pdf" | cut -f1)
echo "📊 File size: $FILE_SIZE"

# Count pages
PAGES=$(pdfinfo "$OUTPUT_DIR/$PAPER_FILE.pdf" 2>/dev/null | grep "Pages:" | awk '{print $2}')
if [ -n "$PAGES" ]; then
    echo "📄 Total pages: $PAGES"
fi

echo ""
echo "🎉 Your paper is ready for submission!"
echo ""

# Clean up auxiliary files
echo "🧹 Cleaning up auxiliary files..."
rm -f "$OUTPUT_DIR"/*.aux "$OUTPUT_DIR"/*.log "$OUTPUT_DIR"/*.out \
      "$OUTPUT_DIR"/*.bbl "$OUTPUT_DIR"/*.blg "$OUTPUT_DIR"/*.toc
echo "✅ Cleanup complete"

echo ""
echo "To view the paper:"
echo "  Linux:   xdg-open $OUTPUT_DIR/$PAPER_FILE.pdf"
echo "  macOS:   open $OUTPUT_DIR/$PAPER_FILE.pdf"
echo "  Windows: start $OUTPUT_DIR/$PAPER_FILE.pdf"
echo ""
