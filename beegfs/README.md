# BeeGFS

We leverage BeeGFS as our global file system. We have multiple storage pools that are accessible by individual users.

## Quotas and storage types

We currently run two tiers of storage and each has a user level quota enforced in two ways

1) total storage size
2) total number of inodes (in general less large files is better for performance than many small files)

| Pool | Size Quota | inode Quota |   Default Directories  |
|------|------------|-------------|------------------------|
| HDD  |   10TB     |     100M    | /home and /archive     |
| NVMe |   500GB    |       5M    | /Datasets and /scratch |

These pools are distributed across multiple machines and provide a single unified filesystem. Some notes for the end user:

1) When moving files from one pool to the other, use cp and rm instead of mv as mv will simply change metadata and not the physical location of the files.
2) Datasets and log files on HDDs tend to slow down the system if too many people use them that way. Try to avoid this usage pattern by appropriately using `/Datasets` and `/scratch`.

### Checking your quota
Your quota gets printed out whenever you make a new shell on kostas-ap. This is live up to date information. To get a new usage amount:

```
beegfs-ctl --getquota --uid $(id -u)
```

### Finding files with BeeGFS filters
```
beegfs-ctl --find --help
```

## A note about datasets
We maintain a set of commonly used datasets within the `/Datasets` folder that is accessible by every user in the cluster. This helps reduce the overall footprint of large datasets that individuals would otherwise need their own copies of.
