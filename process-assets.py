#!/usr/bin/env python3

from pathlib import Path
import subprocess
import ninja_syntax

def main():
    src = Path("assets-src")
    assets = Path("assets-build")
    ninjafile = Path("build.ninja")
    n = ninja_syntax.Writer(ninjafile.open('w', encoding='utf-8'))
    n.variable("inkscape", "flatpak run org.inkscape.Inkscape")
    n.rule(name="svg2pdf", 
            command="$inkscape -z $in -A $out")
    n.rule(name="svg2pdflatex", 
            command="$inkscape -z $in -A $out --export-latex")

    src_pdf = src / Path("to_pdf")
    src_pdflatex = src / Path("to_pdflatex")

    def build(indir, rule):
        for f in (f for f in indir.iterdir() if f.is_file()):
            if f.suffix == ".svg":
                out = assets / f.with_suffix(".pdf").relative_to(indir)
                n.build(outputs=str(out),
                        rule=rule,
                        inputs=str(f))
    build(src_pdf, "svg2pdf")
    build(src_pdflatex, "svg2pdflatex")

    n.close()
    
    subprocess.run(['ninja'])



if __name__ == "__main__":
    main()
