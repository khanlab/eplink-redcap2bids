configfile: 'config.yml'

envvars:
    'REDCAP_API_KEY'

rule create_participants_tsv:
    params:
        api_url=config['api_url'],
        api_key=os.environ['REDCAP_API_KEY'],
        data_dictionary=config['data_dictionary']
    output: 
        tsv='bids/participants.tsv'
    script: 'scripts/create_participants_tsv.py'
