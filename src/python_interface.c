#include "wireguard.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

/**
 * Generate a private key and store it in result.
 * @param result    Pointer to the location where the key will be stored.
 */
void generate_private_key(unsigned char *result)
{
    wg_generate_private_key(result);
}

/**
 * Generate a public key and store it in result.
 * @param private   The private key to which the public key should correspond.
 * @param result    Pointer to the location where the key will be stored.
 */
void generate_public_key(unsigned char *private, unsigned char *result)
{
    wg_generate_public_key(result, private);
}

void key_to_string(wg_key key, char *result)
{
    wg_key_to_base64(result, key);
}

void key_from_string(char *string, wg_key key)
{
    wg_key_from_base64(key, string);
}

void add_server_device(char *device_name, uint16_t port, wg_key private_key)
{
    wg_device new_device = {
        .flags = WGDEVICE_HAS_PRIVATE_KEY | WGDEVICE_HAS_LISTEN_PORT,
        .listen_port = port,
    };

    snprintf(new_device.name, IFNAMSIZ, "%s", device_name);
    memcpy(new_device.private_key, private_key, sizeof(new_device.private_key));

    if (wg_add_device(new_device.name) < 0) {
        perror("Unable to add device");
        exit(1);
    }

    if (wg_set_device(&new_device) < 0) {
        perror("Unable to set device");
        exit(1);
    }
}

void add_client_device(char *device_name, wg_key private_key)
{
    wg_device new_device = {
        .flags = WGDEVICE_HAS_PRIVATE_KEY,
    };

    snprintf(new_device.name, IFNAMSIZ, "%s", device_name);
    memcpy(new_device.private_key, private_key, sizeof(new_device.private_key));

    if (wg_add_device(new_device.name) < 0) {
        perror("Unable to add device");
        exit(1);
    }

    if (wg_set_device(&new_device) < 0) {
        perror("Unable to set device");
        exit(1);
    }
}

/**
 * Add a peer to device 'device_name'.
 * @param device_name
 * @param public_key
 * @param ip_address
 */
void add_server_peer(char *device_name, unsigned char *public_key, char *ip_address, uint16_t port)
{
    struct sockaddr_in dest_addr;
    bzero(&dest_addr, sizeof (dest_addr));
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(port);
    inet_pton(AF_INET, ip_address, &dest_addr.sin_addr);

    wg_allowedip allowed_ip;
    bzero(&allowed_ip, sizeof (allowed_ip));
    inet_pton(AF_INET, "0.0.0.0", &allowed_ip.ip4);
    allowed_ip.family = AF_INET;
    allowed_ip.cidr = 0;

    wg_peer new_peer = {
        .flags = WGPEER_HAS_PUBLIC_KEY | WGPEER_REPLACE_ALLOWEDIPS
    };

    new_peer.endpoint.addr4 = dest_addr;
    new_peer.first_allowedip = &allowed_ip;
    new_peer.last_allowedip = &allowed_ip;
    memcpy(new_peer.public_key, public_key, sizeof(new_peer.public_key));
    wg_device *device;
    if(wg_get_device(&device, device_name) < 0) {
        perror("Unable to get device");
        exit(1);
    }
    wg_peer *peer;
    if (device->last_peer == NULL) {
        device->first_peer = &new_peer;
        device->last_peer = &new_peer;
    } else {
        peer = device->last_peer;
        peer->next_peer = &new_peer;
        device->last_peer = &new_peer;
    }

    wg_set_device(device);
}

/**
 * Add a peer to device 'device_name'.
 * @param device_name
 * @param public_key
 * @param ip_address
 */
void add_client_peer(char *device_name, unsigned char *public_key, char *ip_address)
{
    wg_allowedip allowed_ip;
    bzero(&allowed_ip, sizeof (allowed_ip));
    inet_pton(AF_INET, ip_address, &allowed_ip.ip4);
    allowed_ip.family = AF_INET;
    allowed_ip.cidr = 32;

    wg_peer new_peer = {
        .flags = WGPEER_HAS_PUBLIC_KEY | WGPEER_REPLACE_ALLOWEDIPS
    };

    new_peer.first_allowedip = &allowed_ip;
    new_peer.last_allowedip = &allowed_ip;
    memcpy(new_peer.public_key, public_key, sizeof(new_peer.public_key));
    wg_device *device;
    if(wg_get_device(&device, device_name) < 0) {
        perror("Unable to get device");
        exit(1);
    }
    wg_peer *peer;
    if (device->last_peer == NULL) {
        device->first_peer = &new_peer;
        device->last_peer = &new_peer;
    } else {
        peer = device->last_peer;
        peer->next_peer = &new_peer;
        device->last_peer = &new_peer;
    }

    wg_set_device(device);
}

int delete_device(char *device_name)
{
    if (wg_del_device(device_name) < 0) {
        perror("Unable to delete device");
        return 1;
    }
    return 0;
}

void list_devices(void)
{
    char *device_names, *device_name;
    size_t len;

    device_names = wg_list_device_names();
    if (!device_names) {
        perror("Unable to get device names");
        exit(1);
    }
    wg_for_each_device_name(device_names, device_name, len) {
        wg_device *device;
        wg_peer *peer;
        wg_key_b64_string key;

        if (wg_get_device(&device, device_name) < 0) {
            perror("Unable to get device");
            continue;
        }
        if (device->flags & WGDEVICE_HAS_PUBLIC_KEY) {
            wg_key_to_base64(key, device->public_key);
            printf("%s has public key %s\n", device_name, key);
        } else
            printf("%s has no public key\n", device_name);
        wg_for_each_peer(device, peer) {
            wg_key_to_base64(key, peer->public_key);
            printf(" - peer %s\n", key);
        }
        wg_free_device(device);
    }
    free(device_names);
}