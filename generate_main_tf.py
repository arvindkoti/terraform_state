import json
import os

def parse_tfstate_file(tfstate_file_path, main_tf_file_path):
    # Read the contents of the tfstate file
    with open(tfstate_file_path) as f:
        tfstate = json.load(f)

    # Generate the main.tf file
    with open(main_tf_file_path, 'w') as f:
        # Write the provider block
        provider = tfstate['modules'][0]['resources']['data.openstack_client_config.current']['primary']['attributes']
        provider_str = f"provider \"openstack\" {{\n  user_name   = \"{provider['username']}\"\n  tenant_name = \"{provider['tenant_name']}\"\n  password    = \"{provider['password']}\"\n  auth_url    = \"{provider['auth_url']}\"\n  region      = \"{provider['region_name']}\"\n}}\n"
        f.write(provider_str)

        # Write the resources
        for resource in tfstate['modules'][0]['resources'].values():
            if resource['type'].startswith('openstack_compute_instance_v2'):
                instance = resource['primary']['attributes']
                instance_str = f"resource \"openstack_compute_instance_v2\" \"{instance['name']}\" {{\n  name            = \"{instance['name']}\"\n  image_name      = \"{instance['image_name']}\"\n  flavor_name     = \"{instance['flavor_name']}\"\n  key_pair        = \"{instance['key_pair']}\"\n  availability_zone = \"{instance['availability_zone']}\"\n  network {{\n    name = \"{instance['network.#']}\"\n  }}\n}}\n"
                f.write(instance_str)

    print(f"Generated {main_tf_file_path} from {tfstate_file_path}.")

if __name__ == '__main__':
    tfstate_file_path = 'terraform.tfstate'
    main_tf_file_path = 'main.tf'
    parse_tfstate_file(tfstate_file_path, main_tf_file_path)
