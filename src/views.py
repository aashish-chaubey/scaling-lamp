from src import db

def get_all(model):
    data = model.query.all()
    return data

def get_item(model, idx):
    data = model.query.get(idx)
    return data

def add_item(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()

def get_items_from_index(model, idx, rng):
    data = model.query.offset(idx-1).limit(rng).all()
    return data

def delete_item(model, idx):
    data = model.query.get(idx)
    model.query.filter_by(anime_id=idx).delete()
    commit_changes()
    return data

def delete_items_from_index(model, idx, rng):
    data = get_items_from_index(model, idx, rng)
    model.query.filter(model.anime_id.between(idx, idx+rng)) \
        .delete(synchronize_session='fetch')
    commit_changes()
    return data

def update_item_in_table(model, idx, value):
    status = model.query.filter_by(anime_id=idx).update({
        "title": value
    })
    commit_changes()
    return status

def commit_changes():
    db.session.commit()
