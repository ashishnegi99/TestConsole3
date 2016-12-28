import jenkins
from xml.dom import minidom as XMLDom

class JenkinsApp:

    # TDOD: write a wrapper over xml minidom and move these functions to that place
    def update_node_val(self, xml_dom, node_name, node_data):
        assigned_node = xml_dom.getElementsByTagName(node_name)[0]
        for node in assigned_node.childNodes:
            if node.nodeType == node.TEXT_NODE:
                node.data = node_data


    def update_node_child(self, xml_dom, node_name, child_elem):
        assigned_node = xml_dom.getElementsByTagName(node_name)[0]
        assigned_node.appendChild(child_elem)
    
    #end of xmlminidom helper functions 

    def __init__(self, host, username, password):
        self.srvr =  jenkins.Jenkins(host, username, password)
        self.new_folder_config = XMLDom.parse('app/runtime/configs/new_folder_config.xml')
        #self.new_job_config = XMLDom.parse('app/runtime/configs/new_job_config.xml')


    def create_jnkns_cron_job(self, job_path, slave_name, command, *params):
        self.create_folder(job_path)
        new_job_config = XMLDom.parse('app/runtime/configs/new_cron_job_config.xml')
        self.update_node_val(new_job_config, "assignedNode", slave_name)
        self.update_node_val(new_job_config, "command", command)

        param_config = '<hudson.model.StringParameterDefinition><name>param</name><description></description><defaultValue></defaultValue></hudson.model.StringParameterDefinition>'
        suffix = 1
        param_dict = {}
        for param in params:
            param_node = XMLDom.parseString(param_config)
            param_name = "param" + str(suffix)
            self.update_node_val(param_node, "name", param_name)
            self.update_node_child(new_job_config, "parameterDefinitions", param_node.firstChild)
            param_dict[param_name] =  param
            suffix += 1

        job_path +=  "/" + slave_name
        if not self.srvr.job_exists(job_path):
            self.srvr.create_job(job_path, new_job_config.toxml())
        else:
            self.srvr.reconfig_job(job_path, new_job_config.toxml())

        self.srvr.enable_job(job_path)
        self.srvr.build_job(job_path, param_dict)


    def create_job(self, name, path, check_path, slave_name, command, nobuild, *params):
        if check_path:
            self.create_folder(path)
        new_job_config = XMLDom.parse('app/runtime/configs/new_job_config.xml')
        self.update_node_val(new_job_config, "assignedNode", slave_name)
        self.update_node_val(new_job_config, "command", command)

        param_config = '<hudson.model.StringParameterDefinition><name>param</name><description></description><defaultValue></defaultValue></hudson.model.StringParameterDefinition>'
        suffix = 1
        param_dict = {}
        for param in params:
            param_node = XMLDom.parseString(param_config)
            param_name = "param" + str(suffix)
            self.update_node_val(param_node, "name", param_name)
            self.update_node_child(new_job_config, "parameterDefinitions", param_node.firstChild)
            param_dict[param_name] =  param
            suffix += 1

        job_path = path + "/" + name
        if not self.srvr.job_exists(job_path):
            self.srvr.create_job(job_path, new_job_config.toxml())
        else:
            self.srvr.reconfig_job(job_path, new_job_config.toxml())

        self.srvr.enable_job(job_path)
        if not nobuild:
            self.srvr.build_job(job_path, param_dict)


    def create_folder(self, full_path_with_folder_name):
        folder_hierarchy = full_path_with_folder_name.split("/")
        folder_name = ""
        for folder in folder_hierarchy:
            if not folder_name:
                folder_name += folder
            else:    
                folder_name += "/" + folder
            
            if not self.srvr.job_exists(folder_name):
                self.srvr.create_job(folder_name, self.new_folder_config.toxml())

    def sample_groovy():
        jobsToRun = []
        jobsToRun.append(create_groovy_job('IPC2_01', 10, param1="some long param", param2="def"))
        jobsToRun.append(create_groovy_job('IPC2_02', 6, param1="ac", param2="df"))
        jstr = json.dumps(jobsToRun)
        schedule_job(jstr)
    
    def create_groovy_job(self, job_name, wait_in_sec, **params):
        job = {}
        job["name"] = job_name
        job["WaitFor"] = wait_in_sec
        parameters = { "param1" : params.get("param1") , "param2" : params.get("param2") }
        job["Parameters"] = parameters
        return job

    def schedule_job(self, jobs_as_json_str):
        with open('schedule.groovy', 'r') as content_file:
            content = content_file.read()

        content = "def jobsToRunStr = '" + jobs_as_json_str + "'\n" + content
        info = self.srvr.run_script(content)
