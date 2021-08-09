#!/usr/bin/env python3

'''
this script is for /terminal page
'''

from flask import render_template,redirect,Response,request,jsonify
from web_interface.functions.web_modules import check_login ,replace_user ,replace_dashboard_title
from modules.logger import Logger

terminalLogger = Logger(file_name='terminal')

class TerminalWeb:

    def run(self):
        if not (check_login()):  # check if user is logged in ,returns true if is logged in
            return redirect('/login' ,code=302)

        page = self.read_page()
        page = replace_user(page=page)
        page = page.replace('{to_replace_text}', self.add_element())
        page = replace_dashboard_title(page=page, name='Terminal')
        return page

    def read_page(self):
        template = render_template('dashboard.html')
        return template

    def add_element(self):
        html_text = '''

<div class="form-group mb-2">
    <label class="sr-only">Terminal Command</label>
    <input type="text" class="form-control command_input" placeholder="Command" required>
</div>
    <p class="terminal_get_default_target">Default Target --> None</p>
    <button class="btn btn-success mb-2 my-3 event_send_cmd">Execute</button>
                
<div class="terminal" data-content="C2X Terminal">
    <div class="terminal-body">
  <p></p>
    </div>
</div>
<br>
<button class="btn btn-primary mb-2 clear_terminal_history">Clear Terminal History</button>

        '''
        return html_text

def terminal_get_output_url_func(streamer_function):
    # streamer_function is function for get terminal.txt file

    if not (check_login()):  # check if user is logged in ,returns true if is logged in
        return redirect('/login', code=302)

    return Response(streamer_function(), mimetype="text/plain", content_type="text/event-stream")

def send_terminal_cmd_func(server_module_var):

    if not (check_login()):  # check if user is logged in ,returns true if is logged in
        return redirect('/login', code=302)

    if request.form['cmd']:
        command = request.form['cmd']
        try:
            server_module_var.send_command_from_terminal(command=command)
        except AttributeError:
            terminalLogger.log(text='First Start the Server !')

    return 'Command Request Sent'

def terminal_get_default_target_func(server_module_var):

    if not (check_login()):  # check if user is logged in ,returns true if is logged in
        return redirect('/login', code=302)

    temp_list = []

    if ((server_module_var is not None) and (server_module_var.default_target is not None)):

        temp_list = [server_module_var.default_target]

    else:
        temp_list = ['None']

    return jsonify(temp_list)