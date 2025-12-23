import oci
import io
import json
import logging
from fdk import response

logging.getLogger('oci').setLevel(logging.INFO)

def handler(ctx, data: io.BytesIO = None):
    # 1. Retrieve configuration parameters from Function Config
    cfg = ctx.Config()
    tag_namespace = cfg.get("TAG_NAMESPACE")
    tag_key = cfg.get("TAG_NAME")
    
    try:
        # 2. Parse the Event Body
        event_body = json.loads(data.getvalue())
        volume_id = event_body.get("data", {}).get("resourceId")

        
        if not volume_id:
            message = "No volume ID found in event"
            logging.getLogger().info(message)
            return response.Response(ctx, response_data=message, status_code=400)

        # Initialize OCI client
        signer = oci.auth.signers.get_resource_principals_signer()
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
            message = f"Assigned policy {policy_id} to volume {volume_id}"
            logging.getLogger().info(message)
            return response.Response(ctx, response_data=message, status_code=200)
        
        message = "No matching backup tag found on volume"
        logging.getLogger().info(message)
        return response.Response(ctx, response_data="message", status_code=200)

    except Exception as e:
        logging.getLogger().error(str(e))
        return response.Response(ctx, response_data=str(e), status_code=500)

