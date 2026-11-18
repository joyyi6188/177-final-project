#!/usr/bin/env python3
"""Prepare NHTSA recalls for a D3 dashboard. Standard library only.

Usage:
    python3 scripts/prepare_recalls.py data/raw/export.csv --out data/processed

No rows are discarded. The original input is never overwritten.
"""
import argparse
import collections
import csv
import datetime as dt
import json
import pathlib
import re
from urllib.parse import urlparse


def component_group(raw):
    s = raw.strip().upper()
    if s.startswith('SERVICE BRAKES') or s == 'PARKING BRAKE':
        return 'Brakes'
    if s.startswith('ELECTRICAL SYSTEM'):
        return 'Electrical'
    if s == 'STEERING':
        return 'Steering'
    if s == 'AIR BAGS':
        return 'Airbags'
    if s in ('ENGINE', 'ENGINE AND ENGINE COOLING'):
        return 'Engine'
    if s.startswith('FUEL SYSTEM') or s == 'FUEL/PROPULSION SYSTEM':
        return 'Fuel System'
    if s.startswith('VISIBILITY') or s in ('EXTERIOR LIGHTING', 'INTERIOR LIGHTING'):
        return 'Visibility & Lighting'
    if s in ('TIRES', 'WHEELS'):
        return 'Tires & Wheels'
    if s in ('SEATS', 'SEAT BELTS', 'CHILD SEAT'):
        return 'Seats & Restraints'
    if s.startswith('EQUIPMENT'):
        return 'Equipment'
    if s in ('BACK OVER PREVENTION', 'FORWARD COLLISION AVOIDANCE',
             'LANE DEPARTURE', 'ELECTRONIC STABILITY CONTROL',
             'ELECTRONIC STABILITY CONTROL (ESC)', 'TRACTION CONTROL SYSTEM'):
        return 'Driver Assistance & Stability'
    if s in ('SUSPENSION', 'STRUCTURE', 'POWER TRAIN', 'VEHICLE SPEED CONTROL',
             'LATCHES/LOCKS/LINKAGES', 'TRAILER HITCHES',
             'HYBRID PROPULSION SYSTEM', 'COMMUNICATION'):
        return s.title()
    return 'Other / Unknown'


def write_csv(path, data, headers):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)


def prepare(input_path, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    parsed = []
    counts = collections.Counter()
    component_counts = collections.Counter()
    by_year = collections.Counter()
    by_year_component = collections.Counter()
    by_maker_year_comp = collections.Counter()
    by_year_advisory = collections.Counter()
    by_manufacturer = collections.Counter()
    advisory_year_manufacturer = collections.Counter()
    type_manufacturer_year_component = collections.Counter()
    type_manufacturer_year_advisory = collections.Counter()
    quality = collections.Counter()
    seen_ids = set()

    with input_path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [x.strip() for x in reader.fieldnames]
        required = ['Report Received Date', 'NHTSA ID', 'Recall Link', 'Manufacturer',
                    'Subject', 'Component', 'Recall Type', 'Potentially Affected',
                    'Recall Description', 'Consequence Summary', 'Corrective Action',
                    'Do Not Drive Advisory', 'Park Outside Advisory']
        missing_columns = set(required) - set(reader.fieldnames)
        if missing_columns:
            raise ValueError(f'Missing columns: {sorted(missing_columns)}')

        for row in reader:
            r = {k: (v or '').strip() for k, v in row.items()}
            rid = r['NHTSA ID']
            if not rid or rid in seen_ids:
                raise ValueError(f'Missing or duplicate NHTSA ID: {rid!r}')
            seen_ids.add(rid)
            date = dt.datetime.strptime(r['Report Received Date'], '%m/%d/%Y').date()
            affected = int(r['Potentially Affected'].replace(',', ''))
            if affected < 0:
                raise ValueError(f'Negative affected units on {rid}')
            if r['Do Not Drive Advisory'] not in ('Yes', 'No') or r['Park Outside Advisory'] not in ('Yes','No'):
                raise ValueError(f'Unexpected safety advisory on {rid}')
            dnd = r['Do Not Drive Advisory'] == 'Yes'
            park = r['Park Outside Advisory'] == 'Yes'
            advisory = ('Both' if dnd and park else
                        'Do Not Drive only' if dnd else
                        'Park Outside only' if park else 'Neither')
            raw_link = r['Recall Link']
            match = re.search(r'https?://[^)\s]+', raw_link)
            recall_url = match.group(0) if match else ''
            if not recall_url or urlparse(recall_url).netloc.lower() != 'www.nhtsa.gov':
                quality['invalid_recall_url'] += 1
            manufacturer = r['Manufacturer']
            comp = component_group(r['Component'])
            search_text = ' '.join(filter(None, [r['Subject'], r['Recall Description']])).casefold()
            out = {
                'recall_id': rid, 'date': date.isoformat(), 'year': date.year,
                'manufacturer': manufacturer, 'manufacturer_search_key': manufacturer.casefold(),
                'subject': r['Subject'], 'component_raw': r['Component'], 'component_group': comp,
                'recall_type': r['Recall Type'], 'affected_units': affected,
                'model_search_text': search_text,
                'description': r['Recall Description'], 'consequence': r['Consequence Summary'],
                'corrective_action': r['Corrective Action'], 'recall_url': recall_url,
                'do_not_drive': str(dnd).lower(), 'park_outside': str(park).lower(),
                'advisory_group': advisory,
            }
            parsed.append(out)
            counts['rows'] += 1
            component_counts[comp] += 1
            by_year[date.year] += 1
            by_year_component[(date.year, comp)] += 1
            by_maker_year_comp[(manufacturer, date.year, comp)] += 1
            by_year_advisory[(date.year, advisory)] += 1
            by_manufacturer[manufacturer] += 1
            advisory_year_manufacturer[(manufacturer, date.year, advisory)] += 1
            type_manufacturer_year_component[(r['Recall Type'], manufacturer, date.year, comp)] += 1
            type_manufacturer_year_advisory[(r['Recall Type'], manufacturer, date.year, advisory)] += 1
            quality['description_missing'] += not bool(r['Recall Description'])
            quality['consequence_missing'] += not bool(r['Consequence Summary'])
            quality['corrective_action_missing'] += not bool(r['Corrective Action'])
            quality['both_advisories'] += dnd and park
            quality['do_not_drive'] += dnd
            quality['park_outside'] += park
            quality['zero_affected'] += affected == 0
            quality['completion_missing'] += not bool(r['Completion Rate % (Blank - Not Reported)'])

    headers = list(parsed[0])
    write_csv(output_dir/'recalls_clean.csv', parsed, headers)
    write_csv(output_dir/'annual_totals.csv',
              [{'year': y, 'recall_count': n} for y, n in sorted(by_year.items())],
              ['year', 'recall_count'])
    write_csv(output_dir/'year_component_counts.csv',
              [{'year': y, 'component_group': c, 'recall_count': n}
               for (y,c),n in sorted(by_year_component.items())],
              ['year', 'component_group', 'recall_count'])
    write_csv(output_dir/'manufacturer_year_component_counts.csv',
              [{'manufacturer':m,'year':y,'component_group':c,'recall_count':n}
               for (m,y,c),n in sorted(by_maker_year_comp.items())],
              ['manufacturer','year','component_group','recall_count'])
    write_csv(output_dir/'advisory_year_counts.csv',
              [{'year':y, 'advisory_group':a, 'recall_count':n}
               for (y,a),n in sorted(by_year_advisory.items())],
              ['year','advisory_group','recall_count'])
    write_csv(output_dir/'manufacturer_year_advisory_counts.csv',
              [{'manufacturer':m,'year':y,'advisory_group':a,'recall_count':n}
               for (m,y,a),n in sorted(advisory_year_manufacturer.items())],
              ['manufacturer','year','advisory_group','recall_count'])
    write_csv(output_dir/'manufacturers.csv',
              [{'manufacturer':m,'recall_count':n} for m,n in by_manufacturer.most_common()],
              ['manufacturer','recall_count'])
    write_csv(output_dir/'type_manufacturer_year_component_counts.csv',
              [{'recall_type':t,'manufacturer':m,'year':y,'component_group':c,'recall_count':n}
               for (t,m,y,c),n in sorted(type_manufacturer_year_component.items())],
              ['recall_type','manufacturer','year','component_group','recall_count'])
    write_csv(output_dir/'type_manufacturer_year_advisory_counts.csv',
              [{'recall_type':t,'manufacturer':m,'year':y,'advisory_group':a,'recall_count':n}
               for (t,m,y,a),n in sorted(type_manufacturer_year_advisory.items())],
              ['recall_type','manufacturer','year','advisory_group','recall_count'])
    report = {'input_file':input_path.name, 'recall_records':len(parsed),
              'unique_recall_ids':len(seen_ids),
              'date_min':min(x['date'] for x in parsed),
              'date_max':max(x['date'] for x in parsed),
              'unique_manufacturers':len(by_manufacturer),
              'component_groups':dict(component_counts.most_common()),
              'advisory_groups':{a:sum(v for (y,b),v in by_year_advisory.items() if b==a)
                                 for a in ['Neither','Do Not Drive only','Park Outside only','Both']},
              'quality_checks':dict(quality),
              'rules':{'unit_of_observation':'one NHTSA recall campaign per recall_id',
                       'model_search':'case-insensitive substring in Subject + Recall Description; not a verified vehicle model mapping',
                       'component_group':'explicit convenience mapping; original component_raw retained',
                       'advisories':'four mutually exclusive categories; both retained separately',
                       'manufacturer':'no speculative company merger; exact original names retained',
                       'rows_removed':0}}
    (output_dir/'quality_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input_csv',type=pathlib.Path)
    p.add_argument('--out',type=pathlib.Path,default=pathlib.Path('data/processed'))
    args=p.parse_args()
    prepare(args.input_csv,args.out)
