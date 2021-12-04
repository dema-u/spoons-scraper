INSERT INTO locations (pub_name, street_address, locality, region, post_code)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;