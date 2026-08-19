---
layout: site
permalink: /rucio.html
title: "Rucio"
---

# Using Rucio with FCC Simulations

[Rucio](https://rucio.cern.ch) is the data management system used by FCC to
catalog and locate simulation datasets. This page describes how to set up and
use the Rucio client to find FCC samples.

## FCC Data Federation

<table style="border-collapse:collapse; width:100%;">
<thead><tr><th width="23%" style="border:1px solid var(--bs-border-color); padding:0.4rem 0.6rem;">Active RSEs</th><th style="border:1px solid var(--bs-border-color); padding:0.4rem 0.6rem; min-width:8rem;">Site</th><th style="border:1px solid var(--bs-border-color); padding:0.4rem 0.6rem;">Map</th></tr></thead>
<tr>
<td style="vertical-align:top; border:1px solid var(--bs-border-color); padding:0; font-size:0.8rem;">
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN_PROD_DISK</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN_WINTER2023_DELPHES_DISK</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN_WINTER23_DISK</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">FCC_PROD_PHYS_HIGGS</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">FCC_PROD_PHYS_TOP</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">FCC_PROD_PHYS_TOP_BACKUP</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">FCC_TEST_1</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">INFN_BARI_DISK</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">INFN_CNAF_DISK</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">SK_IEPSAS_DISK</div>
<div style="padding:0.3rem 0.6rem;">US_MIT_DISK</div>
</td>
<td style="vertical-align:top; border:1px solid var(--bs-border-color); padding:0; font-size:0.8rem;">
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN (CH)</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN (CH)</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN (CH)</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN (CH)</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN (CH)</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN (CH)</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CERN (CH)</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">INFN, Bari (IT)</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">CNAF (IT)</div>
<div style="border-bottom:1px solid var(--bs-border-color); padding:0.3rem 0.6rem;">IEPSAS (SK)</div>
<div style="padding:0.3rem 0.6rem;">MIT (US)</div>
</td>
<td style="vertical-align:top; border:1px solid var(--bs-border-color); padding:0; height:100%;">
<iframe src="{{ '/assets/html/map.html' | relative_url }}" width="100%" height="100%" style="border:none; display:block; min-height:250px;"></iframe>
</td>
</tr>
</table>

## Rucio client setup

The Rucio client is available via CVMFS. To set it up, source the FCC software
environment and then the Rucio setup script. Sourcing the Key4hep stack first is
recommended, as some Rucio releases require Python 3.10 or later — newer than
the Python 3.9 found on the Alma9 nodes of lxplus.

```
$ source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
AlmaLinux/RockyLinux/RHEL 9 detected
Setting up the Key4hep software stack nightly build latest-opt from CVMFS
Use the following command to reproduce the current environment:

        source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh -r 2026-08-18

Nightly builds are intended for testing and development, if you need a stable environment use the releases
If you have any issues, comments or requests, open an issue at https://github.com/key4hep/key4hep-spack/issues

$ source /cvmfs/fcc.cern.ch/rucio/latest/setup.sh
INFO: Set RUCIO_HOME to /cvmfs/fcc.cern.ch/rucio/latest
INFO: Rucio client environment is set up.
INFO: RUCIO_ACCOUNT is set to 'dlange'.
```

The setup script sets `RUCIO_ACCOUNT` to your current login name. If your Rucio
account was registered under a different username, override it before proceeding:

```bash
export RUCIO_ACCOUNT=<your_rucio_username>
```

To authenticate, run `rucio whoami`. Note that the FCC Rucio instance uses
token-based authentication (OIDC) rather than X.509 certificates, so this may
differ from other Rucio environments you have used:

```
$ rucio whoami

Please use your internet browser, go to:

    https://fcc-auth.rucioit.cern.ch/auth/oidc_redirect?YWd5M88eC5nJusM5i1u8gy7_polling

and authenticate with your Identity Provider.
In the next 3 minutes, Rucio Client will be polling
the Rucio authentication server for a token.
----------------------------------------------
```

Open the URL in a browser and log in with your CERN account via "CERN SSO / eduGAIN".
If this is your first time using the FCC Rucio service, a one-time account
approval is required before you can proceed — see the [next section](#one-time-account-approval).
If your account is already set up, you will see a confirmation page like this:

![Rucio login confirmation page]({{ '/assets/img/rucio_login.png' | relative_url }}){: style="max-width: 375px; display: block; margin: 1rem auto;" }

After authenticating with SSO you will see a confirmation that the Rucio client
can now fetch your token:

![Rucio authorization confirmation]({{ '/assets/img/rucio_authorized.png' | relative_url }}){: style="max-width: 375px; display: block; margin: 1rem auto;" }

The terminal will then complete the `rucio whoami` command and display your account information:

```
account_type : USER
account      : dlange
status       : ACTIVE
email        : david.lange@cern.ch
deleted_at   : None
created_at   : 2026-08-05T10:44:02
suspended_at : None
updated_at   : 2026-08-05T10:44:02
```

Your Rucio client is now set up for use.

## One-time account approval

Note: Currently this section is likely not yet correct...

If you do not yet have an FCC Rucio account, clicking "Apply for an account" on
the login page will take you to a registration form. Fill in your details and,
importantly, provide a clear explanation of your motivation in the **Notes**
field — this will speed up the approval process:

![Rucio account registration form]({{ '/assets/img/rucio_register.png' | relative_url }}){: style="max-width: 375px; display: block; margin: 1rem auto;" }

If the form is submitted successfully, the [IAM dashboard](https://fcc-auth.cern.ch/dashboard#!/home)
will confirm your registration:

![IAM for FCC dashboard after successful registration]({{ '/assets/img/rucio_iam_dashboard.png' | relative_url }}){: style="max-width: 375px; display: block; margin: 1rem auto;" }

Once submitted, your request will be reviewed by the FCC Rucio administrators.
You will be notified by email when your account has been approved. This is a
manual process — if you have not heard back within a reasonable time, do not
hesitate to reach out for help via the channels listed in the
[Getting help](#getting-help) section.

## Scopes

In Rucio, a **scope** is a namespace that groups related datasets and files,
typically corresponding to an experiment, working group, or production campaign.
All data identifiers (DIDs) in Rucio take the form `scope:name`, so knowing the
relevant scope is the first step to locating any dataset or file.

To list all available scopes:

```
$ rucio scope list
+---------------+-----------+
| SCOPE         | ACCOUNT   |
|---------------+-----------|
| user.gguerrie | gguerrie  |
| gguerrie      | gguerrie  |
| mc25          | root      |
| winter23      | fccprod   |
| winter2023    | fccprod   |
| bib           | bibprod   |
+---------------+-----------+
```

## Datasets and files

In Rucio, every piece of data is identified by a **data identifier (DID)** of the
form `scope:name`. There are three types of DIDs:

- **Files** are the individual data files.
- **Datasets** are ordered collections of files.
- **Containers** are collections of datasets or other containers, allowing
  hierarchical organization (similar to directories).

Datasets are organized hierarchically within a scope. For example, the Winter
2023 Delphes samples are in the `winter2023` scope. Use `rucio did list` with a
wildcard to browse the available containers and datasets:

```
$ rucio did list "winter2023:*" | head
+----------------------------------------------------------------------------------------------+--------------+
| SCOPE:NAME                                                                                   | [DID TYPE]   |
|----------------------------------------------------------------------------------------------+--------------|
| winter2023:91.19gev                                                                          | CONTAINER    |
| winter2023:91.19gev/tautau                                                                   | CONTAINER    |
| winter2023:91.19gev/tautau/lhef                                                              | CONTAINER    |
| winter2023:91.19gev/tautau/lhef/00016140                                                     | CONTAINER    |
| winter2023:91.19gev/tautau/lhef/00016140/                                                    | DATASET      |
| winter2023:91.19gev/tautau/idea                                                              | CONTAINER    |
| winter2023:91.19gev/tautau/idea/delphes                                                      | CONTAINER    |
+----------------------------------------------------------------------------------------------+--------------+
```

The `--filter type=dataset` option restricts the listing to datasets only:

```
$ rucio did list "winter2023:*" --filter type=dataset | head
+----------------------------------------------------------------------------------------------+--------------+
| SCOPE:NAME                                                                                   | [DID TYPE]   |
|----------------------------------------------------------------------------------------------+--------------|
| winter2023:91.19gev/tautau/lhef/00016140/                                                    | DATASET      |
| winter2023:91.19gev/tautau/idea/delphes/00016140/                                            | DATASET      |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/                                            | DATASET      |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/005/                                        | DATASET      |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/004/                                        | DATASET      |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/003/                                        | DATASET      |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/002/                                        | DATASET      |
+----------------------------------------------------------------------------------------------+--------------+
```

To list the individual files within a dataset, use `rucio list-files`:

```
$ rucio list-files winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/005/
+-------------------------------------------------------------------------------------+--------+-------------+------------+----------+
| SCOPE:NAME                                                                          | GUID   | ADLER32     | FILESIZE   | EVENTS   |
|-------------------------------------------------------------------------------------+--------+-------------+------------+----------|
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/005/ee_Zbb_delphes_16139_5000.root | (None) | ad:eb98bc8c | 818.666 MB |          |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/005/ee_Zbb_delphes_16139_5001.root | (None) | ad:673060e3 | 819.549 MB |          |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/005/ee_Zbb_delphes_16139_5002.root | (None) | ad:aabb6597 | 818.504 MB |          |
| ...                                                                                  |        |             |            |          |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/005/ee_Zbb_delphes_16139_5034.root | (None) | ad:ce4a2bdb | 819.083 MB |          |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/005/ee_Zbb_delphes_16139_5035.root | (None) | ad:7316e5df | 818.668 MB |          |
| winter2023:91.19gev/ee_Zbb/idea/delphes/00016139/005/ee_Zbb_delphes_16139_5036.root | (None) | ad:5e2622f0 | 818.759 MB |          |
+-------------------------------------------------------------------------------------+--------+-------------+------------+----------+
Total files : 37
Total size : 30.298 GB
```

Note that `rucio list-files` is deprecated; the warning can be ignored for now.

## Datasets and sites

To find which storage sites hold replicas of a dataset, use `rucio replica list dataset`:

```
$ rucio replica list dataset winter2023:IDEA/wzp6_ee_ccH_Hgg_ecm240/

DATASET: winter2023:IDEA/wzp6_ee_ccH_Hgg_ecm240/
+------------------------------+---------+---------+
| RSE                          |   FOUND |   TOTAL |
|------------------------------+---------+---------|
| INFN_CNAF_DISK               |       4 |       4 |
| CERN_WINTER2023_DELPHES_DISK |       4 |       4 |
| INFN_BARI_DISK               |       4 |       4 |
+------------------------------+---------+---------+
```

Each row is a Rucio Storage Element (RSE) — a storage site in the FCC data
federation. `FOUND` is the number of files available at that site and `TOTAL` is
the number of files in the dataset. In the example above, all four files are
fully replicated at CERN, INFN-CNAF (Bologna), and INFN-BARI.

To see the individual file replicas and their physical URLs at each site, use
`rucio replica list file`:

```
$ rucio replica list file winter2023:IDEA/wzp6_ee_ccH_Hgg_ecm240/
+------------+---------------------------------------------------+------------+-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| SCOPE      | NAME                                              | FILESIZE   | ADLER32   | RSE: REPLICA                                                                                                                                                              |
|------------+---------------------------------------------------+------------+-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| winter2023 | IDEA/wzp6_ee_ccH_Hgg_ecm240/events_011000494.root | 1.789 GB   | 75da2a3d  | INFN_BARI_DISK: davs://webdav.recas.ba.infn.it:8443/fcc/rucio/winter2023/IDEA/wzp6_ee_ccH_Hgg_ecm240/events_011000494.root                                                |
| winter2023 | IDEA/wzp6_ee_ccH_Hgg_ecm240/events_011000494.root | 1.789 GB   | 75da2a3d  | INFN_CNAF_DISK: davs://xfer-archive.cr.cnaf.infn.it:8443/fcc/rucio/winter2023/IDEA/wzp6_ee_ccH_Hgg_ecm240/events_011000494.root                                           |
| winter2023 | IDEA/wzp6_ee_ccH_Hgg_ecm240/events_011000494.root | 1.789 GB   | 75da2a3d  | CERN_WINTER2023_DELPHES_DISK: https://eospublic.cern.ch:8444//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_ccH_Hgg_ecm240/events_011000494.root |
| winter2023 | IDEA/wzp6_ee_ccH_Hgg_ecm240/events_032319350.root | 1.785 GB   | 06838c91  | INFN_BARI_DISK: davs://webdav.recas.ba.infn.it:8443/fcc/rucio/winter2023/IDEA/wzp6_ee_ccH_Hgg_ecm240/events_032319350.root                                                |
| winter2023 | IDEA/wzp6_ee_ccH_Hgg_ecm240/events_032319350.root | 1.785 GB   | 06838c91  | INFN_CNAF_DISK: davs://xfer-archive.cr.cnaf.infn.it:8443/fcc/rucio/winter2023/IDEA/wzp6_ee_ccH_Hgg_ecm240/events_032319350.root                                           |
| winter2023 | IDEA/wzp6_ee_ccH_Hgg_ecm240/events_032319350.root | 1.785 GB   | 06838c91  | CERN_WINTER2023_DELPHES_DISK: https://eospublic.cern.ch:8444//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_ccH_Hgg_ecm240/events_032319350.root |
| ...        |                                                   |            |           |                                                                                                                                                                           |
+------------+---------------------------------------------------+------------+-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

This gives the direct access URL for each replica, which can be used to open
files directly with ROOT or copy them with `xrdcp`.

## Web UI

The FCC Rucio web interface is available at
[https://fcc-webui.rucioit.cern.ch/](https://fcc-webui.rucioit.cern.ch/).
It provides a browser-based alternative to the command-line client for browsing
scopes, datasets, files, and replica locations. When the login page loads, click
"fcc" to authenticate via your CERN SSO account:

![Rucio web UI login page]({{ '/assets/img/rucio_webui_login.png' | relative_url }}){: style="max-width: 375px; display: block; margin: 1rem auto;" }

Then click "Authorize" to complete the login. Once authenticated, you can browse
scopes, search for datasets and files, and look up replica locations — the same
queries available through the command-line client. For example, the DIDs page
lets you search for datasets by scope and name pattern:

![Rucio web UI DID search]({{ '/assets/img/rucio_webui_dids.png' | relative_url }}){: style="max-width: 75%; display: block; margin: 1rem auto;" }

## Quota policies

Coming soon...

## Getting help

All Rucio commands are documented via `rucio -h` or `rucio <command> -h`. For
broader documentation on Rucio commands and concepts, see the
[Rucio documentation](https://rucio.github.io).

For FCC-specific questions and support, use the **Rucio and data lakes** channel
on the [FCC software and computing Mattermost team](https://mattermost.web.cern.ch/signup_user_complete/?id=ea9j3u7pb3refrx4y57d8qhw9y&md=link&sbr=su),
or post in the
[Distributed Computing category](https://fccsw-forum.web.cern.ch/c/distributed-computing/12)
of the FCCSW forum.
