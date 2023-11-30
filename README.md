# eplink-redcap2bids
Workflow for exporting redcap braincode data to bids

Requires redcap API access (put the secret key in an environent variable called `REDCAP_API_KEY`)

Currently only creates `bids/participants.tsv`, using a subset of fields from the EPL31 project on redcap. In the future could add creation of other metadata tsv files for a more complete data dump. 

The `config.yml` contains the mapping of redcap fields to columns in the `participants.tsv` file.
