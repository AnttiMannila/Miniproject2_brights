ALTER TABLE himos DROP CONSTRAINT himos_pkey;
ALTER TABLE ilomantsi DROP CONSTRAINT ilomantsi_pkey;
ALTER TABLE kilpisjärvi DROP CONSTRAINT kilpisjärvi_pkey;
ALTER TABLE levi DROP CONSTRAINT levi_pkey;
ALTER TABLE pyhä DROP CONSTRAINT pyhä_pkey;
ALTER TABLE salpausselkä DROP CONSTRAINT salpausselkä_pkey;
ALTER TABLE sveitsi DROP CONSTRAINT sveitsi_pkey;
ALTER TABLE tahko DROP CONSTRAINT tahko_pkey;
ALTER TABLE talma DROP CONSTRAINT talma_pkey;
ALTER TABLE vihti DROP CONSTRAINT vihti_pkey;

DELETE FROM himos
WHERE id NOT IN (
    SELECT MIN(id)
    FROM himos
    GROUP BY date
);

DELETE FROM ilomantsi
WHERE id NOT IN (
    SELECT MIN(id)
    FROM ilomantsi
    GROUP BY date
);

DELETE FROM kilpisjärvi
WHERE id NOT IN (
    SELECT MIN(id)
    FROM kilpisjärvi
    GROUP BY date
);

DELETE FROM levi
WHERE id NOT IN (
    SELECT MIN(id)
    FROM levi
    GROUP BY date
);

DELETE FROM pyhä
WHERE id NOT IN (
    SELECT MIN(id)
    FROM pyhä
    GROUP BY date
);

DELETE FROM salpausselkä
WHERE id NOT IN (
    SELECT MIN(id)
    FROM salpausselkä
    GROUP BY date
);

DELETE FROM sveitsi
WHERE id NOT IN (
    SELECT MIN(id)
    FROM sveitsi
    GROUP BY date
);

DELETE FROM tahko
WHERE id NOT IN (
    SELECT MIN(id)
    FROM tahko
    GROUP BY date
);

DELETE FROM talma
WHERE id NOT IN (
    SELECT MIN(id)
    FROM talma
    GROUP BY date
);

DELETE FROM vihti
WHERE id NOT IN (
    SELECT MIN(id)
    FROM vihti
    GROUP BY date
);

ALTER TABLE himos ADD CONSTRAINT pk_date PRIMARY KEY (date);
ALTER TABLE ilomantsi ADD CONSTRAINT pk_date PRIMARY KEY (date);
ALTER TABLE kilpisjärvi ADD CONSTRAINT pk_date PRIMARY KEY (date);
ALTER TABLE levi ADD CONSTRAINT pk_date PRIMARY KEY (date);
ALTER TABLE pyhä ADD CONSTRAINT pk_date PRIMARY KEY (date);
ALTER TABLE salpausselkä ADD CONSTRAINT pk_date PRIMARY KEY (date);
ALTER TABLE sveitsi ADD CONSTRAINT pk_date PRIMARY KEY (date);
ALTER TABLE tahko ADD CONSTRAINT pk_date PRIMARY KEY (date);
ALTER TABLE talma ADD CONSTRAINT pk_date PRIMARY KEY (date);
ALTER TABLE vihti ADD CONSTRAINT pk_date PRIMARY KEY (date);

SELECT * FROM himos;
SELECT * FROM ilomantsi;
SELECT * FROM kilpisjärvi;
SELECT * FROM levi;
SELECT * FROM pyhä;
SELECT * FROM salpausselkä;
SELECT * FROM sveitsi;
SELECT * FROM tahko;
SELECT * FROM talma;
SELECT * FROM vihti;

SELECT *
FROM himos
FULL JOIN ilomantsi USING (date)
FULL JOIN kilpisjärvi USING (date)
FULL JOIN levi USING (date)
FULL JOIN pyhä USING (date)
FULL JOIN salpausselkä USING (date)
FULL JOIN sveitsi USING (date)
FULL JOIN tahko USING (date)
FULL JOIN talma USING (date)
FULL JOIN vihti USING (date)
ORDER BY date;
