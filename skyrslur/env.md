# Mikilvægar .env breytur
Hægt er að bæta við environment breytur í .env skráini sem er staðset í instance folderinum, ef það er ekki til þarf bara að búa það til eða keyra appið einu sinni þar sem það býr til .env skrá þegar það er keyrt ef .env er ekki þegar til.

## SECRET_KEY
> SECRET_KEY="eitthvað"

---

## SQLALCHEMY_DATABASE_URI
> SQLALCHEMY_DATABASE_URI="path/to/mysql/database.db"

Þetta setur slóð á db skrá, hægt er að breyta því í t.d. "/some/path/test.db" til að nota annan gagnagrunn til að testa.

---

## CONFIG
> CONFIG="config.DevelopmentConfig"

Hægt er að stilla hvaða config appið notar.

Hérna eru allir valmöguleikarnir.
1. config.DevelopmentConfig
2. config.ProductionConfig
3. config.TestConfig
4. config.Config

Getur skoðað öll configin og þeirra stillingar í config.py

---

