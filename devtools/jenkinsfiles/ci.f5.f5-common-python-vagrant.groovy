#!groovy

node("vagrant") {
    def versions
    versions = [
            "11.5.4-hf1", "11.6.0", "11.6.1", "12.0.0", "12.1.0-hf1"
    ]

    should_rebuild_all = REBUILD_ALL.toBoolean()

    slackMessage('#aaaaaa', "Build Started: ${env.JOB_NAME}")

    try {
        stage 'Checkout'
        git url: 'https://gitswarm.f5net.com/optimus/vagrantfiles.git'
        for (ver in versions) {
            sh "mkdir -p ${ver}"
            sh "cp f5-common-python/Vagrantfile.${ver} ./${ver}/Vagrantfile"
        }

        if (should_rebuild_all) {
            stage 'Cleanup'
            for (ver in versions) {
                print "Cleaning up virtual machines"
                cleanupVirtualMachine(ver)
            }
            for (ver in versions) {
                print "Cleaning up any virtual machine remnants"
                cleanupRemnants(ver)
            }
        }

        stage 'Build'
        for (ver in versions) {
            if (!should_rebuild_all) {
                def chk = sh returnStatus: true, script: "vboxmanage showvminfo ci.f5-common-python.${ver}.internal"
                if (chk == 0) {
                    print "VM ${ver} exists, not rebuilding"
                    continue
                } else {
                    print "Rebuilding VM ${ver}"
                    buildVirtualMachine(ver)
                }
            } else {
                print "Rebuilding all VMs"
                buildVirtualMachine(ver)
            }
        }

        slackMessage('good', "Build Finished: ${env.JOB_NAME}")
    } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
        // this condition means a user probably aborted
        throw e
    } catch (e) {
        // this condition means a shell step failed
        slackMessage('danger', "Build Failed: ${env.JOB_NAME}")
        throw e
    }
}

def slackMessage(color, message) {
    slackSend channel: SLACK_CHANNEL,
            color: color,
            message: message,
            teamDomain: SLACK_DOMAIN,
            token: SLACK_TOKEN
}

def cleanupVirtualMachine(ver) {
    def chk = sh returnStatus: true, script: "vboxmanage showvminfo ci.f5-common-python.${ver}.internal"
    if (chk == 0) {
        chk = sh returnStatus: true, script: "cd ${ver} && vagrant destroy --force"
        if (chk == 0) {
            return true
        } else {
            throw new Exception("Failed to delete the vagrant env")
        }
    }
}

def cleanupRemnants(ver) {
    def result
    result = sh returnStdout: true,
            script: "vboxmanage unregistervm ci.f5-common-python.${ver}.internal --delete 2>&1 || true"

    /**
     * I agree, this is incredibly dumb that I have to do it this way.
     * But if I dont, then I have no way to capture stderr in the
     * exception that is raised even if I do the redirect.
     */
    if (result.contains('VBOX_E_OBJECT_NOT_FOUND')) {
        /**
         * Ensures the the directory is truely gone. Virtualbox will raise an
         * error if you try to delete a non-existant VM. There may be cases
         * though that this cleanup process fails though, so we want to deliberately
         * delete the directory that contains the VM files
         */
        dir ("/var/lib/jenkins/VirtualBox VMs/ci.f5-common-python.${ver}.internal") {
            deleteDir()
        }
    }
}

def buildVirtualMachine(ver) {
    def success

    success = false

    // Iterating forever would be dangerous, so only try 10 times
    for (i = 0; i < 10; i++) {
        dir("${ver}") {
            chk = sh returnStatus: true, script: "vagrant up"
            if (chk == 0) {
                snap = sh returnStatus: true, script: "vboxmanage snapshot ci.f5-common-python.${ver}.internal take initial"
                if (snap != 0) {
                    throw new Exception("Failed to snapshot the build")
                }

                halt = sh returnStatus: true, script: "vagrant halt --force"
                if (halt != 0) {
                    throw new Exception("Failed to halt the build")
                }
                success = true
            }
            sleep(1)
        }

        if (success) {
            return true
        }
    }

    // Catch all exception so that we report failure
    throw new Exception("Failed to build the VM")
}
