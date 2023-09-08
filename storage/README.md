# Storage

We supply two levels of storage that are logically and physically separated. Each has quotas and rules that manage the access and usage internally.

## Storage types

1) total storage size
2) total number of inodes (in general less large files is better for performance than many small files)

| Pool | Size Quota | inode Quota |   Default Directories  |
|------|------------|-------------|------------------------|
| HDD  |    4TB     |      10M    | /home                  |
| NVMe |   100GB    |             | /mnt/kostas_graid      |

## HDD

We maintain a TrueNAS Scale based ZFS server for serving home folders for our users. These home folders are accessile through every node within the cluster. Users will see this in `/home/<username>` which is created during the first login.

This is the bulk storage for our users to maintain some history on their experiments. Datasets and log files on HDDs tend to slow down the system if too many people use them that way. Try to avoid this usage pattern. This is default on `/home`.

## NVMe

We maintain a GRAID based server with 40TB of NVMe storage. The uplink for this node into the network is a dual port 100Gbps card allowing for remote failover.

This storage is separated into user software environments and datasets.

### User Software

User software can be found in `/mnt/kostas_graid/sw/envs`. Users are free to make their own folders and each user is allocated 100GB for software.

### Datasets

Datasets can be found in `/mnt/kostas_graid/datsets`. Users are free to make their own folders and there is not currently a quota in place (if more than 1TB please reach out to a cluster admin!). This data is automatically cleaned up based on the file access time. If a file has not been access more than 14 days, it will be removed. Empty folders are also removed. You can check the last time a file as been accessed with:

```
ls -lutr
```
