# AssignBackupPolicy-fn
This template demonstrates how to automate the configuration of backup policies for OCI Block Storage volumes based on volume tags. It uses OCI Events and OCI Functions. When a new boot or block volume is created, an event is emitted that triggers an OCI Function. The function reads the volume’s tags and automatically assigns the appropriate backup policy.

# Pre-Requisites

Create a [dynamic group](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingdynamicgroups.htm) for the compartment where block storage volumes will be created. You can use the following matching rule:

ALL {resource.type = 'fnfunc', resource.compartment.id = 'compartment-id'}

The following policies are required for this dynamic group:

Allow dynamic-group <dynamic-group-name> to manage backup-policy-assignments in compartment id <compartment OCID>
Allow dynamic-group <dynamic-group-name> to use volume-family in compartment id <compartment OCID>

