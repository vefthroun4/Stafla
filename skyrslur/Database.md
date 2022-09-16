# Database
Til að fá Gagnagrunnin til að virka þarf fyrst að byggja gagnagrunnin.

1. keyra skipunina "flask shell" í Bash
2. keyra skipunina í shellinu "db.create_all()"

þetta smíður gagnagrunn skráina í instance folderinn.

# Algengar skipanir

### db.session.add(Model Object)
> db.session.add(User(email="example@example.com", password_hash="somecomplicatedhash"))

Bætir við objectinu í session

---

### db.session.commit()

Bætir objectinum sem eru í session yfir í gagnagruninn

---

# Models

### Model.query.all()

> User.query.all()

Skilar öllum entries af einhverju Model, t.d. User.query.all() skilar öllum notendum sem eru skráðir í gagnagruninum.

---

### Model.query.filter_by(attribute="value")

> User.query.filter_by(email="example@example.com")

Skilar öllum notendum sem hafa emailið "example@example.com"


