import com.cloudbees.hudson.plugins.folder.Folder
import groovy.json.JsonSlurper

def jobsJson = new JsonSlurper().parseText(jobsToRunStr)
def jobsToRun = [:]

jobsJson.each{ it ->
  jobsToRun[it.get("name")] = it
}

def relevantJobs = { job ->
  jobsToRun.containsKey(job.name)
}

def folders = { item ->
  item instanceof Folder 
}

def handleJob = { job ->

  def params = jobsToRun[job.name]['Parameters'].collect { key, val ->
      new hudson.model.StringParameterValue(key, val)
  }
  def paramsAction = new hudson.model.ParametersAction(params)
  def cause = new hudson.model.Cause.UserIdCause()
  def causeAction = new hudson.model.CauseAction(cause)

  job.scheduleBuild2(jobsToRun[job.name]['WaitFor'], causeAction, paramsAction)
}

Jenkins.instance.items.findAll(folders).each{ folder ->
  folder.items.findAll(relevantJobs).each(handleJob)
}