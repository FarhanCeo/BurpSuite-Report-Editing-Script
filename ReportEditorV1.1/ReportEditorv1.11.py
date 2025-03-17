# VERSION 2.1
import os
import datetime
from bs4 import BeautifulSoup

# Ask for file paths and application name
html_file_path = input("Enter the path of the HTML report file: ").strip()
front_page_path = input("Enter the path of the front page file: ").strip()
app_name = input("Enter the application name: ").strip()

# Validate file existence
if not os.path.exists(html_file_path):
    print("Error: HTML report file not found!")
    exit(1)

if not os.path.exists(front_page_path):
    print("Error: Front page file not found!")
    exit(1)

# Read the existing report HTML file
with open(html_file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# ---------------- Add Front Page ----------------
with open(front_page_path, "r", encoding="utf-8") as file:
    front_page_html = file.read()

# Parse front page and insert it at the beginning of <body>
front_page_soup = BeautifulSoup(front_page_html, "html.parser")
soup.body.insert(0, front_page_soup)

# ---------------- Auto-fill Application Name and Date ----------------
current_date = datetime.datetime.now().strftime("%d-%m-%Y")

# Insert values in appropriate placeholders
for span in soup.find_all("span", class_="app-name"):
    span.string = app_name

for span in soup.find_all("span", class_="report-date"):
    span.string = current_date

# ---------------- Modify CSS ----------------
style_tag = soup.find("style")
if style_tag and style_tag.string:
    updated_css = []
    css_rules = style_tag.string.split("}")

    for rule in css_rules:
        if "body {" in rule:
            rule = rule.replace("padding: 0 15px", "padding: 0 80px")
        if "#container {" in rule:
            rule = rule.replace("padding: 0 15px", "padding: 0 80px")
        if ".rr_div" in rule:
            rule = ";".join([prop for prop in rule.split(";") if "max-height" not in prop])

        updated_css.append(rule.strip())

    style_tag.string = "}".join(updated_css) + "}"

# ---------------- Justify Text Inside <span class="TEXT"> ----------------
for span in soup.find_all("span", class_="TEXT"):
    if "style" in span.attrs:
        span["style"] += "; text-align: justify;"
    else:
        span["style"] = "text-align: justify;"

# ---------------- Remove Unwanted Elements ----------------
for tag in soup.find_all("div", class_="title"):
    tag.decompose()
for tag in soup.find_all("a", class_="PREVNEXT"):
    tag.decompose()
for tag in soup.find_all("span", class_="TEXT"):
    if "Report generated by Burp Suite" in tag.get_text():
        tag.decompose()

# ---------------- Save the Modified HTML File ----------------
updated_html_file = "test-report-updated.html"
with open(updated_html_file, "w", encoding="utf-8") as file:
    file.write(str(soup))

print(f"Front page added, CSS updated, text justified, and elements removed!\nCheck '{updated_html_file}'.")

# Optional PDF Conversion (Uncomment if needed)
# from weasyprint import HTML
# HTML(updated_html_file).write_pdf("test-report.pdf")
