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
        self.create_new_folder(job_path)
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
            param_dict["param_name"] =  param
            suffix += 1

        job_path +=  "/" + slave_name
        if not self.srvr.job_exists(job_path):
            self.srvr.create_job(job_path, new_job_config.toxml())
        else:
            self.srvr.reconfig_job(job_path, new_job_config.toxml())

        self.srvr.enable_job(job_path)
        self.srvr.build_job(job_path, param_dict)


    def create_new_folder(self, full_path_with_folder_name):
        folder_hierarchy = full_path_with_folder_name.split("/")
        folder_name = ""
        for folder in folder_hierarchy:
            if not folder_name:
                folder_name += folder
            else:    
                folder_name += "/" + folder
            
            if not self.srvr.job_exists(folder_name):
                self.srvr.create_job(folder_name, self.new_folder_config.toxml())
