import xml.etree.ElementTree as ET

xml_string = """
<NewDataSet>
    <Table>
        <user_id>123</user_id>
        <name>saba</name>
        <su>satesto2</su>
    </Table>
    <Table>
        <user_id>456</user_id>
        <name>company</name>
        <su>tbilisi</su>
    </Table>
</NewDataSet>
"""

root = ET.fromstring(xml_string)

# print(root.tag)
# print(root[0].tag)
print(root[1][0].tag)
print(root[1][1].text)


rows = root.findall('Table')

print(len(rows))

for row in rows:
    print("---")

    for field in row:
        print(f"{field.tag} - {field.text}")



def parse_rows(root):
    result = []

    for row in root.findall('Table'):
        row_dict = {}
        for field in row:
            row_dict[field.tag] = field.text
        result.append(row_dict)

    return result

rows2 = parse_rows(root)

for rows in rows2:
    print(rows)