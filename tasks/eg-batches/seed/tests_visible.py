from sync import db, upload

upload.upload_all(db.connect([(f"SKU{i:03d}", i) for i in range(6)]), size=3)
assert [len(b) for b in upload.SENT] == [3, 3], upload.SENT
print("ok")
