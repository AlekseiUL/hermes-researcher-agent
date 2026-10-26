"""Offline scorer for normalized benchmark annotations, not a language-model judge."""
def grade(case, output):
    errors=[]
    if not isinstance(output, dict): return ['output must be an object']
    sections=output.get('sections',{})
    if not isinstance(sections, dict): return ['sections must be an object']
    for key in case['required_sections']:
        if not isinstance(sections.get(key),str) or not sections[key].strip(): errors.append('missing section:'+key)
    if output.get('decision') != case['expected_decision']: errors.append('unsupported decision')
    claims=output.get('claims')
    if not isinstance(claims,list): return errors+['claims must be a list']
    seen=set()
    for claim in claims:
        if not isinstance(claim,dict): errors.append('invalid claim'); continue
        fact=claim.get('fact'); source=claim.get('source')
        if not isinstance(fact,str) or not isinstance(source,str): errors.append('invalid evidence'); continue
        if fact not in case['supported_facts'] or case['supported_facts'].get(fact)!=source: errors.append('unsupported claim')
        seen.add(fact)
    if seen != set(case['supported_facts']): errors.append('missing or added facts')
    if output.get('limitations') != case['required_limitations']: errors.append('missing uncertainty')
    return errors
