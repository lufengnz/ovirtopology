#!/usr/bin/python3

import os
import json
import uuid

def generate_json_table(json_data, json_name):
    table_html = f'<div id="{json_name}" class="tabcontent">'
    table_html += f"<h3>{json_name}</h3>"
    table_html += '<table border="1" cellpadding="5" cellspacing="0">'
    
    def create_table(json_obj, parent_key=''):
        nonlocal table_html
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                new_key = f"{parent_key}.{key}" if parent_key else key
                create_table(value, new_key)
        else:
            row_id = uuid.uuid4().hex
            table_html += f'<tr id="{row_id}">'
            table_html += f'<td><strong>{parent_key}</strong></td>'
            table_html += f'<td>{json_obj}</td>'
            table_html += '</tr>'
    
    create_table(json_data)
    table_html += '</table>'
    table_html += '</div>'
    return table_html

def generate_html_output(json_files):
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>oVirt Topology</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
            }
            #tabs {
                width: 200px;
                border-right: 2px solid #ddd;
                padding: 10px;
                background-color: #f1f1f1;
            }
            .tab {
                display: block;
                padding: 10px;
                margin-bottom: 5px;
                background-color: #f1f1f1;
                cursor: pointer;
                text-align: left;
            }
            .tab:hover, .active-tab {
                background-color: #ddd;
            }
            .tabcontent {
                display: none;
                padding: 20px;
                flex-grow: 1;
            }
            iframe {
                width: 100%;
                height: 600px;
                border: none;
            }
        </style>
    </head>
    <body>
        <div id="tabs">
    '''
    
    engine_file = next((f for f in json_files if 'engine.json' in f), None)
    if engine_file:
        json_files.remove(engine_file)
        json_files.insert(0, engine_file)
    
    if os.path.exists("db_output.html"):
        json_files.insert(1, "db_output.html")
    
    for json_file in json_files:
        json_name = os.path.basename(json_file).replace('.json', '').replace('.html', '')
        html_content += f'<div class="tab" onclick="openTab(\'{json_name}\')">{json_name}</div>'
    
    html_content += '</div><div id="content">'
    
    for json_file in json_files:
        json_name = os.path.basename(json_file).replace('.json', '').replace('.html', '')
        if json_file.endswith('.html'):
            html_content += f'<div id="{json_name}" class="tabcontent"><iframe src="{json_file}"></iframe></div>'
        else:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
                html_content += generate_json_table(json_data, json_name)
    
    html_content += '''
        </div>
        <script>
            function openTab(tabName) {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {
                    tabcontent[i].style.display = "none";
                }
                tablinks = document.getElementsByClassName("tab");
                for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].className = tablinks[i].className.replace(" active-tab", "");
                }
                document.getElementById(tabName).style.display = "block";
                event.currentTarget.className += " active-tab";
            }
            document.getElementsByClassName("tab")[0].click();
        </script>
    </body>
    </html>
    '''
    
    return html_content

json_files = [f for f in os.listdir('.') if f.endswith('.json')]

if not json_files:
    print("No JSON files found in the current directory.")
else:
    html_output = generate_html_output(json_files)
    
    with open("output.html", "w") as f:
        f.write(html_output)
    
    print("HTML output file created: output.html")
