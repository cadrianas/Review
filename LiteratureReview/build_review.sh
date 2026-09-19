#!/usr/bin/env bash
set -euo pipefail
review_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
review_build_dir="$(mktemp -d)"
trap 'rm -rf "$review_build_dir"' EXIT
command -v pandoc >/dev/null
command -v pdflatex >/dev/null
pandoc "$review_dir/preprint/manuscript.md" --standalone -o "$review_dir/preprint/manuscript.tex"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$review_build_dir" -jobname=covid19_modelling_review "$review_dir/preprint/manuscript.tex" > "$review_build_dir/build.log"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$review_build_dir" -jobname=covid19_modelling_review "$review_dir/preprint/manuscript.tex" >> "$review_build_dir/build.log"
mkdir -p "$review_dir/output/pdf"
cp "$review_build_dir/covid19_modelling_review.pdf" "$review_dir/output/pdf/covid19_modelling_review.pdf"
printf 'Built %s\n' "$review_dir/output/pdf/covid19_modelling_review.pdf"
