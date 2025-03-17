from bs4 import BeautifulSoup

# Step 1: Read the HTML file
with open("demo_report.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Step 2: Remove the summary paragraph
summary = soup.find("p", id="summary")
if summary:
    summary.decompose()

# Step 3: Add a new footer
footer = soup.new_tag("p")
footer.string = "Generated on: March 6, 2025"
soup.body.append(footer)

# Step 4: Add a new row to the table
table = soup.find("table")
if table:
    new_row = soup.new_tag("tr")

    product_cell = soup.new_tag("td")
    product_cell.string = "Product C"
    new_row.append(product_cell)

    sales_cell = soup.new_tag("td")
    sales_cell.string = "$1500"
    new_row.append(sales_cell)

    table.append(new_row)

# Step 5: Save the modified HTML file
with open("updated_report.html", "w", encoding="utf-8") as file:
    file.write(str(soup))

print("Report updated successfully! Check 'updated_report.html'.")
