# VERSION 2.1
import os
import datetime
from bs4 import BeautifulSoup

# Ask for file paths and application name
html_file_path = input("Enter the path of the HTML report file: ").strip()
app_name = input("Enter the application name: ").strip()
#New_html_file = input("Enter the Updated Report file name: ").strip()

# Validate file existence
if not os.path.exists(html_file_path):
    print("Error: HTML report file not found!")
    exit(1)

# Read the existing report HTML file
with open(html_file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# ---------------- Generate Front Page ----------------
current_date = datetime.datetime.now().strftime("%d-%m-%Y")

front_page_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Report</title>
    <style>
        /* Main Page Layout */
        #front-page {{
            width: 200mm;
            height: 260mm;
            margin: 0;
            border: 50px solid #f7941d;
            border-radius: 20px;
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2);
            font-family: Arial, sans-serif;
            position: relative;
            overflow: hidden;
            page-break-before: always;
            background: white;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        /* Upper Section with Bottom Orange Border */
        .top-section {{
            width: 85%;
            height: 60%;
            margin: auto;
            margin-top: 30px;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            border-bottom: 8px solid #f7941d;
            text-align: center;
        }}

        /* Logo */
        .logo {{
            width: 300px;
        }}

        /* Report Title */
        .report-title {{
            font-size: 30px;
            font-weight: bold;
            color: #2e3b4e;
            margin-top: 20px;
        }}

        /* Lower Section */
        .bottom-section {{
            width: 100%;
            height: 30%;
            position: absolute;
            bottom: 0;
            background: white;
            display: flex;
            align-items: center;
            padding: 20px;
        }}

        /* Security Shield Image */
        .shield {{
            width: 150px;
            margin-left: 30px;
        }}

        /* Report Info */
        .report-info {{
            flex-grow: 1;
            text-align: left;
            padding-left: 50px;
            font-size: 18px;
            color: #2e3b4e;
            line-height: 1.5;
        }}

        .report-info strong {{
            font-weight: bold;
        }}

        /* Date */
        .report-date {{
            font-size: 16px;
            font-style: italic;
            margin-top: 5px;
        }}

        /* Ensure colors print correctly */
        @media print {{
            body {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background-color: white;
            }}
            .top-section {{
                border-color: #f7941d !important;
            }}
        }}
    </style>
</head>
<body>
    <div id="front-page">
        <div class="top-section">
            <img src="ReportEditorV1.1\\Netsmartz_logo.png" alt="Company Logo" class="logo"><br>
            <div class="report-title">
                Web Application Penetration Test Report
            </div>
        </div>

        <div class="bottom-section">
            <img src="ReportEditorV1.1\\Shield.png" alt="Security Shield" class="shield">
            <div class="report-info">
                <strong>Application Name:</strong> <span class="app-name">{app_name}</span> <br>
                <p class="report-date"><strong>Date:</strong> {current_date}</p>
            </div>
        </div>
    </div>
</body>
</html>
<br>
"""

# Parse the generated front page HTML
front_page_soup = BeautifulSoup(front_page_html, "html.parser")

# Insert the front page at the beginning of <body>
soup.body.insert(0, front_page_soup)

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
updated_html_file = f"{app_name}_Report_{current_date}.html"
with open(updated_html_file, "w", encoding="utf-8") as file:
    file.write(str(soup))

print(f"Front page added, CSS updated, text justified, and elements removed!\nCheck '{updated_html_file}'.")

# Optional PDF Conversion (Uncomment if needed)
# from weasyprint import HTML
# HTML(updated_html_file).write_pdf("test-report.pdf")
