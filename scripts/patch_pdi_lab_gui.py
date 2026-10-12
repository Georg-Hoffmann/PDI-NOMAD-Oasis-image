from pathlib import Path
import sys

root = Path(
    "/opt/venv/lib/python3.12/site-packages/"
    "nomad_gui/apis/static"
)

target = (
    Path(sys.argv[1]) if len(sys.argv) > 1
    else root / "assets/_dashboardId-DfHO4waO.js"
)

old = 'sandbox:`allow-scripts allow-forms allow-same-origin allow-popups`'

new = (
    'sandbox:`allow-scripts allow-forms allow-same-origin allow-popups'
    '${new URL(_.url,window.location.href).origin===window.location.origin'
    '&&new URL(_.url,window.location.href).pathname'
    '==="/nomad-oasis/dashboards/pdi-lab/"'
    '?" allow-top-navigation-by-user-activation":""}`'
)

if len(sys.argv) == 1:
    html = (root / "index.html").read_text()
    main = (root / "assets/index-BteZpL0b.js").read_text()

    assert html.count("assets/index-BteZpL0b.js") == 1
    assert main.count("_dashboardId-DfHO4waO.js") == 2

source = target.read_text()
assert source.count(old) == 1

target.write_text(source.replace(old, new, 1))

print("OK: PDI-Lab-Fullpage-Fix")
print("OK: Originale NOMAD-Modulstruktur beibehalten")
