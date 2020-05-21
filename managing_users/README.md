# New user creation

To request a new user, please fill out the [Cluster User Request Form](https://forms.gle/97BZLTwX5dMXDV118). The admin team will verify that the account is allowed to be created and create the account.

# Login

[SSH Key Guide](https://linuxize.com/post/how-to-set-up-ssh-keys-on-ubuntu-1804/) We require SSH key based login from remote locations.

If at any point you want to change your password:

```
$ passwd
```

For access from an off campus location, you will need to setup an ssh key for authentication: 

You will *NOT* be able to login from a remote location if you don't have an ssh key setup.

# SLURM Compute Allocation

Depending upon your group's policies, you will either be allocated compute with respect to your group as a whole or an existing lab member will need to allocate you under their compute. If it is the former, this will be done for you. If it is the latter, your point of contact will be able to help you.

# Managing your account

This is for those groups that have a larger organizational structure:

- Kostas Group

## Your account
This account will balance your usage equally with other members of your group. It will additionally bill all usage from students working with you against your account. To look at your account:

```
$ sacctmgr show assoc Account=<your_username>-account
```

## Adding a student under your account
Giving a user access to your compute will count against your overall account and thus you are taking responsibility for their overall usage.

```
$ sacctmgr add user Name=<their_username> DefaultAccount=<your_username>-account
```

You're able to remove them from your account at any point in time as well as modify how they can use your account.
