#VERSION 1.3
from bs4 import BeautifulSoup

# Step 1: Read the existing report HTML file
with open("test-report-060325.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Step 2: Create a new <div> tag
new_div = soup.new_tag("div", id="front-page")
new_div.string = "This is the front page content."

# Step 3: Insert the new <div> at the beginning of the <body>
soup.body.insert(0, new_div)  # Adds new_div as the first element inside <body>

# Step 4: Save the modified HTML file
with open("test-report-updated.html", "w", encoding="utf-8") as file:
    file.write(str(soup))

print("Front-page div added at the beginning! Check 'test-report-updated.html'.")
