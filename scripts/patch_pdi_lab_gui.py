from pathlib import Path
from hashlib import sha256

root = Path(
    "/opt/venv/lib/python3.12/site-packages/"
    "nomad_gui/apis/static"
)
assets = root / "assets"

dashboard = assets / "_dashboardId-DfHO4waO.js"
main = assets / "index-BteZpL0b.js"
html = root / "index.html"

# Exactly the navigation fix already tested successfully.
old = 'sandbox:`allow-scripts allow-forms allow-same-origin allow-popups`'

new = (
    'sandbox:`allow-scripts allow-forms allow-same-origin allow-popups'
    '${new URL(_.url,window.location.href).origin===window.location.origin'
    '&&new URL(_.url,window.location.href).pathname'
    '==="/nomad-oasis/dashboards/pdi-lab/"'
    '?" allow-top-navigation-by-user-activation":""}`'
)

dashboard_source = dashboard.read_text()
main_source = main.read_text()
html_source = html.read_text()

assert dashboard_source.count(old) == 1
assert main_source.count(dashboard.name) == 2
assert html_source.count("assets/" + main.name) == 1

patched_dashboard = dashboard_source.replace(old, new, 1)

dashboard_hash = sha256(
    patched_dashboard.encode()
).hexdigest()[:12]

new_dashboard_name = (
    f"_dashboardId-pdi-fullpage-{dashboard_hash}.js"
)

patched_main = main_source.replace(
    dashboard.name, new_dashboard_name
)

main_hash = sha256(
    patched_main.encode()
).hexdigest()[:12]

new_main_name = f"index-pdi-fullpage-{main_hash}.js"

patched_html = html_source.replace(
    "assets/" + main.name,
    "assets/" + new_main_name,
    1
)

# Validate everything before writing.
assert patched_main.count(new_dashboard_name) == 2
assert patched_html.count("assets/" + new_main_name) == 1

new_dashboard = assets / new_dashboard_name
new_main = assets / new_main_name

assert not new_dashboard.exists()
assert not new_main.exists()

# Keep the original assets for compatibility.
new_dashboard.write_text(patched_dashboard)
new_main.write_text(patched_main)
html.write_text(patched_html)

print("OK: PDI Lab iframe navigation enabled")
print("Dashboard module:", new_dashboard_name)
print("Main module:", new_main_name)
print("OK: index.html updated")
