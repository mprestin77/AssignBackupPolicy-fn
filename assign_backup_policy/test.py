import oci
import io
import json
#from fdk import response

#def handler(ctx, data: io.BytesIO = None):
# 1. Retrieve configuration parameters from Function Config
#    cfg = ctx.Config
#    tag_namespace = cfg["TAG_NAMESPACE"]
#    tag_key = cfg["TAG_NAME"]
tag_namespace = "Production"
tag_key = "BackupPolicyID"
    
try:
        # 2. Parse the Event Body
#        event_body = json.loads(data.getvalue())
        volume_id = "ocid1.volume.oc1.phx.abyhqljrel4jc5ecalndk2jqdfhp2jjrlnelccscbvjfvq7dpjp2n622qd7a"
        
        print(volume_id)
        if not volume_id:
            print("ERROR in volume id", volume_id)
            exit(1)
#            return response.Response(ctx, response_data="No volume ID found in event", status_code=400)

        # Initialize OCI client
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
        bs_client = oci.core.BlockstorageClient(config={}, signer=signer)
        
        # 3. Get the specific volume to check its tags
        volume = bs_client.get_volume(volume_id).data
        defined_tags = volume.defined_tags or {}
        policy_id = defined_tags.get(tag_namespace, {}).get(tag_key)

        if policy_id:
            # 4. Create the backup policy assignment
            assignment_details = oci.core.models.CreateVolumeBackupPolicyAssignmentDetails(
                asset_id=volume_id,
                policy_id=policy_id
            )
            bs_client.create_volume_backup_policy_assignment(assignment_details)
#            return response.Response(ctx, response_data=f"Assigned {policy_id} to {volume_id}", status_code=200)
        
#        return response.Response(ctx, response_data="No matching backup tag found on volume", status_code=200)

except Exception as e:
        print(str(e))
#        return response.Response(ctx, response_data=str(e), status_code=500)

