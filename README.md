# AssignBackupPolicy-fn
This template demonstrates how to automate the configuration of backup policies for OCI Block Storage volumes based on volume tags. It uses OCI Events and OCI Functions. When a new boot or block volume is created, an event is emitted that triggers an OCI Function. The function reads the volume’s tags and automatically assigns the appropriate backup policy.

# Pre-Requisites

Create a [dynamic group](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingdynamicgroups.htm) for the compartment where block storage volumes will be created. You can use the following matching rule:

ALL {resource.type = 'fnfunc', resource.compartment.id = 'compartment-id'}

The following policies are required for this dynamic group:
```
Allow dynamic-group <dynamic-group-name> to manage backup-policy-assignments in compartment id <compartment OCID>
Allow dynamic-group <dynamic-group-name> to use volume-family in compartment id <compartment OCID>
```
Before you deploy AssignBackupPolicy function, make sure you have run step C of the [Oracle Functions Quick Start Guide for Cloud Shell](https://www.oracle.com/webfolder/technetwork/tutorials/infographics/oci_functions_cloudshell_quickview/functions_quickview_top/functions_quickview/index.html)

*Note: Alternatively, You can also use your local machine or OCI Compute as your dev environments. refer the quick start guide.*

**Setup your cloudshell environment**

Login to OCI Cloud Console and Launch cloud shell

Use the context for your region, here us-phoenix-1 is used as an example
```
fn list context
fn use context us-phoenix-1
```
Set up your Cloud Shell dev environment
```
Update the context with the function's compartment ID
```
fn update context oracle.compartment-id ocid1.compartment.oc1..
```
Update the context with the location of the Registry you want to use. As an example I am using for phx for us-phoenix-1 region
```
fn update context registry phx.ocir.io/<tenancy-namespace>/<OCIR-repo-name>
```

**Authenticate to OCIR registry**

Generate [Auth Token](https://docs.cloud.oracle.com/en-us/iaas/Content/Registry/Tasks/registrygettingauthtoken.htm) 

Log into the Registry using the Auth Token as your password
Create an event rule with a **Condition**: Event Type, **Service Name**: Block Volume, and **Event Type**: Create Volume End

Log into the Registry using the Auth Token as your password. As an example I am using for phx for us-phoenix-1 region
docker login -u '<tenancy-namespace>/<user-name>' phx.ocir.io

**Create, deploy and invoke your function**
```
fn init --runtime python

```

Under Actions, set **Action Type** to Functions and select **Function Compartment**, **Function Application**, and **Function Name**.

![image](https://github.com/mprestin77/AssignBackupPolicy-fn/blob/main/images/EventRule.png)



