# AssignBackupPolicy-fn
This template demonstrates how to automate the configuration of backup policies for OCI Block Storage volumes based on volume tags. It uses OCI Events and OCI Functions. When a new boot or block volume is created, an event is emitted that triggers an OCI Function. The function reads the volume’s tags and automatically assigns the appropriate backup policy.

## Pre-Requisites

Create a [dynamic group](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingdynamicgroups.htm) for the compartment where block storage volumes will be created. You can use the following matching rule:

ALL {resource.type = 'fnfunc', resource.compartment.id = 'compartment-id'}

The following policies are required for this dynamic group:
```
Allow dynamic-group <dynamic-group-name> to manage backup-policy-assignments in compartment id <compartment OCID>
Allow dynamic-group <dynamic-group-name> to use volume-family in compartment id <compartment OCID>
```
Before you deploy AssignBackupPolicy function, make sure you have run step C of the [Oracle Functions Quick Start Guide for Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartcloudshell.htm)

*Note: In this example I am using OCI Cloud Shell for deploying my function. Alternatively, you can also use your local machine or OCI Compute as your dev environments. refer the [Functions Quick Start on Local Host](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartlocalhost.htm).*

## Setup your Cloud Shell environment

Login to OCI Cloud Console and Launch Cloud Shell

Use the context for your region, here us-phoenix-1 is used as an example
```
fn list context
fn use context us-phoenix-1
```

Update the context with the function's compartment ID
```
fn update context oracle.compartment-id ocid1.compartment.oc1..
```
Update the context with the location of the Registry you want to use. As an example I am using for phx for us-phoenix-1 region
```
fn update context registry phx.ocir.io/<tenancy-namespace>/<OCIR-repo-name>
```
To find a region key for the region you are using see [OCI Region Availbility](https://docs.oracle.com/en-us/iaas/analytics-for-applications/doc/region-availability.html) map.

## Authenticate to OCIR registry

Generate [Auth Token](https://docs.cloud.oracle.com/en-us/iaas/Content/Registry/Tasks/registrygettingauthtoken.htm) and log into the Registry using the Auth Token as your password. As an example I am using for phx for us-phoenix-1 region
```
docker login -u '<tenancy-namespace>/<user-name>' phx.ocir.io
```
Check that it returns **Login Succeeded**.

## Create, deploy and invoke your function

Copy assign_backup_policy folder to Cloud Shell as described in [Transferring Files to CLoud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/devcloudshellgettingstarted.htm#Cloud_Shell_Transferring_Files). Edit func.yaml file. Set TAG_NAMESPACE to your backup tag namespace. As an example my tag namespace is called *Production*
```
config:
  TAG_NAME: BackupPolicyID
  TAG_NAMESPACE: Production
```
*Note: Optionally you can change TAG_NAME value to the name of the tag that you assign to Block Storage volumes. In my example TAG_NAME is set to BackupPolicyID*

Create an application *backup_policy* as described in [Create Applications](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionscreatingapps.htm) and after that deploy *assign_backup_policy* function by running the following command
```
fn -v deploy --app backup_policy
```

Check that the function is successfully deployed
```
fn list functions backup_policy
```
You should see *assign_backup_policy* listed.

I recommend enabling logging for the function you created as described in [Enable and View Function Logs](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsexportingfunctionlogfiles.htm#usingconsole)

## Create an event rule

Create an event rule with a **Condition**: Event Type, **Service Name**: Block Volume, and **Event Type**: Create Volume End. Add a **Condition** and with the **Attribute Name** set to compartmentID, and specify your compartment OCID in the **Attribute Value** field.

Under Actions, set **Action Type** to Functions and select **Function Compartment**, **Function Application**, and **Function Name**.

![image](https://github.com/mprestin77/AssignBackupPolicy-fn/blob/main/images/EventRule.png)

## Validate that the function is invoked when a new volume is created

Create a backup policy and add a schedule as descibed in [Create a Backup Policy](https://docs.oracle.com/en-us/iaas/private-cloud-appliance/cmn/block/creating-a-backup-policy.htm) 

![image](https://github.com/mprestin77/AssignBackupPolicy-fn/blob/main/images/BackupPolicy.png)

Under **Details** copy the backup policy OCID.

Create a new Block Storage volume or create a new compute instance with a boot volume in the specified compartment or one of its sub-compartments. Assign a tag to the volume matching **TAG_NAMESPACE** and **TAG_NAME** from func.yaml file, and assign the backup policy OCID as the tag value. Once the volume is created it should automatically invoke *assign_backup_policy* function and assign the specified backup policy OCID



