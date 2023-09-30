from bs4 import BeautifulSoup

# Sample HTML content
html_content = """
<html>
<head>
    <title>Sample Page</title>
</head>
<body>
    <div class="content">
        <p class="paragraph" id="first-paragraph">This is a paragraph.</p>
        <p class="paragraph hello" id="second-paragraph">Hello, World!</p>
    </div>
</body>
</html>
"""

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find a specific tag (e.g., the second <p> tag)
p_tag = soup.find('p', id='second-paragraph')

# Get the class attribute of the tag
class_attribute = p_tag.get('class')

# Print the class attribute
print("Class Attribute:", class_attribute)